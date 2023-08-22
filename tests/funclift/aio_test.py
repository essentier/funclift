# https://docs.python.org/3/library/asyncio-task.html

import asyncio
from funclift.types.aio import AIO
from funclift.fp.monad_runner import run_monads
from funclift.fp.curry import curry
import time
import pytest
import logging

log = logging.getLogger(__name__)


def add_5(n: int) -> int:
    return n + 5


@curry
def sum(a: int, b: int) -> int:
    return a + b


def add_5_aio(n: int) -> AIO[int]:
    return AIO.succeed(n + 5)


@pytest.mark.asyncio
async def test_aio_functor():
    aio = AIO.succeed(10)
    aio2 = aio.fmap(add_5)
    task = aio2.unsafe_run()
    result = await task
    assert result == 15


@pytest.mark.asyncio
async def test_aio_applicative():
    aio5 = AIO.succeed(5)
    aio2 = AIO.succeed(2)

    sum_aio = AIO.succeed(sum)
    aio = sum_aio.ap(aio5).ap(aio2)
    task = aio.unsafe_run()
    result = await task
    assert result == 7


@pytest.mark.asyncio
async def test_aio_monad():
    aio = AIO.succeed(10)
    aio2 = aio.flatmap(add_5_aio)
    task = aio2.unsafe_run()
    result = await task
    assert result == 15


def create_program_monads():
    num1 = yield AIO.succeed(10)
    num2 = yield add_5_aio(num1)
    return AIO.succeed(num2)


@pytest.mark.asyncio
async def test_aio_monad_do_notation():
    monads = create_program_monads()
    program = run_monads(monads)
    task = program.unsafe_run()
    result = await task
    assert result == 15
