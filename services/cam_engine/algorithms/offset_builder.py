from __future__ import annotations

from ..geometry import Arc, Line, Contour
from .offset import offset_line

def offset_entities(entities:list, distance:float)->list:
    """
    Offsets supported entities.
    Current version supports Line, copies Arc unchanged.
    """
    result=[]
    for entity in entities:
        if isinstance(entity, Line):
            result.append(offset_line(entity,distance))
        elif isinstance(entity, Arc):
            result.append(entity.copy())
        else:
            result.append(entity.copy())
    return result

def offset_closed_contour(contour:Contour, distance:float)->Contour:
    new_contour=contour.copy()
    new_contour.entities=offset_entities(list(contour),distance)
    return new_contour
