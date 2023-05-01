from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar
from funclift.semigroup import Semigroup
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C', covariant=True)
D = TypeVar('D')
E = TypeVar('E', bound=Semigroup)


class Validated(Generic[E, A]):
    """Validated"""

    @staticmethod
    def pure(a: D) -> Valid[D]:
        return Valid(a)

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Validated[E, B]: ...

    @abstractmethod
    def ap(self: Validated[E, Callable[[C], D]],
           a: Validated[E, C]) -> Validated[E, D]: ...


@dataclass
class Valid(Validated[Any, A]):
    """Valid"""

    value: A

    def get(self) -> A | None:
        return self.value

    @staticmethod
    def pure(a: D) -> Valid[D]:
        return Valid(a)

    def fmap(self, f: Callable[[A], B]) -> Valid[B]:
        return Valid(f(self.value))

    def ap(self: Valid[Callable[[C], D]],
           a: Validated[E, C]) -> Validated[E, D]:
        if isinstance(a, Invalid):
            return a

        return a.fmap(self.value)


@dataclass
class Invalid(Validated[E, Any]):
    """Invalid"""

    error: E

    def fmap(self, f: Callable[[A], B]) -> Invalid[E]:
        return self

    def ap(self, a: Validated[E, C]) -> Invalid[E]:
        """

        Args:
            a (Validated[E, C]): _description_

        Returns:
            Invalid[E]: _description_
        """
        if isinstance(a, Invalid):
            return Invalid(self.error + a.error)

        return self
