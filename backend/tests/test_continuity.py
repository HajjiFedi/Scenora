from __future__ import annotations

from app.schemas import ElementType, Project, Scene, Shot, SpatialElement, SpatialLayout
from app.services.continuity import rules


def project_with(shots: list[Shot], scene: Scene | None = None) -> Project:
    scene = scene or Scene(id="s1", number=1, heading="INT. CAFÉ - JOUR", characters=["Amel", "Karim"])
    return Project(title="Test", scenes=[scene], shots=shots)


def shot(number: int, characters: list[str], shot_id: str | None = None) -> Shot:
    extra = {"id": shot_id} if shot_id else {}
    return Shot(scene_id="s1", number=number, description="plan", characters=characters, **extra)


def test_coherent_project_has_no_issue() -> None:
    assert rules.check(project_with([shot(1, ["Amel", "Karim"])])) == []


def test_scene_without_shots() -> None:
    assert [i.rule for i in rules.scene_without_shots(project_with([]))] == ["scene_sans_plan"]


def test_missing_and_duplicate_numbers() -> None:
    project = project_with([shot(1, ["Amel"]), shot(3, ["Karim"]), shot(3, ["Karim"])])
    assert "n° 2 manque" in rules.missing_shot_numbers(project)[0].message
    assert "2 plans portent le n° 3" in rules.duplicate_shot_numbers(project)[0].message


def test_character_absent_and_never_filmed() -> None:
    project = project_with([shot(1, ["Amel", "Sami"])])
    assert "Sami" in rules.character_absent_from_scene(project)[0].message
    assert "Karim" in rules.character_never_filmed(project)[0].message


def test_prop_never_shown() -> None:
    scene = Scene(id="s1", number=1, heading="INT. CAFÉ - JOUR", visual_elements=["lettre"])
    assert len(rules.prop_never_shown(project_with([], scene))) == 1


def layout(cam1: tuple[float, float], cam2: tuple[float, float]) -> SpatialLayout:
    return SpatialLayout(axis=("Amel", "Karim"), elements=[
        SpatialElement(type=ElementType.ACTOR, label="Amel", x=0, y=0),
        SpatialElement(type=ElementType.ACTOR, label="Karim", x=10, y=0),
        SpatialElement(type=ElementType.CAMERA, label="A", x=cam1[0], y=cam1[1], shot_id="p1"),
        SpatialElement(type=ElementType.CAMERA, label="B", x=cam2[0], y=cam2[1], shot_id="p2"),
    ])


def test_axis_180_same_side_is_fine() -> None:
    project = project_with([shot(1, ["Amel"], "p1"), shot(2, ["Karim"], "p2")])
    project.layouts["s1"] = layout((2, 5), (8, 5))
    assert rules.axis_180(project) == []


def test_axis_180_crossing_is_flagged() -> None:
    project = project_with([shot(1, ["Amel"], "p1"), shot(2, ["Karim"], "p2")])
    project.layouts["s1"] = layout((2, 5), (8, -5))
    issues = rules.axis_180(project)
    assert len(issues) == 1 and "180°" in issues[0].message


def test_axis_180_justified_crossing_is_not_flagged() -> None:
    second = shot(2, ["Karim"], "p2")
    second.axis_crossing_justified = True
    project = project_with([shot(1, ["Amel"], "p1"), second])
    project.layouts["s1"] = layout((2, 5), (8, -5))
    assert rules.axis_180(project) == []


def test_dismissed_issue_is_hidden() -> None:
    project = project_with([])
    first, *others = rules.check(project)
    project.dismissed_issues.append(first.id)
    assert rules.check(project) == others
