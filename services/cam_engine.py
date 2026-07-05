def apply_zero(x, y, zero, sx, sy):
    # transform coordinates based on zero point
    if zero == "CENTER":
        return x + sx/2, y + sy/2
    if zero == "TL":
        return x, y + sy
    if zero == "TR":
        return x + sx, y + sy
    if zero == "BL":
        return x, y
    if zero == "BR":
        return x + sx, y
    return x, y


def contour(x, y, depth, feed, tool, zero, sx, sy):

    ox, oy = apply_zero(0, 0, zero, sx, sy)
    ex, ey = apply_zero(x, y, zero, sx, sy)

    g = []
    g.append("G21 G90")
    g.append("G0 Z5")
    g.append(f"T{tool} M6")

    g.append(f"G0 X{ox} Y{oy}")

    g.append(f"G1 Z-{depth} F120")
    g.append(f"G1 X{ex} Y{oy} F{feed}")
    g.append(f"G1 X{ex} Y{ey}")
    g.append(f"G1 X{ox} Y{ey}")
    g.append(f"G1 X{ox} Y{oy}")

    g.append("G0 Z5")
    g.append("M30")

    return "
".join(g)
