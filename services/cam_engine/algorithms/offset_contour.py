from __future__ import annotations

from ..geometry import Contour, Line
from .offset import offset_line

def offset_contour(contour: Contour, distance: float):
    """
    First implementation of contour offset.

    Offsets every line entity independently.
    Arc support and corner stitching will be added
    in the next stages.
    """
    result = contour.copy()

    entities = []

    for entity in contour:
        if isinstance(entity, Line):
            entities.append(offset_line(entity, distance))
        else:
            entities.append(entity.copy())

    result.entities = entities
    return result
