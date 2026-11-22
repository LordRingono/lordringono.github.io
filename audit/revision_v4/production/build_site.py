"""Rebuild V4 deterministically from the immutable V3 site and reviewed patches."""
import json,re,copy,hashlib,shutil,unicodedata,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'work/review_v4';SITE=ROOT/'output/site'
def load(p,default=None):
 p=P/p
 return json.loads(p.read_text())if p.exists()else default
BASE=load('baseline_exams.json');E=copy.deepcopy(BASE)
changes=[];additions=[];unresolved=[]
def question(bank,id):return next(q for q in E[bank]['questions']if q['id']==id)
def apply_patch(r):
 q=question(r['bank'],r['id']);fields=copy.deepcopy(r.get('set',{}))
 for field in ['Answer','AnswerIsEmpty','AllowNoAnswer','TokenMode','Explanations','Options','Question','Context','Images','Warning','RawAnswer','IgnoredOptions','SharedContexts','References','SourceLabel']:
  if 'proposed'+field in r:fields[field[0].lower()+field[1:]]=copy.deepcopy(r['proposed'+field])
 if r.get('removeUncorrectedStatus'):
  fields['uncorrected']=False
  if 'proposedWarning'not in r:fields['warning']=''
 if r.get('sourcePage') and ('proposedAnswer'in r or 'proposedExplanations'in r):fields['correctionPage']=r['sourcePage']
 if r.get('sourcePages'):fields['correctionEndPage']=max(r['sourcePages'])
 if fields.get('rawAnswer')=='AUCUNE' or fields.get('answerIsEmpty'):
  fields.update(answer='',answerIsEmpty=True,allowNoAnswer=True)
 if 'answer'in fields and fields['answer'] is None:fields['answerIsEmpty']=False
 if r.get('requiresRootDecision'):unresolved.append({'bank':r['bank'],'id':r['id'],'decision':r['requiresRootDecision']})
 if r.get('proposedAdditionalSourceItem'):raise ValueError('Unconverted additional option: '+str(r))
 for asset in ([r['assetFile']]if r.get('assetFile')else[])+r.get('assetFiles',[]):
  src=ROOT/asset;target=SITE/'static'/src.name
  assert src.exists(),src
  if not target.exists()or src.read_bytes()!=target.read_bytes():shutil.copy2(src,target)
 modified={k:{'before':q.get(k),'after':v}for k,v in fields.items()if q.get(k)!=v}
 q.update(fields)
 if modified:changes.append({'bank':r['bank'],'id':r['id'],'reason':r.get('reason',''),'fields':modified,'proof':r.get('refs')or {'file':r.get('sourceFile'),'page':r.get('sourcePage'),'question':r.get('sourceQuestion')}})
def add_question(r):
 q=copy.deepcopy(r['question']);bank=r['bank'];qs=E[bank]['questions'];assert q['id']not in {x['id']for x in qs},(bank,q['id'])
 if q.get('rawAnswer')=='AUCUNE':q.update(answer='',answerIsEmpty=True,allowNoAnswer=True)
 if r.get('afterId') is not None:
  idx=next(i for i,x in enumerate(qs)if x['id']==r['afterId']);qs.insert(idx+1,q)
 else:qs.append(q)
 additions.append(r)

patch_files=['ue5/source_repairs.json','ue5_visual/source_repairs.json','ue2_ue3/source_repairs.json','biomol_root/source_repairs.json','embryo/source_repairs.json','embryo/ue5_assist/source_repairs.json','root_text/source_repairs.json','root_text/tc_source_repairs.json','root_text/tn_source_repairs.json','root_text/tn_context_repairs.json']
for file in patch_files:
 data=load(file,[])
 if isinstance(data,list):patches=data;adds=[]
 else:patches=data.get('patches',[]);adds=data.get('additions',[])
 for r in patches:apply_patch(r)
 for r in adds:add_question(r)
for file in ['embryo/source_additions.json','embryo/ue5_assist/source_additions.json']:
 for r in load(file,[]):add_question(r)

# Display a shared figure once before its group, also when filtering to one QCM.
for file in ['embryo/shared_contexts.json','embryo/ue5_assist/shared_contexts.json','root_text/shared_contexts.json','root_text/tn_shared_contexts.json']:
 for r in load(file,[]):
  refs=r.get('refs',[]);pages=[x['page']for x in refs if isinstance(x.get('page'),int)]
  context={'id':r.get('key',r.get('id')),'text':r.get('text',''),'images':r.get('images',[]),'sourceFile':refs[0].get('file','')if refs else '', 'sourceStartPage':min(pages)if pages else None,'sourceEndPage':max(pages)if pages else None}
  for qid in r['questionIds']:
   q=question(r['bank'],qid)
   fields={'sharedContexts':[c for c in q.get('sharedContexts',[])if c.get('id')!=context['id']]+[context],'images':[x for x in q.get('images',[])if x not in context['images']]}
   if q.get('context')==context['text']:fields['context']=''
   apply_patch({'bank':r['bank'],'id':qid,'set':fields,'reason':'Énoncé et schéma communs affichés avant les QCM concernés, avec maintien lors du filtrage.','refs':refs})

themes=load('../pharma_v3/themes.json');theme_labels=dict(themes)
for r in load('pharma/changes.json',[]):
 old='ue4.annales.theme.'+r['fromTheme'];new='ue4.annales.theme.'+r['toTheme']
 q=next(q for q in E[old]['questions']if q['sourceId']==r['sourceId']);E[old]['questions'].remove(q)
 old_id=q['id'];taken={x['id']for x in E[new]['questions']}
 if q['id']in taken:q['id']=max(taken,default=0)+1
 q['category']=theme_labels[r['toTheme']];q['course']=q['category']
 E[new]['questions'].append(q)
 changes.append({'sourceId':q['sourceId'],'fromBank':old,'fromId':old_id,'bank':new,'id':q['id'],'reason':r['reason'],'fields':{'theme':{'before':r['fromTheme'],'after':r['toTheme']}}})
by_source={q['sourceId']:(b,q)for b,e in E.items()if e['ue']=='ue4'for q in e['questions']}
for r in load('pharma/relatedThemes.json',[]):by_source[r['sourceId']][1]['relatedThemes']=r['relatedThemes']

# Resolve references to the actual supplied file, then package only cited files.
def norm(s):return unicodedata.normalize('NFC',str(s)).casefold()
allfiles=[x for x in ROOT.rglob('*')if x.is_file()and x.suffix.lower()in {'.pdf','.docx'}and 'node_modules'not in x.parts]
file_index=collections.defaultdict(list)
for f in allfiles:file_index[norm(f.name)].append(f)
source_map={};ref_cache={};reference_warnings=[]
digest_cache={}
def digest(p):
 if p not in digest_cache:digest_cache[p]=hashlib.sha256(p.read_bytes()).hexdigest()
 return digest_cache[p]
def resolve(name):
 name=str(name)
 if 'Sujets + corrections compilés' in name or name=='Annales_compilation.pdf':return SITE/'sources/Annales_compilation.pdf'
 p=ROOT/name
 if p.is_file():return p
 if ' / 'in name:name=name.rsplit(' / ',1)[1]
 options=file_index.get(norm(Path(name).name),[])
 if not options:return None
 # Prefer direct materials; for UE5 course/source duplicates prefer the reviewed extraction.
 options=sorted(options,key=lambda x:(0 if 'sources_v4'in x.parts else 1 if 'sources_biomol'in x.parts else 2 if 'review_v4'in x.parts else 3,len(x.parts),str(x)))
 chosen=options[0]
 if len({digest(p)for p in options})>1:
  reference_warnings.append({'file':name,'chosen':str(chosen.relative_to(ROOT)),'alternatives':[str(x.relative_to(ROOT))for x in options]})
 return chosen
def materialize_ref(ref):
 r=copy.deepcopy(ref)
 if r.get('url'):return r
 name=r.get('file')
 if not name:return r
 if name not in ref_cache:
  src=resolve(name)
  if src is None:ref_cache[name]=None
  elif src.is_relative_to(SITE):ref_cache[name]=src.relative_to(SITE).as_posix()
  else:
   key=digest(src);filename=re.sub(r'[^a-zA-Z0-9]+','_',unicodedata.normalize('NFKD',src.stem).encode('ascii','ignore').decode()).strip('_')[:65]+'_'+key[:10]+src.suffix.lower()
   dst=SITE/'sources/revision_v4'/filename;dst.parent.mkdir(parents=True,exist_ok=True)
   if not dst.exists():shutil.copy2(src,dst)
   ref_cache[name]=dst.relative_to(SITE).as_posix();source_map[name]={'localSource':str(src.relative_to(ROOT)),'packaged':ref_cache[name],'sha256':key,'bytes':src.stat().st_size}
 if ref_cache[name]:
  r['href']=ref_cache[name]+('#page='+str(r.get('page',1))if ref_cache[name].endswith('.pdf')else'')
 else:r['unresolvedFile']=True
 return r

proof_refs=[]
for change in changes:
 proof=change.get('proof')
 if isinstance(proof,list):
  change['proof']=[materialize_ref(r)for r in proof];proof_refs.extend(change['proof'])
 elif isinstance(proof,dict)and proof.get('file'):
  change['proof']=materialize_ref(proof);proof_refs.append(change['proof'])
for addition in additions:
 addition['refs']=[materialize_ref(r)for r in addition.get('refs',[])];proof_refs.extend(addition['refs'])

notes=[];coverage=[]
for folder in ['pharma','ue1','ue5','ue5_visual','ue2_ue3','biomol_root','embryo','embryo/ue5_assist','root_text']:
 lot_notes=load(folder+'/notes.json',[])
 lot_coverage=load(folder+'/coverage.json',[])
 if folder=='root_text':
  for label in ['tc','tn']:
   lot_notes+=load(folder+'/'+label+'_notes.json',[])
   lot_coverage+=load(folder+'/'+label+'_coverage.json',[])
 for n in lot_notes:
  n=copy.deepcopy(n)
  if folder=='pharma':bank,q=by_source[n['sourceId']]
  else:bank=n['bank'];q=question(bank,n['id'])
  n['bank']=bank;n['id']=q['id']
  assert all(x in {o['id']for o in q['options']}for x in n.get('items',[])),(bank,q['id'],n)
  for letter,expected in n.get('reviewedItemText',{}).items():
   actual=next(o['text']for o in q['options']if o['id']==letter)
   assert actual==expected,(bank,q['id'],letter,'reviewed item differs after repair')
  for letter,expected in n.get('reviewedExplanation',{}).items():
   assert q.get('explanations',{}).get(letter,'')==expected,(bank,q['id'],letter,'reviewed explanation differs after repair')
  n['refs']=[materialize_ref(r)for r in n.get('refs',[])]
  if not n.get('noteId'):n['noteId']='review-v4-'+str(len(notes)+1)
  notes.append(n)
 for c in lot_coverage:
  c=copy.deepcopy(c)
  if folder=='pharma':bank,q=by_source[c['sourceId']];c['bank']=bank;c['id']=q['id']
  c['sourceLot']=folder
  c['status']=c.get('status')or c.get('reviewStatus')or c.get('reviewstatus')or'needs_source'
  reviewed=c.get('reviewedItemCount',c.get('itemCountReviewed',c.get('itemsReviewed',0)))
  c['itemsReviewedCount']=len(reviewed)if isinstance(reviewed,list)else reviewed
  coverage.append(c)
for update in load('root_text/coverage_overrides.json',[]):
 c=next(c for c in coverage if c['bank']==update['bank']and c['id']==update['id'])
 c.update(copy.deepcopy(update))
 c['itemsReviewedCount']=len(c['itemsReviewed'])
# Remove superseded pharmacology annotations; all current reviews replace V3 notes.
for e in E.values():
 for q in e['questions']:
  q.pop('reviewNotes',None);q.pop('reviewWarningCovered',None)
for n in notes:
 q=question(n['bank'],n['id']);q.setdefault('reviewNotes',[]).append(n)
 if n.get('coversWarning'):q['reviewWarningCovered']=True
for e in E.values():
 for q in e['questions']:
  if q.get('answerIsEmpty'):q['allowNoAnswer']=True

figure_reviews=[]
for file in ['ue5/figure_reviews.json','ue5_visual/figure_reviews.json','embryo/ue5_assist/figure_reviews.json']:
 figure_reviews.extend(load(file,[]))
for c in coverage:
 if c.get('figureReviewed'):
  figure_reviews.append({'bank':c['bank'],'id':c['id'],'images':c.get('imagesReviewed',[]),'observation':c.get('figureReview',''),'figureStatus':c.get('figureCorrespondenceStatus','reviewed'),'sourceLot':c['sourceLot']})
for c in coverage:
 q=question(c['bank'],c['id']);c['noteIds']=[n['noteId']for n in q.get('reviewNotes',[])]
 c['currentItemCount']=len(q['options'])
 applied=[{'reason':r['reason'],'fields':list(r['fields'])}for r in changes if 'sourceId'not in r and r['bank']==c['bank']and r['id']==c['id']]
 if applied:c['sourceRepair']=True;c['appliedRepairs']=applied
 reviewed=[r for r in figure_reviews if r.get('bank')==c['bank']and r.get('id')==c['id']]
 if reviewed:c['visualReview']=reviewed

html=(P/'baseline_index.html').read_text();a=html.index('const EXAMS=')+len('const EXAMS=');z=html.index('const EXAM_ORDER=',a)
prefix=html[:a];tail=html[z:]
prefix=prefix.replace('</style>',(P/'review_style.css').read_text()+'\n</style>',1)
catalog='''<details id="pharma-catalog" class="pharma-catalog hidden"><summary>Retrouver un QCM parmi toutes les annales de pharmacologie</summary><label class="pharma-catalog-search" for="pharma-catalog-search">Rechercher une consigne, une année ou un numéro<input id="pharma-catalog-search" type="search" placeholder="Ex. : 2024 2025, générique, QCM 13…" autocomplete="off"></label><p id="pharma-catalog-count" class="pharma-catalog-count" aria-live="polite"></p><div id="pharma-catalog-results" class="pharma-catalog-results"></div></details>'''
prefix=prefix.replace('<div class="filled-mode-row">',catalog+'\n<div class="filled-mode-row">',1)
start=tail.index('function pharmaReviewHtml(q){');end=tail.index('function pharmaSourceLabel(q){',start)
tail=tail[:start]+(P/'review_runtime.js').read_text()+'\n'+tail[end:]
tail=tail.replace('q.allowNoAnswer','allowsNoAnswer(q)').replace('target.allowNoAnswer','allowsNoAnswer(target)')
tail=tail.replace('status=q.fromCompilation?',"status=(q.fromCompilation||q.answerPolarity==='false')?")
tail=tail.replace("q.fromCompilation?'Cochez les propositions demandées dans la consigne'","(q.fromCompilation||q.answerPolarity==='false')?'Cochez les propositions demandées dans la consigne'")
tail=tail.replace("q.fromCompilation?'À COCHER':'VRAI'","(q.fromCompilation||q.answerPolarity==='false')?'À COCHER':'VRAI'")
tail=tail.replace("q.fromCompilation?'NE PAS COCHER':'FAUX'","(q.fromCompilation||q.answerPolarity==='false')?'NE PAS COCHER':'FAUX'")
tail=tail.replace("renderSelectors();","renderSelectors();\n renderPharmaCatalog();",1)
tail=tail.replace("const session=q.session==='S1'?'Session 1':q.session==='S2'?'Session 2':q.session;","const session=pharmaPrintedSession(q);")
tail=tail.replace("identifiant_source:q.sourceId,annee:q.year,session:q.session,","identifiant_source:q.sourceId,annee:q.year,session:['2018-2019','2019-2020'].includes(q.year)?null:q.session,session_source:pharmaPrintedSession(q),")
tail=tail.replace("if(done&&q.pharmaReviewed)details=details.replace(/<\\/div><\\/details>$/,pharmaReviewHtml(q)+'</div></details>');","if(done)details=details.replace(/<\\/div><\\/details>$/,reviewHtml(q)+'</div></details>');")
for old in ["${issue&&!q.pharmaReviewed?`<div class=\"issue\"><strong>Correction à vérifier</strong>${esc(q.warning)}</div>`:''}","${issue&&!q.pharmaReviewed?`<div class=\"issue\"><strong>Réserve sur le corrigé</strong>${esc(q.warning)}</div>`:''}"]:
 assert old in tail;tail=tail.replace(old,'')
tail=tail.replace('<span class="opt-letter">${o.id}</span>','<span class="opt-letter">${esc(o.id)}</span>')
tail=tail.replace('${esc(o.text)}${o.image?',"${o.sourceLabel?`<small class=\"option-source-label\">${esc(o.sourceLabel)} · </small>`:''}${esc(o.text)}${o.image?")
old="${o.id} · ${(q.tokenMode?q.answer.split(',').includes(o.id):q.answer.includes(o.id))?"
tail=tail.replace(old,"${esc(o.id)}${o.sourceLabel?' ('+esc(o.sourceLabel)+')':''} · ${(q.tokenMode?q.answer.split(',').includes(o.id):q.answer.includes(o.id))?")
old="</span><span class=\"explain-text\">${esc(q.explanations"
new="${q.reviewNotes?.some(n=>n.items?.includes(o.id))?'<small class=\"review-opt-flag\">À vérifier · voir remarque</small>':''}</span><span class=\"explain-text\">${esc(q.explanations"
assert old in tail;tail=tail.replace(old,new)
tail=tail.replace("[q.category,q.course,q.question,q.context,","[q.category,q.course,q.year,q.session,q.sourceNumber,q.question,q.context,")
# All exports obey the same correction-only rule, in both profiles.
tail=tail.replace(",commentaires:!isCorrected(q)?undefined:q.reviewNotes","")
tail=tail.replace("numero:q.id,theme:q.category,reponses:","commentaires:isCorrected(q)?q.reviewNotes:undefined,numero:q.id,theme:q.category,reponses:")
tail=tail.replace("corrige:perQuestionCorrection()&&!isCorrected(q)?null:","corrige:!isCorrected(q)?null:")
tail=tail.replace("erreurs:perQuestionCorrection()&&!isCorrected(q)?null:","erreurs:!isCorrected(q)?null:")
tail=tail.replace("points:perQuestionCorrection()&&!isCorrected(q)?null:","points:!isCorrected(q)?null:")
tail=tail.replace("remarque_corrige:q.pharmaReviewed&&!isCorrected(q)?undefined:q.warning||undefined","remarque_corrige:!isCorrected(q)||q.reviewWarningCovered||q.pharmaWarningCovered?undefined:q.warning||undefined")
event='''$('#pharma-catalog-search').addEventListener('input',renderPharmaCatalog);
document.addEventListener('click',e=>{
 const result=e.target.closest('[data-pharma-bank]');if(!result)return;
 const bank=result.dataset.pharmaBank,id=Number(result.dataset.pharmaQ);
 if(!EXAMS[bank]||EXAMS[bank].ue!=='ue4'||!EXAMS[bank].questions.some(q=>q.id===id))return;
 switchExam(bank);$('#pharma-catalog').open=false;jumpTo(id);
});
'''
assert 'loadExam();renderTabs();render();'in tail
tail=tail.replace('loadExam();renderTabs();render();',event+'\nloadExam();renderTabs();render();',1)
assert 'function pharmaReviewHtml'not in tail and 'if(done)details=details.replace' in tail
html=prefix+json.dumps(E,ensure_ascii=False,separators=(',',':'))+';\n'+tail
(SITE/'index.html').write_text(html)
(P/'current_exams.json').write_text(json.dumps(E,ensure_ascii=False))
(P/'current_runtime.js').write_text(html.split('<script>')[1].split('</script>')[0].split('const EXAM_ORDER=')[1])

audit=SITE/'audit/revision_v4';audit.mkdir(parents=True,exist_ok=True)
all_keys={(b,q['id'])for b,e in E.items()for q in e['questions']}
cover_keys={(c['bank'],c['id'])for c in coverage}
missing_coverage=sorted(all_keys-cover_keys);extra_coverage=sorted(cover_keys-all_keys)
missing_refs=[{'note':n['noteId'],'file':r['file']}for n in notes for r in n['refs']if r.get('unresolvedFile')]
missing_refs.extend({'proof':True,'file':r['file']}for r in proof_refs if r.get('unresolvedFile'))
stats={'questionCount':len(all_keys),'bankCount':len(E),'items':sum(len(q['options'])for e in E.values()for q in e['questions']),'notes':len(notes),'questionsWithNotes':len({(n['bank'],n['id'])for n in notes}),'notesByKind':dict(collections.Counter(n['kind']for n in notes)),'patchedQuestions':len({(c['bank'],c['id'])for c in changes if 'sourceId'not in c}),'changedKeys':sum('answer'in c.get('fields',{})for c in changes),'additions':len(additions),'pharmaReclassifications':len(load('pharma/changes.json',[])),'pharmaQuestions':len(by_source),'coverageQuestions':len(cover_keys),'missingCoverage':missing_coverage,'extraCoverage':extra_coverage,'missingReferences':missing_refs,'referenceResolutionChoices':reference_warnings,'unresolvedDecisions':unresolved}
for filename,data in [('annotations.json',notes),('couverture.json',coverage),('reparations.json',changes),('ajouts.json',additions),('references.json',source_map),('statistiques.json',stats)]:
 (audit/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2))
for f in ['missing_audit.json','fresh_subject_inventory.json','changes.json','relatedThemes.json']:
 shutil.copy2(P/'pharma'/f,audit/('pharmaco_'+f))
(audit/'figures_verifiees.json').write_text(json.dumps(figure_reviews,ensure_ascii=False,indent=2))
(P/'build_stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in stats.items()if k not in ['referenceResolutionChoices','missingCoverage','unresolvedDecisions']},ensure_ascii=False,indent=2))
print('Missing coverage:',len(missing_coverage),'reference choices:',len(reference_warnings),'decisions:',len(unresolved))
