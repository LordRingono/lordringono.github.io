# Préparation V6 — Biochimie

**Lot prêt pour le vérificateur indépendant. Ce rapport est celui du préparateur ; il ne constitue pas l’approbation du second agent.**

## Périmètre effectivement relu

Les **70 banques, 278 QCM et 1 390 propositions** de la biochimie V5 ont été rapprochés des sujets et corrigés de la compilation fournie. Le périmètre comprend les acides aminés et protéines, l’enzymologie, les lipides, les glucides et le métabolisme. Les 14 séries présentes ont été lues une par une ; les identifiants, les banques, leurs clés de stockage, les poids et les clés de notation préexistantes sont conservés. Aucun QCM n’a été ajouté ou retiré.

| Série interne | QCM comparés | Propositions |
|---|---:|---:|
| 2025s1 | 24 | 120 |
| 2024s1 | 24 | 120 |
| 2024s2 | 14 | 70 |
| 2023s1 | 24 | 120 |
| 2023s2 | 14 | 70 |
| 2022s1 | 22 | 110 |
| 2022s2 | 14 | 70 |
| 2021s1 | 22 | 110 |
| 2021s2 | 13 | 65 |
| 2020s1 | 22 | 110 |
| 2020s2 | 13 | 65 |
| 2020paces | 24 | 120 |
| 2019 | 24 | 120 |
| 2018 | 24 | 120 |
| **Total** | **278** | **1 390** |

Ce contrôle n’établit pas que toutes les sessions existantes depuis 2015 ont été fournies. Il n’a pas mis en évidence de question biochimique omise dans les séries représentées. Le numéro 13 de 2023s2, notamment, relève de la biologie moléculaire et ne constitue pas un trou dans la biochimie. Aucune nouvelle série non représentée n’a été importée et aucun QCM antérieur à 2015 n’a été ajouté.

## Méthode et preuves

1. Nouvelle extraction du texte et de sa géométrie depuis `Annales_compilation.pdf`, les anciens index n’étant utilisés que comme localisateurs. Lecture des consignes, de chaque item du sujet, de la répétition corrigée, de la clé détaillée, de chaque détail et de la ligne correspondante de la grille.
2. Seconde passe sur les différences de versions, les fractions, les exposants, les labels recommencés, les tableaux latéraux, les débordements de page et les contextes communs. Les 13 groupes d’énoncés communs de la matière sont conservés et inclus dans les copies nécessaires ; l’énoncé du Q34 de 2018 est également repris depuis le bloc qui le précède dans le corrigé.
3. Consultation visuelle des **81 pages de sujets** et des **14 pages de grilles**. Contrôle documentaire et géométrique des **177 assets interactifs uniques**, avec comparaison à un rendu neuf de leurs rectangles PDF et examen rapproché des cas litigieux. Lecture de tous les corrigés en texte, puis visualisation ciblée de leurs pages ou détails pour les formules, structures, erreurs de lettres et anomalies. Cette méthode ne doit pas être présentée comme la visualisation individuelle à pleine taille de chaque capture finale.
4. Consultation des six ronéos biochimiques disponibles : glucides 1, glucides 2, AG2, lipides simples, lipides complexes et dérivés isopréniques. Leur texte OCR a été utilisé pour repérer les passages et plusieurs pages ciblées ont été examinées en image. Les autres réserves s’appuient sur les sources primaires ou bases de nomenclature citées dans chaque note et dans `scientific_sources.json`.
5. Après assemblage des rectangles, nouveau rendu et examen de cinq cas de frontière : 2021s1 Q32 (figure commune jusqu’au bas de p.243), 2020s1 Q25 (séparation très serrée entre le Q24 et l’énoncé commun), 2018 Q34 (préambule du corrigé), 2022s2 Q16 (contexte sur deux pages), 2020s1 Q30 (figure absente du sujet mais disponible dans la répétition de l’énoncé).

`audit.json` contient une entrée par QCM et par proposition : littéraux, pages, rectangles, lettres imprimées, association logique, clés et détails, réserves et réparations. Les différences de versions sont explicites. Dans les deux tableaux de pKa placés latéralement aux propositions, le texte du tableau est traité comme donnée commune, pas comme suite d’un item. Les extractions provisoires `fresh_source_audit.json` et `comparison_flags.json` sont des étapes de travail ; **l’audit final est `audit.json`**.

## Résultat documentaire

| Contrôle | Résultat |
|---|---:|
| QCM avec sujet et corrigé rapprochés | 278 |
| Propositions avec deux versions et détail localisés | 1 390 |
| Verdicts détaillés explicites VRAI / FAUX | 1 389 |
| Item dont le détail dit seulement « Plus au programme » | 1 |
| QCM avec clé exploitable et notée | 273 |
| QCM contradictoires déjà hors note, maintenus hors note | 5 |
| Copies de sujet non annotées, directement disponibles | 273 |
| Copie non annotée complétée par la figure de l’énoncé répété | 1 |
| Copies originales annotées, différées après correction | 4 |
| QCM avec copie de corrigé | 278 |

L’item sans verdict détaillé explicite est **2020s1 Q20 D**. Le corrigé porte « Plus au programme » et la grille AE ne retient pas D. La grille est conservée ; aucune justification absente du document n’est inventée.

Les cinq contradictions de clés sont :

| QCM | Grille | En-tête détaillé | Traitement |
|---|---|---|---|
| 2022s1 Q25 | BCD | ADE | Hors note conservé |
| 2022s1 Q38 | AB | BC | Hors note conservé |
| 2021s1 Q34 | ADE | AD | Hors note conservé |
| 2021s1 Q36 | ACD | AC | Hors note conservé |
| 2020s1 Q18 | ABD | ABCD | Hors note conservé ; verdicts détaillés ABD |

Leurs avertissements avant validation ne révèlent plus les lettres des réponses. La comparaison exacte des clés est désormais dans une note de correction. `answer` reste vide et `answerIsEmpty` n’est pas ajouté : il ne faut pas transformer ces cas en QCM dont toutes les propositions seraient fausses.

## Réparations et signalements

Les modifications de texte comprennent **25 détails de correction remis en forme ou réparés**, **un label C. dupliqué supprimé du texte d’un item** et **cinq avertissements de contradiction rendus non révélateurs**. `changes.json` consigne chaque avant/après et son motif. Les formules ne sont plus entrelacées avec les numérateurs et dénominateurs de l’item suivant. Les erreurs de calcul déjà imprimées dans l’original ne sont pas dissimulées : leur copie est intacte et une note distingue le résultat correct de celui qui est imprimé.

Les cas principaux sont les calculs de 2022s1 Q24, 2021s1 Q24, 2021s2 Q15, 2020paces Q30/Q32/Q35 et 2025s1 Q26. Cinq glyphes alpha issus de la fonte ont également été rétablis dans 2021s2. La légende issue du tableau des charges de 2020paces Q32 ne déborde plus en texte brut dans le détail E ; le tableau reste accessible dans le corrigé original.

Les répétitions corrigées de **2023s1 Q27, 2021s1 Q29 et 2021s1 Q37** recommencent incorrectement les lettres A/B au milieu des cinq propositions. Le rapprochement utilise le texte intégral et l’ordre du sujet, et non la lettre erronée seule. Trois notes documentaires expliquent ce cas. Une autre note signale **2020paces Q35 C**, imprimé `1 × 10⁻⁴` dans le sujet et `11 × 10⁻⁴` dans la répétition corrigée ; le site conserve le sujet et le verdict faux est compatible avec les deux versions.

Les **35 notes scientifiques antérieures sont conservées intégralement**. **34 notes scientifiques ou de convention nouvelles** ont été ajoutées, avec renvoi précis à une ronéo fournie ou à une source primaire consultée et invitation à revoir le point dans la ronéo. Elles concernent notamment la citrullination des protéines, le caractère non sulfaté de l’acide hyaluronique, le rôle des régions basiques des facteurs bZIP, la classification des sialyltransférases, la localisation cytosolique de la glycolyse, les cétoses épimères, les β-glucosidases humaines, les réactions de la pyruvate déshydrogénase, le NADPH et le glutathion, la régulation du glycogène par le glucagon, les produits d’oxydation des oses et plusieurs erreurs numériques originales. **Aucune clé officielle n’a été changée sur la base d’un désaccord scientifique.**

Un signalement reçu sur **2019 Q40 C, p.439**, a été vérifié sur un agrandissement du PDF : l’original et le site disent bien **complexe II**, pas complexe I. Le sujet propose complexe III et son verdict faux est cohérent. Reactome R-HSA-70994 confirme complexe II. Aucune fausse réserve n’est ajoutée ; la décision et la capture sont dans `decisions.json` et `visual/2019_q40_detail.png`.

## Captures et figures

`crops.json` contient **278 couples sujet/correction**, avec **296 panneaux sujet** et **641 panneaux correction**, ces derniers comprenant les 278 lignes des grilles. Le builder doit les rendre sans perte dans les menus originaux, fermés par défaut. Les contextes nécessaires sont reproduits dans chaque copie concernée même si l’interface ne les affiche qu’une fois avant le groupe.

Pour **2020s1 Q30**, la figure est absente de la page du sujet. Sa répétition non annotée dans le corrigé p.322 a été examinée et seule la figure, sans verdict ni explication, est ajoutée à la copie sujet ; sa provenance est annoncée.

Pour **2020paces Q19, Q21–22 et Q24**, les sujets p.362–364 sont eux-mêmes annotés. Les versions antérieures de trois schémas avaient des zones masquées. Trois nouveaux assets authentiques ont été rendus directement depuis le PDF sans effacer ces annotations. Les quatre questions portent `subjectAfterCorrection:true` dans les recettes ; Q19/Q24 utilisent `q.imagesAfterCorrection:true` pour leurs `stemImages`, et Q21/Q22 utilisent `sharedContexts[].imagesAfterCorrection:true`. L’agent principal a confirmé la prise en charge de ces gardes, y compris `stemImages`.

Les champs anciens `originalImages` et `correctionImages` restent dans la base pour préserver sa structure, mais les menus doivent privilégier les nouvelles `sourceCopies` générées. Les anciens extraits masqués ne doivent pas servir de solution de repli dans la version livrée. Le builder V6 prévu supprime cet affichage de repli quand les nouvelles copies existent.

## Manques à demander après intégration

- Le sujet **non annoté** de 2020paces pour les figures Q19, Q21–22 et Q24. Les répétitions des corrigés p.381, 383 et 384 ne fournissent pas de remplacement propre.
- Les ronéos **acides aminés/protéines**, **enzymologie** et **métabolisme**. Les six ronéos glucides/lipides présentes ont été utilisées ; les réserves dans les autres domaines restent confrontées aux sources primaires disponibles et doivent être rapprochées du cours local.
- Pour une couverture au-delà des séries présentes, les autres sujets/corrigés d’années ou sessions que l’utilisateur souhaite intégrer. Ce lot ne prétend pas à l’exhaustivité de toutes les sessions historiques.

`missing.json` décrit ces limites et la recherche effectuée. Il n’existe pas de sujet ou de corrigé entièrement absent pour l’un des 278 QCM du périmètre.

## Contrôles finaux et remise au vérificateur

`check_final.py` a vérifié les 70 banques, les 278 IDs, les 1 390 options, l’absence de changement de clé/poids/consigne, la conservation exacte des anciennes notes, l’existence des fichiers, les limites géométriques des 937 panneaux et les empreintes des sources/assets. Les calculs réparés ont été recalculés séparément. Les résultats sont dans `validation.json` ; ils ne remplacent pas la vérification indépendante.

Fichiers d’intégration : `reviewed.json`, `audit.json`, `crops.json`, `missing.json`, `asset_manifest.json`, `source_manifest.json`. Fichiers de traçabilité : `changes.json`, `decisions.json`, `scientific_sources.json`, `counts.json`, `validation.json`. `SHA256SUMS` porte les empreintes stables des livrables de ce lot.

Le vérificateur doit particulièrement refaire les rapprochements des fractions, les trois remappages de lettres, les cinq contradictions, les quatre sujets annotés, la variante numérique Q35 C et les contextes placés en bas de la page précédente. Les captures scientifiques et les listes de lecture fournies sont des aides à la localisation, pas une approbation transmise d’un agent à l’autre.
