from __future__ import annotations
from abc import abstractmethod
from typing import Callable, Protocol, TypeVar
from funclift.functor import Functor
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
F = TypeVar('F')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')


class Applicative(Functor[F, A], Protocol):
    """
    An applicative is a [functor][funclift.functor.Functor] that contains a
    function which the applicative applies to arguments.

    The generic type variable F is the applicative type. The generic type
    variable A is the type of the value contained in the applicative type.
    """

    @staticmethod
    def pure(a: B) -> Applicative[F, B]:
        """_summary_

        Args:
            a (B): _description_

        Returns:
            Applicative[F, B]: _description_
        """
        ...

    def ap(self: Applicative[F, Callable[[C], E]],
           a: Applicative[F, C]) -> Applicative[F, E]:
        """_summary_

        Args:
            self (Applicative[F, Callable[[C], E]]): _description_
            a (Applicative[F, C]): _description_

        Returns:
            Applicative[F, E]: _description_
        """
        ...

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Applicative[F, B]:
        ...
