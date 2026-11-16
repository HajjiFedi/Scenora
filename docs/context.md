# Contexte partagé — Scenora

> Document de référence pour l'équipe. Mis à jour le 16 novembre 2026 à partir de l'état réel du dépôt et des décisions d'équipe. Mettre à jour les statuts, décisions et blocages au début et à la fin de chaque journée.

## 1. Mission et promesse

**Scenora** aide un cinéaste à passer d'un scénario à un plan de tournage : analyse de scènes, proposition de shot list, corrections humaines, contrôle de continuité, puis storyboard et export.

La phrase à conserver dans la démo et le pitch : **« L'IA propose, le cinéaste décide. »** L'outil ne remplace ni le jugement artistique ni le contrôle de continuité : ses propositions sont éditables et traçables.

Le projet est présenté au hackathon **IA Éthique 360**, sous-thématique IA et audiovisuel culturel. Public prioritaire : réalisateurs indépendants, étudiants et petites équipes, d'abord en Tunisie et dans l'espace francophone. Les scénarios français, arabe et derja sont dans le périmètre ; l'interface doit être proposée en français et en arabe.

## 2. État réel du dépôt

### Ce qui fonctionne maintenant

- Backend Python/FastAPI fonctionnel avec stockage local SQLite.
- Création, lecture, liste et suppression d'un projet.
- Import d'un **scénario texte** conditionné à la confirmation des droits.
- Analyse et proposition de shot list en mode `demo` hors ligne : ce sont des heuristiques, pas un modèle de langage.
- Édition des scènes et plans, ajout/suppression de plans et approbation par le cinéaste.
- Provenance de chaque scène/plan : `ai_draft`, `human_edited`, `director_approved`.
- Sauvegarde d'un plan 2D sous forme de données (acteurs, objets, caméras, axe).
- Moteur de continuité déterministe avec sept règles et possibilité d'ignorer une alerte.
- Suite Pytest déclarée à 18 tests dans le README.

### Ce qui n'existe pas encore dans le dépôt

- Interface React/TypeScript/Vite/Tailwind ; `frontend/` ne contient qu'un README. Ce choix est désormais le choix de travail recommandé pour livrer vite ; React Konva est retenu pour l'éditeur 2D.
- Fournisseur de modèle de langage hébergé et clé/configuration correspondante.
- Import PDF et DOCX.
- Storyboard et génération d'images.
- Éditeur visuel du plan 2D (les données et le calcul existent seulement côté backend).
- Export PDF.
- Comptes, authentification, collaboration temps réel et base PostgreSQL.

## 3. Architecture et conventions techniques

```text
Navigateur (React + TypeScript, à créer)
  └─ REST/JSON
       └─ FastAPI  backend/app/api/routes.py
            ├─ SQLite / document JSON validé : core/store.py
            ├─ scénario : services/screenplay/
            ├─ IA remplaçable : services/ai/
            ├─ continuité : services/continuity/
            └─ géométrie plan 2D : services/spatial/
```

Le projet est un **monolithe modulaire**. Le backend garde les données, valide les contrats Pydantic et orchestre l'IA ; le frontend affiche et édite. Ne contourner ni les schémas Pydantic ni l'API avec de la logique métier dupliquée côté client.

Le `Shot` est l'objet pivot : storyboard, caméra du plan 2D et alertes se rapportent à un même `shot_id`. Après une modification de plan, l'interface doit relire les alertes de continuité.

Couleurs prévues : anthracite `#222321`, ivoire chaud `#F1EBDD`, bordeaux `#873E43`, or mat `#B58C5A`. Polices : Playfair Display et Inter.

## 4. Données et API à préserver

Entités principales :

| Entité | Éléments importants |
| --- | --- |
| `Project` | titre, description, texte du scénario, droits confirmés, personnages, scènes, plans, plans 2D, alertes ignorées |
| `Scene` | numéro, en-tête, INT/EXT, lieu, moment, personnages, actions, dialogue, éléments visuels, origine |
| `Shot` | `scene_id`, numéro, description, cadrage, angle, mouvement, personnages, accessoires, intention, justification d'un franchissement d'axe, origine |
| `SpatialLayout` | éléments acteur/caméra/objet et paire d'acteurs qui définit l'axe des 180° |
| `ContinuityIssue` | règle, sévérité, message, scène/plan concernés, identifiant stable |

Routes disponibles :

| Action | Route |
| --- | --- |
| Projets | `POST/GET /api/projects`, `GET/DELETE /api/projects/{id}` |
| Import et analyse texte | `POST /api/projects/{id}/screenplay` |
| Corriger une scène | `PATCH /api/projects/{id}/scenes/{scene_id}` |
| Proposer / ajouter des plans | `POST .../shots/suggest`, `POST .../shots` |
| Modifier / supprimer un plan | `PATCH/DELETE /api/projects/{id}/shots/{shot_id}` |
| Enregistrer le plan 2D | `PUT /api/projects/{id}/scenes/{scene_id}/layout` |
| Lire / ignorer les alertes | `GET .../continuity`, `POST .../continuity/{issue_id}/dismiss` |

Attention : suggérer à nouveau les plans d'une scène remplace tous les plans actuels de cette scène. Le frontend doit donc demander confirmation avant cette action si des modifications humaines existent.

## 5. Continuité : les sept règles démontrables

1. `scene_sans_plan` : une scène sans plan.
2. `numero_manquant` : un numéro de plan absent dans une séquence.
3. `numero_double` : deux plans ont le même numéro.
4. `personnage_absent` : un plan montre un personnage absent de la scène.
5. `personnage_non_filme` : un personnage de la scène n'est montré par aucun plan.
6. `accessoire_non_montre` : un élément visuel du scénario n'est montré par aucun plan (information).
7. `regle_180` : deux caméras consécutives se trouvent de côtés opposés de l'axe défini ; le second plan peut justifier le franchissement.

Ces contrôles n'utilisent pas de modèle : ils doivent rester explicables, non destructifs et déterministes. Une alerte ne corrige jamais les données elle-même.

## 6. Parcours à réussir en démonstration

Utiliser d'abord `examples/appartement.txt`, puis démontrer `examples/cafe-tunis.txt` pour le derja :

1. Créer un projet et attester des droits sur le scénario.
2. Importer le texte ; afficher les scènes, personnages et accessoires extraits comme **brouillons IA**.
3. Corriger au moins un élément pour rendre visible la supervision humaine.
4. Générer et ajuster la shot list ; approuver au moins un plan.
5. Pour les plans choisis, créer/montrer le storyboard si cette fonction est livrée.
6. Placer Maya et Adam, puis deux caméras de côtés opposés de leur axe ; afficher l'alerte de règle des 180°.
7. Corriger ou justifier l'alerte, puis exporter le dossier si l'export est livré.

La démonstration reste valide sans image générée : ne jamais bloquer le parcours principal sur une API image ou une clé externe.

## 7. Éthique et critères non négociables

- Les scénarios réels sont traités localement. Un fournisseur externe ne peut servir que pour une démonstration avec données d'exemple approuvées, après consentement explicite et étiquette visible ; il n'est jamais indispensable au parcours.
- Conserver l'original et permettre la correction humaine ; ne pas effacer silencieusement une proposition.
- Afficher l'origine de chaque contenu IA et ne pas représenter les sorties demo comme une vraie IA hébergée.
- Exiger la confirmation des droits pour les scénarios ; appliquer la même idée aux images de référence.
- Interdire les prompts imitant un artiste vivant ou nommé et avertir quand une référence peut montrer une personne identifiable ou un personnage protégé.
- Réduire la génération d'images : uniquement les plans sélectionnés, sans régénération automatique, résolution limitée.
- Tester français, arabe et derja ; éviter les références visuelles clichés et ne jamais inventer une culture à partir d'un stéréotype.
- Les clés restent dans `.env`, jamais dans Git. Le stockage actuel est local SQLite ; ne pas promettre de sécurité multi-utilisateur avant les comptes.
- Scenora ne recherche, ne récupère ni ne scrape des références visuelles. Le cinéaste les importe volontairement, confirme ses droits, peut ajouter auteur/source/licence, les supprime quand il le souhaite et sait si elles sortent de sa machine.

## 8. Installation et vérification

Depuis `Scenora/backend` sous Windows :

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example .env
python -m pytest -q
python -m app.demo ../examples/appartement.txt
uvicorn app.main:app --reload
```

Ouvrir ensuite `http://127.0.0.1:8000/docs`. La livraison visée est **containerisée en local** (Docker Compose : frontend + backend). Pendant le développement frontend, définir clairement l'URL de l'API et une politique CORS minimale pour le serveur Vite local.

## 9. Risques et décisions à verrouiller

| Risque / décision | Impact | Responsable de décision | Échéance souhaitée |
| --- | --- | --- | --- |
| Choix d'un fournisseur local/de démo, coût, confidentialité et sortie JSON | Peut bloquer l'analyse réaliste | Responsable technique + éthique | Jour 1 |
| MVP exact de la demi-finale et de la finale | Empêche la dispersion | Toute l'équipe | Jour 1 |
| Interface sans maquette ni API frontend existante | Risque principal de livraison | Responsable frontend | Jour 1 |
| CORS et contrat de données frontend/backend | Peut bloquer l'intégration | Frontend + backend | Jour 2 |
| Génération d'images locale ou API de démo non fiable/coûteuse | Ne doit pas casser la démo | Produit + technique | Jour 3 |
| Import PDF/DOCX et export PDF | Charge élevée, dépendances nouvelles | Responsable backend | Jour 2 |
| Entretiens utilisateurs et test Boords/Katalist | Preuve de besoin insuffisante sans eux | Recherche/pitch | Jour 2 |
| Supports de langues arabe/derja (RTL, police, cas de test) | Peut faire échouer une exigence jugée | Frontend + produit | Jour 2 |

## 10. Rituel d'équipe

- Stand-up quotidien de 10 minutes : fait, prochain livrable, blocage, décision requise.
- Un seul tableau de tâches avec propriétaire unique, lien vers branche/PR et définition de fini.
- Intégration quotidienne sur une branche partagée ou par PR courte ; aucune modification concurrente de `schemas.py` ou `routes.py` sans accord préalable.
- Avant toute démo : parcours `appartement.txt`, test de régression backend et vérification visuelle du navigateur.
- Chaque décision produit/éthique est ajoutée en bas de ce document avec sa date, son décideur et sa justification.

## 11. Journal de décisions

| Date | Décision | Décideur | Justification / conséquence |
| --- | --- | --- | --- |
| 16 nov. 2026 | À compléter | À compléter | À compléter |

## 12. Décisions confirmées le 16 novembre 2026

| Sujet | Décision |
| --- | --- |
| Calendrier | Préparation du **16 au 24 novembre inclus** (9 jours) ; demi-finale le 21 novembre ; finale le 25 novembre. |
| Capacité | Quatre personnes, environ cinq heures par personne et par jour (180 heures au total avant la finale). |
| Développement | Branches de fonctionnalités ; pas de revue formelle obligatoire. L'auteur exécute la checklist manuelle avant fusion. |
| Déploiement | Démonstration locale, containerisée ; aucune persistance après redémarrage n'est requise. |
| MVP | Parcours navigateur obligatoire ; import texte seulement ; comptes hors périmètre ; plan 2D visuel prioritaire. |
| Langues | Français et arabe dans l'interface ; français, arabe et derja dans les scénarios de démonstration. |
| IA | Mode demo accepté. Les scénarios réels restent locaux ; modèles locaux et clés/API gratuites peuvent être explorés sans devenir une dépendance critique. |
| Export | L'export final doit réunir shot list, storyboard disponible, alertes/décisions de continuité et notes de référence. |
| Qualité | Checklist de test manuel ; traitement gracieux des quatre erreurs clés : droits, fournisseur IA indisponible, texte invalide, API indisponible. |
| Accessibilité | Texte 4,5:1 ; texte large et composants 3:1 ; clavier complet/focus visible/sans piège ; nom accessible pour contrôles et images ; erreurs et progression annoncées. |
| Références visuelles | Import explicite seulement, confirmation des droits, source/auteur/licence facultatifs, jamais d'entraînement, suppression possible, avertissement likeness/personnage protégé et interdiction de style d'artiste nommé. |
| Jury | Pondérations connues : prototype 35 %, éthique 20 %, impact culturel 15 %, entrepreneuriat 10 %. Les 20 % restants sont à clarifier. |
