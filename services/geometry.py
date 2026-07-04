from typing import List, Tuple

Point = Tuple[float, float]


def rectangle_points(
    length: float,
    width: float,
    zero: str,
    allowance: float = 0,
    outside: bool = True,
) -> List[Point]:
    """
    Возвращает точки прямоугольника.

    allowance:
        0 - чистовой контур
        >0 - черновой контур

    outside:
        True  - наружный контур
        False - внутренний контур
    """

    if outside:
        x0 = -allowance
        y0 = -allowance
        x1 = length + allowance
        y1 = width + allowance
    else:
        x0 = allowance
        y0 = allowance
        x1 = length - allowance
        y1 = width - allowance

    if zero == "↙️ Левый нижний":

        dx = 0
        dy = 0

    elif zero == "↖️ Левый верхний":

        dx = 0
        dy = -width

    elif zero == "↘️ Правый нижний":

        dx = -length
        dy = 0

    elif zero == "↗️ Правый верхний":

        dx = -length
        dy = -width

    elif zero == "⭕ Центр детали":

        dx = -length / 2
        dy = -width / 2

    else:
        raise ValueError(f"Неизвестный ноль детали: {zero}")

    return [
        (x0 + dx, y0 + dy),
        (x1 + dx, y0 + dy),
        (x1 + dx, y1 + dy),
        (x0 + dx, y1 + dy),
        (x0 + dx, y0 + dy),
    ]


def contour_start_point(
    first_point: Point,
    allowance: float,
    distance: float = 10.0,
) -> Point:
    """
    Точка безопасного захода.
    """

    x, y = first_point

    return (
        x - distance,
        y - distance,
    )