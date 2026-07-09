from __future__ import annotations

from dataclasses import dataclass
from .entity import Entity
from .point import Point
from .bbox import BoundingBox

@dataclass(slots=True,frozen=True)
class Line(Entity):
    start: Point
    end: Point

    def copy(self)->"Line":
        return Line(self.start.copy(), self.end.copy())

    def length(self)->float:
        return self.start.distance_to(self.end)

    def bbox(self)->BoundingBox:
        return BoundingBox.from_points(self.start,self.end)

    def translate(self,dx:float,dy:float)->"Line":
        return Line(self.start.translate(dx,dy), self.end.translate(dx,dy))

    def rotate(self,angle_deg:float,origin:Point|None=None)->"Line":
        return Line(
            self.start.rotate(angle_deg,origin),
            self.end.rotate(angle_deg,origin)
        )

    @property
    def midpoint(self)->Point:
        return self.start.midpoint(self.end)

    @property
    def dx(self)->float:
        return self.end.x-self.start.x

    @property
    def dy(self)->float:
        return self.end.y-self.start.y
