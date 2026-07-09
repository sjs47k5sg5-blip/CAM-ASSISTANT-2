from __future__ import annotations

from dataclasses import dataclass

from .point import Point

@dataclass(slots=True)
class BoundingBox:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @classmethod
    def from_points(cls, *points: Point) -> "BoundingBox":
        if not points:
            raise ValueError("At least one point is required.")
        return cls(
            min(p.x for p in points),
            min(p.y for p in points),
            max(p.x for p in points),
            max(p.y for p in points),
        )

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def center(self) -> Point:
        return Point(
            (self.min_x + self.max_x) / 2.0,
            (self.min_y + self.max_y) / 2.0,
        )

    def contains(self, point: Point) -> bool:
        return (
            self.min_x <= point.x <= self.max_x
            and self.min_y <= point.y <= self.max_y
        )

    def expand(self, value: float) -> "BoundingBox":
        return BoundingBox(
            self.min_x - value,
            self.min_y - value,
            self.max_x + value,
            self.max_y + value,
        )

    def union(self, other: "BoundingBox") -> "BoundingBox":
        return BoundingBox(
            min(self.min_x, other.min_x),
            min(self.min_y, other.min_y),
            max(self.max_x, other.max_x),
            max(self.max_y, other.max_y),
        )
