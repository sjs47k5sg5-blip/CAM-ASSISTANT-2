from abc import ABC, abstractmethod

from services.cam_engine.models import Project

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


class BasePostProcessor(ABC):

    def __init__(self, project: Project):

        self.project = project

        self.lines = []

    # =====================================
    # ОБЩИЙ МЕТОД
    # =====================================

    def process(self, toolpath):

        self.lines.clear()

        self.header()

        for command in toolpath:

            self.command(command)

        self.footer()

        return "\n".join(self.lines)

    # =====================================
    # ОБРАБОТКА КОМАНД
    # =====================================

    def command(self, cmd):

        if isinstance(cmd, Rapid):
            self.rapid(cmd)

        elif isinstance(cmd, Feed):
            self.feed(cmd)

        elif isinstance(cmd, ArcCW):
            self.arc_cw(cmd)

        elif isinstance(cmd, ArcCCW):
            self.arc_ccw(cmd)

        elif isinstance(cmd, ToolChange):
            self.tool_change(cmd)

        elif isinstance(cmd, SpindleOn):
            self.spindle_on(cmd)

        elif isinstance(cmd, SpindleOff):
            self.spindle_off(cmd)

        elif isinstance(cmd, CoolantOn):
            self.coolant_on(cmd)

        elif isinstance(cmd, CoolantOff):
            self.coolant_off(cmd)

        elif isinstance(cmd, Comment):
            self.comment(cmd)

    # =====================================
    # ОБЩИЕ ВСПОМОГАТЕЛЬНЫЕ
    # =====================================

    def xyz(self, cmd):

        parts = []

        if cmd.x is not None:
            parts.append(f"X{cmd.x:.3f}")

        if cmd.y is not None:
            parts.append(f"Y{cmd.y:.3f}")

        if cmd.z is not None:
            parts.append(f"Z{cmd.z:.3f}")

        return " ".join(parts)

    # =====================================
    # ОБЯЗАТЕЛЬНЫЕ МЕТОДЫ
    # =====================================

    @abstractmethod
    def header(self):
        ...

    @abstractmethod
    def footer(self):
        ...

    @abstractmethod
    def rapid(self, cmd):
        ...

    @abstractmethod
    def feed(self, cmd):
        ...

    @abstractmethod
    def arc_cw(self, cmd):
        ...

    @abstractmethod
    def arc_ccw(self, cmd):
        ...

    @abstractmethod
    def tool_change(self, cmd):
        ...

    @abstractmethod
    def spindle_on(self, cmd):
        ...

    @abstractmethod
    def spindle_off(self, cmd):
        ...

    @abstractmethod
    def coolant_on(self, cmd):
        ...

    @abstractmethod
    def coolant_off(self, cmd):
        ...

    @abstractmethod
    def comment(self, cmd):
        ...