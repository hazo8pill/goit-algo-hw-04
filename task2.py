import argparse
import math
import turtle

ROT_COS, ROT_SIN = math.cos(-math.pi / 3), math.sin(-math.pi / 3)


def koch_segment(p1, p2, level):
    """Return points of a Koch curve from p1 to p2 (p2 excluded)."""
    if level == 0:
        return [p1]
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
    a = (x1 + dx, y1 + dy)
    b = (x1 + 2 * dx, y1 + 2 * dy)
    peak = (a[0] + dx * ROT_COS - dy * ROT_SIN, a[1] + dx * ROT_SIN + dy * ROT_COS)
    points = []
    for start, end in ((p1, a), (a, peak), (peak, b), (b, p2)):
        points += koch_segment(start, end, level - 1)
    return points


def koch_points(level, size):
    if level < 0:
        raise ValueError("level must be >= 0")
    h = size * math.sqrt(3) / 2
    corners = [(-size / 2, -h / 3), (0, 2 * h / 3), (size / 2, -h / 3)]
    points = []
    for start, end in zip(corners, corners[1:] + corners[:1]):
        points += koch_segment(start, end, level)
    return points + [points[0]]


def draw(level, size=400):
    t = turtle.Turtle()
    t.hideturtle()
    t.screen.title(f"Koch snowflake, level {level}")
    t.screen.tracer(0)
    points = koch_points(level, size)
    t.penup()
    t.goto(points[0])
    t.pendown()
    for p in points[1:]:
        t.goto(p)
    t.screen.update()
    turtle.done()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Draw a Koch snowflake.")
    parser.add_argument("level", type=int, nargs="?", help="recursion level (>= 0)")
    return parser.parse_args(argv)


def main(argv=None):
    level = parse_args(argv).level
    while level is None or level < 0:
        try:
            level = int(input("Enter recursion level (>= 0): "))
        except ValueError:
            print("Please enter a non-negative integer.")
    draw(level)


if __name__ == "__main__":
    main()
