import json
import math
from pathlib import Path

DATA_FILE = Path("data/drilling.json")

with open(DATA_FILE, encoding="utf-8") as f:
    DRILLING = json.load(f)


MAX_RPM = 15000


def spindle_speed(vc: float, diameter: float) -> int:
    """Расчет оборотов шпинделя"""
    rpm = (1000 * vc) / (math.pi * diameter)

    if rpm > MAX_RPM:
        rpm = MAX_RPM

    return round(rpm)


def feed_rate(rpm: int, fn: float) -> int:
    """Минутная подача"""
    return round(rpm * fn)


def get_cutting_data(material: str,
                     drill_type: str,
                     diameter: float):

    data = DRILLING[material][drill_type]

    vc = data["vc"]

    table = data["fn"]

    diameters = sorted(
        [float(x) for x in table.keys()]
    )

    nearest = min(
        diameters,
        key=lambda x: abs(x - diameter)
    )

    fn = table[str(int(nearest))]

    return vc, fn


def drilling_cycle(depth: float,
                   diameter: float):

    ratio = depth / diameter

    if ratio <= 3:
        return "G81", 0

    elif ratio <= 5:
        return "G73", 2

    else:
        step = max(2, round(diameter * 0.3))
        return "G83", step


def drilling_time(depth: float,
                  safe_z: float,
                  feed: float):

    length = depth + safe_z

    minutes = length / feed

    return round(minutes * 60, 1)


def coolant(material: str):

    if "Нержавейка" in material:
        return "Эмульсия высокого давления"

    return "Эмульсия"