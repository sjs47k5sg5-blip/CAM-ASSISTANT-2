from __future__ import annotations

from .point import Point

def translate_point(point: Point, dx: float, dy: float) -> Point:
    return point.translate(dx, dy)

def rotate_point(point: Point, angle_deg: float, origin: Point | None = None) -> Point:
    return point.rotate(angle_deg, origin)

def translate_points(points: list[Point], dx: float, dy: float) -> list[Point]:
    return [p.translate(dx, dy) for p in points]

def rotate_points(points: list[Point], angle_deg: float, origin: Point | None = None) -> list[Point]:
    return [p.rotate(angle_deg, origin) for p in points]
