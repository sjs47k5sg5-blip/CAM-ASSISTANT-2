def contour(x, y, depth, feed, tool, zero, allowance, stepdown, corner):

    g = []
    g.append("G21 G90")
    g.append("G0 Z5")
    g.append(f"T{tool} M6")

    # ZERO INFO
    g.append(f"(ZERO={zero})")

    # ROUGH
    z = 0
    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z} F120")
        g.append(f"G1 X{x} Y0 F{feed}")
        g.append(f"G1 X{x} Y{y}")
        g.append(f"G1 X0 Y{y}")
        g.append(f"G1 X0 Y0")

    # FINISH
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth} F80")
        g.append(f"G1 X{x} Y0 F{feed}")
        g.append(f"G1 X{x} Y{y}")
        g.append(f"G1 X0 Y{y}")
        g.append(f"G1 X0 Y0")

    # CORNERS
    if corner == "ФАСКА":
        g.append("(CHAMFER)")
    elif corner == "РАДИУС":
        g.append("(RADIUS)")
    else:
        g.append("(SHARP)")

    g.append("G0 Z5")
    g.append("M30")

    return "\n".join(g)
