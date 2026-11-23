from pathlib import Path
import json,math
import fitz
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'prepare'
VIS=ROOT/'visual';VIS.mkdir(exist_ok=True)
docs={}
def render(file,page,rect=None,scale=2):
    if file not in docs:docs[file]=fitz.open(file)
    p=docs[file][page-1]
    pix=p.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=fitz.Rect(rect) if rect else None,alpha=False)
    return Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def label(im,title):
    out=Image.new('RGB',(max(800,im.width),im.height+32),'white');out.paste(im,(0,32));ImageDraw.Draw(out).text((5,5),title,font=font,fill='black');return out
crops=json.loads((PREP/'crops.json').read_text());ci={(x['bank'],x['id']):x for x in crops}
manifest=[]
for role,pgs in [('subject',range(1,4)),('correction',range(1,8))]:
    source=ci[('bio.ann.cm2',1)][role][0]['file']
    for p in pgs:
        dest=VIS/f'anncm2_{role}_p{p}.png';render(source,p,scale=2).save(dest);manifest.append({'kind':'scanned_source','file':source,'page':p,'render':str(dest)})
audits=json.loads((PREP/'audit.json').read_text())
for a in audits:
    if not a.get('errata'):continue
    b,i=a['bank'],a['id'];parts=ci[(b,i)]['correction'];ims=[render(p['file'],p['page'],p['rect']) for p in parts];out=Image.new('RGB',(max(x.width for x in ims),sum(x.height for x in ims)+len(ims)*32),'white');y=0
    for p,im in zip(parts,ims):
        ImageDraw.Draw(out).text((5,y+4),Path(p['file']).name+' p'+str(p['page']),font=font,fill='black');y+=32;out.paste(im,(0,y));y+=im.height
    dest=VIS/f'erratum_{b}_{i}.png';out.save(dest);manifest.append({'kind':'erratum','bank':b,'id':i,'render':str(dest),'items':a['errata']})
figures=json.loads((ROOT/'figure_inventory.json').read_text());unique={}
for f in figures:
    if f['field']=='images':unique.setdefault(f['src'],{'capture':f['capture'],'questions':[]})['questions'].append(f['bank']+'/'+str(f['id']))
tiles=[]
for n,(src,f) in enumerate(unique.items(),1):
    p=f['capture'];im=render(p['file'],p['page'],p['rect'],scale=2)
    dest=VIS/f'figure_{n:02d}.png';im.save(dest)
    manifest.append({'kind':'figure','number':n,'src':src,'questions':f['questions'],'capture':p,'render':str(dest)})
    ratio=min(680/im.width,800/im.height);thumb=im.resize((round(im.width*ratio),round(im.height*ratio)))
    title=f'{n:02d} '+', '.join(f['questions']);tile=Image.new('RGB',(710,855),'#eee');draw=ImageDraw.Draw(tile);draw.text((8,8),title[:69],font=font,fill='black');tile.paste(thumb,(10,40));tiles.append(tile)
for n in range(0,len(tiles),4):
    out=Image.new('RGB',(1420,1710),'#ddd')
    for j,t in enumerate(tiles[n:n+4]):out.paste(t,((j%2)*710,(j//2)*855))
    out.save(VIS/f'figures_sheet_{n//4+1:02d}.jpg',quality=95)
(ROOT/'visual_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print('Unique figures',len(unique),'sheets',math.ceil(len(unique)/4),'visual items',len(manifest))
