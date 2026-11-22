# Contrelecture indépendante — cinq ajouts TC/TN de juin 2024 S2

Les 25 propositions et leurs verdicts ont été relus dans les PDF d’origine, puis recoupés avec les cours locaux. Aucun fichier de données de l’agent UE5 n’a été modifié.

## Clés et appariement

| Ajout | QCM d’origine | Sujet | Correction | Verdicts A/B/C/D/E | Clé |
|---|---|---|---|---|---|
| histo.ann.tc 57 | QRM11 — tissu conjonctif | TC p11 | TC corrigé p13 | F/V/F/V/V | BDE |
| histo.ann.tc 58 | QRM12 — cartilage | TC p12 | TC corrigé p13 | F/V/F/F/F | B |
| histo.ann.tc 59 | QRM13 — os | TC p12 | TC corrigé p13 | V/V/V/F/F | ABC |
| histo.ann.tn 65 | Question16 — nerfs | TN p18 | TN corrigé p19 | V/F/V/F/F | AC |
| histo.ann.tn 66 | Question17 — LCS | TN p18 | TN corrigé p19 | F/V/V/V/F | BCD |

Fichiers sources : *annales TISSU CONJONCTIF 2020 2025.pdf*, *annales TISSU CONJONCTIF 2020 2025 CORRECTION-2.pdf*, *annales TISSU NERVEUX 2018 2025.pdf* et *annales TISSU NERVEUX 2018 2025 CORRECTION.pdf*.

## Deux conflits directement étayés

### TC58 E — production de MEC par les chondrocytes

Le sujet imprime **« pondrocytes »**, alors que le corrigé reprend **« chondrocytes »**. Cette différence de source doit être documentée séparément ; le texte du sujet ne doit pas être corrigé silencieusement.

La contestation scientifique porte sur l’interprétation explicite du corrigé, qui affirme que les chondrocytes ne produisent pas la MEC et la renouvellent seulement. **TC2_2026.pdf p14** précise qu’un chondrocyte synthétise les fibres de collagène II et la substance fondamentale, et assure la production et le maintien de la MEC. Les pp13 et18 confirment respectivement la fabrication et la synthèse/renouvellement. La distinction production contre renouvellement utilisée pour refuser E n’est donc pas compatible avec cette ronéo.

Qualification recommandée : **roneo_conflict**, avec mention que la correction vise bien les chondrocytes. La clé source B reste conservée.

### TC59 C — majorité de collagène I

L’item parle de la **MEC entière** du tissu osseux. **TC3 2026.pdf p3** distingue 30 % de composante organique et 70 % de composante minérale. La p4 situe la prédominance du collagène I dans la composante organique. Dire qu’il domine cette fraction est compatible avec le cours ; dire qu’il compose majoritairement toute la MEC ne l’est pas selon le décompte du cours.

Qualification recommandée : **roneo_conflict**, en formulant précisément le problème de périmètre du pourcentage. La clé source ABC reste conservée.

## Une réserve de formulation

### TC58 C — MEC « solide et élastique »

Le corrigé répond faux car elle n’est « pas toujours élastique ». **TC2_2026.pdf p13** décrit une MEC solide, « plus ou moins élastique selon le type de cartilage ». Ce passage justifie de signaler la différence de formulation, mais ne permet pas à lui seul d’attribuer une élasticité identique à tous les types de cartilage ou de certifier une inversion du verdict.

Qualification recommandée : **possible_error**, sans présenter l’item comme certainement vrai. Demander la formulation attendue dans le cours/annale d’origine si un arbitrage est nécessaire.

## Points ne justifiant pas de nouvelle annotation

- **TC57** : les cinq verdicts suivent les cours. TC1 corrigé pp2–3 décrit les cellules dispersées ; p5 les macrophages/histiocytes ; p11 le collagène I ; p15 les fibres élastiques à 90 % d’élastine. TC2 p4 classe le tissu adipeux parmi les tissus conjonctifs lâches.
- **TC58 A/B/D** : avascularité, matrice pour la croissance osseuse et prédominance du cartilage hyalin sont compatibles avec TC2 pp13 et16.
- **TC59 A/B/D/E** : réservoir minéral et matrice minéralisée sont décrits par TC3 pp2–3. Les rôles distincts des ostéocytes et ostéoclastes sont exposés pp8–9 ; ces items n’exigent pas une nouvelle réserve dans le cadre du cours.
- **TN65 E** : ne pas créer un conflit de ronéo à partir du remplacement épinèvre/paranèvre. **TN1 - Ronéo 2026 - ACTUALISEE.pdf p11** décrit l’épinèvre comme TC dense maintenant les fascicules, mais aussi le paranèvre comme « capsule de TC dense » séparant le nerf de son environnement. Le corrigé suit cette terminologie. La même page confirme A/C vrais, B/D faux.
- **TN66** : **TN3 - Ronéo 2026.pdf pp5–7** décrit les épendymocytes ventriculaires et du canal épendymaire ainsi que la sécrétion par les plexus choroïdes. La p10 décrit la pie-mère et la limitante gliale entre le LCS sous-arachnoïdien et le tissu nerveux. Les cinq verdicts sont cohérents.

Tous les numéros cités sont les pages PDF. Certains documents ont une pagination imprimée différente : par exemple TC2 p14 PDF porte le numéro27 et TN1 p11 PDF porte le numéro10.

## Contrôle final des livrables JSON — gel validé

Après leur rédaction, les six fichiers `{tc,tn}_source_repairs.json`, `{tc,tn}_coverage.json` et `{tc,tn}_notes.json` ont été contrôlés sans modification. Les **25 textes de propositions correspondent exactement aux sujets**, après seule normalisation des espaces. Les cinq clés sont conformes aux verdicts explicites. Les quatre notes TC correspondent aux bonnes lettres et reproduisent les bonnes explications source ; aucune note TN n’a été ajoutée. Les couvertures contiennent trois et deux QCM sans doublon.

Les références utilisées dans les notes à *TC2 2026 - Partie 1 ACTUALISE.pdf* pp13,14,18 ont aussi été ouvertes et vérifiées : elles portent les mêmes passages pertinents que l’autre version TC2 consultée lors de la contrelecture. **Le lot peut être intégré tel quel.**
