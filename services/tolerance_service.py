import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "data" / "tolerances.json", encoding="utf-8") as f:
    TABLE = json.load(f)


def get_tolerance(field: str, diameter: float):

    if field not in TABLE:
        return None

    values = TABLE[field]

    for rng, tol in values.items():

        start, end = rng.split("-")

        if float(start) < diameter <= float(end):

            return {
                "min": diameter,
                "max": round(diameter + tol, 3),
                "tol": tol,
            }

    return None