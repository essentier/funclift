from __future__ import annotations
from typing import Callable, Generic, Protocol, TypeVar
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
B = TypeVar('B', covariant=True)
C = TypeVar('C', covariant=True)
D = TypeVar('D')
P = TypeVar('P', covariant=True)


class Profunctor(Generic[P, B, C], Protocol):
    """Profunctor"""

    def dimap(self, f: Callable[[A], B],
              g: Callable[[C], D]) -> Profunctor[P, A, D]:
        """_summary_

        Args:
            f (Callable[[A], B]): _description_
            g (Callable[[C], D]): _description_

        Returns:
            Profunctor[P, A, D]: _description_
        """
        ...

    def lmap(self, f: Callable[[A], B]) -> Profunctor[P, A, C]:
        """_summary_

        Args:
            f (Callable[[A], B]): _description_

        Returns:
            Profunctor[P, A, C]: _description_
        """
        ...

    def rmap(self, g: Callable[[C], D]) -> Profunctor[P, B, D]:
        """_summary_

        Args:
            g (Callable[[C], D]): _description_

        Returns:
            Profunctor[P, B, D]: _description_
        """
        ...
