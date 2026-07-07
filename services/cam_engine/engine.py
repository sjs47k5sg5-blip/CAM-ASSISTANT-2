from services.cam_engine.models import Project
from services.cam_engine.operations.contour import ContourOperation
from services.cam_engine.postprocessors.fanuc_oi_mf import FanucOiMFPost


class CamEngine:

    def __init__(self, project: Project):

        self.project = project

    # =====================================
    # КОНТУР
    # =====================================

    def generate_contour(self) -> str:

        operation = ContourOperation(self.project)

        toolpath = operation.build()

        post = FanucOiMFPost(self.project)

        return post.process(toolpath)


# =====================================
# ВНЕШНИЙ ИНТЕРФЕЙС
# =====================================

def generate_contour(project: Project) -> str:

    engine = CamEngine(project)

    return engine.generate_contour()