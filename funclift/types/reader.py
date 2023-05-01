from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from funclift.monoid import Monoid
import logging

log = logging.getLogger(__name__)

W = TypeVar('W', bound=Monoid)
V = TypeVar('V')
A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')
S2 = TypeVar('S2')


@dataclass
class Reader(Generic[R, A]):
    """Reader is a monad."""

    action: Callable[[R], A]
    # data Reader cfg a = Reader { runReader :: cfg -> a }

    @staticmethod
    def pure(b: B) -> Reader[R, B]:
        def new_action(r: R) -> B:
            return b
        return Reader(new_action)

    # @staticmethod
    # def asks(f: Callable[[R], B]) -> Reader[R, B]:
    #     return Reader(f)

    @staticmethod
    def ask() -> Reader[R, R]:
        def new_action(r: R) -> R:
            return r
        return Reader(new_action)

    def fmap(self, f: Callable[[A], B]) -> Reader[R, B]:
        def new_action(r: R) -> B:
            a = self.action(r)
            return f(a)
        return Reader(new_action)

    # def ap(self: Reader[Callable[[C], E]], other: Reader[C]) -> Reader[E]:
    #     return other.fmap(self.action)

    # def ap(self: Some[Callable[[C], E]], other: Option[C]) -> Option[E]:
    #     return other.fmap(self.value)

    def flatmap(self: Reader[R, A],
                f: Callable[[A], Reader[R, B]]) -> Reader[R, B]:
        def new_action(r: R) -> B:
            a = self.action(r)
            rb = f(a)
            return rb.action(r)
        return Reader(new_action)

    @staticmethod
    def run_reader(reader: Reader[R, A], env: R) -> A:
        return reader.action(env)
