from funclift.fp.monad_runner import run_monads
from funclift.types.option import Nothing, Option, Some
import logging

log = logging.getLogger(__name__)

# def add(a: int) -> Option[int]:
# def add(a: int, b: int) -> int:
#     return a + b


def option_add(a: Option[int], b: Option[int]) -> Option[int]:
    return a.flatmap(lambda x: b.flatmap(lambda y: Some(x + y)))


def option_add2(a: Option[int], b: Option[int]) -> Option[int]:
    def get_monads():
        x = yield a
        y = yield b
        yield x + y

    monads = get_monads()
    result = run_monads(monads)
    return result


def test_option_add2():
    some5 = Some(5)
    some2 = Some(2)
    nothing = Nothing()

    result1 = option_add2(some5, some2)
    log.debug(f'result1 {result1}')

    result2 = option_add2(some5, nothing)
    log.debug(f'result2 {result2}')

    result3 = option_add2(nothing, some2)
    log.debug(f'result3 {result3}')


def test_option_add():
    some5 = Some(5)
    some2 = Some(2)
    nothing = Nothing()

    result1 = option_add(some5, some2)
    log.debug(f'result1 {result1}')

    result2 = option_add(some5, nothing)
    log.debug(f'result2 {result2}')

    result3 = option_add(nothing, some2)
    log.debug(f'result3 {result3}')


# def test_option_add():
