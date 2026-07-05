import math


# =========================
# GEOMETRY ENGINE CORE
# =========================

def offset_rect(x, y, offset):
    return [
        (offset, offset),
        (x - offset, offset),
        (x - offset, y - offset),
        (offset, y - offset),
        (offset, offset)
    ]


def chamfer_rect(x, y, c):
    return [
        (c, 0),
        (x - c, 0),
        (x, c),
        (x, y - c),
        (x - c, y),
        (0, y - c),
        (0, c),
        (c, 0)
    ]


def radius_rect(x, y, r):
    # simplified arc representation (real CAM would split into G2/G3)
    return [
        (r, 0),
        (x - r, 0),
        (x, r),
        (x, y - r),
        (x - r, y),
        (0, y - r),
        (0, r),
        (r, 0)
    ]


# =========================
# ZERO SYSTEM
# =========================

def apply_zero(x, y, zero, sx, sy):

    if zero == "CENTER":
        return x - sx/2, y - sy/2
    if zero == "TL":
        return x, y
    if zero == "TR":
        return x - sx, y
    if zero == "BL":
        return x, y - sy
    if zero == "BR":
        return x - sx, y - sy

    return x, y


# =========================
# TOOLPATH GENERATOR
# =========================

def generate_toolpath(x, y, depth, stepdown, tool, zero, allowance, corner_type, corner_value):

    g = []

    g.append("G21 G90")
    g.append("G0 Z5")
    g.append(f"T{tool} M6")

    # tool offset
    offset = tool / 2

    # base geometry selection
    if corner_type == "ФАСКА":
        path = chamfer_rect(x, y, corner_value)
    elif corner_type == "РАДИУС":
        path = radius_rect(x, y, corner_value)
    else:
        path = offset_rect(x, y, offset)

    # move to start
    sx, sy = path[0]
    g.append(f"G0 X{sx} Y{sy}")

    # depth passes
    z = 0
    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z} F120")

        for px, py in path:
            g.append(f"G1 X{px} Y{py} F200")

    # finish pass
    if allowance > 0:
        g.append("(FINISH PASS)")
        for px, py in path:
            g.append(f"G1 X{px} Y{py} F120")

    g.append("G0 Z5")
    g.append("M30")

    return "\n".join(g)