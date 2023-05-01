from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Generic, TypeVar, cast
from funclift.monad import MonadBase
from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)

V = TypeVar('V', covariant=True)
E = TypeVar('E', covariant=True)
A = TypeVar('A')
B = TypeVar('B')


class Result(Generic[V, E], ABC):
    """Result is a monad."""

    @abstractmethod
    def pure(self, a: A) -> Result[A, E]: ...

    @abstractmethod
    def fmap(self, f: Callable[[A], Result[B, E]]) -> Result[B, E]: ...

    @abstractmethod
    def flatmap(self, f: Callable[[A], Result[B, E]]) -> Result[B, E]: ...


ResultEx = Result[B, Exception]


@dataclass
class Failure(Result[Any, Exception]):
    value: Exception
    mtype: ClassVar[type] = Result

    def pure(self, a: A) -> Result[A, Exception]:
        return Success(a)

    def fmap(self, f: Callable[[A], ResultEx]) -> ResultEx:
        return FailureMonad.fmap(self, f)

    def flatmap(self, f: Callable[[A], ResultEx]) -> ResultEx:
        return FailureMonad.flatmap(self, f)


@dataclass
class Success(Result[V, Any]):
    value: V
    mtype: ClassVar[type] = Result

    def pure(self, a: A) -> Result[A, Any]:
        return Success(a)

    def fmap(self, f: Callable[[A], ResultEx]) -> ResultEx:
        return SuccessMonad.fmap(self, f)

    def flatmap(self, f: Callable[[A], ResultEx]) -> ResultEx:
        return SuccessMonad.flatmap(self, f)


class SuccessMonad(MonadBase):
    @classmethod
    def flatmap(cls, fa: Success[Any], f: Callable[[A], ResultEx]) -> ResultEx:
        try:
            result = f(cast(A, fa.value))
            return result
        except Exception as e:
            return Failure(e)

    @classmethod
    def pure(cls, a: A) -> Success[A]:
        return Success(a)


class FailureMonad(MonadBase):
    @classmethod
    def flatmap(cls, fa: Failure, f: Callable[[A], ResultEx]) -> ResultEx:
        return fa

    @classmethod
    def pure(cls, a: Exception) -> Failure:
        return Failure(a)
