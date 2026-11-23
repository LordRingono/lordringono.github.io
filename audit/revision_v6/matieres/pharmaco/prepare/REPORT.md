# Pharmacologie V6 — rapport du préparateur

**État : lot terminé et prêt pour la vérification indépendante.** Le préparateur ne s’est pas attribué de validation indépendante. Aucun fichier de `output/site` n’a été modifié.

## Base et périmètre

La base utilisée est exclusivement `work/site_v6/baseline_exams.json` (V5). Les 15 banques thématiques de `roster.json` comprennent 336 QCM, soit 1 680 propositions. Les 14 séries représentées couvrent 2018–2019 à 2025–2026. Aucun ajout, retrait, changement de thème, d’ID, de `sourceId`, de progression historique ou de clé de notation n’a été effectué. Les profils et le code du site n’ont pas été touchés.

Le recueil original `output/site/sources/Annales_compilation.pdf` a été consulté directement ; les pages 699–986 ont fait l’objet d’une nouvelle extraction paginée et positionnée. Les anciens manifestes n’ont servi que de localisateurs. Les deux documents de cours UE4 fournis, Droit Pharma (10 pages) et cycle de vie du médicament / Le Borgne (9 pages), ont aussi été consultés ; leurs figures utiles ont été rendues.

## Couverture effectivement réalisée

| Contrôle | Résultat |
|---|---:|
| Sujets comparés, consigne et propositions | 336 / 336 |
| Propositions sujet comparées | 1 680 / 1 680 |
| Textes identiques après normalisation prudente | 1 663 |
| Propositions exclusivement graphiques A–E vérifiées visuellement | 15 |
| Artefacts de couche texte résolus par le rendu | 2 |
| Blocs de corrigé retrouvés | 335 / 336 |
| Reprises textuelles des items dans les corrigés | 1 635 |
| Reprises graphiques des items dans les corrigés | 15 |
| Détails individuels A–E effectivement imprimés et comparés | 1 625 |
| Détails transcrits conformes | 1 620 |
| Détails remplacés en V5 par une réserve documentée, conservée | 5 |
| Items sans détail individuel imprimé | 55 |
| QCM avec une clé littérale non ambiguë | 329 |
| QCM avec clé explicitement hésitante « (C)E » | 1 |
| QCM « Hors programme » sans clé | 5 |
| QCM sans corrigé ni clé associable | 1 |
| QCM notés conservés | 325, dont 1 avec aucune réponse vraie |
| QCM hors note conservés | 11 |
| Grilles courtes inspectées visuellement | 14 / 14 |
| Figures interactives inspectées visuellement | 13 / 13 |
| Sujets ayant eu une lecture visuelle individuelle complète | 31 |
| Corrigés de ces QCM ayant eu une lecture visuelle individuelle | 30, le dernier étant absent |

**Limite de visualisation :** les autres 305 sujets et leurs corrigés ont reçu une comparaison documentaire des textes et un contrôle géométrique des limites, pas une lecture visuelle individuelle que l’on annoncerait comme faite. `coverage_preparer.json` liste les QCM réellement vus. Toutes les 14 grilles ont été vues, et leurs 335 cases pertinentes ont été associées à la bonne série/numérotation.

Les 55 items sans détail individuel se répartissent entre 5 items du corrigé absent, 25 items des cinq questions hors programme, 20 items de quatre QCM QSAR avec un raisonnement général, et 5 items du Q14 de 2019–2020 qui ne fournit que la clé B. Un verdict issu seulement de la grille est distingué d’un verdict explicite dans une justification.

## Réparations et décisions

### Citations obsolètes dans les notes

Vingt renvois de dix-neuf notes pointaient vers Q1/Q2 par confusion avec les préfixes de Q10–Q29. Les bons liens vers les questions complètes étaient déjà présents. Les renvois sans rapport ont été supprimés après consultation des passages originaux ; le texte des 179 notes, leur `noteId` et les clés sont conservés. Le détail avant/après figure dans `changes.json` et les candidats documentés dans `citation_candidates.json`.

### Q13 BPF/BPP de 2021–2022 S1

Le sujet p843 contient 25 questions, mais le corrigé comporte 24 questions. La grille p848 donne A à son n°13, qui correspond aux cinq propositions du sujet Q14 (absorption), reprises p853–854. Il ne s’agit pas de la correction du sujet Q13. Une recherche de la phrase distinctive BPF/BPP dans les 1 660 pages du recueil n’a retrouvé que le sujet p843 (`searches.json`).

La ligne de `crops.json` comporte donc `correction:[]` et `correctionMissing` avec la raison précise. Aucun panneau de grille ne lui a été attribué. Les anciens pointeurs `correctionPage` et `shortCorrectionPage` vers p848 sont mis à `null` dans `reviewed.json`, pour ne pas maintenir un lien générique ambigu. La référence p848 reste possible dans la note qui démontre l’omission. Le QCM demeure hors note. Pour les sujets Q14–Q25, la correspondance au corrigé n°13–n°24 est explicite dans les notes des copies.

### Lettres du corrigé 2023–2024 S1 Q24

Le sujet p773 utilise A–E. Sa reprise dans le corrigé p786 est imprimée F–J, mais la clé AC et les justifications sont A–E. L’ordre et le texte des cinq propositions établissent F→A, G→B, H→C, I→D, J→E. Les lettres originales sont conservées dans les preuves et expliquées dans `correctionNote` ; les options du sujet ne sont pas renumérotées.

### Copie annotée 2019–2020 Q4

Le sujet p941 comporte un ajout manuscrit près des descripteurs QSAR. Son interprétation n’est pas certaine. La copie complète est conservée sans retouche et porte `subjectAfterCorrection:true`, avec une explication. La figure interactive existante ne montre que le tableau des molécules ; elle reste complète et n’expose pas cet ajout.

**Point d’intégration :** vérifier que l’ancien champ `originalImages` de ce QCM ne reste pas accessible avant validation par une autre commande de l’interface. La protection du nouveau menu doit s’appliquer à la copie complète ; il n’y a pas lieu de masquer l’image interactive actuelle.

### Textes, contextes et schémas

Les deux anomalies de couche texte du sujet 2022–2023 S2 Q14 (« bdistribution », « è50% ») ne sont pas visibles dans le rendu, qui montre bien « distribution » et « 50% ». La transcription V5 est exacte et reste inchangée. Les cinq justifications déjà remplacées par « La justification imprimée ne correspond pas à cet item » restent accompagnées des réserves V5 ; leur texte original complet est conservé dans `audit.json` et dans les copies authentiques.

Le contexte commun de l’oxyde de zinc est isolé de Q12 et ajouté à Q13/Q14 dans les deux rôles. Le tableau et les calculs QSAR de 2020–2021 S1 Q9 sont traités comme explication générale, sans les mélanger à E. Les treize figures interactives ont été confrontées à leurs originaux : lettres, légendes, structures, tableaux et valeurs sont présents. Aucune retouche de pixels n’a été faite.

## Copies originales

Les 336 entrées de `crops.json` proposent 338 panneaux sujet : un sujet par QCM et deux panneaux supplémentaires pour le contexte commun. Elles proposent 731 panneaux de correction pour 335 QCM, incluant les parties sur plusieurs pages, le contexte partagé et la case authentique de la grille courte de la même série. Les copies de correction doivent rester accessibles seulement après validation.

Les cadrages prennent toute la largeur PDF lorsqu’il le faut : certains schémas atteignent les bords des pages 708/709/878. Les limites verticales sont établies à partir des en-têtes, des lignes, des images et des cadres vectoriels ; elles n’incluent pas la question suivante. Le corrigé comprend ses figures, même lorsqu’une figure se trouve sur la page précédente et la justification sur la suivante.

Aucun PDF Word n’a été converti pour ce lot. Aucun nouveau schéma interactif n’est nécessaire. `source_manifest.json` et `asset_manifest.json` sont donc des listes vides : le PDF est déjà présent dans `sources/Annales_compilation.pdf`.

## Pièces ou arbitrages encore manquants

Les onze cas suivants restent hors note ; le détail par question et les recherches sont dans `missing.json`.

| Question | Document ou arbitrage nécessaire |
|---|---|
| 2021-2022 · S1 · q13 | Corrigé officiel ou erratum du sujet UE4 S1 2021–2022 Q13 (BPF/BPP), avec verdicts A–E. |
| 2020-2021 · S2 · q10 | Erratum officiel du verdict de B : grille et clé BDE, détail B FAUX. |
| 2020-2021 · PACES · q05 | Une correction authentique avec clé A–E de 2020-2021 PACES Q5, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme ». |
| 2020-2021 · PACES · q13 | Erratum des valeurs d’activité ou des équations QSAR ; le corrigé affirme qu’aucune réponse n’est exacte et retient A comme approximation. |
| 2020-2021 · PACES · q25 | Version lisible ou erratum officiel de l’item D (unité imprimée « Vig » au sujet ; « mg » dans le corrigé). |
| 2020-2021 · PACES · q29 | Confirmation du professeur/erratum de l’item C et clé définitive ; le corrigé imprime « (C)E » et « FAUX ? ». |
| 2019-2020 · S1 · q10 | Une correction authentique avec clé A–E de 2019-2020 S1 Q10, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme ». |
| 2019-2020 · S1 · q12 | Une correction authentique avec clé A–E de 2019-2020 S1 Q12, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme ». |
| 2019-2020 · S1 · q13 | Une correction authentique avec clé A–E de 2019-2020 S1 Q13, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme ». |
| 2019-2020 · S1 · q19 | Erratum explicite de l’item A (« adsorption » au sujet ; « absorption » dans le corrigé). |
| 2019-2020 · S1 · q30 | Une correction authentique avec clé A–E de 2019-2020 S1 Q30, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme ». |

La copie non annotée de 2019–2020 Q4 serait utile uniquement pour rendre le sujet intégral consultable avant validation. Les notes scientifiques non résolues sont répertoriées séparément dans `missing.json` : l’absence d’une ronéo spécialisée ne signifie pas que le sujet ou son corrigé est absent. Aucun désaccord scientifique n’a été utilisé pour inventer une nouvelle clé officielle.

## Fichiers remis et contrôle final

- `reviewed.json` : les 336 objets complets, sous leurs 15 banques V5.
- `audit.json` : une entrée par QCM, cinq entrées par item, textes bruts, verdicts, grille, positions PDF, limites et statut visuel.
- `crops.json` : 336 entrées avec rectangles PDF exacts et notes de rôle.
- `missing.json` : onze demandes documentaires/errata bloquant la notation, détails non imprimés, copie annotée et réserves scientifiques.
- `REPORT.md` : présent rapport.
- `changes.json`, `coverage_preparer.json`, `inventory.json`, `documentary_differences.json`, `searches.json` : preuves et récapitulatifs de préparation.
- `prepared_sha256.json` : empreintes des livrables figés pour le vérificateur.

Les contrôles structurels ont vérifié 336 IDs uniques, 1 680 items, les champs de progression historiques, les années/sessions, les ordres, les clés, l’unique QCM « AUCUNE » et tous les rectangles dans les limites des pages. Aucun test de l’interface n’est revendiqué : il appartient à l’intégration par l’agent principal.

**Feu vert du préparateur : lot complet, figé et transmissible au vérificateur indépendant.** Les limites ci-dessus restent à conserver dans la validation et dans le bilan final.
