"""Add the three new annales units without rewriting the protected banks."""
from pathlib import Path
import json, re, shutil, hashlib

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'baseline/site'
OUT = ROOT / 'output/site'
WORK = ROOT / 'work'
ED_KEY_REPAIRS={6:('', 'C'),7:('A','B'),8:('','BC'),13:('','BD')}


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def replace_ed_banks(original, existing):
    """Replace only the three ED banks now expressly authorized by the user.

    Retain the literal JSON of every other original bank, not just its values.
    """
    path=WORK/'agents/biomol_ed/overrides.json'
    if not path.exists():
        return original
    overrides=json.loads(path.read_text())
    allowed={'ue2.ed.annales','ue2.ed.2025-2026','ue2.ed.2026-2027'}
    assert set(overrides)==allowed, set(overrides)
    for key,exam in overrides.items():
        old=existing[key]
        assert {k:v for k,v in old.items() if k not in ['questions','contextRevised']}=={k:v for k,v in exam.items() if k not in ['questions','contextRevised']},key
        assert len(old['questions'])==len(exam['questions']),key
        for before,after in zip(old['questions'],exam['questions']):
            for field in ['id','answer','answerIsEmpty','weight','tokenMode','ignoredOptions','allowNoAnswer']:
                if key=='ue2.ed.annales' and field=='answer' and before['id'] in ED_KEY_REPAIRS:
                    assert (before.get(field),after.get(field))==ED_KEY_REPAIRS[before['id']],(key,before['id'],field)
                    continue
                assert before.get(field)==after.get(field),(key,before['id'],field)
            assert [o['id'] for o in before['options']]==[o['id'] for o in after['options']],key
    decoder=json.JSONDecoder();pos=1;spans=[]
    while True:
        while original[pos].isspace() or original[pos]==',':pos+=1
        if original[pos]=='}':break
        key,pos=decoder.raw_decode(original,pos)
        while original[pos].isspace() or original[pos]==':':pos+=1
        begin=pos
        _,pos=decoder.raw_decode(original,pos)
        if key in overrides:spans.append((begin,pos,dump(overrides[key])))
    assert len(spans)==3
    for begin,end,value in reversed(spans):original=original[:begin]+value+original[end:]
    for folder in ['static','sources']:
        source=path.parent/folder
        if folder=='static' and not source.exists():source=path.parent/'assets'
        if source.exists():
            for asset in source.rglob('*'):
                if asset.is_file():
                    relative=Path(folder)/asset.relative_to(source)
                    assert not (BASE/relative).exists(),relative
                    (OUT/relative).parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(asset,OUT/relative)
    (WORK/'context_revision_v2/overrides_applied.json').write_text(json.dumps(overrides,ensure_ascii=False,indent=2))
    return original


def build():
    html = (BASE / 'index.html').read_text()
    start = html.index('const EXAMS=') + len('const EXAMS=')
    existing, length = json.JSONDecoder().raw_decode(html[start:])
    original_json = html[start:start+length]
    additions = {}
    courses = {}
    for folder, unit in [('ue2', 'ue2c'), ('ue3', 'ue3'), ('ue4', 'ue4')]:
        directory = WORK / 'agents' / folder
        path = directory / 'exams.json'
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        assert isinstance(data, dict), path
        for key, exam in data.items():
            assert key not in existing and key not in additions, key
            assert exam['ue'] == unit, (key, exam['ue'], unit)
            for question in exam['questions']:
                question['fromCompilation'] = True
                question['allowNoAnswer'] = True
                if key=='ue4.annales.2020-2021.s1.galenique' and str(question['sourceNumber']) in ['13','14']:
                    # The source explicitly scopes this information to Q13–14.
                    assert not question.get('context') or 'oxyde de zinc' in question['context']
                    question['context']=''
                    question['sharedContexts']=[{'id':'ue4-2020-s1-zinc-13-14','text':'On vous précise que l’oxyde de zinc est à la fois insoluble dans l’eau et les huiles minérales.','images':[],'questionNumbers':[13,14],'sourceStartPage':879,'sourceEndPage':879}]
            additions[key] = exam
        raw_courses = json.loads((directory / 'courses.json').read_text())
        courses[unit] = raw_courses[unit] if isinstance(raw_courses, dict) and unit in raw_courses else raw_courses
        if isinstance(courses[unit], dict):
            courses[unit] = list(courses[unit].items())
        assert all(isinstance(x, list) and len(x) == 2 for x in courses[unit]), courses[unit]
        assetdir = directory / 'static'
        if not assetdir.exists():
            assetdir = directory / 'assets'
        if assetdir.exists():
            for asset in assetdir.rglob('*'):
                if not asset.is_file():
                    continue
                dest = OUT / 'static' / asset.relative_to(assetdir)
                assert not (BASE / 'static' / asset.relative_to(assetdir)).exists(), dest
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(asset, dest)
    original_json=replace_ed_banks(original_json,existing)
    # Preserve the other 77 original banks, and every scoring/storage identity.
    new_json = original_json[:-1] + (',' + dump(additions)[1:-1] if additions else '') + '}'
    html = html[:start] + new_json + html[start+length:]

    def replace(old, new, count=1):
        nonlocal html
        found = html.count(old)
        assert found == count, (old[:100], found, count)
        html = html.replace(old, new)

    replace('<title>Révisions PASS Lyon-Sud · UE1 / UE2 / UE5</title>', '<title>Révisions PASS Lyon-Sud · UE1 / UE2 / UE3 / UE4 / UE5</title>')
    replace('UE1 SSH, UE2 Biologie moléculaire et UE5 Histologie, Biologie cellulaire et Embryologie. Autotests, annales, exercices dirigés, correction PASS.', 'UE1 SSH, UE2 Biologie moléculaire, Biochimie et Chimie, UE3 Biostatistiques, UE4 Médicaments et UE5 Histologie, Biologie cellulaire et Embryologie. Autotests, annales, exercices dirigés, correction PASS.')

    new_units = [('ue2c', 'UE2 · Biochimie et chimie', 'BC'),
                 ('ue3', 'UE3 · Biostatistiques', 'BS'),
                 ('ue4', 'UE4 · Médicaments', 'M')]
    present_units = [x for x in new_units if x[0] in courses]
    unit_order = ['ue1', 'ue2b'] + [x[0] for x in present_units] + ['ue5h', 'ue5b', 'ue5e']
    replace("const UNIT_ORDER=['ue1','ue2b','ue5h','ue5b','ue5e'];", 'const UNIT_ORDER='+dump(unit_order)+';')
    replace('const UNIT_COURSES={', 'const UNIT_COURSES={\n'+''.join(dump(k)+':'+dump(v)+',\n' for k,v in courses.items()))
    labels = {unit:label for unit,label,mark in present_units}
    marks = {unit:mark for unit,label,mark in present_units}
    replace('const EXAM_KEYS=Object.keys(EXAMS);', 'const ADDED_UNIT_LABELS='+dump(labels)+';\nconst ADDED_UNIT_MARKS='+dump(marks)+';\nconst EXAM_KEYS=Object.keys(EXAMS);')
    for mobile in (False, True):
        dot = '' if mobile else '<span class="unit-dot"></span>'
        anchor = '<button type="button" class="unit-button js-unit-btn" data-unit="ue5h">'+dot+'UE5 · Histologie</button>'
        buttons = '\n  '.join('<button type="button" class="unit-button js-unit-btn" data-unit="'+unit+'">'+dot+label+'</button>' for unit,label,mark in present_units)
        replace(anchor, buttons+'\n  '+anchor)
    replace("esc(unit==='ue2b'?'UE2 · Biologie moléculaire':unit==='ue5h'?'UE5 · Histologie':unit==='ue5b'?'UE5 · Biologie cellulaire':'UE5 · Embryologie')", "esc(ADDED_UNIT_LABELS[unit]||(unit==='ue2b'?'UE2 · Biologie moléculaire':unit==='ue5h'?'UE5 · Histologie':unit==='ue5b'?'UE5 · Biologie cellulaire':'UE5 · Embryologie'))")
    replace("$('.brand-mark').textContent=exam.ue==='ue1'?'SSH':exam.ue==='ue2b'?'BM':exam.ue==='ue5h'?'H':exam.ue==='ue5b'?'BC':'DE';", "$('.brand-mark').textContent=ADDED_UNIT_MARKS[exam.ue]||(exam.ue==='ue1'?'SSH':exam.ue==='ue2b'?'BM':exam.ue==='ue5h'?'H':exam.ue==='ue5b'?'BC':'DE');")
    replace("$('#hero-kicker').textContent=exam.ue==='ue1'", "$('#hero-kicker').textContent=ADDED_UNIT_LABELS[exam.ue]?'PASS LYON-SUD / '+ADDED_UNIT_LABELS[exam.ue].toUpperCase():exam.ue==='ue1'")
    replace('cochez les propositions exactes pour chaque question, puis cliquez sur', "${ADDED_UNIT_LABELS[exam.ue]?'répondez selon la consigne de chaque question':'cochez les propositions exactes pour chaque question'}, puis cliquez sur")

    css = '''
/* Imported annales: isolated styles; the existing question layouts are unchanged. */
body[data-ue="ue2c"]{--teal:#aa5b27;--teal-soft:#fff0e3}
body[data-ue="ue3"]{--teal:#346ca2;--teal-soft:#eaf3fc}
body[data-ue="ue4"]{--teal:#377b68;--teal-soft:#eaf6f0}
.annales-stem{display:grid;gap:12px;margin:0 26px 20px}
.annales-stem figure{margin:0;border:1px solid var(--border);border-radius:11px;background:#fff;padding:10px;min-width:0}
.annales-stem a{display:block;cursor:zoom-in}
.annales-stem img{display:block;max-width:100%;width:auto;height:auto;margin:0 auto}
.annales-stem figcaption{font-size:10px;color:var(--muted);text-align:center;margin-top:6px}
.annales-correction-images{margin:14px 0 0}
.annales-option-image{display:block;max-width:100%;width:auto;height:auto;margin-top:6px}
.from-compilation .opt-text,.from-compilation .explain-text{white-space:pre-wrap;overflow-wrap:anywhere}
.from-compilation .option-content,.from-compilation .opt-text{min-width:0}
.from-compilation .option-none{background:var(--paper,#f9fbfc);font-size:12px}
.annales-correction-source{font-size:10px;color:var(--muted);margin:12px 0 4px;overflow-wrap:anywhere}
.annales-references .annales-stem{margin:12px 0 0}
.from-compilation .qsource a,.annales-correction-source a{color:inherit;text-decoration:underline;text-underline-offset:2px}
@media(max-width:700px){.annales-stem{margin:0 13px 16px}.annales-stem figure{padding:6px}.annales-correction-images{margin:12px 0 0}}
'''
    replace('</style>', css+'\n'+(WORK/'shared_contexts.css').read_text()+'\n</style>')
    helpers = '''
function isGradable(q){return !!q.answer||q.answerIsEmpty===true;}
function expectedLabel(q){return q.answerIsEmpty?'Aucune proposition':q.answer;}
function annalesPages(q,correction=false){
 const first=correction?q.correctionPage:(q.sourceStartPage||q.subjectPage);
 const last=correction?(q.correctionEndPage||first):(q.sourceEndPage||q.subjectPage||first);
 if(!first)return '';return first===last?' · p. '+first:' · pp. '+first+'–'+last;
}
function annalesImages(sources,caption,correction=false){
 if(!sources?.length)return '';
 return `<div class="annales-stem ${correction?'annales-correction-images':''}">${sources.map((src,i)=>`<figure><a href="${esc(src)}" target="_blank" rel="noopener noreferrer" aria-label="Agrandir ${esc(caption)} ${i+1}"><img loading="lazy" decoding="async" src="${esc(src)}" alt="${esc(caption)} ${i+1}"></a><figcaption>${esc(caption)}${sources.length>1?' · '+(i+1):''} · Cliquer pour agrandir</figcaption></figure>`).join('')}</div>`;
}
function noAnswerOption(q,done,v){
 if(!q.allowNoAnswer)return '';
 const checked=v.chosen==='∅';let cls=checked?'selected':'';let label='';
 if(done){cls='locked '+(!v.nonGraded&&q.answerIsEmpty?(checked?'grade-true':'grade-true-missed'):checked&&!v.nonGraded?'grade-false-selected':'');label=v.nonGraded?'Non évalué':q.answerIsEmpty?'Réponse attendue':checked?'Réponse incorrecte':'';}
 return `<label class="option option-none ${cls}"><input type="checkbox" data-q="${q.id}" value="∅" ${checked?'checked':''} ${done?'disabled':''} aria-label="QCM ${q.id}, aucune proposition"><span class="option-content"><span class="opt-letter">∅</span><span class="opt-text">Aucune proposition</span></span>${done&&label?`<span class="opt-status">${esc(label)}</span>`:''}</label>`;
}
'''
    replace('function selected(q){', helpers+'\n'+(WORK/'shared_contexts.js').read_text()+'\nfunction selected(q){')
    replace("matching.map(renderQuestionCard).join('')",'renderQuestionList(matching)')
    replace('q.question,q.context,...q.options.map(x=>x.text)',"q.question,q.context,...(q.sharedContexts||[]).map(c=>c.text),...q.options.map(x=>x.text)")
    replace('${q.context?`<div class="qcontext">','${sharedStatementLinks(q)}${q.context?`<div class="qcontext">')
    replace('QUESTIONS.filter(q=>q.answer)', 'QUESTIONS.filter(isGradable)', count=2)
    replace("for(const q of QUESTIONS){if(q.tokenMode)", "for(const q of QUESTIONS){if(q.allowNoAnswer&&obj.answers[q.id]==='∅'){answers[q.id]='∅';}else if(q.tokenMode)")
    replace('if(!q.answer)return {chosen,expected:null', 'if(!isGradable(q))return {chosen,expected:null')
    replace('const expected=q.answer;', "const expected=q.answerIsEmpty?'∅':q.answer;")
    replace('rated=all.filter(q=>q.answer&&', 'rated=all.filter(q=>isGradable(q)&&')
    replace("q.answer?'':' (non notée)'", "isGradable(q)?'':' (non notée)'")
    replace('<span class="opt-text">${esc(o.text)}</span>', '<span class="opt-text">${esc(o.text)}${o.image?`<img class="annales-option-image" loading="lazy" src="${esc(o.image)}" alt="Proposition ${esc(o.id)} du sujet original">`:\'\'}</span>')
    replace("}).join('');\n const ptcls", "}).join('')+noAnswerOption(q,done,v);\n const ptcls")
    replace('Correction du tutorat · ${esc(q.answer)}', 'Correction du tutorat · ${esc(expectedLabel(q))}')
    replace('Réponses attendues : ${esc(q.answer)}', 'Réponses attendues : ${esc(expectedLabel(q))}')
    replace('corrige:onlyFilledMode&&!isCorrected(q)?null:q.answer', "corrige:onlyFilledMode&&!isCorrected(q)?null:(q.answerIsEmpty?'∅':q.answer)")
    replace('return `<article class="qcard ${done&&issue?', '''if(done&&revisedSource(q)){
  const source=`<div class="annales-correction-source">${sourceReference(q.sourceCorrection||'Corrigé fourni',sourcePdfFor(q,true),q.correctionPage,q.correctionEndPage)}</div>`;
  details=details.replace(/<\\/div><\\/details>$/,source+annalesImages(q.correctionImages,'Extrait du corrigé fourni',true)+'</div></details>');
 }
 return `<article class="qcard ${revisedSource(q)?'from-compilation ':''}${done&&issue?''')
    replace('${q.originalImages?.length?`<details', "${annalesImages(q.stemImages,q.stemCaption||'Extrait du sujet non corrigé')}${q.originalImages?.length?`<details")
    replace('<summary>Voir l’extrait original du sujet non corrigé</summary>', '<summary>${q.fromCompilation?\'Voir les extraits de l’énoncé\':\'Voir l’extrait original du sujet non corrigé\'}</summary>')
    replace('alt="Extrait original non corrigé du document source"', 'alt="${q.fromCompilation?\'Extrait de l’énoncé du document source\':\'Extrait original non corrigé du document source\'}"')
    replace('<div class="opt-list">${opt}</div>', '${questionReferences(q)}${q.referenceImages?.length?`<details class="source-excerpt annales-references"><summary>${esc(q.referenceTitle||\'Tables et formulaire fournis avec le sujet\')}</summary>${q.referenceNote?`<p class="annales-correction-source">${esc(q.referenceNote)}</p>`:\'\'}${annalesImages(q.referenceImages,\'Annexe statistique du dossier\')}</details>`:\'\'}<div class="opt-list">${opt}</div>')
    replace("const target=QUESTIONS.find(q=>q.id===qid);if(!target||isCorrected(target))return;if(target?.tokenMode)", """const target=QUESTIONS.find(q=>q.id===qid);if(!target||isCorrected(target))return;
 if(target.allowNoAnswer&&id==='∅'){
  answers[qid]=input.checked?'∅':'';save();renderQuestions();updateCounters();return;
 }
 if(target.allowNoAnswer&&old==='∅'){
  answers[qid]=input.checked?id:'';save();renderQuestions();updateCounters();return;
 }
 if(target?.tokenMode)""")
    # Only imported banks show extra provenance and neutral selection labels.
    replace("${esc(q.sourceSubject||'Sujet fourni')}${q.sourceStartPage", "${revisedSource(q)&&sourcePdfFor(q)?`<a href=\"${esc(sourcePdfFor(q))}#page=${q.sourceStartPage||q.subjectPage||1}\" target=\"_blank\" rel=\"noopener noreferrer\">${esc(q.sourceSubject||'Sujet fourni')}</a>`:esc(q.sourceSubject||'Sujet fourni')}${revisedSource(q)&&q.sourceNumber?' · QCM source '+esc(q.printedSourceNumber||q.sourceNumber):''}${revisedSource(q)?annalesPages(q):q.sourceStartPage")
    # The answer key lists choices to select, including questions asking for false propositions.
    replace("status=truth?(checked?'Vrai · coché':'Vrai · oublié'):(checked?'Faux · coché':'Faux');", "status=q.fromCompilation?(truth?(checked?'Attendu · coché':'Attendu · oublié'):(checked?'Non attendu · coché':'Non attendu')):(truth?(checked?'Vrai · coché':'Vrai · oublié'):(checked?'Faux · coché':'Faux'));")
    replace("?'VRAI':'FAUX'}</span><span class=\"explain-text\">", "?(q.fromCompilation?'À COCHER':'VRAI'):(q.fromCompilation?'NE PAS COCHER':'FAUX')}</span><span class=\"explain-text\">")
    replace("<span>Plusieurs réponses possibles · cochez les propositions justes${ungraded?", "<span>${q.fromCompilation?'Cochez les propositions demandées dans la consigne':'Plusieurs réponses possibles · cochez les propositions justes'}${ungraded?")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'index.html').write_text(html)
    # Earlier QA builds can leave obsolete crops behind. Ship only the new
    # annales images referenced by the final page; never remove old assets.
    referenced=set(re.findall(r'static/[^\s"\'<>]+\.(?:png|jpg|jpeg|webp|svg)',html))
    removed=[]
    for asset in list((OUT/'static').glob('annales_*'))+list((OUT/'static').glob('biomol_ed_revision_*')):
        relative=asset.relative_to(OUT).as_posix()
        if asset.is_file() and relative not in referenced and not (BASE/relative).exists():
            removed.append(relative)
            asset.unlink()
    (WORK/'review/obsolete_crops_removed.json').write_text(json.dumps(removed,indent=2))
    (WORK / 'added_exams.json').write_text(json.dumps(additions, ensure_ascii=False, indent=2))
    (WORK / 'added_courses.json').write_text(json.dumps(courses, ensure_ascii=False, indent=2))
    print(json.dumps({'new_series':len(additions),'new_questions':sum(len(v['questions']) for v in additions.values()),'units':list(courses),'html_bytes':len(html.encode())},ensure_ascii=False))


if __name__ == '__main__':
    build()
