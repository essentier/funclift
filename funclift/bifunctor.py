from __future__ import annotations
from typing import Callable, Generic, Protocol, TypeVar
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
B = TypeVar('B', covariant=True)
C = TypeVar('C', covariant=True)
D = TypeVar('D')
F = TypeVar('F', covariant=True)


class BiFunctor(Generic[F, A, B], Protocol):
    """BiFunctor"""

    def bimap(self, fl: Callable[[A], C],
              fr: Callable[[B], D]) -> BiFunctor[F, C, D]:
        """_summary_

        Args:
            fl (Callable[[A], C]): _description_
            fr (Callable[[B], D]): _description_

        Returns:
            BFunctor[F, C, D]: _description_
        """
        ...

    def first(self, fl: Callable[[A], C]) -> BiFunctor[F, C, B]:
        """_summary_

        Args:
            fl (Callable[[A], C]): _description_

        Returns:
            BFunctor[F, C, B]: _description_
        """
        ...

    def second(self, fr: Callable[[B], D]) -> BiFunctor[F, A, D]:
        """_summary_

        Args:
            fr (Callable[[B], D]): _description_

        Returns:
            BFunctor[F, A, D]: _description_
        """
        ...
