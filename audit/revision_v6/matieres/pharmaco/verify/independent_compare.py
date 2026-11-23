from pathlib import Path
import re,json,unicodedata,collections,difflib,fitz,hashlib
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/pharmaco/verify'
def load(p):return json.loads(p.read_text())
def save(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
def norm(t):
 t=unicodedata.normalize('NFKC',t or '').casefold()
 for a,b in [('’',"'"),('`',"'"),('–','-'),('—','-'),('‑','-'),('œ','oe'),('ﬁ','fi'),('ﬂ','fl')]:t=t.replace(a,b)
 return re.sub(r'\s+','',t)
def loose(t):return re.sub(r'[^\w+%=<>/°µ²³-]','',norm(t))
def txt(ls):return ' '.join(l['text'] for l in ls)
def ref(ls):return [{'page':l['page'],'rect':l['bbox'],'text':l['text']} for l in ls]
SEG=load(OUT/'independent_segments.json')
QDATA=load(ROOT/'work/site_v6/pharmaco/prepare/reviewed.json')
itempat=re.compile(r'^([A-J])[.)]\s*(.*)',re.I)
keypat=re.compile(r'^(?:[A-E]{1,5}|\([A-E]\)[A-E]+|AUCUNE)$')
def parts(seg):
 ls=seg['lines']
 kis=[i for i,l in enumerate(ls) if keypat.match(l['text'])] if seg['role']=='correction' else []
 ki=kis[0] if kis else None
 before=ls[:ki] if ki is not None else ls
 after=ls[ki+1:] if ki is not None else []
 def parse_items(lines):
  marks=[(i,itempat.match(l['text'])) for i,l in enumerate(lines) if itempat.match(l['text'])]
  opts={};labelmap={}
  for j,(i,m) in enumerate(marks):
   end=marks[j+1][0] if j+1<len(marks) else len(lines)
   bl=lines[i:end];x=m[2]+' '+txt(bl[1:]);opts[m[1].upper()]={'text':x.strip(),'refs':ref(bl),'literalLabel':m[1]}
  return opts,lines[:marks[0][0]] if marks else lines
 opts,stem=parse_items(before);details,general=parse_items(after)
 if seg['role']=='subject':stem=stem.copy();stem[0]=dict(stem[0]);stem[0]['text']=re.sub(r'^\d{1,2}[.)]\s*','',stem[0]['text'])
 return {'stem':txt(stem),'stemRefs':ref(stem),'options':opts,'key':ls[ki]['text'] if ki is not None else None,'keyRef':ref([ls[ki]]) if ki is not None else [],'details':details,'general':txt(general),'generalRefs':ref(general),'isHorsProgramme':'hors programme' in txt(ls).lower() and not opts}
INDEX={(s['year'],s['session'],s['role'],s['number']):s for s in SEG}
COM=[];FLAGS=[]
for bank,b in QDATA['banks'].items():
 for q in b['questions']:
  n=int(q['sourceNumber']);base=(q['year'],q['session']);ss=INDEX[base+('subject',n)];sp=parts(ss)
  cn=q.get('correctionNumber')
  # Explicit independent correspondence of the source: source Q13 absent;
  # item identity proves subject Q14..25 = correction ordinal Q13..24.
  if base==('2021-2022','S1'):expected_cn=n if n<13 else (None if n==13 else n-1)
  else:expected_cn=n
  cs=INDEX.get(base+('correction',expected_cn)) if expected_cn else None
  cp=parts(cs) if cs else None
  c={'bank':bank,'id':q['id'],'sourceId':q['sourceId'],'year':q['year'],'session':q['session'],'sourceNumber':n,'subject':sp,'correction':cp,'subjectFirstPage':ss['startPage'],'correctionFirstPage':cs['startPage'] if cs else None,'items':[]}
  if cn!=expected_cn:FLAGS.append({'sourceId':q['sourceId'],'type':'correctionNumber','given':cn,'expected':expected_cn})
  if q['subjectPage']!=ss['startPage']:FLAGS.append({'sourceId':q['sourceId'],'type':'subjectPage','given':q['subjectPage'],'expected':ss['startPage']})
  if q.get('correctionPage')!=c['correctionFirstPage']:FLAGS.append({'sourceId':q['sourceId'],'type':'correctionPage','given':q.get('correctionPage'),'expected':c['correctionFirstPage']})
  # Stem+context comparison retains punctuation; small formal differences shown separately.
  shown=' '.join([q.get('question',''),q.get('context','')])
  c['displayedStem']=shown
  c['stemMatch']=norm(shown)==norm(sp['stem'])
  c['stemLooseMatch']=loose(shown)==loose(sp['stem'])
  if not c['stemLooseMatch']:FLAGS.append({'sourceId':q['sourceId'],'type':'stem','site':shown,'source':sp['stem']})
  for o in q['options']:
   oid=o['id'];so=sp['options'].get(oid);coid=chr(ord(oid)+5) if q['sourceId']=='ue4:2023-2024:S1:q24' else oid;co=cp['options'].get(coid) if cp else None;de=cp['details'].get(oid) if cp else None
   item={'id':oid,'displayed':o['text'],'subject':so,'correctionLabel':coid,'correctionStatement':co,'displayedDetail':q.get('explanations',{}).get(oid,''),'detail':de}
   for typ,raw,target in [('subject',so,o['text']),('correctionStatement',co,o['text']),('detail',de,item['displayedDetail'])]:
    item[typ+'Match']=norm(raw['text'])==norm(target) if raw else None
    item[typ+'LooseMatch']=loose(raw['text'])==loose(target) if raw else None
    if raw and not item[typ+'LooseMatch']:FLAGS.append({'sourceId':q['sourceId'],'item':oid,'type':typ,'site':target,'source':raw['text']})
   c['items'].append(item)
  c['displayedAnswer']=q.get('answer');c['rawAnswer']=q.get('rawAnswer');c['displayedGeneral']=q.get('generalExplanation','')
  if cp and cp['key'] and q.get('rawAnswer')!=cp['key']:FLAGS.append({'sourceId':q['sourceId'],'type':'key','site':q.get('rawAnswer'),'source':cp['key']})
  COM.append(c)
save('independent_comparison.json',COM);save('comparison_flags.json',FLAGS)
print('Questions',len(COM),'Items',sum(len(c['items']) for c in COM))
print('Flags',collections.Counter(f['type'] for f in FLAGS))
print('Missing source option',sum(i['subject'] is None for c in COM for i in c['items']))
print('Missing correction option',sum(i['correctionStatement'] is None for c in COM for i in c['items']))
print('Missing correction detail',sum(i['detail'] is None for c in COM for i in c['items']))
for f in FLAGS:print(json.dumps(f,ensure_ascii=False))
