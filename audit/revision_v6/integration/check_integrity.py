"""Verify the final archive's local evidence links and original-file integrity."""
from pathlib import Path
import hashlib, json, re
from urllib.parse import unquote
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parent
SITE=ROOT.parent.parent/'output/site'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

if __name__=='__main__':
    report={'result':'FAIL','errors':[],'baselineFilesChecked':0,'localLinksChecked':0,'capturesDecoded':0,'pixelSamples':[],'extraAssetsChecked':0}
    try:
        data=read(ROOT/'current_exams.json');baseline=read(ROOT/'baseline_exams.json')
        assert set(data)==set(baseline),'Bank identities changed'
        for bank,exam in data.items():
            assert {k:v for k,v in exam.items() if k!='questions'}=={k:v for k,v in baseline[bank].items() if k!='questions'},bank
            old={q['id']:q for q in baseline[bank]['questions']};new={q['id']:q for q in exam['questions']}
            assert len(new)==len(exam['questions']) and set(old)<=set(new),bank
            for n,q in old.items():assert q.get('weight',1)==new[n].get('weight',1),(bank,n,'weight')
            for q in exam['questions']:
                for key in ('title','stem','question','text','prompt'):
                    value=q.get(key)
                    if isinstance(value,str):assert not re.search(r'\.(?:pdf|docx)\b',value,re.I),(bank,q['id'],'filename used in question',key)
        report['questionFilenameTitles']=0
        for old in read(ROOT/'baseline_files.json'):
            if old['file']=='index.html':continue
            path=SITE/old['file'];assert path.is_file() and sha(path)==old['sha256'],old['file']
            report['baselineFilesChecked']+=1
        paths=set()
        def walk(value):
            if isinstance(value,dict):
                for child in value.values():walk(child)
            elif isinstance(value,list):
                for child in value:walk(child)
            elif isinstance(value,str) and value.startswith(('sources/','static/','assets/')):
                paths.add(unquote(value.split('#',1)[0].split('?',1)[0]))
        walk(data)
        for rel in paths:
            path=(SITE/rel).resolve();assert path.is_relative_to(SITE) and path.is_file(),rel
        report['localLinksChecked']=len(paths)
        manifest=read(SITE/'audit/revision_v6/captures.json')
        captured=sorted(set(row['src'] for row in manifest))
        for rel in captured:
            with Image.open(SITE/rel) as image:
                assert image.width>0 and image.height>0,rel
                image.verify()
        report['capturesDecoded']=len(captured)
        ownership={bank:s for s,r in read(ROOT/'roster.json').items() for bank in r['banks']}
        selected={}
        for row in manifest:
            key=(ownership[row['bank']],row['role']);selected.setdefault(key,row)
        # Additional protected-original samples ensure that annotations survive
        # unchanged in their files even though the interface defers them.
        by_q={(r['bank'],r['id'],r['role']):[] for r in manifest}
        for row in manifest:by_q[row['bank'],row['id'],row['role']].append(row)
        for b,e in data.items():
            for q in e['questions']:
                if q['sourceCopies']['subject'].get('afterCorrection'):
                    rows=by_q.get((b,q['id'],'subject'),[])
                    if rows:selected.setdefault((b,q['id']),rows[0])
        for row in selected.values():
            with fitz.open(SITE/row['source']) as doc:
                pix=doc[row['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(row['rect']),alpha=False)
                expected=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
            with Image.open(SITE/row['src']) as im:
                actual=im.convert('RGB')
                assert expected.size==actual.size and expected.tobytes()==actual.tobytes(),row
            report['pixelSamples'].append({k:row[k] for k in ['bank','id','role','source','page','src']})
        for asset in read(SITE/'audit/revision_v6/assets_complementaires.json'):
            assert sha(SITE/asset['src'])==asset['sha256'],asset['src'];report['extraAssetsChecked']+=1
        report['result']='PASS'
    except Exception as exc:
        import traceback
        report['errors'].append(traceback.format_exc())
    (ROOT/'integrity_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({**report,'pixelSamples':len(report['pixelSamples'])},ensure_ascii=False,indent=2))
    if report['result']!='PASS':raise SystemExit(1)
