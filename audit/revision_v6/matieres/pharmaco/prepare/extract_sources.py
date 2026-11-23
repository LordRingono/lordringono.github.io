import json,re,unicodedata,fitz,collections,difflib
from pathlib import Path
R=Path(__file__).resolve().parent
P=json.loads((R/'pages.json').read_text())
M=json.loads(Path('output/site/audit/UE4_manifeste.json').read_text())
BASE=json.loads(Path('work/site_v6/baseline_exams.json').read_text())
KS=json.loads(Path('work/site_v6/roster.json').read_text())['pharmaco']['banks']
QMAP={q['sourceId']:(k,q) for k in KS for q in BASE[k]['questions']}
PDF=str(Path('output/site/sources/Annales_compilation.pdf').resolve())
DOC=fitz.open(PDF)

def textnorm(x):
 x=unicodedata.normalize('NFKD',x.lower()).replace('œ','oe').replace('æ','ae').replace('≠',' non egal ').replace('≥',' superieur egal ').replace('≤',' inferieur egal ')
 return re.sub(r'[^a-z0-9<>+=%°/-]','',x)

def flatlines(pg):
 ls=[]
 for b in P[str(pg)]['dict']['blocks']:
  for l in b.get('lines',[]):
   t=''.join(s['text'] for s in l['spans']).strip()
   if t and 60<l['bbox'][1]<780:
    ls.append({'page':pg,'rect':list(l['bbox']),'text':t,'spans':l['spans']})
 # merge separate pieces with approximately same baseline (e.g. widely spaced lithium contextual sentence)
 ls=sorted(ls,key=lambda l:(round(l['rect'][1],1),l['rect'][0]))
 return ls
L={pg:flatlines(pg) for pg in range(699,987)}

def heading_candidates(start,end,numbered=None):
 lines=[x for pg in range(start,end+1) for x in L[pg]]
 heads=[]
 for i,l in enumerate(lines):
  t=l['text'];ss=[s for s in l['spans'] if s['text'].strip()]
  bold=sum(len(s['text']) for s in ss if s['flags']&16)/max(1,sum(len(s['text']) for s in ss))
  num=re.match(r'^(\d{1,2})\.\s+\S',t)
  if num and int(num[1])>0 and l['rect'][0]<90:
   heads.append({'index':i,'number':int(num[1]),'page':l['page'],'rect':l['rect'],'text':t,'kind':'printed_number'});continue
  if numbered:continue
  if l['rect'][0]<90 and bold>.72 and re.match(r'^(?:Cochez|Cocher|Concernant|Parmi|Selon|Soit|On mesure|A propos|L[’\'](?:encadrement|évaluation|observance)|Les traitements|Une étude|Quelle\(s\)|HORS PROGRAMME|Hors programme)',t):
   # do not treat line continuation "Cochez ..." after "Concernant..." as a new Q
   if heads and heads[-1]['page']==l['page'] and l['rect'][1]-heads[-1]['rect'][1]<30 and not any(re.match(r'^[A-E][.)]',x['text']) for x in lines[heads[-1]['index']:i]):
    continue
   heads.append({'index':i,'number':None,'page':l['page'],'rect':l['rect'],'text':t,'kind':'bold_heading'})
 return lines,heads

allgroups=[]
for s in M['subjects']:
 g={'year':s['year'],'session':s['session'],'ranges':{'subject':s['subjectRange'],'correction':s['correctionRange']}}
 for role in ['subject','correction']:
  lo,hi=g['ranges'][role];lo+=1 if role=='subject' else 2
  lines,h=heading_candidates(lo,hi)
  for j,hd in enumerate(h):
   hd['sequence']=j+1
  g[role]={'lines':lines,'headings':h}
 print(s['year'],s['session'],'S',len(g['subject']['headings']),'C',len(g['correction']['headings']))
 for role in ['subject','correction']:
  n=len(g[role]['headings']); target=s['subjectQuestionCount']-(1 if role=='correction' and s['year']=='2021-2022' and s['session']=='S1' else 0)
  if n!=target:print('MISMATCH',role,'expected',target,[(h['sequence'],h['page'],h['text'][:75]) for h in g[role]['headings']])
 allgroups.append(g)
(R/'groups_raw.json').write_text(json.dumps(allgroups,ensure_ascii=False,indent=2))
