import json, re, pathlib, unicodedata, hashlib, fitz

ROOT=pathlib.Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/biomol/verify'
SRC=ROOT/'sources_biomol/extracted'

def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
    s=s.translate(str.maketrans({'’':"'",'‘':"'",'′':"'",'–':'-','−':'-','‐':'-','‑':'-','→':'->','α':'alpha','β':'beta','γ':'gamma','ε':'epsilon','δ':'delta','µ':'mu'}))
    return re.sub(r'\s+',' ',s).strip()

def compact(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD',norm(s).lower()))

def extract(f):
    d=fitz.open(f); lines=[]; pics=[]; pages=[]
    for pn,p in enumerate(d,1):
        pages.append({'page':pn,'width':p.rect.width,'height':p.rect.height})
        # Keep native line geometry, not preparer's extracted files or rectangles.
        lns=[]
        for b in p.get_text('dict')['blocks']:
            if b['type']==1:
                pics.append({'page':pn,'rect':list(b['bbox']),'width':b['width'],'height':b['height']})
                continue
            for ln in b.get('lines',[]):
                t=''.join(sp['text'] for sp in ln['spans'])
                if not t.strip(): continue
                if 'David Bard' in t or (ln['bbox'][1]>p.rect.height-35 and re.fullmatch(r'\s*\d+\s*',t)):continue
                lns.append({'page':pn,'rect':list(ln['bbox']),'text':norm(t),'spans':[{'text':sp['text'],'font':sp['font'],'color':sp['color'],'flags':sp['flags'],'rect':list(sp['bbox'])} for sp in ln['spans']]})
        lns.sort(key=lambda l:(round(l['rect'][1]/3)*3,l['rect'][0]))
        for ln in lns:
            ln['index']=len(lines); lines.append(ln)
    return {'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pages':pages,'images':pics,'lines':lines}

H=re.compile(r'^(?:QCM\s*)?(\d{1,2}|X)\s*([\'’′]?)\s*\.\s*(.*)$')
KEY=re.compile(r'^([A-F]+(?:\([A-F]+\))?)(?=\s|$|:)')
ITEM=re.compile(r'^([A-GВ])\s*[.\-–)]\s*(.*)$')

def parse(doc):
    lines=doc['lines']; heads=[]
    edkey=doc['file'].startswith('2. Correction ED')
    for ln in lines:
        m=H.match(ln['text'])
        if not m:
            if ln['text'].startswith('Concernant la traduction et le code génétique chez'):
                heads.append({'index':ln['index'],'page':ln['page'],'num':'sans numéro','text':ln['text'],'kind':'question','key':None,'rect':ln['rect']})
            continue
        num,prime,body=m.groups(); k=KEY.match(body)
        if ln['rect'][0]>110 and not edkey and not k:continue
        kind='key' if k and 'CORRECTION' in doc['file'] and not body.startswith(('A propos','A l\'aide')) else 'question'
        if edkey:
            if not k:continue
            kind='question'
        heads.append({'index':ln['index'],'page':ln['page'],'num':num+prime,'text':body,'kind':kind,'key':k.group(1).strip() if k else None,'rect':ln['rect']})
    # An isolated question number and its heading may be extracted as neighboring lines.
    qs=[]
    for h in heads:
        if h['kind']=='question':
            if qs:qs[-1]['end']=h['index']
            qs.append({**h,'end':len(lines)})
    for q in qs:
        q['lines']=lines[q['index']:q['end']]
        q['keys']=[h for h in heads if h['kind']=='key' and q['index']<h['index']<q['end']]
        if 'CORRECTION' in doc['file'] and not q['keys']:
            bare=[ln for ln in q['lines'][1:] if re.fullmatch(r'[A-G]{1,7}',ln['text'])]
            if bare:
                ln=bare[0];q['keys']=[{'index':ln['index'],'page':ln['page'],'num':q['num'],'text':ln['text'],'kind':'key','key':ln['text'],'rect':ln['rect']}]
        last=None; items=[]
        for ln in q['lines'][1:]:
            m=ITEM.match(ln['text'])
            if m:
                last={'id':m.group(1),'text':m.group(2),'lines':[ln]};items.append(last)
            elif last:
                if H.match(ln['text']) or re.fullmatch(r'20\d{2}[-–]20\d{2}.*',ln['text']):last=None
                else:last['text']+=' '+ln['text'];last['lines'].append(ln)
        q['items']=items
    return {'heads':heads,'questions':qs}

if __name__=='__main__':
    docs={}
    for f in sorted(SRC.glob('*.pdf')):
        doc=extract(f);doc.update(parse(doc));docs[f.name]=doc
    (OUT/'independent_sources.json').write_text(json.dumps(docs,ensure_ascii=False))
    (OUT/'source_heads.txt').write_text('\n'.join(f"{name}\n"+'\n'.join(f"p{h['page']} i{h['index']} {h['kind']} {h['num']} {h['text']}" for h in d['heads']) for name,d in docs.items()))
    for name,d in docs.items():print(name,len(d['pages']),len(d['questions']),len(d['heads']))
