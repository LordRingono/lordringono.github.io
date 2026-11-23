from pathlib import Path
import json,re,unicodedata,fitz,difflib,collections,hashlib
ROOT=Path('/workspace/scratch/f3cb3bb97377')
OUT=ROOT/'work/site_v6/embryologie/verify'
BASE=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text())
BANKS={k:v for k,v in BASE.items() if v.get('ue')=='ue5e'}
def norm(s):
 return re.sub(r'[^a-z0-9αβγδ]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
def key(s):return ''.join(sorted(set(re.findall('[A-Z]',s or ''))))
def dump(n,o): (OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2))
FILES=list((ROOT/'work/site_v6/materialized/embryo_original').rglob('*.pdf'))
MAN={}
for b in BANKS.values():
 for q in b['questions']:
  for role in ('sourceSubject','sourceCorrection'):
   s=q.get(role)
   if s:
    m=[p for p in FILES if norm(p.name)==norm(s)]
    MAN[s]=str(m[0]) if len(m)==1 else None

def getlines(file):
 out=[]
 with fitz.open(file) as d:
  for pi,p in enumerate(d):
   for block in p.get_text('dict')['blocks']:
    for line in block.get('lines',[]):
     t=''.join(s['text'] for s in line['spans']).strip()
     if not t:continue
     if t.startswith('David Bard') or (t.isdigit() and (line['bbox'][1]<50 or line['bbox'][1]>780)):continue
     out.append(dict(page=pi+1,bbox=line['bbox'],text=t,spans=line['spans']))
 return out

def getheads(lines):
 heads=[]
 for i,x in enumerate(lines):
  t=x['text'];sp=[s for s in x['spans'] if s['text'].strip()]
  if not sp or not sp[0]['flags']&16:continue
  m=re.match(r'^Q\s*(\d{1,3})(?=\D|$)',t)
  if m and re.match(r'^Q\s*\d+\s*et\s*\d+',t):continue
  if not m: m=re.match(r'^(\d{1,3})\s*[:.\-–]\s*(?!\d)',t)
  if not m:continue
  num=int(m[1]);compact=re.match(r'^(?:Q\s*)?\d{1,3}\s*[:.\-–]\s*([A-K() ]{1,16})(?:\s*$)',t)
  if heads and heads[-1]['num']==num and compact and any(re.match('^[A-Z]\\s*[.\\-–:]',l['text']) for l in lines[heads[-1]['i']+1:i]) and not any(re.match('^20\\d\\d[\\-–]20\\d\\d',l['text']) for l in lines[heads[-1]['i']+1:i]):
   # Footer answer key belonging to a question already headed by its actual stem.
   if not heads[-1].get('answerRaw'):
    heads[-1]['answer_i']=i;heads[-1]['answerRaw']=compact[1];continue
  heads.append(dict(i=i,num=num,text=t,answerRaw=compact[1] if compact else None))
 return heads

def blocks(file):
 lines=getlines(file);heads=getheads(lines);out=[]
 for j,h in enumerate(heads):
  end=heads[j+1]['i'] if j+1<len(heads) else len(lines)
  ls=lines[h['i']:end]
  # strip year/author/end material from preceding Q
  for z,l in enumerate(ls[1:],1):
   if re.match(r'^20\d\d[–-]20\d\d',l['text']):ls=ls[:z];break
  out.append({**h,'lines':ls,'page':ls[0]['page'],'endPage':ls[-1]['page']})
 return out

def items(block, lowercase=False):
 out=collections.defaultdict(list);active=None;seg=None
 for x in block['lines'][1:]:
  t=x['text'];m=re.match(r'^([A-Za-z]{1,2})\s*[.:–\-)]\s*(.*)',t) if lowercase else re.match(r'^([A-Z])\s*[.:–\-)]\s*(.*)',t)
  if m:
   active=m[1].upper();seg={'text':m[2],'page':x['page'],'lines':[x]};out[active].append(seg)
  elif re.match(r'^(?:Q\s*)?\d{1,3}\s*[.\-–:]\s*[A-K() ]+$',t):active=None;seg=None
  elif seg is not None:
   seg['text']+=' '+t;seg['lines'].append(x)
 for letter,segs in out.items():
  for s in segs:
   s['verdicts']=[{'raw':m[0],'verdict':m[0].lower().startswith('vrai'),'offset':m.start()} for m in re.finditer(r'\b(?:vrai|faux|vraie|fausse)\b',s['text'],re.I)]
   s['colored']=[{'color':sp['color'],'text':sp['text']} for l in s['lines'] for sp in l['spans'] if sp['color'] not in (0,2829099) and sp['text'].strip()]
 return dict(out)

coverage=[];issues=[];sourceblocks={}
for bid,b in BANKS.items():
 f=MAN[b['questions'][0]['sourceCorrection']]
 bb=blocks(f);sourceblocks[bid]=bb
 # Match by source number preserving occurrence order; remapped site IDs Q30/Q33 remain stable.
 pools=collections.defaultdict(list)
 for block in bb:pools[block['num']].append(block)
 for q in b['questions']:
  num=int(q['sourceNumber']);pool=pools[num]
  if pool:block=pool.pop(0)
  else:
   coverage.append({'bank':bid,'id':q['id'],'status':'source_block_unmatched'});issues.append({'bank':bid,'id':q['id'],'kind':'source_block_unmatched'});continue
  its=items(block,bid=='embryo.aut.coeur');r={'bank':bid,'id':q['id'],'sourceNumber':num,'source':f,'page':block['page'],'endPage':block['endPage'],'head':block['text'],'sourceAnswerRaw':block['answerRaw'],'items':[]}
  if block['answerRaw'] and key(block['answerRaw'])!=key(q.get('answer','')):
   issue={'bank':bid,'id':q['id'],'kind':'answer_key_mismatch','site':q.get('answer'),'source':block['answerRaw']};issues.append(issue);r.setdefault('flags',[]).append(issue)
  for o in q['options']:
   letter=o['id'];ss=its.get(letter,[]);rn={'id':letter,'siteText':o['text'],'siteExplanation':q.get('explanations',{}).get(letter,''),'siteTrue':letter in ((q.get('answer') or '').split(',') if q.get('tokenMode') else (q.get('answer') or '')),'sourceSegments':ss}
   if not ss:
    rn['status']='option_unmatched';issues.append({'bank':bid,'id':q['id'],'item':letter,'kind':'option_unmatched'})
   else:
    st=ss[0]['text'];ns=norm(st);no=norm(o['text']);rn['statementExactPrefix']=ns.startswith(no) if no else None;rn['statementContained']=no in ns if no else None
    if not rn['statementContained']:
     rn['status']='statement_diff';issues.append({'bank':bid,'id':q['id'],'item':letter,'kind':'statement_diff','site':o['text'],'source':st})
    else:rn['status']='statement_matched_in_original'
    rawmarker=ss[0]['verdicts'][0] if ss[0]['verdicts'] else None
    # markers in original statement need avoid being interpreted as correction
    if rawmarker and norm(st[:rawmarker['offset']])==no:
     rn['sourceMarker']=rawmarker
     if rawmarker['verdict']!=rn['siteTrue']:
      issues.append({'bank':bid,'id':q['id'],'item':letter,'kind':'item_key_mismatch','site':rn['siteTrue'],'source':rawmarker['raw'],'sourceText':st})
     after=norm(st[rawmarker['offset']:]);ne=norm(rn['siteExplanation']);rn['explanationExact']=ne==after;rn['explanationContained']=ne in after or after in ne
     if not rn['explanationContained']:
      issues.append({'bank':bid,'id':q['id'],'item':letter,'kind':'explanation_diff','site':rn['siteExplanation'],'source':st[rawmarker['offset']:]})
    elif block['answerRaw']:
     rn['sourceMarker']={'raw':block['answerRaw'],'verdict':letter in block['answerRaw'],'kind':'question_key'}
    else: rn['sourceMarker']=None
   r['items'].append(rn)
  coverage.append(r)
 print(bid,'blocks',len(bb),'site',len(b['questions']),'unmatched heads',[(n,len(v)) for n,v in pools.items() if v])
dump('source_manifest.json',MAN);dump('sourceblocks.json',sourceblocks);dump('coverage_initial.json',coverage);dump('issues_initial.json',issues)
print('COVERAGE',len(coverage),'ISSUES',dict(collections.Counter(x['kind'] for x in issues)))
