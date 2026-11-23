# Embryologie V6 — vérification indépendante finale

## Verdict et fichiers à intégrer

**Lot approuvé avec limites documentaires explicites.** Utiliser exclusivement les objets complets `approved_reviewed.json` et `approved_crops.json` de ce dossier pour la fusion, en remplacement des brouillons du préparateur. Les empreintes de ces deux fichiers et celles du lot préparateur examiné sont dans `final_validation.json`.

Le périmètre est constitué des **22 banques d’embryologie (`ue5e`), 599 QCM et 3 389 propositions**. Les identifiants des QCM et des anciennes propositions, ainsi que leur ordre relatif, sont conservés. Deux propositions distinctes omises dans V5 ont été rétablies dans des QCM existants. Aucun autre contenu du site ni aucune autre matière n’a été modifié par le vérificateur. Les profils et leur stockage sont hors du lot de données.

Les livrables sont :

- `approved_reviewed.json` : objets complets approuvés des 22 banques ;
- `approved_crops.json` : 319 jeux de copies sujet, 599 jeux de copies correction, soit 1 048 panneaux ;
- `coverage.json` : 599 entrées, avec une entrée par proposition, preuves, limites et indicateurs distincts sujet/correction/cadrages ;
- `issues.json` : anomalies réparées, conflits documentés et sources encore manquantes ;
- `missing.json` : demandes précises des sujets, schémas vierges et clarifications restantes ;
- `changes_vs_baseline.json` et `verifier_changes.json` : différences respectivement par rapport à V5 et au lot figé du préparateur ;
- `final_validation.json` : bilan chiffré, invariants vérifiés et empreintes.

## Couverture réellement acquise

| Contrôle | Résultat |
|---|---:|
| QCM relus depuis les documents disponibles | 599 / 599 |
| Propositions finales | 3 389 |
| Propositions confrontées au contenu du corrigé | 3 388 / 3 389 |
| QCM dont le document sujet a été confronté | 319 |
| Dont sujets propres, utilisables avant correction | 315 |
| Dont sujets déjà annotés dans le fichier fourni, protégés après correction | 4 |
| Propositions confrontées à un document sujet | 1 724 |
| Dont propositions avec sujet propre | 1 704 |
| QCM sans sujet non corrigé retrouvé | 280 |
| QCM conservés hors note faute de clé complète certaine | 6 |
| Jeux de copies correction disponibles | 599 |

`correctionChecked:true` au niveau d’un QCM signifie que son document corrigé a été consulté. Ce n’est pas une affirmation qu’il résout tous les items : le Q70 de Colle S4 porte `correctionComplete:false`, et son item E porte `correctionChecked:false`. L’item est absent du corrigé, qui s’arrête après D.

`cropsChecked:true` signifie que les cadres disponibles ont subi la confrontation géométrique et documentaire. `subjectCropChecked:false` indique clairement une copie sujet absente. Les indicateurs de contrôle visuel sont distincts par rôle ; ils ne sont pas déduits de la simple réussite d’un rendu.

### Détail par banque

| Banque | QCM | Items | Sujets propres | Sujets annotés protégés | Sujets absents |
|---|---:|---:|---:|---:|---:|
| Autotest · Méiose (`embryo.aut.meiose`) | 15 | 135 | 0 | 0 | 15 |
| Autotest · Spermatogenèse (`embryo.aut.sperm`) | 7 | 106 | 0 | 0 | 7 |
| Autotest · Ovogenèse (`embryo.aut.ovo`) | 19 | 209 | 0 | 0 | 19 |
| Autotest · Fécondation (`embryo.aut.fec`) | 24 | 163 | 0 | 0 | 24 |
| Autotest · S1 · Première semaine (`embryo.aut.s1`) | 13 | 121 | 0 | 0 | 13 |
| Autotest · S2 · Deuxième semaine (`embryo.aut.s2`) | 10 | 50 | 0 | 0 | 10 |
| Autotest · S3 · Troisième semaine (`embryo.aut.s3`) | 37 | 205 | 37 | 0 | 0 |
| Autotest · S4 · Quatrième semaine (`embryo.aut.s4`) | 35 | 256 | 33 | 2 | 0 |
| Autotest · Formation du cœur et des vaisseaux (`embryo.aut.coeur`) | 9 | 92 | 7 | 2 | 0 |
| Annales · Méiose et gamétogenèse (`embryo.ann.gamet`) | 36 | 180 | 26 | 0 | 10 |
| Annales · Fécondation (`embryo.ann.fec`) | 21 | 105 | 15 | 0 | 6 |
| Annales · S1 · Première semaine (`embryo.ann.s1`) | 13 | 65 | 9 | 0 | 4 |
| Annales · S2 · Deuxième semaine (`embryo.ann.s2`) | 14 | 70 | 10 | 0 | 4 |
| Annales · S3 · Troisième semaine (`embryo.ann.s3`) | 39 | 195 | 39 | 0 | 0 |
| Annales · S4 · Quatrième semaine (`embryo.ann.s4`) | 41 | 205 | 41 | 0 | 0 |
| Annales · Formation du cœur et des vaisseaux (`embryo.ann.coeur`) | 24 | 120 | 24 | 0 | 0 |
| Colle en chambre · Méiose et gamétogenèse (`embryo.col.gamet`) | 36 | 124 | 0 | 0 | 36 |
| Colle en chambre · Fécondation (`embryo.col.fec`) | 26 | 129 | 0 | 0 | 26 |
| Colle en chambre · S1 · Première semaine (`embryo.col.s1`) | 18 | 86 | 0 | 0 | 18 |
| Colle en chambre · S2 · Deuxième semaine (`embryo.col.s2`) | 35 | 164 | 0 | 0 | 35 |
| Colle en chambre · S3 · Troisième semaine (`embryo.col.s3`) | 53 | 258 | 0 | 0 | 53 |
| Colle en chambre · S4 · Quatrième semaine (`embryo.col.s4`) | 74 | 351 | 74 | 0 | 0 |

## Sources et méthode de relecture

La comparaison indépendante est partie des **29 PDF de l’archive initiale Embryo.zip** : les 22 corrigés et les 7 sujets distincts. Les pièces individuelles récupérées et les documents conservés dans `sources/revision_v4` ont été examinés comme sources complémentaires. Les anciens audits ont servi à localiser les difficultés ; leurs conclusions n’ont pas constitué à elles seules une preuve.

Les 599 blocs ont été repérés indépendamment dans les originaux, avec numéro imprimé, pages, lignes, positions et marqueurs. Chaque proposition a été comparée au texte et à ses marques de correction : Vrai/Faux, lettres de grille, annotations colorées, mots barrés et explications ajoutées. La lecture des différences a séparé le texte initial des ajouts correctifs. Les numéros et lettres dupliqués ont été rapprochés par le contenu, notamment l’autotest Cœur Q2 et les deux items rétablis.

Le lot préparateur a ensuite été revu, y compris les détails de correction restaurés. Les frontières de questions, la pagination, les contextes communs et les figures ont fait l’objet d’un second passage. Les difficultés mises au jour ont été renvoyées au préparateur puis revérifiées dans sa version figée ; les compléments tardifs sont intégrés directement dans les objets approuvés de ce dossier.

La compilation générale a fourni **60 sujets authentiques** rapprochés de la session et des cinq propositions. Vingt recoupaient les parties non annotées des PDF mixtes ; quarante sujets sont des compléments nouveaux. Les copies de la compilation remplacent ces 60 rôles sujet, ce qui évite notamment qu’un encadré de correction voisin de la figure de l’annale S2 ID14 soit exposé comme sujet.

La première extraction automatique de la compilation commençait à p.1001. Après le signalement de l’agent principal, le début de la section a également été relu : **p.989–1000, les 15 QCM d’embryologie de 2025–2026 (Q1–14 et Q25), soit 75 propositions**. Ils sont distincts des 599 QCM existants, dont les annales thématiques s’arrêtent à 2024–2025. Les rapprochements partiels correspondent à des expressions ou thèmes communs, pas à un même sujet. Aucune de ces 15 nouvelles questions n’est importée dans cet audit ; aucune capture de version simplement voisine n’est présentée comme preuve identique. Voir `compilation_early_comparison.json`.

## Réparations et compléments majeurs

### Clés et propositions

**Sept clés auparavant absentes sont rétablies**, à partir de la grille p.1232 et des cinq verdicts détaillés correspondants de la compilation, après appariement du sujet :

| Banque / ID du site | Numéro imprimé | Clé | Page du corrigé détaillé |
|---|---:|---|---:|
| Annales Gamétogenèse 27 | 1 | AB | 1233 |
| Annales Gamétogenèse 28 | 2 | DE | 1233 |
| Annales Fécondation 17 | 3 | AE | 1234 |
| Annales Fécondation 18 | 4 | ABDE | 1234 |
| Annales S1 9 | 5 | BDE | 1235 |
| Annales S1 10 | 6 | C | 1235 |
| Annales S2 9 | 7 | B | 1236 |

La clé **RIEN** de l’annale S3 ID26, Q11 imprimé, était déjà correctement configurée comme réponse vide valide ; elle a été **confirmée**, et ses cinq détails complétés depuis p.1238. Il ne faut donc pas compter huit clés absentes réparées.

Les huit jeux de correction concernés conservent les deux documents : corrigé thématique et corrigé complémentaire de la compilation. Les panneaux portent leur propre `fileLabel` et `sourceNumber`, et une `correctionNote` distingue leur origine. Les détails ne sont pas fusionnés sans attribution.

Deux propositions auparavant perdues sont rétablies :

- Autotest Méiose ID5 : seconde proposition imprimée K sur le brassage intrachromosomique en méiose I, conservée sous la lettre libre O, immédiatement après K. La clé inclut O ;
- Autotest Fécondation ID23, Q24 imprimé : seconde proposition M sur la sous-unité alpha, conservée sous N, avec le verdict Faux et la correction « Béta ».

Le second J de l’autotest Méiose est une répétition identique ; il n’est pas ajouté une seconde fois. Les anciens identifiants restent stables. Le contrôle de notation doit tenir compte du mode de lettres multiples de l’autotest Cœur Q1 (`AA`, `CC`, etc.), déjà présent dans la base.

### Énoncés, détails et contextes

Le diff final par rapport à V5 comporte **17 énoncés de propositions existantes réparés**, les **2 propositions rétablies**, et **353 champs de détail modifiés ou complétés**, répartis sur 156 QCM. Ce décompte décrit des champs de données ; il ne signifie pas 353 nouvelles erreurs scientifiques.

Parmi les réparations vérifiées :

- Annales S2 IDs12/13 : suppression d’un mélange de corrections causé par un sujet sans numéro sur la page. L’ID12 retrouve exclusivement A/B/E de sa propre grille CD ; l’ID13 garde sa grille AB et ses détails C/D/E, avec copie du groupe exact ;
- Annales Gamétogenèse ID13 : retrait des corrections parasites des items B et D et restitution de « en métaphase I » dans A depuis le sujet original p.1604 ;
- Annales Gamétogenèse ID10A : restitution de la portion de phrase barrée qui appartenait à l’énoncé, sans y incorporer le texte correctif « à 21 J » ;
- Annales Gamétogenèse ID15E : restitution d’« ovocytes I » ; annale S2 ID14B : « lame choriale » ;
- Annales S1 ID12 : J3/J4 et le mot Faux relus sur le vrai corrigé ; annale S3 ID13E : fin du détail sur la plaque préchordale et SHH rétablie ;
- Autotest S3 ID8D : ajout de la fin de l’explication distinguant la coupe décrite de celle représentée ;
- retrait de deux marqueurs HP qui s’étaient glissés dans les énoncés d’items de S1, tout en conservant leur exclusion de notation ;
- déplacement des consignes communes hors des derniers items des QCM précédents, conservation des schémas communs des groupes concernés, et réparation des pages de référence des groupes Colle S3 31/32 et 41/42 ;
- années des annales Fécondation IDs13/14 corrigées en 2020–2021 ; le sujet original l’indique ;
- retrait des avertissements de consigne introuvable devenus obsolètes pour Colle S4 54/55/68.

Le sujet de l’annale S2 ID6 est numéroté 10 dans la compilation et 7 dans le document thématique : cette divergence est explicitement indiquée dans sa copie, et le numéro propre à chaque capture est conservé.

### Contradictions scientifiques ou documentaires

Les corrigés restent la référence de notation. Les divergences repérées sont signalées **après correction**, avec leurs références. Les notes antérieures sont conservées ; ce travail ne prétend pas constituer une nouvelle vérification de toutes les pages de cours citées dans chacune des notes V4.

Les nouvelles remarques appuyées sur des documents consultés concernent notamment :

- la distinction entre centriole distal et axonème (Annales Gamétogenèse ID25D, fiche de synthèse Gamétogenèse p.4) ;
- la barrière placentaire et la différence entre échanges et contact direct des circulations (Annales S3 ID11E, ronéo S3 p.7 et suivantes) ;
- l’usage du terme « processus chordal » selon qu’il désigne la première structure ou toute son évolution (Annales S3 ID26A, ronéo S3 p.22) ;
- la confusion entre plaque préchordale et plaque chordale dans un détail de correction (Annales S3 ID29B, ronéo S3 p.24–27) ;
- les tubules mésonéphrotiques et le canal de Wolff (Annales S3 ID30D, ronéo S4 p.27–28).

Pour l’annale Fécondation ID18B, le corrigé thématique barre « cellules du cumulus » au profit de « zone pellucide », alors que la grille et le détail de la compilation donnent Vrai. Les deux références sont visibles ; la clé ABDE de la grille explicite est utilisée et le désaccord est signalé, avec invitation à vérifier dans la ronéo. Il n’est pas présenté comme un consensus scientifique.

La ronéo S3 p.47 admet explicitement le rapprochement épiblaste/ectoblaste dans le contexte examiné. Aucune fausse alerte n’est ajoutée sur ce seul choix de terme.

## Vérification des copies et protection des réponses

Les 1 048 rectangles ont été confrontés aux dimensions des pages et aux lignes attendues, y compris les fins d’items sur la page suivante et les blocs communs. Les chevauchements de figures dans des mises en page en colonnes ont été repris en plusieurs panneaux : texte, puis figure originale complète. Aucun pixel correctif n’a été effacé pour fabriquer un faux sujet vierge.

Le contrôle visuel explicite couvre :

- les 60 nouvelles copies sujet de la compilation, chacune vue ;
- les 8 copies de correction complémentaire, chacune vue ;
- les 34 ensembles uniques recadrés, représentant 46 rôles de QCM, chacun vu ;
- les 21 pages originales où les figures et les colonnes créaient un risque de mauvais cadrage.

Le registre des rôles contrôlés visuellement contient 114 rôles de 95 QCM. Les autres cadrages ont fait l’objet de la confrontation documentaire et géométrique exhaustive. **Il ne faut pas présenter les 599 copies comme ayant toutes été affichées et lues individuellement à l’écran.** Les alertes géométriques restantes sont expliquées une à une dans `crop_flag_resolutions.json` : 18 sont des textes du groupe suivant mal rattachés par l’ordre d’extraction PDF ; la dernière est l’espace après « Faux », dont tous les caractères sont visibles.

Quatre sujets fournis comme ENONCE contiennent déjà des réponses :

- Autotest S4 23/24 : le cartouche « Là où se trouvent les IWP » est présent dans l’original ;
- Autotest Cœur 5/6 : les vaisseaux sont déjà nommés, avec les repères demandés par les items manquants.

Leurs copies sont protégées par `subjectAfterCorrection:true`. Les figures existantes sont également protégées dans les données `q.imagesAfterCorrection` et `sharedContexts[].imagesAfterCorrection`. La recherche des chemins dans les objets finaux ne révèle pas de duplication non protégée dans `originalImages`, `stemImages` ou un autre champ d’image. L’intégration UI et son contrôle final incombent au builder principal.

## Pièces encore nécessaires

Les 280 sujets absents concernent : les 6 autotests sans sujet séparé (Méiose, Spermatogenèse, Ovogenèse, Fécondation, S1, S2), les 5 colles Gamétogenèse/Fécondation/S1/S2/S3 et les premières séries des 4 annales Gamétogenèse/Fécondation/S1/S2. `missing.json` donne les identifiants exacts, sans demander de nouveau les sujets déjà retrouvés dans la compilation.

Il faut également les deux schémas vierges décrits ci-dessus pour les quatre QCM actuellement protégés.

Les six QCM maintenus hors note sont : Annales Fécondation ID4, Annales S1 ID13, Colle S3 ID11, Colle S4 IDs13,16,70. Leurs sources comportent respectivement une clé ambiguë avec lettre dupliquée, une réponse conditionnelle, ou un verdict incomplet. L’item E de Colle S4 Q70 est totalement absent du corrigé. Aucun verdict n’est comblé par une déduction scientifique présentée comme officielle.

## Vérifications finales d’intégrité

Les 599 identifiants, les 22 banques, l’ordre relatif des anciennes propositions, l’appartenance des clés aux lettres existantes et les liens locaux des notes ont été vérifiés. Les marqueurs HP restent hors de l’énoncé et sont pris en charge par la notation existante. La protection des quatre figures annotées est conservée dans les objets approuvés. Le script `build_approved.py` permet de reproduire la fusion depuis le lot préparateur figé ; `final_audit.py` produit le bilan et les empreintes. Aucune écriture n’a été faite dans `output/site` par ce vérificateur.
