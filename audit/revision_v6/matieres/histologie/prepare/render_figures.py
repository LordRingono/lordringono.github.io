import json,pathlib,fitz
from PIL import Image,ImageDraw
from parse_sources import ROOT,OUT,NAMES
m=json.loads((OUT/'sources_examined.json').read_text());sels=[]
for f in m:
 d=fitz.open(f['file'])
 for i,p in enumerate(d):
  ims=[x for x in p.get_image_info() if (x['bbox'][2]-x['bbox'][0])>30 and (x['bbox'][3]-x['bbox'][1])>30]
  if ims:
   fn=OUT/'render'/f'{pathlib.Path(f["file"]).stem}_p{i+1}.png';p.get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(fn);sels.append({'file':str(fn),'source':f['file'],'page':i+1})
for start in range(0,len(sels),4):
 items=sels[start:start+4];sheet=Image.new('RGB',(1620,2330),'#e8e8e8');dr=ImageDraw.Draw(sheet)
 for j,it in enumerate(items):
  im=Image.open(it['file']);im.thumbnail((800,1120));x=(j%2)*810;y=(j//2)*1165;sheet.paste(im,(x,y+40));dr.text((x+8,y+8),f'{start+j+1} {pathlib.Path(it["file"]).name}',fill='black')
 fn=OUT/'render'/f'figure_sheet_{start//4+1:02d}.jpg';sheet.save(fn,quality=92)
(OUT/'figure_pages.json').write_text(json.dumps(sels,ensure_ascii=False,indent=2));print(len(sels),'figure-pages,', (len(sels)+3)//4,'sheets')
