import math


# =========================
# ZERO MODE NORMALIZER
# =========================

def normalize_zero_mode(zero_mode: str) -> str:
    """
    Приводит любые кнопки UI к внутренним значениям
    """

    if zero_mode in ["⬆️ Верх детали", "top", "TOP", "верх"]:
        return "top"

    if zero_mode in ["⬇️ Низ детали", "bottom", "BOTTOM", "низ"]:
        return "bottom"

    return "top"


# =========================
# ZERO Z CALCULATION
# =========================

def calc_z(depth, zero_mode, thickness):
    """
    depth = глубина резания (положительное число)
    """

    if zero_mode == "top":
        return -depth

    elif zero_mode == "bottom":
        return -(thickness - depth)

    return -depth


# =========================
# MAIN GENERATOR
# =========================

def contour_gcode(
    width=20,
    height=20,
    depth_step=3,
    final_depth=21,
    safe_z=5,
    feed_cut=200,
    feed_move=800,
    tool=20,
    zero_mode="top",
    thickness=20,
    use_g28=False
):
    lines = []

    # normalize input (ВАЖНО)
    zero_mode = normalize_zero_mode(zero_mode)

    # ================= HEADER =================
    lines.append("%")
    lines.append("O1004 (CAM FIX V3 ZERO Z)")
    lines.append("G21")
    lines.append("G17")
    lines.append("G90")
    lines.append("G40")
    lines.append("G49")
    lines.append("G80")

    # tool change
    if use_g28:
        lines.append("G28 U0 W0")

    lines.append(f"T{tool} M06")
    lines.append("S2500 M03")

    lines.append("G00 G54 X0 Y0")
    lines.append(f"G00 Z{safe_z}")

    # ================= CONTOUR PATH =================
    path = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
        (0, 0)
    ]

    depth = depth_step

    while depth <= final_depth:

        z = calc_z(depth, zero_mode, thickness)

        # approach
        lines.append(f"G00 Z{safe_z}")
        lines.append(f"G00 X{path[0][0]} Y{path[0][1]}")

        # plunge
        lines.append(f"G01 Z{z} F{feed_cut}")

        # contour
        for x, y in path[1:]:
            lines.append(f"G01 X{x} Y{y} F{feed_cut}")

        depth += depth_step

    # ================= END =================
    lines.append(f"G00 Z{safe_z}")
    lines.append("M05")
    lines.append("M30")
    lines.append("%")

    return "\n".join(lines)