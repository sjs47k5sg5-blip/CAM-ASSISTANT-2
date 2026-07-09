from __future__ import annotations

from .toolpath.builder import ToolPathBuilder
from .toolpath.passes import PassPlanner
from .toolpath.lead_in import LeadIn
from .toolpath.lead_out import LeadOut
from .postprocessors.fanuc_oi_mf import FanucOiMFPost


class CamEngine:
    """
    CAM Engine
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

    def generate_gcode(self, contour, feed, total_depth, step_down):
        result = self.build_contour(
            contour,
            feed,
            total_depth,
            step_down,
        )

        post = FanucOiMFPost()

        return post.generate(result["toolpath"])


def generate_contour(project):
    """
    Совместимость со старыми обработчиками Telegram-бота.
    """

    engine = CamEngine()

    contour = getattr(project, "contour", None)
    if contour is None:
        raise ValueError("Контур проекта не задан")

    feed = getattr(project.machining, "feed", 500.0)
    total_depth = getattr(project.workpiece, "z", 0.0)
    step_down = getattr(project.machining, "step_z", 1.0)

    return engine.generate_gcode(
        contour=contour,
        feed=feed,
        total_depth=total_depth,
        step_down=step_down,
    )