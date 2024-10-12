import pathlib
import pickle
import json
import functools
import logging
import time


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
            results = func()
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