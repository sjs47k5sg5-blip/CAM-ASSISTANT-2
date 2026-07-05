from dataclasses import dataclass
from typing import Tuple

Point = Tuple[float, float]


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Arc:
    start: Point
    end: Point
    center: Point
    clockwise: bool


@dataclass
class Circle:
    center: Point
    radius: float


@dataclass
class Polyline:
    entities: list