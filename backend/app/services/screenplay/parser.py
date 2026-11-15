"""Découpage déterministe d'un scénario texte en scènes.

Sert à préparer le texte avant l'IA et de solution de repli quand aucun
fournisseur d'IA n'est configuré. Le texte original n'est jamais modifié.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

HEADING = re.compile(r"^\s*(?:\d+\s*[.)]?\s*)?(INT\.?/EXT|EXT\.?/INT|INT|EXT|I/E)[.\s]", re.IGNORECASE)
TIME_SPLIT = re.compile(r"\s+[-–—]\s+")
CUE = re.compile(r"^[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ' .-]{1,30}$")


@dataclass
class RawScene:
    number: int
    heading: str
    lines: list[str] = field(default_factory=list)


def split_scenes(text: str) -> list[RawScene]:
    """Coupe le texte à chaque en-tête de scène (INT. / EXT.)."""
    scenes: list[RawScene] = []
    for line in text.splitlines():
        if HEADING.match(line):
            scenes.append(RawScene(len(scenes) + 1, line.strip()))
        elif scenes and line.strip():
            scenes[-1].lines.append(line.rstrip())
    return scenes


def parse_heading(heading: str) -> tuple[bool | None, str, str]:
    """Renvoie (intérieur, lieu, moment) à partir d'un en-tête de scène."""
    body = re.sub(r"^\s*\d+\s*[.)]?\s*", "", heading)
    prefix, _, rest = body.partition(".") if "." in body[:8] else body.partition(" ")
    interior = None if "/" in prefix else prefix.strip().upper().startswith("INT")
    parts = TIME_SPLIT.split(rest.strip())
    location = parts[0].strip(" .")
    time_of_day = parts[-1].strip(" .") if len(parts) > 1 else ""
    return interior, location, time_of_day


def is_cue(line: str) -> bool:
    """Une ligne en majuscules seule (ex. « AMEL ») annonce un dialogue."""
    stripped = line.strip()
    return bool(CUE.match(stripped)) and not HEADING.match(stripped) and len(stripped.split()) <= 4
