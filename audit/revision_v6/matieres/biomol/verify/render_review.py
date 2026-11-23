import json,pathlib,fitz,hashlib
from PIL import Image,ImageDraw,ImageFont
from independent_extract import ROOT,OUT,SRC
D=json.loads((OUT/'independent_sources.json').read_text())
V=OUT/'visual';V.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
index=[]
for fi,(fn,d) in enumerate(D.items()):
    pdf=fitz.open(SRC/fn)
    for pn,p in enumerate(pdf,1):
        key=f'd{fi:02d}_p{pn:02d}'
        path=V/(key+'.png')
        pix=p.get_pixmap(matrix=fitz.Matrix(1.25,1.25));pix.save(str(path))
        index.append({'file':fn,'page':pn,'path':str(path),'key':key})
    # Per document, compact overview at 680 px / page. Text evidence is read separately.
    pgs=[r for r in index if r['file']==fn]
    for offset in range(0,len(pgs),4):
        group=pgs[offset:offset+4];ims=[]
        for r in group:
            im=Image.open(r['path']).convert('RGB');im.thumbnail((680,980))
            tile=Image.new('RGB',(700,1020),'#ddd');tile.paste(im,((700-im.width)//2,35));ImageDraw.Draw(tile).text((10,10),fn[:68]+' p'+str(r['page']),fill='black',font=font);ims.append(tile)
        sheet=Image.new('RGB',(1400,1020*((len(ims)+1)//2)),'white')
        for i,im in enumerate(ims):sheet.paste(im,((i%2)*700,(i//2)*1020))
        sheet.save(V/(f'overview_d{fi:02d}_{offset//4+1}.jpg'),quality=90)
(OUT/'visual_manifest.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
print('Rendered',len(index),'pages')
