
from funclift.types.option import Option, Some, Nothing
from funclift.types.star import Star


def ten_mod_by(n: int) -> Option[int]:
    if n == 0:
        return Nothing()
    
    return Some(10 % n)


def str_to_int(text: str) -> int:
    return int(text)


def is_even(n: int) -> bool:
    return n % 2 == 0


def test_star():
    star1 = Star(ten_mod_by)
    assert star1.run(3) == Some(1)
    assert star1.run(0) == Nothing()

    star2 = star1.dimap(str_to_int, is_even)
    assert star2.run('3') == Some(False)
    assert star2.run('6') == Some(True)
    assert star2.run('0') == Nothing()
