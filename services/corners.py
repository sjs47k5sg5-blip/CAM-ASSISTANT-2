from typing import Tuple

Point = Tuple[float, float]


def corner_enabled(
    corner: int,
    selected: str,
) -> bool:
    """
    Проверяет, нужно ли обрабатывать данный угол.
    """

    if selected == "Все углы":
        return True

    names = {
        1: "↙️ Левый нижний",
        2: "↘️ Правый нижний",
        3: "↗️ Правый верхний",
        4: "↖️ Левый верхний",
    }

    return names.get(corner) == selected


def chamfer_points(
    p_prev: Point,
    p: Point,
    p_next: Point,
    size: float,
):

    x1, y1 = p_prev
    x2, y2 = p
    x3, y3 = p_next

    # точка входа
    if x1 == x2:
        start = (
            x2,
            y2 - size if y1 < y2 else y2 + size,
        )
    else:
        start = (
            x2 - size if x1 < x2 else x2 + size,
            y2,
        )

    # точка выхода
    if x2 == x3:
        end = (
            x2,
            y2 + size if y3 > y2 else y2 - size,
        )
    else:
        end = (
            x2 + size if x3 > x2 else x2 - size,
            y2,
        )

    return start, end


def radius_points(
    p_prev: Point,
    p: Point,
    p_next: Point,
    radius: float,
):

    x1, y1 = p_prev
    x2, y2 = p
    x3, y3 = p_next

    # начало дуги
    if x1 == x2:
        start = (
            x2,
            y2 - radius if y1 < y2 else y2 + radius,
        )
    else:
        start = (
            x2 - radius if x1 < x2 else x2 + radius,
            y2,
        )

    # конец дуги
    if x2 == x3:
        end = (
            x2,
            y2 + radius if y3 > y2 else y2 - radius,
        )
    else:
        end = (
            x2 + radius if x3 > x2 else x2 - radius,
            y2,
        )

    return start, end