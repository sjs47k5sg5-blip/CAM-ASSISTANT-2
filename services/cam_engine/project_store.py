from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("PROJECT_DB_PATH", "data/projects.sqlite3"))


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock_json TEXT NOT NULL,
            geometry_json TEXT,
            operations_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return db


def create_project(name: str, stock: dict[str, float], owner_id: int) -> int:
    clean_name = name.strip()
    if not clean_name or len(clean_name) > 64:
        raise ValueError("Название проекта должно содержать от 1 до 64 символов.")
    dimensions = {key: float(stock[key]) for key in ("x", "y", "z")}
    if any(value <= 0 for value in dimensions.values()):
        raise ValueError("Размеры заготовки должны быть больше нуля.")
    with _connect() as db:
        cursor = db.execute(
            "INSERT INTO projects(name, stock_json, operations_json) VALUES (?, ?, ?)",
            (clean_name, json.dumps({**dimensions, "owner_id": int(owner_id)}), "[]"),
        )
        return int(cursor.lastrowid)


def get_project(project_id: int, owner_id: int) -> dict[str, Any] | None:
    with _connect() as db:
        row = db.execute("SELECT * FROM projects WHERE id = ?", (int(project_id),)).fetchone()
    if row is None:
        return None
    stock = json.loads(row["stock_json"])
    if int(stock.get("owner_id", -1)) != int(owner_id):
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "stock": stock,
        "geometry": json.loads(row["geometry_json"]) if row["geometry_json"] else None,
        "operations": json.loads(row["operations_json"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_projects(owner_id: int) -> list[dict[str, Any]]:
    with _connect() as db:
        rows = db.execute("SELECT id FROM projects ORDER BY updated_at DESC").fetchall()
    result = []
    for row in rows:
        project = get_project(row["id"], owner_id)
        if project is not None:
            result.append(project)
    return result


def set_geometry(project_id: int, owner_id: int, geometry: dict[str, Any]) -> None:
    project = get_project(project_id, owner_id)
    if project is None:
        raise ValueError("Проект не найден.")
    with _connect() as db:
        db.execute(
            "UPDATE projects SET geometry_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (json.dumps(geometry, ensure_ascii=False), int(project_id)),
        )


def add_operation(project_id: int, owner_id: int, operation: dict[str, Any]) -> int:
    project = get_project(project_id, owner_id)
    if project is None:
        raise ValueError("Проект не найден.")
    operations = project["operations"]
    if len(operations) >= 30:
        raise ValueError("В проекте можно хранить не более 30 операций.")
    operation_id = max((int(item.get("id", 0)) for item in operations), default=0) + 1
    operations.append({"id": operation_id, **operation})
    with _connect() as db:
        db.execute(
            "UPDATE projects SET operations_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (json.dumps(operations, ensure_ascii=False), int(project_id)),
        )
    return operation_id
