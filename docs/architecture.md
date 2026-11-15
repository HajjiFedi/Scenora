# Architecture de Scenora

Scenora est un **monolithe modulaire** : une seule application backend, découpée en modules, et une interface web séparée.

```text
Interface React (prévue)
        │  REST / JSON
        ▼
API FastAPI ─────────────── backend/app/api/routes.py
  ├── Projets et scénario    backend/app/core/store.py (SQLite)
  ├── Analyse du scénario    backend/app/services/screenplay/ + services/ai/
  ├── Shot list              routes + services/ai/ (suggestions)
  ├── Plan 2D                backend/app/services/spatial/geometry.py
  ├── Moteur de continuité   backend/app/services/continuity/rules.py
  ├── Storyboard             prévu (API de génération d'images)
  └── Export PDF             prévu
```

## Principes

1. **Le plan (Shot) est l'objet central.** Storyboard, caméras du plan 2D et alertes de continuité se réfèrent au même plan. Modifier un plan met à jour tout ce qui en dépend ; il n'y a pas de documents à synchroniser à la main.
2. **Le backend possède les données et l'orchestration de l'IA.** L'interface possède l'édition interactive et la visualisation.
3. **Toute sortie de l'IA est validée par un schéma Pydantic** (`backend/app/schemas.py`) avant d'être enregistrée.
4. **On ne demande pas à un modèle de langage ce qu'un calcul peut vérifier.** La règle des 180° est un calcul géométrique (`side_of_axis`), pas une estimation de l'IA.
5. **Le fournisseur d'IA est remplaçable.** L'application dépend du protocole `AIProvider` (`backend/app/services/ai/provider.py`), pas d'un modèle précis.

## Modèle de données

| Entité | Attributs principaux | État |
| --- | --- | --- |
| Project | id, title, description, screenplay_text, rights_confirmed | Implémenté |
| Character | id, name, description | Implémenté |
| Scene | id, number, heading, interior, location, time_of_day, characters, actions, dialogue, visual_elements, origin | Implémenté |
| Shot | id, scene_id, number, description, framing, angle, movement, characters, props, purpose, origin | Implémenté |
| SpatialElement | id, type (actor, camera, object), label, x, y, rotation, shot_id | Implémenté |
| ContinuityIssue | id, rule, scene_id, shot_id, severity, message | Implémenté |
| Storyboard | id, shot_id, image_path, prompt, version, origin | Prévu (24 novembre) |
| LocationReference | id, scene_id, image_path | Prévu (24 novembre) |
| User | id, email, password_hash | Prévu après le hackathon |

Le champ `origin` vaut `ai_draft` (brouillon de l'IA), `human_edited` (modifié par un humain) ou `director_approved` (approuvé par le cinéaste).

Pour le prototype, chaque projet est enregistré comme un document JSON validé dans SQLite. Le passage à des tables relationnelles (SQLAlchemy, PostgreSQL) est prévu pour le déploiement.

## API

| Méthode | Route | Rôle |
| --- | --- | --- |
| POST | /api/projects | Créer un projet |
| GET | /api/projects | Lister les projets |
| GET | /api/projects/{id} | Lire un projet |
| DELETE | /api/projects/{id} | Supprimer un projet et toutes ses données |
| POST | /api/projects/{id}/screenplay | Importer un scénario texte (droits confirmés) et l'analyser |
| PATCH | /api/projects/{id}/scenes/{scene_id} | Corriger l'extraction d'une scène |
| POST | /api/projects/{id}/scenes/{scene_id}/shots/suggest | Proposer une shot list |
| POST | /api/projects/{id}/scenes/{scene_id}/shots | Ajouter un plan à la main |
| PATCH | /api/projects/{id}/shots/{shot_id} | Modifier ou approuver un plan |
| DELETE | /api/projects/{id}/shots/{shot_id} | Supprimer un plan |
| PUT | /api/projects/{id}/scenes/{scene_id}/layout | Enregistrer le plan 2D d'une scène |
| GET | /api/projects/{id}/continuity | Lister les alertes de continuité |
| POST | /api/projects/{id}/continuity/{issue_id}/dismiss | Ignorer une alerte |

La documentation interactive est servie par FastAPI sur `http://127.0.0.1:8000/docs`.
