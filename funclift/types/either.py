from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, ClassVar, Generic, TypeVar, Any
import logging

log = logging.getLogger(__name__)

L = TypeVar('L')
R = TypeVar('R')
E = TypeVar('E')
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C', covariant=True)


class Either(Generic[L, R]):
    """
    The Either class represents one of two cases: left or right. The left case
    usually represents an error and is modeled by the
    [`Left`][funclift.types.either.Left] class. The right case represents a
    success and is modeled by the [`Right`][funclift.types.either.Right]
    class.

    Either is a [`Monad`][funclift.monad.Monad]. It is parameterized by
    two type variables: L and R. The type variable L is the value type of the
    left case. The type variable R is the value type of the right case.
    Either is monadic in the type varaible R.
    """

    @staticmethod
    def pure(a: E) -> Right[E]:
        """Creates a [`Right`][funclift.types.either.Right] instance to represent a success case whose value
        is the passed-in parameter.

        Args:
            a (E): value of the success case.

        Returns:
            Right[E]: a [`Right`][funclift.types.either.Right] instance that represents a success case.
        """
        return Right(a)

    @abstractmethod
    def fmap(self, f: Callable[[R], B]) -> Either[L, B]:
        """
        Need to repeat this to make mypy happy or else mypy will think
        the return type is Functor[B].

        Args:
            f (Callable[[R], B]): _description_

        Returns:
            Either[L, B]: _description_
        """
        ...

    @abstractmethod
    def flatmap(self, f: Callable[[R], Either[L, B]]) -> Either[L, B]:
        """_summary_

        Args:
            f (Callable[[R], Either[L, B]]): _description_

        Returns:
            Either[L, B]: _description_
        """
        ...


@dataclass
class Right(Either[Any, A]):
    """Right"""

    value: A
    mtype: ClassVar[type] = Either

    def fmap(self, f: Callable[[A], B]) -> Right[B]:
        return Right(f(self.value))

    def flatmap(self, f: Callable[[A], Either[L, B]]) -> Either[L, B]:
        return f(self.value)

    def ap(self: Right[Callable[[R], E]], other: Either[L, R]) -> Either[L, E]:
        return other.fmap(self.value)


@dataclass
class Left(Either[L, Any]):
    """Left"""

    value: L
    mtype: ClassVar[type] = Either

    def fmap(self, f: Callable[[Any], Any]) -> Left[L]:
        return self

    def flatmap(self, f: Callable[[Any], Either[L, B]]) -> Either[L, B]:
        return self

    def ap(self, other: Either[L, R]) -> Either[L, E]:
        return self
