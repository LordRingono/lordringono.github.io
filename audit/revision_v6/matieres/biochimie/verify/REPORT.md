# Biochimie — contre-vérification indépendante V6

## Décision

**Feu vert pour intégrer les versions complètes `approved_reviewed.json` et `approved_crops.json` de ce dossier**, avec les limites documentaires explicites ci-dessous. Ce feu vert porte sur la comparaison des importations aux documents fournis, la conservation de la notation officielle, les remarques scientifiques sourcées et les locateurs des captures. Il ne signifie pas que les contradictions internes du tutorat ont disparu ni qu’une ronéo absente a été contrôlée.

| Livrable approuvé | SHA-256 |
|---|---|
| `approved_reviewed.json` | `b581cfba8c6f4fc5f7ba9963e606ec9d9345f71b57776c7efb64111531efe840` |
| `approved_crops.json` | `3f54e5bae6065b72dec153eef1e7e0001bf27137aee2755385adb8cea4e5e693` |

Entrées contrôlées : `prepare/reviewed.json` (`2c181a3972b064f7f6c076d8ba779b5fdac7d130dc75faa3bf8be257b0465d09`) et `prepare/crops.json` (`e1329d2d2e80955f55fede329cb720ccb2204a3093658cf0cb3681e45fcc4ffe`). Le PDF source de 1 660 pages porte l’empreinte `f4bd0582c8d110fe22561066a89ad5ecf458207cd212765ce007e6d41e9273ec`.

## Périmètre réellement comparé

- **70 banques, 278 QCM, 1 390 propositions et leurs détails**, lus systématiquement après une extraction indépendante de la couche texte et de la géométrie du PDF original.
- **14 séries**, réparties entre 2018 et 2025 : 2018 (24), 2019 (24), 2020 PACES (24), 2020 S1 (22), 2020 S2 (13), 2021 S1 (22), 2021 S2 (13), 2022 S1 (22), 2022 S2 (14), 2023 S1 (24), 2023 S2 (14), 2024 S1 (24), 2024 S2 (14), 2025 S1 (24).
- **273 QCM notés et cinq hors note**, conformément à la base. Aucune clé officielle, aucun poids, aucun ID, aucune clé de stockage et aucun ordre des propositions modifiés par le vérificateur.
- **1 389 verdicts VRAI/FAUX explicites** dans les détails. Pour 2020 S1 Q20 D, le document dit seulement « Plus au programme » ; la grille officielle AE est distinguée de cette absence de verdict détaillé.
- **13 contextes partagés** contrôlés. Les schémas répétés dans le PDF des Q32–34 de 2025 S1 et Q28–29 de 2024 S1 sont bien présents dans chaque capture concernée ; aucun panneau supplémentaire de contexte n’y est nécessaire.

Chaque item dispose d’une entrée dans `coverage.json` : texte source, répétition dans le corrigé, détail, verdict littéral, association aux lettres du site, clé et pages. `independent_source.json` conserve les lignes brutes, boîtes et spans extraits du PDF. Les 14 fichiers de `readings/` ont tous été lus. Les 127 différences normalisées détectées ont été examinées : elles comprennent notamment les formules rendues en images, les réparations mathématiques du préparateur et quelques limites du découpage automatique, et ne correspondent pas à 127 erreurs du site.

## Deux réparations supplémentaires

1. **2019 Q25 B, lipides** : restitution de « C. » à la fin de « phospholipase C. ». Dans le sujet p. 406, cette lettre est rejetée sur la ligne suivante ; la répétition du sujet dans le corrigé p. 429 confirme la lecture. La clé A est inchangée.
2. **2022 S2 Q20, glucides** : élargissement du bord droit de la capture de la grille p. 222, de 274,35 à 280 points. Le cadrage initial coupait le bord droit du E de la clé AE. La nouvelle capture a été rendue puis vue ; elle reproduit le numéro et les deux lettres complets.

Les 25 réparations mathématiques et de détails réalisées par le préparateur ont été confrontées aux documents. Les clés n’ont pas été déduites d’une intuition scientifique.

## Contradictions officielles conservées et signalées

| Série / QCM | Grille | En-tête du détail | Décision |
|---|---|---|---|
| 2022 S1 Q25 | BCD | ADE | Hors note conservé |
| 2022 S1 Q38 | AB | BC | Hors note conservé |
| 2021 S1 Q34 | ADE | AD | Hors note conservé |
| 2021 S1 Q36 | ACD | AC | Hors note conservé |
| 2020 S1 Q18 | ABD | ABCD | Hors note conservé ; les verdicts item par item donnent ABD |

La répétition du sujet dans certains corrigés redémarre incorrectement les lettres : 2023 S1 Q27 (A, A, B, C, D), 2021 S1 Q29 (A, B, A, B, C) et 2021 S1 Q37 (A, A, B, C, D). L’association par contenu et ordre au sujet A–E est correcte ; les notes du préparateur sont conservées.

Les fausses alertes de découpage ont été résolues : marqueurs B–E avec tirets en 2020 S2 Q16 ; mentions « HORS PROGRAMME » accolées à la clé de 2020 PACES Q30 et 2019 Q33 ; lettres des tableaux de pKa entrelacées avec les propositions de 2020 PACES Q32 et 2018 Q33. Les vraies clés détaillées des deux derniers sont AE et AC, constatées sur les pages rendues.

## Notes scientifiques et documentaires

**Les 78 notes du lot préparateur sont conservées**, dont les 35 notes antérieures. **Seize notes supplémentaires** portent le total à 94 ; un nombre de notes ne constitue pas un nombre de QCM faux.

| Point précis | QCM concernés | Fondement consulté et formulation retenue |
|---|---|---|
| Épimères et anomères | 2020 PACES Q24 E | Définitions IUPAC et ronéo glucides 2 p. 1 : différence de convention terminologique explicitée, clé conservée |
| Fructose furanose/pyranose | 2020 S2 Q19 E | Étude primaire RMN du fructose libre aqueux et ronéo glucides 2 p. 2 ; distinction avec les formes liées, pas d’extrapolation chiffrée à l’être humain |
| Site catalytique | 2023 S1 Q29 C | Corrigé original 2021 S1 Q23 C, p. 261 : site catalytique compris dans le site actif ; « proche » est imprécis |
| Allostérie et oligomérie | 2024 S2 Q17 C ; 2023 S2 Q17 C ; 2022 S2 Q15 C ; 2018 Q34 C | Étude primaire RMN de la glucokinase monomérique : le modèle oligomérique du cours n’est pas une loi universelle |
| Cholestérol et fluidité | 2021 S1 Q30 B ; 2019 Q25 C | Étude expérimentale POPC/cholestérol et ronéo isopréniques p. 5 : effet dépendant du contexte membranaire, simplification du cours reconnue |
| Barrière hémato-encéphalique | 2018 Q36 A ; 2020 S1 Q35 C | Étude primaire MFSD2A/DHA : transport de DHA sous forme de lysophosphatidylcholine ; ne transforme pas les acides gras en principal combustible cérébral du jeûne |
| Bilan ATP du palmitate | 2023 S2 Q26 E ; 2022 S1 Q38 E ; 2020 S1 Q39 E | Références P/O mitochondriaux ; calcul de 106 ATP explicitement conditionnel aux coefficients 2,5/1,5 et au coût d’activation de deux équivalents ATP |
| Détail original inachevé | 2025 S1 Q33 D | P. 36 puis p. 37 : aucune suite à « La sphingomyélinase hydrolyse » |
| pKa illisible et verdict absent | 2020 S1 Q20 B/C/D | Le « ç » est imprimé dans le document, pas inventé par l’OCR ; 9 suggéré par les autres données mais pas substitué. D indique seulement « Plus au programme » |

Toutes ces remarques sont dans `reviewNotes`, réservées à l’affichage de correction. Elles citent le document ou la source primaire pertinente et invitent à vérifier la ronéo. Les affirmations non suffisamment étayées n’ont pas été transformées en réserves nouvelles. La fausse alerte sur le complexe II de 2019 Q40 C a été écartée après grossissement du PDF ; le corrigé imprimé dit bien complexe II.

Les six ronéos disponibles sur glucides et lipides ont été mobilisées : **28 pages ciblées lues** par OCR frais ou rendu visuel, dont huit vues individuellement en image (glucides 2 p. 1, 2 et 19 ; isopréniques p. 5 ; lipides complexes p. 9 et 16 ; lipides simples p. 2 et 3). Les sources scientifiques ciblées sont référencées dans les notes, pas utilisées pour réécrire les clés officielles.

## Captures, figures et absence de réponses avant validation

- **296 panneaux sujet, 641 panneaux correction**, dont 278 lignes de grille : **937 rectangles** vérifiés sur les dimensions et les lignes de texte du PDF. Après la réparation de grille, aucune alerte de ligne partiellement coupée ne subsiste selon ce contrôle géométrique. Ce contrôle ne prétend pas détecter à lui seul toute particularité d’une image raster.
- **177 assets interactifs actuels** confrontés aux rendus frais des régions sources : 174 existants et trois nouveaux originaux PACES. Les 174 existants ont été vus en planches de contact ; les trois nouveaux l’ont été individuellement à leur résolution de sortie. Le cas d’antialiasing d’une formule, 2021 S1 Q24 A, a été inspecté à taille réelle et dans le PDF : aucun caractère perdu.
- Les trois nouveaux assets PACES sont **identiques pixel pour pixel** aux rendus correspondants. Ils remplacent les anciens masquages et conservent les annotations authentiques.
- **20 pages pertinentes de la compilation ont été vues individuellement** pour lever les doutes de structure, tableau, partage d’énoncé, annotation ou formule : 13, 14, 36, 37, 53, 180, 222, 240, 243, 303, 304, 306, 362, 363, 364, 388, 389, 406, 475, 476. Deux pages supplémentaires regardées lors du repérage ne sont pas comptées dans ces 20 pages de biochimie.
- Les **937 captures finales ne sont pas revendiquées comme ayant toutes été ouvertes individuellement à pleine taille**. La comparaison documentaire est exhaustive ; le contrôle visuel des captures individuelles est ciblé et le contrôle des assets interactifs est systématique en aperçu.

Répartition des sujets : 273 QCM avec copie propre provenant du sujet, un QCM (2020 S1 Q30) avec sujet propre et figure non annotée reprise de la répétition dans le corrigé, et quatre QCM (2020 PACES Q19, Q21, Q22, Q24) dont l’original porte des annotations. Pour ces quatre, `subjectAfterCorrection` protège la copie ; `imagesAfterCorrection` protège les figures de Q19/Q24 et le contexte partagé de Q21/Q22. Les champs de données ont été vérifiés dans `gating_check.json`. Le responsable de l’intégration doit conserver cette protection pour `stemImages` et `sharedContexts`, puis vérifier le comportement de l’interface.

## Limites et pièces à demander

`missing.json` distingue précisément les manques :

- Une version **sans annotations manuscrites** de 2020 PACES Q19, Q21, Q22 et Q24 permettrait de rendre leurs figures à nouveau visibles avant correction. Aucune suppression artificielle de réponses n’est retenue.
- Les ronéos complètes **protéines/acides aminés, enzymes et métabolisme** ne sont pas disponibles dans ce lot. Les sujets et corrigés correspondants ont été comparés intégralement ; une certification scientifique indépendante de chacune des 1 390 propositions n’est pas revendiquée.
- La suite éventuelle du détail 2025 S1 Q33 D, l’erratum du pKa 2020 S1 Q20 et le statut attendu de son item D restent à demander au tutorat ou à vérifier dans la ronéo.
- Les cinq divergences de clés ci-dessus nécessitent un erratum officiel pour sortir les QCM du statut hors note.

Aucun sujet ni corrigé complet n’est absent pour les 278 QCM du lot. La présence des 14 séries a été contrôlée dans les documents fournis ; cela ne prouve pas l’exhaustivité de toutes les sessions historiques, notamment d’éventuelles séries 2015–2017 non fournies dans ce périmètre.

## Fichiers de contrôle

- `coverage.json` : une entrée pour chacun des 278 QCM et des 1 390 items.
- `issues.json` : deux réparations du vérificateur, cinq contradictions de clés, seize nouvelles notes.
- `missing.json` : limites et documents nécessaires.
- `validation.json` : invariants, comptes et empreintes.
- `crop_validation.json`, `asset_validation.json`, `gating_check.json` : contrôles de géométrie, authenticité et protection des originaux annotés.
- `independent_source.json`, `readings/`, `comparison_flags.json` : preuves de la relecture indépendante.

**Feu vert final : le lot peut être intégré avec ces deux JSON complets approuvés et les trois assets authentiques du manifeste préparateur. Aucun changement du barème ni du stockage n’est requis.**

## Références exactes des notes ajoutées

Les références sont également embarquées dans chaque note après correction. Les documents de cours ci-dessous ont été lus aux pages indiquées ; les liens externes correspondent aux définitions officielles ou études originales consultées pour les réserves ciblées.

| Notes | Référence exacte |
|---|---|
| Anomérie/épimérie | [IUPAC Gold Book — Anomers](https://goldbook.iupac.org/terms/view/A00373) ; [IUPAC Gold Book — Epimers](https://goldbook.iupac.org/terms/view/E02167) ; ronéo glucides 2, p. 1 |
| Fructose aqueux | [Barclay et al., 2011 — Observation of the keto tautomer of D-fructose in D₂O using ¹H NMR spectroscopy](https://pmc.ncbi.nlm.nih.gov/articles/PMC3254704/) ; ronéo glucides 2, p. 2 |
| Allostérie monomérique, quatre notes | [Larion et al., 2012 — Order–disorder transitions govern kinetic cooperativity and allostery of monomeric human glucokinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC3525530/) |
| Cholestérol, deux notes | [Étude expérimentale POPC/cholestérol, 2003 — PubMed 12582817](https://pubmed.ncbi.nlm.nih.gov/12582817/) ; ronéo dérivés isopréniques, p. 5 |
| Transport cérébral, deux notes | [Nguyen et al., 2014 — Mfsd2a is a transporter for the essential omega-3 fatty acid docosahexaenoic acid](https://www.nature.com/articles/nature13241) |
| Conventions ATP/P/O, trois notes | [Lee et al., 1996 — PubMed 8641569](https://pubmed.ncbi.nlm.nih.gov/8641569/) ; le calcul conditionnel 106 résulte de 7 × (2,5 + 1,5) + 8 × 10 − 2 |
| Site catalytique | Compilation p. 140, 2023 S1 Q29 C, comparée à p. 261, 2021 S1 Q23 C |
| Phrase inachevée | Compilation p. 36–37, 2025 S1 Q33 D |
| pKa / Plus au programme | Compilation p. 303 et 318, 2020 S1 Q20, avec la ligne AE de sa grille |

Les résultats de RMN sur le fructose en solution aqueuse ne sont pas présentés comme une mesure in vivo. L’étude MFSD2A démontre un transport sous forme de lysophosphatidylcholine et n’est pas présentée comme un passage indistinct de tous les acides gras. Le bilan 106 ATP est un calcul sous conventions explicites, et non une valeur universelle mesurée. Ces limites sont reprises dans les notes destinées à l’élève.
