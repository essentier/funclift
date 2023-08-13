from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Generic, Tuple, TypeVar, cast
from funclift.monoid import Monoid
import logging

log = logging.getLogger(__name__)

Mnd = Monoid | int | list
W = TypeVar('W', bound=Mnd)
# W = TypeVar('W')
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')
T = TypeVar('T', bound=Mnd)


@dataclass
class Predicate(Generic[A]):
    """Predicate is a contravariant functor."""
    action: Callable[[A], bool]

    def cmap(self, f: Callable[[B], A]) -> Predicate[B]:
        def new_action(b: B) -> bool:
            return self.action(f(b))

        return Predicate(new_action)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.action(args[0])

    def run(self, a: A) -> bool:
        return self.action(a)
