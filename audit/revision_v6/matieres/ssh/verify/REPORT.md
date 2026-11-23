# SSH — vérification indépendante finale V6

**Feu vert pour intégration des fichiers approuvés ci-dessous**, avec les limites de provenance et les deux exclusions de notation explicitement conservées.

## Périmètre réellement contrôlé

| Série | QCM | Items | QCM notables |
|---|---:|---:|---:|
| ACC | 38 | 190 | 38 |
| Colle 2 | 79 | 395 | 77 |
| Colle 1 | 78 | 390 | 78 |
| EB blanc | 79 | 395 | 79 |
| Total | 274 | 1 370 | 272 |

J’ai extrait directement et indépendamment les huit PDF fournis (184 pages), puis lu les 274 énoncés, les 1 370 propositions et leurs verdicts/détails, dans douze lots de lecture. `independent_sources.json` conserve les lignes et leurs coordonnées ; `coverage.json` consigne le contrôle de chaque QCM et de chaque item. Le contrôle ne repose pas seulement sur le rapport du préparateur.

Les 272 clés applicables correspondent aux verdicts de la source. Les symboles cochés/croisés de Colle 1 et EB ont été confrontés à leurs clés récapitulatives ; les VRAI/FAUX d’ACC et Colle 2 ont été confrontés à leurs clés. La grille courte de Colle 2 a été extraite séparément : ses 79 entrées correspondent au détail du corrigé, sans rendre applicables les clés des questions 11 et 12 à un autre sujet.

## Résultat de la comparaison systématique

- 1 367 propositions importées correspondent exactement au texte non corrigé après normalisation des espaces, accents et ponctuation. Trois accords grammaticaux sans changement de sens sont acceptés : ACC 5E, 29A et 31D. ACC 3 conserve un écart d’article le/la sans incidence pédagogique.
- Neuf autres différences mineures entre sujet et répétition du corrigé sont documentées ; elles ne changent pas la correspondance des items. Les dix propositions de Colle 2 Q11/Q12 appartiennent en revanche à des questions différentes dans le corrigé.
- Tous les détails applicables correspondent au PDF. Les quatre détails non vides du mauvais couple Colle 2 Q11/Q12 restent exclus. Les 752 absences de détail dans les sources n’ont pas été comblées par une explication inventée ; 746 concernent les 272 QCM assortis du bon corrigé. Le site a 756 champs de détail vides, dont les dix items des deux QCM exclus.
- Le contexte commun ACC 25–26 est présent et fidèle au sujet. Les coupures multipages et le commentaire général ACC 38 ont été vérifiés. Les intitulés des cours suivants n’entrent pas dans les détails ACC 16E et 26E.
- Les 559 panneaux ont tous été rendus et contrôlés pour leurs coordonnées, leur contenu textuel et l’absence d’image vide. J’ai lu visuellement 23 planches ciblées, listées dans `coverage.json` ; je ne présente pas les 559 panneaux comme ayant tous fait l’objet d’une lecture visuelle individuelle.

## Compléments du vérificateur

Sept notes apparaissent uniquement dans la correction, sans modification de clé :

| QCM/item | Réserve ajoutée |
|---|---|
| Colle 2 73B | Composition et durée des mandats du CCNE : ancien cadre dans le détail, comparé à L1412-2 depuis 2021. |
| Colle 2 74C | Déclaration des recherches sur iPS : portée limitée à certains protocoles, avec pouvoirs d’opposition de l’ABM. |
| Colle 2 39A | Distinguer l’achèvement du Projet génome humain en 2003 des travaux T2T de 2022. |
| Colle 1 43E | Responsabilité pour infection nosocomiale : exception de la cause étrangère. |
| Colle 1 55C | Le verdict repose sur les mots « d’autres troubles » ; ne pas en déduire une négation du masquage évoqué par le correcteur. |
| Colle 1 69D | Le sujet compare a posteriori à a posteriori ; intention a priori supposée mais non substituée. |
| EB 37D | Les premiers hôpitaux ne datent pas, en général, de la peste de 1347. |

Les 39 anciennes notes sont inchangées. Les 58 notes du préparateur sont conservées, avec remplacement d’un lien AP-HP 404 par une autre publication de l’AP-HP. Les 34 références primaires mobilisées pour les nouvelles réserves du préparateur ont été reconsultées, au besoin via le texte original ou une publication institutionnelle de remplacement ; `external_source_checks.json` trace ces cas. La réserve sur l’hématome sous-dural de Colle 1 Q70 existait déjà : elle est pertinente et n’a pas été dupliquée. Total : 104 notes.

## Limites et documents encore nécessaires

1. **Colle 2 Q11/Q12 : corrigés correspondants manquants.** Le corrigé au même numéro porte sur d’autres propositions, retrouvées dans EB 54–55. Les deux QCM gardent une réponse vide, sans `answerIsEmpty`, et `correctionMismatch:true` avec un avertissement explicite. Le document non correspondant peut être montré pour transparence, mais ne doit jamais être présenté comme une clé validée de ces sujets.
2. **Colle 1 et EB : originaux institutionnels non remis en page manquants.** Les PDF fournis contiennent déjà des commentaires personnalisés et une présentation reconstruite. La fidélité à ces pièces est vérifiée ; la fidélité de leur transcription initiale à des originaux absents ne peut pas l’être. Demander notamment le texte complet d’EB 6B et la consigne d’origine d’EB 77.
3. **Ronéos et errata du tutorat non fournis.** Les notes signalent des contradictions ou des conventions à faire confirmer. Les références externes ne sont pas présentées comme les ronéos du cours.

`missing.json` liste ces pièces. Aucun autre lot ni fichier du site final n’a été modifié par ce vérificateur. Les contrôles du rendu de l’interface, du masquage avant correction et des profils restent à l’intégrateur.

## Fichiers approuvés

- `approved_reviewed.json` — SHA256 `0e6beca7c5815b5e844801045ca2d7814e168c6c2014045cae54fb02bc17aeb9`
- `approved_crops.json` — SHA256 `a439d5c05e0d2afe1bc3f2868e7a9e8c90ffef6dde5672f014d024e0fa277d23`
- `coverage.json` — SHA256 `8e8b4d14032fbb2432bb71ead9f783a2b325b48db674357df4dd64ca0665c6ef`
- `issues.json` — SHA256 `b8045c1ca376d33e7afe2cbb9346bdda91ea4e628578335a18f9e600e9e35e9a`
- `missing.json` — SHA256 `7cec78d4eeb618a642941b8140e0089c8f36c9be959b2353b9bfe85d429aec20`
