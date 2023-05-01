from inspect import signature
from typing import Callable, Protocol, TypeVar

from funclift.functor import Functor
from funclift.monoid import Monoid, get_mempty
import logging

log = logging.getLogger(__name__)

F = TypeVar('F', bound=Functor)
A = TypeVar('A', covariant=True)
B = TypeVar('B')
M = TypeVar('M', bound=Monoid | str)


class Foldable(Protocol):
    """A foldable can be reduced to a value."""

    def fold_right(self, f: Callable[[A, B], B]) -> B:
        """Reduces a foldable in a right-associative manner.

        Args:
            self: A foldable structure that contains values of type A.
            f (Callable[[A, B], B]): A function to be used while folding the
            structure.

        Returns:
            B: The value the structure reduces to.
        """
        ...

    def fold_left(self, f: Callable[[B, A], B]) -> B:
        """Reduces a foldable in a left-associative manner.

        Args:
            self: A foldable structure that contains values of type A.
            f (Callable[[B, A], B]): A function to be used while folding the
            structure.

        Returns:
            B: The value the structure reduces to.
        """
        ...

    def fold_map(self, f: Callable[[A], M]) -> M:
        """_summary_

        Args:
            f (Callable[[A], M]): _description_

        Returns:
            M: _description_
        """
        ...


class ListFoldable:
    """Implements [Foldable][funclift.foldable.Foldable] for lists."""

    @staticmethod
    def fold_right(fa: list[A], f: Callable[[A, B], B], id: B) -> B:
        acc = id
        for a in reversed(fa):
            acc = f(a, acc)
        return acc

    @staticmethod
    def fold_left(fa: list[A], f: Callable[[B, A], B], id: B) -> B:
        acc = id
        for a in fa:
            acc = f(acc, a)
        return acc

    @staticmethod
    def fold_map(fa: list[A], f: Callable[[A], M]) -> M:
        sig = signature(f)
        mcls = sig.return_annotation
        acc: M = get_mempty(mcls)

        for a in fa:
            m = f(a)
            acc = acc + m
        return acc

    @staticmethod
    def fold_map2(mcls: type, fa: list[A], f: Callable[[A], M]) -> M:
        acc: M = get_mempty(mcls)

        for a in fa:
            m = f(a)
            acc = acc + m
        return acc
