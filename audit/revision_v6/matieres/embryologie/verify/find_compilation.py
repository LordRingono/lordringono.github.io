from pathlib import Path
import fitz,json,re,unicodedata,collections,difflib
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/embryologie/verify'
ex=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text());pdf=ROOT/'output/site/sources/Annales_compilation.pdf';doc=fitz.open(pdf)
def norm(s):
 s=s.replace('œ','oe').replace('Œ','OE').replace('æ','ae')
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
 return re.sub('[^a-z0-9]','',s)
pages=[]
for pn in range(1000,len(doc)):
 p=doc[pn];t=p.get_text();h=' '.join(t[:250].split());m=re.search(r'(Sujet|Correction)\s+(?:UE5|ue5).*?(20\d\d[–-]20\d\d)',h,re.I)
 if m:
  pages.append({'page':pn+1,'role':m[1].lower(),'year':m[2],'header':h,'text':t,'normalized':norm(t),'lines':[{'text':' '.join(s['text'] for s in l['spans']),'bbox':l['bbox']} for b in p.get_text('dict')['blocks'] for l in b.get('lines',[])]})
print('PAGES',len(pages),min(p['page'] for p in pages),max(p['page'] for p in pages))
print('GROUPS')
last=None
for p in pages:
 g=p['role']+p['year']
 if g!=last:print(p['page'],p['header'][:120]);last=g
rows=[]
for bid,b in ex.items():
 if b.get('ue')!='ue5e' or '.ann.' not in bid:continue
 for q in b['questions']:
  year=q.get('category','')[:9]; ns=[norm(o['text']) for o in q['options']]
  cand=[]
  for p in pages:
   if p['role']!='sujet' or p['year']!=year:continue
   counts=[n in p['normalized'] for n in ns]
   prefix=[n[:70] in p['normalized'] for n in ns if len(n)>70]
   c=sum(counts);pr=sum(prefix)
   if c or pr:cand.append({'page':p['page'],'count':c,'prefix':pr,'exact':counts,'header':p['header'][:120]})
  cand.sort(key=lambda x:(x['count'],x['prefix']),reverse=True)
  rows.append({'bank':bid,'id':q['id'],'sourceNumber':q.get('sourceNumber'),'category':q.get('category'),'subjectDistinct':q.get('sourceSubject')!=q.get('sourceCorrection'),'candidates':cand[:4]})
(OUT/'compilation_pages.json').write_text(json.dumps(pages,ensure_ascii=False))
(OUT/'compilation_matches_initial.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('\nMATCHES FOR MISSING SUBJECTS')
for x in rows:
 if not x['subjectDistinct']: print(x['bank'],x['id'],x['category'],x['candidates'][:2])
