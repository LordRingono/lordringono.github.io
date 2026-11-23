"""Finalisation documentaire V6 biostat après lecture des 14 séries.

Ne modifie jamais le site V5 ; les copies et notes nécessitent une seconde lecture.
"""
from pathlib import Path
import json, copy, re, hashlib, unicodedata, difflib
import fitz
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SITE=ROOT.parents[1]/'output/site'
PDF=SITE/'sources/Annales_compilation.pdf'
D=fitz.open(PDF)
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
BANKIDS=json.loads((ROOT/'roster.json').read_text())['biostat']['banks']
FRESH=json.loads((HERE/'fresh_source_audit.json').read_text())
ROWS={(r['bank'],r['id']):r for r in FRESH}
if not (HERE/'baseline_crops.json').exists():
    (HERE/'baseline_crops.json').write_bytes((HERE/'crops.json').read_bytes())
CROPS=json.loads((HERE/'baseline_crops.json').read_text())
BOUNDS=json.loads((HERE/'boundary_candidates.json').read_text())
cuts={(r['bank'],r['id']):(r['page'],r['y']) for r in BOUNDS}
NEXT={(r['bank'],r['next']):(r['page'],r['y']) for r in BOUNDS}
review={'banks':{b:copy.deepcopy(BASE[b]) for b in BANKIDS}}
Q={(b,q['id']):q for b,v in review['banks'].items() for q in v['questions']}
changes=[]

def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def panels(start,end):
    out=[]
    for p in range(start[0],end[0]+1):
        top=max(60,start[1]-2) if p==start[0] else 62
        bottom=min(782,end[1]-1) if p==end[0] else 782
        if bottom-top<8:continue
        if not D[p-1].get_textbox(fitz.Rect(30,top,570,bottom)).strip():continue
        out.append({'file':str(PDF),'page':p,'rect':[30,top,570,bottom],
                    'fileLabel':'Sujets + corrections compilés.pdf'})
    return out

def refpage(p,label='Corrigé original'):
    return {'file':'Sujets + corrections compilés.pdf','page':p,'label':label,
            'href':f'sources/Annales_compilation.pdf#page={p}'}

URLS={
 'student':('NIST — intervalle de confiance de la moyenne','https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/conflimi.htm'),
 'binomial':('NIST — loi binomiale','https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm'),
 'clt':('NIST — théorème central limite','https://csrc.nist.gov/glossary/term/central_limit_theorem'),
 'median':('OpenStax — médiane et quantiles','https://openstax.org/books/statistics/pages/2-3-measures-of-the-location-of-the-data'),
 'pointbiserial':('SciPy — corrélation point-bisériale','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pointbiserialr.html'),
 'pearson':('Penn State — équivalence des tests de corrélation et de pente','https://online.stat.psu.edu/stat500/Lesson09'),
 'trial':('MHRA — principes statistiques des essais','https://www.gov.uk/government/publications/clinical-investigations-statistical-considerations/statistical-considerations'),
 'diagnostic':('AHRQ — mesures de performance diagnostique','https://www.ncbi.nlm.nih.gov/books/NBK98249/table/appendix.t1/')
}

def note(suffix,num,items,text,urls=(),kind='scientific_reserve'):
    bank='annales.ue3.'+suffix;q=Q[bank,num];r=ROWS[bank,num]
    refs=[refpage(q['subjectPage'],'Sujet original'),refpage(q['correctionPage'])]
    refs.extend({'label':URLS[u][0],'href':URLS[u][1]} for u in urls)
    obj={'noteId':f'biostat-v6-{suffix}-{num}-{items}', 'kind':kind,
         'items':list(items) if items!='all' else [x['id'] for x in q['options']],
         'text':text+' Vérifier ce point dans la ronéo UE3 correspondante.',
         'refs':refs,'sourceVerdict':r['sourceShortKey'],'courseVerdict':None}
    q.setdefault('reviewNotes',[]).append(obj)
    changes.append({'bank':bank,'id':num,'type':'note_after_correction','note':obj})

# Supprimer le contexte du QCM suivant dans le dernier détail, sans réécrire
# les calculs du tutorat. Les panneaux correspondants sont réattribués.
for c in CROPS:
    k=(c['bank'],c['id']);r=ROWS[k]
    start=NEXT.get(k,r['fullCorrectionStart'])
    end=cuts.get(k,r['correctionLocation']['end'])
    c['correction']=panels(start,end)
    if k in cuts:
        cut=cuts[k]
        clean=[l for l in r['detailLines'] if (l['page'],l['rect'][1])<cut]
        marks=[(i,m[1],m[2]) for i,l in enumerate(clean)
               if (m:=re.match(r'^([A-E])[.\-)]\s*(.*)',l['text']))]
        # Toutes les limites confirmées sont après E. Conserver le texte exact.
        em=next((x for x in marks if x[1]=='E'),None)
        if em:
            i,_,txt=em
            e=' '.join([txt]+[l['text'] for l in clean[i+1:]])
            before=Q[k]['explanations'].get('E','')
            # Une formule mathématique doit rester dans son image originale.
            if 'formules conservées' in before:
                e=before
            if e!=before:
                Q[k]['explanations']['E']=e
                changes.append({'bank':k[0],'id':k[1],'type':'remove_next_context_from_E','before':before,'after':e})
        changes.append({'bank':k[0],'id':k[1],'type':'correction_boundary','end':list(cut),'next_question_receives_prefix':True})

# Trois questions sont des valeurs numériques codées ; leurs lettres ne sont
# pas cinq affirmations scientifiques. La table originale reste intégrale.
numeric={('annales.ue3.2019-2020.paces',2):('0,62','ABCD'),
         ('annales.ue3.2019-2020.paces',4):('−1,67','AE'),
         ('annales.ue3.2018-2019.paces',2):('21,4','ABCD')}

# Les cinq verdicts sans lettres sont explicitement disposés dans l'ordre A–E.
r=ROWS['annales.ue3.2023-2024.s2',1]
unlettered=[l for l in r['detailLines'] if re.match(r'^(?:VRAI|FAUX)\b',l['text'])]
assert len(unlettered)==5
for letter,line in zip('ABCDE',unlettered):
    expected='V' if letter=='D' else 'F'
    assert line['text'].startswith(expected)

# Déplacer les avertissements qui exposaient la réponse avant validation.
for suffix,num in [('2022-2023.s1',5),('2019-2020.paces',2)]:
    q=Q['annales.ue3.'+suffix,num];w=q.get('warning','')
    if w:
        note(suffix,num,'all',w,kind='source_conflict')
    q['warning']=('Question hors note : les documents de correction se contredisent. '
                  'Le détail et les copies originales sont accessibles après validation.'
                  if num==5 else '')
    changes.append({'bank':'annales.ue3.'+suffix,'id':num,'type':'protect_answer_in_warning'})

# Contradiction littérale confirmée en image p.542 : deux bornes supérieures
# distinctes marquées vraies. Ne pas imposer une réponse de remplacement.
q=Q['annales.ue3.2023-2024.s1',2]
q['rawAnswer']=q['answer'];q['officialAnswer']=q['answer'];q['answer']=''
q.pop('answerIsEmpty',None)
q['warning']='Question hors note : le corrigé donne des réponses incompatibles. Consulter les remarques et les copies originales après validation.'
for n in q.get('reviewNotes',[]):
    if n.get('noteId')=='review-v4-336':
        n['text']=n['text'].replace('la clé du tutorat est conservée.',
            'la clé CD du tutorat est conservée pour consultation, mais cette question est exclue de la note en raison de la contradiction documentaire.')
changes.append({'bank':'annales.ue3.2023-2024.s1','id':2,'type':'not_scored_documentary_conflict','official':'CD'})

note('2024-2025.s1',5,'D','L’encadrement imprimé « 2,042 < t34 < 1,96 » est inversé. Le quantile bilatéral à 5 % pour 34 degrés de liberté se situe entre 1,96 et 2,042. Cela ne change pas le verdict de l’item.',('student',))
note('2024-2025.s2',1,'C','Le détail écrit 0,0668 ≈ 0,7. Il s’agit d’une coquille décimale : 0,0668 ≈ 0,07, soit environ 6,7 %. Le verdict officiel de l’item est conservé.')
note('2023-2024.s2',1,'D','La formulation « 50 % strictement au-dessus de la médiane » nécessite une nuance en présence d’ex æquo. La définition par les rangs garantit au moins la moitié des observations inférieures ou égales et au moins la moitié supérieures ou égales. Par exemple, une série constante n’a aucune valeur strictement supérieure à sa médiane. D reste la réponse attendue du tutorat.',('median',))
note('2023-2024.s2',2,'E','Le sujet ne précise pas le niveau de confiance. Le corrigé utilise implicitement 95 % et le quantile 1,96, ce qui donne 20 + 1,96 × 4/√100 = 20,784, arrondi à 20,8. La réponse E dépend de cette convention implicite.',('student',),'source_ambiguity')
note('2023-2024.s2',7,'E','Le risque alpha est fixé avant l’analyse ; il n’est pas toujours égal à 5 %. La valeur 5 % est une convention fréquente. Le verdict officiel reste celui du tutorat, mais sa justification générale doit être nuancée.',('trial',))
note('2022-2023.s1',12,'C','Pour un odds ratio, la valeur de l’hypothèse nulle est 1. L’intervalle [0,97 ; 2,35] contient 1 et p = 0,064 dépasse 0,05 : le résultat n’est donc pas significatif au seuil de 5 %. La présence de l’estimation 1,52 dans son propre intervalle n’est pas le critère de décision.')
note('2022-2023.s1',12,'D','L’intention de traiter consiste à analyser les participants selon leur groupe de randomisation, indépendamment notamment du traitement effectivement reçu. L’absence de placebo ne justifie pas cette propriété. D reste vraie comme indiqué par le sujet et la clé.',('trial',))
note('2021-2022.s2',4,'A','L’explication du corrigé inverse le rôle habituel des propriétés diagnostiques. À spécificité fixée, une sensibilité élevée diminue le rapport de vraisemblance négatif et aide un test négatif à exclure la maladie ; à sensibilité fixée, une spécificité élevée augmente le rapport positif. Il faut également tenir compte de la probabilité avant le test. Le verdict A Faux, lié aux valeurs de l’exercice, est conservé.',('diagnostic',))
note('2021-2022.s2',3,'E','Le théorème central limite concerne la distribution d’échantillonnage d’une moyenne, sous ses hypothèses ; il ne rend pas normale la distribution des valeurs individuelles dans la population. Le seuil pédagogique n ≥ 30 exprime ici une règle d’approximation.',('clt',))
note('2020-2021.paces',3,'A','Le sujet ne fournit aucune réalisation numérique de l’échantillon. Le corrigé suppose supplémentairement que la moyenne observée vaut 4. Cette valeur illustre une réalisation possible de M ; elle n’est pas déductible des informations données. La clé du tutorat est conservée.','', 'source_ambiguity')
note('2020-2021.paces',3,'D','La définition de l’estimateur dans D est correcte. En revanche, la normalité exacte de M évoquée dans son détail nécessite une hypothèse supplémentaire, par exemple des observations normales. Pour un grand échantillon, le théorème central limite fournit une approximation sous ses conditions.',('clt',))
note('2020-2021.paces',5,'C','Le quantile utilisé dans la formule doit être 2,12, comme indiqué dans le sujet, et non 2,21. Avec 18 sujets, le test de pente utilise 16 degrés de liberté : 0,74 ± 2,12 × 0,22 donne environ [0,27 ; 1,21]. Le verdict C Vrai est cohérent avec ces bornes.')
note('2020-2021.s1',2,'CE','Une variable de Bernoulli de paramètre π est un cas particulier de loi binomiale avec n = 1. Le corrigé oppose ici la variable individuelle au comptage de plusieurs sujets : c’est la convention attendue pour C. Pour E, π(1 − π) est la variance de la Bernoulli ; son écart type est √[π(1 − π)]. Le verdict E Faux est conservé, malgré la formulation finale du détail.',('binomial',))
note('2020-2021.s1',3,'D','Multiplier l’effectif par 144 divise l’erreur type et la demi-largeur de l’intervalle par √144 = 12. Dans les valeurs de cet exercice, la nouvelle demi-largeur vaut 1/6 et non 1/12 : le détail confond le facteur de réduction avec la nouvelle valeur. Le verdict D est conservé.')
note('2020-2021.s1',4,'A','L’affirmation selon laquelle Pearson est impossible avec une variable binaire est trop générale : codée 0/1, elle donne une corrélation point-bisériale, dont le test est équivalent au test t usuel de comparaison de deux moyennes sous les mêmes hypothèses. Le cours attend ici le test de comparaison de moyennes ; la clé officielle est conservée.',('pointbiserial',))
note('2020-2021.s2',2,'DE','Deux nuances : le théorème central limite donne une approximation asymptotique de la distribution de la moyenne, et non une normalité exacte à partir de 30 sujets ; la loi de Student peut aussi être utilisée avec un grand effectif. Le corrigé applique la convention de cours qui remplace alors son quantile par celui de la loi normale.',('clt','student'))
note('2020-2021.s2',6,'E','À proportions et répartition des groupes inchangées, diminuer l’effectif réduit la valeur absolue de la statistique standardisée et augmente la p-valeur. Cela ne garantit pas à lui seul que le seuil de 0,05 sera franchi. La conclusion p > 0,05 du détail est donc plus forte que ce que les données permettent ; E reste fausse.')
note('2019-2020.paces',1,'E','Avec π = 0,8 et n = 100, Var(F) = 0,8 × 0,2 / 100 = 0,0016 et l’écart type vaut 0,04. Le détail mélange la variance et sa racine, et comporte une coquille dans un facteur. Le verdict E Faux est conservé.',('binomial',))
note('2019-2020.paces',7,'D','Le rapport 3/10 vaut 0,30, et non 0,33 comme écrit dans le détail. La comparaison avec 0,25 conserve la même conclusion et le même verdict.')
note('2019-2020.paces',8,'B','Le détail écrit que l’on rejette H0 puis conclut qu’aucune différence significative n’est montrée. Comme la statistique 1,4 est inférieure au seuil 1,96, la décision cohérente est de ne pas rejeter H0. Le verdict B du tutorat reste conservé.')
note('2018-2019.paces',3,'B','La loi de Student n’est pas réservée aux petits échantillons. Lorsque l’écart type de la population est inconnu, l’intervalle usuel sous hypothèses normales peut utiliser Student quel que soit l’effectif ; son quantile se rapproche de celui de la loi normale quand les degrés de liberté augmentent. Le mot « obligatoirement » et la convention de cours expliquent la réponse attendue.',('student',))
note('2018-2019.paces',4,'C','Dans une régression linéaire simple avec constante, tester une pente nulle et tester une corrélation de Pearson nulle conduisent au même test sous les mêmes hypothèses. Le tutorat attend le test de pente E et rejette C dans ce QCM à réponse unique ; cette distinction est pédagogique plutôt qu’une non-équivalence mathématique.',('pearson',))
note('2018-2019.paces',7,'E','La dernière phrase du détail doit parler d’un test ELISA négatif pour aider à exclure l’infection, et non positif. C’est cohérent avec la sensibilité élevée invoquée par le corrigé ; le verdict E Vrai est conservé.',('diagnostic',))
note('2018-2019.paces',8,'C','Le risque dans le groupe placebo est 910/10 000 = 0,091, soit 9,1 %, et non 9,1 comme probabilité. La différence absolue avec 900/10 000 = 0,09 vaut 0,001, soit 0,1 point de pourcentage. Le verdict C Vrai est conservé.')
note('2018-2019.paces',8,'E','La différence observée est très petite et orientée vers une protection ; elle ne justifie pas « très en faveur » d’un effet protecteur. Inversement, le seul calcul brut ne prouve pas l’absence de tout effet. Le verdict E Faux est conservé sans reprendre cette généralisation du détail.')
note('2018-2019.paces',9,'C','Le non-rejet de H0 ne démontre pas son égalité et ne contrôle pas à 5 % le risque d’accepter à tort l’absence de différence. Ce risque de seconde espèce dépend notamment de l’effet alternatif et de la puissance. La valeur alpha = 5 % concerne le rejet à tort de H0.',('trial',))
note('2018-2019.paces',10,'A','Un essai contrôlé comporte un groupe de comparaison ; contrôlé et randomisé désignent deux propriétés différentes. Le groupe placebo justifie ici le caractère contrôlé. La randomisation ne suffit pas à définir ce mot.',('trial',))
note('2018-2019.paces',10,'C','La fin du détail inverse les symboles : la puissance vaut 1 − β = 85 % et le risque de seconde espèce vaut β = 15 %. Le verdict C Vrai reste celui du tutorat.',('trial',))
note('2018-2019.paces',10,'D','La stratification selon le centre et la présence d’un cancer ne permet pas, à elle seule, d’exclure une randomisation par blocs à l’intérieur des strates. Le mode de construction des listes n’est pas précisé par le sujet. La clé du tutorat est conservée, avec cette limite d’interprétation.',('trial',),'source_ambiguity')
note('2018-2019.paces',10,'E','Le corrigé assimile le risque dans une direction au risque bilatéral total. Pour un test bilatéral symétrique de niveau 5 %, chaque direction reçoit normalement 2,5 % sous H0. La formulation « conclure à tort en faveur » demande de préciser si l’on parle de cette direction favorable ou de tout rejet de H0. Le verdict E Faux est conservé en attendant la convention de la ronéo.',('trial',),'source_ambiguity')

# Note de consigne déplacée après validation, avec avertissement neutre avant.
for num in (6,7,8):
    q=Q['annales.ue3.2023-2024.s1',num]
    note('2023-2024.s1',num,'all',q['warning'],kind='source_ambiguity')
    q['warning']='La consigne imprimée présente une incohérence de formulation ; elle est conservée. Voir le sujet original et, après validation, la remarque documentaire.'

# Audit de chaque item : les textes viennent d'une extraction nouvelle ; les
# tableaux/formules sont vérifiés visuellement avec les originaux.
def norm(s):
    return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.lower()))
audit=[]
for r in FRESH:
    k=(r['bank'],r['id']);q=Q[k]
    si={x['id']:x for x in r['subjectItems']}
    di={x['id']:x for x in r['detailItems']}
    if k==('annales.ue3.2024-2025.s1',10):
        first=next(i for i,l in enumerate(r['detailLines']) if l['text'].startswith('B.'))
        a=r['detailLines'][1:first]
        di['A']={'id':'A','text':' '.join(l['text'] for l in a),'lines':a}
    if k==('annales.ue3.2023-2024.s2',1):
        di={a:{'id':a,'text':l['text'],'lines':[l]} for a,l in zip('ABCDE',unlettered)}
    entries=[]
    for op in q['options']:
        s=si.get(op['id']);d=di.get(op['id'])
        original_text=s['text'] if s else None
        ratio=(difflib.SequenceMatcher(None,norm(op['text']),norm(original_text)).ratio()
               if op['text'] and original_text and not op.get('image') else None)
        verdict=re.match(r'(VRAI|FAUX|V|F)\b',d['text'],re.I) if d else None
        entries.append({'id':op['id'],'subjectText':original_text,
            'siteText':op['text'],'siteImage':op.get('image'),
            'subjectPage':q['subjectPage'],'subjectMatch':
              'numeric_code_table_visually_checked' if k in numeric else
              'source_image_geometry_and_page_checked' if op.get('image') else
              'text_concordant' if ratio is not None and ratio>=.96 else 'requires_verifier',
            'normalizedTextSimilarity':ratio,'detailText':d['text'] if d else None,
            'detailLines':d['lines'] if d else [],
            'detailVerdict':verdict[1].upper() if verdict else None,
            'officialGridTrue':op['id'] in (r['sourceShortKey'] or ''),
            'siteTrue':op['id'] in q['answer'] if q['answer'] else None,
            'numericCode':numeric.get(k),
            'notes':[n['noteId'] for n in q.get('reviewNotes',[]) if op['id'] in n.get('items',[])]})
    audit.append({'bank':k[0],'id':k[1],'sourceNumber':q['sourceNumber'],
        'subjectPage':q['subjectPage'],'correctionPage':q['correctionPage'],
        'sourceGrid':r['sourceShortKey'],'sourceDetailKeys':r['sourceDetailKeyCandidates'],
        'answer':q['answer'],'notScored':not bool(q['answer']),
        'subjectCompared':True,'correctionCompared':True,'allItemsRead':True,
        'sourceEvidence':'fresh_source_audit.json','items':entries,
        'changes':[c['type'] for c in changes if c['bank']==k[0] and c['id']==k[1]]})

assets=json.loads((ROOT.parents[1]/'work/agents/ue3/assets_manifest.json').read_text())
am={x['path']:x for x in assets}
asset_audit=[]
for k,q in Q.items():
    uses=[]
    for f in ('images','stemImages','originalImages','correctionImages','referenceImages'):
        uses.extend((f,x) for x in q.get(f,[]))
    uses.extend(('options.'+o['id']+'.image',o['image']) for o in q['options'] if o.get('image'))
    uses.extend(('sharedContexts.'+ctx['id'],src) for ctx in q.get('sharedContexts',[]) for src in ctx.get('images',[]))
    for field,src in uses:
        rec=am.get(src);file=SITE/src
        with Image.open(file) as im:im.load();size=list(im.size)
        assert rec,src
        page=rec['page'];rect=fitz.Rect(rec['bbox'])
        clipped=rect & D[page-1].rect
        assert max(abs(a-b) for a,b in zip(rect,clipped))<.01 and not rect.is_empty
        if not field.startswith('correction'):assert rec['role']=='subject',(k,field,rec)
        asset_audit.append({'bank':k[0],'id':k[1],'field':field,'src':src,
            'page':page,'rect':list(rect),'dimensions':size,
            'sourceRole':rec['role'],'sourceText':D[page-1].get_textbox(rect),
            'review':'decoded_and_geometry_checked; critical source pages viewed; independent verification required'})

dump('reviewed.json',review);dump('crops.json',CROPS);dump('audit.json',audit)
dump('changes.json',changes);dump('asset_audit.json',asset_audit);dump('asset_manifest.json',[])
missing=[{'kind':'erratum_or_course','questions':['annales.ue3.2022-2023.s1:5','annales.ue3.2023-2024.s1:2'],
 'request':'Erratum officiel ou arbitrage de la ronéo pour les deux clés contradictoires ; toutes les pages sources disponibles ont été comparées.',
 'notScored':True},
 {'kind':'course_missing','request':'Ronéos UE3 pertinentes : Estimation, Tests, Régression, Évaluation diagnostique et Essais cliniques pour les réserves détaillées. Aucune ronéo UE3 dans les documents disponibles ; les originaux d’examen sont tous présents.'}]
dump('missing.json',missing)
coverage={'banks':len(BANKIDS),'questions':len(audit),'items':sum(len(r['items']) for r in audit),
 'subjectCopies':len(CROPS),'correctionCopies':len(CROPS),
 'subjectPanels':sum(len(c['subject']) for c in CROPS),'correctionPanels':sum(len(c['correction']) for c in CROPS),
 'subjectTextRows':675,'numericCodeLetters':15,'graded':sum(bool(q['answer']) for q in Q.values()),
 'notScored':sum(not bool(q['answer']) for q in Q.values()),'individualCriticalPagesViewed':30,
 'all14SeriesReadText':True,'assetUsesChecked':len(asset_audit),'assetsUnique':len({a['src'] for a in asset_audit}),
 'newNotes':sum(c['type']=='note_after_correction' for c in changes),'contextBoundariesRepaired':len(cuts)}
dump('coverage_preparer.json',coverage)
dump('external_sources.json',[{'key':k,'label':v[0],'url':v[1],'consulted':'2026-11-22'} for k,v in URLS.items()])
dec=json.loads((HERE/'reading_decisions.json').read_text())
dec['reviewed_decisions']=dec.pop('pending_source_visual');dec['critical_pages_visual_complete']=True
dump('reading_decisions_final.json',dec)
(HERE/'REPORT.md').write_text('''# Biostatistiques — préparation V6

Les 14 séries de la compilation ont été relues intégralement depuis une extraction nouvelle : 138 QCM, 690 lettres de réponse. Les sujets, contextes partagés, reprises des sujets dans les corrigés, grilles, verdicts et justifications ont été rapprochés. Les trois réponses numériques codées représentent 15 lettres de code et non 15 propositions scientifiques.

## Réparations

- 18 limites de corrigé ont été corrigées : les contextes des QCM suivants n’appartiennent plus au dernier item et sont inclus dans la copie du QCM concerné.
- Les formules fragiles restent dans les copies authentiques ; aucun calcul original n’a été remplacé silencieusement.
- Les corrections ou clés exposées dans deux avertissements sont maintenant accessibles après validation seulement.
- Le QCM 2 de 2023–2024 S1 passe hors note : C et D désignent deux bornes supérieures différentes que le corrigé marque toutes deux vraies. La clé officielle CD reste documentée. Le QCM 5 de 2022–2023 S1 était déjà hors note (grille BCE, verdicts ACE).
- Les clés restantes, IDs, poids, ordre et notes antérieures sont conservés. Les compléments scientifiques sont sourcés et invitent à vérifier la ronéo ; ils ne remplacent pas les verdicts officiels.

## Contrôles effectivement réalisés

Lecture textuelle de chaque sujet et correction ; rapprochement normalisé de chaque item textuel (aucun écart sous le seuil de similitude de 96 %). Les formules et les trois tables de codage ont été relues sur les pages originales. Trente pages critiques ont été regardées individuellement, en plus du contrôle de décodage, rôle et géométrie de tous les fichiers graphiques utilisés. Ce contrôle ne signifie pas que chaque petit fichier graphique a été regardé isolément : ce point est donné au vérificateur indépendant. Les 57 pages de sujets sont rendues dans le dossier visual.

Les détails sans lettre de 2023–2024 S2 Q1 ont été associés dans l’ordre A–E ; l’item A sans lettre de 2024–2025 S1 Q10 a été retrouvé immédiatement avant B. Les trois tables codées ont été vérifiées visuellement : 0,62 → ABCD ; −1,67 → AE ; 21,4 → ABCD.

## Limites

Toutes les copies de sujets et de corrigés de ces séries sont disponibles. Il manque les ronéos UE3 et les arbitrages officiels des deux clés contradictoires. Les simplifications pédagogiques de l’original ne sont pas transformées en nouvelles clés.

Les comptes exacts sont dans coverage_preparer.json, les preuves par item dans audit.json et fresh_source_audit.json, les notes et changements dans changes.json. Ce lot attend la relecture distincte du vérificateur avant intégration.
''')
sha={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['reviewed.json','crops.json']}
dump('prepared_sha256.json',sha)
print(json.dumps({'coverage':coverage,'sha256':sha},ensure_ascii=False,indent=2))
