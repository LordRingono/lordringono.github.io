# Histologie — vérification indépendante V6

## Décision

**FEU VERT EXPLICITE pour intégrer les fichiers complets `approved_reviewed.json` et `approved_crops.json` de ce répertoire**, avec les cinq limites de notation et la réserve documentaire décrites ci-dessous. Le préparateur et le vérificateur sont deux agents distincts. Cette approbation porte sur 13 banques, **321 QCM et 1 614 propositions**. Aucun QCM ni identifiant supplémentaire n’est créé pendant la vérification.

| Banque | QCM relus | Propositions comparées |
|---|---:|---:|
| histo.ann.te | 29 | 145 |
| histo.ann.tc | 59 | 295 |
| histo.ann.tn | 66 | 330 |
| histo.ann.tech | 39 | 195 |
| histo.te1 | 13 | 65 |
| histo.te2 | 19 | 95 |
| histo.tc1 | 12 | 60 |
| histo.tc2 | 13 | 65 |
| histo.tc3 | 24 | 118 |
| histo.tn1 | 16 | 80 |
| histo.tn2 | 10 | 61 |
| histo.tn3 | 8 | 40 |
| histo.autotech | 13 | 65 |
| **Total** | **321** | **1 614** |

Les **128 autotests V5, soit 649 propositions**, sont inclus dans cette relecture. Leurs captures sont réutilisées après vérification du contenu, des positions et de l’existence des fichiers ; la réutilisation ne signifie pas qu’ils ont été exclus de l’audit. Les 193 annales contiennent 965 propositions après les cinq restitutions du préparateur.

## Travail réellement effectué

Le vérificateur a rouvert les PDF originaux et relu tous les énoncés, toutes les propositions, les marqueurs de correction et les détails explicatifs. Les textes ont été extraits à nouveau depuis les positions des documents, puis confrontés à ceux du site. Les positions de l’audit préparateur servent de localisateurs ; son statut « verified » n’a pas été utilisé comme preuve de conformité.

Les 26 documents principaux et la compilation ont été consultés. La confrontation avec le premier envoi retrouve **25 originaux identiques octet pour octet sur 26**. Pour le Word de correction TN3, le texte visible et les médias sont identiques ; la différence est interne à l’organisation du Word. La trace indépendante se trouve dans `old_source_verification.json`.

La comparaison des éditions porte sur **172 QCM de la même session et 856 propositions thématiques disponibles**, relues intégralement en regard de la compilation, avec la consigne, le contexte, la grille et les détails. Les en-têtes de session et les lignes de clés ont été retrouvés directement dans les PDF. Les différences textuelles ont été relues, y compris les versions à quatre propositions. Les 21 QCM sans correspondance de même session confirmée n’ont pas reçu de clé par analogie. La trace est dans `edition_verification.json`.

Les **321 paires** de copies ont un contrôle textuel et géométrique exhaustif : les positions des éléments attendus sont contenues dans les panneaux, avec les continuations de page. Les sept différences de normalisation sont expliquées item par item dans `coverage.json` : TC31 D, TC33 A, TN45 C, Techniques8 B, TE2 Q9 B et TC1 Q11 A/B. Le sujet propre de TN30 omet uniquement la mention « (1 point) » présente dans la version thématique.

Le contrôle visuel direct comprend **39 pages sources contrôlées pour les figures et limites de questions**, **les 21 figures interactives authentiques**, **14 paires de captures critiques** et, en plus, le corrigé TN7 pour sa rature. Les paires critiques sont Techniques annales Q1/5/6/7, TC annales Q5/10/42, TN annales Q22/30/45/63, TE2 Q17, TN2 Q7 et autotest Techniques Q12. Les montages de contrôle sont issus de nouveaux rendus des sources dans `fresh/`. Les autres paires ne sont pas annoncées comme vues une à une : leur contrôle est documentaire et géométrique.

## Clés, détails et réparations confirmés

Aucune clé supplémentaire n’a été réécrite par le vérificateur. Les réparations du préparateur sont confirmées : D distinct de C pour TC5 et clé ACD ; A manquant de TC42 confirmé Vrai par les cinq propositions et la grille ABE de la compilation p. 1078 ; A manquant de TN63 confirmé Faux avec CD p. 1026 ; restauration des cinq propositions des Techniques Q1/5/6/7, avec remappages documentés. Techniques Q5 est bien BCD après restitution de D.

Les questions demandant l’affirmation **inexacte**, notamment TN6 et TN9, conservent leur polarité négative. Les lettres F ne sont pas confondues avec « Faux » : TE2 Q17 a des lettres F–J dans le corrigé qui correspondent à A–E du sujet ; TN2 contient aussi des propositions F. TN2 Q7 est une question sur l’ordre des événements, dont seule la séquence E porte Vrai. L’autotest Techniques Q12 possède une numérotation fautive dans le sujet, résolue par comparaison des cinq énoncés complets. TC3 Q17 conserve son véritable cas « toutes les propositions fausses », avec les drapeaux prévus.

La séparation des items et des questions voisines est confirmée, notamment TC5, TC40–43 et Techniques26–27. Les sujets propres de TN30 et TN45 viennent de la compilation ; les versions thématiques portant déjà « Faux » restent accessibles après correction. Les figures et contextes ne sont pas fusionnés entre éditions : TE11 a un autre triptyque dans la compilation, et Techniques10 un autre contexte expérimental. Les copies de Techniques30 couvrent bien la figure et la consigne p. 11, les items p. 12, puis le corrigé p. 14–15.

## Modifications apportées pendant la vérification

- **477 libellés de panneaux** sont remplacés par les véritables noms de fichiers. Les pages, rectangles et numéros sources sont conservés.
- **20 menus de corrigé** sont réordonnés afin que le document principal soit réellement le corrigé : TN annales **Q1 à Q13** ; Techniques annales **Q5 à Q10 et Q21**. Les contextes repris du sujet apparaissent ensuite avec une note explicite. Le détail est dans `copy_order_changes.json`.
- Les quatre remarques des Techniques Q1/5/6/7 sont alignées sur la migration décidée par l’intégrateur : **les choix sont conservés et remappés ; seule la validation du QCM est retirée dans les deux profils**. Les libellés de clés anciennes dans deux remarques secondaires sont clarifiés. Les 59 notes antérieures V4/V5 sont conservées intégralement.
- **Trois réserves sourcées** sont ajoutées uniquement dans la correction : TN3 D, TN7 C et TC42 D, détaillées ci-dessous. Le lot contient désormais 115 notes : 59 anciennes, 53 du préparateur et 3 du vérificateur.

### Réserves scientifiques ajoutées

**TN annales Q3 D — rapport glie/neurones.** Le corrigé et la ronéo TN3 p. 3 reprennent le rapport 10:1. Le comptage original d’Azevedo et al. trouve des nombres globaux voisins de neurones et de cellules non neuronales dans le cerveau humain adulte. La note distingue cellules non neuronales et cellules gliales, ainsi que les régions anatomiques ; elle ne transforme pas D en Vrai. [Publication primaire, PMID 19226510](https://pubmed.ncbi.nlm.nih.gov/19226510/).

**TN annales Q7 C — appareil épineux et rature.** La source p. 4 imprime VRAI, mais barre toute la proposition et le marqueur sans légende. La ronéo TN2 p. 14 décrit la densité postsynaptique, tandis que la reconstruction ultrastructurale de Spacek distingue l’appareil épineux, continu avec le réticulum endoplasmique lisse. La note conserve la clé CE littéralement importée et demande l’erratum de mai 2019 ; elle n’invente pas une clé E à partir d’une rature. [Publication primaire, PMID 3985372](https://pubmed.ncbi.nlm.nih.gov/3985372/).

**TC annales Q42 D — périchondre.** Le détail D de la copie complémentaire de la compilation p. 1078 dit trop largement que le cartilage hyalin n’a pas de périchondre. La ronéo TC2, PDF p. 13 / page imprimée 26, précise cartilage articulaire et fibrocartilage. Cette réserve porte sur le commentaire de la source complémentaire ; la clé ABE est conservée.

## Limites documentaires et notation

Le lot contient **316 QCM notables et cinq QCM hors note** :

| Banque / QCM | Motif documentaire |
|---|---|
| TC annales Q10 | D sans verdict exploitable dans le thématique ; désaccord supplémentaire entre éditions sur E. |
| TN annales Q22 | E contient une contradiction explicite « Faux … on peut dire Vrai … ??? » ; compilation ACE contre ancien AC. |
| Techniques annales Q1 | Cinq propositions restaurées ; opposition des éditions sur E. |
| Techniques annales Q6 | Cinq propositions restaurées ; A Faux dans le thématique, A Vrai dans la compilation. Aucun cas « tous faux » n’est inventé. |
| Techniques annales Q7 | Oppositions sur A et D ; E hors programme dans la compilation. Aucune clé hybride. |

Ces cinq questions gardent leurs sources et remarques. Un erratum ou la ronéo de leur session est nécessaire pour lever leur statut hors note. TN7 C ajoute une demande de clarification sur la rature et le vocabulaire, sans nouvelle modification de clé. Le schéma de correction TN1 Q13 est déjà rogné à gauche dans son EMF original : aucune légende manquante n’a été fabriquée. Ces demandes et les divergences complémentaires d’édition sont réunies dans `missing.json`.

L’audit vérifie les importations, les appariements et les divergences repérables. Il ne certifie pas que chaque affirmation des documents pédagogiques est scientifiquement infaillible. Une réserve sourcée reste séparée de la clé du tutorat, conformément à la demande.

## Intégration et sauvegardes

Utiliser les deux objets complets approuvés. Les 21 fichiers de `prepare/asset_manifest.json` ont été contrôlés et restent à intégrer. Aucun nouveau manifeste de sources n’est nécessaire. L’ordre des banques et des QCM, leurs identifiants, les textes, options, explications, clés et coefficients sont identiques au lot préparateur approuvé, hormis les remarques et métadonnées décrites ci-dessus.

La migration gérée par l’agent principal concerne **TC5 et Techniques1/5/6/7** : les anciens choix sont conservés, les lettres sont remappées lorsque nécessaire, et seule leur validation est retirée. Les autres réponses et corrections restent enregistrées dans chacun des deux profils, y compris le profil classique jusqu’à la prochaine validation globale. Ne pas suivre la phrase antérieure du rapport préparateur demandant d’effacer les réponses.

## Empreintes finales approuvées

| Fichier | SHA-256 |
|---|---|
| `approved_reviewed.json` | `9f08c421e53b4de17b2e3d812c6db3ca5635bc2b12a0c1ab5cdaf574a8b27f7f` |
| `approved_crops.json` | `3dcc020f087c8a6c41318c0c623288ead709c97eafb0778391991261f72d935e` |

Entrées préparateur vérifiées et inchangées : `reviewed.json` SHA-256 `96011ffc9d44898ada0ad9c759e075525a945c528cdf0b01664e0976fa529d69` ; `crops.json` SHA-256 `1996925b232a018193748ebc0aa2b48ea44da10a31fe7505c80895be2c4b12d9`.

`coverage.json` contient une trace pour chacun des 321 QCM et de leurs 1 614 propositions. `issues.json` distingue les réparations du vérificateur, les réserves ajoutées et les limites documentaires persistantes. `approval.json` récapitule les comptes et les empreintes. Aucun fichier de `output/site` ni d’une autre matière n’a été modifié par ce vérificateur.
