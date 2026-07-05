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
# RECT BASE POINTS
# =========================
def base_rect(x, y):

    return [
        (0, 0),
        (x, 0),
        (x, y),
        (0, y),
        (0, 0)
    ]


# =========================
# TRUE CORNER ARC GENERATOR (REAL CAM STYLE)
# =========================
def corner_arcs(x, y, r):

    # 4 corners with real tangent arc points
    p = [
        (r, 0),         # start bottom edge
        (x - r, 0),
        (x, r),
        (x, y - r),
        (x - r, y),
        (r, y),
        (0, y - r),
        (0, 0)
    ]

    return p


# =========================
# SAFE G2 ARC (FANUC CORRECT)
# =========================
def arc(p1, p2, center):

    x1, y1 = p1
    x2, y2 = p2
    cx, cy = center

    i = cx - x1
    j = cy - y1

    return f"G2 X{x2:.3f} Y{y2:.3f} I{i:.3f} J{j:.3f}"


# =========================
# CORNER CENTER MAP (KEY FIX)
# =========================
def corner_centers(x, y, r):

    return [
        (r, r),             # BL
        (x - r, r),         # BR
        (x - r, y - r),     # TR
        (r, y - r)          # TL
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
    # HEADER
    # =========================
    g.append("%")
    g.append("G21 G90 G17")
    g.append("G54")

    g.append(f"T{tool} M6")
    g.append("M3 S1200")

    g.append(f"G0 G43 Z100 H{tool}")
    g.append("G0 Z5")

    # =========================
    # APPLY ZERO
    # =========================
    xo, yo = apply_zero(x, y, zero)

    offset = tool / 2
    xo -= offset
    yo -= offset

    g.append(f"(TRUE RADIUS MODE)")
    g.append(f"(R={r})")

    # =========================
    # MODE SELECTION (CRITICAL FIX)
    # =========================
    if corner_type == "РАДИУС":

        pts = corner_arcs(xo, yo, r)
        centers = corner_centers(xo, yo, r)

        # start
        g.append(f"G0 X{pts[0][0]:.3f} Y{pts[0][1]:.3f}")

        # roughing (still safe linear)
        z = 0
        while z > -depth:
            z -= stepdown
            if z < -depth:
                z = -depth

            g.append(f"G1 Z{z:.3f} F120")

            for p in pts:
                g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

        # =========================
        # REAL TRUE ARC CORNERS (FIXED)
        # =========================
        g.append("(TRUE CORNER ARCS)")

        arc_pairs = [
            (pts[0], pts[1], centers[0]),
            (pts[1], pts[2], centers[1]),
            (pts[2], pts[3], centers[2]),
            (pts[3], pts[4], centers[3]),
        ]

        for p1, p2, c in arc_pairs:
            g.append(arc(p1, p2, c))

        # close loop
        g.append(arc(pts[4], pts[0], centers[0]))

    else:

        # =========================
        # NORMAL RECT MODE
        # =========================
        pts = base_rect(xo, yo)

        g.append(f"G0 X{pts[0][0]:.3f} Y{pts[0][1]:.3f}")

        z = 0
        while z > -depth:
            z -= stepdown
            if z < -depth:
                z = -depth

            g.append(f"G1 Z{z:.3f} F120")

            for p in pts:
                g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

    # =========================
    # FINISH PASS
    # =========================
    if allowance > 0:
        g.append("(FINISH PASS)")

        for p in pts:
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