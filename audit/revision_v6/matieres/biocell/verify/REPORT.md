# BIOLOGIE CELLULAIRE — vérification indépendante V6

## Décision

**FEU VERT FINAL pour intégrer `approved_reviewed.json` et `approved_crops.json`, avec les limites documentaires explicites ci-dessous.** Les deux fichiers sont complets : ils remplacent intégralement leurs homologues de préparation pour les 18 banques de biologie cellulaire. Aucune clé supplémentaire n’a été modifiée par le vérificateur. Les 226 QCM notés et les 4 QCM hors note de la préparation sont confirmés.

## Périmètre réellement contrôlé

| Contrôle | Résultat |
|---|---:|
| Banques | 18 |
| QCM confrontés aux sujets et corrigés | 230 |
| Propositions confrontées | 1 137 |
| Identifiants V5 conservés, avec coefficients inchangés | 224 |
| Questions omises restaurées dans les séries existantes | 6 |
| QCM notés / hors note | 226 / 4 |
| QCM notés dont tous les items sont faux | 4 |
| Copies de sujet propres / annotées différées / absentes | 229 / 1 / 0 |
| QCM disposant d’une copie du corrigé | 230 |
| Sujets propres retrouvés dans la compilation, rapprochés indépendamment | 48 |
| Verdicts d’errata graphiques relus visuellement | 13 sur 12 QCM |
| Figures interactives uniques relues visuellement | 73 |
| Emplois de ces figures après vérification | 93 |
| Panneaux de sujet / corrigé | 335 / 281 |
| Rectangles uniques | 590 |
| Word originaux confrontés aux rendus | 18 |
| PDF de sujet supplémentaires confrontés aux rendus Word | 9 |
| Notes finales / identifiants de notes historiques conservés | 87 / 68 |

La lecture documentaire porte sur chaque consigne, proposition, clé, détail et contexte. Les textes ont été réextraits directement des PDF, depuis leurs rectangles et pages, sans réutiliser les transcriptions du rapport préparatoire. Un contrôle distinct, conservant les signes `+`, `−`, `<` et `>`, n’a trouvé aucune nouvelle divergence de signe. La vérification des blocs complets de commentaire a confronté 1 067 items par extraction structurée ; les 70 exceptions de mise en page, scans, lettrage ou fusion ont été traitées manuellement.

La lecture visuelle comprend les trois pages de sujet CM2 entièrement scannées et les sept premières pages de son corrigé, les 12 ensembles d’errata, les 73 figures uniques, les 48 sujets de compilation, les cas de divergence et les six cadrages retouchés. Les autres panneaux ont reçu un contrôle documentaire et géométrique. **Ce rapport ne prétend pas que chacun des 616 panneaux a été affiché individuellement.** Les feuilles de contrôle sont dans `visual/`, leurs manifestes et extractions dans les fichiers JSON de ce répertoire.

## Réparations indépendantes

1. **Annales CM2, ID14 E : fin de commentaire rétablie.** Le texte s’arrêtait à « n’est pas » ; la page 14 du corrigé poursuit « présente dans la matrice. ». La comparaison par simple inclusion n’aurait pas détecté cette omission.
2. **Annales CM4, ID4 A : conservation des phrases non barrées.** L’erratum remplace FAUX par VRAI et barre la conclusion « type 2 », mais laisse deux phrases explicatives. Elles sont rétablies en distinguant explicitement le texte non barré de l’ancien verdict et de l’ancienne conclusion.
3. **Détails secondaires rétablis.** Le commentaire A du Q48/annales CM5 provenant de la compilation et le commentaire E du Q43/annales CM8 sont présents, avec indication de leur provenance. Le Q48 reste hors note.
4. **Trois remarques générales de correction rétablies.** Elles concernent annales CM10 ID3 (lecture de l’expérience annexine/IP), annales CM10 ID9 (rappel annexine/IP) et annales CM2 ID5 (remarque finale du corrigé scanné). Les formulations officielles sont conservées.
5. **Contexte annales CM2 ID3 : `Noe` corrigé en `Noc`.** La condition est ainsi imprimée dans le sujet et sur le Western blot.
6. **Note historique CM6 ID7 réconciliée.** Le commentaire sur le mouvement externe → interne appartient à E du sujet, D du corrigé, portant sur les flippases. L’ancienne note l’attribuait aux floppases. La ronéo CM6 p. 8 a été relue ; la note indique désormais que ce décalage est résolu et que l’absence de B dans le corrigé reste la véritable limite.
7. **Note CM8 ID10 remise au bon lettrage.** Après restauration des huit items, la prose de la note renvoyait encore à E et A au lieu de F et B. Elle distingue désormais le lapsus de A, la formulation de B et la cascade FAS de F. Les pages 5–7 de la ronéo CM8 ont été relues ; la clé BDEF reste inchangée.
8. **Note historique annales CM5 ID16 préservée.** La préparation avait supprimé `review-v4-ue5-visual-016`. Elle est rétablie avec son identifiant, en expliquant que la figure 6 annoncée a été retrouvée p. 11 et que la limite antérieure est résolue. Les 68 identifiants de notes de la base V5 sont donc tous présents.
9. **Expérience précédente jointe à deux QCM autonomes.** La figure 1 et son protocole sont joints à annales CM2 ID5 et annales CM10 ID3, dont le raisonnement exploite les résultats précédents. Cela fait passer les emplois d’images de 91 à 93, avec toujours 73 figures uniques.
10. **Cinq limites de panneau ajustées.** Les fragments voisins sont exclus des sujets CM5 ID17, CM6 ID1/2/10 et annales CM7 ID6. Les premières et dernières lignes ont été revérifiées après rendu. Le panneau de figure annales CM5 ID8 commence avant la légende Figure 7, excluant le `e` isolé de « Hors Programme ».
11. **Édition annales CM5 ID5 documentée.** La rubrique thématique imprime session 2, tandis que la question 42 complète de la compilation appartient à la session 1 2023–2024. La session 1 déjà affichée est conservée et cette divergence est expliquée dans la note de copie.
12. **Anciens chemins graphiques de secours retirés.** Les 69 champs `originalImages` et les 3 champs `correctionImage`, remplacés par les copies complètes issues des rectangles approuvés, ne restent plus comme chemins susceptibles de réafficher un ancien extrait. Les anciens chemins et leurs remplacements sont consignés dans `retired_legacy_graphics.json`. Les figures interactives actives sont toutes reliées à un rectangle approuvé.

Les 22 modifications de champs ou de cadrage sont détaillées dans `issues.json`. Les changements de nettoyage des anciens champs graphiques y sont consignés séparément.

## Confirmations sensibles de la préparation

Les six restaurations sont bien présentes dans les documents : CM7 IDs12/13/14, CM8 ID17, annales CM4 ID9 et annales CM9 ID10. Aucune nouvelle série ni annale antérieure à 2015 n’est ajoutée.

Les 13 substitutions graphiques comportent un verdict final explicite. La simple rature de « VRAI » à annales CM4 ID7 A ne produit aucun changement arbitraire de clé ; la correction de détail « 15 à 30 AA » est conservée. Les contradictions sans erratum, notamment annales CM6 ID7 A et annales CM7 ID10 B, gardent leur clé imprimée avec une note.

Les remappages F–J du sujet vers A–E du corrigé sont confirmés pour annales CM7 ID12 et annales CM9 ID10. Les champs de clé utilisent les lettres du sujet. Les questions entièrement fausses gardent `answer:""`, `answerIsEmpty:true` et `allowNoAnswer:true` : CM4 ID10, CM7 ID2 et ID8, annales CM6 ID24.

Le XML Word du CM3 contient `srcRect l="40501"` : le document original montre C et D seulement. Celui du CM8 contient `l="16694" t="24751" r="60826" b="48275"` ; le rendu respecte ces quatre limites. Tous les segments textuels significatifs des 18 Word sont retrouvés dans leurs PDF de travail. Les neuf PDF supplémentaires ont le même contenu normalisé que les rendus de sujet.

Les coefficients de toutes les questions V5 sont inchangés, notamment annales CM8 IDs6/7 : coefficient interactif 1 malgré « 1,5 point » imprimé. Profils, clés de stockage et contenu des autres matières n’ont pas été modifiés par ce travail.

## Limites à conserver et documents à demander à la fin

| Question / document | Limite confirmée | Comportement approuvé |
|---|---|---|
| Autotest CM6 ID7 | B du sujet absent du corrigé ; quatre lignes corrigées pour cinq items | Hors note ; demander une version harmonisée ou un verdict officiel |
| Autotest CM10 ID1 | Deux assertions fusionnées en A du sujet ; cinq lignes dans le corrigé | Hors note ; correspondances conservées et divergence expliquée |
| Annales CM5 ID1, Q48 | Grille BCDE dans la compilation, D FAUX explicite dans l’édition thématique ; autres ratures non légendées | Hors note ; demander la clé finale officielle |
| Annales CM5 ID2, Q49 | Grille ABCDE dans la compilation, C FAUX explicite dans l’édition thématique ; autres ratures non légendées | Hors note ; demander la clé finale officielle |
| Annales CM6 ID25, 2017–2018 Q42 | Seul sujet disponible annoté | Texte interactif propre et clé ACD conservés ; copie originale seulement après validation ; demander le sujet non annoté |
| Ronéo CM10 mort/sénescence 2026 | Cours spécifique absent pour arbitrer cytokines pro-inflammatoires et formulation sur p16/cycline D | Clés officielles et réserves existantes conservées ; demander le cours complet |

Les images incorporées aux originaux comportent parfois un défaut natif : première ligne de légende tronquée, fragment de titre ou bord de petit graphique. Le rapprochement avec les pages complètes confirme que ces défauts ne viennent pas des rectangles de préparation. Ils sont explicités dans `issues.json` ; aucun pixel n’a été reconstruit ou effacé pour simuler un meilleur original.

## Intégration

Utiliser les fichiers complets approuvés et les hashes de `approved.json`. Le builder doit créer les WebP aux identifiants dérivés des rectangles approuvés ; aucun `asset_manifest.json` supplémentaire n’est nécessaire. Garder les corrigés, remarques et la copie annotée d’annales CM6 ID25 derrière la validation. L’approbation documentaire est terminée ; le contrôle de l’interface intégrée revient à l’agent principal.
