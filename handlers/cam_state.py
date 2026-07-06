from dataclasses import dataclass

@dataclass
class CamState:

    # Общий экран
    screen: str = "main"

    # Размер детали
    size_x: float = 0
    size_y: float = 0
    size_z: float = 0

    # Материал
    material: str = ""

    # Ноль
    zero: str = "CENTER"
    zero_z: str = "TOP"

    # Углы
    corner_type: str = "SHARP"
    corner_select: str = "ALL"
    corner_value: float = 0

    # Припуск
    allowance: float = 0
    finish_pass: bool = False
    finish_tool: bool = False

    # Инструмент
    tool_diameter: float = 0

    # Проверка заполнения
    ready: bool = False


CAM_DB = {}