from dataclasses import dataclass
import math

from services.vector import (
    add,
    sub,
    mul,
    normalize,
    length,
    left_normal,
    right_normal,
)


@dataclass
class CornerData:
    start: tuple
    end: tuple
    center: tuple | None
    radius: float
    chamfer: bool
    clockwise: bool


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


def chamfer_corner(
    prev,
    corner,
    nxt,
    size,
):

    v1 = normalize(sub(prev, corner))
    v2 = normalize(sub(nxt, corner))

    start = add(
        corner,
        mul(v1, size),
    )

    end = add(
        corner,
        mul(v2, size),
    )

    return CornerData(
        start=start,
        end=end,
        center=None,
        radius=0,
        chamfer=True,
        clockwise=False,
    )


def radius_corner(
    prev,
    corner,
    nxt,
    radius,
    clockwise,
):

    v1 = normalize(sub(prev, corner))
    v2 = normalize(sub(nxt, corner))

    start = add(
        corner,
        mul(v1, radius),
    )

    end = add(
        corner,
        mul(v2, radius),
    )

    bisector = normalize(
        add(v1, v2)
    )

    angle = math.acos(
        max(
            -1,
            min(
                1,
                v1[0] * v2[0] +
                v1[1] * v2[1]
            ),
        )
    )

    d = radius / math.sin(angle / 2)

    center = add(
        corner,
        mul(bisector, d),
    )

    return CornerData(
        start=start,
        end=end,
        center=center,
        radius=radius,
        chamfer=False,
        clockwise=clockwise,
    )