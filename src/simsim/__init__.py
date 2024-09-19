import pathlib
import pickle
import functools
import logging
import time
import collections


logger = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


_registry = {}


def experiment(path: str):
    def decorator_experiment(func):

        path_ = pathlib.Path(path)
        name = func.__name__
        fp = (path_/name).with_suffix(".pkl")
        _registry[name] = fp 

        @functools.wraps(func)
        def wrapper():
            logger.info(f"Running experiment '{name}'")
            time0 = time.time_ns()
            results = func()
            time_total = time.time_ns() - time0

            path_.mkdir(exist_ok=True)
            with open(fp, "wb") as f:
                pickle.dump(results, f)

            logger.info(f"Experiment '{name}' terminated successfully in {time_total/1.e9} s")
        
        return wrapper
    return decorator_experiment


def presentation(*experiments):
    def decorator_presentation(presentation_func):
        @functools.wraps(presentation_func)
        def wrapper():
            results = []
            for ex in experiments:
                with open(_registry[ex.__name__], "rb") as f:
                    res = pickle.load(f)
                    results.append(res)
            presentation_func(results if len(results) > 1 else results[0])
        
        return wrapper
    return decorator_presentation


def results(ex):
    with open(_registry[ex.__name__], "rb") as f:
        return pickle.load(f)