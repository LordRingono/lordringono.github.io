# Maintenance — structure et règles durables

## Instructions à conserver

Préserver les banques UE1, UE5 et biologie moléculaire UE2 existantes. N’ajouter aucun QCM antérieur à 2015. Traiter un sujet et son corrigé à la fois, puis relire consignes, propositions, schémas et clés. Ne pas confondre annales PASS et PACES d’une même année. Les contextes peuvent commencer à la page précédente.

Les titres contiennent les consignes ; fichier/page restent discrets. Aucune correction ni identification manuscrite ne doit apparaître dans les panneaux de l’énoncé. Prendre les figures exactes du sujet, avec toute leur information scientifique. Documenter tout recadrage excluant une annotation. L’unique reproduction de figure depuis un corrigé est le schéma UE2 2020 S1 Q30, p322, rectangle [42.85,212.59,538.55,337.09] : contrôlé sans réponses, rôle distinct et provenance explicite.

Une contradiction formelle entre clés/verdicts, une correction absente ou un item matériellement différent entraîne un QCM hors note. Ne jamais inventer une clé. Les erreurs purement typographiques sont signalées et la source reste consultable.

## Structure

`index.html` contient le style, l’interface et le script. `const EXAMS=` est un objet JSON, suivi de `const EXAM_ORDER=`. Chaque banque possède une clé stable, une unité (`ue`), un cours (`courseId`), un type (`kind`), les libellés, une clé de sauvegarde (`storage`) et une liste de questions (`questions`).

Unités protégées : `ue1`, `ue2b`, `ue5h`, `ue5b`, `ue5e` — 80 banques / 1 950 questions. Nouvelles unités : `ue2c`, `ue3`, `ue4` — 276 banques / 838 questions. Les empreintes des banques et images de référence sont conservées dans `audit/empreintes_base_protegee.json`.

Une question possède un `id` local séquentiel. Le numéro d’origine est `sourceNumber`, avec `printedSourceNumber` et `correctionNumber` lorsque la numérotation diverge. `question` est la consigne ; `options` contient les cinq choix A–E. `answer` est la clé utilisée ; une chaîne vide signifie hors note sauf si `answerIsEmpty:true`. `rawAnswer` conserve, lorsqu’elle existe, la clé source écartée. `warning` explique les réserves.

Champs de provenance : `sourceSubject`, `sourceCorrection`, `subjectPage`, `sourceStartPage`, `sourceEndPage`, `correctionPage`, `correctionEndPage`. Les pages sont celles du PDF compilé en base1.

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
