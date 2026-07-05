
def contour_gcode(w, h, step, depth, zero="top"):

    lines = ["%", "O1001", "G21 G90 G17", "G54", "G40 G49 G80"]

    safe = 5
    lines.append(f"G00 Z{safe}")

    z0 = 0 if zero == "top" else -depth

    d = 0
    while d < depth:
        d += step
        if d > depth:
            d = depth

        z = z0 - d if zero == "top" else z0 + d

        lines.append(f"G00 Z{safe}")
        lines.append(f"G01 Z{z} F200")
        lines.append("G01 X0 Y0")
        lines.append(f"G01 X{w}")
        lines.append(f"G01 Y{h}")
        lines.append("G01 X0 Y0")

    lines += ["G00 Z50", "M30", "%"]
    return "\n".join(lines)
