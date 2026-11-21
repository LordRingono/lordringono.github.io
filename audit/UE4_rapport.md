# Audit des annales UE4 — médicaments

## Périmètre et résultat

Le PDF **Sujets + corrections compilés(1).pdf** est la seule source utilisée. Les pages 699 à 986 constituent le périmètre UE4 ; les pages 699–700 sont la couverture et le sommaire. Les 14 sujets et leurs corrections sont traités individuellement. Aucune banque existante ni aucun fichier principal du site n’a été modifié par ce traitement.

**336 QCM conservés**, répartis dans 12 matières et 154 séries matière/année/session. **324 QCM notés**, dont un QCM explicitement corrigé « AUCUNE », et **12 QCM accessibles hors note**. Les sujets vont de 2018–2019 à 2025–2026 ; aucun sujet UE4 antérieur à 2015 n’est présent dans ce périmètre. Aucun QCM de ces 14 sujets n’a été supprimé.

Les numéros de page ci-dessous sont ceux du PDF compilé, en base 1. Le numéro original du QCM reste dans `sourceNumber`, tandis que `id` est local à sa série. Les réserves et les captures du corrigé sont destinées à l’affichage après validation.

## Couverture, sujet par sujet

| Année | Session | Pages du sujet | Pages du corrigé | QCM inclus | Notés | Hors note |
|---|---|---|---|---:|---:|---:|
| 2025-2026 | S1 | 701–710 | 711–726 | 28 | 28 | 0 |
| 2024-2025 | S1 | 727–734 | 735–750 | 28 | 28 | 0 |
| 2024-2025 | S2 | 751–756 | 757–766 | 15 | 15 | 0 |
| 2023-2024 | S1 | 767–774 | 775–788 | 28 | 28 | 0 |
| 2023-2024 | S2 | 789–792 | 793–800 | 15 | 14 | 1 |
| 2022-2023 | S1 | 801–808 | 809–822 | 25 | 25 | 0 |
| 2022-2023 | S2 | 823–828 | 829–838 | 18 | 18 | 0 |
| 2021-2022 | S1 | 839–846 | 847–858 | 25 | 24 | 1 |
| 2021-2022 | S2 | 859–864 | 865–874 | 19 | 19 | 0 |
| 2020-2021 | S1 | 875–882 | 883–896 | 25 | 25 | 0 |
| 2020-2021 | S2 | 897–902 | 903–914 | 20 | 19 | 1 |
| 2020-2021 | PACES | 915–922 | 923–938 | 30 | 26 | 4 |
| 2019-2020 | S1 | 939–948 | 949–962 | 30 | 25 | 5 |
| 2018-2019 | S1 | 963–970 | 971–986 | 30 | 30 | 0 |

## Classement par matière

| Matière | QCM |
|---|---:|
| Pharmacodynamie et mécanismes d’action | 16 |
| Pharmacocinétique | 14 |
| Pharmacovigilance et iatrogénie | 18 |
| Évaluation clinique et médico-économique | 27 |
| Biotechnologies et biothérapies | 34 |
| Chimie thérapeutique et modélisation | 49 |
| Prescription et bon usage du médicament | 44 |
| Droit, réglementation et industrie pharmaceutiques | 37 |
| Molécules actives d’origine naturelle | 24 |
| Formes et préparations pharmaceutiques | 35 |
| Contrôle et qualité des médicaments | 21 |
| Identification de molécules thérapeutiques | 17 |

## Politique de notation et intégrité des sources

Clés source univoques conservées. Sans clé, clé explicitement incertaine, contradiction formelle entre clé et verdicts, ou différence matérielle entre item du sujet et item corrigé : question accessible hors note. Aucune rectification scientifique de fond par l’assistant.

La valeur littérale de la grille courte est conservée dans `rawAnswer`. Le manifeste conserve aussi `shortKey`, `detailKey` et `appliedAnswer`. La grille détaillée utilise une fois `ABDCE` pour `ABCDE` : il s’agit seulement d’un changement d’ordre des mêmes lettres. Aucune nouvelle réponse n’a été déduite pour remplacer une correction absente.

Le QCM 9 de la session 2 2022–2023 est explicitement corrigé « AUCUNE ». Il porte `answerIsEmpty: true`. Tous les nouveaux QCM portent `allowNoAnswer: true` pour permettre une réponse volontaire « aucune proposition » sans révéler lesquels ont une clé vide. Une chaîne `answer` vide sans `answerIsEmpty` reste hors note.

## QCM hors note et réserves conservées

| Référence source | Page du sujet | Page du corrigé | Traitement | Motif |
|---|---:|---:|---|---|
| ue4:2023-2024:S1:q23 | 773 | 786 | Noté avec réserve | Le tutorat qualifie l’item D d’ambigu dans sa justification. La clé ABDE fournie est conservée. |
| ue4:2023-2024:S2:q05 | 790 | 796 | Hors note | Divergence dans le corrigé fourni : la grille courte et la clé placée sous le QCM donnent ACE, mais les justifications déclarent A et B vrais, C, D et E faux. La clé source ACE reste documentée ; cette contradiction non résolue impose de conserver le QCM hors note. |
| ue4:2022-2023:S2:q14 | 826 | 836 | Noté avec réserve | Le titre du sujet mentionne les paramètres pharmacocinétiques, tandis que plusieurs items portent sur la pharmacodynamie. Le corrigé classe C vrai tout en le signalant « HP maintenant ». L’énoncé original et la clé BC sont conservés. |
| ue4:2021-2022:S1:q04 | 840 | 850 | Noté avec réserve | Le corrigé donne ACDE mais accompagne la justification de C de « VRAI ?? » et précise que ce point n’a pas été explicitement dit dans le cours. La clé source ACDE est conservée avec cette réserve. |
| ue4:2021-2022:S1:q13 | 843 | 848 | Hors note | Le sujet comporte 25 QCM, mais le corrigé en comporte 24 : cette question sur les bonnes pratiques de fabrication et de préparation est absente du corrigé. Le QCM reste accessible sans note. À partir du QCM 14 du sujet, les numéros du corrigé sont décalés de −1. |
| ue4:2020-2021:S2:q10 | 900 | 909 | Hors note | Divergence dans le corrigé fourni : la grille courte et la clé placée sous le QCM donnent BDE, mais la justification de B le classe FAUX. La clé source BDE reste documentée ; cette contradiction non résolue impose de conserver le QCM hors note. |
| ue4:2020-2021:PACES:q05 | 917 | 927 | Hors note | Le corrigé mentionne uniquement « Hors programme » et la grille courte indique « / ». Aucune clé exploitable n’est fournie : QCM conservé hors note. |
| ue4:2020-2021:PACES:q13 | 919 | 930 | Hors note | Le tutorat précise qu’aucune équation proposée n’est exactement juste et retient A parce qu’elle donne les résultats les plus proches. La clé source A reste documentée ; le QCM est conservé hors note en raison de cette erreur reconnue dans le document. |
| ue4:2020-2021:PACES:q25 | 921 | 936 | Hors note | L’item D du sujet imprimé contient « 500 Vig », tandis que le corrigé reproduit « 500 mg » et considère cet item vrai. L’unité du sujet est indéfinie. Le texte du sujet et la clé source ADE restent documentés ; le QCM est conservé hors note à cause de cette différence d’énoncé. |
| ue4:2020-2021:PACES:q29 | 922 | 937 | Hors note | La clé source est « (C)E ». Le corrigé hésite explicitement sur C (« FAUX ? ») et demande la confirmation du professeur. Aucune règle de neutralisation n’est indiquée : le QCM est conservé hors note, avec ses justifications originales. |
| ue4:2019-2020:S1:q10 | 942 | 954 | Hors note | Le corrigé mentionne « HORS PROGRAMME » et la grille courte indique « / ». Aucune clé exploitable n’est fournie : QCM conservé hors note. |
| ue4:2019-2020:S1:q12 | 943 | 955 | Hors note | Le corrigé mentionne « HORS PROGRAMME » et la grille courte indique « / ». Aucune clé exploitable n’est fournie : QCM conservé hors note. |
| ue4:2019-2020:S1:q13 | 943 | 955 | Hors note | Le corrigé mentionne « HORS PROGRAMME » et la grille courte indique « / ». Aucune clé exploitable n’est fournie : QCM conservé hors note. |
| ue4:2019-2020:S1:q19 | 944 | 957 | Hors note | L’item A du sujet est « L’adsorption », alors que le corrigé reproduit « L’absorption » et le classe vrai. Le texte du sujet et la clé source ABC restent documentés ; le QCM est conservé hors note car le corrigé ne répond pas exactement au même item. |
| ue4:2019-2020:S1:q30 | 947 | 961 | Hors note | Le corrigé mentionne « HORS PROGRAMME » et la grille courte indique « / ». Aucune clé exploitable n’est fournie : QCM conservé hors note. |

## Décalage de numérotation 2021–2022, session 1

Le sujet contient 25 QCM. Son QCM 13, consacré aux bonnes pratiques de fabrication/préparation, est absent du corrigé de 24 QCM. Les cinq propositions des questions suivantes permettent de confirmer le décalage. Le QCM 13 du sujet reste accessible hors note.

| Numéro dans le sujet | Numéro dans le corrigé |
|---:|---:|
| 1 à 12 | 1 à 12 |
| 13 | Absent |
| 14 | 13 |
| 15 | 14 |
| 16 | 15 |
| 17 | 16 |
| 18 | 17 |
| 19 | 18 |
| 20 | 19 |
| 21 | 20 |
| 22 | 21 |
| 23 | 22 |
| 24 | 23 |
| 25 | 24 |

## Schémas, consignes et protection contre les fuites de correction

Les 14 images intégrées aux pages de sujet ont été rattachées aux 13 QCM concernés. Les deux images du QCM 9 de 2020–2021, session 1, sont réunies dans un même panneau, y compris la légende très à gauche de la page. Les trois QCM à options entièrement graphiques disposent des cinq choix A–E et du schéma original complet. Tous les QCM possèdent aussi des extraits du sujet non corrigé consultables.

**Cas particulier p. 941, QCM 4 de 2019–2020 :** la photographie déjà présente dans le sujet porte des coefficients manuscrits dans sa légende. Cette zone a été écartée des images visibles avant validation. Le tableau des molécules et activités est conservé, les descripteurs sont transcrits fidèlement et les extraits originaux sont limités aux zones non annotées. Aucune structure chimique ni donnée d’activité n’a été redessinée.

Le contexte commun « Questions 13 à 14 » relatif à l’oxyde de zinc, situé après le QCM 12 de 2020–2021, session 1, est affiché avant chacun des QCM 13 et 14. Il ne fait plus partie de l’item E du QCM 12.

Deux caractères invisibles dans l’extraction textuelle du QCM 14 de 2022–2023, session 2 (`bdistribution`, `è50%`) ont été supprimés après comparaison du rendu du sujet et du corrigé. En revanche, les différences réellement imprimées « adsorption/absorption » et « 500 Vig/500 mg » ont été conservées et signalées.

Le manifeste `assets_manifest.json` donne pour chaque image son rôle, sa page, son rectangle dans le PDF, sa référence QCM, sa taille et son SHA-256. Il recense 689 images WEBP (20.7 Mio). Les rôles `subject` et `correction` ont été vérifiés contre les plages de pages des 14 paires sujet/corrigé.

## Relectures et vérifications réalisées

- Inventaire des couvertures, bornes de chaque sujet et de chaque correction, numérotation exhaustive.
- Comparaison des cinq propositions sujet/corrigé lorsque la correction reproduit le sujet ; contrôle des écarts et de la numérotation.
- Concordance des clés des grilles courtes et du corrigé détaillé ; comparaison des VRAI/FAUX avec les clés ; réserves explicites.
- Contrôle visuel des schémas, tableaux et options graphiques ; tous les crops avant validation proviennent des pages de sujet.
- Validation finale des schémas JSON, unicité, couverture, liens d’images, stabilité des identifiants et rôles des assets.

Contrôles finaux : 330 correspondances de clés grille courte/corrigé détaillé ; 1635 comparaisons de propositions sujet/corrigé ; 336 consignes non vides ; 1 680 choix A–E ; aucune référence d’image manquante ; aucun identifiant source ni clé de sauvegarde dupliqué. Les comparaisons textuelles des corrections ne comprennent pas les six questions sans corrigé exploitable ni les options intégralement graphiques. Les divergences formelles et les réserves explicites de la source sont listées ci-dessus.

La vérification porte sur la fidélité au dossier fourni et sa cohérence interne. Elle ne transforme pas les corrigés du tutorat en corrigés scientifiques nouvellement validés. Les clichés de moindre qualité du PDF restent de la qualité de leur source ; aucune information n’a été inventée pour les compléter.

## Fichiers livrés

- `exams.json` : nouvelles séries UE4, prêtes à fusionner.
- `courses.json` : 12 couples identifiant/libellé de matière.
- `manifest.json` : inventaire exhaustif des sujets, corrections et 336 questions, y compris les cas hors note.
- `assets_manifest.json` et `assets/` : images WEBP et provenance de chaque crop.
- `audit.json` : compteurs, contrôles, remappages et réserves structurés.
- `audit.md` : ce rapport.
- `extract.py`, `prepare.py`, `build.py`, `verify.py` : scripts reproductibles dans ce répertoire de travail.
