from dataclasses import dataclass


@dataclass
class CamState:
    step: int = 0

    tool: int = 0
    zero: str = ""
    depth: float = 0.0
    stepdown: float = 0.0
    allowance: float = 0.0

    corner_type: str = ""
    corner_value: float = 0.0
    corner_scope: str = ""

    ready: bool = False


CAM_DB = {}