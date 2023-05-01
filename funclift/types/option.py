from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from inspect import signature
from typing import Any, Callable, ClassVar, Generator, Generic
from typing import Iterator, TypeVar
from funclift.applicative import Applicative
from funclift.exceptions import FunctorValueError
import logging

log = logging.getLogger(__name__)

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C", covariant=True)
D = TypeVar("D")
E = TypeVar("E")
M = TypeVar("M")
AP = TypeVar("AP", bound=Applicative)
AP_B = Applicative[AP, B]


class Option(Generic[A]):
    """
    The Option class represents one of two cases: something or nothing.
    The case of nothing is modeled by the
    [`Nothing`][funclift.types.option.Nothing] class. The case of something
    is modeled by the [`Some`][funclift.types.option.Some] class.

    Option is a [`Monad`][funclift.monad.Monad]. It is parameterized by
    a type variable A. When an Option object contains something, A is
    the type of that something. When an Option object contains nothing,
    A will match any type.
    """

    @staticmethod
    def pure(a: E) -> Some[E]:
        """Creates a [`Some`][funclift.types.option.Some] instance that
        contains the passed-in parameter as its value.

        Args:
            a (E): value to be contained in a
            [`Some`][funclift.types.option.Some] instance

        Returns:
            Some[E]: a [`Some`][funclift.types.option.Some] instance that
            contains the passed-in parameter as its value.
        """
        return Some(a)

    @staticmethod
    def empty() -> Nothing:
        """_summary_

        Returns:
            Nothing: _description_
        """
        return Nothing()

    @staticmethod
    def create(value: A | None) -> Option[A]:
        """Creates an Option instance. Returns a Nothing instance if the
        passed-in value is None; otherwise, returns a Some instance.

        Args:
            value (A | None): a value to be wrapped up in an Option instance.

        Returns:
            Option[A]: the returned Option instance.
        """
        if value is None:
            return Nothing()
        else:
            return Some(value)

    @abstractmethod
    def get(self) -> A:
        """_summary_

        Returns:
            A: _description_
        """
        ...

    def __iter__(self) -> Iterator[A]:
        yield self.get()

    # Need to repeat this to make mypy happy or else mypy will think
    # the return type is Functor[B]
    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Option[B]:
        """Option is a Functor and therefore implements the fmap method.
        Need to repeat this to make mypy happy or else mypy will think
        the return type is Functor[F, B]. See the fmap method in
        [`Functor`][funclift.functor.Functor] for details.
        """
        ...

    @abstractmethod
    def flatmap(self, f: Callable[[A], Option[B]]) -> Option[B]:
        ...

    @abstractmethod
    def ap(self: Option[Callable[[C], E]], a: Option[C]) -> Option[E]:
        ...

    # def ap(fab: Option[Callable[[A], B]], a: Option[A]) -> Option[B]: ...
    # @abstractmethod
    # def ap2(self, f: Option[Callable[[A], B]]) -> Option[B]: ...

    @staticmethod
    def product(d: Option[D], e: Option[E]) -> Option[tuple[D, E]]:
        if isinstance(d, Nothing):
            return Nothing()

        if isinstance(e, Nothing):
            return Nothing()

        # return Some.product(d, e)
        return Some((d.get(), e.get()))

    @classmethod
    def do(cls, expr: Generator[B, None, None]) -> Option[B]:
        try:
            return Some.pure(next(expr))
        except FunctorValueError as exc:
            return exc.halted_container


@dataclass
class Some(Option[A]):
    """Some"""

    value: A
    mtype: ClassVar[type] = Option

    def get(self) -> A:
        return self.value

    @staticmethod
    # def pure(a: A) -> Some[A]:
    def pure(a: E) -> Some[E]:
        return Some(a)

    def fmap(self, f: Callable[[A], B]) -> Some[B]:
        return Some(f(self.value))

    def flatmap(self, f: Callable[[A], Option[B]]) -> Option[B]:
        result = f(self.value)
        return result

    # This won't work because E does not come from anywhere
    # def ap(self, other: Option[D]) -> Option[E]:
    #     return other.fmap(cast(Callable[[D], E], self.value))

    def ap(self: Some[Callable[[C], E]], other: Option[C]) -> Option[E]:
        return other.fmap(self.value)
        # return other.ap2(self.value)

    # @staticmethod
    # def product(d: Some[D], e: Some[E]) -> Some[tuple[D, E]]:
    #     return Some((d.value, e.value))

    def traverse(self: Some[A],
                 f: Callable[[A], AP_B]) -> Applicative[AP, Some[B]]:
        ap_b: Applicative[AP, B] = f(self.value)
        return ap_b.fmap(lambda x: Some(x))
        # return cast(Applicative[AP, Some[B]], ap_b.fmap(lambda x: Some(x)))
        # return ap_b.pure(lambda x: Some(x)).ap(ap_b)


@dataclass
class Nothing(Option[Any]):
    """Nothing"""

    mtype: ClassVar[type] = Option

    def get(self) -> Any:
        raise FunctorValueError(self)

    # @staticmethod
    # def pure(a: E) -> Nothing[E]:
    #     return Nothing()

    def fmap(self, f: Callable[[A], B]) -> Nothing:
        return Nothing()

    def flatmap(self, f: Callable[[A], Option[B]]) -> Nothing:
        return Nothing()

    # def ap(self, a: Option) -> Option:
    def ap(self, other: Option[C]) -> Nothing:
        return Nothing()

    def traverse(self, f: Callable[[A], AP_B]) -> Applicative[AP, Option[B]]:
        # return IO.pure(Nothing())
        sig = signature(f)
        return sig.return_annotation.pure(Nothing())
