# Checklist MVP verrouillée — Scenora

## But de la démo

En moins de cinq minutes, montrer qu'un cinéaste garde le contrôle : il importe un scénario dont il détient les droits, obtient des brouillons locaux, corrige et approuve une shot list, organise l'espace, comprend une alerte des 180° et prend une décision visible.

## À livrer obligatoirement avant le 21 novembre

- [ ] `docker compose up --build` (ou instruction équivalente vérifiée) démarre le frontend et le backend locaux.
- [ ] Le navigateur permet de créer un projet et d'importer un scénario texte avec confirmation des droits.
- [ ] Le mode `demo` local fonctionne sans clé et est explicitement étiqueté comme tel.
- [ ] Les scènes et la shot list sont visibles ; un utilisateur peut ajouter, modifier, supprimer et approuver un plan.
- [ ] Les origines `ai_draft`, `human_edited` et `director_approved` sont visibles.
- [ ] Le plan 2D visuel permet de placer deux acteurs, au moins deux caméras et de définir l'axe.
- [ ] Une caméra de chaque côté de l'axe déclenche une alerte des 180° explicable.
- [ ] Une alerte peut être ignorée comme décision du cinéaste, jamais comme correction automatique.
- [ ] Tous les contrôles sont utilisables au clavier ; contrastes et messages d'erreur respectent les exigences documentées.
- [ ] Le flux est vérifié en français et l'interface/cas de test arabe ou derja est vérifié au minimum sur import et scènes.
- [ ] Une checklist manuelle est exécutée et les tests backend passent après tout changement backend.

## À décider après la demi-finale, seulement si le MVP est vert

- [ ] Storyboard IA local ou API de démo consentie, avec aucun scénario réel/référence utilisateur transmis vers l'extérieur.
- [ ] Ou export PDF complet : shot list, storyboard disponible, alertes/décisions et crédits des références.
- [ ] Import de références visuelles avec droits, attribution facultative, avertissements et suppression.

## Démo finale et plan de secours

- [ ] Démo complète sur `examples/appartement.txt`.
- [ ] Démo ou capture préparée sur scénario arabe/derja fourni par l'équipe.
- [ ] Captures ou vidéo de secours disponibles hors ligne.
- [ ] Le plan de secours est testé : Docker/local + fournisseur demo + exemple fictif, sans Internet.
- [ ] Le pitch relie chaque assertion aux critères jury : fonctionnalité, éthique, impact culturel et entrepreneuriat.
