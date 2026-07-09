from __future__ import annotations

from math import tan, radians

from ..geometry import Line, Point


def fillet_radius_offset(radius: float, angle_deg: float) -> float:
    """
    Distance from the corner to the tangent points.
    """
    if angle_deg <= 0 or angle_deg >= 180:
        raise ValueError("Angle must be between 0 and 180 degrees.")
    return radius / tan(radians(angle_deg) / 2.0)


def line_fillet_placeholder(
    first: Line,
    second: Line,
    radius: float,
) -> tuple[Point, Point]:
    """
    Temporary implementation.

    Returns tangent points on the two lines.
    A full geometric fillet (Arc creation) will be implemented
    after robust line-line intersection support.
    """
    d = fillet_radius_offset(radius, 90.0)
    return (
        first.end.translate(-d, 0.0),
        second.start.translate(d, 0.0),
    )
