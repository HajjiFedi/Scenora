"""Point d'entrée : uvicorn app.main:app --reload (depuis le dossier backend)."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Scenora API",
    description="Du scénario au plan de tournage : l'IA propose, le cinéaste décide.",
    version="0.1.0",
)
app.include_router(router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
