from dataclasses import dataclass
from typing import List, Optional


# ==========================================
# БАЗОВАЯ КОМАНДА
# ==========================================

@dataclass
class Command:

    pass


# ==========================================
# RAPID (G0)
# ==========================================

@dataclass
class Rapid(Command):

    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None


# ==========================================
# FEED (G1)
# ==========================================

@dataclass
class Feed(Command):

    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None

    feed: Optional[float] = None


# ==========================================
# ARC CW (G2)
# ==========================================

@dataclass
class ArcCW(Command):

    x: float

    y: float

    i: float

    j: float

    feed: Optional[float] = None


# ==========================================
# ARC CCW (G3)
# ==========================================

@dataclass
class ArcCCW(Command):

    x: float

    y: float

    i: float

    j: float

    feed: Optional[float] = None


# ==========================================
# SPINDLE
# ==========================================

@dataclass
class SpindleOn(Command):

    rpm: int

    clockwise: bool = True


@dataclass
class SpindleOff(Command):

    pass


# ==========================================
# TOOL CHANGE
# ==========================================

@dataclass
class ToolChange(Command):

    tool: int

    length_offset: int


# ==========================================
# COOLANT
# ==========================================

@dataclass
class CoolantOn(Command):

    pass


@dataclass
class CoolantOff(Command):

    pass


# ==========================================
# COMMENT
# ==========================================

@dataclass
class Comment(Command):

    text: str


# ==========================================
# TOOLPATH
# ==========================================

class ToolPath:

    def __init__(self):

        self.commands: List[Command] = []

    # --------------------------------------

    def add(self, command: Command):

        self.commands.append(command)

    # --------------------------------------

    def extend(self, commands):

        self.commands.extend(commands)

    # --------------------------------------

    def clear(self):

        self.commands.clear()

    # --------------------------------------

    def __iter__(self):

        return iter(self.commands)

    # --------------------------------------

    def __len__(self):

        return len(self.commands)

    # --------------------------------------

    def __getitem__(self, item):

        return self.commands[item]