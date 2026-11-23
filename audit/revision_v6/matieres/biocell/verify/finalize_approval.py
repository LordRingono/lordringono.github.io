from pathlib import Path
import json,copy,hashlib,re,unicodedata,collections
import fitz

V=Path(__file__).resolve().parent;P=V.parent/'prepare';ROOT=V.parents[3]
def load(p):return json.loads(p.read_text())
def dump(name,data):(V/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
R=load(P/'reviewed.json');C=load(P/'crops.json');BASE=load(V.parents[1]/'baseline_exams.json')
OR=copy.deepcopy(R);OC=copy.deepcopy(C);M=load(P/'source_manifest.json')
def q(b,i):return next(x for x in R['banks'][b]['questions'] if x['id']==i)
def cr(b,i):return next(x for x in C if x['bank']==b and x['id']==i)
def origq(b,i):return next(x for x in OR['banks'][b]['questions'] if x['id']==i)
fixes=[]
def change(b,i,field,before,after,reason,evidence):
 fixes.append({'bank':b,'id':i,'field':field,'before':before,'after':after,'reason':reason,'evidence':evidence,'status':'fixed_in_approved_files'})
def setfield(b,i,field,after,reason,evidence):
 old=q(b,i).get(field);q(b,i)[field]=after;change(b,i,field,old,after,reason,evidence)
def setdetail(b,i,letter,text,reason,evidence):
 old=q(b,i)['explanations'].get(letter,'');q(b,i)['explanations'][letter]=text;change(b,i,'explanations.'+letter,old,text,reason,evidence)

# A genuine trailing sentence omission found by comparing complete correction blocks.
setdetail('bio.ann.cm2',14,'E',q('bio.ann.cm2',14)['explanations']['E']+' présente dans la matrice.',
 'La dernière ligne du commentaire E avait été omise.',{'file':'Annales CM2 corrigées-1.pdf','page':14,'literalTail':'présente dans la matrice.'})
setdetail('bio.ann.cm4',4,'A',
 'Texte non barré du corrigé : « La séquence de 20 acides aminés hydrophobes correspond vraisemblablement à un segment transmembranaires. On voit que les charges + sont du côté N-ter, ce qui signifie que l’extrémité N-ter se trouvera dans le cytosol. » Le verdict FAUX et la conclusion « Il s’agit donc d’une protéine de type 2 » sont barrés ; l’annotation finale indique VRAI.',
 'Les phrases non barrées du paragraphe subsistent dans la source, même après remplacement explicite du verdict.',{'file':'Annales corrigées CM4 2018-2025.pdf','page':4,'visual':'visual/erratum_bio.ann.cm4_4.png'})
setdetail('bio.ann.cm5',1,'A','Compilation générale : « jamais » (A FAUX). Le fichier thématique rature l’item sans verdict explicite ; la question entière reste hors note à cause du désaccord de clé entre les deux versions.',
 'Le détail explicitement imprimé dans la compilation doit rester consultable malgré la clé globale discordante.',{'file':'Annales_compilation.pdf','page':1041})
setdetail('bio.ann.cm8',1,'E','Plusieurs mitochondries par cellules et plusieurs copies par mitochondries (complément du corrigé de la compilation générale, p. 1038).',
 'Rétablissement du détail E imprimé dans la seconde copie de correction utilisée pour ce QCM.',{'file':'Annales_compilation.pdf','page':1038})

setfield('bio.ann.cm10',3,'generalExplanation',
 'Pour comprendre l’expérience : l’annexine-V et l’IP sont des marqueurs d’apoptose (les cellules en apoptose les expriment fortement). Ici, les cellules situées en bas à gauche des graphiques sont donc en meilleure santé que celles situées en haut à droite. On observe ainsi que l’ouabaïne semble induire l’apoptose des cellules qui y sont exposées.',
 'Paragraphe général du corrigé omis dans la version interactive ; formulation officielle conservée.',{'file':'Annales corrigées CM10 2023-2025.pdf','page':5})
setfield('bio.ann.cm10',9,'generalExplanation',
 'Rappel : l’annexine V est un marqueur d’apoptose et l’IP est un marqueur de nécrose et d’apoptose tardive (il marque l’ADN et permet donc d’identifier des cellules dont la membrane plasmique est endommagée).',
 'Rappel général imprimé avant les verdicts A–E, absent du texte interactif.',{'file':'Annales corrigées CM10 2023-2025.pdf','page':9})
setfield('bio.ann.cm2',5,'generalExplanation',
 'Vous pouvez répondre à ces 5 items juste avec le cours sans regarder le document.',
 'Remarque finale du corrigé scanné rétablie.',{'file':'Annales CM2 corrigées-1.pdf','page':5,'visual':'visual/anncm2_correction_p5.png'})

old=q('bio.ann.cm2',3)['context'];new=old.replace('Noe +Ro3306','Noc +Ro3306').replace('Noe + Ro3306','Noc + Ro3306')
assert new!=old
setfield('bio.ann.cm2',3,'context',new,'Correction de transcription du nom de la condition Noc, confirmé sur le sujet et la figure.',{'file':'Annales CM2 non corrigées.pdf','page':3,'visual':'visual/anncm2_subject_p3.png'})

n=next(x for x in q('bio.cm6',7)['reviewNotes'] if x['noteId']=='ue5-063');old=copy.deepcopy(n)
n['items']=['D','E'];n['kind']='import_mapping_resolved'
n['text']='La réserve antérieure sur le sens de la floppase provenait d’un décalage d’import : le commentaire « quand il est à l’extérieur elles le remettent sur le feuillet interne » appartient à l’item sur les flippases, soit E dans le sujet et D dans le corrigé. Il a été réattribué à E ; aucun commentaire de ce type n’est imprimé pour les floppases. La ronéo p. 8 confirme flippases externe → interne et floppases interne → externe. Le véritable défaut documentaire restant est l’absence de l’item B du sujet dans le corrigé ; la question reste hors note.'
n['reviewedItemText']={k:next(o['text'] for o in q('bio.cm6',7)['options'] if o['id']==k) for k in n['items']}
n['reviewedExplanation']={k:q('bio.cm6',7)['explanations'][k] for k in n['items']}
change('bio.cm6',7,'reviewNotes.ue5-063',old,n,'La note ancienne décrivait une explication désormais réattribuée à son véritable item.',{'correction':'CORRECTION AUTOTEST CM6 LES MEMBRANES(1).docx','page':2,'course':'roneo CM6 MP 2026 - Actualisee.pdf','coursePage':8})
n=next(x for x in q('bio.cm8',10)['reviewNotes'] if x['noteId']=='ue5-078');old=copy.deepcopy(n)
n['items']=['A','B','F'];n['text']='Le lapsus de l’item A (« arginine aspartate protéase ») est explicitement corrigé dans la source : les caspases sont des cystéinyl-aspartate protéases. Pour F, la ronéo place l’activation du récepteur FAS par son ligand avant le recrutement des adaptateurs et des procaspases 8/10 dans le DISC. Les caspases ne forment donc pas ce complexe en activant d’abord FAS. Pour B, lire apoptosome, assemblé avec APAF1 et le cytochrome c. Ces lettres correspondent aux huit propositions restaurées du sujet ; la clé BDEF du corrigé est conservée.'
n['reviewedItemText']={k:next(o['text'] for o in q('bio.cm8',10)['options'] if o['id']==k) for k in n['items']}
n['reviewedExplanation']={k:q('bio.cm8',10)['explanations'][k] for k in n['items']}
change('bio.cm8',10,'reviewNotes.ue5-078',old,n,'La prose de la note conservait les anciens lettrages E/A malgré le rétablissement de huit items.',{'course':'CM8 Ronéo 2026 - Actualisee.pdf','pages':[5,6,7]})

# Preserve the historical note identifier while recording that its missing figure was found.
historical=next(n for x in BASE['bio.ann.cm5']['questions'] if x['id']==16 for n in x.get('reviewNotes',[]) if n.get('noteId')=='review-v4-ue5-visual-016')
n=copy.deepcopy(historical);n['kind']='reference_restored'
n['text']='La consigne renvoie à la figure 6 et aux informations précédentes. La figure expérimentale, absente de l’ancien extrait, a été retrouvée à la page 11 du sujet original : les six constructions GFP et leurs images sont désormais présentées avec le protocole UBQLN2/MTM1 de la page 10. Aucune image n’a été reconstruite. La limite documentaire signalée par cette note est donc résolue ; la clé AB reste celle du corrigé.'
n['courseVerdict']='Figure expérimentale originale retrouvée et présentée avec son protocole.';n['sourceVerdict']='Clé officielle appliquée : AB'
n['refs'].append({'file':'Annales CM5 2018-2025.pdf','page':11,'label':'Figure 6 originale : constructions GFP et immunofluorescence','href':'sources/revision_v4/Annales_CM5_2018_2025_e28d5cc12f.pdf#page=11'})
q('bio.ann.cm5',16).setdefault('reviewNotes',[]).append(n)
change('bio.ann.cm5',16,'reviewNotes.review-v4-ue5-visual-016',None,n,'Conserver la note historique supprimée en préparation, avec sa limite explicitement résolue par la figure retrouvée.',{'file':'Annales CM5 2018-2025.pdf','pages':[10,11]})

# Shared earlier evidence expressly used in the following question's correction.
figure1=next(p for p in cr('bio.ann.cm2',4)['subject'] if p.get('purpose')=='figure_or_shared_context')
src1=q('bio.ann.cm2',4)['images'][0]
for b,i in [('bio.ann.cm2',5),('bio.ann.cm10',3)]:
 prior=q(b,i)['context'];setfield(b,i,'context','Expérience précédente — '+q('bio.ann.cm2',4)['context']+'\n\n'+prior,
 'Le raisonnement du corrigé renvoie à la question précédente ; son protocole et sa figure sont fournis pour rendre le QCM autonome.',{'file':'Annales CM2 non corrigées.pdf','pages':[4,5],'correction':'Annales corrigées CM10 2023-2025.pdf','correctionPage':5})
 old=copy.deepcopy(q(b,i)['images']);q(b,i)['images']=[src1]+old
 panel=copy.deepcopy(figure1);panel['label']='Figure 1 et protocole de l’expérience précédente, utilisés par le corrigé de la figure 2';cr(b,i)['subject'].append(panel)
 change(b,i,'images',old,q(b,i)['images'],'Rattachement de la figure 1 déjà vérifiée, sans création de dessin ni de nouvelle figure unique.',figure1)

# Tighten five question borders to exclude text from an adjacent paragraph/question.
for b,i,which,value in [('bio.cm5',17,1,477.9),('bio.cm6',1,3,135.9),('bio.cm6',2,1,149.6),('bio.cm6',10,1,519.25),('bio.ann.cm7',6,1,104.35)]:
 p=cr(b,i)['subject'][0];old=copy.deepcopy(p['rect']);p['rect'][which]=value
 change(b,i,'crops.subject[0].rect',old,p['rect'],'Exclusion d’un fragment voisin sans couper le premier ni le dernier glyphe du QCM.',{'file':p['file'],'page':p['page']})
hashes={}
def capture_src(p):
 if p['file'] not in hashes:hashes[p['file']]=sha(p['file'])
 ident=json.dumps([hashes[p['file']],p['page'],[round(float(v),4) for v in p['rect']]],separators=(',',':'))
 return 'static/revision_v6/'+hashlib.sha256(ident.encode()).hexdigest()[:24]+'.webp'
p=next(x for x in cr('bio.ann.cm5',8)['subject'] if x.get('purpose')=='figure_or_shared_context');old=copy.deepcopy(p);oldsrc=capture_src(p)
p['rect'][1]=132.0;p['label']='Figure 7 complète, protocole et résultats ; le titre marginal Hors Programme est exclu du cadrage'
newsrc=capture_src(p);q('bio.ann.cm5',8)['images']=[newsrc if x==oldsrc else x for x in q('bio.ann.cm5',8)['images']]
change('bio.ann.cm5',8,'figureCrop',old,p,'Le cadrage reprenait le e final de la mention marginale Hors Programme ; le nouveau bord commence avant la légende Figure 7.',{'file':p['file'],'page':p['page']})

old=cr('bio.ann.cm5',5).get('subjectNote','')
cr('bio.ann.cm5',5)['subjectNote']=old+' La rubrique du document thématique indique « session 2 » ; le sujet général de la compilation identifie cette même question 42 et ses cinq items en session 1 2023–2024. La session 1 affichée est conservée.'
change('bio.ann.cm5',5,'crops.subjectNote',old,cr('bio.ann.cm5',5)['subjectNote'],'Documenter la divergence d’intitulé entre deux reproductions du même QCM.',{'thematicFile':'Annales CM5 2018-2025.pdf','thematicPages':[4,5],'compilationPanels':cr('bio.ann.cm5',5)['subject']})

# Retire fallback assets superseded by the complete authenticated sourceCopies built from C.
legacy=[]
for b,ex in R['banks'].items():
 for item in ex['questions']:
  for field in ['originalImages','correctionImage']:
   if field in item:
    legacy.append({'bank':b,'id':item['id'],'field':field,'oldValue':item.pop(field),'replacement':'sourceCopies generated from approved_crops.json'})
dump('retired_legacy_graphics.json',legacy)

# Full coverage, retaining the distinction between literal detail and absent detail.
native={(x['bank'],x['id']):x for x in load(V/'independent_extraction.json')}
clean={(x['bank'],x['id']):x for x in load(V/'clean_subject_checks.json')}
visual=load(V/'visual_manifest.json');errata=[x for x in visual if x.get('kind')=='erratum']
erratum_ids={('bio.ann.cm4',2),('bio.ann.cm4',4),('bio.ann.cm4',7),('bio.ann.cm4',9),('bio.ann.cm5',4),('bio.ann.cm5',9),('bio.ann.cm5',10),('bio.ann.cm5',15),('bio.ann.cm7',5),('bio.ann.cm7',8),('bio.ann.cm8',1),('bio.ann.cm9',7)}
documents={};captures={};geometry=[]
for row in C:
 for role in ['subject','correction']:
  for p in row[role]:
   if p['file'] not in documents:documents[p['file']]=fitz.open(p['file'])
   pg=documents[p['file']][p['page']-1];rr=fitz.Rect(p['rect'])
   if rr.is_empty or not (pg.rect+(-.1,-.1,.1,.1)).contains(rr):geometry.append({'bank':row['bank'],'id':row['id'],'role':role,'panel':p})
   captures[capture_src(p)]=p
assert not geometry
coverage=[];figure_refs=[]
for b,ex in R['banks'].items():
 for item in ex['questions']:
  i=item['id'];row=cr(b,i);fresh=native[(b,i)];limits=[]
  if item.get('correctionComplete') is False:limits.append('hors_note_source_discrepancy')
  if row.get('subjectAfterCorrection'):limits.append('annotated_subject_deferred')
  if b=='bio.ann.cm6' and i==7 or b=='bio.ann.cm7' and i==10:limits.append('printed_key_detail_contradiction_preserved')
  refs={role:[{'file':p['file'],'sha256':hashes[p['file']],'page':p['page'],'rect':p['rect']} for p in row[role]] for role in ['subject','correction']}
  its=[]
  for op in item['options']:
   k=op['id'];nr=next(x for x in fresh['items'] if x['id']==k);e=item.get('explanations',{}).get(k,'')
   if e:ds='detail_compared_to_original'
   elif item.get('officialVerdicts',{}).get(k) is None:ds='no_unambiguous_individual_verdict_or_detail'
   elif (b,i) in erratum_ids:ds='verdict_only_or_cancelled_detail_in_original'
   else:ds='no_individual_detail_printed'
   its.append({'item':k,'statement':op['text'],'statementCompared':True,'statementMethod':'fresh_native_source_and_manual_review' if nr['statementInSubjectNative'] else 'manual_visual_or_documented_typographic_reconciliation','officialVerdict':item.get('officialVerdicts',{}).get(k),'officialVerdictCompared':True,'explanation':e,'detailStatus':ds,'generalExplanationAvailable':bool(item.get('generalExplanation')),'subjectReferences':refs['subject'],'correctionReferences':refs['correction']})
  figs=[]
  for src in item.get('images',[]):
   assert src in captures,(b,i,src)
   f={'bank':b,'id':i,'src':src,'capture':captures[src],'status':'source_render_visually_verified'};figs.append(f);figure_refs.append(f)
  coverage.append({'bank':b,'id':i,'status':'compared_with_explicit_limits' if limits else 'verified','sourceQuestionNumber':item.get('sourceQuestionNumber'),'question':item['question'],'questionCompared':True,'contextCompared':True,'answer':item['answer'],'answerIsEmpty':bool(item.get('answerIsEmpty')),'graded':bool(item['answer'] or item.get('answerIsEmpty')),'keyCompared':True,'correctionComplete':item.get('correctionComplete',True),'subjectCopyStatus':'annotated_after_validation' if row.get('subjectAfterCorrection') else 'clean','correctionCopyAvailable':bool(row['correction']),'subjectReferences':refs['subject'],'correctionReferences':refs['correction'],'cleanCompilationSubjectIndependentlyCompared':(b,i) in clean,'graphicalErratumVisuallyVerified':(b,i) in erratum_ids,'figures':figs,'items':its,'limitations':limits})

baseline_banks=BASE.get('banks',BASE) if isinstance(BASE,dict) else BASE
if isinstance(baseline_banks,list):baseline_banks={x['id']:x for x in baseline_banks}
baseline_count=0;weight_checks=[];old_notes=set();new_notes=set()
for b,ex in R['banks'].items():
 old=baseline_banks[b]
 oqs=old['questions']
 for oq in oqs:
  nq=q(b,oq['id']);baseline_count+=1
  assert oq.get('weight',1)==nq.get('weight',1),(b,oq['id'],'weight')
  weight_checks.append({'bank':b,'id':oq['id'],'weight':nq.get('weight',1),'preserved':True})
  for n in oq.get('reviewNotes',[]):old_notes.add(n.get('noteId'))
 for nq in ex['questions']:
  for n in nq.get('reviewNotes',[]):new_notes.add(n.get('noteId'))
assert old_notes<=new_notes,(old_notes-new_notes)
assert baseline_count==224
assert len(coverage)==230 and sum(len(x['items']) for x in coverage)==1137
assert sum(x['graded'] for x in coverage)==226
assert len({x['src'] for x in figure_refs})==73 and len(figure_refs)==93
assert len([x for x in coverage if x['answerIsEmpty']])==4
assert len([x for x in coverage if x['subjectCopyStatus']=='annotated_after_validation'])==1
assert all(q(*k)['answer']==origq(*k)['answer'] for k in [(r['bank'],r['id']) for r in C])

summary={'banks':18,'questionsCompared':230,'itemsComparedToSubjectAndCorrection':1137,'baselineIdsPreserved':224,'restoredOmittedQuestions':6,'graded':226,'ungraded':4,'allFalseGraded':4,'cleanSubjectCopies':229,'annotatedSubjectCopiesAfterValidation':1,'absentSubjectCopies':0,'correctionCopiesAvailable':230,'cleanSubjectsRecoveredFromCompilation':48,'graphicalErrataQuestionsVisuallyChecked':12,'graphicalVerdictsVisuallyChecked':13,'interactiveFigureOccurrences':93,'interactiveFiguresUniqueVisuallyChecked':73,'subjectPanels':sum(len(x['subject']) for x in C),'correctionPanels':sum(len(x['correction']) for x in C),'uniqueRectangles':len(captures),'wordOriginalsChecked':18,'additionalPdfSubjectsCompared':9,'nativeDetailBlocksCompared':1067,'manualExceptionalDetailBlocksCompared':70,'nonemptyInteractiveDetails':sum(bool(i['explanation']) for x in coverage for i in x['items']),'generalExplanations':sum(bool(q(x['bank'],x['id']).get('generalExplanation')) for x in coverage),'notesPreserved':sum(len(qq.get('reviewNotes',[])) for b in R['banks'].values() for qq in b['questions']),'baselineNoteIdsPreserved':len(old_notes),'retiredLegacyOriginalImagesFields':sum(x['field']=='originalImages' for x in legacy),'retiredLegacyCorrectionImageFields':sum(x['field']=='correctionImage' for x in legacy)}
dump('approved_reviewed.json',R);dump('approved_crops.json',C)
dump('coverage.json',{'status':'complete_with_explicit_source_limitations','summary':summary,'method':'Lecture fraîche de toutes les questions, propositions, contextes et corrections ; comparaison documentaire complète ; lecture visuelle des scans CM2, des 12 errata, des 73 figures uniques, des 48 sujets de compilation et des cas limites. Les autres rectangles sont contrôlés par texte et géométrie, sans prétendre à une visualisation individuelle de tous les panneaux.','questions':coverage,'baselineWeights':weight_checks,'wordChecksFile':'word_original_checks.json','cleanSubjectsChecksFile':'clean_subject_checks.json','detailCompletenessFile':'detail_completeness_checks.json','graphics':figure_refs})
missing=load(P/'missing.json')
for x in missing:
 x['independentVerification']='confirmed'
 if x['type']=='course_for_scientific_arbitration_missing':
  x['alsoNeededFor']=[{'bank':'bio.cm10','id':3,'item':'A','reason':'p16, transcription de la cycline D : réserve existante non arbitrable sans ronéo CM10.'}]
dump('missing.json',missing)
dump('issues.json',{'status':'no_unresolved_import_blocker_after_approved_changes','independentFixes':fixes,'keysChangedByVerifier':0,'retiredLegacyGraphics':legacy,'preparerFixesIndependentlyConfirmed':{'restoredQuestionIds':[{'bank':'bio.cm7','ids':[12,13,14]},{'bank':'bio.cm8','ids':[17]},{'bank':'bio.ann.cm4','ids':[9]},{'bank':'bio.ann.cm9','ids':[10]}],'explicitGraphicalVerdicts':13,'cleanSubjects':48,'wordCropping':{'bio.cm3':'l=40501 ; seuls C et D sont visibles dans le Word','bio.cm8':'l=16694, t=24751, r=60826, b=48275'},'nativeEmptyKeys':[{'bank':x['bank'],'id':x['id']} for x in coverage if x['answerIsEmpty']],'preservedPrintedVsV5Weight':{'bank':'bio.ann.cm8','ids':[6,7],'printed':1.5,'interactive':1}},'documentedNativeImageDefects':[{'figure':13,'issue':'La première ligne de légende est déjà coupée à droite dans l’image incorporée ; le contexte textuel restitue le protocole.'},{'figure':17,'issue':'Quelques fragments de pixels sont déjà présents au-dessus du panneau A dans l’image incorporée.'},{'figure':30,'issue':'Le fragment de titre incliné est inclus dans l’image incorporée à la source ; aucune suppression artificielle.'},{'figure':40,'issue':'Le dessin est coupé au bord droit dans l’image incorporée de la source.'},{'figure':55,'issue':'Les limites du petit graphique correspondent exactement au raster incorporé.'}],'sourceLimitations':missing,'unresolvedImportIssues':[]})

# Re-render changed crops for the final visual check, without making new published image assets.
for b,i in [('bio.cm5',17),('bio.cm6',1),('bio.cm6',2),('bio.cm6',10),('bio.ann.cm7',6),('bio.ann.cm5',8)]:
 row=cr(b,i);p=row['subject'][0] if (b,i)!=('bio.ann.cm5',8) else next(x for x in row['subject'] if x.get('purpose')=='figure_or_shared_context')
 documents[p['file']][p['page']-1].get_pixmap(matrix=fitz.Matrix(1.8,1.8),clip=fitz.Rect(p['rect']),alpha=False).save(V/'visual'/('approved_crop_'+b+'_'+str(i)+'.png'))

dump('approval_statistics.json',summary)
print(json.dumps({'summary':summary,'fixes':len(fixes),'hashes':{n:sha(V/n) for n in ['approved_reviewed.json','approved_crops.json','coverage.json','issues.json','missing.json']}},ensure_ascii=False,indent=2))
