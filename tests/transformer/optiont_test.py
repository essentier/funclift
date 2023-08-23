from __future__ import annotations

from funclift.fp.monad_runner import run_monads
from funclift.types.option import Nothing, Some
from funclift.types.optiont import OptionT
from funclift.types.io import IO


def check_username(name_str: str) -> OptionT[IO, str]:
    name = yield OptionT.lift(IO.pure(name_str))
    if len(name) > 5:
        return Some("valid")
    else:
        return Nothing()


def test_optiont_some():
    monads = check_username("abcdef")
    result = run_monads(monads)
    result1 = result.run().unsafe_run()
    assert result1 == Some("valid")


def test_optiont_nothing():
    monads = check_username("abc")
    result = run_monads(monads)
    result1 = result.run().unsafe_run()
    assert result1 == Nothing()
