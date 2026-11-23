"""Verify assembled data against the nine signed snapshots and installed originals."""
from pathlib import Path
import copy,hashlib,json
import fitz

ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT.parent.parent/'output/site'
OUT=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
html=(SITE/'index.html').read_text()
assert 'const V6_ITEM_REPAIRS=' in html,'Wait for the authorized V6 build'
start=html.index('const EXAMS=')+len('const EXAMS=')
release=json.JSONDecoder().raw_decode(html[start:])[0]
assert release==read(ROOT/'current_exams.json'),'Embedded data and integrity-check data differ'
signoffs=read(ROOT/'signoffs.json')
assert len(signoffs)==9
allowed={'sourceCopies','sourceQuestionNumber','sourceSubject','sourceCorrection','subjectPage','sourceStartPage','sourceEndPage','approximateDocxPage','sourcePdf','correctionPage','correctionEndPage','correctionPdf'}
documents=read(SITE/'audit/revision_v6/documents.json')
by_input={str(Path(d['input']).resolve()):d for d in documents}
expected_captures=[]
report={'method':'Exact comparison of embedded release data with nine SHA256-bound signed snapshots; SHA256 comparison of all installed source documents; exact crop-metadata comparison and page-bound checks','siteSha256':sha(SITE/'index.html'),'subjects':0,'banks':0,'questions':0,'notes':0,'sourceCopiesChecked':0,'documentPageLabelsChecked':0,'multiDocumentCopies':0,'captureMetadataChecked':0,'cropBoundsChecked':0,'sourceDocuments':0,'originalsChecked':[],'result':'RUNNING'}
for subject,signoff in signoffs.items():
 p=ROOT/signoff['reviewed'];assert sha(p)==signoff['reviewed_sha256']
 c=ROOT/signoff['crops'];assert sha(c)==signoff['crops_sha256']
 crop_rows={(row['bank'],row['id']):row for row in read(c)}
 report['subjects']+=1
 for bank,exam in read(p)['banks'].items():
  report['banks']+=1
  actual_questions=release[bank]['questions']
  assert [q['id'] for q in actual_questions]==[q['id'] for q in exam['questions']],(bank,'question order/IDs')
  for before,actual in zip(exam['questions'],actual_questions):
   report['questions']+=1
   crop=crop_rows[(bank,before['id'])]
   if crop.get('reuseExisting'):
    assert actual['sourceCopies']==before['sourceCopies'],(bank,before['id'],'reused source copies changed')
    report['sourceCopiesChecked']+=2
   else:
    for role in ('subject','correction'):
     parts=crop.get(role,[]);copy_meta=actual['sourceCopies'][role]
     report['sourceCopiesChecked']+=1
     if not parts:
      assert copy_meta.get('missing') is True and copy_meta['captures']==[],(bank,before['id'],role,'missing source metadata')
      assert copy_meta['reason']==str(crop[role+'Missing'])
      continue
     assert bool(copy_meta.get('afterCorrection'))==bool(crop.get(role+'AfterCorrection')),(bank,before['id'],role,'annotation gate changed')
     assert bool(copy_meta.get('mismatch'))==bool(crop.get(role+'Mismatch')),(bank,before['id'],role,'source mismatch flag changed')
     assert copy_meta.get('note')==(crop.get(role+'Note') or None),(bank,before['id'],role,'source note changed')
     assert len(copy_meta['captures'])==len(parts),(bank,before['id'],role,'source capture count')
     displayed_documents=copy_meta.get('documents') or [copy_meta]
     if len(displayed_documents)>1:report['multiDocumentCopies']+=1
     assert {d['pdf'] for d in displayed_documents}=={cap['pdf'] for cap in copy_meta['captures']},(bank,before['id'],role,'document list mismatch')
     for doc in displayed_documents:
      doc_captures=[cap for cap in copy_meta['captures'] if cap['pdf']==doc['pdf']]
      pages=sorted({cap['page'] for cap in doc_captures})
      if len(displayed_documents)>1:assert doc['pages']==pages,(bank,before['id'],role,'pages mixed between documents')
      assert doc['firstPage'] in pages,(bank,before['id'],role,'invalid first page')
      assert all(cap['file']==doc['file'] for cap in doc_captures),(bank,before['id'],role,'capture/document label mismatch')
      if doc['pdf']=='sources/Annales_compilation.pdf':assert doc['file']=='Annales_compilation.pdf',(bank,before['id'],role,'compilation filename')
      report['documentPageLabelsChecked']+=1
     for number,(part,capture) in enumerate(zip(parts,copy_meta['captures']),1):
      original=Path(part['file']);original=original.resolve() if original.is_absolute() else (ROOT.parent.parent/original).resolve()
      document=by_input[str(original)]
      page=int(part['page']);rect=[round(float(v),4) for v in part['rect']]
      identity=json.dumps([document['sha256'],page,rect],separators=(',',':'))
      src='static/revision_v6/'+hashlib.sha256(identity.encode()).hexdigest()[:24]+'.webp'
      assert capture['src']==src and capture['pdf']==document['path'] and capture['page']==page,(bank,before['id'],role,number,'wrong crop association')
      expected_captures.append({'bank':bank,'id':before['id'],'role':role,'part':number,'source':document['path'],'src':src,'page':page,'rect':rect})
   expected=copy.deepcopy(before);found=copy.deepcopy(actual)
   for key in allowed:expected.pop(key,None);found.pop(key,None)
   expected_notes=expected.get('reviewNotes',[]);actual_notes=found.get('reviewNotes',[])
   assert len(expected_notes)==len(actual_notes),(bank,before['id'],'notes count')
   for old,note in zip(expected_notes,actual_notes):
    report['notes']+=1
    for field in ('reviewedItemText','reviewedExplanation'):
     if field in old:
      if field=='reviewedItemText':required={o['id']:o['text'] for o in actual['options'] if o['id'] in note.get('items',[])}
      else:required={letter:actual.get('explanations',{}).get(letter,'') for letter in note.get('items',[])}
      assert note.get(field)==required,(bank,before['id'],field)
      old.pop(field);note.pop(field)
    for prior_ref,ref in zip(old.get('refs',[]),note.get('refs',[])):
     if not prior_ref.get('href') and not prior_ref.get('url'):ref.pop('href',None)
   assert expected==found,(bank,before['id'],'approved semantic content was modified')
for doc in documents:
 installed=SITE/doc['path'];digest=sha(installed)
 assert digest==doc['sha256'],(doc['path'],'installed original checksum')
 assert digest==sha(doc['input']),(doc['path'],'input original checksum')
 report['sourceDocuments']+=1
 report['originalsChecked'].append({'file':doc['path'],'sha256':digest})
manifest=read(SITE/'audit/revision_v6/captures.json')
sort_capture=lambda c:(c['bank'],c['id'],c['role'],c['part'])
assert sorted(manifest,key=sort_capture)==sorted(expected_captures,key=sort_capture),'Actual capture manifest differs from approved rectangles'
report['captureMetadataChecked']=len(manifest)
by_document={}
for item in manifest:by_document.setdefault(item['source'],[]).append(item)
for source,items in by_document.items():
 with fitz.open(SITE/source) as document:
  for item in items:
   assert 1<=item['page']<=len(document),item
   rect=fitz.Rect(item['rect']);page=document[item['page']-1]
   assert rect.width>0 and rect.height>0 and (page.rect+(-.1,-.1,.1,.1)).contains(rect),item
   report['cropBoundsChecked']+=1
report['result']='PASS'
(OUT/'release_comparison_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in report.items()},ensure_ascii=False,indent=2))
