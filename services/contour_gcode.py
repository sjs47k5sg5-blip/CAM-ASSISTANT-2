import math


def contour_gcode(
    tool: int,
    rpm: int,
    feed: int,
    length: float,
    width: float,
    depth: float,
    step: float,
    allowance: float,
    outside: bool = True,
    climb: bool = True,
):

    passes = math.ceil(depth / step)

    lines = []

    lines.append("%")
    lines.append("O1003")
    lines.append("(RECTANGLE CONTOUR)")
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
    lines.append("G00 G43 H01 Z100.")

    current_depth = 0

    start_x = -15 - allowance
    start_y = -5 - allowance

    end_x = length + allowance
    end_y = width + allowance

    for p in range(passes):

        current_depth += step

        if current_depth > depth:
            current_depth = depth

        lines.append("")
        lines.append(f"(PASS {p+1})")

        lines.append(f"G00 X{start_x:.3f} Y{start_y:.3f}")

        lines.append(f"G01 Z-{current_depth:.3f} F200")

        if outside:
            lines.append("G41 D01")
        else:
            lines.append("G42 D01")

        # Заход по дуге
        lines.append(
            f"G03 X{-5-allowance:.3f} Y{-5-allowance:.3f} R10."
        )

        if climb:

            lines.append(f"G01 X{end_x:.3f} F{feed}")
            lines.append(f"G01 Y{end_y:.3f}")
            lines.append(f"G01 X{-5-allowance:.3f}")
            lines.append(f"G01 Y{-5-allowance:.3f}")

        else:

            lines.append(f"G01 Y{end_y:.3f} F{feed}")
            lines.append(f"G01 X{end_x:.3f}")
            lines.append(f"G01 Y{-5-allowance:.3f}")
            lines.append(f"G01 X{-5-allowance:.3f}")

        # Выход по дуге
        lines.append(
            f"G03 X{start_x:.3f} Y{start_y:.3f} R10."
        )

        lines.append("G40")

        lines.append("G00 Z5.")

    lines.append("")
    lines.append("G00 Z100.")
    lines.append("M09")
    lines.append("M05")
    lines.append("")
    lines.append("G91 G28 Z0.")
    lines.append("G90")
    lines.append("")
    lines.append("M30")
    lines.append("%")

    return "\n".join(lines)