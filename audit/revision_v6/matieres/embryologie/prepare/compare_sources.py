import json,re,pathlib,unicodedata,copy,difflib,collections
P=pathlib.Path(__file__).parent;B=json.load(open(P.parents[1]/'baseline_exams.json'));B={k:v for k,v in B.items() if v.get('ue')=='ue5e'};S=json.load(open(P/'segments.json'));A=json.load(open(P/'assignments.json'))
def norm(t):
 t=unicodedata.normalize('NFKD',t).lower().replace('œ','oe').replace('æ','ae');return re.sub(r'[^a-z0-9]','',t)
def getseg(bank,q,role):
 a=next((a for a in A[bank] if a['id']==q['id'] and a['role']==role and a['status']=='linked'),None)
 return S[a['source']][a['segmentIndex']] if a else None
OPT=re.compile(r'^([A-Za-z]{1,2})\s*[–—:.)-]\s*(.*)')
def optblocks(s):
 out=[];cur=None
 for l in s['lines'][1:]:
  t=l['text'];m=OPT.match(t)
  if m and (m[1].isupper() or 'coeur' in globals().get('bank','')):
   cur={'id':m[1].upper(),'lines':[l],'text':m[2],'page':l['page']};out.append(cur)
  elif cur:
   if re.match(r'^20\d\d[-–]',t):continue
   cur['lines'].append(l);cur['text']+=' '+t
 for o in out:
  v=re.search(r'\b(Vrai|Faux)\b',o['text'],re.I)
  o['verdict']=bool(v and v[1].lower()=='vrai') if v else None
  o['statement']=o['text'][:v.start()].strip() if v else o['text']
  o['detail']=o['text'][v.start():].strip() if v else ''
  o['colored']=' '.join(s['text'].strip() for l in o['lines'] for s in l['spans'] if s['color'] not in (0,0xffffff) and s['text'].strip())
 return out
rows=[];flags=[]
for bank,b in B.items():
 for q in b['questions']:
  corr=getseg(bank,q,'correction');subj=getseg(bank,q,'subject') or (corr.get('subjectPart') if corr else None)
  cp=corr.get('correctionPart',corr)
  co=optblocks(cp);so=optblocks(subj) if subj else []
  rawheader=cp['text'];hm=re.match(r'^\s*(?:Q\s*)?\d+\s*[.\-–:]\s*([A-K()]{1,14})(?:$|\s*[Δ:])',rawheader)
  key=hm[1] if hm else None
  oo=[]
  for o in q['options']:
   c=next((x for x in reversed(co) if x['id']==o['id']),None);u=next((x for x in reversed(so) if x['id']==o['id']),None)
   record={'item':o['id'],'siteStatement':o.get('text',''),'siteVerdict':o['id'] in (q.get('answer') or ''),'siteExplanation':q.get('explanations',{}).get(o['id'],''),'subject':u,'correction':c}
   # normal full corrected inline / separate subject is evidence; permutations need special treatment
   statement=(u or c or {}).get('statement','');n1,n2=norm(o.get('text','')),norm(statement);sim=difflib.SequenceMatcher(None,n1,n2).ratio()
   record['statementSimilarity']=round(sim,4);record['statementExactNormalized']=n1==n2
   issues=[]
   if n1 and n1 not in norm(' '.join(l['text'] for l in (subj or corr)['lines'])) and sim<.98:issues.append('statement_difference')
   if c and c['verdict'] is not None and c['verdict']!=record['siteVerdict'] and not (q.get('weight')==0 or o['id'] in q.get('ignoredOptions',[])):issues.append('verdict_difference')
   if c and c['detail'] and len(norm(c['detail']))>len(norm(record['siteExplanation']))+15:issues.append('shorter_explanation')
   if key and (o['id'] in key)!=record['siteVerdict'] and not (q.get('weight')==0 or o['id'] in q.get('ignoredOptions',[])):issues.append('header_key_difference')
   if not c:issues.append('no_letter_block')
   if issues:flags.append({'bank':bank,'id':q['id'],'sourceNumber':q.get('sourceNumber'),'page':cp['page'],'item':o['id'],'issues':issues,'siteText':o.get('text',''),'sourceText':statement,'siteExplanation':record['siteExplanation'],'sourceDetail':c['detail'] if c else None,'colored':c['colored'] if c else None,'sourceKey':key,'siteAnswer':q['answer']})
   oo.append(record)
  rows.append({'bank':bank,'id':q['id'],'sourceCorrection':q['sourceCorrection'],'correctionPage':cp['page'],'rawHeader':rawheader,'rawKey':key,'hasUncorrectedSubject':bool(subj),'items':oo})
(P/'comparison.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(P/'flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('Questions',len(rows),'items',sum(len(r['items']) for r in rows),'flags',len(flags));print(collections.Counter(x for f in flags for x in f['issues']))
for bank in B:
 fl=[f for f in flags if f['bank']==bank];print(bank,len(fl),collections.Counter(x for f in fl for x in f['issues']))
