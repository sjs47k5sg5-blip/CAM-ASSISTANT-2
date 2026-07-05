import math

from services.vector import (
    add,
    sub,
    mul,
    normalize,
    left_normal,
    right_normal,
)


def arc_center(
    start,
    end,
    radius,
    clockwise,
):
    """
    Вычисляет центр дуги по двум точкам и радиусу.
    """

    sx, sy = start
    ex, ey = end

    dx = ex - sx
    dy = ey - sy

    chord = math.hypot(dx, dy)

    if chord == 0:
        raise ValueError("Начало и конец дуги совпадают.")

    if chord > radius * 2:
        raise ValueError("Радиус меньше половины хорды.")

    mid = (
        (sx + ex) / 2,
        (sy + ey) / 2,
    )

    h = math.sqrt(radius * radius - (chord / 2) ** 2)

    direction = normalize((dx, dy))

    if clockwise:
        normal = right_normal(direction)
    else:
        normal = left_normal(direction)

    center = add(
        mid,
        mul(normal, h),
    )

    return center


def ij(
    start,
    center,
):
    """
    Возвращает I и J
    относительно начала дуги.
    """

    return (
        center[0] - start[0],
        center[1] - start[1],
    )