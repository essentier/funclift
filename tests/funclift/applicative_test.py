from typing import Callable, TypeVar
from funclift.types.option import Nothing, Option, Some
from funclift.fp.curry import curry
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
B = TypeVar('B')


def func1(n: int) -> str:
    return 'h' * n


num1 = Some(5)
num2 = Some(3)
nothing = Nothing()


@curry
def func2(n1: int, n2: int) -> str:
    return 'h' * (n1 + n2)


@curry
def add3(a: int, b: int, c: int) -> int:
    return a + b + c


def test_example1():
    # result1: Option[str] = Some.pure(func1).ap(num1)
    # some_func = Some[Callable[[int], str]].pure(func1)
    some_func: Some[Callable[[int], str]] = Some.pure(func1)
    # some_func = Some.pure(func1)
    num1: Option[int] = Some(5)
    result1 = some_func.ap(num1)
    # result1 = Some.pure(func1).ap(num1)
    assert result1 == Some('hhhhh')


def test_example2():
    # some_func = Some[Callable[[A], B]].pure(func2)
    # some_func: Some[Callable[[int], Callable[[int], str]]] =
    #    Some[Callable[[A], B]].pure(func2)
    some_func: Some[Callable[[int], Callable[[int], str]]] = Some.pure(func2)
    num1: Option[int] = Some(5)
    partial_func = some_func.ap(num1)
    result1 = partial_func.ap(num2)
    # result1 = some_func.ap(num1).ap(num2)
    log.debug(f'result1 {result1}')


def test_example3():
    some_func: Some[Callable[[int], Callable[[int], str]]] = Some.pure(func2)
    result1 = some_func.ap(num1).ap(num2)
    # result2: Option[str] =
    #  Some[Callable[[A], B]].pure(func2).ap(num1).ap(num2)
    # result2 = Some.pure(func2).ap(num1).ap(num2)
    assert result1 == Some('hhhhhhhh')

    result3 = some_func.ap(Nothing()).ap(num2)
    assert result3 == Nothing()

    # result4: Option[str] = Nothing().ap(num1).ap(num2)
    nothing_func = Nothing()
    result4 = nothing_func.ap(num1).ap(num2)
    assert result4 == Nothing()


def test_example4():
    # we lose some type info here because 'curry' is not yet typed.
    result1 = num1.fmap(func2).ap(num2)
    assert result1 == Some('hhhhhhhh')

    result2 = nothing.fmap(func2).ap(num2)
    assert result2 == nothing

    result3 = num1.fmap(func2).ap(nothing)
    assert result3 == nothing
