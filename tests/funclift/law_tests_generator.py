import inspect
import logging

log = logging.getLogger(__name__)


def create_law_test_case() -> None:
    def test_function():
        log.debug('test function is run')

    stack = inspect.stack()
    called_from = stack[1]
    module = inspect.getmodule(called_from[0])

    test_function.__name__ = 'test_foo'

    setattr(
        module,
        test_function.__name__,
        test_function,
    )


def create_law_test_case2(module) -> None:
    def test_function():
        log.debug('test function is run')

    # stack = inspect.stack()
    # called_from = stack[1]
    # module = inspect.getmodule(called_from[0])

    test_function.__name__ = 'test_foo'

    setattr(
        module,
        test_function.__name__,
        test_function,
    )
