from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Protocol, TypeVar, cast
from funclift.functor import Functor
from funclift.monad import Monad
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B', covariant=True)
D = TypeVar('D')
E = TypeVar('E')
F = TypeVar('F')
K = TypeVar('K')
H = TypeVar('H')
G = TypeVar('G', bound=Monad)


class FunctionK(Generic[H, G], Protocol):
    # def getmonad(self) -> Type[Monad]: ...
    # def getmonad(self) -> Type[G]: ...

    # def apply(self, fa: H) -> G: ...
    def apply(self, fa: Functor[H, A]) -> Monad[G, A]: ...

    def mempty(self, a: A) -> Monad[G, A]: ...


# class Free(Monad[F, A], Generic[F, A]):
class Free(Generic[F, A]):
    """_summary_

    Args:
        Generic (_type_): _description_
    """

    def fmap(self, f: Callable[[A], B]) -> Free[F, B]:
        return self.flatmap(lambda a: Free.pure(f(a)))

    # def flatMap(fa: Free[M, A], f: A -> Free[M, B]) -> Free[M, B]:
    # @staticmethod
    def flatmap(self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        return FlatMap(self, f)
    # def flatmap(self, f: Callable[[A], Monad[B]]) -> Free[F, B]:
    #     return FlatMap(self, cast(Callable[[A], Free[F, B]], f))

    def ap(self, a: Free[F, D]) -> Free[F, E]:
        return a.fmap(cast(Callable[[D], E], self))

    # def pure(a: A) -> F[A]:
    @staticmethod
    def pure(a: E) -> Free[F, E]:
        return Pure(a)

    @staticmethod
    def mempty(a: E) -> Free[F, E]:
        return Pure(a)

    @staticmethod
    # def liftm(ma: F[A]) -> Free[F, A]:
    # def liftm(fa: Any) -> Free[F, A]:
    # def liftm(fa: Functor[K, E]) -> Lift[K, E]:
    def liftm(fa: Functor[F, A]) -> Lift[F, A]:
        return Lift(fa)

    # def foldmap(self, nt: Callable[[F], G]) -> G:
    @abstractmethod
    def foldmap(self, nt: FunctionK[F, G]) -> Monad[G, A]: ...


@dataclass
class FlatMap(Generic[F, E, A], Free[F, A]):
    inner: Free[F, E]
    f: Callable[[E], Free[F, A]]

    def foldmap(self, nt: FunctionK[F, G]) -> Monad[G, A]:
        # return self.inner.foldmap(nt).flatmap(
        #   lambda e: self.f(e).foldmap(nt))
        # return cast(G, self.inner.foldmap(nt).flatmap(
        #   lambda e: self.f(e).foldmap(nt)))
        ge: Monad[G, E] = self.inner.foldmap(nt)

        def _inner(e: E) -> Monad[G, A]:
            free_fa = self.f(e)
            return free_fa.foldmap(nt)

        return ge.flatmap(_inner)


@dataclass
class Pure(Free[F, A]):
    a: A

    # def foldmap(self, nt: Callable[[F], G]) -> G:
    def foldmap(self, nt: FunctionK[F, G]) -> Monad[G, A]:
        # gm: Type[G] = nt.getmonad()
        # result: Monad[G, A] = gm.mempty(self.a)
        # return result
        return nt.mempty(self.a)


@dataclass
class Lift(Generic[F, A], Free[F, A]):
    fa: Functor[F, A]  # Any # F[A]

    def foldmap(self, nt: FunctionK[F, G]) -> Monad[G, A]:
        return nt.apply(self.fa)
