from pathlib import Path
import fitz,json,re,hashlib,copy,unicodedata,difflib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1];SITE=ROOT.parents[1]/'output/site'
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
FILES={
 'acc':('Sujet ACC SSH (2026-2027) PDF .pdf','Correction_ACC_SSH_2026_2027_PDF_5289830c46.pdf'),
 'colle2':('Sujet Colle 2 SSH PDF (1).pdf','Correction_Colle_2_SSH_pdf_f40e021e49.pdf'),
 'colle1':('Colle1_1_QCM_entrainement.pdf','Colle1_2_Corrections_f8abddbcba.pdf'),
 'eb':('EB blanc SSH sujet .pdf','EB_blnc_SSH_corrections_d80c585c99.pdf')}
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.lower()))
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def load(file,modern):
 d=fitz.open(file);ls=[]
 for p in d:
  for b in p.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    t=''.join(s['text'] for s in l['spans']).strip()
    if not t:continue
    if modern:
     if l['bbox'][1]>798:continue
    elif l['bbox'][1]<62 or l['bbox'][1]>782:continue
    ls.append({'page':p.number+1,'rect':list(l['bbox']),'text':t,
      'spans':[{k:s[k] for k in ('text','bbox','size','flags','color','font')} for s in l['spans']]})
 return d,sorted(ls,key=lambda x:(x['page'],round(x['rect'][1],2),x['rect'][0]))
def crop(file,ls):
 out=[]
 for p in sorted(set(x['page'] for x in ls)):
  z=[x for x in ls if x['page']==p]
  out.append({'file':str(file),'page':p,'rect':[30,min(x['rect'][1] for x in z)-3,570,max(x['rect'][3] for x in z)+3],
   'fileLabel':file.name})
 return out
def matched_items(q,ls):
 # Les sujets ACC présentent certaines lettres sous forme de glyphes non
 # extractibles ; retrouver chaque texte par sa position et ses mots, puis
 # faire contrôler les glyphes sur le PDF.
 out=[];start=0
 for op in q['options']:
  target=norm(op['text']);best=None
  for i in range(start,len(ls)):
   first=re.sub(r'^(?:[☐✔✘]\s*)?[A-E][.\-)]\s*','',ls[i]['text'])
   if not norm(first):continue
   if target[:20] not in norm(first) and norm(first)[:20] not in target:continue
   parts=[]
   for j in range(i,min(len(ls),i+10)):
    parts.append(first if j==i else ls[j]['text'])
    actual=' '.join(parts);ratio=difflib.SequenceMatcher(None,norm(actual),target).ratio()
    if best is None or ratio>best[0]:best=(ratio,i,j,actual)
    if len(norm(actual))>len(target)+40:break
  if best is not None and best[0]>.65:
   ratio,i,j,text=best;out.append({'id':op['id'],'sourceText':text,'lines':ls[i:j+1],
    'similarity':ratio,'matchStart':i,'matchEnd':j});start=j+1
  else:out.append({'id':op['id'],'sourceText':None,'lines':[],'similarity':0})
 return out

review={'banks':{k:copy.deepcopy(BASE[k]) for k in FILES}}
aud=[];crops=[];sources=[];shortgrids={}
(HERE/'readings').mkdir(parents=True,exist_ok=True)
for bank,(sf,cf) in FILES.items():
 modern=bank in ('colle1','eb')
 subject=ROOT/'materialized/ssh_individual'/sf;correction=SITE/'sources/revision_v4'/cf
 SD,SL=load(subject,modern);CD,CL=load(correction,modern)
 for role,file in [('subject',subject),('correction',correction)]:
  sources.append({'bank':bank,'role':role,'absolute':str(file),
   'packaged':'sources/revision_v6/ssh/'+re.sub(r'[^A-Za-z0-9_.-]','_',file.name) if role=='subject' else 'sources/revision_v4/'+file.name,
   'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'metadata':(SD if role=='subject' else CD).metadata})
 sr=[(i,int(m[1])) for i,l in enumerate(SL) if (m:=re.match(r'^Question (\d+)\b' if modern else r'^(\d+)\.\s',l['text']))]
 assert [n for i,n in sr]==list(range(1,len(BASE[bank]['questions'])+1)),(bank,sr)
 subj={num:SL[i:sr[z+1][0] if z+1<len(sr) else len(SL)] for z,(i,num) in enumerate(sr)}
 if modern:
  cr=[(i,int(m[1])) for i,l in enumerate(CL) if (m:=re.match(r'^Question (\d+)\b',l['text']))]
  corr={num:CL[i:cr[z+1][0] if z+1<len(cr) else len(CL)] for z,(i,num) in enumerate(cr)}
 else:
  kl=[i for i,l in enumerate(CL) if re.fullmatch(r'[A-E]{1,5}',l['text']) and l['page']>=(2 if bank=='acc' else 3)
      and (bank!='colle2' or (i+1<len(CL) and re.match(r'^A[.]\s*(?:VRAI|FAUX)',CL[i+1]['text'])))]
  assert len(kl)==len(BASE[bank]['questions']),(bank,len(kl))
  starts=[]
  for z,k in enumerate(kl):
   prev=kl[z-1] if z else -1
   gray=[i for i in range(prev+1,k) if any(s['color']==10921638 and s['text'].strip() for s in CL[i]['spans'])]
   assert gray,(bank,z)
   starts.append(gray[0])
  corr={z+1:CL[st:starts[z+1] if z+1<len(starts) else len(CL)] for z,st in enumerate(starts)}
 if bank=='colle2':
  shortgrids[bank]=dict((int(n),k) for n,k in re.findall(r'N°\s*(\d+)\s*\n\s*([A-E]+|—)\s*\n',CD[1].get_text()))
 blocks=[]
 for q in BASE[bank]['questions']:
  n=q['id'];sl=subj[n];cl=corr[n]
  si=matched_items(q,sl)
  last=max((i.get('matchEnd',0) for i in si),default=0)
  subject_body=sl[:last+1] if last else sl
  if modern:
   kr=[(i,re.sub(r'[^A-E]','',l['text'].split(':',1)[1])) for i,l in enumerate(cl) if l['text'].startswith('Bonne(s) réponse(s)')]
   assert len(kr)==1,(bank,n,kr)
   ki,key=kr[0]
   ci=[]
   marks=[(i,m[1],m[2],m[3]) for i,l in enumerate(cl[:ki]) if (m:=re.match(r'^([✔✘])\s*([A-E])[.]\s*(.*)',l['text']))]
   for z,(i,symbol,letter,first) in enumerate(marks):
    end=marks[z+1][0] if z+1<len(marks) else ki
    chunk=cl[i:end]
    it=[x for x in chunk if not any(abs(s['size']-8.6)<.05 for s in x['spans'])]
    de=[x for x in chunk if any(abs(s['size']-8.6)<.05 for s in x['spans'])]
    text=' '.join([first]+[x['text'] for x in it[1:]])
    ci.append({'id':letter,'subjectText':text,'verdict':'VRAI' if symbol=='✔' else 'FAUX',
     'detail':' '.join(x['text'] for x in de),'lines':chunk,'textLines':it,'detailLines':de})
   # Une rubrique de cours après la note appartient au prochain QCM ; ne pas
   # l'incorporer comme détail. Les commentaires orange restent authentiques.
   ce=ki+1
   for i in range(ki+1,len(cl)):
    if any(s['color'] in (11347968,11552000) for s in cl[i]['spans']):ce=i+1
    elif cl[i]['text'].startswith('⚠') or (ce>ki+1 and cl[i]['rect'][0]>=57):ce=i+1
   cor_body=cl[:max(ki+1,ce)]
  else:
   keys=[(i,l['text']) for i,l in enumerate(cl) if re.fullmatch(r'[A-E]{1,5}',l['text'])
         and (bank!='colle2' or (i+1<len(cl) and re.match(r'^A[.]\s*(?:VRAI|FAUX)',cl[i+1]['text'])))]
   assert len(keys)==1,(bank,n,keys)
   ki,key=keys[0];gray=cl[:ki];det=cl[ki+1:]
   sm=[(i,m[1],m[2]) for i,l in enumerate(gray) if (m:=re.match(r'^([A-E])[.\-)]\s*(.*)',l['text']))]
   dm=[(i,m[1],m[2]) for i,l in enumerate(det) if (m:=re.match(r'^([A-E])[.\-)]\s*(.*)',l['text']))]
   if len(sm)!=5:print('SUBJECT_MARKS',bank,n,len(sm))
   texts={letter:' '.join([txt]+[l['text'] for l in gray[i+1:sm[z+1][0] if z+1<len(sm) else len(gray)]]) for z,(i,letter,txt) in enumerate(sm)}
   details={}
   for z,(i,letter,txt) in enumerate(dm):
    part=det[i:dm[z+1][0] if z+1<len(dm) else len(det)]
    full=' '.join([txt]+[l['text'] for l in part[1:]])
    v=re.match(r'(?i)(VRAI|FAUX|V|F)\b\s*:?\s*(.*)',full)
    details[letter]={'detail':v[2] if v else full,'verdict':v[1].upper() if v else None,'lines':part}
   ci=[{'id':letter,'subjectText':texts.get(letter),'verdict':details.get(letter,{}).get('verdict'),
     'detail':details.get(letter,{}).get('detail'),'lines':details.get(letter,{}).get('lines',[])} for letter in 'ABCDE']
   cor_body=cl
  row={'bank':bank,'id':n,'subjectFile':str(subject),'correctionFile':str(correction),
   'subjectLines':subject_body,'correctionLines':cor_body,'allRawCorrectionLines':cl,
   'subjectItems':si,'correctionItems':ci,'sourceKey':key,'sourceShortKey':shortgrids.get(bank,{}).get(n),
   'siteKey':q['answer'],'subjectMatched':all(x['similarity']>=.96 for x in si),
   'keyLine':cl[ki],'originalGeneralLines':cl[ki+1:] if not modern and not dm else []}
  aud.append(row)
  crops.append({'bank':bank,'id':n,'subject':crop(subject,subject_body),'correction':crop(correction,cor_body)})
  blocks.append('\n'.join([f'{bank} Q{n} SITE {q["answer"] or "HORS NOTE"} / SOURCE {key}',
     'SUJET','\n'.join(x['text'] for x in subject_body),
     'CORRECTION','\n'.join(x['text'] for x in cor_body),
     'NOTES V5','\n'.join(x['text'] for x in q.get('reviewNotes',[])),q.get('warning','')]))
 (HERE/'readings'/f'{bank}.txt').write_text('\n\n===== QCM SUIVANT =====\n\n'.join(blocks))
dump('reviewed_initial.json',review);dump('fresh_source_audit.json',aud);dump('crops_initial.json',crops)
dump('source_manifest.json',sources);dump('short_grids.json',shortgrids)
print(json.dumps({'questions':len(aud),'items':sum(len(x['subjectItems']) for x in aud),
 'subjectTextDisagreements':[(r['bank'],r['id'],[(x['id'],round(x['similarity'],3)) for x in r['subjectItems'] if x['similarity']<.96]) for r in aud if not r['subjectMatched']],
 'keyDifferences':[(r['bank'],r['id'],r['siteKey'],r['sourceKey']) for r in aud if r['siteKey']!=r['sourceKey']]},ensure_ascii=False,indent=2))
