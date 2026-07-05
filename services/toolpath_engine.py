
import math

class ToolpathEngine:

    def contour(self, w, h, o=0.0):
        return [
            (o, o),
            (w-o, o),
            (w-o, h-o),
            (o, h-o),
            (o, o)
        ]

    def pocket(self, w, h, step=2.0):
        paths = []
        o = 0
        while w-2*o > 0 and h-2*o > 0:
            paths.append([
                (o,o),
                (w-o,o),
                (w-o,h-o),
                (o,h-o),
                (o,o)
            ])
            o += step
        return paths

    def fillet(self, x, y, r=1.0):
        pts = []
        for i in range(6):
            a = (math.pi/2)*(i/5)
            pts.append((x + r*math.cos(a), y + r*math.sin(a)))
        return pts
