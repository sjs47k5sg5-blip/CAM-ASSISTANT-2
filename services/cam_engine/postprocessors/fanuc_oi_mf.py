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

        self.lines.append("%")
        self.lines.append("O0001")
        self.lines.append("")

        self.lines.append("(CAM ASSISTANT)")
        self.lines.append("")

        self.lines.append("G21")
        self.lines.append("G17")
        self.lines.append("G90")
        self.lines.append("G40")
        self.lines.append("G49")
        self.lines.append("G80")
        self.lines.append("")

        self.lines.append("G54")
        self.lines.append("")

        self.lines.append(f"T{p.tool.number} M6")
        self.lines.append(f"S{p.tool.spindle} M3")
        self.lines.append(
            f"G43 H{p.tool.number} Z{p.machine.safe_z:.3f}"
        )

        self.lines.append("G0 Z5.000")
        self.lines.append("")

    # =====================================
    # FOOTER
    # =====================================

    def footer(self):

        p = self.project

        self.lines.append("")
        self.lines.append(f"G0 Z{p.machine.safe_z:.3f}")

        self.lines.append("M5")

        self.lines.append("")

        self.lines.append("G53 G0 Z0")
        self.lines.append("G53 G0 Y0")

        self.lines.append("")

        self.lines.append("M30")
        self.lines.append("%")

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

        if cmd.feed is not None:
            line += f" F{cmd.feed:.0f}"

        self.lines.append(line)
         # =====================================
    # G2
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

        self.lines.append(line)

    # =====================================
    # G3
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

        self.lines.append(line)

    # =====================================
    # TOOL CHANGE
    # =====================================

    def tool_change(self, cmd):

        self.lines.append(f"T{cmd.tool} M6")
        self.lines.append(f"S{cmd.rpm} M3")
        self.lines.append(
            f"G43 H{cmd.length_offset} Z{self.project.machine.safe_z:.3f}"
        )
        self.lines.append("G0 Z5.000")

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