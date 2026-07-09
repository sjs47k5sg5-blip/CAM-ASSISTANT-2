from __future__ import annotations

from dataclasses import dataclass
from ..geometry import Point


@dataclass(slots=True)
class RapidMove:
    target: Point
    z: float | None = None


@dataclass(slots=True)
class LinearMove:
    target: Point
    feed: float
    z: float | None = None


@dataclass(slots=True)
class ArcMove:
    target: Point
    center: Point
    clockwise: bool
    feed: float
    z: float | None = None


@dataclass(slots=True)
class ToolChange:
    tool: int


@dataclass(slots=True)
class SpindleCommand:
    rpm: int
    clockwise: bool = True


@dataclass(slots=True)
class CoolantCommand:
    enabled: bool = True
