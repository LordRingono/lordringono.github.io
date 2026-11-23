"""V6 BIOCHIMIE: assemble the individually read source comparisons and decisions.

The V5 data remain immutable. All writes are confined to this prepare directory.
Run only after the reading/visual passes described in REPORT.md.
"""
from pathlib import Path
import copy, hashlib, io, json, re, unicodedata
import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = ROOT.parents[1]
PDF = WORK / 'output/site/sources/Annales_compilation.pdf'
D = fitz.open(PDF)
BASE = json.loads((ROOT / 'baseline_exams.json').read_text())
ROSTER = json.loads((ROOT / 'roster.json').read_text())['biochimie']['banks']
FRESH = json.loads((HERE / 'fresh_source_audit.json').read_text())
GRIDS = {(r['sourceSet'], r['sourceNumber']): r for r in json.loads((HERE / 'grid_recheck.json').read_text())}
INV = json.loads((HERE / 'interactive_inventory.json').read_text())
reviewed = {'banks': {b: copy.deepcopy(BASE[b]) for b in ROSTER}}
Q = {(q['sourceSet'],q['sourceNumber']):(b,q) for b,v in reviewed['banks'].items() for q in v['questions']}
F = {(r['sourceSet'],r['sourceNumber']):r for r in FRESH}
edits=[]; decisions=[]; assets=[]; extra_notes=[]

def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def edit(s,n,field,new,item=None,reason=''):
    bank,q=Q[s,n]
    if item and field=='options':
        target=next(o for o in q['options'] if o['id']==item); old=target['text'];target['text']=new
    elif item:
        old=q[field].get(item);q[field][item]=new
    else: old=q.get(field);q[field]=new
    if old!=new: edits.append({'bank':bank,'id':q['id'],'sourceSet':s,'sourceNumber':n,'field':field,'item':item,'before':old,'after':new,'reason':reason})

def pdfref(page,label='Corrigé original'):
    return {'file':'Sujets + corrections compilés.pdf','page':page,'label':label,'href':f'sources/Annales_compilation.pdf#page={page}'}

RONEOS = json.loads((HERE/'roneo_inventory.json').read_text())
def course(prefix,page,label):
    p=next(Path(r['file']) for r in RONEOS if Path(r['file']).name.startswith(prefix))
    return {'file':p.name,'page':page,'label':label,'href':f'sources/revision_v4/{p.name}#page={page}'}

def web(url,label): return {'file':label,'label':label,'href':url}
PAD=web('https://iubmb.qmul.ac.uk/enzyme/EC3/5/3/15.html','IUBMB — protéine-arginine déiminase, EC 3.5.3.15')
PDH=web('https://iubmb.qmul.ac.uk/enzyme/EC1/2/1/104.html','IUBMB — pyruvate déshydrogénase, EC 1.2.1.104')
GLY=web('https://reactome.org/content/detail/R-HSA-70171','Reactome — Glycolysis, R-HSA-70171')
GNG=web('https://reactome.org/content/detail/R-HSA-70263','Reactome — Gluconeogenesis, R-HSA-70263')
PHOS=web('https://enzyme.expasy.org/EC/2.4.1.1','ENZYME / IUBMB — glycogène phosphorylase, EC 2.4.1.1')

def note(s,n,letters,text,refs,kind='scientific_dispute'):
    bank,q=Q[s,n]; r=F[s,n]
    pages=sorted({l['page'] for l in r['correctionLines']})
    itemrefs=[pdfref(p) for p in pages]
    for ref in refs:
        if ref not in itemrefs:itemrefs.append(ref)
    obj={'bank':bank,'id':q['id'],'sourceId':str(n),'items':list(letters),'kind':kind,
         'text':text+' La clé officielle est conservée ; vérifie ce point dans la ronéo.',
         'refs':itemrefs,'sourceVerdict':q['answer'],'noteId':f'review-v6-biochimie-{s}-{n}-'+''.join(letters)}
    assert not any(x.get('noteId')==obj['noteId'] for x in q.get('reviewNotes',[]))
    q.setdefault('reviewNotes',[]).append(obj);extra_notes.append(obj)

# Exact import repair: the item label had been copied a second time into its text.
b,q=Q['2019',25]
edit('2019',25,'options',q['options'][2]['text'].removeprefix('C. '),'C','La lettre C. est déjà le label de l’option, et non une partie de son énoncé.')

# Linear transcriptions of original fractions: no new official verdict is inferred.
MATH_REASON='Fractions/exposants relus sur le PDF rendu ; remise en ordre des lignes et rattachement au bon item, sans changement de verdict.'
transcriptions={
 ('2022s1',24):{
  'A':'FAUX : Km = (k₋₁ + kcat) / k₁ = (5 × 10⁴ + 1 × 10²) / (5 × 10⁹) ≈ 1 × 10⁻⁵ mol·L⁻¹. Le corrigé ajoute : « Km est presque toujours (voire toujours) inférieur à 1 mol/L » et souligne que 10⁵ mol·L⁻¹ serait beaucoup trop élevé. Le calcul donné ici suffit à écarter la valeur proposée.',
  'B':'FAUX : Vmax = V₀(Km + [S]) / [S] = [30 × 10⁻⁶ × (10⁻⁵ + 5 × 10⁻⁵)] / (5 × 10⁻⁵) = 36 × 10⁻⁶ mol·L⁻¹·min⁻¹.',
  'C':'VRAI : V₀ = kcat[E]₀[S] / (Km + [S]), donc [E]₀ = V₀(Km + [S]) / (kcat[S]) = 36 × 10⁻⁸ mol·L⁻¹.',
  'D':'VRAI : pour [S] = 3Km, V₀ = Vmax × 3 / 4 = 36 × 10⁻⁶ × 3 / 4 = 27 × 10⁻⁶ mol·L⁻¹·min⁻¹.',
  'E':'VRAI : pour [S] = 8Km, V₀ = Vmax × 8 / 9 = 36 × 10⁻⁶ × 8 / 9 = 32 × 10⁻⁶ mol·L⁻¹·min⁻¹.'},
 ('2021s1',24):{
  'A':'FAUX : Km = (k₋₁ + kcat) / k₁ = (2 × 10⁴ + 1 × 10²) / (8 × 10⁹) ≈ 2,5 × 10⁻⁶ mol·L⁻¹.',
  'B':'VRAI : Vmax = V₀(Km + [S]) / [S] = [25 × 10⁻⁶ × (2,5 × 10⁻⁶ + 2,5 × 10⁻⁶)] / (2,5 × 10⁻⁶) = 50 × 10⁻⁶ mol·L⁻¹·min⁻¹. Une puissance de 10 est erronée dans une étape intermédiaire imprimée : voir la remarque.',
  'C':'VRAI : [E]₀ = Vmax / kcat = (50 × 10⁻⁶) / (1 × 10²) = 50 × 10⁻⁸ mol·L⁻¹.',
  'D':'FAUX : pour [S] = 4Km, V₀ = Vmax[S] / (Km + [S]) = 50 × 10⁻⁶ × 4 / 5. Le corrigé imprime ensuite « 4 × 10⁻⁶ » : voir la remarque sur cette erreur de calcul.',
  'E':'VRAI : pour [S] = 9Km, V₀ = 50 × 10⁻⁶ × 9 / 10 = 45 × 10⁻⁶ mol·L⁻¹·min⁻¹.'},
 ('2021s2',15):{
  'D':'VRAI : C’est une phrase du cours (page 12).',
  'E':'FAUX : dans cette représentation, l’ordonnée est l’inverse de la vitesse initiale (1/V₀), et l’abscisse est l’inverse de la concentration en substrat (1/[S]).'},
 ('2020paces',35):{
  'A':'VRAI : Km = (k₋₁ + kcat) / k₁ = (10⁴ + 10²) / 10⁹ ≈ 10⁴ / 10⁹ = 10⁻⁵ mol·L⁻¹.',
  'B':'VRAI : V₀ = Vmax[S] / (Km + [S]), donc Vmax = V₀(Km + [S]) / [S] = [10 × 10⁻⁶ × (10⁻⁵ + 10⁻⁴)] / 10⁻⁴ = 11 × 10⁻⁶ mol·L⁻¹·min⁻¹.',
  'C':'FAUX : Vmax = kcat[E]₀, donc [E]₀ = Vmax / kcat = (11 × 10⁻⁶) / 10² = 11 × 10⁻⁸ mol·L⁻¹.'},
 ('2020paces',32):{
  'E':'VRAI : à pH = 11 (entre 10,2 et 12,5), ce peptide aurait une charge nette de −2. Le tableau des charges est visible dans le corrigé original.'},
 ('2020paces',30):{'C':'VRAI : pHi = (4,3 + 2,2) / 2 = 3,25.'},
 ('2025s1',26):{
  'C':'FAUX : 1/Vmax = 2 × 10⁶, donc Vmax = 1 / (2 × 10⁶) = 0,5 × 10⁻⁶ mol·L⁻¹·min⁻¹.',
  'D':'VRAI : 1/Vmax,app = 4 × 10⁶, donc Vmax,app = 1 / (4 × 10⁶) = 0,25 × 10⁻⁶ mol·L⁻¹·min⁻¹.',
  'E':'VRAI : pour cet inhibiteur incompétitif, Vmax,app = Vmax / (1 + [I]/Ki), donc Ki = [I] / ((Vmax/Vmax,app) − 1) = 4 × 10⁻⁵ mol·L⁻¹.'}
}
for (s,n),items in transcriptions.items():
    for item,txt in items.items():edit(s,n,'explanations',txt,item,MATH_REASON)
for n,letters in [(16,'A'),(20,'DE'),(21,'BD')]:
    for item in letters:
        q=Q['2021s2',n][1]
        edit('2021s2',n,'explanations',q['explanations'][item].replace('∝','α'),item,'Rétablissement du glyphe α (alpha), déformé en signe de proportionnalité lors de l’extraction.')

# New evidence-backed notes, confined to the post-correction reviewNotes channel.
for s,n,l in [('2025s1',20,'A'),('2024s1',20,'C'),('2021s2',13,'B')]:
    note(s,n,l,'Le détail « uniquement à l’état libre » est trop absolu pour la citrulline : la déimination d’une arginine déjà présente dans une protéine produit un résidu de citrulline. Cette modification post-traductionnelle ne rend pas la citrulline directement codée lors de la traduction.',[PAD])
note('2025s1',40,'D','Le nombre de 36 ATP ne correspond pas à la glycolyse prise isolément : celle-ci a un gain direct net de 2 ATP. Un bilan global après réoxydation et respiration dépend du périmètre et des conventions de rendement du cours.',[GLY], 'course_convention')
note('2024s1',38,'E','L’acide hyaluronique est un glycosaminoglycane non sulfaté. La remarque du corrigé sur les ions Na⁺ ne suffit donc pas à discuter l’affirmation concernant ses groupements sulfates.',[course('Roneo_glucides_2',19,'Ronéo glucides 2 — acide hyaluronique non sulfaté')])
note('2024s1',43,'C','Le transporteur mobile Q est le coenzyme Q (ubiquinone), pas un « cytochrome Q ». L’ATP synthase utilise le gradient de protons ; elle ne transporte pas les électrons de la chaîne respiratoire.',[web('https://reactome.org/content/detail/R-HSA-163217','Reactome — complexe I et coenzyme Q')])
note('2024s2',14,'C','Le détail associé à C reprend une explication sur la tyrosine et la mélanine, alors que cet item porte sur la leucine. Il s’agit d’un décalage rédactionnel dans le corrigé original, et non d’une justification de l’item C.',[], 'source_error')
note('2023s2',16,'E','Dans un facteur bZIP, la région qui contacte l’ADN est riche en résidus basiques ; les leucines du zipper assurent surtout la dimérisation. La leucine elle-même est apolaire et n’explique pas le caractère basique de la région de liaison à l’ADN.',[web('https://pubmed.ncbi.nlm.nih.gov/1871104/','Pu et Struhl, 1991 — région basique et leucine zipper')])
note('2023s2',20,'D','La sialyltransférase est bien une sous-classe de glycosyltransférases (EC 2.4.3). Le corrigé semble exiger ici le nom spécifique de l’enzyme, comme la ronéo ; écarter le terme général ne signifie pas qu’il soit faux du point de vue de la classification enzymatique.',[web('https://enzyme.expasy.org/EC/2.4.3.-','ENZYME / IUBMB — les sialyltransférases parmi les glycosyltransférases'),course('Roneo_lipides_complexes',16,'Ronéo lipides complexes — ajout des oses et de l’acide sialique')], 'course_convention')
note('2023s2',25,'B','La glycolyse se déroule dans le cytosol, y compris en conditions aérobies. Ce sont l’oxydation mitochondriale ultérieure du pyruvate et la réoxydation des coenzymes qui changent selon les conditions ; la glycolyse elle-même ne devient pas mitochondriale.',[GLY])
note('2022s1',31,'C','Les structures 2 et 3 correspondent ici au D-mannose et au L-glucose : elles diffèrent sur plusieurs carbones asymétriques. Ce sont des diastéréoisomères, mais pas des épimères, puisque la définition d’épimères exige un seul carbone différent.',[pdfref(183,'Structures du sujet'),course('Roneo_glucides_1',7,'Ronéo glucides 1 — filiation et épimères')])
note('2022s1',34,'D','L’affirmation générale « l’Homme ne possède pas de β-glucosidase » est trop large. La β-glucosidase acide humaine hydrolyse notamment le glucosylcéramide (GBA1). Cela ne signifie pas que l’Homme puisse digérer la cellulose.',[web('https://enzyme.expasy.org/EC/3.2.1.45','ENZYME / IUBMB — glucosylcéramidase et β-glucosidases humaines'),course('Roneo_lipides_complexes',18,'Ronéo lipides complexes — maladie de Gaucher')])
note('2022s1',37,'B','Le détail confond deux réactions : la pyruvate déshydrogénase transforme le pyruvate en acétyl-CoA avec production de CO₂ et NADH. La formation du lactate relève de la lactate déshydrogénase.',[PDH])
note('2022s2',20,'BE','Deux détails paraissent être des coquilles : B donne le nom du fructose à la place d’une β-fructosidase ; E répond sur le lactose alors que l’item porte sur le cellobiose. La ronéo distingue bien ces disaccharides et leurs enzymes d’hydrolyse.',[course('Roneo_glucides_2',10,'Ronéo glucides 2 — saccharose'),course('Roneo_glucides_2',11,'Ronéo glucides 2 — maltose et cellobiose')], 'source_error')
note('2021s1',24,'BD','Le calcul imprimé de D contient un facteur 10 erroné : (50 × 10⁻⁶) × 4/5 = 40 × 10⁻⁶, et non 4 × 10⁻⁶ mol·L⁻¹·min⁻¹. D reste faux par rapport à la valeur proposée. En B, une étape intermédiaire imprime aussi 10⁻⁴ à la place de 10⁻⁶ ; le résultat final 50 × 10⁻⁶ est cohérent.',[], 'source_error')
note('2021s1',29,'B','Un céramide comporte déjà un acide gras lié par une liaison amide à la sphingosine. La formation d’un glucosylcéramide ajoute un glucose au céramide ; elle ne nécessite pas d’y ajouter un second acide gras.',[course('Roneo_lipides_complexes',9,'Ronéo lipides complexes — céramide'),course('Roneo_lipides_complexes',13,'Ronéo lipides complexes — glucosylcéramide')])
note('2021s1',37,'D','Les états d’oxydoréduction sont inversés dans le détail : NAD⁺ est la forme oxydée et NADH la forme réduite. Dans la réaction de la pyruvate déshydrogénase, NAD⁺ entre et NADH est produit ; vérifie aussi le sens des coenzymes sur le schéma fourni.',[PDH])
note('2021s2',19,'A','Des cétoses peuvent également être épimères. La filiation de la ronéo montre par exemple le D-fructose et le D-psicose, qui diffèrent au niveau d’un seul carbone asymétrique. La restriction des épimères aux aldoses est donc trop générale.',[course('Roneo_glucides_1',7,'Ronéo glucides 1 — filiation des cétoses')])
note('2020s1',28,'A','Le détail dit que les stéarates sont plus hydrophobes, ce qui soutient l’énoncé selon lequel la trioléine est moins hydrophobe que la tristéarine, alors que A est marqué faux. La ronéo relie les doubles liaisons à une augmentation de polarité : ce verdict mérite une vérification dans le cours.',[course('Roneo_cours_AG2',6,'Ronéo AG2 — insaturation et propriétés physiques'),course('Roneo_lipides_simples',4,'Ronéo lipides simples — triglycérides')])
note('2020s1',33,'C','L’oxydation de la fonction aldéhyde du glucose conduit à l’acide gluconique (via une gluconolactone), pas à l’acide glucuronique. Ce dernier correspond à l’oxydation de l’alcool primaire en C6 ; le nom donné dans le détail est litigieux.',[web('https://iubmb.qmul.ac.uk/enzyme/EC1/1/5/2.html','IUBMB — glucose déshydrogénase et gluconate')])
note('2020s1',34,'E','Le cours emploie ici « glucosidique » dans un sens restreint. En nomenclature générale, un glucoside peut unir le glucose à un autre aglycone, pas nécessairement à un deuxième glucose. Pour le lactose de cet item, le terme β-galactosidique reste le terme spécifique attendu.',[web('https://www.ncbi.nlm.nih.gov/mesh/68005960','MeSH — glucosides'),course('Roneo_glucides_2',8,'Ronéo glucides 2 — vocabulaire des liaisons osidiques')], 'course_convention')
note('2020s1',37,'DE','La réduction du glutathion oxydé utilise le NADPH, et non le ribose. Par ailleurs, la transcétolase transfère un fragment à deux carbones entre deux oses phosphates ; elle ne réalise pas une simple isomérisation intramoléculaire aldose/cétose.',[web('https://www.reactome.org/content/detail/R-HSA-71682','Reactome — glutathion réductase et NADPH'),web('https://amigo.geneontology.org/amigo/term/GO%3A0004802','Gene Ontology — activité transcétolase')])
note('2020s1',38,'D','La glycogène phosphorylase s’arrête à quatre résidus d’un point de branchement α(1→6). L’enzyme débranchante transfère ensuite trois de ces résidus ; confondre ces deux nombres explique probablement le « trois » du détail.',[web('https://reactome.org/content/detail/R-HSA-70221','Reactome — dégradation du glycogène et enzyme débranchante')])
note('2020s2',21,'E','L’item peut être retenu parce qu’une liaison est hydrolysable par une α-glucosidase. En revanche, le détail disant que cette enzyme hydrolyse les deux liaisons est trop large : la molécule représentée contient une liaison α et une liaison β, qui n’ont pas la même spécificité enzymatique.',[course('Roneo_glucides_2',9,'Ronéo glucides 2 — spécificité des osidases')])
note('2020s2',22,'C','Le « 8 glucose-1-phosphate » imprimé dans le détail n’est pas un nombre fixe de produits par coupure. Une réaction de glycogène phosphorylase libère un glucose-1-phosphate et raccourcit la chaîne d’un résidu ; le nombre total dépend des coupures effectuées.',[PHOS], 'source_error')
note('2020s2',22,'E','Le détail inverse les effets hépatiques du glucagon : il favorise l’activation de la glycogène phosphorylase et l’inhibition de la glycogène synthase. L’expérience citée observe bien cette activation de la dégradation et cette inhibition de la synthèse.',[web('https://pubmed.ncbi.nlm.nih.gov/6432774/','Étude de 1984 — effets du glucagon sur phosphorylase et glycogène synthase')])
note('2020paces',21,'C','Pour déterminer α ou β, on compare le substituant oxygéné du carbone anomérique au groupement CH₂OH, pas l’hydrogène porté par C1. La liaison osidique se forme à partir d’un groupement hydroxyle ; la justification imprimée confond ces atomes.',[course('Roneo_glucides_2',1,'Ronéo glucides 2 — anomérie et cyclisation')])
note('2020paces',37,'D','La synthèse d’un glucose à partir de deux pyruvates consomme 4 ATP et 2 GTP, soit six liaisons phosphates riches en énergie. Un bilan limité à « 4 ATP » doit préciser qu’il ne compte pas les deux GTP.',[GNG], 'course_convention')
note('2019',27,'D','La conversion glucose-6-phosphate → glucose-1-phosphate ne consomme pas d’ATP. Dans le bilan partant du glucose libre, les dépenses sont sa phosphorylation et l’activation via l’UTP pour former l’UDP-glucose ; le détail attribue la dépense à une mauvaise étape.',[web('https://education.med.nyu.edu/mbm/carbohydrates/glycogen.shtml','NYU — synthèse et régulation du glycogène')])
note('2019',30,'A','À pH 2, les groupes acides de K, A et E sont majoritairement protonés, tandis que les groupes aminés sont positifs : ces trois acides aminés ne sont donc pas retenus comme des anions. La rétention proposée pour K et E sur un échangeur d’anions n’est pas cohérente avec ces charges.',[pdfref(408,'Table des pKa fournie dans la même série')])
note('2019',31,'A','L’urée dénature la protéine mais ne réduit pas, à elle seule, les ponts disulfure. Dans l’expérience d’Anfinsen, leur réduction fait intervenir un réducteur tel que le β-mercaptoéthanol ; il faut distinguer les deux traitements.',[web('https://williams.chemistry.gatech.edu/course_Information/6572_fall_2021/papers/ANFINSEN_1961.pdf','Anfinsen et collaborateurs, 1961 — réduction et renaturation de la ribonucléase')])
note('2019',33,'E','Le texte autour des Q32–33 intervertit certains pHi des fragments : avec les pKa fournis, TRDY a un pHi voisin de (3,7 + 9,1)/2 = 6,4, et LMCK de (8,2 + 9,8)/2 = 9,0. Le « 9 » invoqué pour le fragment de l’item E est donc litigieux, même si sa charge reste positive à pH 2.',[pdfref(408,'Table des pKa et peptide du sujet')], 'source_error')
note('2019',34,'BC','Les résultats annoncés Vmax = 2 × 10⁻⁷ et Km = 10⁻⁴ sont cohérents avec le graphique, mais certaines écritures intermédiaires des inverses et puissances de 10 ne le sont pas. Il faut lire Vmax = 1/(5 × 10⁶) et −1/Km = −10⁴.',[], 'source_error')
note('2019',36,'A','Le détail contient vraisemblablement une coquille : la néoglucogenèse produit du glucose à partir de précurseurs non glucidiques, comme le lactate ou certains acides aminés. L’expression « précurseurs glucidiques » ne décrit pas cette définition.',[GNG], 'source_error')

# Three repeated statements restart their letters midway. The non-corrected
# statement and the exact statement texts establish the correspondence A–E.
label_remappings={
 ('2023s1',27):['A','A','B','C','D'],
 ('2021s1',29):['A','B','A','B','C'],
 ('2021s1',37):['A','A','B','C','D']}
for (s,n),printed in label_remappings.items():
    bank,q=Q[s,n]
    q.setdefault('reviewNotes',[]).append({'bank':bank,'id':q['id'],'sourceId':str(n),'items':list('ABCDE'),'kind':'source_labels',
      'text':'La répétition de l’énoncé dans le corrigé comporte des lettres mal numérotées ('+', '.join(printed)+'). Les cinq propositions ont été rapprochées une à une du sujet non corrigé ; les lettres A à E du site suivent ce sujet et correspondent aux verdicts du tableau détaillé.',
      'refs':[pdfref(F[s,n]['subjectStart']['p'],'Sujet non corrigé')]+[pdfref(p) for p in sorted({l['page'] for l in F[s,n]['correctionLines']})],
      'sourceVerdict':q['answer'],'noteId':f'review-v6-biochimie-{s}-{n}-lettres'})
bank,q=Q['2020paces',35]
q.setdefault('reviewNotes',[]).append({'bank':bank,'id':q['id'],'sourceId':'35','items':['C'],'kind':'source_variant',
 'text':'Le sujet écrit [E]₀ = 1 × 10⁻⁴, tandis que sa répétition dans le corrigé écrit 11 × 10⁻⁴ mol·L⁻¹. Le site conserve la valeur du sujet. Les deux propositions restent fausses par rapport au résultat détaillé 11 × 10⁻⁸ mol·L⁻¹.',
 'refs':[pdfref(F['2020paces',35]['subjectStart']['p'],'Sujet non corrigé'),pdfref(390,'Répétition et détail du corrigé')],
 'sourceVerdict':q['answer'],'noteId':'review-v6-biochimie-2020paces-35-variante-C'})

# Resolve no key by invention. Existing contradictory questions remain ungraded;
# move their disclosed key comparisons out of the pre-correction warning.
for s,n in [('2022s1',25),('2022s1',38),('2021s1',34),('2021s1',36),('2020s1',18)]:
    bank,q=Q[s,n]; g=GRIDS[s,n];r=F[s,n]
    edit(s,n,'warning','Les sources de correction se contredisent ; ce QCM est exclu de la note.',reason='Les clés contradictoires ne doivent pas apparaître avant validation.')
    assert q['answer']=='' and not q.get('answerIsEmpty')
    detail=r['detailKey']; text=f'La grille récapitulative indique {g["key"]}, tandis que l’en-tête du corrigé détaillé indique {detail}.'
    if (s,n)==('2020s1',18):text+=' Les verdicts item par item donnent ABD.'
    q.setdefault('reviewNotes',[]).append({'bank':bank,'id':q['id'],'sourceId':str(n),'items':list('ABCDE'),'kind':'source_conflict','text':text+' Faute d’erratum permettant de départager ces indications, le QCM reste hors note ; vérifie la ronéo ou demande confirmation au tutorat.','refs':[pdfref(g['page'],'Grille de correction')]+[pdfref(p) for p in sorted({l['page'] for l in r['correctionLines']})],'sourceVerdict':'','noteId':f'review-v6-biochimie-{s}-{n}-contradiction'})

# Authentic source assets. The original manuscript annotations are not erased.
(HERE/'assets').mkdir(exist_ok=True)
asset_by_src={x['src']:x for x in INV}
replacements={}
for old,filename in [
 ('static/annales_ue2_362_40e72948b4.webp','paces2020_q19_original_annote.webp'),
 ('static/annales_ue2_v2_363_55b1bf102d7a.webp','paces2020_q21_22_original_annote.webp'),
 ('static/annales_ue2_364_39b487b29d.webp','paces2020_q24_original_annote.webp')]:
    loc=asset_by_src[old]['locator'];p=loc['page'];rect=fitz.Rect(loc['bbox'])
    pm=D[p-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False)
    target=HERE/'assets'/filename
    Image.frombytes('RGB',[pm.width,pm.height],pm.samples).save(target,'WEBP',lossless=True)
    src='static/revision_v6/biochimie/'+filename;replacements[old]=src
    assets.append({'file':str(target),'src':src,'source':{'file':str(PDF),'page':p,'rect':list(rect)},'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
for n in [19,21,22,24]:
    bank,q=Q['2020paces',n]
    if n in (19,24):
        q['stemImages']=[replacements.get(x,x) for x in q.get('stemImages',[])];q['imagesAfterCorrection']=True
    else:
        for context in q.get('sharedContexts',[]):
            context['images']=[replacements.get(x,x) for x in context.get('images',[])];context['imagesAfterCorrection']=True
    decisions.append({'sourceSet':'2020paces','sourceNumber':n,'decision':'subject_annotated_guarded','reason':'Le sujet fourni contient des annotations manuscrites qui dévoilent des éléments de réponse. Les pixels sont conservés et la copie/figure ne sera accessible qu’après correction.'})

# The old locators are only bounds: all following context intervals were read
# against the actual PDF, including the preceding page and the next heading.
trims_subject={
 ('2022s2',15):(217,86.8),('2021s1',30):(243,550.3),
 ('2020s1',24):(304,461.35),('2020s1',26):(305,72.5),('2020s1',32):(306,70.0),
 ('2020paces',20):(363,254.8),('2019',20):(405,276.3),('2019',31):(408,72.5),
 ('2024s2',26):(90,356.9)}
trims_correction={
 ('2022s2',15):(227,758.8),('2021s1',30):(267,318.4),
 ('2020s1',24):(320,205),('2020s1',26):(321,71),('2020s1',32):(323,330.7),
 ('2020paces',20):(383,72.5),('2019',20):(427,202.1),('2019',31):(432,382.7),
 ('2018',33):(476,241.7),('2018',36):(478,71),('2024s2',26):(108,71)}
contexts=[
 ('2022s2',[16,17],[(217,86.8,210.2)],[(227,758.8,780),(228,71.1,213.6)]),
 ('2021s1',[31,32,33],[(243,550.3,822)],[(267,318.4,600)]),
 ('2020s1',[25,26],[(304,461.35,552)],[(320,208.75,301.2)]),
 ('2020s1',[27,28],[(305,72.5,112.4)],[(321,71,130.9)]),
 ('2020s1',[33,34],[(306,70,339.3)],[(323,330.7,604.3)]),
 ('2020paces',[21,22],[(363,254.8,424.6)],[(383,72.5,259)]),
 ('2019',[17,18,19],[(404,303.1,372.0)],[(425,72.5,172.0)]),
 ('2019',[21,22,23],[(405,276.3,362.0)],[(427,202.1,295.6)]),
 ('2019',[32,33],[(408,72.5,303.5)],[(432,382.7,607)]),
 ('2018',[17,18,19],[(450,70.5,209.0)],[(469,69.5,209)]),
 ('2018',[37,38],[(455,70.5,301.5)],[(478,71,300.5)]),
]
CONTEXT={}
for s,nums,spec,cspec in contexts:
    for n in nums: CONTEXT[s,n]={'numbers':nums,'subject':spec,'correction':cspec}
CONTEXT['2018',34]={'numbers':[34],'subject':[],'correction':[(476,241.7,432.5)]}

CACHE={}
def lines(page):
    if page not in CACHE:
        out=[]
        for block in D[page-1].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                t=''.join(s['text'] for s in line['spans']).strip()
                if t and 60<=line['bbox'][1]<780:out.append({'page':page,'rect':list(line['bbox']),'text':t})
        CACHE[page]=sorted(out,key=lambda l:(round(l['rect'][1],1),l['rect'][0]))
    return CACHE[page]

def panel(page,top,bottom,number=None,label='Sujets + corrections compilés.pdf'):
    x={'file':str(PDF),'page':page,'rect':[0,max(0,top),D[page-1].rect.width,min(D[page-1].rect.height,bottom)],'fileLabel':label}
    if number is not None:x['sourceNumber']=number
    return x

def section(r,role):
    st=r[role+'Start'];en=copy.deepcopy(r[role+'End'])
    trim=(trims_subject if role=='subject' else trims_correction).get((r['sourceSet'],r['sourceNumber']))
    if trim and (trim[0],trim[1])<(en['p'],en['y']):en={'p':trim[0],'y':trim[1]+.8}
    result=[]
    for p in range(st['p'],en['p']+1):
        top=st['y']-2 if p==st['p'] else 62
        bottom=en['y']-.8 if p==en['p'] else 780
        if bottom-top<9:continue
        if not any(top-.1<=l['rect'][1]<bottom for l in lines(p)):
            continue
        result.append(panel(p,top,bottom,r['printedNumber'] if role=='subject' else r['sourceNumber']))
    return result

def combine_context(parts,spec,nums,role):
    # If the first question already contains the context, keep a single intact crop.
    extras=[]
    for p,top,bottom in spec:
        overlaps=[c for c in parts if c['page']==p and c['rect'][1]<=top+.5 and c['rect'][3]>=bottom-.5]
        if overlaps:continue
        # Same-page immediately preceding context can simply extend the first crop.
        adjacent=[c for c in parts if c['page']==p and c['rect'][1]<bottom+25 and c['rect'][1]>top]
        if adjacent:
            adjacent[0]['rect'][1]=top
        else:extras.append(panel(p,top,bottom,label='Énoncé commun — QCM '+', '.join(map(str,nums))+' — '+role))
    return extras+parts

crops=[]
for r in FRESH:
    s,n=r['sourceSet'],r['sourceNumber'];bank,q=Q[s,n]
    cp={'bank':bank,'id':q['id'],'subject':section(r,'subject'),'correction':section(r,'correction'),
        'subjectNumber':r['printedNumber'],'correctionNumber':n}
    c=CONTEXT.get((s,n))
    if c:
        for role in ('subject','correction'):cp[role]=combine_context(cp[role],c[role],c['numbers'],role)
    if (s,n)==('2020s1',30):
        inv=asset_by_src['static/annales_ue2_322_92bce5382d.webp']['locator']
        cp['subject'].insert(0,{'file':str(PDF),'page':322,'rect':inv['bbox'],'fileLabel':'Figure non annotée reproduite avec l’énoncé dans le corrigé','sourceNumber':30})
        cp['subjectNote']='La figure manque sur la page du sujet. Elle est reprise de la répétition non annotée de l’énoncé dans le corrigé, sans les réponses ni leur détail.'
    if s=='2020paces' and n in (19,21,22,24):
        cp['subjectAfterCorrection']=True
        cp['subjectNote']='Le document fourni contient des annotations manuscrites donnant des indices de réponse. La copie authentique et sa figure sont conservées sans effacement et deviennent accessibles après correction. Une version non annotée reste nécessaire.'
    g=GRIDS[s,n]
    cp['correction'].append({'file':str(PDF),'page':g['page'],'rect':g['rect'],'fileLabel':'Grille récapitulative de correction','sourceNumber':n})
    cp['correctionNote']='Le corrigé détaillé et la ligne de la grille récapitulative sont reproduits. Les éventuelles réserves scientifiques ne remplacent pas la clé du tutorat.'
    crops.append(cp)
CP={(r['bank'],r['id']):r for r in crops}

def in_main(l,r,role):
    st=r[role+'Start'];en=r[role+'End'];trim=(trims_subject if role=='subject' else trims_correction).get((r['sourceSet'],r['sourceNumber']))
    end=(en['p'],en['y']-.7)
    if trim and trim<end:end=trim
    return (st['p'],st['y']-.7)<=(l['page'],l['rect'][1])<end

def blocks(ls, remap=False):
    # A dash is a label separator only when followed by whitespace: D-glucose
    # at a wrapped line boundary is not an item D.
    starts=[]
    for i,l in enumerate(ls):
        m=re.match(r'^([A-E])(?:[.)]\s*|-\s+)(.*)',l['text'])
        if m:starts.append((i,m[1],m[2]))
    result={}
    for z,(i,letter,first) in enumerate(starts):
        end=starts[z+1][0] if z+1<len(starts) else len(ls)
        content=ls[i:end]
        logical='ABCDE'[z] if remap and len(starts)==5 else letter
        result[logical]={'literal':' '.join([first]+[x['text'] for x in content[1:]]).strip(),'printedLabel':letter,
                        'locations':[{'page':x['page'],'rect':x['rect'],'text':x['text']} for x in content]}
    return result

audit=[]
for r in FRESH:
    s,n=r['sourceSet'],r['sourceNumber'];bank,q=Q[s,n];g=GRIDS[s,n];cp=CP[bank,q['id']]
    sl=[l for p in range(r['subjectStart']['p'],r['subjectEnd']['p']+1) for l in lines(p) if in_main(l,r,'subject')]
    cl=[l for p in range(r['correctionStart']['p'],r['correctionEnd']['p']+1) for l in lines(p) if in_main(l,r,'correction')]
    candidates=[]
    for i,l in enumerate(cl):
        m=re.fullmatch(r'([ABCDE]{1,5})(?:\s+HORS PROGRAMME)?',l['text'])
        if m and l['rect'][0]<150:
            score=sum(bool(re.match(r'^[A-E][.)]\s*(VRAI|FAUX)',x['text'],re.I)) for x in cl[i+1:])
            candidates.append((score,i,m[1]))
    assert candidates,(s,n,'no detail key')
    _,ki,key=max(candidates)
    si,ci,di=blocks(sl),blocks(cl[:ki],remap=(s,n) in label_remappings),blocks(cl[ki+1:])
    # Side-by-side pKa tables are common data, not continuations of item prose.
    table_limit={('2020paces',32):390,('2018',33):420}.get((s,n))
    if table_limit:
        si=blocks([x for x in sl if x['rect'][0]<table_limit])
    row={'bank':bank,'id':q['id'],'sourceSet':s,'sourceNumber':n,'printedSubjectNumber':r['printedNumber'],
         'comparisonStatus':'compared_to_subject_and_correction',
         'subjectSource':cp['subject'],'correctionSource':cp['correction'],
         'instruction':{'site':q['question'],'subjectHeader':r['subjectStart']['title'],'correctedHeader':r['correctionStart']['title'],
                        'sharedContexts':q.get('sharedContexts',[]),'checkedPreviousAndNextPage':True},
         'shortKey':{'literal':g['rawText'],'answer':g['key'],'page':g['page'],'rect':g['rect']},
         'detailedKey':{'literal':cl[ki]['text'],'answer':key,'page':cl[ki]['page'],'rect':cl[ki]['rect']},
         'finalKey':q['answer'],'graded':bool(q['answer']) or bool(q.get('answerIsEmpty')),
         'subjectOriginalStatus':'annotated_hidden_until_correction' if cp.get('subjectAfterCorrection') else 'clean_available',
         'preservedPriorNotes':len(BASE[bank]['questions'][[x['id'] for x in BASE[bank]['questions']].index(q['id'])].get('reviewNotes',[])),
         'scientificNotes':q.get('reviewNotes',[]),'items':[]}
    if (s,n) in label_remappings:
        row['correctedStatementLabelMapping']={'printed':label_remappings[s,n],'logical':list('ABCDE'),'basis':'Texte intégral et ordre des cinq propositions rapprochés du sujet non corrigé ; les verdicts détaillés utilisent A–E.'}
    if (s,n)==('2020s1',30):row['subjectOriginalStatus']='clean_question_with_figure_from_repeated_statement'
    for option in q['options']:
        letter=option['id'];source=si.get(letter,{});corr=ci.get(letter,{});det=di.get(letter,{})
        literal=det.get('literal','');m=re.match(r'^(VRAI|FAUX)\b',literal,re.I)
        graphical=bool(option.get('image'))
        imageloc=None
        if graphical:
            inv=asset_by_src.get(option['image'])
            if inv:imageloc=inv['locator']
        edits_here=[e for e in edits if (e['bank'],e['id'],e['item'])==(bank,q['id'],letter)]
        row['items'].append({'id':letter,'status':'verified_with_source' if m else 'key_verified_detail_not_explicit',
            'siteText':option['text'],'subjectLiteral':source.get('literal'), 'subjectLocations':source.get('locations',[]),
            'correctedStatementLiteral':corr.get('literal'),'correctedStatementPrintedLabel':corr.get('printedLabel'),'correctedStatementLocations':corr.get('locations',[]),
            'renderedAsImage':graphical,'optionImage':option.get('image'),'optionImageSource':imageloc,
            'shortGridVerdict':'VRAI' if letter in g['key'] else 'FAUX',
            'detailedVerdictLiteral':m.group(1).upper() if m else literal,
            'detailedLiteral':literal,'detailLocations':det.get('locations',[]),
            'siteExplanation':q.get('explanations',{}).get(letter,''),'documentedRepairs':edits_here,
            'scientificNoteIds':[x['noteId'] for x in q.get('reviewNotes',[]) if letter in x.get('items',[])],
            'comparisonMethod':'Lecture du sujet et de sa répétition corrigée, contrôle de la lettre et du verdict/détail ; la proposition graphique est confrontée au rectangle original.' if graphical else 'Lecture des deux versions, de la lettre, de la grille et du détail ; les différences de composition sont conservées ou réparées explicitement.'})
        itemrow=row['items'][-1]
        a=source.get('literal','');c=corr.get('literal','')
        norm=lambda t:re.sub(r'\W+','',unicodedata.normalize('NFKC',t).lower())
        if norm(a)!=norm(c):
            if re.match(r'^'+letter+r'[.)]\s*',c) and norm(re.sub(r'^'+letter+r'[.)]\s*','',c))==norm(a):
                issue='Le label est imprimé deux fois dans la répétition corrigée ; même proposition.'
            elif (s,n,letter)==('2020paces',35,'C'):
                issue='Variante numérique du corrigé (1 contre 11) signalée dans une note ; valeur du sujet conservée.'
            elif (s,n)==('2021s1',24) and letter in 'AB':
                issue='La répétition du corrigé superpose/duplique des unités dans les deux premières propositions ; comparaison visuelle faite sur la composition et les données du sujet.'
            elif (s,n,letter)==('2019',25,'B'):
                issue='La répétition corrigée précise phospholipase C ; le sujet dit phospholipase. Les deux versions et leur différence sont conservées dans les copies, l’item suit le sujet.'
            else:
                issue='Différence typographique ou de composition du sujet répété ; les deux littéraux sont tracés, l’item interactif conserve le sujet.'
            itemrow['sourceVersionDifference']=issue
    audit.append(row)

missing=[
 {'kind':'clean_subject','source':'Annales_compilation.pdf','series':'2020–2021 PACES','sourceSet':'2020paces','sourceNumbers':[19,21,22,24],'pages':[362,363,364],
  'reason':'Les pages du sujet comportent des annotations manuscrites. Les répétitions corrigées p.381, 383 et 384 ne fournissent pas une variante propre.',
  'searched':['Sujet original de la compilation','Répétitions des énoncés dans le corrigé','Inventaire de tous les documents et six ronéos biochimiques disponibles'],
  'needed':'Sujet non annoté de cette série, avec les figures des Q19, Q21–22 et Q24.',
  'handling':'Pixels authentiques conservés, accessibles seulement après correction ; aucune suppression discrète des annotations.'},
 {'kind':'course_documents','needed':['Ronéo acides aminés et protéines','Ronéo enzymologie','Ronéos métabolisme glucidique, lipidique, cycle de Krebs et chaîne respiratoire'],
  'reason':'Aucun de ces cours spécifiques ne figure parmi les six ronéos biochimiques fournies. Les divergences repérées sont confrontées aux sources primaires citées et aux calculs, sans changer la clé officielle.',
  'searched':['documents_available.json','additional_documents.json','output/site/sources/revision_v4','Documents initiaux histo/biocell et biomol, hors contenu biochimie ciblé']},
 {'kind':'detail_not_explicit','sourceSet':'2020s1','sourceNumber':20,'item':'D','reason':'Le détail original dit seulement « Plus au programme ». La grille AE exclut D ; aucun verdict Vrai/Faux explicite ni justification de D n’est fourni.',
  'handling':'Grille conservée, absence du détail explicite tracée ; aucune explication inventée.'},
 {'kind':'coverage_boundary','reason':'L’audit couvre les 14 séries de biochimie déjà représentées (2018–2019 à 2025–2026), pas une garantie d’existence de toutes les sessions depuis 2015. Aucune autre série complète non importée n’a été établie dans les documents rapprochés.',
  'needed':'Sujets et corrigés supplémentaires pour toute année ou session non présente que l’utilisateur souhaite ajouter.',
  'handling':'Aucun QCM antérieur à 2015 ajouté ; aucune nouvelle série générale créée silencieusement.'}
]

source_manifest=[{'absolute':str(PDF),'packaged':'sources/Annales_compilation.pdf','sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()}]
for x in RONEOS:
    p=Path(x['file']);source_manifest.append({'absolute':str(p),'packaged':'sources/revision_v4/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
web_refs={ref['href']:ref for row in audit for note_ in row['scientificNotes'] if note_.get('noteId','').startswith('review-v6-') for ref in note_.get('refs',[]) if ref.get('href','').startswith('http')}
scientific_sources=[{'url':u,'label':r['label'],'consulted':'2026-11-22','role':'Réserve scientifique après correction ; ne remplace pas le verdict du tutorat.'} for u,r in sorted(web_refs.items())]
scientific_sources.append({'url':'https://www.reactome.org/content/detail/R-HSA-70994','label':'Reactome — succinate déshydrogénase, complexe II','consulted':'2026-11-22','role':'Signalement Q40 C de 2019 vérifié sans anomalie : le PDF et le site disent bien complexe II.'})
decisions.append({'sourceSet':'2019','sourceNumber':40,'item':'C','decision':'reported_issue_not_reproduced','sourcePage':439,'evidenceImage':'visual/2019_q40_detail.png','reason':'L’agrandissement de la source montre explicitement complexe II. Le site reproduit II. Le sujet propose III et le verdict faux est cohérent. Reactome R-HSA-70994 confirme II ; aucune fausse réserve ajoutée.'})
decisions.append({'sourceSet':'2023s2','sourceNumber':13,'decision':'outside_biochimie_scope','reason':'La question concerne la mutation en biologie moléculaire ; ce n’est pas une omission de la série biochimie.'})

dump('reviewed.json',reviewed);dump('audit.json',audit);dump('crops.json',crops);dump('missing.json',missing)
dump('asset_manifest.json',assets);dump('source_manifest.json',source_manifest);dump('scientific_sources.json',scientific_sources)
dump('changes.json',edits);dump('decisions.json',decisions)
counts={'banks':len(reviewed['banks']),'questions':len(audit),'items':sum(len(r['items']) for r in audit),
 'gradedQuestions':sum(r['graded'] for r in audit),'ungradedConflictingKeys':sum(not r['graded'] for r in audit),
 'cleanOriginalSubjects':sum(r['subjectOriginalStatus']=='clean_available' for r in audit),
 'cleanStatementWithFigureFromRepeat':sum(r['subjectOriginalStatus']=='clean_question_with_figure_from_repeated_statement' for r in audit),
 'annotatedSubjectsAfterCorrection':sum(r['subjectOriginalStatus']=='annotated_hidden_until_correction' for r in audit),
 'subjectCopies':len(crops),'correctionCopies':len(crops),'sourcePanels':sum(len(r['subject']) for r in crops),'correctionPanelsIncludingGrids':sum(len(r['correction']) for r in crops),
 'explicitItemVerdicts':sum(x['status']=='verified_with_source' for r in audit for x in r['items']),
 'detailNotExplicit':sum(x['status']!='verified_with_source' for r in audit for x in r['items']),
 'oldNotesPreserved':sum(r['preservedPriorNotes'] for r in audit),'newScientificNotes':len(extra_notes),'newConflictNotes':5,'newSourceLabelNotes':3,'newSourceVariantNotes':1,
 'editedFields':len(edits),'newAuthenticInteractiveAssets':len(assets),'sharedGroupsReviewed':13,
 'subjectPagesVisuallyViewed':81,'gridPagesVisuallyViewed':14,'interactiveAssetsDocumentaryGeometricChecked':177}
dump('counts.json',counts)
print(json.dumps(counts,ensure_ascii=False))
