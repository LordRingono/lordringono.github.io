"""Assemble only reviewed V6 subject patches and authentic original-source captures.

The V5 index and source assets remain the immutable input. Run after all binômes
have delivered; the final release replaces only the intended files in output/site.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import copy, hashlib, json, re, shutil, unicodedata
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
SITE=WORKSPACE/'output/site'
SUBJECTS=['ssh','histologie','biocell','embryologie','biomol','biochimie','chimie','biostat','pharmaco']

def read(path):return json.loads(Path(path).read_text())
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def slug(value):
    return re.sub('[^a-zA-Z0-9]+','_',unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode()).strip('_')[:90]
def absolute(path):
    p=Path(path)
    return p.resolve() if p.is_absolute() else (WORKSPACE/p).resolve()

def render_capture(task):
    target=Path(task.get('target') or SITE/task['src'])
    if target.exists():return
    target.parent.mkdir(parents=True,exist_ok=True)
    with fitz.open(task['file']) as doc:
        assert 1<=task['page']<=len(doc),task
        page=doc[task['page']-1];rect=fitz.Rect(task['rect'])
        assert rect.width>0 and rect.height>0 and (page.rect+(-.1,-.1,.1,.1)).contains(rect),task
        pix=page.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False)
        image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        image.save(target,'WEBP',lossless=True,method=1)

def main():
    before=read(ROOT/'baseline_exams.json');after=copy.deepcopy(before)
    html=(ROOT/'baseline_index.html').read_text()
    groups={};crop_rows={};ownership={};extra_assets_by_src={}
    signoffs=read(ROOT/'signoffs.json')
    assert set(signoffs)==set(SUBJECTS),'All subject pairs must give final approval before integration'
    source_mapping={};preferred_destinations={}
    render_manifest=ROOT/'render/biocell_manifest.json'
    if render_manifest.exists():
        for row in read(render_manifest):source_mapping[str(absolute(row['pdf']))]=row
    for subject in SUBJECTS:
        directory=ROOT/subject
        assert (directory/'verify/REPORT.md').exists(),f'Independent verifier missing: {subject}'
        approved_reviewed=directory/'verify/approved_reviewed.json'
        approved_crops=directory/'verify/approved_crops.json'
        reviewed_path=approved_reviewed if approved_reviewed.exists() else directory/'prepare/reviewed.json'
        crops_path=approved_crops if approved_crops.exists() else directory/'prepare/crops.json'
        for kind,path in [('reviewed',reviewed_path),('crops',crops_path)]:
            assert (ROOT/signoffs[subject][kind]).resolve()==path.resolve(),(subject,kind,'Unapproved input')
            assert sha(path)==signoffs[subject][kind+'_sha256'],(subject,kind,'Input changed after approval')
        data=read(reviewed_path)
        groups[subject]=data['banks']
        for bank,exam in data['banks'].items():
            assert bank in before and bank not in ownership,(subject,bank)
            ownership[bank]=subject
            prior_ids={q['id'] for q in before[bank]['questions']}
            new_ids=[q['id'] for q in exam['questions']]
            assert len(new_ids)==len(set(new_ids)) and prior_ids<=set(new_ids),(bank,'IDs lost/duplicated')
            after[bank]['questions']=copy.deepcopy(exam['questions'])
        for row in read(crops_path):
            key=(row['bank'],row['id']);assert key not in crop_rows,key
            crop_rows[key]=row
        for role in ('prepare','verify'):
            manifest=directory/role/'asset_manifest.json'
            if manifest.exists():
                rows=read(manifest)
                if isinstance(rows,dict):rows=rows.get('assets',[])
                for asset in rows:
                    file=absolute(asset['file']);src=asset['src']
                    assert src.startswith(('static/','sources/','assets/')) and (SITE/src).resolve().is_relative_to(SITE),src
                    assert file.is_file(),file
                    prior=extra_assets_by_src.get(src)
                    assert not prior or prior['subject']==subject,(src,'Conflicting subject assets')
                    extra_assets_by_src[src]={'subject':subject,'file':str(file),'src':src,'sha256':sha(file),'role':role}
        for role in ('prepare','verify'):
            manifest=directory/role/'sourceManifest.json'
            if not manifest.exists():manifest=directory/role/'source_manifest.json'
            if manifest.exists():
                rows=read(manifest)
                if isinstance(rows,dict):rows=rows.get('documents',rows.get('sources',list(rows.values())))
                for row in rows:
                    if not isinstance(row,dict):continue
                    if row.get('pdf'):source_mapping[str(absolute(row['pdf']))]=row
                    original_path=row.get('absolute') or row.get('pdf') or row.get('file')
                    if row.get('packaged') and original_path and absolute(original_path).exists():
                        preferred_destinations[str(absolute(original_path))]=row['packaged']
    assert set(ownership)==set(before),{'unreviewedBanks':sorted(set(before)-set(ownership))}
    baseline_files={row['file']:row for row in read(ROOT/'baseline_files.json')}
    extra_assets=list(extra_assets_by_src.values())
    for asset in extra_assets:
        src=asset['src'];target=SITE/src;target.parent.mkdir(parents=True,exist_ok=True)
        if src in baseline_files:assert baseline_files[src]['sha256']==asset['sha256'],(src,'Immutable original asset')
        if not target.exists() or sha(target)!=asset['sha256']:shutil.copy2(asset['file'],target)
    sources=SITE/'sources/revision_v6';sources.mkdir(parents=True,exist_ok=True)
    assets=SITE/'static/revision_v6';assets.mkdir(parents=True,exist_ok=True)
    document_cache={};document_manifest=[];capture_tasks={};capture_manifest=[];changes=[]
    existing_sources={row['sha256']:row['file'] for row in read(ROOT/'baseline_files.json') if row['file'].startswith('sources/')}

    def install_document(file):
        file=absolute(file);key=str(file)
        if key in document_cache:return document_cache[key]
        assert file.is_file(),file
        digest=sha(file)
        if key in preferred_destinations:
            relative=preferred_destinations[key]
            assert relative.startswith('sources/') and (SITE/relative).resolve().is_relative_to(SITE),relative
            (SITE/relative).parent.mkdir(parents=True,exist_ok=True)
            if (SITE/relative).exists():assert sha(SITE/relative)==digest,relative
            else:shutil.copy2(file,SITE/relative)
        elif file.is_relative_to(SITE):relative=file.relative_to(SITE).as_posix()
        elif digest in existing_sources:relative=existing_sources[digest]
        else:
            relative='sources/revision_v6/'+slug(file.stem)+'_'+digest[:12]+file.suffix.lower()
            if not (SITE/relative).exists():shutil.copy2(file,SITE/relative)
        document_cache[key]={'path':relative,'sha256':digest,'file':file.name}
        document_manifest.append({'input':key,**document_cache[key]})
        return document_cache[key]

    for bank,exam in after.items():
        prior={q['id']:q for q in before[bank]['questions']}
        for q in exam['questions']:
            key=(bank,q['id']);row=crop_rows.get(key)
            assert row is not None,(bank,q['id'],'No source-copy audit')
            if row.get('reuseExisting'):
                assert q.get('sourceCopies',{}).get('subject') and q.get('sourceCopies',{}).get('correction'),key
            else:
                q['sourceCopies']={}
                q['sourceQuestionNumber']=row.get('sourceNumber') or q.get('sourceQuestionNumber') or q.get('printedSourceNumber') or q.get('sourceNumber') or q['id']
                for role in ['subject','correction']:
                    parts=row.get(role,[])
                    if not parts:
                        reason=row.get(role+'Missing')
                        assert reason,(bank,q['id'],role,'Unexplained missing source')
                        q['sourceCopies'][role]={'missing':True,'reason':str(reason),'captures':[]}
                        continue
                    field='sourceSubject' if role=='subject' else 'sourceCorrection'
                    documents={};meta={'captures':[]}
                    note=row.get(role+'Note')
                    if note:meta['note']=note
                    if row.get(role+'AfterCorrection'):meta['afterCorrection']=True
                    if row.get(role+'Mismatch'):meta['mismatch']=True
                    if row.get(role+'Number'):meta['questionNumber']=row[role+'Number']
                    for number,part in enumerate(parts,1):
                        pdf_file=absolute(part['file']);pdf_key=str(pdf_file)
                        pdf=install_document(pdf_file)
                        if pdf_key not in documents:
                            original_mapping=source_mapping.get(pdf_key,{})
                            original_file=absolute(original_mapping.get('original') or pdf_file)
                            original=install_document(original_file)
                            fallback=q.get(field) if number==1 and re.search(r'_[0-9a-f]{10,12}$',original_file.stem) else original_file.name
                            display=part.get('fileLabel') or part.get('sourceFile') or (row.get(role+'File') if number==1 else None) or fallback or original_file.name
                            source_label=display
                            if original_file.name=='Annales_compilation.pdf' or not re.search(r'\.(pdf|docx)$',str(display),re.I):display=original_file.name
                            documents[pdf_key]={'file':display,'pdf':pdf['path'],'original':original['path'],'converted':original_file.suffix.lower()=='.docx','pages':[],'firstPage':int(part['page'])}
                            if source_label!=display:documents[pdf_key]['sourceLabel']=source_label
                        document=documents[pdf_key]
                        page=int(part['page']);rect=[round(float(v),4) for v in part['rect']]
                        if page not in document['pages']:document['pages'].append(page)
                        identity=json.dumps([pdf['sha256'],page,rect],separators=(',',':'))
                        capid=hashlib.sha256(identity.encode()).hexdigest()[:24]
                        src=f'static/revision_v6/{capid}.webp'
                        capture_tasks.setdefault(capid,{'file':str(pdf_file),'page':page,'rect':rect,'src':src})
                        capture={'src':src,'page':page,'pdf':document['pdf'],'file':document['file']}
                        if part.get('sourceNumber'):capture['questionNumber']=part['sourceNumber']
                        meta['captures'].append(capture)
                        capture_manifest.append({'bank':bank,'id':q['id'],'role':role,'part':number,'source':pdf['path'],'src':src,'page':page,'rect':rect})
                    primary=next(iter(documents.values()))
                    for document in documents.values():document['pages'].sort()
                    meta.update({k:v for k,v in primary.items() if k!='pages'})
                    if len(documents)>1:meta['documents']=list(documents.values())
                    q['sourceCopies'][role]=meta
                    q[field]=meta['file']
                    if role=='subject':
                        q['subjectPage']=primary['firstPage'];q['sourceStartPage']=primary['pages'][0];q['sourceEndPage']=primary['pages'][-1]
                        q['approximateDocxPage']=meta['converted']
                        if q.get('fromCompilation') or q.get('contextRevised'):q['sourcePdf']=meta['pdf']
                    else:
                        q['correctionPage']=primary['firstPage'];q['correctionEndPage']=primary['pages'][-1]
                        if q.get('fromCompilation') or q.get('contextRevised'):q['correctionPdf']=meta['pdf']
            # Keep note snapshots synchronized with the actual revised option text.
            for note in q.get('reviewNotes',[]):
                if 'reviewedItemText' in note:
                    note['reviewedItemText']={o['id']:o['text'] for o in q['options'] if o['id'] in note.get('items',[])}
                if 'reviewedExplanation' in note:
                    note['reviewedExplanation']={letter:q.get('explanations',{}).get(letter,'') for letter in note.get('items',[])}
                for ref in note.get('refs',[]):
                    if ref.get('href') or ref.get('url'):continue
                    for role in ['subject','correction']:
                        source=q.get('sourceCopies',{}).get(role,{})
                        for document in source.get('documents') or [source]:
                            if ref.get('file') and ref.get('file') in [document.get('file'),document.get('sourceLabel')] and document.get('pdf'):
                                ref['href']=document['pdf']+'#page='+str(ref.get('page') or (document.get('pages') or [source['captures'][0]['page']])[0])
            old=prior.get(q['id'])
            fields={f:{'before':(old or {}).get(f),'after':q.get(f)} for f in set(old or {})|set(q) if (old or {}).get(f)!=q.get(f)}
            if fields:changes.append({'bank':bank,'id':q['id'],'newQuestion':old is None,'fields':fields})

    render_tasks=[]
    for capid,task in capture_tasks.items():
        cached=ROOT/'capture_cache'/f'{capid}.webp'
        if cached.exists():shutil.copy2(cached,SITE/task['src'])
        else:render_tasks.append(task)
    with ProcessPoolExecutor(max_workers=3) as pool:list(pool.map(render_capture,render_tasks))
    start=html.index('const EXAMS=')+len('const EXAMS=')
    _,length=json.JSONDecoder().raw_decode(html[start:])
    html=html[:start]+json.dumps(after,ensure_ascii=False,separators=(',',':'))+html[start+length:]
    a=html.index('// Original histology documents:')
    b=html.index('function renderQuestionCard(q){',a)
    html=html[:a]+(ROOT/'source_copies.js').read_text()+'\n'+html[b:]
    html=html.replace('${!q.sourceCopies&&q.originalImages?.length?','${!q.sourceCopies?.subject&&q.originalImages?.length?')
    html=html.replace('${!q.sourceCopies&&q.correctionImage?','${!q.sourceCopies?.correction&&q.correctionImage?')
    html=html.replace('if(done&&revisedSource(q)){','if(done&&revisedSource(q)&&!q.sourceCopies?.correction?.captures?.length){')
    html=html.replace('${q.images?.length?`<div class="q-image-panel">','${q.imagesAfterCorrection&&q.images?.length&&!subjectOriginalReady(q)?`<p class="histo-source-note source-figure-deferred">Le schéma fourni est annoté ; il est accessible après validation des QCM concernés.</p>`:\'\'}${q.images?.length&&(!q.imagesAfterCorrection||subjectOriginalReady(q))?`<div class="q-image-panel">')
    html=html.replace('alt="Figure du sujet non corrigé — question ${q.id}', 'alt="${q.imagesAfterCorrection?\'Figure annotée du document fourni\':\'Figure du sujet non corrigé\'} — question ${q.id}')
    html=html.replace("${annalesImages(q.stemImages,q.stemCaption||'Extrait du sujet non corrigé')}", "${q.imagesAfterCorrection&&q.stemImages?.length&&!subjectOriginalReady(q)?'<p class=\"histo-source-note source-figure-deferred\">Le schéma fourni est annoté ; il est accessible après validation des QCM concernés.</p>':annalesImages(q.stemImages,q.imagesAfterCorrection?'Extrait du document fourni (annoté)':q.stemCaption||'Extrait du sujet non corrigé')}")
    html=html.replace('function sharedStatement(context,q,anchor){\n const label=contextQuestionLabel(context);','function sharedStatement(context,q,anchor){\n const label=contextQuestionLabel(context),ready=sharedOriginalReady(context);')
    html=html.replace("${annalesImages(context.images,'Énoncé commun · '+label)}", "${!ready?'<p class=\"histo-source-note source-figure-deferred\">Le schéma fourni est annoté ; il est accessible après validation des QCM concernés.</p>':annalesImages(context.images,'Énoncé commun · '+label)}")
    html=html.replace('context.sourcePdf||sourcePdfFor(q),context.sourceStartPage', "ready?(context.sourcePdf||sourcePdfFor(q)):'',context.sourceStartPage")
    html=html.replace('revisedSource(q)&&sourcePdfFor(q)?', 'revisedSource(q)&&sourcePdfFor(q)&&subjectOriginalReady(q)?')
    # Restore the meaning of saved choices when a lost item has shifted labels.
    # Repaired and restored questions await validation; other progress remains.
    html=html.replace("const ACTIVE_KEY=", (ROOT/'progress_migration.js').read_text()+'\nconst ACTIVE_KEY=',1)
    html=html.replace('function perQuestionCorrection(){return onlyFilledMode||groupedPharma();}', 'function perQuestionCorrection(){return onlyFilledMode||groupedPharma()||classicPartialCorrection;}')
    html=html.replace('let answers={},submitted=false,correctedIds=new Set(),', 'let classicPartialCorrection=false;\nlet answers={},submitted=false,correctedIds=new Set(),')
    html=html.replace(' answers={};submitted=false;correctedIds=new Set();', ' answers={};submitted=false;correctedIds=new Set();classicPartialCorrection=false;')
    html=html.replace("try{const obj=fallbackSessions[profileKey()]||JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');if(obj&&obj.answers", "try{let obj=fallbackSessions[profileKey()]||JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');obj=migrateV6Progress(obj);if(obj&&obj.answers")
    html=html.replace('   }else submitted=!!obj.submitted;', '   }else{classicPartialCorrection=!!V6_ITEM_REPAIRS[activeExam]&&!!obj.revision6Partial;if(classicPartialCorrection)correctedIds=new Set((obj.correctedIds||[]).map(Number).filter(id=>QUESTIONS.some(q=>q.id===id)));submitted=classicPartialCorrection?correctedIds.size>0:!!obj.submitted;}')
    html=html.replace(' if(onlyFilledMode)snap.correctedIds=[...correctedIds];', ' if(onlyFilledMode||classicPartialCorrection)snap.correctedIds=[...correctedIds];\n if(classicPartialCorrection)snap.revision6Partial=true;\n if(V6_ITEM_REPAIRS[activeExam])snap.itemSchemaVersion=6;')
    html=html.replace(' try{localStorage.setItem(STORAGE_KEY,JSON.stringify(snap));}catch(e){}',' persistV6Progress(snap);')
    html=html.replace("$('#filled-mode-profile').textContent=onlyFilledMode?'Profil 1 · progression sauvegardée':'Profil 2 · progression indépendante';", "$('#filled-mode-profile').textContent=v6PendingBackups.has(STORAGE_KEY)?'Sauvegarde locale indisponible · ancienne progression préservée. Gardez cet onglet ouvert.':onlyFilledMode?'Profil 1 · progression sauvegardée':'Profil 2 · progression indépendante';")
    html=html.replace('if(groupedPharma()&&!onlyFilledMode){renderPharmaClassicToolbar();return;}', 'if(perQuestionCorrection()&&!onlyFilledMode){renderPharmaClassicToolbar();return;}')
    html=html.replace('if(groupedPharma()&&!onlyFilledMode){if(!TOTAL||QUESTIONS.every(isCorrected))return;correctedIds=new Set(QUESTIONS.map(q=>q.id));submitted=true;', 'if(perQuestionCorrection()&&!onlyFilledMode){if(!TOTAL||QUESTIONS.every(isCorrected))return;correctedIds=new Set(QUESTIONS.map(q=>q.id));submitted=true;classicPartialCorrection=false;')
    html=html.replace("function modify(){if(perQuestionCorrection()){correctedIds.clear();}submitted=false;", "function modify(){if(perQuestionCorrection()){correctedIds.clear();}classicPartialCorrection=false;submitted=false;")
    html=html.replace('return;answers={};submitted=false;correctedIds.clear();', 'return;answers={};submitted=false;correctedIds.clear();classicPartialCorrection=false;')
    # One original matching exercise has no A–E options. It stays outside the
    # score, but can now be marked complete to access its source in selective mode.
    html=html.replace('function allowsNoAnswer(q){return Array.isArray(q.options)&&q.options.length>0;}', 'function allowsNoAnswer(q){return Array.isArray(q.options);}')
    html=html.replace("if(!allowsNoAnswer(q))return '';\n const checked=", "if(!allowsNoAnswer(q))return '';\n const noneLabel=q.options.length?'Aucune proposition':'J’ai fait cet exercice (hors note)';\n const checked=")
    html=html.replace('aria-label="QCM ${q.id}, aucune proposition"','aria-label="QCM ${q.id}, ${esc(noneLabel)}"')
    html=html.replace('<span class="opt-letter">∅</span><span class="opt-text">Aucune proposition</span>', '<span class="opt-letter">${q.options.length?\'∅\':\'✓\'}</span><span class="opt-text">${esc(noneLabel)}</span>')
    html=html.replace('>Correction indisponible · hors note</summary>', ">${q.sourceCopies?.correction?.captures?.length?'Corrigé original · hors note':'Correction indisponible · hors note'}</summary>")
    html=html.replace('Clé ou extraction insuffisante pour noter cet énoncé de manière fiable.', "${q.options.length?'Clé ou extraction insuffisante pour noter cet énoncé de manière fiable.':'Cet exercice de mise en correspondance est présenté hors note.'}")
    html=html.replace('Correction non exploitable dans les documents fournis</span>', 'Exclu du calcul de la note</span>')
    (SITE/'index.html').write_text(html)
    write(ROOT/'current_exams.json',after)
    audit_dir=SITE/'audit/revision_v6';audit_dir.mkdir(parents=True,exist_ok=True)
    write(audit_dir/'documents.json',document_manifest)
    write(audit_dir/'captures.json',capture_manifest)
    write(audit_dir/'modifications.json',changes)
    write(audit_dir/'assets_complementaires.json',extra_assets)
    write(audit_dir/'approbations_binomes.json',signoffs)
    for subject in SUBJECTS:
        target=audit_dir/'matieres'/subject
        for role in ('prepare','verify'):
            target_role=target/role;target_role.mkdir(parents=True,exist_ok=True)
            # Keep the actual two passes, their approved data and source proofs.
            # Internal page previews are replaced by the site's final source copies.
            for path in sorted((ROOT/subject/role).rglob('*')):
                if path.is_file() and path.suffix.lower() in ('.json','.md','.py','.js','.cjs','.txt'):
                    destination=target_role/path.relative_to(ROOT/subject/role)
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(path,destination)
    summary={'questionsBefore':sum(len(b['questions']) for b in before.values()),'questionsAfter':sum(len(b['questions']) for b in after.values()),'banks':len(after),'items':sum(len(q['options']) for b in after.values() for q in b['questions']),'newCaptureFiles':len(capture_tasks),'captureReferences':len(capture_manifest),'missingSubjectCopies':[],'missingCorrectionCopies':[],'subjects':{}}
    for bank,exam in after.items():
        subject=ownership[bank]
        entry=summary['subjects'].setdefault(subject,{'banks':0,'questions':0,'items':0,'subjectCopies':0,'correctionCopies':0,'cleanSubjectCopies':0,'annotatedSubjectCopies':0,'graded':0,'ungraded':0,'newQuestions':0,'restoredItems':0,'changedItemTexts':0,'restoredKeys':0,'newlyUngraded':0,'changedKeys':0,'changedExplanations':0})
        entry['banks']+=1
        old_questions={q['id']:q for q in before[bank]['questions']}
        for q in exam['questions']:
            entry['questions']+=1;entry['items']+=len(q['options'])
            gradable=bool(q.get('answer')) or q.get('answerIsEmpty') is True
            entry['graded' if gradable else 'ungraded']+=1
            old=old_questions.get(q['id'])
            if old is None:entry['newQuestions']+=1
            else:
                old_options={o['id']:o for o in old['options']}
                for option in q['options']:
                    if option['id'] not in old_options:entry['restoredItems']+=1
                    elif option.get('text')!=old_options[option['id']].get('text'):entry['changedItemTexts']+=1
                old_gradable=bool(old.get('answer')) or old.get('answerIsEmpty') is True
                if gradable and not old_gradable:entry['restoredKeys']+=1
                if old_gradable and not gradable:entry['newlyUngraded']+=1
                if (q.get('answer'),q.get('answerIsEmpty',False))!=(old.get('answer'),old.get('answerIsEmpty',False)):entry['changedKeys']+=1
                for letter in set(q.get('explanations',{}))|set(old.get('explanations',{})):
                    if q.get('explanations',{}).get(letter)!=old.get('explanations',{}).get(letter):entry['changedExplanations']+=1
            subject_copy=q['sourceCopies']['subject']
            if subject_copy.get('captures'):entry['annotatedSubjectCopies' if subject_copy.get('afterCorrection') else 'cleanSubjectCopies']+=1
            for role in ('subject','correction'):
                if q['sourceCopies'][role].get('captures'):entry[role+'Copies']+=1
                else:summary['missing'+role.title()+'Copies'].append({'bank':bank,'id':q['id'],'reason':q['sourceCopies'][role].get('reason')})
    write(audit_dir/'statistiques.json',summary);write(ROOT/'build_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
