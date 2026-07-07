# ==========================================
# ПОСТРОЕНИЕ ПРОХОДОВ ПО ГЛУБИНЕ
# ==========================================

def build_passes(depth: float, step: float):

    """
    Возвращает список глубин проходов.

    Пример:

    depth = 10
    step = 3

    вернет:

    [-3, -6, -9, -10]
    """

    if depth <= 0:
        return []

    if step <= 0:
        step = depth

    passes = []

    current = 0.0

    while True:

        current -= step

        if current < -depth:
            current = -depth

        passes.append(current)

        if current <= -depth:
            break

    return passes