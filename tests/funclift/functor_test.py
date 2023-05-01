from typing import Any, Callable, Protocol, TypeVar, overload
from funclift.types.clist import CList
from funclift.types.option import Option, Some
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')


class FunctorSupport(Protocol):
    @staticmethod
    def fmap(fa: Any, f: Any) -> Any: ...


class CListFunctor():
    @staticmethod
    def fmap(fa: CList[A], f: Callable[[A], B]) -> CList[B]:
        return fa.fmap(f)


class OptionFunctor():
    @staticmethod
    def fmap(fa: Option[A], f: Callable[[A], B]) -> Option[B]:
        return fa.fmap(f)


@overload
def fmap_all(fa: Option[A], f: Callable[[A], B],
             fs: FunctorSupport) -> Option[B]:
    ...


@overload
def fmap_all(fa: CList[A],
             f: Callable[[A], B], fs: FunctorSupport) -> CList[B]:
    ...


# fa is Any because of the overload for list[A].
# otherwise, fa can be Functor[A] like this:
# def fmap_all(fa: Functor[A], f: Callable[[A], B],
#             fs: FunctorSupport) -> Functor[B]:
def fmap_all(fa: Any, f: Callable[[A], B], fs: FunctorSupport) -> Any:
    return fs.fmap(fa, f)


def int_to_str(num: int) -> str:
    return 'h' * num


def test_functor_example():
    log.debug('--------- Functor examples ---------')
    maybe_3 = Some(3)
    maybe_str = fmap_all(maybe_3, int_to_str, OptionFunctor)
    # reveal_type(maybe_str)
    # log.debug('', maybe_str)
    assert maybe_str == Some('hhh')

    list_nums = CList([1, 2, 3])
    list_str = fmap_all(list_nums, int_to_str, CListFunctor)
    assert list_str == CList(['h', 'hh', 'hhh'])
