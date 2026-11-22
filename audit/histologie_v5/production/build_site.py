"""Apply the systematic histology audit to the unchanged V4 full-site baseline."""
from pathlib import Path
import copy, hashlib, json, re, shutil
import fitz
from render_sources import PAIRS

ROOT=Path(__file__).resolve().parent
SITE=ROOT.parents[1]/'output/site'
BASE=ROOT/'baseline_site'
GROUPS=['te_tech','tc','tn']

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if not (ROOT/'baseline_installed.json').exists():
        if SITE.exists():
            backup=ROOT/'preexisting_site_backup'
            assert not backup.exists(), 'Do not overwrite the previous local site'
            shutil.move(SITE,backup)
        shutil.copytree(BASE,SITE)
        write_json(ROOT/'baseline_installed.json',{'baseline':str(BASE),'site':str(SITE)})
    original=(BASE/'index.html').read_text()
    before=json.loads((ROOT/'baseline_exams.json').read_text())
    after=copy.deepcopy(before)
    reviewed={};crops={};audits=[]
    for group in GROUPS:
        reviewed.update(json.loads((ROOT/group/'reviewed.json').read_text())['banks'])
        for row in json.loads((ROOT/group/'crops.json').read_text()):
            key=(row['bank'],row['id']);assert key not in crops;crops[key]=row
        audits+=json.loads((ROOT/group/'audit.json').read_text())
    assert len(reviewed)==9 and sum(len(e['questions']) for e in reviewed.values())==128
    source_dir=SITE/'sources/histo_v5';source_dir.mkdir(parents=True,exist_ok=True)
    static_dir=SITE/'static/histo_v5';static_dir.mkdir(parents=True,exist_ok=True)
    old_map={x['new']:x['old'] for x in json.loads((ROOT/'quality/old_new_comparison.json').read_text())}
    documents={};source_manifest=[]
    for bank in reviewed:
        code=bank.split('.')[1]
        for role_i,role in enumerate(['subject','correction']):
            if code=='autotech':
                file=ROOT/'old_source'/('Autotest.pdf' if role=='subject' else 'autotest correction.pdf')
                pdf=file;old=file
            else:
                file=ROOT/'source'/PAIRS[code][role_i]
                pdf=next((ROOT/'render'/f'{code}_{role}').glob('*.pdf'))
                old=ROOT/'old_source'/old_map[file.name]
            original_rel=f'sources/histo_v5/{code}_{role}{file.suffix}'
            pdf_rel=f'sources/histo_v5/{code}_{role}.pdf'
            shutil.copy2(file,SITE/original_rel)
            if pdf.resolve()!=file.resolve():shutil.copy2(pdf,SITE/pdf_rel)
            old_rel=original_rel
            if code!='autotech':
                old_rel=f'sources/histo_v5/{code}_{role}_premier_envoi.docx'
                shutil.copy2(old,SITE/old_rel)
            meta={'file':file.name,'pdf':pdf_rel,'original':original_rel,'converted':file.suffix=='.docx'}
            documents[(bank,role)]=meta
            source_manifest.append({'bank':bank,'role':role,**meta,'sha256':sha(file),'pdfSha256':sha(pdf),'firstFile':old.name,'firstOriginal':old_rel,'firstSha256':sha(old),'originalsIdentical':sha(file)==sha(old)})
    opened={};capture_manifest=[];changes=[]
    for bank,exam in reviewed.items():
        after[bank]['questions']=copy.deepcopy(exam['questions'])
        old_questions={q['id']:q for q in before[bank]['questions']}
        for q in after[bank]['questions']:
            parts=crops[(bank,q['id'])]
            q['sourceCopies']={}
            q['sourceQuestionNumber']=q.get('sourceQuestionNumber') or parts.get('sourceNumber') or q['id']
            for role in ['subject','correction']:
                metadata=copy.deepcopy(documents[(bank,role)])
                metadata['captures']=[]
                for i,part in enumerate(parts[role],1):
                    file=str(Path(part['file']).resolve())
                    if file not in opened:opened[file]=fitz.open(file)
                    doc=opened[file];page=doc[part['page']-1];rect=fitz.Rect(part['rect'])
                    assert rect.width>0 and rect.height>0 and page.rect.contains(rect),part
                    assert Path(file).name==Path(metadata['file']).with_suffix('.pdf').name
                    src=f'static/histo_v5/{bank.replace(".","_")}_q{q["id"]}_{role}_{i}.png'
                    pix=page.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False)
                    pix.save(SITE/src)
                    metadata['captures'].append({'src':src,'page':part['page']})
                    capture_manifest.append({'bank':bank,'id':q['id'],'role':role,'src':src,'source':metadata['pdf'],'page':part['page'],'rect':part['rect'],'width':pix.width,'height':pix.height,'sha256':sha(SITE/src)})
                if bank=='histo.te2' and q['id']==17 and role=='correction':
                    metadata['note']='Les items A–E du sujet correspondent, dans le même ordre, aux lettres F–J du corrigé : A↔F, B↔G, C↔H, D↔I, E↔J.'
                q['sourceCopies'][role]=metadata
            q['sourceSubject']=q['sourceCopies']['subject']['file']
            q['sourceCorrection']=q['sourceCopies']['correction']['file']
            q['subjectPage']=q['sourceCopies']['subject']['captures'][0]['page']
            q['sourceEndPage']=q['sourceCopies']['subject']['captures'][-1]['page']
            q['correctionPage']=q['sourceCopies']['correction']['captures'][0]['page']
            q['correctionEndPage']=q['sourceCopies']['correction']['captures'][-1]['page']
            q['approximateDocxPage']=q['sourceCopies']['subject']['converted']
            for note in q.get('reviewNotes',[]):
                for ref in note.get('refs',[]):
                    if ref.get('href'):continue
                    for role in ['subject','correction']:
                        source=q['sourceCopies'][role]
                        if ref.get('file')==source['file']:
                            ref['href']=source['pdf']+'#page='+str(ref.get('page') or source['captures'][0]['page'])
                if not note.get('refs') and note.get('kind')=='source_conflict':
                    note['refs']=[{'file':q['sourceCopies'][role]['file'],'page':q['sourceCopies'][role]['captures'][0]['page'],'label':label,'href':q['sourceCopies'][role]['pdf']+'#page='+str(q['sourceCopies'][role]['captures'][0]['page'])} for role,label in [('subject','Sujet original'),('correction','Corrigé original')]]
            old=old_questions.get(q['id'])
            field_changes={k:{'before':old.get(k) if old else None,'after':q.get(k)} for k in set(old or {})|set(q) if (old or {}).get(k)!=q.get(k)}
            changes.append({'bank':bank,'id':q['id'],'sourceNumber':q['sourceQuestionNumber'],'newQuestion':old is None,'fields':field_changes})
    for doc in opened.values():doc.close()
    assert len(capture_manifest)==283,len(capture_manifest)
    for bank in before:
        if bank not in reviewed:assert before[bank]==after[bank]
        else:
            assert {q['id'] for q in before[bank]['questions']}<={q['id'] for q in after[bank]['questions']}
    start=original.index('const EXAMS=')+len('const EXAMS=')
    _,length=json.JSONDecoder().raw_decode(original[start:])
    html=original[:start]+json.dumps(after,ensure_ascii=False,separators=(',',':'))+original[start+length:]
    def replace_once(old,new):
        nonlocal html
        assert html.count(old)==1,(old,html.count(old))
        html=html.replace(old,new,1)
    replace_once('</style>',(ROOT/'source_copies.css').read_text()+'\n</style>')
    replace_once('function renderQuestionCard(q){',(ROOT/'source_copies.js').read_text()+'\nfunction renderQuestionCard(q){')
    replace_once("if(done)details=details.replace(/<\\/div><\\/details>$/,reviewHtml(q)+'</div></details>');","if(done)details=details.replace(/<\\/div><\\/details>$/,reviewHtml(q)+histoSourceCopy(q,'correction')+'</div></details>');")
    replace_once('${q.originalImages?.length?','${!q.sourceCopies&&q.originalImages?.length?')
    replace_once('${q.correctionImage?','${!q.sourceCopies&&q.correctionImage?')
    replace_once('<div class="opt-list">${opt}</div><div class="qfoot">','<div class="opt-list">${opt}</div>${histoSourceCopy(q,\'subject\')}<div class="qfoot">')
    (SITE/'index.html').write_text(html)
    write_json(ROOT/'current_exams.json',after)
    audit_dir=SITE/'audit/histologie_v5';audit_dir.mkdir(parents=True,exist_ok=True)
    for filename,value in [('documents_sources.json',source_manifest),('captures.json',capture_manifest),('comparaison_items.json',audits),('modifications.json',changes)]:write_json(audit_dir/filename,value)
    summary={'banksReviewed':len(reviewed),'questionsReviewed':128,'itemsReviewed':sum(len(q['options']) for e in reviewed.values() for q in e['questions']),'newQuestions':sum(c['newQuestion'] for c in changes),'sourcePanels':len(capture_manifest),'sourceMenus':256,'allSiteQuestionsBefore':sum(len(e['questions']) for e in before.values()),'allSiteQuestionsAfter':sum(len(e['questions']) for e in after.values()),'unchangedBanks':len(before)-len(reviewed),'banks':[{'bank':bank,'label':after[bank]['label'],'questions':len(e['questions']),'items':sum(len(q['options']) for q in e['questions'])} for bank,e in reviewed.items()]}
    write_json(audit_dir/'statistiques.json',summary)
    write_json(ROOT/'build_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
