import math

from services.material_service import get_modes


def face_mode(material, tool="Твердосплавная"):
    """
    Возвращает режимы резания для материала.
    """

    return get_modes(material, tool)


def face_feed(rpm, teeth, fz):
    """
    Расчет подачи.
    """

    return round(rpm * teeth * fz)


def face_step(diameter):
    """
    Рекомендуемый шаг между проходами.
    Принято 70% от диаметра фрезы.
    """

    return round(diameter * 0.7, 1)


def face_passes(width, step):
    """
    Количество проходов.
    """

    return math.ceil(width / step)


def face_time(length, passes, feed):
    """
    Приблизительное время обработки.
    """

    if feed <= 0:
        return 0

    travel = length * passes

    return round((travel / feed) * 60, 1)