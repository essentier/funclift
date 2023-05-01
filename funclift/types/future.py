
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from funclift.monad import MonadBase
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')


@dataclass
class Future(Generic[A]):
    """Future"""

    value: A | None

    def pure(self, a: A) -> Future[A]:
        return Future(a)

    def fmap(self, f: Callable[[A], B]) -> Future[B]:
        return FutureMonad.fmap(self, f)

    def flatmap(self, f: Callable[[A], Future[B]]) -> Future[B]:
        return FutureMonad.flatmap(self, f)


class FutureFunctor():
    @staticmethod
    def fmap(fa: Future[A], f: Callable[[A], B]) -> Future[B]:
        if fa.value is None:
            return Future(None)
        else:
            return Future(f(fa.value))
            # return Future(f(cast(A, fa.value)))


class FutureMonad(MonadBase):
    @classmethod
    def flatmap(cls, fa: Future[A], f: Callable[[A], Future[B]]) -> Future[B]:
        if fa.value is None:
            return Future(None)
        else:
            result = f(fa.value)
            # result = f(cast(A, fa.value))
            return result

    @classmethod
    def pure(cls, a: A) -> Future[A]:
        return Future(a)
