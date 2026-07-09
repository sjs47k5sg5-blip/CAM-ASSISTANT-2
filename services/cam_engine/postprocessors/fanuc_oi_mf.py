from __future__ import annotations

from ..toolpath.commands import (
    RapidMove, LinearMove, ArcMove,
    ToolChange, SpindleCommand, CoolantCommand
)


class FanucOiMFPost:

    def generate(
        self,
        toolpath,
        work_offset="G54",
        safe_z=100.0,
        approach_z=5.0,
        tool=1,
        rpm=6000,
    ) -> str:

        lines = [
            "%",
            "G21",
            "G17",
            "G90",
            "G40",
            "G49",
            "G80",
            work_offset,
            f"T{tool} M6",
            f"S{rpm} M3",
            f"G43 H{tool} Z{safe_z:.3f}",
            f"G0 Z{approach_z:.3f}",
            "M8",
        ]

        for cmd in toolpath:

            if isinstance(cmd, RapidMove):
                z = f" Z{cmd.z:.3f}" if cmd.z is not None else ""
                lines.append(
                    f"G0 X{cmd.target.x:.3f} Y{cmd.target.y:.3f}{z}"
                )

            elif isinstance(cmd, LinearMove):
                z = f" Z{cmd.z:.3f}" if cmd.z is not None else ""
                lines.append(
                    f"G1 X{cmd.target.x:.3f} Y{cmd.target.y:.3f}{z} F{cmd.feed:.1f}"
                )

            elif isinstance(cmd, ArcMove):
                g = "G2" if cmd.clockwise else "G3"
                z = f" Z{cmd.z:.3f}" if cmd.z is not None else ""
                i = cmd.center.x - cmd.target.x
                j = cmd.center.y - cmd.target.y
                lines.append(
                    f"{g} X{cmd.target.x:.3f} Y{cmd.target.y:.3f}{z} I{i:.3f} J{j:.3f} F{cmd.feed:.1f}"
                )

        lines += [
            "M9",
            f"G0 Z{safe_z:.3f}",
            "G91 G28 Z0.",
            "G91 G28 Y0.",
            "G90",
            "M30",
            "%"
        ]

        return "\n".join(lines)
