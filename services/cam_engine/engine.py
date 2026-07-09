from __future__ import annotations

from .toolpath.builder import ToolPathBuilder
from .toolpath.passes import PassPlanner
from .toolpath.lead_in import LeadIn
from .toolpath.lead_out import LeadOut

class CamEngine:
    """
    First CAM engine pipeline.
    """

    def __init__(self):
        self.builder = ToolPathBuilder()
        self.pass_planner = PassPlanner()
        self.lead_in = LeadIn()
        self.lead_out = LeadOut()

    def build_contour(self, contour, feed, total_depth, step_down):
        toolpath = self.builder.build_contour(contour, feed)
        passes = self.pass_planner.build(total_depth, step_down)
        return {
            "toolpath": toolpath,
            "passes": passes,
            "lead_in": self.lead_in.build(contour.start),
            "lead_out": self.lead_out.build(contour.end),
        }


from .postprocessors.fanuc_oi_mf import FanucOiMFPost

    def generate_gcode(self, contour, feed, total_depth, step_down):
        result = self.build_contour(contour, feed, total_depth, step_down)
        post = FanucOiMFPost()
        return post.generate(result["toolpath"])
