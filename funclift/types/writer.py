from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Tuple, TypeVar, cast
from funclift.monoid import Monoid
import logging

log = logging.getLogger(__name__)

Mnd = Monoid | int | list
W = TypeVar('W', bound=Mnd)
# W = TypeVar('W')
V = TypeVar('V')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')
T = TypeVar('T', bound=Mnd)


@dataclass
class Writer(Generic[W, V]):
    """Writer is a monad."""

    value: V
    written: W

    # @staticmethod
    # def pure(a: E, m: Type[Monoid[T]]) -> Writer[T, E]:
    # def pure(a: E, m: Type[T]) -> Writer[T, E]:
    #   return Writer(a, m.empty())
    #   return Writer(a, cast(T, m.empty()))

    # @staticmethod
    # def pure(a: E) -> Writer[W, E]:
    #     w: W
    #     wt = type(w)
    #     return Writer(a, monoid_empty(wt))
    def pure(self, a: E) -> Writer[W, E]:
        if isinstance(self.written, int):
            return Writer(a, cast(W, 0))
        else:
            return Writer(a, cast(Monoid, self.written).empty())

    @staticmethod
    def pure2(a: E, m: T) -> Writer[T, E]:
        return Writer(a, m)

    def fmap(self, f: Callable[[V], B]) -> Writer[W, B]:
        return Writer(f(self.value), self.written)

    def flatmap(self, f: Callable[[V], Writer[W, B]]) -> Writer[W, B]:
        new_writer = f(self.value)
        new_written = cast(W, self.written + new_writer.written)
        return Writer(new_writer.value, new_written)

    def ap(self: Writer[W, Callable[[C], E]],
           other: Writer[W, C]) -> Writer[W, E]:
        return other.fmap(self.value)


def tell(w: W) -> Writer[W, None]:
    # return IntWriter(None, w)
    return Writer.pure2(None, w)
    # return Writer.pure2(None, w)


def run_writer(writer: Writer[W, V]) -> Tuple[V, W]:
    return writer.value, writer.written


class LogWriter(Writer[list[str], V]):
    @staticmethod
    def pure(a: E) -> LogWriter[E]:
        return LogWriter(a, [])

# class IntWriter(Writer[int, V]):
#     @staticmethod
#     def pure(a: E) -> IntWriter[E]:
#         return IntWriter(a, 0)
