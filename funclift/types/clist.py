from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from funclift.applicative import Applicative
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')
AP = TypeVar('AP', bound=Applicative)


@dataclass
class CList(Generic[A]):
    """_summary_

    Args:
        Generic (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    clist: list[A]

    def fmap(self, f: Callable[[A], B]) -> CList[B]:
        return CList([f(item) for item in self.clist])

    def flatmap(self, f: Callable[[A], CList[B]]) -> CList[B]:
        result = []
        for item in self.clist:
            result.extend(f(item).clist)
        return CList(result)

    def to_list(self) -> list[A]:
        return self.clist

    # @staticmethod
    # def product(d: CList[D], e: CList[E]) -> CList[tuple[D, E]]:
