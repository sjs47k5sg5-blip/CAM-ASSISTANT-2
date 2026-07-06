from dataclasses import dataclass


@dataclass
class CamState:
    step: int = 0

    size_x: float = 0.0
    size_y: float = 0.0
    size_z: float = 0.0

    tool: float = 0.0
    corner_value: float = 0.0

    zero: str = "CENTER"
    mode: str = "CONTOUR"


CAM_DB = {}