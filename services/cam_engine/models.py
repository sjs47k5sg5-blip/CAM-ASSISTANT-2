from dataclasses import dataclass, field


# ==========================================
# TOOL
# ==========================================

@dataclass
class Tool:

    number: int

    diameter: float

    flutes: int = 2

    length_offset: int | None = None

    spindle: int = 3000

    feed: int = 300

    plunge: int = 120


# ==========================================
# MATERIAL
# ==========================================

@dataclass
class Material:

    name: str

    vc: float = 150

    fz: float = 0.05


# ==========================================
# WORKPIECE
# ==========================================

@dataclass
class Workpiece:

    x: float

    y: float

    z: float

    zero: str = "CENTER"

    zero_z: str = "TOP"

    step_z: float = 2.0


# ==========================================
# CORNER
# ==========================================

@dataclass
class Corner:

    # SHARP / RADIUS / CHAMFER
    kind: str = "SHARP"

    # Какие углы обрабатывать
    positions: list[str] = field(
        default_factory=lambda: [
            "TL",
            "TR",
            "BL",
            "BR",
        ]
    )

    # Радиус или фаска
    value: float = 0.0


# ==========================================
# FINISH
# ==========================================

@dataclass
class Finish:

    allowance: float = 0.0

    enabled: bool = False

    another_tool: bool = False


# ==========================================
# MACHINING
# ==========================================

@dataclass
class Machining:

    # CLIMB / CONVENTIONAL
    direction: str = "CLIMB"

    # Черновая
    roughing: bool = False

    # Боковой шаг
    stepover: float = 0.6

    # Шаг по Z
    step_z: float = 2.0


# ==========================================
# TOOL COMPENSATION
# ==========================================

@dataclass
class Compensation:

    enabled: bool = False

    side: str = "LEFT"

    d_number: int = 1


# ==========================================
# ROUGHING
# ==========================================

@dataclass
class Roughing:

    enabled: bool = False

    stepover: float = 0.6

    strategy: str = "OUTSIDE_IN"

    direction: str = "CLIMB"


# ==========================================
# MACHINE
# ==========================================

@dataclass
class Machine:

    name: str = "Victor Center 136"

    controller: str = "Fanuc Oi-MF"

    safe_z: float = 100.0

    rapid_z: float = 5.0

    spindle_max: int = 15000


# ==========================================
# PROJECT
# ==========================================

@dataclass
class Project:

    workpiece: Workpiece

    tool: Tool

    material: Material

    corner: Corner

    finish: Finish

    machining: Machining

    machine: Machine