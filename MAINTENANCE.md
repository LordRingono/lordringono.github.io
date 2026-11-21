# Maintenance — structure et règles durables

## Instructions à conserver

Préserver les banques UE1, UE5 et biologie moléculaire UE2 hors ED. La demande du 21 novembre 2026 autorise les corrections ciblées d’énoncés/items des banques ue2.ed.annales, ue2.ed.2025-2026 et ue2.ed.2026-2027 ; leurs IDs, pondérations et sauvegardes restent inchangés. Seules quatre clés des annales ED sont réappariées au corrigé : locaux6 C,7 B,8 BC,13 BD (PDF corrigé p3,4,6). N’ajouter aucun QCM antérieur à 2015. Traiter un sujet et son corrigé à la fois, puis relire consignes, propositions, schémas et clés. Ne pas confondre annales PASS et PACES d’une même année. Les contextes peuvent commencer à la page précédente.

Les titres contiennent les consignes ; fichier/page restent discrets. Aucune correction ni identification manuscrite ne doit apparaître dans les panneaux de l’énoncé. Prendre les figures exactes du sujet, avec toute leur information scientifique. Documenter tout recadrage excluant une annotation. L’unique reproduction de figure depuis un corrigé est le schéma UE2 2020 S1 Q30, p322, rectangle [42.85,212.59,538.55,337.09] : contrôlé sans réponses, rôle distinct et provenance explicite.

Dans les annales importées UE2c/UE3/UE4, une contradiction formelle entre clés/verdicts, une correction absente ou un item matériellement différent entraîne un QCM hors note. Les ED biomol suivent leurs clés imprimées, avec réserves de source explicitement affichées pour ED2026 Q31 et annales ED local38 ; ne pas interpréter ces réserves comme une résolution scientifique de la contradiction. Ne jamais inventer une clé. Les erreurs purement typographiques sont signalées et la source reste consultable.

## Structure

`index.html` contient le style, l’interface et le script. `const EXAMS=` est un objet JSON, suivi de `const EXAM_ORDER=`. Chaque banque possède une clé stable, une unité (`ue`), un cours (`courseId`), un type (`kind`), les libellés, une clé de sauvegarde (`storage`) et une liste de questions (`questions`).

Banques originales : 80 / 1 950 questions. Parmi elles, 77 banques / 1 824 questions restent identiques ; seules les 3 banques ED biomol / 126 questions sont révisées pour la présentation fidèle de leurs énoncés, items, figures et annexes. Nouvelles unités : `ue2c`, `ue3`, `ue4` — 276 banques / 838 questions. Les empreintes des banques et images de référence sont conservées dans `audit/empreintes_base_protegee.json`.

Une question possède un `id` local séquentiel. Le numéro d’origine est `sourceNumber`, avec `printedSourceNumber` et `correctionNumber` lorsque la numérotation diverge. `question` est la consigne ; `options` contient les cinq choix A–E. `answer` est la clé utilisée ; une chaîne vide signifie hors note sauf si `answerIsEmpty:true`. `rawAnswer` conserve, lorsqu’elle existe, la clé source écartée. `warning` explique les réserves.

Champs de provenance : `sourceSubject`, `sourceCorrection`, `subjectPage`, `sourceStartPage`, `sourceEndPage`, `correctionPage`, `correctionEndPage`. Les pages sont celles du PDF compilé en base1, sauf pour les ED biomol dont sourcePdf/correctionPdf désignent le PDF distinct. Les fichiers source sont conservés sans modification.

## Énoncés partagés

`sharedContexts` contient une liste ordonnée de contextes : id stable, text, images, questionNumbers (source), questionIds si nécessaire, sourceStartPage, sourceEndPage, sourceFile et sourcePdf. Le même objet est attaché à tous les QCM concernés. Le rendu montre un bloc distinct avant le premier membre visible d’un groupe, puis les sous-contextes aux endroits nécessaires. La recherche inclut le texte partagé. Ne pas conserver le même paragraphe/figure dans un item ou dans les médias locaux.

`references` contient les annexes repliables avec titre, images et provenance ; les données indispensables pour répondre restent dans l’énoncé commun visible. Les ED révisés portent contextRevised:true mais ne reçoivent pas fromCompilation ni l’option Aucune proposition ajoutée aux nouvelles annales.

## Images

- `images` / `stemImages` : figures et contextes visibles avant réponse.
- `options[].image` : formule ou schéma associé à une proposition.
- `originalImages` : extraits de l’énoncé en volet repliable.
- `referenceImages` : annexes statistiques ; `referenceTitle` et `referenceNote` indiquent leur provenance.
- `correctionImages` : affichage seulement après correction du QCM.
- `stemCaption` : légende particulière lorsque la provenance l’exige.

Chaque image d’annales est répertoriée dans le manifeste de son UE : page, rectangle source, rôle et références. La page HTML référence des chemins relatifs `static/...` et le PDF `sources/Annales_compilation.pdf`. Conserver l’ensemble du dossier lors de la distribution.

## Profils et notation

Les anciennes clés `storage` restent inchangées. Profil1 : `storage` ; profil2 : `storage+'_profil_2_v1'`. Préférence de mode : `ssh_pass_only_filled_mode_v1`. Banque sélectionnée : `ssh_pass_selected_exam_v1`.

Tous les nouveaux QCM portent `fromCompilation:true` et `allowNoAnswer:true`. La réponse choisie `∅` signifie « aucune proposition », distincte d’un blanc. Ne pas afficher cette option uniquement sur les questions dont la clé est vide : cela révélerait la réponse.

Barème existant conservé : 10/5/2/0 points pour0/1/2/3+ erreurs, conversion sur20, coefficients éventuels. En mode sélectif, seuls les QCM renseignés et corrigés comptent dans la note. Les états des deux profils restent séparés.

## Reprendre le contrôle

Consulter d’abord `CONTROLE_ANNALES.md`, l’inventaire CSV et les manifestes par UE. Les JSON de vérification indiquent ce qui a été réellement testé. Les vérifications d’état/rendu utilisent le script réel avec un adaptateur DOM ; elles ne remplacent pas une inspection visuelle dans un navigateur.

Préserver les identifiants et sauvegardes pour les mises à jour futures. Après toute modification, comparer les données protégées et les images de référence, contrôler les contextes/pages, puis vérifier correction sélective, profils, notation, absence de fuite et présence des fichiers d’image. Ne pas supprimer les réserves documentaires sans nouvelle source permettant de les résoudre.
