# Audit UE3 — Biostatistiques

14 sujets, 138 QCM inclus ; 137 notés et 1 conservé hors note.

## Périmètre

Pages 487 à 698 du dossier compilé. Années 2018–2019 à 2025–2026 ; aucun QCM antérieur à 2015 dans ce périmètre. Les sujets restent complets, regroupés dans le cours « Annales complètes de biostatistiques » avec une catégorie thématique pour chaque QCM. Aucun contenu existant UE1, UE5 ou UE2 n’a été édité.

## Inventaire exhaustif

| Année | Session | Pages sujet | Pages corrigé | QCM | Notés |
|---|---|---|---|---:|---:|
| 2025-2026 | S1 | 488–492 | 494–504 | 12 | 12 |
| 2024-2025 | S1 | 506–510 | 512–520 | 12 | 12 |
| 2024-2025 | S2 | 522–524 | 526–532 | 7 | 7 |
| 2023-2024 | S1 | 534–538 | 540–548 | 12 | 12 |
| 2023-2024 | S2 | 550–552 | 554–558 | 7 | 7 |
| 2022-2023 | S1 | 560–564 | 566–576 | 12 | 11 |
| 2022-2023 | S2 | 578–580 | 582–586 | 7 | 7 |
| 2021-2022 | S1 | 588–592 | 594–602 | 11 | 11 |
| 2021-2022 | S2 | 604–606 | 608–612 | 7 | 7 |
| 2020-2021 | PACES | 614–622 | 624–632 | 11 | 11 |
| 2020-2021 | S1 | 634–638 | 640–650 | 11 | 11 |
| 2020-2021 | S2 | 652–654 | 656–660 | 7 | 7 |
| 2019-2020 | PACES | 662–670 | 672–682 | 11 | 11 |
| 2018-2019 | PACES | 684–688 | 690–698 | 11 | 11 |

Le manifeste JSON donne, pour chacun des 138 QCM, les pages, numéros, clés courte et détaillée, mode de rendu, contexte repris et décision d’inclusion. Aucune question n’a été supprimée. Seules les couvertures et trois pages sujet vides ne sont pas affichées.

## Relectures et corrections techniques

1. **Inventaire sujet par sujet** — 14 sujets et 14 corrigés identifiés ; 138 numéros d’origine, dont 3 réponses numériques codées.
2. **Énoncés et dépendances** — Les 14 sujets sont relus : 39 blocs partagés explicites, consignes locales séparées, données de pages précédentes et aides de calcul conservées. La consigne d’intervalle demandée en 2018 Q2 est rétablie pour Q3.
3. **Clés de correction** — 138 comparaisons : grille courte = clé détaillée ; un conflit additionnel entre clé et verdicts VRAI/FAUX neutralisé hors note.
4. **Images et mathématiques** — Les 16 panneaux A–E regroupés sont remplacés par 80 captures distinctes, une par proposition, relues visuellement. Formules, exposants, tableaux codés et figures sont conservés.
5. **Contrôle anti-fuite** — 68 pages de sujets examinées en planches, cas graphiques/mathématiques sensibles agrandis. Aucune annotation de correction repérée. Toutes les images visibles avant correction appartiennent à des pages sujet.
6. **Structure et références** — IDs, clés de correction et stockages inchangés par rapport à v1 ; cinq options par question ; objets sharedContexts identiques entre leurs membres ; références et provenances validées.

## Anomalies du document source

- **2022–2023, session 1, Q5** (sujet p561 ; détail p570) : grille courte et clé détaillée BCE, mais les verdicts et justifications détaillées donnent ACE. Question conservée **hors note**, `answer:""`, `rawAnswer:"BCE"`, `detailedVerdictAnswer:"ACE"`. Aucune clé de remplacement inventée.
- **2023–2024, session 1, Q6–8** : la consigne sur une p-valeur et une réponse unique semble recopiée du Q5, alors que les propositions et la correction portent sur d’autres thèmes et plusieurs réponses. Texte et clé originaux conservés avec avertissement après correction.
- **2020–2021, session 1, Q7, item E** (p636) : phrase incomplète dans le sujet (« population du personnel COVID-19 est de 10 % »). Elle n’a pas été complétée par supposition ; avertissement présent.

- **2019–2020, PACES, Q2** (détail p674) : la justification écrit F ≤ 0,82 à la place de F > 0,82 pour la seconde queue. Le calcul à deux queues et la clé ABCD (0,62) correspondent à la demande du sujet. La clé est conservée, avec avertissement.

## Cas particuliers et contrat de rendu

- `sharedContexts` contient les blocs communs, avec identifiant stable, texte ou images, numéros des questions concernées et pages source. Le moteur les affiche une seule fois avant le premier membre visible, y compris après filtrage.
- `stemImages` conserve uniquement les données et figures locales à la question ainsi que les trois tableaux de réponses numériques codées. Les anciens panneaux A–E sont supprimés de ce champ : chaque item concerné possède sa propre `option.image`, avec un texte vide pour éviter les fragments mathématiques déformés.
- Les Q2 et Q4 de PACES 2019–2020 et le Q2 de PACES 2018–2019 utilisent un tableau de codes : l’utilisateur coche les lettres associées à la valeur numérique choisie. Les trois tableaux originaux sont visibles avant réponse.
- `sourceContext` sert à la recherche et à l’audit. Son contenu est visible dans `sharedContexts` ou `stemImages` ; ne pas l’afficher en doublon.
- `correctionImages` doit rester caché jusqu’à la correction. Les explications mathématiques renvoient à ces extraits exacts.
- `originalImages` contient le QCM d’origine complet en contrôle secondaire, sans correction.
- `referenceImages` contient les tables et formulaire propres à PACES 2019–2020 (p667–670) et PACES 2020–2021 (p619–622). Pour les autres sujets, seules les trois tables statistiques p667–669 sont proposées, avec `referenceTitle` et `referenceNote` indiquant explicitement leur provenance ; le formulaire n’est pas ajouté.
- `assets_manifest.json` trace chaque image (page, rectangle source, rôle, dimensions, empreinte et utilisations). Les images des sujets et des corrections sont distinctes.

## Résultat des contrôles automatiques

492 images WebP utilisées, 18.44 Mo. 138/138 clés concordent entre grilles courtes et clés détaillées ; 137 questions sont automatiquement notées. Aucun asset manquant ni référence de corrigé dans les champs d’énoncé. Identifiants et clés de sauvegarde propres aux nouvelles banques. Les rendus temporaires inutilisés ont été retirés.

## Limite de la vérification

Cette intégration vérifie la fidélité des énoncés et l’accord des sources ; elle ne constitue pas une nouvelle validation scientifique indépendante des 138 corrigés.
