from __future__ import annotations

from .toolpath import ToolPath
from .commands import RapidMove, LinearMove, ArcMove
from ..geometry import Line, Arc

class ToolPathBuilder:
    def build_contour(self, contour, feed, z_levels=None):
        path = ToolPath()
        if contour is None:
            return path
        entities=list(contour)
        if not entities:
            return path
        if z_levels is None:
            z_levels=[0.0]

        for z in z_levels:
            first=entities[0]
            path.add(RapidMove(first.start))
            try:
                path.add(LinearMove(first.start, feed, z=z))
            except TypeError:
                path.add(LinearMove(first.start, feed))
            for e in entities:
                if isinstance(e, Line):
                    try:
                        path.add(LinearMove(e.end, feed, z=z))
                    except TypeError:
                        path.add(LinearMove(e.end, feed))
                elif isinstance(e, Arc):
                    try:
                        path.add(ArcMove(target=e.end, center=e.center, clockwise=e.clockwise, feed=feed, z=z))
                    except TypeError:
                        path.add(ArcMove(target=e.end, center=e.center, clockwise=e.clockwise, feed=feed))
        return path
