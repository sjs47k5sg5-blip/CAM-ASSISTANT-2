from __future__ import annotations

from .point import Point

EPS = 1e-9

def almost_equal(a: float, b: float, eps: float = EPS) -> bool:
    return abs(a - b) <= eps

def midpoint(p1: Point, p2: Point) -> Point:
    return p1.midpoint(p2)

def distance(p1: Point, p2: Point) -> float:
    return p1.distance_to(p2)

def lerp(p1: Point, p2: Point, t: float) -> Point:
    return Point(
        p1.x + (p2.x - p1.x) * t,
        p1.y + (p2.y - p1.y) * t,
    )
