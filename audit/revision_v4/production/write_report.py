"""Write current, user-readable documentation from the final reviewed data."""
import json,collections,shutil,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'work/review_v4';S=R/'output/site';A=S/'audit/revision_v4'
def read(path):return json.loads(path.read_text())
E=read(P/'current_exams.json');stats=read(P/'build_stats.json');N=read(A/'annotations.json');C=read(A/'couverture.json');patches=read(A/'reparations.json');adds=read(A/'ajouts.json')
assert not stats['missingCoverage']and not stats['missingReferences']and not stats['unresolvedDecisions']
tests=read(P/'logic_checks.json');content=read(P/'content_checks.json');assert tests['result']=='PASS'and not tests['draft']and not content['missingFiles']
labels={'ue1':'UE1 · SSH','ue2b':'UE2 · Biologie moléculaire','ue2c':'UE2 · Biochimie / chimie physique','ue3':'UE3 · Biostatistiques','ue4':'UE4 · Pharmacologie','ue5h':'UE5 · Histologie','ue5b':'UE5 · Biologie cellulaire','ue5e':'UE5 · Embryologie'}
units=list(dict.fromkeys(e['ue']for e in E.values()))
def unitlabel(u):return labels.get(u,u)
def md(s):return str(s or'').replace('|','\\|').replace('\n',' ')
def banklabel(b):return re.sub('<[^>]+>','',E[b].get('label')or E[b].get('title')or b)
def reftext(ref):
 name=ref.get('label')or ref.get('file')or'Référence';page=' · p. '+str(ref['page'])if ref.get('page')else''
 return f'[{name}{page}]({ref.get("href")or ref.get("url")})'if ref.get('href')or ref.get('url')else name+page
uq={(n['bank'],n['id'])for n in N}
keys_changed={(p['bank'],p['id'])for p in patches if 'answer'in p.get('fields',{})}
false_restored={(p['bank'],p['id'])for p in patches if p.get('fields',{}).get('answerIsEmpty',{}).get('after')is True}
course_questions=sum(c['status']in ['reviewed_with_course','partially_course_checked']for c in C)
reviewed_items=sum(c['itemsReviewedCount']for c in C)
pharma=[q for e in E.values()if e['ue']=='ue4'for q in e['questions']]
pharma_count=collections.Counter((q['year'],q['session'])for q in pharma)
related=sum(len(q.get('relatedThemes',[]))for q in pharma)
paperrows=[('2025-2026','S1',701,710,711,726),('2024-2025','S1',727,734,735,750),('2024-2025','S2',751,756,757,766),('2023-2024','S1',767,774,775,788),('2023-2024','S2',789,792,793,800),('2022-2023','S1',801,808,809,822),('2022-2023','S2',823,828,829,838),('2021-2022','S1',839,846,847,858),('2021-2022','S2',859,864,865,874),('2020-2021','S1',875,882,883,896),('2020-2021','S2',897,902,903,914),('2020-2021','PACES',915,922,923,938),('2019-2020','S1',939,948,949,962),('2018-2019','S1',963,970,971,986)]
assert sum(pharma_count[(y,s)]for y,s,*_ in paperrows)==336
lines=['# Vérification des QCM — révision V4','', '22 novembre 2026','',
 f'Le site contient **{str(stats["questionCount"])} QCM/fiches**, répartis dans **{stats["bankCount"]} banques**. Cette révision rétablit **{len(adds)} questions complètes** présentes dans les documents mais perdues à l’importation, corrige les appariements démontrés par les sources et installe **{len(N)} remarques sur {len(uq)} questions**. Les remarques sont visibles dans la correction uniquement.','',
 '## 1. Pharmacologie : vérification réelle des sujets','',
 'Le PDF de 1 660 pages a été parcouru à nouveau pour inventorier les blocs UE4, indépendamment du total déjà importé. Les 14 sujets fournis contiennent **336 QCM et 1 680 propositions** : 333 ensembles de cinq items textuels et trois QCM dont les propositions sont des repères de figure. Les 13 QCM illustrés ont été inspectés. Aucun QCM numéroté supplémentaire de pharmacologie n’a été retrouvé hors de cet inventaire.','',
 '**Les documents ne couvrent pas toutes les années depuis 2015.** Aucun sujet UE4 de 2015–2016, 2016–2017 ou 2017–2018, ni de session 2 de 2025–2026, n’est présent dans le dossier fourni. Aucun contenu n’a été inventé pour combler ces absences.','',
 '| Année | Session imprimée / type | QCM | Pages du sujet | Pages du corrigé |','|---|---|---:|---:|---:|']
for y,session,a,b,c,d in paperrows:
 display='Non précisée sur la couverture'if y in ['2018-2019','2019-2020']else session
 lines.append(f'| {y.replace("-","–")} | {display} | {pharma_count[(y,session)]} | {a}–{b} | {c}–{d} |')
lines+=['','Les pages sont celles du fichier `sources/Annales_compilation.pdf`, en comptant la première page comme page 1. Les identifiants historiques contenant S1 pour 2018–2019 et 2019–2020 restent conservés pour la progression ; l’interface n’affirme plus une session absente de la couverture.','',
 '### Classement et accès','',
 f'Les 15 thèmes demandés sont conservés. **25 QCM ont changé de thème principal** après relecture des énoncés et des cours disponibles ; **{sum(bool(q.get("relatedThemes"))for q in pharma)} questions transversales ont {related} renvois** vers d’autres thèmes. Ces renvois ne créent pas de doubles dans la notation. Un index repliable permet de chercher dans toute la pharmacologie par consigne, mots-clés, année ou numéro source.','',
 '| Thème principal | QCM |','|---|---:|']
theme_labels=dict(read(P.parent/'pharma_v3/themes.json'))
for b,e in E.items():
 if e['ue']=='ue4':lines.append(f'| {md(theme_labels[e["courseId"]])} | {len(e["questions"])} |')
lines+=['','Les 336 QCM UE4 comprennent **325 questions évaluables et 11 hors note**, inchangées par rapport à la révision précédente. Une clé « aucune proposition vraie » est distinguée d’un corrigé absent. Les décalages de numérotation sujet/corrigé de 2021–2022 S1 restent documentés.','',
 '## 2. Questions récupérées et erreurs d’importation réparées','',
 '| Banque | Nouvel identifiant dans le site | Question source | Pages sujet / corrigé |','|---|---:|---|---|']
for a in adds:
 q=a['question']
 def pages(first,last):return str(first)if not last or first==last else str(first)+'–'+str(last)
 sp=pages(q.get('subjectPage','—'),q.get('sourceEndPage'));cp=pages(q.get('correctionPage','—'),q.get('correctionEndPage'))
 lines.append(f'| {md(banklabel(a["bank"]))} | {q["id"]} | {md(q.get("category"))} · {md(q.get("sourceNumber",q.get("num")))} | {sp} / {cp} |')
lines+=['',f'Les **{tests["oldQuestionIdentitiesPreserved"]} questions préexistantes gardent leur identité**. Les nouvelles questions reçoivent des identifiants libres : les réponses sauvegardées ne sont pas déplacées vers une autre question.','',
 f'Les réparations touchent **{stats["patchedQuestions"]} questions existantes**, hors déplacements de thèmes de pharmacologie. **{len(keys_changed)} clés ont été rétablies ou désambiguïsées selon les documents** ; ce nombre comprend les retraits de notation lorsque le lettrage ne permet pas une clé fiable. **{len(false_restored)} statuts “aucun item vrai” ont été reconnus explicitement** (certains figurent aussi dans le nombre de clés modifiées). Les détails avant/après et les preuves sont dans `audit/revision_v4/reparations.json`.','',
 'Les réparations concernent notamment les treize blocs de correction TC2 réappariés, des annales de biologie cellulaire, des clés Wooclap et des questions primées de biomol, ainsi que des items d’embryologie fusionnés avec leurs voisins. Les en-têtes d’années absorbés dans le dernier item ont été retirés. Les choix dont la lettre est répétée dans le PDF sont distingués avec un repère source, sans perdre les anciens identifiants.','',
 'Les schémas communs sont présentés avant les questions concernées et restent visibles si une recherche ne montre qu’un membre du groupe. Les figures et formules restaurées proviennent des documents originaux ; elles ne sont pas redessinées. Les défauts déjà présents dans le sujet — repères manquants, image trop peu lisible — sont signalés comme limites de la source.','',
 '## 3. Remarques scientifiques dans les corrections','',
 'Une erreur d’importation et un désaccord scientifique sont traités séparément. Une erreur d’appariement prouvée est réparée. Si la clé officielle contredit sa justification, un cours ou une référence scientifique, la clé imprimée reste visible et le commentaire précise le désaccord sur les bons items. Une formulation seulement ambiguë n’est pas présentée comme une erreur certaine.','',
 '| Nature de la remarque | Nombre |','|---|---:|']
kindlabels={'scientific_conflict':'Erreur scientifique repérée / référence externe','roneo_conflict':'Désaccord ou nuance étayés par un cours fourni','source_conflict':'Contradiction entre éléments des documents','possible_error':'Point ou formulation à vérifier','outdated_reference':'Référence / convention à actualiser','missing_reference':'Source insuffisante'}
for k in kindlabels:lines.append(f'| {kindlabels[k]} | {stats["notesByKind"].get(k,0)} |')
lines+=['','Ces catégories décrivent des **remarques**, et non autant de verdicts faux. Un même QCM peut comporter plusieurs remarques. Chaque commentaire indique les lettres concernées, le problème précis et les références disponibles ; les cours fournis sont liés à leur page. Les références scientifiques externes sont identifiées comme telles.','',
 '| Périmètre | QCM/fiches relus | Questions avec remarque |','|---|---:|---:|']
for u in units:
 bs={b for b,e in E.items()if e['ue']==u};count=sum(len(E[b]['questions'])for b in bs);noted=len({(b,i)for b,i in uq if b in bs})
 lines.append(f'| {unitlabel(u)} | {count} | {noted} |')
lines+=['',f'La couverture enregistrée porte sur **{len(C)} fiches** et **{reviewed_items} propositions lisibles relues**. Un item reste tronqué dans le sujet original : ADN, annales, QCM du site 17, item E. Aucun texte manquant n’a été inventé. L’autotest d’introduction biomol 10 est un exercice de correspondance, sans liste A–E.','',
 f'Les cours ont été consultés sur les notions concernées pour **{course_questions} fiches**, parfois sur une partie seulement des items. Les autres ont été relues à partir de la banque, des sujets et corrigés disponibles, avec des recoupements ciblés. En pharmacologie, les seuls cours exploitables fournis sont Droit pharma et Cycle de vie du médicament. Aucune ronéo SSH complète ni de traduction/régulation n’est disponible, et la ronéo spécifique cœur/vaisseaux manque également. Les cours présents contiennent eux-mêmes quelques formulations discutables.','',
 '**La relecture ne constitue donc pas une certification scientifique de toutes les réponses.** Les réserves précises et les limites sont conservées dans le site. Les nouvelles remarques ont fait l’objet d’une seconde lecture ; plusieurs signalements trop affirmatifs ont été nuancés ou supprimés après retour au cours ou à l’image.','',
 '## 4. Vérifications du fonctionnement','',
 f'- {tests["blankCards"]} cartes avant correction et {tests["correctedCards"]} cartes après correction contrôlées ; remarques et réponses masquées avant validation.',
 f'- Notation vérifiée sur les {tests["gradedBanks"]} banques : les réponses de référence obtiennent 20/20 sur les questions évaluables ; les questions hors note restent exclues.',
 f'- Séparation des deux profils contrôlée sur les {tests["profileChecks"]} banques ; migration et rechargement de {tests["migratedPharmaStates"]} états de pharmacologie, avec reclassement.',
 '- Persistance des identifiants, export sans correction des QCM non validés, choix explicite « aucune proposition » et énoncés communs après filtrage vérifiés.',
 '- Le choix « Aucune proposition » est disponible pour tous les QCM ayant des items : sa présence ne permet pas de deviner une clé tout-faux. Sa sauvegarde reste distincte d’un blanc.',
 '- Les deux questions de tissu nerveux demandant une affirmation inexacte affichent « À cocher / Ne pas cocher » ; la réponse demandée n’est plus étiquetée à tort « Vrai ».',
 f'- {content["imagesVerified"]} fichiers image référencés décodés sans erreur ; {content["pdfsOpened"]} PDF liés ouverts ; {content["noteReferencePagesChecked"]} renvois de notes et {content["proofReferencePagesChecked"]} renvois de preuves de réparation contrôlés dans leurs bornes.',
 '- Les vérifications d’application utilisent un adaptateur DOM déterministe ; elles ne remplacent pas un contrôle de mise en page dans un navigateur.','',
 '## 5. Utilisation et progression','',
 'Décompresser toute l’archive, puis ouvrir `index.html`. Garder `static/` et `sources/` à côté. Pour retrouver les sauvegardes existantes, utiliser le même navigateur et remplacer le site à son emplacement habituel, en conservant le nom `index.html`. Les réponses sont stockées dans le navigateur ; le ZIP ne contient pas de progression personnelle.','',
 'Interrupteur activé : profil 1, seuls les QCM renseignés sont corrigés. Interrupteur désactivé : profil 2, progression indépendante et correction globale. Les remarques scientifiques apparaissent dans le panneau de correction, jamais comme partie des énoncés ou des options. Aucun QCM antérieur à 2015 n’a été ajouté ; les anciens QCM déjà présents dans la biomol sont conservés.','',
 '## Documents de contrôle dans l’archive','',
 '- `POINTS_A_VERIFIER.md` : toutes les remarques, classées par unité et banque, avec les sources.',
 '- `audit/revision_v4/annotations.json` et `couverture.json` : annotations et périmètre réel de lecture question par question.',
 '- `audit/revision_v4/reparations.json` et `ajouts.json` : différences d’importation documentées et nouvelles questions.',
 '- `audit/revision_v4/pharmaco_fresh_subject_inventory.json` : inventaire indépendant des sujets de pharmacologie.',
 '- `audit/revision_v4/logic_checks.json` et `content_checks.json` : résultats des vérifications du fonctionnement et des fichiers.',
 '- `audit/fichiers_sha256.json` : empreintes des fichiers du site. Les anciens rapports sont conservés comme historique, avec la version V3 dans `audit/historique_v3_2026-11-22/`.','']
report='\n'.join(lines)
(R/'output/Verification_QCM_revision_v4.md').write_text(report)
(S/'CONTROLE_ANNALES.md').write_text(report)

points=['# Points à vérifier dans les corrections — V4','',f'{len(N)} remarques sur {len(uq)} questions. Les clés du tutorat restent conservées lorsqu’il s’agit d’un désaccord scientifique. Les sources et la nature de chaque réserve sont précisées. Ce document de contrôle contient des éléments de correction.','']
for u in units:
 points+=['## '+unitlabel(u),'']
 for b,e in E.items():
  if e['ue']!=u:continue
  ns=[n for n in N if n['bank']==b]
  if not ns:continue
  points+=['### '+banklabel(b),'']
  for n in ns:
   q=next(q for q in e['questions']if q['id']==n['id']);ident='QCM '+str(q['id'])+' · '+('items '+', '.join(n.get('items',[]))if n.get('items')else'consigne/contexte')
   if q.get('sourceId'):ident+=' · '+q['year']+' · source '+str(q.get('printedSourceNumber')or q.get('sourceNumber'))
   points+=['#### '+ident,'','**'+kindlabels.get(n['kind'],n['kind'])+'.** '+n['text'],'']
   if n.get('sourceVerdict'):points+=['Document fourni : '+str(n['sourceVerdict']),'']
   if n.get('courseVerdict'):points+=[str(n['courseVerdict']),'']
   if n.get('refs'):points+=['Sources : '+' ; '.join(reftext(x)for x in n['refs'])+'.','']
(S/'POINTS_A_VERIFIER.md').write_text('\n'.join(points))

readme=f'''# Site de révision PASS — V4

Version du 22 novembre 2026. **{stats['questionCount']} QCM/fiches**, toutes les unités relues ; pharmacologie en quinze thèmes.

## Ouvrir le site

1. Décompresser toute l’archive.
2. Ouvrir `index.html` dans le navigateur.
3. Conserver `static/` et `sources/` à côté.

Le site fonctionne localement, sans compte ni serveur. L’index repliable de pharmacologie recherche les consignes, mots-clés, années et numéros source dans les 336 QCM des quatorze sujets fournis. Les sujets 2015–2018 et la session 2 de 2025–2026 ne sont pas fournis.

## Corrections

Cette révision restaure {len(adds)} QCM présents dans les documents et corrige des appariements d’items, clés et figures. {len(N)} remarques sur {len(uq)} questions signalent un problème précis, dans la correction uniquement. Elles distinguent erreur étayée, contradiction documentaire et point à confirmer. Les désaccords scientifiques ne remplacent pas la clé du tutorat ; les erreurs d’importation prouvées sont réparées.

Les ronéos disponibles ne couvrent pas tous les cours. Une question sans remarque n’est pas une certification de la justesse de chaque verdict. La liste complète et les sources sont dans `POINTS_A_VERIFIER.md`, le bilan dans `CONTROLE_ANNALES.md`.

## Progression et profils

- Interrupteur activé : profil 1, correction des seuls QCM renseignés.
- Interrupteur désactivé : profil 2, progression indépendante et correction globale.
- « Aucune proposition » est disponible uniformément et constitue une réponse volontaire, différente d’un blanc.
- Recommencer ne remet à zéro que la série et le profil courants.

Les anciennes réponses de pharmacologie sont rattachées à leur identité source, indépendamment des reclassements. Les anciens identifiants des autres unités sont conservés. Pour retrouver sa progression, utiliser le même navigateur et remplacer le site au même emplacement, en gardant `index.html`. Les réponses sont dans le navigateur, pas dans le ZIP.

`audit/revision_v4/` contient les preuves et vérifications. `MAINTENANCE.md` décrit la structure à conserver lors des modifications suivantes.
'''
(S/'README.md').write_text(readme)
maintenance=f'''# Maintenance — révision V4, 22 novembre 2026

## Périmètre et contrat

État courant : {stats['questionCount']} QCM/fiches, 217 banques, 336 QCM de pharmacologie dans les quinze thèmes fournis. La demande V4 autorise une relecture scientifique des autres unités et la réparation documentée des pertes/appairages. Elle n’autorise pas à remplacer les clés officielles pour un désaccord scientifique non résolu. Les identités de tous les QCM préexistants sont conservées ; les ajouts ont des IDs libres. Aucun QCM antérieur à 2015 n’est ajouté ; le contenu ancien déjà présent dans la biomol n’est pas supprimé.

## Données et affichage

`index.html` contient CSS, interface et JavaScript. `const EXAMS=` est du JSON. Les banques portent `ue`, `courseId`, `kind`, `questions` et `storage`. Les thèmes UE4 sont `ue4.annales.theme.<themeId>`, `pharmaGrouped:true`.

`question`, `context`, `options[].text`, `images`, `stemImages`, `originalImages`, `options[].image` sont des énoncés. `explanations`, `generalExplanation`, `correctionImages`, `reviewNotes` et les réserves `warning` appartiennent à l’après-correction. Le rendu `reviewHtml(q)` est appelé seulement si `isCorrected(q)`. L’export respecte la même condition pour chaque QCM, dans les deux profils. `reviewWarningCovered` et `pharmaWarningCovered` évitent les réserves historiques en doublon.

Les notes ont `noteId`, `items`, `kind`, `text`, `refs`, éventuellement `sourceVerdict`/`courseVerdict`. Une référence de cours n’est pas une garantie pour tous les items d’un chapitre. `itemsReviewedCount` mesure la lecture, les champs `status`/`courseVerification` et `visualReview` précisent sa portée. Les fichiers locaux cités dans les notes sont dans `sources/revision_v4/` ; les pages sont en base 1.

## Identités et stockage

La pharmacologie utilise `sourceId` comme identité stable : le numéro local `id` peut changer lors d’un reclassement sans déplacer les réponses. `sourceNumber` et `printedSourceNumber` sont ceux du document. La progression UE4 est dans `qcm-pass-ls-ue4-progress-by-source-v1` et sa variante `_profil_2_v1`, via `bySource`. `PHARMA_PROGRESS_LINKS`, `legacyProgress` et `PHARMA_EXAM_ALIASES` maintiennent la migration. Ne jamais réimporter une réponse effacée volontairement : une entrée vide est une entrée existante.

Les années 2018–2019 et 2019–2020 gardent S1 dans leurs anciennes identités de stockage ; leurs couvertures ne précisent pas la session. `pharmaPrintedSession` corrige l’affichage et l’export sans modifier les identités.

Hors pharmacologie, `storage` correspond au profil 1 et `storage+'_profil_2_v1'` au profil 2. Ne renuméroter ni les questions ni les choix préexistants. Si une lettre répétée dans le document exige un nouveau choix, employer une lettre libre et `options[].sourceLabel` pour expliquer le repère original. Les choix peuvent dépasser A–E. Les identifiants composés relèvent de `tokenMode`.

## Clés et notation

Une clé vide est hors note, sauf `answerIsEmpty:true`. Dans ce dernier cas, `answer:''`, `allowNoAnswer:true` et le choix volontaire ∅ rendent possible une réponse tout-faux. Le contrôle `allowsNoAnswer(q)` propose désormais ∅ uniformément à tous les QCM ayant des options, indépendamment de leur clé, pour ne pas donner d’indice avant correction ; les anciens attributs `allowNoAnswer` restent conservés dans les données. Conserver `rawAnswer` pour les divergences de lettrage ou une clé ambiguë. `ignoredOptions` exclut les seuls items hors programme identifiés ; ne pas y placer tous les choix d’un QCM car cela lui donnerait artificiellement tous les points. Les QCM entièrement marqués HP dans une vieille source sont signalés dans les commentaires ; leur barème n’a pas été refondu sans demande.

Barème conservé : 10/5/2/0 points pour 0/1/2/3+ erreurs, zéro pour un blanc, conversion sur 20 et coefficients existants. La pharmacologie contient toujours 325 QCM évaluables et onze hors note. Les clés changées ailleurs sont exclusivement les réparations référencées dans `audit/revision_v4/reparations.json`. Une contradiction scientifique reste une note, pas une réécriture silencieuse de `answer`. Une question dont `answerPolarity` vaut `false` attend une affirmation inexacte : employer « À cocher / Ne pas cocher », sans présenter la lettre attendue comme un verdict scientifique Vrai.

## Contextes et figures

`sharedContexts` contient l’énoncé/figure avant le premier membre visible du groupe, même après recherche ou filtrage. Ne pas remettre cet énoncé dans le dernier item du QCM précédent. `references` et `referenceImages` servent aux annexes. Les titres des cartes sont les consignes ; nom de fichier et page sont des métadonnées discrètes.

Extraire les figures exactes des sujets ; distinguer les surcouches de lettres Word du bitmap embarqué. Un crop de corrigé contenant réponses ou commentaires ne doit pas devenir une image d’énoncé. Une figure déjà défectueuse dans le sujet est signalée, sans redessin supposé.

## Reproduction et audit

Le constructeur V4 repart de `baseline_index.html`/`baseline_exams.json` immuables puis applique les patches des lots et leurs annotations. Les scripts, données de départ et décisions sont sauvegardés sous `audit/revision_v4/production/`. Ces scripts documentent la production dans son espace de travail d’origine : avant de les relancer ailleurs, adapter les chemins racines, les chemins des assets et la résolution des PDF aux dossiers de l’archive. Les anciens scripts généraux peuvent rétablir des erreurs et ne doivent pas être relancés sans porter ces changements.

Ordre : `build_site.py`, `test_site.cjs` (sans `--draft`), `check_content.py`, `write_report.py`, conditionnement ZIP et manifeste SHA256. Les contrôles sont documentaires et exécutés dans un adaptateur DOM ; aucun résultat de mise en page réelle dans un navigateur n’est revendiqué. Le manifeste de l’archive couvre tous les fichiers sauf lui-même.

Les rapports antérieurs sont historiques, notamment `audit/historique_v3_2026-11-22/`. `CONTROLE_ANNALES.md` est le bilan courant.
'''
(S/'MAINTENANCE.md').write_text(maintenance)
for file in ['logic_checks.json','content_checks.json']:shutil.copy2(P/file,A/file)
prod=A/'production';prod.mkdir(exist_ok=True)
for file in ['CONTRACT.md','baseline_index.html','baseline_exams.json','build_site.py','review_runtime.js','review_style.css','test_site.cjs','dom_adapter.cjs','check_content.py','write_report.py']:
 shutil.copy2(P/file,prod/file)
shutil.copy2(P.parent/'pharma_v3/themes.json',prod/'pharma_themes.json')
for lot in ['pharma','ue1','ue5','ue5_visual','ue2_ue3','biomol_root','embryo','embryo/ue5_assist','root_text']:
 dest=prod/lot;dest.mkdir(parents=True,exist_ok=True)
 for file in ['notes.json','source_repairs.json','source_additions.json','coverage.json','coverage_overrides.json','shared_contexts.json','figure_reviews.json','findings.md','stats.json','crossreview.md','histo_completeness.md','build_repairs.py','changes.json','relatedThemes.json']:
  src=P/lot/file
  if src.exists():shutil.copy2(src,dest/file)
 if lot=='root_text':
  for pattern in ['tc_*','tn_*','*.md']:
   for src in (P/lot).glob(pattern):
    if src.is_file():shutil.copy2(src,dest/src.name)
print(json.dumps({'report':str(R/'output/Verification_QCM_revision_v4.md'),'questionCount':stats['questionCount'],'notes':len(N),'notedQuestions':len(uq),'readableItemsReviewed':reviewed_items,'courseQuestions':course_questions,'keysChanged':len(keys_changed),'allFalseRestored':len(false_restored)},ensure_ascii=False,indent=2))
