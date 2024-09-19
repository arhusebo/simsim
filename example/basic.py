import math
import simsim


@simsim.experiment(path="./experiments/")
def fibonacci() -> list[float]:
    x = [0, 1]
    for i in range(20):
        x.append(x[i]+x[i+1])
    return x


@simsim.experiment(path="./experiments/")
def primes():
    prm = []
    for x in range(2, 1000):
        if all(x%y != 0 for y in range(2, int(math.sqrt(x))+1)):
            prm.append(x)
    return prm


@simsim.presentation(fibonacci)
def present_fibonacci(x):
    print("Fibonacci sequence: "+", ".join(str(val) for val in x))


@simsim.presentation(fibonacci, primes)
def present_multiple(results):
    print("Fibonacci sequence: "+", ".join(str(val) for val in results[0]))
    print("Prime sequence: "+", ".join(str(val) for val in results[1]))