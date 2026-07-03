from typing import List, Tuple

Point = Tuple[float, float]


def rectangle_points(
    length: float,
    width: float,
    zero: str,
) -> List[Point]:
    """
    Возвращает вершины прямоугольника
    относительно выбранного нуля детали.
    """

    if zero == "↙️ Левый нижний":

        x0 = 0.0
        y0 = 0.0

    elif zero == "↖️ Левый верхний":

        x0 = 0.0
        y0 = -width

    elif zero == "↘️ Правый нижний":

        x0 = -length
        y0 = 0.0

    elif zero == "↗️ Правый верхний":

        x0 = -length
        y0 = -width

    elif zero == "⭕ Центр детали":

        x0 = -length / 2
        y0 = -width / 2

    else:
        raise ValueError(f"Неизвестный ноль детали: {zero}")

    return [
        (x0, y0),
        (x0 + length, y0),
        (x0 + length, y0 + width),
        (x0, y0 + width),
        (x0, y0),
    ]


def contour_start_point(
    first_point: Point,
    allowance: float,
    distance: float = 10.0,
) -> Point:
    """
    Возвращает безопасную точку захода
    перед первым углом контура.
    """

    x, y = first_point

    return (
        x - allowance - distance,
        y - allowance - distance,
    )