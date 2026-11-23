from pathlib import Path
import fitz, json, hashlib, re, unicodedata, difflib

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'prepare'
WS=ROOT.parents[3]
DOC=WS/'output/site/sources/Annales_compilation.pdf'

def write(name,data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
def compact(s):return re.sub(r'\s+',' ',s).strip()
def norm(s):
    return re.sub(r'[^a-z0-9+<>≠=−-]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())

if __name__=='__main__':
    banks=json.loads((PREP/'reviewed.json').read_text())['banks']
    crops={(x['bank'],x['id']):x for x in json.loads((PREP/'crops.json').read_text())}
    assets=json.loads((PREP/'asset_audit.json').read_text())
    doc=fitz.open(DOC)
    (ROOT/'readings').mkdir(exist_ok=True)
    page_text={str(n):doc[n-1].get_text('text',sort=True) for n in range(487,699)}
    write('pages_direct.json',page_text)
    rows=[]
    for bank,exam in banks.items():
        readout=[]
        for q in exam['questions']:
            row={'bank':bank,'id':q['id'],'sourceNumber':q['sourceNumber'],'siteKey':q['answer'],'roles':{}}
            readout.append(f"\n## {bank} Q{q['id']} / clé site {q['answer'] or 'HORS NOTE'}\n")
            for role in ('subject','correction'):
                parts=[]
                for c in crops[bank,q['id']][role]:
                    p=doc[c['page']-1];r=fitz.Rect(c['rect'])
                    assert p.rect.contains(r)
                    parts.append({'page':c['page'],'rect':c['rect'],'text':p.get_text('text',clip=r,sort=True)})
                row['roles'][role]=parts
                text=' '.join(compact(x['text']) for x in parts)
                if role=='correction':
                    # Keep every correction word; omit only an exact duplicated
                    # subject prefix where the document prints it a second time.
                    pat=re.search(r'(?<!\w)(?:[ABCDE]{1,5}\s+)?A[.)]?\s*(?:VRAI|FAUX|Vrai|Faux)\b',text)
                    if pat:text=text[pat.start():]
                readout.append(role.upper()+': '+text+'\n')
            row['explanations']=q.get('explanations',{})
            row['notes']=q.get('reviewNotes',[])
            rows.append(row)
        (ROOT/'readings'/f'{bank}.txt').write_text('\n'.join(readout))
    write('direct_question_sources.json',rows)
    write('input_signatures.json',{'reviewed':hashlib.sha256((PREP/'reviewed.json').read_bytes()).hexdigest(),'crops':hashlib.sha256((PREP/'crops.json').read_bytes()).hexdigest(),'source':hashlib.sha256(DOC.read_bytes()).hexdigest()})
    print({'questions':len(rows),'items':sum(len(q['options']) for e in banks.values() for q in e['questions']),'pages':len(page_text),'source':str(DOC)})
