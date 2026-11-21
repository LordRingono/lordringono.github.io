# Relecture croisée des contextes UE2 — version révisée

**Conclusion : les six groupes ciblés sont complets et correctement séparés de leurs propositions dans la version contrôlée.** Les quatorze QCM comportent leurs soixante-dix items conformes au sujet. La contamination trouvée en bord supérieur de l'ancienne capture commune 2020 Q25–26 a été éliminée dans une nouvelle image ; le E du Q24 est également entier dans son nouvel extrait original. Aucun changement aux banques n'a été effectué par le relecteur.

Relecteur indépendant : agent UE3. Date : 21 novembre 2026.

## Version et périmètre

Source : `upload/Sujets + corrections compilés(1).pdf`, pages PDF 243, 244, 304, 305, 306, 450 et 455.

Banque contrôlée : `work/agents/ue2/exams.json` après la migration des contextes vers `sharedContexts`.

SHA-256 du JSON au contrôle : `c5da216ca3e7f0f9e5ad7c073c27c8dca9937fbed38998db120d0a30a45c4e12`.

Les pages ont été lues en texte et sous forme de rendus intégraux. Les six anciennes captures communes, les cinq nouvelles captures communes, les trois nouveaux extraits des questions donneuses, le nouvel original du Q24 et les deux items D en image ont été inspectés individuellement. Les 70 propositions ont été comparées aux pages du sujet. Les identifiants, numéros, clés, poids et objets d'options des quatorze questions ont été comparés au JSON antérieur : aucun changement.

## Résultats par groupe

| Annale et QCM canoniques | Source | Vérification de la version révisée | Résultat |
| --- | --- | --- | --- |
| 2020–2021 S1, Q25–26 | p304 | La consigne raster est fidèlement transcrite dans le texte commun. Le nouveau diagramme montre les six acides gras ①–⑥, 18:2 → 18:3 → 20:3 → 20:4 → 22:4 → 22:5, avec E1–E5. Le E du Q24 est absent du bloc. L'ancien petit titre Q25 qui accompagnait Q26 est retiré. | Conforme |
| 2020–2021 S1, Q27–28 | p305 | Le texte commun conserve huile d'olive, trioléine, triacylglycérol homogène et C18:1 cis Δ9. Il est identique dans les deux QCM. Le nouvel original Q27 commence à son propre titre, sans fragment de la ligne précédente. L'item D du Q28 est entier dans sa capture et n'emporte aucun autre item. | Conforme |
| 2020–2021 S1, Q33–34 | p306 | La consigne commune et les quatre diholosides sont restitués. Le nouveau recadrage conserve tous les atomes et les numéros ①–④, sans item A–E. L'ancien titre Q33 ajouté devant Q34 est retiré. | Conforme |
| 2021–2022 S1, Q31–33 | p243–244 | Le bloc partagé contient la phrase sur le polyoside végétal présent dans l'alimentation humaine et le schéma provenant de la page précédente. La capture descend jusqu'à819,5 et conserve l'extrémité basse, qui dépasse la hauteur du pied de page. Le motif répété, les légendes et les hydroxyles terminaux sont visibles. Le numéro de page et le titre local doublonné de Q33 sont retirés. | Conforme |
| 2018–2019, Q17–19 | p450 | Les trois molécules d'acides gras et la phrase introductive sont dans le bloc partagé. Le nouveau dessin n'inclut aucun item. L'extrait original du donneur Q17 se limite à ses propositions A–E. Les Q18 et Q19 héritent du même contexte et de ses trois molécules. | Conforme |
| 2018–2019, Q37–38 | p455 | La voie complète est conservée : glucose, glucose-6-phosphate, fructose-6-phosphate, composés A et B, pyruvate, alanine, lactate et acétyl-CoA, avec les réactions1–5. La voie suivante du Q39 canonique reste séparée. Le décalage source est maintenu : Q37 imprimé38, Q38 imprimé39. L'item D de Q38 est entier et isolé dans sa capture. | Conforme |

## Anomalie trouvée puis résolue

L'ancienne image `annales_ue2_304_baba63df24.webp` contenait sur son bord supérieur la proposition E du Q24 : « L'ATP est un activateur allostérique de la phosphofructokinase. » Elle a été signalée à l'auteur UE2 et au responsable. Le nouveau fichier `annales_ue2_v2_304_2f32a0ba24a2.webp`, limité au diagramme, ne contient plus cette proposition. Le texte commun a été transcrit séparément sans perte.

L'auteur a également constaté que l'ancien original du Q24 s'arrêtait au milieu de ce E. Le nouveau fichier `annales_ue2_v2_304_97680cb21ae3.webp` a été inspecté : E est entier, et aucun fragment de l'énoncé partagé suivant n'y est ajouté.

## Contrôles de structure

Les quatorze questions ont chacune un bloc commun. Les six identifiants de contexte sont stables et les objets sont strictement identiques chez tous les membres du groupe. Les listes `questionNumbers` couvrent exactement les membres attendus ; les `questionIds` correspondent aux identifiants locaux. Aucun de ces contextes ne subsiste en doublon dans `stemImages`.

Les cinq nouvelles images communes sont présentes, avec une provenance `subject` et la bonne page dans le manifeste. Les six textes communs ont été comparés à leurs consignes sources. Les groupes graphiques ne comportent aucune proposition A–E ni correction. Les 68 items textuels et les deux items en image sont inchangés par la migration.

## Limites de ce visa

Cette relecture porte sur la fidélité des énoncés, les limites des extraits et l'affectation des contextes aux QCM. Elle ne remplace pas la vérification finale du rendu du site et du filtrage, effectuée par le responsable d'intégration. Elle n'introduit aucune correction scientifique : les imperfections déjà imprimées dans les sujets sont conservées, notamment les notations `α1à β2`, `β2à1` et les caractères parasites présents dans deux propositions de 2020. Aucun manque restant n'a été relevé dans ce périmètre.

## Complément de visa — version finale gelée

**Résultat : PASS pour les deux groupes supplémentaires et les 42 recadrages d'items.** Ce complément a été effectué après le premier visa, sur la banque définitive comportant 15 contextes communs pour35 questions. Aucune banque ni image n'a été modifiée par le relecteur.

SHA-256 du JSON final contrôlé : `ceb82bfa67d21f7135460aa5ff6262e20d177030f83643e8ad919d64d105c8b5`.

### Deux groupes ajoutés

Les pages sources13,14 et53 ont été lues en texte et en rendu intégral. Les cinq consignes individuelles et les25 propositions ont été confrontées au JSON ; les deux nouvelles images communes ont été inspectées.

| Groupe | Constat indépendant | Résultat |
| --- | --- | --- |
| 2025–2026 S1, Q32–34, p13–14 | Le même lipide avec les composés A, B et C est reproduit trois fois dans le PDF. Les trois occurrences ont indépendamment donné le même digest d'image PDF `98aa4d13ed963e29c80656420a4f1c53`. Le nouveau dessin conserve les deux oses, la liaison et la chaîne du composé C, ainsi que les lettres A/B/C. Le libellé neutre du bloc partagé n'introduit aucune donnée scientifique. Les consignes locales sur A/B, sur C et sur les liaisons restent distinctes et fidèles. | Conforme |
| 2024–2025 S1, Q28–29, p53 | Les deux occurrences de la filiation ont été comparées visuellement : même succession 18:2 → 18:3 → 20:3 → 20:4 → 22:4 → 22:5. La donnée C18:2(9,12) est conservée dans le texte partagé ; l'invitation à choisir les réponses reste dans chaque QCM. Aucun A–E ni correction n'est inclus dans le diagramme. | Conforme |

Les objets partagés de ces deux groupes sont identiques chez tous leurs membres, les `questionNumbers` et `questionIds` correspondent exactement aux cinq QCM, et aucune ancienne image commune ne subsiste dans leurs `stemImages`.

### Quarante-deux captures d'items aux interlignes serrés

Les deux planches `v2_option_boundaries_after_1.png` et `v2_option_boundaries_after_2.png` ont été relues intégralement : les42 propositions y restent complètes et isolées. Les débuts de ligne, fins de phrase, exposants, indices, signes, unités et lignes de continuation visibles ne sont pas rognés. Aucun début de proposition voisine, consigne suivante ou corrigé n'a été relevé.

La planche `v2_option_boundaries_before_after.png` a également été vérifiée. Dans les quatre exemples, les traces de la ligne précédente ont disparu et le contenu de l'item est préservé. Le nouveau D du Q28 de2020, qui remplace la capture citée au premier visa, conserve notamment les deux lignes et l'indice2 de I₂.

Les identités d'options et textes mentionnés dans le premier visa restent valables ; seules les références d'images concernées par cette dernière correction de limites ont changé. Les deux ajouts portent le périmètre de relecture des contextes à **8 groupes,19 QCM et95 propositions**. Aucun manque restant n'a été constaté dans ce complément.
