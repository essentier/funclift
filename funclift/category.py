from __future__ import annotations
from typing import Callable, Generic, Protocol, TypeVar
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
B = TypeVar('B', covariant=True)
C = TypeVar('C', covariant=True)
D = TypeVar('D')
Cat = TypeVar('Cat', covariant=True)


class Category(Generic[Cat, A, B], Protocol):
    """Category"""

    @staticmethod
    def id() -> Category[Cat, A, A]:
        ...

    def then(self, f: Callable[[B], C]) -> Category[Cat, A, C]:
        ...

