"""Stockage des projets dans SQLite (bibliothèque standard).

Chaque projet est un document JSON validé par Pydantic à la lecture et à l'écriture.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from app.schemas import Project

DEFAULT_DB = Path(os.environ.get("SCENORA_DB", "scenora.db"))


class ProjectStore:
    def __init__(self, path: Path | str = DEFAULT_DB) -> None:
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute("CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, data TEXT NOT NULL)")

    def save(self, project: Project) -> Project:
        self._conn.execute(
            "INSERT OR REPLACE INTO projects (id, data) VALUES (?, ?)",
            (project.id, project.model_dump_json()),
        )
        self._conn.commit()
        return project

    def get(self, project_id: str) -> Project | None:
        row = self._conn.execute("SELECT data FROM projects WHERE id = ?", (project_id,)).fetchone()
        return Project.model_validate_json(row[0]) if row else None

    def list(self) -> list[Project]:
        rows = self._conn.execute("SELECT data FROM projects").fetchall()
        return [Project.model_validate_json(r[0]) for r in rows]

    def delete(self, project_id: str) -> bool:
        cur = self._conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self._conn.commit()
        return cur.rowcount > 0
