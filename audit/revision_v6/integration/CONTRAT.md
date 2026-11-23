# Révision V6 — ensemble du site, binômes par matière

## Demande active

Appliquer à TOUT le site la vérification exhaustive faite en V5 pour les autotests d’histologie. Pour chaque matière : un agent préparateur et un agent distinct qui vérifie son travail depuis les documents. Utiliser tous les documents disponibles, y compris les premiers envois. Faire tout ce qui est possible ; lister les manques précisément et demander seulement à la fin les pièces restantes.

## Base immuable

- `work/site_v6/baseline_index.html` et `baseline_exams.json` : V5, 2 806 QCM/fiches, 217 banques.
- Site complet courant : `output/site/`.
- Documents déjà dans le site : `work/site_v6/documents_available.json`.
- Inventaire par UE : `work/site_v6/unit_inventory.json`.
- Les travaux V4 et V5 sont dans `output/site/audit/` ; ils servent de repères, pas de preuve suffisante pour annoncer une nouvelle relecture.

## Invariants

Conserver les IDs préexistants, les options et leur ordre sauf réparation documentée, les clés de stockage et les deux profils. Ne pas refondre l’apparence ni le classement par thèmes. Les corrigés restent la référence de notation ; un désaccord scientifique produit une note après correction, pas une clé réécrite sans preuve. Les réparations d’import prouvées peuvent rétablir les clés originales. Aucun ajout d’annale antérieure à 2015 ; ne pas supprimer les anciens contenus présents sans instruction.

## Vérification par question

Rapprocher consigne complète, contextes partagés, options (seulement leur énoncé), figures et toutes leurs lettres, verdicts V/F/Vrai/Faux/gras/couleur selon le document, grille de correction et détails explicatifs. Vérifier aussi les pages précédentes/suivantes. Examiner les divergences sans inventer une justification. Les items sans source exploitable restent identifiés comme tels ; ne pas annoncer leur vérification comme acquise.

## Copies originales

Pour chaque QCM et chaque rôle sujet/correction, préparer des rectangles exacts dans les PDF sources, toutes les pages nécessaires et figures incluses. Le sujet doit provenir d’une version réellement non corrigée (ou partie non corrigée d’un document mixte). Ne pas fabriquer une capture de sujet en supprimant secrètement les annotations. Si le sujet manque, le signaler ; le corrigé ne doit pas apparaître avant correction.

Les fichiers Word sont rendus en PDF sans modification avec le renderer documents. Tous les documents originaux sont conservés. Les données V5 utilisent `sourceCopies.subject` / `sourceCopies.correction` avec `file`, `pdf`, `original`, `converted`, `captures:[{src,page}]`, `note?`. Conserver les copies V5 déjà exactes. Les nouveaux menus seront intégrés par l’agent principal.

## Livrables par préparateur

Écrire seulement dans `work/site_v6/<matiere>/prepare/` :

- `reviewed.json` : `{banks:{bankId:{questions:[objets complets basés V5]}}}`.
- `audit.json` : une entrée par question et preuves par item (sujet, corrigé, clé littérale, détail, statut vérifiable/manquant, références/page/position).
- `crops.json` : `[{bank,id,subject:[{file:chemin PDF absolu,page:base1,rect:[x0,y0,x1,y1]}],correction:[...],subjectMissing?:raison,correctionMissing?:raison}]` ; peut inclure `note` par rôle, et un `sourceManifest` séparé pour PDF rendu/Word original.
- `missing.json` : documents ou éléments manquants, questions concernées, recherches réalisées.
- `REPORT.md` : réparations, limites et instructions.

Informer rapidement l’agent principal de sources manquantes. Ne modifier ni `output/site` ni les autres matières.

## Livrables par vérificateur

Écrire seulement dans `work/site_v6/<matiere>/verify/`. Lire indépendamment tous les QCM et les sources, puis contrôler chaque item de `prepare/reviewed.json`, les clés et justifications, les associations sujet/corrigé et les cadrages. Produire `coverage.json` par QCM/item, `issues.json` avec problèmes à réparer, `REPORT.md`. Signaler les limites honnêtement. Ne pas valider simplement parce que le script s’exécute ou que le précédent audit disait OK.

En cas de réparations ou compléments lors de la vérification, livrer les objets complets approuvés dans `verify/approved_reviewed.json` et `verify/approved_crops.json`. Le builder les utilisera en priorité. Si le lot préparateur est approuvé sans changement, `verify/approved.json` doit donner les empreintes SHA256 des deux fichiers examinés. Indiquer clairement les limites non résolues dans le rapport.

## Fin de travail

## Sources complémentaires récupérées pendant la V6

- `work/site_v6/materialized/embryo_original/` : 29 PDF de l’archive initiale (22 corrigés, 7 sujets distincts).
- `work/site_v6/materialized/embryo_individual/` : sujets séparés S3, S4 et cœur récupérés dans les messages.
- `work/site_v6/materialized/biomol_original/` : 46 PDF de l’archive Biomol UE2 initiale.
- `work/site_v6/materialized/ssh_individual/` : les quatre sujets SSH.
- `work/site_v6/materialized/biocell_individual/` : les neuf sujets PDF des autotests de biologie cellulaire.
- `work/histo_v5/old_source/` : les 62 documents originaux de la toute première Archive.zip (histo, biocell, annales et autotests).
- `work/site_v6/render/biocell_manifest.json` : rendus PDF des 18 Word biocell originaux (génération en cours au lancement).

La compilation générale `output/site/sources/Annales_compilation.pdf` contient aussi les sujets et corrigés UE5 des pages 989–1660 (sujet UE5 S1 2025–2026 dès 989, et non seulement après 1040). Les binômes UE5 doivent la confronter aux annales thématiques : une correspondance doit être prouvée par l’ensemble des items et la session, pas par une seule phrase similaire. Les sujets propres de cette compilation peuvent compléter les copies manquantes. Ne pas confondre son corrigé avec celui de la série thématique si les deux éditions divergent.

Si un document intitulé ENONCE contient lui-même une annotation donnant la réponse, ne pas altérer la capture. Mettre `subjectAfterCorrection:true` et `subjectNote` dans la ligne de crops.json. L’interface rendra alors cette copie accessible seulement après validation, avec une explication discrète auparavant.

Les remarques scientifiques doivent citer précisément un document de cours fourni ou une source primaire pertinente consultée. Une intuition seule ne devient pas une correction affirmée ; garder la clé du tutorat et proposer de vérifier le point précis dans la ronéo. Ne pas modifier les commentaires scientifiques déjà sourcés sans preuve contraire.

## Fin de travail

L’agent principal réconcilie les binômes, intègre les copies, teste la notation et les profils, conditionne le ZIP complet et fournit un rapport plus la liste précise des pièces à demander. La V5 demeure récupérable.
