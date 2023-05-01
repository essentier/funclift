from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Protocol, TypeVar
from funclift.applicative import Applicative, Applicative
from funclift.functor import Functor
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
F = TypeVar('F')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')
H = TypeVar('H')
G = TypeVar('G', bound=Applicative)


class FunctionK(Generic[H, G], Protocol):
    def apply(self, fa: Functor[H, A]) -> Applicative[G, A]: ...

    def mempty(self, a: A) -> Applicative[G, A]: ...


class FreeA(Generic[F, A]):
    """_summary_

    Args:
        Generic (_type_): _description_

    Returns:
        _type_: _description_
    """

    @staticmethod
    def pure(a: B) -> FreeA[F, B]:
        return Pure(a)

    @staticmethod
    def lift(fa: Functor[F, A]) -> Lift[F, A]:
        return Lift(fa)

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> FreeA[F, B]: ...

    # def ap(self: FreeA[F, E], a: Functor[F, C]) -> Functor[F, E]: ...
    # def ap(self: FreeA[F, A], b: FreeA[F, Callable[[A], B]]) -> FreeA[F, B]:
    #     if isinstance(b, Pure):
    #         return self.fmap(b.a)

    #     return Ap(b, self)

    @abstractmethod
    def ap(self: FreeA[F, Callable[[B], C]], b: FreeA[F, B]) -> FreeA[F, C]:
        ...

    @abstractmethod
    def foldmap(self, nt: FunctionK[F, G]) -> Applicative[G, A]: ...


@dataclass
class Lift(FreeA[F, A]):
    fa: Functor[F, A]

    def fmap(self, f: Callable[[A], C]) -> FreeA[F, C]:
        return Ap(Pure(f), self)

    def ap(self: Lift[F, Callable[[B], C]], b: FreeA[F, B]) -> FreeA[F, C]:
        return Ap(self, b)

    def foldmap(self, nt: FunctionK[F, G]) -> Applicative[G, A]:
        return nt.apply(self.fa)


@dataclass
class Pure(FreeA[F, A]):
    a: A

    def foldmap(self, nt: FunctionK[F, G]) -> Applicative[G, A]:
        return nt.mempty(self.a)

    def fmap(self, f: Callable[[A], B]) -> Pure[F, B]:
        return Pure(f(self.a))

    def ap(self: Pure[F, Callable[[B], C]], b: FreeA[F, B]) -> FreeA[F, C]:
        return Ap(self, b)

    # def ap(self: Pure[F, Callable[[C], E]], b: FreeA[F, C]) -> FreeA[F, E]:
    #     return b.fmap(self.a)


@dataclass
class Ap(FreeA[F, A], Generic[F, A, B]):
    fba: FreeA[F, Callable[[B], A]]
    fb: FreeA[F, B]

    def fmap(self: Ap[F, A, B], f: Callable[[A], C]) -> FreeA[F, C]:
        return Ap(Pure(f), self)

    def ap(self: Ap[F, Callable[[C], E], B], c: FreeA[F, C]) -> FreeA[F, E]:
        return Ap(self, c)

    def foldmap(self, nt: FunctionK[F, G]) -> Applicative[G, A]:
        # gba = nt.apply(self.fba)
        # gb = nt.apply(self.fb)
        gba = self.fba.foldmap(nt)
        gb = self.fb.foldmap(nt)
        return gba.ap(gb)
