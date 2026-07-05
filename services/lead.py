import math


def _offset_point(x, y, dx, dy, dist):
    """Сдвиг точки вдоль нормали"""
    length = math.hypot(dx, dy)
    if length == 0:
        return x, y

    nx = -dy / length
    ny = dx / length

    return x + nx * dist, y + ny * dist


def lead_in(x, y, radius=5.0, outside=True, climb=True):

    start_x = x - radius
    start_y = y

    i = start_x - x
    j = start_y - y

    return [
        f"G01 X{start_x:.3f} Y{start_y:.3f}",
        f"G02 X{x:.3f} Y{y:.3f} I{i:.3f} J{j:.3f}",
    ]


def lead_out(x, y, radius=5.0, outside=True, climb=True):

    end_x = x - radius
    end_y = y

    i = x - end_x
    j = y - end_y

    return [
        f"G03 X{end_x:.3f} Y{end_y:.3f} I{i:.3f} J{j:.3f}",
        "G40",
    ]