"""Independent structural/provenance audit of the common-statement revision."""
from pathlib import Path
import json,hashlib,re,collections
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'work'
SITE=ROOT/'output/site'
def read(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

base=read(WORK/'base_exams.json')
old_added=read(WORK/'context_revision_v2/added_v1.json')
added=read(WORK/'added_exams.json')
ed=read(WORK/'context_revision_v2/overrides_applied.json')
all_revised={**added,**ed}
ED_KEY_REPAIRS={6:('', 'C'),7:('A','B'),8:('','BC'),13:('','BD')}
errors=[];notices=[];groups={};changed=collections.Counter();items_changed=collections.Counter()
image_count=0;image_paths=set();sources={};manifest={}
for folder in ['ue2','ue3','ue4','biomol_ed']:
    data=read(WORK/'agents'/folder/'assets_manifest.json')
    if isinstance(data,dict):data=data.get('assets',data.get('images',list(data.values())))
    for m in data:manifest[m.get('path') or m.get('file')]=m

for key,exam in all_revised.items():
    old=(base if key in ed else old_added)[key]
    unit='biomol_ed' if key in ed else exam['ue']
    if exam['storage']!=old['storage']:errors.append([key,'storage changed'])
    if len(exam['questions'])!=len(old['questions']):errors.append([key,'question count changed'])
    for q,before in zip(exam['questions'],old['questions']):
        ref=[key,q['id']]
        if q!=before:changed[unit]+=1
        for field in ['id','answer','answerIsEmpty','weight','tokenMode','ignoredOptions']:
            if key=='ue2.ed.annales' and field=='answer' and q['id'] in ED_KEY_REPAIRS:
                if (before.get(field),q.get(field))!=ED_KEY_REPAIRS[q['id']]:errors.append(ref+['documented key repair mismatch'])
                continue
            if q.get(field)!=before.get(field):errors.append(ref+['scoring identity changed',field])
        for o,old_o in zip(q['options'],before['options']):
            if o['id']!=old_o['id']:errors.append(ref+['option id changed'])
            if o!=old_o:items_changed[unit]+=1
            text=o.get('text','')
            # These markers are structural, not scientific claims about truth.
            if re.search(r'\b(?:Énoncé commun aux|Questions? suivantes?\s*:|Correction détaillée|Réponses attendues\s*:)',text,re.I):
                errors.append(ref+['foreign statement marker in option',o['id'],text[:160]])
            if key=='ue2.ed.annales' and o['id']=='E' and q['id'] in [7,9,13,16,20,23,28,33,38,43]:
                if re.search(r'\s'+str(q['subjectPage'])+r'$',text):errors.append(ref+['source folio remains inside item E'])
        local_images=set(q.get('images',[])+q.get('stemImages',[]))
        group_ids=set()
        for c in q.get('sharedContexts',[]):
            cid=c.get('id');gid=(unit,cid)
            if not cid or cid in group_ids:errors.append(ref+['missing/duplicate context id',cid])
            group_ids.add(cid)
            if not c.get('text','').strip() and not c.get('images'):errors.append(ref+['empty context',cid])
            if c.get('questionIds') and q['id'] not in c['questionIds']:errors.append(ref+['context question id membership',cid])
            if c.get('questionNumbers') and str(q.get('sourceNumber')) not in [str(n) for n in c['questionNumbers']]:errors.append(ref+['context source number membership',cid])
            if gid not in groups:groups[gid]={'unit':unit,'id':cid,'data':c,'members':[]}
            elif groups[gid]['data']!=c:errors.append(ref+['context data differ across members',cid])
            groups[gid]['members'].append({'bank':key,'id':q['id'],'sourceNumber':q.get('sourceNumber')})
            if local_images.intersection(c.get('images',[])):errors.append(ref+['context image duplicated inside card',cid])
            pdf=c.get('sourcePdf') or q.get('sourcePdf') or ('sources/Annales_compilation.pdf' if q.get('fromCompilation') else '')
            if not pdf or not (SITE/pdf).is_file():errors.append(ref+['context source PDF missing',cid,pdf])
            else:
                if pdf not in sources:
                    doc=fitz.open(SITE/pdf);sources[pdf]={'pages':len(doc),'sha256':digest(SITE/pdf)};doc.close()
                first=c.get('sourceStartPage');last=c.get('sourceEndPage') or first
                if not isinstance(first,int) or not isinstance(last,int) or not 1<=first<=last<=sources[pdf]['pages']:errors.append(ref+['context pages invalid',cid,first,last])
            if c.get('text') and len(c['text'])>100:
                norm=lambda s:re.sub(r'\s+',' ',s).strip()
                for o in q['options']:
                    if norm(c['text']) in norm(o.get('text','')):errors.append(ref+['complete common text remains in option',o['id']])
            for link in c.get('images',[]):
                m=manifest.get(link,{})
                if m.get('role')!='subject':errors.append(ref+['shared image not from subject',cid,link])
                if m.get('sourcePdf') and m['sourcePdf']!=pdf:errors.append(ref+['shared image source mismatch',cid,link])
                if c.get('sourceStartPage') and m.get('page') and not c['sourceStartPage']<=m['page']<=(c.get('sourceEndPage') or c['sourceStartPage']):errors.append(ref+['shared image outside context page range',cid,link])
        if key in ed:
            # Newly moved references and ED panels must be clean, and every path
            # must be backed by the source manifest, including reused assets.
            panels=[(field,q.get(field,[])) for field in ['images','stemImages','originalImages','correctionImages']]
            panels += [('sharedContexts',c.get('images',[])) for c in q.get('sharedContexts',[])]
            panels += [('references',r.get('images',[])) for r in q.get('references',[])]
            panels += [('option',[o['image']]) for o in q['options'] if o.get('image')]
            for field,paths in panels:
                for link in paths:
                    image_count+=1
                    if not (SITE/link).is_file():errors.append(ref+['ED image missing',link]);continue
                    m=manifest.get(link)
                    if not m:errors.append(ref+['ED image provenance missing',field,link]);continue
                    role='correction' if field=='correctionImages' else 'subject'
                    if m.get('role')!=role:errors.append(ref+['ED image source role wrong',field,link,m.get('role')])
                    if m.get('sha256') and digest(SITE/link)!=m['sha256']:errors.append(ref+['ED image checksum differs',link])
                    if link not in image_paths:
                        try:Image.open(SITE/link).verify()
                        except Exception as ex:errors.append(ref+['ED image corrupted',link,str(ex)])
                        image_paths.add(link)

# The previous release's scientific images cannot silently change under the
# same name: replacements must use a new, auditable path.
prior=read(WORK/'context_revision_v2/files_v1.json')
if 'files' in prior:prior=prior['files']
preserved_images=0
for relative,info in prior.items():
    if not relative.startswith('static/') or not (SITE/relative).exists():continue
    expected=info.get('sha256') if isinstance(info,dict) else info
    if digest(SITE/relative)!=expected:errors.append(['existing image content changed',relative])
    preserved_images+=1

counts=collections.Counter(g['unit'] for g in groups.values())
members=collections.defaultdict(set)
for g in groups.values():
    for m in g['members']:members[g['unit']].add((m['bank'],m['id']))
report={'result':'PASS' if not errors else 'FAIL','changed_questions':dict(changed),'changed_options':dict(items_changed),'common_groups':dict(counts),'questions_with_common_context':{u:len(v) for u,v in members.items()},'ED_key_repairs':ED_KEY_REPAIRS,'ED_key_repairs_verified_against':'biomol_ed_annales_corrige.pdf pages 3, 4, 6, texte et rendu des pages vérifiés indépendamment','ED_image_references_checked':image_count,'ED_unique_images_decoded':len(image_paths),'previous_images_preserved':preserved_images,'source_pdfs':sources,'errors':errors,'notices':notices,'groups':list(groups.values())}
(WORK/'review/context_revision_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['groups','source_pdfs']},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
