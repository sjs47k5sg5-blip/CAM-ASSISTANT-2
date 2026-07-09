from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, hypot, radians

EPS = 1e-9

@dataclass(slots=True,frozen=True)
class Point:
    x: float
    y: float

    def copy(self)->"Point":
        return Point(self.x,self.y)

    def to_tuple(self)->tuple[float,float]:
        return (self.x,self.y)

    @classmethod
    def from_tuple(cls,v:tuple[float,float])->"Point":
        return cls(v[0],v[1])

    def distance_to(self, other:"Point")->float:
        return hypot(other.x-self.x, other.y-self.y)

    def translate(self, dx:float, dy:float)->"Point":
        return Point(self.x+dx, self.y+dy)

    def rotate(self, angle_deg:float, origin:"Point|None"=None)->"Point":
        if origin is None:
            origin = Point(0.0,0.0)
        a=radians(angle_deg)
        x=self.x-origin.x
        y=self.y-origin.y
        xr=x*cos(a)-y*sin(a)
        yr=x*sin(a)+y*cos(a)
        return Point(xr+origin.x, yr+origin.y)

    def midpoint(self, other:"Point")->"Point":
        return Point((self.x+other.x)/2,(self.y+other.y)/2)

    def __add__(self, other):
        try:
            return Point(self.x+other.x,self.y+other.y)
        except AttributeError:
            return NotImplemented

    def __sub__(self, other):
        try:
            return Point(self.x-other.x,self.y-other.y)
        except AttributeError:
            return NotImplemented

    def __mul__(self, value:float):
        return Point(self.x*value,self.y*value)

    __rmul__=__mul__

    def __truediv__(self, value:float):
        return Point(self.x/value,self.y/value)

    def almost_equals(self, other:"Point", eps:float=EPS)->bool:
        return abs(self.x-other.x)<=eps and abs(self.y-other.y)<=eps
