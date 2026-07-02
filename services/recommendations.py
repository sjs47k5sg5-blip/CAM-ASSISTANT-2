from services.machine import max_rpm

MAX_RPM = max_rpm()


def adjust_modes(vc: float, fz: float, overhang: float, machining: str):
    """
    Корректировка режимов резания.

    vc - скорость резания (м/мин)
    fz - подача на зуб (мм)
    overhang - вылет инструмента (мм)
    machining - Черновая / Получистовая / Чистовая
    """

    warning = ""

    # Коррекция по вылету
    if overhang >= 80:
        vc *= 0.75
        fz *= 0.85
        warning += "⚠ Большой вылет инструмента (>80 мм).\n"

    elif overhang >= 60:
        vc *= 0.85
        fz *= 0.90
        warning += "⚠ Увеличенный вылет инструмента.\n"

    elif overhang >= 40:
        vc *= 0.93
        fz *= 0.95

    # Коррекция по типу обработки
    if machining == "Чистовая":
        vc *= 1.10
        fz *= 0.80

    elif machining == "Получистовая":
        vc *= 1.00
        fz *= 0.90

    elif machining == "Черновая":
        vc *= 0.95
        fz *= 1.10

    return round(vc, 1), round(fz, 3), warning


def limit_rpm(rpm: int):
    """
    Ограничение оборотов шпинделя.
    """

    if rpm > MAX_RPM:
        return MAX_RPM, (
            f"⚠ Обороты ограничены возможностями станка "
            f"({MAX_RPM} об/мин)."
        )

    return rpm, ""


def recommend_ap_ae(diameter: float, machining: str):
    """
    Рекомендуемые глубина (Ap) и ширина (Ae)
    в зависимости от типа обработки.
    """

    if machining == "Черновая":
        ap = diameter * 1.0
        ae = diameter * 0.50

    elif machining == "Получистовая":
        ap = diameter * 0.70
        ae = diameter * 0.35

    else:  # Чистовая
        ap = diameter * 0.20
        ae = diameter * 0.10

    return round(ap, 1), round(ae, 1)


def coolant(tool: str, material: str):
    """
    Рекомендации по охлаждению.
    """

    if "Нержавейка" in material:
        return "Эмульсия высокого давления"

    if tool == "HSS":
        return "Обязательно использовать эмульсию"

    return "Эмульсия"


def spindle_load(feed: int):
    """
    Примерная оценка нагрузки на шпиндель.
    """

    if feed < 500:
        return "🟢 Низкая"

    if feed < 1500:
        return "🟡 Средняя"

    return "🔴 Высокая"