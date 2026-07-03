import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "data" / "iso286" / "it.json", encoding="utf-8") as f:
    IT_TABLE = json.load(f)["ranges"]

with open(BASE_DIR / "data" / "iso286" / "deviation.json", encoding="utf-8") as f:
    DEVIATIONS = json.load(f)


def get_it_grade(diameter: float, grade: str):
    """
    Возвращает значение допуска IT для указанного диаметра.
    Например:
        grade = "IT7"
    """

    for row in IT_TABLE:
        if row["min"] < diameter <= row["max"]:
            return row[grade]

    return None


def calculate_hole_h(diameter: float, grade: str):
    """
    Расчет отверстия H.
    Например H7.
    """

    it = get_it_grade(diameter, grade)

    if it is None:
        return None

    return {
        "ei": 0.0,
        "es": round(it, 3),
        "min": round(diameter, 3),
        "max": round(diameter + it, 3),
        "tol": round(it, 3),
    }


def calculate_shaft_h(diameter: float, grade: str):
    """
    Расчет вала h.
    Например h6.
    """

    it = get_it_grade(diameter, grade)

    if it is None:
        return None

    return {
        "es": 0.0,
        "ei": round(-it, 3),
        "min": round(diameter - it, 3),
        "max": round(diameter, 3),
        "tol": round(it, 3),
    }