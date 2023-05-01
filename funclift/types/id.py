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
C = TypeVar('C')
E = TypeVar('E')


@dataclass
class Id(Generic[A]):
    """Id is a [`Monad`][funclift.monad.Monad]."""
    a: A

    def fmap(self, f: Callable[[A], B]) -> Id[B]:
        return Id(f(self.a))

    @staticmethod
    def pure(b: B) -> Id[B]:
        return Id(b)

    def ap(self: Id[Callable[[C], E]], other: Id[C]) -> Id[E]:
        # return Id(self.a(other.a))
        return other.fmap(self.a)

    def flatmap(self, f: Callable[[A], Id[B]]) -> Id[B]:
        return f(self.a)
