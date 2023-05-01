# https://hackage.haskell.org/package/containers
# https://hackage.haskell.org/package/containers-0.6.7/docs/Data-Tree.html
# https://hackage.haskell.org/package/containers-0.6.7/docs/src/Data.Tree.html#line-174

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, cast
import logging

log = logging.getLogger(__name__)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')


class Tree(ABC, Generic[A]):
    """Tree is a monad."""

    @staticmethod
    def pure(b: B) -> Tree[B]:
        return Node(b, [])

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Tree[B]: ...

    @abstractmethod
    def flatmap(self, f: Callable[[A], Tree[B]]) -> Tree[B]: ...

    # @abstractmethod
    # def ap(self: Tree[Callable[[C], E]], a: Tree[C]) -> Tree[E]: ...


@dataclass
class Node(Tree[A]):
    a: A
    children: list[Tree[A]]

    def fmap(self, f: Callable[[A], B]) -> Node[B]:
        return Node(f(self.a), [child.fmap(f) for child in self.children])

    # @staticmethod
    # def pure(b: B) -> Node[B]:
    #     return Node(b, [])

    # def ap(self: Id[Callable[[C], E]], other: Id[C]) -> Id[E]:
    #     # return Id(self.a(other.a))
    #     return other.fmap(self.a)

    def flatmap(self, f: Callable[[A], Tree[B]]) -> Tree[B]:
        tree = f(self.a)
        if isinstance(tree, EmptyTree):
            return tree

        tree_node = cast(Node[B], tree)
        mapped_children = [child.flatmap(f) for child in self.children]
        new_children = tree_node.children + mapped_children
        return Node(tree_node.a, new_children)


@dataclass
class EmptyTree(Tree[Any]):

    # @staticmethod
    # def pure(b: Any) -> EmptyTree:
    #     return EmptyTree()

    def fmap(self, f: Callable[[A], B]) -> EmptyTree:
        return self

    def flatmap(self, f: Callable[[A], Tree[B]]) -> EmptyTree:
        return self
