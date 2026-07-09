from __future__ import annotations

from dataclasses import dataclass
from ..geometry import Point

@dataclass(slots=True)
class RapidMove:
    target: Point

@dataclass(slots=True)
class LinearMove:
    target: Point
    feed: float

@dataclass(slots=True)
class ArcMove:
    target: Point
    center: Point
    clockwise: bool
    feed: float

@dataclass(slots=True)
class ToolChange:
    tool: int

@dataclass(slots=True)
class SpindleCommand:
    rpm: int
    clockwise: bool=True

@dataclass(slots=True)
class CoolantCommand:
    enabled: bool=True
