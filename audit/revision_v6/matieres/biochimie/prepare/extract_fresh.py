"""Fresh source text/geometry, using the old index only to locate source blocks."""
from pathlib import Path
import copy,difflib,hashlib,json,re,unicodedata
import fitz

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
WORK=ROOT.parents[1]
PDF=WORK/'output/site/sources/Annales_compilation.pdf'
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
BANKS=json.loads((ROOT/'roster.json').read_text())['biochimie']['banks']
OLD=json.loads((WORK/'work/agents/ue2/raw_questions.json').read_text())
LOC={(q['_set'],q['sourceNumber']):q for q in OLD}
D=fitz.open(PDF)
ASSETS={r['path']:r for r in json.loads((WORK/'work/agents/ue2/assets_manifest.json').read_text())}
CONTEXT=json.loads((WORK/'work/agents/ue2/context_revision.json').read_text())
def clean(t):return re.sub(r'\s+',' ',t).strip()
def norm(t):return re.sub(r'[^\w]+','',unicodedata.normalize('NFKC',t).lower())
def dump(name,data):
 (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
CACHE={}
def lines(p):
 if p not in CACHE:
  out=[]
  for block in D[p-1].get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    spans=[{k:s[k] for k in ('text','bbox','size','flags','color')} for s in line['spans']]
    text=''.join(s['text'] for s in spans).strip()
    if not text or line['bbox'][1]<60 or line['bbox'][1]>780:continue
    out.append({'page':p,'rect':list(line['bbox']),'text':text,'spans':spans})
  CACHE[p]=sorted(out,key=lambda l:(round(l['rect'][1],1),l['rect'][0]))
 return CACHE[p]
def segment(start,end):
 return [l for p in range(start['p'],end['p']+1) for l in lines(p) if not(p==start['p'] and l['rect'][1]<start['y']-.7) and not(p==end['p'] and l['rect'][1]>=end['y']-.7)]
def blocks(ls):
 labels=[(i,m[1],m[2]) for i,l in enumerate(ls) if (m:=re.match(r'^([A-E])[.)-]\s*(.*)',l['text']))]
 items=[]
 for z,(i,letter,first) in enumerate(labels):
  end=labels[z+1][0] if z+1<len(labels) else len(ls)
  items.append({'id':letter,'text':clean(' '.join([first]+[l['text'] for l in ls[i+1:end]])),'lines':ls[i:end]})
 return items
def crop_parts(s,e,ls):
 out=[]
 for p in range(s['p'],e['p']+1):
  top=s['y']-4 if p==s['p'] else 62
  bottom=e['y']-4 if p==e['p'] else 780
  if bottom-top<12 or not any(l['page']==p for l in ls):continue
  out.append({'file':str(PDF),'page':p,'rect':[0,max(0,top),D[p-1].rect.width,min(D[p-1].rect.height,bottom)],'fileLabel':'Sujets + corrections compilés.pdf'})
 return out

reviewed={'banks':{b:copy.deepcopy(BASE[b]) for b in BANKS}}
audit=[];crops=[];flags=[];readings={}
for bank in BANKS:
 for q in BASE[bank]['questions']:
  origin=LOC[q['sourceSet'],q['sourceNumber']]
  ss,se,cs,ce=[origin[k] for k in ['_start','_end','_corrStart','_corrEnd']]
  sl=segment(ss,se);cl=segment(cs,ce)
  # Original table typography: standalone A-E letters before explicit verdicts.
  candidate=[]
  for i,l in enumerate(cl):
   if re.fullmatch('[ABCDE]{1,5}',l['text']) and l['rect'][0]<150:
    candidate.append((sum(bool(re.match(r'^[ABCDE][.)-]\s*(VRAI|FAUX)',x['text'],re.I)) for x in cl[i+1:]),i,l['text']))
  key_index=max(candidate)[1] if candidate else None
  key=cl[key_index]['text'] if key_index is not None else None
  subject_items=blocks(sl)
  corrected_subject_items=blocks(cl[:key_index]) if key_index is not None else []
  details=blocks(cl[key_index+1:]) if key_index is not None else []
  # Trace the complete block; special mixed graphical rows are resolved manually.
  row={'bank':bank,'id':q['id'],'sourceSet':q['sourceSet'],'sourceNumber':q['sourceNumber'],'printedNumber':q.get('printedSourceNumber',q['sourceNumber']),'subjectStart':ss,'subjectEnd':se,'correctionStart':cs,'correctionEnd':ce,'subjectLines':sl,'correctionLines':cl,'subjectItems':subject_items,'correctedSubjectItems':corrected_subject_items,'detailItems':details,'detailKey':key,'currentKey':q['answer'],'items':[]}
  for option in q['options']:
   matching=[x for x in subject_items if x['id']==option['id']]
   corrmatch=[x for x in corrected_subject_items if x['id']==option['id']]
   det=[x for x in details if x['id']==option['id']]
   current_detail=q.get('explanations',{}).get(option['id'],'')
   item={'id':option['id'],'siteText':option['text'],'sourceText':matching[0]['text'] if matching else None,'correctedSourceText':corrmatch[0]['text'] if corrmatch else None,'siteExplanation':current_detail,'sourceExplanation':det[0]['text'] if det else None,'subjectTextEqual':bool(matching) and norm(matching[0]['text'])==norm(option['text']),'detailTextEqual':bool(det) and norm(det[0]['text'])==norm(current_detail)}
   row['items'].append(item)
   if not item['subjectTextEqual'] or not item['detailTextEqual']:flags.append({'bank':bank,'id':q['id'],**item})
  audit.append(row)
  cp={'bank':bank,'id':q['id'],'subject':crop_parts(ss,se,sl),'correction':crop_parts(cs,ce,cl),'subjectNumber':q.get('printedSourceNumber',q['sourceNumber']),'correctionNumber':q['sourceNumber']}
  crops.append(cp)
  text=[f"{bank} / ID {q['id']} / source {q['sourceNumber']} (imprimé {q.get('printedSourceNumber')}) / clé site {q['answer'] or 'HORS NOTE'} / clé détail {key}",f"SUJET p{ss['p']}:{ss['y']:.1f} → p{se['p']}:{se['y']:.1f}", '\n'.join(x['text'] for x in sl),f"CORRIGÉ p{cs['p']}:{cs['y']:.1f} → p{ce['p']}:{ce['y']:.1f}",'\n'.join(x['text'] for x in cl),'TRANSCRIPTION SITE',q['question'],json.dumps(q['options'],ensure_ascii=False),json.dumps(q.get('explanations',{}),ensure_ascii=False),json.dumps(q.get('generalExplanation'),ensure_ascii=False)]
  readings.setdefault(q['sourceSet'],[]).append('\n'.join(text))
dump('reviewed.json',reviewed);dump('fresh_source_audit.json',audit);dump('crops.json',crops);dump('comparison_flags.json',flags)
dump('source_manifest.json',[{'absolute':str(PDF),'packaged':'sources/Annales_compilation.pdf','sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()}])
(HERE/'readings').mkdir(exist_ok=True)
for name,parts in readings.items():(HERE/'readings'/f'{name}.txt').write_text('\n\n===== QUESTION SUIVANTE =====\n\n'.join(parts))
print(json.dumps({'questions':len(audit),'items':sum(len(r['items']) for r in audit),'flags':len(flags),'subjectPages':len({l['page'] for r in audit for l in r['subjectLines']}),'correctionPages':len({l['page'] for r in audit for l in r['correctionLines']})}))
