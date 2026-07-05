def corner_enabled(index: int, mode):

    # отключено
    if mode is None:
        return False

    if mode == "none":
        return False

    # все углы включены
    if mode == "all":
        return True

    # список [1,2,3]
    if isinstance(mode, (list, tuple)):
        return index in mode

    # строка "1,2,3"
    if isinstance(mode, str):
        try:
            parts = mode.split(",")
            allowed = [int(p.strip()) for p in parts if p.strip().isdigit()]
            return index in allowed
        except:
            return True

    # fallback (не ломаем систему)
    return True


def chamfer_points(prev, cur, nxt, value):
    """
    простая фаска (safe version)
    """
    # входная точка (упрощённо)
    start = (
        cur[0] + (prev[0] - cur[0]) * 0.2,
        cur[1] + (prev[1] - cur[1]) * 0.2,
    )

    # выходная точка
    end = (
        cur[0] + (nxt[0] - cur[0]) * 0.2,
        cur[1] + (nxt[1] - cur[1]) * 0.2,
    )

    return start, end


def radius_arc(prev, cur, nxt, radius):
    """
    стабильная дуга (I/J safe)
    """

    # середина для центра (упрощённый стабильный вариант)
    start = (
        cur[0] + (prev[0] - cur[0]) * 0.3,
        cur[1] + (prev[1] - cur[1]) * 0.3,
    )

    end = (
        cur[0] + (nxt[0] - cur[0]) * 0.3,
        cur[1] + (nxt[1] - cur[1]) * 0.3,
    )

    center = (
        cur[0],
        cur[1],
    )

    return start, end, center