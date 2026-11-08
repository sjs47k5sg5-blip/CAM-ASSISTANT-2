from __future__ import annotations

import math
from typing import Any


Point = tuple[float, float]


def _cross(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])


def _distance(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _sample_segment(segment: dict[str, Any], count: int = 24) -> list[Point]:
    if segment["type"] == "line":
        return [tuple(segment["start"]), tuple(segment["end"])]
    sx, sy = segment["start"]
    ex, ey = segment["end"]
    cx, cy = segment["center"]
    start_angle = math.atan2(sy - cy, sx - cx)
    end_angle = math.atan2(ey - cy, ex - cx)
    direction = segment["direction"]
    if direction == "CW":
        while end_angle >= start_angle:
            end_angle -= 2 * math.pi
    else:
        while end_angle <= start_angle:
            end_angle += 2 * math.pi
    radius = _distance((sx, sy), (cx, cy))
    sweep = end_angle - start_angle
    steps = max(2, int(count * abs(sweep) / (2 * math.pi)) + 1)
    return [
        (cx + radius * math.cos(start_angle + sweep * i / steps),
         cy + radius * math.sin(start_angle + sweep * i / steps))
        for i in range(steps + 1)
    ]


def _orientation(a: Point, b: Point, c: Point, eps: float = 1e-8) -> int:
    value = _cross(a, b, c)
    return 1 if value > eps else (-1 if value < -eps else 0)


def _segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2 = _orientation(a, b, c), _orientation(a, b, d)
    o3, o4 = _orientation(c, d, a), _orientation(c, d, b)
    if o1 != o2 and o3 != o4:
        return True

    def on_segment(p: Point, q: Point, r: Point) -> bool:
        return (min(p[0], r[0]) - 1e-8 <= q[0] <= max(p[0], r[0]) + 1e-8
                and min(p[1], r[1]) - 1e-8 <= q[1] <= max(p[1], r[1]) + 1e-8)

    return ((o1 == 0 and on_segment(a, c, b))
            or (o2 == 0 and on_segment(a, d, b))
            or (o3 == 0 and on_segment(c, a, d))
            or (o4 == 0 and on_segment(c, b, d)))


def validate_geometry(geometry: dict[str, Any], tolerance: float = 0.02) -> list[str]:
    errors: list[str] = []
    segments = geometry.get("segments") or []
    if not segments:
        return ["Контур пустой."]
    for index, segment in enumerate(segments):
        if segment.get("type") not in {"line", "arc"}:
            errors.append(f"Сегмент {index + 1}: неизвестный тип.")
            continue
        try:
            start, end = tuple(segment["start"]), tuple(segment["end"])
            if not all(math.isfinite(float(v)) for v in (*start, *end)):
                errors.append(f"Сегмент {index + 1}: координаты нечисловые.")
            if _distance(start, end) <= 1e-8:
                errors.append(f"Сегмент {index + 1}: нулевая длина.")
            if segment["type"] == "arc":
                center = tuple(segment["center"])
                r0, r1 = _distance(start, center), _distance(end, center)
                if r0 <= 1e-8 or abs(r0 - r1) > max(tolerance, r0 * 0.001):
                    errors.append(f"Дуга {index + 1}: радиусы начала и конца не совпадают.")
                if segment.get("direction") not in {"CW", "CCW"}:
                    errors.append(f"Дуга {index + 1}: неверное направление.")
        except (KeyError, TypeError, ValueError):
            errors.append(f"Сегмент {index + 1}: неполные координаты.")
    for index, segment in enumerate(segments):
        next_segment = segments[(index + 1) % len(segments)]
        if _distance(tuple(segment["end"]), tuple(next_segment["start"])) > tolerance:
            errors.append(f"Разрыв между сегментами {index + 1} и {(index + 1) % len(segments) + 1}.")
    if geometry.get("closed"):
        sampled: list[Point] = []
        for segment in segments:
            points = _sample_segment(segment)
            sampled.extend(points[:-1])
        count = len(sampled)
        for i in range(count):
            a, b = sampled[i], sampled[(i + 1) % count]
            for j in range(i + 1, count):
                if j == i or j == (i + 1) % count or (j + 1) % count == i:
                    continue
                if i == 0 and j == count - 1:
                    continue
                c, d = sampled[j], sampled[(j + 1) % count]
                if _segments_intersect(a, b, c, d):
                    errors.append("Обнаружено самопересечение контура.")
                    return list(dict.fromkeys(errors))
    return list(dict.fromkeys(errors))


def build_rounded_polygon(vertices: list[tuple[float, float, float]]) -> dict[str, Any]:
    """Build a convex closed polygon; each vertex is X,Y,fillet-radius."""
    if len(vertices) < 3:
        raise ValueError("Нужно минимум три вершины.")
    points: list[Point] = []
    radii: list[float] = []
    for index, item in enumerate(vertices):
        if len(item) != 3:
            raise ValueError(f"Вершина {index + 1}: нужны X Y R.")
        x, y, radius = map(float, item)
        if not all(math.isfinite(v) for v in (x, y, radius)) or abs(x) > 100000 or abs(y) > 100000:
            raise ValueError(f"Вершина {index + 1}: недопустимые значения.")
        if radius < 0:
            raise ValueError(f"Вершина {index + 1}: радиус не может быть отрицательным.")
        points.append((x, y))
        radii.append(radius)
    if len(set(points)) != len(points):
        raise ValueError("Повторяющиеся вершины.")
    area2 = sum(points[i][0] * points[(i + 1) % len(points)][1]
                - points[(i + 1) % len(points)][0] * points[i][1]
                for i in range(len(points)))
    if abs(area2) <= 1e-8:
        raise ValueError("Площадь контура равна нулю.")
    orientation = 1 if area2 > 0 else -1
    tangencies: list[tuple[Point, Point, Point | None]] = []
    for i, vertex in enumerate(points):
        prev_point, next_point = points[i - 1], points[(i + 1) % len(points)]
        in_vec = (prev_point[0] - vertex[0], prev_point[1] - vertex[1])
        out_vec = (next_point[0] - vertex[0], next_point[1] - vertex[1])
        in_len, out_len = math.hypot(*in_vec), math.hypot(*out_vec)
        if min(in_len, out_len) <= 1e-8:
            raise ValueError(f"Вершина {i + 1}: нулевое ребро.")
        u = (in_vec[0] / in_len, in_vec[1] / in_len)
        v = (out_vec[0] / out_len, out_vec[1] / out_len)
        dot = max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1]))
        angle = math.acos(dot)
        turn = u[0] * v[1] - u[1] * v[0]
        if abs(turn) <= 1e-8 or angle <= 1e-6 or abs(math.pi - angle) <= 1e-6:
            raise ValueError(f"Вершина {i + 1}: коллинеарный или вырожденный угол.")
        if turn * orientation >= 0:
            raise ValueError("Поддерживаются только выпуклые многоугольники без вогнутых углов.")
        radius = radii[i]
        if radius == 0:
            tangencies.append((vertex, vertex, None))
            continue
        tangent_distance = radius / math.tan(angle / 2)
        if tangent_distance >= min(in_len, out_len) * 0.499:
            raise ValueError(f"Радиус R{radius:g} у вершины {i + 1} слишком велик для соседних рёбер.")
        before = (vertex[0] + u[0] * tangent_distance, vertex[1] + u[1] * tangent_distance)
        after = (vertex[0] + v[0] * tangent_distance, vertex[1] + v[1] * tangent_distance)
        bisector = (u[0] + v[0], u[1] + v[1])
        bisector_len = math.hypot(*bisector)
        center_distance = radius / math.sin(angle / 2)
        center = (vertex[0] + bisector[0] / bisector_len * center_distance,
                  vertex[1] + bisector[1] / bisector_len * center_distance)
        tangencies.append((before, after, center))

    for i in range(len(points)):
        current = tangencies[i]
        following = tangencies[(i + 1) % len(points)]
        edge_length = _distance(points[i], points[(i + 1) % len(points)])
        used = _distance(current[1], points[(i + 1) % len(points)]) + _distance(following[0], points[i])
        if used > edge_length + 1e-7:
            raise ValueError(f"Скругления на ребре {i + 1} пересекаются: уменьшите радиусы.")

    segments: list[dict[str, Any]] = []
    for i in range(len(points)):
        prev = tangencies[i - 1]
        current = tangencies[i]
        line_start, line_end = prev[1], current[0]
        if _distance(line_start, line_end) > 1e-8:
            segments.append({"type": "line", "start": line_start, "end": line_end})
        before, after, center = current
        if center is not None:
            segments.append({
                "type": "arc", "start": before, "end": after,
                "center": center, "direction": "CCW" if orientation > 0 else "CW",
            })
    geometry = {"units": "mm", "closed": True, "segments": segments, "source": "rounded_polygon"}
    errors = validate_geometry(geometry)
    if errors:
        raise ValueError("Геометрия не прошла проверку: " + "; ".join(errors))
    return geometry
