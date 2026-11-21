# Relecture indépendante des figures UE2 — PACES 2020–2021

## Périmètre et méthode

Contrôle ciblé des QCM 19, 21, 22 et 24, pages **362–364 du PDF compilé**. Comparaison visuelle du rendu intégral des pages et des agrandissements originaux `zoom_362.png`, `zoom_363.png`, `zoom_364.png` avec les WebP livrés. Vérification des champs `stemImages`, `option.image` et `originalImages` de `exams.json`, ainsi que de leur provenance dans `assets_manifest.json`.

Les **8 fichiers distincts accessibles avant correction** ont été ouverts. Ils proviennent tous des pages du sujet (rôle `subject`), et aucun chemin de corrigé n'est utilisé dans ces champs. Aucun fichier UE2 n'a été modifié par le relecteur.

## Résultats par figure

| QCM | Source | Vérification des éléments imprimés nécessaires | Vérification des annotations |
| --- | --- | --- | --- |
| 19 | p. 362 | Squelette du glycérol, trois esters, toutes les chaînes, doubles liaisons, groupes CH₂/CH₃ et indices 14/7 conservés. Le deuxième triglycéride de l'item E et sa phrase introductive sont également présents. | Identifications manuscrites retirées : « palmitique », « oléique », indications C18:1. Aucune identification manuscrite lisible ne subsiste dans la figure ni dans l'extrait complet. |
| 21 et 22 | p. 363 | Consigne commune intégrale, structures A et B, cadres pointillés, liaison osidique, tous les OH, CH₂OH, CH₂, H, N, CO et indices 12/22 conservés. Les cinq propositions de chaque QCM correspondent au sujet. | Mention manuscrite « glc » sous le cycle retirée. Aucun indice de réponse manuscrit visible dans la figure partagée ni dans les extraits complets. |
| 24 | p. 364 | Quatre cycles, numéros cerclés 1 à 4, liaisons et orientations des substituants, OH et CH₂OH intégralement conservés. Consigne et cinq propositions présentes. | Les quatre identifications manuscrites des hexoses sont retirées. Le minuscule fragment près du numéro 2 signalé pendant la relecture a également été retiré ; la figure et l'extrait complet régénérés ont été revérifiés visuellement. |

### Cas particulier du cliché Q19 : fragment de légende imprimée

Tout en bas du cliché original de la p. 362, une légende **imprimée**, déjà tronquée par le cadrage de la photographie source, laisse lire une identification se terminant par « …2,3-dioléoyl-sn-glycérol ». Le masquage de la bande inférieure écarte également ce fragment. Il ne s'agit donc pas uniquement d'une suppression d'écriture manuscrite.

Cette exclusion a été explicitement signalée au responsable d'intégration, qui l'a confirmée : la légende nominative révèle une identification, tandis que la totalité des structures nécessaires à la résolution demeure visible. Aucun atome ni aucune liaison n'est reconstitué ou retouché. Le PDF source original est conservé. La distinction entre légende imprimée partielle et annotations manuscrites doit apparaître dans le manifeste et l'audit UE2.

## Fichiers avant correction vérifiés

Tous les chemins ci-dessous sont relatifs au dossier des ressources UE2 `assets/` ; le JSON utilise le préfixe `static/`.

| Page | Fichier | Usage |
| --- | --- | --- |
| 362 | `annales_ue2_362_40e72948b4.webp` | Q19 : figure visible avec la consigne |
| 362 | `annales_ue2_362_2ae3badde1.webp` | Q19 : extrait complet du sujet |
| 362 | `annales_ue2_362_4effd471d5.webp` | Q19 : texte et figure de la proposition E |
| 363 | `annales_ue2_363_62671178c8.webp` | Q21/Q22 : consigne et figure communes, également reprises dans les extraits source |
| 363 | `annales_ue2_363_8c773c9881.webp` | Q21 : consigne locale et propositions |
| 363 | `annales_ue2_363_6108e5e84d.webp` | Q22 : consigne locale et propositions |
| 364 | `annales_ue2_364_39b487b29d.webp` | Q24 : consigne et quatre structures, version finale |
| 364 | `annales_ue2_364_9ebc7c1b4f.webp` | Q24 : extrait complet du sujet, version finale |

## Points remontés pendant la relecture

1. **Q24 p. 364, petit résidu manuscrit** sous et à droite du numéro 2 cerclé, vers les pixels x416–425 / y82–95 des WebP. Il ne permet pas de reconstituer une réponse, mais a été signalé pour retrait dans les deux images concernées. Capture de contrôle : `review/ue2_residue_q24_number2.png`.
2. **Q19 p. 362, provenance du masquage** : documenter distinctement la légende imprimée partielle d'identification retirée, en plus des annotations manuscrites. Capture de contrôle du PDF : `review/ue2_q19_caption_before.png`.
3. **Q21 p. 383, fin de correction textuelle** : `explanations.C` s'arrêtait à « β- », alors que le PDF poursuit sur la ligne suivante « D-glucose. ». Signalé à l'auteur UE2 pour compléter cette fin de phrase exactement d'après le corrigé. Ce point ne concerne pas le sujet visible avant correction.

## Contrôle final après régénération

Les trois points remontés sont résolus et ont été contrôlés après régénération :

- **Q24** : les deux nouveaux WebP ont été ouverts. Le fragment manuscrit près du 2 a disparu. Aucun trait du numéro, atome, substituant, liaison ou texte imprimé du problème n'a été supprimé avec lui.
- **Q19** : les entrées `review` du manifeste distinguent désormais les identifications manuscrites de la légende d'identification imprimée déjà tronquée. La structure chimique demeure intacte.
- **Q21** : la correction C du JSON se termine maintenant exactement par « il s'agit donc du β-D-glucose. » ; la fin de ligne du PDF p. 383 est restaurée.

**Conclusion du contrôle ciblé : aucune omission de donnée nécessaire ni annotation manuscrite de réponse visible dans les figures et extraits source des quatre QCM examinés.** La seule suppression de texte imprimé est la légende nominative partielle de Q19, explicitement documentée et confirmée par le responsable d'intégration.

Version de `exams.json` contrôlée en fin de relecture, SHA-256 : `ffa634ba264cd54f9bde4fda9953d84b1deaaf07bb477bf78bc820b785c499f4`.

