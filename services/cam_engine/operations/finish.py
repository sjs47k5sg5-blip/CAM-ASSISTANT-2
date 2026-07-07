from services.cam_engine.toolpath import (
    Rapid,
    Feed,
    ArcCW,
)


def build_finish(toolpath, contour, depth):

    if not contour:
        return

    first = contour[0]

    toolpath.add(
        Rapid(
            x=first.x,
            y=first.y,
        )
    )

    toolpath.add(
        Feed(
            z=-depth,
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
                )
            )

        else:

            toolpath.add(
                Feed(
                    x=point.x,
                    y=point.y,
                )
            )