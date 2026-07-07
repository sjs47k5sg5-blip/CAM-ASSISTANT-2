from services.cam_engine.postprocessors.base import BasePostProcessor

from services.cam_engine.toolpath import (
    Rapid,
    Feed,
    ArcCW,
    ArcCCW,
    ToolChange,
    SpindleOn,
    SpindleOff,
    CoolantOn,
    CoolantOff,
    Comment,
)


class FanucOiMFPost(BasePostProcessor):

    # =====================================
    # HEADER
    # =====================================

    def header(self):

        p = self.project

        self.lines.extend([
            "%",
            "O0001",
            "",
            "G21",
            "G17",
            "G90",
            "G40",
            "G49",
            "G80",
            "",
            "G54",
            "",
            f"T{p.tool.number} M6",
            f"S{p.tool.spindle} M3",
            f"G43 H{p.tool.number} Z{p.machine.safe_z:.3f}",
            "M8",
            "",
            f"G0 Z{p.machine.rapid_z:.3f}",
        ])

    # =====================================
    # FOOTER
    # =====================================

    def footer(self):

        self.lines.extend([
            "",
            f"G0 Z{self.project.machine.safe_z:.3f}",
            "",
            "M9",
            "M5",
            "",
            "G53 G0 Z0",
            "G53 G0 Y0",
            "",
            "M30",
            "%"
        ])

    # =====================================
    # RAPID
    # =====================================

    def rapid(self, cmd):

        self.lines.append(
            "G0 " + self.xyz(cmd)
        )

    # =====================================
    # FEED
    # =====================================

    def feed(self, cmd):

        line = "G1 " + self.xyz(cmd)

        if cmd.z is not None and cmd.x is None and cmd.y is None:

            line += f" F{self.project.tool.plunge}"

        elif cmd.feed is not None:

            line += f" F{cmd.feed:.0f}"

        else:

            line += f" F{self.project.tool.feed}"

        self.lines.append(line)

    # =====================================
    # ARC CW
    # =====================================

    def arc_cw(self, cmd):

        line = (
            f"G2 "
            f"X{cmd.x:.3f} "
            f"Y{cmd.y:.3f} "
            f"I{cmd.i:.3f} "
            f"J{cmd.j:.3f}"
        )

        if cmd.feed is not None:

            line += f" F{cmd.feed:.0f}"

        else:

            line += f" F{self.project.tool.feed}"

        self.lines.append(line)

    # =====================================
    # ARC CCW
    # =====================================

    def arc_ccw(self, cmd):

        line = (
            f"G3 "
            f"X{cmd.x:.3f} "
            f"Y{cmd.y:.3f} "
            f"I{cmd.i:.3f} "
            f"J{cmd.j:.3f}"
        )

        if cmd.feed is not None:

            line += f" F{cmd.feed:.0f}"

        else:

            line += f" F{self.project.tool.feed}"

        self.lines.append(line)

    # =====================================
    # TOOL
    # =====================================

    def tool_change(self, cmd):

        self.lines.append(f"T{cmd.tool} M6")
        self.lines.append(f"G43 H{cmd.length_offset} Z{self.project.machine.safe_z:.3f}")

    # =====================================
    # SPINDLE
    # =====================================

    def spindle_on(self, cmd):

        if cmd.clockwise:
            self.lines.append(f"S{cmd.rpm} M3")
        else:
            self.lines.append(f"S{cmd.rpm} M4")

    def spindle_off(self, cmd):

        self.lines.append("M5")

    # =====================================
    # COOLANT
    # =====================================

    def coolant_on(self, cmd):

        self.lines.append("M8")

    def coolant_off(self, cmd):

        self.lines.append("M9")

    # =====================================
    # COMMENT
    # =====================================

    def comment(self, cmd):

        self.lines.append(f"({cmd.text})")