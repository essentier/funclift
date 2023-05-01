from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Tuple, TypeVar

from funclift.monoid import Monoid
import logging

log = logging.getLogger(__name__)

W = TypeVar('W', bound=Monoid)
V = TypeVar('V')
A = TypeVar('A')
B = TypeVar('B')
S = TypeVar('S')
S2 = TypeVar('S2')


@dataclass
class State(Generic[A, S]):
    """State is a monad."""

    action: Callable[[S], Tuple[A, S]]

    def fmap(self, f: Callable[[A], B]) -> State[B, S]:
        def new_action(s: S) -> Tuple[B, S]:
            a, s2 = self.action(s)
            return f(a), s2
        return State(new_action)

    @staticmethod
    def pure(b: B) -> State[B, S2]:
        def new_action(s: S2) -> Tuple[B, S2]:
            return b, s
        return State(new_action)

    @staticmethod
    def read() -> State[S, S]:
        def new_action(s: S) -> Tuple[S, S]:
            return s, s
        return State(new_action)

    @staticmethod
    def write(s2: S) -> State[None, S]:
        def new_action(s: S) -> Tuple[None, S]:
            return None, s2
        return State(new_action)

    def run(self, s: S) -> Tuple[A, S]:
        return self.action(s)

    @staticmethod
    def run_state(sm: State[A, S], s: S) -> Tuple[A, S]:
        return sm.action(s)

    def flatmap(self: State[A, S],
                f: Callable[[A], State[B, S]]) -> State[B, S]:
        def new_action(s: S) -> Tuple[B, S]:
            a, s2 = self.action(s)
            return f(a).action(s2)
        return State(new_action)


# from typing import TypeVar, Callable

# State = TypeVar("State")
# A = TypeVar("A")

# def state_monad(f: Callable[[State], (A, State)]):
#     def bind(g):
#         def h(s):
#             (a, s_) = f(s)
#             return g(a)(s_)
#         return h
#     return bind

# def get_state(s: State) -> (State, State):
#     return s, s

# def set_state(s: State) -> (None, State):
#     return None, s

# def run_state(s: State, t: Callable[[State], (A, State)]) -> A:
#     return t(s)[0]
