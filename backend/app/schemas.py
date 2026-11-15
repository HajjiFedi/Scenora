"""Contrat de données partagé par tous les modules.

Le plan (Shot) est l'objet central : storyboard, plan 2D et continuité s'y réfèrent.
"""

from __future__ import annotations

from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


def new_id() -> str:
    return uuid4().hex[:12]


class Origin(str, Enum):
    """Qui a produit l'élément et ce que le cinéaste en a fait."""

    AI_DRAFT = "ai_draft"                    # Brouillon généré par l'IA
    HUMAN_EDITED = "human_edited"            # Modifié par un humain
    DIRECTOR_APPROVED = "director_approved"  # Approuvé par le cinéaste


class Character(BaseModel):
    id: str = Field(default_factory=new_id)
    name: str
    description: str = ""


class Scene(BaseModel):
    id: str = Field(default_factory=new_id)
    number: int
    heading: str
    interior: bool | None = None
    location: str = ""
    time_of_day: str = ""
    description: str = ""
    characters: list[str] = Field(default_factory=list, description="Noms des personnages présents")
    actions: list[str] = Field(default_factory=list)
    dialogue: list[str] = Field(default_factory=list)
    visual_elements: list[str] = Field(default_factory=list)
    origin: Origin = Origin.AI_DRAFT


class Shot(BaseModel):
    id: str = Field(default_factory=new_id)
    scene_id: str
    number: int
    description: str
    framing: str = Field("", description="Valeur de plan : plan large, plan moyen, gros plan…")
    angle: str = ""
    movement: str = ""
    characters: list[str] = Field(default_factory=list)
    props: list[str] = Field(default_factory=list)
    purpose: str = Field("", description="Intention narrative")
    axis_crossing_justified: bool = False
    origin: Origin = Origin.AI_DRAFT


class ElementType(str, Enum):
    ACTOR = "actor"
    CAMERA = "camera"
    OBJECT = "object"


class SpatialElement(BaseModel):
    id: str = Field(default_factory=new_id)
    type: ElementType
    label: str
    x: float
    y: float
    rotation: float = 0.0
    shot_id: str | None = Field(None, description="Pour une caméra : le plan qu'elle filme")


class SpatialLayout(BaseModel):
    elements: list[SpatialElement] = Field(default_factory=list)
    axis: tuple[str, str] | None = Field(None, description="Labels des deux acteurs qui définissent l'axe des 180°")


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"


class ContinuityIssue(BaseModel):
    id: str = Field("", description="Identifiant stable, pour ignorer l'alerte")
    rule: str
    scene_id: str | None = None
    shot_id: str | None = None
    severity: Severity = Severity.WARNING
    message: str


class Project(BaseModel):
    id: str = Field(default_factory=new_id)
    title: str
    description: str = ""
    screenplay_text: str = ""
    rights_confirmed: bool = False
    characters: list[Character] = Field(default_factory=list)
    scenes: list[Scene] = Field(default_factory=list)
    shots: list[Shot] = Field(default_factory=list)
    layouts: dict[str, SpatialLayout] = Field(default_factory=dict, description="Plan 2D par scene_id")
    dismissed_issues: list[str] = Field(default_factory=list, description="Alertes ignorées par le cinéaste")
