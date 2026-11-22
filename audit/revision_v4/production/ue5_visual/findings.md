# UE5 — contre-lecture visuelle finale

**Lot gelé, prêt pour intégration.** Les livrables fusionnent le bloc principal histologie/CM2–CM5 et le bloc CM6/CM7/CM10 relu par l’agent UE2/UE3. Les sources originales et les cours utilisés restent les documents locaux fournis.

## Périmètre et décompte

- Le manifest contient **80 images** concernant **97 QCM uniques**. Les cinq petites images GFP répètent les mêmes Q2/Q3 et ne doivent pas gonfler le décompte des QCM.
- Le JPEG de `bio.cm3 Q5`, absent du manifest mais présent dans le site, a aussi été vu : **98 QCM illustrés couverts au total**.
- L’EMF manquant de `bio.cm6 Q3` a été retrouvé dans le DOCX et rendu en PNG. Il ne représente pas un QCM supplémentaire.
- `figure_reviews.json` contient **97 entrées uniques**. Ajouter la revue existante de `histo.tn3 Q6` pour obtenir les98 QCM. L’entrée TN3 Q7 complète la première revue en résolvant la perte des lettres A/B/C.
- Les20 noms d’images différents entre le manifest baseline et `current_exams.json` ont été comparés : les contenus étaient identiques. Les véritables fichiers utilisés ont donc bien été pris en compte.
- `coverage.json` concerne exclusivement les **3 QCM nouvellement récupérés**, soit15 propositions. La couverture des533 QCM du lot histologie/biocell existant reste celle de l’agent UE5.

## Livrables

| Fichier | Contenu final |
|---|---|
| `source_repairs.json` |43 réparations concernant43 QCM existants, plus3 ajouts dans le même objet `{patches, additions}`|
| `notes.json` |19 notes concernant14 QCM :9 conflits de source,7 points possibles à vérifier,2 désaccords étayés par une ronéo,1 référence manquante|
| `figure_reviews.json` |97 revues au format bank/id/images/observation/figureStatus|
| `coverage.json` |3 lignes, exclusivement pour les questions ajoutées|
| `assets/` et les assets du bloc délégué |20 images originales rendues ou recadrées depuis les sources, référencées par `assetFile`/`assetFiles` dans les réparations|

Aucun identifiant de question ou de réponse existant n’est changé. **Aucune chaîne de réponse existante n’est remplacée.** Le cas `bio.ann.cm6 Q24` restaure seulement le statut explicite « aucune réponse » : la source écrit RIEN puis cinq FAUX, page19. La clé vide était déjà présente ; elle devient exploitable au lieu de rester hors note.

## Trois QCM effectivement perdus

| Banque et nouvel ID | Source | Clé conservée ou transposée |
|---|---|---|
|histo.ann.tech38|Juin2024 session2, QUESTION14, sujetp9 et corrigép11|B|
|histo.ann.tech39|Juin2024 session2, QUESTION15, sujetp9 et corrigép11|ABD|
|bio.ann.cm7 12|2023–2024 session1, QCM40, sujetp3 et corrigép4|FI avec les lettresF–J du sujet ; équivalent exact de AD imprimé avec les lettresA–E du corrigé|

Les deux QCM de techniques étaient absorbés dans le titre de l’actuel ID23, dont les propositions et la cléBC correspondent au Q16 CC2025. ID23 conserve ses items, sa clé et ses sauvegardes ; seule la consigne est nettoyée. Les nouveaux IDs38/39 s’insèrent après22 sans renuméroter les autres questions.

Le QCM du noyau avait échappé à l’import à cause des lettresF–J. Il s’insère aprèsID2 avec un nouvel ID12 ; la consigne seule, `sourceNumber:40`, `year:'2023-2024'`, `session:'S1'` et le classement demandé sont présents. Le commentaireG contient réellement « plus de % » sans nombre : aucun pourcentage n’a été inventé. Les nuances sur Ran-GDP enH et la composition des condensines enI font l’objet de notes prudentes. Le cours disponible ne donne pas le nombre de sous-unités des condensines.

## Restaurations visuelles principales

| QCM | Défaut confirmé dans la source | Réparation |
|---|---|---|
|histo.tn3 7|Les lettresA/B/C étaient des surcouches Word, absentes du raster|Rendu original avec lettres et flèches|
|bio.cm6 3|Formule du glycérol dans un EMF dont le lien était cassé|PNG fidèle ; distinction figureB/C puis figureD/E|
|histo.ann.te11|Seul le panneauT était visible|Planche complète T/S/R et ses lettres|
|histo.ann.tech25|Image mitochondriale du QCM précédent|Vraie coupe épithéliale au trichrome et flèche jaune|
|bio.ann.cm3 3|Deux figures sur trois perdues|Photographie d’actine deB et filamine deC, en plus de la tropomyosine deE|
|bio.ann.cm3 8|La légende décrivait une figureIRM absente|Restauration des deuxIRM de la figure5, en complément de la figure4|
|bio.ann.cm3 13|Figure3 perdue|Restauration de la figure3 à côté de la figure4 fluorescente|
|bio.ann.cm4 4|Schéma du trafic vésiculaire d’une autre question|Vraie protéine avec segment hydrophobe et charges flanquantes|
|bio.ann.cm5 4|Schéma du QCM suivant, seulement repéré1/2|Vrai schéma du Q29 avec repères1–5|
|bio.ann.cm6 2|Micrographie du Q1 à la place de la molécule|Triglycéride original|
|bio.ann.cm6 7|Figures deC etD perdues|Glycosphingolipide et profil hydrophobe restaurés ; figureE conservée|
|bio.ann.cm6 24|Profil hydrophobeA/B perdu|Profil restauré en plus du schémaFLIP|
|bio.ann.cm10 9|Photos du Q10 à la place du tableau|Tableau annexine/IP et sa légende|
|bio.ann.cm10 2/3/8/10|Légendes expérimentales rognées|Plans complets avec les légendes originales|

**Cas important de CM8Q6 :** le raster brut importé était une capture Acrobat contenant un ancienQ5 et une barre0,3µm. Le document Word recadrait cette image et ajoutait sa propre flèche ainsi qu’une barre sans valeur numérique. Le rendu Word a été inspecté et restauré exactement. L’ancienne échelle ne constitue donc pas une preuve d’erreur scientifique du corrigé0,5µm. La note porte seulement sur la différence éditoriale entre quatre propositions dans le sujet et cinq assertions séparées dans le corrigé ; les lettres sauvegardées restent intactes.

## Contextes et associations

Les légendes GFP des colles orales CM2, le protocole de complémentation GFP des annalesCM2 Q13–15, le protocole des ARNm thérapeutiques en histotech21 et le protocole mTOR/Lamp2 en CM7Q11 sont rétablis. CM2Q15 récupère les deux figures nécessaires à la comparaison sauvage/mutée. CM2Q11 récupère les figures8/9 précédentes pour son itemE demandant l’ensemble des résultats, afin que le filtrage sur un seul QCM laisse toutes les données nécessaires.

Treize associations parasites sont retirées après vérification des limites dans les pages originales : histoTE10, histoTC37, histoTN55/59, histotech16/28/29, bioCM3ann5/9/11, bioCM5ann9, bioCM6ann11, bioCM7ann8. Les contextes réellement partagés sont conservés, notamment les tubes séminifères et le schéma de trafic des annalesCM5 Q11/12.

## Annotations nouvelles les plus importantes

- **Compartiment3 et sécrétion constitutive :** CM5Q3C est faux, mais la même proposition est acceptée dans les clés de CM5Q4D et CM4Q3D. Le corrigéCM5 comporte même une annotation barrantD.VRAI et ajoutantFAUX. Les pages10–11 de la ronéo CM5 distinguent le trajet endosomal et la sécrétion constitutive. Les trois clés restent celles de leurs sources.
- **Immunogold, CM5Q13B :** les points noirs proviennent du marqueur d’or décrit dans le protocole et dans la ronéo de techniques histologiquesp26. Leur assimilation à du matériel lysosomal non digéré est contestée. PourE, le protocole présenteRab7 comme lysosomal tandis que le commentaire le refuse en invoquant l’endosome tardif ; la ronéoCM5p18 explique la maturation et justifie une réserve, pas une identification exclusivement lysosomale.
- **Étoposide/ouabaïne, colle oraleCM2Q4E :** le corrigé change nécrose en apoptose et répond faux, alors que les populations marquées diminuent dans la figure. Les annalesCM10 interprètent explicitement la même figure comme une résistance accrue aprèsétoposide. La note distingue cette divergence de toute certification du mécanisme de mort par les seuls marqueurs.
- **Noyau :** justification de la lectureACT du fragment nucléotidique, nuance sur le passage par le pore plutôt que le franchissement successif de deux bicouches, ainsi que limites des commentairesRan-GDP et condensine du QCM retrouvé.
- **HistotechQ39 :** dénominationformol/paraformaldéhyde, portée de la liste des fixateurs et nuance sur la préservation des activités enzymatiques. Ces notes restent prudentes ; elles ne remplacent pas la cléABD.
- **CM10Q3D :** la familleBCL2 comprend des membres pro- et anti-apoptotiques, contrairement à la généralisation du commentaire. La protéineBCL2 elle-même reste anti-apoptotique.

Les notes antérieures du lotUE5 ne sont pas dupliquées : par exemple conflit papilles gustatives en histotech15, endocrine/exocrine en histotech22, SRP/récepteur, rôle desRab et contradictions sur les membranes de mitophagie.

## Limites documentées

- La figure1 évoquée en CM6annQ7A manque déjà dans le sujet et dans le corrigé fournis. Le commentaireA se contredit lui-même, « VRAI » puis « donc FAUX ». Aucune figure ni clé n’est inventée.
- La figure6 expérimentale évoquée en CM5annQ16 n’est pas reproduite dans cette compilation. Son protocole textuel est présent et conservé. La recherche des termesMTM1/UBQLN2/GFP-CASQ1 dans les textes locaux n’a retrouvé que les copies de cette même compilation.
- CM5annQ1 conserve une correction incomplète et son statut hors note ; la figure ne permet pas de reconstruire une clé officielle complète.
- Les cinq imagesGFP de la colle orale sont petites dans la source. Leurs légendes sont récupérées, sans inventer une résolution supérieure.
- Une revue visuelle constate la présence, le rattachement et la lisibilité d’un document ainsi que ses rapports aux propositions. Elle ne certifie pas toute la science d’un QCM. Les recoupements de cours sont localisés dans chaque note ; un conflit entre documents reste distinct d’une erreur démontrée par une ronéo.

## Contrôles de livraison

La simulation des43 réparations et3 ajouts valide tous les IDs et toutes les lettres des notes. Les listes d’images des97 revues correspondent aux images après réparation. Les20 assets sont présents. Les références locales se résolvent. Aucun verdictVRAI/FAUX n’est introduit dans les textes des options réparées. Les trois nouvelles questions possèdent seules des lignes de couverture nouvelles. Aucune chaîne de réponse existante n’est modifiée pour une raison scientifique.
