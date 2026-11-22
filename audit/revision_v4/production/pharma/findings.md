# Révision V4 — Pharmacologie UE4

## Résultat utile au signalement de QCM manquants

Le défaut concret trouvé est le classement thématique. Le cours fourni « Cycle de vie du médicament — M. Le Borgne » comporte Drug Discovery, RSA/pharmacophore, pharmacomodulation, Markush, brevets, AINS et naproxène. Le site n’en présente actuellement que 2 QCM dans Cycle de vie : les questions sur ces parties sont réparties dans Identification PA, Chimie organique et Droit. Cela empêche de retrouver ces annales en ouvrant uniquement le cours attendu.

changes.json propose 25 reclassements primaires, tous attachés à une source précise. Ils portent Cycle de vie de 2 à 26 QCM, Identification PA de 32 à 17, Chimie organique de 9 à 2, Droit de 46 à 44, Biotechnologies de 31 à 30 et Cibles de 7 à 8. Les autres thèmes ne changent pas. Les 15 thèmes sont conservés ; aucun QCM n’est créé ni copié. relatedThemes.json ajoute 32 propositions de renvois pour les questions mixtes. Les identifiants bank/id des notes restent ceux de la base V3 afin que root puisse préserver les sauvegardes lors du déplacement.

Un second cas est explicite dans la consigne : 2024–2025 S1 Q19 annonce « Cibles et mécanisme d’action » mais est classé Biotechnologies ; le reclassement vers Cibles est proposé. 2024–2025 S1 Q20 annonce aussi Cibles, mais traite surtout d’essais du vaccin : un renvoi secondaire est proposé, sans déplacement forcé. 2023–2024 S2 Q3 et Q4 annoncent le cycle du médicament mais étaient tous deux dans Droit : le Q3 sur le générique est proposé en Cycle de vie ; le Q4 réglementaire garde Droit avec renvoi secondaire.

## Nouvel audit de la présence et du texte des QCM

Le décompte a été refait directement à partir des pages sources, sans reprendre le précédent total comme règle. Une recherche sur les 1660 pages retrouve 104 pages de sujets UE4 réparties en 14 blocs, uniquement entre les pages PDF 701 et 970 (les corrections occupent le reste du bloc UE4 jusqu’à 986). Les sujets comportent 333 groupes textuels A–E et 3 QCM dont les cinq molécules sont dans une figure : 336 questions sources. Les numéros textuels, pages et groupes d’items ont été rapprochés de la base. Pour les deux sujets 2021–2022 dont les numéros ne sont pas extraits comme texte, le contrôle repose sur la succession des groupes A–E et de la figure.

Le contrôle de contenu ne s’arrête pas aux identifiants : 1663 des 1680 propositions correspondent directement au texte original après normalisation typographique. Quinze autres sont les libellés des trois figures de molécules, inspectées visuellement. Les deux derniers écarts sont les caractères parasites « bdistribution » et « è50% » du sujet 2022–2023 S2 Q14, déjà nettoyés sans changement de sens dans le site. Les 13 QCM comportant une figure ont tous été inspectés. Aucune question source supplémentaire ni troncature substantielle d’item n’a été identifiée dans ce PDF.

Douze chaînes answer sont vides : onze questions ont une réserve explicite et restent accessibles hors note ; 2022–2023 S2 Q9 est distinct, car sa clé source est AUCUNE. Le moteur doit distinguer ce dernier cas d’une correction absente. Les tests d’accès réel dans le site relèvent de root ; cette revue n’en prétend pas les résultats.

L’annale UE4 la plus ancienne de la compilation est 2018–2019. On ne peut donc pas ajouter des sujets 2015–2016, 2016–2017 ou 2017–2018, ni une session absente, sans autre document. Root a indiqué que le catalogue des fichiers importés ne contient pas d’autre annale UE4 distincte.

### Blocs sources vérifiés

| Pages du sujet PDF | QCM sources | Correspondance base |
|---|---:|---|
| 701–710 | 28 | 28 |
| 727–734 | 28 | 28 |
| 751–756 | 15 | 15 |
| 767–774 | 28 | 28 |
| 789–792 | 15 | 15 |
| 801–808 | 25 | 25 |
| 823–828 | 18 | 18 |
| 839–846 | 25 | 25 |
| 859–864 | 19 | 19 |
| 875–882 | 25 | 25 |
| 897–902 | 20 | 20 |
| 915–922 | 30 | 30 |
| 939–948 | 30 | 30 |
| 963–970 | 30 | 30 |

## Relecture des corrections

Les 336 QCM et leurs 1680 items ont été relus. Les 160 remarques V3 ont été revues et soit conservées avec référence source, soit précisées/remplacées. Le fichier notes.json contient 179 notes localisées sur 152 QCM : 64 conflits internes ou entre corrigés, 91 points possibles à vérifier, 15 écarts avec les cours, 7 références/corrections manquantes et 2 références datées. Aucune clé n’a été changée. Aucun signalement générique n’a été ajouté aux questions sans anomalie localisée.

Les écarts avec les cours ne sont pas tous des inversions démontrées d’une réponse. Ils comprennent des erreurs d’explication et des divergences à arbitrer. Les plus nets sont :

| QCM source | Problème localisé | Référence du cours fournie |
|---|---|---|
| 2025–2026 S1 Q11 A/B | Code de déontologie validé simultanément comme législatif et réglementaire ; le cours le situe dans le règlement. | Droit, p6 |
| 2022–2023 S1 Q2 A | Commissaires déclarés élus par les assemblées nationales ; cours : nommés, non élus. | Droit, p5 |
| 2021–2022 S1 Q1 B/E | ANSES et EMA interverties quant au champ humain/vétérinaire. | Droit, p7–8 |
| 2021–2022 S2 Q1 D | Absence absolue de dispositions CSP sur l’animal, en contradiction avec la définition L5111-1 enseignée. | Droit, p6–7 |
| 2018–2019 Q12 E | Exclusion de Nice et chronologie attribuée à Rome incompatibles avec la liste des traités du cours. | Droit, p4 |
| 2022–2023 S2 Q7 C/D | Naproxène classé arylcarboxylique et non arylalcanoïque ; le cours le classe naphtylalcanoïque. | Cycle de vie, p4 et p7 |
| 2024–2025 S1 Q21 E | Verdict faux cohérent, mais justification confond biostéréoconversion R/S et activation d’un promédicament. | Cycle de vie, p2, p7–8 |
| 2018–2019 Q9 B/C | Justification confond publication du brevet et expiration ; le cours distingue 18 mois et 20 ans. | Cycle de vie, p3 |
| 2022–2023 S1 Q10 A | « Arylalcaloïdes » imprimé au lieu de la famille arylalcanoïque enseignée. | Cycle de vie, p6 |
| 2018–2019 Q20 A | ADMET justifié par « administration », alors que le tableau du cours donne Absorption et Toxicité. | Cycle de vie, p2 |

D’autres précisions sont limitées à une explication (ANSES dans 2020–2021 PACES Q17 ; attribution des cibles à la PK dans PACES Q9) ou signalent un écart de formulation sans trancher toute la proposition. Chaque note indique ce qui est effectivement soutenu par le cours et conserve le verdict de la source.

### Conflits entre annales nouvellement explicités

Les comparaisons A–E ont retrouvé notamment des verdicts opposés pour AMBER/protéine-ADN, visualisation des structures secondaires, affinité prédite par QSAR, criblage à haut débit/sérendipité, mêmes indications des me-too, hémisynthèse et ressource naturelle, modifications d’extraits, origine de la céphalosporine et centrage de l’ETP. Les références sont données des deux côtés du conflit. Ces oppositions constituent des preuves d’incohérence entre corrigés, mais ne remplacent pas la ronéo absente pour choisir scientifiquement un verdict.

## Sources consultées et limites

- Compilation originale : Sujets + corrections compilés(1).pdf, sujets/corrections UE4, pages PDF 701–986 ; revue de toutes les propositions et des 13 figures.
- Droit Pharma_261001_102709.pdf : 10 pages intégralement lues ; pages citées contrôlées visuellement.
- cycle de vie du médicament _ M. Le Borgne.pdf : 9 pages intégralement lues, y compris toutes les figures et tableaux des pages peu textuelles.

Les deux fiches fournies ne couvrent pas intégralement les 15 cours. Les cours détaillés Sources naturelles, Galénique, PK/PD, Cibles, Biotechnologies, BUM, Développement clinique, Balance bénéfice/risque, Analyse/contrôles et Iatrogénie ne sont pas accessibles dans les sources UE4 transmises. Les questions correspondantes restent relues, mais une absence d’anomalie détectée ne constitue pas une validation scientifique.

La fiche Droit contient elle-même des simplifications et incohérences. Exemple directement pertinent : p6 écrit « directive de 2014 », tandis que l’annale 2022–2023 S1 Q2C corrige en « règlement ». La note présente cette différence comme un point à arbitrer, jamais comme la preuve que le corrigé est faux. De même, la remarque sur des formes galéniques différentes pour les génériques (p7) ne suffit pas à invalider un item de définition réglementaire de forme pharmaceutique. La formulation de la fiche selon laquelle l’EMA délivre l’AMM n’est pas réutilisée pour attribuer formellement cette décision.

coverage.json couvre chaque bank/id : {'reviewed_without_course': 250, 'reviewed_with_course': 79, 'needs_source': 7}. Le statut avec cours signifie un recoupement partiel d’items pertinents, explicitement limité dans chaque fiche de couverture ; il ne certifie pas les cinq items.

## Fichiers à intégrer

- notes.json : ensemble complet des notes UE4 révisées ; remplacer le lot de notes V3, plutôt que l’ajouter une seconde fois.
- coverage.json : couverture question par question.
- changes.json : 25 déplacements proposés, à appliquer en maintenant identifiants et migrations de sauvegardes.
- relatedThemes.json : 32 renvois sans copie de questions.
- missing_audit.json et fresh_subject_inventory.json : audit documentaire frais et blocs sources.
- stats.json : comptages et impact des déplacements proposés.

Aucune réparation nouvelle d’énoncé ou de clé source n’est demandée. Les décalages et réserves de correction déjà gérés en V3 restent documentés.
