# Contre-relecture ciblée des verrous de sources V6

## Conclusion

**Aucun défaut résiduel concret trouvé dans le correctif actuel et ses données approuvées.** Cette conclusion porte sur la lecture du code et l’inspection structurelle des snapshots ; elle reste distincte des tests du site assemblé exécutés par le vérificateur d’intégration.

## Preuves contrôlées

- `source_copies.js` : `sharedOriginalReady(context)` recherche les membres dans `QUESTIONS`, donc dans la banque entière, et exige `every(isCorrected)`. Son résultat ne dépend pas de la liste visible ni de l’ordre de rendu. Une validation retirée est immédiatement prise en compte au rendu suivant ; aucun résultat n’est mis en cache.
- `subjectOriginalReady(q)` exige la validation de la question puis celle des groupes annotés auxquels elle appartient. Les figures et les copies sujet annotées ont donc un verrou cohérent.
- `histoSourceCopy(q, 'correction')` retourne immédiatement une chaîne vide tant que la question n’est pas validée. Les données actuelles ne portent aucun `correctionAfterCorrection` ni `sourceCopies.correction.afterCorrection` : le verrou collectif ne masque donc pas par erreur un corrigé individuel déjà autorisé.
- `build_site.py` remplace les six ancres critiques du template V5 — images, stemImages, initialisation de `sharedStatement`, images du contexte, lien PDF du contexte, lien PDF individuel. Chacune est présente exactement une fois dans le template lu ; aucun remplacement critique n’est silencieusement absent dans cette base.
- L’appel du contexte à `sourceReference()` reçoit une URL vide quand le groupe est verrouillé. Le lien individuel de `qsource` exige `subjectOriginalReady(q)`. Le nom documentaire et la pagination restent de simples textes dans cet état.
- Les anciens `originalImages` ne sont pas réaffichés lorsqu’une métadonnée `sourceCopies.subject` existe ; le nouveau menu est alors le chemin d’accès prévu.

## Données réelles examinées

Les douze marqueurs de rôle trouvés concernent uniquement des sujets annotés. Les trois groupes protégés sont :

| Banque | Questions | Contexte |
|---|---|---|
| `embryo.aut.s4` | 23, 24 | `v6-shared-embryo.aut.s4-23` |
| `embryo.aut.coeur` | 5, 6 | `v4-shared-embryo.aut.coeur-5` |
| `annales.ue2c.lipides.2020paces` | 5, 6 | `ue2c-2020paces-common-21-22` |

Chacun des six membres possède à la fois `context.imagesAfterCorrection:true` et `subjectAfterCorrection:true`. Les deux membres de chaque groupe renvoient au même asset annoté. Aucun de ces six objets ne possède de `references`, `referenceImages` ou `options[].image` susceptible de proposer un accès graphique parallèle non protégé.

## Revue des tests principaux

`check_runtime.cjs` contrôle désormais séparément les menus sujet et correction, ainsi que les états initial, partiel et complet du contexte partagé. Le vérificateur d’intégration a prévu des tests indépendants supplémentaires pour les deux ordres de validation, les listes filtrées, le reverrouillage et le profil classique. Ces tests n’ont pas été dupliqués dans cette passe.

## Limites

Aucun build ni test navigateur n’a été exécuté dans cette contre-relecture. Aucun script root ni snapshot matière n’a été modifié. La présence ou l’absence sémantique d’annotations dans les images non signalées relève des binômes documentaires.

Les protections évaluées concernent les menus, images et liens de l’interface d’entraînement. Le site reste statique : un utilisateur inspectant volontairement les fichiers locaux ou le code embarqué peut consulter les corrigés. Cette propriété n’est pas une fuite par les contrôles d’affichage examinés.
