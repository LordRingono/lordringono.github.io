import fitz,json,hashlib,unicodedata,re
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent/'prepare';site=P.parents[3]/'output/site'
J=lambda f:json.loads(Path(f).read_text())
def norm(x):return ''.join(c for c in unicodedata.normalize('NFKD',str(x)).lower().replace('œ','oe') if c.isalnum())
D={}
def doc(f):
 if f not in D:D[f]=fitz.open(f)
 return D[f]
data=J(B/'reviewed.json')['banks'];rows=[];flags=[]
for r in J(B/'crops.json'):
 q=next(x for x in data[r['bank']]['questions'] if x['id']==r['id']);rr={'bank':r['bank'],'id':r['id'],'reuseExisting':r.get('reuseExisting',False),'roles':{},'items':[]}
 for role in ('subject','correction'):
  panels=[]
  for c in r[role]:
   pg=doc(c['file'])[c['page']-1];rect=fitz.Rect(c['rect']);tx=pg.get_textbox(rect);panels.append({'file':c['file'],'page':c['page'],'rect':c['rect'],'rectInPage':pg.rect.contains(rect),'text':tx})
  rr['roles'][role]={'panels':panels,'wholeText':' '.join(x['text'] for x in panels)}
  if r.get('reuseExisting'):
   copies=q['sourceCopies'][role]
   rr['roles'][role]['reusedPDF']=copies['pdf'];rr['roles'][role]['captures']=[{'src':x['src'],'page':x['page'],'exists':(site/x['src']).exists(),'sha256':hashlib.sha256((site/x['src']).read_bytes()).hexdigest()} for x in copies['captures']]
 for op in q['options']:
  ok=norm(op['text']) in norm(rr['roles']['subject']['wholeText']);row={'id':op['id'],'subjectTextIncluded':ok}
  if not ok:flags.append({'bank':r['bank'],'id':r['id'],'item':op['id'],'text':op['text'],'problem':'subject_text_not_exact_in_panels'})
  rr['items'].append(row)
 for role in ('subject','correction'):
  if not all(x['rectInPage'] for x in rr['roles'][role]['panels']):flags.append({'bank':r['bank'],'id':r['id'],'problem':'rect_outside_page','role':role})
 rr['subjectStemLiteralIncluded']=norm(q['question']) in norm(rr['roles']['subject']['wholeText'])
 rows.append(rr)
(P/'copies_verification.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(P/'copies_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('rows',len(rows),'items',sum(len(r['items']) for r in rows),'subject exact',sum(o['subjectTextIncluded'] for r in rows for o in r['items']),'stems exact',sum(r['subjectStemLiteralIncluded'] for r in rows),'flags',len(flags));print(json.dumps(flags,ensure_ascii=False))
