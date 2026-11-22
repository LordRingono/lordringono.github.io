# Contrelecture indépendante — UE4 2023–2024, session 2, Q5

## Conclusion

**Le Q5 a bien pour clé ACE. Le hors-note actuel provient d’un appariement incorrect avec les justifications du Q6.** Il n’existe pas, pour ce QCM, de contradiction entre la grille courte et le verdict détaillé imprimés dans le document.

Contrôle effectué en lecture seule du lot recent et des banques. Aucun fichier du lot recent ni aucun asset n’a été modifié.

## Sources confrontées

- Sujet PDF p790 : Q5 « Concernant les paramètres pharmacocinétiques… » et ses cinq propositions.
- Grille courte p794 : Q5 = **ACE**, Q6 = **AB**.
- Corrigé détaillé p796 : les cinq propositions du Q5 sont reproduites, puis l’encadré porte **ACE** et les verdicts ci-dessous.
- Corrigé détaillé p797 : début du Q6, consacré à la définition d’un effet indésirable grave, puis clé **AB**.

| Item du Q5 | Verdict réellement imprimé p796 | Justification source |
|---|---|---|
| A — biodisponibilité et absorption | VRAI | Pas de justification supplémentaire. |
| B — insuffisance rénale | FAUX | « en cas d’insuffisance hépatique » |
| C — biodisponibilité IV à 100 % | VRAI | Pas de justification supplémentaire. |
| D — Cmax et phase d’absorption | FAUX | « Tmax est un paramètre qui permet d’évaluer l’absorption du médicament (= Temps nécessaire pour atteindre Cmax) » |
| E — modalités d’administration | VRAI | Pas de justification supplémentaire. |

## Portée visuelle des captures existantes

Les trois captures ont été ouvertes et lues intégralement.

| Fichier existant | Contenu observé | Décision |
|---|---|---|
| `static/annales_ue4_2023-2024_s2_q05_original_p790.webp` | Consigne du Q5 et cinq items A–E, sans question voisine ni corrigé. | Conserver. |
| `static/annales_ue4_2023-2024_s2_q05_explanation_p796.webp` | Encadré complet ACE du Q5 ; cinq verdicts, justification hépatique de B et Tmax de D. | Conserver : capture suffisante du corrigé du Q5. |
| `static/annales_ue4_2023-2024_s2_q05_explanation_p797.webp` | Consigne visible « 6. », les cinq critères d’effets indésirables graves et encadré AB. | Retirer des `correctionImages` du Q5 : ce contenu appartient entièrement au Q6. |

Le vecteur de verdicts actuellement stocké pour Q5 — A/B VRAI, C/D/E FAUX — est exactement celui de l’encadré AB du Q6, et non celui du Q5. La première capture du Q5 contient déjà la bonne correction ; la seconde capture introduit indûment le Q6 et explique le faux signal de contradiction.

## Réparation justifiée

- Rétablir `answer: "ACE"`, correspondant à `rawAnswer` et aux deux corrections sources.
- Restituer les cinq explications du Q5 depuis la p796.
- Retirer l’avertissement de divergence créé par cet appariement erroné.
- Limiter `correctionImages` du Q5 à la capture p796.
- Conserver les identifiants, les cinq propositions et la pondération 1.

Cette validation concerne la fidélité de l’appariement sujet/corrigé. Elle n’ajoute aucune clé scientifique reconstruite et ne transforme pas la justification imprimée en une recommandation médicale générale.
