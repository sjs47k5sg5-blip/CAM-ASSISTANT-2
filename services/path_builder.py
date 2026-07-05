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

                start, end = radius_points(
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

        # Если предыдущий угол тоже обработан,
        # идем от конца предыдущей дуги/фаски
        if i > 0:

            prev_prev = order[(i - 2) % count]

            prev_enabled = (
                corner_type != "none"
                and corner_value > 0
                and corner_enabled(
                    i,
                    corner_select,
                )
            )

            if prev_enabled:

                if corner_type == "chamfer":
                    _, prev_end = chamfer_points(
                        prev_prev,
                        prev,
                        cur,
                        corner_value,
                    )
                else:
                    _, prev_end = radius_points(
                        prev_prev,
                        prev,
                        cur,
                        corner_value,
                    )

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

            lines.append(
                f"{arc} "
                f"X{end[0]:.3f} "
                f"Y{end[1]:.3f} "
                f"R{corner_value:.3f}"
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
            start, _ = radius_points(
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