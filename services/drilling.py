import json
from pathlib import Path

DATA_FILE = Path("data/drilling.json")

with open(DATA_FILE, encoding="utf-8") as f:
    DATABASE = json.load(f)


def get_mode(material, tool, diameter):
    """
    Возвращает готовый режим из базы.
    """

    diameters = sorted(
        int(d)
        for d in DATABASE[material][tool].keys()
    )

    nearest = min(
        diameters,
        key=lambda x: abs(x - diameter)
    )

    return DATABASE[material][tool][str(nearest)]


def drilling_time(depth, feed):
    """
    Время сверления (сек)
    """

    if feed <= 0:
        return 0

    return round((depth / feed) * 60, 1)