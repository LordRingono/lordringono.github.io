# Vérification indépendante de l’intégration V6

## Statut

**Feu vert final pour l’intégration examinée. Les trois défauts de comportement découverts ont été corrigés par l’agent principal et leurs correctifs vérifiés sur le site réellement assemblé. Aucun défaut bloquant d’intégration ne reste ouvert.**

Empreinte SHA256 de `output/site/index.html` contrôlé : `3b5438e47c8241431025e368f1a57628f390cfa6be394d057e415b8dd782f7c6`. Les empreintes des scripts, des approbations et des résultats sont consignées dans `verified_release.json`. Les trois contre-tests indépendants ont été réexécutés sur cette dernière version, après la clarification des libellés documentaires.

Cette passe concerne l’assemblage, les protections d’affichage, la préservation des données approuvées et la migration des deux profils. Elle complète les neuf binômes documentaires ; elle ne remplace pas leur comparaison individuelle des QCM avec les PDF et Word.

L’auditeur n’a modifié aucun des scripts d’intégration ni aucune donnée de matière. Tous ses scripts et résultats sont dans `work/site_v6/integration_verify/`. Aucun build de substitution n’a été lancé.

## Sources du contrôle

Lecture de `CONTRAT.md`, `AGENT_GUIDE.md`, `build_site.py`, `source_copies.js`, `progress_migration.js`, `check_runtime.cjs`, `check_integrity.py` et des fonctions correspondantes du template V5 dans `baseline_index.html`. Comparaison indépendante de `baseline_exams.json` avec les neuf snapshots des matières. La comparaison finale a utilisé exclusivement les chemins et empreintes des neuf approbations présentes dans `signoffs.json`.

### Constats structurels prouvés

Le premier passage `inspect_inputs.py` couvre 217 banques et 2 812 QCM, contre 2 806 dans la base V5. Il trouve six IDs nouveaux et treize séquences d’items modifiées. Les dix banques concernées et les dix-neuf QCM correspondants sont tous couverts par `V6_ITEM_REPAIRS`. Aucun ID antérieur, poids, clé de stockage ou métadonnée de banque n’a changé dans les snapshots examinés. Le rapprochement manuel des textes d’items confirme les déplacements de lettres décrits par cette table, dont le transfert des anciens choix F–J de `bio.cm8` Q13 vers le QCM restauré ID 17.

Le builder repart de la base V5, conserve les métadonnées de banques et remplace leurs listes de questions par les versions signées. Il vérifie les empreintes de `reviewed` et `crops`, l’unicité des IDs et la conservation des IDs antérieurs avant d’écrire la sortie. Les changements de métadonnées de source et la synchronisation des instantanés de notes sont explicites ; aucun changement de clé, option ou explication scientifique supplémentaire n’est prévu dans l’intégrateur.

Les douze copies sujet signalées comme annotées comprennent trois groupes partagés : `embryo.aut.s4` Q23–24, `embryo.aut.coeur` Q5–6 et `annales.ue2c.lipides.2020paces` Q5–6. Sept questions portent `imagesAfterCorrection`. Aucun champ additionnel de protection non pris en charge n’a été trouvé dans les options ou références des snapshots examinés.

## Défauts découverts et corrections

### INT-001 — Lien PDF direct restant accessible pour un sujet annoté

Le menu `histoSourceCopy()` et les images étaient protégés, mais le template conservait le lien `qsource` vers le PDF sur la page annotée pour les questions issues de compilation. Le lien `sourceReference()` du contexte partagé restait lui aussi actif. Exemples réels : lipides 2020 PACES Q3/Q5/Q6 et glucides 2020 PACES Q1. La présence d’un message de report dans le menu n’empêchait pas cet accès parallèle.

L’agent principal a conditionné le lien individuel à `subjectOriginalReady(q)` et le lien du contexte à `sharedOriginalReady(context)`. Il a étendu cette condition aux figures individuelles et aux `stemImages`. **Correctif confirmé sur la sortie : les douze sujets annotés n’exposent pas leurs liens avant validation ; les sources des trois groupes se déverrouillent après les validations requises.**

### INT-002 — Déverrouillage prématuré d’un schéma annoté partagé

La version initiale de `sharedStatement()` ne vérifiait que `isCorrected(q)` pour la première question rendue. Valider cette question suffisait à dévoiler le schéma commun aux autres questions du groupe, même si elles restaient en attente. Le résultat dépendait également de l’ordre et du filtrage de la liste visible.

Le nouveau `sharedOriginalReady()` consulte tous les QCM de `QUESTIONS` portant le même ID de contexte et exige leur validation. Le sujet original annoté de chaque question du groupe est soumis au même verrou. Les copies du corrigé individuel restent accessibles après la validation de cette question. **Correctif confirmé pour les trois groupes, les deux ordres de validation, le filtrage d’une seule question, l’ouverture après validation complète et le reverrouillage après retrait d’une validation.** Le profil classique est également testé avant et après correction globale.

### INT-003 — Migration persistée sans sauvegarde lorsque le quota est atteint

La migration initiale stockait immédiatement le résultat dans `fallbackSessions`, tentait la sauvegarde dans un `try`, puis avalait l’erreur. Si la création de la nouvelle clé de sauvegarde échouait alors que le remplacement de la clé existante restait possible, le prochain `save()` écrasait définitivement la progression V5. Le test initial l’a reproduit avec le choix BCD devenu CDE et `backupExists:false` : voir `initial_backup_failure_result.json`.

Le correctif conserve l’original dans `v6PendingBackups` et fait passer les écritures de `save()` par `persistV6Progress()`. Tant que la sauvegarde originale ne peut pas être créée et relue, aucune progression migrée ne remplace l’ancienne clé persistante. La session remappée reste utilisable en mémoire ; la sauvegarde est retentée ensuite, avec une indication visible dans l’interface lorsqu’elle reste bloquée.

La contre-vérification isolée est **PASS** : échec explicite de type quota et faux succès silencieux, deux profils distincts, répétition des tentatives sans écrasement, idempotence en mémoire, rétablissement du stockage, sauvegarde originale exacte et ensuite inchangée. **Le branchement réel de `save()`, `loadExam()` et `switchProfile()` est également PASS sur le site assemblé**, avec modifications de choix conservées en mémoire, indication visible de la panne, reprise de la sauvegarde et rechargement des deux profils.

### INT-004 — Faux échec de la suite principale sur l’ordre des lettres

La première exécution principale comparait une sélection synthétique `BDC`, injectée directement depuis la clé officielle, à la sélection normalisée `BCD` après rechargement. Les choix représentent le même ensemble d’items ; l’interface trie les lettres lors des véritables sélections. Il s’agissait d’un défaut de la préparation des données de test, sans corruption du site.

L’agent principal a normalisé les trois injections synthétiques de la suite comme le fait l’interface, puis a relancé l’ensemble du contrôle principal. **Résultat final PASS sur les 217 banques.** La clé approuvée `BDC` et le contenu du site n’ont pas été modifiés. Le premier résultat est conservé dans `initial_runtime_report.json` pour la traçabilité.

## Tests effectivement exécutés

| Test | Résultat et portée |
|---|---|
| `inspect_inputs.py` | PASS structurel : 217 banques, 2 812 QCM, 13 séquences d’items modifiées et 6 IDs nouveaux ; aucune réparation structurelle sans migration. |
| Reproduction initiale du quota | Défaut prouvé avant correction ; sortie conservée dans `initial_backup_failure_result.json`. |
| `test_backup_failure.cjs` après correction | Ancienne clé inchangée malgré le remappage en mémoire et deux tentatives de sauvegarde bloquées. |
| `test_backup_guard.cjs` | PASS pour deux modes de défaillance et les deux profils, puis reprise et immutabilité des sauvegardes originales. |
| `test_release.cjs` | PASS : trois groupes annotés, deux ordres de validation par groupe, filtres, reverrouillage, profil classique, douze sujets annotés et soixante scénarios de migration. |
| `test_release_storage.cjs` | PASS : vrais appels de chargement, sauvegarde et changement de profil sous panne puis reprise du stockage, deux profils indépendants, rechargement correct. |
| `compare_release.py` | PASS : neuf approbations, 217 banques, 2 812 QCM, 890 notes, 5 624 métadonnées sujet/correction, 5 158 regroupements de pages par document dont 67 copies multi-PDF, 6 762 associations document/page/rectangle et limites géométriques, 146 documents installés identiques aux originaux. |
| Contrôle de schéma des clés | PASS : aucune lettre attendue absente des options et aucune clé non vide simultanément marquée `answerIsEmpty` parmi les 2 812 QCM ; `answer_schema_result.json`. |
| `check_runtime.cjs`, exécuté par l’agent principal puis résultat examiné | PASS : 217 banques, 11 249 états de cartes, 2 771 clés, 6 846 chemins de fichiers, 434 profils persistés et 20 profils de migration. |
| `check_integrity.py`, exécuté par l’agent principal puis résultat examiné | PASS : 3 625 fichiers antérieurs inchangés, 9 522 liens locaux, 6 383 captures décodées, 30 comparaisons de pixels et 191 assets complémentaires. |
| Vérification syntaxique des scripts indépendants | PASS pour les deux scripts Node de contrôle final et les deux scripts Python. |

Les tests JavaScript exécutés utilisent **Node VM**. Ils ne vérifient pas les pixels de l’interface, le rendu responsive, le comportement natif du navigateur ou l’accessibilité dans un navigateur.

## Portée de la preuve sur la sortie

`test_release.cjs` a vérifié les trois groupes annotés et leurs liens en états initial, partiellement validé, complètement validé, filtré et reverrouillé. Il a contrôlé la migration de soixante anciennes sessions : dix banques, deux profils, trois formes d’historique (partiel, ancien format sans liste de validations, non validé). La liste des questions exigeant une nouvelle validation est dérivée indépendamment des différences de schéma et des IDs nouveaux entre V5 et V6. Les choix et validations des questions inchangées sont conservés. Le rechargement ne remigre pas une seconde fois les lettres.

`test_release_storage.cjs` a exécuté les vrais `loadExam()`, `save()` et `switchProfile()` du site construit, avec une panne du stockage puis son rétablissement, en vérifiant les deux clés de profil, les anciennes sauvegardes, les choix remappés et l’indication visible dans le DOM simulé.

`compare_release.py` a comparé les données réellement embarquées dans `index.html` avec `current_exams.json` et les neuf snapshots signés. Les champs sémantiques sont exactement conservés, y compris options, clés, explications, poids, ordre et texte des notes. Les changements autorisés se limitent aux métadonnées d’intégration des sources, aux instantanés des textes déjà associés aux notes et aux liens ajoutés à leurs références. Les 146 documents installés correspondent octet pour octet à leurs originaux d’entrée par SHA256.

Les métadonnées de capture de chaque sujet/corrigé ont été rapprochées du lot `crops` signé, y compris les indicateurs d’annotation, les notes, les rôles manquants et les sources V5 réutilisées. Les 6 762 références de captures correspondent exactement aux documents, pages et rectangles approuvés ; chaque rectangle est positif et contenu dans sa page. Les 6 383 fichiers de captures sont moins nombreux, car les captures identiques sont partagées.

La dernière relecture des rapports par l’agent principal a conduit à clarifier les libellés documentaires : `Annales_compilation.pdf` est affiché sous son nom réel et les descriptions de panneaux sont conservées dans `sourceLabel` plutôt que présentées comme des noms de fichier. Cette modification de métadonnées a été suivie d’un nouveau build et d’une nouvelle exécution des trois contre-tests. Les 5 158 regroupements de pages par document, dont 67 copies réunissant plusieurs PDF, ont été contrôlés : les pages et les noms de capture correspondent à leur propre document, sans mélange entre PDF. Aucun contenu approuvé ni cadrage n’a changé.

Les résultats des contrôles principaux `check_runtime.cjs` et `check_integrity.py` ont été examinés. Le premier vérifie le barème 10/5/2/0 sur les questions notées et la persistance des deux profils. Le second compare des pixels seulement sur un échantillon de trente captures explicitement recensé ; le décodage de toutes les captures ne constitue pas une relecture visuelle individuelle. Une seconde lecture indépendante du correctif de protection figure dans `secondary/REPORT.md` et `secondary/source_review.json`.

## Risques et limites résiduels

La preuve documentaire sur les annotations effectivement présentes et l’exactitude des cadrages relève des rapports des binômes. L’intégration peut vérifier que toutes les protections déclarées fonctionnent, mais ne peut pas inférer automatiquement qu’aucune image non signalée ne comporte d’annotation.

Le site est un support statique local : la protection testée concerne les chemins d’accès proposés dans l’interface d’entraînement. Elle ne constitue pas un mécanisme d’autorisation contre l’inspection volontaire des fichiers ou du code source.

Le feu vert porte sur l’intégration portant l’empreinte indiquée en tête et sur les contrôles décrits ici. Les limites documentaires propres aux neuf matières restent celles de leurs rapports approuvés ; elles ne sont pas effacées par la réussite des tests techniques.
