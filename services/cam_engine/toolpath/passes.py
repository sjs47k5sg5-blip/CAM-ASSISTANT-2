from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class PassLevel:
    depth: float
    finish: bool=False

class PassPlanner:
    """
    Builds Z-level machining passes.
    """

    def build(self,total_depth:float,step_down:float,finish_allowance:float=0.0)->list[PassLevel]:
        if total_depth<=0:
            return []
        levels=[]
        depth=step_down
        while depth<total_depth:
            levels.append(PassLevel(depth=depth))
            depth+=step_down
        finish_depth=total_depth-finish_allowance
        if finish_depth>0 and (not levels or levels[-1].depth!=finish_depth):
            levels.append(PassLevel(depth=finish_depth))
        if finish_allowance>0:
            levels.append(PassLevel(depth=total_depth,finish=True))
        return levels
