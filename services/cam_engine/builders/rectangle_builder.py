from __future__ import annotations

from ..geometry import Point, Line, Arc, Contour

class RectangleBuilder:
    def build(self,size_x:float,size_y:float,zero:str="CENTER",radius:float=0.0):
        if zero=="CENTER":
            x0=-size_x/2; y0=-size_y/2
        else:
            x0=0; y0=0
        x1=x0+size_x; y1=y0+size_y
        r=max(0.0,min(radius,size_x/2,size_y/2))
        if r<=0:
            ents=[
                Line(Point(x0,y0),Point(x1,y0)),
                Line(Point(x1,y0),Point(x1,y1)),
                Line(Point(x1,y1),Point(x0,y1)),
                Line(Point(x0,y1),Point(x0,y0)),
            ]
            return Contour(ents)
        p1=Point(x0+r,y0); p2=Point(x1-r,y0); p3=Point(x1,y0+r); p4=Point(x1,y1-r)
        p5=Point(x1-r,y1); p6=Point(x0+r,y1); p7=Point(x0,y1-r); p8=Point(x0,y0+r)
        ents=[
            Line(p1,p2),
            Arc(p2,p3,Point(x1-r,y0+r),False),
            Line(p3,p4),
            Arc(p4,p5,Point(x1-r,y1-r),False),
            Line(p5,p6),
            Arc(p6,p7,Point(x0+r,y1-r),False),
            Line(p7,p8),
            Arc(p8,p1,Point(x0+r,y0+r),False),
        ]
        return Contour(ents)
