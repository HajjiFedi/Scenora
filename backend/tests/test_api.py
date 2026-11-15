from __future__ import annotations

from fastapi.testclient import TestClient


def create(client: TestClient) -> str:
    return client.post("/api/projects", json={"title": "Démo"}).json()["id"]


def test_import_requires_rights(client: TestClient, screenplay: str) -> None:
    pid = create(client)
    r = client.post(f"/api/projects/{pid}/screenplay", json={"text": screenplay, "rights_confirmed": False})
    assert r.status_code == 400


def test_full_journey(client: TestClient, screenplay: str) -> None:
    pid = create(client)
    project = client.post(f"/api/projects/{pid}/screenplay", json={"text": screenplay, "rights_confirmed": True}).json()
    scene = project["scenes"][0]
    assert scene["origin"] == "ai_draft" and scene["characters"] == ["Maya", "Adam"]

    shots = client.post(f"/api/projects/{pid}/scenes/{scene['id']}/shots/suggest").json()
    assert shots[0]["framing"] == "plan large" and all(s["origin"] == "ai_draft" for s in shots)

    edited = client.patch(f"/api/projects/{pid}/shots/{shots[0]['id']}", json={"movement": "travelling avant"}).json()
    assert edited["origin"] == "human_edited"
    approved = client.patch(f"/api/projects/{pid}/shots/{shots[1]['id']}", json={"approve": True}).json()
    assert approved["origin"] == "director_approved"

    client.delete(f"/api/projects/{pid}/shots/{shots[1]['id']}")
    issues = client.get(f"/api/projects/{pid}/continuity").json()
    assert "numero_manquant" in {i["rule"] for i in issues}

    issue_id = issues[0]["id"]
    assert client.post(f"/api/projects/{pid}/continuity/{issue_id}/dismiss").status_code == 204
    assert issue_id not in {i["id"] for i in client.get(f"/api/projects/{pid}/continuity").json()}


def test_axis_crossing_through_api(client: TestClient, screenplay: str) -> None:
    pid = create(client)
    scene = client.post(f"/api/projects/{pid}/screenplay", json={"text": screenplay, "rights_confirmed": True}).json()["scenes"][0]
    shots = client.post(f"/api/projects/{pid}/scenes/{scene['id']}/shots/suggest").json()
    layout = {"axis": ["Maya", "Adam"], "elements": [
        {"type": "actor", "label": "Maya", "x": 0, "y": 0},
        {"type": "actor", "label": "Adam", "x": 10, "y": 0},
        {"type": "camera", "label": "A", "x": 3, "y": 6, "shot_id": shots[1]["id"]},
        {"type": "camera", "label": "B", "x": 7, "y": -6, "shot_id": shots[2]["id"]},
    ]}
    assert client.put(f"/api/projects/{pid}/scenes/{scene['id']}/layout", json=layout).status_code == 200
    rules = {i["rule"] for i in client.get(f"/api/projects/{pid}/continuity").json()}
    assert "regle_180" in rules


def test_delete_project(client: TestClient) -> None:
    pid = create(client)
    assert client.delete(f"/api/projects/{pid}").status_code == 204
    assert client.get(f"/api/projects/{pid}").status_code == 404
