from services.cam_engine.models import Project

from services.cam_engine.geometry import (
    rectangle,
    radius_rectangle,
    chamfer_rectangle,
)

from services.cam_engine.geometry_offset import (
    build_offset_contours,
)

from services.cam_engine.operations.passes import (
    build_passes,
)

from services.cam_engine.operations.finish import (
    build_finish,
)

from services.cam_engine.operations.leadin import (
    build_leadin,
)

from services.cam_engine.operations.leadout import (
    build_leadout,
)

from services.cam_engine.toolpath import (
    ToolPath,
    Feed,
    ArcCW,
)


class ContourOperation:

    def __init__(self, project: Project):
        self.project = project

    # =====================================
    # ГЕОМЕТРИЯ
    # =====================================

    def build_geometry(self):

        p = self.project

        width = p.workpiece.x
        height = p.workpiece.y

        allowance = p.finish.allowance

        width -= allowance * 2
        height -= allowance * 2

        if width <= 0 or height <= 0:
            raise ValueError("Припуск слишком большой.")

        if p.machining.roughing:

            contours = build_offset_contours(p)

        else:

            if p.corner.kind == "SHARP":

                contours = [
                    rectangle(
                        width=width,
                        height=height,
                        tool=p.tool.diameter,
                        zero=p.workpiece.zero,
                    )
                ]

            elif p.corner.kind == "RADIUS":

                contours = [
                    radius_rectangle(
                        width=width,
                        height=height,
                        radius=p.corner.value,
                        tool=p.tool.diameter,
                        zero=p.workpiece.zero,
                        position=p.corner.position,
                    )
                ]

            elif p.corner.kind == "CHAMFER":

                contours = [
                    chamfer_rectangle(
                        width=width,
                        height=height,
                        chamfer=p.corner.value,
                        tool=p.tool.diameter,
                        zero=p.workpiece.zero,
                        position=p.corner.position,
                    )
                ]

            else:

                raise ValueError("Неизвестный тип углов.")

        # =====================================
        # ВСТРЕЧНОЕ ФРЕЗЕРОВАНИЕ
        # =====================================

        if p.machining.direction == "CONVENTIONAL":

            result = []

            for contour in contours:

                first = contour[0]
                body = contour[1:-1]

                body.reverse()

                result.append(
                    [first] + body + [first]
                )

            contours = result

        return contours

    # =====================================
    # BUILD
    # =====================================

    def build(self):

        p = self.project

        contours = self.build_geometry()

        toolpath = ToolPath()

        for z in build_passes(

            depth=p.workpiece.z,

            step=p.machining.step_z,

        ):

            # ---------------------------------
            # Один подвод
            # ---------------------------------

            first = contours[0][0]

            build_leadin(

                toolpath=toolpath,

                point=first,

                depth=z,

                safe_z=p.machine.safe_z,

                rapid_z=p.machine.rapid_z,

                plunge_feed=p.tool.plunge,

            )

            # ---------------------------------
            # Все контуры на одной глубине
            # ---------------------------------

            for contour in contours:

                start = contour[0]

                toolpath.add(

                    Feed(

                        x=start.x,

                        y=start.y,

                        feed=p.tool.feed,

                    )

                )

                for point in contour[1:]:

                    if hasattr(point, "radius"):

                        toolpath.add(

                            ArcCW(

                                x=point.x,

                                y=point.y,

                                i=point.i,

                                j=point.j,

                                feed=p.tool.feed,

                            )

                        )

                    else:

                        toolpath.add(

                            Feed(

                                x=point.x,

                                y=point.y,

                                feed=p.tool.feed,

                            )

                        )

            # ---------------------------------
            # Один отход
            # ---------------------------------

            build_leadout(

                toolpath,

                p.machine.safe_z,

            )

        # =====================================
        # ЧИСТОВОЙ ПРОХОД
        # =====================================

        if p.finish.enabled:

            build_finish(

                toolpath=toolpath,

                contour=contours[0],

                depth=p.workpiece.z,

            )

        return toolpath