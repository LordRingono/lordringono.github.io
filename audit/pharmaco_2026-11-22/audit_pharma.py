"""Verify the merged pharmacology review and create complete delivery inventories."""
from pathlib import Path
import collections, copy, csv, hashlib, json, re
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SITE=ROOT/'output/site'
AUDIT=SITE/'audit'

def read(name):return json.loads((HERE/name).read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def write_json(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def all_asset_paths(value):
    if isinstance(value,dict):
        for v in value.values():yield from all_asset_paths(v)
    elif isinstance(value,list):
        for v in value:yield from all_asset_paths(v)
    elif isinstance(value,str) and (value.startswith('static/') or value.startswith('sources/')):yield value
def get_field(q,field):
    for part in field.split('.'):
        q=next(x for x in q if str(x['id'])==part) if isinstance(q,list) else q.get(part)
    return q
def set_field(q,field,value):
    parts=field.split('.');node=q
    for part in parts[:-1]:node=next(x for x in node if str(x['id'])==part) if isinstance(node,list) else node[part]
    node[parts[-1]]=copy.deepcopy(value)
def graded(q):return bool(q.get('answer')) or bool(q.get('answerIsEmpty'))
def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)

def main():
    baseline=read('baseline_exams.json');exams=read('exams_v3.json');records=read('questions_v2.json')
    manifest=read('build_manifest.json');mapping=read('question_map.json');decisions=read('patch_decisions.json')
    assert not manifest['draft']
    assert manifest['htmlSha256']==sha(SITE/'index.html')
    old={r['question']['sourceId']:r for r in records}
    reviews={};review_lots=[]
    for lot,expected in [('recent',114),('middle',112),('older',110)]:
        data=read(lot+'/reviews.json');assert len(data)==expected,(lot,len(data))
        for r in data:
            sid=r['sourceId'];assert sid not in reviews;reviews[sid]=r
            assert set(r['checksAtoE'])==set('ABCDE')
            assert r.get('reason') and r.get('confidence')
            for letter,check in r['checksAtoE'].items():
                assert check,(sid,letter,'empty review')
                text=next(o['text'] for o in old[sid]['question']['options'] if o['id']==letter)
                if 'subjectText' in check:assert check['subjectText']==text,(sid,letter,'review text mismatch')
                if 'optionTextSha256' in check:assert hashlib.sha256(text.encode()).hexdigest()==check['optionTextSha256']
        review_lots.append({'lot':lot,'questions':expected,'items':expected*5,'review_sha256':sha(HERE/lot/'reviews.json')})
    assert set(reviews)==set(old)==set(mapping)
    nonpharma={k:v for k,v in baseline.items() if v['ue']!='ue4'}
    for k,v in nonpharma.items():assert exams[k]==v,('protected data changed',k)
    assert len(nonpharma)==202 and sum(len(b['questions']) for b in nonpharma.values())==2452
    pharma={k:v for k,v in exams.items() if v['ue']=='ue4'}
    assert len(pharma)==15 and len(exams)==217
    assert [b['courseId'] for b in pharma.values()]==[x[0] for x in read('themes.json')]
    seen={};applied=[];notes=[];qrows=[];irows=[];contexts=collections.defaultdict(list)
    for bank,b in pharma.items():
        assert b['kind']=='annales' and b['pharmaGrouped']
        assert not b.get('year') and not b.get('session')
        assert [q['id'] for q in b['questions']]==list(range(1,len(b['questions'])+1))
        for q in b['questions']:
            sid=q['sourceId'];assert sid not in seen;seen[sid]=q
            record=old[sid];before=record['question'];r=reviews[sid]
            assert int(q['year'][:4])>=2015
            assert r['themeId']==b['courseId'] and q['category']==q['course']==dict(read('themes.json'))[r['themeId']]
            expected=copy.deepcopy(before)
            for patch in r.get('patches',[]):
                key=sid+'|'+patch['field'];decision=decisions[key]
                assert get_field(expected,patch['field'])==patch['before'],key
                if decision['apply']:
                    set_field(expected,patch['field'],patch['after']);applied.append({'sourceId':sid,'field':patch['field']})
                    if patch['field']=='answer':assert decision.get('restoresSourceKey') and patch['after']==q['rawAnswer']
            # The only non-editorial content changes must be the explicitly reviewed patches.
            for field,value in expected.items():
                if field in {'id','category','course','sharedContexts'}:continue
                assert q[field]==value,(sid,'unexpected content change',field)
            assert q['options']==before['options'],(sid,'item text or image changed')
            assert q['question']==before['question'] and q['context']==before['context']
            assert q['legacyProgress']=={'storage':record['legacyStorage'],'id':record['legacyId'],'bank':record['legacyBank']}
            assert q['reviewNotes']==r.get('reviewNotes',[])
            for note in q['reviewNotes']:
                assert note.get('text') and 'ronéo' in note['text'].lower()
                assert set(note.get('items',[]))<=set('ABCDE')
                notes.append({'sourceId':sid,'theme':q['category'],'year':q['year'],'session':q['session'],'sourceNumber':q['sourceNumber'],'subjectPage':q['subjectPage'],'correctionPage':q['correctionPage'],**note})
            for context in q.get('sharedContexts',[]):
                original=next(c for c in before.get('sharedContexts',[]) if c['id']==context['id'])
                assert {k:v for k,v in context.items() if k!='questionIds'}=={k:v for k,v in original.items() if k!='questionIds'}
                contexts[(bank,context['id'])].append(q['id'])
            common={'identifiant_source':sid,'theme':q['category'],'annee':q['year'],'session':q['session'],'numero_source':q['sourceNumber'],'serie':bank,'numero_local':q['id'],'page_sujet':q['subjectPage'],'page_corrige':q['correctionPage'],'page_grille':q['shortCorrectionPage']}
            qrows.append({**common,'consigne':q['question'],'cle_utilisee':q['answer'],'cle_source':q.get('rawAnswer',''),'statut':'Noté' if graded(q) else 'Hors note','motif_classement':r['reason'],'commentaires':' | '.join(('Items '+','.join(n.get('items',[]))+': ' if n.get('items') else '')+n['text'] for n in q['reviewNotes']),'reserve_preexistante':q.get('warning','')})
            for o in q['options']:
                n=[n['text'] for n in q['reviewNotes'] if not n.get('items') or o['id'] in n['items']]
                irows.append({**common,'consigne':q['question'],'item':o['id'],'texte_item':o['text'],'image_item':o.get('image',''),'attendu_selon_cle_source':o['id'] in q.get('rawAnswer',''),'correction_source_avant_revue':before.get('explanations',{}).get(o['id'],''),'correction_affichee':q.get('explanations',{}).get(o['id'],''),'explication_commune':q.get('generalExplanation',''),'commentaires':' | '.join(n),'controle':json.dumps(r['checksAtoE'][o['id']],ensure_ascii=False),'statut_qcm':'Noté' if graded(q) else 'Hors note'})
    assert len(seen)==336 and len(irows)==1680
    for (bank,cid),members in contexts.items():
        for q in pharma[bank]['questions']:
            for c in q.get('sharedContexts',[]):
                if c['id']==cid:assert c['questionIds']==members
    key_changes=[sid for sid,q in seen.items() if q['answer']!=old[sid]['question']['answer']]
    assert key_changes==['ue4:2023-2024:S2:q05'],key_changes
    assert sum(graded(q) for q in seen.values())==325
    assert len(applied)==len(manifest['appliedPatches'])
    # All old image/PDF bytes, including files no longer referenced after a repair,
    # remain intact. Only question-to-asset references change where approved.
    protected_files=0
    for name,info in read('baseline_files.json')['files'].items():
        if name.startswith(('static/','sources/')):
            p=SITE/name;assert p.is_file() and p.stat().st_size==info['bytes'] and sha(p)==info['sha256'],('protected asset changed',name)
            protected_files+=1
    references=sorted(set(all_asset_paths(exams)));image_count=0;preexisting_missing=[]
    pharma_references=set(all_asset_paths(pharma))
    for name in references:
        p=SITE/name
        if not p.is_file():
            assert name not in pharma_references,('missing pharmacology asset',name)
            assert name in set(all_asset_paths(nonpharma)),('new missing asset',name)
            preexisting_missing.append(name);continue
        if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif'}:
            with Image.open(p) as im:im.verify()
            image_count+=1
    assert sha(SITE/'sources/Annales_compilation.pdf')=='f4bd0582c8d110fe22561066a89ad5ecf458207cd212765ce007e6d41e9273ec'
    assert preexisting_missing==['static/docx_3ec65cccd480.emf'],preexisting_missing
    assert 'static/annales_ue4_2023-2024_s2_q05_explanation_p797.webp' not in seen['ue4:2023-2024:S2:q05']['correctionImages']
    AUDIT.mkdir(exist_ok=True)
    write_csv(AUDIT/'PHARMACO_classement_336_QCM.csv',qrows)
    write_csv(AUDIT/'PHARMACO_relecture_1680_items.csv',irows)
    write_json(AUDIT/'PHARMACO_reserves.json',notes)
    # Current general inventory, retaining all other units verbatim by row.
    with (HERE/'baseline_inventory.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    changed_rows=0
    for row in rows:
        if not row['unite'].startswith('UE4'):continue
        year=row['annee'].replace('–','-');session={'Session 1':'S1','Session 2':'S2','PACES':'PACES'}.get(row['session'],row['session'])
        sid=f"ue4:{year}:{session}:q{int(row['numero_source']):02d}";q=seen[sid];m=mapping[sid]
        row.update(unite='UE4 · Pharmaco',matiere=m['theme'],serie=m['bank'],numero_local=str(m['id']),statut='Noté' if graded(q) else 'Hors note',cle_utilisee=q['answer'],reserve=q.get('warning',''))
        changed_rows+=1
    assert changed_rows==336 and len(rows)==838
    write_csv(AUDIT/'inventaire_838_qcm.csv',rows)
    report={'status':'PASS','scope':'Complétude et fidélité documentaire de la revue ; pas de certification scientifique des corrigés du tutorat.','total_site_qcm':sum(len(b['questions']) for b in exams.values()),'total_site_banks':len(exams),'pharma_qcm':336,'pharma_items':1680,'pharma_subjects':14,'themes':manifest['themeCounts'],'graded_pharma':325,'ungraded_pharma':11,'new_import_ungraded_total':sum(not graded(q) for b in exams.values() if b['ue'] in {'ue2c','ue3','ue4'} for q in b['questions']),'questions_with_new_notes':sum(bool(q['reviewNotes']) for q in seen.values()),'new_note_count':len(notes),'preexisting_warnings':sum(bool(q.get('warning')) for q in seen.values()),'key_restorations':key_changes,'applied_field_patches':applied,'protected_other_banks':202,'protected_other_qcm':2452,'protected_image_pdf_files':protected_files,'referenced_files':len(references),'decoded_images':image_count,'shared_context_questions':sum(bool(q.get('sharedContexts')) for q in seen.values()),'review_lots':review_lots,'html_sha256':sha(SITE/'index.html')}
    report['preexisting_missing_nonpharma_assets']=preexisting_missing
    report['pharma_missing_assets']=[]
    write_json(HERE/'data_audit.json',report)
    write_json(AUDIT/'PHARMACO_validation_donnees.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
