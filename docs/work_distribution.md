# Répartition de travail — 4 personnes, 16–24 novembre

> Neuf jours de préparation, à raison d'environ cinq heures par personne et par jour. Demi-finale le 21 novembre ; finale le 25 novembre. Le plan privilégie les critères connus du jury : fonctionnalité (35 %), éthique (20 %), impact culturel (15 %) et entrepreneuriat (10 %).

## Rôles provisoires

Les membres répartissent définitivement les rôles entre eux. En attendant, chaque colonne décrit un périmètre, pas une autorité personnelle :

| Périmètre | Responsable provisoire | Livrable central |
| --- | --- | --- |
| Backend et intégration | Fedi Hajji | API stable, configuration locale et Docker Compose |
| Frontend et accessibilité | Aziz Derbel | Application navigateur utilisable de bout en bout |
| Produit, recherche, éthique | Loua Klai | Preuves d'usage, politique éthique, script de démo et pitch |
| Design, 2D/storyboard, communication | Wala Selmi | Éditeur 2D, système visuel, supports de présentation et export |

Le propriétaire d'une tâche travaille sur sa branche de fonctionnalité, teste manuellement son flux puis fusionne. Il n'y a pas de revue formelle ; toute personne qui détecte un problème critique le signale immédiatement au groupe.

## MVP gelé

Le MVP doit fonctionner sans réseau et dans des conteneurs locaux :

1. Interface React + TypeScript + Vite, avec Tailwind ; React Konva pour le plan 2D.
2. Créer/lister un projet, importer un **texte** avec confirmation des droits, analyser via le fournisseur `demo` local.
3. Voir/éditer scènes et plans ; ajouter/supprimer/modifier/approuver des plans ; montrer leur origine.
4. Enregistrer un plan 2D visuel : acteurs, objets, caméras et axe des 180°.
5. Voir, comprendre et ignorer les alertes ; les suppressions sont affichées comme une décision du cinéaste, avec raison facultative si livrable.
6. Interface française et arabe, navigation clavier complète et gestion RTL validée au minimum sur l'écran import/scènes.
7. Parcours testé sur `appartement.txt` et au moins un exemple arabe/derja fourni par l'équipe.
8. Conteneurs frontend/backend et un guide de lancement en une commande ou une commande clairement documentée.

### Fonctionnalités conditionnelles (ne passent qu'après le MVP)

- Génération de storyboard **avec IA**, par un fournisseur local ou une API de démo explicitement consentie. Aucun scénario réel ni image de référence n'est envoyé à une API externe. Si la génération n'est pas configurée, l'UI explique la limite et ne bloque pas la démo.
- Export PDF incluant projet, shot list, storyboard disponible, alertes/décisions et notes de sources des références.
- Import de références visuelles avec droits confirmés, champs auteur/source/licence, avertissement sur likeness/personnage protégé et suppression.

Les imports PDF/DOCX, comptes, persistance après redémarrage, PostgreSQL, collaboration, 3D et analyse d'image restent hors MVP.

## Tableau de bord journalier

| Date | Backend et intégration | Frontend et accessibilité | Produit, éthique, recherche | Design, 2D, communication | Vérification collective |
| --- | --- | --- | --- | --- | --- |
| **16 nov.** | Faire passer les tests, définir CORS et `docker-compose`; publier un exemple JSON API | Initialiser React/TS/Vite/Tailwind, thème, routing et appel API | Geler MVP, écrire guide d'entretien et grille concurrents | Maquette du flux et composants ; préparer le modèle d'écran 2D | API et UI se lancent localement ; rôles confirmés |
| **17 nov.** | Ajouter seulement les correctifs API nécessaires ; image Docker backend | Écrans liste/création/import, confirmation des droits, états chargement/erreur | Obtenir ou planifier entretiens ; vérifier Boords/Katalist : import, shot list, continuité, prix/limites | Maquettes finalisées ; préparer icônes/éléments accessibles | Import de `appartement.txt` utilisable depuis le navigateur |
| **18 nov.** | Stabiliser fournisseur `demo`; écrire/documenter la stratégie de dégradation IA | Écrans scènes et shot list : édition, ajout/suppression, origine et approbation | Premier entretien ou test utilisateur ; documenter besoins et limites | Vignettes/storyboard de secours et style de présentation | Modification et approbation d'un plan visibles en UI |
| **19 nov.** | Vérifier/corriger le contrat layout et 180° ; tests de régression | Construire le plan 2D (acteurs, objets, caméras, axe), clavier et focus | Deuxième entretien ; préparer discours éthique, local-first et références | Rendre le plan 2D lisible ; commencer slides | Alerte 180° déclenchée puis expliquée sans JSON manuel |
| **20 nov.** | Docker Compose complet et erreurs API lisibles | Écran alertes, décision d'ignorer, français/arabe et premier test RTL | Finaliser preuves avant demi-finale ; préparer FAQ concurrentielle | Préparer support et captures de secours | Répétition complète sur appartement + cas arabe/derja |
| **21 nov. — demi-finale** | Geler les changements non critiques et assister la démo | Démontrer parcours navigateur local | Présenter problème, preuves et éthique ; relever questions jury | Présenter plan 2D/identité visuelle | Démo de demi-finale ; journal des retours et priorités |
| **22 nov.** | Choisir et réaliser un seul bonus faisable ; conserver mode demo | Corriger friction observée ; ajouter UI du bonus retenu | Analyser retours jury, renforcer impact culturel/entrepreneurial | Réaliser bonus visuel : storyboard IA opt-in **ou** export, selon faisabilité | Test manuel complet et décision de couper/continuer le bonus |
| **23 nov.** | Si bonus IA : fournisseur local/démo et absence de fuite ; sinon PDF/export | Polissage, accessibilité, erreurs et dégradation gracieuse | Finaliser citations, politique référence et messages de limites | Finaliser slides, visuels, export/support de secours | Répétition chronométrée avec réseau coupé |
| **24 nov.** | Tests finaux, images Docker, `.env.example`, sauvegarde de démo | Build final et vérification clavier/RTL dans navigateur final | Script final, Q&A, checklist de soumission | Slides/captures/vidéo de secours prêts | Geler la version ; seuls bugs bloquants sont autorisés |
| **25 nov. — finale** | Démarrer environnement local et plan B | Conduire démo si désigné | Pitch et réponses éthique/produit si désigné | Présentation visuelle si désigné | Présenter ; consigner les apprentissages |

## Checklist avant chaque fusion

- La fonctionnalité est utilisable depuis l'interface, pas seulement par Swagger ou JSON manuel.
- Les erreurs de droits, API indisponible, IA indisponible et texte invalide ne cassent pas l'écran.
- Les contrôles ont un nom accessible, un focus visible et sont utilisables au clavier.
- Aucune clé, scénario réel ou référence utilisateur n'est ajoutée au dépôt.
- Le scénario `appartement.txt` fonctionne toujours et `python -m pytest -q` reste vert si le backend change.
- Le changement est ajouté au script de démo ou explicitement laissé hors démonstration.

## Décisions d'équipe à prendre au plus tard le 16 novembre

1. Attribuer les quatre rôles provisoires ci-dessus à des personnes réelles.
2. Nommer la personne qui peut arbitrer une coupe de périmètre le jour même ; à défaut, la décision se prend collectivement en 10 minutes et est notée dans `context.md`.
3. Choisir le bonus unique des 22–23 novembre : storyboard IA locale/démo ou export PDF. Le plan 2D est déjà P0.
4. Préparer ou fournir le scénario de test arabe/derja et un texte de consentement d'entretien.
5. Identifier les 20 % de critères jury manquants et confirmer le format/durée de présentation.
