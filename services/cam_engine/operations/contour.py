from services.cam_engine.models import Project
from services.cam_engine.geometry import (
    rectangle,
    radius_rectangle,
    chamfer_rectangle,
)
from services.cam_engine.toolpath import (
    ToolPath,
    Rapid,
    Feed,
    ArcCW,
)


class ContourOperation:

    def __init__(self, project: Project):
        self.project = project

    # =====================================
    # ПОСТРОИТЬ ТРАЕКТОРИЮ
    # =====================================

    def build(self):

        p = self.project

        x = p.workpiece.x
        y = p.workpiece.y
        depth = p.workpiece.z

        tool = p.tool.diameter

        allowance = p.finish.allowance

        step = p.workpiece.step_z

        if step <= 0:
            step = 2.0

        x -= allowance * 2
        y -= allowance * 2

        if x <= 0 or y <= 0:
            raise ValueError("Припуск слишком большой.")

        # ---------------------------------

        if p.corner.kind == "SHARP":

            points = rectangle(
                width=x,
                height=y,
                tool=tool,
                zero=p.workpiece.zero,
            )

        elif p.corner.kind == "RADIUS":

            points = radius_rectangle(
                width=x,
                height=y,
                radius=p.corner.value,
                tool=tool,
                zero=p.workpiece.zero,
                position=p.corner.position,
            )

        elif p.corner.kind == "CHAMFER":

            points = chamfer_rectangle(
                width=x,
                height=y,
                chamfer=p.corner.value,
                tool=tool,
                zero=p.workpiece.zero,
                position=p.corner.position,
            )

        else:

            raise ValueError("Неизвестный тип углов.")

        # ---------------------------------

        tp = ToolPath()

        first = points[0]

        tp.add(
            Rapid(
                x=first.x,
                y=first.y,
            )
        )

        current = 0.0

        while True:

            current -= step

            if current < -depth:
                current = -depth

            tp.add(
                Feed(
                    z=current
                )
            )

            for point in points[1:]:

                if hasattr(point, "radius"):

                    tp.add(
                        ArcCW(
                            x=point.x,
                            y=point.y,
                            i=point.i,
                            j=point.j,
                        )
                    )

                else:

                    tp.add(
                        Feed(
                            x=point.x,
                            y=point.y,
                        )
                    )

            if current <= -depth:
                break

        # ---------------------------------
        # Чистовой проход
        # ---------------------------------

        if p.finish.enabled:

            for point in points[1:]:

                if hasattr(point, "radius"):

                    tp.add(
                        ArcCW(
                            x=point.x,
                            y=point.y,
                            i=point.i,
                            j=point.j,
                        )
                    )

                else:

                    tp.add(
                        Feed(
                            x=point.x,
                            y=point.y,
                        )
                    )

        return tp