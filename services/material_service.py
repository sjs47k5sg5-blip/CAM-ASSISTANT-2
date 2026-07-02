import json
from pathlib import Path

DATA_FILE = Path("data/materials.json")

with open(DATA_FILE, encoding="utf-8") as f:
    MATERIALS = json.load(f)


def get_modes(material: str, tool: str):
    return MATERIALS[material][tool]