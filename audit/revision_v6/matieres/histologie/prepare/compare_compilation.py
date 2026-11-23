import json,re,pathlib,fitz,sys,difflib
from parse_sources import ROOT,OUT,BASE,NAMES,norm,text,mergelines
try:from rapidfuzz.fuzz import ratio,partial_ratio
except ImportError:
 def ratio(a,b):return 100*difflib.SequenceMatcher(None,a,b).ratio()
 def partial_ratio(a,b):return 100 if a in b else ratio(a,b)
DOC=fitz.open(ROOT/'output/site/sources/Annales_compilation.pdf');ls=[];headings={}
for pi in range(988,len(DOC)):
 pg=DOC[pi]; raw=[]
 for b in pg.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   raw.append({'text':''.join(s['text'] for s in l['spans']),'rect':list(l['bbox']),'spans':[{k:s[k] for k in ['text','font','size','color','flags']} for s in l['spans']]})
 lines=mergelines(raw);headings[pi+1]=next((l['text'].strip() for l in lines if 'UE5' in l['text'] and ('Sujet' in l['text'] or 'Correction' in l['text'])),DOC[pi].get_text(sort=True).splitlines()[0] if DOC[pi].get_text().strip() else '')
 if 'Correction' not in headings[pi+1]:continue
 for l in lines:
  if re.search(r'(?:Correction UE5|Tutorat Santé Lyon Sud|\d+\s*/\s*\d+)',l['text']):continue
  ls.append(dict(l,page=pi+1,heading=headings[pi+1]))
keys=[]
for i,l in enumerate(ls):
 tt=l['text'].strip();m=re.fullmatch(r'(?:Réponses?\s*:?\s*)?([ABCDE]{1,5})',tt,re.I)
 if not m or len(set(m[1]))!=len(m[1]):continue
 # Last A option starts original item group; key must follow its E option.
 ast=None
 for j in range(i-1,max(-1,i-70),-1):
  if re.match(r'^A\s*[.\-–)]\s*',ls[j]['text'].strip()):ast=j;break
 if ast is None:continue
 inds=[(j,re.match(r'^([A-E])\s*[.\-–)]\s*',ls[j]['text'].strip())) for j in range(ast,i)]
 inds=[(j,m[1]) for j,m in inds if m]
 if [a[1] for a in inds] not in [list('ABCDE'),list('ABCD')]:continue
 opts={}
 for k,(j,label) in enumerate(inds):opts[label]=text(ls[j:inds[k+1][0] if k+1<len(inds) else i])
 if any(re.search(r'^'+k+r'\s*[.\-–)]\s*(VRAI|FAUX)',v) for k,v in opts.items()):continue
 # Collect following explanation lines through next 5-item group.
 end=i+1
 while end<len(ls):
  if end>i+1 and re.match(r'^\d{1,2}\s*[.\-–)]',ls[end]['text'].strip()):break
  if end>i+1 and re.match(r'^(?:Parmi ces|Concernant|Quelle|Les propositions|En fonction|En utilisant)',ls[end]['text'].strip()) and ls[end]['rect'][0]<110:break
  if end-i>90:break
  end+=1
 keys.append({'page':l['page'],'key':m[1].upper(),'heading':l['heading'],'options':opts,'questionLines':ls[ast:i],'keyLine':l,'correctionLines':ls[i+1:end]})
CAN=json.loads((OUT/'canonical.json').read_text());res=[]
for bank,qs in CAN.items():
 if '.ann.' not in bank:continue
 for q in qs:
  scores=[]
  for n,k in enumerate(keys):
   vv=[]
   for it in q['items']:
    a=norm(it['subject']);b=norm(re.sub(r'^[A-E]\s*[.\-–)]\s*','',k['options'].get(it['id'],'')))
    vv.append(ratio(a,b))
   score=sum(vv)/len(vv)
   if score>90:scores.append({'index':n,'score':round(score,2),'ratios':[round(v,2) for v in vv],'page':k['page'],'key':k['key'],'heading':k['heading']})
  scores.sort(key=lambda z:z['score'],reverse=True)
  res.append({'bank':bank,'id':q['id'],'referenceKey':q['baselineKey'],'matches':scores})
(OUT/'compilation_key_blocks.json').write_text(json.dumps(keys,ensure_ascii=False,indent=2));(OUT/'compilation_key_matches.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));(OUT/'compilation_headings.json').write_text(json.dumps(headings,ensure_ascii=False,indent=2))
print('Keys found',len(keys),'matching Q',sum(bool(x['matches']) for x in res))
for r in res:
 if r['matches']:
  m=r['matches'][0]
  if m['key']!=r['referenceKey']:print(r['bank'],r['id'],r['referenceKey'],'vs',[(m['page'],m['key'],m['score']) for m in r['matches']])
 else:print('NO MATCH',r['bank'],r['id'])
