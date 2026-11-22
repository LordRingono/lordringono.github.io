# Site de révision PASS — V5

Version du 22 novembre 2026. **2 806 QCM/fiches, 217 banques.** Les neuf autotests d’histologie ont été vérifiés intégralement : **128 QCM / 649 items**, avec une relecture indépendante et les copies du sujet et du corrigé pour chaque QCM.

## Ouvrir le site

1. Décompresser toute l’archive.
2. Ouvrir `index.html` dans le navigateur.
3. Conserver `static/` et `sources/` à côté.

Le site fonctionne localement, sans compte ni serveur.

## Nouveautés histologie

Les menus **Voir le sujet original** et **Voir le corrigé original** sont repliés par défaut. Le corrigé original n’apparaît qu’après correction du QCM. Les captures incluent les reprises sur la page suivante, les figures et les items. Les liens donnent accès au PDF complet et au Word non modifié lorsque le sujet était fourni en Word.

Deux QCM de techniques histologiques manquants sont rétablis. Les mentions V/F de TE2 Q11 et le cas tout-faux de TC3 Q17 sont reconnus correctement. Les explications sont reprises item par item et les ambiguïtés sont signalées dans la correction. Voir [VERIFICATION_HISTOLOGIE_V5.md](VERIFICATION_HISTOLOGIE_V5.md).

Les 208 banques hors de ces neuf autotests sont inchangées. Les annales d’histologie et la pharmacologie gardent leur organisation V4 ; les 336 QCM de pharmacologie restent regroupés en quinze thèmes. Aucun sujet absent des documents n’est inventé.

## Progression et profils

- Interrupteur activé : profil 1, correction des seuls QCM renseignés.
- Interrupteur désactivé : profil 2, progression indépendante et correction globale.
- « Aucune proposition » constitue une réponse volontaire, différente d’un blanc.
- Recommencer ne remet à zéro que la série et le profil courants.

Les identifiants existants sont conservés. Pour retrouver sa progression, utiliser le même navigateur et remplacer le site au même emplacement, en gardant `index.html`. Les réponses sont dans le navigateur, pas dans le ZIP.

## Sources et contrôles

`audit/histologie_v5/` contient la comparaison exhaustive et les tests de cette révision. Son fichier `fichiers_sha256.json` est le manifeste actuel ; les manifestes précédents restent historiques. `audit/revision_v4/` et les rapports historiques conservent le contrôle antérieur de toutes les unités. Les clés du tutorat restent distinctes des remarques scientifiques : les désaccords ne changent pas silencieusement la note officielle. `MAINTENANCE.md` décrit la structure à conserver.
