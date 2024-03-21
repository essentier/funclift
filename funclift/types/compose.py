from __future__ import annotations
from typing import Callable, Generic, TypeVar
from funclift.functor import Functor
from dataclasses import dataclass
import logging

log = logging.getLogger(__name__)

A = TypeVar("A", covariant=True)
B = TypeVar("B")
F = TypeVar("F")
G = TypeVar("G")


@dataclass
class Compose(Generic[F, G, A]):
    inner: Functor[F, Functor[G, A]]

    def fmap(self, f: Callable[[A], B]) -> Compose[F, G, B]:
        def _f(a: Functor[G, A]) -> Functor[G, A]:
            return a.fmap(f)
        return Compose(self.inner.fmap(_f))

