import math


# =========================
# SAFE CONVERT
# =========================
def f(v):
    try:
        return float(v)
    except:
        return 0.0


# =========================
# RECT
# =========================
def rect(x, y):
    return [
        (0, 0),
        (x, 0),
        (x, y),
        (0, y),
        (0, 0)
    ]


# =========================
# CHAMFER
# =========================
def chamfer(x, y, c):
    return [
        (c, 0),
        (x - c, 0),
        (x, c),
        (x, y - c),
        (x - c, y),
        (0, y - c),
        (0, 0)
    ]


# =========================
# FANUC ARC (G2/G3)
# =========================
def arc_fanuc(x, y, r):

    # 4-corner arc approximation with I/J centers
    # simplified full-round rectangle

    return {
        "type": "ARC",
        "start": (r, 0),
        "end": (0, r),
        "center_i": -r,
        "center_j": 0
    }


# =========================
# TOOLPATH ENGINE
# =========================
def contour(
    x,
    y,
    depth,
    stepdown,
    tool,
    zero,
    allowance,
    step,
    corner_type,
    corner_value
):

    x = f(x)
    y = f(y)
    depth = abs(f(depth))
    stepdown = abs(f(stepdown))
    tool = f(tool)
    allowance = f(allowance)
    r = f(corner_value)

    g = []

    # HEADER
    g.append("%")
    g.append("G21 G90 G17")
    g.append("G0 Z5")
    g.append(f"T{int(tool)} M6")

    offset = tool / 2
    x -= offset
    y -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(TYPE={corner_type})")

    # =========================
    # PATH SELECTION
    # =========================
    if corner_type == "ФАСКА":
        path = chamfer(x, y, r)
        use_arc = False

    elif corner_type == "РАДИУС":
        path = rect(x, y)
        use_arc = True

    else:
        path = rect(x, y)
        use_arc = False

    # START
    sx, sy = path[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    # =========================
    # ROUGHING
    # =========================
    z = 0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z:.3f} F120")

        for i in range(len(path)):
            x1, y1 = path[i]
            g.append(f"G1 X{x1:.3f} Y{y1:.3f} F250")

    # =========================
    # FANUC ARC MODE
    # =========================
    if use_arc:
        g.append("(G2 ARC MODE)")

        # simple 1/4 arc example with I/J
        g.append(f"G2 X{x:.3f} Y{y:.3f} I{-r:.3f} J0.000 F200")

    # FINISH PASS
    if allowance > 0:
        g.append("(FINISH)")
        for x1, y1 in path:
            g.append(f"G1 X{x1:.3f} Y{y1:.3f} F120")

    # END
    g.append("G0 Z5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)