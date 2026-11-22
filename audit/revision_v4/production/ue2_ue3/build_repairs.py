import json,copy,re,fitz
from pathlib import Path
p=Path('work/review_v4/ue2_ue3'); exams=json.loads((p/'exams.json').read_text())
out={'additions':[],'patches':[]}
def q(bank,id):return next(x for x in exams[bank]['questions'] if x['id']==id)
def ref(file,page,label):return {'file':file,'page':page,'label':label}
def patch(bank,id,changes,reason,refs):out['patches'].append({'bank':bank,'id':id,'set':changes,'reason':reason,'refs':refs})
def new(bank,id,after,source,category,question,items,key,explanations,sp,cp):
 base=copy.deepcopy(q(bank,after))
 base.update(id=id,sourceNumber=source,num=int(source.replace('’','')) if source.replace('’','').isdigit() else 0,prime='’' if '’' in source else '',category=category,question=question,options=[{'id':chr(65+i),'text':text} for i,text in enumerate(items)],answer=key,explanations=explanations,warning='',subjectPage=sp,startPage=sp,sourceEndPage=sp,correctionPage=cp,startY=None,images=[],originalImages=[],figureRefs=[],context='')
 out['additions'].append({'bank':bank,'afterId':after,'question':base,'reason':'QCM intégral présent dans les PDF fournis, mais absorbé dans le dernier item de la question précédente lors du découpage. Nouvel identifiant en fin de numérotation ; aucun identifiant existant changé.','refs':[ref(base['sourceSubject'],sp,'Énoncé complet du QCM récupéré'),ref(base['sourceCorrection'],cp,'Clé et explications originales')]})
 return base
b='ue2.arn.annales';s=q(b,17)['sourceSubject'];c=q(b,17)['sourceCorrection']
new(b,28,17,'X','2020-2021 PACE','Les ARN de transfert :',[
'Sont transférés du noyau au cytoplasme lors de la traduction.',
'Contiennent de très nombreux ribonucléotides atypiques obtenus par modification enzymatique post-transcriptionnelle.',
'Le ribonucléotide terminal de type cytosine fixe de façon covalente l’acide aminé spécifié par l’anti-codon.',
'L’anticodon porté par le bras A s’associe de façon anti-parallèle et complémentaire au codon porté par l’ARNm.',
'Un ARNt portant un anticodon donné est lié à un acide aminé spécifique.'], 'BDE', {'A':'Faux, la traduction se fait TOUJOURS dans le cytoplasme, donc ils sont formés dans le cytoplasme','C':'Faux, c’est une adénine et non une cytosine (séquence terminale CCA 3’)'},4,6)
x=copy.deepcopy(q(b,17)['options']);x[-1]['text']='Des miARN sont retrouvés dans les mitochondries (mitomiR) et peuvent activer la traduction des ARNm mitochondriaux.'
patch(b,17,{'options':x,'sourceEndPage':3,'explanations':{'C':'Vrai car on les retrouve dans le sang'},'warning':''},'Retrait de la question X PACE absorbée dans E et restauration des explications du Q7 miARN ; clé ABCDE inchangée.',[ref(s,3,'Fin réelle de Q7 miARN'),ref(s,4,'Question X séparée'),ref(c,6,'Q7 ABCDE et son explication C puis X BDE')])
new(b,29,18,'X','2020-2021 PASS Session 2','Les petits ARN non codants :',[
'Les snARN et les snoARN sont des ARN régulateurs.',
'Les snARN représentent 10% des ARN totaux.',
'Les snARN modifient les ribonucléotides des ARN ribosomiques en plaçant des enzymes au niveau de certaines séquences de leur ARN cible.',
'Les snARN s’associent à des protéines spécifiques pour former des ribonucléoprotéines nucléaires.',
'Les snoARN sont impliqués dans la modification post-transcriptionnelle d’ARN non codants.'], 'ADE', {'A':'Vrai, ils régulent la maturation d’autres ARN','B':'Faux, tous les ARN régulateurs représentent <1% des ARN totaux','C':'Faux, ce sont les snoARN qui le font'},4,6)
x=copy.deepcopy(q(b,18)['options']);x[-1]['text']='Les ARNt associés au même acide aminé sont appelés ARNt iso-accepteurs.'
patch(b,18,{'options':x,'category':'2020-2021 PASS Session 2','explanations':{'A':'Faux, ARN codant = ARN qui est traduit, seuls les ARNm sont des ARN codants','D':'Faux, c’est la 1ère base de l’anticodon, qui correspond à la 3ème base du codon sur l’ARNm : Attention codon et anti-codon sont antiparallèles'},'warning':''},'Retrait du QCM X petits ARN absorbé dans E et restauration du corrigé Q5 ARNt ; clé BCE inchangée.',[ref(s,4,'Q5 puis X sont deux QCM distincts'),ref(c,6,'Clés et explications de Q5 BCE et X ADE')])
b='ue2.anomalies.annales';s=q(b,4)['sourceSubject'];c=q(b,4)['sourceCorrection']
new(b,9,4,'15’','2020-2021','Une insertion de 3 nucléotides :',[
'Induit un décalage du cadre de lecture.',
'Peut conduire à la formation d’un codon stop.',
'Induit une modification du site d’épissage en amont de l’exon.',
'Est responsable de recombinaison chromosomique.',
'Peut modifier la fonction de la protéine codée par le gène.'], 'BE', {'A':'Faux','B':'Vrai si les 3 nts sont un codon stop','C':'Faux pas d’action à distance','D':'Faux, aucune raison','E':'Vrai si l’AA ajouté affecte un domaine fonctionnel ou le repliement de la protéine'},1,2)
x=copy.deepcopy(q(b,4)['options']);x[-1]['text']='Un variant génétique synonyme.'
patch(b,4,{'options':x,'explanations':{'A':"Vrai, c'est la définition du cours"},'warning':''},'Q15’ absorbé dans E et explications de Q15 contaminées par Q15’ ; clé A inchangée.',[ref(s,1,'Q15 et Q15’ distincts'),ref(c,2,'Q15 A puis Q15’ BE')])
b='ue2.transcription.autotest'
for i,key in enumerate(['DE','AD','BD','CD','BD','ACD','ADE'],29):
 z=q(b,i);cp=6 if i<33 else 7
 patch(b,i,{'answer':key,'warning':'','category':'Wooclap 2025','correctionPage':cp},'Clé imprimée seule après les propositions, perdue par le parseur ; restauration littérale.',[ref(z['sourceSubject'],z['subjectPage'],'Wooclap 2025 Q'+z['sourceNumber']),ref(z['sourceCorrection'],cp,'Clé isolée '+key)])
x=copy.deepcopy(q(b,28)['options']);x[-1]['text']='Il est composé d’un seul brin.'
ex=copy.deepcopy(q(b,28)['explanations']);ex['E']=''
patch(b,28,{'options':x,'explanations':ex},'Retrait du titre de section Wooclap 2025 accolé à l’item E et à son explication.',[ref(q(b,28)['sourceSubject'],5,'Fin de Q28 puis titre de section'),ref(q(b,28)['sourceCorrection'],6,'Item E Faux puis titre Wooclap')])
b='ue2.transcription.annales'
fixes={17:('BD',{'A':'Faux. La transcription commence 25 nt après la boite TATA','B':'Vrai. Pour permettre la synthèse en 5’→3’','C':'Faux on est chez les eucaryotes donc signal de term = AATAAA (chez les procaryotes : riche en T après le palindrome imparfait)','E':'Faux. La queue polyA est non transcrite et non présente sur l’ADN'}),18:('B',{'A':'Faux. Dans le noyau','C':'Faux. Le site accepteur d’épissage est en 3’ des introns','D':'Faux. C’est une 7-méthyl guanosine','E':'Faux du brin anti sens'}),19:('BCE',{'A':'Faux. Epissage uniquement dans le noyau','D':'Faux. Constitués de snARN (attention à ne pas confondre les snARN et les snoARN !!)'})}
for i,(key,ex) in fixes.items():
 z=q(b,i)
 patch(b,i,{'answer':key,'explanations':ex,'correctionPage':6,'category':'2020-2021 Session 1 et 2 PACE et PASS','warning':''},'Appariement prouvé par les cinq propositions identiques : numéros 1’/2’/3’ dans le sujet, 10/11/12 dans le corrigé.',[ref(z['sourceSubject'],4,'Question '+z['sourceNumber']),ref(z['sourceCorrection'],6,'Question '+str(i-7)+' : '+key)])
b='ue2.replication.annales';i=18;z=q(b,i)
patch(b,i,{'answer':'ACD','correctionPage':6,'category':'2022-2023 sessions 1 et 2','explanations':{'B':'Faux, l’amorce fait 4 à 12 nts','E':'Faux, une seule séquence sur le brin avancé, la ligase est nécessaire sur le brin retardé'},'warning':''},'Même QCM : numéro 39’ dans le sujet, 39 dans l’énoncé du corrigé mais 39’ devant la clé ACD. Appariement par les cinq items.',[ref(z['sourceSubject'],4,'Q39’'),ref(z['sourceCorrection'],6,'Q39 et clé 39’ ACD')])
b='ue2.reparation.annales';i=11;z=q(b,i)
patch(b,i,{'answer':'BDE','correctionPage':4,'explanations':{'A':'Faux, altération du système MMR','C':'Faux, des substitutions'},'warning':''},'Clé BDE isolée en tête de la page suivante, immédiatement après le Q9 de la page précédente.',[ref(z['sourceSubject'],z['subjectPage'],'Q9 La réparation de l’ADN'),ref(z['sourceCorrection'],3,'Q9 en fin de page'),ref(z['sourceCorrection'],4,'BDE et explications A/C en haut de page')])
b='ue2.anomalies.autotest';i=1;z=q(b,i)
patch(b,i,{'answer':'','answerIsEmpty':True,'warning':''},'Les cinq items A à E portent explicitement Faux dans la correction. La clé vide est donc une réponse tout faux, et non une absence de corrigé.',[ref(z['sourceSubject'],1,'Autotest 1 Les SNV'),ref(z['sourceCorrection'],1,'Cinq verdicts Faux explicitement imprimés')])
# Titres d’année suivants absorbés dans un item E : retrait documenté, sans autre changement de texte.
for b,i in [('ue2.adn.annales',15),('ue2.adn.annales',17),('ue2.organisation.annales',7),('ue2.replication.annales',11),('ue2.replication.annales',13),('ue2.replication.annales',15),('ue2.transcription.annales',16),('ue2.transcription.annales',27),('ue2.reparation.annales',16),('ue2.reparation.annales',21)]:
 z=q(b,i);opts=copy.deepcopy(z['options']);old=opts[-1]['text'];mt=re.search(r'20\d\d\s*[-–]\s*20\d\d',old);assert mt
 clean=old[:mt.start()].strip();opts[-1]['text']=clean
 d=fitz.open(Path('sources_biomol/extracted')/z['sourceSubject']);norm=lambda t:re.sub(r'\s+',' ',t).strip()
 pages=list(range(z['subjectPage'],z.get('sourceEndPage',z['subjectPage'])+1));body=' '.join(d[n-1].get_text() for n in pages)
 assert norm(clean) in norm(body),(b,i,clean)
 changes={'options':opts};ex=copy.deepcopy(z.get('explanations',{}))
 for letter,text in ex.items():
  m=re.search(r'20\d\d\s*[-–]\s*20\d\d',text)
  if m:ex[letter]=text[:m.start()].strip()
 if ex!=z.get('explanations',{}):changes['explanations']=ex
 patch(b,i,changes,'Retrait du seul titre de la série suivante accolé à la fin de l’item E. Les mots précédant ce titre sont présents tels quels dans le PDF. Aucune fin inventée pour ADN17E, qui reste tronqué dans la source.',[ref(z['sourceSubject'],n,'Fin de la question et titre de la série suivante') for n in pages])
(p/'source_repairs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Additions',len(out['additions']),'patches',len(out['patches']),'restored keys',sum('answer' in x['set'] for x in out['patches']))
