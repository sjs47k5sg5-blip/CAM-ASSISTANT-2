from __future__ import annotations

import math


MACHINE_X = 1350.0
MACHINE_Y = 700.0
MACHINE_Z = 610.0
MAX_SPINDLE = 15000
MAX_FEED = 15000.0


def depth_levels(thickness: float, step: float, zero_z: str) -> list[float]:
    if thickness <= 0 or step <= 0:
        raise ValueError("Толщина и шаг по Z должны быть больше нуля.")
    if zero_z not in {"TOP", "BOTTOM"}:
        raise ValueError("Неизвестное положение нуля Z.")
    count = math.ceil(thickness / step)
    levels = [min(i * step, thickness) for i in range(1, count + 1)]
    if zero_z == "TOP":
        return [-round(value, 4) for value in levels]
    return [round(thickness - value, 4) for value in levels]


def rectangle_origin(x: float, y: float, zero: str) -> tuple[float, float]:
    origins = {
        "CENTER": (-x / 2, -y / 2),
        "BL": (0.0, 0.0),
        "BR": (-x, 0.0),
        "TL": (0.0, -y),
        "TR": (-x, -y),
    }
    if zero not in origins:
        raise ValueError("Неизвестное положение нуля XY.")
    return origins[zero]


def rectangle_contour(
    x: float,
    y: float,
    tool_diameter: float,
    corner_radius: float,
    allowance: float,
    zero: str,
    z: float,
    feed: float,
) -> list[str]:
    if min(x, y, tool_diameter, feed) <= 0:
        raise ValueError("Размеры детали, диаметр инструмента и подача должны быть положительными.")
    if corner_radius < 0 or allowance < 0:
        raise ValueError("Радиус и припуск не могут быть отрицательными.")

    tool_radius = tool_diameter / 2
    if tool_diameter >= min(x, y):
        raise ValueError("Диаметр фрезы слишком велик относительно детали.")
    if corner_radius >= min(x, y) / 2:
        raise ValueError("Радиус угла должен быть меньше половины меньшего размера.")

    part_x0, part_y0 = rectangle_origin(x, y, zero)
    offset = tool_radius + allowance
    x0, y0 = part_x0 - offset, part_y0 - offset
    x1, y1 = x0 + x + 2 * offset, y0 + y + 2 * offset
    radius = offset + corner_radius
    if radius >= min(x1 - x0, y1 - y0) / 2:
        raise ValueError("Радиус траектории не помещается в габарит детали.")

    p = [
        (x0 + radius, y0),
        (x1 - radius, y0),
        (x1, y0 + radius),
        (x1, y1 - radius),
        (x1 - radius, y1),
        (x0 + radius, y1),
        (x0, y1 - radius),
        (x0, y0 + radius),
        (x0 + radius, y0),
    ]
    centers = [
        (x1 - radius, y0 + radius),
        (x1 - radius, y1 - radius),
        (x0 + radius, y1 - radius),
        (x0 + radius, y0 + radius),
    ]

    # Tangential lead-in starts outside the stock envelope before plunging.
    lead_x, lead_y = p[0][0] - 5.0, y0 - 5.0
    commands = [
        f"G00 X{lead_x:.3f} Y{lead_y:.3f}",
        f"G01 Z{z:.3f} F{feed:.1f}",
        f"G01 X{p[0][0]:.3f} Y{p[0][1]:.3f} F{feed:.1f}",
    ]

    for i in range(4):
        start = p[2 * i + 1]
        end = p[2 * i + 2]
        commands.append(f"G01 X{start[0]:.3f} Y{start[1]:.3f} F{feed:.1f}")
        cx, cy = centers[i]
        commands.append(
            f"G03 X{end[0]:.3f} Y{end[1]:.3f} "
            f"I{cx - start[0]:.3f} J{cy - start[1]:.3f} F{feed:.1f}"
        )
        if i < 3:
            next_start = p[2 * i + 3]
            commands.append(
                f"G01 X{next_start[0]:.3f} Y{next_start[1]:.3f} F{feed:.1f}"
            )
    return commands


def build_contour_program(data: dict) -> str:
    required = ("x", "y", "z", "tool", "tool_d", "zero", "zero_z", "rpm", "feed", "step_z")
    missing = [key for key in required if data.get(key) is None]
    if missing:
        raise ValueError("Не заполнены параметры: " + ", ".join(missing))

    x, y, thickness = float(data["x"]), float(data["y"]), float(data["z"])
    tool, diameter = int(data["tool"]), float(data["tool_d"])
    rpm, feed = int(data["rpm"]), float(data["feed"])
    step = float(data["step_z"])
    allowance = float(data.get("allowance", 0.0))
    corner_radius = float(data.get("corner_r", 0.0)) if data.get("corner") == "RADIUS" else 0.0

    if x > MACHINE_X or y > MACHINE_Y or thickness > 500:
        raise ValueError("Габариты превышают допустимый диапазон, заданный для этого проекта.")
    if not 1 <= tool <= 30:
        raise ValueError("Номер инструмента должен быть от 1 до 30.")
    if not 100 <= rpm <= MAX_SPINDLE:
        raise ValueError("Обороты должны быть в диапазоне 100–15000 об/мин.")
    if not 1 <= feed <= MAX_FEED:
        raise ValueError("Подача должна быть в диапазоне 1–15000 мм/мин.")
    if not 0 < step <= 10:
        raise ValueError("Шаг по Z должен быть больше 0 и не более 10 мм.")
    if not 0 <= allowance <= 5:
        raise ValueError("Припуск должен быть от 0 до 5 мм.")

    levels = depth_levels(thickness, step, data["zero_z"])
    safe_z = 100.0 if data["zero_z"] == "TOP" else thickness + 100.0
    approach_z = 5.0 if data["zero_z"] == "TOP" else thickness + 5.0
    if safe_z > MACHINE_Z or approach_z > MACHINE_Z:
        raise ValueError("Безопасная высота выходит за пределы хода Z.")

    lines = [
        "%",
        "O1001 (RECTANGLE PROFILE - VERIFY BEFORE USE)",
        "G21 G17 G90 G40 G49 G80",
        "G54",
        f"T{tool} M6",
        f"S{rpm} M3",
        f"G43 H{tool} Z{safe_z:.3f}",
        "M8",
    ]

    for z in levels:
        lines.append(f"G00 Z{approach_z:.3f}")
        # Rough wall pass leaves the selected radial allowance.
        if allowance > 0:
            lines.extend(rectangle_contour(
                x, y, diameter, corner_radius, allowance,
                data["zero"], z, feed,
            ))
            lines.append(f"G00 Z{approach_z:.3f}")
        # Finish pass follows the nominal cutter-radius offset.
        lines.extend(rectangle_contour(
            x, y, diameter, corner_radius, 0.0,
            data["zero"], z, feed,
        ))

    lines.extend([
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
