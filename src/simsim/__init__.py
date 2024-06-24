import os
import sys
import pickle
import functools
import logging
import importlib


autoreload = False

logger = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


def _do_autoreload(func):
    global autoreload
    if autoreload:
        mod = sys.modules[func.__module__]
        importlib.reload(mod)
        logger.debug(f"Module {func.__module__} was reloaded")
        newfunc = getattr(mod, func.__name__)
        return newfunc
    return func


def _get_path(path: str, name: str):
    fname = f"{name}.pkl"
    return os.path.join(path, fname)


def experiment(path: str):
    def decorator_experiment(func):
        @functools.wraps(func)
        def wrapper():
            #func1 = _do_autoreload(func)
            name = func.__name__
            logger.info(f"Running experiment '{name}'")
            results = func()

            if not os.path.exists(path):
                os.mkdir(path)

            with open(_get_path(path, name), "wb") as f:
                pickle.dump(results, f)

            logger.info(f"Experiment '{name}' terminated successfully")
        
        return wrapper
    return decorator_experiment


def presentation(path: str, name: str | list[str]):
    def decorator_presentation(presentation_func):
        @functools.wraps(presentation_func)
        def wrapper():
            # load results
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