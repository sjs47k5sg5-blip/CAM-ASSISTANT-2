from __future__ import annotations

import math
from typing import Any

from shapely.geometry import Polygon
from shapely.validation import explain_validity

from services.cam_engine.geometry_offset import flatten_geometry


def _rings(polygon: Polygon) -> list[dict[str, Any]]:
    rings: list[dict[str, Any]] = []
    for role, ring in [("outer", polygon.exterior), *[("hole", item) for item in polygon.interiors]]:
        points = [(float(x), float(y)) for x, y in ring.coords]
        if len(points) < 4:
            continue
        if math.dist(points[0], points[-1]) > 1e-7:
            raise ValueError("CAM: смещённый контур не замкнут.")
        points.pop()
        if len(points) < 3:
            raise ValueError("CAM: в контуре меньше трёх точек.")
        rings.append({"role": role, "points": points})
    return rings


def build_profile_toolpath(
    geometry: dict[str, Any],
    tool_diameter: float,
    total_depth: float,
    stepdown: float,
    side: str,
    allowance: float = 0.0,
    tolerance: float = 0.02,
    max_levels: int = 100,
    max_points: int = 50000,
) -> dict[str, Any]:
    """Build a 2D cutter-centre profile path at successive Z levels.

    This is geometry output only: it intentionally does not emit executable NC.
    """
    values = [tool_diameter, total_depth, stepdown, allowance, tolerance]
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("Все параметры должны быть конечными числами.")
    tool_diameter, total_depth, stepdown, allowance, tolerance = map(float, values)
    if not 0.1 <= tool_diameter <= 100:
        raise ValueError("Диаметр фрезы должен быть от 0.1 до 100 мм.")
    if not 0 < total_depth <= 500:
        raise ValueError("Глубина должна быть больше 0 и не более 500 мм.")
    if not 0 < stepdown <= 10:
        raise ValueError("Шаг по Z должен быть больше 0 и не более 10 мм.")
    if not 0 <= allowance <= 5:
        raise ValueError("Припуск должен быть от 0 до 5 мм.")
    side = side.upper()
    if side not in {"INSIDE", "OUTSIDE"}:
        raise ValueError("Сторона обработки: INSIDE или OUTSIDE.")

    points = flatten_geometry(geometry, tolerance)
    polygon = Polygon(points)
    if not polygon.is_valid:
        raise ValueError("Исходный контур некорректен: " + explain_validity(polygon))
    if polygon.area <= 1e-6:
        raise ValueError("Площадь контура слишком мала.")

    # Cutter centre follows the outside or inside offset of the nominal boundary.
    offset = tool_diameter / 2 + allowance
    distance = offset if side == "OUTSIDE" else -offset
    buffered = polygon.buffer(distance, quad_segs=24, join_style="round")
    if buffered.is_empty:
        raise ValueError("Смещение схлопнуло контур. Уменьшите диаметр или припуск.")
    polygons = list(buffered.geoms) if buffered.geom_type == "MultiPolygon" else [buffered]
    if any(item.geom_type != "Polygon" or not item.is_valid or item.area <= 1e-7 for item in polygons):
        raise ValueError("Результат смещения содержит неподдерживаемую геометрию.")
    if len(polygons) > 100:
        raise ValueError("После смещения получилось больше 100 отдельных областей.")

    rings: list[dict[str, Any]] = []
    for polygon_index, item in enumerate(polygons, 1):
        for ring in _rings(item):
            rings.append({"polygon": polygon_index, **ring})
    point_count = sum(len(ring["points"]) for ring in rings)
    if not rings or point_count > max_points:
        raise ValueError("Слишком сложная геометрия для предпросмотра траектории.")

    level_count = math.ceil(total_depth / stepdown)
    if level_count > max_levels:
        raise ValueError(f"Слишком много уровней Z ({level_count}). Увеличьте шаг по Z.")
    levels = [-round(min((i + 1) * stepdown, total_depth), 4) for i in range(level_count)]

    toolpaths = []
    for z in levels:
        for ring_index, ring in enumerate(rings, 1):
            toolpaths.append({
                "z": z,
                "polygon": ring["polygon"],
                "ring": ring_index,
                "role": ring["role"],
                "points": ring["points"],
                "closed": True,
            })

    length = 0.0
    for path in toolpaths:
        pts = path["points"]
        length += sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
    return {
        "format": "cam-assistant-profile-path-v1",
        "units": "mm",
        "side": side,
        "tool_diameter": tool_diameter,
        "radial_allowance": allowance,
        "offset_distance": offset,
        "total_depth": total_depth,
        "stepdown": stepdown,
        "z_levels": levels,
        "tolerance": tolerance,
        "paths": toolpaths,
        "path_count": len(toolpaths),
        "point_count": point_count * len(levels),
        "estimated_cut_length_mm": round(length, 3),
        "status": "GEOMETRY_ONLY_NOT_NC",
        "warnings": [
            "Это геометрия центра фрезы, а не готовая управляющая программа.",
            "Не рассчитаны безопасное врезание, отводы, держатель, коллизии и крепёж.",
            "Перед постпроцессором требуется симуляция и проверка станочной кинематики.",
        ],
    }


def render_toolpath_preview(toolpath: dict[str, Any], width: int = 1100, height: int = 760) -> bytes:
    from io import BytesIO
    from PIL import Image, ImageDraw

    all_points = [point for path in toolpath["paths"] for point in path["points"]]
    if not all_points:
        raise ValueError("Траектория пуста.")
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x, span_y = max(max_x - min_x, 1.0), max(max_y - min_y, 1.0)
    margin = 80
    scale = min((width - margin * 2) / span_x, (height - margin * 2) / span_y)

    def transform(point):
        return (int(margin + (point[0] - min_x) * scale),
                int(height - margin - (point[1] - min_y) * scale))

    image = Image.new("RGB", (width, height), "#151a22")
    draw = ImageDraw.Draw(image)
    for path in toolpath["paths"]:
        pts = [transform(p) for p in path["points"]]
        if len(pts) >= 3:
            draw.line(pts + [pts[0]], fill="#45c4a0" if path["role"] == "outer" else "#f4a261", width=3)
    draw.text((margin, 24), "CAM profile toolpath preview — geometry only", fill="#f0f3f7")
    draw.text((margin, height - 42),
              f"{toolpath['side']} | D={toolpath['tool_diameter']:g} mm | "
              f"Z levels={len(toolpath['z_levels'])} | paths={toolpath['path_count']}",
              fill="#c2cad5")
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()
