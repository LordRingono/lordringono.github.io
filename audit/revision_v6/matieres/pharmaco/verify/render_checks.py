from pathlib import Path
import fitz,json,io,re
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/pharmaco/verify';V=OUT/'visual';V.mkdir(exist_ok=True)
D=fitz.open(ROOT/'output/site/sources/Annales_compilation.pdf')
Q={q['sourceId']:q for b in json.loads((ROOT/'work/site_v6/pharmaco/prepare/reviewed.json').read_text())['banks'].values() for q in b['questions']}
C={x['sourceId']:x for x in json.loads((ROOT/'work/site_v6/pharmaco/prepare/crops.json').read_text())}
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
def render(p,r=None,scale=1.8):
 pix=D[p-1].get_pixmap(matrix=fitz.Matrix(scale,scale),clip=fitz.Rect(r) if r else None,alpha=False)
 return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
def fit(im,w):
 return im.resize((w,round(im.height*w/im.width)),Image.Resampling.LANCZOS)
def stack(ims,w=950):
 arr=[fit(x,w) for x in ims];out=Image.new('RGB',(w,sum(x.height for x in arr)+12*(len(arr)-1)),'white');y=0
 for im in arr:out.paste(im,(0,y));y+=im.height+12
 return out
def board(panels,labels,path,width=950):
 ims=[fit(p,width) for p in panels];out=Image.new('RGB',(width*len(ims),max(im.height for im in ims)+70),(240,242,245));dr=ImageDraw.Draw(out)
 for i,(im,l) in enumerate(zip(ims,labels)):out.paste(im,(i*width,60));dr.text((i*width+12,15),l,font=FONT,fill='black')
 out.save(path)
index={'figures':[],'grids':[],'special':[]}
for sid,q in Q.items():
 if not q.get('images'):continue
 name=sid.replace(':','_')
 original=stack([render(p['page'],p['rect']) for p in C[sid]['subject']])
 interactive=stack([Image.open(ROOT/'output/site'/s).convert('RGB') for s in q['images']])
 path=V/(name+'_figure.png')
 board([original,interactive],[sid+' | Source sujet','Figure interactive actuelle'],path)
 index['figures'].append({'sourceId':sid,'file':str(path),'subjectPages':[p['page'] for p in C[sid]['subject']]})
gridpages=sorted(set(q['shortCorrectionPage'] for q in Q.values() if q.get('shortCorrectionPage')))
for k in range(0,len(gridpages),2):
 pages=gridpages[k:k+2];ims=[render(p,[35,65,558,478]) for p in pages]
 path=V/f'grids_{pages[0]}_{pages[-1]}.png';board(ims,[f'Grille source p{p}' for p in pages],path,width=950);index['grids'].append({'pages':pages,'file':str(path)})
special=['ue4:2022-2023:S2:q14','ue4:2023-2024:S1:q02','ue4:2023-2024:S1:q24','ue4:2021-2022:S1:q12','ue4:2021-2022:S1:q13','ue4:2021-2022:S1:q14','ue4:2020-2021:S2:q10','ue4:2020-2021:PACES:q25','ue4:2020-2021:PACES:q29','ue4:2019-2020:S1:q19','ue4:2018-2019:S1:q06','ue4:2018-2019:S1:q15','ue4:2025-2026:S1:q13','ue4:2025-2026:S1:q14','ue4:2020-2021:S1:q12','ue4:2020-2021:S1:q13','ue4:2020-2021:S1:q14']
for sid in special:
 row=C[sid];s=stack([render(p['page'],p['rect']) for p in row['subject']]);co=[render(p['page'],p['rect']) for p in row['correction'] if 'Grille' not in p.get('fileLabel','')];co=stack(co) if co else Image.new('RGB',(950,100),'white')
 path=V/(sid.replace(':','_')+'_special.png');board([s,co],[sid+' | Sujet','Corrige source integral'],path);index['special'].append({'sourceId':sid,'file':str(path)})
(OUT/'visual_manifest.json').write_text(json.dumps(index,ensure_ascii=False,indent=2));print({k:len(v) for k,v in index.items()})
