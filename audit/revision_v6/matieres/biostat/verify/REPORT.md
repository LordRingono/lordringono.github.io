# Biostatistiques — vérification indépendante V6

**Feu vert final pour intégrer les versions complètes `approved_reviewed.json`, `approved_crops.json` et le manifeste de 167 nouveaux fichiers authentiques.** Les deux QCM déjà identifiés comme contradictoires restent hors note. Aucun fichier historique ni aucune autre matière n’a été modifié par ce vérificateur.

## Périmètre et résultat

L’examen porte sur les **14 séries présentes dans le site**, soit **138 QCM**, depuis les pages 487 à 698 de `Annales_compilation.pdf`. Les 690 lettres de réponse correspondent à **675 propositions ordinaires** et **15 lettres de code dans trois questions numériques**. Les questions numériques ne sont donc pas présentées comme quinze propositions scientifiques indépendantes.

| Série | QCM | Grille originale | Notables / hors note |
| --- | ---: | ---: | ---: |
| 2025–2026 S1 | 12 | p.494 | 12 / 0 |
| 2024–2025 S1 | 12 | p.512 | 12 / 0 |
| 2024–2025 S2 | 7 | p.526 | 7 / 0 |
| 2023–2024 S1 | 12 | p.540 | 11 / 1 |
| 2023–2024 S2 | 7 | p.554 | 7 / 0 |
| 2022–2023 S1 | 12 | p.566 | 11 / 1 |
| 2022–2023 S2 | 7 | p.582 | 7 / 0 |
| 2021–2022 S1 | 11 | p.594 | 11 / 0 |
| 2021–2022 S2 | 7 | p.608 | 7 / 0 |
| 2020–2021 PACES | 11 | p.624 | 11 / 0 |
| 2020–2021 S1 | 11 | p.640 | 11 / 0 |
| 2020–2021 S2 | 7 | p.656 | 7 / 0 |
| 2019–2020 PACES | 11 | p.672 | 11 / 0 |
| 2018–2019 PACES | 11 | p.690 | 11 / 0 |
| **Total** | **138** | **14 grilles** | **136 / 2** |

Les 595 propositions ordinaires transcrites en texte concordent avec le sujet non corrigé après normalisation de la typographie et des espaces. Une comparaison stricte conservant signes numériques et ponctuation significative ne laisse aucun écart d’importation. Les 80 propositions sous forme d’image ont été rattachées à leurs coordonnées originales et comparées au rendu du PDF.

La reprise du sujet dans le corrigé concorde pour 593 de ces 595 textes. Les deux écarts restants existent dans les documents : Q6 E de 2023–2024 S1 comporte une p-valeur parasite dans le sujet, absente du corrigé ; Q5 C de 2022–2023 S2 écrit « synucléique » dans le sujet et « synucléine » dans le corrigé. Le sujet original est conservé. La première divergence dispose déjà d’une réserve explicite.

Les **675 verdicts individuels** ont été retrouvés, y compris les verdicts sans lettres et ceux accolés aux formules. Le seul désaccord entre grille et verdicts individuels concerne les lettres A et B du Q5 2022–2023 S1, déjà hors note. Les trois tables numériques ont été vérifiées : **0,62 → ABCD**, **−1,67 → AE**, **21,4 → ABCD**. Les calculs indépendants et pages des tables figurent dans `numeric_codes.json`.

## Réparations supplémentaires du vérificateur

1. **Copie du corrigé manquante : Q1 de 2020–2021 S2.** Le panneau complet de la page 656, avec la reprise du sujet, la clé ACD et ses cinq détails, a été rétabli. Il ne manque plus de copie de corrigé dans ce lot.
2. **Dix détails textuels restaurés.** Les cinq explications de Q10 2024–2025 S1 (p.519) et les cinq de Q1 2023–2024 S2 (p.555) étaient vides dans les champs textuels préparés. L’absence de lettre A dans le premier corrigé et l’absence de toutes les lettres dans le second ont été résolues par l’ordre imprimé, les verdicts et leur concordance avec la grille. Les images authentiques restent disponibles.
3. **Recadrages sans perte.** 193 débuts de panneaux incluaient les jambages d’une ligne précédente ; 119 fins coupaient les derniers pixels d’une ligne ou d’un dénominateur. Ces limites sont réparées. Un panneau vide a été retiré. Les 37 panneaux de contexte hérités ont été élargis de x=37…550 à x=30…570 ; deux d’entre eux coupaient réellement des fins de mots.
4. **Anciennes images du corrigé.** Les limites des 18 corrigés réparées par le préparateur ont aussi été appliquées aux images de détail utilisées par le site. Quatre images ne montrant que le contexte du QCM suivant ont été retirées. Les 138 autres images de correction ont été rendues à nouveau depuis le PDF avec les bonnes limites et une largeur complète.
5. **Autres captures.** 28 images de sujet ou contexte dont des lignes dépassaient x=550 ont été rendues à nouveau. Le formulaire statistique p.670, image imprimée jusqu’à x=552,65, bénéficie également d’un nouveau cadre. Le manifeste contient donc **167 fichiers WebP sans perte**, à de nouveaux chemins `static/revision_v6/biostat/…`. Aucun ancien fichier n’a été écrasé.
6. **Réserve arithmétique réparée.** La réserve de Q3 D de 2020–2021 S1 confondait passage de 36 à 144 sujets et multiplication de l’effectif par 144. Elle explique maintenant correctement le facteur 4, la demi-largeur divisée par 2, et le passage de 1/3 à 1/6. Le détail original erroné (1/12) reste visible comme original, avec la réserve après validation.
7. **Précision scientifique supplémentaire.** Q1 C/D de 2020–2021 S2 comporte une réserve sur les proportions exactes de 50 % pour la médiane et l’intervalle interquartile en présence d’ex æquo. Les conventions du tutorat et la clé officielle ACD sont conservées. La note est étayée par les définitions consultées du NIST et d’OpenStax et invite à vérifier la ronéo.

Les **53 notes préparées ou antérieures sont préservées**, dont une amendée avec preuve arithmétique ; la note supplémentaire porte le total à 54. Le vérificateur n’a changé aucune clé, aucun identifiant, aucun poids ni l’ordre des propositions par rapport à la préparation.

## Contrôles réellement effectués

- Extraction nouvelle du texte des 212 pages du segment ; lecture de chaque sujet et de chaque corrigé, rapprochement systématique des items, grilles et détails. Les traces par item sont dans `coverage.json` et `final_source_comparison.json`.
- **57 pages de sujets et 8 pages d’annexes examinées visuellement**, sur des planches lisibles de pages, avec agrandissements et lectures ciblées des graphiques, tableaux de code et corrections sensibles. Les formules de Q5 2024–2025 S2 sont bien présentes dans le contexte partagé de la page précédente ; elles n’ont pas été omises.
- **492 images originales uniques / 957 usages** contrôlés numériquement : empreinte conforme au manifeste historique, décodage, rattachement, rôle et comparaison avec un rendu indépendant du PDF. Ce contrôle numérique ne signifie pas que les 492 petits fichiers ont tous été ouverts séparément à l’écran. Les captures regardées individuellement sont consignées dans `visual_log.json`.
- Vérification des 167 nouveaux fichiers, des chemins utilisés, de leurs empreintes, de la présence des sources et de l’absence de perte des notes. Le résultat utilise 488 images uniques pour 953 usages après retrait des quatre captures parasites.
- Résultat documentaire : **138 copies de sujet propres**, **138 copies de corrigé**, réparties en **183 panneaux sujet et 218 panneaux correction**. Les corrections et notes doivent rester accessibles après validation ; le responsable réalise les essais de l’interface et de la notation.

## Limites documentaires explicites

**Q5 2022–2023 S1** : la grille donne BCE, mais les verdicts du détail donnent ACE (pp.561, 566, 570). **Q2 2023–2024 S1** : le corrigé marque vraies deux bornes supérieures différentes et son calcul ne justifie pas la clé CD (pp.534, 540, 542). Ces deux questions restent hors note en attendant un erratum ou un arbitrage de cours.

Les ronéos UE3 pertinentes ne sont pas disponibles dans les documents recensés. Les réserves sourcées n’inventent pas de clé officielle. La couverture exhaustive annoncée concerne les 14 séries effectivement présentes dans le site et dans ce segment de compilation ; elle ne prouve pas que toutes les sessions universitaires possibles depuis 2015 ont été fournies. Aucune série antérieure à 2015 n’a été ajoutée.

## Sources scientifiques consultées directement par le vérificateur

- [NIST — intervalle de confiance d’une moyenne](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/conflimi.htm), notamment la dépendance en 1/√n.
- [NIST — loi binomiale](https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm), paramètres, dispersion et estimation.
- [SciPy — corrélation point-bisériale](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pointbiserialr.html), équivalence avec Pearson et le test de deux groupes.
- [NIST — mesures de position](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm), définition de la médiane par les rangs.
- [OpenStax — médiane et quantiles](https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data), égalités et conventions des quantiles empiriques.

Le détail des réserves et leurs références aux pages originales restent attachés aux QCM concernés.
