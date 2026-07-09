from __future__ import annotations

from ..geometry import Line, Point

def line_line_intersection(a: Line, b: Line) -> Point | None:
    x1,y1=a.start.x,a.start.y
    x2,y2=a.end.x,a.end.y
    x3,y3=b.start.x,b.start.y
    x4,y4=b.end.x,b.end.y

    den=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if abs(den)<1e-9:
        return None

    px=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/den
    py=((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/den
    return Point(px,py)
