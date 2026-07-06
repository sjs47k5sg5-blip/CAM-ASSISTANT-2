from dataclasses import dataclass


@dataclass
class CamState:
    step: int = 0

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    material: str = ""
    zero: str = ""
    zero_z: str = ""

    corner_target: str = ""
    corner_mode: str = ""
    corner_value: float = 0.0

    allowance: float = 0.0
    tool_d: float = 0.0


CAM_DB = {}