from dataclasses import dataclass


@dataclass
class CamState:

    step: int = 0

    # geometry
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    material: str = "ALU"

    zero: str = "CENTER"
    zero_z: str = "TOP"

    corner_mode: str = "STRAIGHT"
    corner_target: str = "ALL"
    corner_value: float = 0.0

    allowance: float = 0.0

    tool_d: float = 0.0
    finish: bool = False
    finish_pass: str = "NO"


CAM_DB = {}