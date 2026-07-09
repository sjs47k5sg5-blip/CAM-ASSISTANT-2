from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, sin, pi

from .entity import Entity
from .point import Point
from .bbox import BoundingBox


@dataclass(slots=True,frozen=True)
class Arc(Entity):
    start: Point
    end: Point
    center: Point
    clockwise: bool=False

    @property
    def radius(self)->float:
        return self.center.distance_to(self.start)

    @property
    def start_angle(self)->float:
        return atan2(self.start.y-self.center.y,self.start.x-self.center.x)

    @property
    def end_angle(self)->float:
        return atan2(self.end.y-self.center.y,self.end.x-self.center.x)

    def copy(self)->"Arc":
        return Arc(self.start.copy(),self.end.copy(),self.center.copy(),self.clockwise)

    def length(self)->float:
        a1=self.start_angle
        a2=self.end_angle
        if self.clockwise:
            if a1<a2:
                a1+=2*pi
            sweep=a1-a2
        else:
            if a2<a1:
                a2+=2*pi
            sweep=a2-a1
        return self.radius*sweep

    def bbox(self)->BoundingBox:
        return BoundingBox.from_points(self.start,self.end,self.center)

    def translate(self,dx:float,dy:float)->"Arc":
        return Arc(self.start.translate(dx,dy),self.end.translate(dx,dy),self.center.translate(dx,dy),self.clockwise)

    def rotate(self,angle_deg:float,origin:Point|None=None)->"Arc":
        return Arc(self.start.rotate(angle_deg,origin),self.end.rotate(angle_deg,origin),self.center.rotate(angle_deg,origin),self.clockwise)

    def point_at_angle(self,angle:float)->Point:
        return Point(self.center.x+self.radius*cos(angle),self.center.y+self.radius*sin(angle))
