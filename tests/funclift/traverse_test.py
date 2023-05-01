from funclift.types.io import IO
from funclift.traverable import ListTraversable
from funclift.types.option import Nothing, Some, Option
import logging

log = logging.getLogger(__name__)


def bar(num: int) -> Option[str]:
    if num > 4:
        return Nothing()
    else:
        return Some('h' * num)


def test_list1_traverse():
    # because there are numbers greater than 4, the result is Nothing
    nums = [1, 2, 5, 4, 3]
    result: Option[list[str]] = ListTraversable.traverse(nums, bar)
    assert result == Nothing()


def test_list2_traverse():
    # because there are no numbers greater than 4, the result is Some
    nums = [1, 2, 4, 3]
    result: Option[list[str]] = ListTraversable.traverse(nums, bar)
    assert result == Some(['h', 'hh', 'hhhh', 'hhh'])


def foo(num: int) -> IO[str]:
    def bar() -> str:
        log.debug(f'number {num}')
        return 'hi'

    return IO(bar)


def test_nothing_traverse():
    o1 = Nothing()
    io1: IO[Option[str]] = o1.traverse(foo)
    result = io1.unsafe_run()
    assert result == Nothing()


def test_some_traverse():
    o1 = Some(5)
    io1: IO[Option[str]] = o1.traverse(foo)
    result = io1.unsafe_run()
    assert result == Some('hi')
