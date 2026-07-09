from __future__ import annotations

from dataclasses import dataclass

from ..geometry import Point

@dataclass(slots=True)
class LeadOut:
    length: float = 5.0

    def build(self, end: Point) -> Point:
        """
        Simple linear lead-out.
        """
        return Point(end.x + self.length, end.y)
