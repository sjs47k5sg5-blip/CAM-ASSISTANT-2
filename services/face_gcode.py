import math

from services.geometry import rectangle_points


def face_gcode(
    tool: int,
    rpm: int,
    feed: int,
    width: float,
    length: float,
    depth: float,
    step: float,
    zero: str = "↙️ Левый нижний",
):

    passes = math.ceil(width / step)

    points = rectangle_points(
        length=length,
        width=width,
        zero=zero,
    )

    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    xmin = min(p1[0], p2[0], p3[0], p4[0])
    xmax = max(p1[0], p2[0], p3[0], p4[0])

    ymin = min(p1[1], p2[1], p3[1], p4[1])
    ymax = max(p1[1], p2[1], p3[1], p4[1])

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
    lines.append("G54")
    lines.append("")
    lines.append(f"S{rpm} M03")
    lines.append("M08")
    lines.append("")
    lines.append("G00 G43 H01 Z50.")
    lines.append("")

    y = ymin - 5

    for i in range(passes):

        lines.append(f"(PASS {i + 1})")

        if i % 2 == 0:

            lines.append(
                f"G00 X{xmin - 5:.3f} Y{y:.3f}"
            )

            lines.append(
                f"G01 Z-{depth:.3f} F200"
            )

            lines.append(
                f"G01 X{xmax + 5:.3f} F{feed}"
            )

        else:

            lines.append(
                f"G00 X{xmax + 5:.3f} Y{y:.3f}"
            )

            lines.append(
                f"G01 Z-{depth:.3f} F200"
            )

            lines.append(
                f"G01 X{xmin - 5:.3f} F{feed}"
            )

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