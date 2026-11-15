from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api import routes
from app.core.store import ProjectStore
from app.main import app

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    store = ProjectStore(tmp_path / "test.db")
    app.dependency_overrides[routes.get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def screenplay() -> str:
    return (EXAMPLES / "appartement.txt").read_text(encoding="utf-8")
