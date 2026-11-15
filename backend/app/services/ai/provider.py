"""Interface du fournisseur d'IA.

Le fournisseur est remplaçable : l'application ne dépend que de ce protocole.
Toute sortie est validée par les schémas Pydantic avant d'être enregistrée.
"""

from __future__ import annotations

import os
from typing import Protocol

from app.schemas import Scene, Shot


class AIProvider(Protocol):
    name: str

    def analyze_screenplay(self, text: str) -> list[Scene]:
        """Extrait scènes, personnages, lieux, actions et éléments visuels."""

    def suggest_shots(self, scene: Scene) -> list[Shot]:
        """Propose un premier découpage technique pour une scène."""


def get_provider() -> AIProvider:
    """Choisit le fournisseur selon SCENORA_AI_PROVIDER (par défaut : demo)."""
    name = os.environ.get("SCENORA_AI_PROVIDER", "demo")
    if name == "demo":
        from app.services.ai.demo import DemoProvider

        return DemoProvider()
    raise ValueError(f"Fournisseur d'IA inconnu : {name}. Valeurs possibles : demo.")


SHOT_PROMPT = """Tu es un assistant de préparation de tournage.
Voici une scène :
{scene}
Propose une shot list technique possible. Pour chaque plan, donne :
description, valeur de plan, angle, mouvement de caméra, personnages, intention narrative.
Respecte le scénario original. N'invente pas de dialogue et ne change pas l'histoire.
Réponds en JSON structuré. Toutes les propositions seront revues par le cinéaste."""
