import pathlib
import pickle
import json
import functools
import logging
import time
import inspect


logger = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


_registry = {}


def _load_data(ex):
    path = _registry[ex.__name__]
    match path.suffix:
        case ".pkl":
            with open(path, "rb") as f:
                return pickle.load(f)
        case ".json":
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        case _:
            raise ValueError("unrecognized experiment filetype")
 

def _write_data(ex, results):
    path = _registry[ex.__name__]
    match path.suffix:
        case ".pkl":
            with open(path, "wb") as f:
                return pickle.dump(results, f)
        case ".json":
            with open(path, "w", encoding="utf-8", newline="") as f:
                return json.dump(results, f, ensure_ascii=False,
                                 indent=None, separators=(",", ":"))
        case _:
            raise ValueError("unrecognized experiment filetype")


class SetOnce:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
        self.isset = False

    def __set__(self, obj, value):
        if self.isset:
            raise AttributeError("this attribute may be set only once")
        setattr(obj, self.private_name, value)
        self.isset = True
        obj.logger.info(f"`{self.public_name}` was set to {value}")
    
    def __get__(self, obj, objtype=None):
        attr = getattr(obj, self.private_name)
        if not attr:
            raise AttributeError("attribute {self.name} not set!")
        return attr
    

class ExperimentStatus:

    max_progress = SetOnce()

    def __init__(self, logger, time_start):
        self.logger = logger
        self._progress = None
        self._time0 = time_start

    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, val):
        self._progress = val
        frac = self._progress/self.max_progress
        msg = f"{self._progress}/{self.max_progress} ({round(100*frac)}%)"
        time1 = time.time_ns()
        elapsed = time1-self._time0
        step_time = elapsed/val
        est_remain = step_time*(self.max_progress - val)
        msg += f" - {round(est_remain*1e-9)}s remain"
        self.logger.info(msg)


def experiment(path: str, json=False):
    def decorator_experiment(func):

        path_ = pathlib.Path(path)
        name = func.__name__
        fp = path_/name
        fp = fp.with_suffix(".json") if json else fp.with_suffix(".pkl")
        _registry[name] = fp

        @functools.wraps(func)
        def wrapper():
            logger.info(f"Running experiment '{name}'")
            time0 = time.time_ns()
            fargs = inspect.getfullargspec(func)[0]
            match len(fargs):
                case 0:
                    results = func()
                case 1:
                    results = func(ExperimentStatus(logger, time0))
                case _:
                    raise ValueError("invalid number of arguments for experiment function")
            time_total = time.time_ns() - time0
            logger.info(f"Experiment '{name}' terminated successfully in {time_total/1.e9} s")

            if results is None:
                logger.info(f"No results were returned")
            else:
                path_.mkdir(parents=True, exist_ok=True)
                _write_data(func, results)
                logger.info(f"Results were saved to \"{fp}\"")
        
        return wrapper
    return decorator_experiment


def presentation(*experiments):
    def decorator_presentation(presentation_func):
        @functools.wraps(presentation_func)
        def wrapper():
            results = []
            for ex in experiments:
                results.append(_load_data(ex))
            presentation_func(results if len(results) > 1 else results[0])
        
        return wrapper
    return decorator_presentation


def results(ex):
    # TODO: This function should not be called before the presentation 
    # function is called, after which this function should be called
    # after every additional presentation function call.
    try:
        return _load_data(ex)
    except FileNotFoundError:
        logger.warning(
            f"Experiment {ex.__name__} has not yet been run. "+
            "To access the results, the experiment must be run and the "+
            "interpreter restarted.")