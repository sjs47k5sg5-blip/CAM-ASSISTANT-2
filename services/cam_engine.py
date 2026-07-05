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
# ARC ENGINE (REAL I/J)
# =========================
def arc(p1, p2, r):

    x1, y1 = p1
    x2, y2 = p2

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return None

    ux = -dy / dist
    uy = dx / dist

    h = math.sqrt(max(r * r - (dist / 2) ** 2, 0))

    cx = mx + ux * h
    cy = my + uy * h

    i = cx - x1
    j = cy - y1

    return f"G2 X{x2:.3f} Y{y2:.3f} I{i:.3f} J{j:.3f}"


# =========================
# RADIUS PATH
# =========================
def radius_path(x, y, r):

    return [
        (r, 0),
        (x - r, 0),
        (x, r),
        (x, y - r),
        (x - r, y),
        (r, y),
        (0, y - r),
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

    g.append(f"G0 G43 Z100 H{tool}")
    g.append("G0 Z5")

    # =========================
    # WCS APPLY
    # =========================
    xo, yo = apply_zero(x, y, zero)

    offset = tool / 2
    xo -= offset
    yo -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(SIZE X={xo:.3f} Y={yo:.3f})")

    # =========================
    # PATH SELECT
    # =========================
    base = rect(xo, yo)

    # =========================
    # START POSITION
    # =========================
    sx, sy = base[0]

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

        for p in base:
            g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

    # =========================
    # RADIUS MODE (FULL FIX)
    # =========================
    if corner_type == "РАДИУС":

        g.append("(INDUSTRIAL RADIUS + G41 SAFE ENTRY)")

        pts = radius_path(xo, yo, r)

        # =========================
        # LEAD-IN (IMPORTANT FIX)
        # =========================
        lead_x = pts[0][0] - 5
        lead_y = pts[0][1]

        g.append(f"G1 X{lead_x:.3f} Y{lead_y:.3f} F200")
        g.append("G41 D1")  # tool radius compensation

        g.append(f"G1 X{pts[0][0]:.3f} Y{pts[0][1]:.3f} F200")

        # contour
        for i in range(len(pts) - 1):
            g.append(arc(pts[i], pts[i + 1], r))

        # close
        g.append(arc(pts[-1], pts[0], r))

        g.append("G40")

    # =========================
    # FINISH PASS
    # =========================
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth:.3f} F80")

        for p in base:
            g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f}")

    # =========================
    # SAFE EXIT
    # =========================
    g.append("G0 Z100")
    g.append("G53 Z0 Y0")

    g.append("M5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)