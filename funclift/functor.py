from __future__ import annotations
from typing import Callable, Generic, Protocol, TypeVar
import logging

log = logging.getLogger(__name__)

A = TypeVar("A", covariant=True)
B = TypeVar("B")
F = TypeVar("F")
G = TypeVar("G")


class Functor(Generic[F, A], Protocol):
    """Functor"""

    def fmap(self, f: Callable[[A], B]) -> Functor[F, B]:
        """
        fmap takes a function of type A -> B and produces a value of type F[B].

        Args:
            f (Callable[[A], B]): A function of type A -> B

        Returns:
            Functor[F, B]: A value of type F[B]
        """
        ...

class Contravariant(Generic[F, A], Protocol):
    """Contravariant functor"""

    def cmap(self, f: Callable[[B], A]) -> Contravariant[F, B]:
        """Contravariant map

        Args:
            f (Callable[[B], A]): _description_

        Returns:
            Contravariant[F, B]: _description_
        """
        ... 
