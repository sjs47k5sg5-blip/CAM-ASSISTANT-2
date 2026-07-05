import math


def f(v):
    try:
        return float(v)
    except:
        return 0.0


# =========================
# ZERO SYSTEM (FIXED WCS)
# =========================
def apply_zero(x, y, mode):

    x = f(x)
    y = f(y)

    # CENTER = origin in middle
    if mode == "CENTER":
        return -x / 2, -y / 2

    # LEFT TOP
    if mode == "TL":
        return 0, y

    # RIGHT TOP
    if mode == "TR":
        return x, y

    # LEFT BOTTOM
    if mode == "BL":
        return 0, 0

    # RIGHT BOTTOM
    if mode == "BR":
        return x, 0

    return 0, 0


# =========================
# RECT PATH
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
# CHAMFER (REAL GEOMETRY)
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
# FANUC ARC (I/J)
# =========================
def g2(x, y, i, j):
    return f"G2 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}"


# =========================
# MAIN ENGINE
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
    tool = int(f(tool))
    allowance = f(allowance)
    r = f(corner_value)

    g = []

    # =========================
    # HEADER (FANUC STYLE)
    # =========================
    g.append("%")
    g.append("G21 G90 G17")
    g.append("G54")

    g.append(f"T{tool} M6")
    g.append("M3 S1200")

    g.append(f"G0 G43 Z100 H{tool}")
    g.append("G0 Z5")

    # =========================
    # APPLY WCS ZERO FIX
    # =========================
    xo, yo = apply_zero(x, y, zero)

    # tool offset
    offset = tool / 2

    xo -= offset
    yo -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(WCS OFFSET X={xo:.3f} Y={yo:.3f})")

    # =========================
    # PATH SELECT
    # =========================
    if corner_type == "ФАСКА":
        path = chamfer(xo, yo, r)
    else:
        path = rect(xo, yo)

    # =========================
    # START
    # =========================
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

        for px, py in path:
            g.append(f"G1 X{px:.3f} Y{py:.3f} F250")

    # =========================
    # RADIUS MODE (REAL G2)
    # =========================
    if corner_type == "РАДИУС":

        g.append("(RADIUS MODE G2)")

        # simple corner arc example
        g.append(g2(xo - r, yo, -r, 0))

    # =========================
    # FINISH
    # =========================
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth:.3f} F80")

        for px, py in path:
            g.append(f"G1 X{px:.3f} Y{py:.3f}")

    # =========================
    # END FANUC
    # =========================
    g.append("G0 Z100")
    g.append("G53 Z0 Y0")

    g.append("M5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)