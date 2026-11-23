import json,re,unicodedata,hashlib,copy,collections,fitz
from pathlib import Path
R=Path(__file__).resolve().parent
BASE=Path('work/site_v6/baseline_exams.json');B=json.loads(BASE.read_text());KS=json.loads(Path('work/site_v6/roster.json').read_text())['pharmaco']['banks']
S=json.loads((R/'segments.json').read_text());G=json.loads((R/'groups_raw.json').read_text());C=json.loads((R/'crops.json').read_text());CM={r['sourceId']:r for r in C}
PDF=Path('output/site/sources/Annales_compilation.pdf').resolve();DOC=fitz.open(PDF)
QM={q['sourceId']:(k,q) for k in KS for q in B[k]['questions']}
reviewed={'banks':{k:{'questions':copy.deepcopy(B[k]['questions'])} for k in KS}}
changes=[]
candidates=json.loads((R/'citation_candidates.json').read_text())
by_note=collections.defaultdict(list)
for candidate in candidates:by_note[candidate['noteId']].append(candidate)
for k,v in reviewed['banks'].items():
 for q in v['questions']:
  for note in q.get('reviewNotes',[]):
   if note['noteId'] not in by_note:continue
   bad=by_note[note['noteId']];before=copy.deepcopy(note['refs'])
   for candidate in bad:
    # Ensure each explicit, correct counterpart is also present before removing a stale prefix match.
    for year,session,number in candidate['mentions']:
     expected=f'ue4:{year}:{session}:q{number:02}'
     assert any(expected in r.get('label','') for r in before),(note['noteId'],expected)
   note['refs']=[r for r in note['refs'] if not any(r==x['stale'] for x in bad)]
   assert len(before)-len(note['refs'])==len(bad)
   changes.append({'bank':k,'id':q['id'],'sourceId':q['sourceId'],'field':f"reviewNotes[{note['noteId']}].refs",'before':before,'after':note['refs'],'removedRefs':[x['stale'] for x in bad],'reason':'Suppression de renvois obsolètes vers Q1/Q2, ajoutés par une correspondance de préfixe au lieu du numéro complet Q10–Q29 cité dans la note. Les passages originaux ont été rapprochés ; les bonnes références aux numéros complets sont déjà présentes et sont conservées. Texte de la note, identifiant et clé inchangés.'})
for k,v in reviewed['banks'].items():
 for q in v['questions']:
  if q['sourceId']=='ue4:2021-2022:S1:q13':
   before={'correctionPage':q['correctionPage'],'shortCorrectionPage':q['shortCorrectionPage']}
   q['correctionPage']=None;q['shortCorrectionPage']=None
   changes.append({'bank':k,'id':q['id'],'sourceId':q['sourceId'],'field':'correctionPage/shortCorrectionPage','before':before,'after':{'correctionPage':None,'shortCorrectionPage':None},'reason':'Ces anciens pointeurs vers p848 désignaient la grille numérotée selon le corrigé, sans clé pour le sujet Q13. Aucune association à un corrigé n’est possible ; la page reste citée seulement comme preuve de l’omission dans la note.'})
repaired_source_ids={c['sourceId'] for c in changes}
RQM={q['sourceId']:(k,q) for k in KS for q in reviewed['banks'][k]['questions']}
annotated=CM['ue4:2019-2020:S1:q04'];annotated['subjectAfterCorrection']=True;annotated['subjectNote']='La copie originale comporte un ajout manuscrit près des descripteurs QSAR, dont l’interprétation n’est pas certaine. Elle est conservée intacte et proposée après validation. La figure interactive actuelle montre seulement le tableau des molécules, sans cet ajout.'
(R/'reviewed.json').write_text(json.dumps(reviewed,ensure_ascii=False,indent=2));(R/'crops.json').write_text(json.dumps(C,ensure_ascii=False,indent=2));(R/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2));(R/'source_manifest.json').write_text('[]\n');(R/'asset_manifest.json').write_text('[]\n')

# Comparison keeps mathematical operators, signs, units and digits; only spelling accents,
# case, ordinary punctuation and spacing are normalized.
def norm(s):
 s=unicodedata.normalize('NFKC',s).casefold().translate(str.maketrans({'−':'-','–':'-','—':'-','×':'x','⁄':'/','’':"'",'œ':'oe','æ':'ae'}));s=''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch));return re.sub(r'[\s.,;:!?\'"«»“”()\[\]{}]','',s)
def refs(ls):
 return [{'file':str(PDF),'page':l['page'],'rect':[round(x,4) for x in l['rect']],'raw':l['text']} for l in ls]
def image_refs(row):
 out=[]
 for pg in sorted(set(l['page'] for l in row['lines'])):
  lo=min(l['rect'][1] for l in row['lines'] if l['page']==pg);hi=max(l['rect'][3] for l in row['lines'] if l['page']==pg)
  nxt=row.get('nextHeading');hi=nxt['rect'][1] if nxt and nxt['page']==pg else 780
  for im in DOC[pg-1].get_image_info():
   if im['bbox'][2]-im['bbox'][0]>30 and im['bbox'][3]-im['bbox'][1]>30 and im['bbox'][1]>=lo-4 and im['bbox'][1]<hi:
    out.append({'file':str(PDF),'page':pg,'rect':list(im['bbox']),'width':im['width'],'height':im['height']})
 return out

def canon_key(k):
 if k=='AUCUNE':return ''
 if k and re.fullmatch('[ABCDE]+',k):return ''.join(sorted(set(k)))
 return None
fig_ids={sid for sid,(k,q) in QM.items() if q.get('images')}
selected={'ue4:2023-2024:S1:q24','ue4:2025-2026:S1:q13','ue4:2025-2026:S1:q14','ue4:2022-2023:S2:q14','ue4:2023-2024:S1:q02','ue4:2021-2022:S1:q12','ue4:2021-2022:S1:q13','ue4:2021-2022:S1:q14','ue4:2020-2021:PACES:q25','ue4:2020-2021:PACES:q29','ue4:2019-2020:S1:q19','ue4:2020-2021:S2:q10','ue4:2018-2019:S1:q06','ue4:2018-2019:S1:q15','ue4:2019-2020:S1:q25','ue4:2020-2021:S1:q12','ue4:2020-2021:S1:q13','ue4:2020-2021:S1:q14'}
visual_ids=fig_ids|selected
stats=collections.Counter();aud=[];issues=[];inventory=[]
for g in G:
 inventory.append({'year':g['year'],'session':g['session'],'subjectRange':g['ranges']['subject'],'correctionRange':g['ranges']['correction'],'freshSubjectCount':len(g['subject']['headings']),'freshCorrectionCount':len(g['correction']['headings']),'questionHeaders':[{'sourceNumber':h['number'] or h['sequence'],'page':h['page'],'rect':h['rect'],'raw':h['text'],'method':h['kind']} for h in g['subject']['headings']]})
for sid,row in S.items():
 bank,q=QM[sid];s=row['subject'];c=row.get('correction');grid=row.get('grid');crop=CM[sid]
 a={'bank':bank,'id':q['id'],'sourceId':sid,'year':q['year'],'session':q['session'],'sourceNumber':q['sourceNumber'],'source':str(PDF),'subject':{'raw':s['raw'],'stemRaw':s['stem'],'stemDisplayed':q['question']+' '+q['context'],'stemRefs':refs(s['stemLines']),'panels':crop['subject'],'sharedContextRefs':refs(s.get('sharedContextLines',[])),'visualReview':sid in visual_ids,'subjectAfterCorrection':crop.get('subjectAfterCorrection',False)},'correction':None,'items':[],'grading':{'answer':q['answer'],'rawAnswer':q['rawAnswer'],'answerIsEmpty':q.get('answerIsEmpty',False),'graded':bool(q['answer']) or q.get('answerIsEmpty',False),'warning':q['warning'],'warningReview':'revalidated_from_original' if q['warning'] else 'no_preexisting_warning'},'existingReviewNotes':{'count':len(q.get('reviewNotes',[])),'noteIds':[n['noteId'] for n in q.get('reviewNotes',[])],'policy':'Contenus et clés conservés. Les références aux deux cours fournis ont été consultées ; aucune nouvelle conclusion scientifique sans source.','citationRepair':sid in repaired_source_ids},'visualReview':{'subject':sid in visual_ids,'correction':sid in visual_ids and bool(c),'grid':bool(grid),'interactiveImages':bool(q.get('images')),'interactiveImageSources':q.get('images',[])},'limitations':[]}
 stats['qcm_subject_compared']+=1;stats['subject_items']+=5
 if not a['grading']['graded']:stats['ungraded_qcm']+=1
 else:stats['graded_qcm']+=1
 if q.get('answerIsEmpty'):stats['all_false_qcm']+=1
 if sid in visual_ids:stats['subject_qcm_visually_viewed']+=1
 if c:
  stats['correction_blocks']+=1
  if sid in visual_ids:stats['correction_qcm_visually_viewed']+=1
  a['correction']={'raw':c['raw'],'printedNumber':c['heading']['number'] or c['heading']['sequence'],'heading':c['heading']['text'],'statementLabelMap':c.get('sourceItemLabelMap',{}),'keyLiteral':c['key'],'keyRefs':refs(c['keyLines']),'grid':{'page':grid['page'],'number':grid['number'],'literal':grid['literal'],'refs':refs(grid['lines']),'rect':grid['rect']},'generalRaw':c.get('general',''),'generalDisplayed':q.get('generalExplanation',''),'panels':crop['correction'],'sharedContextRefs':refs(c.get('sharedContextLines',[])),'visualReview':sid in visual_ids}
  if canon_key(c['key']) is not None:stats['qcm_with_unambiguous_literal_key']+=1
  elif c['key']=='(C)E':stats['qcm_with_ambiguous_literal_key']+=1
  else:stats['qcm_no_usable_key_hors_programme']+=1
 else:
  a['limitations'].append(crop['correctionMissing']);stats['correction_missing_qcm']+=1
 for o in q['options']:
  label=o['id'];si=s['items'].get(label);ci=c['items'].get(label) if c else None;ex=c['explanations'].get(label) if c else None
  it={'id':label,'displayedStatement':o['text'],'subjectEvidence':None,'correctionStatementEvidence':None,'literalVerdict':None,'keyVerdict':None,'explanationEvidence':None,'status':None,'notes':[]}
  if si:
   it['subjectEvidence']={'kind':'pdf_text_layer','raw':si['text'],'refs':refs(si['lines']),'matchesDisplayed':norm(si['text'])==norm(o['text'])}
   if norm(si['text'])==norm(o['text']):stats['subject_text_items_matching']+=1
   else:
    assert sid=='ue4:2022-2023:S2:q14' and label in ['D','E']
    it['subjectEvidence']['visualReading']=o['text'];it['subjectEvidence']['status']='pdf_text_layer_artifact_resolved_visually';it['notes'].append('Le rendu original affiche « distribution » / « 50% » ; la couche texte ajoute respectivement un b / un è, invisibles. Texte V5 conservé.');stats['subject_text_layer_artifacts_resolved']+=1
  else:
   assert sid in ['ue4:2024-2025:S1:q24','ue4:2021-2022:S1:q07','ue4:2018-2019:S1:q03']
   it['subjectEvidence']={'kind':'printed_figure_label','raw':label,'description':f'Proposition {label} : structure chimique repérée par la lettre {label} dans le tableau original. Libellé technique « Molécule {label} (voir le schéma) » conservé.','refs':image_refs(s),'visualReview':True};stats['subject_figure_label_items']+=1
  if ci:
   it['correctionStatementEvidence']={'raw':ci['text'],'printedLabel':ci.get('printedLabel',label),'refs':refs(ci['lines']),'matchesSubject':bool(si) and norm(ci['text'])==norm(si['text'])}
   stats['correction_statement_items']+=1
   if ci.get('printedLabel'):it['notes'].append(f"Le corrigé réimprime cet item sous {ci['printedLabel']} ; correspondance avec {label} du sujet établie par son texte, son ordre et le détail A–E.")
   if si and norm(ci['text'])!=norm(si['text']):
    it['notes'].append('Le sujet et la reprise de l’énoncé dans le corrigé divergent littéralement ; les deux textes sont conservés dans les preuves. Le texte affiché est celui du sujet.')
    issues.append({'sourceId':sid,'bank':bank,'id':q['id'],'item':label,'type':'printed_subject_correction_difference','subject':si['text'],'correction':ci['text'],'impact':'already_preserved_or_documented; no key rewrite'})
  elif c and sid in ['ue4:2024-2025:S1:q24','ue4:2021-2022:S1:q07','ue4:2018-2019:S1:q03']:
   it['correctionStatementEvidence']={'kind':'printed_figure_label','raw':label,'refs':image_refs(c),'visualReview':True};stats['correction_figure_label_items']+=1
  if c:
   ck=canon_key(c['key'])
   if ck is not None:it['keyVerdict']='VRAI' if label in ck else 'FAUX';stats['items_with_unambiguous_key']+=1
   elif c['key']=='(C)E':it['keyVerdict']='indéterminé' if label=='C' else ('VRAI' if label=='E' else 'FAUX');stats['items_in_ambiguous_key_qcm']+=1
  if ex:
   m=re.match(r'\(?\s*(VRAI|FAUX)(\s*\?)?',ex['text'],re.I);it['literalVerdict']=m.group(0) if m else None
   it['explanationEvidence']={'raw':ex['text'],'displayed':q['explanations'].get(label,''),'refs':refs(ex['lines']),'matchesDisplayed':norm(ex['text'])==norm(q['explanations'].get(label,''))};stats['items_with_individual_detail']+=1
   if it['explanationEvidence']['matchesDisplayed']:stats['individual_details_transcribed_matching']+=1
   else:
    assert q['explanations'].get(label,'').startswith('La justification imprimée ne correspond pas')
    it['explanationEvidence']['status']='source_misassigned_justification_preserved_in_original_copy_and_previous_note';it['notes'].append('La formule de réserve V5 est conservée au lieu de présenter une justification sans rapport comme valable ; le texte imprimé intégral figure ici et dans la copie authentique.');stats['individual_details_replaced_by_existing_reservation']+=1
   if m and it['keyVerdict'] in ['VRAI','FAUX'] and m[1].upper()!=it['keyVerdict']:
    it['status']='unresolved_internal_key_detail_conflict';it['notes'].append('Clé et détail contradictoires dans le document ; QCM déjà hors note, conservé ainsi.')
   elif sid=='ue4:2020-2021:PACES:q29' and label=='C':it['status']='unresolved_explicit_source_doubt'
   else:it['status']='documentary_compared'
  elif not c:
   it['status']='correction_absent';stats['items_without_individual_detail']+=1
  elif re.search('programme',c['key'] or '',re.I):
   it['status']='hors_programme_without_key_or_detail';stats['items_without_individual_detail']+=1
  else:
   it['status']='key_and_general_correction_only' if c.get('general') else 'key_only_without_individual_detail';stats['items_without_individual_detail']+=1
   it['explanationEvidence']={'raw':c.get('general',''),'kind':'general_correction' if c.get('general') else 'no_individual_detail','refs':refs(c.get('generalLines',[]) or c['lines'][c['lines'].index(c['keyLines'][0])+1:]) if c['keyLines'] else []}
  a['items'].append(it)
 aud.append(a)

# Search trace for the absent BPF/BPP correction in the complete supplied compilation.
needle=norm("Les bonnes pratiques de préparation sont uniquement des recommandations sans statut juridique particulier")
match_pages=[]
for i,p in enumerate(DOC):
 if needle in norm(p.get_text()):match_pages.append(i+1)
searches={'pdf':str(PDF),'pagesScanned':len(DOC),'phrase':'Les bonnes pratiques de préparation sont uniquement des recommandations sans statut juridique particulier','matchingPages':match_pages,'conclusion':'La phrase propre au Q13 BPF/BPP est trouvée au sujet p843 seulement. Le détail et la grille associés sont absents ; la grille p848 ne doit pas être réattribuée.'}
(R/'searches.json').write_text(json.dumps(searches,ensure_ascii=False,indent=2))

missing=[]
for a in aud:
 if a['grading']['graded']:continue
 sid=a['sourceId'];row=S[sid];q=QM[sid][1]
 if not row.get('correction'):kind='missing_official_correction';need='Corrigé officiel ou erratum du sujet UE4 S1 2021–2022 Q13 (BPF/BPP), avec verdicts A–E.'
 elif re.search('programme',row['correction']['key'] or '',re.I):kind='no_key_hors_programme';need=f"Une correction authentique avec clé A–E de {q['year']} {q['session']} Q{q['sourceNumber']}, si cette question doit être notée ; le recueil actuel indique seulement « Hors programme »."
 elif sid=='ue4:2020-2021:PACES:q25':kind='subject_correction_unit_conflict';need='Version lisible ou erratum officiel de l’item D (unité imprimée « Vig » au sujet ; « mg » dans le corrigé).'
 elif sid=='ue4:2020-2021:PACES:q29':kind='explicitly_ambiguous_key';need='Confirmation du professeur/erratum de l’item C et clé définitive ; le corrigé imprime « (C)E » et « FAUX ? ».'
 elif sid=='ue4:2020-2021:PACES:q13':kind='source_recognized_no_exact_answer';need='Erratum des valeurs d’activité ou des équations QSAR ; le corrigé affirme qu’aucune réponse n’est exacte et retient A comme approximation.'
 elif sid=='ue4:2019-2020:S1:q19':kind='subject_correction_statement_conflict';need='Erratum explicite de l’item A (« adsorption » au sujet ; « absorption » dans le corrigé).'
 elif sid=='ue4:2020-2021:S2:q10':kind='internal_key_detail_conflict';need='Erratum officiel du verdict de B : grille et clé BDE, détail B FAUX.'
 else:raise Exception(sid)
 missing.append({'sourceId':sid,'bank':a['bank'],'id':a['id'],'items':['A','B','C','D','E'],'kind':kind,'neededDocumentOrClarification':need,'subjectPages':sorted(set(l['page'] for l in row['subject']['lines'])),'correctionPages':sorted(set(l['page'] for l in row.get('correction',{}).get('lines',[]))),'gridPage':row.get('grid',{}).get('page'),'currentTreatment':'hors_note_preserved','evidence':a['grading']['warning'],'searchesPerformed':['Nouvelle extraction et comparaison du sujet et du corrigé du recueil PDF, pages précédentes/suivantes comprises.','Rapprochement de la grille courte de la même année/session avec le détail.','Inventaires documents_available.json et additional_documents.json consultés ; seuls Droit Pharma et cycle de vie du médicament sont disponibles pour compléter l’UE4.']+(['Recherche de la phrase distinctive sur les 1660 pages du recueil ; occurrence au seul sujet p843.'] if not row.get('correction') else [])})
no_individual=[]
for sid,row in S.items():
 c=row.get('correction')
 if c and not c['explanations'] and not re.search('programme',c['key'] or '',re.I):no_individual.append({'sourceId':sid,'items':['A','B','C','D','E'],'key':c['key'],'generalExplanationAvailable':bool(c.get('general')),'pages':sorted(set(l['page'] for l in c['lines'])),'treatment':'La clé et l’éventuel raisonnement général sont reproduits ; aucune justification individuelle inventée.'})
# Precise inventory of previous scientific reservations, separate from missing original corrections.
reserves=[]
for sid,(bank,q) in RQM.items():
 for n in q.get('reviewNotes',[]):
  if n['kind']!='missing_reference':reserves.append({'sourceId':sid,'bank':bank,'id':q['id'],'noteId':n['noteId'],'items':n.get('items',[]),'theme':q['category'],'kind':n['kind'],'text':n['text'],'referenceVerdict':n.get('courseVerdict',''),'refs':n.get('refs',[])})
missobj={'missingQuestionsInRepresentedSeries':[],'blockingOfficialDocumentsOrErrata':missing,'individualDetailsNotPrintedButKeyPresent':no_individual,'annotatedSubjectCopies':[{'sourceId':'ue4:2019-2020:S1:q04','page':941,'annotationRegion':[245,105,310,145],'neededDocument':'Sujet non annoté uniquement si l’on souhaite une copie intégrale avant validation. La question interactive actuelle conserve les descripteurs transcrits et le tableau sans l’ajout.','currentTreatment':'subjectAfterCorrection:true; original pixels preserved'}],'previousScientificReservationsPreserved':reserves,'availableCourseDocuments':[{'file':'sources/revision_v4/Droit_Pharma_261001_102709_382ac72fda.pdf','pages':10},{'file':'sources/revision_v4/cycle_de_vie_du_medicament_M_Le_Borgne_e21aea198f.pdf','pages':9}],'scopeNote':'Les réserves scientifiques sont conservées séparément de l’état de transcription. L’absence d’une ronéo spécialisée ne signifie pas que le sujet ou son corrigé est absent.'}
(R/'missing.json').write_text(json.dumps(missobj,ensure_ascii=False,indent=2))

stats.update({'banks':len(KS),'represented_series':len(G),'subject_clean_copies':len(C)-1,'subject_annotated_copies':1,'subject_missing_copies':0,'correction_copies':sum(bool(x['correction']) for x in C),'short_grids_visually_reviewed':14,'interactive_figures_visually_reviewed':len(fig_ids),'subject_panels':sum(len(x['subject']) for x in C),'correction_panels':sum(len(x['correction']) for x in C),'existing_review_notes_preserved':179,'source_question_additions':0,'grading_key_changes':0,'source_option_changes':0,'notes_with_citation_repairs':len(by_note),'stale_citations_removed':len(candidates)})
metadata={'version':'V6-preparer','date':'2026-11-22','sourceFile':str(PDF),'sourceSHA256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'baselineFile':str(BASE.resolve()),'baselineSHA256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'method':'Nouvelle extraction paginée/positionnée depuis le PDF original ; séquences de questions identifiées dans chaque sujet et corrigé ; comparaison de chacun des 1680 items et des 1625 détails individuels imprimés ; inspection visuelle de 31 sujets, 30 corrigés, 13 figures interactives et 14 grilles. Le reste a eu un contrôle documentaire et géométrique, pas une visualisation individuelle annoncée.','status':'ready_for_independent_verifier','stats':dict(stats)}
(R/'audit.json').write_text(json.dumps({'metadata':metadata,'questions':aud},ensure_ascii=False,indent=2));(R/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2));(R/'documentary_differences.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2));(R/'coverage_preparer.json').write_text(json.dumps({'stats':dict(stats),'visualSubjectSourceIds':sorted(visual_ids),'visualCorrectionSourceIds':sorted(sid for sid in visual_ids if S[sid].get('correction')),'visualInteractiveFigureSourceIds':sorted(fig_ids),'gridPages':[g['ranges']['correction'][0]+1 for g in G],'courseVisualPages':{'cycle_de_vie_du_medicament':[2,4,5,6,7,8,9]},'limitations':'La comparaison textuelle des 336 questions est exhaustive ; seuls les 31 QCM listés ont eu une lecture visuelle individuelle complète du sujet. Les 14 grilles ont été inspectées visuellement dans leur intégralité utile.'},ensure_ascii=False,indent=2))
# Structural, not scientific, invariants and geometric gates.
assert len(aud)==336 and sum(len(a['items']) for a in aud)==1680
assert len(C)==336 and len({(x['bank'],x['id']) for x in C})==336
for k in KS:
 for before,after in zip(B[k]['questions'],reviewed['banks'][k]['questions']):
  for f in ['id','sourceId','sourceNumber','year','session','category','course','question','context','options','answer','rawAnswer','legacyProgress']:
   assert before[f]==after[f],(k,before['id'],f)
for r in C:
 for role in ['subject','correction']:
  for p in r[role]:
   rc=p['rect'];pr=DOC[p['page']-1].rect
   assert 0<=rc[0]<rc[2]<=pr.width+.2 and 0<=rc[1]<rc[3]<=pr.height,(r['sourceId'],role,p)
print(json.dumps(dict(stats),ensure_ascii=False,indent=2))
print('missing official/errata',len(missing),'raw statement differences',len(issues),'absent-Q13 search matches',match_pages)
