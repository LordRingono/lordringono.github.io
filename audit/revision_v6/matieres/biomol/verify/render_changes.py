from pathlib import Path
import json,fitz,hashlib
from PIL import Image,ImageDraw,ImageFont
B=Path('/workspace/scratch/f3cb3bb97377/work/site_v6/biomol');O=B/'verify';V=O/'visual';new=json.loads((O/'approved_crops.json').read_text());old=json.loads((B/'prepare/crops.json').read_text());old={(r['bank'],r['id']):r for r in old}; panels={}
for r in new:
 for role in ('subject','correction'):
  bef=old[(r['bank'],r['id'])][role]
  for p in r[role]:
   if any(x['file']==p['file'] and x['page']==p['page'] and x['rect']==p['rect'] for x in bef):continue
   k=(p['file'],p['page'],tuple(p['rect']))
   if k not in panels:panels[k]={'panel':p,'uses':[]}
   panels[k]['uses'].append([r['bank'],r['id'],role])
cache={};L=[]
for i,d in enumerate(panels.values(),1):
 p=d['panel'];f=p['file'];cache.setdefault(f,fitz.open(f));pg=cache[f][p['page']-1];pix=pg.get_pixmap(matrix=fitz.Matrix(1.7,1.7),clip=fitz.Rect(p['rect']),alpha=False);dest=V/f'approved_panel_{i:03d}.png';pix.save(dest);d['path']=str(dest);d['index']=i;L.append(d)
(O/'changed_panel_manifest.json').write_text(json.dumps(L,ensure_ascii=False,indent=2))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for offset in range(0,len(L),4):
 sheet=Image.new('RGB',(1400,2020),'#dedede');draw=ImageDraw.Draw(sheet)
 for j,d in enumerate(L[offset:offset+4]):
  x=(j%2)*700;y=(j//2)*1010;im=Image.open(d['path']);im.thumbnail((680,947));sheet.paste(im,(x+(700-im.width)//2,y+57));t=str(d['index'])+' '+str(d['uses'][0])+(' +shared' if len(d['uses'])>1 else '');draw.text((x+5,y+4),t,font=font,fill='black');draw.text((x+5,y+23),f"p{d['panel']['page']} {d['panel']['rect']}",font=font,fill='black')
 sheet.save(V/f'approved_contact_{offset//4+1:02d}.jpg',quality=92)
print(len(L),'unique changed panels', (len(L)+3)//4,'contact sheets')
