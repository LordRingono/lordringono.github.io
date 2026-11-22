"""Documented final repairs after checking the original histology subject pages."""
import copy,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E=json.loads((P/'baseline_exams.json').read_text())
OUT=Path(__file__).resolve().parent
patches=[];adds=[];coverage=[];overrides=[]
def q(bank,id):return next(copy.deepcopy(x)for x in E[bank]['questions']if x['id']==id)
def refs(question):
 return [{'file':question['sourceSubject'],'page':question['subjectPage'],'label':'Énoncé original et limite réelle des items'},
         {'file':question['sourceCorrection'],'page':question['correctionPage'],'label':'Correction originale et limite réelle des commentaires'}]
def patch(bank,id,fields,reason):
 old=q(bank,id)
 patches.append({'bank':bank,'id':id,'set':fields,'reason':reason,'refs':refs(old)})
 final={**old,**fields}
 overrides.append({'bank':bank,'id':id,'itemsReviewed': [o['id']for o in final['options']],
  'itemCountReviewed':len(final['options']),'sourceRepair':True,
  'sourceRecheck':{'scope':'Contrôle final de chaque item, de sa lettre et de ses limites dans les deux PDF originaux ; suppression des titres voisins et restauration des choix perdus.',
                   'refs':refs(old)}})

bank='histo.ann.te'
consigne='Concernant le tissu épithélial, indiquez la ou les affirmation(s) correcte(s) parmi les propositions suivantes :'
subject='Annales Tissu épithélial NON corrigé 2020 2026.pdf'
correction='Annales Tissu Epithélial 2020 2026 CORRECTION.pdf'
for id,number,after,options,key,expl,cpage in [
 (28,9,17,[
  'les cellules sont jointives, étroitement juxtaposées',
  'les cellules sont solidarisées par des systèmes de jonction',
  'les filaments intermédiaires sont constitués de vimentine',
  'les cellules reposent directement sur le tissu conjonctif',
  'les cellules ne sont pas en contact des capillaires sanguins'],
  'ABE',{'A':'Vrai.','B':'Vrai.','C':'Faux : de cytokératine sauf pour les épithéliums apparentés comme l’endothélium ou les mésothéliums.','D':'Faux : sur la membrane basale.','E':'Vrai : le tissu épithélial est avasculaire.'},5),
 (29,10,28,[
  'un épithélium unistratifié pavimenteux présente une faible épaisseur',
  'les cellules épithéliales cylindriques peuvent présenter des cils vibratiles',
  'l’épithélium pavimenteux stratifié est constitué de 2 couches de cellules',
  'les microvillosités sont présentes sur les faces latérales des cellules',
  'les jonctions serrées permettent la diffusion des molécules'],
  'AB',{'A':'Vrai : il facilite les échanges.','B':'Vrai : comme dans les voies respiratoires.','C':'Faux : il s’agit de l’épithélium malpighien → nombreuses couches cellulaires, seule la plus apicale est pavimenteuse.','D':'Faux : sur la face apicale.','E':'Faux : elles contrôlent la diffusion des petites molécules.'},6)
]:
 new={'id':id,'sourceNumber':number,'year':'2023-2024','session':'S2','category':'Annales · 2023–2024 · Session 2 (juin 2024)',
  'course':'Tissu épithélial (TE)','question':consigne,'options':[{'id':chr(65+i),'text':v}for i,v in enumerate(options)],
  'answer':key,'explanations':expl,'warning':'','images':[],'subjectPage':5,'correctionPage':cpage,
  'correctionEndPage':6,'sourceSubject':subject,'sourceCorrection':correction,'weight':1}
 proof=[{'file':subject,'page':5,'label':f'QRM {number}, session 2 de juin 2024'},
        {'file':correction,'page':cpage,'label':f'Correction du QRM {number}'}]
 if cpage==5:proof.append({'file':correction,'page':6,'label':'Suite des verdicts C–E du QRM 9'})
 adds.append({'bank':bank,'afterId':after,'question':new,
  'reason':'QRM complet présent dans les sujets et corrigés, mais absent de la banque : les QRM 9 et 10 n’avaient pas été individualisés et le second était absorbé dans la consigne du QCM 18. Nouvel identifiant libre, anciens identifiants préservés.','refs':proof})
 course_refs=[{'file':'Tissu épithélial 1 - CG ACTUALISE.pdf','page':page,'label':'Passage relu lors de la contrelecture indépendante'}for page in ([2,3]if id==28 else [6,7,9,14])]
 if id==29:course_refs.append({'file':'Tissu épithélial 2 - CG - ACTUALISE.pdf','page':2,'label':'Jonctions serrées et contrôle sélectif de diffusion'})
 coverage.append({'bank':bank,'id':id,'status':'reviewed_with_course','itemsReviewed':list('ABCDE'),'itemCountReviewed':5,
  'reviewScope':'Les cinq items et les cinq verdicts relus dans le sujet et le corrigé originaux ; question retrouvée lors du contrôle des frontières entre questions.',
  'consultedFiles':proof,'sourceRepair':True,'figureReview':'no_attached_figure','limitations':[],
  'courseVerification':'Contrelecture indépendante de tous les items contre les passages indiqués ; aucun conflit de verdict identifié. La correction des jonctions serrées conserve la notion de contrôle sélectif de diffusion.',
  'courseReferences':course_refs,'itemsCourseChecked':list('ABCDE')})

old=q(bank,18);ex=copy.deepcopy(old['explanations']);ex['E']='cylindrique'
patch(bank,18,{'question':consigne,'explanations':ex},'Retrait des cinq propositions du QRM 10 et du titre de session absorbés dans la consigne ; retrait du titre de la question suivante dans la correction E. Clé BC conservée.')
old=q(bank,19);opts=old['options'];opts[-1]['text']='les occludines sont des protéines de soudure des JS';ex=old['explanations'];ex['E']=''
patch(bank,19,{'options':opts,'explanations':ex},'Le titre de la question 22 est retiré de l’item E et de son explication ; les cinq items et la clé ACE restent ceux du Q21 original.')
patch(bank,21,{'question':'Au sujet de l’urothélium, indiquez-la ou les affirmation(s) correcte(s) parmi les propositions suivantes :'},'Consigne seule dans le titre ; retrait de l’en-tête CC 2024–2025 et du numéro source déjà distinct des items. Aucun changement de clé.')

bank='histo.ann.tc';old=q(bank,8);opts=old['options']
opts[2]['text']="dans le processus d'ossification de membrane, les ostéoblastes périphériques forment le périoste."
opts.insert(3,{'id':'D','text':"l'ossification endochondrale est un processus moins long que l'ossification de membrane."})
ex=old['explanations'];ex['C']='';ex['D']='Faux : au contraire.'
patch(bank,8,{'options':opts,'explanations':ex,'warning':'','uncorrected':False},'Le choix D du QRM 29, absorbé dans C, est restauré avec sa correction propre. La clé source ABCE est inchangée ; la réserve d’import « clé incomplète » n’a plus lieu d’être.')
overrides[-1].update(status='partially_course_checked',itemsCourseChecked=['C','D'],
 courseReferences=[{'file':'TC3 2026.pdf','page':16,'label':'Ossification de membrane et périoste'}, {'file':'TC3 2026.pdf','page':17,'label':'Durée comparée de l’ossification endochondrale'}],
 courseVerification='Contrelecture indépendante des items C et D avec les deux pages citées : verdicts C vrai et D faux concordants ; pas de signalement scientifique ajouté.')

clean={
 'histo.ann.tc':{
  9:('les fibrocytes sont des cellules très mobiles','quiescentes'),
  10:('les fibres de réticuline forment l’armature du TC lâche','du TC réticulaire'),
  11:('leur SF est minéralisée',''),
  12:('le fibrocartilage présente une bonne résistance mécanique','→ disques intervertébraux'),
  13:(None,''),
  21:('Le complexe macromoléçulaire de la matrice extracellulaire est très hydrophobe.','hydrophile')},
 'histo.ann.tn':{
  34:('ils contrôlent les fonctions sensitives motrices et sécrétoires du TD',''),
  35:('en condition physiologique il est absorbé par l’épendyme','?'),
  36:('elle contient davantage de myéline que la substance blanche','')}
}
for bank,rows in clean.items():
 for id,(option,exp)in rows.items():
  old=q(bank,id);ex=old['explanations'];ex['E']=exp;fields={'explanations':ex}
  if option is not None:
   opts=old['options'];next(o for o in opts if o['id']=='E')['text']=option;fields['options']=opts
  patch(bank,id,fields,'Retrait du titre et de la consigne du QCM suivant, absorbés dans le dernier item et/ou son explication. Items scientifiques et clé source inchangés ; la correction réellement incomplète TC10 reste hors note.')

shared=[]
# The 2019 spinal/cortical motor-neuron case has three successive source stems.
tn_source='annales TISSU NERVEUX 2018 2025.pdf'
for ids,page,key,text in [
 ([5,6,7,8,9],3,'sla', 'La sclérose latérale amyotrophique (SLA) est une maladie neurodégénérative grave, caractérisée par une paralysie musculaire progressive due à une dégénérescence des motoneurones du cortex moteur primaire et des motoneurones de la corne antérieure de la moelle épinière.'),
 ([7],3,'voie-pyramidale', 'La SLA est donc une pathologie neurodégénérative qui affecte le système pyramidal qui contrôle la motricité volontaire. L’influx nerveux généré par les motoneurones corticaux emprunte une voie longue, la voie pyramidale, entrecoupée par un relais synaptique où s’effectue la transmission entre les motoneurones corticaux et les motoneurones périphériques.'),
 ([8,9],4,'nerfs-rachidiens', 'Les motoneurones situés dans la corne antérieure de la moelle lombaire innervent les muscles des membres inférieurs. Leurs axones rentrent dans la constitution des nerfs rachidiens.')
]:
 shared.append({'bank':'histo.ann.tn','questionIds':ids,'id':'v4-shared-histo-tn-mai2019-'+key,'text':text,'images':[],
  'refs':[{'file':tn_source,'page':page,'label':'Contexte original — mai 2019, questions 33–37'}]})
for id in [5,6,7,8,9]:
 fields={'category':'Annales · mai 2019','year':'2018-2019','sourceNumber':id+28}
 if id in [6,9]:fields['answerPolarity']='false'
 if id==6:
  opts=q('histo.ann.tn',id)['options'];next(o for o in opts if o['id']=='E')['text']='Il s’agit d’un neurone de projection de type Golgi I.';fields['options']=opts
 patch('histo.ann.tn',id,fields,'Métadonnées de la session mai 2019 et contexte original rétablis. Les consignes « affirmation inexacte » utilisent un affichage À COCHER/NE PAS COCHER, sans inversion de la clé ; le paragraphe suivant Q34 est retiré de son item E et présenté avant Q35.')

for bank,ids,page,image,text in [
 ('embryo.col.s4',[29,30],5,'static/emb_col_s4_029_1.png','Les questions 29 et 30 se rapportent au schéma ci-dessous :'),
 ('embryo.col.s4',[35,36],6,'static/emb_col_s4_035_1.png','Questions 35 et 36 : ces questions se rapportent au schéma suivant.'),
 ('embryo.col.s4',[44,45],7,'static/emb_col_s4_044_1.png','Questions 44 et 45 : les questions se rapportent au schéma suivant.'),
 ('embryo.aut.coeur',[5,6],2,'static/emb_aut_coeur_005_1.png','Ce schéma concerne les questions 5 et 6 :')
]:
 first=q(bank,ids[0])
 shared.append({'bank':bank,'questionIds':ids,'id':'v4-shared-'+bank+'-'+str(ids[0]),
  'text':text,'images':[image],'refs':[{'file':first['sourceSubject'],'page':page,'label':'Annonce et figure communes dans le sujet original'}]})
 for id in ids:
  old=q(bank,id)
  if old.get('warning')=='Consigne non récupérable automatiquement. Voir la page source.':
   patch(bank,id,{'warning':''},'L’annonce originale et le schéma commun sont rétablis avant le groupe ; la réserve technique « consigne non récupérable » est devenue obsolète.')

(OUT/'source_repairs.json').write_text(json.dumps({'patches':patches,'additions':adds},ensure_ascii=False,indent=2))
(OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
(OUT/'coverage_overrides.json').write_text(json.dumps(overrides,ensure_ascii=False,indent=2))
(OUT/'shared_contexts.json').write_text(json.dumps(shared,ensure_ascii=False,indent=2))
print(json.dumps({'patches':len(patches),'additions':len(adds),'sourceRechecks':len(overrides)},ensure_ascii=False))
