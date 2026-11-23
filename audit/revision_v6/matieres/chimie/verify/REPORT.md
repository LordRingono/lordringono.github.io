# Chimie UE2c — vérification indépendante V6

## Décision finale

**FEU VERT pour l’intégration des versions complètes `approved_reviewed.json` et `approved_crops.json`.**

Vérificateur : `/root/chimie_verifie`, distinct du préparateur `/root`.

La vérification porte sur **86 QCM et leurs 430 propositions**, répartis dans **38 banques et 14 séries**. Toutes les questions présentes ont été comparées aux sujets et aux corrigés originaux. Les clés, détails textuels, formules, figures, contextes communs et limites de question ont été examinés. Les anomalies scientifiques de la source sont signalées après correction, sans remplacer sa clé par une réponse déduite.

| Fichier à intégrer | SHA-256 approuvé |
|---|---|
| `approved_reviewed.json` | `511f535441e70ec7a99dcaca5e75ee8aaba9e0c6fb500b3a38ddcd338591b1f2` |
| `approved_crops.json` | `57624752bf5c6e07a00777b30baa779ef7101944d9abe818aed947f6962e626d` |

Les préparations ont été conservées intactes : `reviewed.json` de SHA `f2027d139a34660c33b47600660ab9169d2c6efeaa4d75905fa3b0c60dc60a78` et `crops.json` de SHA `57624752bf5c6e07a00777b30baa779ef7101944d9abe818aed947f6962e626d`. Aucun fichier de `output/site` n’a été modifié par le vérificateur.

## Couverture exhaustive

| Série dans le site | QCM comparés | Propositions comparées |
|---|---:|---:|
| 2025s1 | 7 | 35 |
| 2024s1 | 7 | 35 |
| 2024s2 | 4 | 20 |
| 2023s1 | 7 | 35 |
| 2023s2 | 4 | 20 |
| 2022s1 | 6 | 30 |
| 2022s2 | 4 | 20 |
| 2021s1 | 6 | 30 |
| 2021s2 | 4 | 20 |
| 2020s1 | 6 | 30 |
| 2020s2 | 4 | 20 |
| 2020paces | 8 | 40 |
| 2019 | 9 | 45 |
| 2018 | 10 | 50 |
| **Total** | **86** | **430** |

`coverage.json` contient une entrée pour chaque QCM et chaque item, avec texte source, texte corrigé source, option finale, verdict de la grille, verdict détaillé, verdict utilisé pour la note, état du détail, références des pages et commentaires scientifiques associés. `independent_source.json` conserve l’extraction fraîche des zones consultées, avec lignes, positions et spans. Les fichiers `readings/` contiennent les lectures de chaque série. Ils ont servi à lire systématiquement le contenu, pas à approuver automatiquement les réponses à partir d’un simple rapprochement de chaînes.

Les 14 grilles de correction courte ont été relues directement dans le PDF : pages 20, 60, 94, 126, 160, 190, 222, 250, 286, 310, 340, 372, 416 et 460. Les 86 clés ainsi lues correspondent aux relevés du préparateur. **85 QCM sont notés ; un seul reste hors note.**

### Conflit de clé maintenu hors note

En 2018, la question du moment dipolaire est imprimée **Q50 dans le sujet** et **Q49 dans le corrigé**. La grille donne A, tandis que le détail donne C et 1,9 D. Les pages 458, 460 et 484 ont été confrontées. La clé du site reste vide sans `answerIsEmpty`, et l’avertissement explicite est conservé. Aucun verdict scientifique déduit n’est présenté comme un erratum officiel.

## Contrôle des originaux et des captures

- **86 copies sujet propres**, aucun sujet absent, aucun sujet annoté avec une réponse identifié dans cette matière.
- **86 copies de correction**, aucune absente.
- **205 panneaux contrôlés** : 89 pour les sujets, 116 pour les corrigés.
- Toutes les coordonnées sont à l’intérieur de la page source. Les limites de question et les figures/contextes nécessaires ont été rapprochés des originaux. L’unique autre numéro détecté dans une copie sujet est le préambule « les deux questions » de Q40, légitimement repris pour Q41 en 2021s1 ; aucun item de Q40 n’est inclus dans ce panneau commun.
- Les 31 pages sujet ont toutes été rendues et vues : 16–18, 57–58, 90–91, 112–113, 157–158, 186–187, 219, 246–247, 283, 307–308, 337–338, 368–370, 411–414 et 456–458.
- **23 pages de corrigés détaillés ont été vues en image**, ainsi que la grille p. 460 : 80, 81, 108, 127, 130, 172, 173, 211, 233, 272, 274, 298, 328, 355, 395, 396, 439, 441, 443, 480, 482, 483, 484. Le texte de tous les corrigés des 86 QCM a été lu. Ce rapport ne prétend pas que chaque panneau de corrigé a été individuellement visionné en image.

Les vérifications particulières confirment la présence du contexte des Q27/Q28 de 2024s2, du contexte commun Q40/Q41 de 2021s1 et de la figure complète des sept structures pour Q42/Q43 de 2020 PACES. La hauteur de cette dernière atteint le bas réel du schéma ; elle ne s’arrête pas avant les structures inférieures. Les blocs « hors programme » des questions suivantes ne sont pas intégrés aux items précédents. Les décalages de numérotation 2018 sont explicités dans les captures.

### Images interactives déjà présentes

Les **372 assets uniques** ont été décodés, leurs SHA contrôlés et leurs pixels comparés à un nouveau rendu du PDF de leur zone d’origine. Leurs affectations aux QCM et aux lettres d’items ont aussi été rapprochées des coordonnées et du texte du PDF. Les écarts observés sont compatibles avec la compression et l’arrondi du rendu ; quatre images présentent un pixel d’écart de dimension. Les résultats détaillés sont dans `assets_verified.json`.

Les 31 pages source complètes ont été vues. **Cinq miniatures ont en plus été ouvertes individuellement** : les items Mg et Si p. 219, un item de thermodynamique p. 187, le produit énamine p. 413 et la figure commune p. 368. Les 367 autres ont eu un contrôle de correspondance au raster et de géométrie, pas une visualisation individuelle. Les champs actifs `stemImages`, `originalImages`, images d’options et contextes communs sont couverts. Le builder a été lu pour vérifier que les anciens panneaux de correction ne sont pas dupliqués lorsque les nouvelles copies existent ; le contrôle fonctionnel de l’ensemble assemblé revient au responsable d’intégration.

## Réparations et réserves

Les **20 réparations de détails** du préparateur sont validées. Elles portent notamment sur les fractions, indices, exposants et les repères erronés A/B/A/B/C du corrigé atomistique 2021s2 Q27, réassociés par contenu.

Le vérificateur a réparé **deux transcriptions supplémentaires** en atomistique 2020s1 Q43 : le fragment Z² avait été rattaché au détail A, alors qu’il constitue le numérateur de Z²/n² dans la formule du détail B. A retrouve son seul renvoi au schéma ; B contient la formule complète avec son signe négatif. La source p. 328 a été relue visuellement.

Les **30 notes scientifiques existantes sont conservées intégralement**. **Dix notes supplémentaires**, sourcées et limitées à la correction, ont été ajoutées :

| Série / QCM du corrigé | Item(s) | Point signalé |
|---|---|---|
| 2020s1 Q43 | D | Configuration du phosphore imprimée avec 13 électrons au lieu de 15 ; possible omission de 2s², non corrigée silencieusement. |
| 2023s2 Q29 | D | L’ionisation de F⁸⁺ à n=9 utilise E₉ ; le mot « fondamental » du détail est incorrect. |
| 2024s1 Q47 | B | Aldéhyde nommé « cétone » dans la justification aldolique. |
| 2024s2 Q27 | C | Structure 1 sans C* : les deux groupes éthyle sont identiques. Le verdict faux reste cohérent, le comptage du détail ne l’est pas. |
| 2021s1 Q44 | D | Cr fondamental : 5 électrons de m=−1 dans le modèle utilisé ; le caractère demi-plein de d permet le décompte. |
| 2022s2 Q27 | D | Ordre Cu/Ni contraire aux valeurs de Pauling de la RSC ; échelle ou approximation du cours à préciser. |
| 2018 Q46 | D | Dans la convention d’axe z, pz correspond à m=0 ; l’argument du corrigé sur m=−1 est litigieux. |
| 2018 Q45 | A, B | Le caractère tertiaire ne suffit pas à imposer SN1 en présence d’alcoolates ; concurrence E2 et conditions à préciser. |
| 2019 Q47 | C | « Hyperconjugaison » et réseau π conjugué : vocabulaire à clarifier dans le cours. |
| 2019 Q47 | E | Le carbone sp³ reconnu dans B contredit l’argument « tous les carbones sont sp² » de E ; sens de la planéité à préciser. |

Ces observations distinguent erreur certaine du détail, ambiguïté des conditions et convention pédagogique. **Aucune clé, option, ID, ordre, poids ni sauvegarde n’a été modifié.** Les références consultées sont la ronéo fournie d’atomistique et les publications de l’IUPAC, de la Royal Society of Chemistry, d’OpenStax et du MIT. Les URLs et points vérifiés figurent dans `external_sources_consulted.json` et dans les notes affichées.

Deux fausses alertes provisoires sont explicitement écartées dans `issues.json` : Mg possède bien 6 électrons s, et le grossissement du corrigé biochimie p. 439 montre bien « complexe II ». Aucun commentaire erroné ni modification hors chimie n’a été publié pour ces alertes.

## Détails présents et limites documentaires

Les 430 items disposent d’une source de correction exploitable, sous réserve du conflit officiel A/C déjà indiqué. **371 ont un détail textuel**, **34 ne comportent qu’un verdict textuel bref**, et **25 relèvent d’une correction globale ou graphique originale**, sans détail séparé A–E à inventer. Ces 25 cas concernent cinq QCM (calculs thermodynamiques, Lewis et moment dipolaire), dont le QCM hors note ; leurs copies de correction donnent accès au raisonnement original.

Aucune omission supplémentaire de chimie n’a été prouvée dans les 14 séries représentées. Cette conclusion porte sur les documents disponibles et ne prouve pas l’existence de toutes les sessions historiques. Les annales 2015–2016, 2016–2017 et 2017–2018 ne sont pas présentes dans ces séries ; leur fourniture serait nécessaire pour une extension. Les ronéos de chimie organique et un erratum officiel du moment dipolaire 2018 restent utiles pour arbitrer les réserves. La liste concrète figure dans `missing.json`.

`approved.json` constitue la signature finale de ce contrôle documentaire. L’intégration doit utiliser les deux versions approuvées et maintenir l’affichage des réserves et des corrigés uniquement après correction.
