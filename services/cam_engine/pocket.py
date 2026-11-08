from __future__ import annotations

import math

MACHINE_X = 1350.0
MACHINE_Y = 700.0
MACHINE_Z = 610.0
MAX_RPM = 15000
MAX_FEED = 15000.0


def _number(name: str, raw: object, minimum: float = 0.0) -> float:
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{name}: некорректное число.") from None
    if not math.isfinite(value) or value <= minimum:
        raise ValueError(f"{name}: значение должно быть больше {minimum:g}.")
    return value


def pocket_origin(width: float, height: float, choice: str) -> tuple[float, float]:
    mapping = {
        "CENTER": (-width / 2, -height / 2),
        "BL": (0.0, 0.0),
        "BR": (-width, 0.0),
        "TL": (0.0, -height),
        "TR": (-width, -height),
    }
    if choice not in mapping:
        raise ValueError("Неизвестное положение нуля XY.")
    return mapping[choice]


def depth_levels(depth: float, step: float, zero_z: str) -> list[float]:
    depth = _number("Глубина", depth)
    step = _number("Шаг по Z", step)
    count = math.ceil(depth / step)
    values = [min(i * step, depth) for i in range(1, count + 1)]
    if zero_z == "TOP":
        return [-round(v, 4) for v in values]
    if zero_z == "BOTTOM":
        return [round(depth - v, 4) for v in values]
    raise ValueError("Ноль Z должен быть TOP или BOTTOM.")


def raster_path(x0: float, y0: float, x1: float, y1: float, stepover: float) -> list[tuple[float, float]]:
    if x1 <= x0 or y1 <= y0 or stepover <= 0:
        raise ValueError("Некорректные границы или боковой шаг траектории.")
    rows = max(1, math.ceil((y1 - y0) / stepover))
    ys = [y0 + (y1 - y0) * i / rows for i in range(rows + 1)]
    points: list[tuple[float, float]] = []
    for row, y in enumerate(ys):
        points.extend(((x0, y), (x1, y)) if row % 2 == 0 else ((x1, y), (x0, y)))
    return points


def build_pocket_program(data: dict) -> str:
    required = ("x", "y", "depth", "tool", "tool_d", "zero", "zero_z",
                "rpm", "feed", "step_z", "stepover")
    missing = [key for key in required if data.get(key) is None]
    if missing:
        raise ValueError("Не заполнены параметры: " + ", ".join(missing))

    x = _number("X", data["x"])
    y = _number("Y", data["y"])
    depth = _number("Глубина", data["depth"])
    diameter = _number("Диаметр фрезы", data["tool_d"])
    step_z = _number("Шаг по Z", data["step_z"])
    stepover_pct = _number("Боковой шаг", data["stepover"])
    feed = _number("Подача", data["feed"])
    try:
        rpm = int(data["rpm"])
        tool = int(data["tool"])
        allowance = float(data.get("allowance", 0.0))
    except (TypeError, ValueError):
        raise ValueError("Проверьте номер инструмента, обороты и припуск.") from None

    if not all(math.isfinite(v) for v in (x, y, depth, diameter, step_z, stepover_pct, feed, allowance)):
        raise ValueError("Параметры должны быть конечными числами.")
    if x > MACHINE_X or y > MACHINE_Y or depth > 500:
        raise ValueError("Габариты превышают допустимый диапазон проекта.")
    if not 1 <= tool <= 30:
        raise ValueError("Номер инструмента должен быть от 1 до 30.")
    if not 100 <= rpm <= MAX_RPM:
        raise ValueError("Обороты должны быть в диапазоне 100–15000 об/мин.")
    if feed > MAX_FEED:
        raise ValueError("Подача не должна превышать 15000 мм/мин.")
    if step_z > 10:
        raise ValueError("Шаг по Z не должен превышать 10 мм.")
    if not 5 <= stepover_pct <= 80:
        raise ValueError("Боковой шаг должен быть от 5 до 80 процентов диаметра.")
    if not 0 <= allowance <= 5:
        raise ValueError("Припуск на стенку должен быть от 0 до 5 мм.")
    if diameter >= min(x, y):
        raise ValueError("Фреза слишком большая для кармана.")
    if data["zero_z"] not in {"TOP", "BOTTOM"}:
        raise ValueError("Неизвестное положение нуля Z.")

    part_x, part_y = pocket_origin(x, y, data["zero"])
    radius = diameter / 2
    # Roughing centerline stays one radial allowance away from the finished wall.
    rough_x0 = part_x + radius + allowance
    rough_y0 = part_y + radius + allowance
    rough_x1 = part_x + x - radius - allowance
    rough_y1 = part_y + y - radius - allowance
    finish_x0 = part_x + radius
    finish_y0 = part_y + radius
    finish_x1 = part_x + x - radius
    finish_y1 = part_y + y - radius

    if rough_x1 - rough_x0 < diameter * 0.5 or rough_y1 - rough_y0 < diameter * 0.5:
        raise ValueError("Недостаточно места для выбранной фрезы и припуска.")

    levels = depth_levels(depth, step_z, data["zero_z"])
    safe_z = 100.0 if data["zero_z"] == "TOP" else depth + 100.0
    approach_z = 5.0 if data["zero_z"] == "TOP" else depth + 5.0
    if safe_z > MACHINE_Z:
        raise ValueError("Безопасная высота выходит за пределы хода Z.")

    stepover = diameter * stepover_pct / 100.0
    rough_points = raster_path(rough_x0, rough_y0, rough_x1, rough_y1, stepover)
    finish_points = raster_path(finish_x0, finish_y0, finish_x1, finish_y1, diameter * 0.25)

    # Use a shallow linear ramp at each depth level. The required ramp length
    # is calculated for a maximum 5-degree ramp angle; reject undersized pockets.
    first_level_drop = abs(levels[0])
    ramp_required = first_level_drop / math.tan(math.radians(5.0))
    available_diagonal = math.hypot(rough_x1 - rough_x0, rough_y1 - rough_y0)
    ramp_length = min(available_diagonal * 0.7, max(rough_x1 - rough_x0, rough_y1 - rough_y0))
    if ramp_length < ramp_required:
        raise ValueError(
            "Карман мал для пологого линейного врезания при таком шаге Z. "
            "Уменьшите шаг по Z или используйте меньшую фрезу."
        )

    lines = [
        "%",
        "O1003 (RECTANGULAR POCKET - VERIFY BEFORE USE)",
        "G21 G17 G90 G40 G49 G80",
        "G54",
        f"T{tool} M6",
        f"S{rpm} M3",
        f"G43 H{tool} Z{safe_z:.3f}",
        "M8",
    ]

    start_x, start_y = rough_points[0]
    ramp_x, ramp_y = start_x + ramp_length, start_y
    if ramp_x > rough_x1:
        ramp_x = start_x - ramp_length
    if ramp_x < rough_x0 or ramp_x > rough_x1:
        raise ValueError("Не удалось построить безопасный линейный вход в карман.")

    previous_level = 0.0
    for index, z in enumerate(levels, 1):
        level_drop = abs(z - previous_level)
        if level_drop / math.tan(math.radians(5.0)) > ramp_length:
            raise ValueError(
                f"Шаг по Z на проходе {index} слишком велик для безопасного рампового входа. "
                "Уменьшите шаг по Z."
            )
        lines.extend([
            f"(ROUGH POCKET PASS {index})",
            f"G00 Z{approach_z:.3f}",
            f"G00 X{start_x:.3f} Y{start_y:.3f}",
            f"G01 Z{0.000 if data['zero_z'] == 'TOP' else depth:.3f} F{feed:.1f}",
            f"G01 X{ramp_x:.3f} Z{z:.3f} F{feed:.1f}",
        ])
        for px, py in rough_points[1:]:
            lines.append(f"G01 X{px:.3f} Y{py:.3f} F{feed:.1f}")
        lines.append(f"G00 Z{approach_z:.3f}")
        previous_level = z

    # Finish floor with a denser raster and finish all four walls at final depth.
    final_z = levels[-1]
    lines.extend([
        "(FINISH FLOOR)",
        f"G00 X{finish_points[0][0]:.3f} Y{finish_points[0][1]:.3f}",
        f"G01 Z{final_z:.3f} F{feed:.1f}",
    ])
    for px, py in finish_points[1:]:
        lines.append(f"G01 X{px:.3f} Y{py:.3f} F{feed:.1f}")

    lines.extend([
        "(FINISH WALL)",
        f"G01 X{finish_x1:.3f} Y{finish_y0:.3f} F{feed:.1f}",
        f"G01 X{finish_x1:.3f} Y{finish_y1:.3f} F{feed:.1f}",
        f"G01 X{finish_x0:.3f} Y{finish_y1:.3f} F{feed:.1f}",
        f"G01 X{finish_x0:.3f} Y{finish_y0:.3f} F{feed:.1f}",
        f"G00 Z{safe_z:.3f}",
        "M9",
        "M5",
        "G49",
        "G91 G28 Z0.",
        "G90",
        "M30",
        "%",
    ])
    return "\n".join(lines) + "\n"
