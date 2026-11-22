from pathlib import Path
import json, re, unicodedata
import fitz
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'quality/independent_keys.json').read_text())
crops={}
for group in ['tc','tn','te_tech']:
 for c in json.loads((ROOT/group/'crops.json').read_text()):crops[(c['bank'],c['id'])]=c

def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFKD',s.replace('\uf061','α')).lower() if c.isalnum())

docs={}
def crop_text(cs):
 text=[]
 for c in cs:
  if c['file'] not in docs:docs[c['file']]=fitz.open(c['file'])
  page=docs[c['file']][c['page']-1]
  text.append(page.get_text('text',clip=fitz.Rect(c['rect'])))
 return '\n'.join(text)

checks=[]; problems=[]; question_checks=[]; image_checks=[]
for r in records:
 c=crops[(r['bank'],r['id'])]
 for side in ['subject','correction']:
  txt=crop_text(c[side]); nt=norm(txt)
  for part in c[side]:
   pg=docs[part['file']][part['page']-1];rect=fitz.Rect(part['rect'])
   for im in pg.get_image_info():
    bbox=fitz.Rect(im['bbox']);intersection=bbox&rect
    if intersection.is_empty:continue
    ic={'bank':r['bank'],'id':r['id'],'side':side,'page':part['page'],'image_bbox':list(bbox),'fraction_in_crop':intersection.get_area()/bbox.get_area()}
    image_checks.append(ic)
    if ic['fraction_in_crop']<0.999:problems.append({'image_partially_cropped':ic})
  stem=r[side+'_heading']['text']
  sq={'bank':r['bank'],'id':r['id'],'source_number':r['source_number'],'side':side,'pages':[v['page'] for v in c[side]],'crop_count':len(c[side]),'stem_complete':norm(stem) in nt,'contexts_complete':all(norm(v['text']) in nt for v in r.get(side+'_context',[])),'text':txt}
  sq['foreign_headings']=([{'source_number':int(n)} for n in re.findall(r'^\s*(\d+)\)',txt,re.M) if int(n)!=r['source_number']] if r['bank']=='histo.tn1' else [{'id':other['id'],'source_number':other['source_number']} for other in records if other['bank']==r['bank'] and other['id']!=r['id'] and norm(other[side+'_heading']['text']) in nt])
  if sq['foreign_headings']:problems.append({'bank':r['bank'],'id':r['id'],'side':side,'foreign_headings':sq['foreign_headings']})
  question_checks.append(sq)
  if not sq['stem_complete'] or not sq['contexts_complete']:problems.append({k:v for k,v in sq.items() if k!='text'})
  for item in r['items']:
   field='subject' if side=='subject' else 'corrected'
   source_text=item[field]['text']
   check={'bank':r['bank'],'id':r['id'],'source_number':r['source_number'],'item':item['id'],'side':side,'pages':sq['pages'],'complete':norm(source_text) in nt,'source_text':source_text}
   checks.append(check)
   if not check['complete']:problems.append(check)
result={'questions':len(records),'items':sum(len(r['items']) for r in records),'crop_parts':sum(len(c[s]) for c in crops.values() for s in ['subject','correction']),'question_checks':question_checks,'item_checks':checks,'image_checks':image_checks,'unresolved':problems}
(ROOT/'quality/crop_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('CROPS',result['crop_parts'],'QUESTION_SIDES',len(question_checks),'ITEM_SIDES',len(checks),'FLAGS',len(problems))
print(json.dumps(problems,ensure_ascii=False,indent=2))
