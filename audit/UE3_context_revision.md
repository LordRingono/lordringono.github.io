# Révision UE3 — contextes communs et limites des propositions

## Résultat livré

Les **14 sujets et 138 QCM** ont été repris. La structure comprend désormais **39 blocs `sharedContexts`**, utilisés par **76 questions**. Les énoncés communs sont séparés des données locales et ne contiennent aucune proposition A–E. Les 16 anciens panneaux regroupés de propositions ont été remplacés par **80 captures distinctes**, chacune attachée à son propre item.

Les identifiants, numéros source, clés de correction, poids et clés de stockage sont inchangés. Il reste **137 QCM notés et un QCM hors note** pour la contradiction de source déjà documentée. Aucun contenu extérieur au lot UE3 n’a été modifié.

La sauvegarde complète de la version antérieure, JSON, scripts, rapports et images compris, se trouve dans `work/agents/ue3/v1/`.

## Défaut réel de dépendance réparé

**2018–2019 PACES, QCM 2 → QCM 3, p. 684–685.** Le QCM 3 parle de l’intervalle calculé précédemment. L’ancienne reprise ne montrait pour Q3 que les données Apache II (81 patients, moyenne 20, écart-type 6, référence 15) ; elle ne reprenait pas la consigne d’intervalle de confiance à 95 % ni ses règles d’arrondi. Le bloc commun Q2–Q3 reprend maintenant ces données **et la demande exacte du QCM 2**. Le tableau de réponses codées reste local à Q2 et aucune de ses valeurs n’est introduite dans le bloc commun.

Cette vérification a porté sur les contextes situés avant le numéro de question, après l’item E précédent et sur les pages précédentes. Les autres données déjà présentes dans la v1 ont été regroupées explicitement plutôt que réinventées.

## Séparation entre données communes et consignes locales

- **2025–2026 S1, Q6–9** : l’étude HFME et son tableau constituent le bloc commun général. La comparaison à Necker est un second bloc réservé à Q8–Q9. La consigne de comparaison des sensibilités reste propre à Q7.
- **2024–2025 S1, Q6–8** : le lot initial de 200 lésions, le gastroentérologue et le taux de 60 % constituent le contexte partagé des trois questions. Le test contre la cible de 70 % et sa statistique proche de 3 constituent une dépendance distincte **Q6/Q8**, puisque Q8-C renvoie expressément à Q6. Ils ne sont pas affichés comme une consigne du Q7.
- **2023–2024 S1, Q9–10** : l’essai AVC et les données de départ sont communs. La demande de comparer les évaluations locale/centralisée et la statistique 2,7 restent dans la consigne propre à Q9.
- **2022–2023 S2, Q1–3** : l’histogramme et l’effectif 8 100 sont communs. La moyenne 2,70 et l’écart-type sont rappelés pour Q2–Q3. La demande d’intervalle et l’aide 4/3 ≈ 1,3 restent locales à Q2 ; Q3 garde son hypothèse de moyenne 3,00.
- **2021–2022 S1, Q8–10** : le suivi HADS du groupe de 100 patients est commun. La référence hors COVID à 0,2 et la statistique 2,5 restent locales à Q8. Les données de ventilation sont locales à Q9, et le suivi de dépression local à Q10.
- **2021–2022 S2, Q4–7** : la définition de la silicose est commune. Les performances de TDM restent dans Q4. L’étude de 8 000 travailleurs de Q5 et celle de 3 500 patients de Q6–7 conservent leurs effectifs et leurs finalités distincts.
- **2019–2020 PACES, Q8–9** : le contexte des adénocarcinomes du côlon est commun ; les effectifs 130/90/60/80 de la comparaison diagnostique sont réservés au QCM 8. La nouvelle étude de résection du QCM 9 reste distincte.
- **2018–2019 PACES, Q4–5** : le but du test sur la pente/régression reste visible pour Q5. La consigne « unique proposition » de Q4 n’est plus héritée par Q5.

Les données placées avant un saut de page restent accessibles au groupe correspondant, notamment p. 522 → Q4–5 p. 523, p. 562 → Q8–9 p. 563, p. 605 → Q6–7 p. 606, p. 615 → Q6–7 p. 616, p. 662 → Q4 p. 663, p. 663 → Q6–7 p. 664 et p. 685 → Q6–7 p. 686.

Les autres blocs reprennent fidèlement leurs données communes, tableaux, courbes, distributions ou aides numériques. Les énoncés concernant une seule question restent locaux à cette question.

## Inventaire des groupes, sujet par sujet

Chaque numéro ci-dessous est un numéro source, indépendant des filtres de l’interface. Deux listes partiellement superposées représentent deux blocs distincts, chacun avec son champ d’application explicite.

| Sujet | QCM conservés | Blocs communs | Groupes de numéros source |
|---|---:|---:|---|
| 2025-2026 / s1 | 12 | 3 | 4, 5 ; 6, 7, 8, 9 ; 8, 9 |
| 2024-2025 / s1 | 12 | 4 | 4, 5 ; 9, 10 ; 6, 7, 8 ; 6, 8 |
| 2024-2025 / s2 | 7 | 2 | 2, 3 ; 4, 5 |
| 2023-2024 / s1 | 12 | 3 | 2, 3 ; 7, 8 ; 9, 10 |
| 2023-2024 / s2 | 7 | 1 | 6, 7 |
| 2022-2023 / s1 | 12 | 5 | 1, 2, 3 ; 2, 3 ; 4, 5 ; 8, 9 ; 10, 11 |
| 2022-2023 / s2 | 7 | 4 | 1, 2, 3 ; 4, 5 ; 6, 7 ; 2, 3 |
| 2021-2022 / s1 | 11 | 2 | 6, 7 ; 8, 9, 10 |
| 2021-2022 / s2 | 7 | 2 | 6, 7 ; 4, 5, 6, 7 |
| 2020-2021 / paces | 11 | 1 | 6, 7 |
| 2020-2021 / s1 | 11 | 2 | 6, 7 ; 8, 9 |
| 2020-2021 / s2 | 7 | 2 | 2, 3 ; 5, 6 |
| 2019-2020 / paces | 11 | 4 | 1, 2 ; 3, 4 ; 6, 7 ; 8, 9 |
| 2018-2019 / paces | 11 | 4 | 4, 5 ; 6, 7 ; 8, 9 ; 2, 3 |

## Contrôle strict des items

Les 80 nouvelles captures ont été inspectées en huit planches, puis les frontières sensibles ont été ouvertes individuellement. Les fractions, racines, exposants, indices et symboles sont conservés. Chaque rectangle contient la lettre de sa propre proposition et aucune lettre de proposition voisine. L’absence d’un marqueur voisin complète la vérification visuelle ; elle ne la remplace pas.

Une première découpe de **2024–2025 S1 Q3-A** laissait un minuscule fragment du signe de Q3-B. Sa limite inférieure a été ramenée à **y=193,0** ; les nouvelles images A et B ont ensuite été revérifiées séparément. Le fragment a disparu et les deux formules sont complètes.

Les anciennes chaînes mathématiques déformées de `sourceOptions` ne sont plus présentes dans le JSON actif. Les propositions concernées utilisent `text: ""` et `image: "static/…revision…webp"`. Le moteur doit afficher l’image à l’intérieur de la case A/B/C/D/E correspondante. Les trois questions numériques codées conservent leur tableau et leurs cases de code.

Les 138 fins d’item E ont été relues avec les débuts suivants. Aucun en-tête d’exercice suivant ou corrigé n’a été introduit dans un item. Deux particularités visibles existent déjà dans le PDF et sont conservées comme anomalies de source, sans correction scientifique inventée :

- 2023–2024 S1 Q6-E comporte une plage de p-valeur accolée à sa phrase. Elle est déjà imprimée dans le sujet ; elle n’a pas été aspirée depuis la question suivante.
- 2023–2024 S2 Q4-E porte un caractère `$` final dans le sujet original.

## Provenance et fichiers conservés

La version finale utilise **492 images** : 350 extraits de sujet et 142 extraits de corrigé. Parmi elles, **409 images conservées sont identiques octet pour octet à la v1**. Les **83 nouvelles images** portent toutes un nom contenant `_revision_` : 80 propositions, deux blocs communs recadrés et une aide de calcul locale. Aucun ancien fichier n’a été écrasé sous son nom d’origine.

`assets_manifest.json` contient la page, le rectangle exact, le rôle sujet/correction, l’identifiant propriétaire, le numéro d’item éventuel, l’empreinte et toutes les utilisations, y compris `sharedContexts.images` et `option.image`. Les captures partagées et les nouvelles propositions proviennent exclusivement des pages des sujets non corrigés. Les corrigés restent dans `correctionImages`.

## Contrat avec le moteur

```text
q.sharedContexts = [{
  id: identifiant stable et unique,
  text: texte fidèle ou chaîne vide,
  images: références de captures,
  questionNumbers: numéros source concernés,
  sourceStartPage: première page source,
  sourceEndPage: dernière page source
}]
```

Un même identifiant correspond à un objet identique dans chaque question membre. Le moteur affiche ce bloc **une seule fois avant le premier membre visible**, y compris si les premiers membres sont masqués par un filtre. Les objets sont ordonnés du contexte général au contexte complémentaire. Aucun des extraits déplacés n’est encore présent dans `stemImages` du même QCM.

`stemImages` conserve les éléments locaux ; certains textes locaux sont repris directement au début de `question` afin de ne pas mélanger une consigne propre avec le bloc commun. Les clés, profils et comportements de correction ne changent pas.

## Vérifications et reproductibilité

- Relecture des 138 contextes/préfixes et demandes, sujet par sujet.
- Relecture des dépendances explicites aux questions précédentes et des fins d’item E.
- Vérification visuelle des 80 nouvelles captures de propositions et des trois autres nouveaux extraits.
- Vérification des 39 objets partagés : membres exacts, objets identiques, pages source valides et aucun item A–E dans les captures communes.
- Comparaison des 138 identifiants/clés/poids et des 14 clés de stockage à la sauvegarde v1.
- Comparaison des 409 empreintes d’images conservées et contrôle des 492 chemins référencés.

Les scripts reproductibles sont `revise_contexts.py`, puis `audit_ue3.py`, puis `validate_context_revision.py`. Le premier repart de la sauvegarde v1. Les fichiers actifs à intégrer sont `exams.json`, `static/`, `assets_manifest.json`, `manifest.json`, `audit.json/md` et `context_revision.json/md`.

La validation scientifique indépendante des corrigés reste hors de cette révision. Le conflit de clé déjà neutralisé et les autres réserves de source demeurent documentés.

## Identifiants et pages des blocs partagés

| Identifiant stable | QCM source | Pages source | Support |
|---|---|---|---|
| annales.ue3.2025-2026.s1.context.douleur | 4, 5 | 489 | Image |
| annales.ue3.2025-2026.s1.context.diagnostic_hfme | 6, 7, 8, 9 | 490 | Image |
| annales.ue3.2025-2026.s1.context.specificite_necker | 8, 9 | 491 | Image |
| annales.ue3.2024-2025.s1.context.fonction_renale | 4, 5 | 507 | Image |
| annales.ue3.2024-2025.s1.context.metastases | 9, 10 | 509 | Image |
| annales.ue3.2024-2025.s2.context.test_student | 2, 3 | 522 | Image |
| annales.ue3.2024-2025.s2.context.fibromes | 4, 5 | 522 | Image |
| annales.ue3.2023-2024.s1.context.evenements_cardiovasculaires | 2, 3 | 534 | Image |
| annales.ue3.2023-2024.s1.context.marqueurs_hemophilie | 7, 8 | 536 | Image |
| annales.ue3.2023-2024.s2.context.thrombectomie | 6, 7 | 551 | Image |
| annales.ue3.2022-2023.s1.context.bicarbonate | 1, 2, 3 | 560 | Image |
| annales.ue3.2022-2023.s1.context.intervalle_bicarbonate | 2, 3 | 560 | Image |
| annales.ue3.2022-2023.s1.context.narcolepsie | 4, 5 | 561 | Image |
| annales.ue3.2022-2023.s1.context.cancer_poumon | 8, 9 | 562 | Image |
| annales.ue3.2022-2023.s1.context.diagnostic_pulmonaire | 10, 11 | 563 | Image |
| annales.ue3.2022-2023.s2.context.mesures | 1, 2, 3 | 578 | Image |
| annales.ue3.2022-2023.s2.context.parkinson | 4, 5 | 579 | Image |
| annales.ue3.2022-2023.s2.context.tislezumab | 6, 7 | 580 | Image |
| annales.ue3.2021-2022.s1.context.legionellose | 6, 7 | 590 | Image |
| annales.ue3.2021-2022.s2.context.silicose_survie | 6, 7 | 605 | Image |
| annales.ue3.2020-2021.paces.context.scores_covid | 6, 7 | 615 | Image |
| annales.ue3.2020-2021.s1.context.tests_covid | 6, 7 | 636 | Image |
| annales.ue3.2020-2021.s1.context.reanimation_covid | 8, 9 | 636 | Image |
| annales.ue3.2020-2021.s2.context.albuminemie | 2, 3 | 652 | Image |
| annales.ue3.2020-2021.s2.context.valeriane | 5, 6 | 653 | Image |
| annales.ue3.2019-2020.paces.context.arthrose | 1, 2 | 662 | Image |
| annales.ue3.2019-2020.paces.context.hemoglobine | 3, 4 | 662 | Image |
| annales.ue3.2019-2020.paces.context.irm_sein | 6, 7 | 663 | Image |
| annales.ue3.2018-2019.paces.context.scores_saps_apache | 4, 5 | 685 | Texte + image |
| annales.ue3.2018-2019.paces.context.ebola | 6, 7 | 685 | Image |
| annales.ue3.2018-2019.paces.context.omega3 | 8, 9 | 686 | Image |
| annales.ue3.2024-2025.s1.context.lesions_colorectales | 6, 7, 8 | 508 | Texte |
| annales.ue3.2024-2025.s1.context.comparaison_reference_q6 | 6, 8 | 508 | Texte |
| annales.ue3.2023-2024.s1.context.etude_avc | 9, 10 | 537 | Image |
| annales.ue3.2022-2023.s2.context.moyenne_ecart_type | 2, 3 | 578 | Texte |
| annales.ue3.2021-2022.s1.context.anxiete_covid | 8, 9, 10 | 591 | Texte |
| annales.ue3.2021-2022.s2.context.silicose_definition | 4, 5, 6, 7 | 605 | Texte |
| annales.ue3.2019-2020.paces.context.adenocarcinomes_colon | 8, 9 | 664 | Texte |
| annales.ue3.2018-2019.paces.context.intervalle_apache | 2, 3 | 684 | Image |
