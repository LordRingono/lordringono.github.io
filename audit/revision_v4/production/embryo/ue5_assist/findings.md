# Révision S4 et cœur — complément UE5

## Périmètre réellement relu

183 questions, 1019 propositions déjà importées et cinq propositions source rétablies : 1024 propositions relues. Les 35 autotests S4, 41 annales S4, 74 colles S4, 9 autotests cœur et 24 annales cœur ont été lus intégralement, avec leurs explications.

Les 44 pages physiques de la ronéo S4 ont été lues. Les passages cités ont été comparés à la version « Ronéo CG corrigées S4 » : même texte normalisé aux pages utilisées. Les pages 48–50 de la ronéo S3 ont été lues pour IWP/cardiogène. Aucune ronéo cœur/vaisseaux distincte n’a été trouvée dans les documents récupérés ; cette limite reste portée dans la couverture.

Les 12 images uniques de ce lot ont été inspectées visuellement, couvrant 19 questions une fois les quatre associations partagées rétablies. Deux questions cœur restent sans correspondance numérique vérifiable : la figure originale elle-même n’a pas les numéros 1–6 annoncés.

## Réparations d’import prouvées

Aucune question entière manquante n’a été trouvée dans ces cinq banques après confrontation des titres et numéros sources. Les groupes Q23/24, Q54/55 et les Q74/73 dans l’ordre inversé sont déjà présents ; les anciens IDs restent inchangés.

- Autotest S4 Q9 : J fusionné dans I ; Q11 : B fusionné dans A ; Q23 : D fusionné dans C. Options séparées et clés explicites restaurées.
- Autotest S4 Q13 : deuxième H perdu, restitué sous M ; Q14 : deuxième C perdu, restitué sous E. `sourceLabel` garde le double libellé du PDF. Aucun ancien ID renommé ; aucun nouveau tokenMode.
- Autotest S4 Q29E : retrait de la légende de figure « Là où se trouvent les IWP » collée à l’item par l’extraction. Le texte propre et la clé restent ceux du sujet.
- Autotest cœur Q2 : 16 options dans le sujet, 17 lignes dans le corrigé parce que le sujet réunit deux phrases sous F. Les deux sont fausses. Réappariement par texte des explications, clé source ACDJMNO, sans découper F ni déplacer les IDs.
- Colle S4 Q6 et Q72, annale cœur Q4 : clés complètes récupérées en conservant les HP individuels existants. Colle S4 Q69 : cinq Faux explicites, donc réponse vide connue (`AUCUNE`, `answerIsEmpty`, `allowNoAnswer`), et non absence de corrigé.
- Figures partagées réattachées aux colles S4 Q30/Q36/Q45 et à l’autotest cœur Q6. Images sources existantes conservées.

Les lettres sautées dans les PDF (par exemple D de l’autotest S4 Q9, F de Q12 ou plusieurs items retirés des colles comme annoncé dans leur préambule) ne sont pas inventées. Les HP entiers ann.s4 Q7/Q16/Q24 sont uniquement annotés, selon décision root ; aucune exclusion de notation ajoutée.

## Résultats et limites

49 notes sur 44 questions : 6 roneo_conflict, 17 possible_error, 17 source_conflict, 6 outdated_reference, 3 missing_reference.

Les contradictions principales concernent : origine des muscles faciaux dans une justification ; splanchnopleure/somatopleure de la figure Q44 ; tube neural définitif confondu avec neurectoblaste ; disparition complète du cœlome externe ; définition du péricarde ; zone cardiogène classée différemment par la colle et la ronéo ; clés globales en conflit avec leurs propres verdicts détaillés aux annales S4 Q6/Q8/Q11/Q17.

Les chronologies de ligne primitive et d’hématopoïèse comportent des désaccords entre corrigés. Ils sont conservés comme conflits de sources, sans imposer de nouvelle réponse. Les généralisations sur hémoglobines, nucléation des hématies, stomodéum et types de spina bifida restent signalées avec leur niveau de preuve ; les réserves non démontrées commencent par « À vérifier dans la ronéo ».

Les colles S4 Q13E et Q16E n’ont pas de verdict dans le corrigé (« date non précisée ») ; Q70E manque du corrigé. Ces trois clés complètes restent indéterminées. Une réponse déduite du cours n’est pas une réponse de la source.

La datation de 25 paires de somites à J28 et d’environ 30 à la fin du premier mois n’a pas été faussement signalée : la ronéo distingue explicitement J28 et J30. L’absence de migration du dermatome ou l’intégralité des items comprenant plusieurs clauses n’a pas été validée du seul fait qu’une explication terminologique était défectueuse. L’item « hématies fœtales nucléées contiennent… » (ann.cœur Q3D) n’a pas été assimilé à « toutes les hématies fœtales sont nucléées ».

## Couverture

| Statut | Questions |
|---|---:|
| reviewed_with_course | 140 |
| reviewed_without_course | 38 |
| needs_source | 5 |

`coverage.json` contient les IDs des propositions réellement relues, les thèmes et pages consultés, les images vues, les liens vers notes et les limites par question. « Aucun problème supplémentaire identifié » ne constitue pas une certification scientifique. Aucune clé n’a été modifiée pour un désaccord avec le cours.

## Index des notes

| Banque | Q | Items | Nature | Note |
|---|---:|---|---|---|
| embryo.aut.s4 | 6 | G | roneo_conflict | embryo-ue5-assist-001 |
| embryo.aut.s4 | 7 | C | possible_error | embryo-ue5-assist-002 |
| embryo.aut.s4 | 13 | H, M | source_conflict | embryo-ue5-assist-003 |
| embryo.aut.s4 | 14 | C, E | source_conflict | embryo-ue5-assist-004 |
| embryo.aut.s4 | 21 | A | possible_error | embryo-ue5-assist-005 |
| embryo.aut.s4 | 29 | E | roneo_conflict | embryo-ue5-assist-006 |
| embryo.aut.s4 | 30 | C | outdated_reference | embryo-ue5-assist-007 |
| embryo.aut.s4 | 30 | D | source_conflict | embryo-ue5-assist-008 |
| embryo.aut.s4 | 30 | E | outdated_reference | embryo-ue5-assist-009 |
| embryo.aut.s4 | 33 | C | outdated_reference | embryo-ue5-assist-010 |
| embryo.aut.s4 | 35 | B | possible_error | embryo-ue5-assist-011 |
| embryo.ann.s4 | 4 | D | possible_error | embryo-ue5-assist-012 |
| embryo.ann.s4 | 6 | D | source_conflict | embryo-ue5-assist-013 |
| embryo.ann.s4 | 8 | A | source_conflict | embryo-ue5-assist-014 |
| embryo.ann.s4 | 11 | D | source_conflict | embryo-ue5-assist-015 |
| embryo.ann.s4 | 17 | B | source_conflict | embryo-ue5-assist-016 |
| embryo.ann.s4 | 7 | A, B, C, D, E | outdated_reference | embryo-ue5-assist-017 |
| embryo.ann.s4 | 16 | A, B, C, D, E | outdated_reference | embryo-ue5-assist-018 |
| embryo.ann.s4 | 24 | A, B, C, D, E | outdated_reference | embryo-ue5-assist-019 |
| embryo.ann.s4 | 27 | D | possible_error | embryo-ue5-assist-020 |
| embryo.ann.s4 | 38 | B | possible_error | embryo-ue5-assist-021 |
| embryo.col.s4 | 13 | E | missing_reference | embryo-ue5-assist-022 |
| embryo.col.s4 | 16 | E | missing_reference | embryo-ue5-assist-023 |
| embryo.col.s4 | 21 | E | possible_error | embryo-ue5-assist-024 |
| embryo.col.s4 | 38 | B | roneo_conflict | embryo-ue5-assist-025 |
| embryo.col.s4 | 41 | B | source_conflict | embryo-ue5-assist-026 |
| embryo.col.s4 | 44 | D | source_conflict | embryo-ue5-assist-027 |
| embryo.col.s4 | 47 | B | source_conflict | embryo-ue5-assist-028 |
| embryo.col.s4 | 49 | A | roneo_conflict | embryo-ue5-assist-029 |
| embryo.col.s4 | 50 | D | possible_error | embryo-ue5-assist-030 |
| embryo.col.s4 | 52 | E | roneo_conflict | embryo-ue5-assist-031 |
| embryo.col.s4 | 54 | A | possible_error | embryo-ue5-assist-032 |
| embryo.col.s4 | 60 | E | roneo_conflict | embryo-ue5-assist-033 |
| embryo.col.s4 | 70 | E | missing_reference | embryo-ue5-assist-034 |
| embryo.col.s4 | 72 | D | possible_error | embryo-ue5-assist-035 |
| embryo.col.s4 | 74 | D | source_conflict | embryo-ue5-assist-036 |
| embryo.aut.coeur | 1 | M | possible_error | embryo-ue5-assist-037 |
| embryo.aut.coeur | 2 | K | source_conflict | embryo-ue5-assist-038 |
| embryo.aut.coeur | 2 | E | possible_error | embryo-ue5-assist-039 |
| embryo.aut.coeur | 5 | A, B, C, D, E | source_conflict | embryo-ue5-assist-040 |
| embryo.aut.coeur | 6 | B, C | source_conflict | embryo-ue5-assist-041 |
| embryo.aut.coeur | 7 | E | possible_error | embryo-ue5-assist-042 |
| embryo.aut.coeur | 9 | G, N | source_conflict | embryo-ue5-assist-043 |
| embryo.aut.coeur | 9 | I | possible_error | embryo-ue5-assist-044 |
| embryo.ann.coeur | 4 | E | possible_error | embryo-ue5-assist-045 |
| embryo.ann.coeur | 6 | D | possible_error | embryo-ue5-assist-046 |
| embryo.ann.coeur | 9 | D | source_conflict | embryo-ue5-assist-047 |
| embryo.ann.coeur | 9 | E | source_conflict | embryo-ue5-assist-048 |
| embryo.ann.coeur | 11 | E | possible_error | embryo-ue5-assist-049 |
