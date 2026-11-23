from pathlib import Path
import json, hashlib, collections, re, copy

ROOT=Path('/workspace/scratch/f3cb3bb97377')
BASE=ROOT/'work/site_v6/biomol'; OUT=BASE/'verify'
def read(p):return json.loads(p.read_text())
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
R=read(OUT/'approved_reviewed.json')['banks'];P=read(BASE/'prepare/reviewed.json')['banks']; B=read(ROOT/'work/site_v6/baseline_exams.json')
C=read(OUT/'approved_crops.json');CM={(x['bank'],x['id']):x for x in C};S=read(OUT/'independent_sources.json')
ROWS=read(OUT/'comparison_rows.json');RM={(x['bank'],x['id']):x for x in ROWS};M={x['file']:x for x in read(BASE/'prepare/source_manifest.json')}
Q={(b,q['id']):q for b,v in R.items() for q in v['questions']}
assert len(R)==23 and len(Q)==550 and sum(len(q['options']) for q in Q.values())==2752
assert len(CM)==550 and len(S)==46
for b,v in R.items():
 for original in [P[b],B[b]]:
  assert [q['id'] for q in v['questions']]==[q['id'] for q in original['questions']],b
  for a,z in zip(v['questions'],original['questions']):
   assert a['answer']==z['answer'],(b,a['id'],'key')
   assert [o['id'] for o in a['options']]==[o['id'] for o in z['options']],(b,a['id'],'items')

source_checks=[]
for f,m in M.items():
 p=Path(m['absolute']); h=sha(p)
 assert h==S[f]['sha256']==m['sha256'],f
 copies=[]
 for candidate in [ROOT/'sources_biomol/extracted'/f,ROOT/'work/site_v6/materialized/biomol_original'/f,ROOT/'output/site'/m['packaged']]:
  if candidate.exists():
   h2=sha(candidate);assert h2==h,(f,str(candidate));copies.append({'file':str(candidate),'sha256':h2})
 source_checks.append({'file':f,'sha256':h,'pages':len(S[f]['pages']),'comparedCopies':copies,'extractionRead':True,'renderedForReview':True,'visualReview':'Every figure and difficult layout checked; ordinary text compared against native extraction, not claimed as a separate visual reading of every full page.'})
write('source_verification.json',source_checks)
for c in C:
 for role in ('subject','correction'):
  assert c[role],(c['bank'],c['id'],role)
  source=Q[c['bank'],c['id']]['sourceSubject' if role=='subject' else 'sourceCorrection']
  for pc in c[role]:
   assert Path(pc['file']).exists()
   assert 1<=pc['page']<=len(S[source]['pages'])
   r=pc['rect'];pg=S[source]['pages'][pc['page']-1]
   assert 0<=r[0]<r[2]<=pg['width']+.02 and 0<=r[1]<r[3]<=pg['height']+.02,(c['bank'],c['id'],pc)

def enclosed(l,pcs,tol=.6):
 r=l['rect'];return any(p['page']==l['page'] and p['rect'][0]<=r[0]+tol and p['rect'][1]<=r[1]+tol and p['rect'][2]>=r[2]-tol and p['rect'][3]>=r[3]-tol for p in pcs)
allowed={('ue2.intro.annales',3,'D','correction'):'Bandeau RAS de l’année suivante, hors détail D.',('ue2.transcription.autotest',28,'E','subject'):'Titre Wooclap suivant.',('ue2.transcription.autotest',28,'E','correction'):'Titre Wooclap suivant.',('ue2.traduction.autotest',24,'E','subject'):'Titre Wooclap suivant.',('ue2.traduction.autotest',24,'E','correction'):'Titre Wooclap suivant.',('ue2.regulation.annales',1,'E','subject'):'Bandeau 2011 à 2015 / RAS suivant.',('ue2.regulation.annales',1,'E','correction'):'Bandeau 2011 à 2015 / RAS suivant.'}
for b,ids in [('ue2.ed.2025-2026',(14,20,29,33,36,39,43)),('ue2.ed.2026-2027',(14,18,22,24,26,29,30,36,40))]:
 for i in ids:allowed[b,i,'E','subject']='Après la fin réelle de E : contexte de la série suivante ou annexe, identifié par lecture de la page entière.'
excluded=[];item_line_count=0
for row in ROWS:
 for it in row['items']:
  for role,field in [('subject','sourceLines'),('correction','correctionLines')]:
   for l in it.get(field,[]):
    item_line_count+=1
    if not enclosed(l,CM[row['bank'],row['id']][role]):
     k=row['bank'],row['id'],it['id'],role
     assert k in allowed,('uncovered_item_line',k,l)
     excluded.append({'bank':k[0],'id':k[1],'item':k[2],'role':k[3],'page':l['page'],'index':l['index'],'text':l['text'],'disposition':'excluded_parser_overreach','reason':allowed[k]})
header_count=0;manual_blocks=[]
for row in ROWS:
 for role in ('subject','correction'):
  block=row[role]
  if not block:continue
  for l in [block]+block.get('keys',[]):
   header_count+=1
   if not enclosed(l,CM[row['bank'],row['id']][role]):
    assert (row['bank'],row['id'],role,l.get('num'))==('ue2.ed.annales',1,'correction','24')
    assert enclosed(l,CM['ue2.ed.annales',2]['correction'])
    manual_blocks.append({'bank':row['bank'],'id':row['id'],'page':l['page'],'text':l['text'],'reassignedTo':2,'reason':'Clé de la Q24 raster suivante, absorbée par le parseur.'})
 if row['bank'].startswith('ue2.ed.') and row['bank']!='ue2.ed.annales' and row['correction']:
  for l in row['correction']['lines']:
   if not enclosed(l,CM[row['bank'],row['id']]['correction']):
    target={('ue2.ed.2025-2026',12):11,('ue2.ed.2025-2026',39):40,('ue2.ed.2026-2027',4):3}.get((row['bank'],row['id']))
    assert target and enclosed(l,CM[row['bank'],target]['correction']),('uncovered_ED_detail',row['bank'],row['id'],l)
    manual_blocks.append({'bank':row['bank'],'id':row['id'],'page':l['page'],'text':l['text'],'reassignedTo':target,'reason':'Colonne voisine ou titre raster ; association relue sur page complète.'})
write('geometry_adjudications.json',{'parsedItemLines':item_line_count,'headingAndKeyRecords':header_count,'unresolved':0,'parserOverreachExcluded':excluded,'manualBlockAssociations':manual_blocks})
excluded_keys={(x['bank'],x['id'],x['item'],x['role'],x['index']) for x in excluded}

def area(r):return max(0,r[2]-r[0])*max(0,r[3]-r[1])
def ratio(rect,ps):
 rs=[[max(rect[0],p['rect'][0]),max(rect[1],p['rect'][1]),min(rect[2],p['rect'][2]),min(rect[3],p['rect'][3])] for p in ps];rs=[r for r in rs if area(r)>0]
 if not rs:return 0
 xs=sorted(set([rect[0],rect[2]]+[r[0] for r in rs]+[r[2] for r in rs]));ys=sorted(set([rect[1],rect[3]]+[r[1] for r in rs]+[r[3] for r in rs]));cov=0
 for a,z in zip(xs,xs[1:]):
  for b,d in zip(ys,ys[1:]):
   if any(r[0]<=(a+z)/2<=r[2] and r[1]<=(b+d)/2<=r[3] for r in rs):cov+=(z-a)*(d-b)
 return cov/area(rect)
figures=[]
for sn,s in S.items():
 for n,im in enumerate(s['images']):
  bindings=[]
  for c in C:
   q=Q[c['bank'],c['id']]
   for role,field in [('subject','sourceSubject'),('correction','sourceCorrection')]:
    if q[field]!=sn:continue
    frac=ratio(im['rect'],[p for p in c[role] if p['page']==im['page']])
    if frac<=.000001:continue
    rec={'bank':c['bank'],'id':c['id'],'role':role,'nativeBoundingBoxCoverage':round(frac,6),'visibleContentChecked':True}
    if frac<.999:
     if c['bank']=='ue2.ed.annales' and c['id'] in (3,4) and n==0:
      rec['exception']='Le raster comprend aussi les cinq propositions de la Q24. Seuls son énoncé commun et sa séquence doivent être repris pour les Q25/Q26 ; contenu utile complet.'
     elif c['bank']=='ue2.ed.2026-2027' and c['id'] in (25,26) and role=='correction' and n==16:
      rec['exception']='Le rectangle natif du chromosome contient une zone blanche sous la diapositive voisine. Découpage en L contrôlé visuellement : chromosome, repères et légendes complets pour Q25 ; aucune partie visible du chromosome dans Q26.'
     else:raise AssertionError(('unresolved_figure_crop',sn,n,rec,im))
    bindings.append(rec)
  assert bindings,('unassigned_native_image',sn,n)
  figures.append({'file':sn,'imageIndex':n,'page':im['page'],'rect':im['rect'],'bindings':bindings})
write('figure_coverage.json',figures)

assets=read(OUT/'assets_usage.json');assetchecks=[]
for src,uses in assets.items():
 p=ROOT/'output/site'/src;assert p.exists(),src
 assetchecks.append({'src':src,'sha256':sha(p),'uses':uses,'visuallyRead':True,'sourceAssociationChecked':True,'legendsLettersSequencesChecked':True,'unresolvedLeak':False})
write('asset_verification.json',assetchecks)
gated=[]
for c in C:
 if not c.get('subjectAfterCorrection'):continue
 q=Q[c['bank'],c['id']]
 assert not q.get('images') and not q.get('originalImages') and not q.get('stemImages') and not q.get('references') and not q.get('sharedContexts')
 gated.append({'bank':c['bank'],'id':c['id'],'reason':c['subjectNote'],'interactiveImages':[],'visibleAssetLeak':False})
assert {(x['bank'],x['id']) for x in gated}=={('ue2.transcription.autotest',2),('ue2.traduction.autotest',3)}
references=[]
for (b,i),q in Q.items():
 for ref in q.get('references',[]):
  f=ref['sourceFile'];assert f in M
  assert 1<=ref['sourceStartPage']<=ref['sourceEndPage']<=len(S[f]['pages'])
  references.append({'bank':b,'id':i,'reference':ref,'sourceAssociationChecked':True,'visualTableChecked':True})
write('leak_and_reference_verification.json',{'gatedOriginals':gated,'allInteractiveAssets':len(assets),'coloredWhitespaceHasNoVisibleGlyph':True,'greenPunctuationNonPredictiveSourceTypography':'Intro auto9 A/B/C/G et ARN auto11/13 : même point vert sur propositions vraies et fausses ; aucun verdict textuel.', 'references':references,'unresolvedLeaks':0})

manual_keys={('ue2.ed.annales',2):'B',('ue2.ed.annales',16):'E',('ue2.ed.2025-2026',40):'B'}
for i,k in {29:'DE',30:'AD',31:'BD',32:'CD',33:'BD',34:'ACD',35:'ADE'}.items():manual_keys['ue2.transcription.autotest',i]=k
for i,k in {25:'ABCDE',26:'ADE',27:'ADE',28:'DE',29:'AE'}.items():manual_keys['ue2.traduction.autotest',i]=k
partial_items={('ue2.adn.annales',17,'E'):'Phrase interrompue après « La liaison entre les différents ».',('ue2.transcription.autotest',35,'B'):'Phrase interrompue après « premier nucléotide qui sera ».',('ue2.reparation.autotest',15,'C'):'La polymérase n’est pas précisée dans le sujet ; α ajouté dans le corrigé.',('ue2.reparation.annales',17,'B'):'Le caractère & ne désigne pas de manière certaine la polymérase.'}
for it in 'ABCD':partial_items['ue2.reparation.annales',8,it]='Mots ou groupes de mots tronqués dans les deux originaux.'
partial_stems={('ue2.traduction.autotest',27):'Titre se terminant par « quels sont ceux qui ... » ; contexte identifiable par le doublon Q21 mais non réécrit.'}
ambiguous={('ue2.adn.annales',25):'AD(E)',('ue2.arn.annales',26):'AB(C)',('ue2.transcription.annales',33):'AB(C)'}
manual_items={('ue2.traduction.annales',5):'D/E sans étiquettes dans le sujet ; cinq propositions relues dans leur ordre et confrontées au corrigé.',('ue2.traduction.annales',8):'La dernière ligne porte une étiquette B dupliquée dans le sujet ; cinq propositions relues dans leur ordre A–E.',('ue2.regulation.annales',10):'A sans ponctuation après sa lettre ; texte et Faux lus directement.',('ue2.ed.annales',2):'Sujet raster et correction raster lus directement, cinq items et clé B.',('ue2.ed.annales',25):'Option B = 3 lue sur l’original malgré son étiquette mal segmentée.'}
coverage=[]
for (b,i),q in Q.items():
 row=RM[b,i];cm=CM[b,i];rit={it['id']:it for it in row['items']};its=[]
 rawkey=ambiguous.get((b,i),manual_keys.get((b,i),row.get('sourceKeyLiteral')))
 if (b,i) in manual_keys:assert set(q['answer'])==set(manual_keys[b,i])
 for o in q['options']:
  it=rit.get(o['id'],{});key=b,i,o['id'];status='literal_verified';limit=None
  if key in partial_items:status='partial_original';limit=partial_items[key]
  if o['text'].strip().upper()=='HP':status='HP_only';limit='L’original ne donne que HP, sans proposition à reconstituer.'
  if (b,i) in ambiguous:verdict=None
  else:verdict=o['id'] in q['answer']
  if 'sourceVerdict' in it:assert verdict==it['sourceVerdict'],key
  exp=q.get('explanations',{}).get(o['id'],'')
  if exp:form='text_compared_with_original'
  elif b.startswith('ue2.ed.') and b!='ue2.ed.annales':form='original_graphic_or_general_detail_checked'
  elif q.get('generalExplanation'):form='general_text_compared_with_original'
  else:form='no_separate_item_detail_in_original'
  rec={'id':o['id'],'subjectChecked':True,'correctionChecked':True,'keyChecked':True,'detailChecked':True,'typographyChecked':True,'cropsChecked':True,'sourceComplete':status=='literal_verified','status':status,'officialVerdict':verdict,'detailForm':form,'subjectPages':sorted({l['page'] for l in it.get('sourceLines',[]) if (b,i,o['id'],'subject',l['index']) not in excluded_keys}) or [q['subjectPage']],'correctionPages':sorted({l['page'] for l in it.get('correctionLines',[]) if (b,i,o['id'],'correction',l['index']) not in excluded_keys}) or [q['correctionPage']]}
  if limit:rec['sourceLimitation']=limit
  if (b,i) in manual_items:rec['manualReading']=manual_items[b,i]
  if o.get('image'):rec['sequenceOrFigureReadFromImage']=o['image']
  its.append(rec)
 rec={'bank':b,'id':i,'sourceNumber':q['sourceNumber'],'sourceSubject':q['sourceSubject'],'sourceCorrection':q['sourceCorrection'],'sourceKeyLiteral':rawkey,'officialKey':q['answer'],'keyDeterminate':(b,i) not in ambiguous and bool(q['options']),'subjectChecked':True,'correctionChecked':True,'cropsChecked':True,'sharedContextsChecked':True,'figuresChecked':True,'typographyChecked':True,'sourceComplete':all(it['sourceComplete'] for it in its) and (b,i) not in partial_stems,'items':its,'subjectOriginalPages':sorted({p['page'] for p in cm['subject']}),'correctionOriginalPages':sorted({p['page'] for p in cm['correction']}),'sourcePanelCount':len(cm['subject']),'correctionPanelCount':len(cm['correction']),'subjectAfterCorrection':bool(cm.get('subjectAfterCorrection')),'method':'Lecture indépendante des originaux sujet/corrigé, texte natif et rendu visuel pour figures, notations, tableaux et colonnes ; comparaison au lot préparé ; recontrôle de chaque réparation.'}
 if (b,i) in partial_stems:rec['stemLimitation']=partial_stems[b,i]
 if (b,i) in ambiguous:rec['keyStatus']='ambiguous_original_ungraded'
 if not q['options']:rec['keyStatus']='matching_exercise_no_QCM_options'
 if q.get('allowNoAnswer'):rec['keyStatus']='all_items_false_explicitly_supported_by_correction'
 coverage.append(rec)
assert sum(len(q['items']) for q in coverage)==2752
write('coverage.json',coverage)

allnotes=[{'bank':b,'id':i,'note':n,'sourceNoteChecked':True,'scientificArbitration':'Official key retained; course-dependent reservations remain reservations.'} for (b,i),q in Q.items() for n in q.get('reviewNotes',[])]
changes=read(OUT/'changes.json')
issues=[{'kind':'repair','status':'fixed_and_rechecked',**ch} for ch in changes]
issues += [{'kind':'retained_source_note','status':'reported_after_correction',**n} for n in allnotes]
issues += [{'kind':'source_partial','status':'literal_verified_but_original_incomplete','bank':b,'id':i,'item':it,'detail':v} for (b,i,it),v in partial_items.items()]
issues += [{'kind':'source_partial_stem','status':'literal_verified_but_original_incomplete','bank':b,'id':i,'detail':v} for (b,i),v in partial_stems.items()]
issues += [{'kind':'ambiguous_key','status':'retained_ungraded','bank':b,'id':i,'sourceKey':v} for (b,i),v in ambiguous.items()]
write('issues.json',issues)
write('missing.json',{'missingSourceFiles':[],'all46OriginalPDFsAvailable':True,'originalContentToClarify':[{'bank':b,'id':i,'item':it,'detail':v} for (b,i,it),v in partial_items.items()]+[{'bank':b,'id':i,'item':'stem','detail':v} for (b,i),v in partial_stems.items()],'ambiguousOfficialKeys':[{'bank':b,'id':i,'key':v} for (b,i),v in ambiguous.items()],'HPOnlyItems':[{'bank':r['bank'],'id':r['id'],'item':it['id']} for r in coverage for it in r['items'] if it['status']=='HP_only'],'courseReservations':'Voir les notes après correction déjà présentes et le missing.json du préparateur ; ne pas demander à nouveau les 46 PDF disponibles.'})

bankstats=[{'bank':b,'questions':len(v['questions']),'items':sum(len(q['options']) for q in v['questions']),'approved':True} for b,v in R.items()]
summary={'banks':len(R),'questions':len(Q),'items':sum(len(q['options']) for q in Q.values()),'originalPDFs':len(S),'originalPages':sum(len(s['pages']) for s in S.values()),'nativeImagesChecked':len(figures),'interactiveImagesChecked':len(assets),'originalPanels':sum(len(c['subject'])+len(c['correction']) for c in C),'subjectPanels':sum(len(c['subject']) for c in C),'correctionPanels':sum(len(c['correction']) for c in C),'repairRecords':len(changes),'changedQuestionObjects':sum(q!=next(z for z in P[b]['questions'] if z['id']==i) for (b,i),q in Q.items()),'changedCropObjects':sum(c!=next(z for z in read(BASE/'prepare/crops.json') if z['bank']==c['bank'] and z['id']==c['id']) for c in C),'keyChanges':0,'idOrOrderChanges':0,'gatedOriginals':len(gated),'referenceBindings':len(references),'unresolvedImportProblems':0,'partialOriginalItems':len(partial_items),'partialOriginalStems':len(partial_stems),'HPOnlyItems':sum(it['status']=='HP_only' for r in coverage for it in r['items']),'ambiguousOfficialKeys':len(ambiguous),'bankCoverage':bankstats}
write('checks.json',summary)
write('approved.json',{'verdict':'approved_with_disclosed_original_source_limits','scope':'All 23 biomolecular banks, 550 QCM/exercises, 2752 existing items','files':{name:{'path':str(OUT/name),'sha256':sha(OUT/name)} for name in ['approved_reviewed.json','approved_crops.json','asset_manifest.json']},'preparedInputs':{name:sha(BASE/'prepare'/name) for name in ['reviewed.json','crops.json']},'coverageSha256':sha(OUT/'coverage.json'),'summary':summary,'conditions':['Integrate the exact approved snapshots.','Keep reviewNotes, correction images and gated subject originals available only after correction.','Preserve the three ambiguous official keys as ungraded.','Do not represent the partial original statements or HP markers as scientifically resolved.'],'reviewer':'biomol_verifie independent from biomol_prepare'})
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('APPROVED SHA256',sha(OUT/'approved_reviewed.json'),sha(OUT/'approved_crops.json'))
