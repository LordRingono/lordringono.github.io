# Autotests TC1, TC2, TC3 — comparaison exhaustive des sources

Les 49 QCM et leurs 243 items ont été comparés, dans l’ordre, entre le sujet non corrigé et son corrigé. Les 19 pages des six documents ont été inspectées visuellement. Les six nouveaux DOCX sont identiques, octet par octet (SHA256), aux six documents correspondants de la première archive fournie : le défaut observé ne vient donc pas d’une version différente des documents.

| Banque | QCM | Items | Pages sujet | Pages corrigé |
|---|---:|---:|---:|---:|
| TC1 | 12 | 60 | 2 | 2 |
| TC2 | 13 | 65 | 3 | 3 |
| TC3 | 24 | 118 | 4 | 5 |
| Total | 49 | 243 | 9 | 10 |

## Données et corrections restaurées

- Chaque explication commence maintenant par un verdict explicite **Vrai.** ou **Faux.**, suivi du détail original intégral lorsqu’il existe. Les formulations « V », « F », « VRAI » et « FAUX » des sources sont tracées individuellement dans l’audit. Aucun verdict n’a été déduit d’un silence du corrigé.
- **TC3, Q17 :** les cinq items sont explicitement faux. La chaîne de clé reste vide, mais la question possède désormais `answerIsEmpty` et `allowNoAnswer` ; le message « hors note faute de correction exploitable » est retiré. La question est donc corrigeable comme une réponse « aucune proposition ».
- **TC1, Q11 A et B :** les symboles **α**, stockés en Word sous forme de caractères Symbol, sont restaurés dans les items. L’espace manquant dans « αprésentent » est rétabli dans le site ; l’audit conserve la transcription originale exacte.
- **TC1, Q11 E :** la précision « visible en MET », située avant le mot Vrai dans la version corrigée, est conservée dans l’explication. Le sujet ne reçoit pas cette précision de correction.
- **TC3, Q9 :** l’avertissement du titre corrigé (« ne pas confondre avec les centres d’ossification primaire ») est conservé en `generalExplanation`, uniquement pour la correction.
- Les flèches Wingdings de plusieurs détails sont restaurées. Les six petites variantes de rédaction sujet/corrigé sont tracées dans l’audit et n’altèrent pas les items du sujet.

Les 49 chaînes de lettres de réponse préexistantes concordent avec les verdicts explicites des corrigés. Le changement de notation matériel concerne TC3 Q17, précédemment écartée à tort malgré ses cinq Faux explicites.

## Réserves séparées, visibles après correction

Les six anciennes réserves V4 sont conservées, avec leurs textes et références : TC2 Q2 C, Q6 C, Q7 E, Q11 E, Q12 E et TC3 Q22 C. Leurs empreintes de texte/explication ont été actualisées pour le rendu Vrai/Faux.

Deux réserves fondées sur une contradiction documentaire précise sont ajoutées :

- **TC3, Q8 :** le sujet annonce une QRU, tandis que D et E sont explicitement vrais dans le corrigé. La clé **DE** est conservée et la mention QRU est signalée à vérifier dans la ronéo ou auprès de l’enseignant.
- **TC1, Q11 E :** le sujet porte « 67nM », le corrigé « 67Nm », tandis que la ronéo TC1 p. 13 indique une périodicité de **67 nm**. Une note précise l’unité attendue sans changer la formulation source ni la clé Vrai.

Le détail TC1 Q11 B sur le clivage dans les vésicules a été confronté à la ronéo TC1, p. 12–13 : les supports fournis décrivent eux-mêmes ce clivage dans les vésicules de sécrétion. Aucune contradiction avec cette ronéo n’a donc été inventée.

## Numérotation et présentation des originaux

- Le dernier QCM TC1 est **numéroté 13 dans les deux originaux**, qui sautent le numéro 12. Il y a bien 12 QCM. L’identifiant stable 12 est conservé et `sourceQuestionNumber: 13` permet d’afficher le numéro réel dans le menu original.
- **TC3 Q12 a trois items A, B, C** dans les deux sources. Aucun item D/E n’est inventé.
- Dans le corrigé TC3 Q11, les lettres A/B ne sont pas imprimées devant les deux premières propositions ; elles ont été appariées par leur texte et leur ordre avec le sujet.

## Captures et contrôle de complétude

`crops.json` fournit, pour chaque QCM, les rectangles précis du sujet et du corrigé dans les PDF rendus à partir des originaux. Il y a **107 panneaux** pour 98 côtés sujet/corrigé : neuf côtés se poursuivent sur une deuxième page.

Les cas de coupure sont TC1 Q7 corrigé ; TC2 Q6 sujet et corrigé, Q12 corrigé ; TC3 Q8, Q14 et Q20 sujets, Q15 et Q20 corrigés. Les deux parties sont incluses, jusqu’à la fin du dernier item, sans emporter le titre de la question suivante.

Un contrôle indépendant du texte des rectangles PDF confirme la présence complète des **486 versions d’items** (243 sujets + 243 corrigés) ainsi que de chaque titre. Les 98 côtés contiennent chacun exactement leur propre titre de question. Les 19 pages originales ont été relues visuellement ; les captures de coupure et les glyphes α ont également été vérifiés.

## Fichiers remis au parent

- `reviewed.json` : les 49 objets questions complets à fusionner dans les trois banques V4.
- `audit.json` : preuve par QCM et par item, variantes, verdict littéral, détail intégral, ancien/nouveau texte, pages et lignes des captures.
- `crops.json` : 107 rectangles absolus PDF, avec pages à partir de 1.
- `diff.json` : différences finales avec V4, après mise à jour des pages.
- `old_vs_new.json` : correspondance SHA256 des six anciens/nouveaux documents.
- `visual_review.json`, `capture_text_check.json`, `validation_summary.json` : traces des contrôles.

Tous les identifiants de question et d’option sont inchangés. Les références des deux nouvelles notes qui pointent aux DOCX doivent être raccordées aux fichiers originaux empaquetés par le parent ; les liens de ronéo V4 sont déjà valides.
