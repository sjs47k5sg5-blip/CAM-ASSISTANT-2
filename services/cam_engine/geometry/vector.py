from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from .point import Point, EPS

@dataclass(slots=True, frozen=True)
class Vector:
    x: float
    y: float

    @classmethod
    def from_points(cls, start: Point, end: Point) -> "Vector":
        return cls(end.x - start.x, end.y - start.y)

    @property
    def length(self) -> float:
        return hypot(self.x, self.y)

    def normalized(self) -> "Vector":
        l = self.length
        if l <= EPS:
            raise ValueError("Cannot normalize zero-length vector.")
        return Vector(self.x / l, self.y / l)

    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector") -> float:
        return self.x * other.y - self.y * other.x

    def perpendicular_left(self) -> "Vector":
        return Vector(-self.y, self.x)

    def perpendicular_right(self) -> "Vector":
        return Vector(self.y, -self.x)

    def scale(self, value: float) -> "Vector":
        return Vector(self.x * value, self.y * value)

    def to_point(self) -> Point:
        return Point(self.x, self.y)
