from pathlib import Path
import json, re, hashlib, unicodedata
from copy import deepcopy
import audit_biomol as a

OUT=a.OUT
BANKS=deepcopy(a.BANKS)
REFS=json.loads((a.ROOT/'output/site/audit/revision_v4/references.json').read_text())
ED_MAP=json.loads((a.ROOT/'work/agents/biomol_ed/source_map.json').read_text())
MANIFEST={}
for b in BANKS.values():
 for q in b['questions']:
  for field in ['sourceSubject','sourceCorrection']:
   name=q[field]
   if name in MANIFEST:continue
   hit=REFS.get(name)
   if name in ED_MAP:packaged='sources/'+ED_MAP[name]
   elif hit:packaged=hit['packaged']
   elif name=='2. Annales Acide nucléiques LS ENONCE.pdf':packaged='sources/biomol_v6/intro_annales_sujet.pdf'
   elif name=='2. Annales Acide nucléiques LS CORRECTION.pdf':packaged='sources/biomol_v6/intro_annales_corrige.pdf'
   else:
    slug=re.sub(r'[^A-Za-z0-9]+','_',unicodedata.normalize('NFKD',Path(name).stem).encode('ascii','ignore').decode()).strip('_')
    packaged='sources/biomol_v6/'+slug+'.pdf'
   f=a.SOURCE/name
   MANIFEST[name]={'file':name,'absolute':str(f),'packaged':packaged,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pages':len(a.fitz.open(f))}

def ref(name,page,label):return {'file':name,'page':page,'label':label,'href':MANIFEST[name]['packaged']+f'#page={page}'}

CHANGES=[];NOTES=[];AUDIT=[];CROPS=[];REVIEW_FLAGS=[]

def record(bank,q,field,old,new,reason):
 if old==new:return
 CHANGES.append({'bank':bank,'id':q['id'],'field':field,'before':old,'after':new,'reason':reason})

def note(bank,q,items,text):
 n={'bank':bank,'id':q['id'],'sourceId':str(q.get('sourceNumber',q['id'])),'items':items,'kind':'source_conflict','text':text,
    'refs':[ref(q['sourceSubject'],q['subjectPage'],'Sujet original'),ref(q['sourceCorrection'],q['correctionPage'],'Corrigé original')],
    'sourceVerdict':'Clé conservée : '+(q.get('answer') or ('aucune proposition vraie' if q.get('answerIsEmpty') else 'ambiguë / hors note')),
    'noteId':f'biomol-v6-{len(NOTES)+1:03d}'}
 q.setdefault('reviewNotes',[]).append(n);NOTES.append(n)

def parsed(block,bank,q):
 # Typographical source labels are normalized only for correspondence, never on the original image.
 b=deepcopy(block)
 expanded=[]
 for l in b['lines']:
  if l['text'].startswith('В. '):l['text']='B. '+l['text'][3:]
  if bank=='ue2.regulation.annales' and q['id']==10 and l['text'].startswith('A '):l['text']='A. '+l['text'][2:]
  if bank=='ue2.traduction.annales' and q['id']==5:
   if l['text'].startswith("L'anti-codon présent sur les ARNt"):l['text']='D. '+l['text']
   if l['text'].startswith('Un acide aminé donné ost toujours'):l['text']='E. '+l['text']
  if bank=='ue2.traduction.annales' and q['id']==8 and l['text'].startswith('B- Elément (e)'):l['text']='E- '+l['text'][3:]
  if bank=='ue2.intro.annales' and q['id']==7 and l['text'].startswith('B- ') and ' C. ' in l['text']:
   tail=deepcopy(l);first,second=l['text'].split(' C. ',1);l['text']=first;tail['text']='C. '+second;expanded.extend([l,tail]);continue
  expanded.append(l)
 b['lines']=expanded
 return a.parse_options(b)

def correction_parts(bank,q,cb):
 ll=cb['lines']
 if cb['onlykey']:
  # Reconstruct the correct column before reading explanations: simultaneous
  # headings otherwise truncate the left panel at the right panel's title.
  panels=make_rects(cb)
  ll=[l for l in a.load(cb['source']) if any(l['page']==r['page'] and r['rect'][0]-1<=l['rect'][0] and l['rect'][2]<=r['rect'][2]+1 and r['rect'][1]-1<=l['rect'][1] and l['rect'][3]<=r['rect'][3]+1 for r in panels)]
 keys=[k for k in a.candidates(cb['source'],True) if k['index'] in {l['index'] for l in ll}]
 if cb['onlykey']:keys=[cb['start']]
 if not keys:
  # Unnumbered keys appear as separate printed lines, not as a guessed scientific verdict.
  for l in ll[1:]:
   if re.fullmatch(r'[A-J]{1,10}',l['text']):
    keys.append({'num':str(q.get('sourceNumber')),'index':l['index'],'page':l['page'],'key':l['text'],'heading':l['text'],'rect':l['rect'],'isKey':True})
 if len(keys)>1:raise ValueError(('multiple keys',bank,q['id'],keys))
 # ED annales Q16 has a per-item correction and no aggregate key.
 derived=(bank=='ue2.ed.annales' and q['id']==16)
 if keys:
  key=keys[0]
  body=[l for l in ll if l['index']>key['index']]
  original=deepcopy(cb);original['lines']=[l for l in ll if l['index']<key['index']]
 elif derived:
  at=next(l['index'] for l in ll if l['text'].startswith('A. Faux car la fin'))
  key={'index':at-1,'key':'E','heading':'A Faux ; B Faux ; C Faux ; D Faux ; E Vrai','page':next(l['page'] for l in ll if l['index']==at),'derivedFromExplicitItemMarkers':True}
  body=[l for l in ll if l['index']>=at]
  original=deepcopy(cb);original['lines']=[l for l in ll if l['index']<at]
 else:key=None;body=[];original=cb
 detail={};active=None;general=[]
 for l in body:
  txt=l['text']
  if bank=='ue2.regulation.annales' and q['id']==10 and txt.startswith('A '):txt='A. '+txt[2:]
  m=a.OPT_RE.match(txt)
  if m:
   label,tail=m.groups();detail[label]={'text':tail,'lines':[l]};active=label
  elif active:
   detail[active]['text']+=' '+txt;detail[active]['lines'].append(l)
  else:general.append(txt)
 for dt in detail.values():dt['text']=a.norm(dt['text'])
 # Explanation immediately after a compact key belongs to the whole QCM.
 if key and not key.get('derivedFromExplicitItemMarkers'):
  km=a.KEY_RE.match(key['heading'])
  tail=key['heading'][km.end():].strip(' ,.;:') if km else ''
  if tail:general.insert(0,tail)
 return {'key':key,'original':original,'details':detail,'general':a.norm(' '.join(general))}

def make_rects(block,cut_after=None):
 """Clip complete original pages from heading to next heading/section, with original vector figures."""
 name=block['source'];d=a.DOCS[name];s=block['start'];nxt=block.get('next')
 if s.get('imageOnly'):
  if 'ENONCE' in name:return [{'file':str(a.SOURCE/name),'page':1,'rect':[32,495,574,712]}]
  return [{'file':str(a.SOURCE/name),'page':2,'rect':[30,43,575,323]}]
 ll=block['lines']
 startpage=s['page'];y0=max(18,s['rect'][1]-3)
 endpage=ll[-1]['page'] if ll else s['page'];end_y=ll[-1]['rect'][3]+4 if ll else s['rect'][3]+4
 # Include all images inside the original question/solution section, up to its next boundary.
 boundary=None
 alllines=a.load(name)
 if ll and ll[-1]['index']+1<len(alllines):
  following=alllines[ll[-1]['index']+1]
  if nxt and following['index']>nxt['index']:following=alllines[nxt['index']]
  boundary=(following['page'],following['rect'][1]-4)
 if nxt and not boundary:boundary=(nxt['page'],nxt['rect'][1]-4)
 # In text-only ED corrections the figures carry explanations; extend to the next question.
 if block['onlykey']:
  next_after=[c for c in a.candidates(name,True) if c['page']>s['page'] or (c['page']==s['page'] and c['rect'][1]>s['rect'][1]+5)]
  lower=next_after[0] if next_after else None
  boundary=(lower['page'],lower['rect'][1]-5) if lower else (len(d),813)
  endpage=boundary[0];end_y=boundary[1]
  if endpage>startpage and end_y<60:endpage-=1;end_y=813
 # Source figures outside the text block but before the next QCM/section are still part of this question.
 search_end=boundary[0] if boundary else endpage
 for pn in range(startpage,search_end+1):
  for im in d[pn-1].get_text('dict')['blocks']:
   if im['type']!=1:continue
   r=im['bbox']
   if pn==startpage and r[1]<y0-2:continue
   if boundary and (pn>boundary[0] or (pn==boundary[0] and r[3]>boundary[1]+2)):continue
   if pn>endpage:endpage=pn;end_y=r[3]+4
   elif pn==endpage:end_y=max(end_y,r[3]+4)
 rects=[]
 for pn in range(startpage,endpage+1):
  top=y0 if pn==startpage else 18
  bottom=min(816,end_y if pn==endpage else 816)
  if bottom>top+4:
   x0,x1=30,max(575,d[pn-1].rect.width-12)
   for im in d[pn-1].get_text('dict')['blocks']:
    if im['type']==1 and im['bbox'][1]>=top-2 and im['bbox'][3]<=bottom+2:
     x0=min(x0,im['bbox'][0]-2);x1=max(x1,im['bbox'][2]+2)
   rects.append({'file':str(a.SOURCE/name),'page':pn,'rect':[round(max(0,x0),3),round(top,3),round(min(d[pn-1].rect.width,x1),3),round(bottom,3)]})
 # Two correction panels can share a row. Their horizontal bounds must remain independent.
 if block['onlykey']:
  row=[c for c in a.candidates(name,True) if c['page']==s['page'] and abs(c['rect'][1]-s['rect'][1])<5]
  if len(row)>1:
   row.sort(key=lambda c:c['rect'][0]);ix=next(i for i,c in enumerate(row) if c['num']==s['num'])
   # Figure extents are confirmed separately by visual review for these paired rows.
   split={'2. Correction ED 2025-2026.pdf':{'2':218,'3':218,'9':350,'10':350,'11':296,'12':296},'2. Correction ED 2026-2027.pdf':{'3':335,'4':335}}.get(name,{}).get(s['num'],300)
   for r in rects:
    if r['page']==s['page']:
     if ix==0:r['rect'][2]=split
     else:r['rect'][0]=split
 return rects

def main():
 for bank,b in BANKS.items():
  ss=a.start_blocks(bank,'subject');cc=a.start_blocks(bank,'correction')
  for idx,q in enumerate(b['questions']):
   before=deepcopy(q);sb=ss[idx];cb=cc[idx]
   sp=parsed(sb,bank,q);cp=correction_parts(bank,q,cb);corrected=parsed(cp['original'],bank,q)
   sby={o['id']:o for o in sp['options']};cby={o['id']:o for o in corrected['options']}
   entry={'bank':bank,'id':q['id'],'sourceNumber':q.get('sourceNumber'),'subject':{'file':q['sourceSubject'],'page':sb['start']['page'],'printedNumber':sb['start']['num'],'heading':sp['stem']},'correction':{'file':q['sourceCorrection'],'page':cb['start']['page'],'printedNumber':cb['start']['num'],'key':cp['key']},'items':[],'status':'paired_originals_compared','sourceLimits':[]}
   crop={'bank':bank,'id':q['id'],'subject':make_rects(sb),'correction':make_rects(cb)}
   if bank=='ue2.transcription.autotest' and q['id']==2:
    op=next(o for o in q['options'] if o['id']=='D');op['text']=re.sub(r'\s+Fau$','',op['text'])
    record(bank,q,'options.D',before['options'][3]['text'],op['text'],'Le sujet non corrigé contient le résidu « Fau » du mot de correction ; retiré de l’item interactif.')
    crop['subjectAfterCorrection']=True;crop['subjectNote']='Le fichier intitulé ENONCE contient « Fau » après l’item D. Cette copie exacte est accessible après correction pour ne pas révéler cet indice.'
    note(bank,q,['D'],'Le sujet non corrigé contient déjà « Fau » après la phrase de D, alors que le corrigé porte « Faux ». Ce résidu de correction a été retiré de l’item interactif. La copie authentique du sujet est donc accessible après validation uniquement.')
   if (bank,q['id']) in [('ue2.intro.annales',9),('ue2.transcription.annales',14)]:
    op=next(o for o in q['options'] if o['id']=='E');old=op['text'];op['text']=sby['E']['text']
    record(bank,q,'options.E',old,op['text'],'Suppression d’une consigne/mention suivante, absente de cet item dans le sujet original.')
   source_answer=''
   for o in q['options']:
    so=sby.get(o['id']);co=cby.get(o['id'])
    raw=co['text'] if co else None
    item={'id':o['id'],'siteText':o.get('text',''),'sourceText':so['text'] if so else None,'subjectEvidence':so['lines'] if so else [],'correctedStatement':None,'correctionEvidence':co['lines'] if co else [],'sourceMarker':None,'sourceVerdict':None,'sourceDetail':None,'comparison':'matched','notes':[]}
    if bank=='ue2.ed.annales' and q['id']==2:
     item['sourceText']=o.get('sourceText',o['text']);item['comparison']='visually_transcribed_image_question';item['notes'].append('Énoncé et items sous forme d’image dans les deux PDF ; vérification sur les pages rendues, pas de couche texte.')
    elif so is None:item['comparison']='needs_manual_review'
    elif a.cmp(so['text'])!=a.cmp(o.get('sourceText',o.get('text',''))):
     if bank=='ue2.transcription.autotest' and q['id']==2 and o['id']=='D':item['comparison']='source_annotation_removed'
     else:item['comparison']='needs_manual_review'
    if 'autotest' in bank and not cp['key'] and raw:
     marks=list(re.finditer(r'\b(Vrai|Faux|VRAI|FAUX)\b',raw))
     if not marks:marks=list(re.finditer(r'(?<![\w-])([VF])(?=\s|[.,;:]|$)',raw))
     if marks:
      m=marks[0];item['sourceMarker']=m.group();item['sourceVerdict']=m.group().lower() in ('vrai','v')
      item['sourceDetail']=raw[m.end():].lstrip(' ,:;.');item['correctedStatement']=raw[:m.start()].rstrip(' ,:;')
      if item['sourceVerdict']:source_answer+=o['id']
      if a.cmp(item['correctedStatement'])!=a.cmp(item['sourceText'] or ''):item['notes'].append('Le libellé du corrigé diffère du sujet : comparer les deux copies.')
      old=q.get('explanations',{}).get(o['id'],'')
      if a.cmp(old)!=a.cmp(item['sourceDetail']):
       # Do not add a verdict word to a source-free explanation, or invent content.
       q.setdefault('explanations',{})[o['id']]=item['sourceDetail']
       record(bank,q,'explanations.'+o['id'],old,item['sourceDetail'],'Détail relu dans la correction originale, après son marqueur explicite.')
     else:item['notes'].append('Aucun verdict textuel détecté ; contrôle visuel nécessaire.')
    else:
     if cp['key']:
      item['sourceMarker']=cp['key']['heading'];item['sourceVerdict']=o['id'] in (cp['key']['key'] or '')
      item['correctedStatement']=raw
     dt=cp['details'].get(o['id'])
     if dt:
      item['sourceDetail']=dt['text'];item['detailEvidence']=dt['lines']
      vm=re.match(r'^(Vrai|Faux|VRAI|FAUX)\b',dt['text'])
      if vm:
       item['detailVerdict']=vm.group().lower()=='vrai'
       if item['sourceVerdict'] is not None and item['detailVerdict']!=item['sourceVerdict']:item['notes'].append('Le verdict écrit dans le détail contredit la clé globale.')
     if not cb['onlykey'] or dt:
      # Copy only the actual per-item correction, eliminating duplicate import text and following stems.
      new=dt['text'] if dt else ''
      old=q.get('explanations',{}).get(o['id'],'')
      if a.cmp(old)!=a.cmp(new):
       q.setdefault('explanations',{})[o['id']]=new
       record(bank,q,'explanations.'+o['id'],old,new,'Alignement avec le détail exact du corrigé source, sans duplication ni consigne suivante.')
    item['detailVerification']='original_text_compared' if item.get('sourceDetail') else ('original_correction_capture_attached' if cb['onlykey'] else 'no_separate_textual_detail')
    entry['items'].append(item)
   if cp['key']:source_answer=''.join(sorted(set(cp['key']['key'] or '')))
   entry['sourceAnswer']=source_answer;entry['siteAnswer']=q.get('answer','')
   entry['keyComparison']='matched' if set(source_answer)==set(q.get('answer','')) else 'needs_manual_review'
   if cp['key'] and '(' in cp['key']['heading'].split(' ')[0] or (cp['key'] and re.match(r'^[A-J]+\s+\([A-J]+\)',cp['key']['heading'])):
    entry['keyComparison']='source_ambiguous_preserved_ungraded';entry['sourceLimits'].append('Clé parenthétique ambiguë ; question conservée hors note.')
   if not q['options']:
    entry['keyComparison']='non_qcm_matching_exercise';entry['sourceLimits'].append('Exercice de correspondance sans options, conservé hors note.')
   if entry['keyComparison']=='source_ambiguous_preserved_ungraded':
    literal=cp['key']['heading']
    note(bank,q,[c for c in 'ABCDE' if '('+c in literal or c+')' in literal],f'La clé imprimée est « {literal} », avec une réponse entre parenthèses. Le détail discute précisément cet item et ne permet pas de fixer une clé unique sans arbitrage. La question reste hors note ; comparer la copie du corrigé et vérifier la réponse attendue dans la ronéo ou auprès du tutorat.')
   # Original explanatory prose is attached once to the QCM, not appended to its last option.
   if cp['general'] and not cb['onlykey']:
    old=q.get('generalExplanation','');new=cp['general']
    if a.cmp(old)!=a.cmp(new):q['generalExplanation']=new;record(bank,q,'generalExplanation',old,new,'Commentaire général présent dans le corrigé source.')
   if bank=='ue2.traduction.annales' and q['id']==5:
    crop['subjectNote']='Les deux derniers items sont imprimés sans lettres ; leur position correspond à D puis E dans la clé ABD.'
    crop['correctionNote']=crop['subjectNote']
   if bank=='ue2.traduction.annales' and q['id']==8:
    crop['subjectNote']='La cinquième ligne porte par erreur B dans le document ; elle correspond à E (élément e) dans la clé CDE.'
    crop['correctionNote']=crop['subjectNote']
   if (bank,q['id'])==('ue2.adn.autotest',13):
    note(bank,q,['C'],'Le sujet écrit « n’est pas autonome », mais la version corrigée écrit « est autonome » puis donne Faux, avec « fonctionnement SEMI autonome avec 1 ORI ». La négation diffère donc entre les deux documents : le verdict ne porte pas sur exactement la même phrase. Clé du corrigé conservée ; vérifier la formulation et le statut attendu dans la ronéo.')
   if (bank,q['id'])==('ue2.organisation.autotest',9):
    note(bank,q,['E'],'Différence entre les originaux : le sujet cite le facteur VII, tandis que le corrigé a remplacé VII par VIII et valide E. La clé BCE valide donc une version modifiée de cet item. Le sujet interactif conserve VII ; consulter la ronéo pour le facteur concerné, comme indiqué dans la réserve de cours.')
   if (bank,q['id'])==('ue2.reparation.autotest',11):
    note(bank,q,['D'],'Le sujet parle de MSH2/MSH6 et de « retards de méthylation ». Le corrigé remplace entièrement D par « Les protéines du système MMR détectent les mésappariements de l’ADN et retirent plusieurs nucléotides du brin fils autour du mésappariement », puis le donne vrai. La clé BCD se rapporte donc à une rédaction différente. Comparer les deux copies et vérifier la version attendue dans la ronéo.')
   if (bank,q['id'])==('ue2.reparation.autotest',15):
    note(bank,q,['C'],'Le sujet s’arrête à « Le système NER fait intervenir l’ADN pol. » sans préciser la polymérase. Le corrigé ajoute α à l’énoncé puis le déclare faux, en citant notamment δ dans son explication. Le verdict porte ainsi sur une précision absente du sujet. Clé AE conservée ; vérifier l’item complet dans la ronéo.')
   if bank=='ue2.replication.annales' and q['id']==18:
    crop['correctionNote']='Ce QCM 39′ du sujet est imprimé 39 dans le corrigé ; association vérifiée par les cinq énoncés, à distinguer du QCM 39 suivant.'
   if bank=='ue2.transcription.annales' and idx in [16,17,18]:
    crop['correctionNote']=f"Numéro du sujet : {q['sourceNumber']} ; numéro du corrigé : {cb['start']['num']}. Association vérifiée par les cinq énoncés, pas par le seul numéro."
   if entry['keyComparison']=='needs_manual_review' or any(i['comparison']=='needs_manual_review' for i in entry['items']):REVIEW_FLAGS.append(entry)
   AUDIT.append(entry);CROPS.append(crop)
 # One drawing and its instruction apply to two consecutive QCM, not to the E item before them.
 bank='ue2.intro.annales';qs={q['id']:q for q in BANKS[bank]['questions']};im=qs[10]['images'][0]
 c={'id':'ue2.intro.annales.bases-pyrimidiques-2022','title':'Énoncé commun — bases pyrimidiques','text':'Soient les trois bases pyrimidiques suivantes : même schéma pour les deux QCM suivants.','images':[im],'questionIds':[10,11],'questionNumbers':['4','5'],'sourceStartPage':3,'sourceEndPage':3,'sourceFile':qs[10]['sourceSubject'],'sourcePdf':MANIFEST[qs[10]['sourceSubject']]['packaged']}
 for n in [10,11]:qs[n].setdefault('sharedContexts',[]).append(deepcopy(c))
 qs[10]['images']=[]
 CHANGES.append({'bank':bank,'ids':[10,11],'field':'sharedContexts','reason':'Consigne et schéma commun rétablis avant chacun des QCM concernés, y compris après filtrage.'})
 add_context_copies()
 # Preserve metadata snapshots of any annotations whose reviewed text was repaired.
 for bank,b in BANKS.items():
  for q in b['questions']:
   for n in q.get('reviewNotes',[]):
    if 'reviewedItemText' in n:n['reviewedItemText']={o['id']:o.get('text','') for o in q['options'] if o['id'] in n.get('items',[])}
    if 'reviewedExplanation' in n:n['reviewedExplanation']={k:q.get('explanations',{}).get(k,'') for k in n.get('items',[])}
 (OUT/'reviewed.json').write_text(json.dumps({'banks':{k:{'questions':b['questions']} for k,b in BANKS.items()}},ensure_ascii=False,indent=2))
 for name,content in [('audit.json',AUDIT),('crops.json',CROPS),('changes.json',CHANGES),('manual_review_flags.json',REVIEW_FLAGS),('source_manifest.json',list(MANIFEST.values())),('notes.json',NOTES)]:
  (OUT/name).write_text(json.dumps(content,ensure_ascii=False,indent=2))
 print('Q',len(AUDIT),'ITEMS',sum(len(e['items']) for e in AUDIT),'CHANGES',len(CHANGES),'NOTES',len(NOTES),'FLAGS',len(REVIEW_FLAGS),'CAPTURES',sum(len(c['subject'])+len(c['correction']) for c in CROPS))

def add_context_copies():
 """An original question copy also carries the common statement used by that question."""
 by={(c['bank'],c['id']):c for c in CROPS};context_rects={}
 for bank,b in BANKS.items():
  qs=b['questions'];lookup={q['id']:i for i,q in enumerate(qs)};blocks=a.start_blocks(bank,'subject')
  for q in qs:
   for ctx in q.get('sharedContexts',[]):
    if ctx['id'] in context_rects:continue
    firstid=min(ctx['questionIds'],key=lambda qid:lookup[qid]);i=lookup[firstid];qb=qs[i];block=blocks[i]
    f=str(a.SOURCE/qb['sourceSubject']);startpage=ctx['sourceStartPage'];endpage=ctx['sourceEndPage'];rects=[]
    if ctx['id']=='ue2.intro.annales.bases-pyrimidiques-2022':
     l=next(l for l in a.load(qb['sourceSubject']) if l['text'].startswith('Soient les trois bases pyrimidiques suivantes'))
     rects=[{'file':f,'page':3,'rect':[30,l['rect'][1]-3,575,l['rect'][3]+3]}, {'file':f,'page':3,'rect':[292.36,300.52,555.2,405.2]}]
    elif ctx['id']=='ue2.ed.annales.2013-2014-exon1':rects=[{'file':f,'page':1,'rect':[33,497,575,594]}]
    elif ctx['id'].endswith('.introduction'):rects=[{'file':f,'page':1,'rect':[30,25,582,800]}]
    else:
     prev=by[(bank,qs[i-1]['id'])]['subject'] if i else []
     onpage=[r for r in prev if r['page']==startpage]
     top=max(r['rect'][3] for r in onpage)+2 if onpage else 18
     if block['start']['page']==startpage:
      bottom=block['start']['rect'][1]-3
      if bottom<=top+20:
       # Common wording can be part of the first question's own heading.
       options=parsed(block,bank,qb)['options']
       if options:
        top=block['start']['rect'][1]-3;bottom=options[0]['lines'][0]['rect'][1]-2
      if bottom>top+4:rects.append({'file':f,'page':startpage,'rect':[30,round(top,3),582,round(bottom,3)]})
     else:
      for pn in range(startpage,min(endpage,block['start']['page'])+1):
       bottom=block['start']['rect'][1]-3 if pn==block['start']['page'] else 810
       rects.append({'file':f,'page':pn,'rect':[30,round(top if pn==startpage else 18,3),582,round(bottom,3)]})
    for r in rects:r['purpose']='Énoncé commun : '+ctx['title'];r['contextId']=ctx['id']
    context_rects[ctx['id']]=rects
  for q in qs:
   own=by[(bank,q['id'])]['subject'];extra=[]
   for ctx in q.get('sharedContexts',[]):
    for r in context_rects[ctx['id']]:
     if not any(x['page']==r['page'] and x['rect'][0]<=r['rect'][0] and x['rect'][1]<=r['rect'][1] and x['rect'][2]>=r['rect'][2] and x['rect'][3]>=r['rect'][3] for x in own):extra.append(deepcopy(r))
   if extra:
    unique={json.dumps([r['page'],r['rect']]):r for r in extra}
    by[(bank,q['id'])]['subject']=list(unique.values())+own
 (OUT/'context_crops.json').write_text(json.dumps(context_rects,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
