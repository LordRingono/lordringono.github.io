# Relecture UE4 V3 — lot récent, revue finale

## Résultat et périmètre

Les **114 QCM et leurs 570 propositions A–E** ont été relus sujet par sujet, puis contrôlés une deuxième fois contre la source et le JSON. Les questions restent indivisibles. `reviews.json` contient une entrée unique par `sourceId`, le thème retenu, le motif du classement, les cinq contrôles d’items, les éventuelles réserves après correction et les patches documentés.

Source exclusive : `upload/Sujets + corrections compilés(1).pdf`. Toutes les pages mentionnées ici sont celles du PDF compilé, numérotées à partir de 1. Aucun contenu scientifique externe n’a remplacé le corrigé fourni. Les ronéos ne sont pas dans ce lot ; les commentaires invitent à y vérifier les points réellement discutables.

| Sujet | QCM | Items | Pages du sujet | Grille courte | Corrigé détaillé |
|---|---:|---:|---|---|---|
| 2025–2026 S1 | 28 | 140 | 702–709 | 712 | 713–726 |
| 2024–2025 S1 | 28 | 140 | 728–734 | 736 | 737–749 |
| 2024–2025 S2 | 15 | 75 | 752–755 | 758 | 759–765 |
| 2023–2024 S1 | 28 | 140 | 768–774 | 776 | 777–788 |
| 2023–2024 S2 | 15 | 75 | 790–792 | 794 | 795–800 |
| **Total** | **114** | **570** | | | |

Aucun HTML, aucune banque ancienne et aucun asset existant n’ont été modifiés par cette revue. Aucune nouvelle image scientifique n’est nécessaire. Les quatre figures d’énoncé présentes sont complètes et réutilisables.

## Erreur d’appariement à réparer : 2023–2024 S2 Q5

Cette question de pharmacocinétique était hors note dans l’entrée. La contrelecture visuelle révèle que ce statut reposait sur une erreur d’appariement, et non sur une contradiction du PDF :

- La grille courte p794 donne **ACE**.
- La boîte de correction de Q5 p796 donne aussi **ACE**, avec A/C/E vrais, B faux (« en cas d’insuffisance hépatique »), D faux (justification sur Tmax).
- La page797 commence **Q6, effet indésirable grave**, dont les verdicts sont AB vrais, C/D/E faux. Ce sont ces cinq verdicts qui avaient remplacé les explications de Q5 dans le JSON.
- La capture `annales_ue4_2023-2024_s2_q05_explanation_p796.webp` montre la bonne boîte, intégralement. La capture suffixée `p797.webp` contient explicitement le sujet et le corrigé du Q6 et doit être retirée de Q5.

Sept patches séparés figurent dans `reviews.json`, avec valeur avant/après et preuve : `explanations.B`, `.C`, `.D`, `.E`, `correctionImages`, `warning`, `answer`. La proposition restaure **answer: ACE**, déjà conservée dans `rawAnswer`, et retire le faux avertissement de divergence. L’explication A, le poids, les identifiants, `correctionPage:796` et `shortCorrectionPage:794` restent identiques. Il ne faut pas maintenir artificiellement cette question hors note après réparation de son appariement.

La règle de conservation des clés a été respectée pour les 113 autres QCM. Le rétablissement de ACE est la seule exception de notation proposée, fondée sur deux clés imprimées concordantes. Les autres hors-note de l’UE4 sont hors du périmètre de ce lot.

## Justifications hors sujet imprimées dans la source : 2025–2026 S1

Trois autres patches, autorisés en principe par le root, neutralisent uniquement une justification manifestement étrangère à l’item. Les clés restent inchangées et les captures conservent l’original.

| Question/item | Pages | Défaut constaté | Proposition |
|---|---|---|---|
| Q13 C | 718 | L’item traite de synthèse d’analogues ; la justification parle de faible quantité dans des écorces et de production industrielle. | Remplacer `explanations.C` par une mention neutre et renvoyer à la réserve. |
| Q14 D | 718–719 | Justification sur la thérapie cellulaire et la DMLA, répétée sous Q15 D, sans rapport avec le produit naturel de Q14. | Même mention neutre ; clé ABC conservée. |
| Q14 E | 718–719 | Justification sur les métabolites/métabolome, répétée sous Q15 E, sans rapport avec l’item de Q14. | Même mention neutre ; clé ABC conservée. |

Mention proposée : « La justification imprimée ne correspond pas à cet item ; voir la réserve ci-dessous. » Les textes avant modification sont intégralement présents dans les patches. Aucun commentaire scientifique de remplacement n’est inventé.

**Bilan des propositions : 10 champs à réparer, sur 3 QCM.** Aucun patch d’énoncé ni d’option n’est nécessaire dans ce lot.

## Réserves croisées entre sujets

Les réserves sont réciproques pour que le lecteur les trouve quelle que soit l’année qu’il consulte. Elles restent strictement après correction.

| Point | Premier verdict imprimé | Verdict ou justification opposée |
|---|---|---|
| Héparine produite à grande échelle par biotechnologie | 2025–2026 S1 Q13 B, vrai, p718 | 2024–2025 S2 Q2 B, faux, p759 |
| R&D développé en « résolution et développement » | 2025–2026 S1 Q15 A, vrai, p719 | 2023–2024 S1 Q1 A, faux : « recherche », p777 |
| Séances d’ETP comme première étape | 2025–2026 S1 Q10 C, vrai, p717 | 2023–2024 S1 Q13 C, faux : troisième étape, p782 |
| Chromatographie qualitative et quantitative | 2025–2026 S1 Q26 A, vrai, p723 ; 2024–2025 S1 Q17 C, vrai, p744 | 2023–2024 S1 Q24 D, faux : seulement qualitative, p786 |
| Optimisation d’un lead | 2024–2025 S1 Q22 D décrit une phase de lead optimization, p746 | 2023–2024 S1 Q8 D refuse la modulation de chaîne car le lead serait déjà optimisé, p780 |
| Document décrivant les modes de fabrication | 2024–2025 S1 Q17 A : dossier d’AMM, p744 | 2023–2024 S1 Q24 E : pharmacopée, p786, avec sigle « TBF » non défini dans le sujet |

Ces notes ne changent aucun verdict. Elles distinguent une contradiction entre corrigés, une justification insuffisante et une incertitude explicitement reconnue par le tutorat.

## Points sensibles relus dans chaque sujet

### 2025–2026 S1

Contrôles particuliers : gravité des effets indésirables Q3 A/E ; procédé des biothérapies et confusion PK/PD Q5 D/E ; ETP Q10 C ; code de déontologie simultanément présenté comme législatif et réglementaire Q11 A/B ; sources naturelles Q13/Q14 ; R&D Q15 A ; contrôle visuel versus stérilité Q17 E ; biodisponibilité Q18 A ; isotonie Q19 B ; pharmacophore Q27 A ; calcul QSAR Q28 B/E.

Pour Q28, les descripteurs des trois molécules sont `(3,2,4)`, `(1,3,4)`, `(2,3,4)`. Les coefficients E `(2,3,1)` donnent bien **16,15,17**. La source imprime `1×2=1` dans B et des signes d’inégalité à côté des égalités de E : la clé E reste cohérente. Les règles de comptage incertaines de Q27 A sont signalées comme telles, conformément à l’hésitation du corrigé p725.

### 2024–2025 S1

Contrôles particuliers : AND dans le sujet versus ADN dans sa reprise corrigée Q1 E ; commentaires de statut magistral/hospitalier Q8 A/C ; BPF/procédé et édition datée de pharmacopée Q18 A/B ; expansion des CAR-T Q19 D ; bio-séroconversion versus activation d’un promédicament Q21 E ; DFT et AMBER Q23 B/D ; composantes de l’EBM Q26 ; absence des tests d’activité dans le schéma explicatif de Q28.

Q24 est graphique : les cinq libellés JSON « Molécule A/B/C/D/E (voir le schéma) » sont des renvois d’interface. Les cinq structures, leur lettre, le pharmacophore et sa légende sont bien dans l’image d’énoncé p733. Ces renvois ne doivent pas être traités comme des énoncés manquants.

### 2024–2025 S2

Contrôles particuliers : héparine/insuline et hémisynthèse Q2 ; Formulaire national/répertoire interne Q7 B ; formule d’ASC sans doses Q8 B ; prix et balance bénéfice-risque Q10 A ; commentaire annonçant quatre déterminants mais en listant cinq Q12 C ; visibilité de la structure secondaire refusée par opposition à la représentation tertiaire Q15 E. Les 15 clés concordent avec leurs tableaux détaillés et la grille courte.

### 2023–2024 S1

Contrôles particuliers : R&D Q1 ; jalon de séquençage génomique Q2 E ; origine de céphalosporine attribuée à un mollusque marin Q7 E ; optimisation du lead Q8 D ; ordre de l’ETP Q13 C ; essai vaccinal Q17 ; adultération des huiles essentielles qualifiée d’ambiguë par le tutorat Q23 D ; chromatographie et textes de fabrication Q24 ; périmètre de prescription infirmier Q26 D ; opposition « approximations/calculs » en mécanique moléculaire Q27 D.

L’énoncé Q17 p771 comporte bien les **21720/21728 participants**, les **8/162 infections**, le délai de sept jours après la seconde injection et la confirmation PCR. Le corrigé p783 déduit une phase IV de l’effectif/randomisation, et met lui-même des points d’interrogation après C et E : ces limites sont signalées sans changer AC.

Q24 : le sujet p773 porte A–E ; sa reprise p786 est malencontreusement étiquetée F–J. Le tableau détaillé reste A–E, dans le même ordre que le vrai sujet. Le mapping est donc correct et documenté dans chaque contrôle d’item.

Q28 : le sujet écrit `nCv` dans les descripteurs et `nCy` dans les options. Les trois molécules, activités **6,7,15µM**, et les vecteurs `(4,1,0)`, `(5,1,0)`, `(7,2,2)` conduisent à D, coefficients `(1,2,2)`. Le corrigé est un calcul global sans verdict imprimé pour chacune des cinq lettres : les contrôles l’indiquent explicitement et ne prétendent pas lire cinq VRAI/FAUX inexistants.

### 2023–2024 S2

En plus de l’appariement Q5, réserves sur la date de la Charte et son intégration constitutionnelle Q1 A ; formulation « même biodisponibilité » pour les génériques Q3 E ; champ d’application des BPF Q4 A ; évaluation de toxicité dite principalement en phase II Q10 B ; justifications de phase I/IV et minimum de trois doses déduit sans source explicite Q12 B/C/D.

Les 15 consignes et 75 items concordent textuellement avec le sujet. Les 14 autres appariements sont corrects. Aucune image d’énoncé supplémentaire n’est requise dans ce sujet.

## Répartition proposée selon les 15 thèmes imposés

| Thème | QCM de ce lot |
|---|---:|
| Sources naturelles - Kerzaon | 9 |
| Galénique | 5 |
| Le droit pharma | 18 |
| Cycle de vie du médicament | 1 |
| Balance bénéfice/risque | 9 |
| Conception rationnelle : Terreux | 8 |
| Identification PA : Bourguignon | 13 |
| Développement clinique | 6 |
| Biotechnologies | 12 |
| Chimie organique | 3 |
| PK PD | 8 |
| Cibles, mécanisme & actions | 0 |
| Analyse & contrôles des médicaments | 8 |
| Iatrogénie | 2 |
| BUM | 12 |
| **Total** | **114** |

L’absence de QCM dans « Cibles, mécanisme & actions » dans ce lot n’est pas une omission : les questions sur agonisme sont centrées sur les paramètres PK/PD, et les questions CAR-T sur les biotechnologies.

### Frontières de classement à harmoniser au niveau global

- 2025–2026 S1 Q22 → **Cycle de vie** : évaluation et positionnement du générique (efficacité, bioéquivalence, substitution, ASMR, BBR). C’est le cas le plus transversal. Les définitions et exigences juridiques du générique (2023–2024 S2 Q3 ; 2024–2025 S2 Q6) restent **Droit**.
- Les textes opposables, droits de prescription, statuts de préparations et conditions légales → **Droit** ; les méthodes de dosage et impuretés → **Analyse & contrôles** ; formes/voies/stérilité → **Galénique**.
- Formules de Markush, hit/lead, criblage et Drug Discovery → **Identification PA**. Descripteurs, docking, QSAR et mécanique moléculaire → **Conception rationnelle**. Châssis/fonctions/chiralité des AINS → **Chimie organique**.
- CAR-T → **Biotechnologies**. Essais vaccins, phases et éthique clinique → **Développement clinique**. Expertise clinique et attentes du patient dans l’EBM → **BUM**.
- Effet indésirable grave seul (2023–2024 S2 Q6) → **Iatrogénie** ; évaluation de toxicité/surveillance et pharmaco-épidémiologie → **Balance bénéfice/risque**.

Les 20 entrées de confiance moyenne donnent leur justification de frontière ; aucune question n’a été séparée en plusieurs thèmes.

## Contrôles finaux et limites

- 114 identifiants uniques, exactement ceux de l’entrée ; 570 contrôles A–E, sans omission.
- Les 114 consignes et 565 propositions textuelles concordent avec leur sujet après normalisation typographique. Les 5 propositions graphiques de Q24 2024–2025 sont vérifiées visuellement.
- Les 114 clés brutes concordent avec les grilles courtes. Les verdicts détaillés concordent après réparation de l’appariement Q5 ; Q28 2023–2024 utilise sa correction globale par calcul.
- Les changements proposés de Q13/Q14 2025–2026 ne remplacent aucune clé : ils empêchent seulement une justification étrangère à l’item d’être présentée comme pertinente.
- Seule différence de notation proposée : retour de Q5 2023–2024 S2 à ACE, démontré par la source. Aucun poids ni identifiant de sauvegarde modifié.
- 54 notes sur 45 QCM : 21 contradictions documentaires, 18 erreurs possibles, 14 incertitudes et 1 référence d’édition datée. Toutes invitent à consulter la ronéo et doivent rester après correction.
- Les consignes de sélection ont été relues. Les deux questions portant sur une forme non stérile demandent les propositions exactes : les verdicts ne sont pas inversés. Aucune réserve n’est fondée sur une simple inversion « vrai/faux » de la consigne.
- Les quatre figures scientifiques ont été comparées au sujet, puis revues à la seconde passe. Structures, atomes, liaisons, lettres, légendes, descripteurs et valeurs restent visibles avant correction, sans annotation de réponse ajoutée.
- Inspection visuelle des pages 708,709,717,718,725,726,728,733,745–749,759,764,765,774,777,779,782,783,786–788,795–800, plus captures spécifiques. Les autres pages ont fait l’objet de la comparaison des énoncés, items, clés et explications textuelles.
- Aucun nouvel asset ni manifeste d’images additionnelles n’est à intégrer. Ne pas supprimer globalement l’asset p797 : le patch retire seulement son rattachement à Q5 ; les documents source restent conservés.

## Fichiers et intégrité

- `reviews.json` : résultat complet, prêt à être intégré après validation des 10 patches par le root.
- `review.md` : présent rapport.
- `qa/` : rendus de contrôle intermédiaires, à ne pas embarquer dans le site.

SHA-256 de l’entrée : `30cd69944a54cef87c1e2bda8898287da64fbe31e8745807c5b1b1bacb9439a9`.
SHA-256 de reviews.json : `a1605ac90740f08db9119b8fcd51edf05f86204b3ba4dc0032ede9ea2c67441e`.
