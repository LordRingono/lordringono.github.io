# Relecture croisée ciblée — UE3

## Périmètre et méthode

Relecture indépendante des données de `work/agents/ue3/exams.json` contre le PDF fourni **Sujets + corrections compilés(1).pdf**. Les pages ont été rendues, puis comparées aux images effectivement référencées dans `stemImages` et `referenceImages`, ainsi qu’aux textes des options. Les extraits repliables `originalImages` n’ont pas été considérés comme suffisants pour fournir les données nécessaires à la réponse.

Aucun fichier de l’UE3 n’a été modifié par cette relecture. Les deux points relevés ont été communiqués au responsable UE3 et au responsable de l’intégration, puis leur traitement a été revérifié dans le JSON final.

## Sujet 2025–2026, session 1 : 12 QCM

| QCM | Pages PDF | Contrôle des données visibles avant correction | Résultat |
|---|---:|---|---|
| 1 | 488 | Les cinq propositions sont dans le panneau visible ; la fraction **s/n** de E est complète et identique au sujet. | Conforme |
| 2 | 488 | Sodium : moyenne théorique 130,00 mmol/L, écart-type 2,00, groupe de 4 patients, intervalle centré à 95 %, précision demandée. Les cinq bornes/options sont conservées. | Conforme |
| 3 | 488 | Patch : 35 patients, 28 irritations, IC 95 %, deux chiffres significatifs ; variable X et paramètre π. Les cinq propositions sont reproduites, dont la loi binomiale de paramètre (35, π). | Conforme |
| 4 | 489 | Contexte complet des 16 patientes en deux groupes, traitements, moyennes −3/−2,5 et écarts-types 0,3/0,4 ; cinq propositions visibles. | Conforme |
| 5 | 489 | Même contexte commun que Q4, plus statistique du test −2,000. Les cinq options, l’intervalle et les valeurs numériques sont conservés. | Conforme |
| 6 | 490 | Étude HFME : 910 patients, 10 malades ; tableau des sensibilités/spécificités **90 %/70 % et 80 %/80 %** intégralement inclus dans le contexte visible. | Conforme |
| 7 | 490 | Contexte commun de Q6 et consigne locale de comparaison des sensibilités ; cinq propositions conformes. | Conforme |
| 8 | 490–491 | Contexte HFME, spécificité de référence à Necker 85 %, deux approximations numériques et cinq propositions. | Conforme après nettoyage du contexte hérité |
| 9 | 490–491 | Contexte HFME/Necker nécessaire au « QCM précédent », propositions sur puissance, risque α et valeurs prédictives. | Conforme après nettoyage du contexte hérité |
| 10 | 491 | 25 sujets, r = 0,56 et t observé = 3,24 ; les cinq propositions sont conservées. | Conforme |
| 11 | 492 | Essai spironolactone : 64 centres, équilibre tous les 6 patients, aveugle, critère composite et analyse en intention de traiter ; cinq propositions. | Conforme |
| 12 | 492 | Étude nirsevimab : 690 cas, 345 témoins, année 2023, effet 0,83 et IC [0,73 ; 0,89] ; cinq propositions. | Conforme |

La seule anomalie d’assemblage constatée était l’héritage de la phrase locale du QCM 7, « On souhaite comparer la sensibilité des deux tests diagnostiques », dans les QCM 8 et 9 portant ensuite sur la spécificité. Le responsable UE3 l’a retirée de `sourceContext` et de `stemImages` pour Q8/Q9. **La suppression a été vérifiée dans le JSON**, et le contexte commun de l’exercice ainsi que le contexte Necker sont conservés.

## Trois QCM à réponse codée

| Sujet / QCM | Sujet | Corrigé | Contrôle |
|---|---:|---:|---|
| 2019–2020 PACES, Q2 | p. 662 | grille p. 672, détail p. 674 | Contexte arthrose 80 %, échantillon 100, bornes 0,78 et 0,82 : complets. Toutes les cases du tableau 1 sont visibles, sans correction sur l’image. **0,62 correspond à ABCD**, comme dans les deux corrigés. |
| 2019–2020 PACES, Q4 | contexte p. 662, QCM p. 663 | grille p. 672, détail p. 675 | Le contexte de la page précédente est récupéré : référence 135 g/L, moyenne 133, n = 25, variance 36. Le tableau 2 inclut les valeurs négatives et leur signe. **−1,67 correspond à AE**, comme dans les deux corrigés. |
| 2018–2019 PACES, Q2 | p. 684 | grille p. 690, détail p. 692 | Contexte Apache II complet : référence 15, n = 81, moyenne 20, écart-type 6. Les consignes d’arrondi et l’ensemble du tableau sont présents. **21,4 correspond à ABCD**, comme dans les deux corrigés. |

**Réserve de source signalée et ajoutée :** le corrigé détaillé du QCM 2 de 2019–2020, p. 674, écrit `P(F ≤ 0,78) + P(F ≤ 0,82)` alors que le sujet demande la queue inférieure à 0,78 ou la queue supérieure à 0,82. Le résultat 0,62 et le code ABCD concordent avec le calcul des deux queues demandé. La clé reste celle de la source ; une remarque explicite signale la coquille du signe dans la justification. **Cette remarque est présente dans le JSON final.**

## Contrôle d’une annexe nécessaire

Le **QCM 1 de PACES 2020–2021** (sujet p. 614) demande une lecture dans une table de loi normale. Son contexte visible conserve les bornes d’hémoglobine 124 et 156 g/L, les percentiles 2,5/97,5, le seuil d’anémie à 120 g/L et les règles d’arrondi. Ses `referenceImages` contiennent les annexes source p. 619–622. La **table de fonction de répartition p. 619 a été comparée visuellement au PDF** : en-têtes, marges, corps du tableau, grandes valeurs et exemple sont complets. La table de l’écart réduit p. 620 est également complète. Ces annexes proviennent des pages du sujet, avant la couverture du corrigé p. 623.

Le responsable UE3 a ajouté une provenance explicite pour les autres séries qui réutilisent les trois tables statistiques p. 667–669 ; cette relecture n’évalue pas la totalité de ces rattachements.

## Conclusion du contrôle ciblé

Aucune donnée, option, équation ou figure nécessaire manquante n’a été trouvée dans les 16 QCM ciblés. Les données utiles sont présentes dans les panneaux visibles ou les annexes, sans devoir ouvrir l’extrait original. Les deux observations — consigne locale héritée et coquille du signe dans un corrigé — ont été traitées et vérifiées.

Fichier UE3 contrôlé après ces modifications : SHA-256 `4c04d654f6b4a280dac31d0b9c07a8c631e2de44b796749b071f504ee0496fca`.

## Confirmation complémentaire UE4, photographie p. 941

Le dossier livrable `work/agents/ue4/assets/` ne contient plus l’ancienne capture `annales_ue4_2019-2020_s1_q04_original_p941.webp`. Le panneau de figure a été recadré sur le tableau molécules/activités. Les trois extraits originaux restants sont limités au titre, à la partie non annotée de la légende et au tableau avec les options. Ces quatre images ont été inspectées visuellement : **aucun coefficient manuscrit n’y reste visible**. Le manifeste UE4 ne référence que ces versions sans annotation.
