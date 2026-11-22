# Embryologie — première partie finalisée

## Couverture réelle

Les **414 questions existantes** des 17 banques ci-dessous ont été relues avec leurs propositions et explications. Les deux questions supplémentaires proposées viennent du PDF de colle S2 ; elles ont également été lues. Le fichier `coverage.json` contient donc **416 lignes**, dont deux marquées `restoredSourceQuestion`. Les **183 questions S4 et cœur** sont confiées à l’agent UE5 et figurent dans `ue5_assist/` lorsqu’il a fini ; elles ne sont pas déclarées relues dans ce fichier.

La lecture a porté sur 2347 options de la base, y compris les fragments ensuite identifiés comme mal appariés. Après les restaurations matérielles proposées, le périmètre relu représente 2363 propositions sources, incluant les deux QCM restaurés. L’absence de note ne vaut pas certification scientifique.

| Banque | Questions de la base relues | Options de la base lues |
|---|---:|---:|
| embryo.aut.meiose | 15 | 134 |
| embryo.aut.sperm | 7 | 106 |
| embryo.aut.ovo | 19 | 209 |
| embryo.aut.fec | 24 | 161 |
| embryo.ann.gamet | 36 | 180 |
| embryo.col.gamet | 36 | 124 |
| embryo.ann.fec | 21 | 104 |
| embryo.col.fec | 26 | 130 |
| embryo.aut.s1 | 13 | 121 |
| embryo.ann.s1 | 13 | 65 |
| embryo.col.s1 | 18 | 86 |
| embryo.aut.s2 | 10 | 50 |
| embryo.ann.s2 | 14 | 65 |
| embryo.col.s2 | 33 | 154 |
| embryo.aut.s3 | 37 | 205 |
| embryo.ann.s3 | 39 | 195 |
| embryo.col.s3 | 53 | 258 |

## Résultats remis

- **71 notes** localisées sur 66 questions : {'roneo_conflict': 41, 'source_conflict': 15, 'possible_error': 14, 'missing_reference': 1}.
- **51 propositions de réparation matérielle**, sans substitution de clé pour désaccord scientifique.
- **2 QCM entièrement perdus**, **plusieurs propositions perdues**, **4 exercices d’associations mal structurés**, **3 schémas partagés manquant sur la seconde question du groupe**.
- **3 contextes communs** remis dans `shared_contexts.json` pour les couples 25–26, 31–32 et 41–42 de la colle S3.

## Questions et contenu réellement absents ou inaccessibles

1. **Colle S2, QCM source 30 et 33**, p.7 : ils avaient été absorbés dans les justifications des QCM précédents. Ils sont proposés avec les nouveaux IDs 34 et 35 en fin de banque. Les anciens IDs ne changent pas. Le premier comporte cinq items Faux ; le second six items avec clé ABC. Voir `source_additions.json` et la reproduction `render/cs27.png`.
2. **Annales S2, ID13 / source Q7 (2024–2025 S1)**, p.4 : la base ne contenait que les explications C–E, sans énoncé, propositions ni figure. Les cinq propositions, la consigne, la clé AB et le schéma ont été retrouvés sur cette même page. Le schéma était attribué à tort à l’ID12 ; sa réattribution à ID13 est proposée.
3. **Autotest fécondation, ID7 / source Q8**, p.2 : deux propositions portent C. La seconde, explicitement Vrai, a disparu. Restauration sous D libre avec `sourceLabel: C bis (source)`, sans renuméroter A/B/C/E ; clé ABD. Cette intégration a été validée par root.
4. **Annales fécondation, ID4**, p.1 : deux propositions portent A. La seconde a disparu. Restauration sous E libre avec `sourceLabel: A bis (source)` ; clé imprimée ABD conservée dans `rawAnswer`, `answer: null` car l’appariement n’est pas certifiable. La clé ne devient pas une validation des phrases B/D mal lettrées. Cette intégration a été validée par root.
5. **Colle gamétogenèse, IDs20/27/29/34**, pp.3–6 : des listes de cellules/formules avaient été prises pour les choix. Les vraies associations A–E sont remises avec leur contexte. Les verdicts imprimés donnent respectivement aucune / BDE / DE / ADE.
6. **Colle S3, IDs26/32/42** : les schémas communs n’étaient attachés qu’à 25/31/41. Les consignes communes et les figures ont été contrôlées ; chaque question doit être autonome en sélection filtrée.

Des clés explicites sont aussi restaurées lorsqu’elles avaient été perdues. Les clés vides correspondant à des items tous Faux sont distinguées des clés inconnues : `rawAnswer: AUCUNE`. Une telle restauration ne change pas un verdict scientifique du tutorat. Les numéros omis dès le document source, par exemple l’absence de Q3 dans l’autotest de fécondation et certaines lettres supprimées dans les colles, ne sont pas reconstitués artificiellement. L’autotest S1 porte deux Q3 et comporte bien treize QCM, non douze.

## Erreurs de correction à afficher après réponse

Les exemples suivants sont étayés par les cours fournis ; les clés du tutorat sont conservées.

- **Autotest ovogenèse 15 E** : GP1 est N,2C dans la fiche de gamétogenèse pp.8–9 ; la justification écrit NC.
- **Autotest ovogenèse 10 A et colle S1 8 A** : les explications placent la fécondation ou l’embryon J3 dans le pavillon ; le ronéo S1 pp.2–3 et 9–10 indique l’ampoule tubaire.
- **Autotest S3 4 A** : la correction exclut la plaque préchordale de l’induction neurale, alors que le ronéo S3 pp.39–40 la cite avec la chorde.
- **Colle S3 38 A** : « intra-villositaire » et « extra-embryonnaire » ne s’excluent pas. Le mésenchyme extra-embryonnaire forme l’axe de la villosité dans le ronéo pp.5–7 ; le motif du Faux est invalide.
- **Colle S3 50 E** : l’effet de BMP4 est dit dorsalisant dans la justification ; le ronéo pp.29 et 32 explique la migration latérale et ventrale.
- **Autotest S3 37 B et colle S3 34 E** : les supports confondent l’asymétrie droite–gauche physiologique et une anomalie de latéralité. Le ronéo pp.30–31 décrit cette asymétrie normale.

Les contradictions purement internes sont signalées séparément, par exemple annales gamétogenèse 1 B (clé ABD contre mention Faux) et annales S3 20 E (clé ABD contre mention Vrai). Aucune nouvelle clé scientifique n’est calculée pour ces cas.

## Qualité et limites des ronéos

La fiche de gamétogenèse (14 pages), les ronéos S1 (20 pages), S2 (20 pages) et S3 (55 pages) ont été lus intégralement. La fiche Anomalies du génome p.3 a été utilisée pour la distinction translocation équilibrée/déséquilibrée. Le fichier de couverture distingue comparaison thématique, références ciblées et absence de cours spécialisé.

Les ronéos contiennent eux-mêmes des formulations discutables : lyonisation/empreinte, classement de FGF8 parmi TGF-β, localisation de tous les gènes Hox sur le chromosome 3, « 3–4 somites » contre « 3–4 paires » et date de plaque chordale. Ces points portent une **réserve**, pas une certification d’erreur fondée sur une fiche qui répéterait la même confusion. Aucun recours au web n’a servi d’arbitrage.

## Questions restant sans clé entièrement certifiable

- `embryo.ann.gamet` Q27 (source Q1, p. 6).
- `embryo.ann.gamet` Q28 (source Q2, p. 7).
- `embryo.ann.fec` Q4 (source Q6, p. 1).
- `embryo.ann.fec` Q17 (source Q3, p. 4).
- `embryo.ann.fec` Q18 (source Q4, p. 4).
- `embryo.ann.s1` Q9 (source Q5, p. 3).
- `embryo.ann.s1` Q10 (source Q6, p. 3).
- `embryo.ann.s1` Q13 (source Q6, p. 4).
- `embryo.ann.s2` Q9 (source Q7, p. 3).
- `embryo.col.s3` Q11 (source Q11, p. 3).

Ces cas ne sont pas présentés comme faux simplement faute de clé. Pour l’annale S1 ID13, les photographies sont présentes mais la clé ABC(D)E rend D explicitement ambigu ; la fausse mention « figure indisponible » est supprimée.

## Contrôle des livrables

Les propositions proposées ont été relues sans y laisser de verdict Vrai/Faux ni de correction suivante. Le « Vrai » accolé à l’item E d’annales gamétogenèse7 a été retiré. Les figures S1/S2/S3 utilisées ont été inspectées. Tous les changements restent dans ce dossier sous forme de propositions ; la base immuable n’est pas modifiée.
