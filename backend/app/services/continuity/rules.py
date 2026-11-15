"""Règles de continuité (étape 6). Fonctions pures, sans IA.

Chaque règle lit un projet et renvoie des alertes. Aucune ne modifie le projet :
le cinéaste décide de corriger ou d'ignorer.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from typing import Callable

from app.schemas import ContinuityIssue, ElementType, Project, Scene, Severity, Shot
from app.services.spatial.geometry import side_of_axis

Rule = Callable[[Project], list[ContinuityIssue]]


def _issue(rule: str, message: str, scene: Scene, shot: Shot | None = None,
           severity: Severity = Severity.WARNING) -> ContinuityIssue:
    shot_id = shot.id if shot else None
    return ContinuityIssue(
        id=hashlib.sha1(f"{rule}|{scene.id}|{shot_id}|{message}".encode()).hexdigest()[:12], rule=rule, scene_id=scene.id,
        shot_id=shot_id, severity=severity, message=message,
    )


def _shots(project: Project, scene: Scene) -> list[Shot]:
    return sorted((s for s in project.shots if s.scene_id == scene.id), key=lambda s: s.number)


def scene_without_shots(project: Project) -> list[ContinuityIssue]:
    return [
        _issue("scene_sans_plan", f"La scène {sc.number} n'a aucun plan.", sc)
        for sc in project.scenes if not _shots(project, sc)
    ]


def missing_shot_numbers(project: Project) -> list[ContinuityIssue]:
    issues = []
    for sc in project.scenes:
        numbers = {s.number for s in _shots(project, sc)}
        for n in sorted(set(range(1, max(numbers, default=0) + 1)) - numbers):
            issues.append(_issue("numero_manquant", f"Scène {sc.number} : le plan n° {n} manque.", sc))
    return issues


def duplicate_shot_numbers(project: Project) -> list[ContinuityIssue]:
    issues = []
    for sc in project.scenes:
        counts = Counter(s.number for s in _shots(project, sc))
        for n, count in sorted(counts.items()):
            if count > 1:
                issues.append(_issue("numero_double", f"Scène {sc.number} : {count} plans portent le n° {n}.", sc))
    return issues


def character_absent_from_scene(project: Project) -> list[ContinuityIssue]:
    issues = []
    for sc in project.scenes:
        for shot in _shots(project, sc):
            for name in shot.characters:
                if name not in sc.characters:
                    msg = f"Plan {shot.number} : {name} n'est pas dans la scène {sc.number} selon le scénario."
                    issues.append(_issue("personnage_absent", msg, sc, shot))
    return issues


def character_never_filmed(project: Project) -> list[ContinuityIssue]:
    issues = []
    for sc in project.scenes:
        filmed = {c for s in _shots(project, sc) for c in s.characters}
        for name in sc.characters:
            if name not in filmed:
                msg = f"{name} est dans la scène {sc.number} mais aucun plan ne le ou la montre."
                issues.append(_issue("personnage_non_filme", msg, sc))
    return issues


def prop_never_shown(project: Project) -> list[ContinuityIssue]:
    issues = []
    for sc in project.scenes:
        shown = {p for s in _shots(project, sc) for p in s.props}
        for prop in sc.visual_elements:
            if prop not in shown:
                msg = f"« {prop} » est dans la scène {sc.number} mais aucun plan ne le montre."
                issues.append(_issue("accessoire_non_montre", msg, sc, severity=Severity.INFO))
    return issues


def axis_180(project: Project) -> list[ContinuityIssue]:
    """Signale deux plans consécutifs filmés de part et d'autre de l'axe des 180°."""
    issues = []
    for sc in project.scenes:
        layout = project.layouts.get(sc.id)
        if not layout or not layout.axis:
            continue
        actors = {e.label: (e.x, e.y) for e in layout.elements if e.type == ElementType.ACTOR}
        if not all(name in actors for name in layout.axis):
            continue
        a, b = actors[layout.axis[0]], actors[layout.axis[1]]
        cameras = {e.shot_id: (e.x, e.y) for e in layout.elements if e.type == ElementType.CAMERA and e.shot_id}
        sided = [(s, side_of_axis(a, b, cameras[s.id])) for s in _shots(project, sc) if s.id in cameras]
        sided = [(s, side) for s, side in sided if side != 0]
        for (prev, prev_side), (cur, cur_side) in zip(sided, sided[1:]):
            if prev_side != cur_side and not cur.axis_crossing_justified:
                msg = (f"Scène {sc.number} : entre les plans {prev.number} et {cur.number}, la caméra "
                       f"franchit l'axe {layout.axis[0]}–{layout.axis[1]} (règle des 180°).")
                issues.append(_issue("regle_180", msg, sc, cur))
    return issues


RULES: list[Rule] = [
    scene_without_shots,
    missing_shot_numbers,
    duplicate_shot_numbers,
    character_absent_from_scene,
    character_never_filmed,
    prop_never_shown,
    axis_180,
]


def check(project: Project) -> list[ContinuityIssue]:
    """Toutes les alertes, sauf celles que le cinéaste a choisi d'ignorer."""
    issues = [issue for rule in RULES for issue in rule(project)]
    return [i for i in issues if i.id not in project.dismissed_issues]
