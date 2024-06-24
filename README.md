# simsim
## "Simple Simulation"

Provides a very simple framework for running isolated experiments and presenting the results.

Experiments are defined in nullary functions decorated by the `@simsim.experiment` decorator and returns the experiment results. The results are saved to the path specified in the decorator, under the function's name.

The results may be presented using functions decorated by the `@simsim.presentation` decorator, which must be provided the name(s) of the experiment function(s).

## Installation
Install using pip:
```
python -m pip install git+https://github.com/arhusebo/simsim.git
```

## Usage
Please refer to the `/example` directory for the function declarations.

The simplest way of running an experiment is through Python interactive mode:
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

In [3] autocall 3

In [4] from example.basic import *

In [5] fibonacci
-------> fibonacci()
Running experiment 'fibonacci'
Experiment 'fibonacci' terminated successfully

In [6] present_fibonacci
-------> present_fibonacci()
Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946