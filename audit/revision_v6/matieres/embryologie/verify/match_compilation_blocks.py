from pathlib import Path
import json,re,fitz,unicodedata,collections,difflib
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/embryologie/verify';PAGES=json.loads((OUT/'compilation_pages.json').read_text());EX=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text())
PDF=ROOT/'output/site/sources/Annales_compilation.pdf';DOC=fitz.open(PDF)
def norm(s):
 s=s.replace('œ','oe').replace('Œ','OE').replace('æ','ae');s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
 return re.sub('[^a-z0-9]','',s)
blocks=[]
for p in PAGES:
 if p['role']!='sujet':continue
 ls=[x for x in p['lines'] if x['text'].strip() and 68<=x['bbox'][1]<780]
 starts=[i for i,l in enumerate(ls) if re.match('^A\\.',l['text'].strip())]
 for ai,i in enumerate(starts):
  # title runs backwards from A until a previous item / material separated by a sizeable gap
  si=i-1
  while si>0:
   prev=ls[si-1];now=ls[si]
   if re.match(r'^[A-E]\.',prev['text'].strip()) or now['bbox'][1]-prev['bbox'][3]>16 or re.match(r'^\d{1,2}\.\s',now['text'].strip()):break
   si-=1
  si=max(0,si)
  if re.match('^[A-E]\\.',ls[si]['text'].strip()):si=i
  segment=[];active=None;its={}
  endi=starts[ai+1] if ai+1<len(starts) else len(ls)
  for j in range(i,endi):
   x=ls[j];t=x['text'].strip();m=re.match(r'^([A-E])\.\s*(.*)',t)
   if m:
    active=m[1];its[active]={'text':m[2],'lines':[x]}
   elif active:
    if re.match(r'^\d{1,2}\.\s',t):break
    if j>i and x['bbox'][1]-ls[j-1]['bbox'][3]>16:break
    its[active]['text']+=' '+t;its[active]['lines'].append(x)
   segment.append(x)
  if not all(l in its for l in 'ABCDE'):continue
  endy=max(x['bbox'][3] for z in its.values() for x in z['lines'])
  title=' '.join(x['text'].strip() for x in ls[si:i]);bbox=[30,max(65,ls[si]['bbox'][1]-4),DOC[p['page']-1].rect.width-30,endy+5]
  # In most source layouts figures sit between title and options; all are included by full-width rectangle.
  blocks.append({'page':p['page'],'year':p['year'],'header':p['header'][:125],'title':title,'rect':bbox,'items':{k:v['text'] for k,v in its.items()}})
rows=[]
for bid,b in EX.items():
 if bid not in ['embryo.ann.gamet','embryo.ann.fec','embryo.ann.s1','embryo.ann.s2']:continue
 for q in b['questions']:
  ns={o['id']:norm(o['text']) for o in q['options']};cs=[]
  for bl in blocks:
   exact=sum(ns[l]==norm(bl['items'].get(l,'')) for l in ns)
   partial=sum(ns[l] in norm(bl['items'].get(l,'')) or norm(bl['items'].get(l,'')) in ns[l] for l in ns)
   if exact>=2 or partial>=3:
    sim=sum(difflib.SequenceMatcher(None,ns[l],norm(bl['items'].get(l,''))).ratio() for l in ns)/len(ns)
    cs.append((sim,exact,partial,bl))
  cs.sort(key=lambda x:(x[0],x[1]),reverse=True)
  if cs and cs[0][0]>.82:
   sim,exact,partial,bl=cs[0];diffs=[{'id':o['id'],'site':o['text'],'source':bl['items'].get(o['id'])} for o in q['options'] if norm(o['text'])!=norm(bl['items'].get(o['id'],''))]
   rows.append({'bank':bid,'id':q['id'],'category':q['category'],'subject':bl,'similarity':sim,'exactItems':exact,'diffs':diffs,'file':str(PDF),'yearMismatch':q['category'][:9]!=bl['year'],'alternateCandidates':[{'similarity':a[0],'page':a[3]['page']} for a in cs[1:3]]})
(OUT/'compilation_blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2));(OUT/'compilation_supplements_draft.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('BLOCKS',len(blocks),'MATCHES',len(rows),'exact',sum(x['exactItems']==5 for x in rows))
for x in rows:
 if x['diffs'] or x['yearMismatch']:
  print(x['bank'],x['id'],'category',x['category'],'page',x['subject']['page'],'year',x['subject']['year'],'sim',round(x['similarity'],3),'title',x['subject']['title'])
  for d in x['diffs']:print(d['id'],'SITE',d['site'],'| SOURCE',d['source'])
