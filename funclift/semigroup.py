from __future__ import annotations
from typing import Protocol, TypeVar
import logging

log = logging.getLogger(__name__)

T = TypeVar('T')


class Semigroup(Protocol[T]):
    """A type is a Semigroup if it implements the __add__ method."""

    def __add__(self: Semigroup[T], other: Semigroup[T]) -> Semigroup[T]:
        """_summary_

        Args:
            self (T): _description_
            other (T): _description_

        Returns:
            T: _description_
        """
        ...
