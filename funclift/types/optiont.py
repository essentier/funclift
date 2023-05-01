from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from funclift.applicative import Applicative
from funclift.monad import Monad
import logging
from funclift.types.option import Nothing, Option, Some

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C', covariant=True)
D = TypeVar('D')
E = TypeVar('E')
M = TypeVar('M')
AP = TypeVar('AP', bound=Applicative)


@dataclass
class OptionT(Generic[M, A]):
    """
    OptionT is a monad transformer in the style of the mtl library for
    Haskell.
    """

    value: Monad[M, Option[A]]

    def run(self) -> Monad[M, Option[A]]:
        return self.value

    # def pure(self, a: E) -> OptionT[M, E]:
    #     return OptionT(self.value.pure(Some.pure(a)))

    def pure(self, option_e: Option[E]) -> OptionT[M, E]:
        return OptionT(self.value.pure(option_e))

    # def fmap(self, f: Callable[[A], B]) -> Some[B]:
    #     return Some(f(self.value))

    def flatmap(self, f: Callable[[A], OptionT[M, B]]) -> OptionT[M, B]:
        def foo(option_a: Option[A]) -> Monad[M, Option[B]]:
            if isinstance(option_a, Nothing):
                return self.value.pure(Nothing())
            else:
                return f(option_a.get()).value

        # self.value: IO[Option[A]]
        # foo: [Option[A]] -> IO[Option[B]]
        # self.value.flatmap(foo): IO[Option[B]]
        return OptionT(self.value.flatmap(foo))

    # def flatmap(self, f: Callable[[A], Option[B]]) -> OptionT[M, B]:
    #     def foo(option_a: Option[A]) -> Option[B]:
    #         if isinstance(option_a, Nothing):
    #             return Nothing()
    #         else:
    #             return f(option_a.get())

    #     return OptionT(self.value.fmap(foo))

    @staticmethod
    def lift(ma: Monad[M, A]) -> OptionT[M, A]:
        return OptionT(ma.fmap(lambda a: Some.pure(a)))
