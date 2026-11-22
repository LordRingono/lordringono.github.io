from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parent
SITE=ROOT.parents[1]/'output/site'
DEST=SITE.parent/'Site_revision_PASS_UE1_UE2_UE3_UE4_UE5_annales.zip'
TEMP=DEST.with_suffix('.building.zip')
MANIFEST=SITE/'audit/histologie_v5/fichiers_sha256.json'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    runtime=json.loads((ROOT/'runtime_checks/runtime_report.json').read_text())
    assert runtime['result']=='PASS'
    assert runtime['siteSHA256']==digest(SITE/'index.html'),'Site changed after final functional checks'
    quality=json.loads((ROOT/'quality/coverage.json').read_text())
    assert quality['summary']['questions']==128 and quality['summary']['items']==649
    assert quality['summary']['unknown_verdicts']==0 and quality['summary']['unexplained_item_differences']==0
    for f,sha in quality['primary_snapshot_sha256'].items():assert digest(ROOT/f)==sha
    checksums={p.relative_to(SITE).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(SITE.rglob('*')) if p.is_file() and p!=MANIFEST}
    MANIFEST.write_text(json.dumps({'revision':'V5, 22 novembre 2026','scope':'Tous les fichiers du site, sauf le présent manifeste. Les manifestes des révisions antérieures sont conservés à titre historique.','files':checksums},ensure_ascii=False,indent=2))
    files=[p for p in sorted(SITE.rglob('*')) if p.is_file()]
    with zipfile.ZipFile(TEMP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
        for p in files:archive.write(p,p.relative_to(SITE).as_posix())
    with zipfile.ZipFile(TEMP) as archive:
        assert archive.testzip() is None,'ZIP CRC failure'
        assert set(archive.namelist())=={p.relative_to(SITE).as_posix() for p in files}
        assert hashlib.sha256(archive.read('index.html')).hexdigest()==runtime['siteSHA256']
        report={'file':str(DEST),'bytes':TEMP.stat().st_size,'sha256':digest(TEMP),'entries':len(archive.infolist()),'uncompressedBytes':sum(i.file_size for i in archive.infolist()),'crcCheck':'PASS','htmlSHA256':runtime['siteSHA256'],'sourceCaptures':283,'questionsReviewed':128,'itemsReviewed':649}
    TEMP.replace(DEST)
    (ROOT/'package_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
