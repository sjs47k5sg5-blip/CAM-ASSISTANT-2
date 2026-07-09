from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Workpiece:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    zero: str = "CENTER"
    zero_z: str = "TOP"

@dataclass
class Tool:
    number: int = 1
    diameter: float = 10.0
    length_offset: int = 1

@dataclass
class Material:
    name: str = "Steel"

@dataclass
class Finish:
    enabled: bool = False
    allowance: float = 0.0
    another_tool: bool = False

@dataclass
class Machining:
    feed: float = 500.0
    step_z: float = 2.0

@dataclass
class Project:
    workpiece: Workpiece = field(default_factory=Workpiece)
    tool: Tool = field(default_factory=Tool)
    material: Material = field(default_factory=Material)
    finish: Finish = field(default_factory=Finish)
    machining: Machining = field(default_factory=Machining)
    contour: object | None = None
