from pathlib import Path
import copy, hashlib, json, shutil

ROOT=Path(__file__).resolve().parent
SITE=ROOT.parents[1]/'output/site'
OUT=SITE.parent
DATA=json.loads((ROOT/'current_exams.json').read_text())
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
BANKS=['histo.te1','histo.te2','histo.tc1','histo.tc2','histo.tc3','histo.tn1','histo.tn2','histo.tn3','histo.autotech']

def dump(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def href(ref):return ref.get('href','')

def main():
    audit=SITE/'audit/histologie_v5'
    for folder in ['te_tech','tc','tn','quality','runtime_checks']:
        dest=audit/folder;dest.mkdir(parents=True,exist_ok=True)
        for f in (ROOT/folder).iterdir():
            if f.is_file() and f.suffix in ['.json','.csv','.md','.py','.cjs']:
                shutil.copy2(f,dest/f.name)
    production=audit/'production';production.mkdir(exist_ok=True)
    for name in ['root_review.py','build_site.py','render_sources.py','source_copies.js','source_copies.css','check_browser.cjs','finish_reports.py','package_site.py','baseline_exams.json','build_summary.json']:
        shutil.copy2(ROOT/name,production/name)
    shutil.copy2(ROOT/'baseline_site/index.html',production/'baseline_v4_index.html')
    dump(audit/'browser_check.json',{'status':'BLOCKED','reason':'Chromium ne peut pas démarrer dans cet environnement : socket() failed, Operation not permitted. Aucun contrôle de pixels ou de mise en page dans un navigateur n’est revendiqué.','functionalVerification':'Voir runtime_checks/runtime_report.json : JavaScript réel, notation, profils et HTML généré.','sourceVisualVerification':'Voir quality/visual_review.json : les 56 pages originales ont été inspectées.'})
    notes=[(b,q,n) for b in BANKS for q in DATA[b]['questions'] for n in q.get('reviewNotes',[])]
    total_notes=sum(len(q.get('reviewNotes',[])) for e in DATA.values() for q in e['questions'])
    total_flagged=sum(bool(q.get('reviewNotes')) for e in DATA.values() for q in e['questions'])
    rows='\n'.join(f"| {DATA[b]['label']} | {len(DATA[b]['questions'])} | {sum(len(q['options']) for q in DATA[b]['questions'])} |" for b in BANKS)
    report=f'''# Vérification des autotests d’histologie — V5

22 novembre 2026. **128 QCM, 649 items, neuf séries vérifiés systématiquement.** Ce rapport contient des clés et des détails de correction.

La version complète du site comporte maintenant **2 806 QCM/fiches dans 217 banques**. Cette révision intervient uniquement dans les neuf banques d’autotests d’histologie et ajoute leurs menus de sources. Les **208 autres banques, soit 2 678 QCM/fiches, sont strictement identiques à V4**. Leurs données, leurs anciennes sources et leurs anciens fichiers d’audit sont conservés.

## Utilisation

Décompresser l’archive complète puis ouvrir `index.html`. Garder `static/` et `sources/` dans le même dossier. Pour retrouver la progression, employer le même navigateur et remplacer les fichiers au même emplacement, avec le même nom `index.html`. Les sauvegardes restent dans le navigateur : elles ne sont pas transportées par le ZIP.

Chaque QCM d’histologie possède deux menus discrets, repliés par défaut :

- **Voir le sujet original** : accessible pendant la réponse ; capture complète de la consigne, des items et des figures associées.
- **Voir le corrigé original** : accessible dans le panneau de correction, seulement après correction de ce QCM.

Le nom du fichier, le numéro imprimé et les pages sont indiqués en petit. Cliquer sur une capture ouvre l’image en grand. Le PDF complet est accessible depuis le menu ; le Word non modifié est également téléchargeable pour les huit paires DOCX. Les QCM répartis sur deux pages disposent de plusieurs captures dans le même menu. La pagination des Word correspond à la conversion PDF livrée.

Les copies des sujets et les copies des corrigés sont produites à partir des documents respectifs. Les images de corrigé ne servent pas d’énoncé. Le texte interactif sépare la proposition, le verdict et sa justification.

## Couverture exhaustive

| Série | QCM vérifiés | Items vérifiés |
|---|---:|---:|
{rows}
| **Total** | **128** | **649** |

Les 16 documents Word du nouvel envoi ont été confrontés aux 16 documents correspondants du premier envoi. Le contenu pédagogique et les images concordent pour les 16 couples ; 15 sont identiques octet par octet. Le corrigé TN3 diffère seulement dans sa structure Word, notamment un signet déplacé, sans différence de texte, de verdict ou d’image. Les deux PDF de techniques histologiques ont été récupérés dans la première archive fournie.

## Réparations confirmées par les originaux

| Série / question | Résultat |
|---|---|
| **TE2, QCM 11** | Clé **ABD** récupérée depuis les mentions courtes V/F. Le détail « FI » de C est explicité comme « filaments intermédiaires ». |
| **TC3, QCM 17** | Les cinq propositions sont explicitement fausses. Le QCM est maintenant noté avec la réponse volontaire **Aucune proposition** ; une absence de réponse reste distincte. |
| **Techniques, question source 8** | QCM absent réintégré sous l’identifiant stable **12**, clé **ABDE**. Les cinq textes sont alignés ; le lettrage répété du sujet est expliqué dans la correction. |
| **Techniques, question source 16** | QCM absent réintégré sous l’identifiant **13**, avec ses lettres originales **F–J** et la clé **GIJ**. |
| **TE2, QCM 9 B** | Le sujet s’interrompt après « Elle est constitutivement ». Le mot « ouverte » est rétabli à partir de l’énoncé complet du corrigé ; une note expose cette restitution. |
| **TC1, QCM 11 A–B** | Le symbole **α**, perdu lors de l’importation, est rétabli. |
| **TC1, QCM 11 E** | Le détail « visible en MET » est conservé dans la correction. |
| **TC3, QCM 9** | L’avertissement sur l’ossification est conservé dans l’explication générale, après correction. |
| **TN2, QCM 7** | Les cinq événements restent dans le contexte, et les cinq permutations restent les réponses. L’avertissement historique de correction introuvable est retiré ; la clé E était déjà correcte. |

Chaque détail de correction commence par **Vrai.** ou **Faux.**, suivi de l’explication du document lorsqu’elle existe. Une réponse sans justification dans le document ne reçoit pas une explication inventée.

Parmi les 649 verdicts, **645 portent une mention littérale dans les corrigés**. Les quatre autres sont les permutations A–D de TN2 Q7 : le sujet demande un ordre unique et seul E est marqué Vrai. Leur exclusion est donc expliquée comme la conséquence de l’ordre retenu, et non comme une annotation présente dans le document.

Les trous de numérotation des originaux ont été respectés : TE1 saute le numéro 5, TC1 saute le numéro 12 ; TC3 Q12 comporte réellement seulement trois propositions. Aucun item supplémentaire n’a été inventé. Les identifiants antérieurs utilisés pour la progression sont conservés ; le numéro source peut donc différer du numéro affiché sur la carte.

## Différences entre sujets et corrigés

Les variations ont été examinées individuellement. En particulier, TE2 Q6 D ne comporte aucune valeur numérique dans le sujet ; le corrigé ajoute 10/20 nm puis le rejette. Le site conserve le texte du sujet, affiche le verdict du corrigé et explique cette différence dans une réserve. Pour TE2 Q17, la capture du corrigé précise la correspondance A–E du sujet avec F–J du corrigé.

Les clés officielles ne sont pas remplacées à cause d’un désaccord scientifique. Une réserve distincte précise l’item, la difficulté et le passage de ronéo à revoir. Cette version comporte **{len(notes)} remarques dans les neuf séries d’histologie**. Elles incluent les réserves V4 conservées et les précisions ajoutées lors de cette vérification.

## Vérification indépendante et technique

Un agent distinct de ceux ayant préparé les séries a relu **chacun des 128 QCM**, comparé les 649 items et tous les détails de correction avec sa propre lecture des sources. Il a aussi contrôlé les 128 consignes, les contextes, les figures et les coupures de page.

- **56 pages originales** relues visuellement : 50 pages issues des Word et six pages PDF de techniques.
- **283 captures** réparties dans 256 menus sujet/corrigé.
- **1 298 comparaisons intégrales** d’items avec leurs captures : 649 sujets et 649 corrigés, toutes réussies.
- Tous les titres et contextes se trouvent dans leurs cadrages ; aucun titre du QCM suivant ne déborde.
- Les neuf objets image présents dans les extraits sont intégralement cadrés.
- **640 états de cartes** contrôlés avec le JavaScript réel du site : sujet avant correction, corrigé après correction, et corrigé caché pour les QCM laissés vides en mode sélectif.
- Les 128 QCM obtiennent 10/10 avec leur clé ; chacune des neuf séries obtient 20/20 dans les deux profils.
- Les réponses différentes des deux profils sont sauvegardées et restaurées sans mélange, y compris la réponse ∅ et les choix F–J.
- **3 208 anciens fichiers** de sources, images et audits sont conservés à l’identique, dont les 172 anciens fichiers d’audit.

Le navigateur Chromium n’a pas pu démarrer dans cet environnement. Les tests techniques exécutent le JavaScript réel dans l’adaptateur DOM et vérifient le HTML produit ; ils ne constituent pas une validation visuelle de la mise en page sur ordinateur ou téléphone. Le contrôle visuel porte bien sur les documents originaux et leurs cadrages.

La relecture établit la fidélité aux sources et documente les ambiguïtés repérées. Elle ne certifie pas que toutes les affirmations des documents d’enseignement ont été confirmées par une revue exhaustive de la littérature scientifique.

## Registre des réserves dans les neuf séries

Les numéros ci-dessous sont ceux des cartes du site. Chaque commentaire figure uniquement après correction.

'''
    for b,q,n in notes:
        report+=f"### {DATA[b]['label']} — QCM {q['id']}"+(f" — item(s) {', '.join(n['items'])}" if n.get('items') else '')+'\n\n'
        report+=n['text']+'\n\n'
        refs=[]
        for ref in n.get('refs',[]):
            label=ref.get('label') or ref.get('file') or 'Source'
            if ref.get('page'):label+=f" · p. {ref['page']}"
            refs.append(f"[{label}]({href(ref)})" if href(ref) else label)
        if refs:report+='Sources : '+' ; '.join(refs)+'.\n\n'
    report+='''## Fichiers de contrôle livrés

- `audit/histologie_v5/quality/review.md` : seconde relecture indépendante et registre des 128 QCM avec clés et pages.
- `audit/histologie_v5/quality/coverage.json` et `coverage.csv` : grille exhaustive des 649 items.
- `audit/histologie_v5/comparaison_items.json` : comparaison des textes du sujet et du corrigé, verdicts littéraux et détails.
- `audit/histologie_v5/modifications.json` : changements par question, incluant les deux ajouts.
- `audit/histologie_v5/captures.json` et `quality/crop_audit.json` : origine et contrôle des captures.
- `audit/histologie_v5/documents_sources.json` : inventaire des originaux récents et anciens, avec leurs empreintes.
- `audit/histologie_v5/runtime_checks/` : script, résultats de notation, profils et conservation des autres banques.
- `sources/histo_v5/` : documents non modifiés, versions PDF utilisées pour les captures et premières versions Word.

Les rapports V4 restent des bilans historiques de cette version ; les résultats spécifiques de la présente révision sont dans ce rapport et `audit/histologie_v5/`. Le manifeste actuel est `audit/histologie_v5/fichiers_sha256.json` ; les manifestes antérieurs décrivent les versions antérieures.
'''
    independent=(ROOT/'quality/review.md').read_text()
    report+='\n'+independent[independent.index('## Registre de tous les QCM relus'):]
    (SITE/'VERIFICATION_HISTOLOGIE_V5.md').write_text(report)
    standalone=report+'\nLes liens relatifs vers les documents sources fonctionnent depuis la copie de ce rapport placée dans l’archive décompressée, à côté du dossier `sources/`.\n'
    (OUT/'Verification_autotests_histologie_v5.md').write_text(standalone)
    old_readme=(ROOT/'baseline_site/README.md').read_text()
    archive=audit/'documents_v4';archive.mkdir(exist_ok=True)
    for name in ['README.md','LIRE_DABORD.md','MAINTENANCE.md','CONTROLE_ANNALES.md','POINTS_A_VERIFIER.md']:
        shutil.copy2(ROOT/'baseline_site'/name,archive/name)
    intro='''# Site de révision PASS — V5

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
'''
    (SITE/'README.md').write_text(intro)
    (SITE/'LIRE_DABORD.md').write_text(intro)
    maintenance='''# Maintenance — état V5, 22 novembre 2026

## Contrat de la présente révision

État : **2 806 QCM/fiches, 217 banques**. Les neuf banques `histo.te1`, `histo.te2`, `histo.tc1`, `histo.tc2`, `histo.tc3`, `histo.tn1`, `histo.tn2`, `histo.tn3`, `histo.autotech` contiennent 128 QCM et 649 items vérifiés. Les 208 autres banques sont identiques à V4. Les anciens IDs, les clés de stockage, les profils, le barème et les anciennes sources sont conservés. Les deux ajouts utilisent les IDs libres 12 et 13 de `histo.autotech`, correspondant aux numéros source 8 et 16. Ne pas confondre ordre du document, ID de progression et numéro source.

## Sources visibles à la demande

Chaque QCM ciblé porte `sourceCopies.subject` et `sourceCopies.correction`, avec `file`, `original`, `pdf`, `converted`, `captures:[{src,page}]` et éventuellement `note`. Les images exactes sont dans `static/histo_v5/`, les Word originaux et les PDF de conversion dans `sources/histo_v5/`. Les anciens Word figurent aussi sous les noms `*_premier_envoi.docx`. Les documents sont non modifiés ; la pagination des Word est celle du PDF livré.

`histoSourceCopy(q, role)` produit un menu replié. Le rôle correction est refusé si `isCorrected(q)` est faux. La copie du sujet est placée après les choix, celle du corrigé à l’intérieur du panneau de correction. Les anciennes copies `originalImages` / `correctionImage` sont masquées uniquement si la nouvelle paire complète `sourceCopies` existe, afin d’éviter les doublons. Les figures ordinaires `images` restent visibles dans l’énoncé. Le CSS `.histo-source-copy` est limité à ces menus.

## Fidélité des données et cas particuliers

Chaque `explanations[lettre]` comporte un verdict explicite puis le détail intégral de la source. Le texte du sujet est conservé ; une restitution d’énoncé doit être prouvée et signalée (TE2 Q9B). TE2 Q11 a la clé ABD. TC3 Q17 a `answer:''`, `answerIsEmpty:true`, `allowNoAnswer:true`. Autotech ID13 garde les choix F–J avec GIJ. TN2 Q7 est une question d’ordre unique, avec cinq événements dans `context`, cinq permutations et la clé E. Pour TE2 Q17, le menu du corrigé explique A–E ↔ F–J.

Les commentaires scientifiques restent après correction et ne remplacent pas les clés officielles. Une divergence entre sujet et corrigé doit être identifiée comme telle, par exemple la valeur ajoutée dans TE2 Q6D. Les trois composants texte d’item / verdict / explication ne doivent jamais être fusionnés.

## Audit et réutilisation

`audit/histologie_v5/quality/coverage.json` couvre les 649 items et les 128 questions. `captures.json` donne les rectangles en points PDF et les pages en base 1 ; la conversion est faite à 144 dpi. `runtime_checks` vérifie les fonctions réelles et les deux profils avec l’adaptateur DOM. Le navigateur local n’a pas pu démarrer : aucun test graphique réel n’est revendiqué.

Les scripts de production et la base HTML V4 sont conservés dans `audit/histologie_v5/production/`. Ils décrivent les chemins de l’espace de production d’origine. Avant une réexécution ailleurs, adapter ces chemins et résoudre les fichiers via `documents_sources.json` ; ne pas lancer un constructeur ancien qui écraserait V5. Les PDF nécessaires aux captures et les données relues par série sont tous dans l’archive. Les règles de migration et de notation V4 ci-dessous restent applicables.

---

## Référence historique V4

'''+(ROOT/'baseline_site/MAINTENANCE.md').read_text()
    (SITE/'MAINTENANCE.md').write_text(maintenance)
    for name in ['CONTROLE_ANNALES.md','POINTS_A_VERIFIER.md']:
        history=(ROOT/'baseline_site'/name).read_text()
        preamble=f'''# Mise à jour V5 — autotests d’histologie

La révision actuelle comprend 2 806 QCM/fiches. Pour les neuf autotests d’histologie, consulter [VERIFICATION_HISTOLOGIE_V5.md](VERIFICATION_HISTOLOGIE_V5.md) : 128 QCM, 649 items et leurs copies originales. Le registre actuel contient {total_notes} remarques sur {total_flagged} questions, dont 23 remarques dans les neuf séries ciblées.

Le texte ci-dessous conserve le bilan V4. Les corrections et réserves propres aux autotests d’histologie sont actualisées dans le rapport V5 ; les autres banques restent inchangées.

---

'''
        (SITE/name).write_text(preamble+history)
    contract={'scope':BANKS,'questions':128,'items':649,'unchangedOtherBanks':208,'currentAllSiteQuestionCount':2806,'baseline':{'version':4,'zipSHA256':'c1699c28c029f7b8002152f19d1524a4c29a6d22146f1dd84eb08d20b18cdfcf'},'preserve':['existing progress IDs','both profiles','non-histology banks','histology annales','original documents','official grading keys when only scientific disagreement'],'coreRule':'Subject statements and screenshots before grading; correction details, screenshot and caveats only after isCorrected(q).'}
    dump(audit/'contrat_revision.json',contract)
    print(json.dumps({'report':str(OUT/'Verification_autotests_histologie_v5.md'),'histoNotes':len(notes),'allNotes':total_notes,'allFlaggedQuestions':total_flagged},ensure_ascii=False))

if __name__=='__main__':main()
