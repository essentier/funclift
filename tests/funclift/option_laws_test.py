from typing import Any
from funclift.types.option import Some, Nothing, Option
from hypothesis.strategies import integers
from hypothesis import given


def add1(a: int) -> int:
    return a + 1


def add2(a: int) -> int:
    return a + 2


def add1_add2(a: int) -> int:
    return add2(add1(a))


def id(a: Any) -> Any:
    return a


def id_option(a: Option[Any]) -> Option[Any]:
    return a


@given(i=integers())
def test_functor_identity_law_on_some(i):
    some_int = Some(i)
    assert id_option(some_int) == some_int.fmap(id)


@given(i=integers())
def test_functor_composition_law_on_some(i):
    some_int = Some(i)
    assert some_int.fmap(add1).fmap(add2) == some_int.fmap(add1_add2)


def test_functor_composition_law_on_nothing():
    nothing = Nothing()
    assert nothing.fmap(add1).fmap(add2) == nothing.fmap(add1_add2)


def test_functor_identity_law_on_nothing():
    nothing = Nothing()
    assert id_option(nothing) == nothing.fmap(id)
