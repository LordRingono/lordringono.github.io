import fitz,json,re,hashlib,unicodedata,difflib
from pathlib import Path
P=Path(__file__).resolve().parent;BASE=P.parent/'prepare';SITE=P.parents[3]/'output/site'
J=lambda p:json.loads(Path(p).read_text())
reviewed=J(BASE/'reviewed.json')['banks'];audit=J(BASE/'audit.json');crops=J(BASE/'crops.json');docs={};page_lines={}
def doc(path):
 path=str(Path(path).resolve())
 if path not in docs:docs[path]=fitz.open(path)
 return docs[path]
def norm(s):
 s=unicodedata.normalize('NFKD',str(s)).lower().replace('œ','oe').replace('æ','ae')
 return ''.join(c for c in s if c.isalnum())
def fresh(ev):
 lines=[]
 for pos in ev['positions']:
  pg=doc(ev['file'])[pos['page']-1];rect=fitz.Rect(pos['rect']);a=[]
  pk=(ev['file'],pos['page'])
  if pk not in page_lines:page_lines[pk]=[line for block in pg.get_text('dict')['blocks'] for line in block.get('lines',[])]
  for line in page_lines[pk]:
   rr=fitz.Rect(line['bbox'])
   if abs(rr.y0-rect.y0)<1.0 and abs(rr.y1-rect.y1)<1.0 and (rect+(-1,-1,1,1)).contains(rr):a.append(''.join(sp['text'] for sp in line['spans']).strip())
  # Some Word PDFs separate the letter and its statement into different text
  # lines. Do not accept a letter-only match as the entire source proposition.
  if not a or re.fullmatch(r'[A-O][.\-:]?', ''.join(a).strip()):
   a=[' '.join(pg.get_textbox(rect+(-.5,-.5,.5,.5)).split())]
  lines.append({'page':pos['page'],'rect':list(rect),'text':' '.join(a)})
 return {'file':ev['file'],'sourceLabel':ev.get('label'),'text':' '.join(x['text'] for x in lines),'lines':lines}
rows=[];flags=[];reads={}
for a in audit:
 b=a['bank'];q=next(x for x in reviewed[b]['questions'] if x['id']==a['id']);entry={'bank':b,'id':q['id'],'siteQuestion':q['question'],'key':q['answer'],'allFalse':q.get('answerIsEmpty',False),'items':[]}
 lines=[f"\n### {b} / {q['id']} | clé {q['answer'] or ('tous faux' if q.get('answerIsEmpty') else 'HORS NOTE')}\n{q['question']}"]
 for it in a['items']:
  option=next(x for x in q['options'] if x['id']==it['id']);sub=[fresh(x) for x in it['subjectEvidence']];cor=[fresh(x) for x in it['correctionEvidence']];text=' '.join(x['text'] for x in cor);stext=' '.join(x['text'] for x in sub)
  row={'id':option['id'],'siteText':option['text'],'siteExplanation':q.get('explanations',{}).get(option['id'],''),'source':sub,'correction':cor,'literalMarkers':re.findall(r'\b(?:vrai|faux|[VF])\b',text,re.I)}
  sn=norm(stext);tn=norm(option['text']);row['subjectExactNormalized']=tn in sn
  if not row['subjectExactNormalized']:flags.append({'bank':b,'id':q['id'],'item':option['id'],'reason':'subject_text_diff','site':option['text'],'source':stext})
  # Drop repeated question text only when faithfully contained, retaining all correction words.
  cc=re.sub(r'^\s*[A-O]\s*[.\-–—:]\s*','',text)
  if norm(option['text']) in norm(cc):
   # fuzzy prefix length with punctuation/spacing normalized
   wanted=norm(option['text']);acc='';idx=0
   for idx,ch in enumerate(cc):
    acc+=norm(ch)
    if acc==wanted:cc=cc[idx+1:].strip();break
    if not wanted.startswith(acc):break
  row['freshCorrectionTail']=cc
  entry['items'].append(row);lines.append(f"{option['id']}. {option['text']}\n  SOURCE CORRECTION: {cc}\n  SITE DETAIL: {row['siteExplanation']}")
 rows.append(entry);reads.setdefault(b,[]).append('\n'.join(lines))
for b,ls in reads.items():(P/'fresh'/('compare_'+b+'.txt')).write_text('\n'.join(ls))
(P/'fresh_evidence.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(P/'text_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('Questions',len(rows),'items',sum(len(x['items']) for x in rows),'flags',len(flags),'PDFs',len(docs))
print(json.dumps(flags,ensure_ascii=False,indent=2))
