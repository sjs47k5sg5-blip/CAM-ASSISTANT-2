import math


def f(v):
    try:
        return float(v)
    except:
        return 0.0


def apply_zero(x, y, mode):

    x = f(x)
    y = f(y)

    if mode == "CENTER":
        return -x / 2, -y / 2
    if mode == "TL":
        return 0, y
    if mode == "TR":
        return x, y
    if mode == "BL":
        return 0, 0
    if mode == "BR":
        return x, 0

    return 0, 0


def base_rect(x, y):
    return [(0,0),(x,0),(x,y),(0,y),(0,0)]


def radius_rect(x, y, r):
    r = min(r, x/2, y/2)
    return [(r,0),(x-r,0),(x,y-r),(x,y),(0,y),(0,r),(r,0)]


def chamfer_rect(x, y, c):
    c = min(c, x/2, y/2)
    return [(c,0),(x-c,0),(x,y-c),(x,y),(0,y),(0,c),(c,0)]


def contour(x, y, depth, stepdown, tool, zero, allowance, step, corner_type, corner_value):

    x = f(x)
    y = f(y)
    depth = abs(f(depth))
    stepdown = abs(f(stepdown))
    tool = int(f(tool))
    r = f(corner_value)

    g = []

    g.append("%")
    g.append("G21 G90 G17")
    g.append("G54")
    g.append(f"T{tool} M6")
    g.append("M3 S3000")

    xo, yo = apply_zero(x, y, zero)

    if "РАД" in (corner_type or "").upper():
        path = radius_rect(xo, yo, r)
    elif "ФАС" in (corner_type or "").upper():
        path = chamfer_rect(xo, yo, r)
    else:
        path = base_rect(xo, yo)

    sx, sy = path[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    z = 0
    while z > -depth:
        z -= stepdown
        g.append(f"G1 Z{z:.3f}")

        for p in path:
            g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f}")

    g.append("G0 Z100")
    g.append("M30")
    g.append("%")

    return "\n".join(g)