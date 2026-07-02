def drilling_gcode(
    tool: int,
    rpm: int,
    feed: int,
    depth: float,
    cycle: str,
    step: float,
    x: float = 0,
    y: float = 0,
):
    lines = []

    lines.append("(CNC Assistant Pro)")
    lines.append("(Drilling)")
    lines.append("")
    lines.append(f"T{tool} M06")
    lines.append(f"S{rpm} M03")
    lines.append("M08")
    lines.append("")
    lines.append("G90 G54")
    lines.append(f"G00 X{x:.3f} Y{y:.3f}")
    lines.append("G43 H01 Z50.0")
    lines.append("")

    if cycle == "G81":
        lines.append(
            f"G81 X{x:.3f} Y{y:.3f} Z-{depth:.3f} R2.0 F{feed}"
        )

    elif cycle == "G73":
        lines.append(
            f"G73 X{x:.3f} Y{y:.3f} Z-{depth:.3f} R2.0 Q{step:.3f} F{feed}"
        )

    elif cycle == "G83":
        lines.append(
            f"G83 X{x:.3f} Y{y:.3f} Z-{depth:.3f} R2.0 Q{step:.3f} F{feed}"
        )

    lines.append("G80")
    lines.append("")
    lines.append("G00 Z100.")
    lines.append("M09")
    lines.append("M30")

    return "\n".join(lines)