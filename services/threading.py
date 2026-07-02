import json
from pathlib import Path

DATA_FILE = Path("data/threads.json")

with open(DATA_FILE, encoding="utf-8") as f:
    THREADS = json.load(f)


def get_thread(thread_name: str):
    """
    Возвращает параметры выбранной резьбы.
    """

    return THREADS[thread_name]


def spindle_speed(thread_name: str):
    """
    Рекомендуемые обороты для жесткого нарезания.
    """

    if thread_name in ("M3", "M4"):
        return 800

    if thread_name in ("M5", "M6"):
        return 600

    if thread_name in ("M8", "M10"):
        return 400

    if thread_name in ("M12", "M14", "M16"):
        return 300

    return 200


def feed_rate(rpm: int, pitch: float):
    """
    Подача при нарезании резьбы.
    F = S × шаг
    """

    return round(rpm * pitch)


def tapping_cycle(right_hand=True):
    """
    Выбор цикла Fanuc.
    """

    if right_hand:
        return "G84"

    return "G74"


def tapping_time(depth: float, feed: float):
    """
    Приблизительное время нарезания.
    """

    if feed <= 0:
        return 0

    return round((depth / feed) * 60, 1)