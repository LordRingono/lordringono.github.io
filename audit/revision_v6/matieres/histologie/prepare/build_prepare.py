"""Préparation V6 : preuves documentaires relues et réparations délimitées.

Ce script ne modifie jamais le site. Les sources et les sorties de lecture sont
immuables ; les décisions humaines explicites ci-dessous construisent le lot.
"""
import copy, json, re, hashlib, collections, pathlib, difflib
import fitz
from PIL import Image, ImageDraw
from parse_sources import ROOT, OUT, BASE, NAMES, norm, text, mergelines

SITE = ROOT/'output/site'
COMP = SITE/'sources/Annales_compilation.pdf'
CAN = json.loads((OUT/'canonical.json').read_text())
BLOCKS = json.loads((OUT/'compilation_key_blocks.json').read_text())
MATCHES = json.loads((OUT/'compilation_key_matches.json').read_text())
PDFS = {pathlib.Path(x['file']).stem:pathlib.Path(x['file']) for x in json.loads((OUT/'sources_examined.json').read_text())}
REVIEW = {'banks':{k:{'questions':copy.deepcopy(BASE[k]['questions'])} for k in NAMES}}
FIXES=[]; EXTRA_EVIDENCE={}; COMP_SUPPLEMENTS={}; CLEAN_SUBJECTS={}; ASSETS=[]; FIGURES={}; SESSION={}

def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def qobj(bank,id): return next(q for q in REVIEW['banks'][bank]['questions'] if q['id']==id)
def cq(bank,id): return next(q for q in CAN[bank] if q['id']==id)
def filefor(bank,role): return PDFS[NAMES[bank][0 if role=='subject' else 1]]
def ref(path,page,label):
    path=pathlib.Path(path)
    return {'file':path.name,'page':page,'label':label,'href':str(path.relative_to(SITE))+'#page='+str(page)}
def note(bank,id,items,kind,txt,refs,**kwargs):
    q=qobj(bank,id); x={'bank':bank,'id':id,'items':items,'kind':kind,'text':txt,'refs':refs,
                       'sourceVerdict':'Clé thématique conservée : '+(BASE[bank]['questions'][next(i for i,z in enumerate(BASE[bank]['questions']) if z['id']==id)]['answer'] or 'incomplète'),
                       'noteId':f'histo-v6-{bank}-{id}-{len(q.get("reviewNotes",[]))+1}',**kwargs}
    q.setdefault('reviewNotes',[]).append(x)
def change(bank,id,field,value,reason):
    q=qobj(bank,id); old=copy.deepcopy(q.get(field));q[field]=value
    if old!=value:FIXES.append({'bank':bank,'id':id,'field':field,'before':old,'after':copy.deepcopy(value),'reason':reason})
def option(bank,id,letter,value,reason):
    q=qobj(bank,id);old=copy.deepcopy(q['options']);next(o for o in q['options'] if o['id']==letter)['text']=value
    if old!=q['options']:FIXES.append({'bank':bank,'id':id,'field':'options','before':old,'after':copy.deepcopy(q['options']),'reason':reason})
def explain(bank,id,letter,value,reason):
    q=qobj(bank,id);old=q['explanations'].get(letter);q['explanations'][letter]=value
    if old!=value:FIXES.append({'bank':bank,'id':id,'field':'explanations.'+letter,'before':old,'after':value,'reason':reason})
def horsnote(bank,id,warning,official=None):
    q=qobj(bank,id)
    if official is not None:q['officialAnswer']=official
    change(bank,id,'answer','',warning)
    q.pop('answerIsEmpty',None);q.pop('allowNoAnswer',None)
    change(bank,id,'warning',warning,warning)

def sessions(bank,groups):
    for ids,label,expected in groups:
        for id in ids: SESSION[(bank,id)]={'label':label,'compilationHeader':expected}
sessions('histo.ann.te',[
 (range(1,5),'Décembre 2020, PASS S1 2020–2021','Session 1 2020-2021'),
 (range(5,9),'Décembre 2021, S1 2021–2022','Session 1 2021-2022'),
 (range(9,12),'Décembre 2022, S1 2022–2023','Session 1 2022-2023'),
 (range(12,15),'Juin 2023, S2 2022–2023','Session 2 2022-2023'),
 (range(15,18),'Décembre 2023, S1 2023–2024','Session 1 2023-2024'),
 ([28,29],'Juin 2024, S2 2023–2024','Session 2 2023-2024'),
 (range(18,21),'Décembre 2024, S1 2024–2025','Session 1 2024-2025'),
 ([21,22],'Contrôle continu 2024–2025',None),
 ([23,24],'Juin 2025, S2 2024–2025','Session 2 2024-2025'),
 (range(25,28),'Décembre 2025, S1 2025–2026','Session 1 2025-2026')])
sessions('histo.ann.tc',[
 (range(1,9),'Décembre 2020, PASS S1 2020–2021','Session 1 2020-2021'),
 (range(9,15),'Juillet 2021, PASS S2 2020–2021','Session 2 2020-2021'),
 (range(15,21),'Décembre 2021, S1 2021–2022','Session 1 2021-2022'),
 ([21,22],'Juin 2022, S2 2021–2022','Session 2 2021-2022'),
 (range(23,30),'Décembre 2022, S1 2022–2023','Session 1 2022-2023'),
 (range(30,35),'Juin 2023, S2 2022–2023','Session 2 2022-2023'),
 (range(35,40),'Décembre 2023, S1 2023–2024','Session 1 2023-2024'),
 ([57,58,59],'Juin 2024, S2 2023–2024','Session 2 2023-2024'),
 (range(40,47),'Décembre 2024, S1 2024–2025','Session 1 2024-2025'),
 (range(47,50),'Juin 2025, S2 2024–2025','Session 2 2024-2025'),
 (range(50,57),'Décembre 2025, S1 2025–2026','Session 1 2025-2026')])
sessions('histo.ann.tn',[
 (range(1,5),'Mai 2018, PACES 2017–2018','2017-2018'),
 (range(5,10),'Mai 2019, PACES 2018–2019','2018-2019'),
 (range(10,14),'Mai 2020, PACES 2019–2020','UE5 2019-2020'),
 (range(14,19),'Décembre 2020, PASS S1 2020–2021','Session 1 2020-2021'),
 (range(19,23),'Mai 2021, PACES 2020–2021','PACES 2020-2021'),
 (range(23,27),'Juillet 2021, PASS S2 2020–2021','Session 2 2020-2021'),
 (range(27,34),'Décembre 2021, S1 2021–2022','Session 1 2021-2022'),
 (range(34,38),'Juin 2022, S2 2021–2022','Session 2 2021-2022'),
 (range(38,44),'Décembre 2022, S1 2022–2023','Session 1 2022-2023'),
 (range(44,48),'Juin 2023, S2 2022–2023','Session 2 2022-2023'),
 (range(48,54),'Décembre 2023, S1 2023–2024','Session 1 2023-2024'),
 ([65,66],'Juin 2024, S2 2023–2024','Session 2 2023-2024'),
 (range(54,59),'Décembre 2024, S1 2024–2025','Session 1 2024-2025'),
 (range(59,65),'Décembre 2025, S1 2025–2026','Session 1 2025-2026')])
sessions('histo.ann.tech',[
 (range(1,5),'Mai 2019, PACES 2018–2019','2018-2019'),
 ([5,6],'Décembre 2020, PASS S1 2020–2021','Session 1 2020-2021'),
 (range(7,11),'Décembre 2021, S1 2021–2022','Session 1 2021-2022'),
 (range(11,15),'Décembre 2022, S1 2022–2023','Session 1 2022-2023'),
 (range(15,19),'Juin 2023, S2 2022–2023','Session 2 2022-2023'),
 (range(19,23),'Décembre 2023, S1 2023–2024','Session 1 2023-2024'),
 ([38,39],'Juin 2024, S2 2023–2024','Session 2 2023-2024'),
 ([23],'Contrôle continu 2025',None),([24],'Examen blanc 2025',None),
 (range(25,32),'Décembre 2024, S1 2024–2025','Session 1 2024-2025'),
 ([32,33],'Juin 2025, S2 2024–2025','Session 2 2024-2025'),
 (range(34,38),'Décembre 2025, S1 2025–2026','Session 1 2025-2026')])

# Réparation d'une fusion de deux propositions dans l'import, prouvée dans les
# deux documents thématiques. Le D sans tiret n'avait pas été reconnu en V5.
b='histo.ann.tc';q=qobj(b,5);src=cq(b,5)
change(b,5,'options',[{'id':i['id'],'text':i['subject']} for i in src['items']],
       'C et D sont deux propositions distinctes sur les deux originaux, p. 2.')
change(b,5,'answer','ACD','A, C et D portent Vrai dans le corrigé thématique p. 2.')
explain(b,5,'C','', 'Retrait du D absorbé par le détail de C.')
explain(b,5,'D','Vrai.', 'Verdict explicite du D rétabli, corrigé p. 2.')
change(b,5,'warning','', 'Clé désormais complète et appariée aux cinq propositions.')

# Séparation des énoncés suivants et des explications de l'item précédent.
for bank,id,letter in [('histo.ann.tech',26,'E'),('histo.ann.tech',27,'E')]:
    source=next(i for i in cq(bank,id)['items'] if i['id']==letter)
    option(bank,id,letter,source['subject'],'Retrait de la consigne du QCM suivant, absente de cet item source.')
for bank,id,letter,value in [
 ('histo.ann.tech',26,'E',''),
 ('histo.ann.tech',27,'C','Il faut que l’anticorps secondaire cible l’anticorps primaire'),
 ('histo.ann.tech',27,'E','Non elle n’est pas plus spécifique, mais elle est plus sensible car plusieurs anticorps secondaires peuvent se lier à un anticorps primaire, ce qui permet une détection plus facile'),
 ('histo.ann.tc',40,'E','mais accrochée sur un axe l’acide hyaluronique'),
 ('histo.ann.tc',41,'E','dans la MEC'),('histo.ann.tc',42,'E',''),
 ('histo.ann.tc',43,'E','c’est la coronaire'),('histo.ann.tn',7,'E','')]:
    explain(bank,id,letter,value,'Fin du commentaire vérifiée sur la page source ; retrait du QCM ou du contexte suivant.')

# Deux sujets thématiques contiennent déjà une réponse : la version originale
# propre de la compilation remplace la copie avant correction (sans retouche).
for id,letter,page,yrange,clean in [
 (30,'A',1318,(513,611),'ils ne possèdent pas de cytosquelette.'),
 (45,'C',1275,(67,164),'Il est exclusivement au contact du système nerveux central')]:
    bank='histo.ann.tn';option(bank,id,letter,clean,'Retrait d’une réponse importée dans l’item ; vrai sujet propre retrouvé dans la compilation de la même session.')
    CLEAN_SUBJECTS[(bank,id)]={'file':str(COMP),'page':page,'rect':[38 if id==30 else 52,yrange[0],551,yrange[1]],'fileLabel':'Sujet propre de la compilation, même session','sourceNumber':33 if id==30 else 6}
    note(bank,id,[letter],'source_conflict',
         f'Le PDF thématique intitulé sujet contient déjà une réponse dans l’item {letter}. Le texte interactif est rétabli sans cette réponse à partir du vrai sujet non corrigé de la même session, dans la compilation p. {page}. Les cinq propositions et la session ont été rapprochées. La copie thématique annotée reste jointe au corrigé, sans modification de ses pixels.',
         [ref(filefor(bank,'subject'),cq(bank,id)['subject']['page'],'Sujet thématique déjà annoté'),ref(COMP,page,'Sujet non corrigé de la même session')])

# Coquilles de la source, restaurées par concordance du corrigé de la même
# série et de l'édition complète ; les deux pixels originaux restent conservés.
for id,letter,new,cp,why in [
 (31,'D','Les fibres élastiques sont formées à 90 % de fibrillines.',1292,'Le sujet thématique écrit « g0 o/o » ; le corrigé thématique et la compilation écrivent 90 %.'),
 (33,'A','La composante organique est formée en majorité de fibres de collagène I.',1293,'Le sujet thématique porte « L, composante » et « collagène L » ; le corrigé donne « La composante » et « collagène 1 », la compilation « collagène I ».')]:
    option('histo.ann.tc',id,letter,new,why)
    note('histo.ann.tc',id,[letter],'source_conflict',why+' La forme lisible est rétablie dans l’item interactif sans changer le verdict. Les originaux sont conservés.',
         [ref(filefor('histo.ann.tc','subject'),10,'Coquille du sujet thématique'),ref(filefor('histo.ann.tc','correction'),cq('histo.ann.tc',id)['correction']['page'],'Corrigé de la même série'),ref(COMP,cp,'Version complète de la même session')])
option('histo.ann.tech',8,'B',qobj('histo.ann.tech',8)['options'][1]['text'].replace('56 0 C','56 °C'),'Le zéro en exposant représente le signe de degré dans le PDF ; notation typographique normalisée.')

# Compléments qui lèvent effectivement une lacune, sans composer de verdicts
# contradictoires entre les deux éditions.
for bank,id,key,cp,number in [('histo.ann.tc',42,'ABE',1078,25),('histo.ann.tn',63,'CD',1026,30)]:
    change(bank,id,'answer',key,'Grille imprimée complète retrouvée dans la compilation, même session et cinq propositions concordantes.')
    change(bank,id,'warning','', 'La source complémentaire lève la lacune de verdict.')
    if id==42:explain(bank,id,'A','Vrai. Verdict explicite dans la compilation, Q25, p. 1078.','A sans marqueur dans le PDF thématique ; VRAI imprimé dans la compilation.')
    else:explain(bank,id,'A','Faux. Elle constitue bien la partie interne de la moelle spinale mais elle constitue la partie EXTERNE des hémisphères cérébraux et cérébelleux.','Explication en gras du corrigé thématique, confirmée par FAUX et la grille CD dans la compilation.')
    COMP_SUPPLEMENTS[(bank,id)]={'page':cp,'number':number}
    note(bank,id,['A'],'source_conflict',
         f'Le marqueur de l’item A manque dans le corrigé thématique. La compilation de la même session reprend les cinq propositions et donne explicitement la clé {key} (question {number}, p. {cp}). Cette concordance permet de rétablir la notation. Les deux éditions du corrigé sont jointes ; la numérotation thématique peut différer.',
         [ref(filefor(bank,'correction'),cq(bank,id)['correction']['page'],'Corrigé thématique incomplet'),ref(COMP,cp,'Corrigé complet, même session')],sourceVerdict='Clé complète rétablie : '+key)

horsnote('histo.ann.tc',10,'Hors note : D n’a pas de verdict dans le corrigé thématique (« ??? non dit cette année »). La compilation donne D Faux et E Vrai, tandis que le corrigé thématique donne E Faux. Aucun erratum ne permet de choisir une clé unique.')
qobj('histo.ann.tc',10)['rawAnswer']={'thematic':{'A':False,'B':True,'C':True,'D':None,'E':False},'compilation':'BCE'}
COMP_SUPPLEMENTS[('histo.ann.tc',10)]={'page':1485,'number':26}
note('histo.ann.tc',10,['D','E'],'source_conflict',
     'La compilation de juillet 2021 (p. 1485, Q26) reprend les cinq propositions, sous réserve de l’abréviation TC et de 1/I. Elle imprime BCE : D Faux et E Vrai. Le corrigé thématique p. 3 laisse D indéterminé et rejette E (« du TC réticulaire »). Retenir BC reviendrait à combiner des éditions qui se contredisent. La question reste donc hors note. Faire confirmer D et E dans la ronéo ou par un erratum de l’enseignant.',
     [ref(filefor('histo.ann.tc','correction'),3,'D sans verdict ; E Faux'),ref(COMP,1485,'Grille BCE ; D Faux et E Vrai')],sourceVerdict='Thématique : B et C vraies, D non tranché ; compilation : BCE')
horsnote('histo.ann.tn',22,'Hors note : pour E, le corrigé thématique imprime à la fois « Faux » puis « on peut dire Vrai … ??? ». La compilation retient E et la clé ACE ; l’ancienne clé thématique AC est conservée dans les remarques, sans arbitrage.',official='AC')
qobj('histo.ann.tn',22)['rawAnswer']={'thematicImported':'AC','thematicE':'Faux entre 0 et 40nm on peut dire Vrai entre 0 et 40 ???','compilation':'ACE'}
COMP_SUPPLEMENTS[('histo.ann.tn',22)]={'page':1524,'number':24}
note('histo.ann.tn',22,['E'],'source_conflict',
     'Le corrigé thématique p. 9 ne tranche pas E : il juxtapose « Faux » et « on peut dire Vrai » avec des points d’interrogation. La compilation PACES 2020–2021, Q24 p. 1524, accepte E et imprime ACE. L’ancienne clé importée AC est conservée comme trace, mais la question n’est plus notée. La ronéo TN2 p. 12 décrit 0–40 nm ; demander un erratum précisant le verdict attendu de « moins de 40 nm ».',
     [ref(filefor('histo.ann.tn','correction'),9,'Contradiction littérale de E'),ref(COMP,1524,'Même session PACES, clé ACE'),ref(SITE/'sources/revision_v4/TN2_Roneo_2026_Actualisee_660afa6a3c.pdf',12,'Largeur de la fente synaptique')],sourceVerdict='Ancienne clé AC ; compilation ACE ; contradiction ouverte')

DOC_CACHE={}
def doc(path):
    p=str(path)
    if p not in DOC_CACHE:DOC_CACHE[p]=fitz.open(p)
    return DOC_CACHE[p]
def pdf_lines(path,page,y0=0,y1=1000):
    result=[]
    for block in doc(path)[page-1].get_text('dict')['blocks']:
        for l in block.get('lines',[]):
            s=''.join(x['text'] for x in l['spans']).strip()
            if s and y0<=round(l['bbox'][1],1)<y1:
                result.append({'text':s,'rect':list(l['bbox']),'spans':l['spans'],'page':page})
    return sorted(result,key=lambda x:(round(x['rect'][1],0),x['rect'][0]))
def line_text(lines):return ' '.join(x['text'].strip() for x in lines if x['text'].strip())
def noletter(s):return re.sub(r'^[A-Z]\s*[.\-–:]\s*','',s).strip()
def block_items(block):
    result={};current=None
    for l in block['correctionLines']:
        s=l['text'].strip()
        if not s:continue
        m=re.match(r'^([A-E])\s*[.\-:]\s*(.+)',s)
        if m:current=m[1];result[current]=[]
        if current:result[current].append(l)
    return result

# Quatre questions de Techniques ont une proposition omise dans l'édition
# thématique. La version complète est retrouvée dans le sujet de la même
# session ; les identifiants des QCM restent identiques.
TECH_RESTORES={
 1:{'block':579,'subjectPage':1611,'number':21,'rect':[52,101,551,267],
    'stemY':[105,134],'ys':{'A':[134,149],'B':[149,165],'C':[165,194],'D':[194,236],'E':[236,265]},
    'mapping':{'A':'A','B':'C','C':'D','D':'E'},'added':['B'],
    'warning':'Hors note : la version complète contient cinq propositions. Le corrigé thématique à quatre propositions accepte son D (nouveau E), tandis que la compilation de la même session refuse E. Sans erratum, aucune clé commune ne peut être retenue.',
    'differences':'La proposition B (fragments de peau maintenus en survie, conditions ex vivo) est absente de la série thématique. L’ancien B devient C, l’ancien C devient D, l’ancien D devient E. Le D complet précise aussi le montage sur grille de nickel ou cuivre. Le verdict de E est explicitement opposé : Vrai dans la série thématique (ancien D), Faux dans la compilation. Les deux versions restent consultables.'},
 5:{'block':390,'subjectPage':1408,'number':16,'rect':[38,165,555,356],
    'stemY':[168,183],'ys':{'A':[183,225],'B':[225,254],'C':[254,283],'D':[283,312],'E':[312,355]},
    'mapping':{'A':'A','B':'B','C':'C','D':'E'},'added':['D'],
    'contextY':[114,155],
    'differences':'La proposition D (organes très fins déposés sur lame avant dissection) manque dans la version thématique. L’ancien D devient E. Les quatre verdicts communs concordent après ce remappage : A Faux, B Vrai, C Vrai, ancien D/nouveau E Faux. La compilation donne en outre D Vrai et la grille BCD. La clé complète BCD peut donc être rétablie sans mélange de verdicts contradictoires.'},
 6:{'block':391,'subjectPage':1408,'number':17,'rect':[38,382,555,713],
    'stemY':[386,472],'ys':{'A':[472,514],'B':[514,570],'C':[570,612],'D':[612,668],'E':[668,710]},
    'mapping':{'A':'A','B':'B','C':'C','D':'D'},'added':['E'],
    'contextY':[114,155],
    'warning':'Hors note : E (montage) est rétabli depuis le sujet complet. Le corrigé thématique donne A Faux ; la compilation de la même session donne A Vrai et la clé A. Cette opposition ne permet ni une clé hybride ni une réponse « tous faux ». Un erratum ou la ronéo de cette session est nécessaire.',
    'differences':'La proposition E sur le montage après déshydratation est absente de l’édition thématique. A à D gardent leur lettre. Le détail de A dans le corrigé thématique affirme Faux (précipitation des protéines), tandis que la compilation imprime A Vrai et la grille A pour la même proposition sur les glucides et lipides. B, C et D sont Faux dans les deux éditions ; E est Faux dans la compilation. La question complète reste hors note.'},
 7:{'block':304,'subjectPage':1312,'number':16,'rect':[38,277,555,456],
    'stemY':[280,336],'ys':{'A':[336,351],'B':[351,380],'C':[380,396],'D':[396,424],'E':[424,454]},
    'mapping':{'A':'A','B':'B','C':'D','D':'E'},'added':['C'],
    'contextY':[180,261],
    'warning':'Hors note : C (organes très fins) est rétabli, les anciens C et D deviennent D et E. Les deux corrigés de la même session s’opposent sur A et D, et la compilation classe E hors programme. Aucune clé fusionnée ne peut être retenue sans erratum.',
    'differences':'La proposition C (organes très fins déposés sur lame après dissection) manque dans l’édition thématique ; l’ancien C devient D et l’ancien D devient E. A est Vrai dans le corrigé thématique et Faux dans la compilation ; D (ancien C) est Faux dans le corrigé thématique et Vrai dans la compilation. L’ancien D/nouveau E est Vrai dans le thématique, mais « HORS PROGRAMME » dans la compilation. La grille BCD de la compilation est conservée comme document, sans transformer E en Faux.'}
}
INVALIDATIONS=[]
for id,spec in TECH_RESTORES.items():
    bank='histo.ann.tech';q=qobj(bank,id);old=copy.deepcopy(q);block=BLOCKS[spec['block']]
    subjectItems={l:pdf_lines(COMP,spec['subjectPage'],*bounds) for l,bounds in spec['ys'].items()}
    compDetails=block_items(block)
    opts=[{'id':l,'text':noletter(line_text(lines))} for l,lines in subjectItems.items()]
    stem=line_text(pdf_lines(COMP,spec['subjectPage'],*spec['stemY']))
    stem=re.sub(r'^\d+\s*[.\-:]\s*','',stem)
    change(bank,id,'question',stem,'Consigne de la version complète du sujet, même session que la série thématique.')
    change(bank,id,'options',opts,'Proposition omise rétablie, lettres alignées sur la version originale complète.')
    newexps={}
    inverse={v:k for k,v in spec['mapping'].items()}
    for l in subjectItems:
        corr=noletter(line_text(compDetails.get(l,[])))
        if id==5:newexps[l]='Compilation, p. '+str(block['page'])+' : '+corr
        else:
            x='Compilation, p. '+str(block['page'])+' : '+corr
            if l in inverse:
                oi=next(i for i in cq(bank,id)['items'] if i['id']==inverse[l])
                x+=' Édition thématique, ancien '+inverse[l]+' : '+oi['literal']+'.'
                if oi['detail']:x+=' '+oi['detail']
            else:x+=' Proposition absente de l’édition thématique.'
            newexps[l]=x
    change(bank,id,'explanations',newexps,'Commentaires des deux éditions explicitement identifiés ; aucune justification hybride.')
    q['rawAnswer']={'thematicImported':old['answer'],'thematicItemVerdicts':{i['id']:i['literal'] for i in cq(bank,id)['items']},
                    'compilationGrid':block['key'],'compilationItemVerdicts':{l:noletter(line_text(ls)) for l,ls in compDetails.items()},
                    'oldToNewLabels':spec['mapping']}
    if id==5:
        change(bank,id,'answer','BCD','Cinq verdicts exploitables ; les quatre items communs concordent avec la série thématique après remappage.')
        change(bank,id,'warning','','La version complète et son corrigé rétablissent la proposition omise et sa clé.')
    else:horsnote(bank,id,spec['warning'],official=old['answer'])
    if 'contextY' in spec:
        context=line_text(pdf_lines(COMP,spec['subjectPage'],*spec['contextY']))
        q.setdefault('sharedContexts',[]).append({'id':f'histo-v6-tech-{id}-session','title':'Contexte de la session','text':context,'images':[],
                                                'sourceFile':'Annales_compilation.pdf','sourceStartPage':spec['subjectPage'],'sourceEndPage':spec['subjectPage']})
    change(bank,id,'subjectPage',spec['subjectPage'],'Page du sujet complet désormais présenté.')
    q['sourceSubject']='Annales_compilation.pdf'
    q['sourceQuestionNumber']=spec['number']
    q['correctionPage']=block['page'];q['sourceCorrection']='Annales_compilation.pdf'
    CLEAN_SUBJECTS[(bank,id)]={'file':str(COMP),'page':spec['subjectPage'],'rect':spec['rect'],'fileLabel':'Sujet complet de la compilation, cinq propositions','sourceNumber':spec['number']}
    COMP_SUPPLEMENTS[(bank,id)]={'page':block['page'],'number':spec['number'],'block':spec['block']}
    EXTRA_EVIDENCE[(bank,id)]={'type':'restored_complete_edition','subjectItems':subjectItems,'correctionItems':compDetails,'spec':spec,
                             'oldQuestion':old,'session':SESSION[(bank,id)],'compilationOptions':block['options']}
    note(bank,id,list('ABCDE'),'source_conflict',spec['differences']+' Les réponses enregistrées à cette ancienne version doivent être effacées pour ce seul QCM dans les deux profils. Pour les divergences, demander la ronéo de la session ou un erratum précis.',
         [ref(filefor(bank,'subject'),cq(bank,id)['subject']['page'],'Version thématique abrégée'),ref(filefor(bank,'correction'),cq(bank,id)['correction']['page'],'Corrigé thématique'),ref(COMP,spec['subjectPage'],'Sujet complet, même session'),ref(COMP,block['page'],'Corrigé complet, même session')],
         sourceVerdict=('Clé complète BCD rétablie' if id==5 else 'Hors note : clés des deux éditions conservées séparément'))
    INVALIDATIONS.append({'bank':bank,'id':id,'action':'invalidateSavedResponsesForThisQuestionInBothProfiles','reason':'Version à cinq propositions rétablie ; nombre ou signification des lettres modifié.',
                          'oldToNewLabels':spec['mapping'],'addedLabels':spec['added'],'beforeOptions':old['options'],'afterOptions':copy.deepcopy(opts),
                          'beforeKey':old['answer'],'afterKey':q['answer'],'preserveOtherQuestions':True})

TECH_COURSE=SITE/'sources/revision_v4/Roneo_Techniques_Histologiques_Gouriou_2026_ACTUALISEE_fc6fab116f.pdf'
for id,letter,cp in [(1,'C',1640),(5,'A',1432)]:
    note('histo.ann.tech',id,[letter],'scientific_disagreement',
         'Le commentaire de la compilation écrit « culture in vivo » pour des cellules qui se multiplient en dehors d’un organisme. Le sujet et la ronéo de Techniques 2026 p. 8 parlent de culture in vitro ; la p. 9 réserve ex vivo aux cellules prélevées puis maintenues en survie. Cette coquille du détail est conservée dans la citation du corrigé, sans modifier son verdict. Vérifier cette terminologie dans la ronéo.',
         [ref(COMP,cp,'Commentaire imprimé « in vivo »'),ref(TECH_COURSE,8,'Cultures in vitro'),ref(TECH_COURSE,9,'Cultures ex vivo')])

# Confrontation documentaire des annales : un rapprochement lexical ne suffit
# pas. La session attendue est confrontée au titre imprimé de la compilation.
EDITION_COMPARISONS=[]
MATERIAL_VARIANTS={('histo.ann.tech',8):'La compilation donne 50 °C en B, le sujet thématique 56 °C ; D est également développé différemment.',
 ('histo.ann.tech',9):'La compilation ajoute « collées » en C et « montage » en D.',
 ('histo.ann.tech',10):'La compilation précise le montage à sec en D et ne reprend pas « avant fixation » en E.',
 ('histo.ann.tech',12):'La compilation écrit « au centre de la lame » en E, le thématique « au centre des tissus ».',
 ('histo.ann.tn',21):'La compilation précise « microscopie photonique » en A ; le thématique dit « microscopie ».',
 ('histo.ann.te',11):'La correspondance textuelle ne suffit pas à certifier l’identité des repères du triptyque : aucune migration de verdict.'}
for row in MATCHES:
    bank,id=row['bank'],row['id'];src=cq(bank,id);expected=SESSION[(bank,id)]['compilationHeader']
    candidates=[m for m in row['matches'] if expected and expected in m['heading']]
    selected=candidates[0] if candidates else None
    if bank=='histo.ann.tech' and id in TECH_RESTORES:
        spec=TECH_RESTORES[id];bl=BLOCKS[spec['block']]
        if expected not in bl['heading']:raise AssertionError(('Session des cinq items',bank,id))
        selected={'index':spec['block'],'page':bl['page'],'key':bl['key'],'heading':bl['heading'],
                  'method':'Rapprochement manuel du sujet complet et des lettres après remise en ordre ; session vérifiée.',
                  'oldToNewLabels':spec['mapping'],'addedLabels':spec['added']}
    rec={'bank':bank,'id':id,'session':SESSION[(bank,id)],'thematicQuestionNumber':src['sourceIndex'],'thematicKey':src['baselineKey'],
         'subject':{'file':str(filefor(bank,'subject')),'page':src['subject']['page']},'correction':{'file':str(filefor(bank,'correction')),'page':src['correction']['page']},
         'candidateMatches':row['matches'],'selected':selected,'items':[]}
    if not selected:
        rec['status']='no_confirmed_same_session_match';rec['reason']='Aucun bloc textuellement rapproché avec la session correspondante ; clé thématique conservée.'
    else:
        block=BLOCKS[selected['index']];details=block_items(block)
        mapping=TECH_RESTORES[id]['mapping'] if bank=='histo.ann.tech' and id in TECH_RESTORES else {i['id']:i['id'] for i in src['items']}
        for i in src['items']:
            target=mapping[i['id']]
            rec['items'].append({'sourceLabel':i['sourceLabel'],'thematicText':i['subject'],'thematicVerdict':i['literal'],
              'compilationLabel':target,'compilationText':noletter(block['options'].get(target,'')),
              'compilationDetail':noletter(line_text(details.get(target,[]))),
              'compilationKeySelected':target in block['key'],
              'thematicPositions':i['subjectLines'],'compilationPositions':[l for l in block['questionLines'] if False]})
        rec['compilation']={'file':str(COMP),'page':selected['page'],'header':selected['heading'],'key':selected['key'],'blockIndex':selected['index']}
        rec['status']='full_edition_restored' if (bank,id) in EXTRA_EVIDENCE else ('parallel_wording_variant' if (bank,id) in MATERIAL_VARIANTS else 'same_session_all_items_compared')
        rec['wordingLimit']=MATERIAL_VARIANTS.get((bank,id),'Variantes de typographie, ponctuation ou abréviation consignées dans les deux textes par item.')
        rec['keyDifference']=src['baselineKey']!=selected['key']
    EDITION_COMPARISONS.append(rec)

# Les conflits entre deux corrigés complets demeurent des notes de source : la
# clé de l'édition thématique utilisée par cette banque reste sa référence.
DISAGREEMENTS={
 'histo.ann.te':{5:'E',15:'A'},
 'histo.ann.tc':{12:'D',17:'B',20:'A',24:'A',28:'CE',30:'B',31:'DE',38:'E',43:'E',47:'CD',54:'C',58:'AC'},
 'histo.ann.tn':{11:'E',16:'C',24:'C',26:'A',28:'D',31:'C',34:'D',35:'ABE',38:'ABD',39:'DE',40:'E',44:'D',45:'A',46:'A',54:'B',62:'E'},
 'histo.ann.tech':{14:'C',19:'A',20:'E'}
}
for bank,qs in DISAGREEMENTS.items():
    for id,letters in qs.items():
        rec=next(x for x in EDITION_COMPARISONS if x['bank']==bank and x['id']==id)
        if not rec['selected']:raise AssertionError(('session non prouvée',bank,id))
        block=BLOCKS[rec['selected']['index']];src=cq(bank,id);key=qobj(bank,id)['answer']
        d=block_items(block);comparisons=[]
        for l in letters:
            item=next(i for i in src['items'] if i['id']==l)
            comparisons.append(f'{l} : thématique « {item["literal"]} » ; compilation « {noletter(line_text(d.get(l,[])))} »')
        special=''
        if (bank,id)==('histo.ann.tc',47):special=' Dans la compilation elle-même, la grille BDE contredit ses détails : C Vrai et D Faux, soit BCE, comme le thématique. La grille seule ne justifie donc pas de modifier les réponses.'
        if (bank,id)==('histo.ann.te',5):special=' Le commentaire de E dans la compilation exprime lui-même une hésitation et propose de contacter le professeur.'
        msg=(f'Les deux éditions de {rec["session"]["label"]} divergent. La banque suit le corrigé thématique p. {src["correction"]["page"]} : clé {key}. '
             f'La compilation p. {block["page"]} imprime {block["key"]}. '+' ; '.join(comparisons)+'.'+special+
             ' La clé thématique reste conservée ; demander confirmation des propositions indiquées dans la ronéo de la session ou par un erratum. Cette note constate le désaccord des documents sans créer une nouvelle clé.')
        note(bank,id,list(letters),'source_conflict',msg,[ref(filefor(bank,'correction'),src['correction']['page'],'Corrigé thématique retenu'),ref(COMP,block['page'],'Autre édition, même session')])

# Périmètres des figures vérifiés sur les pages rendues. Les repères extérieurs
# au bitmap (Noyau, axone, T/S/R, Document C) appartiennent à la figure.
FIGURES={
 ('histo.tn3',6):{'subject':[(1,[30,638,280,772])]},
 ('histo.tn3',7):{'subject':[(2,[28,94,276,302])]},
 ('histo.autotech',11):{'subject':[(3,[33,203,259,324])]},
 ('histo.ann.te',11):{'subject':[(3,[36,408,495,496])],'correction':[(3,[36,627,495,716])]},
 ('histo.ann.te',13):{'subject':[(4,[33,59,225,295])],'correction':[(4,[33,309,194,508])]},
 ('histo.ann.te',17):{'subject':[(5,[33,141,337,295])],'correction':[(5,[33,540,337,694])]},
 ('histo.ann.te',24):{'subject':[(7,[33,61,394,180])],'correction':[(8,[33,61,325,158])]},
 ('histo.ann.tc',38):{'subject':[(11,[33,309,195,414])],'correction':[(12,[33,61,195,165])]},
 ('histo.ann.tn',8):{'subject':[(4,[65,157,274,334.4])],'correction':[(4,[65,435,274,616])]},
 ('histo.ann.tn',56):{'subject':[(19,[51,423,252,559])],'correction':[(20,[51,485,252,620])]},
 ('histo.ann.tn',57):{'subject':[(20,[51,113,233,241])],'correction':[(21,[51,113,233,241])]},
 ('histo.ann.tn',60):{'subject':[(21,[51,321,325,513])],'correction':[(22,[51,334,325,526])]},
 ('histo.ann.tech',11):{'subject':[(5,[33,82,234,267])],'correction':[(5,[33,390,272,595])]},
 ('histo.ann.tech',12):{'subject':[(5,[33,82,234,267])],'correction':[(5,[33,390,272,595])]},
 ('histo.ann.tech',15):{'subject':[(6,[125,174,470,372])],'correction':[(7,[197,75,398,192])]},
 ('histo.ann.tech',21):{'subject':[(7,[33,482,429,656])],'correction':[(10,[33,95,429,269])]},
 ('histo.ann.tech',22):{'subject':[(8,[33,74,222,313])],'correction':[(9,[33,95,222,335])]},
 ('histo.ann.tech',24):{'subject':[(10,[69,85,447,341])],'correction':[(12,[69,84,447,340])]},
 ('histo.ann.tech',25):{'subject':[(10,[33,536,215,686])],'correction':[(13,[33,96,215,247])]},
 ('histo.ann.tech',30):{'subject':[(11,[150,586,445,786])],'correction':[(14,[33,450,398,696])]},
 ('histo.ann.tech',35):{'subject':[(13,[33,49,493,216])],'correction':[(16,[33,361,493,528])]}}

# Les recadrages destinés à l'affichage de la seule figure n'emportent pas
# quelques pixels du titre ou de l'item voisin. Les boîtes raster exactes
# évitent ces fragments ; les figures avec légendes vectorielles sont traitées
# explicitement ci-dessous.
EXTERNAL_LABELS={('histo.tn3',6),('histo.tn3',7),('histo.autotech',11),('histo.ann.te',11),('histo.ann.tech',11),('histo.ann.tech',12)}
for k,roles in FIGURES.items():
    for role,entries in list(roles.items()):
        if k in EXTERNAL_LABELS:continue
        adjusted=[]
        pages=json.loads((OUT/'text'/(NAMES[k[0]][0 if role=='subject' else 1]+'.json')).read_text())
        for page,r in entries:
            candidates=[z for z in pages[page-1]['images'] if fitz.Rect(z).intersects(fitz.Rect(r))]
            exact=max(candidates,key=lambda z:fitz.Rect(z).get_area())
            adjusted.append((page,exact))
        roles[role]=adjusted
FIGURES[('histo.tn3',6)]['subject']=[(1,[30.65,641.5,275,769.7])]
FIGURES[('histo.tn3',7)]['subject']=[(2,[30.65,106,272.65,299])]
FIGURES[('histo.ann.te',11)]['subject']=[(3,[35.8,411.6,523.2,492])]
FIGURES[('histo.ann.te',11)]['correction']=[(3,[35.8,630.65,523.2,711.1])]
FIGURES[('histo.ann.tech',12)]['correction']=[(5,[36,392.76,267.96,591.24])]

# Les anciennes images dites « original » étaient tantôt une copie textuelle,
# tantôt la figure du QCM suivant. Toutes les copies de texte ont maintenant
# leur rôle dans sourceCopies ; seules les vraies figures du sujet restent
# interactives. Leur attribution a été vérifiée sur les 48 fichiers existants.
for bank,meta in REVIEW['banks'].items():
    for q in meta['questions']:
        if q.get('originalImages'):
            change(bank,q['id'],'originalImages',[],
                   'Ancien champ contrôlé : remplacé par les copies authentiques complètes ; les figures du sujet sont attribuées explicitement dans images.')

for (bank,id),roles in FIGURES.items():
    pics=[]
    for j,(page,rect) in enumerate(roles['subject'],1):
        filename=f'{bank.replace(".","_")}_q{id}_figure_{j}.webp'
        dest=OUT/'assets'/filename;dest.parent.mkdir(exist_ok=True)
        pix=doc(filefor(bank,'subject'))[page-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(rect),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        im.save(dest,'WEBP',lossless=True,method=6)
        src='static/revision_v6/histologie/'+filename
        ASSETS.append({'file':str(dest),'src':src,'source':str(filefor(bank,'subject')),'page':page,'rect':rect,
                       'bank':bank,'id':id,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'pixelsEdited':False})
        pics.append(src)
    change(bank,id,'images',pics,'Recadrage authentique du sujet avec toutes les flèches et légendes ; attribution au bon QCM.')

def printed_number(obj):
    s=obj.get('stem','')
    m=re.search(r'\b(?:QCM|QRM|QRU|QUESTION)\s*(\d+)',s,re.I) or re.match(r'^\s*(\d+)\s*[.\-:]',s)
    return int(m[1]) if m else obj.get('index')
def panel(path,page,rect,label=None,number=None):
    x={'file':str(path),'page':page,'rect':[round(float(v),3) for v in rect]}
    if label:x['fileLabel']=label
    if number is not None:x['sourceNumber']=number
    return x
def positions_panels(path,lines,extra=(),label=None,number=None):
    grouped=collections.defaultdict(list)
    for l in lines:
        if l['text'].strip():grouped[l['page']].append(l['rect'])
    for page,r in extra:grouped[page].append(r)
    out=[]
    for page,rects in sorted(grouped.items()):
        pg=doc(path)[page-1]
        # Les sources sont à une colonne. Trois points de marge gardent le
        # contour et les empattements sans atteindre le QCM voisin.
        r=[max(0,min(z[0] for z in rects)-3),max(0,min(z[1] for z in rects)-3),
           min(pg.rect.width,max(z[2] for z in rects)+3),min(pg.rect.height,max(z[3] for z in rects)+3)]
        out.append(panel(path,page,r,label,number))
    return out
def original_panels(bank,id,role):
    src=cq(bank,id)[role]
    lines=src['stemLines']+[l for a in src['itemLines'].values() for l in a]
    extra=FIGURES.get((bank,id),{}).get(role,[])
    return positions_panels(filefor(bank,role),lines,extra,
       ('Sujet thématique' if role=='subject' else 'Corrigé thématique'),printed_number(src))

CONTEXTS={
 'v4-shared-histo.ann.tn-2018-case':(1,[34,133,561,210]),
 'v4-shared-histo.ann.tn-2018-biopsie':(1,[34,353,561,415]),
 'v4-shared-histo.ann.tn-2018-leucopathie':(2,[34,71,561,134]),
 'v4-shared-histo-tn-mai2019-sla':(3,[34,104,561,151]),
 'v4-shared-histo-tn-mai2019-voie-pyramidale':(3,[34,441,561,503]),
 'v4-shared-histo-tn-mai2019-nerfs-rachidiens':(4,[34,71,561,105]),
 'v4-shared-histo.ann.tn-2020-sgb':(5,[34,104,561,164]),
 'v4-shared-histo.ann.tn-2020-paresthesies':(5,[34,265,561,298])}

# Les consignes générales de décembre 2021 s'appliquent aux QCM 7 à 10.
for id in [8,9,10]:
    context=line_text(pdf_lines(filefor('histo.ann.tech','subject'),3,85,173))
    qobj('histo.ann.tech',id).setdefault('sharedContexts',[]).append({
        'id':'histo-v6-tech-dec2021-context','text':context,'images':[],
        'sourceFile':filefor('histo.ann.tech','subject').name,'sourceStartPage':3,'sourceEndPage':3})

def context_panels(bank,id):
    q=qobj(bank,id);result=[]
    for c in q.get('sharedContexts',[]):
        if c.get('id') in CONTEXTS:
            p,r=CONTEXTS[c['id']];result.append(panel(filefor(bank,'subject'),p,r,'Contexte du sujet'))
    if bank=='histo.ann.tech':
        if id in [5,6,7]:
            s=TECH_RESTORES[id];result.append(panel(COMP,s['subjectPage'],[38,s['contextY'][0]-3,555,s['contextY'][1]+3],'Consigne générale, sujet complet'))
        elif id in [8,9,10]:result.append(panel(filefor(bank,'subject'),3,[33,82,566,174],'Consigne générale de décembre 2021'))
        elif id==21:result.append(panel(filefor(bank,'subject'),7,[33,362,566,435],'Contexte de l’expérience sur les ARNm'))
    return result

def compilation_panels(block,number):
    # Reprendre aussi la consigne imprimée avant A ; la boîte du corrigé ne
    # remplace pas l'énoncé lorsque la proposition se poursuit sur une page.
    lines=[l for l in block['questionLines'] if l['text'].strip()]+[block['keyLine']]+[l for l in block['correctionLines'] if l['text'].strip()]
    first=min(block['questionLines'],key=lambda l:(l['page'],l['rect'][1]))
    before=pdf_lines(COMP,first['page'],0,first['rect'][1])
    heads=[l for l in before if re.match(r'^'+str(number)+r'\s*[.\-:]',l['text'])]
    if heads:
        top=heads[-1]['rect'][1]
        lines+= [l for l in before if l['rect'][1]>=top]
    elif (block['page'],number)==(1485,26):
        # Le 26 imprimé est un glyphe non extrait ; titre et numéro ont été
        # contrôlés sur le rendu de la page.
        lines += [l for l in before if l['rect'][1]>=70]
    else:raise AssertionError(('Consigne complémentaire introuvable',block['page'],number))
    return positions_panels(COMP,lines,label='Corrigé de la compilation, même session',number=number)

OLD_CROPS=[]
for part in ['te_tech','tc','tn']:OLD_CROPS+=json.loads((ROOT/'work/histo_v5'/part/'crops.json').read_text())
OLD_CROPS={(x['bank'],x['id']):x for x in OLD_CROPS}
CROPS=[];REUSE_CHECKS=[]
for bank,meta in REVIEW['banks'].items():
    for q in meta['questions']:
        id=q['id'];src=cq(bank,id);entry={'bank':bank,'id':id}
        if not bank.startswith('histo.ann.'):
            entry=copy.deepcopy(OLD_CROPS[(bank,id)])
            checks=[]
            for role in ['subject','correction']:
                for p in entry[role]:
                    oldfile=pathlib.Path(p['file']);newfile=filefor(bank,role)
                    identical=hashlib.sha256(oldfile.read_bytes()).digest()==hashlib.sha256(newfile.read_bytes()).digest()
                    if not identical:raise AssertionError(('PDF V5 non identique',bank,id,role))
                    p['file']=str(newfile)
                sc=q['sourceCopies'][role]
                for cap in sc['captures']:
                    f=SITE/cap['src']
                    if not f.is_file():raise AssertionError(('Capture V5 absente',f))
                    checks.append({'role':role,'capture':cap['src'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'page':cap['page']})
            entry['reuseExisting']=True
            entry['note']='Copies V5 conservées après nouvelle lecture des documents, contrôle des rectangles, des images et de l’identité des PDF sources.'
            REUSE_CHECKS.append({'bank':bank,'id':id,'sourcePdfsIdentical':True,'captures':checks})
        else:
            context=context_panels(bank,id)
            entry['subject']=context+original_panels(bank,id,'subject')
            entry['correction']=context+original_panels(bank,id,'correction')
            if (bank,id) in CLEAN_SUBJECTS:
                entry['subject']=context+[CLEAN_SUBJECTS[(bank,id)]]
                prior=original_panels(bank,id,'subject')
                for p in prior:p['fileLabel']='Ancien sujet thématique, version abrégée' if bank=='histo.ann.tech' else 'Sujet thématique déjà annoté, visible après correction'
                entry['correction']+=prior
                entry['subjectNote']='Véritable sujet complet de la même session dans la compilation. La version thématique est conservée après correction.'
            if (bank,id) in COMP_SUPPLEMENTS:
                spec=COMP_SUPPLEMENTS[(bank,id)]
                if 'block' in spec:block=BLOCKS[spec['block']]
                else:
                    keys={('histo.ann.tc',42):'ABE',('histo.ann.tn',63):'CD',('histo.ann.tc',10):'BCE',('histo.ann.tn',22):'ACE'}
                    block=next(x for x in BLOCKS if x['page']==spec['page'] and x['key']==keys[(bank,id)])
                entry['correction']+=compilation_panels(block,spec['number'])
                entry['correctionNote']='Les deux éditions sont identifiées : le corrigé thématique et la compilation de la même session. Consulter les remarques pour les différences de lettres ou de verdicts.'
            if (bank,id)==('histo.ann.tech',12):
                # La figure commune est sur la page du QCM précédent : ne pas
                # fusionner l'ensemble de cette page avec les items du Q12.
                p,r=FIGURES[(bank,id)]['subject'][0]
                own=positions_panels(filefor(bank,'subject'),src['subject']['stemLines']+[l for v in src['subject']['itemLines'].values() for l in v],label='Sujet thématique',number=printed_number(src['subject']))
                entry['subject']=[panel(filefor(bank,'subject'),p,r,'Figure commune aux QCM 16 et 17')]+own
                p,r=FIGURES[(bank,id)]['correction'][0]
                own=positions_panels(filefor(bank,'correction'),src['correction']['stemLines']+[l for v in src['correction']['itemLines'].values() for l in v],label='Corrigé thématique',number=printed_number(src['correction']))
                entry['correction']=[panel(filefor(bank,'correction'),p,r,'Figure commune du corrigé')]+own
            # Pages de début et de fin, y compris les figures qui précèdent les
            # items, réconciliées avec le contenu réellement capturé.
            if (bank,id) not in CLEAN_SUBJECTS:
                primary=original_panels(bank,id,'subject')
                change(bank,id,'subjectPage',min(x['page'] for x in primary),'Début réel du sujet, figures comprises.')
                q['sourceEndPage']=max(x['page'] for x in primary)
            q['correctionEndPage']=max(x['page'] for x in original_panels(bank,id,'correction'))
            q['sourceQuestionNumber']=printed_number(src['subject']) if (bank,id) not in EXTRA_EVIDENCE else TECH_RESTORES[id]['number']
        CROPS.append(entry)

# Variantes de formulation, de contexte ou de figure : elles interdisent une
# transposition automatique des grilles, même si l'année et plusieurs phrases
# coïncident.
VARIANT_NOTES={
 ('histo.ann.te',11):('DE',1245,'La figure est différente : le thématique emploie un triptyque horizontal coloré T/S/R, tandis que la compilation présente un triptyque vertical en niveaux de gris R/S/T, avec un autre dessin pour T. Les repères et leur morphologie ont été vus dans les deux éditions. Les clés BCDE et BC concernent donc des versions graphiques distinctes ; la clé BCDE du corrigé thématique est conservée. Il ne faut pas transférer les verdicts D/E de la compilation sur cette image.'),
 ('histo.ann.tech',8):('ABD',1343,'Les éditions ont été adaptées différemment : le thématique mentionne le montage « non vu cette année », donne 56 °C en B et abrège D ; la compilation donne 50 °C en B et détaille le déparaffinage, la réhydratation et le montage en D. A conserve la même formulation sur la préservation des « structures biologiques », mais est Vrai dans le thématique et Faux dans la compilation, qui remplace ce mot par « histologiques » dans son commentaire. La clé thématique AD est conservée.'),
 ('histo.ann.tech',9):('ACD',1344,'Les deux versions visent des coupes en congélation. A a le même texte mais est Vrai dans le thématique, Faux dans la compilation (« structures histologiques » dans le commentaire). C est Faux dans le thématique et Vrai dans la compilation, laquelle ajoute « collées » ; D y précise aussi le montage. La clé thématique ABD reste la référence de cette version, sans transposition de BCD.'),
 ('histo.ann.tech',10):('ABCDE',1345,'Le contexte expérimental change : le thématique demande une coupe en résine, alors que la compilation demande un examen extemporané. D est développé différemment et E ne reprend pas la restriction « avant la fixation » dans la compilation. Les grilles AE et BCD ne sont donc pas interchangeables. La question interactive et sa clé AE suivent la version thématique en résine.'),
 ('histo.ann.tech',12):('DE',1242,'La microphotographie commune a été rapprochée : mêmes tubes, même cadrage et barre de 100 µm, mais reproduction en gris dans la compilation. D porte Vrai dans le thématique et « FAUX ? » dans la compilation. E diffère aussi entre « au centre des tissus » et « au centre de la lame ». La clé thématique ACD est conservée ; l’interrogation imprimée dans l’autre édition ne permet pas de supprimer D.'),
 ('histo.ann.tn',21):('A',1524,'La formulation de A diffère : le thématique dit « observable en microscopie par méthode de Golgi » et le retient, tandis que la compilation ajoute « photonique », le rejette et écrit « ÉLECTRONIQUE » dans son commentaire. La clé thématique AB est conservée ; la variante de formulation et de correction ne justifie pas de transférer la grille B.')}
for (bank,id),(letters,page,msg) in VARIANT_NOTES.items():
    note(bank,id,list(letters),'source_conflict',msg+' Pour ce point précis, consulter la ronéo de la session ou demander un erratum en précisant l’édition utilisée.',
         [ref(filefor(bank,'subject'),cq(bank,id)['subject']['page'],'Version thématique du sujet'),ref(filefor(bank,'correction'),cq(bank,id)['correction']['page'],'Corrigé thématique retenu'),ref(COMP,page,'Variante de la compilation')])
    rec=next(x for x in EDITION_COMPARISONS if (x['bank'],x['id'])==(bank,id))
    rec['status']='different_figure' if bank=='histo.ann.te' else ('different_experimental_context' if id==10 and bank=='histo.ann.tech' else 'parallel_wording_variant')
    rec['wordingLimit']=msg

def split_labels(lines):
    result={};current=None
    for l in lines:
        m=re.match(r'^([A-J])\s*[.\-:]\s*',l['text'].strip())
        if m:current=m[1];result[current]=[]
        if current:result[current].append(l)
    return result
for rec in EDITION_COMPARISONS:
    rec['thematicOrdinal']=rec.pop('thematicQuestionNumber')
    rec['thematicQuestionNumber']=printed_number(cq(rec['bank'],rec['id'])['subject'])
    if (rec['bank'],rec['id']) in COMP_SUPPLEMENTS:rec['compilationQuestionNumber']=COMP_SUPPLEMENTS[(rec['bank'],rec['id'])]['number']
    if not rec['selected']:continue
    block=BLOCKS[rec['selected']['index']];groups=split_labels(block['questionLines'])
    for i in rec['items']:
        i['compilationPositions']=groups.get(i['compilationLabel'],[])
    if (rec['bank'],rec['id']) in FIGURES:
        rec['supplementalFigureComparison']=(
            'Different figure inspected; no key transfer' if (rec['bank'],rec['id'])==('histo.ann.te',11) else
            'Same diagram and all H/J/K/L/M labels inspected' if (rec['bank'],rec['id'])==('histo.ann.tc',38) else
            'Same microphotograph, grayscale reproduction inspected on p.1241' if rec['bank']=='histo.ann.tech' and rec['id'] in [11,12] else
            'Primary subject and primary correction figures inspected; compilation image not used to alter the key')

def compact_lines(lines):
    return [{'page':x['page'],'text':x['text'],'rect':[round(v,3) for v in x['rect']],
             'runs':[{'text':s['text'],'font':s.get('font'),'size':s.get('size'),'color':s.get('color'),'flags':s.get('flags')} for s in x.get('spans',[])]} for x in lines if x['text'].strip()]
def evidence(path,label,lines,txt=None):
    return {'file':str(path),'label':label,'text':line_text(lines) if txt is None else txt,'positions':compact_lines(lines)}
def inpanels(path,line,panels,tol=1):
    r=fitz.Rect(line['rect'])
    return any(p['file']==str(path) and p['page']==line['page'] and
               (fitz.Rect(p['rect'])+(-tol,-tol,tol,tol)).contains(r) for p in panels)

AUDIT=[];GEOMETRY=[];SUBJECT_DELTAS=[];REFERENCE_GAPS=[]
CROPMAP={(x['bank'],x['id']):x for x in CROPS}
FIGURE_PAGES=json.loads((OUT/'figure_pages.json').read_text())
VISUAL_PAGES={(x['source'],x['page']) for x in FIGURE_PAGES}
LEGACY_ASSETS=json.loads((OUT/'legacy_assets.json').read_text())
for bank,meta in REVIEW['banks'].items():
    if [x['id'] for x in meta['questions']]!=[x['id'] for x in BASE[bank]['questions']]:raise AssertionError(('IDs',bank))
    for q in meta['questions']:
        id=q['id'];src=cq(bank,id);base=next(x for x in BASE[bank]['questions'] if x['id']==id);crop=CROPMAP[(bank,id)]
        if q.get('weight')!=base.get('weight'):raise AssertionError(('Coefficient',bank,id))
        if q.get('reviewNotes',[])[:len(base.get('reviewNotes',[]))]!=base.get('reviewNotes',[]):raise AssertionError(('Notes anciennes modifiées',bank,id))
        letters=[o['id'] for o in q['options']]
        if len(letters)!=len(set(letters)) or any(l not in letters for l in q['answer']):raise AssertionError(('Clé/lettres',bank,id))
        graded=bool(q['answer']) or q.get('answerIsEmpty') is True
        items=[]
        for o in q['options']:
            l=o['id'];status='verified_literal';meaning='Verdict Vrai/Faux du corrigé de référence.'
            if (bank,id) in EXTRA_EVIDENCE:
                e=EXTRA_EVIDENCE[(bank,id)];spec=e['spec'];inverse={v:k for k,v in spec['mapping'].items()}
                oldlabel=inverse.get(l);olditem=next((i for i in src['items'] if i['id']==oldlabel),None)
                sl=e['subjectItems'][l];cl=e['correctionItems'][l]
                se=[evidence(COMP,l,sl,o['text'])];ce=[evidence(COMP,l,cl)]
                if olditem:
                    se.append(evidence(filefor(bank,'subject'),oldlabel,olditem['subjectLines'],olditem['subject']))
                    ce.append(evidence(filefor(bank,'correction'),oldlabel,olditem['correctionLines'],olditem['correctionRaw']))
                literal=noletter(line_text(cl));truth=True if re.match(r'^VRAI\b',literal,re.I) else False if re.match(r'^FAUX\b',literal,re.I) else None
                detail=literal;status='restored_from_full_same_session_edition' if id==5 else 'documented_editions_question_ungraded'
                if oldlabel is None:status+='; previously_missing_item'
                oldtext=next((x['text'] for x in base['options'] if x['id']==oldlabel),None)
            else:
                it=next(i for i in src['items'] if i['id']==l)
                se=[evidence(filefor(bank,'subject'),it['sourceLabel'],it['subjectLines'],it['subject'])]
                ce=[evidence(filefor(bank,'correction'),it['correctionLabel'],it['correctionLines'],it['correctionRaw'])]
                literal=it['literal'];truth=it['truth'];detail=it['detail'];oldtext=next((x['text'] for x in base['options'] if x['id']==l),None)
                if (bank,id)==('histo.autotech',12) and l=='D':
                    literal='Vrai (run gras immédiatement après « patient »)';truth=True
                    detail='on les maintient ainsi afin d’être réinjectées après traitement ou modif génétiques'
                    meaning='Le run gras Vrai est distinct, malgré la concaténation patientVrai dans le texte extrait.'
                if (bank,id)==('histo.tn2',7) and l in 'ABCD':
                    literal=None;truth=None;status='verified_by_unique_explicit_selection'
                    meaning='Aucun V/F littéral pour cet ordre. E seul porte Vrai ; non-sélection de cet item déduite de la réponse unique E.'
                if (bank,id)==('histo.ann.tn',9):meaning='Le corrigé emploie ici Vrai pour la réponse inexacte à sélectionner (C), et Faux pour les distracteurs. Ces marqueurs ne sont pas inversés une seconde fois.'
                elif src.get('invert'):meaning='La consigne demande la proposition inexacte : sélection de l’item explicitement Faux.'
                if (bank,id) in [('histo.ann.tc',42),('histo.ann.tn',63)] and l=='A':
                    spec=COMP_SUPPLEMENTS[(bank,id)];rec=next(x for x in EDITION_COMPARISONS if x['bank']==bank and x['id']==id)
                    bl=BLOCKS[rec['selected']['index']];cls=block_items(bl)[l]
                    ce.append(evidence(COMP,l,cls));literal=noletter(line_text(cls));truth=bank=='histo.ann.tc';status='missing_thematic_marker_restored_from_same_session'
                if (bank,id)==('histo.ann.tc',10) and l in 'DE':status='unresolved_source_conflict';truth=None if l=='D' else truth
                if (bank,id)==('histo.ann.tn',22) and l=='E':status='unresolved_literal_true_false_conflict';truth=None
                if (bank,id) in [('histo.ann.tn',30),('histo.ann.tn',45)]:
                    clean=CLEAN_SUBJECTS[(bank,id)];ls=pdf_lines(COMP,clean['page'],clean['rect'][1],clean['rect'][3]);g=split_labels(ls)
                    se.insert(0,evidence(COMP,l,g[l],noletter(line_text(g[l]))))
                    if l==('A' if id==30 else 'C'):status='answer_annotation_removed_using_authentic_clean_subject'
            if o['text']!=oldtext:SUBJECT_DELTAS.append({'bank':bank,'id':id,'item':l,'before':oldtext,'after':o['text']})
            items.append({'id':l,'siteText':o['text'],'baselineText':oldtext,'subjectEvidence':se,'correctionEvidence':ce,
                         'literalVerdict':literal,'literalTruthValue':truth,'verdictMeaning':meaning,'sourceDetail':detail,
                         'siteDetail':q['explanations'].get(l,''),'selectedByFinalKey':l in q['answer'] if graded else None,
                         'status':status,'sourceRead':True})
        gaps=[]
        for role in ['subject','correction']:
            ls=src[role]['stemLines']+[l for v in src[role]['itemLines'].values() for l in v]
            target=crop['correction'] if role=='subject' and (bank,id) in CLEAN_SUBJECTS else crop[role]
            for line in ls:
                if not inpanels(filefor(bank,role),line,target):gaps.append({'role':role,'line':line['text'],'page':line['page']})
        if (bank,id) in CLEAN_SUBJECTS:
            p=CLEAN_SUBJECTS[(bank,id)]
            for line in pdf_lines(COMP,p['page'],p['rect'][1],p['rect'][3]):
                if not inpanels(COMP,line,crop['subject']):gaps.append({'role':'cleanSubject','line':line['text'],'page':line['page']})
        for role in ['subject','correction']:
            for p in crop[role]:
                r=fitz.Rect(p['rect']);page=doc(p['file'])[p['page']-1]
                if r.is_empty or not (page.rect+(-.1,-.1,.1,.1)).contains(r):gaps.append({'role':role,'badRectangle':p})
        GEOMETRY.append({'bank':bank,'id':id,'gaps':gaps,'allPrimaryTextIncluded':not gaps,'subjectPanels':len(crop['subject']),'correctionPanels':len(crop['correction'])})
        if gaps:raise AssertionError(('Cadrage incomplet',bank,id,gaps))
        for n in q.get('reviewNotes',[]):
            for r in n.get('refs',[]):
                h=r.get('href','').split('#')[0]
                if h.startswith('sources/') and not (SITE/h).exists():REFERENCE_GAPS.append({'bank':bank,'id':id,'noteId':n.get('noteId'),'href':h})
        sourcefigs=[]
        for role in ['subject','correction']:
            path=filefor(bank,role);pages=json.loads((OUT/'text'/(NAMES[bank][role=='correction']+'.json')).read_text())
            original=original_panels(bank,id,role) if bank.startswith('histo.ann.') else crop[role]
            for p in original:
                for r in pages[p['page']-1]['images']:
                    area=fitz.Rect(r).get_area()
                    if area>150 and (fitz.Rect(r)&fitz.Rect(p['rect'])).get_area()/area>.9:
                        sourcefigs.append({'role':role,'file':str(path),'page':p['page'],'rect':r,'pageViewed':(str(path),p['page']) in VISUAL_PAGES})
        rec=next((x for x in EDITION_COMPARISONS if x['bank']==bank and x['id']==id),None)
        AUDIT.append({'bank':bank,'id':id,'status':'verified_with_documented_limits' if not graded or q.get('reviewNotes') else 'verified',
          'subject':{'file':str(filefor(bank,'subject')),'printedQuestionNumber':printed_number(src['subject']),'questionOrdinalInThematicBank':src['sourceIndex'],
                     'literalStem':src['subject']['stem'],'positions':compact_lines(src['subject']['stemLines']),'siteStem':q['question'],
                     'sharedContexts':q.get('sharedContexts',[]),'context':q.get('context',''),'completeSubjectEditionRestored':(bank,id) in EXTRA_EVIDENCE},
          'correction':{'file':str(filefor(bank,'correction')),'printedQuestionNumber':printed_number(src['correction']),
                        'questionOrdinalInThematicBank':src['correctionIndex'],'literalStem':src['correction']['stem'],'positions':compact_lines(src['correction']['stemLines'])},
          'items':items,'key':{'before':base['answer'],'after':q['answer'],'graded':graded,'allFalseExplicit':q.get('answerIsEmpty') is True,
                              'officialAnswer':q.get('officialAnswer'),'rawAnswer':q.get('rawAnswer'),
                              'machineCandidateBeforeManualInterpretation':src['candidateKey'],'warning':q.get('warning','')},
          'session':SESSION.get((bank,id)),'compilationComparison':rec,
          'figures':{'sourceImages':sourcefigs,'interactiveAssets':[x for x in ASSETS if x['bank']==bank and x['id']==id],
                     'legacyImageReferencesInspected':[x for x in LEGACY_ASSETS if x['bank']==bank and x['id']==id]},
          'copies':{'subjectClean':True,'correctionAvailable':True,'reuseExisting':crop.get('reuseExisting',False),'subjectPanels':len(crop['subject']),
                    'correctionPanels':len(crop['correction']),'allPrimaryTextGeometricallyIncluded':True,
                    'annotatedThematicSubjectOnlyAfterCorrection':(bank,id) in [('histo.ann.tn',30),('histo.ann.tn',45)]},
          'preservedReviewNoteIds':[n.get('noteId') for n in base.get('reviewNotes',[])],
          'newReviewNoteIds':[n.get('noteId') for n in q.get('reviewNotes',[])[len(base.get('reviewNotes',[])):]],
          'preparationDecisions':[x for x in FIXES if x['bank']==bank and x['id']==id]})

if REFERENCE_GAPS:raise AssertionError(('Références locales absentes',REFERENCE_GAPS))
if len(AUDIT)!=321 or sum(len(x['items']) for x in AUDIT)!=1614:raise AssertionError('Couverture inattendue')

HORSNOTE=[{'bank':x['bank'],'id':x['id'],'reason':x['key']['warning']} for x in AUDIT if not x['key']['graded']]
SUMMARY={
 'banks':13,'questions':321,'baselineItems':1609,'reviewedItems':1614,
 'autotestQuestions':128,'autotestItems':649,'annalesQuestions':193,'annalesItems':965,
 'gradedQuestions':sum(x['key']['graded'] for x in AUDIT),'ungradedQuestions':len(HORSNOTE),
 'explicitAllFalseQuestions':[{'bank':x['bank'],'id':x['id']} for x in AUDIT if x['key']['allFalseExplicit']],
 'cleanSubjectCopies':321,'correctionCopies':321,'annotatedSubjectCopiesRetainedAfterCorrection':2,
 'reusedV5QuestionCopies':len(REUSE_CHECKS),'newInteractiveFigureAssets':len(ASSETS),
 'legacyImageReferencesActuallyViewed':len(LEGACY_ASSETS),'primaryFigurePagesActuallyViewed':len(VISUAL_PAGES),
 'newInteractiveFigureAssetsActuallyViewed':21,
 'allFinalCopiesIndividuallyViewed':False,
 'visualMethod':'Les 39 pages sources contenant les figures, les 48 anciens fichiers graphiques et les 21 nouvelles figures ont été vus. Les copies finales ont un contrôle textuel et géométrique exhaustif ; elles ne sont pas toutes déclarées vues individuellement.',
 'compilationComparisonStatuses':dict(collections.Counter(x['status'] for x in EDITION_COMPARISONS)),
 'literalItemStatuses':dict(collections.Counter(i['status'] for x in AUDIT for i in x['items'])),
 'preservedReviewNotes':sum(len(q.get('reviewNotes',[])) for b in NAMES for q in BASE[b]['questions']),
 'newReviewNotes':sum(len(q.get('reviewNotes',[])) for v in REVIEW['banks'].values() for q in v['questions'])-sum(len(q.get('reviewNotes',[])) for b in NAMES for q in BASE[b]['questions']),
 'newQuestionIds':[],'restoredItemCount':5,
 'responseInvalidationQuestions':[{'bank':x['bank'],'id':x['id']} for x in INVALIDATIONS],
 'bankCoverage':[{'bank':b,'questions':len(v['questions']),'items':sum(len(q['options']) for q in v['questions'])} for b,v in REVIEW['banks'].items()]}

MISSING=[]
for item in HORSNOTE:
    bank,id=item['bank'],item['id'];a=next(x for x in AUDIT if x['bank']==bank and x['id']==id)
    MISSING.append({'kind':'official_arbitration_required','priority':'grading','bank':bank,'ids':[id],
      'needed':'Ronéo de la session ou erratum explicite identifiant les propositions concernées et l’édition complète du QCM.',
      'reason':item['reason'],'sourcesAlreadyAvailable':[str(filefor(bank,'subject')),str(filefor(bank,'correction')),str(COMP)],
      'searchesPerformed':'Documents thématiques sujet/corrigé relus, originaux du premier envoi confrontés, compilation UE5 recherchée sur l’ensemble des propositions et la session, deux éditions conservées dans les copies.',
      'session':SESSION[(bank,id)],'resolution':'Question conservée et consultable, corrigés disponibles après validation, aucune note calculée.'})
MISSING.append({'kind':'source_figure_quality','priority':'optional','bank':'histo.tn1','ids':[13],
 'needed':'Version complète du schéma explicatif de myélinisation dans le corrigé TN1, si elle existe.',
 'reason':'Les légendes à gauche sont déjà rognées dans le fichier EMF inclus dans le Word original. Le PDF et la capture reproduisent cette limite ; aucun texte graphique absent n’a été inventé.',
 'searchesPerformed':'Word du premier envoi, Word conservé dans le site, extraction de son EMF, rendu de l’EMF et comparaison avec le PDF V5.',
 'resolution':'Aucun impact sur les cinq propositions ou leur clé. La figure explicative authentique reste dans la copie du corrigé.'})
disputed=[{'bank':x['bank'],'id':x['id'],'session':x['session'],'primaryKey':qobj(x['bank'],x['id'])['answer'],
            'compilationPage':x.get('compilation',{}).get('page'),'status':x['status']}
          for x in EDITION_COMPARISONS if x.get('keyDifference') and (x['bank'],x['id']) not in COMP_SUPPLEMENTS]
MISSING.append({'kind':'edition_errata_optional','priority':'clarification','questions':disputed,
 'needed':'Pour les divergences indiquées dans les remarques après correction, une ronéo ou un erratum de la bonne session et de la bonne version serait utile.',
 'reason':'Plusieurs corrigés thématiques complets divergent de la compilation. Certains textes, contextes et schémas ont aussi été adaptés ; les deux grilles ne sont pas interchangeables.',
 'resolution':'La clé du corrigé thématique est conservée quand elle est complète ; aucune décision scientifique personnelle ne réécrit cette clé.'})

SOURCE_INVENTORY={'primaryExamPdfs':json.loads((OUT/'sources_examined.json').read_text()),
 'firstUploadComparisons':json.loads((OUT/'old_original_comparison.json').read_text()),
 'compilation':{'file':str(COMP),'sha256':hashlib.sha256(COMP.read_bytes()).hexdigest(),'pages':1660,
                'ue5TextIndexedPages':[989,1660],'sameSessionComparisons':sum(x['selected'] is not None for x in EDITION_COMPARISONS),
                'individuallyViewedPages':[1026,1078,1159,1241,1245,1275,1312,1318,1342,1408,1432,1433,1485,1524,1611,1640],
                'method':'Extraction sur toute la section UE5 ; rapprochement de toutes les propositions et de la session ; contrôle manuel des compléments utilisés pour réparer, des divergences et des variantes de formulation. La totalité des 672 pages UE5 n’est pas déclarée visualisée.'},
 'referencePagesReread':json.loads((OUT/'note_reference_pages.json').read_text()),
 'additionalReferencePagesReread':[{'file':str(TECH_COURSE),'page':p,'text':doc(TECH_COURSE)[p-1].get_text()} for p in [8,9]],
 'primaryFigurePagesViewed':FIGURE_PAGES,
 'sourceManifestNote':'Tous les PDF et les Word employés sont déjà conservés dans output/site/sources ; aucun nouveau PDF à empaqueter.'}

# La seule différence binaire parmi les 26 originaux d'examens se trouve dans
# la répartition des runs du Word de correction TN3, pas dans son contenu.
import zipfile,xml.etree.ElementTree as ET
oldtn=ROOT/'work/histo_v5/old_source/CORRECTION AUTOTEST TN3.docx'
newtn=SITE/'sources/histo_v5/tn3_correction.docx'
def docx_content(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
        wt='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
        tx=''.join(x.text or '' for x in root.iter(wt))
        imgs=sorted(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/'))
    return {'visibleText':tx,'textSha256':hashlib.sha256(tx.encode()).hexdigest(),'imageSha256':imgs}
oldc,newc=docx_content(oldtn),docx_content(newtn)
if oldc!=newc:raise AssertionError('Le contenu TN3 diffère au-delà de la répartition des runs')
SOURCE_INVENTORY['tn3WordComparison']={'firstUpload':str(oldtn),'packagedOriginal':str(newtn),'sameVisibleText':True,'sameMedia':True,
 'textSha256':oldc['textSha256'],'imageSha256':oldc['imageSha256'],'difference':'Seule la répartition du texte entre runs Word diffère (notamment Vrai et son espace).'}

OUTPUTS={'reviewed.json':REVIEW,'audit.json':AUDIT,'crops.json':CROPS,'missing.json':MISSING,
         'source_manifest.json':[],'asset_manifest.json':ASSETS,'source_inventory.json':SOURCE_INVENTORY,
         'coverage_summary.json':SUMMARY,'edition_comparisons.json':EDITION_COMPARISONS,'geometry_checks.json':GEOMETRY,
         'response_invalidations.json':INVALIDATIONS,'changes.json':FIXES,'subject_item_changes.json':SUBJECT_DELTAS,
         'reuse_checks.json':REUSE_CHECKS}
for filename,obj in OUTPUTS.items():dump(filename,obj)

CORE_HASHES={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['reviewed.json','crops.json']}
rows='\n'.join(f'| {x["bank"]} | {x["questions"]} | {x["items"]} |' for x in SUMMARY['bankCoverage'])
conflicts='\n'.join(f'- **{x["bank"]}, Q{x["id"]}** : {x["reason"]}' for x in HORSNOTE)
report=f'''# Histologie — préparation V6

## État du lot

**Feu vert préparateur pour une vérification indépendante.** Ce lot porte sur les 13 banques d’histologie, 321 QCM et 1 614 propositions. Il ne constitue pas la validation du second agent et ne modifie pas le site.

Les 128 QCM d’autotests (649 propositions) ont été relus depuis leurs sujets et corrigés ; leurs 128 paires de copies V5 sont conservées après contrôle des textes, des rectangles, des figures, de l’identité des PDF et de l’existence des captures. Les 193 QCM d’annales ont été relus à frais nouveaux, sujet et corrigé, avec leurs figures et contextes. Leur total passe de 960 à 965 propositions par cinq restitutions documentées. Aucun QCM nouveau, aucun ID nouveau et aucune annale antérieure à 2015 ne sont ajoutés.

| Banque | QCM | Propositions après préparation |
|---|---:|---:|
{rows}

## Résultat de notation

Le lot contient **316 QCM notables et cinq QCM hors note**. L’autotest TC3 Q17 possède une clé explicitement « tous faux » : `answerIsEmpty: true` et `allowNoAnswer: true` sont conservés. Les cinq questions hors note ont `answer: ""` sans ces drapeaux ; leurs sources et leurs clés documentaires restent accessibles après correction.

{conflicts}

Les coefficients, les identifiants et l’ordre des banques et des questions viennent de la V5. Ce lot ne touche ni au barème 10–5–2–0 ramené sur 20, ni aux profils. **{SUMMARY['preservedReviewNotes']} notes V4/V5 sont conservées intégralement**, et {SUMMARY['newReviewNotes']} notes précises sont ajoutées. Les divergences scientifiques et documentaires apparaissent après correction avec leurs sources ; elles ne sont pas transformées en nouvelles clés personnelles.

## Réparations démontrées

### Propositions et clés

- **TC annales Q5** : le D sans tiret était fusionné avec C. Les deux originaux thématiques p. 2 contiennent cinq propositions distinctes et donnent A, C et D vrais. D est rétabli ; la clé passe de AC à ACD et la justification de C n’absorbe plus D.
- **TC annales Q42** : le thématique p. 14 omet le verdict A. La compilation de la même session, Q25 p. 1078, donne A Vrai et la grille ABE. Les cinq propositions, la session et les deux numérotations sont consignées dans l’audit. La notation ABE est rétablie.
- **TN annales Q63** : le thématique p. 23 présente une explication en gras sans marqueur A. La compilation S1 2025–2026, Q30 p. 1026, imprime A Faux et CD. Les cinq propositions sont appariées ; la clé CD et l’explication complète de A sont rétablies.
- **Techniques annales Q1, Q5, Q6 et Q7** : les versions thématiques n’ont que quatre propositions ; les vrais sujets de la même session en ont cinq. Les versions complètes sont rétablies avec preuve par item et session. Q5 devient BCD, puisque les quatre verdicts communs concordent après remappage. Q1, Q6 et Q7 restent hors note en raison des oppositions explicites entre les deux corrigés. Les deux éditions sont conservées, avec leurs lettres et leurs détails, sans clé hybride.
- **TC Q10** : l’item D reste indéterminé dans le thématique ; la compilation s’oppose en outre sur E. Aucun mélange de D Faux de la compilation et E Faux du thématique n’est fait.
- **TN Q22** : la contradiction ouverte « Faux … on peut dire Vrai … ??? » de E est tracée, avec l’ancienne clé AC, la grille ACE de la compilation et la ronéo TN2 p. 12. La question passe effectivement hors note.

### Textes, contextes et images

- Des consignes du QCM suivant avaient contaminé Techniques Q26 E et Q27 E ; elles sont retirées des propositions. Des commentaires voisins sont également retirés des explications de TC Q40–43, TN Q7 et Techniques Q26–27.
- **TN Q30 A et Q45 C** contenaient déjà « Faux » dans le PDF intitulé sujet. Le vrai sujet propre a été retrouvé dans la compilation, respectivement p. 1318 et p. 1275. Le texte interactif et la copie avant correction viennent de ces pages ; les PDF thématiques annotés sont conservés après correction, sans effacer leurs pixels.
- **TC Q31 D et Q33 A** : les coquilles « g0 o/o », « L, composante » et « collagène L » sont normalisées par concordance du corrigé de la même série et de la compilation. Techniques Q8 B retrouve le signe degré de 56 °C.
- Les consignes générales des Techniques de décembre 2020 et décembre 2021 sont jointes aux QCM concernés. Les vignettes cliniques partagées de TN, le contexte de l’expérience sur les ARNm et les consignes à cheval sur deux pages sont conservés.
- **21 figures interactives authentiques** sont livrées dans `assets/`. Elles gardent les flèches, les repères extérieurs et les légendes. Le document 4 de TN3 Q6 inclut Noyau/axone ; le Document C de l’autotest Techniques est complet ; le triptyque T/S/R garde son cadre et ses lettres. Les anciennes images attribuées au QCM voisin (TE10, TC37, TN55, TN59, Techniques16/29) sont supprimées de ces mauvaises associations. Les anciennes captures textuelles `originalImages` sont remplacées par les menus de copies complètes.
- **Techniques Q30** commence réellement p. 11 avec sa figure, puis ses items continuent p. 12. Son corrigé occupe les p. 14–15. Ces pages sont toutes comprises dans les panneaux.

## Remappages et réponses sauvegardées

Le registre machine complet est `response_invalidations.json`. **Invalider seulement les réponses sauvegardées des quatre QCM ci-dessous, dans les deux profils**, car une lettre sauvegardée pourrait maintenant désigner un autre énoncé. Ne pas déplacer automatiquement les réponses et ne pas effacer les autres QCM.

| Banque / ID | Anciennes lettres vers nouvelles | Proposition ajoutée |
|---|---|---|
| histo.ann.tech / 1 | A→A ; B→C ; C→D ; D→E | B |
| histo.ann.tech / 5 | A→A ; B→B ; C→C ; D→E | D |
| histo.ann.tech / 6 | A→A ; B→B ; C→C ; D→D | E |
| histo.ann.tech / 7 | A→A ; B→B ; C→D ; D→E | C |

TC Q5 reçoit un D distinct mais ne change pas le sens des lettres existantes ; son C cesse simplement de contenir le texte de D. Ce cas est tracé dans `changes.json` et n’est pas inclus dans les quatre invalidations demandées par l’intégrateur.

## Confrontation des éditions

La compilation a été indexée sur toute la section UE5, p. 989–1660. {SOURCE_INVENTORY['compilation']['sameSessionComparisons']} rapprochements de la même session sont documentés, en comparant toutes les propositions disponibles et leurs lettres ; les changements de notation ont été confirmés manuellement sur les pages originales.

La session n’a pas été déduite d’une phrase semblable. TN Q11 est rapproché de 2019–2020 p. 1576, et non de la réutilisation en 2023–2024. Les candidats d’une autre session pour TN Q1, TN Q33 et Techniques Q24 ne permettent pas de transférer leur clé. **TE Q11** a une figure différente dans la compilation : les clés BCDE et BC ne décrivent pas le même triptyque. **Techniques Q10** change de contexte, coupe en résine contre examen extemporané ; les clés AE et BCD ne sont pas interchangeables. Les autres variantes de mots, de températures, de consignes ou d’interrogations imprimées figurent dans `edition_comparisons.json` et dans les remarques concernées.

Pour les corrigés thématiques complets qui divergent d’une autre édition, la clé thématique reste la référence de cette banque. Les réserves précisent les items, les pages, la session et le texte des deux verdicts. TC Q47 illustre aussi une grille BDE contredisant les détails BCE de la compilation elle-même ; la clé thématique BCE est conservée.

## Sources et vérification réellement effectuée

Les 26 PDF principaux ont été relus ; leurs originaux ont été confrontés au premier envoi. **25 originaux sur 26 sont identiques octet pour octet**. Pour le Word de correction TN3, le texte visible et les deux médias sont identiques ; seule la répartition entre runs Word diffère. Les anciennes notes ont été recontrôlées sur leurs 64 pages de référence, auxquelles s’ajoutent les p. 8–9 de la ronéo de Techniques pour la coquille « in vivo » dans certains commentaires de la compilation.

Les **39 pages sources contenant les figures**, les **48 anciens fichiers graphiques référencés** et les **21 nouvelles figures** ont réellement été vus. Les pages de compilation déterminantes et les pages comportant une annotation, un marqueur absent ou une ambiguïté typographique ont été rendues et examinées. Les 321 paires de copies ont un contrôle textuel et géométrique exhaustif : aucun texte de proposition ou de correction attendu ne reste hors de ses panneaux. Les 128 paires de copies V5 ont aussi une preuve d’identité des PDF et des empreintes des captures existantes.

**Toutes les captures finales ne sont pas annoncées comme vues individuellement.** Les autres cadrages ont été contrôlés par les positions des lignes, les changements de page, les bornes des figures et l’absence de titre du QCM voisin ; le titre « Coupe de tube séminifère » est volontairement partagé entre les QCM 11 et 12. L’image du corrigé TN1 Q13 est déjà rognée à gauche dans l’EMF original : cette limite est signalée, sans fabriquer les légendes absentes.

## Fichiers et intégration

- `reviewed.json` : objets complets basés sur la V5 ; seuls ces 13 groupes sont à intégrer.
- `audit.json` : 321 entrées, 1 614 items, avec textes, positions, styles utiles, verdict littéral, détail, décision et correspondance des éditions.
- `crops.json` : 321 entrées ; sujets propres avant correction, plusieurs pages/PDF quand nécessaires, étiquettes des éditions et numéros originaux. `reuseExisting: true` conserve les copies V5 validées.
- `asset_manifest.json` : les 21 figures à copier aux chemins `static/revision_v6/histologie/…`.
- `source_manifest.json` : liste vide, car tous les PDF et Word cités sont déjà empaquetés dans le site ; `source_inventory.json` donne leurs empreintes et leur provenance.
- `response_invalidations.json` : les quatre migrations ciblées, avec texte avant/après et correspondance des lettres.
- `missing.json` : cinq arbitrages officiels nécessaires, une limite graphique facultative et les demandes d’errata complémentaires. Aucun sujet ou corrigé principal n’est absent.
- `geometry_checks.json`, `reuse_checks.json`, `changes.json`, `coverage_summary.json` et `edition_comparisons.json` complètent la traçabilité.

Le vérificateur doit relire les sources indépendamment, surtout les quatre rétablissements de Techniques et les deux lacunes levées TC42/TN63. Il doit confirmer les correspondances de session et le statut hors note des cinq contradictions avant l’intégration.

## Empreintes remises au vérificateur

- reviewed.json — SHA-256 `{CORE_HASHES['reviewed.json']}`
- crops.json — SHA-256 `{CORE_HASHES['crops.json']}`
'''
(OUT/'REPORT.md').write_text(report)
FINAL_FILES=list(OUTPUTS)+['REPORT.md']
dump('final_manifest.json',{'state':'preparer_ready_for_independent_verification','independentVerificationPending':True,
     'counts':SUMMARY,'sha256':{f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in FINAL_FILES},
     'assetSha256':{a['src']:a['sha256'] for a in ASSETS}})
print(json.dumps({'prepared':True,'questions':321,'items':1614,'ungraded':len(HORSNOTE),'sha256':CORE_HASHES},ensure_ascii=False))
