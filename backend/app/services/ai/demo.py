"""Fournisseur de démonstration, sans modèle ni clé d'API.

Il applique des heuristiques simples pour que le parcours complet soit
démontrable hors ligne. Il ne remplace pas le modèle de langage prévu :
ses résultats sont des brouillons que le cinéaste corrige.
"""

from __future__ import annotations

import re

from app.schemas import Origin, Scene, Shot
from app.services.screenplay.parser import is_cue, parse_heading, split_scenes

STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "il", "elle", "ils", "elles", "puis", "on", "son", "sa",
    "the", "a", "an", "he", "she", "they", "then", "his", "her", "it", "in", "at", "ya",
    "int", "ext", "jour", "nuit", "day", "night",
}
PROPS = {
    "lettre", "letter", "table", "fenêtre", "window", "lampe", "lamp", "téléphone", "phone",
    "clé", "key", "photo", "verre", "glass", "sac", "bag", "porte", "door", "café", "coffee",
    "voiture", "car", "couteau", "knife", "livre", "book",
}
WORD = re.compile(r"[A-Za-zÀ-ÿ']+")
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _names(action_text: str, cues: list[str]) -> list[str]:
    found = [c.title() for c in cues]
    for word in WORD.findall(action_text):
        if word[0].isupper() and len(word) > 2 and word.lower() not in STOPWORDS:
            found.append(word)
    return list(dict.fromkeys(found))


def _props(action_text: str) -> list[str]:
    words = [w.lower() for w in WORD.findall(action_text)]
    return list(dict.fromkeys(w for w in words if w in PROPS))


class DemoProvider:
    name = "demo"

    def analyze_screenplay(self, text: str) -> list[Scene]:
        return [self._scene(raw.number, raw.heading, raw.lines) for raw in split_scenes(text)]

    def _scene(self, number: int, heading: str, lines: list[str]) -> Scene:
        interior, location, time_of_day = parse_heading(heading)
        cues, dialogue, actions = [], [], []
        for i, line in enumerate(lines):
            if is_cue(line):
                cues.append(line.strip())
            elif i > 0 and is_cue(lines[i - 1]):
                dialogue.append(line.strip())
            else:
                actions.extend(s for s in SENTENCE.split(line.strip()) if s)
        action_text = " ".join(actions)
        return Scene(
            number=number, heading=heading, interior=interior, location=location,
            time_of_day=time_of_day, description=action_text, characters=_names(action_text, cues),
            actions=actions, dialogue=dialogue, visual_elements=_props(action_text),
        )

    def suggest_shots(self, scene: Scene) -> list[Shot]:
        shots = [Shot(
            scene_id=scene.id, number=1, description=f"Plan d'ensemble : {scene.location}",
            framing="plan large", angle="hauteur d'œil", movement="fixe",
            characters=list(scene.characters), purpose="Situer le lieu et les personnages",
        )]
        for name in scene.characters:
            shots.append(Shot(
                scene_id=scene.id, number=len(shots) + 1, description=f"{name} dans l'action",
                framing="plan moyen", angle="hauteur d'œil", movement="fixe",
                characters=[name], purpose=f"Suivre {name}",
            ))
        for prop in scene.visual_elements:
            shots.append(Shot(
                scene_id=scene.id, number=len(shots) + 1, description=f"Insert : {prop}",
                framing="gros plan", angle="plongée légère", movement="fixe",
                props=[prop], purpose="Montrer un élément important du récit",
            ))
        for shot in shots:
            shot.origin = Origin.AI_DRAFT
        return shots
