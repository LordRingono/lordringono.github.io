import json,re,copy,sys,difflib
from parse_sources import ROOT,OUT,BASE,NAMES,norm,text
P=json.loads((OUT/'parsed_sources.json').read_text())
STOP=re.compile(r'^(?:(?:CORRECTION|CORRIGE)\s+)?(?:SUJET\b|ANNALES\b|ANN[A]?LES\b|EPREUVE\b|Epreuve\b|SESSION\b|CC\s|DECEMBRE\b|Décembre\b|MAI\b|Mai\b|Juillet\b|Juin\b|TISSU CONJONCTIF EPREUVE\b|UE5\b|Dr Patrick\b|PARCOURS\b)',re.I)
CONTEXTS=['Un patient est suivi','Une biopsie de la tumeur','Le patient est traité par','La sclérose latérale','La SLA est donc','Les motoneurones situés','Le syndrome de Guillain','Les paresthésies sont','Dans une étude parue']
def trim(lines):
 end=len(lines)
 for i,l in enumerate(lines[1:],1):
  if STOP.match(l['text'].strip()) or any(l['text'].strip().startswith(z) for z in CONTEXTS):end=i;break
 return lines[:end]
def withoutlabel(s):return re.sub(r'^[A-J]\s*[.\-–):]?\s*','',s).strip()
def verdict(s):
 m=re.search(r'\b(vrai|faux|V|F)\b',s,re.I)
 if m:return {'literal':m[1],'truth':m[1].upper() in ['VRAI','V'],'detail':s[m.end():].strip(' .:;,'),'statement':s[:m.start()].strip()}
 return {'literal':None,'truth':None,'detail':None,'statement':s}
CAN={};changes=[];keys=[];gaps=[]
for bank in NAMES:
 CAN[bank]=[]
 for i,q in enumerate(BASE[bank]['questions']):
  si=i;ci=i
  if bank=='histo.ann.tech' and i in [20,21]:ci=41-i
  # zero-based indexes 20 and 21 swap => 41-i
  sq=copy.deepcopy(P[bank]['subject'][si]);cq=copy.deepcopy(P[bank]['correction'][ci]);items=[]
  for obj in [sq,cq]:
   if obj['itemLines']:
    last=list(obj['itemLines'])[-1];obj['itemLines'][last]=trim(obj['itemLines'][last]);obj['options'][last]=text(obj['itemLines'][last])
  sids=list(sq['options']);cids=list(cq['options']);extra=[]
  for j,sid in enumerate(sids):
   source=withoutlabel(sq['options'][sid]);cid=cids[j] if j<len(cids) else sid;cs=withoutlabel(cq['options'].get(cid,''));v=verdict(cs)
   # TE2 Q17 correction labels F-J correspond to A-E subject by order.
   existing=next((o for o in q['options'] if o['id']==sid),None)
   if existing and norm(source)!=norm(existing['text']):changes.append({'bank':bank,'id':q['id'],'item':sid,'type':'subject','baseline':existing['text'],'source':source,'ratio':round(difflib.SequenceMatcher(None,norm(source),norm(existing['text'])).ratio(),3)})
   if not existing:extra.append(sid)
   oldex=q.get('explanations',{}).get(sid,'');oldex=re.sub(r'^(?:Vrai|Faux|V|F)\b\s*[.:]?\s*','',oldex,flags=re.I)
   if v['detail'] is not None and norm(oldex)!=norm(v['detail']):changes.append({'bank':bank,'id':q['id'],'item':sid,'type':'detail','baseline':oldex,'source':v['detail']})
   if v['truth'] is None:gaps.append({'bank':bank,'id':q['id'],'item':sid,'source':cs,'page':cq['page'],'spans':sum([l['spans'] for l in cq['itemLines'].get(cid,[])],[])})
   items.append({'id':sid,'sourceLabel':sid,'correctionLabel':cid,'subject':source,'correctionRaw':cs,**v,'subjectLines':sq['itemLines'][sid],'correctionLines':cq['itemLines'].get(cid,[])})
  invert=bool(re.search(r'affirmation inexacte',sq['stem'],re.I));newkey=''.join(o['id'] for o in items if o['truth'] is not None and o['truth']!=invert)
  if newkey!=q.get('answer') or extra:keys.append({'bank':bank,'id':q['id'],'old':q['answer'],'candidate':newkey,'missingVerdicts':[z['id'] for z in items if z['truth'] is None],'extraOptions':extra})
  CAN[bank].append({'id':q['id'],'sourceIndex':si+1,'correctionIndex':ci+1,'subject':sq,'correction':cq,'items':items,'invert':invert,'candidateKey':newkey,'baselineKey':q['answer']})
for fn,x in [('canonical.json',CAN),('initial_changes.json',changes),('initial_key_deltas.json',keys),('verdict_gaps.json',gaps)]: (OUT/fn).write_text(json.dumps(x,ensure_ascii=False,indent=2))
print('KEY DELTAS');print(json.dumps(keys,ensure_ascii=False,indent=2));print('GAPS',len(gaps));print('\n'.join(f"{x['bank']} Q{x['id']}.{x['item']} p{x['page']} {x['source']}" for x in gaps));print('SUBJECT DIFFS');print(json.dumps([z for z in changes if z['type']=='subject'],ensure_ascii=False,indent=2));print('DETAIL DIFF COUNT',len([z for z in changes if z['type']=='detail']))
