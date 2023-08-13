
from typing import Any
from funclift.types.either import Right, Either, Left

def add1(n: int) -> int:
    return n + 1


def enhance_error_message(error: str) -> str:
    return 'enhanced ' + error


def test_right():
    r1: Either[Any, int] = Right(5)
    r2 = r1.fmap(add1)
    assert r2 == Right(6)

    r3 = r1.bimap(enhance_error_message, add1)
    assert r3 == Right(6)
    

def test_left():
    l1: Either[str, Any] = Left('error message')
    l2 = l1.fmap(add1)
    assert l2 == l1

    l3 = l1.bimap(enhance_error_message, add1)
    assert l3 == Left('enhanced error message')
