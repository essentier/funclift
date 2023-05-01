from funclift.types.option import Nothing, Option, Some


def test_example2():
    result = Option.product(Option.create(7), Option.create('hi'))
    assert result == Some((7, 'hi'))

    result2 = Option.product(Option.create(7), Nothing())
    assert result2 == Nothing()
