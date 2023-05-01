from __future__ import annotations
from abc import abstractmethod
from typing import Any, Callable, Protocol, TypeVar
from funclift.applicative import Applicative
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
B = TypeVar('B')
T = TypeVar('T')
F = TypeVar('F')


class MonadBase():
    """MonadBase"""

    # def flatMap(fa: F[A], f: A -> F[B]) -> F[B]:
    @classmethod
    def flatmap(cls, fa: Any, f: Any) -> Any: ...

    # def pure(a: A) -> F[A]:
    @classmethod
    def pure(cls, a: Any) -> Any: ...

    # map can be implemented in terms of flatMap and pure
    @classmethod
    def fmap(cls, fa: Any, f: Any) -> Any:
        return cls.flatmap(fa, lambda a: cls.pure(f(a)))


class Monad(Applicative[F, A], Protocol):
    """Monad"""

    @abstractmethod
    def flatmap(self, f: Callable[[A], Monad[F, B]]) -> Monad[F, B]:
        """_summary_

        Args:
            f (Callable[[A], Monad[F, B]]): _description_

        Returns:
            Monad[F, B]: _description_
        """
        ...

    @staticmethod
    def mempty(a: B) -> Monad[F, B]:
        """_summary_

        Args:
            a (B): _description_

        Returns:
            Monad[F, B]: _description_
        """
        ...
