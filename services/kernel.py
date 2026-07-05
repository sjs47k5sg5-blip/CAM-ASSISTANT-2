from services.path_planner import PathPlanner
from services.post_fanuc import FanucPost


class CamKernel:

    def __init__(self):

        self.planner = PathPlanner()
        self.post = FanucPost()

    def clear(self):

        self.planner.clear()

    def entities(self):

        return self.planner.get_entities()

    def gcode(self):

        return self.post.build(
            self.planner.get_entities()
        )