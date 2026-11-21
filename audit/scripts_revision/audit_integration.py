"""Independent cross-checks of imported annales against source maps and keys."""
from pathlib import Path
import json, re, hashlib, collections
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'work'
OUT=ROOT/'output/site'


def read_json(path):
    return json.loads(path.read_text())


def run():
    added=read_json(WORK/'added_exams.json')
    errors=[]; notices=[]; stats={}; assets={}; asset_ranges={}; source_units={}
    for folder,unit in [('ue2','ue2c'),('ue3','ue3'),('ue4','ue4')]:
        directory=WORK/'agents'/folder
        path=directory/'assets_manifest.json'
        if path.exists():
            data=read_json(path)
            if isinstance(data,dict):data=data.get('assets',data.get('images',list(data.values())))
            for item in data:
                ap=item.get('path') or item.get('file')
                if ap:
                    assets[ap]=item;source_units[ap]=unit
        manifest=directory/'manifest.json'
        if manifest.exists():
            m=read_json(manifest)
            subjects=m if isinstance(m,list) else m.get('subjects',m.get('sessions',[]))
            ranges=[]
            for s in subjects:
                subject=s.get('subjectRange') or s.get('subjectPageRange') or s.get('subject')
                correction=s.get('correctionRange') or s.get('correctionPageRange') or s.get('correction')
                if isinstance(subject,list) and isinstance(correction,list):ranges.append((subject,correction))
            asset_ranges[unit]=ranges

    short_pages=read_json(WORK/'root_short_keys.json')
    keymaps={p['page']:{int(n):v.strip() for n,v in p['values']} for p in short_pages}
    seen_source=set(); all_storage=set(); checked_keys=0; checked_links=0; checked_images=set()
    pending_manual=[]
    for examkey,exam in added.items():
        unit=exam['ue'];stats.setdefault(unit,collections.Counter())
        stats[unit]['series']+=1
        if exam['storage'] in all_storage:errors.append([examkey,'duplicate storage key'])
        all_storage.add(exam['storage'])
        ids=[q['id'] for q in exam['questions']]
        if ids!=list(range(1,len(ids)+1)):errors.append([examkey,'non sequential ids',ids])
        for q in exam['questions']:
            ref=[examkey,q['id'],q.get('sourceNumber'),q.get('subjectPage')]
            stats[unit]['questions']+=1
            rated=bool(q.get('answer')) or q.get('answerIsEmpty') is True
            stats[unit]['graded' if rated else 'ungraded']+=1
            stats[unit]['warnings']+=bool(q.get('warning'))
            if q.get('answerIsEmpty'):stats[unit]['empty_keys']+=1
            if not q.get('question','').strip():errors.append(ref+['missing instruction'])
            if re.fullmatch(r'(?:Question|QCM|QRM)\s*\d+\s*[.:]?',q.get('question',''),re.I):errors.append(ref+['title is only a number'])
            if not rated and not q.get('warning'):errors.append(ref+['ungraded without explanation'])
            if q.get('answer') and not re.fullmatch(r'[ABCDE]+',q['answer']):errors.append(ref+['invalid key',q['answer']])
            if [o['id'] for o in q['options']]!=list('ABCDE'):errors.append(ref+['unexpected option ids'])
            if (q.get('weight') or 1) not in [1,2,3]:notices.append(ref+['unusual coefficient',q.get('weight')])
            years=re.findall(r'20\d{2}|19\d{2}',str(q.get('year') or q.get('sourceExam',{}).get('year') or exam['seriesLabel']))
            if not years:errors.append(ref+['year unknown'])
            elif min(map(int,years))<2015:errors.append(ref+['older than2015',years])
            identity=(unit,q.get('subjectPage'),q.get('sourceNumber'))
            if identity in seen_source:errors.append(ref+['duplicate question source'])
            seen_source.add(identity)
            prompt_fields=[q.get('question',''),q.get('context','')]+[o.get('text','') for o in q['options']]+[c.get('text','') for c in q.get('sharedContexts',[])]
            for content in prompt_fields:
                if re.search(r'(?:VRAI|FAUX)\s*:|Correction (?:courte|détaillée)|Réponses attendues|\ufffd|[\ue000-\uf8ff]',content):errors.append(ref+['suspicious prompt text',content[:300]])
            if not q.get('originalImages'):
                notices.append(ref+['no original source excerpt'])
            image_fields=[(field,q.get(field,[])) for field in ['images','stemImages','originalImages','referenceImages','correctionImages']]
            image_fields += [('sharedContexts',c.get('images',[])) for c in q.get('sharedContexts',[])]
            image_fields += [('references',c.get('images',[])) for c in q.get('references',[])]
            for field,links in image_fields:
                for link in links:
                    checked_links+=1
                    if not (OUT/link).is_file():errors.append(ref+['missing asset',field,link]);continue
                    meta=assets.get(link)
                    if not meta:errors.append(ref+['missing asset provenance',link]);continue
                    role=meta.get('role','');pg=meta.get('page')
                    # One original diagram is absent from the subject PDF and
                    # reproduced, unannotated, in its correction. Both source
                    # pages and this exact crop were visually checked by root.
                    verified_reproduction=(
                        unit=='ue2c' and q.get('subjectPage')==305
                        and int(q.get('sourceNumber',0))==30 and pg==322
                        and role=='subject_reproduced_in_correction'
                        and meta.get('verifiedUnannotated') is True
                        and len(meta.get('bbox',[]))==4
                        and all(abs(a-b)<0.1 for a,b in zip(meta['bbox'],[42.85,212.59,538.55,337.09]))
                    )
                    if field!='correctionImages' and role!='subject' and not verified_reproduction:errors.append(ref+['answer leak: pre-correction image',field,role,link])
                    if field=='correctionImages' and role!='correction':notices.append(ref+['correction image role unexpected',role,link])
                    ranges=asset_ranges.get(unit,[])
                    if ranges and pg and not any((sr if role=='subject' else cr)[0]<=pg<=(sr if role=='subject' else cr)[1] for sr,cr in ranges):errors.append(ref+['asset outside declared source ranges',role,pg,link])
                    if link not in checked_images:
                        try:
                            im=Image.open(OUT/link);im.verify()
                        except Exception as e:errors.append(ref+['image corrupted',link,str(e)])
                        checked_images.add(link)
            for o in q['options']:
                if o.get('image'):
                    link=o['image'];checked_links+=1
                    if not (OUT/link).exists():errors.append(ref+['missing option image',link])
                    meta=assets.get(link,{})
                    if meta.get('role')!='subject':errors.append(ref+['option image provenance',link])
                    pg=meta.get('page');ranges=asset_ranges.get(unit,[])
                    if ranges and pg and not any(sr[0]<=pg<=sr[1] for sr,cr in ranges):errors.append(ref+['option image outside subject ranges',pg,link])
                    if link not in checked_images and (OUT/link).exists():
                        try:
                            im=Image.open(OUT/link);im.verify()
                        except Exception as e:errors.append(ref+['option image corrupted',link,str(e)])
                        checked_images.add(link)
            # Independently extracted short correction grids, not the agents' answer copies.
            cp=q.get('correctionPage');cn=q.get('correctionNumber') or q.get('sourceNumber')
            if isinstance(cp,int) and str(cn).isdigit():
                prior=[p for p in keymaps if p<=cp]
                if prior:
                    kp=max(prior);raw=keymaps[kp].get(int(cn))
                    if rated and raw and re.fullmatch('[ABCDE]+',raw):
                        if q.get('answer')!=raw:errors.append(ref+['key differs from original grid',kp,int(cn),raw,q.get('answer')])
                        else:checked_keys+=1
                    elif rated and q.get('answerIsEmpty') and raw in ['AUCUNE','RIEN']:
                        checked_keys+=1
                    elif rated:
                        pending_manual.append(ref+['short grid check needs manual review',kp,int(cn),raw])
    for unit,counts in stats.items():stats[unit]=dict(counts)
    # Every existing source reference must resolve, including the recovered old WEBPs.
    full=(OUT/'index.html').read_text()
    refs=set(re.findall(r'static/[^\s"\'<>]+\.(?:png|jpg|jpeg|webp|svg)',full))
    for rel in refs:
        if not (OUT/rel).is_file():errors.append(['missing link in complete site',rel])
    report={'stats':stats,'errors':errors,'notices':notices,'manual_grid_review':pending_manual,'independently_checked_keys':checked_keys,'asset_references_checked':checked_links,'unique_images_decoded':len(checked_images),'all_site_asset_references':len(refs),'source_pdf_sha256':hashlib.sha256((OUT/'sources/Annales_compilation.pdf').read_bytes()).hexdigest()}
    (WORK/'review/integration_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['errors','notices','manual_grid_review']},ensure_ascii=False,indent=2))
    print('ERRORS',len(errors),'NOTICES',len(notices),'MANUAL',len(pending_manual))
    print(json.dumps(errors[:25],ensure_ascii=False,indent=2))
    if pending_manual:print('MANUAL',json.dumps(pending_manual[:20],ensure_ascii=False))


if __name__=='__main__':run()
