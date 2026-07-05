from services.corners import (
    corner_enabled,
    chamfer_points,
    radius_arc,
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

    # Порядок обхода
    if climb:
        order = list(points)
    else:
        order = [
            points[0],
            points[3],
            points[2],
            points[1],
        ]

    clockwise = (
        (outside and climb)
        or
        (not outside and not climb)
    )

    arc = "G02" if clockwise else "G03"

    count = len(order)

    for i in range(count):

        prev = order[(i - 1) % count]
        cur = order[i]
        nxt = order[(i + 1) % count]

        use_corner = (
            corner_type != "none"
            and corner_value > 0
            and corner_enabled(
                i + 1,
                corner_select,
            )
        )

        if use_corner:

            if corner_type == "chamfer":

                start, end = chamfer_points(
                    prev,
                    cur,
                    nxt,
                    corner_value,
                )

            else:

                start, end, center = radius_arc(
                    prev,
                    cur,
                    nxt,
                    corner_value,
                )
        else:

            start = cur
            end = cur
        # Первый элемент траектории
        if i == 0:

            if use_corner:
                lines.append(
                    f"G01 X{start[0]:.3f} "
                    f"Y{start[1]:.3f}"
                )
            else:
                lines.append(
                    f"G01 X{cur[0]:.3f} "
                    f"Y{cur[1]:.3f}"
                )

        if i > 0:

            target = start if use_corner else cur

            lines.append(
                f"G01 X{target[0]:.3f} "
                f"Y{target[1]:.3f}"
            )

                
         # Строим фаску
        if use_corner and corner_type == "chamfer":

            lines.append(
                f"G01 X{end[0]:.3f} "
                f"Y{end[1]:.3f}"
            )

        # Строим радиус
        elif use_corner and corner_type == "radius":

    offset_i = center[0] - start[0]
    offset_j = center[1] - start[1]

    lines.append(
        f"{arc} "
        f"X{end[0]:.3f} "
        f"Y{end[1]:.3f} "
        f"I{offset_i:.3f} "
        f"J{offset_j:.3f}"
    )

    # Замыкаем контур
    first = order[0]

    first_enabled = (
        corner_type != "none"
        and corner_value > 0
        and corner_enabled(
            1,
            corner_select,
        )
    )

    if first_enabled:

        prev = order[-1]
        nxt = order[1]

        if corner_type == "chamfer":
            start, _ = chamfer_points(
                prev,
                first,
                nxt,
                corner_value,
            )
        else:
            start, _, _ = radius_arc(
                prev,
                first,
                nxt,
                corner_value,
            )

        lines.append(
            f"G01 X{start[0]:.3f} "
            f"Y{start[1]:.3f}"
        )

    else:

        lines.append(
            f"G01 X{first[0]:.3f} "
            f"Y{first[1]:.3f}"
        )