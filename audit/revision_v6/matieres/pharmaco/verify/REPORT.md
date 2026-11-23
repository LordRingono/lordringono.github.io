# Pharmacologie UE4 V6 — vérification indépendante finale

**FEU VERT FINAL pour l’intégration de `approved_reviewed.json` et `approved_crops.json`.** Les deux fichiers sont complets. Le bilan approuvé est de **336 QCM, 1 680 propositions, 15 thèmes, 14 séries, 324 QCM notés et 12 hors note**. Les limites documentaires sont explicites et ne sont pas présentées comme des corrections acquises. Aucun fichier de `output/site` ou d’une autre matière n’a été modifié par le vérificateur.

## 1. Décisions issues de la vérification

### Q15 de 2018–2019 S1 : nouvelle mise hors note

La lecture directe des images du sujet p967 et du corrigé p979 confirme que D et E portent exactement **« Un extrait brut peut être actif »**, sans différence de ponctuation ni de négation. Le corrigé donne D VRAI, E FAUX et la clé BCD ; la grille p972 confirme BCD. Le détail de E, « B, C, et D sont vrais », ne répond pas à la proposition imprimée. La note antérieure `ue4-v4-022` décrit déjà cette contradiction correctement.

Une notation cohérente n’est donc pas possible sans erratum. La version approuvée conserve les deux propositions, les explications et `rawAnswer:"BCD"`, mais passe `answer` à `""`, **sans `answerIsEmpty:true`**. Un avertissement concis renvoie à la réserve après validation. Aucune clé de remplacement n’a été inventée. Ce changement a été explicitement approuvé par l’agent principal après le signalement indépendant. Les preuves sont dans `changes.json`, `coverage.json` et la planche `visual/ue4_2018-2019_S1_q15_special.png`.

### Q13 BPF/BPP de 2021–2022 S1 : absence confirmée

Le sujet comporte 25 QCM, le corrigé 24. Le Q13 BPF/BPP p843 n’a pas de corrigé associable. Le numéro 13 de la grille p848 et du corrigé p853–854 correspond aux cinq propositions du **Q14 du sujet**, relatives à l’absorption. L’identité de tous les items permet de suivre le décalage de −1 jusqu’au Q25 du sujet. La recherche indépendante de la phrase distinctive BPF/BPP dans les 1 660 pages retrouve seulement p843 (`source_searches.json`, `independent_inventory.json`, `independent_comparison.json`).

Les pointeurs `correctionPage` et `shortCorrectionPage` à `null`, `correction:[]` et le statut hors note du préparateur sont approuvés. Aucun panneau de grille n’est attribué à ce QCM. Une dernière ambiguïté de présentation a été corrigée : le libellé de la référence p848 dans `ue4-v4-045` indique désormais qu’il s’agit de la **preuve d’absence de clé pour le Q13 du sujet**, et non de son corrigé. Le texte de la note et son URL n’ont pas changé.

## 2. Travail réellement effectué

La comparaison a été reconstruite directement depuis `output/site/sources/Annales_compilation.pdf`, sans reprendre les segments ou verdicts du script préparateur. La nouvelle extraction conserve les coordonnées des lignes. Elle retrouve les 28 couvertures sujet/correction, les limites de questions, les cinq propositions, les clés littérales et tous les détails présents. Les numéros imprimés, les changements de page et les figures ont servi à vérifier les associations (`independent_extract.py`, `independent_compare.py`, `independent_pages.json`, `independent_segments.json`).

Une recherche supplémentaire porte sur **les 1 660 pages du recueil**, et les deux inventaires `documents_available.json` et `additional_documents.json` ont été consultés. Les deux cours UE4 disponibles, Droit Pharma et cycle de vie du médicament / Le Borgne, ont été relus pour les passages cités ; leurs 19 pages ont été extraites et 11 pages utiles examinées en image (`independent_courses.json`, `visual_manifest.json`). Il s’agit d’un rapprochement avec les documents fournis, sans prétendre certifier l’état actuel du droit ou de la science.

| Contrôle indépendant | Résultat |
|---|---:|
| QCM / consignes rapprochés | 336 / 336 |
| Propositions du sujet rapprochées | 1 680 / 1 680 |
| Propositions textuelles conformes après normalisation prudente | 1 663 |
| Propositions graphiques A–E vérifiées dans les images | 15 |
| Artefacts de couche texte résolus par le rendu | 2 |
| Blocs de corrigé disponibles et associés | 335 / 336 |
| Détails individuels imprimés et comparés | 1 625 |
| Détails transcrits conformes | 1 620 |
| Détails remplacés antérieurement par une réserve documentée | 5 |
| Items sans détail individuel imprimé ou sans corrigé | 55 |
| Clés littérales non ambiguës retrouvées | 329 |
| Clé explicitement hésitante `(C)E` | 1 |
| QCM « Hors programme » sans clé exploitable | 5 |
| QCM sans corrigé associable | 1 |
| QCM notés après vérification | 324 |
| QCM hors note après vérification | 12 |
| QCM noté dont toutes les propositions sont fausses | 1 |
| Panneaux sujet / correction | 338 / 731 |
| Figures interactives examinées visuellement | 13 / 13 |
| Grilles courtes examinées visuellement | 14 / 14 |
| Sujets lus individuellement en image | 30 |
| Corrigés lus individuellement en image | 29 |
| Notes scientifiques antérieures préservées | 179 |
| Références de ces notes contrôlées | 282 |

**Limite visuelle :** les 306 autres sujets et leurs 306 corrigés ont fait l’objet du rapprochement documentaire et du contrôle géométrique complet, pas d’une lecture individuelle en image que ce rapport prétendrait avoir effectuée. Les 30 sujets et 29 corrigés réellement lus en image sont identifiés par QCM dans `coverage.json` et dans `visual_manifest.json`. Toutes les grilles et toutes les figures interactives ont été regardées.

Les 55 items sans détail individuel se répartissent en 5 pour le corrigé absent, 25 pour les cinq questions hors programme, 20 pour quatre QCM QSAR à raisonnement général et 5 pour le Q14 de 2019–2020, qui ne fournit que la clé B. Le statut de chaque item distingue le verdict fourni par la clé, le détail explicitement imprimé, le raisonnement général et l’absence de source. Les 1 680 traces sont présentes dans `coverage.json`.

## 3. Couverture des séries et absence d’omissions

Les limites ci-dessous ont été détectées depuis les couvertures et les questions du recueil. Les numéros du sujet sont tous représentés dans les banques ; aucune question manquante dans une série existante n’a été trouvée (`independent_inventory.json`, `source_searches.json`, rubrique `series` de `coverage.json`).

| Année | Session | Pages du corps du sujet | Pages du corps du corrigé | QCM sujet / corrigé |
|---|---|---:|---:|---:|
| 2025–2026 | S1 | 702–710 | 713–726 | 28 / 28 |
| 2024–2025 | S1 | 728–734 | 737–750 | 28 / 28 |
| 2024–2025 | S2 | 752–756 | 759–766 | 15 / 15 |
| 2023–2024 | S1 | 768–774 | 777–788 | 28 / 28 |
| 2023–2024 | S2 | 790–792 | 795–800 | 15 / 15 |
| 2022–2023 | S1 | 802–808 | 811–822 | 25 / 25 |
| 2022–2023 | S2 | 824–828 | 831–838 | 18 / 18 |
| 2021–2022 | S1 | 840–846 | 849–858 | 25 / 24 |
| 2021–2022 | S2 | 860–864 | 867–874 | 19 / 19 |
| 2020–2021 | S1 | 876–882 | 885–896 | 25 / 25 |
| 2020–2021 | S2 | 898–902 | 905–914 | 20 / 20 |
| 2020–2021 | PACES | 916–922 | 925–938 | 30 / 30 |
| 2019–2020 | S1 | 940–948 | 951–962 | 30 / 30 |
| 2018–2019 | S1 | 964–970 | 973–986 | 30 / 30 |

Aucune autre série UE4 à partir de 2015 n’a été trouvée dans les documents inventoriés. Les années 2015–2018 ne sont donc pas annoncées comme relues : aucune série UE4 correspondante n’est disponible. Aucun contenu antérieur à 2015 n’a été ajouté.

## 4. Cadrages, contextes et figures

Le contrôle indépendant des **1 069 rectangles** a vérifié les limites des pages, la présence de toutes les lignes attendues, les boîtes des images incluses, l’absence de question voisine et le rôle sujet/correction. Les 335 cases de grille associables portent les bons numéros et les bonnes sessions. `geometry_flags.json` est vide ; `geometry_coverage.json` conserve le détail par rôle. Les 59 anciens `correctionPage` qui pointent vers une page de clé/détail après le début du bloc restent valides : les panneaux incluent aussi les pages précédentes nécessaires.

Les points sensibles sont confirmés :

- **Q27/Q28 2025–2026 et Q9 2020–2021 S1** : les figures atteignant les parties latérales des pages 708, 709 et 878 sont prises sur toute la largeur nécessaire. Les molécules, labels, descripteurs, valeurs et légendes sont présents.
- **Q13/Q14 2020–2021 S1** : le contexte partagé sur l’insolubilité de l’oxyde de zinc est rattaché aux deux QCM dans les deux rôles (sujet p879, corrigé p890), sans être inclus dans l’item E du Q12.
- **Q24 2023–2024 S1** : les options A–E du sujet p773 correspondent exactement, dans l’ordre, à F–J dans la reprise p786. La clé et les détails sont A–E. La correspondance F→A, G→B, H→C, I→D, J→E est documentée dans les copies et la couverture.
- **Q14 2022–2023 S2** : « bdistribution » et « è50% » sont des artefacts de couche texte ; les images montrent « distribution » et « 50% ». La transcription existante est correcte.
- **Q9 2020–2021 S1** : le tableau des descripteurs et les trois calculs suivant E sont correctement transcrits dans l’explication générale ; ils ne sont pas une continuation de la justification individuelle de E.
- **Q4 2019–2020** : le sujet p941 comporte une annotation manuscrite près des descripteurs. La copie complète reste authentique, sans effacement, avec `subjectAfterCorrection:true`. La figure interactive ne contient que le tableau complet des molécules et ne divulgue pas cette annotation.

Les 688 occurrences de fichiers graphiques des champs existants ont aussi été inventoriées : existence, dimensions, empreinte et identité du QCM (`existing_graphics.json`). Ce contrôle d’inventaire n’est pas présenté comme une visualisation des 688 fichiers. Les 13 figures interactives ont été comparées visuellement à leurs sources. Aucun nouvel actif graphique ni aucune retouche n’est nécessaire ; `asset_manifest.json` est vide.

**Consigne d’intégration à respecter :** les copies originales V6 doivent utiliser les panneaux approuvés. Pour 2019–2020 Q4, le verrou après validation doit couvrir toutes les voies montrant la copie complète, y compris les anciens `originalImages`. La figure interactive propre reste accessible. Les copies de correction et les notes scientifiques restent après validation.

## 5. Remarques scientifiques et références

Les **179 textes et `noteId`** ont été confrontés à la base immuable V5 et restent inchangés. Les réserves ont été relues avec leurs passages sources ; les clés officielles sont conservées même lorsqu’une remarque invite à vérifier un point dans la ronéo. Les cours disponibles ne permettent pas de trancher toutes les controverses, ce que les notes indiquent. La vérification ne transforme pas une intuition scientifique en clé officielle.

Les **20 renvois supprimés dans 19 notes** par le préparateur étaient bien des associations de préfixes : Q1 ou Q2 à la place de Q10–Q29. Les bonnes références aux numéros complets sont conservées. Le contrôle indépendant retrouve 259 références ordinaires au bon bloc d’annale, une référence à la grille comme preuve d’omission et 22 références aux cours fournis, soit 282 au total (`notes_verification.json`). Le seul changement supplémentaire de référence est le libellé explicite de la preuve d’omission BPF/BPP décrit plus haut.

Les passages de cours vérifiés comprennent notamment la nomination des commissaires européens, le caractère réglementaire du texte de déontologie, les compétences ANSM/ANSES/EMA, les nuances du générique (Droit Pharma p4–8), les distinctions pharmacodynamie/ADMET, la durée/publication du brevet, les familles d’AINS et la biostéréoconversion (Le Borgne p2–4, 6–8). Leurs formulations sont traitées comme celles des documents fournis et non comme une mise à jour réglementaire ou médicale.

Les 95 signaux produits par la comparaison brute sont tous expliqués dans `comparison_adjudication.json` : 59 pointeurs internes à des blocs sur plusieurs pages, 24 différences imprimées sujet/corrigé, 7 différences de détail liées à des réserves ou séparations de contexte, 3 différences de couche texte/contextes, 1 consigne présente dans une image et 1 ordre littéral de lettres `ABDCE` équivalent à `ABCDE`. Aucun de ces signaux ne reste un défaut d’import non traité.

## 6. Pièces encore nécessaires pour lever les limites

`missing.json` donne les questions, items, pages, recherches et documents précis. Les douze QCM suivants restent hors note :

| QCM | Pièce ou clarification nécessaire |
|---|---|
| 2021–2022 S1 Q13 | Corrigé BPF/BPP absent, avec les cinq verdicts |
| 2020–2021 S2 Q10 | Erratum de B : clé/grille BDE mais détail B FAUX |
| 2020–2021 PACES Q5 | Clé authentique, le recueil portant seulement « Hors programme » |
| 2020–2021 PACES Q13 | Erratum des valeurs ou équations QSAR ; le corrigé reconnaît qu’aucune réponse n’est exacte |
| 2020–2021 PACES Q25 | Erratum/lisible de l’unité D : « Vig » dans le sujet, « mg » dans le corrigé |
| 2020–2021 PACES Q29 | Décision définitive sur C et la clé hésitante `(C)E` |
| 2019–2020 S1 Q10, Q12, Q13, Q30 | Clés authentiques des quatre mentions « Hors programme » |
| 2019–2020 S1 Q19 | Erratum de A : « adsorption » au sujet, « absorption » au corrigé |
| 2018–2019 S1 Q15 | Erratum de D/E identiques avec verdicts opposés |

Un original complet non annoté de 2019–2020 Q4 permettrait, s’il existe, de montrer sa copie avant validation. Il n’est pas requis pour utiliser la figure interactive propre et le QCM actuel. Les ronéos spécifiques non fournies restent demandables pour les réserves scientifiques déjà recensées ; leur absence n’autorise pas à remplacer les clés du tutorat.

## 7. Fichiers approuvés et traçabilité

Les versions approuvées sont des objets complets, pas des patches. Les 336 IDs, `sourceId`, options et leur ordre, thèmes, années/sessions, poids et données `legacyProgress` ont été comparés à V5 et préservés. Les deux profils et le code du site n’ont pas été touchés. Les différences complètes contre V5 sont listées dans `issues.json`.

| Fichier | SHA256 |
|---|---|
| `approved_reviewed.json` | `d603c3287fd1068bc7c2caa49ad5599ad25b677c2606889305a52b9b0e95323d` |
| `approved_crops.json` | `af9448c6fbd4a2542d986fee59f66bf1964de84cb45749ca06504b1637c6d9b6` |
| `coverage.json` | `243abaddc6e2aad1fce9032e5e65a56a71014179fcc3cbbc43f294dee4e390d7` |
| `issues.json` | `5d46e130d1a9cead93258f652aae8a81d9e330a943ebb8d9df06bc5b5fbf918f` |
| `missing.json` | `079515d2a78cd8ef3700d925b689e714a274284904d2bacaa11b21ed9885bff4` |

Empreinte du recueil indépendamment consulté : `f4bd0582c8d110fe22561066a89ad5ecf458207cd212765ce007e6d41e9273ec`. Empreintes des entrées préparateur : `reviewed.json` = `b5b8b16db16e90a1ef6dbddcec67aeb991d03d93821213d50f3a21b502b4c6f3` ; `crops.json` = `af9448c6fbd4a2542d986fee59f66bf1964de84cb45749ca06504b1637c6d9b6`.

`approved.json` contient le feu vert explicite, les chemins absolus, les empreintes, les comptes et les instructions d’intégration. La vérification documentaire est terminée ; les contrôles de rendu final, du verrou des copies et de la notation/progression dans l’interface relèvent de l’intégration par l’agent principal.
