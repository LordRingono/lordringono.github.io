from pathlib import Path
import json, fitz, re, unicodedata, collections

ROOT=Path('/workspace/scratch/f3cb3bb97377')
V=ROOT/'work/site_v6/embryologie/verify'
P=ROOT/'work/site_v6/embryologie/prepare'
CI=json.load(open(V/'coverage_initial.json'))
C={(r['bank'],r['id']):r for r in json.load(open(V/'approved_crops.json'))}
S={(r['bank'],r['id']):r for r in json.load(open(V/'subjects_initial.json'))}
docs={}
def norm(t):
    return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t.replace('œ','oe')).encode('ascii','ignore').decode().lower())
def d(file):
    if file not in docs: docs[file]=fitz.open(file)
    return docs[file]
def covered(line,crops):
    r=fitz.Rect(line['bbox'])
    parts=[r&fitz.Rect(c['rect']) for c in crops if c['page']==line['page'] and not (r&fitz.Rect(c['rect'])).is_empty]
    xs=sorted(set([r.x0,r.x1]+[p.x0 for p in parts]+[p.x1 for p in parts]))
    ys=sorted(set([r.y0,r.y1]+[p.y0 for p in parts]+[p.y1 for p in parts]))
    area=sum((x1-x0)*(y1-y0) for x0,x1 in zip(xs,xs[1:]) for y0,y1 in zip(ys,ys[1:])
             if any(fitz.Point((x0+x1)/2,(y0+y1)/2) in p for p in parts))
    return area/max(r.get_area(),1)>.97
reports=[]; flags=[]
for row in CI:
    key=row['bank'],row['id']; crop=C[key]
    rep={'bank':key[0],'id':key[1], 'correction':{}, 'subject':{}}
    for role in ['subject','correction']:
        crops=crop[role]; valid=[]; texts=[]
        for c in crops:
            page=d(c['file'])[c['page']-1]; rect=fitz.Rect(c['rect'])
            ok=rect.width>20 and rect.height>10 and rect in page.rect
            valid.append(ok); texts.append(page.get_text(clip=rect))
            if not ok: flags.append({'bank':key[0],'id':key[1],'role':role,'issue':'invalid_rect','crop':c})
        rep[role]={'panels':len(crops),'rectsValid':all(valid),'textLength':sum(map(len,texts))}
        if role=='subject' and key in S:
            txt=norm(' '.join(texts)); items=[]
            for item in S[key]['items']:
                checked=norm(item.get('sourceText','')) in txt
                items.append({'id':item['id'],'textIncluded':checked})
                if not checked: flags.append({'bank':key[0],'id':key[1],'role':role,'issue':'subject_text_not_whole','item':item['id'],'expected':item.get('sourceText',''),'cropText':' '.join(texts)})
            rep[role]['items']=items
    expected=[]
    for item in row['items']:
        segs=item['sourceSegments']
        for seg in segs:
            for line in seg['lines']:
                # Annales S2 Q12 is followed by an unnumbered new question;
                # the initial independent parser retained it as a duplicate item.
                if key==('embryo.ann.s2',12) and line['page']==4 and line['bbox'][1]>300: continue
                expected.append((item['id'],line))
    misses=[]
    for iid,line in expected:
        ok=covered(line,crop['correction'])
        if not ok: misses.append({'item':iid,'page':line['page'],'bbox':line['bbox'],'text':line['text']})
    rep['correction'].update(expectedLines=len(expected),linesIncluded=len(expected)-len(misses))
    if misses: flags.append({'bank':key[0],'id':key[1],'role':'correction','issue':'correction_line_not_whole','misses':misses})
    reports.append(rep)
(V/'crop_geometry.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
(V/'crop_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('Questions',len(reports),'panels',sum(x[r]['panels'] for x in reports for r in ['subject','correction']))
print('Flags',len(flags),collections.Counter(f['issue'] for f in flags))
for f in flags:
    if 'misses' in f: print(f['bank'],f['id'],f['role'],f['issue'],f['misses'])
    else: print({k:v for k,v in f.items() if k!='cropText'})
