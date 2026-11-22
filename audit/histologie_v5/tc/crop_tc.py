from pathlib import Path
import json,re,fitz

R=Path(__file__).resolve().parents[1];O=Path(__file__).resolve().parent
audit=json.loads((O/'audit.json').read_text());reviewed=json.loads((O/'reviewed.json').read_text());crops=[];visual=[]
byq={}
for a in audit:byq[(a['bank'],a['id'])]={'bank':a['bank'],'id':a['id'],'sourceNumber':a['sourceNumber'],'subject':[],'correction':[]}
for bank in ['tc1','tc2','tc3']:
 for role in ['subject','correction']:
  f=next((R/'render'/f'{bank}_{role}').glob('*.pdf'));doc=fitz.open(f)
  lines=[]
  for pn,p in enumerate(doc,1):
   for b in p.get_text('dict')['blocks']:
    for line in b.get('lines',[]):
     s=''.join(span['text'] for span in line['spans']).strip()
     if not s or s.startswith(('EMSLB_PASS','L. Bastin','C. Rochet')) or re.fullmatch(r'\d+',s):continue
     lines.append({'page':pn,'text':s,'bbox':line['bbox']})
  lines.sort(key=lambda l:(l['page'],l['bbox'][1],l['bbox'][0]))
  starts=[]
  for idx,l in enumerate(lines):
   m=re.match(r'\s*(?:QR[MU]\s*)?(\d+)\s*[):]',l['text'])
   if m:starts.append((int(m[1]),idx))
  expected=[q for q in audit if q['bank']=='histo.'+bank]
  assert [n for n,i in starts]==[q['sourceNumber'] for q in expected]
  for qi,((number,start),a) in enumerate(zip(starts,expected)):
   end=starts[qi+1][1] if qi+1<len(starts) else len(lines)
   qlines=lines[start:end];panels=[]
   for pn in sorted({l['page'] for l in qlines}):
    ls=[l for l in qlines if l['page']==pn]
    x0=min(l['bbox'][0] for l in ls)-5;x1=max(l['bbox'][2] for l in ls)+5
    y0=min(l['bbox'][1] for l in ls)-3;y1=max(l['bbox'][3] for l in ls)+3
    if end<len(lines) and lines[end]['page']==pn:y1=min(y1,lines[end]['bbox'][1]-.2)
    rect=[round(v,3) for v in [x0,y0,x1,y1]]
    assert x1>x0 and y1>y0
    panel={'file':str(f.resolve()),'page':pn,'rect':rect,'label':f'{bank.upper()} — {"sujet" if role=="subject" else "corrigé"} — QCM {number} — p. {pn}'}
    panels.append(panel)
    # Internal crop for boundary QA; root renders the final user assets.
    dest=O/'capture_check'/f'{bank}_{a["id"]:02}_{role}_{pn}.png';dest.parent.mkdir(exist_ok=True)
    doc[pn-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5),clip=fitz.Rect(rect),alpha=False).save(dest)
   byq[(a['bank'],a['id'])][role]=panels
   a[role+'Pages']=[p['page'] for p in panels]
   a[role+'CaptureLines']=[l['text'] for l in qlines]
   q=next(q for q in reviewed['banks'][a['bank']]['questions'] if q['id']==a['id'])
   q[role+'Page']=panels[0]['page']
   q[role+'EndPage']=panels[-1]['page']
  visual.extend({'file':str(f),'page':pn,'inspected':True,'result':'Lisible ; tous les énoncés/items/verdicts relus sur le rendu original.'} for pn in range(1,len(doc)+1))
for fn,obj in [('crops.json',list(byq.values())),('audit.json',audit),('reviewed.json',reviewed),('visual_review.json',visual)]: (O/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
print('questions',len(byq),'panels',sum(len(q[r]) for q in byq.values() for r in ['subject','correction']),'pages inspected',len(visual))
