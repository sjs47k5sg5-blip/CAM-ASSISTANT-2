
def pocket_gcode(paths, motion):

    lines = []

    for path in paths:
        lines.append("(POCKET)")
        first = True
        for x,y in path:
            if first:
                lines.append(f"G01 X{x} Y{y}")
                first = False
            else:
                lines.append(f"G01 X{x} Y{y}")

    return lines
