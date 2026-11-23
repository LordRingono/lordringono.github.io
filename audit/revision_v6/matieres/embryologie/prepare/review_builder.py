import json,re,pathlib,copy,unicodedata,difflib,collections,fitz,hashlib
P=pathlib.Path(__file__).parent;ROOT=P.parents[3]
B=json.load(open(P.parents[1]/'baseline_exams.json'));B={k:copy.deepcopy(v) for k,v in B.items() if v.get('ue')=='ue5e'}
S=json.load(open(P/'segments.json'));A=json.load(open(P/'assignments.json'));M=json.load(open(P/'source_manifest.json'));E=json.load(open(P/'extraction.json'))
changes=[];audit=[];crop=[];missing=[];flags=[]
def norm(t):
 t=unicodedata.normalize('NFKD',t).lower().replace('œ','oe').replace('æ','ae');return re.sub(r'[^a-z0-9]','',t)
def getseg(bank,q,role):
 a=next((a for a in A[bank] if a['id']==q['id'] and a['role']==role and a['status']=='linked'),None)
 return S[a['source']][a['segmentIndex']] if a else None
def optblocks(s,bank,lower=False):
 out=[];cur=None;lines=s['lines'][1:]
 for l in lines:
  t=l['text'];m=re.match(r'^([A-Za-z]{1,2})\s*[–—:.)-]\s*(.*)',t)
  if m and (m[1].isupper() or lower):
   cur={'id':m[1].upper(),'lines':[l],'text':m[2],'page':l['page']};out.append(cur)
  elif cur:
   if re.match(r'^20\d\d[-–]',t):continue
   # Layout labels at the side of diagrams are not part of the last option.
   if l['bbox'][0]>300 and (bank in ['embryo.aut.s3','embryo.aut.s4']):continue
   if re.match(r'^(?:Ce schéma|Les (?:2 )?questions|Questions \d|Q\s*\d+\s*et\s*\d|Plaque préchordale|Là où)',t,re.I):continue
   cur['lines'].append(l);cur['text']+=' '+t
 for o in out:
  v=re.search(r'\b(Vrai|Faux)\b',o['text'],re.I)
  o['verdict']=bool(v and v[1].lower()=='vrai') if v else None
  o['statement']=o['text'][:v.start()].strip() if v else o['text']
  o['detail']=o['text'][v.start():].strip() if v else ''
  o['original']=' '.join(l.get('originalText',l['text']) for l in o['lines'])
  o['original']=re.sub(r'^[A-Za-z]{1,2}\s*[–—:.)-]\s*','',o['original']).strip()
  if re.search(r'\b(Vrai|Faux)\b',o['original'],re.I):o['original']=re.split(r'\b(?:Vrai|Faux)\b',o['original'],1,flags=re.I)[0].strip()
  o['added']=' '.join(l.get('addedText','') for l in o['lines']).strip()
  o['struck']=' '.join(l.get('struckText','') for l in o['lines']).strip()
  o['rectified']=' '.join(l.get('correctedText',l['text']) for l in o['lines'])
  o['rectified']=re.sub(r'^[A-Za-z]{1,2}\s*[–—:.)-]\s*','',o['rectified']).strip()
 return out
def change(bank,q,field,value,why):
 old=q.get(field)
 if old==value:return
 changes.append({'bank':bank,'id':q['id'],'field':field,'old':copy.deepcopy(old),'new':copy.deepcopy(value),'reason':why});q[field]=value
def itemchange(bank,q,letter,text,why):
 options=copy.deepcopy(q['options']);next(o for o in options if o['id']==letter)['text']=text;change(bank,q,'options',options,why)
def addnote(bank,q,items,text):
 q.setdefault('reviewNotes',[]).append({'bank':bank,'id':q['id'],'items':items,'kind':'source_conflict','text':text,'refs':[{'file':q['sourceCorrection'],'page':q['correctionPage'],'label':'Corrigé original — p. '+str(q['correctionPage']),'href':''}],'noteId':f'embryo-v6-{bank}-{q["id"]}-{len(q.get("reviewNotes",[]))+1}'})
def qget(bank,id):return next(q for q in B[bank]['questions'] if q['id']==id)
# Proven lost repeated-letter entries, stable existing option identifiers.
q=qget('embryo.aut.meiose',5);opts=copy.deepcopy(q['options']);pos=next(i for i,o in enumerate(opts) if o['id']=='L');opts.insert(pos,{'id':'O','sourceLabel':'K bis (source)','text':'En méiose 1 il y a brassage intrachromosomique.'});change('embryo.aut.meiose',q,'options',opts,'Seconde proposition K distincte, visible dans le corrigé original p.2, omise lors de l’import.');change('embryo.aut.meiose',q,'answer','BCEFMNO','Verdict Vrai imprimé pour la seconde proposition K, identifiée O dans le site.');q['explanations']['O']='Vrai. Le document comporte deux propositions K différentes ; cette seconde proposition est identifiée K bis.';addnote('embryo.aut.meiose',q,['K','O'],'Le corrigé emploie deux fois la lettre K pour des phrases différentes : la condensation en méiose I (Faux) et le brassage intrachromosomique en méiose I (Vrai). La seconde est restituée sous O, avec le libellé K bis. La répétition identique de J dans la source n’est affichée qu’une fois.')
q=qget('embryo.aut.fec',23);opts=copy.deepcopy(q['options']);opts.append({'id':'N','sourceLabel':'M bis (source)','text':'correspond à la sous-unité alpha du dimère.'});change('embryo.aut.fec',q,'options',opts,'Seconde proposition M distincte, explicitement Faux Béta dans le PDF p.7, absente du site.');q['explanations']['N']='Faux : Béta (texte du corrigé).';addnote('embryo.aut.fec',q,['M','N'],'Le corrigé porte deux propositions M. La première, sur la cape post-acrosomique, est indiquée Vrai ; la seconde, sur la sous-unité alpha, est indiquée Faux avec la rectification « Béta ». Cette seconde proposition est restituée sous N avec son libellé source M bis.')
# Stem pollution / damaged words: confirmed by independent verifier and original PDF.
for bank,id,letter,pattern,repl,why in [
 ('embryo.aut.coeur',4,'G',r'\s*Ce schéma concerne les questions 5 et 6\s*:.*$','','Consigne commune suivante retirée de l’item G ; déjà conservée dans le bloc Q5/Q6.'),
 ('embryo.col.s4',28,'E',r'\s*Les questions 29 et 30 se rapportent au schéma ci-dessous\s*:.*$','','Consigne commune suivante retirée de l’item E ; bloc commun préservé.'),
 ('embryo.col.s4',34,'E',r'\s*Questions 35 et 36\s*:.*$','','Consigne commune suivante retirée de l’item E ; bloc commun préservé.'),
 ('embryo.col.s4',43,'D',r'\s*Questions 44 et 45\s*;.*$','','Consigne commune suivante retirée de l’item D ; bloc commun préservé.'),
 ('embryo.aut.coeur',9,'N',r'extr-embryonnaire','extra-embryonnaire','Mot rétabli conformément au sujet original.'),
 ('embryo.ann.coeur',15,'C',r'l s deux','Les deux','Mot déformé rétabli d’après le sujet original.'),
 ('embryo.ann.coeur',18,'E',r'\s*RAS\s*$','','Note RAS parasite retirée de l’énoncé de l’item.'),
 ('embryo.col.s4',48,'C',r'H\s+ns\s+n','Hensen','Nom rétabli d’après les PDF sujet et corrigé.'),
 ('embryo.col.s4',54,'A',r'4°"','4e','Ordinal déformé rétabli d’après le document original.')]:
 q=qget(bank,id);o=next(o for o in q['options'] if o['id']==letter);new=re.sub(pattern,repl,o['text']);itemchange(bank,q,letter,new,why)
q=qget('embryo.aut.coeur',2);addnote('embryo.aut.coeur',q,['F','G','H','I','J','K','L','M','N','O','P'],'Correspondance des documents : le sujet réunit deux phrases dans l’item f, alors que le corrigé les sépare en f et g. L’item F du site suit le sujet et correspond donc aux deux f/g du corrigé ; les items G à P correspondent ensuite aux h à q du corrigé. La clé conserve l’appariement des phrases, pas un simple décalque des lettres.')
q=qget('embryo.col.s4',47);addnote('embryo.col.s4',q,['A'],'Le sujet indique J24 dans A, tandis que la phrase recopiée dans le corrigé indique J25 puis ajoute « Vrai c’est J24 ». Le site conserve J24, conformément au sujet non corrigé. Consulter les deux copies originales pour voir cette différence.')
# Add actual common source blocks for the remaining repeated images.
for bank,ids,text in [
 ('embryo.aut.s4',[23,24],'Q23 et 24 : Cette coupe'),
 ('embryo.col.s4',[54,55],'Questions 54 et 55 : à propos du schéma suivant.'),
 ('embryo.col.s4',[68,69],'Questions 68 et 69 se rapportant au schéma suivant.')]:
 qq=[qget(bank,i) for i in ids];images=list(dict.fromkeys(im for q in qq for im in q.get('images',[])))
 ctx={'id':f'v6-shared-{bank}-{ids[0]}','text':text,'images':images,'sourceFile':qq[0]['sourceSubject'],'sourceStartPage':qq[0]['subjectPage'],'sourceEndPage':qq[-1]['subjectPage']}
 for q in qq:
  change(bank,q,'sharedContexts',[ctx],'Consigne et figure réellement communes aux deux QCM, affichées avant le premier QCM visible.');change(bank,q,'images',[],'Figure placée dans le bloc commun pour éviter sa répétition comme schéma individuel.')
# Full document comparison and literal explanation restoration.
for bank,b in B.items():
 for q in b['questions']:
  corr=getseg(bank,q,'correction');subject=getseg(bank,q,'subject') or corr.get('subjectPart');cp=corr.get('correctionPart',corr);co=optblocks(cp,bank,bank=='embryo.aut.coeur');so=optblocks(subject,bank,bank=='embryo.aut.coeur') if subject else []
  ckey=re.match(r'^\s*(?:Q\s*)?\d+\s*[.\-–:]\s*([A-K()]{1,14})(?:$|\s*[Δ:])',cp['text']);ckey=ckey[1] if ckey else None
  rows=[]
  for o in q['options']:
   candidates=[c for c in co if c['id']==o['id']]
   # All candidate phrases compared; stable IDs may differ from repeated original letters.
   if bank=='embryo.aut.coeur' and q['id']==2:
    letters=['F','G'] if o['id']=='F' else [chr(ord(o['id'])+1)] if o['id']>='G' else [o['id']]
    candidates=[c for c in co if c['id'] in letters]
   elif o.get('sourceLabel'):
    lab=re.match(r'([A-Z]+)',o['sourceLabel']); candidates=[c for c in co if c['id']==lab[1]] if lab else candidates
   def similarity(c):return max(difflib.SequenceMatcher(None,norm(o['text']),norm(c[k])).ratio() for k in ['statement','original'])
   c=max(candidates,key=similarity) if candidates else None
   sc=[x for x in so if x['id']==o['id']]
   if o.get('sourceLabel'):
    lab=re.match(r'([A-Z]+)',o['sourceLabel']);sc=[x for x in so if x['id']==lab[1]] if lab else sc
   u=max(sc,key=lambda c:difflib.SequenceMatcher(None,norm(o['text']),norm(c['statement'])).ratio()) if sc else None
   old=q.get('explanations',{}).get(o['id'],'');detail=(c or {}).get('detail','')
   # The separate correction portion is actual detailed feedback, not another stem.
   if corr.get('correctionPart') and c:
    if not detail:detail=c['text'].strip()
    if len(norm(detail))>len(norm(old))+12 and not (q.get('answer') is None or q.get('rawAnswer')=='AUCUNE'):
     ex=copy.deepcopy(q.get('explanations',{}));ex[o['id']]=detail;change(bank,q,'explanations',ex,'Détail de correction séparé restitué littéralement depuis le PDF, à la bonne lettre.')
   # Inline older annales: restore the source's coloured rectification without inventing an explanation.
   elif '.ann.' in bank and c and c['added'] and (not old or norm(old) in ['vrai','faux']):
    if c['detail']:detail=c['detail']
    elif c['struck']:
     detail='Dans le corrigé, « '+re.sub(r'\s+',' ',c['struck']).strip()+' » est barré. Annotation ajoutée : « '+re.sub(r'\s+',' ',c['added']).strip()+' ».'
    else:detail='Annotation du corrigé : « '+c['added'].strip()+' ».'
    ex=copy.deepcopy(q.get('explanations',{}));ex[o['id']]=detail;change(bank,q,'explanations',ex,'Annotation de correction absente rétablie depuis les passages colorés/barrés du PDF original.')
   if c and not old and not '.ann.' in bank and detail:
    # Do not treat only-source missing marker as inferred true or false.
    ex=copy.deepcopy(q.get('explanations',{}));ex[o['id']]=detail;change(bank,q,'explanations',ex,'Verdict/détail explicite manquant rétabli depuis le corrigé.')
   if u: textstatus='matched_subject' if norm(o['text'])==norm(u['statement']) else 'subject_difference_to_review'
   elif c:textstatus='correction_only'
   else:textstatus='mapping_to_review'
   r={'id':o['id'],'sourceLabel':o.get('sourceLabel',o['id']),'siteStatement':o['text'],'subjectStatement':u['statement'] if u else None,'correctionStatement':c['statement'] if c else None,'sourceText':c['text'] if c else None,'rawVerdict':re.search(r'\b(?:Vrai|Faux)\b',c['detail'],re.I)[0] if c and re.search(r'\b(?:Vrai|Faux)\b',c['detail'],re.I) else None,'sourceHeaderKey':ckey,'sourceDetail':detail,'status':textstatus,'sourcePages':sorted(set(l['page'] for l in c['lines'])) if c else [],'sourceAdded':c['added'] if c else None,'sourceStruck':c['struck'] if c else None}
   if textstatus.endswith('review'):flags.append({'bank':bank,'id':q['id'],'item':o['id'],'status':textstatus,'site':o['text'],'subject':u['statement'] if u else None,'correction':c['statement'] if c else None})
   rows.append(r)
  audit.append({'bank':bank,'id':q['id'],'printedNumber':q.get('sourceNumber'),'sourceSubject':q['sourceSubject'] if subject else None,'sourceCorrection':q['sourceCorrection'],'subjectPages':sorted(set(l['page'] for l in subject['lines'])) if subject else [],'correctionPages':sorted(set(l['page'] for l in corr['lines'])),'status':'subject_and_correction_compared' if subject else 'correction_compared_subject_missing','items':rows,'sourceHeader':cp['text'],'key':q['answer']})
(P/'reviewed.json').write_text(json.dumps({'banks':{k:{'questions':v['questions']} for k,v in B.items()}},ensure_ascii=False,indent=2));(P/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));(P/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2));(P/'residual_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('Draft',len(audit),'questions',sum(len(a['items']) for a in audit),'items',len(changes),'changes',len(flags),'flags')
print('Change types',collections.Counter(c['field'] for c in changes));print('Coverage',collections.Counter(a['status'] for a in audit))
