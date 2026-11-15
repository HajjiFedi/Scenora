"""API REST de Scenora."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from app.core.store import ProjectStore
from app.schemas import Character, ContinuityIssue, Origin, Project, Scene, Shot, SpatialLayout
from app.services.ai.provider import get_provider
from app.services.continuity.rules import check

router = APIRouter(prefix="/api")
_store: ProjectStore | None = None


def get_store() -> ProjectStore:
    global _store
    if _store is None:
        _store = ProjectStore()
    return _store


def _load(project_id: str, store: ProjectStore) -> Project:
    project = store.get(project_id)
    if project is None:
        raise HTTPException(404, "Projet introuvable")
    return project


def _find(items: list, item_id: str, label: str):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(404, f"{label} introuvable")


class ProjectIn(BaseModel):
    title: str
    description: str = ""


class ScreenplayIn(BaseModel):
    text: str
    rights_confirmed: bool


class SceneUpdate(BaseModel):
    location: str | None = None
    time_of_day: str | None = None
    description: str | None = None
    characters: list[str] | None = None
    visual_elements: list[str] | None = None


class ShotIn(BaseModel):
    number: int
    description: str
    framing: str = ""
    angle: str = ""
    movement: str = ""
    characters: list[str] = []
    props: list[str] = []
    purpose: str = ""


class ShotUpdate(BaseModel):
    number: int | None = None
    description: str | None = None
    framing: str | None = None
    angle: str | None = None
    movement: str | None = None
    characters: list[str] | None = None
    props: list[str] | None = None
    purpose: str | None = None
    axis_crossing_justified: bool | None = None
    approve: bool = False


def _apply(target, changes: BaseModel, exclude: set[str] = frozenset()) -> bool:
    data = changes.model_dump(exclude_none=True, exclude=set(exclude))
    for key, value in data.items():
        setattr(target, key, value)
    return bool(data)


@router.post("/projects", status_code=201)
def create_project(body: ProjectIn, store: ProjectStore = Depends(get_store)) -> Project:
    return store.save(Project(title=body.title, description=body.description))


@router.get("/projects")
def list_projects(store: ProjectStore = Depends(get_store)) -> list[Project]:
    return store.list()


@router.get("/projects/{project_id}")
def get_project(project_id: str, store: ProjectStore = Depends(get_store)) -> Project:
    return _load(project_id, store)


@router.delete("/projects/{project_id}", status_code=204, response_class=Response, response_model=None)
def delete_project(project_id: str, store: ProjectStore = Depends(get_store)) -> None:
    if not store.delete(project_id):
        raise HTTPException(404, "Projet introuvable")


@router.post("/projects/{project_id}/screenplay")
def import_screenplay(project_id: str, body: ScreenplayIn, store: ProjectStore = Depends(get_store)) -> Project:
    if not body.rights_confirmed:
        raise HTTPException(400, "Confirmez que vous avez les droits sur ce scénario.")
    project = _load(project_id, store)
    scenes = get_provider().analyze_screenplay(body.text)
    names = list(dict.fromkeys(n for sc in scenes for n in sc.characters))
    project.screenplay_text, project.rights_confirmed = body.text, True
    project.scenes, project.shots, project.layouts = scenes, [], {}
    project.characters = [Character(name=n) for n in names]
    return store.save(project)


@router.patch("/projects/{project_id}/scenes/{scene_id}")
def update_scene(project_id: str, scene_id: str, body: SceneUpdate,
                 store: ProjectStore = Depends(get_store)) -> Scene:
    project = _load(project_id, store)
    scene = _find(project.scenes, scene_id, "Scène")
    if _apply(scene, body):
        scene.origin = Origin.HUMAN_EDITED
    store.save(project)
    return scene


@router.post("/projects/{project_id}/scenes/{scene_id}/shots/suggest")
def suggest_shots(project_id: str, scene_id: str, store: ProjectStore = Depends(get_store)) -> list[Shot]:
    project = _load(project_id, store)
    scene = _find(project.scenes, scene_id, "Scène")
    shots = get_provider().suggest_shots(scene)
    project.shots = [s for s in project.shots if s.scene_id != scene_id] + shots
    store.save(project)
    return shots


@router.post("/projects/{project_id}/scenes/{scene_id}/shots", status_code=201)
def add_shot(project_id: str, scene_id: str, body: ShotIn, store: ProjectStore = Depends(get_store)) -> Shot:
    project = _load(project_id, store)
    _find(project.scenes, scene_id, "Scène")
    shot = Shot(scene_id=scene_id, origin=Origin.HUMAN_EDITED, **body.model_dump())
    project.shots.append(shot)
    store.save(project)
    return shot


@router.patch("/projects/{project_id}/shots/{shot_id}")
def update_shot(project_id: str, shot_id: str, body: ShotUpdate, store: ProjectStore = Depends(get_store)) -> Shot:
    project = _load(project_id, store)
    shot = _find(project.shots, shot_id, "Plan")
    if _apply(shot, body, exclude={"approve"}):
        shot.origin = Origin.HUMAN_EDITED
    if body.approve:
        shot.origin = Origin.DIRECTOR_APPROVED
    store.save(project)
    return shot


@router.delete("/projects/{project_id}/shots/{shot_id}", status_code=204, response_class=Response, response_model=None)
def delete_shot(project_id: str, shot_id: str, store: ProjectStore = Depends(get_store)) -> None:
    project = _load(project_id, store)
    _find(project.shots, shot_id, "Plan")
    project.shots = [s for s in project.shots if s.id != shot_id]
    store.save(project)


@router.put("/projects/{project_id}/scenes/{scene_id}/layout")
def set_layout(project_id: str, scene_id: str, body: SpatialLayout,
               store: ProjectStore = Depends(get_store)) -> SpatialLayout:
    project = _load(project_id, store)
    _find(project.scenes, scene_id, "Scène")
    project.layouts[scene_id] = body
    store.save(project)
    return body


@router.get("/projects/{project_id}/continuity")
def continuity(project_id: str, store: ProjectStore = Depends(get_store)) -> list[ContinuityIssue]:
    return check(_load(project_id, store))


@router.post("/projects/{project_id}/continuity/{issue_id}/dismiss", status_code=204, response_class=Response, response_model=None)
def dismiss_issue(project_id: str, issue_id: str, store: ProjectStore = Depends(get_store)) -> None:
    project = _load(project_id, store)
    if issue_id not in {i.id for i in check(project)}:
        raise HTTPException(404, "Alerte introuvable")
    project.dismissed_issues.append(issue_id)
    store.save(project)
