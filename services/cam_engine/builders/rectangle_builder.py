from __future__ import annotations

from ..geometry import Point, Line, Contour


class RectangleBuilder:
    """
    Builds a rectangular contour from workpiece dimensions.
    """

    def build(self, size_x: float, size_y: float, zero: str = "CENTER"):
        if zero == "CENTER":
            x0 = -size_x / 2
            y0 = -size_y / 2
        else:
            x0 = 0
            y0 = 0

        x1 = x0 + size_x
        y1 = y0 + size_y

        points = [
            Point(x0, y0),
            Point(x1, y0),
            Point(x1, y1),
            Point(x0, y1),
            Point(x0, y0),
        ]

        entities = [
            Line(points[i], points[i + 1])
            for i in range(len(points) - 1)
        ]

        return Contour(entities)
