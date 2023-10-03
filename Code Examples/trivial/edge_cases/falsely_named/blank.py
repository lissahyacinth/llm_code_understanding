import functools
import operator


def doubles(x: int) -> int:
    return x**2


def sum_list(x: list[int]) -> int:
    return functools.reduce(operator.add, (doubles(y) for y in x))
