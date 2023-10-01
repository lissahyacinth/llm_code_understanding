import operator
import functools


def doubles(x: int) -> int:
    return x * 2


def triples(x: int) -> int:
    return x * 3


def sum_list(x: list[int]) -> int:
    applied_function = triples
    return functools.reduce(operator.add, (eval(f"applied_function({y})") for y in x))
