"""Independent V6 verification: source extraction; never imports preparer parsing code."""
from pathlib import Path
import fitz, re, json, hashlib, unicodedata, collections, difflib

ROOT=Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/pharmaco/verify'
SOURCE=ROOT/'output/site/sources/Annales_compilation.pdf'
DOC=fitz.open(SOURCE)

def save(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))

def norm(s):
    s=unicodedata.normalize('NFKC',s or '').casefold()
    for a,b in [('’',"'"),('`',"'"),('–','-'),('—','-'),('‑','-'),('œ','oe'),('ﬁ','fi'),('ﬂ','fl')]:s=s.replace(a,b)
    return re.sub(r'\s+','',s)

def lines_of(pn):
    p=DOC[pn-1]; out=[]
    for block in p.get_text('dict')['blocks']:
        for l in block.get('lines',[]):
            t=''.join(s['text'] for s in l['spans']).strip()
            if not t:continue
            out.append({'page':pn,'bbox':[round(v,3) for v in l['bbox']],'text':t})
    out.sort(key=lambda l:(round(l['bbox'][1],1),l['bbox'][0]))
    return out

PAGES={pn:lines_of(pn) for pn in range(699,987)}
save('independent_pages.json',PAGES)

covers=[]
for pn in range(699,987):
    t=' '.join(l['text'] for l in PAGES[pn])
    if not re.search(r'Type de l.épreuve',t):continue
    m=re.search(r'(Sujet|Correction) UE4(.*?)(20\d\d)\s*-\s*(20\d\d)',t,re.I)
    if not m:raise ValueError((pn,t[:100]))
    session='PACES' if 'PACES' in m[2] else ('S2' if re.search('session 2',m[2],re.I) else 'S1')
    covers.append({'page':pn,'role':'subject' if m[1]=='Sujet' else 'correction','year':m[3]+'-'+m[4], 'session':session,'title':m[0]})
for i,c in enumerate(covers): c['end']=(covers[i+1]['page']-1 if i+1<len(covers) else 986)

prefix=re.compile(r'^(?:Cochez|Cocher|Concernant|Parmi|Quelle|A propos|À propos|Soit le pharmacophore|On mesure|L’évaluation de la balance|L’encadrement éthique|HORS PROGRAMME|Hors programme)',re.I)
numbered=re.compile(r'^(\d{1,2})[.)]\s+([A-ZÀÉÎÔ])')
itempat=re.compile(r'^([A-J])[.)]\s*(.*)')
segments=[]; diagnostics=[]
for c in covers:
    body=[]
    start=c['page']+1+(1 if c['role']=='correction' else 0)
    for pn in range(start,c['end']+1):
        body += [l.copy() for l in PAGES[pn] if 65<l['bbox'][1]<780]
    num=[i for i,l in enumerate(body) if numbered.match(l['text']) and l['bbox'][0]<80]
    if num:
        heads=num;mode='printed_number'
    else:
        mode='unnumbered_sequence'
        candidates=[i for i,l in enumerate(body) if prefix.match(l['text']) and l['bbox'][0]<80]
        heads=[]
        for i in candidates:
            if heads:
                prev=heads[-1]
                between=body[prev:i]
                labels=any(itempat.match(l['text']) for l in between)
                special=('hors programme' in body[prev]['text'].casefold() or ('pharmacophore' in ' '.join(l['text'] for l in between).lower() and body[i]['page']>body[prev]['page']))
                if not labels and not special:continue
            heads.append(i)
    nums=[]
    for seq,i in enumerate(heads,1):
        end=heads[seq] if seq<len(heads) else len(body)
        ls=body[i:end]
        m=numbered.match(ls[0]['text']);no=int(m[1]) if m else seq;nums.append(no)
        seg={'year':c['year'],'session':c['session'],'role':c['role'],'number':no,'method':mode,'startPage':ls[0]['page'],'lines':ls}
        segments.append(seg)
    diagnostics.append({**c,'bodyPages':[start,c['end']],'mode':mode,'count':len(heads),'numbers':nums,'headers':[{'number':int(numbered.match(body[i]['text'])[1]) if numbered.match(body[i]['text']) else k+1,**body[i]} for k,i in enumerate(heads)]})
save('independent_inventory.json',diagnostics)
save('independent_segments.json',segments)
for x in diagnostics:print(x['year'],x['session'],x['role'],x['bodyPages'],x['mode'],x['count'],x['numbers'])
