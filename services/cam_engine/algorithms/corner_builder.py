from __future__ import annotations

from dataclasses import dataclass

from ..geometry import Line, Point
from .intersections import line_line_intersection

@dataclass(slots=True)
class Corner:
    vertex: Point
    first: Line
    second: Line

def build_corner(first: Line, second: Line) -> Corner | None:
    """
    Creates a corner description from two connected lines.
    """
    pt = line_line_intersection(first, second)
    if pt is None:
        return None
    return Corner(vertex=pt, first=first, second=second)
