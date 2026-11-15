# Démarche éthique à 360°

Les six angles du hackathon IA Éthique 360 sont traduits en choix de conception, pas seulement en déclarations.

| Angle | Risque | Ce que fait Scenora | État |
| --- | --- | --- | --- |
| Les créateurs | L'IA impose un découpage standard | L'IA propose, le cinéaste décide. Chaque scène et chaque plan porte une étiquette : brouillon de l'IA, modifié par un humain, approuvé par le cinéaste. Aucune alerte ne modifie le projet. | Implémenté |
| Les créateurs | Remplacement des dessinateurs de storyboard | Brouillons volontairement sommaires, pour préparer le tournage ; à discuter avec des dessinateurs lors des entretiens | Prévu |
| Les droits | Scénario ou image importés sans autorisation | L'import exige que l'utilisateur confirme détenir les droits sur le scénario. Même règle pour les images de référence. Conditions du fournisseur d'images respectées. | Implémenté pour le scénario |
| Les droits | Imitation du style d'un artiste | Aucun prompt « à la manière de » un artiste nommé | Prévu avec le storyboard |
| Les données | Fuite d'un scénario inédit | Stockage local (SQLite), suppression complète d'un projet par l'API, collecte minimale, clé d'API hors du dépôt (`.env`). Aucun réentraînement sur les scénarios. | Implémenté ; contrôle d'accès prévu avec les comptes |
| Les cultures et les langues | Derja mal comprise, clichés orientalistes | Le texte original est conservé tel quel. Exemple de scène en derja dans le dépôt. Français, arabe et derja à tester avec le modèle de langage. Références visuelles tunisiennes sous licence pour le storyboard. | Partiel |
| La transparence | Le public ou l'équipe ignore ce qui vient de l'IA | Étiquette d'origine sur chaque élément ; chaque alerte cite sa règle | Implémenté ; étiquette sur les images prévue |
| La planète | Coût énergétique des images, environ 60 fois celui du texte ([Luccioni et al.](https://arxiv.org/html/2311.16863v3)) | Images seulement pour les plans choisis, pas de régénération automatique, résolution limitée. Les règles de continuité n'utilisent aucun modèle. | Partiel |

## Risques résiduels

- Une alerte de continuité peut être fausse ou manquer une erreur : Scenora réduit le nombre d'erreurs sans garantir leur absence.
- Un cinéaste pressé peut tout approuver sans relire. Les étiquettes d'origine rendent ce choix visible, sans l'empêcher.
- Un storyboard généré peut être séduisant tout en plaçant mal les personnages. Les métadonnées du plan restent séparées de l'image et font foi.
