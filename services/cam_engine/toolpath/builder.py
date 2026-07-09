from __future__ import annotations

from .toolpath import ToolPath
from .commands import RapidMove, LinearMove, ArcMove
from ..geometry import Line, Arc

class ToolPathBuilder:
    def build_contour(self, contour, feed):
        path = ToolPath()
        if contour is None:
            return path
        entities = list(contour)
        if not entities:
            return path
        first = entities[0]
        path.add(RapidMove(first.start))
        for entity in entities:
            if isinstance(entity, Line):
                path.add(LinearMove(entity.end, feed))
            elif isinstance(entity, Arc):
                path.add(
                    ArcMove(
                        target=entity.end,
                        center=entity.center,
                        clockwise=entity.clockwise,
                        feed=feed,
                    )
                )
        return path
