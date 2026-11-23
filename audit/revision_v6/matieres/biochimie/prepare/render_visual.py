from pathlib import Path
import json,fitz
from PIL import Image,ImageDraw
base=Path('work/site_v6/biochimie/prepare'); out=base/'visual';out.mkdir(exist_ok=True)
f=json.loads((base/'fresh_source_audit.json').read_text()); pages=sorted({l['page'] for q in f for l in q['subjectLines']})
doc=fitz.open('output/site/sources/Annales_compilation.pdf')
idx=[]
for k in range(0,len(pages),4):
 ps=pages[k:k+4]; canvas=Image.new('RGB',(1440,2100),'#dddddd');draw=ImageDraw.Draw(canvas)
 for j,p in enumerate(ps):
  pg=doc[p-1]; pix=pg.get_pixmap(matrix=fitz.Matrix(700/pg.rect.width,700/pg.rect.width),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  x=(j%2)*720+10;y=(j//2)*1050+30;canvas.paste(im,(x,y));draw.text((x,y-22),f'PAGE {p} - SUJET ORIGINAL',fill='black')
 dest=out/f'subjects_{k//4:02d}.jpg';canvas.save(dest,quality=93);idx.append({'file':str(dest),'pages':ps})
(base/'visual_index.json').write_text(json.dumps(idx,indent=2))
grids=json.load(open('work/agents/ue2/grid_evidence.json'))
for k in range(0,len(grids),4):
 canvas=Image.new('RGB',(1440,2100),'#ddd');d=ImageDraw.Draw(canvas)
 for j,g in enumerate(grids[k:k+4]):
  p=g['page'];pg=doc[p-1];pix=pg.get_pixmap(matrix=fitz.Matrix(700/pg.rect.width,700/pg.rect.width),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);x=j%2*720+10;y=j//2*1050+30;canvas.paste(im,(x,y));d.text((x,y-22),f'GRILLE {g["sourceSet"]} p{p}',fill='black')
 canvas.save(out/f'grids_{k//4:02d}.jpg',quality=95)
print('subject pages',len(pages),'contact sheets',len(idx))
