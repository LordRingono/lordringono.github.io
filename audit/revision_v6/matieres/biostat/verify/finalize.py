import json,hashlib,math,shutil,re
from pathlib import Path
from collections import Counter
V=Path(__file__).parent;P=V.parent/'prepare';WS=V.parents[3]
def read(p):return json.loads(p.read_text())
def save(n,d):(V/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
R=read(V/'working_reviewed.json');C=read(V/'working_crops.json');Pre=read(P/'reviewed.json');F=read(V/'final_source_comparison.json');N=read(V/'native_comparison.json');M=read(V/'asset_manifest.json');A=read(P/'asset_audit.json');rep=read(V/'repairs.json');cr=read(V/'crop_repairs.json');changes=read(P/'changes.json');B=read(V/'bitmap_comparison.json')
CM={(x['bank'],x['id']):x for x in C};FM={(x['bank'],x['id']):x for x in F};NM={(x['bank'],x['id']):x for x in N}
rows={
'2025-2026.s1':(494,'ABD B CD AD BD ACD A ABC BC ABC AC BE'),
'2024-2025.s1':(512,'ACE BCD E CE AD BC C DE ABCD BDE BCE ABDE'),
'2024-2025.s2':(526,'C B BCD ABCE CD C ABD'),
'2023-2024.s1':(540,'B CD ABE BD E ADE ADE AD BCDE ABC BCE BC'),
'2023-2024.s2':(554,'D E B D B ABCDE AB'),
'2022-2023.s1':(566,'D A C C BCE BD E ABDE BCD BE AC ADE'),
'2022-2023.s2':(582,'B BD AD B CD ABCD CD'),
'2021-2022.s1':(594,'ACE BD CDE ACE ACE BC BCD DE BCD D AE'),
'2021-2022.s2':(608,'ADE C BCD BC AD BCDE ADE'),
'2020-2021.paces':(624,'ACE AD ABCD BDE BCE AC CD BCD ABCD BD AD'),
'2020-2021.s1':(640,'DE AD BDE CDE BD ABC CE ACD ACDE ABE BDE'),
'2020-2021.s2':(656,'ACD BD ACDE BCD BCD AD AB'),
'2019-2020.paces':(672,'BCD ABCD BD AE ADE BCD BD ABD ADE AE AC'),
'2018-2019.paces':(690,'BDE ABCD CD E BDE C BDE BCD AD BC ABCD')}
codeValues={('annales.ue3.2019-2020.paces',2):{'tablePage':662,'value':'0,62','code':'ABCD','calculation':'2 × (1 − arrondi[Phi(0,5), 2 décimales]) = 2 × (1 − 0,69) = 0,62'},('annales.ue3.2019-2020.paces',4):{'tablePage':663,'value':'−1,67','code':'AE','calculation':'(133 − 135) / (sqrt(36) / sqrt(25)) = −1,6666… → −1,67'},('annales.ue3.2018-2019.paces',2):{'tablePage':684,'value':'21,4','code':'ABCD','calculation':'20 + 2 × 6 / sqrt(81) = 21,3333… ; arrondi extérieur au dixième → 21,4'}}
coverage=[];grid_check=[];notes_before=[];notes_after=[];keys=[];banks=[]
for bank,b in R['banks'].items():
 old=Pre['banks'][bank];assert [q['id'] for q in b['questions']]==[q['id'] for q in old['questions']]
 page,ks=rows[bank.removeprefix('annales.ue3.')];ks=ks.split();assert len(ks)==len(b['questions'])
 bc={'bank':bank,'questions':len(ks),'items':len(ks)*5,'gridPage':page,'firstSubjectPage':min(q['subjectPage'] for q in b['questions']),'lastCorrectionPage':max(c['page'] for q in b['questions'] for c in CM[(bank,q['id'])]['correction']),'graded':0,'ungraded':0}
 for q,oq,k in zip(b['questions'],old['questions'],ks):
  ident=(bank,q['id']);c=CM[ident];f=FM[ident];n=NM[ident];key=q['answer'] or q.get('rawAnswer','');assert key==k,(bank,q['id'],key,k)
  assert q['answer']==oq['answer'];assert q['options']==oq['options'];assert q['weight']==oq['weight']
  assert c['subject'] and c['correction'];assert all(Path(p['file']).exists() for role in ['subject','correction'] for p in c[role])
  assert 'answerIsEmpty' not in q
  for sc in q.get('sharedContexts',[]):assert q['id'] in sc['questionNumbers']
  if q['answer']:bc['graded']+=1
  else:bc['ungraded']+=1
  notes_before.extend(oq.get('reviewNotes',[]));notes_after.extend(q.get('reviewNotes',[]));keys.append((bank,q['id'],key))
  grid_check.append({'bank':bank,'id':q['id'],'page':page,'literalKey':k,'runtimeKey':q['answer'],'match':True,'ungraded':not bool(q['answer'])})
  itemrows=[]
  for o in q['options']:
   l=o['id'];nr=next(i for i in n['items'] if i['letter']==l);fr=next(i for i in f['items'] if i['letter']==l);code=ident in codeValues
   if code:
    status='verified_numeric_code_letter';assert k==codeValues[ident]['code'];proof=codeValues[ident]
   elif o.get('image'):
    status='verified_authentic_image_item';aa=next(a for a in A if a['src']==o['image']);proof={'sourcePage':aa['page'],'rect':aa['rect'],'src':o['image'],'method':'PDF source pages visually reviewed; individual bitmap compared against 2× source crop and original SHA manifest.'}
   else:
    status='verified_text_against_original';assert nr['comparison']=='identical_normalized';proof={'sourceText':nr['source'],'siteText':o['text'],'normalization':'Only typography and whitespace; stricter numeric-sign comparison separately passed.'}
   verdict=fr['detail_verdict']
   if not code:assert verdict in ['VRAI','FAUX']
   itemrows.append({'id':l,'subjectStatus':status,'subjectEvidence':proof,'correctedSubjectStatus':'numeric_table_no_proposition' if code else 'authentic_image_compared' if o.get('image') else 'same_after_typographic_normalization' if fr['subject_correction_identical'] else 'original_printed_difference_preserved','originalCorrectionVerdict':verdict if not code else None,'officialGridIncluded':l in k,'gridAndDetailAgree':None if code else verdict==('VRAI' if l in k else 'FAUX'),'correctionDetailStatus':'shared_numeric_calculation_in_authentic_copy' if code else 'verdict_and_detail_compared_in_source','renderedDetail':q.get('explanations',{}).get(l,''),'formulaCopyAvailable':bool(q.get('correctionImages')),'reviewNotes':[a['noteId'] for a in q.get('reviewNotes',[]) if l in a.get('items',[])]})
  coverage.append({'bank':bank,'id':q['id'],'questionCompared':True,'sourceContextCompared':True,'subjectPages':sorted(set(p['page'] for p in c['subject'])),'correctionPages':sorted(set(p['page'] for p in c['correction'])),'gridPage':page,'officialGridKey':k,'runtimeKey':q['answer'],'graded':bool(q['answer']),'subjectCopy':'present_clean','correctionCopy':'present','subjectPanels':len(c['subject']),'correctionPanels':len(c['correction']),'sharedContexts':[s['id'] for s in q.get('sharedContexts',[])],'allReferencedImagesAudited':True,'sourceSubjectPagesVisuallyReviewed':True,'items':itemrows,'reviewNotes':[n['noteId'] for n in q.get('reviewNotes',[])]})
 banks.append(bc)
assert len(coverage)==138 and sum(len(x['items']) for x in coverage)==690
assert sum(x['graded'] for x in coverage)==136
assert set(n['noteId'] for n in notes_before).issubset(set(n['noteId'] for n in notes_after))
assert len(notes_before)==53 and len(notes_after)==54
assert len(M)==167 and len(set(a['src'] for a in M))==167
for a in M: assert Path(a['file']).exists() and a['src'].startswith('static/revision_v6/biostat/')
def assets(v):
 if isinstance(v,str):
  if v.startswith('static/') and re.search(r'\.(?:webp|png|jpg|jpeg)$',v):yield v
 elif isinstance(v,list):
  for a in v:yield from assets(a)
 elif isinstance(v,dict):
  for a in v.values():yield from assets(a)
allassets=list(assets(R));newmap={a['src']:Path(a['file']) for a in M}
for a in allassets:assert (newmap.get(a) or WS/'output/site'/a).exists(),a
summary={'banks':14,'questionsCompared':138,'ordinaryPropositionsCompared':675,'textPropositionsCompared':595,'imagePropositionsCompared':80,'numericCodeQuestions':3,'numericCodeLettersCompared':15,'responseLettersTotal':690,'originalCorrectionVerdictsCompared':675,'ordinaryRepeatedSubjectTextExactAfterTypography':593,'ordinaryRepeatedSubjectTextPrintedDifferences':2,'ordinaryGridDetailConflicts':2,'graded':136,'ungraded':2,'subjectPanels':183,'correctionPanels':218,'cleanSubjectCopies':138,'annotatedSubjectCopies':0,'missingSubjectCopies':0,'missingCorrectionCopies':0,'subjectPagesVisuallyReviewedInContactSheets':57,'annexPagesVisuallyReviewedInContactSheets':8,'originalUniqueAssetsBitmapCompared':492,'originalAssetUses':957,'finalUniqueAssets':len(set(allassets)),'finalAssetUses':len(allassets),'newAuthenticAssets':len(M),'existingNotesPreserved':53,'existingNotesAmendedWithEvidence':1,'newScientificNotes':1,'totalReviewNotes':54,'restoredTextExplanations':10,'restoredCorrectionPanels':1}
save('coverage.json',{'status':'complete_with_explicit_source_limitations','reviewer':'independent_verifier_biostat','summary':summary,'banks':banks,'questions':coverage,'scopeLimit':'The 14 biostatistics series present on the site and in compilation pp.487–698; this is not a claim that every possible university exam since 2015 was supplied.','visualMethod':'All 57 subject pages and 8 appendix pages viewed as legible page contact sheets, with full-size follow-ups on sensitive graphics; targeted correction crops viewed. All 492 original unique assets digitally compared, not all individually visually opened.'})
save('grid_check.json',grid_check);save('numeric_codes.json',[{'bank':b,'id':n,**v} for (b,n),v in codeValues.items()])
save('missing.json',read(P/'missing.json'))
notes_changes=[]
old_notes={n['noteId']:n for n in notes_before}
for n in notes_after:
 if n['noteId'] not in old_notes:notes_changes.append({'type':'added','note':n})
 elif n!=old_notes[n['noteId']]:notes_changes.append({'type':'amended','before':old_notes[n['noteId']],'after':n})
remaining=[{'bank':'annales.ue3.2022-2023.s1','id':5,'status':'ungraded_source_conflict','grid':'BCE','detail':'ACE','pages':[561,566,570],'resolution':'Official erratum or course arbitration needed; no fabricated key.'},{'bank':'annales.ue3.2023-2024.s1','id':2,'status':'ungraded_source_conflict','grid':'CD','pages':[534,540,542],'resolution':'The official detail marks two different upper bounds true; original calculation is inconsistent with the key. No unique replacement key asserted.'}]
save('issues.json',{'status':'no_unresolved_import_blocker_after_approved_changes','independentRepairs':rep,'copyBoundaryRepairs':cr,'preparerBoundaryRepairsIndependentlyReviewed':[x for x in changes if x['type']=='correction_boundary'],'remainingSourceConflicts':remaining,'scientificNoteChanges':notes_changes,'originalRepeatedSubjectDifferences':read(V/'corrected_subject_differences.json'),'notes':'Official keys are unchanged by the verifier. The two existing ungraded conflicts remain ungraded. No verdict, invented explanation or scientific annotation is added to an uncorrected proposition.'})
visual={'subjectContactSheets':[f'visual/subjects_{i:02}.jpg' for i in range(15)],'subjectPageCount':57,'annexContactSheets':['visual/annexes_0.jpg','visual/annexes_1.jpg'],'annexPages':[619,620,621,622,667,668,669,670],'fullSourcePagesViewed':[488,656],'beforeRepairTopBoundaryStripSamples':15,'finalPanelSamplesViewed':4,'finalPanelSampleFile':'visual/final_panel_samples.jpg','correctedAssetFilesIndividuallyViewed':['verified_annales_ue3_2020-2021_s2_q01_correction_p656.webp','verified_annales_ue3_2022-2023_s1_q05_correction_p570.webp','verified_annales_ue3_2024-2025_s1_q04_correction_p515.webp','verified_annales_ue3_2023-2024_s1_q09_correction_p546.webp','verified_annales_ue3_2020-2021_paces_q08_correction_p630.webp','verified_annales_ue3_2023-2024_s1_q02_correction_p542.webp','verified_annales_ue3_2024-2025_s1_q10_correction_p519.webp','verified_annales_ue3_2023-2024_s2_q01_correction_p555.webp','verified_annales_ue3_2019-2020_paces_annexes_p670.webp'],'additionalOriginalAssetsIndividuallyViewed':['static/annales_ue3_2024-2025_s2_q05_context_p523.webp','static/annales_ue3_2024-2025_s2_q04_context_p522.webp','static/annales_ue3_2019-2020_paces_annexes_p670.webp'],'disclaimer':'Rendering a file alone is not treated as visual review. Not every one of the 492 original image assets was viewed separately.'}
save('visual_log.json',visual)
save('primary_sources_consulted.json',[{'url':'https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/conflimi.htm','publisher':'NIST','verified':'Mean confidence interval and inverse square-root dependence on n.'},{'url':'https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm','publisher':'NIST','verified':'Binomial mean, standard deviation and parameter estimation.'},{'url':'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pointbiserialr.html','publisher':'SciPy official documentation','verified':'Point-biserial correlation and Pearson/t-test equivalence; the isolated n−1 typo in a prose line is not used.'},{'url':'https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm','publisher':'NIST','verified':'Median formula based on ordered ranks.'},{'url':'https://openstax.org/books/introductory-statistics-2e/pages/2-3-measures-of-the-location-of-the-data','publisher':'OpenStax, Rice University','verified':'Median and quartiles, equality at quantiles and empirical-rank conventions.'}])
shutil.copyfile(V/'working_reviewed.json',V/'approved_reviewed.json');shutil.copyfile(V/'working_crops.json',V/'approved_crops.json')
assets_check=[{**a,'sha256':sha(Path(a['file']))} for a in M];save('asset_integrity.json',assets_check)
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('REVIEWED',sha(V/'approved_reviewed.json'));print('CROPS',sha(V/'approved_crops.json'));print('MANIFEST',sha(V/'asset_manifest.json'))
