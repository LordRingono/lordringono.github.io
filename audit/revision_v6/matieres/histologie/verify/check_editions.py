import fitz,json,re,unicodedata,difflib,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent/'prepare';site=P.parents[3]/'output/site'
J=lambda s:json.loads(Path(s).read_text())
def norm(x):return ''.join(c for c in unicodedata.normalize('NFKD',str(x)).lower().replace('œ','oe') if c.isalnum())
docs={}
def getdoc(f):
 f=str(Path(f).resolve())
 if f not in docs:docs[f]=fitz.open(f)
 return docs[f]
def linesfresh(file,positions):
 out=[]
 for pos in positions:
  page=getdoc(file)[pos['page']-1];rect=fitz.Rect(pos['rect']);c=[]
  for b in page.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    rr=fitz.Rect(l['bbox'])
    if abs(rr.y0-rect.y0)<1.5 and abs(rr.y1-rect.y1)<1.5 and (rect+(-2,-2,2,2)).contains(rr):c.append(''.join(s['text'] for s in l['spans']).strip())
  if not c:c=[page.get_textbox(rect+(-1,-1,1,1)).strip()]
  out.append({'page':pos['page'],'rect':list(rect),'text':' '.join(c)})
 return out
comp=str((site/'sources/Annales_compilation.pdf').resolve());ed=J(B/'edition_comparisons.json');blocks=J(B/'compilation_key_blocks.json');report=[];flags=[]
for e in ed:
 r={'bank':e['bank'],'id':e['id'],'session':e['session'],'selected':e.get('selected'),'items':[]}
 if e.get('selected'):
  bl=blocks[e['selected']['index']];r['freshQuestionLines']=linesfresh(comp,bl['questionLines']);r['freshKeyLine']=linesfresh(comp,[bl['keyLine']]);r['freshCorrectionLines']=linesfresh(comp,bl['correctionLines'])
  r['keyConfirmed']=norm(bl['key']) in norm(r['freshKeyLine'][0]['text'])
  ht=getdoc(comp)[e['selected']['page']-1].get_text();r['headerConfirmed']=norm(e['selected']['heading']) in norm(ht)
  for item in e['items']:
   a=linesfresh(e['subject']['file'],item.get('thematicPositions',[]));b=linesfresh(comp,item.get('compilationPositions',[]))
   ta=' '.join(z['text'] for z in a);tb=' '.join(z['text'] for z in b)
   rr={'thematicLabel':item['sourceLabel'],'compilationLabel':item['compilationLabel'],'freshThematic':ta,'freshCompilation':tb,'thematicPositions':a,'compilationPositions':b,'sourceTextConfirmed':norm(item.get('thematicText','')) in norm(ta),'compilationTextConfirmed':norm(item.get('compilationText','')) in norm(tb),'ratio':round(difflib.SequenceMatcher(None,norm(ta),norm(tb)).ratio(),4)}
   r['items'].append(rr)
   if not rr['sourceTextConfirmed'] or not rr['compilationTextConfirmed']:flags.append({'bank':e['bank'],'id':e['id'],'item':item['sourceLabel'],'error':'fresh_extraction_difference','data':rr})
  if not r['keyConfirmed'] or not r['headerConfirmed']:flags.append({'bank':e['bank'],'id':e['id'],'error':'key_or_header_missing','key':r['freshKeyLine'],'header':r['headerConfirmed']})
 report.append(r)
(P/'edition_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(P/'edition_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
with open(P/'fresh/edition_diffs.txt','w') as out:
 for r in report:
  if not r.get('selected'):continue
  diffs=[x for x in r['items'] if x['ratio']<.975]
  if diffs:
   out.write('\n'+r['bank']+' Q'+str(r['id'])+' '+str(r['selected']['page'])+' '+r['selected']['heading']+'\n')
   for x in diffs:out.write(f"{x['thematicLabel']} > {x['compilationLabel']}: {x['ratio']}\nTHEM: {x['freshThematic']}\nCOMP: {x['freshCompilation']}\n")
print('Selected',sum(bool(r['selected']) for r in report),'items',sum(len(r['items']) for r in report),'flags',len(flags));print(json.dumps([{'bank':f['bank'],'id':f['id'],'item':f.get('item'),'error':f['error']} for f in flags],ensure_ascii=False))
