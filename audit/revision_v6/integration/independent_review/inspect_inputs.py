"""Read-only input audit. Does not build, publish, or modify approved data."""
from pathlib import Path
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
SUBJECTS=['ssh','histologie','biocell','embryologie','biomol','biochimie','chimie','biostat','pharmaco']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=read(ROOT/'baseline_exams.json')
migration_script="const fs=require('fs'),vm=require('vm');let ctx=vm.createContext({});vm.runInContext(fs.readFileSync(process.argv[1],'utf8'),ctx);console.log(JSON.stringify(vm.runInContext('V6_ITEM_REPAIRS',ctx)));"
repairs=json.loads(subprocess.check_output(['node','-e',migration_script,str(ROOT/'progress_migration.js')],text=True))
signoffs=read(ROOT/'signoffs.json') if (ROOT/'signoffs.json').exists() else {}
report={'method':'Independent comparison of V5 and latest verifier snapshots; no publication','inputs':{},'banks':0,'questions':0,'schemaChanges':[],'newQuestions':[],'missingMigrationEntries':[],'annotatedSubjects':[],'sharedAnnotatedContexts':{},'weightChanges':[],'questionIdLosses':[],'storageOrBankMetadataChanges':[],'coreHashes':{}}
for name in ('build_site.py','source_copies.js','progress_migration.js','check_runtime.cjs','check_integrity.py'):
 report['coreHashes'][name]=sha(ROOT/name)
for subject in SUBJECTS:
 directory=ROOT/subject
 p=directory/'verify/approved_reviewed.json';p=p if p.exists() else directory/'prepare/reviewed.json'
 c=directory/'verify/approved_crops.json';c=c if c.exists() else directory/'prepare/crops.json'
 if not p.exists() or not c.exists():continue
 data=read(p)['banks'];crops={(r['bank'],r['id']):r for r in read(c)}
 report['inputs'][subject]={'reviewed':str(p.relative_to(ROOT)),'reviewed_sha256':sha(p),'crops':str(c.relative_to(ROOT)),'crops_sha256':sha(c),'signedOff':subject in signoffs}
 for bank,exam in data.items():
  report['banks']+=1;report['questions']+=len(exam['questions'])
  old={q['id']:q for q in base[bank]['questions']};new={q['id']:q for q in exam['questions']}
  if not set(old)<=set(new):report['questionIdLosses'].append({'bank':bank,'ids':sorted(set(old)-set(new))})
  # Patches often contain questions only, so only explicit bank metadata counts.
  for k,v in exam.items():
   if k!='questions' and v!=base[bank].get(k):report['storageOrBankMetadataChanges'].append({'bank':bank,'field':k})
  for q in exam['questions']:
   prior=old.get(q['id']);ident={'bank':bank,'id':q['id']}
   changed=False
   if prior is None:report['newQuestions'].append(ident);changed=True
   elif [o['id'] for o in prior['options']]!=[o['id'] for o in q['options']]:
    report['schemaChanges'].append({**ident,'before':[o['id'] for o in prior['options']],'after':[o['id'] for o in q['options']]});changed=True
   if changed and str(q['id']) not in repairs.get(bank,{}):report['missingMigrationEntries'].append(ident)
   if prior and prior.get('weight',1)!=q.get('weight',1):report['weightChanges'].append(ident)
   row=crops.get((bank,q['id']),{})
   if row.get('subjectAfterCorrection') or q.get('sourceCopies',{}).get('subject',{}).get('afterCorrection'):
    report['annotatedSubjects'].append({**ident,'fromCompilation':bool(q.get('fromCompilation')),'contextRevised':bool(q.get('contextRevised'))})
   for context in q.get('sharedContexts',[]):
    if context.get('imagesAfterCorrection'):
     k=bank+'/'+context['id'];item=report['sharedAnnotatedContexts'].setdefault(k,{'bank':bank,'context':context['id'],'ids':[],'images':context.get('images',[])})
     item['ids'].append(q['id'])
report['result']='PASS' if not any(report[k] for k in ['missingMigrationEntries','weightChanges','questionIdLosses','storageOrBankMetadataChanges']) else 'FAIL'
(OUT/'input_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in report.items()},ensure_ascii=False,indent=2))
