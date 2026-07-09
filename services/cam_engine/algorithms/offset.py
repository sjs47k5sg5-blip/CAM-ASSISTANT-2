from __future__ import annotations

from ..geometry import Line, Point, Vector

def offset_line(line: Line, distance: float) -> Line:
    """
    Returns a line parallel to the input line shifted to the left
    by the specified distance.
    """
    direction = Vector.from_points(line.start, line.end).normalized()
    normal = direction.perpendicular_left().scale(distance)

    p1 = Point(line.start.x + normal.x, line.start.y + normal.y)
    p2 = Point(line.end.x + normal.x, line.end.y + normal.y)
    return Line(p1, p2)
