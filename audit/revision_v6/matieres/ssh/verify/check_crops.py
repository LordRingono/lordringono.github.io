import fitz, json, hashlib, re, unicodedata, html
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat
ROOT=Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/ssh/verify'
PREP=ROOT/'work/site_v6/ssh/prepare'
def norm(t):
    return ''.join(c for c in unicodedata.normalize('NFKD',html.unescape(re.sub('<[^>]+>',' ',t or ''))).casefold() if c.isalnum())
data=json.loads((PREP/'reviewed.json').read_text())['banks']
crops=json.loads((PREP/'crops.json').read_text())
docs={}; audit=[]; pics=[]
selected={'acc':[1,9,15,16,25,26,34,38], 'colle2':[10,11,12,39,73,74,76], 'colle1':[12,26,39,43,55,69,70,73], 'eb':[5,6,28,37,54,55,69,77]}
(OUT/'visual').mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for qc in crops:
    bank=qc['bank']; q=next(q for q in data[bank]['questions'] if q['id']==qc['id'])
    rec={'bank':bank,'id':q['id'],'panels':[],'subjectOptionsInCrops':{},'correctionDetailsInCrops':{}}
    qimgs=[]; texts={}
    for role in ['subject','correction']:
        texts[role]=[]
        for k,c in enumerate(qc[role]):
            if c['file'] not in docs:docs[c['file']]=fitz.open(c['file'])
            doc=docs[c['file']]; pg=doc[c['page']-1]; rect=fitz.Rect(c['rect'])
            assert pg.rect.contains(rect),(bank,q['id'],role,c)
            assert rect.width>10 and rect.height>10
            tx=pg.get_text(clip=rect); texts[role].append(tx)
            pix=pg.get_pixmap(matrix=fitz.Matrix(1.7,1.7),clip=rect,alpha=False)
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            assert max(ImageStat.Stat(im).stddev)>2,(bank,q['id'],role,'blank')
            p={'role':role,'page':c['page'],'rect':c['rect'],'file':c['file'],'rasterSize':[pix.width,pix.height],'rendered':True,'geometryValid':True,'text':tx}
            rec['panels'].append(p)
            if q['id'] in selected[bank]:
                panel=Image.new('RGB',(960,im.height+34),'#e9edf1'); panel.paste(im,(int((960-im.width)/2),34))
                ImageDraw.Draw(panel).text((12,8),f'{bank} Q{q["id"]} — {role} — page {c["page"]} — panneau {k+1}',font=font,fill='#14232e')
                qimgs.append(panel)
        texts[role]=norm(' '.join(texts[role]))
    for o in q['options']:rec['subjectOptionsInCrops'][o['id']]=norm(o['text']) in texts['subject']
    for a,t in q.get('explanations',{}).items():rec['correctionDetailsInCrops'][a]=norm(t) in texts['correction']
    rec['subjectStemInCrops']=norm(q['question']) in texts['subject']
    rec['sharedContextInCrops']=[norm(c.get('text','')) in texts['subject'] for c in q.get('sharedContexts',[])]
    rec['correctionKeyInCrops']=not q['answer'] or q['answer'].casefold() in texts['correction']
    if qimgs:
        sheet=Image.new('RGB',(960,sum(im.height for im in qimgs)+12*(len(qimgs)-1)),'#cbd5df'); y=0
        for im in qimgs:sheet.paste(im,(0,y));y+=im.height+12
        name=f'{bank}_{q["id"]:02d}.jpg'; sheet.save(OUT/'visual'/name,quality=88)
        pics.append({'bank':bank,'id':q['id'],'path':str(OUT/'visual'/name),'size':list(sheet.size),'panels':len(qimgs)})
    audit.append(rec)
(OUT/'crop_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
(OUT/'visual/manifest.json').write_text(json.dumps(pics,ensure_ascii=False,indent=2))
print('Question pairs',len(audit),'panels',sum(len(q['panels']) for q in audit),'targeted contact sheets',len(pics))
print('Option crop exceptions',[(q['bank'],q['id'],a) for q in audit for a,v in q['subjectOptionsInCrops'].items() if not v])
print('Detail crop exceptions',[(q['bank'],q['id'],a) for q in audit for a,v in q['correctionDetailsInCrops'].items() if not v])
print('Stem crop exceptions',[(q['bank'],q['id']) for q in audit if not q['subjectStemInCrops']])
print('Key crop exceptions',[(q['bank'],q['id']) for q in audit if not q['correctionKeyInCrops']])
