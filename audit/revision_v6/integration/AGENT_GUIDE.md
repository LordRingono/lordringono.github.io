# Guide opérationnel commun aux binômes V6

Lire d’abord `CONTRAT.md`. La base est `baseline_exams.json` (V5), jamais une ancienne base V2/V4. Chaque matière est assignée par la liste de banques de `roster.json`.

## Travail documentaire

Chaque QCM et chaque proposition doivent avoir une trace de comparaison au sujet et au corrigé disponibles. Les audits anciens servent à repérer les pages ; ils ne remplacent pas la consultation des documents. Séparer les cas vérifiés, les originaux absents et les contradictions de l’original. Lire les contextes avant et après les limites de pages, les exposants/indices, les mots barrés et les figures complètes. Ne pas fusionner une consigne suivante avec un item.

Les champs graphiques existants doivent eux aussi être contrôlés : `images`, `stemImages`, `originalImages`, `options[].image`, `sharedContexts[].images`, `references` et `referenceImages`. Corriger le menu de source ne suffit pas si une image interactive conserve une coupe tronquée ou une réponse annotée.

Préserver les notes scientifiques antérieures. Pour toute nouvelle réserve, consulter une ronéo fournie ou une source primaire pertinente ; formuler le désaccord précisément, avec références, et inviter à vérifier dans la ronéo. Ne pas inventer une clé officielle à partir d’une connaissance scientifique. Un erratum imprimé explicite peut réparer une clé d’import ; une rature sans légende ne suffit pas à inventer un nouveau verdict.

La demande actuelle est l’audit de toutes les banques du site et la réparation de leurs importations. Restaurer les questions omises/fusionnées prouvées dans les séries déjà représentées avec des IDs nouveaux. Ne pas lancer silencieusement une nouvelle importation générale de séries distinctes. Signaler ces dernières dans le rapport. Aucun ajout d’annale antérieure à 2015.

## Formats utiles pour l’intégration

Le préparateur fournit `reviewed.json`, `audit.json`, `crops.json`, `missing.json`, `REPORT.md`. Le vérificateur fournit `coverage.json`, `issues.json`, `missing.json`, `REPORT.md`, et s’il répare quelque chose les versions **complètes** `approved_reviewed.json` et `approved_crops.json`. Donner un feu vert final explicite ; l’existence d’un fichier intermédiaire ne vaut pas approbation.

Pour `crops.json`, chaque question a une entrée `{bank,id,subject:[],correction:[]}`. Chaque panneau utilise `{file: chemin PDF absolu,page: numéro à partir de 1,rect:[x0,y0,x1,y1]}`. Les rôles peuvent comporter plusieurs PDF. Ajouter `fileLabel` et `sourceNumber` au panneau si les numérotations ou documents diffèrent. `subjectMissing`/`correctionMissing` doivent expliquer toute absence. `subjectNote`/`correctionNote` sont des explications affichées dans le menu. Les copies déjà vérifiées de V5 peuvent utiliser `reuseExisting:true`, avec leurs `sourceCopies` inchangés dans les questions.

Si un ENONCE original contient une annotation donnant la réponse, conserver les pixels et utiliser `subjectAfterCorrection:true` avec une note. Protéger aussi toute figure interactive concernée par `q.imagesAfterCorrection:true` ou `sharedContexts[].imagesAfterCorrection:true`. Signaler au responsable si un autre champ nécessite la même protection.

Des nouveaux schémas authentiques peuvent être livrés par `asset_manifest.json` : liste de `{file: chemin absolu du fichier créé,src:"static/revision_v6/<matiere>/<nom>.webp"}`. Les copies doivent provenir des PDF/Word sans retouches trompeuses. Ne pas écrire directement dans `output/site`.

Un `source_manifest.json` peut mapper un Word rendu : `{pdf:chemin PDF,original:chemin DOCX}` ; ou demander un emplacement de PDF avec `{absolute:chemin PDF,packaged:"sources/revision_v6/...pdf"}`. Tous les fichiers signalés doivent exister.

Les QCM dont toutes les propositions sont explicitement fausses ont `answer:""`, `answerIsEmpty:true`, `allowNoAnswer:true`. Un QCM sans clé exploitable a `answer:""` sans `answerIsEmpty:true`, avec la limite expliquée. Respecter `tokenMode` et les labels originaux non A–E.

## Rapport de vérité

Donner des comptes distincts : QCM comparés, propositions comparées, copies sujet propres/annotées/absentes, copies de corrigé, items manquants dans le corrigé, clés complètes/hors note. Ne pas annoncer une visualisation individuelle de toutes les captures si certaines n’ont eu qu’un contrôle documentaire et géométrique. Décrire ce qui a effectivement été effectué.

Les sources principales sont recensées dans `documents_available.json` et `additional_documents.json`. Les matières UE2c/UE3/UE4 utilisent surtout `output/site/sources/Annales_compilation.pdf` (1660 pages), les anciens manifestes dans `output/site/audit/`, et les ronéos sous `sources/revision_v4`. Les premières sources histo/biocell sont dans `work/histo_v5/old_source/`. Toutes les captures finales sont rendues en WebP sans perte par le builder.
