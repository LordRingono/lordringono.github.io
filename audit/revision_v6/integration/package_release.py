"""Package the complete verified site, retaining its original documents."""
from pathlib import Path
import hashlib, json, shutil, zipfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent.parent/'output'
SITE=OUT/'site'
def read(p):return json.loads(Path(p).read_text())
def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

if __name__=='__main__':
    assert read(ROOT/'runtime_report.json')['result']=='PASS'
    assert read(ROOT/'integrity_report.json')['result']=='PASS'
    signoffs=read(ROOT/'signoffs.json');assert len(signoffs)==9
    for subject,row in signoffs.items():
        for key in ('reviewed','crops'):assert digest(ROOT/row[key])==row[key+'_sha256'],(subject,key)
    assert (SITE/'Verification_complete_PASS_v6.md').is_file()
    assert (SITE/'Documents_a_completer_PASS_v6.md').is_file()
    independent=read(ROOT/'integration_verify/verified_release.json')
    assert independent['indexSha256']==digest(SITE/'index.html'),'Independent approval is for a different index'
    for name,expected in independent['sourceHashes'].items():assert digest(ROOT/name)==expected,(name,'Changed after independent review')
    assert all(row['result']=='PASS' for row in independent['independentReports'].values())
    target=SITE/'audit/revision_v6/integration';target.mkdir(parents=True,exist_ok=True)
    for name in ['CONTRAT.md','AGENT_GUIDE.md','roster.json','signoffs.json','baseline_files.json','baseline_exams.json',
                 'build_site.py','source_copies.js','progress_migration.js','check_runtime.cjs','check_integrity.py',
                 'runtime_report.json','integrity_report.json','make_release_report.py','release_notes_sections.md','package_release.py']:
        shutil.copy2(ROOT/name,target/name)
    tech=ROOT/'integration_verify'
    if tech.exists():
        for source in tech.rglob('*'):
            if source.is_file() and source.suffix in ['.md','.json','.py','.js','.cjs']:
                dest=target/'independent_review'/source.relative_to(tech);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    files=sorted(p for p in SITE.rglob('*') if p.is_file())
    hash_file=SITE/'audit/revision_v6/empreintes_livraison.json'
    hashes=[{'file':p.relative_to(SITE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files if p!=hash_file]
    hash_file.write_text(json.dumps({'algorithm':'SHA-256','excludes':'audit/revision_v6/empreintes_livraison.json','files':hashes},ensure_ascii=False,indent=2))
    files=sorted(p for p in SITE.rglob('*') if p.is_file())
    groups=[('Site_revision_PASS_UE1_UE2_UE3_UE4_UE5_annales.zip',False),('Sources_originales_PASS_v6.zip',True)]
    seen=set();parts=[]
    for name,source_part in groups:
        archive=OUT/name;temporary=OUT/(archive.stem+'_writing.zip')
        selected=[p for p in files if (p.relative_to(SITE).parts[0]=='sources')==source_part]
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
            for i,p in enumerate(selected,1):
                z.write(p,p.relative_to(SITE).as_posix())
                if i%1000==0:print(f'{name} : {i}/{len(selected)} fichiers conditionnés',flush=True)
        with zipfile.ZipFile(temporary) as z:
            bad=z.testzip();assert bad is None,bad
            names=set(z.namelist());assert len(names)==len(selected) and not names&seen
            assert names=={p.relative_to(SITE).as_posix() for p in selected}
            if not source_part:assert hashlib.sha256(z.read('index.html')).hexdigest()==digest(SITE/'index.html')
            seen.update(names)
        assert temporary.stat().st_size<500_000_000,'Delivery part exceeds the chosen size ceiling'
        temporary.replace(archive)
        parts.append({'file':str(archive.resolve()),'bytes':archive.stat().st_size,'sha256':digest(archive),'files':len(selected),'zipCRC':'PASS'})
    assert seen=={p.relative_to(SITE).as_posix() for p in files}
    receipt={'parts':parts,'totalBytes':sum(p['bytes'] for p in parts),'totalFiles':len(files),
             'index_sha256':digest(SITE/'index.html'),'zipCRC':'PASS','subjectsApproved':9,
             'builtAtUTC':datetime.now(timezone.utc).isoformat()}
    (ROOT/'release_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    print(json.dumps(receipt,ensure_ascii=False,indent=2),flush=True)
