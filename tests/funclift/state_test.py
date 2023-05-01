from funclift.fp.monad_runner import run_monads
from funclift.types.state import State


def foo() -> State[str, int]:
    x = yield State.read()
    _ = yield State.write(x + 1)
    y = yield State.read()
    return 'h' * (y + 3)


def test_state_monad():
    monads = foo()
    s = run_monads(monads)
    result = s.run(0)
    assert result == ('hhhh', 1)
