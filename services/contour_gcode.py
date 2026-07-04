import math

from services.geometry import (
    rectangle_points,
    contour_start_point,
)
from services.lead import lead_in, lead_out
from services.toolpath import (
    get_compensation,
    get_arc,
)


def contour_gcode(
    tool: int,
    rpm: int,
    feed: int,
    length: float,
    width: float,
    depth: float,
    step: float,
    allowance: float,
    finish: bool = False,
    outside: bool = True,
    climb: bool = True,
    zero: str = "↙️ Левый нижний",
    zero_z: str = "Верх детали",
    thickness: float = 0,

    finish_same_tool: bool = True,
    finish_tool: int = 1,
    finish_rpm: int = 0,
    finish_feed: int = 0,
):

    passes = math.ceil(depth / step)

    rough_points = rectangle_points(
    length=length,
    width=width,
    zero=zero,
    allowance=allowance,
    outside=outside,
    )

    finish_points = rectangle_points(
    length=length,
    width=width,
    zero=zero,
    )

    # точки черновой
    p1 = rough_points[0]
    p2 = rough_points[1]
    p3 = rough_points[2]
    p4 = rough_points[3]

    # точки чистовой
    fp1 = finish_points[0]
    fp2 = finish_points[1]
    fp3 = finish_points[2]
    fp4 = finish_points[3]

    start_x, start_y = contour_start_point(
    p1,
    allowance,
    outside=outside,
)

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

    lines.append(f"G00 G43 H{tool:02d} Z100.")
    

    current_depth = 0

    def z_value(value):

        if zero_z == "⬆️ Верх детали":
            return -value

        elif zero_z == "⬇️ Низ детали":
            return -(thickness - value)

        return -value

    for p in range(passes):

        current_depth += step

        if current_depth > depth:
            current_depth = depth

        lines.append("")
        lines.append(f"(PASS {p + 1})")

        lines.append(
            f"G00 X{start_x:.3f} Y{start_y:.3f}"
        )

        lines.append("G00 Z5.")

        lines.append(
            f"G01 Z{z_value(current_depth):.3f} F200"
        )

        comp = get_compensation(
            outside,
            climb,
        )

        lines.append(f"{comp} D{tool:02d}")

        for cmd in lead_in(
    p1[0],
    p1[1],
    outside=outside,
    climb=climb,
):
            lines.append(cmd)

        lines[-2] += f" F{feed}"

        if climb:

            lines.append(
                f"G01 X{p2[0]:.3f} Y{p2[1]:.3f}"
            )

            lines.append(
                f"G01 X{p3[0]:.3f} Y{p3[1]:.3f}"
            )

            lines.append(
                f"G01 X{p4[0]:.3f} Y{p4[1]:.3f}"
            )

            lines.append(
                f"G01 X{p1[0]:.3f} Y{p1[1]:.3f}"
            )

        else:

            lines.append(
                f"G01 X{p4[0]:.3f} Y{p4[1]:.3f}"
            )

            lines.append(
                f"G01 X{p3[0]:.3f} Y{p3[1]:.3f}"
            )

            lines.append(
                f"G01 X{p2[0]:.3f} Y{p2[1]:.3f}"
            )

            lines.append(
                f"G01 X{p1[0]:.3f} Y{p1[1]:.3f}"
            )

        for cmd in lead_out(
    p1[0],
    p1[1],
    outside=outside,
    climb=climb,
):
            lines.append(cmd)

        lines.append("G40")
        lines.append("G00 Z5.")
    if finish:

        lines.append("")
        lines.append("(FINISH PASS)")

        # выбираем инструмент
        if not finish_same_tool:

            lines.append("G00 Z100.")
            lines.append("M09")
            lines.append("M05")

            lines.append(f"T{finish_tool} M06")
            lines.append("G54")
            lines.append(f"G00 G43 H{finish_tool:02d} Z100.")

        rpm_f = finish_rpm if finish_rpm > 0 else rpm
        feed_f = finish_feed if finish_feed > 0 else feed

        lines.append(f"S{rpm_f} M03")
        lines.append("M08")

        start_fx, start_fy = contour_start_point(
    fp1,
    0,
    outside=outside,
)

        lines.append(f"G00 X{start_fx:.3f} Y{start_fy:.3f}")
        lines.append("G00 Z5.")
        lines.append(f"G01 Z{z_value(depth):.3f} F200")

        if finish_same_tool:
            finish_d = tool
        else:
            finish_d = finish_tool

        comp = get_compensation(
            outside,
            climb,
        )

        lines.append(f"{comp} D{finish_d:02d}")

        for cmd in lead_in(
    fp1[0],
    fp1[1],
    outside=outside,
    climb=climb,
):
            lines.append(cmd)

        lines[-2] += f" F{feed_f}"

        if climb:

            lines.append(f"G01 X{fp2[0]:.3f} Y{fp2[1]:.3f}")
            lines.append(f"G01 X{fp3[0]:.3f} Y{fp3[1]:.3f}")
            lines.append(f"G01 X{fp4[0]:.3f} Y{fp4[1]:.3f}")
            lines.append(f"G01 X{fp1[0]:.3f} Y{fp1[1]:.3f}")

        else:

            lines.append(f"G01 X{fp4[0]:.3f} Y{fp4[1]:.3f}")
            lines.append(f"G01 X{fp3[0]:.3f} Y{fp3[1]:.3f}")
            lines.append(f"G01 X{fp2[0]:.3f} Y{fp2[1]:.3f}")
            lines.append(f"G01 X{fp1[0]:.3f} Y{fp1[1]:.3f}")

        for cmd in lead_out(
    fp1[0],
    fp1[1],
    outside=outside,
    climb=climb,
):
            lines.append(cmd)

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