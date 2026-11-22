"""Regroup the reviewed UE4 questions, preserving the delivered V2 elsewhere."""
from pathlib import Path
import argparse, collections, copy, hashlib, html, json, re, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SITE=ROOT/'output/site'
DECODER=json.JSONDecoder()

def read(name):return json.loads((HERE/name).read_text())
def compact(value):return json.dumps(value,ensure_ascii=False,separators=(',',':'))
def sha(value):return hashlib.sha256(value if isinstance(value,bytes) else compact(value).encode()).hexdigest()

def replace_once(text,old,new):
    assert text.count(old)==1,(old[:160],text.count(old))
    return text.replace(old,new,1)

def apply_patch(q,patch):
    field=patch['field'];parts=field.split('.')
    assert parts[0] in {'question','context','options','answer','warning','explanations','generalExplanation','images','stemImages','originalImages','correctionImages','sharedContexts','sourceEndPage','correctionEndPage'},field
    node=q
    for part in parts[:-1]:
        if isinstance(node,list):node=next(x for x in node if str(x['id'])==part)
        else:node=node[part]
    old=node.get(parts[-1])
    assert old==patch.get('before'),(q['sourceId'],field,'before mismatch')
    node[parts[-1]]=copy.deepcopy(patch['after'])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true');args=parser.parse_args()
    original=(HERE/'baseline_index.html').read_text()
    baseline=read('baseline_exams.json');records=read('questions_v2.json');themes=read('themes.json');theme_names=dict(themes)
    reviews={};review_parts=[]
    if args.draft:
        defaults={'nature':'sources-naturelles','galenique':'galenique','droit':'droit','clinique':'developpement-clinique','vigilance':'iatrogenie','chimie':'conception-rationnelle','decouverte':'identification-pa','biotech':'biotechnologies','pd':'pk-pd','pk':'pk-pd','controle':'analyse-controles','usage':'bum'}
        for record in records:reviews[record['question']['sourceId']]={'themeId':defaults[record['bank']['courseId']],'reviewNotes':[],'patches':[]}
    else:
        for lot in ['recent','middle','older']:
            part=read(lot+'/reviews.json');part=part.get('reviews',part) if isinstance(part,dict) else part
            for review in part:
                sid=review['sourceId'];assert sid not in reviews,('duplicate review',sid)
                assert set(review['checksAtoE'])==set('ABCDE'),('incomplete review',sid)
                reviews[sid]=review
            review_parts.append({'lot':lot,'questions':len(part),'sha256':sha((HERE/lot/'reviews.json').read_bytes())})
        assert set(reviews)=={r['question']['sourceId'] for r in records},'Missing or unexpected QCM review'
    decisions=read('patch_decisions.json') if (HERE/'patch_decisions.json').exists() else {}
    covered_warnings=read('warning_coverage.json') if (HERE/'warning_coverage.json').exists() else []
    grouped={k:[] for k,_ in themes};links=[];aliases={};changes=[]
    for record in records:
        before=record['question'];sid=before['sourceId'];review=reviews[sid];theme=review['themeId'];assert theme in theme_names,(sid,theme)
        q=copy.deepcopy(before)
        for patch in review.get('patches',[]):
            decision_key=sid+'|'+patch['field']
            decision=decisions.get(decision_key)
            assert decision is not None,('Unreviewed proposed patch',decision_key)
            if decision['apply']:
                if patch['field']=='answer':assert decision.get('restoresSourceKey') is True,('Key change needs independently verified source evidence',sid)
                apply_patch(q,patch);changes.append({'sourceId':sid,**patch,'decision':decision})
        for field in ['sourceId','answer','rawAnswer','answerIsEmpty','weight','sourceNumber','subjectPage','correctionNumber','correctionPage','allowNoAnswer']:
            if q.get(field)!=before.get(field):
                assert field=='answer' and decisions.get(sid+'|answer',{}).get('restoresSourceKey') is True,(sid,'protected question field',field)
        assert [o['id'] for o in q['options']]==[o['id'] for o in before['options']]
        q['pharmaReviewed']=True
        q['category']=theme_names[theme];q['course']=theme_names[theme]
        q['reviewNotes']=copy.deepcopy(review.get('reviewNotes',[]))
        q['pharmaWarningCovered']=bool(q.get('warning') and sid in covered_warnings and q['reviewNotes'])
        for note in q['reviewNotes']:
            assert isinstance(note.get('text'),str) and note['text'].strip(),(sid,'empty review note')
            assert set(note.get('items',[]))<=set('ABCDE'),(sid,'invalid note item')
            assert 'ronéo' in note['text'].lower(),(sid,'note lacks roneo invitation')
        q['legacyProgress']={'storage':record['legacyStorage'],'id':record['legacyId'],'bank':record['legacyBank']}
        grouped[theme].append(q)
        links.append({'sourceId':sid,'storage':record['legacyStorage'],'id':record['legacyId']})
        aliases.setdefault(record['legacyBank'],'ue4.annales.theme.'+theme)
    banks={};question_map={}
    for theme,label in themes:
        questions=grouped[theme]
        questions.sort(key=lambda q:(-int(q['year'][:4]),{'S1':0,'S2':1,'PACES':2}.get(q['session'],3),int(q['sourceNumber'])))
        key='ue4.annales.theme.'+theme
        for i,q in enumerate(questions,1):
            q['id']=i;question_map[q['sourceId']]={'bank':key,'id':i,'themeId':theme,'theme':label,'legacy':q['legacyProgress']}
        # Remap local membership without changing source numbers or common data.
        contexts={}
        for q in questions:
            for c in q.get('sharedContexts',[]):contexts.setdefault(c['id'],[]).append(q['id'])
        for q in questions:
            for c in q.get('sharedContexts',[]):c['questionIds']=contexts[c['id']]
        banks[key]={'ue':'ue4','courseId':theme,'kind':'annales','pharmaGrouped':True,'seriesLabel':'Annales','label':'Annales · '+label,'short':'UE4','title':html.escape(label)+'<br>Annales','subtitle':'Tous les QCM de ce thème sont réunis dans une seule série. Les références d’origine restent sous chaque consigne.','description':'UE4 · '+label+' · Annales · PASS Lyon-Sud','storage':'qcm-pass-ls-ue4-theme-'+theme+'-v3','questions':questions}
    assert sum(len(b['questions']) for b in banks.values())==336
    assert len(question_map)==336
    output_exams={k:v for k,v in baseline.items() if v['ue']!='ue4'}|banks
    data_start=original.index('const EXAMS=')+len('const EXAMS=');_,data_end=DECODER.raw_decode(original[data_start:]);data_end+=data_start
    raw=original[data_start:data_end];pieces=[];pos=1
    while pos<len(raw)-1:
        while raw[pos].isspace() or raw[pos]==',':pos+=1
        key,start=DECODER.raw_decode(raw,pos);colon=raw.index(':',start);value_start=colon+1
        while raw[value_start].isspace():value_start+=1
        value,end=DECODER.raw_decode(raw,value_start)
        if value['ue']!='ue4':pieces.append(raw[pos:end])
        pos=end
    pieces += [compact(k)+':'+compact(v) for k,v in banks.items()]
    result=original[:data_start]+'{'+','.join(pieces)+'}'+original[data_end:]
    match=re.search(r'^"ue4":\[.*\],$',result,re.M);assert match
    result=result[:match.start()]+'"ue4":'+compact(themes)+','+result[match.end():]
    result=replace_once(result,'"ue4":"UE4 · Médicaments"','"ue4":"UE4 · Pharmaco"')
    assert result.count('UE4 · Médicaments</button>')==2
    result=result.replace('UE4 · Médicaments</button>','UE4 · Pharmaco</button>')
    runtime='const PHARMA_PROGRESS_LINKS='+compact(links)+';\nconst PHARMA_EXAM_ALIASES='+compact(aliases)+';\n'+(HERE/'pharma_runtime.js').read_text()
    result=replace_once(result,"const ACTIVE_KEY='ssh_pass_selected_exam_v1';",runtime+"\nconst ACTIVE_KEY='ssh_pass_selected_exam_v1';")
    result=replace_once(result,"if(EXAMS[saved])activeExam=saved;","if(EXAMS[saved])activeExam=saved;else if(PHARMA_EXAM_ALIASES[saved])activeExam=PHARMA_EXAM_ALIASES[saved];")
    result=replace_once(result,'function isCorrected(q){return onlyFilledMode?correctedIds.has(q.id):submitted;}','function isCorrected(q){return perQuestionCorrection()?correctedIds.has(q.id):submitted;}')
    result=replace_once(result,'answers={};submitted=false;correctedIds=new Set();\n try{','answers={};submitted=false;correctedIds=new Set();\n if(exam.pharmaGrouped){loadPharmaProgress();syncProfileSwitch();return;}\n try{')
    result=replace_once(result,'function save(){\n const snap=','function save(){\n if(groupedPharma()){savePharmaProgress();return;}\n const snap=')
    result=replace_once(result,'function gradeAll(){\n if(onlyFilledMode){','function gradeAll(){\n if(groupedPharma()&&!onlyFilledMode){if(!TOTAL||QUESTIONS.every(isCorrected))return;correctedIds=new Set(QUESTIONS.map(q=>q.id));submitted=true;statusFilter=\'all\';save();render();$(\'#results\').scrollIntoView({behavior:\'smooth\',block:\'start\'});return;}\n if(onlyFilledMode){')
    result=replace_once(result,'function modify(){if(onlyFilledMode){correctedIds.clear();}','function modify(){if(perQuestionCorrection()){correctedIds.clear();}')
    result=replace_once(result,"function renderToolbar(){\n const bar=$('#toolbar-content');","function renderToolbar(){\n if(groupedPharma()&&!onlyFilledMode){renderPharmaClassicToolbar();return;}\n const bar=$('#toolbar-content');")
    # These expressions are identical outside UE4, where perQuestionCorrection()==onlyFilledMode.
    result=result.replace('(!onlyFilledMode||correctedIds.has(', '(!perQuestionCorrection()||correctedIds.has(')
    result=result.replace('(onlyFilledMode?s.ratedWeight:WEIGHTED_TOTAL)','(perQuestionCorrection()?s.ratedWeight:WEIGHTED_TOTAL)')
    result=result.replace("${onlyFilledMode?s.ratedCount:GRADED}","${perQuestionCorrection()?s.ratedCount:GRADED}")
    result=result.replace("${onlyFilledMode?' · QCM corrigés uniquement':''}","${perQuestionCorrection()?' · QCM corrigés uniquement':''}")
    result=result.replace('onlyFilledMode&&!isCorrected(q)','perQuestionCorrection()&&!isCorrected(q)')
    result=result.replace("onlyFilledMode&&!s.ratedCount?null:","perQuestionCorrection()&&!s.ratedCount?null:")
    result=result.replace('qcm_notes:onlyFilledMode?s.ratedCount:GRADED','qcm_notes:perQuestionCorrection()?s.ratedCount:GRADED')
    result=replace_once(result,"const v=assessed(q),done=isCorrected(q),issue=!!q.warning,ungraded=v.nonGraded;","const v=assessed(q),done=isCorrected(q),issue=!!q.warning||!!q.reviewNotes?.length,ungraded=v.nonGraded;")
    result=result.replace('${issue?`<div class="issue">','${issue&&!q.pharmaReviewed?`<div class="issue">')
    result=replace_once(result,"if(done&&revisedSource(q)){\n  const source=","if(done&&q.pharmaReviewed)details=details.replace(/<\\/div><\\/details>$/,pharmaReviewHtml(q)+'</div></details>');\n if(done&&revisedSource(q)){\n  const source=")
    result=replace_once(result,"${revisedSource(q)&&q.sourceNumber?' · QCM source '","${pharmaSourceLabel(q)}${revisedSource(q)&&q.sourceNumber?' · QCM source '")
    result=replace_once(result,"return {numero:q.id,theme:q.category,reponses:a.chosen||'',","return {...(q.pharmaReviewed?{identifiant_source:q.sourceId,annee:q.year,session:q.session,numero_source:q.printedSourceNumber||q.sourceNumber,commentaires:!isCorrected(q)?undefined:q.reviewNotes}:{}),numero:q.id,theme:q.category,reponses:a.chosen||'',")
    result=replace_once(result,'remarque_corrige:q.warning||undefined','remarque_corrige:q.pharmaReviewed&&!isCorrected(q)?undefined:q.warning||undefined')
    result=replace_once(result,"$('#side-track').style.width=`${n/TOTAL*100}%`;","$('#side-track').style.width=`${TOTAL?n/TOTAL*100:0}%`;")
    result=replace_once(result,"const ue5=unit!=='ue1';","$('#sidebar-series .explorer-caption').textContent=unit==='ue4'?'Sélectionnez un thème pour retrouver toutes ses annales.':'Sélectionnez un chapitre puis un questionnaire.';\n const ue5=unit!=='ue1';")
    result=replace_once(result,'</style>','\n'+(HERE/'pharma_style.css').read_text()+'\n</style>')
    destination=HERE/'draft_index.html' if args.draft else SITE/'index.html'
    if not args.draft:
        for lot in ['recent','middle','older']:
            for folder in ['assets','static']:
                for path in (HERE/lot/folder).glob('*'):
                    if not path.is_file():continue
                    target=SITE/'static'/path.name
                    if target.exists():assert path.read_bytes()==target.read_bytes(),('refuse to overwrite existing asset',path.name)
                    else:shutil.copy2(path,target)
    destination.write_text(result)
    prefix='draft_' if args.draft else ''
    (HERE/(prefix+'exams_v3.json')).write_text(json.dumps(output_exams,ensure_ascii=False,indent=2))
    (HERE/(prefix+'question_map.json')).write_text(json.dumps(question_map,ensure_ascii=False,indent=2))
    manifest={'draft':args.draft,'questions':336,'items':1680,'themes':len(banks),'totalSiteQuestions':sum(len(x['questions']) for x in output_exams.values()),'totalSiteBanks':len(output_exams),'notesQuestions':sum(bool(q.get('reviewNotes')) for b in banks.values() for q in b['questions']),'notesCount':sum(len(q.get('reviewNotes',[])) for b in banks.values() for q in b['questions']),'themeCounts':{label:len(grouped[k]) for k,label in themes},'reviewInputs':review_parts,'appliedPatches':changes,'htmlSha256':sha(result.encode()),'protectedNonUE4Banks':len(output_exams)-len(banks),'protectedNonUE4Questions':sum(len(x['questions']) for x in baseline.values() if x['ue']!='ue4')}
    (HERE/(prefix+'build_manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['appliedPatches','reviewInputs']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
