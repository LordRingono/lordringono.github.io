import fitz, json, re, unicodedata, html, hashlib
from pathlib import Path
from difflib import SequenceMatcher

ROOT=Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/ssh/verify'
PREP=ROOT/'work/site_v6/ssh/prepare'

def norm(t):
    t=html.unescape(re.sub('<[^>]+>',' ',t or ''))
    t=unicodedata.normalize('NFKD',t).casefold()
    return ''.join(c for c in t if c.isalnum())

def read_lines(path):
    doc=fitz.open(path); out=[]
    for p in doc:
        page=[]
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                t=''.join(s['text'] for s in l['spans']).strip()
                if not t or re.fullmatch(r'\d+/\d+',t): continue
                r=l['bbox']
                # Repeated page furniture only; question text may begin at y=53.
                if r[1]>p.rect.height-45:continue
                if ('Tutorat Santé Lyon Sud' in t and r[1]<65) or (r[1]>p.rect.height-65 and ('SSH' in t or t.startswith('Page '))):continue
                page.append({'page':p.number+1,'rect':list(r),'text':t,'spans':[{'text':s['text'],'size':s['size'],'font':s['font'],'color':s['color']} for s in l['spans']]})
        out.extend(sorted(page,key=lambda l:(round(l['rect'][1],1),l['rect'][0])))
    return out

def chunks(lines,bank,role):
    if bank=='colle2' and role=='correction':
        anchors=[i for i,l in enumerate(lines) if re.match(r'^A\.\s+(?!VRAI\b|FAUX\b)',l['text'])]
        assert len(anchors)==79, len(anchors)
        # Separate each repeated A-E sequence and its keyed correction. The next question's
        # stem may be in the trailing lines; never use those lines as explanation.
        return {k+1:lines[a:anchors[k+1] if k+1<len(anchors) else len(lines)] for k,a in enumerate(anchors)}
    patt=r'^Question\s+(\d+)\s*$' if bank in ['colle1','eb'] else r'^(\d+)\.\s+'
    a=[(i,int(re.match(patt,l['text']).group(1))) for i,l in enumerate(lines) if re.match(patt,l['text']) and l['rect'][0]<95]
    expected={'acc':38,'colle2':79,'colle1':78,'eb':79}[bank]
    assert [n for i,n in a]==list(range(1,expected+1)),(bank,role,[(lines[i]['page'],n,lines[i]['text']) for i,n in a])
    return {n:lines[i:a[k+1][0] if k+1<len(a) else len(lines)] for k,(i,n) in enumerate(a)}

def join(ls):return ' '.join(l['text'] for l in ls)

def parse(chunk,bank,role):
    if bank not in ['colle1','eb'] and role=='correction':
        expanded=[]
        for l in chunk:
            parts=re.split(r'(?<=\S)\s+(?=[A-E]\.\s)',l['text']) if re.match(r'^[A-E]\.\s',l['text']) and not re.search(r'\b(?:VRAI|FAUX)\b',l['text'],re.I) else [l['text']]
            expanded.extend({**l,'text':t} for t in parts)
        chunk=expanded
    result={'pages':sorted(set(l['page'] for l in chunk)),'text':join(chunk),'options':{},'details':{},'verdicts':{},'keys':[],'lines':chunk}
    if bank in ['colle1','eb']:
        anchors=[]
        for i,l in enumerate(chunk):
            m=re.match(r'^[☐✔✘]\s*([A-E])\.\s*(.*)',l['text'])
            if m: anchors.append((i,m.group(1),m.group(2),l['text'][0]))
        assert len(anchors)==5, (bank,role,join(chunk)[:100])
        for k,(i,letter,text,symbol) in enumerate(anchors):
            rest=chunk[i+1:anchors[k+1][0] if k+1<len(anchors) else len(chunk)]
            # Font size/color separate original statement and gray explanatory text.
            continuation=[]; details=[]
            for l in rest:
                if l['text'].startswith(('Bonne(s)','⚠')):break
                size=round(l['spans'][0]['size'],1)
                if size==9.5:continuation.append(l['text'])
                elif role=='correction' and size==8.6:details.append(l['text'])
                else:break
            result['options'][letter]=' '.join([text]+continuation)
            result['details'][letter]=' '.join(details)
            if role=='correction':result['verdicts'][letter]=symbol=='✔'
        result['stem']=join(chunk[1:anchors[0][0]])
        result['keys']=[re.sub(r'[^A-E]','',l['text'].split(':',1)[1]) for l in chunk if l['text'].startswith('Bonne(s) réponse(s)')]
    elif role=='correction':
        # Extract independent printed key and each explicit VRAI/FAUX entry.
        key_indices=[i for i,l in enumerate(chunk) if re.fullmatch(r'[ABCDE]{1,5}',l['text'])]
        result['keys']=[chunk[i]['text'] for i in key_indices]
        key_at=key_indices[0] if key_indices else len(chunk)
        option_anchors=[]
        for i,l in enumerate(chunk[:key_at]):
            m=re.match(r'^([A-E])\.\s+(.*)',l['text'])
            if m:option_anchors.append((i,m.group(1),m.group(2)))
        assert len(option_anchors)==5,(bank,role,key_at,len(option_anchors),join(chunk)[:500])
        for k,(i,letter,text) in enumerate(option_anchors):
            rest=chunk[i+1:option_anchors[k+1][0] if k+1<len(option_anchors) else key_at]
            result['options'][letter]=' '.join([text]+[l['text'] for l in rest])
        result['stem']=join(chunk[1:option_anchors[0][0]]) if bank=='acc' else ''
        verdict_anchors=[]
        for i,l in enumerate(chunk[key_at+1:],key_at+1):
            m=re.match(r'^([A-E])\.\s*(VRAI|FAUX)\b\s*[:;\-–]?\s*(.*)',l['text'],re.I)
            if m:verdict_anchors.append((i,m.group(1),m.group(2),m.group(3)))
        assert len(verdict_anchors) in [0,5],(bank,role,len(verdict_anchors),join(chunk))
        if not verdict_anchors:
            assert len(result['keys'])==1
            result['verdicts']={a:a in result['keys'][0] for a in 'ABCDE'}
            result['details']={a:'' for a in 'ABCDE'}
            result['generalDetail']=join(chunk[key_at+1:])
        for k,(i,letter,verdict,text) in enumerate(verdict_anchors):
            rest=chunk[i+1:verdict_anchors[k+1][0] if k+1<len(verdict_anchors) else len(chunk)]
            detail=[]
            for l in rest:
                # Following course / next question starts in bold at left or centered.
                # These two next-course headings use mixed runs; visually checked at
                # ACC Q16 / Q26 and explicitly excluded from the prior E detail.
                if re.match(r'^(HPI et TDAH :|Raisonnement et décisions médicales)',l['text']):break
                if all('Bold' in s['font'] for s in l['spans'] if s['text'].strip()) and l['rect'][0]<85:break
                if l['rect'][0]<65 and re.match(r'(Cochez|Concernant|À propos|A propos)',l['text']):break
                if l['rect'][0]>140 and all('Bold' in s['font'] for s in l['spans'] if s['text'].strip()):break
                detail.append(l['text'])
            result['details'][letter]=' '.join([text]+detail).strip()
            result['verdicts'][letter]=verdict.upper()=='VRAI'
    else:
        result['stem']=''
    return result

def main():
    manifest=json.loads((PREP/'source_manifest.json').read_text()); extracted={}
    for s in manifest:
        path=Path(s['absolute']); assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
        ls=read_lines(path); parts=chunks(ls,s['bank'],s['role'])
        for n,c in parts.items():
            extracted.setdefault(s['bank'],{}).setdefault(str(n),{})[s['role']]=parse(c,s['bank'],s['role'])
    (OUT/'independent_sources.json').write_text(json.dumps(extracted,ensure_ascii=False,indent=2))
    data=json.loads((PREP/'reviewed.json').read_text())['banks']; compare=[]
    for bank,b in data.items():
        for q in b['questions']:
            src=extracted[bank][str(q['id'])]; subject=src['subject']; corr=src['correction']
            qrec={'bank':bank,'id':q['id'],'subjectPages':subject['pages'],'correctionPages':corr['pages'],'keyImported':q['answer'],'printedKeys':corr['keys'],'perItem':[]}
            for o in q['options']:
                letter=o['id']; st=norm(subject['text']); item=norm(o['text']); rep=norm(corr['options'][letter]); exp=norm(q.get('explanations',{}).get(letter,'')); detail=norm(corr['details'][letter])
                qrec['perItem'].append({'item':letter,'subjectContainsExact':item in st,'repeatedOptionExact':item==rep,'repeatedOptionSimilarity':round(SequenceMatcher(None,item,rep).ratio(),4),'verdict':corr['verdicts'][letter],'importedVerdict':letter in q['answer'],'explanationExact':exp==detail,'explanationSourcePrefix':exp.startswith(detail) if detail else not exp,'originalDetail':corr['details'][letter],'importedDetail':q.get('explanations',{}).get(letter,''),'originalRepeatedItem':corr['options'][letter],'importedItem':o['text']})
            compare.append(qrec)
    (OUT/'independent_comparison.json').write_text(json.dumps(compare,ensure_ascii=False,indent=2))
    exceptions=[]
    for q in compare:
        for i in q['perItem']:
            if not i['subjectContainsExact'] or not i['repeatedOptionExact'] or not i['explanationExact'] or i['verdict']!=i['importedVerdict']:
                exceptions.append({'bank':q['bank'],'id':q['id'],**i})
    (OUT/'independent_exceptions.json').write_text(json.dumps(exceptions,ensure_ascii=False,indent=2))
    print('Extracted',len(compare),'Q',sum(len(q['perItem']) for q in compare),'items; exceptions',len(exceptions))
    print('Missing subject exact',[(q['bank'],q['id'],i['item']) for q in compare for i in q['perItem'] if not i['subjectContainsExact']])
    print('Verdict mismatches',[(q['bank'],q['id'],i['item']) for q in compare for i in q['perItem'] if i['verdict']!=i['importedVerdict']])
    print('Repeateditem mismatches',sum(not i['repeatedOptionExact'] for q in compare for i in q['perItem']))
    print('Explanation mismatches',sum(not i['explanationExact'] for q in compare for i in q['perItem']))
if __name__=='__main__':main()
