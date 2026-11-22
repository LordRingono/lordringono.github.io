# Relecture exhaustive des autotests TN1, TN2 et TN3

## Périmètre et livrables

34 QCM et 181 items relus : TN1 (16 QCM, 80 items), TN2 (10 QCM, 61 items), TN3 (8 QCM, 40 items).

- `reviewed.json` : objets questions complets, basés exclusivement sur la V4.
- `audit.json` : preuve par item, paragraphes originaux, texte du corrigé, verdict littéral, justification, ancien/nouveau contenu et références de capture.
- `crops.json` : 75 panneaux de capture, 34 sujets et 34 corrigés, avec continuations lorsque nécessaire.
- `source_comparison.json` : comparaison des six documents anciens et nouveaux.
- `capture_text_verification.json` : 362 comparaisons intégrales de paragraphes originaux avec les captures ; aucun échec.

## Résultats

Aucune clé de réponse ne change. Tous les identifiants de questions et d’options, tous les poids et toutes les images du site V4 restent inchangés.

Chaque explication commence désormais par **Vrai.** ou **Faux.**, y compris quand le corrigé ne donne que ce verdict. Les justifications sont transcrites intégralement. Six flèches provenant de symboles Word Wingdings, absentes de l’ancienne extraction, sont rétablies.

TN2 Q7 est une question d’ordre des événements : cinq événements constituent le contexte, cinq permutations constituent les réponses. Seule E est explicitement marquée « Vrai ». A–D sont donc les ordres non retenus ; l’audit distingue cette conclusion d’un « Faux » littéralement présent. L’ancien avertissement prétendant l’absence de correction et une question hors note est retiré. La clé E et le poids 1 sont conservés.

TN3 Q5A : l’espace manquant dans « type 1présentent » est rétabli, conformément au texte du corrigé. C’est la seule modification d’un énoncé d’item.

## Sources anciennes et nouvelles

Cinq des six DOCX sont identiques par SHA256. Le sixième, le corrigé TN3, a les mêmes paragraphes, médias, clés et justifications. Seul le signet interne Word `_GoBack` a été déplacé dans le paragraphe de Q3E, ce qui sépare l’espace final après « Vrai » dans un run distinct. Aucune modification du contenu pédagogique.

## Réserves dans la correction

Les deux notes V4 sont conservées, avec leurs champs de contrôle actualisés :

- TN2 Q3B : inversion « Antérograde = dynéine » dans la justification, en conflit avec la ronéo p. 7.
- TN2 Q10E : ambiguïté entre récepteur présynaptique et transporteur de recapture, ronéo p. 15 et 17.

Quatre notes sont ajoutées, sans modifier les clés officielles :

- TN1 Q7D : l’énoncé cite deux méninges tandis que le corrigé ajoute la dure-mère ; préciser le caractère non exhaustif de l’énoncé. Ronéo TN1, page PDF 5.
- TN2 Q2D : le déplacement de − vers + décrit l’antérograde, sans exclure le rétrograde. Ronéo TN2 p. 7. Cette précision a également été validée par l’agent de relecture indépendante.
- TN2 Q6D : « SNP » est une justification trop abrégée ; la ronéo précise que les synapses électriques sont très rares, mais présentes, dans le SNC. Ronéo TN2 p. 11.
- TN3 Q5B : le corrigé dit « récepteurs GLUT1 et GLUT4 », alors que la ronéo dit transporteurs. Ronéo TN3 p. 11.

Toutes les réserves renvoient aux PDF déjà présents sous `sources/revision_v4/`.

## Captures et contrôle visuel

Les 16 pages originales ont été inspectées. Les 75 extraits ont ensuite été inspectés sur 13 planches de QA sous `crop_qa/`. Le seul défaut détecté au découpage était un fragment du cadre du titre du document au-dessus de TN1 Q1 corrigé ; le cadrage définitif commence à 52,1 points et a été revérifié séparément (`tn1_q1_correction_final.png`).

Les captures conservent les figures, y compris les lettres et flèches ajoutées dans Word. Le schéma explicatif de TN1 Q13 reste uniquement dans le corrigé. Le schéma TN3 Q7 préserve ses étiquettes A, B et C.

Sept côtés demandent deux panneaux : TN1 Q8 corrigé ; TN2 Q6 sujet ; TN2 Q4, Q7 et Q10 corrigés ; TN3 Q6 sujet ; TN3 Q8 corrigé. Les autres côtés sont complets sur un seul panneau.

Les 362 versions d’items (181 sujets et 181 corrigés) sont présentes intégralement dans les extraits correspondants après normalisation des espaces et de la ponctuation. Aucun intitulé de la question suivante ne doit être ajouté à l’item ou à sa correction.

## Intégration

Les pages `subjectPage` et `correctionPage` renvoient au rendu PDF des nouveaux originaux ; `approximateDocxPage` vaut `false`. `sourceSubject` et `sourceCorrection` utilisent le nom des nouveaux fichiers transmis. Les originaux eux-mêmes n’ont pas été modifiés.

Les captures finales doivent être produites à partir des rectangles de `crops.json`, pas à partir des planches de contrôle. Les captures sujet restent disponibles avant correction ; les captures corrigé et les réserves scientifiques doivent rester dans la correction.
