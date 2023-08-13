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
class Costar(Generic[F, B, C]):
    """Costar is a profunctor."""

    action: Callable[[Functor[F, B]], C]

    def dimap(self, ab: Callable[[A], B],
              cd: Callable[[C], D]) -> Costar[F, A, D]:
        def new_action(fa: Functor[F, A]) -> D:
            return cd(self.action(fa.fmap(ab)))

        return Costar(new_action)
    
    def lmap(self, ab: Callable[[A], B]) -> Costar[F, A, C]:
        def new_action(fa: Functor[F, A]) -> C:
            return self.action(fa.fmap(ab))

        return Costar(new_action)

    def rmap(self, cd: Callable[[C], D]) -> Costar[F, B, D]:
        def new_action(fb: Functor[F, B]) -> D:
            return cd(self.action(fb))

        return Costar(new_action)
