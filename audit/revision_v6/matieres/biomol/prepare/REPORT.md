# Biologie moléculaire — préparation V6 terminée

## Périmètre et résultat

Les **23 banques UE2 biomol**, soit **550 QCM/fiches et 2 752 propositions**, ont été rapprochées question par question des **46 PDF originaux** de sujets et corrigés. Les 46 exemplaires de `sources_biomol/extracted/` ont été comparés par SHA256 avec l’archive Biomol UE2 initiale récupérée dans `work/site_v6/materialized/biomol_original/` : ils sont tous identiques. Aucun des sujets ou corrigés correspondant aux banques présentes ne manque.

Les sorties sont prêtes pour le vérificateur indépendant. Il s’agit de la préparation, pas de sa validation finale. La comparaison systématique porte sur les textes positionnés, les marqueurs explicites, les clés littérales, les détails et leur correspondance. La relecture visuelle a couvert les 39 panneaux de contextes communs, les anomalies de source, la question ED sous forme d’image et les pages ED à disposition particulière. Elle ne constitue pas une lecture visuelle séparée de chacune des 1 366 futures captures.

## Livrables

- `reviewed.json` : objets complets des questions basés sur V5, exclusivement les 23 banques biomol.
- `audit.json` : 550 rapprochements, avec preuves positionnées par proposition, texte du corrigé, marqueur littéral, détail, verdict et statut. `detailVerification` distingue un détail textuel comparé d’un original graphique joint.
- `crops.json` : **783 panneaux sujet et 583 panneaux correction**, soit **1 366**. Tous les chemins sont absolus, toutes les pages en base 1. Les contextes communs nécessaires sont inclus dans les copies sujet de chaque question concernée.
- `context_crops.json` : 38 contextes distincts, 39 panneaux authentiques.
- `source_manifest.json` : noms originaux, chemins locaux, chemins de destination, SHA256 et nombre de pages des 46 PDF.
- `checks.json` : contrôle des invariants, des limites de page et de la couverture de toutes les preuves textuelles.
- `changes.json`, `notes.json`, `bank_checkpoints.json` : réparations, huit nouvelles réserves documentaires et étapes par banque.
- `missing.json` : aucun PDF de sujet/corrigé absent ; liste précise des sept arbitrages/versions propres encore utiles.
- Les scripts `audit_biomol.py` et `prepare_final.py` conservent la méthode et les exceptions documentées. Le vérificateur doit relire les originaux indépendamment.

## Réparations principales

### Énoncés et contexte commun

1. **Introduction, annales, id 9, E** : retrait de la consigne des deux questions suivantes, qui avait été annexée à l’item. Le sujet contient uniquement « La base1 peut s’apparier avec la base3. » pour E.
2. **Introduction, annales, ids 10 et 11** : restitution du bloc commun sur les trois bases pyrimidiques avec le schéma original pour les deux questions. L’image était absente de la seconde question. Le bloc utilise l’asset authentique déjà présent `static/ue2_ue2_intro_annales_q010_page03_image2.webp`.
3. **Transcription, annales, id 14, E** : retrait de la mention suivante « RAS : (QCM dans la partie traduction car mélangé) », qui ne fait pas partie de l’item.
4. **Transcription, autotest, id 2, D** : le PDF appelé ENONCE contient lui-même le résidu **« Fau »** après la proposition. Il est retiré du texte interactif ; la capture originale n’est pas retouchée. La ligne de `crops.json` comporte **`subjectAfterCorrection: true`** et une explication. Cette copie doit rester inaccessible avant validation.

### Clés et détails

- **546 clés correspondent** aux verdicts imprimés. L’ordre littéral BDC contre BCD est traité comme un même ensemble.
- **Trois clés parenthétiques** demeurent ambiguës et hors note : ADN annales id 25 (`AD (E)`), ARN annales id 26 et Transcription annales id 33 (`AB(C)`). Une réserve cite la page et demande un arbitrage, sans trancher arbitrairement.
- **Une fiche d’association**, Introduction autotest id 10, n’est pas un QCM à cocher ; elle reste hors note avec ses originaux.
- **Aucune clé de notation n’a été changée** par la préparation.
- **634 détails d’items** ont été alignés sur le texte réellement présent dans le corrigé. La plupart éliminent des répétitions d’import, des marqueurs ou fragments ajoutés au détail, ou remplacent une ancienne explication par l’explication exacte. Douze ajoutent les détails textuels réellement imprimés pour quatre questions des ED 2025–2026 ; les solutions graphiques restent accessibles par leurs copies authentiques.
- **18 commentaires généraux** réellement présents dans les corrigés sont rattachés une fois à la question.

`changes.json` conserve chaque avant/après et sa raison ; les comptes ne représentent pas 656 erreurs scientifiques.

### Versions du sujet et du corrigé divergentes

Ces différences ne peuvent être résolues en attribuant silencieusement au sujet le verdict d’une phrase modifiée. Les formulations du sujet et les clés du corrigé sont conservées, avec une remarque après correction :

| Banque et id | Item | Différence documentée |
|---|---|---|
| ADN autotest 13 | C | Sujet « n’est pas autonome » ; corrigé « est autonome », puis Faux. |
| Organisation autotest 9 | E | Sujet facteur VII ; corrigé facteur VIII. |
| Réparation autotest 11 | D | Proposition sur MSH2/MSH6 et les retards de méthylation remplacée par une autre phrase sur le système MMR dans le corrigé. |
| Réparation autotest 15 | C | Sujet arrêté à « ADN pol. » ; α apparaît uniquement dans le corrigé, qui donne Faux. |

Les réserves scientifiques déjà présentes dans V5 et leur clé de notation sont conservées. Les contradictions clé/détail déjà signalées ont été retrouvées notamment dans ADN annales 14, Traduction annales 11, Régulation annales 18, Anomalies annales 1 et ED annales 38. Les nouvelles réserves ne prétendent pas transformer un désaccord de document en conclusion scientifique indépendante.

## Cadrages particuliers et preuves

- ED annales id 2 correspond au QCM imprimé 24, image seule : sujet page 1, corrigé page 2. La comparaison de ses cinq propositions et de la clé B repose sur les pages rendues. L’audit l’identifie explicitement.
- Le sujet ED 2026–2027 place un schéma Normal/muté après Q26 ; ce schéma et sa consigne concernent Q27 et suivantes. La limite de Q26 et le contexte suivant sont traités séparément.
- Les corrigés ED 2025–2026 juxtaposent Q2/Q3 (page 1), Q9/Q10 et Q11/Q12 (page 3). Les séparations horizontales vérifiées sont respectivement x = 218, 350 et 296 points.
- Le corrigé ED 2026–2027 juxtapose Q3/Q4 page 1 : séparation x = 335 points.
- L’audit des détails suit également ces colonnes ; un titre voisin ne doit pas tronquer le commentaire de la question de gauche.
- Les images débordant la largeur de la colonne de texte et les PDF plus larges que l’A4 ont des cadrages élargis aux dimensions du document. Les corrections longues conservent les pages de continuation.
- Les écarts de numéros imprimés, les lettres manquantes ou erronées et la lettre cyrillique В ont été traités uniquement pour établir la correspondance ; les copies reproduisent les originaux sans retouche.

## Contrôles finaux du préparateur

- 550 questions, 2 752 items, 23 banques, aucun identifiant changé.
- Aucun ordre de question ni d’option modifié ; aucun champ de notation modifié.
- Trois textes d’items modifiés, tous listés et justifiés ci-dessus.
- 46/46 empreintes identiques à l’archive initiale fraîchement récupérée.
- **3 192 lignes de preuves sujet, 3 097 lignes de preuves corrigé, 984 lignes de détails** : toutes sont contenues dans au moins un rectangle du bon rôle et de la bonne page.
- Aucun rectangle vide ou hors page, aucune question privée de copie sujet/corrigé.
- Aucun ajout de QCM, notamment aucune annale antérieure à 2015 ajoutée. Les contenus antérieurs déjà présents dans V5 sont préservés conformément au contrat.
- Aucun changement dans `output/site`, dans les profils, le classement ou les autres matières.

## Intégration par l’agent principal

Ajouter les copies en utilisant `crops.json`, conserver la règle `subjectAfterCorrection` et les notes seulement après correction. `source_manifest.json` réutilise les documents déjà empaquetés quand ils existent ; quatre fichiers ont une nouvelle destination sous `sources/biomol_v6/` et doivent être copiés : les deux annales d’introduction, le corrigé d’annales Organisation du génome et le sujet d’autotests Régulation. Les liens des notes pointent vers ces destinations.

La liste `missing.json` ne signifie pas que les 46 sujets/corrigés sont absents : elle distingue la version propre du sujet annoté, les divergences entre deux originaux et les clés parenthétiques nécessitant une réponse officielle. Les passages de ronéo/errata concernés peuvent être demandés en fin de travail. Aucune note nouvelle n’affirme une correction scientifique non sourcée.

## Couverture par banque

| Banque | Questions/fiches | Items |
|---|---:|---:|
| `ue2.intro.autotest` | 11 | 54 |
| `ue2.intro.annales` | 14 | 70 |
| `ue2.adn.autotest` | 14 | 73 |
| `ue2.adn.annales` | 28 | 140 |
| `ue2.arn.autotest` | 19 | 95 |
| `ue2.arn.annales` | 29 | 145 |
| `ue2.organisation.autotest` | 12 | 60 |
| `ue2.organisation.annales` | 12 | 60 |
| `ue2.replication.autotest` | 27 | 135 |
| `ue2.replication.annales` | 22 | 110 |
| `ue2.transcription.autotest` | 35 | 175 |
| `ue2.transcription.annales` | 34 | 170 |
| `ue2.traduction.autotest` | 29 | 148 |
| `ue2.traduction.annales` | 30 | 150 |
| `ue2.regulation.autotest` | 24 | 122 |
| `ue2.regulation.annales` | 23 | 115 |
| `ue2.reparation.autotest` | 20 | 100 |
| `ue2.reparation.annales` | 25 | 120 |
| `ue2.anomalies.autotest` | 7 | 35 |
| `ue2.anomalies.annales` | 9 | 45 |
| `ue2.ed.annales` | 43 | 215 |
| `ue2.ed.2025-2026` | 43 | 215 |
| `ue2.ed.2026-2027` | 40 | 200 |
