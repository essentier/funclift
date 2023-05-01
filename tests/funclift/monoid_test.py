from funclift.monoid import get_mempty
from funclift.types.option import Nothing, Option


def test_int_mempty():
    mempty = get_mempty(int)
    assert mempty == 0


def test_str_mempty():
    mempty = get_mempty(str)
    assert mempty == ''


def test_option_mempty():
    mempty = get_mempty(Option[str])
    assert mempty == Nothing()
