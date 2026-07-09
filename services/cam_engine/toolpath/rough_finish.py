from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class MachiningPass:
    depth: float
    allowance: float
    finish: bool=False

class RoughFinishPlanner:
    """
    Builds roughing and finishing passes.
    """

    def build(self,total_depth:float,step_down:float,finish_allowance:float)->list[MachiningPass]:
        passes=[]
        depth=step_down
        while depth<max(total_depth-finish_allowance,0):
            passes.append(MachiningPass(depth,finish_allowance,False))
            depth+=step_down
        if finish_allowance>0:
            passes.append(MachiningPass(total_depth-finish_allowance,finish_allowance,False))
            passes.append(MachiningPass(total_depth,0.0,True))
        else:
            passes.append(MachiningPass(total_depth,0.0,True))
        return passes
