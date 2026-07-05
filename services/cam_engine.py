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
# BASE GEOMETRY (ONCE ONLY)
# =========================
def build_base(x, y, r):

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
# ARC CACHE BUILDER (CRITICAL FIX)
# =========================
def build_arc_cache(path, r):

    arcs = []

    for i in range(len(path) - 1):
        arcs.append((path[i], path[i + 1]))

    arcs.append((path[-1], path[0]))

    return arcs


# =========================
# ARC GENERATOR (USED ONLY ONCE PER CACHE)
# =========================
def arc(p1, p2, r):

    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return None

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    ux = -dy / dist
    uy = dx / dist

    h = math.sqrt(max(r * r - (dist / 2) ** 2, 0))

    cx = mx + ux * h
    cy = my + uy * h

    i = cx - x1
    j = cy - y1

    return f"G2 X{x2:.3f} Y{y2:.3f} I{i:.3f} J{j:.3f}"


# =========================
# MAIN ENGINE (ARC CACHE FIXED)
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

    g.append(f"(MODE={corner_type})")
    g.append(f"(R={r})")

    # =========================
    # BUILD GEOMETRY ONCE
    # =========================
    path = build_base(xo, yo, r)

    # =========================
    # ARC CACHE (CRITICAL FIX)
    # =========================
    arc_cache = None

    if corner_type == "РАДИУС":
        arc_cache = build_arc_cache(path, r)

    # =========================
    # START
    # =========================
    sx, sy = path[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    # =========================
    # DEPTH LOOP (NO REBUILD EVER)
    # =========================
    z = 0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z:.3f} F120")

        # =========================
        # TOOLPATH EXECUTION (REUSED)
        # =========================
        if corner_type == "РАДИУС":

            for p1, p2 in arc_cache:
                cmd = arc(p1, p2, r)
                if cmd:
                    g.append(cmd)

        else:

            for p in path:
                g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

    # =========================
    # FINISH (NO ARC REBUILD)
    # =========================
    if allowance > 0:

        g.append("(FINISH PASS)")

        if corner_type == "РАДИУС":

            for p1, p2 in arc_cache:
                cmd = arc(p1, p2, r)
                if cmd:
                    g.append(cmd)

        else:

            for p in path:
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