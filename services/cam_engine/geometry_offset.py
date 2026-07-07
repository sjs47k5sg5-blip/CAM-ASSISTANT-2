from services.cam_engine.geometry import (
    rectangle,
    radius_rectangle,
    chamfer_rectangle,
)


# ==========================================
# OFFSET CONTOURS
# ==========================================

def build_offset_contours(project):

    p = project

    contours = []

    width = p.workpiece.x
    height = p.workpiece.y

    tool = p.tool.diameter

    allowance = p.finish.allowance

    stepover = p.machining.stepover

    if stepover <= 0:
        stepover = 0.6

    # Боковой шаг
    step = tool * stepover

    if step <= 0:
        step = tool * 0.6

    current = 0.0

    while True:

        w = width - current * 2
        h = height - current * 2

        # Оставляем припуск
        if w <= allowance * 2:
            break

        if h <= allowance * 2:
            break

        # Последний проход -- припуск
        if w - step * 2 < allowance * 2:
            w = width - allowance * 2
            h = height - allowance * 2

        # ------------------------------

        if p.corner.kind == "SHARP":

            contour = rectangle(

                width=w,

                height=h,

                tool=tool,

                zero=p.workpiece.zero,

            )

        elif p.corner.kind == "RADIUS":

            contour = radius_rectangle(

                width=w,

                height=h,

                radius=p.corner.value,

                tool=tool,

                zero=p.workpiece.zero,

                position=p.corner.position,

            )

        else:

            contour = chamfer_rectangle(

                width=w,

                height=h,

                chamfer=p.corner.value,

                tool=tool,

                zero=p.workpiece.zero,

                position=p.corner.position,

            )

        contours.append(contour)

        if w == width - allowance * 2:
            break

        current += step

    return contours