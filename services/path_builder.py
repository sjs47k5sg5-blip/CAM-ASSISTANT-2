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

    print("🔥 PATH_BUILDER V2 IS RUNNING")  # DEBUG MARKER

    if climb:
        order = list(points)
    else:
        order = [
            points[0],
            points[3],
            points[2],
            points[1],
        ]

    print(f"📌 ORDER: {order}")

    n = len(order)

    for i in range(n):

        prev = order[i - 1]
        cur = order[i]
        nxt = order[(i + 1) % n]

        print(f"➡️ STEP {i}: CUR={cur}")

        use_corner = (
            corner_type != "none"
            and corner_value > 0
            and corner_enabled(i + 1, corner_select)
        )

        # ---------------- RADII ----------------
        if use_corner and corner_type == "radius":

            print("🔵 RADIUS MODE")

            start, end, center = radius_arc(
                prev, cur, nxt, corner_value
            )

            i_off = center[0] - start[0]
            j_off = center[1] - start[1]

            lines.append(
                f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
            )

            lines.append(
                f"G02 X{end[0]:.3f} Y{end[1]:.3f} I{i_off:.3f} J{j_off:.3f}"
            )

            continue

        # ---------------- CHAMFER ----------------
        if use_corner and corner_type == "chamfer":

            print("🟡 CHAMFER MODE")

            start, end = chamfer_points(
                prev, cur, nxt, corner_value
            )

            lines.append(
                f"G01 X{start[0]:.3f} Y{start[1]:.3f}"
            )

            lines.append(
                f"G01 X{end[0]:.3f} Y{end[1]:.3f}"
            )

            continue

        # ---------------- LINE ----------------
        print("⚪ LINE MODE")

        lines.append(
            f"G01 X{cur[0]:.3f} Y{cur[1]:.3f}"
        )

    print("✅ PATH_BUILDER DONE")

    return lines