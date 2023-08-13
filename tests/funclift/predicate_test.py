
from funclift.types.predicate import Predicate


def is_even(n: int) -> bool:
    return n % 2 == 0

def str_to_int(text: str) -> int:
    return int(text)

def test_predicate():
    even_p = Predicate(is_even)
    even_str_p = even_p.cmap(str_to_int)
    assert even_str_p('6') == True
    assert even_str_p('3') == False