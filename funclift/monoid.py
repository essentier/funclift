from types import GenericAlias
from typing import Protocol, TypeVar

from funclift.semigroup import Semigroup
import logging

log = logging.getLogger(__name__)

T = TypeVar('T')


class Monoid(Semigroup[T], Protocol):
    """A type is a Monoid if it is a Semigroup and also implements
    the empty method.
    """

    @staticmethod
    def empty() -> T: ...


def get_mempty(mcls):
    """_summary_

    Args:
        mcls (_type_): _description_

    Returns:
        _type_: _description_
    """

    if mcls == int:
        return 0
    elif mcls == float:
        return 0
    elif mcls == str:
        return ''
    elif mcls == list:
        return []
    elif isinstance(mcls, GenericAlias):
        return []
    else:
        return mcls.empty()
