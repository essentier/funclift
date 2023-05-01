from typing import Any, Generator
from funclift.monad import Monad
from functools import wraps
import logging

log = logging.getLogger(__name__)


def run_monads(monads: Generator[Any, Any, Any]) -> Any:
    monad = next(monads)
    mfunc = Mfunc(monads, monad)
    result = monad.flatmap(mfunc)
    return result


class Mfunc:
    def __init__(self, monads: Generator[Monad, None, None],
                 this_monad) -> None:
        self.this_monad = this_monad
        self.monads = monads

    def __call__(self, value):
        try:
            log.debug(f'send value {value}')
            next_monad: Monad = self.monads.send(value)
            log.debug(f'next monad {next_monad}')
        except StopIteration as e:
            if e.value:
                # if type(e.value) == type(self.this_monad):
                if hasattr(self.this_monad, 'mtype'):
                    if isinstance(e.value, self.this_monad.mtype):
                        return e.value
                    else:
                        return self.this_monad.pure(e.value)
                else:
                    if isinstance(e.value, type(self.this_monad)):
                        return e.value
                    else:
                        return self.this_monad.pure(e.value)
            else:
                return self.this_monad

        if hasattr(self.this_monad, 'mtype'):
            if not isinstance(next_monad, self.this_monad.mtype):
                return self.this_monad.pure(next_monad)
        else:
            if not isinstance(next_monad, type(self.this_monad)):
                return self.this_monad.pure(next_monad)

        # if type(next_monad) != type(self.this_monad):
        #     return self.this_monad.pure(next_monad)

        # if not hasattr(next_monad, 'flatmap'):
        #     return self.this_monad.pure(next_monad)

        self.this_monad: Monad = next_monad
        log.debug(f'calling next_monad.flatmap {next_monad}')
        return next_monad.flatmap(self)


def monads_runner(mondas_gen):
    @wraps(mondas_gen)
    def wrapper():
        return run_monads(mondas_gen())

    return wrapper
