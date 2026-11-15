from __future__ import annotations

from app.services.ai.demo import DemoProvider
from app.services.screenplay.parser import parse_heading, split_scenes


def test_split_scenes_on_headings() -> None:
    text = "1. INT. CAFÉ - JOUR\nAmel entre.\n\n2. EXT. RUE - NUIT\nKarim sort."
    scenes = split_scenes(text)
    assert [s.number for s in scenes] == [1, 2]
    assert scenes[1].lines == ["Karim sort."]


def test_parse_heading() -> None:
    assert parse_heading("1. INT. CAFÉ, RUE DE MARSEILLE, TUNIS - JOUR") == (True, "CAFÉ, RUE DE MARSEILLE, TUNIS", "JOUR")
    assert parse_heading("EXT. PLAGE — NUIT") == (False, "PLAGE", "NUIT")


def test_demo_provider_extracts_scene(screenplay: str) -> None:
    scene = DemoProvider().analyze_screenplay(screenplay)[0]
    assert scene.characters == ["Maya", "Adam"]
    assert scene.time_of_day == "NUIT"
    assert {"lettre", "table", "fenêtre"} <= set(scene.visual_elements)


def test_demo_provider_reads_dialogue_cues() -> None:
    text = "INT. CAFÉ - JOUR\nAmel s'assoit.\nKARIM\nYa Amel, chnowa ?"
    scene = DemoProvider().analyze_screenplay(text)[0]
    assert "Karim" in scene.characters
    assert scene.dialogue == ["Ya Amel, chnowa ?"]
