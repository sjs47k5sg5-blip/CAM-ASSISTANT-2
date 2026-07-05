def contour(x, y, depth, feed, tool_dia, allowance, stepdown, corner_type, corner_value, zone):

    g = []
    g.append("G21 G90")
    g.append("G0 Z5")
    g.append("G0 X0 Y0")

    # TOOL
    g.append(f"T{tool_dia} M6")

    # SIMPLE compensation logic
    if tool_dia > 10:
        g.append("G41 D1")
    else:
        g.append("G42 D1")

    # ROUGH PASS
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

    # FINISH PASS
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth} F80")
        g.append(f"G1 X{x} Y0 F{feed}")
        g.append(f"G1 X{x} Y{y}")
        g.append(f"G1 X0 Y{y}")
        g.append(f"G1 X0 Y0")

    # CORNERS LOGIC (SIMPLIFIED)
    if corner_type == "FASKA":
        g.append(f"(CHAMFER {corner_value})")
    elif corner_type == "RADIUS":
        g.append(f"(RADIUS {corner_value})")

    if zone != "ALL":
        g.append(f"(ZONE {zone})")

    g.append("G0 Z5")
    g.append("M30")
    return "\n".join(g)
