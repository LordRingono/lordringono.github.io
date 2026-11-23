import json,re,pathlib,sys,copy,difflib
from independent_extract import norm,compact,H,KEY,ITEM,OUT,ROOT

docs=json.loads((OUT/'independent_sources.json').read_text())
banks=json.loads((ROOT/'work/site_v6/biomol/prepare/reviewed.json').read_text())['banks']
cropmap={(r['bank'],r['id']):r for r in json.loads((ROOT/'work/site_v6/biomol/prepare/crops.json').read_text())}

def items_for(lines):
    out=[];last=None
    for ln in lines:
        m=ITEM.match(ln['text'])
        if m:
            last={'id':m[1],'text':m[2],'lines':[ln]};out.append(last)
        elif last:
            if H.match(ln['text']) or re.match(r'^20\d\d[-–]',ln['text']):last=None
            else:last['text']+=' '+ln['text'];last['lines'].append(ln)
    return out

def clean(s):
    # Surface punctuation and line wrap differences are recorded in raw evidence.
    return compact(s)

def same(a,b):return clean(a)==clean(b)

def trimvf(s):return re.sub(r'^\s*(?:vrai|faux|vraie|fausse)\s*[:,;.]?\s*','',norm(s),flags=re.I)

def compare(a,b):
    if same(a,b):return 'exact_after_unicode_and_punctuation'
    if clean(a) and clean(a) in clean(b):return 'site_contained_in_source'
    if clean(b) and clean(b) in clean(a):return 'source_contained_in_site'
    return 'different'

def enclosed(line,crops):
    r=line['rect'];return any(c['page']==line['page'] and c['rect'][0]<=r[0]+1 and c['rect'][1]<=r[1]+1 and c['rect'][2]>=r[2]-1 and c['rect'][3]>=r[3]-1 for c in crops)

flags=[];rows=[]
def flag(b,q,kind,**kw):flags.append({'bank':b,'id':q['id'],'kind':kind,**kw})

for b,bank in banks.items():
    siteqs=bank['questions'];sn=siteqs[0]['sourceSubject'];cn=siteqs[0]['sourceCorrection']
    subj=docs[sn]['questions'];corr=docs[cn]['questions'];is_ed=b.startswith('ue2.ed.') and b!='ue2.ed.annales'
    if b=='ue2.ed.annales':
        subj=copy.deepcopy(subj);corr=copy.deepcopy(corr)
        # Only the 2013 Q24 is raster-only. Preserve a gap to be read visually.
        subj.insert(1,None);corr.insert(1,None)
    if b=='ue2.ed.2025-2026':
        corr=copy.deepcopy(corr);corr.insert(39,None)
    if len(subj)!=len(siteqs) or len(corr)!=len(siteqs):
        flag(b,{'id':'ALL'},'question_count',site=len(siteqs),subject=len(subj),correction=len(corr));continue
    for n,q in enumerate(siteqs):
        s=subj[n];c=corr[n];crops=cropmap[(b,q['id'])]
        row={'bank':b,'id':q['id'],'sourceSubject':sn,'sourceCorrection':cn,'siteNumber':q.get('sourceNumber'),'items':[],'subject':s,'correction':c}
        if s is None:
            flag(b,q,'raster_subject_manual');rows.append(row);continue
        if c is None:flag(b,q,'raster_correction_manual')
        sf=next((ln['index'] for ln in s['lines'][1:] if ITEM.match(ln['text'])),s['end'])
        slines=[ln for ln in s['lines'] if ln['index']<sf]
        sourceHeading=' '.join([s['text']]+[ln['text'] for ln in slines[1:]])
        row['sourceHeading']=sourceHeading
        row['headingComparison']=compare(q['question'],sourceHeading)
        if row['headingComparison']!='exact_after_unicode_and_punctuation':flag(b,q,'heading_comparison',site=q['question'],source=sourceHeading,comparison=row['headingComparison'])
        row['sourceOptions']=items_for(s['lines'][1:]);
        if len(row['sourceOptions'])!=len(q['options']):flag(b,q,'item_count',site=len(q['options']),source=len(row['sourceOptions']))
        smap={i['id']:i for i in row['sourceOptions']}
        keyindex=c['keys'][0]['index'] if c and c['keys'] else None
        if c:
            row['sourceKeyLiteral']=c['text'] if is_ed else (c['keys'][0]['text'] if c['keys'] else None)
            copt=items_for([ln for ln in c['lines'][1:] if keyindex is None or ln['index']<keyindex])
            det=items_for([ln for ln in c['lines'] if keyindex is not None and ln['index']>keyindex])
        else:copt=[];det=[];row['sourceKeyLiteral']=None
        cmap={i['id']:i for i in copt};dmap={i['id']:i for i in det}
        key=row['sourceKeyLiteral']
        if key and (b.endswith('annales') or is_ed):
            k=re.match(r'([A-F]+(?:\s*\([A-F]+\))?)',key)
            row['key']=k[1] if k else None
            if k and '(' in k[1]:
                if q.get('answer'):flag(b,q,'ambiguous_key_scored',key=k[1],answer=q['answer'])
            elif k and k[1]!=q.get('answer'):flag(b,q,'key_mismatch',source=k[1],site=q.get('answer'))
        elif b.endswith('annales') or is_ed:flag(b,q,'key_manual',answer=q.get('answer'))
        for oi,o in enumerate(q['options']):
            it={'id':o['id'],'siteText':o.get('text',''),'sourceText':smap.get(o['id'],{}).get('text'),'sourceLines':smap.get(o['id'],{}).get('lines',[]),'siteVerdict':o['id'] in q.get('answer',''),'siteDetail':q.get('explanations',{}).get(o['id'],'')}
            it['subjectComparison']=compare(it['siteText'],it['sourceText'] or '')
            if it['subjectComparison']!='exact_after_unicode_and_punctuation':flag(b,q,'item_comparison',item=o['id'],site=it['siteText'],source=it['sourceText'],comparison=it['subjectComparison'])
            it['subjectCropped']=bool(it['sourceLines']) and all(enclosed(ln,crops['subject']) for ln in it['sourceLines'])
            if not it['subjectCropped']:flag(b,q,'subject_bounds',item=o['id'],lines=[l for l in it['sourceLines'] if not enclosed(l,crops['subject'])])
            if b.endswith('autotest'):
                ci=cmap.get(o['id']);ct=ci['text'] if ci else ''
                marker=re.search(r'\b(Vrai|Faux|VRAI|FAUX)\b',ct)
                if marker:
                    it['sourceVerdict']=marker[1].lower()=='vrai';it['sourceDetail']=ct[marker.end():].lstrip(' :,;.');it['correctedStatement']=ct[:marker.start()].rstrip()
                    if it['sourceVerdict']!=it['siteVerdict']:flag(b,q,'verdict_mismatch',item=o['id'],source=it['sourceVerdict'],site=it['siteVerdict'],text=ct)
                    it['correctedStatementComparison']=compare(it['siteText'],it['correctedStatement'])
                    if it['correctedStatementComparison']!='exact_after_unicode_and_punctuation':flag(b,q,'corrected_statement_divergence',item=o['id'],site=it['siteText'],source=it['correctedStatement'])
                else:flag(b,q,'marker_manual',item=o['id'],source=ct);it['sourceDetail']=None
                it['correctionLines']=ci['lines'] if ci else []
            elif b.endswith('annales'):
                it['sourceDetail']=dmap.get(o['id'],{}).get('text','');it['correctionLines']=dmap.get(o['id'],{}).get('lines',[])
                if it['siteDetail'] or it['sourceDetail']:
                    it['detailComparison']=compare(trimvf(it['siteDetail']),trimvf(it['sourceDetail']))
                    if it['detailComparison']!='exact_after_unicode_and_punctuation':flag(b,q,'detail_comparison',item=o['id'],site=it['siteDetail'],source=it['sourceDetail'],comparison=it['detailComparison'])
            if b.endswith('autotest') and it.get('sourceDetail') is not None:
                it['detailComparison']=compare(trimvf(it['siteDetail']),trimvf(it['sourceDetail']))
                if it['detailComparison']!='exact_after_unicode_and_punctuation':flag(b,q,'detail_comparison',item=o['id'],site=it['siteDetail'],source=it['sourceDetail'],comparison=it['detailComparison'])
            if it.get('correctionLines') and not all(enclosed(ln,crops['correction']) for ln in it['correctionLines']):flag(b,q,'correction_bounds',item=o['id'],lines=[l for l in it['correctionLines'] if not enclosed(l,crops['correction'])])
            row['items'].append(it)
        rows.append(row)

(OUT/'comparison_rows.json').write_text(json.dumps(rows,ensure_ascii=False))
(OUT/'comparison_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
from collections import Counter
print(len(rows),'rows',sum(len(r['items']) for r in rows),'items')
print(Counter(f['kind'] for f in flags))
for b in banks:print(b,Counter(f['kind'] for f in flags if f['bank']==b))
