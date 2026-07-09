from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

@dataclass(slots=True)
class ToolPath:
    """
    Ordered sequence of machining commands.
    """
    commands: list = field(default_factory=list)

    def add(self, command) -> None:
        self.commands.append(command)

    def extend(self, commands: Iterable) -> None:
        self.commands.extend(commands)

    def clear(self) -> None:
        self.commands.clear()

    def copy(self) -> "ToolPath":
        tp = ToolPath()
        tp.commands = list(self.commands)
        return tp

    def __iter__(self):
        return iter(self.commands)

    def __len__(self):
        return len(self.commands)

    def __getitem__(self, index):
        return self.commands[index]
