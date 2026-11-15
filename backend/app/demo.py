"""Démonstration du parcours complet, sans serveur ni clé d'API.

Usage (depuis le dossier backend) : python -m app.demo ../examples/appartement.txt
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from app.api import routes
from app.core.store import ProjectStore
from app.main import app


def say(text: str) -> None:
    sys.stdout.write(text + "\n")


def run(screenplay_path: str) -> None:
    store = ProjectStore(Path(tempfile.mkdtemp()) / "demo.db")
    app.dependency_overrides[routes.get_store] = lambda: store
    client = TestClient(app)
    pid = client.post("/api/projects", json={"title": "Démo Scenora"}).json()["id"]
    text = Path(screenplay_path).read_text(encoding="utf-8")
    project = client.post(f"/api/projects/{pid}/screenplay", json={"text": text, "rights_confirmed": True}).json()

    for scene in project["scenes"]:
        say(f"\nScène {scene['number']} : {scene['heading']}  [{scene['origin']}]")
        say(f"  Personnages : {', '.join(scene['characters'])}")
        say(f"  Éléments visuels : {', '.join(scene['visual_elements']) or 'aucun'}")
        shots = client.post(f"/api/projects/{pid}/scenes/{scene['id']}/shots/suggest").json()
        for shot in shots:
            say(f"  Plan {shot['number']} ({shot['framing']}) : {shot['description']}  [{shot['origin']}]")
        if len(shots) > 1:
            client.delete(f"/api/projects/{pid}/shots/{shots[1]['id']}")
            say(f"  -> Le cinéaste supprime le plan {shots[1]['number']}.")

    say("\nAlertes de continuité :")
    for issue in client.get(f"/api/projects/{pid}/continuity").json():
        say(f"  [{issue['rule']}] {issue['message']}")
    app.dependency_overrides.clear()


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "../examples/appartement.txt")
