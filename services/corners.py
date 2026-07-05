import math


def corner_enabled(
    corner: int,
    selected: str,
) -> bool:

    if selected in ("all", "Все углы"):
        return True

    names = {
        1: "↙️ Левый нижний",
        2: "↘️ Правый нижний",
        3: "↗️ Правый верхний",
        4: "↖️ Левый верхний",
    }

    return names.get(corner) == selected


def _normalize(x, y):
    length = math.hypot(x, y)

    if length == 0:     
        return 0.0, 0.0

    return x / length, y / length


def chamfer_points(
    prev,
    corner,
    nxt,
    size,
):
    """
    Возвращает две точки фаски.
    """

    x0, y0 = prev
    x1, y1 = corner
    x2, y2 = nxt

    vx1 = x0 - x1
    vy1 = y0 - y1
    vx1, vy1 = _normalize(vx1, vy1)

    vx2 = x2 - x1
    vy2 = y2 - y1
    vx2, vy2 = _normalize(vx2, vy2)

    start = (
        x1 + vx1 * size,
        y1 + vy1 * size,
    )

    end = (
        x1 + vx2 * size,
        y1 + vy2 * size,
    )

    return start, end


def radius_points(
    prev,
    corner,
    nxt,
    radius,
):
    """
    Возвращает две точки касания радиуса.
    """

    x0, y0 = prev
    x1, y1 = corner
    x2, y2 = nxt

    vx1 = x0 - x1
    vy1 = y0 - y1
    vx1, vy1 = _normalize(vx1, vy1)

    vx2 = x2 - x1
    vy2 = y2 - y1
    vx2, vy2 = _normalize(vx2, vy2)

    start = (
        x1 + vx1 * radius,
        y1 + vy1 * radius,
    )

    end = (
        x1 + vx2 * radius,
        y1 + vy2 * radius,
    )

    return start, end


def radius_arc(
    prev,
    corner,
    nxt,
    radius,
):
    """
    Возвращает:
    start,
    end,
    center
    для построения дуги через I/J.
    """

    x0, y0 = prev
    x1, y1 = corner
    x2, y2 = nxt

    vx1 = x0 - x1
    vy1 = y0 - y1
    vx1, vy1 = _normalize(vx1, vy1)

    vx2 = x2 - x1
    vy2 = y2 - y1
    vx2, vy2 = _normalize(vx2, vy2)

    start = (
        x1 + vx1 * radius,
        y1 + vy1 * radius,
    )

    end = (
        x1 + vx2 * radius,
        y1 + vy2 * radius,
    )

    bis_x = vx1 + vx2
    bis_y = vy1 + vy2
    bis_x, bis_y = _normalize(bis_x, bis_y)

    angle = math.acos(
        max(
            -1.0,
            min(
                1.0,
                vx1 * vx2 + vy1 * vy2,
            ),
        )
    )

    if angle == 0:
        center = corner
    else:
        distance = radius / math.sin(angle / 2)

        center = (
            x1 + bis_x * distance,
            y1 + bis_y * distance,
        )

    return start, end, center