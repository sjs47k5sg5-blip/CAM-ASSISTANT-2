from __future__ import annotations

from ..toolpath.commands import (
    RapidMove, LinearMove, ArcMove,
    ToolChange, SpindleCommand, CoolantCommand
)

class FanucOiMFPost:
    def generate(self, toolpath, work_offset="G54", tool_length=None, safe_z=50.0)->str:
        lines=[
            "%",
            "G21","G17","G90","G40","G49","G80",
            work_offset,
            f"G0 Z{safe_z:.3f}"
        ]
        if tool_length is not None:
            lines.append(f"G43 H{tool_length}")

        for cmd in toolpath:
            if isinstance(cmd, ToolChange):
                lines += ["G91 G28 Z0","G90",f"T{cmd.tool} M6",f"G0 Z{safe_z:.3f}"]
            elif isinstance(cmd, SpindleCommand):
                lines.append(f"S{cmd.rpm} {'M3' if cmd.clockwise else 'M4'}")
            elif isinstance(cmd, CoolantCommand):
                lines.append("M8" if cmd.enabled else "M9")
            elif isinstance(cmd, RapidMove):
                lines.append(f"G0 X{cmd.target.x:.3f} Y{cmd.target.y:.3f}")
            elif isinstance(cmd, LinearMove):
                lines.append(f"G1 X{cmd.target.x:.3f} Y{cmd.target.y:.3f} F{cmd.feed:.1f}")
            elif isinstance(cmd, ArcMove):
                g="G2" if cmd.clockwise else "G3"
                i=cmd.center.x-cmd.target.x
                j=cmd.center.y-cmd.target.y
                lines.append(f"{g} X{cmd.target.x:.3f} Y{cmd.target.y:.3f} I{i:.3f} J{j:.3f} F{cmd.feed:.1f}")
        lines += [f"G0 Z{safe_z:.3f}","M9","M30","%"]
        return "\n".join(lines)
