from pathlib import Path
import json,re,hashlib,unicodedata
import fitz

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'prepare'
def load(p): return json.loads(Path(p).read_text())
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('ﬃ','ffi').replace('ﬁ','fi').replace('ﬂ','fl')
    return re.sub(r'[^\w]','',s,flags=re.UNICODE).casefold()
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2))

reviewed=load(PREP/'reviewed.json')['banks'];crops=load(PREP/'crops.json')
docs={};texts={};hashes={}
def doc(path):
    if path not in docs:docs[path]=fitz.open(path);hashes[path]=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return docs[path]
def paneltext(p):
    page=doc(p['file'])[p['page']-1]
    return page.get_text('text',clip=fitz.Rect(p['rect']),sort=True).strip()
def refs(parts):return [{'file':p['file'],'sha256':hashes[p['file']],'page':p['page'],'rect':p['rect']} for p in parts]
rows=[];flags=[];geometry=[];capture_ids={}
for cr in crops:
    b,i=cr['bank'],cr['id'];q=next(x for x in reviewed[b]['questions'] if x['id']==i)
    roles={}
    for role in ['subject','correction']:
        parts=cr[role]
        roles[role]=[{'panel':p,'text':paneltext(p)} for p in parts]
        for n,p in enumerate(parts):
            page=doc(p['file'])[p['page']-1];rr=fitz.Rect(p['rect'])
            if not (page.rect+(-.1,-.1,.1,.1)).contains(rr) or rr.is_empty:geometry.append({'bank':b,'id':i,'role':role,'panel':n,'problem':'outside_or_empty'})
            ident=json.dumps([hashes[p['file']],p['page'],[round(float(v),4) for v in p['rect']]],separators=(',',':'))
            src='static/revision_v6/'+hashlib.sha256(ident.encode()).hexdigest()[:24]+'.webp'
            capture_ids[src]=p
    s='\n'.join(p['text'] for p in roles['subject']);c='\n'.join(p['text'] for p in roles['correction'])
    sn,cn=norm(s),norm(c)
    items=[]
    for o in q['options']:
        e=q.get('explanations',{}).get(o['id'],'')
        row={'id':o['id'],'statement':o['text'],'statementInSubjectNative':norm(o['text']) in sn,'explanation':e,'explanationInCorrectionNative':not e or norm(e) in cn,'officialVerdict':q.get('officialVerdicts',{}).get(o['id']),'subjectReferences':refs(cr['subject']),'correctionReferences':refs(cr['correction'])}
        items.append(row)
        if not row['statementInSubjectNative'] or not row['explanationInCorrectionNative']:flags.append({'bank':b,'id':i,**row})
    rows.append({'bank':b,'id':i,'question':q['question'],'questionInSubjectNative':norm(q['question']) in sn,'answer':q.get('answer'),'answerIsEmpty':q.get('answerIsEmpty',False),'correctionComplete':q.get('correctionComplete'),'context':q.get('context',''),'roles':roles,'items':items,'subjectAfterCorrection':bool(cr.get('subjectAfterCorrection'))})
figures=[]
for b,e in reviewed.items():
    for q in e['questions']:
        for field in ['images','stemImages','referenceImages','originalImages']:
            for src in q.get(field,[]):
                if not isinstance(src,str):continue
                p=capture_ids.get(src)
                figures.append({'bank':b,'id':q['id'],'field':field,'src':src,'capture':p,'knownCapture':p is not None,'legacyFileExists':Path('output/site',src).exists()})
        for o in q['options']:
            if o.get('image'):figures.append({'bank':b,'id':q['id'],'field':'options.'+o['id']+'.image','src':o['image'],'capture':capture_ids.get(o['image'])})
write('independent_extraction.json',rows);write('native_mismatches.json',flags);write('geometry_checks.json',geometry);write('figure_inventory.json',figures)
for b in reviewed:
    out=[]
    for r in rows:
        if r['bank']!=b:continue
        out.append('\n### '+b+' ID '+str(r['id'])+' | ANSWER '+str(r['answer'])+(' [EMPTY TRUE]' if r['answerIsEmpty'] else '')+' | COMPLETE '+str(r['correctionComplete']))
        out.append('PREP STEM: '+r['question'])
        for role in ['subject','correction']:
            out.append(role.upper())
            for panel in r['roles'][role]:
                p=panel['panel'];out.append(Path(p['file']).name+' p'+str(p['page'])+' '+str(p['rect'])+'\n'+panel['text'])
        for x in r['items']:
            if not x['statementInSubjectNative']:out.append('SUBJECT MISMATCH '+x['id']+': '+x['statement'])
            if not x['explanationInCorrectionNative']:out.append('DETAIL MISMATCH '+x['id']+': '+x['explanation'])
    (ROOT/(b+'.txt')).write_text('\n'.join(out))
print(json.dumps({'questions':len(rows),'items':sum(len(x['items']) for x in rows),'nativeMismatches':len(flags),'subjectMismatches':sum(not x['statementInSubjectNative'] for x in flags),'explanationMismatches':sum(not x['explanationInCorrectionNative'] for x in flags),'badGeometry':geometry,'figures':len(figures),'interactiveFigures':sum(x['field']=='images' for x in figures),'legacyFigures':sum(x['field']=='originalImages' for x in figures)},ensure_ascii=False))
