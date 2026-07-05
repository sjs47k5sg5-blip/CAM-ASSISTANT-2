def contour(x, y, depth, stepdown, tool, zero, allowance, step, corner_type, corner_value):

    g = []

    try:
        x = float(x)
        y = float(y)
        depth = float(depth)
    except:
        return "ERROR INPUT"

    g.append("G21 G90")
    g.append("G0 Z5")
    g.append(f"T{tool} M6")

    offset = tool / 2
    x -= offset
    y -= offset

    g.append(f"(ZERO={zero})")
    g.append(f"(CORNER={corner_type} {corner_value})")

    z = 0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z}")
        g.append(f"G1 X{x} Y0")
        g.append(f"G1 X{x} Y{y}")
        g.append(f"G1 X0 Y{y}")
        g.append(f"G1 X0 Y0")

    if allowance > 0:
        g.append("(FINISH)")
        g.append(f"G1 Z{-depth}")

    g.append("G0 Z5")
    g.append("M30")

    return "\n".join(g)