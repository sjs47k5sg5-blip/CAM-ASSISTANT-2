import math


def contour_feed(rpm: int, teeth: int, fz: float):
    """
    Расчет подачи.
    """
    return round(rpm * teeth * fz)


def contour_passes(depth: float, step: float):
    """
    Количество проходов по Z.
    """
    if step <= 0:
        return 1

    return math.ceil(depth / step)


def contour_time(length: float, width: float, passes: int, feed: float):
    """
    Приблизительное время обработки (сек).
    """
    if feed <= 0:
        return 0

    perimeter = (length + width) * 2

    return round((perimeter * passes / feed) * 60, 1)