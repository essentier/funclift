from __future__ import annotations
from typing import Protocol, TypeVar
from funclift.functor import Functor
import logging

log = logging.getLogger(__name__)

A = TypeVar('A', covariant=True)
F = TypeVar('F')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')


class Semigroupal(Functor[F, A], Protocol):
    """Semigroupal"""

    @staticmethod
    def product(d: Functor[F, D], e: Functor[F, E]) -> Functor[F, tuple[D, E]]:
        ...
