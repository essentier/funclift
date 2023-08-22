from __future__ import annotations
from typing import Awaitable, Any, Callable, Generic, TypeVar
from dataclasses import dataclass
from funclift.types.option import Nothing, Option, Some
from functools import wraps
import logging
import asyncio

log = logging.getLogger(__name__)

A = TypeVar("A")
B = TypeVar("B")
D = TypeVar("D")
E = TypeVar("E")


@dataclass
class AIO(Generic[A]):
    """AIO provides abstraction for asynchronous IO."""

    awaitable: Awaitable[A]

    @staticmethod
    def group(*aios):
        async def new_awaitable():
            tasks = []
            async with asyncio.TaskGroup() as tg:
                for aio in aios:
                    task = tg.create_task(aio.awaitable)
                    tasks.append(task)

            return [task.result() for task in tasks]

        return AIO(new_awaitable())

    def group(self, *awaitables):
        async def new_awaitable():
            tasks = []
            async with asyncio.TaskGroup() as tg:
                task = tg.create_task(self.awaitable)
                tasks.append(task)
                for awaitable in awaitables:
                    task = tg.create_task(awaitable)
                    tasks.append(task)

            return [task.result() for task in tasks]

        return AIO(new_awaitable())

    # def then(self, b: AIO[B]) -> AIO[tuple[A, B]]:
    #     async def new_awaitable():
    #         a: A = await self.awaitable
    #         b: B = await b.awaitable
    #         return a, b

    #     return AIO(new_awaitable())

    @staticmethod
    def raise_error(or_else: Callable[[], Exception]) -> AIO[Exception]:
        return AIO.pure(or_else())

    @staticmethod
    def from_option(
        option: Option[A], or_else: Callable[[], Exception]
    ) -> AIO[A] | AIO[Exception]:
        """Creates an AIO from an Option.

        Args:
            option (Option[A]): the option from which to create an AIO.
            or_else (Callable[[], Exception]): this function will be invoked
              when the passed in Option is Nothing.

        Returns:
            AIO[A] | AIO[Exception]: _description_
        """
        match option:
            case Some(v):
                return AIO.succeed(v)
            case Nothing():
                return AIO.raise_error(or_else)
            case _:
                return AIO.raise_error(or_else)

    @staticmethod
    def succeed(a: B) -> AIO[B]:
        async def new_awaitable():
            return a

        return AIO(new_awaitable())

    @staticmethod
    def pure(awaitable: Awaitable[A]) -> AIO[A]:
        return AIO(awaitable)

    def then(self, f: Callable[[A], Awaitable[B]]) -> AIO[B]:
        async def new_awaitable():
            a = await self.awaitable
            b = await f(a)
            return b

        return AIO(new_awaitable())

    def fmap(self, f: Callable[[A], B]) -> AIO[B]:
        async def new_awaitable():
            v = await self.awaitable
            return f(v)

        return AIO(new_awaitable())

    def flatmap(self, f: Callable[[A], AIO[B]]) -> AIO[B]:
        async def new_awaitable():
            a: A = await self.awaitable
            fb: AIO[B] = f(a)
            b: B = await fb.awaitable
            return b

        return AIO(new_awaitable())

    def ap(self: AIO[Callable[[D], E]], aio: AIO[D]) -> AIO[E]:
        async def new_awaitable():
            d: D = await aio.awaitable
            f = await self.awaitable
            e = f(d)
            return e

        return AIO(new_awaitable())

    def unsafe_run(self):
        return asyncio.create_task(self.awaitable)


def aio_effect(unsafe_func):
    @wraps(unsafe_func)
    def wrapper(*args, **kwargs) -> AIO[A]:
        def _effect() -> Any:
            return unsafe_func(*args, **kwargs)

        return AIO(_effect)

    return wrapper
