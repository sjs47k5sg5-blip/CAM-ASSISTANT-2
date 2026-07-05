from services.vector import (
    add,
    sub,
    mul,
    normalize,
    left_normal,
    right_normal,
)


def offset_segment(
    start,
    end,
    distance,
    outside=True,
    clockwise=True,
):
    """
    Смещает один отрезок на заданное расстояние.
    Возвращает новые точки начала и конца.
    """

    direction = normalize(
        sub(end, start)
    )

    if outside:

        normal = (
            right_normal(direction)
            if clockwise
            else left_normal(direction)
        )

    else:

        normal = (
            left_normal(direction)
            if clockwise
            else right_normal(direction)
        )

    shift = mul(normal, distance)

    return (
        add(start, shift),
        add(end, shift),
    )


def offset_rectangle(
    points,
    distance,
    outside=True,
):
    """
    Смещает прямоугольник.

    Пока используется для контуров.
    Позже станет частью общего Offset Engine.
    """

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    xmin = min(x)
    xmax = max(x)

    ymin = min(y)
    ymax = max(y)

    if outside:

        xmin -= distance
        ymin -= distance

        xmax += distance
        ymax += distance

    else:

        xmin += distance
        ymin += distance

        xmax -= distance
        ymax -= distance

    return [

        (xmin, ymin),

        (xmax, ymin),

        (xmax, ymax),

        (xmin, ymax),

    ]