from __future__ import annotations

import math
from typing import Any

from shapely.geometry import Polygon
from shapely.validation import explain_validity

from services.cam_engine.geometry_validation import validate_geometry


Point = tuple[float, float]


def _arc_points(segment: dict[str, Any], tolerance: float) -> list[Point]:
    sx, sy = map(float, segment["start"])
    ex, ey = map(float, segment["end"])
    cx, cy = map(float, segment["center"])
    radius = math.hypot(sx - cx, sy - cy)
    if radius <= 0:
        raise ValueError("Дуга имеет нулевой радиус.")
    start = math.atan2(sy - cy, sx - cx)
    finish = math.atan2(ey - cy, ex - cx)
    direction = str(segment.get("direction", "")).upper()
    if direction == "CW":
        while finish >= start:
            finish -= 2 * math.pi
    elif direction == "CCW":
        while finish <= start:
            finish += 2 * math.pi
    else:
        raise ValueError("Для дуги нужно направление CW или CCW.")
    sweep = abs(finish - start)
    ratio = max(-1.0, min(1.0, 1.0 - tolerance / radius))
    max_angle = max(0.01, 2 * math.acos(ratio))
    count = max(2, min(10000, math.ceil(sweep / max_angle)))
    return [
        (cx + radius * math.cos(start + (finish - start) * i / count),
         cy + radius * math.sin(start + (finish - start) * i / count))
        for i in range(count + 1)
    ]


def flatten_geometry(geometry: dict[str, Any], tolerance: float = 0.02) -> list[Point]:
    if not geometry.get("closed"):
        raise ValueError("Для смещения нужен замкнутый контур.")
    if not math.isfinite(tolerance) or not 0.001 <= tolerance <= 0.1:
        raise ValueError("Допуск аппроксимации должен быть от 0.001 до 0.1 мм.")
    issues = validate_geometry(geometry, tolerance=max(tolerance, 0.02))
    if issues:
        raise ValueError("Контур не прошёл проверку: " + "; ".join(issues))
    points: list[Point] = []
    for segment in geometry.get("segments", []):
        if segment.get("type") == "line":
            part = [tuple(map(float, segment["start"])), tuple(map(float, segment["end"]))]
        elif segment.get("type") == "arc":
            part = _arc_points(segment, tolerance)
        else:
            raise ValueError("Поддерживаются только линии и дуги.")
        if points and math.dist(points[-1], part[0]) > max(tolerance, 0.02):
            raise ValueError("В контуре есть разрыв между сегментами.")
        points.extend(part[:-1])
    if len(points) < 3:
        raise ValueError("Недостаточно точек для замкнутого контура.")
    final_end = tuple(map(float, geometry["segments"][-1]["end"]))
    if math.dist(points[0], final_end) > max(tolerance, 0.02):
        raise ValueError("Последний сегмент не замыкает контур.")
    return points


def offset_geometry(geometry: dict[str, Any], distance: float, side: str,
                    tolerance: float = 0.02) -> dict[str, Any]:
    """Preview-only polygon offset; not a CNC toolpath/postprocessor."""
    try:
        distance = float(distance)
    except (TypeError, ValueError):
        raise ValueError("Смещение должно быть числом.") from None
    if not math.isfinite(distance) or distance <= 0 or distance > 100:
        raise ValueError("Смещение должно быть больше 0 и не более 100 мм.")
    side = side.upper()
    if side not in {"INSIDE", "OUTSIDE"}:
        raise ValueError("Сторона смещения: INSIDE или OUTSIDE.")
    points = flatten_geometry(geometry, tolerance)
    polygon = Polygon(points)
    if not polygon.is_valid:
        raise ValueError("Некорректный исходный контур: " + explain_validity(polygon))
    if polygon.area <= 1e-8:
        raise ValueError("Площадь контура слишком мала.")
    result = polygon.buffer(distance if side == "OUTSIDE" else -distance,
                            quad_segs=16, join_style="round")
    if result.is_empty:
        raise ValueError("При таком смещении контур схлопывается.")
    if result.geom_type != "Polygon":
        raise ValueError("Смещение разделило контур на несколько областей. Уменьшите смещение.")
    if not result.is_valid or result.area <= 1e-8:
        raise ValueError("Результат смещения геометрически некорректен.")
    coords = list(result.exterior.coords)
    segments = [
        {"type": "line", "start": tuple(coords[i]), "end": tuple(coords[i + 1])}
        for i in range(len(coords) - 1)
        if math.dist(coords[i], coords[i + 1]) > 1e-8
    ]
    return {
        "units": "mm", "closed": True, "segments": segments,
        "source": "cutter_offset_preview", "offset_mm": distance,
        "side": side, "approximation_tolerance_mm": tolerance,
        "warning": "Аппроксимация для предпросмотра. Не является готовой УП.",
    }
