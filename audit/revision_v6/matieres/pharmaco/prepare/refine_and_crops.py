import json,re,fitz,hashlib,collections
from pathlib import Path
R=Path(__file__).resolve().parent;S=json.loads((R/'segments.json').read_text());P=json.loads((R/'pages.json').read_text());G=json.loads((R/'groups_raw.json').read_text());PDF=str(Path('output/site/sources/Annales_compilation.pdf').resolve());D=fitz.open(PDF)
B=json.loads(Path('work/site_v6/baseline_exams.json').read_text());KS=json.loads(Path('work/site_v6/roster.json').read_text())['pharmaco']['banks'];QM={q['sourceId']:(k,q) for k in KS for q in B[k]['questions']}

def joined(ls):return re.sub(r'\s+',' ',' '.join(x['text'] for x in ls)).strip()
# Shared context is before Q13 in both original roles, not part of Q12.E.
for role in ['subject','correction']:
 row=S['ue4:2020-2021:S1:q12'][role]
 idx=next(i for i,l in enumerate(row['lines']) if l['text'].startswith('Questions 13'))
 ctxt=row['lines'][idx:];row['lines']=row['lines'][:idx];row['raw']=joined(row['lines']);row['excludedFollowingContext']=ctxt
 items=row['items'] if role=='subject' else row['explanations']
 item=items['E'];item['lines']=[l for l in item['lines'] if l not in ctxt];item['text']=re.sub(r'^E[.)]\s*','',joined(item['lines']))
 for qn in [13,14]:S[f'ue4:2020-2021:S1:q{qn:02}'][role]['sharedContextLines']=ctxt
# General QSAR table is not part of the E justification.
row=S['ue4:2020-2021:S1:q09']['correction'];els=row['explanations']['E']['lines'];general=els[1:];row['explanations']['E']={'text':'FAUX','lines':els[:1]};row['general']=joined(general);row['generalLines']=general
# All-caps ABD appended to E statement in the corrected original is a duplicate literal key.
row=S['ue4:2023-2024:S1:q02']['correction'];row['items']['E']['literalWithDuplicateKey']=row['items']['E']['text'];row['items']['E']['text']=re.sub(r'\s+ABD$','',row['items']['E']['text']);row['embeddedDuplicateKey']='ABD'
# Q24 2023–2024 S1: original correction restates options F–J, but its key/details use A–E.
row=S['ue4:2023-2024:S1:q24']['correction']
key_index=row['lines'].index(row['keyLines'][0]);stem_and_options=row['lines'][:key_index]
marks=[(i,re.match(r'^([F-J])[.)]\s*(.*)$',l['text'])) for i,l in enumerate(stem_and_options) if re.match(r'^([F-J])[.)]\s*(.*)$',l['text'])]
assert ''.join(m[1] for i,m in marks)=='FGHIJ'
row['sourceItemLabelMap']=dict(zip('FGHIJ','ABCDE'));row['items']={}
for j,(i,m) in enumerate(marks):
 end=marks[j+1][0] if j+1<len(marks) else len(stem_and_options);itemls=stem_and_options[i:end];label=row['sourceItemLabelMap'][m[1]]
 row['items'][label]={'text':re.sub(r'^[F-J][.)]\s*','',joined(itemls)),'lines':itemls,'printedLabel':m[1]}
row['stemLines']=stem_and_options[:marks[0][0]];row['stem']=re.sub(r'^\d+\.\s*','',joined(row['stemLines']))
# PACES Q5 has a heading containing the only printed correction.
row=S['ue4:2020-2021:PACES:q05']['correction'];row['key']='Hors programme';row['keyLines']=row['lines'];row['stem']=''

def bbox(ls):
 return [min(l['rect'][0] for l in ls),min(l['rect'][1] for l in ls),max(l['rect'][2] for l in ls),max(l['rect'][3] for l in ls)]
# Independently extract every numbered cell from each synthetic grid.
grids={}
for g in G:
 pg=g['ranges']['correction'][0]+1
 ls=[]
 for block in P[str(pg)]['dict']['blocks']:
  for l in block.get('lines',[]):
   t=''.join(s['text'] for s in l['spans']).strip()
   if t:ls.append({'page':pg,'rect':l['bbox'],'text':t})
 cells={}
 for l in ls:
  m=re.fullmatch('N[°º](\d+)',l['text'])
  if not m:continue
  candidates=[n for n in ls if abs(n['rect'][1]-l['rect'][1])<1 and n['rect'][0]>l['rect'][2]]
  nxt=min(candidates,key=lambda n:n['rect'][0]) if candidates else None
  if not nxt:raise Exception(('missing grid answer',pg,m[1]))
  rect=bbox([l,nxt]);rect=[rect[0]-7,rect[1]-4,rect[2]+7,rect[3]+4]
  cells[int(m[1])]={'page':pg,'number':int(m[1]),'literal':nxt['text'],'lines':[l,nxt],'rect':rect}
 grids[(g['year'],g['session'])]=cells
(R/'grids.json').write_text(json.dumps([{'year':g['year'],'session':g['session'],'cells':grids[(g['year'],g['session'])]} for g in G],ensure_ascii=False,indent=2))

def panels(row,role):
 ls=row['lines'];start=row['heading'];nexthead=row['nextHeading'];pgstart=start['page'];pgend=nexthead['page'] if nexthead else row['range'][1]
 # remove all pages containing only a heading/footer or closing blank area.
 nonempty=[]
 for pg in range(pgstart,pgend+1):
  low=start['rect'][1]-4 if pg==pgstart else 64
  high=nexthead['rect'][1]-4 if nexthead and pg==nexthead['page'] else 779
  if row.get('excludedFollowingContext') and pg==row['excludedFollowingContext'][0]['page']:high=row['excludedFollowingContext'][0]['rect'][1]-4
  if high<=low:continue
  relevant=[l for l in ls if l['page']==pg and l['rect'][1]>=low-1 and l['rect'][1]<high]
  imgs=[x for x in D[pg-1].get_image_info() if x['bbox'][1]<high and x['bbox'][3]>low and x['bbox'][1]>59 and x['bbox'][3]<782]
  if not relevant and not imgs:continue
  draws=[x for x in D[pg-1].get_drawings() if x['rect'].y0>=low-1 and x['rect'].y1<=high+1 and x['rect'].y1>low and x['rect'].y0<high]
  maxy=max([x['rect'][3] for x in relevant]+[x['bbox'][3] for x in imgs]+[x['rect'].y1 for x in draws])
  # preserve all drawing/text down to the next header or white-page boundary; final rows can be tightened.
  high=min(high,maxy+7)
  if high-low<4:continue
  nonempty.append({'file':PDF,'page':pg,'rect':[0.0,round(low,3),float(D[pg-1].rect.width),round(high,3)]})
 return nonempty
C=[]
for sid,row in S.items():
 k,q=QM[sid];r={'bank':k,'id':q['id'],'sourceId':sid,'subject':panels(row['subject'],'subject'),'correction':[]}
 subj=row['subject']
 if subj.get('sharedContextLines'):
  by=collections.defaultdict(list)
  for l in subj['sharedContextLines']:by[l['page']].append(l)
  ps=[]
  for pg,ls in by.items():
   rc=bbox(ls);ps.append({'file':PDF,'page':pg,'rect':[30,rc[1]-4,570,rc[3]+4],'fileLabel':'Contexte commun original des questions 13 et 14','sourceNumber':'13–14'})
  r['subject']=ps+r['subject']
 if 'correction' in row:
  co=row['correction'];cn=co['heading']['number'] or co['heading']['sequence'];grid=grids[(q['year'],q['session'])][cn]
  row['grid']=grid;r['correction']=panels(co,'correction')
  for p in r['correction']:p.update({'fileLabel':f"Corrigé détaillé {q['year']} {q['session']} · n°{cn}",'sourceNumber':cn})
  if co.get('sharedContextLines'):
   cls=co['sharedContextLines'];rc=bbox(cls)
   r['correction'].insert(0,{'file':PDF,'page':cls[0]['page'],'rect':[30,rc[1]-4,570,rc[3]+4],'fileLabel':'Contexte commun original des questions 13 et 14','sourceNumber':'13–14'})
  r['correction'].append({'file':PDF,'page':grid['page'],'rect':grid['rect'],'fileLabel':f"Grille courte {q['year']} {q['session']} · n°{cn}",'sourceNumber':cn})
  if cn!=int(q['sourceNumber']):r['correctionNote']=f"Le sujet porte le n°{q['sourceNumber']} ; le corrigé détaillé et sa grille portent le n°{cn}, à cause de l’omission du QCM 13 du sujet. L’association est établie par les cinq propositions."
  if re.search('programme',co['key'] or '',re.I):r['correctionNote']='Le document porte seulement « Hors programme » et la grille courte « / » : aucune clé de notation ni justification par item n’est fournie.'
  elif len(co['explanations'])<5:r['correctionNote']='La clé officielle et les éléments imprimés sont reproduits. Le document ne fournit pas cinq justifications séparées par item.'
  if co.get('sourceItemLabelMap'):r['correctionNote']='La reprise de l’énoncé est lettrée F–J dans le corrigé, alors que le sujet, la clé et les justifications utilisent A–E. La correspondance F→A, G→B, H→C, I→D, J→E est établie par le texte et l’ordre des cinq propositions.'
 else:
  r['correctionMissing']='Le sujet Q13 (BPF/BPP) est absent des 24 QCM du corrigé. La grille p848 utilise la numérotation du corrigé : son n°13 = A correspond au sujet Q14 (absorption), documenté p853–854. Aucune clé de cette grille ne peut être attribuée au sujet Q13. QCM conservé hors note.'
 for p in r['subject']:p.setdefault('fileLabel',f"Sujet original {q['year']} {q['session']} · n°{q['sourceNumber']}");p.setdefault('sourceNumber',q['sourceNumber'])
 C.append(r)
(R/'segments.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));(R/'crops.json').write_text(json.dumps(C,ensure_ascii=False,indent=2))
print('crops',len(C),'subject panels',sum(len(x['subject']) for x in C),'correction panels',sum(len(x['correction']) for x in C))
for sid,row in S.items():
 if row.get('grid'):
  co=row['correction'];sh=row['grid']['literal'];de=co['key']
  canonical=lambda x:''.join(sorted(set(x))) if x and re.fullmatch('[ABCDE]+',x) else x
  if canonical(sh)!=canonical(de):print('GRID DIFFERENCE',sid,sh,de)
