from pathlib import Path
import fitz,re,json,collections,hashlib
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/pharmaco/verify'
def load(p):return json.loads(p.read_text())
def save(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
DOC=fitz.open(ROOT/'output/site/sources/Annales_compilation.pdf')
SEG=load(OUT/'independent_segments.json');PAGES={int(k):v for k,v in load(OUT/'independent_pages.json').items()}
INV=load(OUT/'independent_inventory.json')
CROPS=load(ROOT/'work/site_v6/pharmaco/prepare/crops.json')
QS={q['sourceId']:q for b in load(ROOT/'work/site_v6/pharmaco/prepare/reviewed.json')['banks'].values() for q in b['questions']}
INDEX={(s['year'],s['session'],s['role'],s['number']):s for s in SEG}
GRIDS={};GFLAGS=[]
for x in INV:
 if x['role']!='correction':continue
 p=x['page']+1;w=DOC[p-1].get_text('words');cells={}
 for word in w:
  m=re.fullmatch(r'N[°º](\d+)',word[4])
  if not m:continue
  n=int(m[1]);same=[z for z in w if z[0]>word[0]+1 and abs(z[1]-word[1])<3]
  same.sort(key=lambda z:z[0]);a=same[0] if same else None
  cells[n]={'number':n,'key':a[4] if a else None,'page':p,'numberRect':list(word[:4]),'answerRect':list(a[:4]) if a else None}
 GRIDS[(x['year'],x['session'])]=cells
 if len(cells)!=100:GFLAGS.append({'page':p,'cells':len(cells)})
save('independent_grids.json',[{'year':y,'session':s,'cells':list(v.values())} for (y,s),v in GRIDS.items()])

FLAGS=[];RESULT=[]
def inside(a,b,tol=1.0):return a[0]>=b[0]-tol and a[1]>=b[1]-tol and a[2]<=b[2]+tol and a[3]<=b[3]+tol
def intersection_area(a,b):
 x=max(0,min(a[2],b[2])-max(a[0],b[0]));y=max(0,min(a[3],b[3])-max(a[1],b[1]));return x*y
def signature(l):return (l['page'],tuple(l['bbox']),l['text'])
for row in CROPS:
 sid=row['sourceId'];q=QS[sid];n=int(q['sourceNumber']);base=(q['year'],q['session']);r={'sourceId':sid,'bank':row['bank'],'id':row['id'],'roles':{}}
 for role in ['subject','correction']:
  cn=n if role=='subject' else (n-1 if base==('2021-2022','S1') and n>13 else n)
  seg=None if role=='correction' and base==('2021-2022','S1') and n==13 else INDEX.get(base+(role,cn))
  expected=[l for l in seg['lines'] if not l['text'].startswith('Questions 13 à 14')] if seg else []
  if base==('2020-2021','S1') and n in [13,14]:expected+= [l for l in INDEX[base+(role,12)]['lines'] if l['text'].startswith('Questions 13 à 14')]
  panels=row[role];info={'panelCount':len(panels),'expectedLines':len(expected),'missingLines':[],'extraneousLines':[],'imageBoxes':[],'grid':None,'correctRolePages':True}
  for pp in panels:
   pg=DOC[pp['page']-1];rect=pp['rect']
   if pp['file']!=str(ROOT/'output/site/sources/Annales_compilation.pdf') or not inside(rect,list(pg.rect),0):FLAGS.append({'sourceId':sid,'role':role,'type':'invalid_rect','panel':pp})
   expectedrange=next(x for x in INV if x['year']==base[0] and x['session']==base[1] and x['role']==role)
   if not expectedrange['page']<=pp['page']<=expectedrange['end']:FLAGS.append({'sourceId':sid,'role':role,'type':'wrong_role_page','panel':pp});info['correctRolePages']=False
  for l in expected:
   if not any(pp['page']==l['page'] and inside(l['bbox'],pp['rect']) for pp in panels):info['missingLines'].append(l)
  sigs=set(signature(l) for l in expected)
  for pp in panels:
   gridpage=GRIDS[base][cn]['page'] if role=='correction' and cn in GRIDS[base] else None
   if role=='correction' and pp['page']==gridpage:
    cell=GRIDS[base][cn];info['grid']=cell
    if not inside(cell['numberRect'],pp['rect']) or not inside(cell['answerRect'],pp['rect']):FLAGS.append({'sourceId':sid,'type':'grid_cell_truncated','panel':pp,'cell':cell})
    others=[x['number'] for x in GRIDS[base].values() if x['number']!=cn and (intersection_area(x['numberRect'],pp['rect'])>1 or intersection_area(x['answerRect'],pp['rect'])>1)]
    if others:FLAGS.append({'sourceId':sid,'type':'neighbor_grid_cell_overlap','otherNumbers':others,'panel':pp})
    continue
   for l in PAGES[pp['page']]:
    if not 65<l['bbox'][1]<780:continue
    if intersection_area(l['bbox'],pp['rect'])>2 and signature(l) not in sigs:
     info['extraneousLines'].append(l)
   # Inspect embedded figures intersecting the panel. Their entire bbox must remain visible.
   for im in DOC[pp['page']-1].get_image_info():
    box=list(im['bbox']);area=intersection_area(box,pp['rect'])
    if area>25 and 65<box[1]<780:
     inf={'page':pp['page'],'bbox':box,'fullyIncluded':inside(box,pp['rect'],1.5),'imageWidth':im['width'],'imageHeight':im['height']}
     info['imageBoxes'].append(inf)
     if not inf['fullyIncluded']:FLAGS.append({'sourceId':sid,'role':role,'type':'image_cut','image':inf,'panel':pp})
  if info['missingLines']:FLAGS.append({'sourceId':sid,'role':role,'type':'missing_lines','lines':info['missingLines']})
  if info['extraneousLines']:FLAGS.append({'sourceId':sid,'role':role,'type':'extra_lines','lines':info['extraneousLines']})
  if role=='correction' and seg and not info['grid']:FLAGS.append({'sourceId':sid,'role':role,'type':'no_grid_panel'})
  r['roles'][role]=info
 RESULT.append(r)
save('geometry_coverage.json',RESULT);save('geometry_flags.json',FLAGS+GFLAGS)
print('GEOMETRY FLAGS',collections.Counter(f.get('type','grid_extraction') for f in FLAGS+GFLAGS))
for f in FLAGS+GFLAGS:print(json.dumps(f,ensure_ascii=False))
