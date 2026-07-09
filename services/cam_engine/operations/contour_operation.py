from __future__ import annotations

from dataclasses import dataclass

from ..geometry import Contour
from ..engine import CamEngine

@dataclass(slots=True)
class ContourOperation:
    contour: Contour
    feed: float
    total_depth: float
    step_down: float
    finish_allowance: float = 0.0

    def generate(self):
        engine = CamEngine()
        return engine.generate_gcode(
            contour=self.contour,
            feed=self.feed,
            total_depth=self.total_depth,
            step_down=self.step_down,
        )
