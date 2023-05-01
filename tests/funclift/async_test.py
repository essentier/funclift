from dataclasses import dataclass
from funclift.fp.monad_runner import run_monads

from funclift.types.future import Future


@dataclass
class User:
    id: str


@dataclass
class Product:
    sku: str
    price: int


def get_user(url: str) -> Future[User]:
    if url.startswith('a'):
        return Future(User('valid_user_id'))
    else:
        return Future(None)


def get_last_order(user_id: str) -> Future[Product]:
    return Future(Product('product1', 30))


def test_example1():
    last_order = get_user('aaa').flatmap(lambda user: get_last_order(user.id))
    result = last_order.fmap(lambda product: product.price + 12)
    assert result == Future(42)

    last_order = get_user('bbb').flatmap(lambda user: get_last_order(user.id))
    result = last_order.fmap(lambda product: product.price + 12)
    assert result == Future(None)


def test_example2():
    def monadic_fun():
        user = yield get_user('aaa')
        product = yield get_last_order(user.id)
        yield product.price + 12

    result = run_monads(monadic_fun())
    assert result == Future(42)

    def monadic_fun2():
        user = yield get_user('bbb')
        product = yield get_last_order(user.id)
        yield product.price + 12

    result = run_monads(monadic_fun2())
    assert result == Future(None)
