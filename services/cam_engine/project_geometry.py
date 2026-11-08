from __future__ import annotations

import io
import math
from typing import Any


def _finite(value: float, label: str) -> float:
    number = float(value)
    if not math.isfinite(number) or abs(number) > 100000:
        raise ValueError(f"{label}: недопустимое значение.")
    return number


def parse_manual_path(source: str) -> dict[str, Any]:
    """M X Y starts; L X Y line; A X Y I J CW|CCW arc; Z closes."""
    current = start = None
    segments: list[dict[str, Any]] = []
    for line_number, raw in enumerate(source.splitlines(), 1):
        parts = raw.replace(",", ".").split()
        if not parts or parts[0].startswith("#"):
            continue
        command = parts[0].upper()
        try:
            if command == "M" and len(parts) == 3 and current is None:
                current = start = (_finite(parts[1], "X"), _finite(parts[2], "Y"))
            elif command == "L" and len(parts) == 3 and current is not None:
                point = (_finite(parts[1], "X"), _finite(parts[2], "Y"))
                if point == current:
                    raise ValueError("Нулевой отрезок.")
                segments.append({"type": "line", "start": current, "end": point})
                current = point
            elif command == "A" and len(parts) == 6 and current is not None:
                x, y, i, j = map(float, parts[1:5])
                x, y, i, j = (_finite(x, "X"), _finite(y, "Y"), _finite(i, "I"), _finite(j, "J"))
                direction = parts[5].upper()
                if direction not in {"CW", "CCW"}:
                    raise ValueError("Направление дуги: CW или CCW.")
                center = (current[0] + i, current[1] + j)
                r0 = math.hypot(current[0] - center[0], current[1] - center[1])
                r1 = math.hypot(x - center[0], y - center[1])
                if r0 <= 0 or abs(r0 - r1) > max(0.02, r0 * 0.001):
                    raise ValueError("Начальный и конечный радиусы дуги не совпадают.")
                segments.append({"type": "arc", "start": current, "end": (x, y), "center": center, "direction": direction})
                current = (x, y)
            elif command == "Z" and len(parts) == 1 and current is not None and start is not None:
                if math.dist(current, start) > 1e-6:
                    segments.append({"type": "line", "start": current, "end": start})
                current = start
            else:
                raise ValueError("Формат: M X Y, L X Y, A X Y I J CW|CCW или Z.")
        except (ValueError, IndexError) as exc:
            raise ValueError(f"Строка {line_number}: {exc}") from None
    if not segments:
        raise ValueError("Контур пустой.")
    return {"units": "mm", "closed": current == start, "segments": segments, "source": "manual"}


def parse_dxf(data: bytes) -> dict[str, Any]:
    try:
        import ezdxf
    except ImportError:
        raise ValueError("DXF-модуль не установлен: добавьте ezdxf в requirements.txt.") from None
    try:
        document = ezdxf.read(io.StringIO(data.decode("utf-8-sig")))
        segments: list[dict[str, Any]] = []
        for entity in document.modelspace():
            kind = entity.dxftype()
            if kind == "LINE":
                a, b = entity.dxf.start, entity.dxf.end
                segments.append({"type": "line", "start": (float(a.x), float(a.y)), "end": (float(b.x), float(b.y))})
            elif kind == "ARC":
                c = entity.dxf.center
                radius = float(entity.dxf.radius)
                sa, ea = math.radians(float(entity.dxf.start_angle)), math.radians(float(entity.dxf.end_angle))
                segments.append({
                    "type": "arc",
                    "start": (c.x + radius * math.cos(sa), c.y + radius * math.sin(sa)),
                    "end": (c.x + radius * math.cos(ea), c.y + radius * math.sin(ea)),
                    "center": (float(c.x), float(c.y)), "direction": "CCW",
                })
            elif kind in {"LWPOLYLINE", "POLYLINE"}:
                for virtual in entity.virtual_entities():
                    vk = virtual.dxftype()
                    if vk == "LINE":
                        a, b = virtual.dxf.start, virtual.dxf.end
                        segments.append({"type": "line", "start": (float(a.x), float(a.y)), "end": (float(b.x), float(b.y))})
                    elif vk == "ARC":
                        c = virtual.dxf.center
                        radius = float(virtual.dxf.radius)
                        sa, ea = math.radians(float(virtual.dxf.start_angle)), math.radians(float(virtual.dxf.end_angle))
                        segments.append({
                            "type": "arc",
                            "start": (c.x + radius * math.cos(sa), c.y + radius * math.sin(sa)),
                            "end": (c.x + radius * math.cos(ea), c.y + radius * math.sin(ea)),
                            "center": (float(c.x), float(c.y)), "direction": "CCW",
                        })
        if not segments:
            raise ValueError("В DXF не найдены LINE, ARC или полилинии.")
        return {"units": "dxf-units", "closed": False, "segments": segments, "source": "DXF"}
    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Не удалось прочитать DXF: {exc}") from None
