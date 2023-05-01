from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, cast
from dataclasses import dataclass
from funclift.types.option import Nothing, Option, Some
from functools import wraps
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')


@dataclass
class AIO(Generic[A]):
    """AIO provides abstraction for asynchronous IO."""

    unsafe_run: Callable[[], A]

    @staticmethod
    def raise_error(or_else: Callable[[], Exception]) -> AIO[Exception]:
        return AIO.pure(or_else())

    @staticmethod
    def from_option(option: Option[A],
                    or_else: Callable[[], Exception]) -> AIO[A] | AIO[Exception]:
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
                return AIO.pure(v)
            case Nothing():
                return AIO.raise_error(or_else)
            case _:
                return AIO.raise_error(or_else)

    @staticmethod
    def pure(a: B) -> AIO[B]:
        return AIO(lambda: a)

    def fmap(self, f: Callable[[A], B]) -> AIO[B]:
        return AIO(lambda: f(self.unsafe_run()))

    def flatmap(self, f: Callable[[A], AIO[B]]) -> AIO[B]:
        # Should not do this because it executes self.unsafe_run() right away.
        # return f(self.unsafe_run())
        def foo():
            a: A = self.unsafe_run()
            fa: AIO[B] = f(a)
            return fa.unsafe_run()
        return AIO(foo)

    def ap(self, a: AIO[D]) -> AIO[E]:
        return a.fmap(lambda x: cast(Callable[[D], E], self.unsafe_run())(x))


def aio_effect(unsafe_func):
    @wraps(unsafe_func)
    def wrapper(*args, **kwargs) -> AIO[A]:
        def _effect() -> Any:
            return unsafe_func(*args, **kwargs)

        return AIO(_effect)

    return wrapper
