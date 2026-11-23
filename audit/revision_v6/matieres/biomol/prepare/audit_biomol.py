from pathlib import Path
import fitz, json, re, unicodedata, difflib, hashlib
from copy import deepcopy

ROOT=Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/biomol/prepare'
SOURCE=ROOT/'sources_biomol/extracted'
BASE=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text())
BANKS={k:deepcopy(b) for k,b in BASE.items() if b.get('ue')=='ue2b'}
DOCS={}; LINES={}

def norm(t):
    t=unicodedata.normalize('NFKC',t).replace('’',"'").replace('`',"'").replace('′',"'").replace('\xad','')
    t=t.replace('ﬀ','ff').replace('ﬁ','fi').replace('ﬂ','fl')
    return re.sub(r'\s+',' ',t).strip()

def cmp(t):
    return re.sub(r'[^\w]', '', norm(t).lower())

def load(name):
    if name in LINES:return LINES[name]
    d=DOCS[name]=fitz.open(SOURCE/name)
    ll=[]
    for pn,p in enumerate(d,1):
        ls=[]
        for block in p.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                txt=norm(''.join(s['text'] for s in line['spans']))
                if not txt:continue
                bbox=list(line['bbox'])
                if txt.startswith('David Bard') or (re.fullmatch(r'\d+',txt) and (bbox[1]<48 or bbox[3]>p.rect.height-45)):continue
                ls.append({'page':pn,'rect':bbox,'text':txt,'spans':[{'text':s['text'],'color':s['color'],'font':s['font'],'flags':s['flags'],'rect':list(s['bbox'])} for s in line['spans']]})
        ll.extend(sorted(ls,key=lambda l:(round(l['rect'][1],1),l['rect'][0])))
    for i,l in enumerate(ll):l['index']=i
    LINES[name]=ll
    return ll

NUM_RE=re.compile(r'^(?:QCM\s*)?(\d{1,3}|X)([\'’′]?)\s*[.):-]\s*(.*)$',re.I)
KEY_RE=re.compile(r'^([A-J](?:\s*[,;/(\-]?\s*[A-J])*\)?)(?=\s|[.,;:]|$)')
OPT_RE=re.compile(r'^([A-J])\s*[.\-–:)\u2014]\s*(.*)$')
YEAR_RE=re.compile(r'^20\d{2}\s*(?:[-–/]|à)\s*20\d{2}')
SECTION_RE=re.compile(r'^(?:Wooclap\b|Partie [A-Z]\.|[IVX]+\. Etude|A propos (?:du début|de la fin)|Le nom officiel de cette mutation|La mutation est en fait localisée|Pour étudier la région|Pour essayer de prédire|Le séquençage de l\'ADN|Code génétique$|Deuxième lettre$|• III\.|Le schéma ci-dessus représente|Normal(?: muté)?$)',re.I)

def candidates(name,keyonly=False):
    ll=load(name);starts=[];keys=[]
    for i,l in enumerate(ll):
        m=NUM_RE.match(l['text'])
        if not m:continue
        n,prime,tail=m.groups(); n=n+prime
        km=KEY_RE.match(tail)
        iskey=(bool(km) and not re.match(r'^A\s+(?:propos\b|l\'aide\b)',tail,re.I)) or re.match(r'^(?:Tout\s+faux|Tout\s+vrai|Aucune|HP|Hors programme|Tous|Annul)',tail,re.I)
        if prime and '-' in l['text'][:5] and not l['text'].startswith('QCM'):continue
        if name.startswith('3. Annales ED') and (l['rect'][0]>80 or tail.startswith(',')):continue
        c={'num':n,'index':i,'page':l['page'],'rect':l['rect'],'heading':tail,'key':re.sub(r'[^A-J]','',km.group(1)) if km else None,'isKey':bool(iskey)}
        if iskey:keys.append(c)
        else:starts.append(c)
    # A question deliberately has no number in both supplied originals.
    if name.startswith('2. Annales Traduction'):
        for l in ll:
            if l['text']=='Concernant la traduction et le code génétique chez les eucaryotes :':
                starts.append({'num':'sans numéro','index':l['index'],'page':l['page'],'rect':l['rect'],'heading':l['text'],'key':None,'isKey':False})
    if name=='2. Correction ED 2025-2026.pdf':
        l=next(l for l in ll if l['text']=='40 B.')
        keys.append({'num':'40','index':l['index'],'page':l['page'],'rect':l['rect'],'heading':'B.','key':'B','isKey':True})
    starts.sort(key=lambda c:c['index']);keys.sort(key=lambda c:c['index'])
    return keys if keyonly else starts

def dump_candidates():
    summary=[]
    for bank,b in BANKS.items():
        for role,field in [('subject','sourceSubject'),('correction','sourceCorrection')]:
            name=b['questions'][0][field]
            st=candidates(name,role=='correction' and '.ed.20' in bank)
            summary.append({'bank':bank,'role':role,'name':name,'expected':len(b['questions']),'found':len(st),'nums':[c['num'] for c in st], 'starts':st})
    (OUT/'candidates.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    for s in summary:
        nums=[norm(str(q.get('sourceNumber',q['id']))) for q in BANKS[s['bank']]['questions']]
        status='OK' if nums==s['nums'] else 'DIFF'
        print(status,s['bank'],s['role'],s['expected'],s['found'])
        if status=='DIFF':
            for op,a,b,c,d in difflib.SequenceMatcher(a=nums,b=s['nums'],autojunk=False).get_opcodes():
                if op!='equal':print(' ',op,a,b,nums[a:b],c,d,s['nums'][c:d])
    (OUT/'source_lines.json').write_text(json.dumps(LINES,ensure_ascii=False))

def start_blocks(bank,role):
    b=BANKS[bank];name=b['questions'][0]['sourceSubject' if role=='subject' else 'sourceCorrection']
    ll=load(name);onlykey=role=='correction' and '.ed.20' in bank
    starts=candidates(name,onlykey)
    if bank=='ue2.ed.annales':
        index,pn,bbox=(23,1,[36.96,499.4356,503.4725,707.2697]) if role=='subject' else (29,2,[36.96,46.7955,503.4725,254.6297])
        starts.insert(1,{'num':'24','index':index,'page':pn,'rect':bbox,'heading':b['questions'][1]['question'],'isKey':False,'imageOnly':True})
    assert len(starts)==len(b['questions']),(bank,role,len(starts),len(b['questions']))
    result=[]
    for k,s in enumerate(starts):
        stop=starts[k+1]['index'] if k+1<len(starts) else len(ll)
        block=deepcopy(ll[s['index']:stop])
        cut=None
        if not onlykey:
            for j,l in enumerate(block[1:],1):
                if YEAR_RE.match(l['text']) or l['text'] in ['RAS','Hors programme'] or SECTION_RE.match(l['text']) or re.match(r'^(?:Questions?\s+(?:bonus|complémentaires)|Exercices?\s+complémentaires)',l['text'],re.I):
                    cut=j;break
        if cut is not None:block=block[:cut]
        result.append({'source':name,'start':s,'next':starts[k+1] if k+1<len(starts) else None,'lines':block,'onlykey':onlykey})
    return result

def parse_options(block):
    opts=[];stem=[];active=None
    for l in block['lines']:
        if l['index']==block['start']['index']:
            stem.append(block['start']['heading']);continue
        m=OPT_RE.match(l['text'])
        if m:
            letter,tail=m.groups()
            opts.append({'id':letter,'text':tail,'lines':[l]});active=opts[-1]
        elif active:
            active['text']+=' '+l['text'];active['lines'].append(l)
        else:stem.append(l['text'])
    for o in opts:o['text']=norm(o['text'])
    return {'stem':norm(' '.join(stem)),'options':opts}

def examine():
    entries=[];flags=[];details=[]
    for bank,b in BANKS.items():
        ss=start_blocks(bank,'subject');cc=start_blocks(bank,'correction')
        for n,q in enumerate(b['questions']):
            sb,cb=ss[n],cc[n]
            s=parse_options(sb)
            rawkeys=[k for k in candidates(cb['source'],True) if cb['start']['index']<=k['index']<(cb['next']['index'] if cb['next'] else len(load(cb['source'])))]
            if cb['onlykey']:rawkeys=[cb['start']]
            csplit=deepcopy(cb)
            if rawkeys and not cb['onlykey']:
                csplit['lines']=[l for l in cb['lines'] if l['index']<rawkeys[0]['index']]
            c=parse_options(csplit)
            if 'sans numéro'==str(q.get('sourceNumber')):
                sl=next(l for l in cb['lines'] if re.fullmatch(r'AC',l['text']))
                rawkeys=[{'index':sl['index'],'key':'AC','heading':'AC','page':sl['page'],'num':'sans numéro'}]
                csplit['lines']=[l for l in cb['lines'] if l['index']<sl['index']];c=parse_options(csplit)
            e={'bank':bank,'id':q['id'],'sourceNumber':q.get('sourceNumber'),'subject':{'file':sb['source'],'page':sb['start']['page'],'num':sb['start']['num'],'stem':s['stem']},'correction':{'file':cb['source'],'page':cb['start']['page'],'num':cb['start']['num'],'keys':rawkeys},'items':[],'flags':[]}
            if norm(str(q.get('sourceNumber'))) != cb['start']['num']:e['flags'].append('source_number_differs')
            if not sb['start'].get('imageOnly'):
                if [x['id'] for x in s['options']]!=[x['id'] for x in q['options']]:e['flags'].append('subject_option_labels')
                if cmp(s['stem'])!=cmp(q['question']):e['flags'].append('stem_text')
            cby={o['id']:o for o in c['options']}
            sby={o['id']:o for o in s['options']}
            source_answer=''
            for o in q['options']:
                so=sby.get(o['id']);co=cby.get(o['id'])
                txt=so['text'] if so else None
                item={'id':o['id'],'siteText':o.get('text',''),'subjectText':txt,'subjectLines':so['lines'] if so else [],'correctionText':co['text'] if co else None,'sourceMarker':None,'sourceDetail':None,'flags':[]}
                if txt is None and not sb['start'].get('imageOnly'):item['flags'].append('subject_option_missing')
                elif txt is not None and cmp(txt)!=cmp(o.get('sourceText',o.get('text',''))):item['flags'].append('subject_text')
                if 'autotest' in bank and co:
                    marks=list(re.finditer(r'\b(Vrai|Faux|VRAI|FAUX)\b',co['text']))
                    if not marks:
                        marks=list(re.finditer(r'(?<![\w-])([VF])(?=\s|[.,;:]|$)',co['text']))
                    if marks:
                        # Verdict follows the original item. No key is inferred from scientific knowledge.
                        m=marks[0];raw=m.group();item['sourceMarker']=raw
                        item['sourceDetail']=co['text'][m.end():].lstrip(' ,:;.')
                        item['correctedStatement']=co['text'][:m.start()].rstrip(' ,:;')
                        item['sourceVerdict']=raw.lower() in ('vrai','v')
                        if item['sourceVerdict']:source_answer+=o['id']
                        if txt is not None and cmp(item['correctedStatement'])!=cmp(txt):item['flags'].append('subject_correction_statement_diff')
                        if cmp(q.get('explanations',{}).get(o['id'],''))!=cmp(item['sourceDetail']):item['flags'].append('detail_text')
                    else:item['flags'].append('marker_missing')
                elif 'autotest' in bank:item['flags'].append('corrected_option_missing')
                e['items'].append(item)
            if 'autotest' not in bank:
                if len(rawkeys)==1:
                    source_answer=rawkeys[0]['key']
                    e['correction']['keyLiteral']=rawkeys[0]['heading']
                    for it in e['items']:it['sourceVerdict']=it['id'] in source_answer if source_answer is not None else None
                else:e['flags'].append('key_count')
            e['sourceAnswer']=source_answer
            e['siteAnswer']=q.get('answer')
            if source_answer!=q.get('answer'):e['flags'].append('answer_diff')
            e['itemCount']=len(q['options'])
            entries.append(e)
            if e['flags'] or any(i['flags'] for i in e['items']):flags.append(e)
        print(bank,len(b['questions']),'questions examined')
    (OUT/'audit_raw.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
    (OUT/'flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
    counts={}
    for e in entries:
        for f in e['flags']:counts[f]=counts.get(f,0)+1
        for i in e['items']:
            for f in i['flags']:counts[f]=counts.get(f,0)+1
    print('FLAGS',counts)

if __name__=='__main__':
    dump_candidates()
    examine()
