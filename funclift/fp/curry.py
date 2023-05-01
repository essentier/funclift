from functools import partial
from inspect import signature
import logging

log = logging.getLogger(__name__)


class Curryable(object):
    def __init__(self, numArgs=-1):
        self.numArgs = numArgs

    def __call__(self, func):
        if self.numArgs == -1:
            self.numArgs = len(signature(func).parameters)
        if self.numArgs > 0:
            @Curryable(numArgs=self.numArgs-1)
            def wrapper(*args, **kwargs):
                if len(args) < self.numArgs:
                    return partial(func, *args)
                else:
                    return partial(func, *args)(**kwargs)
            return wrapper
        else:
            return func


def curry(func):
    return Curryable()(func)
