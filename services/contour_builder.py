from services.path_planner import PathPlanner
from services.corners_v2 import (
    radius_corner,
    chamfer_corner,
    corner_enabled,
)


class ContourBuilder:

    def __init__(self):

        self.planner = PathPlanner()

    def build_rectangle(
        self,
        points,
        outside,
        climb,
        corner_type,
        corner_select,
        corner_value,
    ):

        if climb:

            order = list(points)

        else:

            order = [
                points[0],
                points[3],
                points[2],
                points[1],
            ]

        clockwise = (
            (outside and climb)
            or
            (not outside and not climb)
        )

        count = len(order)

        first_start = None
        last_end = None

        for i in range(count):

            prev = order[(i - 1) % count]
            cur = order[i]
            nxt = order[(i + 1) % count]

            use_corner = (
                corner_type != "none"
                and corner_value > 0
                and corner_enabled(
                    i + 1,
                    corner_select,
                )
            )
                        if use_corner:

                if corner_type == "radius":

                    corner = radius_corner(
                        prev,
                        cur,
                        nxt,
                        corner_value,
                        clockwise,
                    )

                else:

                    corner = chamfer_corner(
                        prev,
                        cur,
                        nxt,
                        corner_value,
                    )

            else:

                corner = None

            # Первый элемент
            if i == 0:

                if corner:

                    first_start = corner.start
                    last_end = corner.end

                else:

                    first_start = cur
                    last_end = cur

                continue

            # Строим прямую
            if corner:

                self.planner.add_line(
                    last_end,
                    corner.start,
                )

            else:

                self.planner.add_line(
                    last_end,
                    cur,
                )
                            # Строим угол
            if corner:

                if corner.chamfer:

                    self.planner.add_line(
                        corner.start,
                        corner.end,
                    )

                else:

                    self.planner.add_arc(
                        start=corner.start,
                        end=corner.end,
                        center=corner.center,
                        clockwise=corner.clockwise,
                    )

                last_end = corner.end

            else:

                last_end = cur

        # Замыкаем контур

        self.planner.add_line(
            last_end,
            first_start,
        )

        return self.planner.get_entities()