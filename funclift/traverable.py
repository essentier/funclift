from dataclasses import dataclass
from inspect import signature
from typing import Callable, Generic, Protocol, TypeVar

from funclift.applicative import Applicative
from funclift.foldable import ListFoldable
from funclift.functor import Functor
from funclift.fp.curry import curry
import logging

log = logging.getLogger(__name__)

AP = TypeVar('AP', bound=Applicative)
F = TypeVar('F', bound=Functor)
A = TypeVar('A')
B = TypeVar('B')
AP_LB = Applicative[AP, list[B]]


class Traversable(Generic[F, A], Protocol):
    """Traversable
    F is a Functor and also a Foldable.

    Need to provide default implementations for the following two methods:
    mapM      :: Monad m => (a -> m b) -> t a -> m (t b)
    sequence  :: Monad m => t (m a) -> m (t a)
    """

    def traverse(self,
                 f: Callable[[A], Applicative[AP, B]]) -> Applicative[AP, Functor[F, B]]:
        """
        AP[B] is an Applicative.
        traverse :: F[A] -> (A -> AP[B]) -> AP[F[B]]

        Args:
            f (Callable[[A], Applicative[AP, B]]): _description_

        Returns:
            Applicative[AP, Functor[F, B]]: _description_
        """
        ...

    def sequence(self, f_ap_a: Functor[F, Applicative[AP, A]]) -> Applicative[AP, Functor[F, A]]:
        # This is called sequenceA in Haskell.
        # sequenceA F [AP[A]] -> AP [F[A]]
        ...


@curry
def colon_right(x: A, xs: list[A]) -> list[A]:
    result = [x]
    result = result + xs
    return result


@curry
def colon_left(xs: list[A], x: A) -> list[A]:
    result = [x]
    result = xs + result
    return result


@dataclass
class ListTraverser():
    effect_cls: type

    def traverse(self, ls: list[A],
                 f: Callable[[A], Applicative[AP, B]]) -> AP_LB:
        return ListTraversable.traverse_left(self.effect_cls, ls, f)

    def sequence(self, list_ap_a: list[Applicative[AP, A]]) -> Applicative[AP, list[A]]:
        def id_func(a: Applicative[AP, A]) -> Applicative[AP, A]:
            return a    # cls.pure(a)

        return ListTraversable.traverse_left(self.effect_cls, list_ap_a, id_func)


class ListTraversable():
    """This class implements the Traversable behavior for the built-in list type."""

    @staticmethod
    def traverse(ls: list[A],
                 f: Callable[[A], Applicative[AP, B]]) -> AP_LB:
        sig = signature(f)
        mcls = sig.return_annotation
        return ListTraversable.traverse_left(mcls, ls, f)

    @staticmethod
    def traverse_right(mcls, ls: list[A],
                       f: Callable[[A], Applicative[AP, B]]) -> AP_LB:
        def fold_func(a: A, bs: AP_LB) -> AP_LB:
            return mcls.pure(colon_right).ap(f(a)).ap(bs)

        return ListFoldable.fold_right(ls, fold_func, mcls.pure([]))

    @staticmethod
    def traverse_left(mcls, ls: list[A],
                      f: Callable[[A], Applicative[AP, B]]) -> AP_LB:
        # mcls is the effect class
        def fold_func(bs: AP_LB, a: A) -> AP_LB:
            return mcls.pure(colon_left).ap(bs).ap(f(a))

        return ListFoldable.fold_left(ls, fold_func, mcls.pure([]))

    @staticmethod
    def sequence(mcls, list_ap_a: list[Applicative[AP, B]]) -> AP_LB:
        # mcls is the effect class
        def id_func(a: Applicative[AP, B]) -> Applicative[AP, B]:
            return a

        return ListTraversable.traverse_left(mcls, list_ap_a, id_func)
