# Révision V4 — lot UE2 / UE3

## Résultat et périmètre

817 fiches initiales ont été examinées : 315 de biologie moléculaire, 364 de biochimie/chimie physique et 138 de biostatistiques. Les 231 fiches de biomol ED, traduction et régulation sont déléguées à root et listées séparément dans `delegated_to_root.json` ; elles ne sont pas revendiquées dans cette couverture. Trois QCM intégralement présents dans les sources ont été récupérés et relus, portant le périmètre livré à 820 fiches.

La couverture compte **4 096 propositions substantiellement relues sur 4 097 propositions disponibles**. La seule proposition non vérifiable est ADN annales17E, tronquée dans le PDF lui-même. Intro autotest10 est un exercice de correspondance sans propositions A–E : son contenu a été examiné, mais aucun item de QCM n’est comptabilisé.

Les **87 notes portent sur 86 questions** : 18 notes UE3, 48 de biochimie/chimie physique et 21 de biomol. Les notes signalent une difficulté précise ; les questions sans note ne sont pas certifiées scientifiquement exactes. Les clés de référence sont conservées pour les désaccords scientifiques. Les seules clés restaurées le sont à partir de preuves textuelles explicites, dans le fichier de réparations distinct.

| Nature des notes | Nombre | Sens |
|---|---:|---|
| Conflit avec une ronéo fournie | 21 | Renvoi réel au fichier et à la page ; certaines conclusions utilisent la structure ou la formule du cours. |
| Contradiction interne de la source | 22 | Clé/commentaire divergents, données incompatibles, calcul ou figure contradictoire. |
| Erreur possible / limite de formulation | 38 | Réserve expliquée ; cours manquant ou convention à faire confirmer. |
| Convention ancienne de bilan énergétique | 5 | Rapports P/O historiques ; pas de remplacement automatique de la clé. |
| Référence manquante | 1 | ADN17E incomplet dans le document source. |

## Méthode de relecture

Les propositions, la consigne, le contexte commun et les explications ont été lus. Les lettres des 87 notes ont été recroisées avec les options et la clé de la bonne question. Aucun item signalé ne se rattache à une consigne inversée non prise en compte. Les calculs diagnostiques, intervalles, tests et bilans signalés ont été refaits. Les figures nécessaires ont été consultées : structures de lipides et de glucides, projections stéréochimiques, configurations électroniques, formules et graphes UE3. Les simples images reproduisant un texte déjà lisible n’ont pas été transformées en revendication de validation scientifique.

Le contrôle final des images a retiré un faux positif : glucides2025s1 Q1E. La structure 3 est un L-glucose et non un L-galactose ; elle n’est donc pas l’énantiomère de la structure 2. La note envisagée a été supprimée. Les hypothèses non retenues sur les siARN de laboratoire, la mutation non codante de MET et l’EPA ont également été écartées lorsque le cours fourni précisait la convention employée.

Les 278 fiches `reviewed_with_course` ont bénéficié d’un cours consulté sur au moins les notions concernées, parfois seulement une partie des items. Les 540 fiches `reviewed_without_course` ont été relues sans cours couvrant leur chapitre. Les deux fiches `needs_source` sont les cas incomplet ou non transformable en QCM décrits plus haut. Cette distinction évite d’assimiler une lecture complète de la banque à une confirmation intégrale par les ronéos.

## Récupération exacte de QCM perdus

Les trois QCM suivants avaient été absorbés dans le dernier item du QCM précédent. `source_repairs.json` contient leur enregistrement complet, les explications originales, la clé et une position d’insertion visuelle. Les anciens identifiants ne sont pas renumérotés.

| Banque / nouvel ID | QCM source | Clé | Sujet | Corrigé | Ancien item à nettoyer |
|---|---|---|---|---|---|
| `ue2.arn.annales` / 28 | 2020–2021 PACE, X, Les ARN de transfert | BDE | Annales ARN ENONCE p4 | Annales ARN CORRECTION p6 | 17E |
| `ue2.arn.annales` / 29 | 2020–2021 PASS S2, X, Les petits ARN non codants | ADE | Annales ARN ENONCE p4 | Annales ARN CORRECTION p6 | 18E |
| `ue2.anomalies.annales` / 9 | 2020–2021, 15’, insertion de trois nucléotides | BE | Annales Anomalies ENONCE p1 | Annales Anomalies CORRECTION p2 | 4E |

Les explications de leurs prédécesseurs étaient aussi contaminées : ARN17 retrouve son seul commentaire C sur les miARN sanguins ; ARN18 retrouve A/D sur les ARNt ; Anomalies4 retrouve A sur la définition du polymorphisme. Les trois clés déjà existantes ABCDE, BCE et A restent inchangées. La justification officielle A du nouveau ARN28 est conservée mais annotée : les ARNt nucléaires ne sont pas formés dans le cytoplasme (cours transcription p4 et p10).

## Clés effectivement présentes mais non extraites

| Banque / IDs | Clés restaurées | Preuve |
|---|---|---|
| Transcription autotests 29–32 | DE, AD, BD, CD | Autotests Transcription CORRECTION p6 : clés autonomes après chaque QCM Wooclap |
| Transcription autotests 33–35 | BD, ACD, ADE | Même corrigé p7 |
| Transcription annales 17–19 | BD, B, BCE | Sujet p4 numéros 1’/2’/3’ ; corrigé p6 numéros 10/11/12 ; cinq propositions identiques |
| Réplication annales18 | ACD | Sujet p4 Q39’ ; corrigé p6 Q39 puis clé 39’ ACD |
| Réparation annales11 | BDE | Q9 en bas du corrigé p3 ; clé isolée au début de p4 |
| Anomalies autotest1 | Tout faux explicite | Cinq verdicts Faux p1 ; `answer:""`, `answerIsEmpty:true` |

Ces cas constituent **12 clés non vides rétablies et un cas tout faux rendu explicite**. Le moteur doit utiliser `answerIsEmpty:true` pour ce dernier. Onze autres retouches retirent uniquement des titres d’année ou de section collés en fin d’item. Au total : 27 patches, plus trois additions. Les preuves et champs exacts sont dans `source_repairs.json`.

### Ambiguïtés préservées

- ADN annales25 : le corrigé p8 imprime **AD(E)**, puis E Faux avec réserve sur « l’intention du prof ». Clé vide conservée.
- ARN annales26 : le corrigé p9 imprime **AB(C)**, puis C Faux avec discussion de formulation. Clé vide conservée.
- Transcription annales33 : même QCM et même ambiguïté **AB(C)**, corrigé p10. Clé vide conservée.
- Les discordances déjà signalées en biochimie et UE3 ne sont pas converties en nouvelles clés.

## Résultats scientifiques saillants

Les contre-sources les plus directement exploitables portent sur la solubilité des triglycérides dans l’acétone ; les liaisons amide des sphingolipides ; le squelette sphingosine et la liaison β(1→1) communs au lactosylcéramide et à GM3 ; le rôle estérifiant de l’ACAT ; le précurseur triterpénique du cholestérol ; la fonction pseudo-cétonique du fructose ; le caractère non réducteur de l’inuline ; les électrons non appariés du silicium ; l’ion hydrogénoïde Li2+ ; les ARNt nucléaires ; le facteur VIII de l’hémophilie A et la condition « non multiple de trois » pour un frameshift.

En UE3, les réserves les plus fortes sont démontrées par les données internes : un rapport de vraisemblance multiplie les cotes et non la probabilité ; la VPP du Q9 2024–2025 vaut 2/3 ; plusieurs statistiques imposées sont incompatibles avec n/r ou les moyennes/écarts types annoncés ; la clé CD de l’intervalle binomial 2023–2024 ne correspond à aucune des deux conventions d’arrondi envisagées. Aucun de ces calculs n’est présenté comme validé par une ronéo UE3 absente.

## Cours disponibles et limites

Les références exactes et pages consultées sont indiquées dans chaque note et dans la couverture. Le texte OCR de 105 pages de ronéos illustrées est dans `courses_ocr.json` ; les figures décisives ont été examinées directement, car une OCR ne suffit pas pour lire une liaison ou une stéréochimie.

- Lipides : intro/AG du 21.09.26 ; AG2 du 03.10.25 ; lipides simples du 06.10.25 ; lipides complexes des 28.09 et 05.10.26 ; dérivés isopréniques du 09.10.26 ; éicosanoïdes26.
- Glucides : ronéos du 09.10.26 et du 23.10.26.
- Chimie physique : chapitres1–2 (atome/configurations),3 (propriétés),5 (liaisons/interactions) et6 (thermodynamique/équilibres). Le chapitre4 est disponible dans les fichiers mais n’a pas été utilisé comme preuve directe des notes.
- Biomol : `downloadfile(1).PDF`, cours de23pages « Transcription et maturation », d’après Pr Janin ; `3. FS Anomalies du génome LS.pdf`, fiche de3pages. La fiche condensée `downloadfile.PDF` est disponible mais n’a pas été substituée au cours de23pages pour les preuves.

**Cours prioritaires manquants** : UE3 (estimation, tests, performances diagnostiques, épidémiologie) ; biochimie des protéines et enzymologie ; glycolyse/néoglucogenèse, glycogène, β-oxydation et bilans de chaîne respiratoire ; chimie organique/stéréochimie et réactivité des carbonyles ; biomol ADN mitochondrial, ARN et catabolisme des bases, organisation du génome, réplication et réparation comparée Homme/E. coli. La version complète de l’item ADN17E est nécessaire séparément.

Plusieurs réserves concernent un cours simplifié ou une convention ancienne plutôt qu’un mauvais appariement : bilans130/11/5ATP, MMR humain assimilé au système bactérien, terminaison de PolII assimilée au clivage3′, liquidité pure/mélange en thermodynamique. Les notes explicitent ce niveau d’incertitude.

## Fichiers d’intégration

- `notes.json` : 87 annotations ; champs de la convention V4.
- `source_repairs.json` : 3 additions et27 patches exacts ; aucune édition du site par cet agent.
- `coverage.json` : 820 lignes (817 initiales +3 ajouts), avec `noteIds` indexés à partir de0.
- `coverage_baseline.json` et `coverage_additions.json` : partitions de la couverture.
- `delegated_to_root.json` : 231 questions hors de ce lot.
- `review_summary.json` : compteurs et sens de la couverture.
- `alignment_report.md` : relecture des lettres, options et clés des questions annotées.

## Catalogue des notes

Les numéros ci-dessous sont un affichage à partir de1 ; les indices de `coverage.json` commencent à0.

### 1. annales.ue3.2024-2025.s1 / 9 — items D, E

**source_conflict** — D est donné vrai et E faux, mais le calcul du corrigé aboutit lui-même à une VPP de 2/3. RV+ = 0,60/(1−0,90) = 6 multiplie l’odds pré-test (1/3), donnant une odds post-test de 2 et une probabilité de 2/3. Il ne multiplie pas la probabilité par 6. Les verdicts scientifiquement cohérents sont donc D faux et E vrai. Clé du tutorat conservée ; ce désaccord est démontré par les données et le calcul figurant dans la source, sans prétendre à une validation par une ronéo UE3 indisponible.

Sources : Sujets + corrections compilés.pdf, p509 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p518 (Correction du tutorat fournie).

### 2. annales.ue3.2024-2025.s1 / 8 — items B

**source_conflict** — Le corrigé rejette B mais explique sous A que l’on compare deux proportions indépendantes. Les 200 lésions supplémentaires forment un groupe distinct des 200 premières : l’écart réduit pour deux proportions indépendantes proposé en B est approprié sous ses conditions usuelles. Avec 0,60 et 0,70, n1=n2=200 et la proportion commune 0,65, |z|≈2,10 ; il ne s’agit pas des données appariées du QCM 7. B devrait être vrai. Clé source conservée ; voir la ronéo UE3 sur les comparaisons de proportions pour confirmation pédagogique.

Sources : Sujets + corrections compilés.pdf, p508 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p517 (Correction du tutorat fournie).

### 3. annales.ue3.2023-2024.s1 / 2 — items B, C, D, E

**source_conflict** — La clé CD est incohérente : C et D proposent deux bornes supérieures différentes, 0,19 et 0,20. Avec f=75/500=0,15, la demi-largeur vaut 1,96×√(0,15×0,85/500)≈0,03130. L’arrondi usuel des bornes donne [0,12 ; 0,18], donc E ; l’arrondi conservateur de la demi-largeur à 0,04 appliqué explicitement par le corrigé donne [0,11 ; 0,19], donc BC. Aucune de ces conventions ne donne CD. La ronéo UE3 « Estimation » doit préciser la convention d’arrondi ; la clé du tutorat est conservée.

Sources : Sujets + corrections compilés.pdf, p534 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p542 (Correction du tutorat fournie).

### 4. annales.ue3.2025-2026.s1 / 5 — items D, E

**source_conflict** — Les verdicts D vrai et E faux suivent la statistique t=−2,000 imposée dans l’énoncé. Mais les données de l’exercice (8 patientes par groupe, moyennes −3 et −2,5, écarts types 0,3 et 0,4) et la variance commune 0,125 calculée en B donnent t=−0,5/√[0,125(1/8+1/8)]≈−2,828, pas −2. Avec 14 degrés de liberté, cela conduit à p≈0,0135 et au rejet à 5 %. C’est une incohérence de données de la source, pas une raison de changer les réponses attendues lorsque t=−2 est imposé. La ronéo « Comparaison de deux moyennes » est nécessaire pour la validation de cours.

Sources : Sujets + corrections compilés.pdf, p489 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p498 (Correction du tutorat fournie).

### 5. annales.ue3.2024-2025.s1 / 11 — items D, E

**source_conflict** — Le corrigé utilise r/t=0,64/2,79≈0,23 pour valider E, conformément à la statistique fournie. Cependant n=28 et r=0,64 donnent, pour le test usuel de Pearson, t=r√[(n−2)/(1−r²)]≈4,25 et √[(1−r²)/(n−2)]≈0,151. Les valeurs r, n et t de l’énoncé ne sont donc pas compatibles entre elles. Conserver la clé du tutorat si l’on utilise le t imposé ; ne pas apprendre 0,23 comme résultat cohérent des trois données. Ronéo requise : UE3 corrélation et régression.

Sources : Sujets + corrections compilés.pdf, p509 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p520 (Correction du tutorat fournie).

### 6. annales.ue3.2022-2023.s1 / 2 — items E

**possible_error** — E est donné faux alors qu’il concerne la moyenne observée m, et non la vraie moyenne μ. L’intervalle calculé ici a la forme m ± u×s/√n : son centre m y appartient par construction. L’explication du corrigé (« aucune certitude absolue ») concerne la couverture de μ et ne réfute pas E. E devrait être vrai pour l’intervalle de l’exercice. À confirmer dans la ronéo UE3 « Estimation » ; clé du tutorat conservée.

Sources : Sujets + corrections compilés.pdf, p560 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p568 (Correction du tutorat fournie).

### 7. annales.ue3.2022-2023.s1 / 5 — items A, B, C, E

**source_conflict** — La source est contradictoire : son en-tête annonce BCE, mais ses explications déclarent A vrai, B faux, C vrai, D faux et E vrai, soit ACE. H0 porte bien sur les espérances, pas sur les moyennes observées ; avec 26 degrés de liberté, 2,053<2,056, on ne rejette pas à 5 %. La clé vide du site ne signifie donc pas que toutes les propositions sont scientifiquement fausses. Aucun choix entre les clés contradictoires de la source ne doit être fait silencieusement. Ronéo requise : UE3 tests de comparaison de moyennes.

Sources : Sujets + corrections compilés.pdf, p561 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p570 (Correction du tutorat fournie).

### 8. annales.ue3.2022-2023.s2 / 3 — items B

**possible_error** — B est donné faux au motif que H0 serait m=3,00. C’est l’inverse : l’hypothèse nulle porte sur l’espérance inconnue μ de la population, H0: μ=3,00 ; m=2,70 est la moyenne déjà observée. B devrait donc être vrai. Le verdict de la source est conservé ; confirmation pédagogique à demander à la ronéo UE3 « Tests d’hypothèses / comparaison d’une moyenne à une référence ».

Sources : Sujets + corrections compilés.pdf, p579 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p584 (Correction du tutorat fournie).

### 9. annales.ue3.2022-2023.s2 / 4 — items E

**possible_error** — E est donné faux avec une explication sur la prévalence, alors que l’item compare deux probabilités conditionnelles : détecter les malades (sensibilité 96 %) et classer les non-malades (spécificité 88 %). Puisque 96 % > 88 %, E est vrai dans les données de l’exercice. La prévalence n’intervient pas dans cette comparaison. Clé du tutorat conservée ; à confirmer dans la ronéo UE3 sur les performances diagnostiques.

Sources : Sujets + corrections compilés.pdf, p579 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p585 (Correction du tutorat fournie).

### 10. annales.ue3.2021-2022.s1 / 9 — items E

**possible_error** — Le corrigé rejette E parce que les proportions restent identiques. Pourtant l’écart réduit divise la différence de proportions par une erreur-type qui augmente lorsque les effectifs diminuent. À proportions et allocation relatives identiques, des effectifs plus faibles donnent un |z| plus faible (et un χ²=z² plus faible). E devrait être vrai dans cette comparaison. Clé source conservée ; ronéo requise : UE3 comparaison de deux proportions indépendantes.

Sources : Sujets + corrections compilés.pdf, p592 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p601 (Correction du tutorat fournie).

### 11. annales.ue3.2020-2021.s2 / 3 — items B, E

**possible_error** — La variable individuelle codée 0/1 est bien une Bernoulli de paramètre π inconnu : B devrait être vrai. Le nombre de personnes atteintes suit une binomiale B(36,π), mais π n’est pas connu égal à 0,33 ; 12/36≈0,33 n’en est qu’une estimation. E confond le paramètre et son estimation et devrait être faux dans sa formulation. La clé ACDE du tutorat est conservée ; à confirmer dans les ronéos UE3 « Lois de probabilité » et « Estimation ».

Sources : Sujets + corrections compilés.pdf, p652 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p657 (Correction du tutorat fournie).

### 12. annales.ue3.2020-2021.s2 / 5 — items A, B

**source_conflict** — La clé BCD classe cette étude comme cas-témoins. L’énoncé décrit pourtant des femmes sélectionnées selon leur appartenance au programme Valériane puis suivies pendant la grossesse, avec observation ultérieure des complications : c’est une cohorte (A), pas un recrutement selon la présence préalable de complications (B). Les groupes ne sont pas formés sur le critère de jugement. A devrait être vrai et B faux. Clé du tutorat conservée ; à confronter à la ronéo UE3 « Designs d’étude en épidémiologie ».

Sources : Sujets + corrections compilés.pdf, p653 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p659 (Correction du tutorat fournie).

### 13. annales.ue3.2018-2019.paces / 8 — items D

**possible_error** — Le calcul 1/(0,091−0,090)=1000 concerne un événement cardiovasculaire évité à 8 ans, qui est le critère recueilli dans l’énoncé. D remplace ce critère par un décès ; les données ne donnent pas le nombre de décès et ne permettent pas d’en déduire ce nombre nécessaire à traiter. D n’est donc pas justifié tel qu’il est écrit, même si le calcul 1000 est correct pour les événements cardiovasculaires. Clé source conservée ; voir la ronéo UE3 sur le nombre nécessaire à traiter et la définition du critère de jugement.

Sources : Sujets + corrections compilés.pdf, p686 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p696 (Correction du tutorat fournie).

### 14. annales.ue3.2024-2025.s2 / 3 — items A

**source_conflict** — Le verdict A faux est cohérent avec le test de Student à 10 degrés de liberté de l’exercice précédent. En revanche, l’explication recopie « la statistique du test suit une loi Normale », ce qui affirme précisément l’item déclaré faux. Il faut lire ici « suit une loi de Student sous H0 ». La lettre de réponse reste inchangée ; cette note corrige seulement la contradiction du commentaire source.

Sources : Sujets + corrections compilés.pdf, p522 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p528 (Correction du tutorat fournie).

### 15. annales.ue3.2023-2024.s2 / 6 — items E

**source_conflict** — E est correctement vrai : l’odds ratio du handicap léger ou nul est supérieur à 1. Mais l’explication parle d’un « facteur aggravant ». L’événement est favorable : le handicap léger ou nul est plus fréquent sous thrombectomie (30/150 contre 3/150), ce qui est un bénéfice pour ce critère, pas une aggravation. Le verdict est conservé ; seule l’interprétation verbale du corrigé est contestée.

Sources : Sujets + corrections compilés.pdf, p551 (Énoncé fourni) ; Sujets + corrections compilés.pdf, p558 (Correction du tutorat fournie).

### 16. annales.ue3.2020-2021.paces / 6 — items D

**source_conflict** — D est donné faux, mais l’explication indique que la courbe HNC-LL est au-dessus de l’autre et que HNC-LL discrimine mieux. C’est précisément le sens pédagogique de distributions mieux séparées entre formes graves et non graves proposé en D. La figure confirme la meilleure discrimination de HNC-LL sur les seuils représentés. Verdict litigieux à revoir avec la ronéo UE3 sur courbes ROC et distributions des marqueurs ; la distance brute entre scores n’est pas comparable sans tenir compte de leur échelle. Clé du tutorat conservée.

Sources : Sujets + corrections compilés.pdf, p616 (Énoncé et figure) ; Sujets + corrections compilés.pdf, p628 (Corrigé fourni).

### 17. annales.ue3.2024-2025.s1 / 1 — items B

**source_conflict** — Le verdict B faux est cohérent. En revanche, le commentaire attribue les 5 % à la probabilité conjointe « très insatisfait et groupe 1 ». Le diagramme donne P(très insatisfait | groupe 1)=5 %, soit 10 personnes parmi les 200 du groupe 1 ; sur les 400 personnes, la probabilité conjointe vaut 10/400=2,5 %. P(groupe 1 | très insatisfait)=10/(10+20)=1/3. Il faut corriger l’interprétation du commentaire, sans changer le verdict B.

Sources : Sujets + corrections compilés.pdf, p506 (Énoncé et figure) ; Sujets + corrections compilés.pdf, p513 (Corrigé fourni).

### 18. annales.ue3.2023-2024.s1 / 6 — items E

**source_conflict** — Le verdict E vrai concerne correctement la significativité à 5 %, mais l’item comporte aussi le fragment « 0,01 < p-valeur < 0,02 ». Avec t=1,7/0,45≈3,78 et 30 degrés de liberté, p bilatérale≈0,00070 : cet encadrement est faux. Le corrigé ne justifie que la significativité et laisse ce fragment inexpliqué. C’est une anomalie déjà présente dans l’énoncé source ; ne pas apprendre l’encadrement imprimé comme vrai. Clé source conservée.

Sources : Sujets + corrections compilés.pdf, p535 (Énoncé et figure) ; Sujets + corrections compilés.pdf, p544 (Corrigé fourni).

### 19. annales.ue2c.lipides.2024s1 / 3 — items C

**roneo_conflict** — C est écarté sur une hypothèse explicite du corrigé (« protecteurs » donc peu oxydables). Ce raisonnement confond effet physiologique et sensibilité chimique : la ronéo décrit la peroxydation des acides gras polyinsaturés et leur protection par la vitamine E. Les multiples doubles liaisons des ω3 les rendent sensibles à cette peroxydation ; leur rôle protecteur cardiovasculaire ne permet pas de rejeter C.

Sources : Sujets + corrections compilés.pdf, p53 (Énoncé fourni, Q30) ; Sujets + corrections compilés.pdf, p73 (Correction de référence) ; Sujets + corrections compilés.pdf, p74 (Suite de la correction de référence) ; Ronéo cours AG2 du vendredi 03.10.25.pdf, p8 (Peroxydation lipidique des AG polyinsaturés) ; Ronéo cours AG2 du vendredi 03.10.25.pdf, p9 (Protection antioxydante des AGPI).

### 20. annales.ue2c.lipides.2024s1 / 4 — items C

**roneo_conflict** — C est donné vrai alors qu’il affirme l’insolubilité des triglycérides dans l’acétone. La ronéo indique explicitement que les glycérides sont solubles dans l’acétone et insolubles dans l’eau. C devrait donc être faux.

Sources : Sujets + corrections compilés.pdf, p54 (Énoncé fourni, Q31) ; Sujets + corrections compilés.pdf, p74 (Correction de référence) ; Ronéo lipides simples du lundi 06.10.25.docx.pdf, p4 (Propriétés physiques : solubilité dans l’acétone).

### 21. annales.ue2c.lipides.2024s1 / 6 — items C

**roneo_conflict** — Le 2-arachidonoylglycérol est un monoacylglycérol : son squelette est du glycérol estérifié par un acide gras. La classification de la ronéo distingue ces glycérides des sphingolipides construits sur une base sphingoïde. Le qualifier de lysosphingolipide (C donné vrai) est donc incompatible avec cette structure.

Sources : Sujets + corrections compilés.pdf, p54 (Énoncé fourni, Q33) ; Sujets + corrections compilés.pdf, p75 (Correction de référence) ; Ronéo lipides simples du lundi 06.10.25.docx.pdf, p2 (Définition des glycérides) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p9 (Sphingosine et céramides).

### 22. annales.ue2c.lipides.2024s1 / 6 — items D

**possible_error** — D est rejeté au motif que le 2-arachidonoylglycérol provient de l’acide arachidonique. Cet argument n’exclut pas un précurseur phosphatidylinositol : un phosphoinositide portant de l’arachidonate peut fournir un diacylglycérol, puis du 2-AG par une DAG-lipase. D paraît donc recevable. Les ronéos lipidiques fournies ne détaillent pas cette voie : à contrôler dans le cours sur les endocannabinoïdes et la signalisation des phosphoinositides avant de conclure au verdict du cours.

Sources : Sujets + corrections compilés.pdf, p54 (Énoncé fourni, Q33) ; Sujets + corrections compilés.pdf, p75 (Correction de référence).

### 23. annales.ue2c.glucides.2024s1 / 2 — items B

**roneo_conflict** — B est donné vrai mais attribue aux formes cycliques du glucose et du fructose une fonction pseudo-aldéhydique commune. Le glucose est un aldose ; le fructose est un cétose et sa cyclisation crée une fonction pseudo-cétonique en C2. La ronéo distingue explicitement ces deux cas.

Sources : Sujets + corrections compilés.pdf, p55 (Énoncé fourni, Q36) ; Sujets + corrections compilés.pdf, p76 (Correction de référence) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p1 (Cyclisation des aldoses : hémiacétal) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p2 (Cyclisation du cétohexose : fonction pseudo-cétonique).

### 24. annales.ue2c.lipides.2023s1 / 6 — items C, E

**roneo_conflict** — C et E sont rejetés alors que les deux molécules conservent le même squelette de lactosylcéramide. Le céramide contient une sphingosine (C vrai) ; le glucose est relié au C1 du céramide par une liaison β(1→1), présente aussi dans GM3 (E vrai). La ronéo montre ce lien pour le lactosylcéramide puis décrit GM3 comme ce noyau portant un résidu d’acide sialique supplémentaire.

Sources : Sujets + corrections compilés.pdf, p115 (Énoncé fourni, Q13) ; Sujets + corrections compilés.pdf, p134 (Correction de référence) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p9 (Céramide = sphingosine et acide gras) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p13 (Lactosylcéramide et liaison β(1→1)) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p16 (GM3 = céramide, deux sucres et NANA).

### 25. annales.ue2c.lipides.2023s1 / 7 — items A

**roneo_conflict** — A est donné faux, mais le squalène C30 est bien un précurseur triterpénique du cholestérol. Le schéma de la ronéo place le squalène en amont du cholestérol. L’explication du corrigé inverse cette filiation et qualifie à tort la vitamine D de triterpène C30.

Sources : Sujets + corrections compilés.pdf, p115 (Énoncé fourni, Q14) ; Sujets + corrections compilés.pdf, p134 (Correction de référence) ; Ronéo cours dérivés isopréniques du vendredi 09.10.26.docx.pdf, p3 (Filiation isoprénique : squalène C30 puis cholestérol) ; Ronéo cours dérivés isopréniques du vendredi 09.10.26.docx.pdf, p4 (Structure et origine du cholestérol).

### 26. annales.ue2c.lipides.2023s2 / 4 — items D

**possible_error** — D est rejeté uniquement parce qu’il écrit « phosphore » au lieu de « phosphate ». La ronéo indique bien une augmentation de l’absorption intestinale du calcium et du phosphate. Dans le vocabulaire nutritionnel et physiologique, l’absorption du phosphore désigne celle de ses formes phosphatées : cette différence de mot ne suffit donc pas à démontrer que l’effet énoncé est faux. Faire confirmer si l’enseignant exige ici cette convention terminologique stricte.

Sources : Sujets + corrections compilés.pdf, p156 (Énoncé fourni, Q21) ; Sujets + corrections compilés.pdf, p169 (Correction de référence) ; Ronéo cours dérivés isopréniques du vendredi 09.10.26.docx.pdf, p13 (Effets intestinaux de la vitamine D : calcium et phosphate).

### 27. annales.ue2c.lipides.2021s1 / 3 — items B, C, E

**roneo_conflict** — La structure est un 1-palmitoyl-2,3-dioléoyl-sn-glycérol. B devrait être faux : le carbone central du glycérol porte quatre substituants distincts, car les deux branches terminales sont estérifiées par des acides gras différents. C devrait être vrai : ce triglycéride est soluble dans l’acétone. E devrait être faux : remplacer les deux oléates par deux stéarates augmente le point de fusion ; le corrigé l’explique lui-même (« c’est l’inverse ») malgré son étiquette VRAI. Les règles de solubilité et de fusion, ainsi que la structure exacte de ce triglycéride, figurent dans la ronéo.

Sources : Sujets + corrections compilés.pdf, p242 (Énoncé fourni, Q27) ; Sujets + corrections compilés.pdf, p264 (Correction de référence) ; Sujets + corrections compilés.pdf, p265 (Suite de la correction de référence) ; Ronéo lipides simples du lundi 06.10.25.docx.pdf, p3 (Même exemple : 1-palmitoyl-2,3-dioléyl-sn-glycérol) ; Ronéo lipides simples du lundi 06.10.25.docx.pdf, p4 (Solubilité et influence des insaturations sur la fusion).

### 28. annales.ue2c.lipides.2021s1 / 6 — items C, E

**roneo_conflict** — C est donné vrai, mais l’ACAT est une acyltransférase qui estérifie le cholestérol ; l’hydrolyse des esters relève d’une hydrolase. La ronéo distingue les deux enzymes. Pour E, le verdict Faux reste justifié par le précurseur immédiat 7-déhydrocholestérol ; en revanche l’explication place à tort le foie et le rein avant la formation du cholécalciférol : les hydroxylations hépatique puis rénale viennent après sa formation cutanée.

Sources : Sujets + corrections compilés.pdf, p243 (Énoncé fourni, Q30) ; Sujets + corrections compilés.pdf, p267 (Correction de référence) ; Ronéo cours dérivés isopréniques du vendredi 09.10.26.docx.pdf, p5 (Estérification par ACAT et hydrolyse) ; Ronéo cours dérivés isopréniques du vendredi 09.10.26.docx.pdf, p13 (Photolyse cutanée puis hydroxylations hépatique et rénale).

### 29. annales.ue2c.lipides.2020s1 / 6 — items A

**roneo_conflict** — A est donné vrai, mais les liaisons entre l’acide gras et la sphingosine des molécules III et IV sont des liaisons amide, pas ester. La ronéo montre la liaison –CO–NH– du céramide. Les quatre liaisons repérées ne peuvent donc pas être toutes des esters.

Sources : Sujets + corrections compilés.pdf, p305 (Énoncé fourni, Q30) ; Sujets + corrections compilés.pdf, p322 (Correction de référence) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p9 (Formation du céramide par une liaison amide) ; Ronéo lipides complexes des lundi 28.09 et 05.10.26.docx.pdf, p13 (Glycosphingolipides à squelette céramide).

### 30. annales.ue2c.glucides.2022s1 / 3 — items E

**roneo_conflict** — Le caractère non réducteur du stachyose est correct, mais E l’appelle un « ose ». Or le stachyose est un tétraholoside, donc un oside hydrolysable constitué de quatre oses, et non un monosaccharide. La ronéo sépare ces deux catégories. Le VRAI du corrigé porte manifestement sur « non réducteur » ; l’item complet contient une impropriété de classification.

Sources : Sujets + corrections compilés.pdf, p184 (Énoncé fourni, Q33) ; Sujets + corrections compilés.pdf, p206 (Correction de référence) ; Sujets + corrections compilés.pdf, p207 (Suite de la correction de référence) ; Ronéo glucides 1 du vendredi 09.10.26.pdf, p2 (Distinction oses / osides) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p11 (Oligosides, raffinose et stachyose).

### 31. annales.ue2c.glucides.2022s2 / 3 — items D

**possible_error** — D est rejeté au motif que l’amylopectine ne réagirait pas avec l’iode. L’amylopectine peut pourtant former une coloration iodée, généralement rouge à violette, distincte du bleu de l’amylose ; le glycogène donne une coloration brun-rouge. La ronéo fournie décrit l’amidon et le glycogène, mais ne détaille pas séparément la couleur de l’amylopectine : faire confirmer D dans le passage du cours consacré aux réactions iodées des polyosides.

Sources : Sujets + corrections compilés.pdf, p218 (Énoncé fourni, Q21) ; Sujets + corrections compilés.pdf, p230 (Correction de référence) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p13 (Amidon : amylose et amylopectine) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p15 (Glycogène et réaction iodée).

### 32. annales.ue2c.glucides.2021s1 / 2 — items E

**roneo_conflict** — Le polyoside représenté est une inuline : le C1 anomérique du glucose et les C2 anomériques des fructoses sont tous engagés dans des liaisons osidiques. Le CH2OH terminal libre n’est pas une fonction hémiacétalique ou hémicétalique réductrice. E, donné vrai sur le seul argument « CH2OH libre », devrait donc être faux. La ronéo montre l’inuline et définit le pouvoir réducteur par une fonction anomérique libre.

Sources : Sujets + corrections compilés.pdf, p244 (Énoncé fourni, Q32) ; Sujets + corrections compilés.pdf, p268 (Correction de référence) ; Sujets + corrections compilés.pdf, p243 (Figure commune des Q31–33) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p8 (Absence de pouvoir réducteur lorsque les fonctions anomériques sont engagées) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p9 (Fonction hémiacétalique libre et pouvoir réducteur) ; Ronéo glucides 2 du vendredi 23.10.26.pdf, p17 (Structure de l’inuline).

### 33. annales.ue2c.glucides.2021s1 / 4 — items E

**source_conflict** — Le QCM reste sans note car le tableau annonce ADE alors que la correction détaillée retient AD. Le désaccord porte sur E : le donneur activé pour la glycogène synthase est l’UDP-glucose, formé à partir de glucose-1-phosphate, et non directement de glucose-6-phosphate. La correction détaillée explique cette distinction. Conserver le signalement de discordance entre les deux clés.

Sources : Sujets + corrections compilés.pdf, p244 (Énoncé fourni, Q34) ; Sujets + corrections compilés.pdf, p269 (Correction de référence).

### 34. annales.ue2c.metabolisme.2024s1 / 3 — items A, C

**possible_error** — A et C sont donnés vrais, mais la distinction acide gras / acyl-CoA est essentielle. Les acides gras courts et moyens peuvent entrer dans la matrice sans la navette carnitine et y être activés ; cela ne signifie pas que leurs esters acyl-CoA diffusent librement à travers la membrane interne. L’affirmation « tous activés avant l’entrée » et l’explication « acyl-CoA court par diffusion » paraissent donc excessives. La ronéo du transport mitochondrial et de la β-oxydation n’a pas été fournie : ces deux verdicts nécessitent ce chapitre précis.

Sources : Sujets + corrections compilés.pdf, p56 (Énoncé fourni, Q41) ; Sujets + corrections compilés.pdf, p78 (Correction de référence).

### 35. annales.ue2c.metabolisme.2024s2 / 2 — items B

**source_conflict** — B décrit correctement le produit majoritaire libéré par la glycogène phosphorylase : le glucose-1-phosphate. Le corrigé le rejette en écrivant glucose-6-phosphate, qui est le produit de la conversion ultérieure par la phosphoglucomutase. La même compilation, dans le corrigé d’enzymologie Q24 de 2020–2021, décrit explicitement le clivage du glycogène en glucose-1-phosphate. Il s’agit d’une contradiction interne identifiable, même sans ronéo du métabolisme glucidique.

Sources : Sujets + corrections compilés.pdf, p89 (Énoncé fourni, Q24) ; Sujets + corrections compilés.pdf, p106 (Correction de référence) ; Sujets + corrections compilés.pdf, p107 (Suite de la correction de référence) ; Sujets + corrections compilés.pdf, p319 (Q24 : la glycogène phosphorylase libère du glucose-1-phosphate).

### 36. annales.ue2c.metabolisme.2024s2 / 3 — items C

**outdated_reference** — Le bilan de 5 ATP par tour de β-oxydation repose sur l’ancienne convention 3 ATP/NADH et 2 ATP/FADH2. Avec les rapports P/O usuels de 2,5 et 1,5, les deux coenzymes réduits représentent environ 4 ATP ; l’acétyl-CoA est compté séparément. Ce décalage de convention ne justifie pas de remplacer automatiquement la clé historique. Le chapitre actuel sur la chaîne respiratoire et les bilans énergétiques est nécessaire pour savoir quelle convention le concours attend.

Sources : Sujets + corrections compilés.pdf, p90 (Énoncé fourni, Q25) ; Sujets + corrections compilés.pdf, p107 (Correction de référence).

### 37. annales.ue2c.metabolisme.2023s1 / 1 — items C

**possible_error** — L’item est donné faux au motif que le muscle squelettique n’utiliserait pas le lactate qu’il produit. Cette exclusion est trop générale : les fibres oxydatives peuvent utiliser le lactate comme substrat, après conversion en pyruvate et oxydation mitochondriale ; production et utilisation peuvent coexister à l’échelle du muscle. Une lecture limitée au muscle très glycolytique ou au cycle de Cori peut expliquer la simplification. À vérifier dans la ronéo « spécificités tissulaires du métabolisme », partie lactate et échanges intertissulaires, qui n’a pas été fournie.

Sources : Sujets + corrections compilés.pdf, p116 (Énoncé fourni, Q18) ; Sujets + corrections compilés.pdf, p136 (Correction de référence).

### 38. annales.ue2c.metabolisme.2023s2 / 1 — items E

**possible_error** — L’item est donné faux au motif que le muscle squelettique n’utiliserait pas le lactate qu’il produit. Cette exclusion est trop générale : les fibres oxydatives peuvent utiliser le lactate comme substrat, après conversion en pyruvate et oxydation mitochondriale ; production et utilisation peuvent coexister à l’échelle du muscle. Une lecture limitée au muscle très glycolytique ou au cycle de Cori peut expliquer la simplification. À vérifier dans la ronéo « spécificités tissulaires du métabolisme », partie lactate et échanges intertissulaires, qui n’a pas été fournie.

Sources : Sujets + corrections compilés.pdf, p157 (Énoncé fourni, Q24) ; Sujets + corrections compilés.pdf, p170 (Correction de référence).

### 39. annales.ue2c.metabolisme.2022s1 / 1 — items C

**possible_error** — L’item est donné faux au motif que le muscle squelettique n’utiliserait pas le lactate qu’il produit. Cette exclusion est trop générale : les fibres oxydatives peuvent utiliser le lactate comme substrat, après conversion en pyruvate et oxydation mitochondriale ; production et utilisation peuvent coexister à l’échelle du muscle. Une lecture limitée au muscle très glycolytique ou au cycle de Cori peut expliquer la simplification. À vérifier dans la ronéo « spécificités tissulaires du métabolisme », partie lactate et échanges intertissulaires, qui n’a pas été fournie.

Sources : Sujets + corrections compilés.pdf, p184 (Énoncé fourni, Q35) ; Sujets + corrections compilés.pdf, p207 (Correction de référence) ; Sujets + corrections compilés.pdf, p208 (Suite de la correction de référence).

### 40. annales.ue2c.proteines.2022s1 / 1 — items A

**possible_error** — L’explication « non protéinogène » n’autorise pas « jamais retrouvée dans les protéines ». La citrulline peut être présente dans des protéines par citrullination post-traductionnelle de résidus arginine, même si aucun codon standard ne l’incorpore directement lors de la traduction. A paraît donc trop absolu. La ronéo sur les acides aminés et les modifications post-traductionnelles manque pour vérifier la convention attendue.

Sources : Sujets + corrections compilés.pdf, p179 (Énoncé fourni, Q18) ; Sujets + corrections compilés.pdf, p198 (Correction de référence) ; Sujets + corrections compilés.pdf, p199 (Suite de la correction de référence).

### 41. annales.ue2c.metabolisme.2021s1 / 4 — items E

**outdated_reference** — Le nombre 130 ATP relève d’un ancien bilan énergétique du palmitate. Avec 2,5 ATP/NADH, 1,5 ATP/FADH2 et un coût d’activation de deux équivalents ATP, l’oxydation complète d’un palmitate libre donne environ 106 ATP nets : 8×10 + 7×4 − 2. Le résultat dépend donc des rapports P/O et de la convention d’activation ; la clé historique est conservée. La ronéo actuelle « β-oxydation, cycle de Krebs et chaîne respiratoire » est nécessaire pour confirmer les conventions du cours.

Sources : Sujets + corrections compilés.pdf, p245 (Énoncé fourni, Q38) ; Sujets + corrections compilés.pdf, p271 (Correction de référence).

### 42. annales.ue2c.metabolisme.2021s2 / 2 — items D

**outdated_reference** — Le nombre 130 ATP relève d’un ancien bilan énergétique du palmitate. Avec 2,5 ATP/NADH, 1,5 ATP/FADH2 et un coût d’activation de deux équivalents ATP, l’oxydation complète d’un palmitate libre donne environ 106 ATP nets : 8×10 + 7×4 − 2. Le résultat dépend donc des rapports P/O et de la convention d’activation ; la clé historique est conservée. La ronéo actuelle « β-oxydation, cycle de Krebs et chaîne respiratoire » est nécessaire pour confirmer les conventions du cours.

Sources : Sujets + corrections compilés.pdf, p282 (Énoncé fourni, Q23) ; Sujets + corrections compilés.pdf, p296 (Correction de référence).

### 43. annales.ue2c.metabolisme.2018 / 5 — items D

**outdated_reference** — Le nombre 130 ATP relève d’un ancien bilan énergétique du palmitate. Avec 2,5 ATP/NADH, 1,5 ATP/FADH2 et un coût d’activation de deux équivalents ATP, l’oxydation complète d’un palmitate libre donne environ 106 ATP nets : 8×10 + 7×4 − 2. Le résultat dépend donc des rapports P/O et de la convention d’activation ; la clé historique est conservée. La ronéo actuelle « β-oxydation, cycle de Krebs et chaîne respiratoire » est nécessaire pour confirmer les conventions du cours.

Sources : Sujets + corrections compilés.pdf, p456 (Énoncé fourni, Q40) ; Sujets + corrections compilés.pdf, p479 (Correction de référence) ; Sujets + corrections compilés.pdf, p480 (Suite de la correction de référence).

### 44. annales.ue2c.metabolisme.2023s1 / 6 — items A

**outdated_reference** — L’égalité 3 NADH + 1 FADH2 = 11 ATP utilise la convention historique 3 et 2 ATP par coenzyme. Avec les rapports P/O usuels 2,5 et 1,5, ces seuls coenzymes donnent environ 9 ATP ; le GTP du cycle porterait le total à 10. Ne pas confondre ce changement de convention avec une faute de calcul dans le corrigé, qui applique bien 3×3 + 2. Le cours actuel sur les bilans de la chaîne respiratoire manque.

Sources : Sujets + corrections compilés.pdf, p118 (Énoncé fourni, Q23) ; Sujets + corrections compilés.pdf, p138 (Correction de référence).

### 45. annales.ue2c.enzymes.2020s1 / 2 — items D

**possible_error** — D est donné vrai alors qu’il nie le caractère allostérique de la glycogène phosphorylase. Sa régulation par phosphorylation n’exclut pas une régulation allostérique ; l’isoforme musculaire répond notamment à AMP, ATP et glucose-6-phosphate. Le commentaire sur la réaction catalysée ne démontre pas l’absence d’allostérie. À vérifier dans la ronéo d’enzymologie, chapitre régulations covalente et allostérique, non fournie.

Sources : Sujets + corrections compilés.pdf, p304 (Énoncé fourni, Q24) ; Sujets + corrections compilés.pdf, p319 (Correction de référence) ; Sujets + corrections compilés.pdf, p320 (Suite de la correction de référence).

### 46. annales.ue2c.proteines.2020s2 / 3 — items D

**possible_error** — D évoque les deux formes mésomères de la liaison peptidique et est rejeté au motif que la liaison possède un caractère partiellement double. Or ce caractère partiellement double est justement la conséquence de la délocalisation électronique entre les deux formes limites. Le motif du corrigé ne réfute donc pas l’item, à condition de lire « deux formes » comme des formes de résonance, et non deux molécules distinctes en équilibre. À vérifier dans le cours de structure des protéines, section liaison peptidique.

Sources : Sujets + corrections compilés.pdf, p334 (Énoncé fourni, Q14) ; Sujets + corrections compilés.pdf, p347 (Correction de référence).

### 47. annales.ue2c.metabolisme.2020s2 / 1 — items A

**source_conflict** — A est donné vrai mais présente le glucose-6-phosphate comme la forme directement incorporée au glycogène. Le substrat donneur de la glycogène synthase est l’UDP-glucose ; G6P puis G1P sont des intermédiaires en amont. Le corrigé de la même compilation, Q34 de 2021–2022, précise cette activation en UDP-glucose. Lire l’item au sens d’incorporation directe rend donc son VRAI incohérent avec cette autre correction.

Sources : Sujets + corrections compilés.pdf, p337 (Énoncé fourni, Q22) ; Sujets + corrections compilés.pdf, p351 (Correction de référence) ; Sujets + corrections compilés.pdf, p269 (Q34 : glucose-1-phosphate et UDP-glucose pour la glycogénogenèse).

### 48. annales.ue2c.proteines.2020paces / 6 — items A

**possible_error** — A décrit des plans peptidiques rigides successifs ; il ne dit pas que l’hélice entière est indéformable. La mobilité de l’hélice invoquée pour le rejeter n’invalide pas la planéité et la rigidité relatives de chaque liaison peptidique, ni leur orientation répétée dans une hélice α régulière. Le motif du corrigé confond deux niveaux de structure. À confronter à la ronéo « liaison peptidique et structures secondaires », absente.

Sources : Sujets + corrections compilés.pdf, p366 (Énoncé fourni, Q33) ; Sujets + corrections compilés.pdf, p389 (Correction de référence).

### 49. annales.ue2c.metabolisme.2020paces / 1 — items C

**possible_error** — La réaction de l’hexokinase est irréversible, mais le glucose-6-phosphate peut encore entrer dans plusieurs voies (glycolyse, glycogénogenèse, voie des pentoses phosphates). L’étape d’engagement spécifique vers la glycolyse est classiquement celle de PFK-1. C, donné vrai, confond donc irréversibilité et engagement dans une voie. Vérifier ce vocabulaire dans la ronéo de glycolyse et de sa régulation, non fournie.

Sources : Sujets + corrections compilés.pdf, p367 (Énoncé fourni, Q36) ; Sujets + corrections compilés.pdf, p391 (Correction de référence).

### 50. annales.ue2c.metabolisme.2019 / 2 — items A, D

**possible_error** — D est donné faux alors que la réaction réversible catalysée par l’aldolase intervient dans les deux voies : clivage du fructose-1,6-bisphosphate en glycolyse, condensation des trioses en néoglucogenèse. La néoglucogenèse contourne les étapes irréversibles, pas cette réaction réversible. Par ailleurs, A peut rester faux à cause de la néoglucogenèse, mais son explication situe à tort la fin de la glycolyse dans la mitochondrie : la conversion du pyruvate en acétyl-CoA et le cycle de Krebs sont distincts de la glycolyse cytosolique. La ronéo de métabolisme glucidique manque pour une validation conforme au cours.

Sources : Sujets + corrections compilés.pdf, p410 (Énoncé fourni, Q37) ; Sujets + corrections compilés.pdf, p437 (Correction de référence).

### 51. annales.ue2c.metabolisme.2019 / 3 — items E

**roneo_conflict** — E est donné vrai, mais l’allongement d’une chaîne d’acide gras s’effectue du côté carboxylique, tandis que l’extrémité méthyle initiale est conservée. La ronéo AG2 illustre cette extrémité invariable et le décalage de la numérotation depuis COOH lors de l’ajout de deux carbones. Le raccourcissement β-oxydatif est bien du côté carboxylique ; c’est la première moitié de E qui pose problème.

Sources : Sujets + corrections compilés.pdf, p410 (Énoncé fourni, Q38) ; Sujets + corrections compilés.pdf, p437 (Correction de référence) ; Sujets + corrections compilés.pdf, p438 (Suite de la correction de référence) ; Ronéo cours AG2 du vendredi 03.10.25.pdf, p3 (Élongation : extrémité méthyle invariable et addition de deux carbones).

### 52. annales.ue2c.lipides.2022s1 / 1 — items A, B, C, D, E

**source_conflict** — Le tableau indique BCD et la correction détaillée ADE : aucune clé unique n’est attribuée au QCM. La filiation représentée dans la ronéo AG2 permet de retrouver les séries et enzymes décrites par la correction détaillée. Ce contrôle étaye ADE pour le contenu scientifique, sans effacer la discordance documentaire ni rétablir arbitrairement une notation.

Sources : Sujets + corrections compilés.pdf, p181 (Énoncé fourni, Q25) ; Sujets + corrections compilés.pdf, p202 (Correction de référence) ; Sujets + corrections compilés.pdf, p203 (Suite de la correction de référence) ; Ronéo cours AG2 du vendredi 03.10.25.pdf, p2 (Filiations ω6 et ω3 : désaturases et élongases).

### 53. annales.ue2c.atomistique.2024s1 / 1 — items A

**roneo_conflict** — Le corrigé assimile le quatrième état excité de H à n=4. Or l’état fondamental est n=1 : le quatrième état excité est n=5. Son seuil d’ionisation vaut 13,6/25 = 0,544 eV, soit une longueur d’onde limite d’environ 2 279 nm, et non 1 458 nm (valeur de n=4). Il faut distinguer quatrième niveau et quatrième état excité.

Sources : Sujets + corrections compilés.pdf, p58 (Énoncé fourni, Q48) ; Sujets + corrections compilés.pdf, p81 (Correction de référence) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p8 (Niveaux d’énergie de l’hydrogène) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p9 (Transitions énergétiques).

### 54. annales.ue2c.atomistique.2023s1 / 1 — items B, C

**roneo_conflict** — Les items et le corrigé emploient Li+ tout en utilisant la formule des hydrogénoïdes Eₙ = −13,6 Z²/n². Li+ possède deux électrons ; l’ion hydrogénoïde de lithium est Li2+, cité explicitement dans la ronéo. Les résultats de B et C ne sont donc valables qu’en supposant une coquille de charge et en lisant Li2+. La figure et la clé originales sont conservées, avec cette hypothèse rendue explicite.

Sources : Sujets + corrections compilés.pdf, p112 (Énoncé fourni, Q1) ; Sujets + corrections compilés.pdf, p127 (Correction de référence) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p8 (Hydrogénoïde = un seul électron ; exemple Li2+).

### 55. annales.ue2c.atomistique.2022s2 / 2 — items E

**roneo_conflict** — E est donné vrai, avec l’argument que Mg et Si ont un nombre pair d’électrons. Avoir un nombre pair d’électrons ne signifie pas qu’ils sont tous appariés. Si fondamental a la configuration [Ne] 3s² 3p² ; la règle de Hund place les deux électrons 3p dans deux orbitales distinctes, donc non appariés. Mg a bien toutes ses sous-couches occupées complètes.

Sources : Sujets + corrections compilés.pdf, p219 (Énoncé fourni, Q28) ; Sujets + corrections compilés.pdf, p233 (Correction de référence) ; Sujets + corrections compilés.pdf, p234 (Suite de la correction de référence) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p13 (Configuration fondamentale, Pauli et règle de Hund).

### 56. annales.ue2c.atomistique.2021s2 / 1 — items E

**roneo_conflict** — E, qui compare le rayon de Se2− à celui de Kr, n’est pas retenu dans la clé A. Les deux espèces ont 36 électrons, mais Se2− possède 34 protons contre 36 pour Kr : à configuration identique, l’attraction nucléaire est plus faible pour Se2− et son rayon plus grand. Cette conclusion découle du modèle de rayon et de charge effective de la ronéo.

Sources : Sujets + corrections compilés.pdf, p283 (Énoncé fourni, Q27) ; Sujets + corrections compilés.pdf, p298 (Correction de référence) ; Chap 3 chimie phy_260906_130652.pdf, p5 (Charge nucléaire effective) ; Chap 3 chimie phy_260906_130652.pdf, p6 (Rayon de Slater et attraction nucléaire).

### 57. annales.ue2c.atomistique.2018 / 1 — items B

**roneo_conflict** — B est donné vrai en appliquant à un atome d’azote excité la configuration fondamentale 1s²2s²2p³ et en assimilant excitation à perte d’un électron. Une excitation redistribue les électrons sans nécessairement ioniser l’atome. La ronéo réserve explicitement les règles de remplissage utilisées ici à l’état fondamental ; l’argument donné ne permet pas de conclure que tout état excité garde trois électrons 2p parallèles. Une configuration excitée doit être précisée pour trancher B.

Sources : Sujets + corrections compilés.pdf, p458 (Énoncé fourni, Q46) ; Sujets + corrections compilés.pdf, p482 (Correction de référence) ; Sujets + corrections compilés.pdf, p483 (Suite de la correction de référence) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p7 (Excitation = passage à un niveau d’énergie supérieur) ; Chap 1 et 2 chimie phy_260918_170147.pdf, p13 (Règles de remplissage pour l’état fondamental).

### 58. annales.ue2c.thermo.2025s1 / 1 — items A, B

**source_conflict** — La réaction imprimée C4H6 + C2H4 → C7H10 ne conserve pas le carbone : six atomes à gauche, sept à droite. Le calcul numérique +409 kJ·mol⁻¹ est bien la différence des valeurs données, mais il ne peut pas représenter l’enthalpie de cette réaction chimique telle qu’écrite. Il faut faire confirmer la formule du produit (ou un réactif manquant) dans le sujet original avant d’interpréter les verdicts thermodynamiques. La coquille est présente dans la source, pas créée par le site.

Sources : Sujets + corrections compilés.pdf, p18 (Énoncé fourni, Q50) ; Sujets + corrections compilés.pdf, p44 (Correction de référence).

### 59. annales.ue2c.thermo.2021s2 / 1 — items B, D

**possible_error** — Le corrigé suppose qu’ajouter l’espèce notée (l) déplace nécessairement l’équilibre. Cette conclusion dépend de son statut : l’activité d’un liquide pur formant une phase distincte reste approximativement égale à 1 ; en ajouter ne déplace alors pas l’équilibre tant que la phase subsiste. Pour un constituant dissous dans un mélange liquide, son activité peut au contraire changer. L’énoncé ne précise pas ce point. La ronéo introduit le quotient réactionnel et les activités, mais ne résout pas cette ambiguïté de phase ; faire confirmer l’hypothèse du QCM dans le cours d’équilibres hétérogènes. Pour B, le verdict Faux peut être conservé, mais à température et volume constants l’ajout d’un gaz inerte ne modifie pas les pressions partielles des espèces réactives : l’explication annonçant un déplacement par simple hausse de pression totale est également à revoir.

Sources : Sujets + corrections compilés.pdf, p283 (Énoncé fourni, Q28) ; Sujets + corrections compilés.pdf, p298 (Correction de référence) ; cHAP 6 chimie phy_260918_180842.pdf, p6 (Quotient réactionnel et activités).

### 60. annales.ue2c.thermo.2020s2 / 1 — items D

**possible_error** — Le corrigé suppose qu’ajouter l’espèce notée (l) déplace nécessairement l’équilibre. Cette conclusion dépend de son statut : l’activité d’un liquide pur formant une phase distincte reste approximativement égale à 1 ; en ajouter ne déplace alors pas l’équilibre tant que la phase subsiste. Pour un constituant dissous dans un mélange liquide, son activité peut au contraire changer. L’énoncé ne précise pas ce point. La ronéo introduit le quotient réactionnel et les activités, mais ne résout pas cette ambiguïté de phase ; faire confirmer l’hypothèse du QCM dans le cours d’équilibres hétérogènes.

Sources : Sujets + corrections compilés.pdf, p338 (Énoncé fourni, Q28) ; Sujets + corrections compilés.pdf, p355 (Correction de référence) ; Sujets + corrections compilés.pdf, p356 (Suite de la correction de référence) ; cHAP 6 chimie phy_260918_180842.pdf, p6 (Quotient réactionnel et activités).

### 61. annales.ue2c.thermo.2020paces / 1 — items C

**possible_error** — Le corrigé suppose qu’ajouter l’espèce notée (l) déplace nécessairement l’équilibre. Cette conclusion dépend de son statut : l’activité d’un liquide pur formant une phase distincte reste approximativement égale à 1 ; en ajouter ne déplace alors pas l’équilibre tant que la phase subsiste. Pour un constituant dissous dans un mélange liquide, son activité peut au contraire changer. L’énoncé ne précise pas ce point. La ronéo introduit le quotient réactionnel et les activités, mais ne résout pas cette ambiguïté de phase ; faire confirmer l’hypothèse du QCM dans le cours d’équilibres hétérogènes.

Sources : Sujets + corrections compilés.pdf, p370 (Énoncé fourni, Q49) ; Sujets + corrections compilés.pdf, p397 (Correction de référence) ; cHAP 6 chimie phy_260918_180842.pdf, p6 (Quotient réactionnel et activités).

### 62. annales.ue2c.thermo.2019 / 1 — items D

**possible_error** — Le corrigé suppose qu’ajouter l’espèce notée (l) déplace nécessairement l’équilibre. Cette conclusion dépend de son statut : l’activité d’un liquide pur formant une phase distincte reste approximativement égale à 1 ; en ajouter ne déplace alors pas l’équilibre tant que la phase subsiste. Pour un constituant dissous dans un mélange liquide, son activité peut au contraire changer. L’énoncé ne précise pas ce point. La ronéo introduit le quotient réactionnel et les activités, mais ne résout pas cette ambiguïté de phase ; faire confirmer l’hypothèse du QCM dans le cours d’équilibres hétérogènes.

Sources : Sujets + corrections compilés.pdf, p413 (Énoncé fourni, Q49) ; Sujets + corrections compilés.pdf, p443 (Correction de référence) ; Sujets + corrections compilés.pdf, p444 (Suite de la correction de référence) ; cHAP 6 chimie phy_260918_180842.pdf, p6 (Quotient réactionnel et activités).

### 63. annales.ue2c.chimie_org.2022s2 / 2 — items A, B

**source_conflict** — La structure 1 représentée possède un CH2 immédiatement voisin du carbonyle : elle a donc des hydrogènes en α et est énolisable, contrairement au VRAI de A. Le critère écrit dans l’explication de A conduit lui-même à ce résultat. Pour B, la structure de départ possède un seul centre stéréogène ; l’addition de CN− au carbonyle en crée un second, pas un troisième. Les produits attendus dans cette lecture ont deux carbones asymétriques. La figure source a été relue ; une ronéo de réactivité des carbonyles permettrait de confirmer l’attendu de B.

Sources : Sujets + corrections compilés.pdf, p219 (Énoncé fourni, Q26) ; Sujets + corrections compilés.pdf, p232 (Correction de référence) ; Sujets + corrections compilés.pdf, p233 (Suite de la correction de référence).

### 64. annales.ue2c.chimie_org.2021s1 / 2 — items D

**possible_error** — Les structures 2 et 3 ont la même connectivité CH3–CH(OH)–CH(CH3)2 : elles représentent toutes deux un 3-méthylbutan-2-ol. D ne peut donc pas être justifié comme une isomérie de constitution simplement parce que l’une est dessinée en Fischer et l’autre en perspective. À vérifier dans le chapitre de stéréochimie et de conversion des représentations, absent des cours fournis.

Sources : Sujets + corrections compilés.pdf, p246 (Énoncé fourni, Q41) ; Sujets + corrections compilés.pdf, p272 (Correction de référence) ; Sujets + corrections compilés.pdf, p273 (Suite de la correction de référence) ; Sujets + corrections compilés.pdf, p246 (Figure commune des structures 1 à 6).

### 65. annales.ue2c.chimie_org.2020paces / 3 — items A

**source_conflict** — A est donné faux au motif que la structure 4 serait méso. Sa projection de Fischer porte pourtant les OH sur des côtés opposés et correspond au (2S,3S)-butane-2,3-diol, chiral ; la forme méso serait (2R,3S). La correction du Q42 précédent attribue elle-même la configuration (2S,3S) à la structure 4. Les deux corrections sont donc incompatibles.

Sources : Sujets + corrections compilés.pdf, p369 (Énoncé fourni, Q43) ; Sujets + corrections compilés.pdf, p395 (Correction de référence) ; Sujets + corrections compilés.pdf, p368 (Figure commune : structure 4) ; Sujets + corrections compilés.pdf, p394 (Q42 E : configuration (2S,3S) de la structure 4) ; Sujets + corrections compilés.pdf, p395 (Q42 : E explicitement vrai avant le corrigé Q43).

### 66. annales.ue2c.proteines.2019 / 5 — items B, C

**source_conflict** — Le fragment le plus long est HSQETF. Avec les pKa donnés, la forme de charge formelle nulle se situe entre le pKa du glutamate (4,2) et celui de l’histidine (6), donnant un pI approché de 5,1. Le commentaire « neutre entre 6 et 8,2 » utilise une borne qui ne convient pas à ce fragment. Dans le modèle de charges entières de l’exercice, B à pH 5 devrait être accepté ; la charge moyenne exacte n’est strictement nulle qu’au pI. C (pHi = 6) reste faux, mais sa justification doit être corrigée. Le Q33 suivant confirme un pI voisin de 5,1.

Sources : Sujets + corrections compilés.pdf, p408 (Énoncé fourni, Q32) ; Sujets + corrections compilés.pdf, p432 (Correction de référence) ; Sujets + corrections compilés.pdf, p433 (Suite de la correction de référence) ; Sujets + corrections compilés.pdf, p408 (Séquence, pKa et questions sur le fragment) ; Sujets + corrections compilés.pdf, p433 (Q33 : courbe et pI du fragment).

### 67. ue2.intro.autotest / 9 — items E

**possible_error** — E appelle l’AZT une « thymidine et un analogue de désoxyribose ». La thymidine contient déjà une thymine et un désoxyribose : ajouter un second sucre dans la définition est incorrect. L’AZT est la 3′-azido-3′-désoxythymidine, que l’on peut décrire comme une thymine liée à un sucre modifié en C3′. Vérifier la formulation dans la ronéo « bases, nucléosides et analogues », non fournie.

Sources : 4. Autotests Acides Nucléiques ENNONCE.pdf, p2 (Énoncé fourni, Q9) ; 4. Autotests Acides Nucléiques CORRECTION.pdf, p2 (Correction de référence).

### 68. ue2.adn.autotest / 13 — items D

**possible_error** — D est rejeté en affirmant que l’ADN mitochondrial n’aurait ni promoteurs ni ADN intergénique. L’ADN mitochondrial humain possède pourtant une région de contrôle avec des promoteurs pour la transcription des brins lourd et léger, tout en étant dépourvu d’introns usuels. La présence de promoteurs ne contredit donc pas l’absence d’introns. Le cours sur l’ADN mitochondrial manque pour confirmer le périmètre et les termes exacts attendus.

Sources : 4. Autotests ADN ENONCE.pdf, p3 (Énoncé fourni, Q13) ; 4. Autotests ADN CORRECTION.pdf, p3 (Correction de référence).

### 69. ue2.adn.annales / 14 — items B

**source_conflict** — La clé imprimée ne retient que D, mais le commentaire du même corrigé dit explicitement « B. Vrai car les phosphates sont négatifs ». L’interaction des résidus basiques des histones avec les phosphates de l’ADN décrite en B est donc acceptée par l’explication et rejetée par la clé. Conserver cette contradiction visible ; elle ne provient pas du choix de l’étudiant.

Sources : 2. Annales ADN LS ENONCE.pdf, p4 (Énoncé fourni, Q5) ; 2. Annales ADN LS CORRECTION.pdf, p5 (Correction de référence).

### 70. ue2.arn.autotest / 7 — items A

**possible_error** — A est rejeté parce que la grande sous-unité se lie à l’ARNt. Ce fait n’exclut pas son interaction avec les extrémités aminoacyl/peptidyl des ARNt et la chaîne naissante ; la petite sous-unité assure bien le décodage de l’ARNm. Le motif donné ne suffit donc pas à rendre A faux. La formulation « interagissant avec les AA » devrait être rapprochée de la ronéo sur la structure du ribosome et le centre peptidyl-transférase, non disponible.

Sources : 4. Autotests ARN et métabolisme ENONCE.pdf, p2 (Énoncé fourni, Q7) ; 4. Autotests ARN et métabolisme CORRECTION.pdf, p2 (Correction de référence).

### 71. ue2.arn.autotest / 8 — items E

**possible_error** — E généralise des ribosomes mitochondriaux à 70S. Chez les mammifères, le mitoribosome est classiquement décrit comme 55S, composé des sous-unités 28S et 39S ; les valeurs varient entre groupes eucaryotes. Le 70S bactérien ne doit donc pas être transposé sans préciser l’organisme. À contrôler dans la ronéo ARN, section ribosomes mitochondriaux, absente ; la clé du document est conservée.

Sources : 4. Autotests ARN et métabolisme ENONCE.pdf, p2 (Énoncé fourni, Q8) ; 4. Autotests ARN et métabolisme CORRECTION.pdf, p2 (Correction de référence).

### 72. ue2.arn.annales / 11 — items A

**roneo_conflict** — A est donné faux avec « uniquement dans le cytoplasme ». Les ARNt d’origine nucléaire sont transcrits dans le noyau avant leur export ; leur présence n’est donc pas exclusivement cytoplasmique. Le cours de transcription situe les ARN polymérases eucaryotes dans le noyau et attribue la synthèse des ARNt à l’ARN polymérase III.

Sources : 2. Annales ARN et métabolisme LS ENONCE.pdf, p2 (Énoncé fourni, Q7) ; 2. Annales ARN et métabolisme LS CORRECTION.pdf, p4 (Correction de référence) ; downloadfile(1).PDF, p4 (ARN polymérase III et localisation nucléaire) ; downloadfile(1).PDF, p10 (Transcription nucléaire et traduction cytoplasmique).

### 73. ue2.arn.annales / 28 — items A

**roneo_conflict** — L’item A reste faux si « lors de la traduction » signifie que l’export a lieu pendant celle-ci. En revanche, la justification officielle « ils sont formés dans le cytoplasme » est erronée pour les ARNt nucléaires : ils sont transcrits dans le noyau, puis exportés avant leur utilisation dans la traduction cytoplasmique. Le verdict et la justification doivent ici être distingués.

Sources : 2. Annales ARN et métabolisme LS ENONCE.pdf, p4 (Énoncé fourni, QX) ; 2. Annales ARN et métabolisme LS CORRECTION.pdf, p6 (Correction de référence) ; downloadfile(1).PDF, p4 (Synthèse des ARNt par l’ARN polymérase III nucléaire) ; downloadfile(1).PDF, p10 (Localisation de la transcription eucaryote).

### 74. ue2.organisation.autotest / 9 — items E

**roneo_conflict** — E est donné vrai mais cite le facteur VII pour l’hémophilie A. Le gène concerné est celui du facteur VIII (F8). La fiche d’anomalies du génome confirme le facteur VIII dans son exemple d’hémophilie A. Le mécanisme d’insertion LINE cité par l’item n’autorise pas à remplacer VIII par VII.

Sources : 4. Autotests Organisation du génome ENONCE.pdf, p2 (Énoncé fourni, Q9) ; 4. Autotests Organisation du génome CORRECTION-1.pdf, p2 (Correction de référence) ; 3. FS Anomalies du génome LS.pdf, p3 (Hémophilie A : gène du facteur VIII).

### 75. ue2.replication.autotest / 10 — items B

**possible_error** — Dans le système Dam d’E. coli, la méthylation de GATC porte sur l’adénine, pas sur la cytosine. B est pourtant donné vrai. La méthylation des cytosines existe dans d’autres contextes, mais ne doit pas être confondue avec le marquage Dam de ces sites. À vérifier dans la ronéo « terminaison de la réplication procaryote et méthylation », non fournie.

Sources : 4. Autotests Réplication ENONCE.pdf, p2 (Énoncé fourni, Q10) ; 4. Autotests Réplication CORRECTION.pdf, p2 (Correction de référence).

### 76. ue2.replication.annales / 21 — items B

**possible_error** — B est rejeté parce que l’ADN polymérase α interviendrait seulement sur le brin retardé. Le complexe primase–polymérase α intervient également dans l’amorçage initial du brin avancé, avant le relais par la polymérase réplicative. Son intervention répétée sur les fragments d’Okazaki n’exclut pas ce rôle initial. La ronéo de réplication eucaryote manque pour étayer le verdict attendu dans le cours.

Sources : 2. Annales Réplication LS ENONCE.pdf, p5 (Énoncé fourni, Q10) ; 2. Annales Réplication LS CORRECTION.pdf, p7 (Correction de référence).

### 77. ue2.transcription.autotest / 14 — items B

**possible_error** — Le cours fourni place le clivage du pré-ARNm 10–15 nucléotides après AAUAAA. Cette distance est celle du site de coupure ; elle ne démontre pas que l’ARN polymérase II cesse elle-même de transcrire exactement à cet endroit. L’item et son explication fusionnent maturation de l’extrémité 3′ et terminaison de la polymérase. Le cours les présente de façon simplifiée : faire confirmer cette distinction dans la partie détaillée sur la terminaison de Pol II.

Sources : 4. Autotests Transcription LS ENONCE.pdf, p3 (Énoncé fourni, Q14) ; 4. Autotests Transcription LS CORRECTION.pdf, p3 (Correction de référence) ; downloadfile(1).PDF, p14 (Coupure du transcrit 10–15 nt après AAUAAA).

### 78. ue2.reparation.autotest / 8 — items A

**possible_error** — Le fait que des lésions spontanées puissent apparaître en dehors de la réplication ne signifie pas qu’elles ne peuvent jamais survenir pendant celle-ci. L’item dit « peuvent » ; le motif du corrigé ne suffit donc pas à le rejeter. Il faut également distinguer une lésion chimique de l’ADN d’une mutation fixée dans la séquence. La ronéo « lésions spontanées, erreurs de réplication et mutations » est nécessaire pour trancher cette formulation.

Sources : 4. Autotests Réparation de l'ADN ENONCE.pdf, p2 (Énoncé fourni, Q8) ; 4. Autotests Réparation de l'ADN CORRECTION.pdf, p2 (Correction de référence).

### 79. ue2.reparation.autotest / 11 — items D

**possible_error** — Le corrigé associe le MMR humain ou les protéines MSH/MLH à un repérage du brin nouveau par retard de méthylation. Cette présentation semble transposer le système Dam/MutH d’E. coli au système humain. Chez l’Homme, MSH2–MSH6 reconnaît les mésappariements ; la discrimination du brin à réparer implique notamment des discontinuités du brin néosynthétisé et le contexte de réplication, sans le mécanisme bactérien MutH guidé par GATC méthylé. Il manque la ronéo de réparation comparant explicitement MMR bactérien et humain : maintenir ce point comme réserve scientifique, sans modifier la clé.

Sources : 4. Autotests Réparation de l'ADN ENONCE.pdf, p2 (Énoncé fourni, Q11) ; 4. Autotests Réparation de l'ADN CORRECTION.pdf, p3 (Correction de référence).

### 80. ue2.reparation.annales / 25 — items A

**possible_error** — Le corrigé associe le MMR humain ou les protéines MSH/MLH à un repérage du brin nouveau par retard de méthylation. Cette présentation semble transposer le système Dam/MutH d’E. coli au système humain. Chez l’Homme, MSH2–MSH6 reconnaît les mésappariements ; la discrimination du brin à réparer implique notamment des discontinuités du brin néosynthétisé et le contexte de réplication, sans le mécanisme bactérien MutH guidé par GATC méthylé. Il manque la ronéo de réparation comparant explicitement MMR bactérien et humain : maintenir ce point comme réserve scientifique, sans modifier la clé.

Sources : 2. Annales Réparation LS ENONCE.pdf, p5 (Énoncé fourni, Q9) ; 2. Annales Réparation LS CORRECTION.pdf, p7 (Correction de référence).

### 81. ue2.reparation.annales / 2 — items D

**possible_error** — Le corrigé associe le MMR humain ou les protéines MSH/MLH à un repérage du brin nouveau par retard de méthylation. Cette présentation semble transposer le système Dam/MutH d’E. coli au système humain. Chez l’Homme, MSH2–MSH6 reconnaît les mésappariements ; la discrimination du brin à réparer implique notamment des discontinuités du brin néosynthétisé et le contexte de réplication, sans le mécanisme bactérien MutH guidé par GATC méthylé. Il manque la ronéo de réparation comparant explicitement MMR bactérien et humain : maintenir ce point comme réserve scientifique, sans modifier la clé.

Sources : 2. Annales Réparation LS ENONCE.pdf, p1 (Énoncé fourni, Q8) ; 2. Annales Réparation LS CORRECTION.pdf, p1 (Correction de référence).

### 82. ue2.reparation.annales / 21 — items A

**possible_error** — A est rejeté au motif que MMR agit « durant la réplication ». Le terme post-réplicatif désigne la correction d’une séquence déjà copiée, derrière la fourche, et ne signifie pas nécessairement après la fin de toute la phase S. Le MMR est classiquement une correction post-réplicative des erreurs échappées à l’édition ; les deux descriptions temporelles ne sont pas incompatibles. À faire confirmer dans la ronéo de réparation MMR, non disponible.

Sources : 2. Annales Réparation LS ENONCE.pdf, p4 (Énoncé fourni, Q14) ; 2. Annales Réparation LS CORRECTION.pdf, p6 (Correction de référence).

### 83. ue2.reparation.annales / 23 — items C

**roneo_conflict** — C est donné vrai sans condition sur la taille de la délétion. La fiche fournie précise qu’un décalage du cadre de lecture apparaît si le nombre de nucléotides supprimés n’est pas un multiple de trois. La délétion de trois nucléotides de CFTR supprimant Phe508 illustre justement une délétion en phase. Toutes les délétions ne décalent donc pas le cadre.

Sources : 2. Annales Réparation LS ENONCE.pdf, p5 (Énoncé fourni, Q42’) ; 2. Annales Réparation LS CORRECTION.pdf, p7 (Correction de référence) ; 3. FS Anomalies du génome LS.pdf, p1 (Petites insertions/délétions et condition non multiple de trois) ; 3. FS Anomalies du génome LS.pdf, p2 (CFTR : suppression de trois nucléotides / Phe508).

### 84. ue2.anomalies.annales / 1 — items E

**source_conflict** — La clé AD exclut E, mais l’explication du même corrigé indique explicitement E Vrai et donne le cancer du poumon et le sarcome d’Ewing comme exemples. La fiche d’anomalies décrit elle aussi une translocation EML4–ALK dans certains cancers du poumon. La contradiction entre clé et commentaire doit rester signalée.

Sources : 2. Annales Anomalies LS ENONCE.pdf, p1 (Énoncé fourni, Q16) ; 2. Annales Anomalies LS CORRECTION.pdf, p1 (Correction de référence) ; 3. FS Anomalies du génome LS.pdf, p3 (Translocation EML4–ALK et cancer du poumon).

### 85. ue2.anomalies.annales / 2 — items D

**possible_error** — D dit qu’une substitution synonyme peut être associée à une pathologie. Le fait de ne pas modifier directement l’acide aminé ne permet pas de l’exclure : une variation synonyme peut notamment perturber un élément d’épissage ou l’expression du transcrit. Le « Faux, pas de changement de la protéine » est donc un argument trop général. La fiche fournie ne traite pas ce cas ; il faut le cours détaillé des variants synonymes et des conséquences sur l’épissage.

Sources : 2. Annales Anomalies LS ENONCE.pdf, p1 (Énoncé fourni, Q14) ; 2. Annales Anomalies LS CORRECTION.pdf, p1 (Correction de référence).

### 86. ue2.arn.annales / 10 — items B

**possible_error** — La molécule 2 est bien la xanthine, mais sa formation à partir de guanine est une désamination hydrolytique catalysée par la guanine désaminase, et non la désamination oxydative annoncée en B. La xanthine oxydoréductase intervient ailleurs dans le catabolisme des purines ; il ne faut pas fusionner ces réactions. La ronéo du catabolisme des bases puriques est manquante : faire vérifier ce qualificatif avant de retenir B.

Sources : 2. Annales ARN et métabolisme LS ENONCE.pdf, p2 (Énoncé fourni, Q5) ; 2. Annales ARN et métabolisme LS CORRECTION.pdf, p4 (Correction de référence).

### 87. ue2.adn.annales / 17 — items E

**missing_reference** — L’item E est incomplet dans le sujet fourni : il s’interrompt après « La liaison entre les différents ». Le titre de l’année suivante a ensuite été accolé à cet item lors de l’extraction. Le corrigé se limite à E Vrai ; ni le texte scientifique manquant ni son objet ne peuvent être reconstitués avec certitude. Il faut la version complète du sujet, Q6 (séquence de quatre désoxyribonucléotides), pour valider E. Aucune fin de phrase n’est inventée.

Sources : 2. Annales ADN LS ENONCE.pdf, p5 (Énoncé fourni, Q6) ; 2. Annales ADN LS CORRECTION.pdf, p6 (Correction de référence).

