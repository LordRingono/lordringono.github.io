from pathlib import Path
import json, re, copy, hashlib
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SITE=ROOT.parents[1]/'output/site'
PDF=SITE/'sources/Annales_compilation.pdf'
D=fitz.open(PDF)
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
BANKIDS=json.loads((ROOT/'roster.json').read_text())['biostat']['banks']
OLD=ROOT.parents[1]/'work/agents/ue3'
ASSETS={x['path']:x for x in json.loads((OLD/'assets_manifest.json').read_text())}
PROV=json.loads((OLD/'provenance.json').read_text())
LOC={(x['owner'],x['kind']):x for x in PROV if x['kind'] in ['subject_original','correction']}
MAN=json.loads((OLD/'manifest.json').read_text())
SETS={x['exam']:x for x in MAN['subjects']}
PREP={f'annales.ue3.{x["year"]}.{x["session"]}':x for x in json.loads((OLD/'prepared.json').read_text())}
CACHE={}
def lines(p):
 if p not in CACHE:
  out=[]
  for b in D[p-1].get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    text=''.join(s['text'] for s in l['spans']).strip()
    if not text or l['bbox'][1]<60 or l['bbox'][1]>780:continue
    out.append({'page':p,'rect':list(l['bbox']),'text':text,'spans':[{k:s[k] for k in ('text','bbox','size','flags','color')} for s in l['spans']]})
  CACHE[p]=sorted(out,key=lambda x:(round(x['rect'][1],1),x['rect'][0]))
 return CACHE[p]
def segment(start,end):
 return [l for p in range(start[0],end[0]+1) for l in lines(p) if not(p==start[0] and l['rect'][1]<start[1]-.7) and not(p==end[0] and l['rect'][1]>=end[1]-.7)]
def crop(start,end):
 result=[]
 for p in range(start[0],end[0]+1):
  top=max(60,start[1]-2) if p==start[0] else 62
  bottom=min(782,end[1]+1) if p==end[0] else 782
  if bottom-top<8 or not any(top-.7<=l['rect'][1]<bottom for l in lines(p)):continue
  result.append({'file':str(PDF),'page':p,'rect':[30,top,570,bottom],'fileLabel':'Sujets + corrections compilés.pdf'})
 return result
def items(ls):
 marks=[(i,m[1],m[2]) for i,l in enumerate(ls) if (m:=re.match(r'^([A-E])[.\-)]\s*(.*)',l['text']))]
 result=[]
 for z,(i,k,txt) in enumerate(marks):
  e=marks[z+1][0] if z+1<len(marks) else len(ls)
  result.append({'id':k,'text':' '.join([txt]+[x['text'] for x in ls[i+1:e]]),'lines':ls[i:e]})
 return result
def merge(panels):
 out=[]
 for x in sorted(panels,key=lambda x:(x['page'],x['rect'][1])):
  if out and out[-1]['page']==x['page'] and x['rect'][1]<=out[-1]['rect'][3]+2:
   out[-1]['rect']=[min(out[-1]['rect'][0],x['rect'][0]),min(out[-1]['rect'][1],x['rect'][1]),max(out[-1]['rect'][2],x['rect'][2]),max(out[-1]['rect'][3],x['rect'][3])]
  else:out.append(copy.deepcopy(x))
 return out
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
review={'banks':{b:copy.deepcopy(BASE[b]) for b in BANKIDS}}
audit=[];crops=[];readings={};gridrows=[]
for bank in BANKIDS:
 info=SETS[bank];prepared={x['num']:x for x in PREP[bank]['prepared']}
 short=dict((int(n),key) for n,key in re.findall(r'N°\s*(\d+)\s*\n\s*([ABCDE]+|HP|/|—)\s*\n',D[info['shortKeyPage']-1].get_text()))
 previous=[info['correctionCover']+2,62]
 for q in BASE[bank]['questions']:
  owner=f'{bank}:{q["id"]}';sloc=LOC[owner,'subject_original'];cloc=LOC[owner,'correction'];pp=prepared[q['id']]
  # A previous detail end is the next exercise's prefix boundary, never reused as its answer.
  fullcorr=segment(previous,cloc['end']);detail=segment(cloc['start'],cloc['end'])
  direct=segment(sloc['start'],sloc['end']);fullsub=segment(pp['prefixstart'],pp['endpoint'])
  sourcepanels=crop(pp['prefixstart'],pp['endpoint'])
  context_sources=[]
  for context in q.get('sharedContexts',[]):context_sources.extend(context.get('images',[]))
  context_sources.extend(q.get('stemImages',[]));context_sources.extend(q.get('images',[]))
  for src in context_sources:
   a=ASSETS[src]
   sourcepanels.append({'file':str(PDF),'page':a['page'],'rect':list(a['bbox']),'fileLabel':'Sujets + corrections compilés.pdf'})
  subject=merge(sourcepanels)
  correction=crop(previous,cloc['end'])
  # Collect fresh context text as well as coordinates; visual/math copy remains authoritative.
  ctx=[]
  for src in context_sources:
   a=ASSETS[src];ctx.append({'src':src,'page':a['page'],'rect':a['bbox'],'text':D[a['page']-1].get_textbox(fitz.Rect(a['bbox']))})
  key_lines=[x['text'] for x in detail if re.fullmatch(r'[A-E]{1,5}',x['text'])]
  row={'bank':bank,'id':q['id'],'sourceNumber':q['sourceNumber'],'subjectLocation':sloc,'correctionLocation':cloc,'fullCorrectionStart':previous,'subjectLines':direct,'prefixLines':fullsub,'correctionLines':fullcorr,'detailLines':detail,'subjectItems':items(direct),'detailItems':items(detail),'sharedContexts':ctx,'sourceShortKey':short.get(q['id']),'sourceDetailKeyCandidates':key_lines,'siteKey':q['answer']}
  audit.append(row);gridrows.append({k:row[k] for k in ['bank','id','sourceShortKey','sourceDetailKeyCandidates','siteKey']})
  crops.append({'bank':bank,'id':q['id'],'subject':subject,'correction':correction,'subjectNumber':q['sourceNumber'],'correctionNumber':q['sourceNumber']})
  previous=cloc['end']
  readings.setdefault(bank,[]).append('\n'.join([f'{bank} Q{q["id"]} · SITE={q["answer"] or "HORS NOTE"} · GRILLE={short.get(q["id"])} · DÉTAIL={key_lines}', 'CONTEXTE(S) PARTAGÉ(S)', '\n'.join(x['text'] for x in ctx),'SUJET ORIGINAL','\n'.join(x['text'] for x in fullsub),'CORRIGÉ ORIGINAL','\n'.join(x['text'] for x in fullcorr),'NOTES EXISTANTES','\n'.join(x['text'] for x in q.get('reviewNotes',[]))]))
dump('reviewed.json',review);dump('crops.json',crops);dump('fresh_source_audit.json',audit);dump('grids.json',gridrows)
dump('source_manifest.json',[{'absolute':str(PDF),'packaged':'sources/Annales_compilation.pdf','sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()}])
for name,r in readings.items():(HERE/'readings'/f'{name}.txt').write_text('\n\n===== QUESTION SUIVANTE =====\n\n'.join(r))
print(json.dumps({'questions':len(audit),'items':sum(len(x['subjectItems']) for x in audit),'sourcePages':len({x['page'] for r in audit for x in r['prefixLines']}),'correctionPages':len({x['page'] for r in audit for x in r['correctionLines']}),'keyDisagreements':[x for x in gridrows if x['siteKey']!=x['sourceShortKey']]}))
