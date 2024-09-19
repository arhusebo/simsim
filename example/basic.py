import math
from typing import TypedDict
import simsim


@simsim.experiment(path="./experiments/")
def fibonacci() -> list[float]:
    x = [0, 1]
    for i in range(20):
        x.append(x[i]+x[i+1])
    return x


@simsim.experiment(path="./experiments/")
def primes() -> list[float]:
    prm = []
    for x in range(2, 1000):
        if all(x%y != 0 for y in range(2, int(math.sqrt(x))+1)):
            prm.append(x)
    return prm


class Rectangle(TypedDict):
    width: float
    height: float
    area: float


@simsim.experiment(path="./experiments/", json=True)
def rectangle_area() -> dict:
    rectangles: list[Rectangle] = []
    for width in range(2, 11, 2):
        for height in range(2, 11, 2):
            rectangles.append({
                "width": width,
                "height": height,
                "area": width*height,
            })
    return rectangles


@simsim.presentation(fibonacci)
def present_fibonacci(x):
    print("Fibonacci sequence: "+", ".join(str(val) for val in x))


@simsim.presentation(fibonacci, primes)
def present_multiple(results):
    print("Fibonacci sequence: "+", ".join(str(val) for val in results[0]))
    print("Prime sequence: "+", ".join(str(val) for val in results[1]))


def alt_presentation(fib_results: list[float] = simsim.results(fibonacci),
                     prm_results: list[float] = simsim.results(primes)):
    print("Alternative presentation of the fibonacci sequence: "+
          ", ".join(str(val) for val in fib_results))
    print("Alternative presentation of the prime sequence: "+
          ", ".join(str(val) for val in prm_results))


def present_rectangle_areas(
        rectangles: list[Rectangle] = simsim.results(rectangle_area)):
    for rectangle in rectangles:
        print(f"Rectangle with width {rectangle['width']} "+
              f"and height {rectangle['height']} "+
              f"has an area of {rectangle['area']}")