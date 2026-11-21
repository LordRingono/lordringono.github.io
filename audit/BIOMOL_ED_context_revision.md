# Révision ciblée des ED de biologie moléculaire

## Périmètre livré

Trois banques existantes, **126 QCM et 630 propositions**, sont révisées :

| Banque | QCM | Blocs communs |
|---|---:|---:|
| `ue2.ed.2025-2026` | 43 | 10 |
| `ue2.ed.2026-2027` | 40 | 12 |
| `ue2.ed.annales` | 43 | 15 |

Le livrable principal est `overrides.json`. Les objets conservent les identifiants des banques, leurs clés de stockage, les identifiants locaux des questions, leurs numéros source, les poids et les autres métadonnées de classement. Seules quatre clés font l’objet des exceptions de transcription autorisées et documentées ci-dessous. Toutes les autres clés sont identiques à la base. Aucune autre banque n’a été modifiée ; UE1, UE5 et les autres cours de biomol restent hors du périmètre.

Cette intervention corrige les banques préexistantes. Elle n’ajoute aucune annale. Les quatre questions déjà présentes de 2011–2012 et de 2013–2014 sont donc conservées avec leurs identifiants ; aucun nouveau QCM antérieur à 2015 n’a été importé.

## Structure des énoncés et des figures

Les données nécessaires à plusieurs questions ont été retirées des fins d’items E, puis rattachées à chaque membre du groupe par `sharedContexts`. Chaque bloc est identique pour tous ses membres et possède un identifiant stable, les identifiants locaux explicites `questionIds`, les numéros d’origine `questionNumbers`, le PDF et la page source. Le moteur commun peut ainsi l’afficher avant la première question visible, y compris si un filtre masque les premières questions du groupe.

Les blocs ne contiennent aucun item A–E et aucun extrait de corrigé. Les données déjà fournies par l’énoncé — repères de SNP, codon souligné, variant, séquence ou figure de patient — sont préservées. Les contextes révélés seulement plus tard dans le sujet restent limités aux questions qui suivent : par exemple, la notation c.164C>T de l’ED 2025–2026 commence au Q34, après les questions d’identification des bases Q32–33.

Les principales corrections sont les suivantes :

- ED 2025–2026 : introduction KCNH2, début du gène, exon 15, données de la patiente, bases substituées, nom de la variation, exon 2 et protocole de PCR reconstitués. Les limites des items E des Q14, Q20, Q29, Q33, Q36, Q39 et Q43 sont nettoyées. Le Q28 avait aussi absorbé la séquence de l’option B dans l’option A ; les deux options sont rétablies depuis le sujet.
- ED 2026–2027 : introduction MYBPC3, séquences de début et de fin, ARNt, données des patients A/B/C et figures 3/4/5 rattachés aux groupes appropriés. Les fins des Q14, Q18, Q22, Q24, Q26, Q29, Q30, Q36 et Q40 sont séparées du contexte suivant. Le fragment de référence Q42–43 de 2025 et le fragment d’ADN Q2–3 de 2021–2022 sont aussi présents lorsque seul le dernier QCM est visible.
- Annales ED : chaque exercice annuel/session est indépendant. Les séquences MYL3, KCNE1 et PLN auparavant attachées à la dernière question de l’exercice précédent sont replacées. Les numéros répétés de QCM ne servent plus seuls à associer la correction.
- Le QCM 24 scanné de 2013–2014 est utilisable : consigne en texte, figure commune Q24–26 séparée et cinq images d’options contenant chacune sa séquence. L’extrait original complet demeure consultable dans ce QCM uniquement.
- Les graines de miARN en gras sont conservées dans les images d’options : Q28/Q29 de 2025, Q19/Q20 de 2026 et Q3 de 2020–2021 S1 (local 24). La séquence du miR-124 de 2015–2016 conserve aussi sa graine en gras.
- Les trois tableaux de code génétique sont présentés via `references`, avec leur provenance, au lieu d’être absorbés dans une option ou dans un titre.

## Réparation de quatre associations de clés

Le sujet, les cinq propositions et la correction ont été confrontés par année, numéro et texte avant d’appliquer ces réparations. Les autres 122 clés restent identiques.

| ID local annales | Exercice / numéro source | Ancienne clé | Clé source rétablie | Provenance |
|---:|---|---|---|---|
| 6 | 2014-2015 · Q2 | vide | C | Sujet p. 2 / corrigé p. 3 |
| 7 | 2014-2015 · Q3 | A | B | Sujet p. 2 / corrigé p. 3 |
| 8 | 2015-2016 · Q3 | vide | BC | Sujet p. 3 / corrigé p. 4 |
| 13 | 2016-2017 · Q4 | vide | BD | Sujet p. 4 / corrigé p. 6 |

`answer_key_repairs.json` contient l’ancienne/nouvelle valeur, l’énoncé de concordance, les fichiers, pages et rectangles des solutions. Le local 7 recevait à tort les explications du SNP de l’année suivante ; le local 8 pointait à tort vers le corrigé du microARN de 2020–2021 en page 13. Leurs explications et pages sont rétablies. Les locaux 6 et 13 avaient une clé vide malgré une clé explicite dans le corrigé.

## Corrigés et réserves de source

Les 43 corrigés des annales ont été relus et associés un à un. Les explications répétées sont dédoublonnées et débarrassées du contexte de l’exercice suivant. Chaque question dispose en plus d’un extrait `correctionImages` limité à sa propre solution. Le diagramme de l’ADN polymérase (local 29, corrigé p. 15) est inclus entièrement. Ces images ont le rôle `correction` dans le manifeste et doivent être affichées seulement après validation.

Deux incohérences internes aux documents sont conservées avec une réserve visible après correction :

1. **ED 2026–2027 Q31**, sujet p. 8, corrigé p. 6 : la clé D désigne T dans le sujet, mais le texte du corrigé mentionne un G en gras. Le sujet cite également la figure 3 alors que les séquences de comparaison sont les figures 4 et 5. La clé D est conservée.
2. **Annales 2024–2025 S1 Q2**, local 38, corrigé p. 18 : la clé annonce DE, tandis que le détail indique C et D vrais et E faux. La clé DE est conservée.

Les explications scientifiques du corrigé ne sont pas réécrites pour masquer leurs propres défauts. Les corrections de transcription avérées sont distinguées des désaccords présents dans les documents.

La rubrique source intitulée « 2019-2018 » conserve cet intitulé. Elle annonce QCM 1 à 3 mais ne fournit que QCM 1 et 2, tant dans le sujet que dans le corrigé. Aucun troisième QCM n’a été fabriqué.

## Images et traçabilité

**110 images référencées** : 67 de rôle `subject`, 43 de rôle `correction`. Parmi elles, 14 images précédentes sont réutilisées et **96 nouvelles captures** sont fournies dans `static/` (environ 4,20 Mo). Les fichiers précédents restent intacts. Les nouveaux noms commencent par `biomol_ed_revision_`.

Les captures sont issues uniquement des six PDF fournis. Aucune image scientifique n’a été générée. Les rectangles de figures ont été rendus depuis le PDF complet pour préserver les masques, les flèches vectorielles et les soulignements ; une simple extraction du bitmap pourrait perdre ces couches. Les séquences et tableaux des anciennes captures avec des fragments de texte au bord ont été recadrés sous de nouveaux noms, sans altérer le document d’origine.

`assets_manifest.json` indique pour chaque image le fichier source, la page, le rectangle, le rôle et le SHA-256. `source_map.json` décrit les noms ASCII des six copies PDF présentes dans `sources/`. Le SHA-256 de l’archive fournie est `e4c3025226d2ca0a777044b0b7cd5f369b2b6913f849f31b01ed8405d9cb44b3`.

## Relectures et vérifications

Les sujets représentent 34 pages et les corrigés 43 pages, soit 77 pages contrôlées. La première passe a comparé les 126 titres et leurs propositions au PDF. La deuxième a repris les contextes, les fins de page, les positions des figures et l’association des corrigés. Une relecture indépendante des deux ED récents a lu leurs 83 titres/listes d’items et inspecté 25 nouveaux extraits ainsi que trois figures réutilisées ; son rapport est dans `review/review_recent_independent.md`. Les petits fragments de ligne qu’elle signalait ont été supprimés des captures finales.

Les douze folios des annales sont des objets de texte distincts situés à x=531,1 et y=815,6. Le parseur exclut uniquement ces objets de pied de page : il ne supprime pas arbitrairement les nombres en fin d’item. Cette correction nettoie notamment les locaux 7, 9, 13, 16, 18, 20, 23, 28, 33, 38 et 43.

`check_and_export.py` vérifie : 126 questions / 630 options A–E ; conservation des identifiants et sauvegardes ; exceptions de clés limitées aux quatre autorisées ; identité des 37 contextes entre leurs membres ; provenance sujet de toutes les images visibles avant correction ; existence de tous les fichiers et concordance des empreintes ; absence de texte de correction coupé dans les captures ; absence d’image non référencée. Le résultat **PASS** est consigné dans `validation.json`.

## Registre des groupes

Les identifiants ci-dessous sont les identifiants locaux stables de la banque, pas les numéros source répétés d’une année à l’autre.

| Banque | Bloc commun | IDs locaux | Page du sujet |
|---|---|---|---:|
| ue2.ed.2025-2026 | Le syndrome du QT long et le gène KCNH2 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43 | 1 |
| ue2.ed.2025-2026 | Début du gène KCNH2 | 15, 16, 17, 18, 19, 20 | 5 |
| ue2.ed.2025-2026 | Fin du gène KCNH2 | 21, 22, 23, 24, 25, 26, 27, 28, 29 | 7 |
| ue2.ed.2025-2026 | Étude d’une patiente | 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43 | 9 |
| ue2.ed.2025-2026 | La substitution nucléotidique | 32, 33, 34, 35 | 9 |
| ue2.ed.2025-2026 | La variation c.164C>T | 34, 35, 36, 37, 38, 39, 40, 41, 42, 43 | 9 |
| ue2.ed.2025-2026 | La mutation dans l’exon 2 | 37, 38, 39, 40, 41, 42, 43 | 10 |
| ue2.ed.2025-2026 | Amplification de l’exon 2 | 40, 41, 42, 43 | 11 |
| ue2.ed.2025-2026 | Le deuxième oligonucléotide | 41, 42, 43 | 11 |
| ue2.ed.2025-2026 | Hypothèse des QCM 42 et 43 | 42, 43 | 11 |
| ue2.ed.2026-2027 | La cardiomyopathie hypertrophique et le gène MYBPC3 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40 | 1 |
| ue2.ed.2026-2027 | Début du gène MYBPC3 | 15, 16, 17, 18 | 4 |
| ue2.ed.2026-2027 | Séquence de l’exon 1 | 15, 16, 17, 18 | 4 |
| ue2.ed.2026-2027 | Fin du gène MYBPC3 | 19, 20, 21, 22, 23, 24 | 5 |
| ue2.ed.2026-2027 | L’ARNt | 23, 24 | 6 |
| ue2.ed.2026-2027 | Patiente A | 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36 | 7 |
| ue2.ed.2026-2027 | Substitution nucléotidique de la patiente A | 27, 28, 29 | 7 |
| ue2.ed.2026-2027 | Séquençage de la patiente A — figure 3 | 30, 31, 32, 33, 34, 35, 36 | 8 |
| ue2.ed.2026-2027 | Localisation de la variation — figures 4 et 5 | 31, 32, 33, 34, 35, 36 | 8 |
| ue2.ed.2026-2027 | Patients B et C — l’exon 2 | 37, 38, 39, 40 | 10 |
| ue2.ed.2026-2027 | Séquençage du patient B | 37, 38 | 10 |
| ue2.ed.2026-2027 | Variation du patient C | 39, 40 | 10 |
| ue2.ed.annales | 2013–2014 — Exon 1 et intron 1 | 2, 3, 4 | 1 |
| ue2.ed.annales | 2014–2015 — Exon 40 | 5, 6, 7 | 2 |
| ue2.ed.annales | 2015–2016 — SNP du gène ITGB3 | 8, 9 | 3 |
| ue2.ed.annales | 2016–2017 — Exon 4 du gène TNNI3 | 10, 11, 12, 13 | 4 |
| ue2.ed.annales | 2017–2018 — Gène KCNE1 | 14, 15, 16 | 5 |
| ue2.ed.annales | 2018–2019 — Gène MYL3 | 17, 18, 19 | 6 |
| ue2.ed.annales | Annale « 2019–2018 » — Gène à 7 exons | 20, 21 | 7 |
| ue2.ed.annales | 2020–2021, session 1 — Canal potassique | 22, 23, 24 | 8 |
| ue2.ed.annales | 2020–2021, session 2 — Exon 34 | 25, 26 | 9 |
| ue2.ed.annales | 2021–2022 — Exon 4 du gène TNNI3 | 27, 28, 29 | 9 |
| ue2.ed.annales | Le fragment d’ADN des QCM 2 et 3 | 28, 29 | 9 |
| ue2.ed.annales | 2022–2023 — Gène TNNT2 | 30, 31, 32 | 10 |
| ue2.ed.annales | 2023–2024 — Exon 34 du gène MYBPC3 | 33, 34, 35, 36 | 10 |
| ue2.ed.annales | 2024–2025, session 1 — Gène PLN | 37, 38, 39, 40 | 11 |
| ue2.ed.annales | 2024–2025, session 2 — Gène TNNC1 | 41, 42, 43 | 12 |

## Fichiers à intégrer

- `overrides.json` : trois objets complets à substituer aux trois banques ED.
- `static/` : uniquement les 96 nouveaux fichiers WebP ; les 14 images réutilisées sont déjà dans le site.
- `sources/` : six PDF sous noms ASCII.
- `assets_manifest.json`, `answer_key_repairs.json`, `context_revision.json`, `validation.json` et ce rapport : audit et traçabilité.

Le code de rendu et les tests d’interface relèvent de l’intégration du parent ; cette livraison ne modifie aucun fichier principal du site.
