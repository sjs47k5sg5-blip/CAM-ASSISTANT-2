import json
from pathlib import Path

DATA_FILE = Path("data/machine.json")

with open(DATA_FILE, encoding="utf-8") as f:
    MACHINE = json.load(f)["machine"]


def max_rpm():
    return MACHINE["spindle"]["max_rpm"]


def spindle_power():
    return MACHINE["spindle"]["power_kw"]


def spindle_torque():
    return MACHINE["spindle"]["torque_nm"]


def max_feed():
    return MACHINE["feed"]["max"]


def machine_name():
    return MACHINE["name"]


def control():
    return MACHINE["control"]


def tool_holder():
    return MACHINE["tool_system"]["holder"]


def tool_magazine():
    return MACHINE["tool_system"]["magazine"]