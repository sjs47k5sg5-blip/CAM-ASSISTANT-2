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
# BASE GEOMETRY
# =========================
def base_path(x, y, r):

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
# ARC GENERATOR
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
# FINISH GEOMETRY (CRITICAL FIX)
# =========================
def finish_path(x, y, allowance):

    # 🔥 IMPORTANT:
    # finish is NOT same as rough
    offset = allowance

    return [
        (offset, offset),
        (x - offset, offset),
        (x - offset, y - offset),
        (offset, y - offset),
        (offset, offset)
    ]


# =========================
# MAIN ENGINE (V61 FIXED FINISH LOGIC)
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
    # ZERO
    # =========================
    xo, yo = apply_zero(x, y, zero)

    offset_tool = tool / 2
    xo -= offset_tool
    yo -= offset_tool

    g.append(f"(MODE={corner_type})")
    g.append(f"(R={r})")

    # =========================
    # ROUGH PATH (MAIN CUT)
    # =========================
    rough = base_path(xo, yo, r)

    # =========================
    # START POINT
    # =========================
    sx, sy = rough[0]
    g.append(f"G0 X{sx:.3f} Y{sy:.3f}")

    # =========================
    # ROUGHING (ONLY THIS PATH)
    # =========================
    z = 0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z:.3f} F120")

        if corner_type == "РАДИУС":

            for i in range(len(rough) - 1):
                cmd = arc(rough[i], rough[i + 1], r)
                if cmd:
                    g.append(cmd)

            cmd = arc(rough[-1], rough[0], r)
            if cmd:
                g.append(cmd)

        else:

            for p in rough:
                g.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F250")

    # =========================
    # TRUE FINISH (FIXED - NOT DUPLICATE)
    # =========================
    if allowance > 0:

        g.append("(TRUE FINISH PASS - OFFSET GEOMETRY)")

        fin = finish_path(xo, yo, allowance)

        if corner_type == "РАДИУС":

            for i in range(len(fin) - 1):
                cmd = arc(fin[i], fin[i + 1], r)
                if cmd:
                    g.append(cmd)

            cmd = arc(fin[-1], fin[0], r)
            if cmd:
                g.append(cmd)

        else:

            for p in fin:
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