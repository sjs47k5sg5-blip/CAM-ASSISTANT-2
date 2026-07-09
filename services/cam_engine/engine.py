from __future__ import annotations

from .toolpath.builder import ToolPathBuilder
from .toolpath.passes import PassPlanner
from .toolpath.lead_in import LeadIn
from .toolpath.lead_out import LeadOut
from .postprocessors.fanuc_oi_mf import FanucOiMFPost

class CamEngine:
    def __init__(self):
        self.builder=ToolPathBuilder()
        self.pass_planner=PassPlanner()
        self.lead_in=LeadIn()
        self.lead_out=LeadOut()

    def generate_gcode(self, contour, feed, total_depth, step_down):
        z_levels=self.pass_planner.build(total_depth, step_down)
        toolpath=self.builder.build_contour(contour, feed, z_levels=z_levels)
        return FanucOiMFPost().generate(toolpath)

def generate_contour(project):
    return CamEngine().generate_gcode(
        contour=project.contour,
        feed=getattr(project.machining,"feed",500.0),
        total_depth=getattr(project.workpiece,"z",0.0),
        step_down=getattr(project.machining,"step_z",1.0),
    )
