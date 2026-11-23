import json,pathlib,re,fitz,copy,collections
P=pathlib.Path(__file__).parent;B=json.load(open(P/'reviewed.json'))['banks'];S=json.load(open(P/'segments.json'));A=json.load(open(P/'assignments.json'));M=json.load(open(P/'source_manifest.json'));E=json.load(open(P/'extraction.json'))
GROUPS={'embryo.aut.coeur':[(5,6)],'embryo.aut.s4':[(23,24)],'embryo.col.s3':[(25,26),(31,32),(41,42)],'embryo.col.s4':[(29,30),(35,36),(44,45),(54,55),(68,69)]}
def asg(bank,id,role):return next((a for a in A[bank] if a['id']==id and a['role']==role and a['status']=='linked'),None)
def cleanlines(lines):
 result=[]
 for l in lines:
  t=l['text']
  if re.match(r'^20\d\d[-–]',t) or re.match(r'^(?:Ce schéma|Les (?:2 )?questions|Questions \d|Q\s*\d+\s*et\s*\d)',t,re.I):
   # A shared header at the actual segment start is part of this question.
   if not result: result.append(l);continue
   break
  result.append(l)
 return result or lines

def role_data(bank,q,role):
 a=asg(bank,q['id'],role)
 if a:return a['source'],S[a['source']][a['segmentIndex']],False
 if role=='subject':
  a=asg(bank,q['id'],'correction');s=S[a['source']][a['segmentIndex']]
  if s.get('subjectPart'):return a['source'],s['subjectPart'],True
 return None,None,False

def bounds(name,lines):
 lines=cleanlines(lines);start=(lines[0]['page'],lines[0]['bbox'][1]);end=(lines[-1]['page'],lines[-1]['bbox'][3]);crops=[]
 # Include entire source panel, with its image height, stopping before the next question/header.
 for pi in range(start[0],end[0]+1):
  p=E[name][pi-1];ylow=max(15,start[1]-4) if pi==start[0] else 15
  high=min(p['height']-30,end[1]+5) if pi==end[0] else p['height']-30
  # Bitmap image often extends farther down than its adjoining option text.
  doc=DOCS.setdefault(name,fitz.open(M[name]['file']));page=doc[pi-1]
  nextheads=[s['y'] for s in S[name] if s['page']==pi and s['y']>high-1]
  nextbound=min(nextheads)-3 if nextheads else p['height']-30
  for im in page.get_image_info():
   x0,y0,x1,y1=im['bbox']
   if y0<high and y1>ylow and y1<=nextbound+2:high=max(high,y1+4)
  if high<=ylow:continue
  crops.append({'file':M[name]['file'],'page':pi,'rect':[24,round(ylow,2),round(p['width']-20,2),round(min(high,p['height']-28),2)]})
 return crops
DOCS={};rows=[]
for bank,b in B.items():
 for q in b['questions']:
  row={'bank':bank,'id':q['id'],'subject':[],'correction':[]}
  for role in ['subject','correction']:
   name,s,mixed=role_data(bank,q,role)
   if not s:
    row[role+'Missing']='Aucune version non corrigée de ce QCM n’est présente dans les PDF thématiques disponibles. Le texte a pu être confronté au corrigé ; la copie du corrigé reste accessible seulement après correction.' if role=='subject' else 'Corrigé original non retrouvé.';continue
   lines=s['lines'];note=[]
   if mixed:note.append('Sujet non annoté reproduit depuis la partie énoncé du document mixte ; la correction qui suit est exclue de cette copie.')
   group=next((g for g in GROUPS.get(bank,[]) if q['id'] in g),None)
   if group:
    pair=[next(z for z in b['questions'] if z['id']==i) for i in group];ps=[role_data(bank,z,role)[1] for z in pair]
    all_lines=[]
    for z in ps:
     if z:all_lines+=z['lines']
    if all_lines:
     # Locate shared introductory line between the previous item and first paired QCM.
     first=min((l['page'],l['bbox'][1]) for l in all_lines);earlier=[]
     for p in E[name]:
      for l in p['lines']:
       pos=(p['page'],l['bbox'][1]);t=l['text']
       if pos<=first and pos[0]>=first[0]-1 and re.search(rf'(?:Q\s*|questions?\s*){group[0]}\s*et\s*{group[1]}\b',t,re.I):earlier.append(dict(l,page=p['page']))
     if earlier:all_lines.append(max(earlier,key=lambda l:(l['page'],l['bbox'][1])))
     # Every line between group header and the end of its second question, no subsequent question.
     start=min((l['page'],l['bbox'][1]) for l in all_lines);lastlines=cleanlines(ps[-1]['lines']);end=max((l['page'],l['bbox'][3]) for l in lastlines)
     lines=[dict(l,page=p['page']) for p in E[name] for l in p['lines'] if start<=(p['page'],l['bbox'][1]) and (p['page'],l['bbox'][3])<=end and l['bbox'][1]<810]
     # Avoid cleanlines stopping on the second heading: grouped crop is deliberate.
     grouped=[]
     for pi in range(start[0],end[0]+1):
      p=E[name][pi-1];low=max(15,start[1]-4) if pi==start[0] else 15;high=min(p['height']-28,end[1]+5) if pi==end[0] else p['height']-30
      grouped.append({'file':M[name]['file'],'page':pi,'rect':[24,round(low,2),round(p['width']-20,2),round(high,2)]})
     row[role]=grouped;note.append(f'Le document présente un schéma commun aux QCM {group[0]} et {group[1]} ; la copie conserve ce groupe pour montrer le schéma et les deux séries d’items.')
   if not row[role]:row[role]=bounds(name,lines)
   row[role+'File']=name
   if note:row[role+'Note']=' '.join(note)
  rows.append(row)
(P/'crops.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
miss=[]
for bank,b in B.items():
 qs=[r['id'] for r in rows if r['bank']==bank and r.get('subjectMissing')]
 if qs:miss.append({'bank':bank,'role':'subject','questionIds':qs,'document':b['questions'][0]['sourceSubject'],'reason':'PDF thématique corrigé uniquement pour ces questions ; recherche complémentaire dans la compilation effectuée par le vérificateur, résultats à fusionner avant rapport final.','searched':['29 PDF de l’archive Embryo.zip','7 versions séparées non corrigées','parties non annotées des PDF mixtes']})
(P/'missing.json').write_text(json.dumps(miss,ensure_ascii=False,indent=2))
print('Crops',len(rows),'role sets',collections.Counter(role for r in rows for role in ['subject','correction'] if r[role]),'panels',sum(len(r[role]) for r in rows for role in ['subject','correction']))
