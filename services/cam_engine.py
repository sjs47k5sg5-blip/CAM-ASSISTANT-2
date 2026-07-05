import math


def f(v):
    try:
        return float(v)
    except:
        return 0.0


# =========================
# ZERO SYSTEM
# =========================
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
    # HEADER FANUC
    # =========================
    g.append("%")
    g.append("G21 G90 G17")
    g.append("G54")

    g.append(f"T{tool} M6")
    g.append("M3 S1200")

    # TOOL LENGTH COMP
    g.append(f"G0 G43 Z100 H{tool}")
    g.append("G0 Z5")

    # =========================
    # WCS
    # =========================
    xo, yo = apply_zero(x, y, zero)

    offset = tool / 2
    xo -= offset
    yo -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(SIZE X={xo:.3f} Y={yo:.3f})")

    # =========================
    # TOOLPATH
    # =========================
    if corner_type == "ФАСКА":
        path = chamfer(xo, yo, r)
        use_comp = False

    elif corner_type == "РАДИУС":
        path = rect(xo, yo)
        use_comp = True

    else:
        path = rect(xo, yo)
        use_comp = False

    # =========================
    # START POINT
    # =========================
    sx, sy = path[0]

    # =========================
    # COMPENSATION START (G41/G42 + D)
    # =========================
    if use_comp:
        g.append(f"G1 X{sx:.3f} Y{sy:.3f} F200")
        g.append(f"G41 D{tool}")

    else:
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
    # FINISH PASS
    # =========================
    if allowance > 0:
        g.append("(FINISH)")
        g.append(f"G1 Z{-depth:.3f} F80")

        for px, py in path:
            g.append(f"G1 X{px:.3f} Y{py:.3f}")

    # =========================
    # CANCEL COMPENSATION
    # =========================
    if use_comp:
        g.append("G40")

    # =========================
    # SAFE EXIT
    # =========================
    g.append("G0 Z100")
    g.append("G53 Z0 Y0")

    g.append("M5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)