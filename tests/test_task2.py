import math

import pytest

from task2 import koch_points, parse_args


@pytest.mark.parametrize("level", [0, 1, 2, 3])
def test_segment_count(level):
    points = koch_points(level, 300)
    assert len(points) - 1 == 3 * 4**level


def test_closed_polygon():
    points = koch_points(2, 300)
    assert points[0] == pytest.approx(points[-1])


def test_level0_is_equilateral_triangle():
    p = koch_points(0, 300)
    sides = [math.dist(p[i], p[i + 1]) for i in range(3)]
    assert sides == pytest.approx([300, 300, 300])


def test_segment_length_shrinks_by_three():
    p = koch_points(1, 300)
    assert math.dist(p[0], p[1]) == pytest.approx(100)


def test_negative_level_rejected():
    with pytest.raises(ValueError):
        koch_points(-1, 300)


def test_parse_args():
    assert parse_args(["4"]).level == 4
    assert parse_args([]).level is None
