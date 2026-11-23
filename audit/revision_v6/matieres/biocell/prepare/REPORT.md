# BIOLOGIE CELLULAIRE — préparation V6

## État du lot

**Préparation exhaustive terminée ; approbation du vérificateur indépendant encore requise.**

Le lot comprend **18 banques, 230 QCM et 1 137 items** : 104 QCM / 507 items d’autotests et 126 QCM / 630 items d’annales. Les **224 IDs V5 sont conservés**. Six QCM omis sont restaurés avec de nouveaux IDs. Les coefficients des questions préexistantes restent identiques à la V5, ainsi que leur banque et leur classement. Les deux profils et les clés de stockage ne sont pas modifiés par ces fichiers.

**226 QCM peuvent être notés ; quatre restent hors note.** Quatre clés officiellement entièrement fausses emploient le support natif answer vide, answerIsEmpty=true, allowNoAnswer=true. Les questions sans clé exploitable ont une réponse vide sans ces deux indicateurs.

La vérification documentaire comporte une entrée par QCM et une preuve par item : énoncé, positions du texte, police/gras/couleur disponibles, verdict littéral, commentaire, différences et décision. Les rasters et les annotations graphiques ont été lus visuellement. Les contrôles de structure complètent cette lecture et ne constituent pas seuls l’audit.

| Banque | QCM V5 → V6 | Items V5 → V6 | Hors note |
|---|---:|---:|---:|
| bio.cm2oral | 7 → 7 | 35 → 35 | 0 |
| bio.cm3 | 10 → 10 | 52 → 52 | 0 |
| bio.cm4 | 10 → 10 | 51 → 52 | 0 |
| bio.cm5 | 17 → 17 | 81 → 82 | 0 |
| bio.cm6 | 13 → 13 | 60 → 60 | 1 |
| bio.cm7 | 11 → 14 | 41 → 44 | 0 |
| bio.cm8 | 16 → 17 | 102 → 105 | 0 |
| bio.cm9 | 11 → 11 | 53 → 53 | 0 |
| bio.cm10 | 5 → 5 | 24 → 24 | 1 |
| bio.ann.cm2 | 15 → 15 | 75 → 75 | 0 |
| bio.ann.cm3 | 13 → 13 | 65 → 65 | 0 |
| bio.ann.cm4 | 8 → 9 | 40 → 45 | 0 |
| bio.ann.cm5 | 16 → 16 | 80 → 80 | 2 |
| bio.ann.cm6 | 25 → 25 | 125 → 125 | 0 |
| bio.ann.cm7 | 12 → 12 | 60 → 60 | 0 |
| bio.ann.cm8 | 13 → 13 | 65 → 65 | 0 |
| bio.ann.cm9 | 9 → 10 | 45 → 50 | 0 |
| bio.ann.cm10 | 13 → 13 | 65 → 65 | 0 |

## Fichiers remis et sources

- **reviewed.json** : objets complets des 230 QCM.
- **audit.json** : 230 entrées, 1 137 items, positions/styles, ancien/nouveau contenu, errata, changements de notes et décisions.
- **crops.json** : 230 lignes sujet/corrigé, **614 panneaux et 590 captures distinctes**.
- **source_manifest.json** : 37 sources directes, identité PDF/Word, empreintes, pagination et comparaison des neuf PDF complémentaires.
- **missing.json** : six demandes documentaires précises.
- Ce rapport.

Aucun fichier du site publié n’a été modifié.

Les 18 Word originaux des autotests ont été lus dans leurs rendus sans modification. Les neuf PDF individuels de sujets ont été confrontés aux rendus : texte des questions, styles par caractère (gras, italique, couleur) et géométrie des images concordent. Les différences d’extraction concernent des blancs, les noms/métriques des polices et un pictogramme décoratif du CM10 ; les indicateurs bruts et leur interprétation sont dans le manifeste.

Les 18 PDF thématiques d’annales ont été confrontés aux corrections correspondantes et, lorsqu’il fallait retrouver un sujet propre, une figure ou un verdict absent, à la compilation de 1 660 pages. La section UE5 commence avant p. 1040 : les sujets 2025–2026 débutent p. 1001. Les éditions antérieures recherchées vont jusqu’à 2018–2019.

Pour chaque substitution de sujet, les cinq propositions et l’édition ont été rapprochées. Les numéros imprimés du sujet et du corrigé sont conservés séparément. Une correction voisine n’a pas été transférée au seul motif qu’une question lui ressemble.

Les trois premiers QCM d’annales CM2 étaient représentés par des formulations de remplacement incomplètes. Leurs 15 propositions ont été transcrites depuis les rasters originaux, comparées individuellement aux textes natifs de la compilation et rapprochées de tous les verdicts/commentaires. L’audit garde les positions précises de la compilation et les panneaux raster thématiques lus.

## Réparations structurelles des autotests

Les changements d’options figurent avant/après dans chaque audit. Les lettres suivent l’ordre réel du sujet ; les IDs préexistants ne sont pas recyclés.

| Banque / ID stable | Réparation | Résultat |
|---|---|---|
| CM4 / 5 | Premier A absorbé dans le titre | Six items A–F ; ABC |
| CM5 / 5, imprimé 6 | Faux isolé perdu | BDEF rétabli |
| CM5 / 12, imprimé 13 | Fin de D tronquée | « noyau » retrouvé dans le corrigé |
| CM5 / 13, imprimé 14 | Premier A absorbé dans le titre | Six items ; ABCF |
| CM6 / 7 | B absent du corrigé ; lettres suivantes décalées | A→A, C→B, D→C, E→D ; hors note |
| CM7 / nouveaux 12,13,14 | Trois QCM à une proposition omis | Réintégrés dans l’ordre source |
| CM7 / 9–11 | Consigne des pores nucléaires tronquée | Consigne complète retrouvée |
| CM8 / 6 | Sujet fusionnant deux propositions dans B ; corrigé à cinq items | Quatre items du sujet conservés, tous vrais : ABCD |
| CM8 / 7 | Faux isolé perdu | CDE |
| CM8 / 10 | Premier A perdu | Huit items ; BDEF |
| CM8 / 13 et nouveau 17 | Deux QCM fusionnés en dix options | ID 13=Q13, cinq items ABD ; ID 17=Q14, cinq items DE |
| CM8 / 15, imprimé 16 | Premier A perdu | Six items ; ABDE |
| CM8 / 16, imprimé 17 | Premier A perdu | Neuf items ; ABCFGI |
| CM10 / 1 | Quatre items au sujet, cinq au corrigé ; fusion dans A | Divergence conservée, hors note |

Les clés entièrement fausses concernent les autotests CM4 ID 10, CM7 IDs 2 et 8, et les annales CM6 ID 24. Les trois premières acquièrent le marquage natif manquant en V5 ; la dernière le conserve.

L’autotest CM5 ID 11, imprimé Q12, présente deux formulations différentes de A. Le texte du sujet et la clé A du corrigé sont conservés, avec une comparaison après validation et la réserve scientifique déjà sourcée sur l’exemple transferrine/fer.

## Ajouts d’annales et labels

Deux QCM omis sont rétablis, sans ajout antérieur à 2015 :

- **Annales CM4 ID 9 : Q56, 2019–2020**, session non précisée. La grille « RIEN » est suivie d’un erratum B VRAI : clé B. L’année est prouvée par l’en-tête thématique et le sujet correspondant de la compilation.
- **Annales CM9 ID 10 : Q43, 2023–2024, session1**. Le sujet imprime F–J, le corrigé A–E. Les lettres F–J restent présentes ; le E vrai du corrigé correspond à J : clé J.

Le mapping F↔A, G↔B, H↔C, I↔D, J↔E est aussi documenté pour l’ID 12 préexistant des annales CM7, clé FI. La copie propre de la compilation imprime A–E : son attribution reste distincte du sujet thématique F–J et la différence est signalée.

Les écarts de numéro sont tracés, notamment annales CM3 sujet Q1 / corrigé Q36 et sujet Q3 / corrigé Q37 ; membranes CM6 sujets Q29–30 / corrigés Q39–40. Le numéro31 du cytosquelette, absent de l’extraction mais imprimé dans les deux PDF, est restauré.

## Errata officiels

**Treize verdicts graphiquement rectifiés, dans douze QCM, vérifiés visuellement.** Les grilles initiales, le verdict ajouté, les positions de l’annotation et la capture restent disponibles.

| Banque / ID stable | Erratum | Clé appliquée |
|---|---|---|
| Annales CM4 / 2 | C FAUX → VRAI | BCE |
| Annales CM4 / 4 | A FAUX → VRAI | AD |
| Annales CM4 / 7 | C et E VRAI → FAUX | ABD |
| Annales CM4 / nouveau 9 | B FAUX → VRAI après grille RIEN | B |
| Annales CM5 / 4 | D VRAI → FAUX | BE |
| Annales CM5 / 9 | A VRAI → FAUX | BDE |
| Annales CM5 / 10 | C FAUX → Vrai | ACE |
| Annales CM5 / 15 | E VRAI → FAUX | ABD |
| Annales CM7 / 5 | C VRAI → FAUX | B |
| Annales CM7 / 8 | B VRAI → Faux | E |
| Annales CM8 / 1 | D VRAI → Faux | ACE |
| Annales CM9 / 7 | B VRAI → Faux | CE |

Pour **CM8 ID 1**, deux preuves distinctes sont nécessaires : compilation p. 1038, B FAUX et grille ACDE ; corrigé thématique, erratum D Faux. La clé ACE applique ces deux éléments, expliqués et montrés séparément après validation.

Les ratures des **annales CM5 IDs 1 et 2** ne désignent pas une clé unique. La compilation p. 1041 propose aussi des grilles incompatibles avec des verdicts thématiques. Les deux QCM restent hors note, avec les deux preuves après validation. Aucune interprétation conjecturale des ratures ne sert de clé.

Deux contradictions textuelles sans erratum graphique restent signalées avec leur grille conservée : **CM6 ID 7**, grille A et commentaire VRAI puis « donc FAUX » ; **CM7 ID 10**, grille ABCE et commentaire B FAUX.

Le Q29 de transport vésiculaire garde **BDE en CM4** et devient **BE en CM5**, seule cette dernière édition contenant l’erratum D. La même expérience de sénescence conserve aussi les clés distinctes de CM2 et CM10. Les éditions ne sont pas fusionnées.

## Figures, contextes et captures

Les **91 images interactives de 73 QCM** renvoient à des rectangles authentiques présents dans crops.json, limités à la figure, sa légende ou son protocole. Ce ne sont pas des reconstructions. Leur identité suit exactement le builder : SHA256 du PDF, page et rectangle arrondi à quatre décimales. Aucun asset_manifest.json supplémentaire n’est nécessaire.

**48 sujets annotés** ont reçu un panneau propre correspondant : 7 CM4, 10 CM5, 24 CM6, 7 CM7. Les pages et dispositions ont été examinées. Le seul sujet encore annoté est **annales CM6 ID 25, Q42 de 2017–2018** : subjectAfterCorrection=true, avec explication ; la copie est différée après validation. Les ratures ne sont ni effacées ni retouchées.

Restaurations sensibles :

- Autotest CM2 oral IDs 2–3 : expérience commune des cinq levures/GFP et labels 1.A–1.E.
- Autotest CM3 ID 5 : document 2, cellules de levure. Le Word possède un rognage original explicite de 40,501 % à gauche ; le sujet montre C–D et une barre de 10 µm. L’ancienne image A–D est remplacée par la figure réellement imprimée.
- Autotest CM3 ID 10 : trois schémas de mitose et paragraphe explicatif dans les panneaux du corrigé uniquement.
- Autotest CM8 IDs 5–7 : grande boîte PDF brute de l’image Q6 et masque Word. Captures resserrées sur le contenu visible, sans questions voisines.
- Annales CM5 ID 8 et CM7 ID 5 : protocoles/figures situés avant le numéro du QCM.
- Annales CM5 IDs 11–12 : figure 4 commune ; IDs 13–14 : protocole anti-Sec62/anti-Rab7 et figure 2 communs.
- **CM5 ID 16, Q51** : protocole MTM1/UBQLN2/GFP p. 10 et véritable figure 6 p. 11 avec ses six panneaux. Ancienne alerte de figure manquante retirée.
- **CM6 ID 7, Q36** : véritable figure 1 de Donnan et protocole p. 1222, avant Q36 p. 1223. Figures C–E conservées ; le manque de figure est résolu, le conflit du corrigé demeure.
- CM7 ID 4 : ADN après E ; copie propre p. 1225 étendue jusqu’au bas effectif de la figure, plus figure seule complète.
- CM2 et CM10 : protocoles END-MSC/étoposide/ouabaïne et BRAF, légendes, cytométrie et résultats précédents nécessaires à « toutes les données ». Cinq items et édition rapprochés pour les figures communes ; corrections propres à chaque banque.
- CM2 IDs 13–15 : contexte et résultats communs alpha-synucléine, dont la figure 1 nécessaire à la question suivante.

Les panneaux de correction incluent les annotations marginales. Les captures ont été contrôlées contre les positions des textes ; les en-têtes et contextes de la question suivante sont exclus lorsqu’ils sont sans rapport. Une légende flottante de Q5 a été retirée de la preuve technique d’un item du Q8, où elle était mal rattachée par l’ordre d’extraction.

## Remarques scientifiques et notation

Les réserves existantes restent après validation et gardent leurs références de cours. Celles précisément résolues par un erratum ou une figure retrouvée sont mises à jour, avec ancien/nouveau texte dans l’audit. Les réserves non résolues sur B de CM4 ID 7, B/D de CM5 ID 15, D de CM7 ID 5, les différences entre éditions et la sénescence restent présentes.

Le nouveau CM4 Q56 reçoit la même réserve GPI que l’item identique de Q33, après relecture de la ronéo RE p. 14. Le verdict officiel reste VRAI. L’incohérence « nucléotides » / « AA » du commentaire officiel est signalée sans réécriture scientifique.

Les annales CM8 IDs 6 et 7 impriment « 1,5 point » ; leur coefficient V5 reste 1 selon instruction explicite. La différence est expliquée après validation.

## Limites et pièces à demander

1. Autotest CM6 Q7 : verdict B absent. Version harmonisée ou confirmation officielle. Hors note.
2. Autotest CM10 Q1 : sujet à quatre items et corrigé à cinq, fusion dans A. Version harmonisée. Hors note.
3. Annales CM5 Q48 (ID 1) : clé finale après ratures ambiguës et divergence de la compilation. Hors note.
4. Annales CM5 Q49 (ID 2) : même besoin de confirmation officielle. Hors note.
5. Annales CM6 2017–2018 Q42 (ID 25) : sujet réellement non annoté. Texte et clé disponibles ; copie annotée différée.
6. Ronéo CM10 sénescence/mort cellulaire 2026 : phénotype sécrétoire et cytokines pro-inflammatoires, pour la divergence scientifique entre annales IDs 7 et 12. Les deux clés du tutorat restent notées.

Les erreurs scientifiques éventuelles ne sont pas assimilées aux erreurs d’import. Les limites ne sont pas présentées comme résolues.

## Passage au vérificateur indépendant

Relire les 230 QCM et 1 137 items depuis les documents, notamment les six ajouts, changements d’options, mappings F–J, treize errata, quatre hors note, quatre clés vides évaluables, sujets propres, figures retrouvées et rognages Word.

Derniers contrôles techniques : aucun ID V5 perdu, aucun coefficient V5 modifié ; 230 audits et 230 lignes uniques ; images interactives reliées aux captures ; rectangles dans leurs pages ; liens de cours existants présents ; aucune position native d’item ou de verdict hors de son panneau. Les trois premiers CM2 ont en plus les preuves textuelles de compilation et les preuves raster thématiques.

Ces contrôles ne valent pas approbation du binôme. Produire la vérification indépendante prescrite dans CONTRAT.md, puis les objets approuvés ou les empreintes d’approbation.
