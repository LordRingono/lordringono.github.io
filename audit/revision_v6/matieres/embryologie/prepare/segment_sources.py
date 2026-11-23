import json,re,pathlib,copy,difflib,unicodedata
P=pathlib.Path(__file__).parent;E=json.load(open(P/'extraction.json'));M=json.load(open(P/'source_manifest.json'));B=json.load(open(P.parents[1]/'baseline_exams.json'));B={k:v for k,v in B.items() if v.get('ue')=='ue5e'}
RNUM=re.compile(r'^(\d{1,3})\s*[-–—:.]\s*(.*)',re.I);RQ=re.compile(r'^Q\s*(\d{1,3})(?:\s*(?:et|&)\s*(\d{1,3}))?\s*[-–—:.]?\s*(.*)',re.I)
KEY=re.compile(r'^([A-K()]{1,14})(?:$|\s*[Δ:])')
def keyhead(t):
 m=RNUM.match(t) or RQ.match(t)
 body=m.groups()[-1] if m else t
 return KEY.match(body.strip())
def extract_segments(name,pages):
 lines=[]
 for p in pages:
  for l in p['lines']:
   if l['bbox'][1]>=810 or 'David Bard' in l['text']:continue
   lines.append(dict(l,page=p['page']))
 heads=[];groups=[]
 for i,l in enumerate(lines):
  t=l['text']; mq=RQ.match(t); mn=RNUM.match(t) if l['bbox'][0]<80 else None
  m=mq or mn
  if not m:continue
  num=int(m[1]);
  if num==0 or num>100:continue
  if mq:
   if mq[2]:groups.append({'num':num,'second':int(mq[2]),'index':i});
   if mq[2] and not (name.startswith('4.') and num==23):continue
   body=mq[3]
  else:body=mn[2]
  if re.match(r'^(?:[0-9]+)?[Nn][,.]',body) or t.startswith('3-4 jours'):continue
  heads.append({'num':num,'index':i,'page':l['page'],'y':l['bbox'][1],'text':t,'groupSecond':int(mq[2]) if mq and mq[2] else None})
 segments=[]
 for hi,h in enumerate(heads):
  end=heads[hi+1]['index'] if hi+1<len(heads) else len(lines)
  s=dict(h,lines=lines[h['index']:end]);segments.append(s)
 # Annales may put an uncorrected question, then its separate keyed explanation.
 if 'Annales' in name:
  merged=[]
  for s in segments:
   if merged and s['num']==merged[-1]['num'] and keyhead(s['text']) and not keyhead(merged[-1]['text']):
    merged[-1]['correctionPart']=s;merged[-1]['subjectPart']=copy.deepcopy({k:v for k,v in merged[-1].items() if k not in ['correctionPart','subjectPart']});merged[-1]['lines']+=s['lines']
   else:merged.append(s)
  segments=merged
 return segments,groups
S={};G={}
for name,pages in E.items():S[name],G[name]=extract_segments(name,pages)
# Any split source 23/24 group is represented by the same authentic panel for each question.
for name,segs in S.items():
 for i,s in list(enumerate(segs)):
  if s.get('groupSecond'):
   sec=copy.deepcopy(s);sec['num']=s['groupSecond'];sec['sharedSource']=True;s['sharedSource']=True;segs.insert(i+1,sec)
# Link by printed number, position and occurrence. Keep explicit unlinked on ambiguity.
A={};summary=[]
for bank,b in B.items():
 qs=b['questions'];a=[]
 for role,field in [('subject','sourceSubject'),('correction','sourceCorrection')]:
  name=qs[0][field]
  if role=='subject' and name==qs[0]['sourceCorrection']:continue
  if name not in S:continue
  segs=S[name]
  # Site source order except restored Q30/31 in col.s2 appended with stable IDs; map to printed #.
  used=set()
  for qi,q in enumerate(qs):
   cands=[(si,s) for si,s in enumerate(segs) if si not in used and s['num']==int(q.get('sourceNumber',q['id']))]
   if not cands:
    a.append({'id':q['id'],'role':role,'status':'unlinked'});continue
   expected=q.get('subjectPage' if role=='subject' else 'correctionPage',1)
   si,s=min(cands,key=lambda z:(abs(z[1]['page']-expected),z[0]))
   used.add(si);a.append({'id':q['id'],'role':role,'source':name,'segmentIndex':si,'page':s['page'],'status':'linked','printed':s['num']})
  if len(used)!=len(segs):summary.append((bank,role,'segments_unassigned',[(s['num'],s['page'],s['text']) for i,s in enumerate(segs) if i not in used]))
 A[bank]=a
 print(bank,len(qs),[(r,len([v for v in a if v['role']==r and v['status']=='linked'])) for r in ['subject','correction']])
for row in summary:print(row)
(P/'segments.json').write_text(json.dumps(S,ensure_ascii=False));(P/'groups.json').write_text(json.dumps(G,ensure_ascii=False,indent=2));(P/'assignments.json').write_text(json.dumps(A,ensure_ascii=False,indent=2));(P/'assignment_issues.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
