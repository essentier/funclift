from funclift.fp.curry import curry
from funclift.types.validated import Invalid, Valid

num1 = Valid(5)
num2 = Valid(3)
error1 = Invalid(['error1'])
error2 = Invalid(['error2'])


@curry
def func2(n1: int, n2: int) -> str:
    return 'h' * (n1 + n2)


@curry
def add3(a: int, b: int, c: int) -> int:
    return a + b + c


def test_example4():
    # we lose some type info here because 'curry' is not yet typed.
    result1 = num1.fmap(func2).ap(num2)
    assert result1 == Valid('hhhhhhhh')

    result2 = error1.fmap(func2).ap(error2)
    assert result2 == Invalid(['error1', 'error2'])

    result3 = num1.fmap(add3).ap(error1).ap(error2)
    assert result3 == Invalid(['error1', 'error2'])

    result4 = Valid.pure(add3).ap(error1).ap(num1).ap(error2)
    assert result4 == Invalid(['error1', 'error2'])
