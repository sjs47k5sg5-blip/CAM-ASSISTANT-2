from __future__ import annotations

from dataclasses import dataclass
from math import pi

from .entity import Entity
from .point import Point
from .bbox import BoundingBox


@dataclass(slots=True, frozen=True)
class Circle(Entity):
    center: Point
    radius: float

    @property
    def start(self) -> Point:
        return Point(self.center.x + self.radius, self.center.y)

    @property
    def end(self) -> Point:
        return self.start

    def copy(self) -> "Circle":
        return Circle(self.center.copy(), self.radius)

    def length(self) -> float:
        return 2.0 * pi * self.radius

    def area(self) -> float:
        return pi * self.radius * self.radius

    def bbox(self) -> BoundingBox:
        return BoundingBox(
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.center.x + self.radius,
            self.center.y + self.radius,
        )

    def translate(self, dx: float, dy: float) -> "Circle":
        return Circle(self.center.translate(dx, dy), self.radius)

    def rotate(self, angle_deg: float, origin: Point | None = None) -> "Circle":
        return Circle(self.center.rotate(angle_deg, origin), self.radius)

    def contains(self, point: Point, eps: float = 1e-9) -> bool:
        return abs(self.center.distance_to(point) - self.radius) <= eps
