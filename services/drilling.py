import json
import math
from pathlib import Path

DATA_FILE = Path("data/drilling.json")

with open(DATA_FILE, encoding="utf-8") as f:
    DATABASE = json.load(f)


def get_cutting_data(material, tool, diameter):
    material_data = DATABASE[material][tool]

    vc = material_data["vc"]
    fn_table = material_data["fn"]

    # Диаметры, которые есть в базе
    available = sorted(int(d) for d in fn_table.keys())

    # Ищем ближайший
    nearest = min(available, key=lambda x: abs(x - diameter))

    fn = fn_table[str(nearest)]

    return vc, fn


def spindle_speed(vc, diameter):
    rpm = (1000 * vc) / (math.pi * diameter)

    # Ограничение Victor Center 136
    rpm = min(rpm, 15000)

    return round(rpm)


def feed_rate(rpm, fn):
    return round(rpm * fn)


def drilling_cycle(depth, diameter):
    ratio = depth / diameter

    if ratio <= 3:
        return "G81", 0

    if ratio <= 5:
        return "G73", round(diameter * 0.5, 1)

    return "G83", round(diameter, 1)


def drilling_time(depth, retract, feed):
    if feed <= 0:
        return 0

    distance = depth + retract

    return round((distance / feed) * 60, 1)


def coolant(material):
    if material in ["D16", "АМг6"]:
        return "Воздух / Эмульсия"

    return "Эмульсия"