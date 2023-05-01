from funclift.types.clist import CList


def int_to_str(n: int) -> str:
    return 'h' * n


def test_map():
    list1 = CList([1, 2, 3])
    list2 = list1.fmap(int_to_str)
    assert list2 == CList(['h', 'hh', 'hhh'])

    list3 = list1.fmap(lambda n: 'h' * n)
    assert list3 == CList(['h', 'hh', 'hhh'])


def test_map_chain():
    list1 = CList([1, 2, 3])
    list2 = list1.fmap(lambda n: n * 2) \
        .fmap(lambda n: n + 1) \
        .fmap(int_to_str)
    assert list2 == CList(['hhh', 'hhhhh', 'hhhhhhh'])
