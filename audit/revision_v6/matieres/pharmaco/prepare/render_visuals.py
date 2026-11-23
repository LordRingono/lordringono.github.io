import json,fitz
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;V=R/'visual';V.mkdir(exist_ok=True)
B=json.loads(Path('work/site_v6/baseline_exams.json').read_text());KS=json.loads(Path('work/site_v6/roster.json').read_text())['pharmaco']['banks'];QM={q['sourceId']:(k,q) for k in KS for q in B[k]['questions']};C={x['sourceId']:x for x in json.loads((R/'crops.json').read_text())};D=fitz.open('output/site/sources/Annales_compilation.pdf')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
def cropim(p,zoom=1.5):
 pix=D[p['page']-1].get_pixmap(matrix=fitz.Matrix(zoom,zoom),clip=fitz.Rect(p['rect']),alpha=False);return Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
def fit(im,w):
 return im.resize((w,round(im.height*w/im.width)))
def stack(ims,w=800):
 ims=[fit(im,w) for im in ims];out=Image.new('RGB',(w,sum(im.height for im in ims)+15*(len(ims)-1)),'#eee');y=0
 for im in ims:out.paste(im,(0,y));y+=im.height+15
 return out
index=[]
for sid,(k,q) in QM.items():
 if not q.get('images'):continue
 sub=stack([cropim(p) for p in C[sid]['subject']]);inter=stack([Image.open('output/site/'+p) for p in q['images']]);w=1630;h=max(sub.height,inter.height)+65;out=Image.new('RGB',(w,h),'#ddd');dr=ImageDraw.Draw(out);dr.text((15,8),sid+' — sujet authentique',font=font,fill='black');dr.text((830,8),'Figure interactive existante',font=font,fill='black');out.paste(sub,(10,50));out.paste(inter,(820,50));name=sid.replace(':','_');out.save(V/(name+'_figure_compare.png'));index.append({'sourceId':sid,'file':str(V/(name+'_figure_compare.png'))})
# All exact original crops for the source anomalies and missing/delayed correction.
selected=['ue4:2023-2024:S1:q24','ue4:2025-2026:S1:q13','ue4:2025-2026:S1:q14','ue4:2022-2023:S2:q14','ue4:2023-2024:S1:q02','ue4:2021-2022:S1:q12','ue4:2021-2022:S1:q13','ue4:2021-2022:S1:q14','ue4:2020-2021:PACES:q25','ue4:2020-2021:PACES:q29','ue4:2019-2020:S1:q19','ue4:2020-2021:S2:q10','ue4:2018-2019:S1:q06','ue4:2018-2019:S1:q15','ue4:2019-2020:S1:q25','ue4:2020-2021:S1:q12','ue4:2020-2021:S1:q13','ue4:2020-2021:S1:q14']
for sid in selected:
 for role in ['subject','correction']:
  ps=C[sid][role]
  if not ps:continue
  out=stack([cropim(p) for p in ps],w=1000);name=sid.replace(':','_')+'_'+role+'.png';out.save(V/name)
# Every short grid, used to review identity and all extracted cells.
for g in json.loads((R/'grids.json').read_text()):
 pg=g['cells']['1']['page'];pix=D[pg-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False);pix.save(V/f'grid_{pg}.png')
(R/'visual_index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2));print('figure comparisons',len(index),'other panels',len(selected)*2,'grids',14)
