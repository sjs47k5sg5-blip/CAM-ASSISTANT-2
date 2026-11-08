from __future__ import annotations

import math
from io import BytesIO
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def _arc_points(segment: dict[str, Any], steps: int = 48) -> list[tuple[float, float]]:
    sx, sy = segment["start"]
    ex, ey = segment["end"]
    cx, cy = segment["center"]
    a0 = math.atan2(sy - cy, sx - cx)
    a1 = math.atan2(ey - cy, ex - cx)
    direction = segment.get("direction", "CCW").upper()
    if direction == "CW":
        while a1 >= a0:
            a1 -= 2 * math.pi
    else:
        while a1 <= a0:
            a1 += 2 * math.pi
    radius = math.hypot(sx - cx, sy - cy)
    sweep = a1 - a0
    count = max(8, min(240, int(abs(sweep) / (2 * math.pi) * steps * 4) + 2))
    return [
        (cx + radius * math.cos(a0 + sweep * index / (count - 1)),
         cy + radius * math.sin(a0 + sweep * index / (count - 1)))
        for index in range(count)
    ]


def _segment_points(segment: dict[str, Any]) -> list[tuple[float, float]]:
    if segment.get("type") == "arc":
        return _arc_points(segment)
    return [tuple(segment["start"]), tuple(segment["end"])]


def render_geometry_preview(geometry: dict[str, Any], width: int = 1100, height: int = 760) -> bytes:
    segments = geometry.get("segments") or []
    if not segments:
        raise ValueError("Нет геометрии для предпросмотра.")
    points = [point for segment in segments for point in _segment_points(segment)]
    if not points:
        raise ValueError("Контур пустой.")
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x, span_y = max(max_x - min_x, 1.0), max(max_y - min_y, 1.0)
    margin = 90
    scale = min((width - margin * 2) / span_x, (height - margin * 2) / span_y)

    def transform(point: tuple[float, float]) -> tuple[int, int]:
        x, y = point
        px = int(margin + (x - min_x) * scale)
        py = int(height - margin - (y - min_y) * scale)
        return px, py

    image = Image.new("RGB", (width, height), "#151a22")
    draw = ImageDraw.Draw(image)
    left, top = margin, margin
    right, bottom = width - margin, height - margin
    for x in range(left, right, 40):
        draw.line((x, top, x, bottom), fill="#252d39", width=1)
    for y in range(top, bottom, 40):
        draw.line((left, y, right, y), fill="#252d39", width=1)
    draw.rectangle((left, top, right, bottom), outline="#4b5667", width=2)

    for segment in segments:
        polyline = [transform(p) for p in _segment_points(segment)]
        if len(polyline) >= 2:
            draw.line(polyline, fill="#45c4a0", width=5, joint="curve")
        start = transform(tuple(segment["start"]))
        draw.ellipse((start[0] - 5, start[1] - 5, start[0] + 5, start[1] + 5), fill="#ffd166")
    end = transform(tuple(segments[-1]["end"]))
    draw.ellipse((end[0] - 7, end[1] - 7, end[0] + 7, end[1] + 7), fill="#ff7b72")
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    title = f"CAM geometry preview | {len(segments)} segments | units: {geometry.get('units', 'unknown')}"
    draw.text((margin, 24), title, fill="#f0f3f7", font=font)
    draw.text((margin, height - 48), f"X: {min_x:.3f} .. {max_x:.3f} mm    Y: {min_y:.3f} .. {max_y:.3f} mm",
              fill="#c2cad5", font=font)
    draw.text((width - 245, 24), "Start: yellow  End: red", fill="#c2cad5", font=font)
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()
