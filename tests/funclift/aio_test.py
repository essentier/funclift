# https://docs.python.org/3/library/asyncio-task.html

import asyncio
from funclift.fp.monad_runner import monads_runner
from funclift.types.aio import AIO
import time
import pytest
import logging

log = logging.getLogger(__name__)


@monads_runner
def program5():
    a = yield AIO.pure(5)
    log.debug(f'a {a}')
    b = yield AIO.pure(2)
    log.debug(f'b {b}')
    yield a + b


# def test_example5():
#     result = program5().unsafe_run()
#     log.debug(f'result {result}')


async def say_after(delay, what):
    await asyncio.sleep(delay)
    log.debug(what)


@pytest.mark.asyncio
async def test_await_in_sequence():
    log.debug(f'started at {time.strftime("%X")}')

    await say_after(1, 'hello')
    await say_after(2, 'world')

    log.debug(f'finished at {time.strftime("%X")}')


@pytest.mark.asyncio
async def test_await_concurrently():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    log.debug(f'started at {time.strftime("%X")}')

    await task1
    await task2

    log.debug(f'finished at {time.strftime("%X")}')
