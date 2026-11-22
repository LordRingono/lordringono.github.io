# Maintenance — état V5, 22 novembre 2026

## Contrat de la présente révision

État : **2 806 QCM/fiches, 217 banques**. Les neuf banques `histo.te1`, `histo.te2`, `histo.tc1`, `histo.tc2`, `histo.tc3`, `histo.tn1`, `histo.tn2`, `histo.tn3`, `histo.autotech` contiennent 128 QCM et 649 items vérifiés. Les 208 autres banques sont identiques à V4. Les anciens IDs, les clés de stockage, les profils, le barème et les anciennes sources sont conservés. Les deux ajouts utilisent les IDs libres 12 et 13 de `histo.autotech`, correspondant aux numéros source 8 et 16. Ne pas confondre ordre du document, ID de progression et numéro source.

## Sources visibles à la demande

Chaque QCM ciblé porte `sourceCopies.subject` et `sourceCopies.correction`, avec `file`, `original`, `pdf`, `converted`, `captures:[{src,page}]` et éventuellement `note`. Les images exactes sont dans `static/histo_v5/`, les Word originaux et les PDF de conversion dans `sources/histo_v5/`. Les anciens Word figurent aussi sous les noms `*_premier_envoi.docx`. Les documents sont non modifiés ; la pagination des Word est celle du PDF livré.

`histoSourceCopy(q, role)` produit un menu replié. Le rôle correction est refusé si `isCorrected(q)` est faux. La copie du sujet est placée après les choix, celle du corrigé à l’intérieur du panneau de correction. Les anciennes copies `originalImages` / `correctionImage` sont masquées uniquement si la nouvelle paire complète `sourceCopies` existe, afin d’éviter les doublons. Les figures ordinaires `images` restent visibles dans l’énoncé. Le CSS `.histo-source-copy` est limité à ces menus.

## Fidélité des données et cas particuliers

Chaque `explanations[lettre]` comporte un verdict explicite puis le détail intégral de la source. Le texte du sujet est conservé ; une restitution d’énoncé doit être prouvée et signalée (TE2 Q9B). TE2 Q11 a la clé ABD. TC3 Q17 a `answer:''`, `answerIsEmpty:true`, `allowNoAnswer:true`. Autotech ID13 garde les choix F–J avec GIJ. TN2 Q7 est une question d’ordre unique, avec cinq événements dans `context`, cinq permutations et la clé E. Pour TE2 Q17, le menu du corrigé explique A–E ↔ F–J.

Les commentaires scientifiques restent après correction et ne remplacent pas les clés officielles. Une divergence entre sujet et corrigé doit être identifiée comme telle, par exemple la valeur ajoutée dans TE2 Q6D. Les trois composants texte d’item / verdict / explication ne doivent jamais être fusionnés.

## Audit et réutilisation

`audit/histologie_v5/quality/coverage.json` couvre les 649 items et les 128 questions. `captures.json` donne les rectangles en points PDF et les pages en base 1 ; la conversion est faite à 144 dpi. `runtime_checks` vérifie les fonctions réelles et les deux profils avec l’adaptateur DOM. Le navigateur local n’a pas pu démarrer : aucun test graphique réel n’est revendiqué.

Les scripts de production et la base HTML V4 sont conservés dans `audit/histologie_v5/production/`. Ils décrivent les chemins de l’espace de production d’origine. Avant une réexécution ailleurs, adapter ces chemins et résoudre les fichiers via `documents_sources.json` ; ne pas lancer un constructeur ancien qui écraserait V5. Les PDF nécessaires aux captures et les données relues par série sont tous dans l’archive. Les règles de migration et de notation V4 ci-dessous restent applicables.

---

## Référence historique V4

# Maintenance — révision V4, 22 novembre 2026

## Périmètre et contrat

État courant : 2804 QCM/fiches, 217 banques, 336 QCM de pharmacologie dans les quinze thèmes fournis. La demande V4 autorise une relecture scientifique des autres unités et la réparation documentée des pertes/appairages. Elle n’autorise pas à remplacer les clés officielles pour un désaccord scientifique non résolu. Les identités de tous les QCM préexistants sont conservées ; les ajouts ont des IDs libres. Aucun QCM antérieur à 2015 n’est ajouté ; le contenu ancien déjà présent dans la biomol n’est pas supprimé.

## Données et affichage

`index.html` contient CSS, interface et JavaScript. `const EXAMS=` est du JSON. Les banques portent `ue`, `courseId`, `kind`, `questions` et `storage`. Les thèmes UE4 sont `ue4.annales.theme.<themeId>`, `pharmaGrouped:true`.

`question`, `context`, `options[].text`, `images`, `stemImages`, `originalImages`, `options[].image` sont des énoncés. `explanations`, `generalExplanation`, `correctionImages`, `reviewNotes` et les réserves `warning` appartiennent à l’après-correction. Le rendu `reviewHtml(q)` est appelé seulement si `isCorrected(q)`. L’export respecte la même condition pour chaque QCM, dans les deux profils. `reviewWarningCovered` et `pharmaWarningCovered` évitent les réserves historiques en doublon.

Les notes ont `noteId`, `items`, `kind`, `text`, `refs`, éventuellement `sourceVerdict`/`courseVerdict`. Une référence de cours n’est pas une garantie pour tous les items d’un chapitre. `itemsReviewedCount` mesure la lecture, les champs `status`/`courseVerification` et `visualReview` précisent sa portée. Les fichiers locaux cités dans les notes sont dans `sources/revision_v4/` ; les pages sont en base 1.

## Identités et stockage

La pharmacologie utilise `sourceId` comme identité stable : le numéro local `id` peut changer lors d’un reclassement sans déplacer les réponses. `sourceNumber` et `printedSourceNumber` sont ceux du document. La progression UE4 est dans `qcm-pass-ls-ue4-progress-by-source-v1` et sa variante `_profil_2_v1`, via `bySource`. `PHARMA_PROGRESS_LINKS`, `legacyProgress` et `PHARMA_EXAM_ALIASES` maintiennent la migration. Ne jamais réimporter une réponse effacée volontairement : une entrée vide est une entrée existante.

Les années 2018–2019 et 2019–2020 gardent S1 dans leurs anciennes identités de stockage ; leurs couvertures ne précisent pas la session. `pharmaPrintedSession` corrige l’affichage et l’export sans modifier les identités.

Hors pharmacologie, `storage` correspond au profil 1 et `storage+'_profil_2_v1'` au profil 2. Ne renuméroter ni les questions ni les choix préexistants. Si une lettre répétée dans le document exige un nouveau choix, employer une lettre libre et `options[].sourceLabel` pour expliquer le repère original. Les choix peuvent dépasser A–E. Les identifiants composés relèvent de `tokenMode`.

## Clés et notation

Une clé vide est hors note, sauf `answerIsEmpty:true`. Dans ce dernier cas, `answer:''`, `allowNoAnswer:true` et le choix volontaire ∅ rendent possible une réponse tout-faux. Le contrôle `allowsNoAnswer(q)` propose désormais ∅ uniformément à tous les QCM ayant des options, indépendamment de leur clé, pour ne pas donner d’indice avant correction ; les anciens attributs `allowNoAnswer` restent conservés dans les données. Conserver `rawAnswer` pour les divergences de lettrage ou une clé ambiguë. `ignoredOptions` exclut les seuls items hors programme identifiés ; ne pas y placer tous les choix d’un QCM car cela lui donnerait artificiellement tous les points. Les QCM entièrement marqués HP dans une vieille source sont signalés dans les commentaires ; leur barème n’a pas été refondu sans demande.

Barème conservé : 10/5/2/0 points pour 0/1/2/3+ erreurs, zéro pour un blanc, conversion sur 20 et coefficients existants. La pharmacologie contient toujours 325 QCM évaluables et onze hors note. Les clés changées ailleurs sont exclusivement les réparations référencées dans `audit/revision_v4/reparations.json`. Une contradiction scientifique reste une note, pas une réécriture silencieuse de `answer`. Une question dont `answerPolarity` vaut `false` attend une affirmation inexacte : employer « À cocher / Ne pas cocher », sans présenter la lettre attendue comme un verdict scientifique Vrai.

## Contextes et figures

`sharedContexts` contient l’énoncé/figure avant le premier membre visible du groupe, même après recherche ou filtrage. Ne pas remettre cet énoncé dans le dernier item du QCM précédent. `references` et `referenceImages` servent aux annexes. Les titres des cartes sont les consignes ; nom de fichier et page sont des métadonnées discrètes.

Extraire les figures exactes des sujets ; distinguer les surcouches de lettres Word du bitmap embarqué. Un crop de corrigé contenant réponses ou commentaires ne doit pas devenir une image d’énoncé. Une figure déjà défectueuse dans le sujet est signalée, sans redessin supposé.

## Reproduction et audit

Le constructeur V4 repart de `baseline_index.html`/`baseline_exams.json` immuables puis applique les patches des lots et leurs annotations. Les scripts, données de départ et décisions sont sauvegardés sous `audit/revision_v4/production/`. Ces scripts documentent la production dans son espace de travail d’origine : avant de les relancer ailleurs, adapter les chemins racines, les chemins des assets et la résolution des PDF aux dossiers de l’archive. Les anciens scripts généraux peuvent rétablir des erreurs et ne doivent pas être relancés sans porter ces changements.

Ordre : `build_site.py`, `test_site.cjs` (sans `--draft`), `check_content.py`, `write_report.py`, conditionnement ZIP et manifeste SHA256. Les contrôles sont documentaires et exécutés dans un adaptateur DOM ; aucun résultat de mise en page réelle dans un navigateur n’est revendiqué. Le manifeste de l’archive couvre tous les fichiers sauf lui-même.

Les rapports antérieurs sont historiques, notamment `audit/historique_v3_2026-11-22/`. `CONTROLE_ANNALES.md` est le bilan courant.
