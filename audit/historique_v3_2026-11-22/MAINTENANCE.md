# Maintenance — état du 22 novembre 2026

## Périmètre à préserver

Le site contient 2788 QCM /217 banques. La dernière révision est limitée aux 336 QCM de pharmacologie UE4 : quinze banques par thème, toutes années réunies. Les 2452 autres QCM /202 banques restent identiques à la version du 21 novembre. Ne modifier ni UE1, ni UE5, ni biomol/ED, biochimie ou biostatistiques sans nouvelle instruction.

Ne pas introduire de QCM antérieur à 2015. Traiter un sujet et son corrigé à la fois. Relire les cinq items, la consigne, les contextes de la page précédente, les figures et les limites entre QCM. Les titres reprennent la consigne ; fichier et page restent discrets. Une question conserve ses cinq propositions ensemble, même si son contenu couvre plusieurs thèmes.

## Données et interface

`index.html` regroupe CSS, interface et JavaScript. `const EXAMS=` est du JSON. Chaque banque possède `ue`, `courseId`, `kind`, `questions`, des libellés et une ancienne clé `storage`. Les banques UE4 sont `ue4.annales.theme.<themeId>`, avec `pharmaGrouped:true` et `kind:annales`. Les quinze libellés et leur ordre sont figés dans le fichier de thèmes de l’audit courant.

Les champs `question` et `options[].text` sont exclusivement des énoncés. Les champs `explanations`, `generalExplanation`, `correctionImages` et `reviewNotes` sont des corrections et ne s’affichent qu’après validation. Les `reviewNotes` ont les champs `items`, `text`, `kind` : motif précis, pas de correction inventée, et invitation à vérifier la ronéo. `pharmaWarningCovered` signifie que la nouvelle réserve reprend déjà le motif du champ historique `warning` ; ce dernier reste conservé dans les données et l’audit.

Identité de contenu : `sourceId`, par exemple `ue4:2023-2024:S2:q05`. Le champ `id` est seulement le numéro local d’affichage dans le thème. `sourceNumber` et, le cas échéant, `printedSourceNumber` restent les numéros du sujet. `correctionNumber` peut être différent (décalage de numérotation documenté en 2021–2022 S1).

## Source et notation

Les pages de `subjectPage`, `sourceStartPage`, `sourceEndPage`, `correctionPage` sont en base 1 dans `sources/Annales_compilation.pdf`, sauf banques historiques avec `sourcePdf`/`correctionPdf` distincts. Ne pas mélanger PASS et PACES d’une même année.

`answer` est la clé retenue ; vide signifie hors note sauf `answerIsEmpty:true`. `rawAnswer` conserve la clé imprimée quand elle est disponible. 325 QCM UE4 sont notés et 11 sont hors note. Le seul changement de clé de cette révision est 2023–2024 S2 Q5 : vide → ACE, confirmé par la grille p794 et l’encadré p796 ; les justifications de Q6 avaient été importées par erreur. Les autres clés sont inchangées. Une réserve scientifique nouvelle ne doit pas être présentée comme une résolution de la contradiction : conserver la clé source et signaler le problème, sauf nouvelle décision étayée et documentée.

Barème existant : 10/5/2/0 points pour 0/1/2/3+ erreurs, conversion sur20, coefficients éventuels. `∅` distingue une réponse volontaire « aucune proposition » d’un blanc. L’option est affichée à tous les QCM importés, pas seulement lorsque la clé est vide.

## Sauvegarde UE4 après reclassement

La progression est indexée par `sourceId` dans `qcm-pass-ls-ue4-progress-by-source-v1` (profil1) et la même clé suivie de `_profil_2_v1` (profil2). Schéma : `{version:1,bySource:{sourceId:{answer,corrected}}}`. Les anciennes correspondances sont dans `PHARMA_PROGRESS_LINKS` et `legacyProgress` ; `PHARMA_EXAM_ALIASES` retrouve un thème depuis une ancienne banque sélectionnée.

La migration ne remplit que les identités absentes ; elle conserve les anciennes clés de stockage sans les écraser. Une entrée vide après réinitialisation est volontaire : ne pas l’interpréter comme un motif de réimportation. La sauvegarde ne met à jour que les QCM du thème courant. Les deux profils sont indépendants. Les états corrigés partiels sont conservés même dans le profil2, car plusieurs anciennes séries annuelles peuvent être réunies dans un thème ; la correction globale termine les questions restantes du thème. La note ne compte que les QCM corrigés tant que le thème n’est pas entièrement corrigé.

Hors UE4, les clés et le fonctionnement antérieurs sont inchangés : profil1 `storage`, profil2 `storage+'_profil_2_v1'`. Préférence `ssh_pass_only_filled_mode_v1`, banque sélectionnée `ssh_pass_selected_exam_v1`.

## Énoncés communs et images

`sharedContexts` contient les données partagées (id, text, images, questionNumbers, questionIds, pages et source). Le bloc est affiché avant le premier membre visible, y compris en recherche/filtrage. Une reclassification peut changer `questionIds`, jamais les numéros sources ou le contenu partagé. `references` et `referenceImages` sont les annexes ; les données indispensables restent visibles dans le bloc commun.

`images`, `stemImages`, `options[].image` et `originalImages` contiennent les éléments de sujet ; aucune réponse ne doit y être introduite. `correctionImages` est réservé à l’après-correction. Les fichiers source doivent rester exacts. Ne jamais reconstituer par génération une figure médicale ou chimique précise. La révision du 22 novembre n’a créé aucun asset et n’a modifié aucun octet d’image/PDF ; elle a retiré un mauvais rattachement de capture au Q5 2023–2024 S2.

Les réparations antérieures des énoncés communs biomol/ED, biochimie et biostatistiques restent applicables. Les détails sont dans l’historique du 21 novembre et les manifestes dédiés. Les quatre clés ED réappariées à cette date ne doivent pas être régressées.

## Reproduction et contrôles

Le dossier `audit/pharmaco_2026-11-22/` conserve les instructions, le cliché immuable de la version précédente, les fiches par sujet, les décisions de patch et les scripts de cette révision. Les chemins d’exécution sont ceux du workspace de production ; adapter les racines si le dossier est déplacé. Ne pas relancer l’ancien constructeur général sans porter les changements UE4 : il rétablirait le classement annuel.

Ordre de la révision courante : `build_pharma.py` → `test_pharma.cjs` → `audit_pharma.py` → `write_report.py` → conditionnement ZIP et manifeste SHA256. Le mode `--draft` du constructeur/tests est seulement une simulation de migration avec un classement provisoire : ne jamais le livrer.

Avant livraison, préserver exactement les données hors périmètre, contrôler tous les identifiants, les références d’images, l’absence de fuite de correction, les deux profils, la migration et la remise à zéro. Les contrôles JavaScript actuels utilisent un adaptateur DOM ; ils ne certifient pas la mise en page d’un navigateur. La revue documentaire ne certifie pas la justesse scientifique des corrigés litigieux : leurs réserves doivent rester visibles après correction.
