import pathlib
import pickle
import functools
import logging
import time


logger = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


def _get_path(path: str, name: str):
    path_ = pathlib.Path(path)
    fname = f"{name}.pkl"
    return path_.joinpath(fname)


def experiment(path: str):
    def decorator_experiment(func):
        @functools.wraps(func)
        def wrapper():
            name = func.__name__
            logger.info(f"Running experiment '{name}'")
            time0 = time.time_ns()
            results = func()
            time_total = time.time_ns() - time0

            path_ = pathlib.Path(path)
            path_.mkdir(exist_ok=True)

            with open(_get_path(path, name), "wb") as f:
                pickle.dump(results, f)

            logger.info(f"Experiment '{name}' terminated successfully in {time_total/1.e9} s")
        
        return wrapper
    return decorator_experiment


def presentation(path: str, name: str | list[str]):
    def decorator_presentation(presentation_func):
        @functools.wraps(presentation_func)
        def wrapper():
            results = list()
            if isinstance(name, str):
                name_list = [name]
            else:
                name_list = name
            for nm in name_list:
                with open(_get_path(path, nm), "rb") as f:
                    results.append(pickle.load(f))
            presentation_func(results if len(results) > 1 else results[0])
        
        return wrapper
    return decorator_presentation