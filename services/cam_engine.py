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

    g = []

    # =========================
    # SAFE CONVERT
    # =========================
    try:
        x = float(x)
        y = float(y)
        depth = float(depth)
        stepdown = float(stepdown)
        tool = float(tool)
        allowance = float(allowance)
        corner_value = float(corner_value)
    except:
        return "ERROR: INVALID INPUT"

    # =========================
    # HEADER
    # =========================
    g.append("%")
    g.append("G21")
    g.append("G90")
    g.append("G17")
    g.append("G40 G49 G80")

    g.append(f"T{int(tool)} M6")
    g.append("G0 Z5")

    # =========================
    # TOOL OFFSET (simplified)
    # =========================
    offset = tool / 2.0

    x_off = x - offset
    y_off = y - offset

    g.append(f"(ZERO={zero})")
    g.append(f"(CORNER={corner_type} {corner_value})")

    # =========================
    # ROUGH PASS
    # =========================
    z = 0.0

    while z > -depth:
        z -= stepdown
        if z < -depth:
            z = -depth

        g.append(f"G1 Z{z:.3f} F120")
        g.append(f"G1 X{x_off:.3f} Y0 F200")
        g.append(f"G1 X{x_off:.3f} Y{y_off:.3f}")
        g.append(f"G1 X0 Y{y_off:.3f}")
        g.append(f"G1 X0 Y0")

    # =========================
    # FINISH PASS
    # =========================
    if allowance > 0:
        g.append("(FINISH PASS)")
        g.append(f"G1 Z{-depth:.3f} F80")
        g.append(f"G1 X{x_off:.3f} Y0 F150")
        g.append(f"G1 X{x_off:.3f} Y{y_off:.3f}")
        g.append(f"G1 X0 Y{y_off:.3f}")
        g.append(f"G1 X0 Y0")

    # =========================
    # CORNER INFO (NO CRASH SAFE)
    # =========================
    if corner_type == "ФАСКА":
        g.append(f"(CHAMFER {corner_value}mm)")
    elif corner_type == "РАДИУС":
        g.append(f"(RADIUS {corner_value}mm)")
    else:
        g.append("(SHARP CORNERS)")

    # =========================
    # FOOTER
    # =========================
    g.append("G0 Z5")
    g.append("M30")
    g.append("%")

    return "\n".join(g)