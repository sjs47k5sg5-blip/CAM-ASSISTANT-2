def contour_gcode(
    width,
    height,
    depth_step,
    final_depth,
    thickness,
    zero_mode="top",
    cam_plan=None
):
    lines = []

    # =========================
    # HEADER
    # =========================
    lines.append("%")
    lines.append("O1001 (CONTOUR CAM FIX)")
    lines.append("G21")
    lines.append("G17")
    lines.append("G90")
    lines.append("G40 G49 G80")
    lines.append("G54")
    lines.append("")

    # =========================
    # SAFE START
    # =========================
    safe_z = 5
    lines.append(f"G00 Z{safe_z}")

    # =========================
    # CAM PLAN (NEW ENGINE SUPPORT)
    # =========================
    rough_enabled = True
    finish_enabled = True
    step_over = 1.0

    if cam_plan:
        rough_enabled = cam_plan.get("rough_pass", {}).get("enabled", True)
        finish_enabled = cam_plan.get("finish_pass", {}).get("enabled", True)

    # =========================
    # ZERO MODE LOGIC
    # =========================
    if zero_mode == "top":
        z0 = 0
        depth_direction = -1
    else:
        z0 = -thickness
        depth_direction = 1

    # =========================
    # DEPTH LOOP
    # =========================
    current_depth = 0

    while abs(current_depth) < final_depth:

        current_depth += depth_step
        if current_depth > final_depth:
            current_depth = final_depth

        z = z0 + (current_depth * depth_direction)

        lines.append("")
        lines.append(f"(DEPTH: {round(current_depth,2)})")
        lines.append(f"G00 Z{safe_z}")

        # =========================
        # ROUGH PASS
        # =========================
        if rough_enabled:
            lines.append(f"G01 Z{z} F200")

            lines.append(f"G01 X0 Y0 F300")
            lines.append(f"G01 X{width}")
            lines.append(f"G01 Y{height}")
            lines.append(f"G01 X0")
            lines.append(f"G01 Y0")

        # =========================
        # FINISH PASS (OFFSET SMALLER STEP)
        # =========================
        if finish_enabled:
            offset = 0.2

            lines.append("(FINISH PASS)")
            lines.append(f"G01 Z{z} F150")

            lines.append(f"G01 X{offset} Y{offset}")
            lines.append(f"G01 X{width - offset}")
            lines.append(f"G01 Y{height - offset}")
            lines.append(f"G01 X{offset}")
            lines.append(f"G01 Y{offset}")

    # =========================
    # END PROGRAM
    # =========================
    lines.append("")
    lines.append("G00 Z50")
    lines.append("M30")
    lines.append("%")

    return "\n".join(lines)