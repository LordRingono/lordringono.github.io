import fitz,json,re,unicodedata,pathlib,hashlib
ROOT=pathlib.Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/embryologie/prepare'
def normfile(s):
 s=unicodedata.normalize('NFKD',s);s=''.join(c for c in s if not unicodedata.combining(c));s=re.sub(r'_[0-9a-f]{10}(?=\.pdf$)','',s);return re.sub(r'[^a-z0-9]','',s.lower())
B=json.load(open(ROOT/'work/site_v6/baseline_exams.json'));banks={k:v for k,v in B.items() if v.get('ue')=='ue5e'}
P=list((ROOT/'output/site/sources/revision_v4').glob('*.pdf'))+list((ROOT/'work/site_v6/materialized/embryo_original').rglob('*.pdf'));N={normfile(p.name):p for p in P}
names=sorted(set(q.get(role) for b in banks.values() for q in b['questions'] for role in ['sourceSubject','sourceCorrection'] if q.get(role)))
M={};E={}
for name in names:
 p=N.get(normfile(name))
 if not p:
  print('MISSING',name);continue
 M[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sourceFile':name}
 d=fitz.open(p);pages=[]
 for pi,page in enumerate(d):
  lines=[]
  for block in page.get_text('dict')['blocks']:
   if 'lines' not in block:continue
   for line in block['lines']:
    spans=[{'text':s['text'],'bbox':list(s['bbox']),'font':s['font'],'size':s['size'],'color':s['color'],'flags':s['flags']} for s in line['spans']]
    t=''.join(s['text'] for s in spans)
    if t.strip():lines.append({'text':t.strip(),'bbox':list(line['bbox']),'spans':spans})
  lines.sort(key=lambda l:(round(l['bbox'][1],1),l['bbox'][0]))
  pages.append({'page':pi+1,'width':page.rect.width,'height':page.rect.height,'lines':lines,'images':[list(x) for x in page.get_image_rects(im[0]) for im in []] if False else []})
 E[name]=pages
(OUT/'source_manifest.json').write_text(json.dumps(M,ensure_ascii=False,indent=2));(OUT/'extraction.json').write_text(json.dumps(E,ensure_ascii=False))
R=re.compile(r'^(?:Q(?:CM|RU)?\s*)?(\d{1,3})\s*[-–—:.]\s*(.*)',re.I)
for name,pages in E.items():
 h=[(p['page'],round(l['bbox'][1],1),l['text']) for p in pages for l in p['lines'] if R.match(l['text'])]
 print(name,'PAGES',len(pages),'HEADERS',len(h));print(h[:5])
