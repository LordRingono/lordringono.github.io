import json,re,unicodedata,collections,difflib
from pathlib import Path
R=Path(__file__).resolve().parent
GROUPS=json.loads((R/'groups_raw.json').read_text())
B=json.loads(Path('work/site_v6/baseline_exams.json').read_text());KS=json.loads(Path('work/site_v6/roster.json').read_text())['pharmaco']['banks'];QM={q['sourceId']:(k,q) for k in KS for q in B[k]['questions']}

def norm(s):
 s=unicodedata.normalize('NFKD',s.lower()).replace('œ','oe').replace('æ','ae')
 return re.sub(r'[^a-z0-9<>+=%°/-]','',s)

def joined(ls):return re.sub(r'\s+',' ',' '.join(x['text'] for x in ls)).strip()

def item_mark(l):return re.match(r'^([A-E])[.)]\s*(.*)$',l['text'],re.I)

def items(ls):
 d={};marks=[(i,item_mark(l)) for i,l in enumerate(ls) if item_mark(l)]
 for ix,(i,m) in enumerate(marks):
  end=marks[ix+1][0] if ix+1<len(marks) else len(ls)
  itemls=ls[i:end]
  if m[1].upper() in d: print('DUP',m[1])
  d[m[1].upper()]={'text':re.sub(r'^[A-E][.)]\s*','',joined(itemls),flags=re.I),'lines':itemls}
 return d

def parse(ls,role):
 mark0=next((i for i,l in enumerate(ls) if item_mark(l)),len(ls))
 stemls=ls[:mark0]
 if role=='subject':return {'stem':re.sub(r'^\d+\.\s*','',joined(stemls)),'stemLines':stemls,'items':items(ls[mark0:]),'raw':joined(ls),'lines':ls}
 keyindices=[i for i,l in enumerate(ls) if re.fullmatch(r'[ABCDE()?/\s]+|AUCUNE|Aucun|Aucune|HORS PROGRAMME|Hors programme',l['text'])]
 # exclude figure item isolated letters before first A.
 keyidx=next((i for i in keyindices if i>mark0),None)
 if keyidx is None and keyindices:keyidx=keyindices[-1]
 if keyidx is None:
  return {'stem':re.sub(r'^\d+\.\s*','',joined(stemls)),'stemLines':stemls,'items':items(ls[mark0:]),'key':None,'keyLines':[],'explanations':{},'general':'','raw':joined(ls),'lines':ls}
 sls=ls[:keyidx];els=ls[keyidx+1:]
 mark0=next((i for i,l in enumerate(sls) if item_mark(l)),len(sls))
 expmark=next((i for i,l in enumerate(els) if item_mark(l)),len(els))
 return {'stem':re.sub(r'^\d+\.\s*','',joined(sls[:mark0])),'stemLines':sls[:mark0],'items':items(sls[mark0:]),'key':ls[keyidx]['text'],'keyLines':[ls[keyidx]],'explanations':items(els[expmark:]),'general':joined(els[:expmark]),'raw':joined(ls),'lines':ls}

segments={};issues=[];counts=collections.Counter()
for g in GROUPS:
 for role in ['subject','correction']:
  heads=g[role]['headings'];lines=g[role]['lines']
  for j,h in enumerate(heads):
   end=heads[j+1]['index'] if j+1<len(heads) else len(lines)
   num=h['number'] or j+1
   if role=='correction' and g['year']=='2021-2022' and g['session']=='S1' and num>=13:num+=1
   sid=f"ue4:{g['year']}:{g['session']}:q{num:02}"
   row=segments.setdefault(sid,{'sourceId':sid,'bank':QM[sid][0],'id':QM[sid][1]['id']})
   row[role]=parse(lines[h['index']:end],role)
   row[role]['heading']=h
   row[role]['nextHeading']=heads[j+1] if j+1<len(heads) else None
   row[role]['range']=g['ranges'][role]
   counts[role+'_q']+=1
 for n in range(1,len(g['subject']['headings'])+1):
  sid=f"ue4:{g['year']}:{g['session']}:q{n:02}"; q=QM[sid][1];s=segments[sid]['subject'];c=segments[sid].get('correction')
  qstem=q['question']+' '+q.get('context','')
  if norm(qstem)!=norm(s['stem']):issues.append({'sourceId':sid,'type':'stem','original':s['stem'],'baseline':qstem,'similarity':difflib.SequenceMatcher(None,norm(qstem),norm(s['stem'])).ratio()})
  for o in q['options']:
   si=s['items'].get(o['id'])
   if not si:issues.append({'sourceId':sid,'type':'subject_item_absent','item':o['id'],'baseline':o['text']})
   elif norm(si['text'])!=norm(o['text']):issues.append({'sourceId':sid,'type':'subject_item','item':o['id'],'original':si['text'],'baseline':o['text'],'similarity':difflib.SequenceMatcher(None,norm(si['text']),norm(o['text'])).ratio()})
   else:counts['subject_item_matches']+=1
   if c:
    ci=c['items'].get(o['id']);ex=c['explanations'].get(o['id']);be=q.get('explanations',{}).get(o['id'],'')
    if ci and si and norm(ci['text'])!=norm(si['text']):issues.append({'sourceId':sid,'type':'subject_correction_item','item':o['id'],'subject':si['text'],'correction':ci['text'],'similarity':difflib.SequenceMatcher(None,norm(si['text']),norm(ci['text'])).ratio()})
    if ex and norm(ex['text'])!=norm(be):issues.append({'sourceId':sid,'type':'explanation','item':o['id'],'original':ex['text'],'baseline':be,'similarity':difflib.SequenceMatcher(None,norm(ex['text']),norm(be)).ratio()})
    elif ex:counts['explanation_matches']+=1
    elif be:issues.append({'sourceId':sid,'type':'detail_absent','item':o['id'],'baseline':be})
  if c and c['key'] != q['rawAnswer']:issues.append({'sourceId':sid,'type':'rawKey','original':c['key'],'baseline':q['rawAnswer']})
(R/'segments.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2))
(R/'comparison.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2))
print(counts);print(collections.Counter(i['type'] for i in issues))
