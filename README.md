# simsim
## "Simple Simulation"

Provides a very simple framework for running isolated experiments and presenting the results.

Experiments are defined in nullary functions decorated by the `@simsim.experiment` decorator and returns the experiment results. The directory in where to store the returned results (serialized using `pickle` or possibly in json-format) is specified as a decorator argument. The results filename corresponds to its respective experiment function name.

Results may be presented using functions decorated by the `@simsim.presentation` decorator. Experiment functions are provided as a decorator argument and their results may be accessed through the first presentation function parameter.

## Installation
Install using pip:
```
python -m pip install git+https://github.com/arhusebo/simsim.git
```

## Usage
Please refer to the `/example` directory for the function declarations.

An experiment can be run by calling the function in which it is defined, e.g. in _command_:
```
python -c "from example.basic import *; fibonacci()"
```

A neat way of running an experiment is through interactive mode:
```
python -i
...
>>> from example.basic import *
>>> fibonacci()
Running experiment 'fibonacci'
Experiment 'fibonacci' terminated successfully
>>> present_fibonacci()
Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946
```

However, `IPython` is highly recommended for developing and debugging as it provides convenient features like autoreloading and removing the need to type function parentheses:
```
ipython
...
In [1]: %load_ext autoreload

In [2]: %autoreload 2

In [3] %autocall 2

In [4] import example.basic as ex

In [5] ex.fibonacci
-------> ex.fibonacci()
Running experiment 'fibonacci'
Experiment 'fibonacci' terminated successfully

In [6] ex.present_fibonacci
-------> ex.present_fibonacci()
Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946
```
Note that _autoreload_ does not work properly with wildcard (*) imports, hence the experiments module is imported with an arbitrary identifier, e.g. `ex`.