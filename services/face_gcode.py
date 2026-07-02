import math


def face_gcode(
    tool: int,
    rpm: int,
    feed: int,
    width: float,
    length: float,
    depth: float,
    step: float,
):
    passes = math.ceil(width / step)

    lines = []

    lines.append("%")
    lines.append("O1002")
    lines.append("(FACE MILLING)")
    lines.append("")
    lines.append("G21")
    lines.append("G17")
    lines.append("G90")
    lines.append("G40")
    lines.append("G49")
    lines.append("G80")
    lines.append("")
    lines.append(f"T{tool} M06")
    lines.append("")
    lines.append("G54")
    lines.append("")
    lines.append(f"S{rpm} M03")
    lines.append("M08")
    lines.append("")
    lines.append("G00 G43 H01 Z50.")
    lines.append("")

    y = -5.0

    for i in range(passes):

        lines.append(f"(PASS {i + 1})")

        lines.append(f"G00 X-5.000 Y{y:.3f}")
        lines.append(f"G01 Z-{depth:.3f} F200")

        if i % 2 == 0:
            lines.append(f"G01 X{length:.3f} F{feed}")
        else:
            lines.append("G01 X-5.000")

        lines.append("G00 Z5.000")

        y += step

    lines.append("")
    lines.append("G00 Z100.")
    lines.append("M09")
    lines.append("M05")
    lines.append("")
    lines.append("M30")
    lines.append("%")

    return "\n".join(lines)