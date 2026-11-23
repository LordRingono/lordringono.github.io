import json, re, unicodedata, hashlib, difflib
from pathlib import Path
from collections import Counter
import fitz
from PIL import Image, ImageChops
import numpy as np

V=Path(__file__).parent
P=V.parent/'prepare'
WS=V.parents[3]
D=fitz.open(WS/'output/site/sources/Annales_compilation.pdf')
R=json.loads((P/'reviewed.json').read_text())
C=json.loads((P/'crops.json').read_text())
A=json.loads((P/'asset_audit.json').read_text())

def save(name, obj): (V/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def norm(t):
    t=unicodedata.normalize('NFKD',t).lower().replace('œ','oe').replace('æ','ae')
    t=t.replace('’',"'").replace('‐','-').replace('–','-').replace('—','-')
    return ''.join(c for c in t if c.isalnum())

changes=[]
for row in C:
    for role in ['subject','correction']:
        panels=[]
        for i,c in enumerate(row[role]):
            page=D[c['page']-1]; x0,y0,x1,y1=c['rect']
            spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip() and s['bbox'][0]<x1 and s['bbox'][2]>x0]
            cuts=[s for s in spans if s['bbox'][1]<y0<s['bbox'][3]]
            if cuts:
                newy=max(s['bbox'][3] for s in cuts)+1
                assert newy-y0<=5, (row,role,i,newy-y0)
                changes.append({'bank':row['bank'],'id':row['id'],'role':role,'panel':i,'page':c['page'],'action':'remove_previous_line_fragment','before':c['rect'].copy(),'after':[x0,newy,x1,y1],'removed_text_spans':[s['text'] for s in cuts]})
                c['rect'][1]=newy
            bottom=[s for s in spans if s['bbox'][1]<y1<s['bbox'][3]]
            if bottom:
                newend=max(s['bbox'][3] for s in bottom)+1
                assert newend-y1<=4, (row,role,i,newend-y1)
                changes.append({'bank':row['bank'],'id':row['id'],'role':role,'panel':i,'page':c['page'],'action':'restore_last_line_descenders_or_formula','before':c['rect'].copy(),'after':[c['rect'][0],c['rect'][1],c['rect'][2],newend],'restored_spans':[s['text'] for s in bottom]})
                c['rect'][3]=newend
            pix=page.get_pixmap(matrix=fitz.Matrix(1,1),clip=fitz.Rect(c['rect']),colorspace=fitz.csGRAY)
            arr=np.frombuffer(pix.samples,dtype=np.uint8)
            if np.sum(arr<210)<8:
                changes.append({'bank':row['bank'],'id':row['id'],'role':role,'panel':i,'page':c['page'],'action':'remove_empty_panel','rect':c['rect'].copy(),'dark_pixels':int(np.sum(arr<210))})
            else: panels.append(c)
        row[role]=panels
    if row['bank']=='annales.ue3.2020-2021.s2' and row['id']==1:
        assert not row['correction']
        row['correction']=[{'file':str(WS/'output/site/sources/Annales_compilation.pdf'),'page':656,'rect':[30,278,570,592],'fileLabel':'Sujets + corrections compilés.pdf'}]
        changes.append({'bank':row['bank'],'id':1,'role':'correction','action':'restore_missing_original_correction','page':656,'rect':[30,278,570,592]})
save('proposed_crops.json',C)
save('crop_repairs.json',changes)

records=[]; candidates=[];corr_candidates=[]
for cr in C:
    q=next(q for q in R['banks'][cr['bank']]['questions'] if q['id']==cr['id'])
    sub='\n'.join(D[c['page']-1].get_text('text',clip=fitz.Rect(c['rect']),sort=True) for c in cr['subject'])
    cor='\n'.join(D[c['page']-1].get_text('text',clip=fitz.Rect(c['rect']),sort=True) for c in cr['correction'])
    ms=list(re.finditer(r'^\s*([A-E])\s*[.)]\s*',sub,re.M))
    opts={m[1]:sub[m.end():ms[j+1].start() if j+1<len(ms) else len(sub)].strip() for j,m in enumerate(ms)}
    cms=list(re.finditer(r'^\s*([A-E])\s*[.)]\s*(VRAI|FAUX)\b',cor,re.M|re.I))
    details={m[1]:{'verdict':m[2].upper(),'text':cor[m.end():cms[j+1].start() if j+1<len(cms) else len(cor)].strip()} for j,m in enumerate(cms)}
    rec={'bank':cr['bank'],'id':q['id'],'sub_labels':[m[1] for m in ms],'correction_labels':[m[1] for m in cms],'items':[]}
    for opt in q['options']:
        l=opt['id'];source=opts.get(l,'');site=opt.get('text','')
        ratio=difflib.SequenceMatcher(None,norm(source),norm(site)).ratio()
        row={'letter':l,'source':source,'site':site,'image':opt.get('image'),'comparison':'image' if opt.get('image') else 'identical_normalized' if norm(source)==norm(site) else 'different','similarity':round(ratio,4),'detail_source':details.get(l),'detail_site':q.get('explanations',{}).get(l),'grid_key':q['answer']}
        rec['items'].append(row)
        if row['comparison']=='different': candidates.append({'bank':cr['bank'],'id':q['id'],**row})
        exp=q.get('explanations',{}).get(l,'')
        if l not in details or ('Voir le corrigé original' not in exp and norm(exp) not in norm(cor)):
            corr_candidates.append({'bank':cr['bank'],'id':q['id'],'letter':l,'site':exp,'source':details.get(l),'correction_text':cor if l not in details else None})
    records.append(rec)
save('native_comparison.json',records)
save('text_differences.json',candidates)
save('correction_text_candidates.json',corr_candidates)
print(json.dumps({'crop_changes':Counter(c['action'] for c in changes),'text_differences':len(candidates),'correction_candidates':len(corr_candidates),'labels':Counter(''.join(r['sub_labels']) for r in records)},ensure_ascii=False))

unique={a['src']:a for a in A}
manifest={r['path']:r for r in json.loads((WS/'output/site/audit/UE3_images.json').read_text())}
ar=[]
for src,a in unique.items():
    f=WS/'output/site'/src
    h=hashlib.sha256(f.read_bytes()).hexdigest()
    m=manifest.get(src)
    actual=Image.open(f).convert('L')
    page=D[a['page']-1]
    pix=page.get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(a['rect']),colorspace=fitz.csGRAY)
    origin=Image.frombytes('L',(pix.width,pix.height),pix.samples)
    def trim(im):
        mask=im.point(lambda x:255 if x<210 else 0)
        b=mask.getbbox()
        return im.crop(b) if b else im
    t1=trim(actual);t2=trim(origin)
    # Lossy WebP and historical white-margin trimming allow a 1-2 px rounding difference.
    # Comparison is a signal, never a claim of bit-exact identity.
    dwh=[t1.width-t2.width,t1.height-t2.height]
    resized=t2.resize(t1.size)
    err=float(np.mean(np.abs(np.asarray(t1,dtype=float)-np.asarray(resized,dtype=float))))
    ar.append({'src':src,'page':a['page'],'rect':a['rect'],'role':a['sourceRole'],'sha256':h,'manifest_hash_match':bool(m and m.get('sha256')==h),'actual_size':actual.size,'render_size':origin.size,'dark_bbox_size_delta':dwh,'mean_absolute_difference':round(err,3),'candidate':max(abs(x) for x in dwh)>3 or err>25})
save('bitmap_comparison.json',ar)
print(json.dumps({'unique_assets':len(ar),'hash_matches':sum(x['manifest_hash_match'] for x in ar),'bitmap_candidates':sum(x['candidate'] for x in ar)},ensure_ascii=False))
