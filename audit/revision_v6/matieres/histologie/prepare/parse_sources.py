import json,re,pathlib,unicodedata,difflib,copy
ROOT=pathlib.Path('/workspace/scratch/f3cb3bb97377'); OUT=ROOT/'work/site_v6/histologie/prepare'; BASE=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text())
NAMES={
 'histo.ann.te':('Annales_Tissu_epithelial_NON_corrige_2020_2026_cd39b0a2e7','Annales_Tissu_Epithelial_2020_2026_CORRECTION_1e6bf3af86'),
 'histo.ann.tc':('annales_TISSU_CONJONCTIF_2020_2025_1db02487eb','annales_TISSU_CONJONCTIF_2020_2025_CORRECTION_2_15a22929d2'),
 'histo.ann.tn':('annales_TISSU_NERVEUX_2018_2025_16377b30d2','annales_TISSU_NERVEUX_2018_2025_CORRECTION_25bc666fc1'),
 'histo.ann.tech':('ANNALES_Techniques_2019_2026_NON_CORRIGEES_3cb51b54da','ANNALES_Techniques_2019_2026_CORRECTION_580d7a5282')}
for suffix in ['te1','te2','tc1','tc2','tc3','tn1','tn2','tn3','autotech']:NAMES['histo.'+suffix]=(suffix+'_subject',suffix+'_correction')
def norm(s):
 s=unicodedata.normalize('NFKD',s.replace('œ','oe').replace('ﬁ','fi').replace('ﬂ','fl')).lower()
 return re.sub(r'[^a-z0-9]','',s)
def text(ls):return re.sub(r'\s+',' ',' '.join(l['text'].strip() for l in ls)).strip()
def headers(t,bank):
 if re.match(r'^QUESTION \d+ à QUESTION',t):return False
 if re.match(r'^(?:QR[MU]|QCM|Question|QUESTION)\s*\d+\b',t):return True
 if re.match(r'^\d{1,2}\.?(?:\s+(?:Concernant|Parmi|La cellule|Un étudiant|Une coloration|Après une|En microscopie|Les images|QCM|Histologie|A propos)\b|\s*$)',t):return True
 if bank=='histo.ann.tech' and (t=='22.' or t.startswith(('Concernant la figure 8','À propos de l’hybridation','Pour utiliser une méthode indirecte','Si on compare la coupe'))):return True
 return False
def cleanline(l,pg):
 t=l['text'].strip();y=l['rect'][1]
 return not(t.startswith(('/3EMSLB_','EMSLB_','L. Bastin','C.ROCHET','C. Rochet')) or (y>780 and t.isdigit()))
def opt(t):
 m=re.match(r'^([A-J])\s*([.\-–):])\s*(.*)',t)
 if not m:m=re.match(r'^([A-E])\s+(?=(?:dans le processus|la |le |les |Le |La |L[’\']|Il |Elle ))(.*)',t)
 return m.group(1) if m else None

def mergelines(lines):
 groups=[]
 for l in sorted(lines,key=lambda l:(l['rect'][1],l['rect'][0])):
  if groups and abs(groups[-1][0]['rect'][1]-l['rect'][1])<2:groups[-1].append(l)
  else:groups.append([l])
 out=[]
 for g in groups:
  g=sorted(g,key=lambda l:l['rect'][0]);r=[min(x['rect'][0] for x in g),min(x['rect'][1] for x in g),max(x['rect'][2] for x in g),max(x['rect'][3] for x in g)]
  out.append({'text':' '.join(x['text'].strip() for x in g),'rect':r,'spans':sum([x['spans'] for x in g],[])})
 return out

def parse(bank,name):
 pages=json.loads((OUT/'text'/(name+'.json')).read_text());ls=[]
 for pg in pages:
  for l in mergelines(pg['lines']):
   if cleanline(l,pg):ls.append(dict(l,page=pg['page']))
 hs=[i for i,l in enumerate(ls) if headers(l['text'].strip(),bank)]
 if not bank.startswith('histo.ann'):
  hs=[i for i,l in enumerate(ls) if headers(l['text'].strip(),bank) or re.match(r'^\d{1,2}\s*[):]\s*',l['text'].strip())]
 qs=[]
 for n,start in enumerate(hs):
  chunk=ls[start:hs[n+1] if n+1<len(hs) else len(ls)]; inds=[(i,opt(l['text'].strip())) for i,l in enumerate(chunk) if opt(l['text'].strip())]
  # Keep only real A->E runs; very occasionally PDF extracts label and text separately.
  ordered=[]; expect=inds[0][1] if inds else 'A'
  for i,k in inds:
   if k==expect or (bank=='histo.autotech' and len(qs)==6 and len(ordered)==3 and k=='A') or (bank=='histo.autotech' and len(qs)==6 and len(ordered)==4 and k=='D'):
    ordered.append((i,chr(ord(inds[0][1])+len(ordered))));expect=chr(ord(ordered[-1][1])+1)
  options={k:chunk[i:ordered[j+1][0] if j+1<len(ordered) else len(chunk)] for j,(i,k) in enumerate(ordered)}
  stem=chunk[:ordered[0][0]] if ordered else chunk
  qs.append({'index':n+1,'page':chunk[0]['page'],'rect':chunk[0]['rect'],'stem':text(stem),'stemLines':stem,'options':{k:text(v) for k,v in options.items()},'itemLines':options,'lines':chunk})
 return qs
if __name__=='__main__':
 parsed={};matches={}
 for bank,names in NAMES.items():
  parsed[bank]={};matches[bank]={}
  for role,name in zip(['subject','correction'],names):
   qs=parse(bank,name);parsed[bank][role]=qs
   available=set(range(len(qs)));maps=[]
   for q in BASE[bank]['questions']:
    btxt=' '.join(o['text'] for o in q['options'])
    scores=[]
    for i,p in enumerate(qs):
     # Similarity of A plus full option text; corrections add explanations.
     ratios=[]
     for o in q['options']:
      raw=p['options'].get(o['id'],'');raw=re.sub(r'^[A-I]\s*[.\-–):]?\s*','',raw)
      if role=='correction':raw=re.split(r'\b(?:vrai|faux)\b',raw,flags=re.I)[0]
      a,b=norm(o['text']),norm(raw)
      ratios.append(difflib.SequenceMatcher(None,a,b).ratio())
     score=sum(ratios)/len(ratios) if ratios else 0
     scores.append((score,i,ratios))
    score,i,ratios=max(scores,default=(0,-1,[])); maps.append({'id':q['id'],'sourceIndex':i+1,'score':round(score,3),'ratios':[round(z,3) for z in ratios]})
   matches[bank][role]=maps
   bad=[(m['id'],m['sourceIndex'],m['score']) for m in maps if m['score']<0.90]
   print(bank,role,'parsed',len(qs),'base',len(BASE[bank]['questions']),'low',bad)
 (OUT/'parsed_sources.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2));(OUT/'source_matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2))
