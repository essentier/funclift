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
# class IO(Monad[A]):
class IO(Generic[A]):
    """_summary_

    Args:
        Generic (_type_): _description_

    Returns:
        _type_: _description_
    """

    unsafe_run: Callable[[], A]

    @staticmethod
    def raise_error(or_else: Callable[[], Exception]) -> IO[Exception]:
        return IO.pure(or_else())

    # def handle_error(self): ...

    @staticmethod
    def from_option(option: Option[A],
                    or_else: Callable[[], Exception]) -> IO[A] | IO[Exception]:
        match option:
            case Some(v):
                return IO.pure(v)
            case Nothing():
                return IO.raise_error(or_else)
            case _:
                return IO.raise_error(or_else)

        # value = option.get()
        # if (value == None):
        #     return IO.raise_error(or_else)
        # else:
        #     return IO.pure(value)

    @staticmethod
    def pure(a: B) -> IO[B]:
        return IO(lambda: a)
        # if callable(a):
        #     return IO(a)
        # else:
        #     return IO(lambda: a)

    def fmap(self, f: Callable[[A], B]) -> IO[B]:
        return IO(lambda: f(self.unsafe_run()))

    def flatmap(self, f: Callable[[A], IO[B]]) -> IO[B]:
        # Should not do this because it executes self.unsafe_run() right away.
        # return f(self.unsafe_run())
        def foo():
            a: A = self.unsafe_run()
            fa: IO[B] = f(a)
            return fa.unsafe_run()
        return IO(foo)

    def ap(self, a: IO[D]) -> IO[E]:
        return a.fmap(lambda x: cast(Callable[[D], E], self.unsafe_run())(x))

    # @staticmethod
    # def create(f: Callable[[], A]) -> IO[A]:
    #     return IO(f)


def io_effect(unsafe_func):
    @wraps(unsafe_func)
    def wrapper(*args, **kwargs) -> IO[A]:
        def _effect() -> Any:
            return unsafe_func(*args, **kwargs)

        return IO(_effect)

    return wrapper
