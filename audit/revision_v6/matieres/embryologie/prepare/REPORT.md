# Embryologie V6 — lot préparateur

## Périmètre et état du lot

Base V5 : **22 banques, 599 QCM, 3 387 items**. Le lot préparé conserve les 599 identifiants de QCM et comporte **3 389 items**, après restitution de deux propositions présentes dans les corrigés originaux mais absentes de l’import.

Les 22 PDF corrigés ont été appariés aux 599 QCM. Les sept sujets distincts couvrent 259 QCM. Les parties énoncé de documents mixtes apportent 19 autres sujets ; un sujet supplémentaire de la compilation générale est déjà intégré ici (ann.gamet ID13). Le lot contient donc **279 copies de sujet, 599 copies de correction et 917 panneaux de capture**. Quatre copies intitulées « sujet » sont réellement annotées dans le document original ; leur accès et les figures correspondantes sont réservés à l’après-correction.

Ce rapport est un état de préparation, antérieur à la dernière validation indépendante. Il ne présente pas une concordance textuelle automatique comme une preuve d’absence d’erreur scientifique. Le vérificateur `embryologie_verifie` relit séparément les sources, les détails ajoutés et les cadrages ; ses compléments et son verdict final sont à fusionner.

## Fichiers à intégrer

- `reviewed.json` : objets complets des 22 banques, même structure et mêmes identifiants V5.
- `audit.json` : 599 lignes, éléments de preuve pour les 3 389 items, formulations sources, verdicts ou clés littérales, détails, pages et statut de disponibilité.
- `crops.json` : 599 lignes ; coordonnées PDF originales, pages en base 1, provenance réelle par rôle.
- `source_manifest.json` : chemins des PDF originaux et empreintes SHA-256.
- `coverage_preparer.json` : compte de couverture et checkpoint de chacune des 22 banques.
- `changes.json` : journal des changements de champs.
- `missing.json` : liste **provisoire**, avant fusion des sujets de la compilation.
- `residual_flags.json` : différences d’extraction résolues (retours de ligne, lettres isolées, coquilles de la source), avec justification ; aucune différence résiduelle ne doit être assimilée à une nouvelle clé scientifique.

## Réparations étayées

### Deux propositions omises

1. **Autotest méiose, Q5** : le corrigé comporte deux propositions K différentes. La seconde, « En méiose 1 il y a brassage intrachromosomique. », est indiquée Vrai et était absente. Elle est rétablie avec l’identifiant stable nouveau **O**, le libellé `K bis (source)` et la clé **BCEFMNO**. Les identifiants préexistants restent inchangés. La répétition identique de J dans le PDF n’est pas ajoutée comme nouvelle question.
2. **Autotest fécondation, ID23 / Q24 imprimé** : la seconde proposition M, « correspond à la sous-unité alpha du dimère. », est indiquée « Faux Béta ». Elle est rétablie sous **N**, libellée `M bis (source)`. La clé ILM ne change pas.

### Énoncés et correspondances

- Aut.coeur Q4 G, col.s4 Q28 E, Q34 E et Q43 D : retrait des consignes des QCM suivants, conservées dans leurs blocs communs.
- Ann.gamet ID13 : le sujet original 2018–2019 de la compilation, p.1604, rétablit « en métaphase I » dans A ; les phrases de correction incorporées par erreur dans B et D sont retirées des propositions et restent dans les explications. La provenance du sujet est explicitement la compilation, celle du corrigé demeure le PDF thématique. Sa contradiction déjà signalée sur E n’est pas masquée.
- Aut.coeur Q9 N, ann.coeur IDs15 C et18 E, col.s4 Q48 C et54 A : réparation des mots déformés ou de la note RAS parasite avec preuve du corrigé et comparaison du sujet.
- Aut.coeur Q2 : conservation du F composite du sujet, qui correspond à f+g dans le corrigé ; G–P correspondent ensuite à h–q. Une note décrit la correspondance, sans décaler artificiellement toutes les clés.
- Col.s4 Q47 A : conservation de J24 imprimé dans le sujet. Une note expose la divergence avec la phrase J25 du corrigé, suivie de « Vrai c’est J24 ».
- Les schémas communs aut.s4 Q23/24 et col.s4 Q54/55, Q68/69 sont regroupés dans `sharedContexts`. Les groupes déjà présents sont conservés.

Au total, **14 propositions** sont nouvelles ou réparées et **328 détails de correction** diffèrent de la V5. Les détails restitués reprennent les verdicts, annotations colorées ou mots barrés du PDF ; un commentaire scientifique n’a pas été inventé pour remplir un vide.

### Réparations issues du contrôle croisé

- **Ann.s2 IDs12/13, p.4** : le sujet du schéma J13 n’a aucun numéro avant sa consigne. Cette mise en page avait fait absorber ses items dans le bloc de correction du QCM précédent. La frontière est maintenant explicite : ID12 conserve uniquement les détails A/B/E de l’encadré `3. CD` ; ID13 dispose de sa propre copie sujet complète, de son schéma et des cinq items, puis de sa clé `7. AB` et de ses explications C/D/E. Les ajouts erronés du brouillon ont été supprimés.
- **Ann.s1 ID12** : J3, J4 et le mot Faux rétablis après lecture de l’image originale p.4.
- **Ann.s3 ID13 E** : annotation rouge prolongée jusqu’à « par la chorde et la plaque préchordale par SHH », sur la ligne suivante du PDF p.3.

## Schémas d’origine déjà annotés

| QCM | Source | Protection préparée |
|---|---|---|
| Aut.s4 Q23 et Q24 | ENONCE p.7 ; « Là où se trouvent les IWP » | `subjectAfterCorrection:true` et `imagesAfterCorrection:true` sur le QCM et le contexte commun |
| Aut.coeur Q5 et Q6 | ENONCE p.2 ; noms anatomiques déjà écrits sur les vaisseaux | Même protection sur les copies et figures communes |

Les fichiers originaux ne sont pas altérés. Les anciens fichiers de figures sont conservés intacts et doivent être masqués avant correction par le renderer de l’agent principal. Aucun `originalImages` ou `stemImages` alternatif ne reste présent sur ces quatre QCM. Demander, si possible, les deux schémas vierges ou seulement numérotés en fin de livraison.

## Compléments du vérificateur à fusionner

Les fichiers `../verify/compilation_supplements.json` et `../verify/compilation_new_keys.json` contiennent les preuves indépendantes suivantes :

- **60 sujets** des annales gamétogenèse, fécondation, S1 et S2 retrouvés dans la compilation générale. Ils recoupent 20 sujets déjà couverts ici ; la fusion apporte donc 40 copies supplémentaires et conduit à **319 QCM couverts pour le sujet**, avec **280 QCM encore sans sujet propre** dans ce périmètre.
- **Huit clés jusque-là absentes**, provenant de la grille p.1232 et des détails des pages suivantes. Leur provenance doit rester explicite, y compris lorsque la rédaction du corrigé thématique diffère. Le cas ann.s3 ID26 est « RIEN » dans la grille et tous Faux dans le détail p.1238.
- Les catégories ann.fec IDs13/14 doivent être corrigées en **2020–2021** selon la session retrouvée.

Ces compléments ne sont pas entièrement incorporés dans ce lot préparateur afin de garder leur contrôle indépendant identifiable. Seul ann.gamet ID13 est déjà appliqué et dispose de sa capture p.1604. Ne pas appliquer ses mêmes réparations deux fois. Régénérer `missing.json` après la fusion avant de demander des documents à l’utilisateur.

## Conservation des clés et limites

Les désaccords internes aux corrigés déjà signalés conservent leurs notes et leurs références de cours. Les clés d’origine ne sont pas réécrites sur intuition. Les questions encore ambiguës ou sans verdict exploitable restent hors note selon les règles V5, sauf les clés manquantes que le vérificateur peut maintenant rétablir avec une source nouvelle explicite.

Les captures ont été préparées systématiquement avec les sources, pages, figures et groupes communs. Le préparateur a rendu et examiné les cas de structure sensibles et les réparations visuelles décrites ci-dessus ; la validation indépendante de l’ensemble des cadrages et détails relève du lot du vérificateur. La présence des 599 captures de correction signifie qu’un document original correspondant est accessible, pas que les 599 corrigés sont scientifiquement irréprochables.

## Reproduction du brouillon

Les scripts sont des outils de préparation, pas des fichiers à déployer. Après extraction et segmentation, l’ordre final est `fix_unnumbered_subject.py`, `review_builder.py`, `build_crops.py`, puis `finalize_review.py`. Ne pas relancer le builder seul après la dernière fusion : il écraserait les réparations manuelles finales et les compléments du vérificateur. Aucun fichier de `output/site` n’a été modifié par ce lot.
