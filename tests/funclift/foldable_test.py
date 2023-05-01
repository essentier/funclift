from funclift.foldable import ListFoldable


nums = [1, 2, 3, 4, 5]


def foo_fold_map(num: int) -> str:
    return str(num)


def foo_fold_right(num: int, acc: str) -> str:
    return str(num) + acc


def foo_fold_left(acc: str, num: int) -> str:
    return acc + str(num)


def test_fold_map():
    result = ListFoldable.fold_map(nums, foo_fold_map)
    assert result == '12345'


def test_fold_right():
    result = ListFoldable.fold_right(nums, foo_fold_right, '')
    assert result == '12345'


def test_fold_left():
    result = ListFoldable.fold_left(nums, foo_fold_left, '')
    assert result == '12345'
