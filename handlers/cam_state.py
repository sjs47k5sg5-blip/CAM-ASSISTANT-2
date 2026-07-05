from dataclasses import dataclass, field


@dataclass
class CamState:
    tool: int = 10
    zero: str = "CENTER"
    depth: float = 5.0
    stepdown: float = 2.0
    allowance: float = 0.2
    corner_type: str = "ОСТРЫЕ"
    corner_value: float = 5.0
    corner_mode: str = "ALL"


# глобальное хранилище (простое)
CAM_MEMORY = {}