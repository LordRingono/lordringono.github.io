"""Reviewed chemistry changes; the fresh source audit remains unmodified evidence."""
from pathlib import Path
import copy, hashlib, json, re
import fitz

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SITE=ROOT.parents[1]/'output/site'
PDF=SITE/'sources/Annales_compilation.pdf'
D=fitz.open(PDF)
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
ROWS=json.loads((HERE/'fresh_source_audit.json').read_text())
BANKS={b:copy.deepcopy(BASE[b]) for b in json.loads((ROOT/'roster.json').read_text())['chimie']['banks']}
if not (HERE/'baseline_crops.json').exists():
 (HERE/'baseline_crops.json').write_bytes((HERE/'crops.json').read_bytes())
CS=json.loads((HERE/'baseline_crops.json').read_text())
Q={(q['sourceSet'],q['sourceNumber']):(b,q) for b,v in BANKS.items() for q in v['questions']}
C={(r['bank'],r['id']):r for r in CS}
CHANGES=[]
def dump(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def explain(s,n,values):
 b,q=Q[s,n]
 for item,text in values.items():
  old=q.setdefault('explanations',{}).get(item)
  if old!=text:CHANGES.append({'bank':b,'id':q['id'],'item':item,'field':'explanations','before':old,'after':text,'reason':'Transcription du rendu original; indices/fractions ou repères des dessins rétablis.'})
  q['explanations'][item]=text
def ref(p,label):return {'file':'Sujets + corrections compilés.pdf','page':p,'label':label,'href':f'sources/Annales_compilation.pdf#page={p}'}
def note(s,n,items,text,extra=(),kind='possible_error'):
 b,q=Q[s,n]
 text+=' La clé officielle est conservée ; vérifier ce point dans la ronéo et, si nécessaire, le faire préciser par l’enseignant.'
 row={'bank':b,'id':q['id'],'sourceId':str(n),'items':list(items),'kind':kind,'text':text,'refs':[ref(q['subjectPage'],f'Sujet original, Q{q.get("printedSourceNumber",n)}'),ref(q['correctionPage'],'Corrigé original'),*extra],'sourceVerdict':q['answer'],'courseVerdict':None,'noteId':f'review-v6-chimie-{s}-{n}-{"".join(items)}'}
 q.setdefault('reviewNotes',[]).append(row)
 CHANGES.append({'bank':b,'id':q['id'],'field':'reviewNotes','noteId':row['noteId'],'text':text})
def course(file,page,label):return {'file':file.rsplit('/',1)[-1],'page':page,'label':label,'href':file+f'#page={page}'}
def web(url,label):return {'file':label,'label':label,'href':url}
ch12='sources/revision_v4/Chap_1_et_2_chimie_phy_260918_170147_9d9e60bef2.pdf'
ch3='sources/revision_v4/Chap_3_chimie_phy_260906_130652_137a0f5169.pdf'
ch6='sources/revision_v4/cHAP_6_chimie_phy_260918_180842_0dc69384ac.pdf'

# Repair flattened mathematics without silently changing the official reasoning.
explain('2024s1',48,{
 'A':'VRAI : Dans cet item nous cherchons une longueur d’onde pour l’atome d’hydrogène. Le corrigé commence par calculer l’énergie d’ionisation à n=4 : Eᵢ = 0 − E₄, avec E₄ = −13,6 × Z²/n² = −13,6 × 1/4² = −0,85 eV, donc Eᵢ = 0,85 eV. E = hc/λ, d’où λ = hc/E = (6,626 × 10⁻³⁴ × 2,997 × 10⁸)/(0,85 × 1,602 × 10⁻¹⁹) = 1458,33 nm. Convertir les eV en J. Voir la réserve ci-dessous sur « quatrième niveau d’excitation ».',
 'B':'VRAI : Eᵢ = E∞ − E₁ = 0 − E₁. E₁ = −13,6 × Z²/n² = −13,6 × 3²/1² = −122,40 eV. Donc Eᵢ = 0 − (−122,4) = 122,4 eV.',
 'C':'VRAI : Il faut calculer l’énergie pour n=4 : E = −13,6 × Z²/n² = −13,6 × 3²/4² = −7,65 eV.',
 'D':'FAUX : Pour que l’énergie d’ionisation soit égale à 13,6 eV, il faut que Z²/n² = 1. Or Z=35 et n=34.'})
explain('2023s1',1,{
 'B':'VRAI : À l’état initial, le corrigé écrit E(₃Li⁺) = −13,6 × 3²/1² = −122,4 eV. Pour l’ioniser : Eᵢ = E∞ − Eₙ₌₁ = 0 − (−122,4) = 122,4 eV. Voir la réserve ci-dessous sur la charge de Li⁺.',
 'C':'VRAI : État fondamental n=1 ; premier état excité n=2 ; cinquième état excité n=6. Le calcul imprimé est ΔE₆→₁ = 13,6 × 3² × (1/1² − 1/6²) = 119 eV = 119 × 1,602 × 10⁻¹⁹ J. ΔE = hc/λ, donc λ = (6,626 × 10⁻³⁴ × 2,997 × 10⁸)/(119 × 1,602 × 10⁻¹⁹) = 1,0417 × 10⁻⁸ m = 10,4 nm. Voir la réserve sur Li⁺.',
 'D':'VRAI : Eᵢ = E∞ − Eₙ₌₉ = 0 − (−13,6 × 9² × 1/9²) = 13,6 eV. Le corrigé rappelle que les énergies des états liés sont négatives et les énergies d’ionisation ou d’excitation positives.'})
explain('2022s1',43,{
 'A':'FAUX : Second niveau excité : n=3. L’énergie, notée E₂ dans le corrigé, est calculée pour n=3 : −13,6 × Z²/n² = −13,6 × 1²/3² = −13,6/9 = −1,51 eV. Eᵢ = E∞ − E₂ = 0 − (−1,51) = 1,51 eV : l’énergie d’ionisation est positive.',
 'B':'FAUX : Ce sont les mêmes valeurs. Pour H au fondamental : E = −13,6 eV, donc Eᵢ = 0 − E = 13,6 eV. Pour ₄Be³⁺ à n=4 : E₄ = −13,6 × Z²/n² = −13,6 × 4²/4² = −13,6 eV, donc Eᵢ = 13,6 eV également.',
 'C':'FAUX : ΔE₁→₂ < ΔEᵢ. Avec ΔE = hc/λ, la longueur d’onde est inversement proportionnelle à ΔE : λ₁→₂ > λᵢ.'})
explain('2021s2',27,{
 'A':'VRAI : l=1 correspond à la sous-couche p ; 16 électrons se trouvent dans les sous-couches p. Le corrigé donne la configuration Se : 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁴.',
 'B':'FAUX : Les électrons de valence sont ceux de 4s et 4p ; il y en a 6.',
 'C':'FAUX : Pour S : 1s² 2s² 2p⁶ 3s² 3p⁴. S et Se appartiennent à la même colonne (p⁴). Se est plus bas (n=4 contre n=3 pour S) ; l’électronégativité augmente de bas en haut et de gauche à droite. S est plus électronégatif que Se.',
 'D':'FAUX : ₃₄Se²⁻ possède 34 protons et 36 électrons.',
 'E':'FAUX : Le corrigé invoque r = (n*²/Z*) × a₀, constate que Se²⁻ et Kr possèdent chacun 36 électrons et la configuration 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶, puis affirme qu’ils auraient les mêmes n* et Z* et des rayons identiques. Cette dernière déduction fait l’objet de la réserve ci-dessous.'})
b,q=Q['2021s2',27]
q['warning']='Le corrigé imprime A, B, A, B, C devant ses cinq justifications. Leur rattachement à A–E a été rétabli par comparaison du texte de chaque proposition et de son ordre avec le sujet. La copie originale permet de vérifier ce rapprochement.'
C[b,q['id']]['correctionNote']='Les cinq justifications sont imprimées sous A, B, A, B, C. Elles sont rattachées aux items A–E selon leur contenu et leur ordre, sans changer la clé A.'
explain('2019',41,{
 'A':'VRAI : Entité 4 dans le plan : on permute son numéro avec l’entité à l’arrière du plan puis on inverse la configuration obtenue. Le dessin conduit de S à R.',
 'B':'VRAI : Entité 4 à l’avant du plan (liaisons horizontales de Fischer à l’avant) : on inverse la configuration obtenue. Le dessin conduit de R à S.',
 'C':'VRAI : La justification est graphique : le groupe entouré correspond à −CH₂CH₃. Voir le schéma dans le corrigé original.'})
explain('2019',43,{
 'B':'VRAI : La chaîne principale doit d’abord contenir le carbone portant la fonction principale (ici l’alcool), puis avoir le maximum de carbones possible. Enfin, elle doit contenir les éventuelles liaisons multiples (ici la double liaison). Voir la numérotation sur le dessin du corrigé.',
 'D':'VRAI : Les entités 1 et les entités 2 sont opposées (ce sont des « Ennemis »). Voir les priorités indiquées sur le dessin du corrigé.'})

# Reserve an error in the official document, keep its official key and wording.
note('2024s2',27,'E','Le détail E compte « 5 C, 1 N et 17 H ». Le décompte des deux structures dessinées donne 7 carbones, soit C₇H₁₇N. La conclusion d’isomérie de constitution reste cohérente ; c’est le comptage du corrigé qui est litigieux.')
note('2023s1',5,'D','La justification D parle d’un aldéhyde au lieu d’une cétone alors que l’item D porte sur le nombre de carbones asymétriques. Cette phrase figure déjà dans le corrigé original et ne justifie donc pas l’item. Le détail E du même corrigé précise que les structures 3 et 4 possèdent chacune un seul C*.')
note('2023s1',6,'E','Le détail E emploie « mélange racémique » puis explique qu’un centre préexistant garde sa configuration et que les deux produits sont diastéréoisomères. Un racémate est un mélange équimolaire de deux énantiomères ; ce terme ne convient pas à cette paire de diastéréoisomères.',[web('https://goldbook.iupac.org/terms/view/R05025','IUPAC — racemate'),web('https://goldbook.iupac.org/terms/view/D01679','IUPAC — diastereoisomerism')])
note('2023s2',28,'D','Le détail D propose C₈H₁₈O. La structure 3 dessinée est une pentan-3-one, C₅H₁₀O : la condensation de deux molécules suivie de la perte d’une molécule d’eau conduit à C₁₀H₁₈O. Le verdict faux de l’item C₆H₁₀O reste compatible avec ce bilan, mais la formule de remplacement du corrigé paraît erronée.')
note('2023s2',29,'C','Le calcul original écrit « niveau 2 » tout en utilisant n=6, puis 1,04 × 10⁸ = 10,4 nm. Il manque le signe moins et l’unité m dans cette dernière égalité : 10,4 nm = 1,04 × 10⁻⁸ m. La différence d’énergie affichée de 119 eV n’est pas remise en cause par ces coquilles.',[ref(173,'Suite du détail C et calcul imprimé')])
note('2023s1',1,'A','Le détail A parle de niveaux « 0 et infini ». Pour l’hydrogène dans ce modèle, le niveau fondamental est n=1 ; n=0 n’est pas un nombre quantique principal permis. Le raisonnement comparatif sur les énergies et les longueurs d’onde doit se lire entre n=1, n=350 et la limite d’ionisation.',[course(ch12,9,'Ronéo — transitions entre niveaux')])
note('2021s1',44,'A','La configuration Cr³⁺ proposée dans le détail A se termine en 3d¹. À partir de Cr : [Ar] 4s¹ 3d⁵, on retire d’abord l’électron 4s puis deux électrons 3d : Cr³⁺ est [Ar] 3d³. Le verdict faux de l’item reste conservé ; la configuration de remplacement du corrigé est le point litigieux.',[course(ch12,16,'Ronéo — exceptions de configuration'),course(ch12,17,'Ronéo — formation des ions')])
note('2021s1',40,'D','Le corrigé emploie « énantiomère de constitution », qui mélange deux relations distinctes. Les structures 2 et 5 ont une connectivité différente : il s’agit d’isomérie de constitution, ce qui est compatible avec le verdict faux donné à l’item qui affirme une relation d’énantiomérie.')
note('2021s1',42,'C','Le détail C rejette « un alcool » au motif que le produit est une cyanhydrine. Or la définition IUPAC classe les cyanhydrines parmi les alcools substitués par un groupe cyano. La distinction pédagogique attendue semble être « cyanhydrine » plutôt que le nom de classe plus général ; la rédaction et le verdict nécessitent donc une clarification.',[web('https://goldbook.iupac.org/terms/view/C01489/html','IUPAC — cyanohydrins')])
note('2020s1',45,'C','Le corrigé attribue l’exception Mg/Al à une sous-couche « demi-pleine » de Mg. Mg possède 3s², une sous-couche pleine, alors qu’Al possède 3s²3p¹. L’ordre d’énergie d’ionisation Al < Mg < Cl est conservé ; c’est la description de la sous-couche qui paraît erronée.',[course(ch3,8,'Ronéo — exception entre colonnes 2 et 13')])
note('2020s2',27,'D','Le détail D omet les parenthèses de l’écran de Slater et écrit 11,15. Le calcul décrit est 34 − (2 × 1 + 8 × 0,85 + 7 × 0,35) = 34 − 11,25 = 22,75. Le résultat de l’item est cohérent, mais les étapes imprimées comportent une coquille.',[course(ch12,21,'Ronéo — coefficients d’écrantage')])
note('2020s2',28,'C','L’enceinte est indilatable. Dans le modèle des gaz parfaits à température constante, ajouter N₂ inerte augmente la pression totale mais laisse chaque pression partielle réactive pᵢ=nᵢRT/V inchangée ; cela ne déplace donc pas l’équilibre. Le verdict faux de l’item « vers la droite » peut être conservé, mais la justification « vers la gauche » est litigieuse. La table de la ronéo fournie contient elle aussi cette difficulté : il faut faire préciser l’hypothèse du cours.',[course(ch6,7,'Ronéo — tableau des perturbations à clarifier'),web('https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants','OpenStax — quotient en pressions partielles')])
note('2020paces',44,'C','Le détail C invoque une inversion de Walden parce que F est un alcool secondaire. Dans la synthèse de Williamson dessinée, l’alcoolate attaque le carbone du bromométhane CH₃Br : la substitution SN2 ne se fait pas sur le carbone portant initialement OH dans F. Celui-ci porte deux groupes benzyle identiques. Le verdict faux est conservé, mais l’explication stéréochimique doit être précisée.',[ref(396,'Détail C original'),web('https://openstax.org/books/organic-chemistry/pages/18-2-preparing-ethers','OpenStax — synthèse de Williamson')])
note('2020paces',45,'A','Le détail A nomme le produit 1 « une amine ». Le dessin représente plus précisément une énamine (motif C=C–N), obtenue ici avec une amine secondaire. La précision de vocabulaire manque dans le corrigé ; les propositions D et E restent celles de la clé officielle.')
note('2018',42,'D','Le détail C affirme que les structures 1 et 2 sont énantiomères, tandis que le détail D les appelle diastéréoisomères. Ces deux phrases du même corrigé se contredisent ; avec un seul centre asymétrique et des configurations opposées, la relation décrite en C est l’énantiomérie. Le verdict faux de D ne change pas.')
note('2018',47,'ABCDE','La justification générale écrit que le chlore aurait « 6 normalement » électrons de valence. Cl (Z=17) possède 3s²3p⁵, donc 7 électrons de valence. La clé C du schéma de Lewis est conservée ; c’est ce nombre dans le détail qui est litigieux.',[ref(173,'Corrigé 2023–2024 S2, Q30 D : configuration et 7 électrons de valence du chlore')])
note('2019',47,'D','L’item et son détail parlent d’« hyperconjugaison » de l’amine avec le cycle C, mais la justification invoque une suite d’atomes sp². Cela décrit plutôt une conjugaison du doublet avec le système π ; au sens IUPAC, l’hyperconjugaison implique des liaisons σ et un réseau π ou une orbitale p. Le vocabulaire du cours mérite ici une clarification.',[web('https://goldbook.iupac.org/terms/view/H02924','IUPAC — hyperconjugation')])

def panel(p,y0,y1):return {'file':str(PDF),'page':p,'rect':[0,y0,D[p-1].rect.width,y1],'fileLabel':'Sujets + corrections compilés.pdf'}
def cp(s,n):
 b,q=Q[s,n];return C[b,q['id']]

# Include the introductions placed before the printed question, avoid the following one.
cp('2024s2',27)['subject']=[panel(90,353,591)]
cp('2024s2',27)['correction']=[panel(108,68,473)]
cp('2024s2',28)['subject'][0]['rect'][1]=83
cp('2024s2',28)['correction'][0]['rect'][1]=482
Q['2024s2',27][1]['sourceEndPage']=90
# Shared contexts copied for both questions, without another question's propositions.
cp('2021s1',41)['subject'].insert(0,panel(246,68,263))
cp('2021s1',41)['correction'].insert(0,panel(271,538,677))
cp('2020paces',41)['subject'][-1]['rect'][3]=611
cp('2020paces',41)['correction'][-1]['rect'][3]=318
for n in (42,43):
 cp('2020paces',n)['subject'].insert(0,panel(368,610,823))
 cp('2020paces',n)['correction'].insert(0,panel(394,319,536))
cp('2020paces',46)['subject'][-1]['rect'][3]=220
cp('2019',47)['subject'][-1]['rect'][3]=609

grids={'2025s1':20,'2024s1':60,'2024s2':94,'2023s1':126,'2023s2':160,'2022s1':190,'2022s2':222,'2021s1':250,'2021s2':286,'2020s1':310,'2020s2':340,'2020paces':372,'2019':416,'2018':460}
gridrows=[]
for s,p in grids.items():
 pairs=dict((int(n),k) for n,k in re.findall(r'N°\s*(\d+)\s*\n\s*([ABCDE]+|HP|/|—)\s*\n',D[p-1].get_text()))
 for (s2,n),(b,q) in Q.items():
  if s2!=s:continue
  key=pairs.get(n)
  assert key==q['shortKey'],(s,n,key,q['shortKey'])
  gridrows.append({'bank':b,'id':q['id'],'sourceSet':s,'sourceNumber':n,'page':p,'readKey':key,'detailedKey':q.get('detailedKey'),'gradedKey':q['answer'],'status':'concordant' if key==q['answer'] else 'contradiction_officielle_hors_note'})
  if s=='2018' and n==49:
   # The conflict is directly reviewable in the correction menu too.
   pg=D[p-1]
   word=pg.search_for('N°49')[0]
   cp(s,n)['correction'].append({'file':str(PDF),'page':p,'rect':[word.x0-5,word.y0-4,min(pg.rect.width,word.x0+150),word.y1+5],'fileLabel':'Sujets + corrections compilés.pdf','sourceNumber':49})
   cp(s,n)['correctionNote']='La grille courte porte A et le corrigé détaillé porte C. Les deux preuves sont incluses ; ce QCM reste hors note.'

visual_subject_pages=sorted({16,17,18,57,58,90,91,112,113,157,158,186,187,219,246,247,283,307,308,337,338,368,369,370,411,412,413,414,456,457,458})
visual_corr_pages=sorted({81,108,127,130,172,173,211,272,274,298,329,355,395,396,439,441,480,483})
aud=[]
for r in ROWS:
 b,q=Q[r['sourceSet'],r['sourceNumber']]
 old=BASE[b]['questions'][next(i for i,v in enumerate(BASE[b]['questions']) if v['id']==q['id'])]
 items=[]
 for i in r['items']:
  option=next(x for x in q['options'] if x['id']==i['id'])
  original_status='image_originale_controlee_sur_page' if option.get('image') or option['text']=='Proposition reproduite ci-dessous.' else 'texte_compare_au_sujet_et_corrige'
  items.append({'id':i['id'],'sourceText':i['sourceText'],'correctedSourceText':i['correctedSourceText'],'siteText':option['text'],'subjectComparison':original_status,'officialVerdict':None if not q['answer'] else i['id'] in q['answer'],'sourceDetail':i['sourceExplanation'],'finalDetail':q.get('explanations',{}).get(i['id']),'detailStatus':'transcription_reparee' if old.get('explanations',{}).get(i['id'])!=q.get('explanations',{}).get(i['id']) else ('detail_graphique_ou_general_original' if not q.get('explanations') else 'compare'),'scientificNotes':[x['noteId'] for x in q.get('reviewNotes',[]) if i['id'] in x.get('items',[])]})
  if r['sourceSet']=='2024s2' and r['sourceNumber']==27 and i['id']=='E': items[-1]['extractionBoundaryNote']='Le texte brut ajoute le contexte Q28 de la page suivante ; cette suite a été explicitement exclue, le site garde seulement E.'
  if r['sourceSet']=='2020paces' and r['sourceNumber']==41 and i['id']=='E': items[-1]['extractionBoundaryNote']='Le contexte commun Q42/Q43 est distinct de E et a été déplacé dans les copies concernées.'
 aud.append({'bank':b,'id':q['id'],'sourceSet':r['sourceSet'],'sourceNumber':r['sourceNumber'],'printedSubjectNumber':q.get('printedSourceNumber'),'subjectPages':sorted({x['page'] for x in C[b,q['id']]['subject']}),'correctionPages':sorted({x['page'] for x in C[b,q['id']]['correction']}),'subjectCompared':True,'correctedSubjectCompared':True,'detailCompared':True,'shortKeyCompared':True,'shortKey':q['shortKey'],'detailedKey':q.get('detailedKey'),'finalKey':q['answer'],'subjectPageVisual':True,'correctionPagesVisual':[p for p in visual_corr_pages if p in [x['page'] for x in C[b,q['id']]['correction']]],'items':items})

for c in CS:
 b,q=next((b,q) for b,v in BANKS.items() for q in v['questions'] if b==c['bank'] and q['id']==c['id'])
 for role in ('subject','correction'):
  for x in c[role]:
   x.setdefault('sourceNumber',q.get('printedSourceNumber',q['sourceNumber']) if role=='subject' else q['sourceNumber'])
   rect=fitz.Rect(x['rect']);assert not rect.is_empty and D[x['page']-1].rect.contains(rect),(c,role,x)
 c.setdefault('subjectNote','Copie du sujet original, avec le contexte et les figures nécessaires. Le numéro imprimé est conservé lorsqu’il diffère de celui du corrigé.')

missing=[{'type':'arbitrage_cle','bank':Q['2018',49][0],'id':Q['2018',49][1]['id'],'documents':'UE2 2018–2019, sujet imprimé Q50 / corrigé Q49','request':'Erratum ou clarification officielle de la clé A dans la grille versus C dans le détail. Les documents sont présents ; le QCM reste hors note.'},{'type':'couverture_documentaire','request':'Annales de chimie 2015–2016, 2016–2017 et 2017–2018 si leur ajout est souhaité : ces sessions ne figurent pas dans les 14 séries de chimie représentées dans la compilation disponible. Ne pas confondre absence du document avec omission vérifiée du site.'}]
dump('reviewed.json',{'banks':BANKS});dump('crops.json',CS);dump('audit.json',aud);dump('changes.json',CHANGES);dump('grids.json',gridrows);dump('missing.json',missing);dump('asset_manifest.json',[])
dump('coverage_preparer.json',{'questions':86,'items':430,'banks':38,'series':14,'subjectCopies':86,'correctionCopies':86,'notedQuestions':85,'ungradedQuestions':1,'subjectPagesVisuallyRead':visual_subject_pages,'correctionPagesVisuallyRead':visual_corr_pages,'shortGridsReadTextually':list(grids.values()),'allSourceAndCorrectionTextRead':True,'addedScientificNotes':sum(x['field']=='reviewNotes' for x in CHANGES),'changedDetails':sum(x['field']=='explanations' for x in CHANGES),'newQuestions':0,'keysChanged':0,'itemsChanged':0,'notesPreserved':True})
print(json.dumps({'questions':len(aud),'items':sum(len(r['items']) for r in aud),'changes':len(CHANGES),'source_panels':sum(len(x['subject']) for x in CS),'correction_panels':sum(len(x['correction']) for x in CS),'notes':sum(x['field']=='reviewNotes' for x in CHANGES)},ensure_ascii=False))
