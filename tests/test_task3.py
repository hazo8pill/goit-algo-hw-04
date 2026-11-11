import random

import pytest

from task3 import benchmark, insertion_sort, make_datasets, merge_sort

CASES = [
    [],
    [1],
    [2, 1],
    [3, 1, 2, 3, 1],
    [-5, 0, 5, -1],
    list(range(20)),
    list(range(20, 0, -1)),
    random.Random(42).sample(range(1000), 200),
]


@pytest.mark.parametrize("sort_fn", [insertion_sort, merge_sort])
@pytest.mark.parametrize("data", CASES)
def test_sorts_match_builtin(sort_fn, data):
    original = list(data)
    assert sort_fn(data) == sorted(original)
    assert data == original


def test_make_datasets():
    ds = make_datasets(50)
    assert set(ds) == {"random", "sorted", "reversed", "nearly_sorted"}
    assert all(len(v) == 50 for v in ds.values())
    assert ds["sorted"] == sorted(ds["sorted"])


def test_benchmark_rows():
    rows = benchmark([10, 20], number=1)
    algos = {r["algorithm"] for r in rows}
    assert algos == {"insertion", "merge", "timsort"}
    assert len(rows) == 3 * 2 * 4
    assert all(r["seconds"] >= 0 for r in rows)
