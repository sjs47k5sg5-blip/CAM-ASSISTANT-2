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

    def __init__(self, project):

        super().__init__(project)

        self.current_feed = None
        self.current_motion = None

    # =====================================
    # HEADER
    # =====================================

    def header(self):

        p = self.project

        self.lines.extend([

            "%",

            "O0001",

            "(CAM ASSISTANT)",

            "",

            "G21 G17 G90",

            "G40 G49 G80",

            "G54",

            "",

            f"T{p.tool.number} M6",

            f"S{p.tool.spindle} M3",

            f"G43 H{p.tool.length_offset} Z{p.machine.safe_z:.3f}",

            "M8",

        ])

    # =====================================
    # FOOTER
    # =====================================

    def footer(self):

        self.lines.extend([

            "",

            f"G0 Z{self.project.machine.safe_z:.3f}",

            "M9",

            "M5",

            "G53 G0 Z0",

            "G53 G0 Y0",

            "M30",

            "%"

        ])

    # =====================================
    # RAPID
    # =====================================

    def rapid(self, cmd):

        line = self.xyz(cmd)

        if self.current_motion != "G0":

            line = "G0 " + line

            self.current_motion = "G0"

        self.lines.append(line)

    # =====================================
    # FEED
    # =====================================

    def feed(self, cmd):

        line = self.xyz(cmd)

        if self.current_motion != "G1":

            line = "G1 " + line

            self.current_motion = "G1"

        if cmd.z is not None and cmd.x is None and cmd.y is None:

            feed = self.project.tool.plunge

        elif cmd.feed is not None:

            feed = int(cmd.feed)

        else:

            feed = self.project.tool.feed

        if feed != self.current_feed:

            line += f" F{feed}"

            self.current_feed = feed

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

        feed = self.project.tool.feed if cmd.feed is None else int(cmd.feed)

        if feed != self.current_feed:

            line += f" F{feed}"

            self.current_feed = feed

        self.current_motion = "G2"

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

        feed = self.project.tool.feed if cmd.feed is None else int(cmd.feed)

        if feed != self.current_feed:

            line += f" F{feed}"

            self.current_feed = feed

        self.current_motion = "G3"

        self.lines.append(line)

    # =====================================
    # TOOL
    # =====================================

    def tool_change(self, cmd):

        self.lines.extend([

            "M9",

            "M5",

            f"G0 Z{self.project.machine.safe_z:.3f}",

            f"T{cmd.tool} M6",

            f"G43 H{cmd.length_offset} Z{self.project.machine.safe_z:.3f}",

            "M8",

        ])

        self.current_feed = None
        self.current_motion = None

    # =====================================
    # SPINDLE
    # =====================================

    def spindle_on(self, cmd):

        self.lines.append(

            f"S{cmd.rpm} {'M3' if cmd.clockwise else 'M4'}"

        )

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