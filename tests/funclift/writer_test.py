from funclift.fp.monad_runner import run_monads
from funclift.types.writer import LogWriter, Writer, tell
import logging

log = logging.getLogger(__name__)


def test_str_writer():
    w1 = Writer[str, int].pure2(5, '')
    assert w1 == Writer(5, '')

    def double(n: int) -> Writer[str, int]:
        return Writer(n * 2, f'double {n}')

    w2 = w1.flatmap(double).flatmap(double)
    assert w2 == Writer(20, 'double 5double 10')


def test_list_str_writer():
    w1: Writer[list[str], int] = Writer[list[str], int].pure2(5, [])
    assert w1 == Writer(5, [])

    def double(n: int) -> Writer[list[str], int]:
        return Writer(n * 2, [f'double {n}'])

    w2 = w1.flatmap(double).flatmap(double)
    assert w2 == Writer(20, ['double 5', 'double 10'])


def test_writer():
    def get_monads():
        a = yield Writer(5, ['a'])
        _ = yield Writer(None, ['No value. Just log.'])
        _ = yield tell(['Another log'])
        b = yield Writer(6, ['b'])
        # cannot just yield a + b because Writer.pure is not pure.
        # yield a + b
        yield Writer(a + b, ['c'])  # bug: 'c' shows up twice in the writer.

    monads = get_monads()
    result = run_monads(monads)
    log.debug(f'result {result}')


def test_logwriter():
    def get_monads():
        a = yield LogWriter(5, ['a'])
        _ = yield LogWriter(None, ['No value. Just log.'])
        # x = yield Some(5)
        b = yield LogWriter(6, ['b'])
        yield a + b

    monads = get_monads()
    result = run_monads(monads)
    log.debug(f'result {result}')
