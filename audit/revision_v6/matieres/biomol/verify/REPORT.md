# Biologie moléculaire V6 — vérification indépendante

## Verdict

**Lot approuvé pour intégration, avec les limites des originaux explicitement conservées.** La vérification couvre les **23 banques, 550 QCM ou fiches et 2 752 items existants**. Les **46 PDF originaux** sont disponibles ; aucun de ces fichiers n’est à redemander.

Les fichiers à intégrer sont exclusivement les deux snapshots complets de ce répertoire :

| Fichier | SHA256 |
|---|---|
| `approved_reviewed.json` | `15141b6a24da994041a69789f88bc7032859228ace30987919a0e87cb9542fd9` |
| `approved_crops.json` | `d00d29fefac631f93927db22ffdeceb6a324a71753ab86a1ac5f059b5563fead` |

`approved.json` contient ces empreintes, celles des entrées figées du préparateur et celle du registre de couverture. `asset_manifest.json` est vide : les images interactives nécessaires existaient déjà. Le `source_manifest.json` du préparateur reste nécessaire pour empaqueter les quatre nouveaux PDF qu’il identifie.

Les IDs, l’ordre des questions, l’ordre et les lettres des options ainsi que toutes les clés sont identiques à la préparation et à la base V5. Les trois clés ambiguës restent hors note. La fiche de correspondance intro/autotest ID10 reste sans options inventées ; son accès en mode sélectif relève du traitement d’interface annoncé par root.

## Étendue et méthode

L’audit ne repose pas sur un échantillon, sur l’ancien audit ou sur la seule réussite d’un script. Les 550 associations sujet/corrigé et les 2 752 propositions ont été comparées aux originaux. Une extraction indépendante conserve les coordonnées, polices, couleurs et exposants ; ses associations ont été confrontées aux rendus dès que la typographie, une figure, une colonne ou un tableau l’exigeait. Les pages ordinaires de texte ont été comparées avec leur texte PDF natif ; le présent rapport ne prétend pas qu’une seconde lecture visuelle intégrale et distincte de chaque page ordinaire a été réalisée.

Le corpus représente **274 pages**, toutes extraites et rendues pour le contrôle. Les **131 images natives** des PDF et les **123 images interactives uniques** du site ont été associées à leur contenu et contrôlées. Les lettres des figures, flèches, séquences 5′/3′, indices, puissances de dix, régions en gras et séquences seed ont fait partie du contrôle. Les 20 rattachements existants d’annexes du code génétique ont été vérifiés, avec leurs fichiers et pages exacts.

Les 12 grilles Wooclap, soit 60 items, ont été lues dans les cadres de réponse imprimés. Deux cas que le texte natif ne segmentait pas ont été traités directement : l’ED annales ID2, Q24 raster, avec ses cinq items et la clé B ; l’ED25 Q40, dont la clé B est imprimée sous une forme non reconnue par le parseur. La clé E de l’ED annales ID16 a été confrontée aux cinq commentaires V/F. L’ordre « DB » du corrigé ED26 Q6 est équivalent à « BD » dans le site.

Les erreurs du parseur ont été distinguées des erreurs du site. Par exemple, un titre Wooclap, un bandeau d’année, la séquence d’une série suivante ou une annexe peuvent être absorbés après le dernier item E. Les 170 candidats initiaux ont une décision dans `comparison_adjudications.json`. Les exclusions géométriques et les réaffectations de colonnes sont détaillées dans `geometry_adjudications.json`.

Les empreintes des PDF lus ont été recalculées et confrontées aux copies originales disponibles et aux copies empaquetées existantes. Le résultat est consigné dans `source_verification.json`.

## Changements apportés après la préparation

Le journal comporte **163 opérations**, dont certaines sont les itérations successives d’un même cadrage. Dans les snapshots finaux, **36 objets question** et **95 objets de captures** diffèrent du lot préparé. Il ne faut donc pas présenter les 163 lignes du journal comme 163 erreurs indépendantes.

### Textes et notations

- Intro annales ID3, détail D : retrait du bandeau « 20125-2016 » qui avait été accolé après « amine ici ». Le bandeau et la mention RAS appartiennent à la section suivante dans le corrigé p. 1.
- Rétablissement de **28 catégories de session** à partir des bandeaux imprimés, y compris les bandeaux répartis sur deux lignes. Les coquilles chronologiques réellement imprimées restent conservées.
- Rétablissement de **sept notations d’items** : six puissances de dix et la charge Mg²⁺. Les exposants sont confirmés par les spans PDF et les rendus, pas inférés à partir de la seule plausibilité scientifique.
- Rétablissement de **quatre détails** contenant des puissances de dix. Les ordinaux, tels que « 109ème », n’ont pas été traités comme des puissances.
- Ajout de quatre notes après correction sur les formulations incomplètes ou le caractère & réellement imprimé, sans compléter une phrase de manière conjecturale.

### Captures et contextes

Le lot final comprend **1 450 panneaux originaux : 805 de sujet et 645 de corrigé**, contre 1 366 dans la préparation. Les panneaux répétés pour des contextes communs ne constituent pas autant de figures distinctes.

Les réparations incluent notamment les six figures initialement coupées d’introduction, d’ARN et de traduction ; la séparation des figures d’ARNt et des questions suivantes ; les pyrimidines communes aux Q10/Q11 d’introduction ; les 14 contextes principaux d’ED annales dans le corrigé ; le fragment d’oligonucléotide réutilisé par la question suivante ; et les copies des annexes du code génétique.

Les ED contemporains ont nécessité des limites qui suivent les colonnes et les figures plutôt que la seule hauteur d’un titre. Cela concerne notamment les sites donneur/accepteur d’épissage, l’acétylation, le code histone, les deux colonnes des Q11/Q12, la structure d’ARNt, le chromosome, les diapositives de fusion et les séquences de mutations. Les clés ED25 Q26/Q42, immédiatement suivies d’une autre clé, ont aussi été recadrées pour inclure leur ligne entière.

Les schémas communs de microARN et de structures des bases sont rattachés aux exercices qui les utilisent. Les marges inférieures du code génétique et des séquences ont été rétablies. Les fragments provenant d’une figure voisine ont été retirés des copies lorsqu’ils n’étaient pas utiles à la question.

Chaque rectangle ajouté ou modifié a été rendu puis examiné ; les réparations révélées par cette relecture ont été corrigées et de nouveau contrôlées. `changed_panel_manifest.json` décrit les 75 rectangles finaux distincts qui diffèrent de la préparation. La couverture géométrique finale inclut toutes les lignes pertinentes. Les seuls recouvrements partiels d’un rectangle raster sont explicités dans `figure_coverage.json` : un raster contenant à la fois contexte commun et options de Q24, et la zone blanche du rectangle d’un chromosome derrière une diapositive voisine.

## Absence de fuite de réponse

Deux originaux de sujet sont différés après correction :

1. **Transcription autotest ID2** : « Fau » rouge figure réellement après D dans le PDF intitulé ENONCE. Le texte interactif ne le contient plus ; la copie reste authentique et différée.
2. **Traduction autotest ID3** : un point rouge résiduel termine C. L’original est conservé, avec accès après validation.

Ces deux questions n’ont ni image interactive, ni image de contexte ou annexe offrant un accès parallèle au résidu. Les autres images interactives ont été vérifiées. Les espaces colorés sans glyphe visible ne révèlent rien ; les points verts présents sur d’autres sujets apparaissent sur des propositions vraies et fausses et ne constituent pas une grille de réponse. Les couleurs et gras qui font partie des données de séquence restent visibles.

L’intégration doit conserver les notes et images de correction après validation ainsi que les deux drapeaux `subjectAfterCorrection`. Root a annoncé la prise en charge du menu des sources pour éviter un accès parallèle au PDF annoté avant correction.

## Limites authentiques des sources

Une vérification littérale réussie ne rend pas complet un original incomplet. `coverage.json` distingue les items vérifiés de ces limites : **huit items incomplets, un titre incomplet et quatre items dont le seul contenu est HP**.

| Banque / ID | Élément | Limite conservée |
|---|---|---|
| ADN annales 17 | E | S’arrête après « La liaison entre les différents ». |
| Transcription autotest 35 | B | S’arrête après « premier nucléotide qui sera » dans les deux originaux. |
| Traduction autotest 27 | Titre | S’arrête à « quels sont ceux qui ... » ; le doublon Q21 donne un contexte, mais le titre original n’est pas réécrit. |
| Réparation annales 8 | A–D | Mots tronqués : « anome », « recombi », groupes non précisés et « mécanis de ». |
| Réparation annales 17 | B | Le caractère & est imprimé à la place d’une polymérase identifiable. |
| Réparation autotest 15 | C | Sujet arrêté à « ADN pol. » ; le corrigé ajoute α avant de donner Faux. |

Les quatre mentions HP sont dans réparation annales ID3 A, ID9 E, ID17 E et ID20 E. Les options absentes de certaines questions hors programme ne sont pas créées.

Les clés **AD(E)** d’ADN annales ID25, **AB(C)** d’ARN annales ID26 et **AB(C)** de transcription annales ID33 restent ambiguës et non notées. Les désaccords déjà signalés entre clé et commentaire sont conservés, notamment ADN annales14 B, traduction annales11 D, régulation annales18 C, anomalies annales1 E et ED annales38 C/E. Les changements de formulation entre sujet et corrigé — négation d’ADN auto13 C, VII/VIII d’organisation auto9 E, réécriture de réparation auto11 D — restent visibles dans les notes sourcées.

Les réserves scientifiques et les demandes de cours détaillé déjà présentes ne sont pas transformées par cet audit de fidélité en arbitrages scientifiques définitifs. Aucune clé officielle n’a été remplacée par une réponse jugée plus plausible.

## Livrables de contrôle

- `coverage.json` : 550 entrées, contenant 2 752 états d’items et les limites explicites de complétude.
- `issues.json` et `changes.json` : réparations, notes conservées et limites des originaux.
- `missing.json` : aucun PDF original manquant ; liste précise des formulations ou clés à clarifier.
- `checks.json` : effectifs, invariants et bilan des banques.
- `source_verification.json`, `asset_verification.json`, `figure_coverage.json` : empreintes, rattachements et contrôles des sources et figures.
- `comparison_adjudications.json`, `geometry_adjudications.json` : décisions sur les anomalies de segmentation et les limites de rectangles.
- `leak_and_reference_verification.json` : contrôle des deux originaux différés et des 20 annexes.
- `approved.json` : manifeste d’approbation des snapshots exacts.

**Aucun problème d’import non résolu n’est retenu dans le lot approuvé.** Les limites restantes proviennent des originaux et restent indiquées, sans inventer de contenu manquant. La vérification finale de l’interface et de l’empaquetage global relève de l’intégration par root.
