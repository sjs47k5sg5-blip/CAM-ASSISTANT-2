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
# RECT BASE
# =========================
def rect(x, y, r):
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
# ARC (SAFE I/J)
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
# TOOLPATH SELECTOR (CRITICAL FIX)
# =========================
def build_path(x, y, r, mode):

    # 🔥 FIX: only ONE active path (no duplication)

    if mode == "РАДИУС":
        return rect(x, y, r), "ARC"

    else:
        return rect(x, y, r), "LINE"


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
    # ZERO APPLY
    # =========================
    xo, yo = apply_zero(x, y, zero)

    offset = tool / 2
    xo -= offset
    yo -= offset

    g.append(f"(MODE={corner_type})")
    g.append(f"(R={r})")

    # =========================
    # SINGLE PATH ONLY (IMPORTANT FIX)
    # =========================
    path, mode = build_path(xo, yo, r, corner_type)

    # =========================
    # START
    # =========================
    sx, sy = path[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    # =========================
    # ROUGHING (ONLY ONCE)
    # =========================
    z = 0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z:.3f} F120")

        for p in path:
            g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

    # =========================
    # TOOLPATH EXECUTION (NO DUPLICATE)
    # =========================
    if mode == "ARC":

        g.append("(CLEAN ARC MODE - NO DUPLICATES)")

        for i in range(len(path) - 1):
            cmd = arc(path[i], path[i + 1], r)
            if cmd:
                g.append(cmd)

        cmd = arc(path[-1], path[0], r)
        if cmd:
            g.append(cmd)

    # =========================
    # FINISH PASS (ONLY IF ALLOWANCE)
    # =========================
    if allowance > 0:
        g.append("(FINISH ONLY)")

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