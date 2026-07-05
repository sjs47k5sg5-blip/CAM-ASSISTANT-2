import math

from services.geometry import (
    rectangle_points,
    contour_start_point,
)
from services.lead import lead_in, lead_out
from services.toolpath import (
    get_compensation,
)

from services.path_builder import build_path


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
    corner_type: str = "none",
    corner_select: str = "all",
    corner_value: float = 0,
):

    import math

    from services.geometry import rectangle_points, contour_start_point
    from services.lead import lead_in, lead_out
    from services.toolpath import get_compensation
    from services.path_builder import build_path

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

    p1, p2, p3, p4 = rough_points
    fp1, fp2, fp3, fp4 = finish_points

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

    def z_value(v):
        if zero_z == "⬆️ Верх детали":
            return -v
        elif zero_z == "⬇️ Низ детали":
            return -(thickness - v)
        return -v

    current_depth = 0

    for p in range(passes):

        current_depth += step
        if current_depth > depth:
            current_depth = depth

        lines.append("")
        lines.append(f"(PASS {p + 1})")

        lines.append(f"G00 X{start_x:.3f} Y{start_y:.3f}")
        lines.append("G00 Z5.")
        lines.append(f"G01 Z{z_value(current_depth):.3f} F200")

        comp = get_compensation(outside, climb)
        lines.append(f"{comp} D{tool:02d}")

        # lead in
        for cmd in lead_in(
            p1[0], p1[1],
            outside=outside,
            climb=climb,
        ):
            lines.append(cmd)
        lines[-1] += f" F{feed}"

        # path
        build_path(
            lines,
            (p1, p2, p3, p4),
            climb,
            outside,
            corner_type,
            corner_select,
            float(allowance if allowance > 0 else corner_value),
        )

        # lead out
        for cmd in lead_out(
            p1[0], p1[1],
            outside=outside,
            climb=climb,
        ):
            lines.append(cmd)

        lines.append("G40")
        lines.append("G00 Z5.")

    # ---------------- FINISH PASS ----------------

    if finish:

        lines.append("")
        lines.append("(FINISH PASS)")

        if not finish_same_tool:
            lines.append("G00 Z100.")
            lines.append("M09")
            lines.append("M05")
            lines.append(f"T{finish_tool} M06")
            lines.append("G54")
            lines.append(f"G00 G43 H{finish_tool:02d} Z100.")

        rpm_f = finish_rpm if finish_rpm > 0 else rpm
        feed_f = finish_feed if finish_feed > 0 else feed

        start_fx, start_fy = contour_start_point(
            fp1, 0, outside=outside
        )

        lines.append(f"S{rpm_f} M03")
        lines.append("M08")
        lines.append(f"G00 X{start_fx:.3f} Y{start_fy:.3f}")
        lines.append("G00 Z5.")
        lines.append(f"G01 Z{z_value(depth):.3f} F200")

        comp = get_compensation(outside, climb)
        lines.append(f"{comp} D{finish_tool if not finish_same_tool else tool:02d}")

        for cmd in lead_in(
            fp1[0], fp1[1],
            outside=outside,
            climb=climb,
        ):
            lines.append(cmd)

        lines[-1] += f" F{feed_f}"

        build_path(
            lines,
            (fp1, fp2, fp3, fp4),
            climb,
            outside,
            corner_type,
            corner_select,
            corner_value,
        )

        for cmd in lead_out(
            fp1[0], fp1[1],
            outside=outside,
            climb=climb,
        ):
            lines.append(cmd)

        lines.append("G40")
        lines.append("G00 Z5.")

    # END PROGRAM
    lines.append("")
    lines.append("G00 Z100.")
    lines.append("M09")
    lines.append("M05")
    lines.append("G91 G28 Z0.")
    lines.append("G90")
    lines.append("M30")
    lines.append("%")

    return "\n".join(lines)