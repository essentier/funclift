from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

import logging

from funclift.functor import Functor

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
F = TypeVar('F')


@dataclass
class Star(Generic[F, B, C]):
    """Star is a profunctor."""

    action: Callable[[B], Functor[F, C]]

    def run(self, x: B) -> Functor[F, C]:
        return self.action(x)

    def dimap(self, ab: Callable[[A], B],
              cd: Callable[[C], D]) -> Star[F, A, D]:
        def new_action(a: A) -> Functor[F, D]:
            return self.action(ab(a)).fmap(cd)

        return Star(new_action)
    
    def lmap(self, ab: Callable[[A], B]) -> Star[F, A, C]:
        def new_action(a: A) -> Functor[F, C]:
            return self.action(ab(a))

        return Star(new_action)

    def rmap(self, cd: Callable[[C], D]) -> Star[F, B, D]:
        def new_action(b: B) -> Functor[F, D]:
            return self.action(b).fmap(cd)

        return Star(new_action)
