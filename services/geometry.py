from typing import List, Tuple

Point = Tuple[float, float]


def rectangle_points(
    length: float,
    width: float,
    zero: str,
    allowance: float = 0.0,
    outside: bool = True,
) -> List[Point]:
    """
    Возвращает вершины прямоугольника с учетом
    наружного/внутреннего контура и припуска.
    """

    offset = allowance if outside else -allowance

    if zero == "↙️ Левый нижний":

        x0 = -offset
        y0 = -offset

    elif zero == "↖️ Левый верхний":

        x0 = -offset
        y0 = -width + offset

    elif zero == "↘️ Правый нижний":

        x0 = -length + offset
        y0 = -offset

    elif zero == "↗️ Правый верхний":

        x0 = -length + offset
        y0 = -width + offset

    elif zero == "⭕ Центр детали":

        x0 = -length / 2 - offset
        y0 = -width / 2 - offset

    else:
        raise ValueError(f"Неизвестный ноль детали: {zero}")

    return [
        (x0, y0),
        (x0 + length + offset * 2, y0),
        (x0 + length + offset * 2, y0 + width + offset * 2),
        (x0, y0 + width + offset * 2),
    ]


def contour_start_point(
    first_point: Point,
    allowance: float,
    outside: bool = True,
    distance: float = 10.0,
) -> Point:
    """
    Возвращает безопасную точку захода.
    """

    x, y = first_point

    if outside:
        return (
            x - allowance - distance,
            y - allowance - distance,
        )

    return (
        x + allowance - distance,
        y + allowance - distance,
    )

from typing import Tuple

Point = Tuple[float, float]


def rectangle_vertices(
    length: float,
    width: float,
):
    """
    Возвращает вершины прямоугольника
    без смещения.
    """

    return [
        (0.0, 0.0),
        (length, 0.0),
        (length, width),
        (0.0, width),
    ]


def close_path(points):
    """
    Замыкает контур.
    """

    if not points:
        return []

    if points[0] == points[-1]:
        return points

    return points + [points[0]]


def reverse_path(points):
    """
    Разворачивает направление обхода.
    """

    return list(reversed(points))