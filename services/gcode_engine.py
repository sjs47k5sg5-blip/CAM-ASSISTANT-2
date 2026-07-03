class GCodeBuilder:
    def __init__(self):
        self.lines = []

    def add(self, line: str):
        self.lines.append(line)

    def rapid(self, x=None, y=None, z=None):
        cmd = "G00"
        if x is not None:
            cmd += f" X{x:.3f}"
        if y is not None:
            cmd += f" Y{y:.3f}"
        if z is not None:
            cmd += f" Z{z:.3f}"
        self.add(cmd)

    def feed(self, x=None, y=None, z=None, f=None):
        cmd = "G01"
        if x is not None:
            cmd += f" X{x:.3f}"
        if y is not None:
            cmd += f" Y{y:.3f}"
        if z is not None:
            cmd += f" Z{z:.3f}"
        if f is not None:
            cmd += f" F{f:.0f}"
        self.add(cmd)

    def cw_arc(self, x, y, i, j, f=None):
        cmd = f"G02 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}"
        if f is not None:
            cmd += f" F{f:.0f}"
        self.add(cmd)

    def ccw_arc(self, x, y, i, j, f=None):
        cmd = f"G03 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}"
        if f is not None:
            cmd += f" F{f:.0f}"
        self.add(cmd)

    def comment(self, text):
        self.add(f"({text})")

    def spindle_on(self, rpm):
        self.add(f"S{rpm} M03")

    def spindle_off(self):
        self.add("M05")

    def coolant_on(self):
        self.add("M08")

    def coolant_off(self):
        self.add("M09")

    def tool_change(self, tool):
        self.add(f"T{tool:02d} M06")

    def length_offset(self, tool, safe_z):
        self.add(f"G43 H{tool:02d} Z{safe_z:.3f}")

    def g41(self, d):
        self.add(f"G41 D{d:02d}")

    def g42(self, d):
        self.add(f"G42 D{d:02d}")

    def g40(self):
        self.add("G40")

    def build(self):
        return "\n".join(self.lines)