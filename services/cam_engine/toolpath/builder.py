from __future__ import annotations

from .toolpath import ToolPath
from .commands import RapidMove, LinearMove, ArcMove
from ..geometry import Line, Arc, Contour

class ToolPathBuilder:
    """
    Converts geometry into machining commands.
    """

    def build_contour(self, contour: Contour, feed: float) -> ToolPath:
        toolpath = ToolPath()

        if len(contour) == 0:
            return toolpath

        toolpath.add(RapidMove(contour.start))

        for entity in contour:
            if isinstance(entity, Line):
                toolpath.add(LinearMove(entity.end, feed))
            elif isinstance(entity, Arc):
                toolpath.add(
                    ArcMove(
                        target=entity.end,
                        center=entity.center,
                        clockwise=entity.clockwise,
                        feed=feed,
                    )
                )

        return toolpath
