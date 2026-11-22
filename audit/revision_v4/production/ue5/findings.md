# Révision UE5 — histologie et biologie cellulaire

## Périmètre et niveau de preuve

533 questions ont fait l’objet d’une lecture intégrale du texte importé : 310 en histologie et 223 en biologie cellulaire, soit 2667 items. Les explications ont été relues avec les items, en tenant compte des questions à formulation inversée (affirmation inexacte). Les trois premiers QCM de biologie CM2, dont les options ne sont pas transcrites, ont été lus sur les pages originales. Les 597 questions d’embryologie n’ont pas été relues par cet agent : elles relèvent du lot distinct embryo.

96 notes sont proposées sur 94 questions. Elles sont destinées uniquement à la zone de correction. Elles ne changent pas les clés pour un désaccord scientifique. Le texte de chaque item visé et son explication importée sont conservés dans notes.json pour permettre une relecture contradictoire.

Les cours ont été utilisés pour des confrontations ciblées des points suspects. La lecture d’une question sans anomalie détectée ne constitue pas une validation exhaustive par la ronéo. La couverture distingue expressément les items confrontés à une page, la lecture textuelle seule et les cas qui nécessitent encore une source ou une figure.

## Réparations d’import séparées des désaccords scientifiques

source_repairs.json contient 30 dossiers de réappariement, dont 28 clés différentes de celles du site initial. Deux dossiers TC2 ne changent que l’appariement des explications. Aucune de ces opérations ne substitue une réponse scientifique à celle du tutorat.

| Banque | Questions concernées | Preuve |
|---|---|---|
| histo.tc2 | 1–13 | CORRECTION autotest TC2.docx, paragraphes associés aux options ; 11 clés et 13 blocs explicatifs concernés |
| bio.ann.cm2 | 4–8 | Annales CM2 corrigées-1.pdf, pages 4–7, pages scannées inspectées visuellement |
| bio.ann.cm5 | 7–14 et 16 | Annales corrigées CM5 2018-2025.pdf, pages 7–14 ; ordre visuel et texte trié par position |
| bio.ann.cm7 | 9 | Correction ACC le noyau.pdf, page 10 |
| bio.ann.cm8 | 3 | Annales corrigees CM8 2019-2025-1.pdf, page 3 |
| histo.ann.tn | 64 | annales TISSU NERVEUX 2018 2025 CORRECTION.pdf, pages 23–24 : clé BDE ; anciennes explications issues des astrocytes page 18 |

La séquence de blocs dans les PDF de biologie n’est pas toujours celle de l’ordre de lecture. Plusieurs clés importées venaient de la question voisine. Le texte trié selon la position sur la page et les rendus inspectés ont permis de distinguer cette erreur de lecture du PDF d’un désaccord scientifique réellement présent dans le corrigé.

## Exemples de conflits étayés par le cours

- Histo.ann.tc 49 E : moelle hématopoïétique entre les travées de l’os spongieux (TC3, page 15).
- Histo.ann.tc 54 C : l’absence de collagène rend l’os fragile (TC3, page 4).
- Histo.ann.tn 61 C : la ronéo nomme explicitement un transport rétrograde rapide par la dynéine (TN2, page 7).
- Histo.autotech 2 E : l’éosine est un colorant acide (Techniques, page 17).
- Bio.cm6 5 E : la phosphatidylsérine se situe surtout sur le feuillet cytosolique (CM6, pages 7–8) ; le faux est bien présent dans le DOCX original.
- Bio.ann.cm5 12 C et 15 B : Rab recrute les moteurs, elle n’est pas elle-même le moteur du cytosquelette (CM5, pages 4 et 6).
- Bio.ann.cm9 7 B : la prophase suit le deuxième point de contrôle G2/M ; le troisième précède l’anaphase (CM9, pages 4 et 10).
- Bio.ann.cm10 5 B : les lysosomes digèrent les acides nucléiques (CM8, page 13).

Les notes distinguent systématiquement une erreur de verdict d’un lapsus dans l’explication d’un verdict juste : cellules de Leydig dans l’interstitium, ostéoblastes et matrice osseuse, dynéine rétrograde, diamètre des microtubules, cytoplasme excluant le noyau, Asn dans la N-glycosylation, fer détaché de la transferrine et apoptosome distinct des corps apoptotiques.

## Contradictions des sources conservées

- Une même proposition sur les cytokines pro-inflammatoires des cellules sénescentes est fausse dans CM10 Q7 E et vraie dans Q12 C.
- La même question illustrée de sénescence a la clé DE en CM2 et ABDE en CM10 ; les affirmations de microscopie électronique divergent.
- Des annotations manuscrites ou ajoutées réfutent certaines réponses sans modifier les clés initiales, notamment CM4 Q7 C/E, CM5 Q9 A, CM5 Q10 C, CM5 Q15 E et CM7 Q5 C.
- Histo.ann.tn Q1 A et Q38 A donnent des verdicts opposés à la liste incluant les organes circumventriculaires.
- Histo.ann.tech Q15 A est noté vrai alors que la phrase et son explication se contredisent sur la visibilité des papilles.

## Références actuelles qui ne permettent pas de trancher

Les 25 notes possible_error sont explicitement rédigées comme des points « À vérifier dans la ronéo ». Elles ne sont pas comptées comme des erreurs confirmées. Exemples : structure tubulaire des filaments intermédiaires, aquaporines et diabète insipide, potentiel Cl− à l’équilibre, masse d’ADN de 100 pg, p16 et sénescence. Aucun cours CM10 spécifique n’a été trouvé dans le pack ; CM8 et CM9 permettent seulement une vérification partielle de ce thème.

Certains raccourcis discutables du QCM se retrouvent dans la ronéo elle-même : shARN assimilé à un transgène, Fe-S associés à l’hème/cytochromes, emploi de glycolyse pour l’oxydation mitochondriale, ATR « transcription » de Chk. Ils sont explicitement séparés des conflits QCM/ronéo. Une ronéo n’est donc pas traitée comme une garantie que toutes ses formulations sont exactes.

Le tableau actualisé TE1 ne renseigne plus la membrane basale du mésothélium : il indique que la légende a été retirée. La réponse ancienne sur son absence est classée outdated_reference, pas validée par le cours actuel.

## Limites structurelles et visuelles

- Bio.cm10 Q1 : le sujet contient quatre lettres après fusion de deux propositions dans A, le corrigé cinq propositions F/F/F/F/V. Le sujet est correctement reproduit mais incompatible avec le corrigé ; la question reste hors note.
- Histo.te2 Q9 B : le sujet s’arrête à « Elle est constitutivement » ; le corrigé apporte « ouverte ». Le document source permet de connaître le mot manquant, mais le sujet lui-même est tronqué.
- Histo.ann.te Q18 et histo.ann.tech Q23 contiennent des fragments de questions antérieures dans le texte importé. Cette concaténation a été repérée ; aucune suppression de texte n’a été imposée par cet agent.
- Histo.ann.tn Q63 : A n’a pas de marque V/F littérale ; son explication oppose néanmoins la partie interne de la moelle à la partie externe des hémisphères. Les autres verdicts sont B faux, C vrai, D vrai, E faux. La question est laissée hors note par prudence documentaire, avec cette preuve disponible pour décision du responsable de fusion.
- 98 questions possèdent une figure qui n’a pas été réinterprétée individuellement pendant ce lot. Les items textuels ont été lus ; les conclusions qui dépendent de l’image restent explicitement non certifiées dans coverage.json.

## Registre complet des notes

| Identifiant | Question | Items | Type | Références |
|---|---|---|---|---|
| ue5-001 | histo.te1 Q4 | E | outdated_reference | Tissu épithélial 1 - CG ACTUALISE.pdf p. 5 |
| ue5-002 | histo.te2 Q6 | D | roneo_conflict | Tissu épithélial 2 - CG - ACTUALISE.pdf p. 6 |
| ue5-003 | histo.te2 Q7 | C | roneo_conflict | Tissu épithélial 2 - CG - ACTUALISE.pdf p. 7 ; Tissu épithélial 2 - CG - ACTUALISE.pdf p. 5 |
| ue5-004 | histo.te2 Q9 | B | source_conflict | autotest TE2 (2).docx — Paragraphe 60 (index à partir de 0), QCM 9 B ; correction autotest TE2 25.docx — Paragraphe 62 (index à partir de 0), QCM 9 B |
| ue5-005 | histo.te2 Q18 | C | roneo_conflict | Tissu épithélial 2 - CG - ACTUALISE.pdf p. 11 |
| ue5-006 | histo.tc3 Q22 | C | possible_error | TC3 2026.pdf p. 10 |
| ue5-007 | histo.autotech Q2 | E | roneo_conflict | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 17 |
| ue5-008 | histo.autotech Q7 | A | possible_error | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 19 |
| ue5-009 | histo.tn2 Q3 | B | roneo_conflict | TN2 - Ronéo 2026 - Actualisée.pdf p. 7 |
| ue5-010 | histo.tn2 Q10 | E | possible_error | TN2 - Ronéo 2026 - Actualisée.pdf p. 15 ; TN2 - Ronéo 2026 - Actualisée.pdf p. 17 |
| ue5-011 | histo.ann.te Q7 | B | roneo_conflict | Tissu épithélial 1 - CG ACTUALISE.pdf p. 15 ; Tissu épithélial 1 - CG ACTUALISE.pdf p. 16 |
| ue5-012 | histo.ann.te Q26 | A | roneo_conflict | Tissu épithélial 1 - CG ACTUALISE.pdf p. 16 |
| ue5-013 | histo.ann.tc Q6 | D | roneo_conflict | TC3 2026.pdf p. 6 ; TC3 2026.pdf p. 7 |
| ue5-014 | histo.ann.tc Q15 | C | roneo_conflict | TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 7 |
| ue5-015 | histo.ann.tc Q21 | A | roneo_conflict | TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 12 |
| ue5-016 | histo.ann.tc Q31 | E | roneo_conflict | TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 11 ; TC2 2026 - Partie 1 ACTUALISE.pdf p. 4 |
| ue5-017 | histo.ann.tc Q49 | E | roneo_conflict | TC3 2026.pdf p. 15 |
| ue5-018 | histo.ann.tc Q54 | C | roneo_conflict | TC3 2026.pdf p. 4 |
| ue5-019 | histo.ann.tc Q56 | B | roneo_conflict | TC3 2026.pdf p. 12 ; TC3 2026.pdf p. 13 |
| ue5-020 | histo.ann.tn Q6 | B | roneo_conflict | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 3 ; Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 24 |
| ue5-021 | histo.ann.tn Q22 | E | source_conflict | TN2 - Ronéo 2026 - Actualisée.pdf p. 12 |
| ue5-022 | histo.ann.tn Q33 | A | roneo_conflict | TN3 - Ronéo 2026.pdf p. 14 |
| ue5-023 | histo.ann.tn Q34 | D | roneo_conflict | TN1 - Ronéo 2026 - ACTUALISEE.pdf p. 13 |
| ue5-024 | histo.ann.tn Q35 | B | possible_error | TN1 - Ronéo 2026 - ACTUALISEE.pdf p. 4 |
| ue5-025 | histo.ann.tn Q1 | A | source_conflict | TN1 - Ronéo 2026 - ACTUALISEE.pdf p. 4 |
| ue5-026 | histo.ann.tn Q38 | A | source_conflict | TN1 - Ronéo 2026 - ACTUALISEE.pdf p. 4 |
| ue5-027 | histo.ann.tn Q58 | C | roneo_conflict | TN3 - Ronéo 2026.pdf p. 12 |
| ue5-028 | histo.ann.tn Q61 | C | roneo_conflict | TN2 - Ronéo 2026 - Actualisée.pdf p. 7 |
| ue5-029 | histo.ann.tech Q2 | E | possible_error | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 14 |
| ue5-030 | histo.ann.tech Q8 | B | roneo_conflict | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 13 |
| ue5-031 | histo.ann.tech Q9 | A | possible_error | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 15 |
| ue5-032 | histo.ann.tech Q10 | E | roneo_conflict | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 21 |
| ue5-033 | histo.ann.tech Q15 | A | source_conflict | ANNALES Techniques 2019 2026 CORRECTION.pdf p. 7 |
| ue5-034 | histo.ann.tech Q17 | D | roneo_conflict | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 24 |
| ue5-035 | histo.ann.tech Q19 | D | roneo_conflict | roneo CM3 LE CYTOSQUELETTE - CG - Actualisation.pdf p. 1 |
| ue5-036 | histo.ann.tech Q20 | B | roneo_conflict | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 38 ; Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 39 |
| ue5-037 | histo.ann.tech Q22 | E | roneo_conflict | Tissu épithélial 2 - CG - ACTUALISE.pdf p. 15 ; Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 29 |
| ue5-038 | histo.ann.tech Q37 | B, D | possible_error | Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 29 ; Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 23 |
| ue5-039 | histo.ann.tech Q36 | B | roneo_conflict | Roneo_CM1_GENERALITES_sur_les_cellules_LBH___CG___26_ACTUALISATION.pdf p. 5 |
| ue5-040 | bio.cm2oral Q1 | B | possible_error | roneo CM2 Techniques en BIO CELL 26 LBH CG corrigées.pdf p. 5 ; roneo CM2 Techniques en BIO CELL 26 LBH CG corrigées.pdf p. 6 |
| ue5-041 | bio.ann.cm2 Q3 | D | roneo_conflict | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 12 ; roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 13 |
| ue5-042 | bio.cm3 Q10 | B | roneo_conflict | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 12 |
| ue5-043 | bio.ann.cm3 Q4 | A | possible_error | roneo CM3 LE CYTOSQUELETTE - CG - Actualisation.pdf p. 1 ; roneo CM3 LE CYTOSQUELETTE - CG - Actualisation.pdf p. 6 |
| ue5-044 | bio.cm4 Q2 | D | roneo_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 22 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 13 |
| ue5-045 | bio.cm4 Q7 | C | possible_error | Ronéo RE et adressage 2026 - Corrigé.pdf p. 14 |
| ue5-046 | bio.ann.cm4 Q1 | E | roneo_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 8 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 22 |
| ue5-047 | bio.ann.cm4 Q3 | A | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 6 |
| ue5-048 | bio.ann.cm5 Q4 | A | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 6 |
| ue5-049 | bio.ann.cm4 Q4 | D | source_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 10 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 11 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 12 |
| ue5-050 | bio.ann.cm4 Q6 | D | source_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 10 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 11 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 12 |
| ue5-051 | bio.ann.cm4 Q5 | D | possible_error | CM8 Ronéo 2026 - Actualisee.pdf p. 9 ; CM8 Ronéo 2026 - Actualisee.pdf p. 10 |
| ue5-052 | bio.ann.cm4 Q7 | B, C, E | roneo_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 11 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 14 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 8 |
| ue5-053 | bio.ann.cm4 Q8 | D | roneo_conflict | Ronéo RE et adressage 2026 - Corrigé.pdf p. 16 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 20 |
| ue5-054 | bio.cm5 Q11 | A | roneo_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 18 |
| ue5-055 | bio.ann.cm5 Q8 | C | roneo_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 6 |
| ue5-056 | bio.ann.cm5 Q9 | A | source_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 10 ; Annales corrigées CM5 2018-2025.pdf p. 8 |
| ue5-057 | bio.ann.cm5 Q10 | C | source_conflict | CM8 Ronéo 2026 - Actualisee.pdf p. 2 ; CM8 Ronéo 2026 - Actualisee.pdf p. 10 ; Annales corrigées CM5 2018-2025.pdf p. 9 |
| ue5-058 | bio.ann.cm5 Q12 | C | roneo_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 4 ; CM5 ronéo 2026 - Corrigé.pdf p. 6 |
| ue5-059 | bio.ann.cm5 Q14 | E | roneo_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 4 |
| ue5-060 | bio.ann.cm5 Q15 | B, D, E | roneo_conflict | CM5 ronéo 2026 - Corrigé.pdf p. 4 ; CM5 ronéo 2026 - Corrigé.pdf p. 9 ; CM5 ronéo 2026 - Corrigé.pdf p. 10 ; CM8 Ronéo 2026 - Actualisee.pdf p. 2 ; CM8 Ronéo 2026 - Actualisee.pdf p. 10 |
| ue5-061 | bio.cm6 Q2 | C | possible_error | roneo CM6 MP 2026 - Actualisee.pdf p. 14 |
| ue5-062 | bio.cm6 Q5 | E | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 7 ; roneo CM6 MP 2026 - Actualisee.pdf p. 8 |
| ue5-063 | bio.cm6 Q7 | D | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 8 |
| ue5-064 | bio.cm6 Q11 | B, E | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 13 ; roneo CM6 MP 2026 - Actualisee.pdf p. 17 |
| ue5-065 | bio.ann.cm6 Q9 | E | possible_error | roneo CM6 MP 2026 - Actualisee.pdf p. 13 |
| ue5-066 | bio.ann.cm6 Q11 | A | roneo_conflict | roneo CM6 MP 2026 - Actualisee.pdf p. 12 |
| ue5-067 | bio.ann.cm6 Q20 | E | possible_error | roneo CM6 MP 2026 - Actualisee.pdf p. 13 |
| ue5-068 | bio.cm7 Q5 | C | roneo_conflict | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 5 ; Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 9 |
| ue5-069 | bio.ann.cm7 Q4 | A | possible_error | Correction ACC le noyau.pdf p. 5 |
| ue5-070 | bio.ann.cm7 Q5 | C | source_conflict | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 19 ; Correction ACC le noyau.pdf p. 6 |
| ue5-071 | bio.ann.cm7 Q8 | B | source_conflict | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 19 ; Correction ACC le noyau.pdf p. 6 |
| ue5-072 | bio.ann.cm7 Q10 | B | source_conflict | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 19 ; Correction ACC le noyau.pdf p. 6 |
| ue5-073 | bio.ann.cm7 Q5 | D | possible_error | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 14 |
| ue5-074 | bio.ann.cm7 Q6 | C | source_conflict | Correction ACC le noyau.pdf p. 7 ; Roneo_CM1_GENERALITES_sur_les_cellules_LBH___CG___26_ACTUALISATION.pdf p. 6 |
| ue5-075 | bio.ann.cm7 Q6 | E | possible_error | Correction ACC le noyau.pdf p. 7 |
| ue5-076 | bio.ann.cm7 Q11 | A | possible_error | Ronéo CM7 Le noyau 2026 CG - Corrigées.pdf p. 16 ; Ronéo RE et adressage 2026 - Corrigé.pdf p. 10 |
| ue5-077 | bio.cm8 Q5 | B | possible_error | CM8 Ronéo 2026 - Actualisee.pdf p. 2 ; CM8 Ronéo 2026 - Actualisee.pdf p. 10 |
| ue5-078 | bio.cm8 Q10 | A, E | roneo_conflict | CM8 Ronéo 2026 - Actualisee.pdf p. 5 ; CM8 Ronéo 2026 - Actualisee.pdf p. 6 ; CM8 Ronéo 2026 - Actualisee.pdf p. 7 |
| ue5-079 | bio.cm8 Q11 | A, E | possible_error | CM8 Ronéo 2026 - Actualisee.pdf p. 7 ; CM8 Ronéo 2026 - Actualisee.pdf p. 8 |
| ue5-080 | bio.ann.cm8 Q6 | D | possible_error | CM8 Ronéo 2026 - Actualisee.pdf p. 7 |
| ue5-081 | bio.cm9 Q11 | A | possible_error | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 9 |
| ue5-082 | bio.ann.cm9 Q1 | A | roneo_conflict | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 4 ; roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 6 |
| ue5-083 | bio.ann.cm9 Q5 | E | possible_error | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 13 |
| ue5-084 | bio.ann.cm9 Q7 | B | roneo_conflict | roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 4 ; roneo CM9 le cycle cellulaire 2026 - Actualisee.pdf p. 10 |
| ue5-085 | bio.cm10 Q1 | A, B, C, D | source_conflict | AUTOTEST CM10 MORT CELLULAIRE.docx — Premier QCM, paragraphe 5 : fusion de deux propositions ; CORRECTION autotest CM10 MORT CELLULAIRE.docx — Premier QCM, paragraphes 5 à 9 : cinq propositions |
| ue5-086 | bio.cm10 Q3 | A | possible_error | Ronéo spécifique absente |
| ue5-087 | bio.ann.cm10 Q1 | A | roneo_conflict | CM8 Ronéo 2026 - Actualisee.pdf p. 5 ; CM8 Ronéo 2026 - Actualisee.pdf p. 7 |
| ue5-088 | bio.ann.cm10 Q5 | B | roneo_conflict | CM8 Ronéo 2026 - Actualisee.pdf p. 13 |
| ue5-089 | bio.ann.cm10 Q7 | E | source_conflict | Annales corrigées CM10 2023-2025.pdf p. 7 ; Annales corrigées CM10 2023-2025.pdf p. 11 |
| ue5-090 | bio.ann.cm10 Q12 | C | source_conflict | Annales corrigées CM10 2023-2025.pdf p. 7 ; Annales corrigées CM10 2023-2025.pdf p. 11 |
| ue5-091 | bio.ann.cm10 Q10 | A, B | source_conflict | Annales corrigées CM10 2023-2025.pdf p. 10 ; Annales CM2 corrigées-1.pdf p. 7 ; Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 32 ; Ronéo Techniques Histologiques Gouriou 2026 ACTUALISEE.pdf p. 38 |
| ue5-092 | histo.tc2 Q2 | C | roneo_conflict | TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 11 ; TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 12 ; TC2 2026 - Partie 1 ACTUALISE.pdf p. 10 |
| ue5-093 | histo.tc2 Q6 | C | possible_error | TC2 2026 - Partie 1 ACTUALISE.pdf p. 2 |
| ue5-094 | histo.tc2 Q7 | E | roneo_conflict | TC2 2026 - Partie 1 ACTUALISE.pdf p. 4 ; TC1 2026 - CG non corrigées - ACTUALISE.pdf p. 11 |
| ue5-095 | histo.tc2 Q11 | E | roneo_conflict | TC2 2026 - Partie 1 ACTUALISE.pdf p. 19 |
| ue5-096 | histo.tc2 Q12 | E | roneo_conflict | TC2 2026 - Partie 1 ACTUALISE.pdf p. 18 ; TC2 2026 - Partie 1 ACTUALISE.pdf p. 19 |

## Fichiers de contrôle

- notes.json : annotations prêtes à fusionner, textes exacts des items relus et références.
- coverage.json : 533 entrées individuelles, items relus, statut, figures, fichiers consultés, notes et limites.
- source_repairs.json : preuves et propositions de réappariement au corrigé original.
- candidate_decisions.json : résolution des 113 points envisagés lors de la lecture ; les suspicions non étayées sont visibles et ne sont pas transformées en erreurs certaines.
- summary.json : comptes de couverture et de résultats.
- course_catalog.json : chemins des ronéos paginées effectivement utilisées.

Toutes les pages citées sont des pages physiques du PDF à partir de 1. Les renvois DOCX utilisent les paragraphes, car aucune pagination Word artificielle n’a été inventée. Aucun fichier du site n’a été modifié par cet agent.
