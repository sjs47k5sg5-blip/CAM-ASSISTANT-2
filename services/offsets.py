from typing import Tuple

Point = Tuple[float, float]


def offset_rectangle(
    length: float,
    width: float,
    offset: float,
    outside: bool,
):

    if outside:

        x0 = -offset
        y0 = -offset

        x1 = length + offset
        y1 = width + offset

    else:

        x0 = offset
        y0 = offset

        x1 = length - offset
        y1 = width - offset

    return [
        (x0, y0),
        (x1, y0),
        (x1, y1),
        (x0, y1),
    ]