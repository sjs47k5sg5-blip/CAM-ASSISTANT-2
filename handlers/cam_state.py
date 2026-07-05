from dataclasses import dataclass


@dataclass
class CamState:
    step: int = 0

    tool: int = 0
    zero: str = ""
    depth: float = 5.0
    stepdown: float = 2.0
    allowance: float = 0.2

    corner_type: str = ""
    corner_value: float = 0.0
    corner_scope: str = ""

    ready: bool = False


# 💥 ВАЖНО: ЭТО ОБЯЗАТЕЛЬНО ДЛЯ ИМПОРТА
CAM_MEMORY = {}