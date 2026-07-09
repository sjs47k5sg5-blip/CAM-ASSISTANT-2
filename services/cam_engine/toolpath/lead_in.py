from __future__ import annotations

from dataclasses import dataclass

from ..geometry import Point

@dataclass(slots=True)
class LeadIn:
    length: float = 5.0

    def build(self, start: Point) -> Point:
        """
        Simple linear lead-in.
        """
        return Point(start.x - self.length, start.y)
