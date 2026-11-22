# Relecture pharmacie V3 — lot MIDDLE

## Statut

**Lot terminé : 112 QCM, 560 propositions, cinq sujets relus un par un.** Les clés, poids, numéros, identifiants et stockages des banques sources restent intacts. Les 112 lignes de `reviews.json` proposent un classement individuel selon la compétence dominante et 53 réserves localisées sur 45 QCM, uniquement après correction.

Source de contenu exclusive : `upload/Sujets + corrections compilés(1).pdf`, pages 801–896. Aucune source extérieure ni nouvelle correction scientifique n’a été introduite. Les réserves signalent une contradiction, une formulation incertaine ou un motif précis à vérifier dans la ronéo ; elles ne remplacent pas les verdicts imprimés.

## Contrôles effectués

1. Lecture de la consigne, du contexte et des cinq propositions de chaque QCM dans le sujet, puis comparaison avec les textes importés.
2. Lecture du corrigé détaillé correspondant, de ses explications A–E et de la grille courte de chaque sujet. Les numéros du corrigé ont été suivis séparément de ceux du sujet.
3. Inspection visuelle des trois QCM à figures (QSAR et pharmacophore), des contextes partagés et des réserves sensibles ; les captures utilisées pour les questions proviennent des sujets, celles du corrigé restent réservées à la correction.
4. Seconde passe sur toutes les clés, les verdicts, les exceptions de couche texte, les réserves réciproques entre sessions et les frontières des thèmes.

**Résultats :** 111 clés disponibles concordent avec les grilles et les en-têtes détaillés. Les 110 jeux de verdicts explicites concordent aussi ; le Q7 2022–2023 S1 donne une solution générale QSAR sans cinq verdicts séparés. Aucune consigne de ce lot ne demande de sélectionner les propositions fausses : aucune inversion de cette nature n’a été introduite.

Les 553 correspondances textuelles directes et les sept exceptions visuelles couvrent les 560 items. Les exceptions sont les cinq molécules graphiques du Q7 2021–2022 S1, représentées par leur figure, et deux parasites de couche texte du Q14 2022–2023 S2. Le rendu visuel confirme les textes importés. Aucun nouveau fichier d’image pour le site n’est nécessaire.

## Cas de source à conserver distincts

- **2021–2022 S1 Q13 (sujet p843)** : le corrigé manque cette question sur les BPF/BPP. Les 25 questions du sujet correspondent à 24 corrections ; à partir du Q14, le numéro du corrigé vaut le numéro du sujet moins un. La clé vide demeure hors note. Le champ de poids d’origine est conservé, sans inventer de clé.
- **2022–2023 S2 Q9** : « AUCUNE » est une vraie réponse du corrigé, avec `answerIsEmpty: true`, et ne doit pas être assimilée au corrigé manquant.
- **2020–2021 S1 Q13/Q14** : le contexte commun précise l’insolubilité de l’oxyde de zinc dans l’eau et les huiles minérales. Les deux membres portent le même bloc partagé et restent dans Galénique.
- **2020–2021 S1 Q21 B/E** : propositions identiques dans le PDF, toutes deux fausses ; doublon source conservé et signalé.

## Proposition éditoriale soumise au constructeur

**2020–2021 S1 Q9, p889 :** deux champs sont proposés en avant/après exacts dans `patches`. La solution globale QSAR (tableau des descripteurs et trois calculs) est concaténée actuellement à `explanations.E`. La proposition ramène E à « FAUX » et place intégralement les nombres et opérations dans `generalExplanation`. Les trois calculs et la clé B restent inchangés ; la capture du corrigé original est conservée. Les deux changements portent `requireRootValidation: true`, `evidence` et `sourcePages: [889]`. Aucune banque n’a été éditée par cet agent.

## Inventaire des sujets

| Sujet | QCM / items | Pages sujet | Pages corrigé détaillé | Grille |
|---|---:|---|---|---:|
| 2022-2023 S1 | 25 / 125 | 802–808 | 811–821 | 810 |
| 2022-2023 S2 | 18 / 90 | 824–827 | 831–837 | 830 |
| 2021-2022 S1 | 25 / 125 | 840–845 | 849–858 | 848 |
| 2021-2022 S2 | 19 / 95 | 860–864 | 867–874 | 866 |
| 2020-2021 S1 | 25 / 125 | 876–882 | 885–895 | 884 |

## Répartition proposée

| Thème exact | QCM |
|---|---:|
| Sources naturelles - Kerzaon | 8 |
| Galénique | 9 |
| Le droit pharma | 13 |
| Cycle de vie du médicament | 0 |
| Balance bénéfice/risque | 6 |
| Conception rationnelle : Terreux | 8 |
| Identification PA : Bourguignon | 10 |
| Développement clinique | 6 |
| Biotechnologies | 11 |
| Chimie organique | 4 |
| PK PD | 6 |
| Cibles, mécanisme & actions | 2 |
| Analyse & contrôles des médicaments | 6 |
| Iatrogénie | 3 |
| BUM | 20 |

Le lot ne contient aucun QCM dominé par le parcours général du Cycle de vie. Le thème reste disponible dans le classement global. Les questions mêlant plusieurs compétences ne sont jamais divisées. Les QCM chimiques 2022–2023 S1 Q10, 2021–2022 S1 Q11 et 2020–2021 S1 Q11 ont été harmonisés en Chimie organique avec le responsable de l’intégration.

## Revue sujet par sujet

### 2022-2023 — S1

25 QCM et 125 items relus. Grille p810, sujets p802–808, corrigés p811–821.

| QCM | Sujet | Corrigé | Clé conservée | Thème proposé |
|---:|---:|---:|---|---|
| 1 | 802 | 811 | ACE | Le droit pharma |
| 2 | 802 | 811 | ABDE | Le droit pharma |
| 3 | 802 | 812 | ACE | Sources naturelles - Kerzaon |
| 4 | 802 | 812 | AD | Sources naturelles - Kerzaon |
| 5 | 803 | 813 | ACE | Analyse & contrôles des médicaments |
| 6 | 803 | 813 | ABCD | Conception rationnelle : Terreux |
| 7 | 804 | 814 | D | Conception rationnelle : Terreux |
| 8 | 804 | 815 | ABD | Biotechnologies |
| 9 | 805 | 815 | ADE | Biotechnologies |
| 10 | 805 | 815 | ABD | Chimie organique |
| 11 | 805 | 816 | ABC | Identification PA : Bourguignon |
| 12 | 805 | 816 | ACDE | Identification PA : Bourguignon |
| 13 | 806 | 817 | DE | Analyse & contrôles des médicaments |
| 14 | 806 | 817 | B | Galénique |
| 15 | 806 | 817 | ACD | Galénique |
| 16 | 806 | 818 | BC | Iatrogénie |
| 17 | 806 | 818 | AC | Balance bénéfice/risque |
| 18 | 807 | 818 | A | PK PD |
| 19 | 807 | 819 | BC | Développement clinique |
| 20 | 807 | 819 | ABC | Balance bénéfice/risque |
| 21 | 807 | 820 | BCDE | Développement clinique |
| 22 | 807 | 820 | ACE | BUM |
| 23 | 808 | 821 | ACDE | BUM |
| 24 | 808 | 821 | BCE | Biotechnologies |
| 25 | 808 | 821 | ACE | Développement clinique |

**Réserves à afficher après correction :**

- Q2 A — Le corrigé valide A, qui affirme que les commissaires représentent leur pays et sont élus par les assemblées nationales. Vérifie ces deux affirmations dans la ronéo de droit pharma ; la clé source ABDE est conservée. [Sujet p802, corrigé p811 ; possible_error]
- Q3 D — D est faux ici, mais la même affirmation sur les antibiotiques issus de venins est validée avec « VRAI ?? » en 2021–2022 S1 Q4C. Vérifie ce point dans la ronéo Sources naturelles ; la clé ACE est conservée. [Sujet p802, corrigé p812 ; source_conflict]
- Q6 C — La justification de C porte explicitement « VRAI ? » à propos du calcul de stabilité par relation structure-activité. Vérifie ce point dans la ronéo Conception rationnelle ; la clé source ABCD est conservée. [Sujet p803, corrigé p813 ; source_uncertainty]
- Q10 A — A emploie le terme « acides arylalcaloïdes », tel qu'imprimé dans le sujet, et le corrigé le valide sans précision. Vérifie la dénomination de cette famille dans la ronéo Identification PA ; le texte source est conservé. [Sujet p805, corrigé p815 ; source_uncertainty]
- Q12 E — Le corrigé valide sans justification le mot « nécessairement » concernant les indications d'un me-too. Vérifie la portée de cette affirmation dans la ronéo Identification PA ; la clé source ACDE est conservée. [Sujet p805, corrigé p816 ; source_uncertainty]
- Q17 C,D — Le corrigé exige en C un mécanisme documenté et exclut en D un effet retardé lorsque la concentration est nulle. Vérifie les critères d'imputabilité et la portée de l'hystérésis dans la ronéo Balance bénéfice/risque ; la clé source AC est conservée. [Sujet p806, corrigé p818 ; possible_error]
- Q18 A — A est vrai ici, alors que le rôle des paramètres pharmacocinétiques dans l’ajustement de la posologie est rejeté en 2021–2022 S1 Q18A. Vérifie cette divergence dans la ronéo PK PD ; la clé A est conservée. [Sujet p807, corrigé p818 ; source_conflict]
- Q19 A,E — Les justifications de A et E définissent le critère clinique comme un guide du choix thérapeutique, alors que le QCM interroge aussi les critères d'efficacité. Vérifie la distinction entre critère de jugement et choix du traitement dans la ronéo Développement clinique ; la clé BC est conservée. [Sujet p807, corrigé p819 ; possible_error]
- Q21 D — D affirme que l'effet placebo est « plus mineur » lorsque le médicament est actif, sans préciser s'il s'agit de sa part relative ou de son importance absolue. Vérifie cette distinction dans la ronéo Développement clinique ; le corrigé source retient D vrai. [Sujet p807, corrigé p820 ; source_uncertainty]
- Q23 D — D est vrai ici, mais le même lien entre erreur de rangement et erreur d’administration est faux en 2021–2022 S1 Q22B. Vérifie ce point dans la ronéo BUM ; la clé ACDE est conservée. [Sujet p808, corrigé p821 ; source_conflict]
- Q24 E — E emploie « vaccin » pour la délivrance du gène dans les lymphocytes et est validé sans explication. Vérifie le vocabulaire du transfert génétique des CAR-T dans la ronéo Biotechnologies ; la clé source BCE est conservée. [Sujet p808, corrigé p821 ; possible_error]
- Q25 B — La justification de B ne cite que les phasesIII etIV pour mesurer les effets indésirables. Vérifie la place de l'étude de la tolérance dans les différentes phases du développement clinique dans ta ronéo ; la clé source ACE est conservée. [Sujet p808, corrigé p821 ; possible_error]

**Cas mixtes conservés entiers :**

- Q4 → Sources naturelles - Kerzaon : Extraction, hémisynthèse et culture des ressources naturelles ; biotechnologie et criblage sont ici comparés comme moyens d'obtention.
- Q9 → Biotechnologies : Biomédicaments, thérapie cellulaire, transcriptomique et production recombinante ; l'item R&D est secondaire.
- Q13 → Analyse & contrôles des médicaments : Identification de la Pharmacopée par ses monographies et spécifications qualitatives/quantitatives de qualité.
- Q19 → Développement clinique : Nature et pertinence des critères cliniques d'efficacité du point de vue du patient.
- Q21 → Développement clinique : Interprétation de l'effet traitement et de sa composante placebo selon les patients et situations.
- Q23 → BUM : Application de la règle des5B, dossier pharmaceutique et RCP comme outils de bon usage.
- Q24 → Biotechnologies : CAR-T : lymphocytes modifiés, transfert génétique et immunothérapie cellulaire.

### 2022-2023 — S2

18 QCM et 90 items relus. Grille p830, sujets p824–827, corrigés p831–837.

| QCM | Sujet | Corrigé | Clé conservée | Thème proposé |
|---:|---:|---:|---|---|
| 1 | 824 | 831 | ACDE | Le droit pharma |
| 2 | 824 | 831 | AB | Sources naturelles - Kerzaon |
| 3 | 824 | 832 | AB | Analyse & contrôles des médicaments |
| 4 | 824 | 832 | ACD | Conception rationnelle : Terreux |
| 5 | 825 | 832 | BCD | Biotechnologies |
| 6 | 825 | 833 | ACE | Biotechnologies |
| 7 | 825 | 833 | ACE | Chimie organique |
| 8 | 825 | 833 | ABCDE | Galénique |
| 9 | 825 | 834 | AUCUNE | Identification PA : Bourguignon |
| 10 | 826 | 834 | ABC | Le droit pharma |
| 11 | 826 | 835 | ACDE | BUM |
| 12 | 826 | 835 | ABCD | Le droit pharma |
| 13 | 826 | 835 | CE | BUM |
| 14 | 826 | 836 | BC | PK PD |
| 15 | 827 | 836 | CE | Balance bénéfice/risque |
| 16 | 827 | 837 | CE | BUM |
| 17 | 827 | 837 | ADE | BUM |
| 18 | 827 | 837 | ABDE | BUM |

**Réserves à afficher après correction :**

- Q4 E — Le corrigé rejette la prédiction d'affinité en E mais justifie ce rejet par « le QSAR calcule l'interaction », sans expliciter la distinction. Vérifie les propriétés prédites par QSAR dans la ronéo Conception rationnelle ; la clé ACD est conservée. [Sujet p824, corrigé p832 ; source_uncertainty]
- Q5 E — La production d’érythropoïétine humaine active par E. coli est fausse ici, mais la même proposition est vraie en 2021–2022 S2 Q6E. Vérifie le système de production et l’activité de la protéine dans la ronéo Biotechnologies ; la clé BCD est conservée. [Sujet p825, corrigé p832 ; source_conflict]
- Q7 C,D,E — Le corrigé qualifie le naproxène d'arylcarboxylique, rejette arylalcanoïque et valide simultanément 2-naphtylpropionique. Vérifie l'articulation de ces familles chimiques dans ta ronéo ; la clé source ACE est conservée. [Sujet p825, corrigé p833 ; possible_error]
- Q9 C — La clé source est « AUCUNE ». Pour C, le corrigé oppose la modélisation mathématique/informatique au « modèle biomathématique » sans expliquer cette exclusion du criblage virtuel. Vérifie ce point dans la ronéo Identification PA ; aucune réponse de remplacement n'est imposée. [Sujet p825, corrigé p834 ; possible_error]
- Q12 A — La justification de A, qui affirme que toute publicité est strictement interdite, porte « VRAI ? ». Vérifie la portée de l'interdiction et les distinctions enseignées dans la ronéo de droit pharma ; la clé ABCD est conservée. [Sujet p826, corrigé p835 ; source_uncertainty]
- Q14 A,C,D,E — Le titre annonce la pharmacocinétique, mais plusieurs items et explications portent sur la pharmacodynamie. C est validé avec la mention « HP maintenant ». Vérifie le périmètre et les notions de demi-vie/effet dans la ronéo PK PD ; la clé BC est conservée. [Sujet p826, corrigé p836 ; source_uncertainty]
- Q14 E — E est faux ici avec la distinction efficacité/Emax et puissance/CE50, mais la même définition par CE50 est validée en 2021–2022 S1 Q19E. Vérifie cette divergence dans la ronéo PK PD ; la clé BC est conservée. [Sujet p826, corrigé p836 ; source_conflict]
- Q18 A — A dit que l'ETP est centrée sur « les soignants » et le corrigé la valide sans explication. Vérifie la distinction entre centrage sur le patient et rôle des soignants dans la ronéo BUM ; la clé ABDE est conservée. [Sujet p827, corrigé p837 ; possible_error]

**Cas mixtes conservés entiers :**

- Q3 → Analyse & contrôles des médicaments : Contrôles des matières premières et falsifications, Pharmacopée et caractérisation physicochimique.
- Q7 → Chimie organique : Identification de la classe chimique du naproxène : taille moléculaire et familles d'acides, sans question de criblage ou de développement.
- Q10 → Le droit pharma : Mentions obligatoires sur la spécialité pharmaceutique et distinction avec la notice.
- Q12 → Le droit pharma : Publicité, responsabilité judiciaire et objectifs de l'industrie pharmaceutique.
- Q17 → BUM : Adaptation de l'usage aux populations à risque : enfants, patients âgés, grossesse et insuffisance rénale.

### 2021-2022 — S1

25 QCM et 125 items relus. Grille p848, sujets p840–845, corrigés p849–858.

| QCM | Sujet | Corrigé | Clé conservée | Thème proposé |
|---:|---:|---:|---|---|
| 1 | 840 | 849 | BC | Le droit pharma |
| 2 | 840 | 849 | ABC | Le droit pharma |
| 3 | 840 | 850 | BCE | Sources naturelles - Kerzaon |
| 4 | 840 | 850 | ACDE | Sources naturelles - Kerzaon |
| 5 | 841 | 850 | ABCE | Analyse & contrôles des médicaments |
| 6 | 841 | 851 | ABD | Conception rationnelle : Terreux |
| 7 | 841 | 851 | ABC | Conception rationnelle : Terreux |
| 8 | 842 | 852 | ABCDE | Biotechnologies |
| 9 | 842 | 852 | ACD | Biotechnologies |
| 10 | 842 | 852 | ABDE | Identification PA : Bourguignon |
| 11 | 842 | 853 | ADE | Chimie organique |
| 12 | 843 | 853 | BE | Identification PA : Bourguignon |
| 13 | 843 | Absente | Absente — hors note | Le droit pharma |
| 14 | 843 | 854 | A | Galénique |
| 15 | 843 | 854 | A | Galénique |
| 16 | 843 | 854 | ACDE | BUM |
| 17 | 844 | 855 | ABDE | BUM |
| 18 | 844 | 855 | BDE | PK PD |
| 19 | 844 | 856 | BCDE | PK PD |
| 20 | 844 | 856 | DE | BUM |
| 21 | 844 | 856 | C | Balance bénéfice/risque |
| 22 | 845 | 857 | AE | BUM |
| 23 | 845 | 857 | ABDE | BUM |
| 24 | 845 | 858 | ABCD | Développement clinique |
| 25 | 845 | 858 | ABCDE | Cibles, mécanisme & actions |

**Réserves à afficher après correction :**

- Q1 B,E — Le corrigé attribue à l'ANSES la compétence sur les médicaments humains et vétérinaires, mais rejette la même double compétence pour l'agence européenne. Vérifie précisément les champs de compétence enseignés dans la ronéo de droit pharma ; la clé BC est conservée. [Sujet p840, corrigé p849 ; possible_error]
- Q4 C — C porte « VRAI ?? » et le corrigé reconnaît que le point n'était pas explicite dans le cours. La même affirmation venins/antibiotiques est fausse en 2022–2023 S1 Q3D. Vérifie ce point dans la ronéo Sources naturelles ; la clé ACDE est conservée. [Sujet p840, corrigé p850 ; source_conflict]
- Q4 A — L’origine fongique de l’ergotamine est vraie ici, mais la même proposition est fausse en 2021–2022 S2 Q2C. Vérifie ce point dans la ronéo Sources naturelles ; la clé ACDE est conservée. [Sujet p840, corrigé p850 ; source_conflict]
- Q7 C — La justification compte deux cycles aromatiques pour C, alors que le dessin présente trois cycles fusionnés. Vérifie la convention de comptage et la correspondance spatiale au pharmacophore dans la ronéo Conception rationnelle ; la clé ABC est conservée. [Sujet p841, corrigé p851 ; source_uncertainty]
- Q10 C — C est noté faux, mais la fin de la justification imprimée contient « mais d'un médicament falsifié », formulation incohérente avec ce verdict. Vérifie la distinction me-too/falsification dans la ronéo Identification PA ; la clé ABDE est conservée. [Sujet p842, corrigé p852 ; source_uncertainty]
- Q13 A,B,C,D,E — Ce QCM sur les BPF/BPP est absent du corrigé fourni. Il reste hors note : vérifie les cinq propositions dans la ronéo de droit pharma. Le décalage de numérotation du corrigé suivant a été pris en compte. [Sujet p843, corrigé p848 ; source_uncertainty]
- Q18 A — A est faux ici, mais l'affirmation selon laquelle les paramètres pharmacocinétiques permettent d'ajuster la posologie est vraie en 2022–2023 S1 Q18A. Vérifie ce point dans la ronéo PK PD ; la clé BDE est conservée. [Sujet p844, corrigé p855 ; source_conflict]
- Q18 C — La justification propose un espacement « toutes les 5 demi-vies », tandis que B/E parlent du délai d'équilibre. Vérifie la distinction entre intervalle des doses et temps d'équilibre dans la ronéo PK PD. [Sujet p844, corrigé p855 ; possible_error]
- Q19 B — La justification assimile « antagoniste complet » à « irréversible » et à une liaison covalente. Vérifie ces notions distinctes dans la ronéo PK PD ; la clé source BCDE est conservée. [Sujet p844, corrigé p856 ; possible_error]
- Q19 D,E — D/E associent puissance, effet maximal et CE50 ; E est vrai ici, alors que2022–2023 S2 Q14E est faux et distingue Emax/CE50. Vérifie cette distinction dans la ronéo PK PD ; aucune clé de remplacement n'est imposée. [Sujet p844, corrigé p856 ; source_conflict]
- Q22 B — Le lien entre erreur de rangement et erreur d'administration est faux ici, mais vrai en 2022–2023 S1 Q23D. La justification donne un exemple d'erreur de voie sans trancher ce lien. Vérifie ce point dans la ronéo BUM ; la clé AE est conservée. [Sujet p845, corrigé p857 ; source_conflict]

**Cas mixtes conservés entiers :**

- Q10 → Identification PA : Bourguignon : Optimisation structure-activité, châssis moléculaires, me-too et protection des séries de composés.
- Q11 → Chimie organique : Biostéréoconversion des acides arylpropioniques et modifications chimiques du naproxène, avec un item de contrôle et un item d’optimisation.
- Q13 → Le droit pharma : Champ d'application et force juridique des BPF/BPP et de la Pharmacopée.
- Q14 → Galénique : Formes et voie orale : absorption, émulsion, ampoule buvable et unités de volume.
- Q17 → BUM : Sens critique des professionnels face à l'information industrielle, intérêt de santé publique et objectifs commerciaux.
- Q20 → BUM : Individualisation de la prescription selon préférences et risque du patient.
- Q21 → Balance bénéfice/risque : Évaluation du progrès thérapeutique par l'ASMR, usage pour prescrire et rôle de la HAS.
- Q24 → Développement clinique : Objectifs des études de phaseIV dans une indication déjà reconnue.
- Q25 → Cibles, mécanisme & actions : Identification des mécanismes d'action impliquant ADN/ARN et récepteurs nucléaires.

### 2021-2022 — S2

19 QCM et 95 items relus. Grille p866, sujets p860–864, corrigés p867–874.

| QCM | Sujet | Corrigé | Clé conservée | Thème proposé |
|---:|---:|---:|---|---|
| 1 | 860 | 867 | ACDE | Le droit pharma |
| 2 | 860 | 867 | ADE | Sources naturelles - Kerzaon |
| 3 | 860 | 868 | AD | Analyse & contrôles des médicaments |
| 4 | 860 | 868 | BDE | Conception rationnelle : Terreux |
| 5 | 860 | 868 | ABCD | Biotechnologies |
| 6 | 861 | 869 | BCDE | Biotechnologies |
| 7 | 861 | 869 | BCDE | Identification PA : Bourguignon |
| 8 | 861 | 870 | ABDE | Identification PA : Bourguignon |
| 9 | 861 | 870 | C | Identification PA : Bourguignon |
| 10 | 862 | 870 | ABCDE | Galénique |
| 11 | 862 | 871 | ABC | Le droit pharma |
| 12 | 862 | 871 | CDE | BUM |
| 13 | 862 | 871 | BCDE | Le droit pharma |
| 14 | 862 | 872 | BDE | PK PD |
| 15 | 863 | 872 | ABCD | BUM |
| 16 | 863 | 873 | ABCE | BUM |
| 17 | 863 | 873 | AB | BUM |
| 18 | 863 | 873 | ABD | BUM |
| 19 | 864 | 874 | E | Développement clinique |

**Réserves à afficher après correction :**

- Q1 D — D valide l’absence de toute disposition sur les médicaments vétérinaires dans le CSP, sans justification. Vérifie ce champ dans la version de la ronéo Le droit pharma utilisée pour ce sujet ; la clé ACDE est conservée. [Sujet p860, corrigé p867 ; possible_error]
- Q2 C — L’origine fongique de l’ergotamine est fausse ici, mais vraie en 2021–2022 S1 Q4A. La justification évoque elle-même l’ergot de seigle. Vérifie ce point dans la ronéo Sources naturelles ; la clé ADE est conservée. [Sujet p860, corrigé p867 ; source_conflict]
- Q3 B — Le corrigé signale lui-même une possible coquille « BFP » pour « BPF », puis invoque leur harmonisation mondiale. Vérifie ces deux motifs distincts dans la ronéo Analyse & contrôles des médicaments ; la clé AD est conservée. [Sujet p860, corrigé p868 ; source_uncertainty]
- Q4 C — C est rejeté au motif que « le score docking n’existe pas » et qu’il s’agirait du « SCORING ». Vérifie la terminologie et les types de complexes évalués dans la ronéo Conception rationnelle ; la clé BDE est conservée. [Sujet p860, corrigé p868 ; source_uncertainty]
- Q6 E — La production d’érythropoïétine humaine active par E. coli est vraie ici, mais la même proposition est fausse en 2022–2023 S2 Q5E. Vérifie le système de production et l’activité de la protéine dans la ronéo Biotechnologies ; la clé BCDE est conservée. [Sujet p861, corrigé p869 ; source_conflict]
- Q9 D — La proposition évoque les modélisations mathématique et informatique du criblage virtuel, mais la justification répond seulement « modèle biomathématique = biologie + maths ». Vérifie le motif du verdict dans la ronéo Identification PA ; la clé C est conservée. [Sujet p861, corrigé p870 ; possible_error]
- Q14 A — L’ajustement des doses par les paramètres pharmacocinétiques est faux ici, mais vrai en 2022–2023 S1 Q18A. Vérifie ce point dans la ronéo PK PD ; la clé BDE est conservée. [Sujet p862, corrigé p872 ; source_conflict]
- Q14 C — La justification propose un espacement « toutes les 5 demi-vies », alors que B/D évoquent le délai d’équilibre. Vérifie la distinction entre intervalle des doses et temps d’équilibre dans la ronéo PK PD. [Sujet p862, corrigé p872 ; possible_error]
- Q14 E — E valide un volume de distribution ne pouvant pas dépasser le volume sanguin. Vérifie cette borne et la définition du volume apparent de distribution dans la ronéo PK PD ; le verdict imprimé est conservé. [Sujet p862, corrigé p872 ; possible_error]
- Q19 D,E — La justification de D parle de « biosimilarité des produits génériques » ; E retient un intervalle 80–125 % sur la demi-vie. Vérifie la distinction bioéquivalence/biosimilarité et les paramètres à comparer dans la ronéo Développement clinique ; la clé E est conservée. [Sujet p864, corrigé p874 ; possible_error]

**Cas mixtes conservés entiers :**

- Q8 → Identification PA : Bourguignon : Séries chimiques d’AINS et représentation de Markush liée à l’exploration d’analogues.
- Q11 → Le droit pharma : Mentions obligatoires de l’étiquetage d’une spécialité pharmaceutique.
- Q13 → Le droit pharma : Encadrement de l’industrie pharmaceutique, sanctions et communication sur ses produits.
- Q15 → BUM : Critères de choix et de prescription adaptés au patient, aux bénéfices et aux risques.
- Q18 → BUM : Prévention des erreurs, suivi de l’observance et adaptation aux populations à risque.
- Q19 → Développement clinique : Études comparatives et critères de démonstration nécessaires à l’AMM d’un biosimilaire.

### 2020-2021 — S1

25 QCM et 125 items relus. Grille p884, sujets p876–882, corrigés p885–895.

| QCM | Sujet | Corrigé | Clé conservée | Thème proposé |
|---:|---:|---:|---|---|
| 1 | 876 | 885 | ABCE | Développement clinique |
| 2 | 876 | 885 | ABDE | Cibles, mécanisme & actions |
| 3 | 876 | 886 | ABCE | Sources naturelles - Kerzaon |
| 4 | 876 | 886 | CE | Sources naturelles - Kerzaon |
| 5 | 877 | 887 | ABD | Analyse & contrôles des médicaments |
| 6 | 877 | 887 | BCDE | Biotechnologies |
| 7 | 877 | 887 | C | Biotechnologies |
| 8 | 877 | 888 | B | Conception rationnelle : Terreux |
| 9 | 878 | 889 | B | Conception rationnelle : Terreux |
| 10 | 878 | 889 | ADE | Identification PA : Bourguignon |
| 11 | 878 | 890 | BDE | Chimie organique |
| 12 | 879 | 890 | BD | Identification PA : Bourguignon |
| 13 | 879 | 890 | ABD | Galénique |
| 14 | 879 | 891 | ADE | Galénique |
| 15 | 879 | 891 | E | Galénique |
| 16 | 879 | 892 | AB | PK PD |
| 17 | 880 | 892 | ACDE | Iatrogénie |
| 18 | 880 | 892 | B | Balance bénéfice/risque |
| 19 | 880 | 893 | ABD | Balance bénéfice/risque |
| 20 | 880 | 893 | ABCD | Le droit pharma |
| 21 | 881 | 894 | A | Le droit pharma |
| 22 | 881 | 894 | ABD | BUM |
| 23 | 881 | 895 | BC | Iatrogénie |
| 24 | 881 | 895 | BCD | BUM |
| 25 | 882 | 895 | ABCDE | BUM |

**Réserves à afficher après correction :**

- Q4 C — Le corrigé cite Aggrastat et Integrilin pour valider la catégorie « anticoagulants ». Vérifie la classe pharmacologique précise de ces exemples dans la ronéo Sources naturelles ; la clé CE est conservée. [Sujet p876, corrigé p886 ; possible_error]
- Q4 E — E regroupe cytarabine et vidarabine sous une application anticancéreuse. Vérifie séparément l’activité attribuée à chaque molécule dans la ronéo Sources naturelles ; le verdict imprimé est conservé. [Sujet p876, corrigé p886 ; possible_error]
- Q6 A — La justification remplace globalement « production de molécules synthétiques chimiques » par « hémisynthèse ». Vérifie la distinction entre synthèse chimique et hémisynthèse dans la ronéo Biotechnologies ; la clé BCDE est conservée. [Sujet p877, corrigé p887 ; possible_error]
- Q7 B — La justification assimile « knock-out » à une simple sous-expression. Vérifie la distinction entre inactivation et diminution d’expression dans la ronéo Biotechnologies ; le verdict imprimé est conservé. [Sujet p877, corrigé p887 ; possible_error]
- Q7 C,D — Le corrigé valide les modèles « in vitro » et rejette les modèles « in vivo » pour la transgenèse animale. Vérifie cette opposition dans la ronéo Biotechnologies ; la clé C est conservée. [Sujet p877, corrigé p887 ; possible_error]
- Q10 C — L’item vise les acides 3-phénylpropioniques, alors que la justification compare aussi les 3-indolylacétiques aux 2-phénylpropioniques. Vérifie les familles réellement comparées dans la ronéo Identification PA ; la clé ADE est conservée. [Sujet p878, corrigé p889 ; source_uncertainty]
- Q12 A — Le corrigé impose la même indication à tout « me-too compound », sans autre précision. Vérifie la portée de cette condition dans la ronéo Identification PA ; la clé BD est conservée. [Sujet p879, corrigé p890 ; source_uncertainty]
- Q16 E — La justification associe l’antagonisme non compétitif à une hausse de CE50 et une baisse d’Emax. Vérifie le modèle de courbe et les paramètres concernés dans la ronéo PK PD ; la clé AB est conservée. [Sujet p879, corrigé p892 ; possible_error]
- Q18 A — La justification décrit les déclarations des professionnels comme reposant sur le « volontariat ». Vérifie le cadre de déclaration retenu par la version de la ronéo Balance bénéfice/risque utilisée pour ce sujet ; la clé B est conservée. [Sujet p880, corrigé p892 ; source_uncertainty]
- Q21 B,E — B et E sont strictement identiques dans le sujet et tous deux faux dans le corrigé. Le doublon source est conservé ; vérifie la distinction transfert/regroupement dans la ronéo Le droit pharma. [Sujet p881, corrigé p894 ; source_uncertainty]
- Q22 E — La consigne demande ce qui « peut » figurer sur une ordonnance, mais la justification de E rappelle seulement la durée du traitement à spécifier. Vérifie la portée attendue de la consigne dans la ronéo BUM ; la clé ABD est conservée. [Sujet p881, corrigé p894 ; source_uncertainty]
- Q23 E — Le correcteur écrit « pour moi le très rend l’item faux » : la réserve porte sur ce degré de prévisibilité. Vérifie la formulation attendue dans la ronéo Iatrogénie ; la clé BC est conservée. [Sujet p881, corrigé p895 ; source_uncertainty]

**Cas mixtes conservés entiers :**

- Q1 → Développement clinique : Éthique des recherches chez l’être humain : protocole, risques, placebo et consentement selon Helsinki.
- Q2 → Cibles, mécanisme & actions : Mécanismes d’action des anticorps monoclonaux : reconnaissance antigénique, cytotoxicité, macrophages et cellules tumorales.
- Q3 → Sources naturelles - Kerzaon : Intérêt et exploration des molécules naturelles, ethnopharmacologie et modes d’obtention de principes actifs.
- Q10 → Identification PA : Bourguignon : Conception et optimisation de petites molécules bioactives, Markush et modulation structurale.
- Q11 → Chimie organique : Trois items portent sur chiralité, pouvoir rotatoire du racémique et synthèse énantiosélective ; deux portent sur la pharmacomodulation.
- Q17 → Iatrogénie : Interactions médicamenteuses/alimentaires et toxicité liées aux cytochromes P450, avec leur variabilité génétique.
- Q22 → BUM : Contenu d’une ordonnance et informations utiles à la prescription adaptée au patient.
- Q24 → BUM : Dossier pharmaceutique, coordination des soins et prévention des risques d’automédication.
- Q25 → BUM : Prescription individualisée, règle des 5B et information médicale, avec des déterminants PK de réponse.

## Traces de contrôle et limites

`audit.json` contient une ligne de contrôle pour chaque QCM et les sept résolutions visuelles. `reviews.json` contient une vérification séparée A, B, C, D, E, les pages justificatives, les notes et le classement. Les fichiers `assignments*.json` conservent les décisions sujet par sujet ; `packets.py` et `verify_reviews.py` permettent de reproduire les rapprochements.

La conformité à la transcription ne garantit pas que le corrigé pédagogique est scientifiquement exact. Les divergences sont conservées avec une réserve ciblée et un renvoi à la ronéo. Les notes juridiques ne présentent aucune règle comme actuellement en vigueur ; elles invitent à vérifier la version du cours sur le point précis.

Aucun HTML, aucune banque source ni aucune autre UE n’a été modifié. Les données de progression sont hors du périmètre de cet agent.
