from services.corners import (
    corner_enabled,
    chamfer_points,
    radius_points,
)


def build_path(
    lines,
    points,
    climb,
    outside,
    corner_type,
    corner_select,
    corner_value,
):

    if climb:
        order = list(points)
    else:
        order = [
            points[0],
            points[3],
            points[2],
            points[1],
        ]

    order.append(order[0])
    order.append(order[1])

    clockwise = (
        (outside and climb)
        or
        (not outside and not climb)
    )

    arc = "G02" if clockwise else "G03"

    first_move = True

    for i in range(4):

        prev = order[i]
        cur = order[i + 1]
        nxt = order[i + 2]

        enabled = (
            corner_type != "none"
            and corner_value > 0
            and corner_enabled(i + 1, corner_select)
        )

        if not enabled:

            if first_move:
                lines.append(
                    f"G01 X{cur[0]:.3f} Y{cur[1]:.3f}"
                )
                first_move = False

            lines.append(
                f"G01 X{nxt[0]:.3f} Y{nxt[1]:.3f}"
            )
            continue

        if corner_type == "chamfer":

            start, end = chamfer_points(
                prev,
                cur,
                nxt,
                corner_value,
            )

            if first_move:
                lines.append(
                    f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
                )
                first_move = False
            else:
                lines.append(
                    f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
                )

            lines.append(
                f"G01 X{end[0]:.3f} Y{end[1]:.3f}"
            )

        elif corner_type == "radius":

            start, end = radius_points(
                prev,
                cur,
                nxt,
                corner_value,
            )

            if first_move:
                lines.append(
                    f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
                )
                first_move = False
            else:
                lines.append(
                    f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
                )

            lines.append(
                f"{arc} "
                f"X{end[0]:.3f} "
                f"Y{end[1]:.3f} "
                f"R{corner_value:.3f}"
            )