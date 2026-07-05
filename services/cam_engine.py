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
# CHAMFER PATH (REAL GEOMETRY)
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
# FANUC ARC (G2 / G3 with I/J)
# =========================
def arc_g2(x, y, r):
    """
    Simplified Fanuc quarter arc
    I = X center offset
    J = Y center offset
    """

    i = -r
    j = 0

    return f"G2 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}"


def arc_g3(x, y, r):
    i = 0
    j = -r

    return f"G3 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}"


# =========================
# MAIN CAM ENGINE
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

    # TOOL OFFSET SIM
    offset = tool / 2
    x -= offset
    y -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(CORNER={corner_type} R={r})")

    # =========================
    # SELECT GEOMETRY
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

    # =========================
    # START POSITION
    # =========================
    sx, sy = path[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    # =========================
    # ROUGHING PASS
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
    # RADIAL CORNER (REAL G2/G3)
    # =========================
    if use_arc:
        g.append("(RADIUS MODE G2)")

        # bottom-right arc example
        g.append(arc_g2(x, y, r))

        # optional opposite arc (for realism)
        g.append(arc_g3(0, y, r))

    # =========================
    # FINISH PASS
    # =========================
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth:.3f} F80")

        for px, py in path:
            g.append(f"G1 X{px:.3f} Y{py:.3f} F120")

    # =========================
    # SAFE EXIT (FANUC)
    # =========================
    g.append("G0 Z100")
    g.append("G53 Z0 Y0")

    g.append("M5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)