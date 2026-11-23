from pathlib import Path
import json,copy,re,hashlib
ROOT=Path('/workspace/scratch/f3cb3bb97377'); BASE=ROOT/'work/site_v6/biomol'; OUT=BASE/'verify'
R=json.loads((BASE/'prepare/reviewed.json').read_text()); C=json.loads((BASE/'prepare/crops.json').read_text()); S=json.loads((OUT/'independent_sources.json').read_text()); ROWS=json.loads((OUT/'comparison_rows.json').read_text()); M={s['file']:s for s in json.loads((BASE/'prepare/source_manifest.json').read_text())}
Q={(b,q['id']):q for b,v in R['banks'].items() for q in v['questions']}; CM={(r['bank'],r['id']):r for r in C}; RM={(r['bank'],r['id']):r for r in ROWS}; changes=[]
def change(b,id,field,new,reason):
 q=Q[(b,id)];old=copy.deepcopy(q.get(field));q[field]=new
 if old!=new:changes.append({'bank':b,'id':id,'field':field,'before':old,'after':new,'reason':reason})
def crops(b,id,role,new,reason):
 c=CM[(b,id)];old=copy.deepcopy(c[role]);c[role]=new
 if old!=new:changes.append({'bank':b,'id':id,'field':'crops.'+role,'before':old,'after':new,'reason':reason})
def panel(b,id,role,page,rect,purpose=None,contextId=None):
 f=Q[(b,id)]['sourceSubject' if role=='subject' else 'sourceCorrection'];d={'file':M[f]['absolute'],'page':page,'rect':[round(x,3) for x in rect]}
 if purpose:d['purpose']=purpose
 if contextId:d['contextId']=contextId
 return d
def note(b,id,items,text,kind='missing_reference'):
 q=Q[(b,id)]; refs=[]
 for role,label in [('subject','Sujet original'),('correction','Corrigé original')]:
  f=q['sourceSubject' if role=='subject' else 'sourceCorrection']; p=q['subjectPage' if role=='subject' else 'correctionPage']
  refs.append({'file':f,'page':p,'label':label,'href':M[f]['packaged']+'#page='+str(p)})
 ns=copy.deepcopy(q.get('reviewNotes',[]));ns.append({'bank':b,'id':id,'sourceId':q['sourceNumber'],'items':items,'kind':kind,'text':text,'refs':refs,'sourceVerdict':'Clé conservée : '+q['answer'],'noteId':'biomol-v6-verify-'+b.split('.')[1]+'-'+str(id)})
 change(b,id,'reviewNotes',ns,'Limite confirmée dans les deux PDF originaux ; pas de fin de phrase ni de symbole inventé.')
# One proven cross-boundary contamination.
b='ue2.intro.annales'; d=copy.deepcopy(Q[(b,3)]['explanations']);d['D']="Faux, c'est un A donc amine ici";change(b,3,'explanations',d,'Le bandeau séparé « 20125-2016 » n’appartient pas au détail D (corrigé p. 1).')
# Source-year headers checked on rendered pages, not inferred from chronology.
for f in json.loads((OUT/'category_flags.json').read_text()):
 b,id=f['bank'],f['id']
 if b=='ue2.transcription.annales' and id in (17,18,19):continue
 val=f['source']
 if b=='ue2.transcription.annales' and id in (20,21,22):val='2020-2021 Session 1 et 2 PACE et PASS'
 change(b,id,'category',val,'Bandeau de session du sujet original, p. '+str(f['page'])+'.')
note('ue2.transcription.autotest',35,['B'],'L’item B s’arrête après « premier nucléotide qui sera » dans le sujet (Wooclap Q7, p. 6) et dans le corrigé (p. 7). La fin de phrase n’est pas fournie. La transcription conserve cette limite et la clé ADE ; une version complète de cet item permettrait de lever ce manque.')
note('ue2.traduction.autotest',27,[],"Le titre du Wooclap Q3 se termine par « quels sont ceux qui ... » dans le sujet et le corrigé. Les cinq propositions reprennent celles de l’autotest Q21 du même document, dont le titre porte sur les éléments jouant un rôle lors de l’initiation de la traduction. Le titre abrégé original et la clé ADE sont conservés.",'source_conflict')
note('ue2.reparation.annales',8,['A','B','C','D'],"Plusieurs mots ou groupes de mots sont déjà tronqués dans les deux originaux (Q33, année 2013–2014) : « anome la réparation » en A, « recombi homologue » en B, « guidé par les groupes » sans groupement précisé en C et « mécanis de » en D. Les copies permettent de constater ces limites ; aucune complétion n’est inventée et la clé ABD est conservée.")
note('ue2.reparation.annales',17,['B'],"Le sujet et le corrigé impriment tous deux « L’ADN polymérase & intervient dans la réparation NER ». Le caractère & ne permet pas d’identifier avec certitude la polymérase visée. Ce caractère original et la clé BC sont conservés ; une version lisible de l’item B reste nécessaire pour préciser son énoncé.")
# Six original-panel figure failures: split text and lateral diagrams where the next Q starts below the text.
fixes=[('ue2.intro.annales',5,'subject',None,[30,53.44,588.2,238.76]),('ue2.arn.autotest',9,'subject',437,[437.3,252.05,559.05,405.3]),('ue2.arn.annales',4,'subject',433,[434.56,529.6,569,720.44]),('ue2.traduction.autotest',7,'subject',463,[464.56,19.361,574.841,157.888]),('ue2.traduction.annales',8,'subject',433,[434.8,317.44,562.28,486.44]),('ue2.traduction.annales',8,'correction',None,[30,218.56,583.32,402.315])]
for b,id,role,x,rect in fixes:
 old=copy.deepcopy(CM[(b,id)][role]);p=old[0]['page']
 if x is None:old[0]['rect']=rect
 else:old[0]['rect'][2]=x;old.append(panel(b,id,role,p,rect,'Figure latérale complète, avec toutes ses lettres'))
 crops(b,id,role,old,'Le panneau préparé coupait une partie de la figure originale ; contrôle visuel et géométrique indépendant.')
for id in (10,11):
 b='ue2.intro.annales';old=copy.deepcopy(CM[(b,id)]['correction']);old.insert(0,panel(b,id,'correction',4,[30,398.9,444.1,548.7],'Contexte commun corrigé : trois bases pyrimidiques','intro-pyrimidines-correction'));crops(b,id,'correction',old,'Restitution du schéma commun et de ses légendes dans le corrigé, accessibles après validation.')
# A colored residue has no clean original alternative. The interactive text contains no colored verdict.
b='ue2.traduction.autotest';id=3;c=CM[(b,id)];c['subjectAfterCorrection']=True;c['subjectNote']='Le PDF du sujet comporte un point rouge en fin d’item C, résidu typographique coloré. La copie authentique est consultable après validation.'
changes.append({'bank':b,'id':id,'field':'crops.subjectAfterCorrection','before':False,'after':True,'reason':c['subjectNote']})
# ED annales: correction copies also need their shared annotated figure/context.
b='ue2.ed.annales'; groups=[];seen=set()
for q in R['banks'][b]['questions']:
 for ctx in q.get('sharedContexts',[]):
  if ctx['id'] in seen or ctx['id'].endswith('oligonucleotide'):continue
  seen.add(ctx['id']);ids=ctx['questionIds'];first=ids[0]
  if first==2: p0=p1=2;top=44.5;bottom=142
  else:
   s=RM[(b,first)]['correction'];prior=[ln for ln in S[Q[(b,first)]['sourceCorrection']]['lines'] if ln['index']<s['index'] and re.match(r'^20\d\d',ln['text'])];hdr=prior[-1];p0=hdr['page'];top=hdr['rect'][1]-4;p1=s['page'];bottom=s['rect'][1]-3
  pcs=[]
  for p in range(p0,p1+1):
   y0=top if p==p0 else 18;y1=bottom if p==p1 else 800
   if y1-y0<10:continue # no context precedes a question at the very top of the next page
   pcs.append(panel(b,first,'correction',p,[30,y0,583.32,y1],'Contexte commun dans le corrigé : '+ctx['title'],ctx['id']+'.correction'))
  groups.append({'id':ctx['id'],'questions':ids,'panels':pcs})
  for id in ids:
   if id==2:continue # the raster Q24 full correction already contains this entire context
   crops(b,id,'correction',copy.deepcopy(pcs)+copy.deepcopy(CM[(b,id)]['correction']),'Contexte et figures communs présents dans le corrigé original, absents de la copie préparée.')
# Q29 explicitly depends on the oligonucleotide in previous Q28.
id=29;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs.insert(1,panel(b,id,'correction',14,[30,573.9,583.32,607],'Fragment d’ADN commun aux QCM 2 et 3','ue2.ed.annales.2021-2022-oligonucleotide.correction'));crops(b,id,'correction',pcs,'Le fragment auquel se réfère cette question figure dans le titre de la précédente.')
# Include existing reference table in each original subject copy which uses that reference.
for b,rect in [('ue2.ed.2025-2026',[45,507,570,785]),('ue2.ed.2026-2027',[45,155,570,680])]:
 for q in R['banks'][b]['questions']:
  if not q.get('references'):continue
  pcs=copy.deepcopy(CM[(b,q['id'])]['subject']);pcs.append(panel(b,q['id'],'subject',11,rect,'Annexe originale : code génétique et liste des acides aminés','code-genetique'))
  crops(b,q['id'],'subject',pcs,'L’annexe existait déjà dans references ; la copie originale comprend désormais le même tableau fourni.')
# Correct ED25 diagrams which sit beside or explain two headings.
b='ue2.ed.2025-2026'
for id in (19,20):
 pcs=[panel(b,id,'correction',6,[30,570,115,622],'Clé de la question'),panel(b,id,'correction',6,[116.5,569.8,570.5,796.2],'Séquence : sites donneur et accepteur d’épissage'),panel(b,id,'correction',7,[30,18,583.32,296.493],'Rappel d’épissage fourni en suite de page')]
 # Isolate the key to avoid exposing the neighboring key in the narrow left panel.
 pcs[0]['rect'][1:4:2]=[572.655 if id==19 else 602.655,600.655 if id==19 else 622]
 crops(b,id,'correction',pcs,'La figure commune commence avant Q19 et descend sous Q20 ; restitution complète sans couper les étiquettes.')
# Q26/27: same polyadenylation sequence under both headings.
id=26;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][3]=34.8;pcs.append(panel(b,id,'correction',10,[35,49.3,454.6,292.9],'Séquence corrigée : signal de polyadénylation'));crops(b,id,'correction',pcs,'Clé Q26 complète et séquence annotée commune Q26/Q27, auparavant absente de cette copie.')
id=27;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][1]=35;crops(b,id,'correction',pcs,'Début du panneau situé entre les clés Q26 et Q27, sans fragment de la ligne précédente.')
id=32;crops(b,id,'correction',[panel(b,id,'correction',12,[30,293.5,300,322.5]),panel(b,id,'correction',12,[306.5,286.6,583.4,438.7],'Tableau des substitutions par transition/transversion')],'Tableau latéral dépassant la hauteur du titre Q32, auparavant tronqué.')
id=33;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][2]=300;crops(b,id,'correction',pcs,'Séparation de la colonne Q33 et du tableau latéral propre à Q32 ; molécules Q33 complètes.')
id=42;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][3]=593.5;pcs.append(panel(b,id,'correction',15,[35,607.8,448.8,811.0],'Amorce, brin matrice et allongement de l’ADN'));crops(b,id,'correction',pcs,'Clé Q42 complète ; le schéma commun d’allongement était rattaché au seul titre Q43, alors qu’il explique Q42.')
id=43;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][1]=593.8;crops(b,id,'correction',pcs,'Début du panneau situé entre les clés Q42 et Q43, sans fragment de la ligne précédente.')
# ED26: diagrams overlap heading heights and must be sliced into meaningful columns.
b='ue2.ed.2026-2027'
id=8;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][2]=594;pcs[0]['rect'][3]=403.3;crops(b,id,'correction',pcs,'Le bord droit de la figure dépassait x=583.32 ; la légende « Région promoteur » sous le schéma gauche est également rétablie.')
for id in (9,10):
 pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][2]=328
 if id==9:pcs[0]['rect'][1]=403.6;pcs[0]['rect'][3]=580
 else:pcs[0]['rect'][1]=580.1;pcs[0]['rect'][3]=639
 pcs.append(panel(b,id,'correction',2,[328.8,474,575.4,645.2],'Acétylation et décompaction de la chromatine'))
 crops(b,id,'correction',pcs,'Figure latérale commune Q9/Q10, auparavant coupée par les hauteurs de titres.')
id=11;crops(b,id,'correction',[panel(b,id,'correction',2,[30,641.7,383,810.2],'Code histone complet')],'Le code histone commence avant Q11 et finit plus bas que Q12.')
id=12;crops(b,id,'correction',[panel(b,id,'correction',2,[388,742.4,583.32,803.5]),panel(b,id,'correction',2,[35,416.7,325.8,580.6],'Illustration QCM 9 explicitement citée dans ce corrigé')],'La correction renvoie à l’illustration QCM9 ; paragraphe complet en colonne droite et retrait d’un fragment tronqué du code histone voisin.')
id=24;crops(b,id,'correction',[panel(b,id,'correction',5,[30,293.8,350,366.5]),panel(b,id,'correction',5,[354.6,302.3,565.2,496.4],'ARNt porteur de proline et codon correspondant')],'ARNt latéral complet, auparavant coupé au début de Q25.')
id=25;crops(b,id,'correction',[panel(b,id,'correction',5,[18.5,366.5,350,591],'Q25 et partie supérieure du chromosome'),panel(b,id,'correction',5,[18.5,589,210,632.2],'Suite du chromosome, sans la diapositive voisine')],'Rétablissement du bord gauche et de la partie basse du caryotype ; séparation de la diapositive Q26.')
id=26;crops(b,id,'correction',[panel(b,id,'correction',5,[30,628.4,211,816]),panel(b,id,'correction',5,[211.7,590.9,565.3,795.2],'Dénaturation, fusion et renaturation')],'La diapositive de fusion commence au-dessus du titre Q26 ; copie originale complète.')
id=38;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][1]=243.8;pcs[0]['rect'][2]=595.32;crops(b,id,'correction',pcs,'Rétablissement du haut de la séquence et du bord droit de l’explication de la mutation.')
id=40;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][1]=597.8;crops(b,id,'correction',pcs,'Rétablissement de la numérotation et du haut de la séquence, au-dessus du titre Q40.')
# Restore mathematically meaningful superscripts proved by native PDF span flags and visual pages.
# Final geometry pass: include the whole native figure and exclude fragments of a neighbor.
for b,id,role,rects,reason in [
 ('ue2.arn.annales',5,'subject',[[30,641.023,433,747.365]],'Le schéma ARNt appartient à la question précédente ; les cinq propositions tiennent dans la colonne gauche.'),
 ('ue2.arn.autotest',10,'subject',[[30,382.373,437,427.5],[30,427.5,583.32,517.775]],'Découpage entre les lignes A et B pour exclure la fin du schéma de Q9 sans couper une proposition.'),
 ('ue2.traduction.autotest',8,'subject',[[30,134.869,463,165.5],[30,165.5,583.32,241.365]],'Découpage entre les lignes A et B pour exclure la fin du schéma de Q7 sans couper une proposition.')]:
 page=CM[(b,id)][role][0]['page'];crops(b,id,role,[panel(b,id,role,page,r) for r in rects],reason)
for b,id,idx,coord,value,reason in [
 ('ue2.ed.2025-2026',6,0,3,618,'Le schéma du gène descend sous la limite automatique du titre suivant.'),
 ('ue2.ed.2025-2026',7,0,1,618.5,'Début après le schéma de Q6, avant le titre Q7.'),
 ('ue2.ed.2025-2026',31,0,3,281.6,'Fin après le schéma Q31, avant le tableau de Q32.'),
 ('ue2.ed.2026-2027',6,0,3,152.7,'Rétablissement du bas de la séquence et de ses repères exon/intron.'),
 ('ue2.ed.2026-2027',7,0,1,153.1,'Début après la figure Q6, avant le titre Q7.'),
 ('ue2.ed.2026-2027',9,1,3,643.45,'Fin de la figure d’acétylation avant le schéma du code histone.'),
 ('ue2.ed.2026-2027',10,1,3,643.45,'Fin de la figure d’acétylation avant le schéma du code histone.'),
 ('ue2.ed.2026-2027',11,0,1,643.4,'Début du code histone après le bas de l’illustration précédente.'),
 ('ue2.ed.2026-2027',26,0,1,630.5,'Début de la colonne de texte après le chromosome voisin, avant la clé Q26.'),
 ('ue2.ed.2026-2027',33,0,3,274.3,'Fin de la séquence entière, sous son bord raster inférieur.'),
 ('ue2.ed.2026-2027',34,0,1,274.8,'Début après la figure Q33, avant la clé Q34.'),
 ('ue2.ed.2026-2027',37,0,3,212.5,'Fin après la figure Q37, avant le haut de celle de Q38.'),
 ('ue2.ed.2026-2027',39,0,3,581.4,'Fin après la figure Q39, avant le haut de celle de Q40.')]:
 pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[idx]['rect'][coord]=value;crops(b,id,'correction',pcs,reason)
for id in (10,11,12,13):
 b='ue2.ed.annales'
 for role,page in [('subject',4),('correction',5)]:
  pcs=copy.deepcopy(CM[(b,id)][role]);changed=False
  for pc in pcs:
   if pc['page']==page and 365<pc['rect'][3]<367:pc['rect'][3]=367.5;changed=True
  if changed:crops(b,id,role,pcs,'Tableau du code génétique et sa dernière ligne d’abréviations entièrement inclus.')
for id in (22,23,24):
 b='ue2.ed.annales';pcs=copy.deepcopy(CM[(b,id)]['correction']);changed=False
 for pc in pcs:
  if pc['page']==12 and 447<pc['rect'][3]<448:pc['rect'][3]=448.8;changed=True
 if changed:crops(b,id,'correction',pcs,'Bord inférieur de la séquence commune entièrement inclus.')
# The unlabeled teaching diagram at the foot of ED25 p10 introduces the following microRNA pair.
b='ue2.ed.2025-2026';id=27;pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs[0]['rect'][3]=292.9;crops(b,id,'correction',pcs,'Fin après le schéma de polyadénylation ; le schéma de biogenèse des microARN est rattaché aux Q28/Q29.')
for b,ids,page,rect,title in [
 ('ue2.ed.2025-2026',(28,29),10,[35,305.3,570.5,716.8],'Biogenèse des microARN : contexte commun aux Q28 et Q29'),
 ('ue2.ed.2025-2026',(32,),12,[35,338.3,277.8,551.5],'Bases normale et mutée : contexte chimique commun aux Q32 et Q33'),
 ('ue2.ed.2026-2027',(22,),4,[35,580.8,570.5,695.1],'Séquence de fin du gène : signal de polyadénylation commun aux Q21 et Q22'),
 ('ue2.ed.2026-2027',(28,29),6,[35,33.8,570.5,229.1],'Structure et nomenclature des bases : figure commune aux Q27 à Q29')]:
 for id in ids:
  pcs=copy.deepcopy(CM[(b,id)]['correction']);pcs.append(panel(b,id,'correction',page,rect,title));crops(b,id,'correction',pcs,'Schéma original commun rattaché aux questions qui exploitent directement ses bases ou ses mécanismes.')
# Restore mathematically meaningful superscripts proved by native PDF span flags and visual pages.
mathopts=[('ue2.replication.autotest',1,'B','109','10⁹'),('ue2.replication.autotest',1,'D','Mg2+','Mg²⁺'),('ue2.replication.autotest',7,'C','109','10⁹'),('ue2.replication.annales',4,'A','109','10⁹'),('ue2.replication.annales',11,'B','107','10⁷'),('ue2.replication.annales',13,'B','109','10⁹'),('ue2.reparation.annales',18,'A','109','10⁹')]
for b,id,it,a,z in mathopts:
 opts=copy.deepcopy(Q[(b,id)]['options']);o=next(o for o in opts if o['id']==it);assert a in o['text'];o['text']=o['text'].replace(a,z);change(b,id,'options',opts,'Exposant visible dans le PDF original et dans ses spans ; la forme aplatie changeait la valeur scientifique.')
for b,id,it,pairs in [('ue2.replication.autotest',1,'B',[('109','10⁹')]),('ue2.replication.autotest',7,'C',[('106','10⁶')]),('ue2.replication.annales',11,'B',[('107','10⁷'),('109','10⁹')]),('ue2.replication.annales',13,'B',[('109','10⁹')])]:
 d=copy.deepcopy(Q[(b,id)]['explanations'])
 for a,z in pairs:assert a in d[it];d[it]=d[it].replace(a,z)
 change(b,id,'explanations',d,'Rétablissement des puissances de dix du détail original.')
# Write complete snapshots; no files outside verify are mutated.
for name,data in [('approved_reviewed.json',R),('approved_crops.json',C),('changes.json',changes),('correction_contexts.json',groups)]: (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(OUT/'asset_manifest.json').write_text('[]\n')
print('changes',len(changes),'questions',len(Q),'items',sum(len(q['options']) for q in Q.values()),'panels',sum(len(c['subject'])+len(c['correction']) for c in C))
