from __future__ import annotations

from dataclasses import dataclass

from .point import Point
from .bbox import BoundingBox


@dataclass(slots=True, frozen=True)
class Rectangle:
    origin: Point
    width: float
    height: float

    @property
    def min_x(self) -> float:
        return self.origin.x

    @property
    def min_y(self) -> float:
        return self.origin.y

    @property
    def max_x(self) -> float:
        return self.origin.x + self.width

    @property
    def max_y(self) -> float:
        return self.origin.y + self.height

    @property
    def center(self) -> Point:
        return Point(
            self.origin.x + self.width / 2.0,
            self.origin.y + self.height / 2.0,
        )

    def bbox(self) -> BoundingBox:
        return BoundingBox(
            self.min_x,
            self.min_y,
            self.max_x,
            self.max_y,
        )

    def contains(self, point: Point) -> bool:
        return (
            self.min_x <= point.x <= self.max_x and
            self.min_y <= point.y <= self.max_y
        )

    def translate(self, dx: float, dy: float) -> "Rectangle":
        return Rectangle(
            self.origin.translate(dx, dy),
            self.width,
            self.height,
        )
