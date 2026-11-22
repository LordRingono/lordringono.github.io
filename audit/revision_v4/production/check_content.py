"""Validate deliverable references and the source-backed repair inventory."""
import json,re,collections,hashlib
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'work/review_v4';SITE=ROOT/'output/site'
E=json.loads((P/'current_exams.json').read_text())
N=json.loads((SITE/'audit/revision_v4/annotations.json').read_text())
changes=json.loads((SITE/'audit/revision_v4/reparations.json').read_text())
additions=json.loads((SITE/'audit/revision_v4/ajouts.json').read_text())
files=collections.defaultdict(list)
def visit(v,where):
 if isinstance(v,dict):
  for k,x in v.items():visit(x,where+'.'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):visit(x,where+'['+str(i)+']')
 elif isinstance(v,str) and v.startswith(('static/','sources/')):
  file=v.split('#',1)[0];files[file].append(where)
for b,e in E.items():visit(e,b)
proof_refs=[]
for i,r in enumerate(changes):
 proof=r.get('proof')or[]
 if isinstance(proof,dict):proof=[proof]
 for ref in proof:proof_refs.append(ref);visit(ref,'repair['+str(i)+'].proof')
for i,r in enumerate(additions):
 for ref in r.get('refs',[]):proof_refs.append(ref);visit(ref,'addition['+str(i)+'].proof')
missing=[];bad_images=[];images=0;pdfs={};pages_checked=0;bad_pages=[]
for file,uses in files.items():
 p=SITE/file
 if not p.is_file():missing.append({'file':file,'uses':uses});continue
 if p.suffix.lower()in {'.png','.jpg','.jpeg','.webp','.gif'}:
  try:
   with Image.open(p)as im:im.verify()
   images+=1
  except Exception as exc:bad_images.append({'file':file,'error':str(exc)})
 if p.suffix.lower()=='.pdf':
  with fitz.open(p)as doc:pdfs[file]=len(doc)
for n in N:
 for r in n.get('refs',[]):
  href=r.get('href','');file=href.split('#',1)[0]
  if file in pdfs:
   page=r.get('page',1);pages_checked+=1
   if not isinstance(page,int)or not(1<=page<=pdfs[file]):bad_pages.append({'note':n['noteId'],'file':file,'page':page,'pageCount':pdfs[file]})
proof_pages=0
for r in proof_refs:
 file=r.get('href','').split('#',1)[0]
 if file in pdfs:
  page=r.get('page')or 1;proof_pages+=1
  if not isinstance(page,int)or not(1<=page<=pdfs[file]):bad_pages.append({'proof':True,'file':file,'page':page,'pageCount':pdfs[file]})
note_ids=[n['noteId']for n in N];duplicate_notes=[k for k,v in collections.Counter(note_ids).items()if v>1]
stats={'questionCount':sum(len(e['questions'])for e in E.values()),'references':len(files),'imagesVerified':images,'pdfsOpened':len(pdfs),'noteReferencePagesChecked':pages_checked,'proofReferencePagesChecked':proof_pages,'missingFiles':missing,'invalidImages':bad_images,'invalidReferencePages':bad_pages,'duplicateNoteIds':duplicate_notes}
(P/'content_checks.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps(stats,ensure_ascii=False,indent=2))
assert not missing and not bad_images and not bad_pages and not duplicate_notes
