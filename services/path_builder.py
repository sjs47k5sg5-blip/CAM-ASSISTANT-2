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

    # порядок обхода
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

    arc_cmd = "G02" if clockwise else "G03"

    n = len(order)

    # стартовая точка
    first = order[0]

    # первый переход в точку старта
    lines.append(
        f"G01 X{first[0]:.3f} Y{first[1]:.3f}"
    )

    for i in range(n):

        prev = order[i - 1]
        cur = order[i]
        nxt = order[(i + 1) % n]

        use_corner = (
            corner_type != "none"
            and corner_value > 0
            and corner_enabled(i + 1, corner_select)
        )

        # --------------------------
        # ФАСКА
        # --------------------------
        if use_corner and corner_type == "chamfer":

            start, end = chamfer_points(
                prev,
                cur,
                nxt,
                corner_value,
            )

            # линия до фаски
            lines.append(
                f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
            )

            # фаска
            lines.append(
                f"G01 X{end[0]:.3f} Y{end[1]:.3f}"
            )

            continue

        # --------------------------
        # РАДИУС (I/J)
        # --------------------------
        if use_corner and corner_type == "radius":

            start, end, center = radius_arc(
                prev,
                cur,
                nxt,
                corner_value,
            )

            # центр дуги
            i_off = center[0] - start[0]
            j_off = center[1] - start[1]

            # подвод к дуге
            lines.append(
                f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
            )

            # дуга I/J
            lines.append(
                f"{arc_cmd} "
                f"X{end[0]:.3f} "
                f"Y{end[1]:.3f} "
                f"I{i_off:.3f} "
                f"J{j_off:.3f}"
            )

            continue

        # --------------------------
        # ОБЫЧНАЯ ЛИНИЯ
        # --------------------------
        lines.append(
            f"G01 X{cur[0]:.3f} Y{cur[1]:.3f}"
        )

    # замыкание контура
    lines.append(
        f"G01 X{first[0]:.3f} Y{first[1]:.3f}"
    )

    return lines