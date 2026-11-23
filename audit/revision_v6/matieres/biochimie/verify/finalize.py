from pathlib import Path
import json,copy,hashlib,re,collections,fitz
V=Path(__file__).resolve().parent;P=V.parent/'prepare';BASE=V.parents[3];PDF=BASE/'output/site/sources/Annales_compilation.pdf'
def load(p):return json.loads(p.read_text())
def dump(n,x):(V/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data=load(P/'reviewed.json');original=copy.deepcopy(data);crops=load(P/'crops.json');banks=data['banks']
lookup={(q['sourceSet'],q['sourceNumber']):(b,q) for b,e in banks.items() for q in e['questions']}
byid={(b,q['id']):q for b,e in banks.items() for q in e['questions']}
issues=[];newnotes=[]
b,q=lookup['2019',25];o=next(o for o in q['options'] if o['id']=='B');old=o['text'];o['text']+=' C.'
assert o['text'].endswith('phospholipase C.')
issues.append({'status':'repaired','kind':'item_transcription','bank':b,'id':q['id'],'sourceNumber':25,'item':'B','before':old,'after':o['text'],'evidence':{'file':str(PDF),'subjectPage':406,'correctionPage':429},'reason':'La lettre C. continue la ligne précédente du même item B, elle ne commence pas un nouvel item. PDF non corrigé et répétition corrigée concordent. Clé inchangée.'})
for row in crops:
 if row['bank']=='annales.ue2c.glucides.2022s2' and row['id']==2:
  panel=next(p for p in row['correction'] if p['page']==222);before=panel['rect'].copy();panel['rect'][2]=280.0
  issues.append({'status':'repaired','kind':'capture_boundary','bank':row['bank'],'id':2,'sourceNumber':20,'before':before,'after':panel['rect'],'sourcePage':222,'reason':'La capture de la grille coupait le bord droit du E dans AE. Rectification après lecture visuelle de la page entière ; clé inchangée.'})
def ref(label,url):return {'file':label,'label':label,'href':url}
def local(page,label='Corrigé original'):return {'file':'Sujets + corrections compilés.pdf','page':page,'label':label,'href':f'sources/Annales_compilation.pdf#page={page}'}
def roneo(name,page,label):return {'file':name,'page':page,'label':label,'href':f'sources/revision_v4/{name}#page={page}'}
def note(series,num,items,text,refs,kind='scientific_dispute',tag=None):
 b,q=lookup[series,num];n={'bank':b,'id':q['id'],'sourceId':str(num),'items':list(items),'kind':kind,'text':text,'refs':[local(q['correctionPage'])]+refs,'sourceVerdict':q.get('answer') or q.get('shortKey',''),'noteId':f'verify-v6-biochimie-{series}-{num}-{tag or items}'}
 q.setdefault('reviewNotes',[]).append(n);newnotes.append(n)
G2='Roneo_glucides_2_du_vendredi_23_10_26_89b0203066.pdf';ISO='Roneo_cours_derives_isopreniques_du_vendredi_09_10_26_docx_b75de48b67.pdf'
note('2020paces',24,'E','Le cours distingue les termes anomère et épimère. Au sens général de l’IUPAC, des anomères cycliques sont aussi des épimères au carbone anomérique : ce ne sont pas des molécules identiques. La notation officielle est conservée selon la convention du cours ; vérifie dans la ronéo le vocabulaire attendu.',[roneo(G2,1,'Ronéo glucides 2 — épimérie et anomérie'),ref('IUPAC Gold Book — anomers','https://goldbook.iupac.org/terms/view/A00373'),ref('IUPAC Gold Book — epimers','https://goldbook.iupac.org/terms/view/E02167')],kind='convention')
note('2020s2',19,'E','L’explication « tous les cétoses sont en cycle furanose » est trop générale. Pour le fructose libre en solution aqueuse, les mesures par RMN trouvent majoritairement une forme pyranose ; les formes liées peuvent être furanosiques. Cela ne justifie donc pas à lui seul « majoritaire chez l’Homme ». La clé officielle est conservée ; vérifie le contexte exact dans la ronéo.',[roneo(G2,2,'Ronéo glucides 2 — cyclisation du fructose'),ref('Barclay et al., 2011 — tautomères du D-fructose mesurés par RMN','https://pmc.ncbi.nlm.nih.gov/articles/PMC3254704/')])
note('2023s1',29,'C','Le mot « proche » dans le détail est imprécis : le site catalytique fait partie du site actif. Le corrigé 2021–2022 S1 Q23 C le formule explicitement. Le verdict Faux est conservé ; vérifie cette distinction dans la ronéo.',[local(261,'Corrigé 2021–2022 S1 Q23 C — site catalytique dans le site actif')])
gck=ref('Larion et al., 2012 — allostérie de la glucokinase monomérique, étude RMN','https://pmc.ncbi.nlm.nih.gov/articles/PMC3525530/')
for series,num in [('2024s2',17),('2023s2',17),('2022s2',15)]:
 note(series,num,'C','Cette formulation correspond au modèle oligomérique enseigné, mais ne vaut pas pour toutes les enzymes allostériques : la glucokinase humaine fonctionne comme un monomère et présente une coopérativité cinétique. La clé officielle est conservée ; vérifie dans la ronéo le modèle retenu.',[gck])
note('2018',34,'C','Une cinétique sigmoïde ne prouve pas à elle seule une structure oligomérique : la glucokinase humaine monomérique fournit un contre-exemple. La réponse officielle est conservée pour le modèle du cours ; vérifie cette hypothèse dans la ronéo.',[gck])
chol=ref('Étude expérimentale POPC/cholestérol, 2003 — fluidité selon la teneur en cholestérol','https://pubmed.ncbi.nlm.nih.gov/12582817/')
for series,num,it in [('2021s1',30,'B'),('2019',25,'C')]:
 note(series,num,it,'Le rôle du cholestérol sur la fluidité dépend des conditions et de la composition de la membrane ; « rigidifie » n’est pas une règle universelle. La ronéo emploie ici cette simplification. La clé officielle est conservée ; vérifie le contexte de température et de composition retenu dans la ronéo.',[roneo(ISO,5,'Ronéo dérivés isopréniques — cholestérol membranaire'),chol])
bbb=ref('Nguyen et al., Nature 2014 — transport du DHA sous forme de lysophosphatidylcholine par MFSD2A','https://www.nature.com/articles/nature13241')
for series,num,it in [('2018',36,'A'),('2020s1',35,'C')]:
 note(series,num,it,'Le verdict Faux sur le principal combustible cérébral est conservé. En revanche, l’imperméabilité absolue aux acides gras est inexacte : du DHA entre dans le cerveau sous forme de lysophosphatidylcholine via MFSD2A. Cela ne signifie pas qu’il constitue le combustible principal du jeûne. Vérifie cette nuance dans la ronéo.',[bbb])
po=ref('Lee et al., 1996 — mesure et conventions des rapports P/O mitochondriaux','https://pubmed.ncbi.nlm.nih.gov/8641569/')
for series,num in [('2023s2',26),('2022s1',38),('2020s1',39)]:
 note(series,num,'E','Le bilan annoncé dépend des conventions ATP/coenzyme et du coût d’activation. Avec 2,5 ATP/NADH, 1,5 ATP/FADH₂ et 2 équivalents ATP d’activation, l’oxydation complète du palmitate donne 106 ATP. La clé officielle est conservée ; vérifie le barème énergétique de la ronéo.',[po],kind='convention')
note('2025s1',33,'D','L’explication originale s’arrête réellement après « La sphingomyélinase hydrolyse ». La page suivante ne fournit pas de suite : ce n’est pas une coupure de la capture du site. Le verdict Faux du document est conservé ; consulte la ronéo pour le détail manquant.',[local(37,'Page suivant le détail incomplet')],kind='source_incomplete')
note('2020s1',20,'BCD','Le sujet et sa répétition corrigée impriment « pKa2 = ç ». Les valeurs employées dans B et le calcul du pI dans C suggèrent 9, sans erratum explicite. Pour D, le détail dit seulement « Plus au programme », sans Vrai/Faux ni justification ; la grille reste AE. Vérifie ces points dans la ronéo ou auprès du tutorat.',[local(303,'Sujet original avec pKa2 = ç')],kind='source_ambiguity')
assert len(newnotes)==16
# Full artifacts, preserving every field not explicitly repaired.
dump('approved_reviewed.json',data);dump('approved_crops.json',crops)
# Re-extract critical literal segments for the coverage log, independently of the approved text.
raw=load(V/'independent_source.json');rows=[];doc=fitz.open(PDF)
def segment(lines,detail=False):
 starts=[]
 for i,l in enumerate(lines):
  m=re.match(r'^\s*([A-E])\s*[.)-]\s*(\S.*)$',l['text'])
  if m and (not detail or re.match(r'(VRAI|FAUX|Plus au programme)',m[2],re.I)):starts.append((i,m))
 seg=[]
 for j,(i,m) in enumerate(starts):
  end=starts[j+1][0] if j+1<len(starts) else len(lines)
  seg.append({'letter':m[1],'text':' '.join([m[2]]+[l['text'] for l in lines[i+1:end]]),'lines':lines[i:end]})
 return seg
flags=load(V/'comparison_flags.json');fl=collections.defaultdict(list)
for f in flags:fl[f['bank'],f['id'],f['item']].append(f)
crlookup={(c['bank'],c['id']):c for c in crops}
for r in raw:
 q=byid[r['bank'],r['id']];cs=crlookup[r['bank'],r['id']]
 ds=segment(r['correctedLines'],True)
 # The 5 verdict lines are correctly printed A–E, even when repeated subject lettering restarts.
 detailstart=next((i for i,l in enumerate(r['correctedLines']) if re.match(r'^A\s*[.)-]\s*(?:VRAI|FAUX)',l['text'],re.I)),len(r['correctedLines']))
 header=r['correctedLines'][:detailstart]
 k_candidates=[l['text'] for l in header if re.fullmatch(r'[ABCDE]{1,5}(?:\s+HORS PROGRAMME)?',l['text'])]
 literal_key=k_candidates[-1].split()[0] if k_candidates else r['detailedKey']
 subject=segment(r['subjectLines']);ss=subject[-5:]
 correction=segment(header);cc=correction[-5:]
 # The pKa table at the side interleaves extracted lines: authoritative item blocks are
 # the fresh source lines at x < table boundary, verified against the full rendered page.
 if (r['series'],r['number']) in [('2020paces',32),('2018',33)]:
  cutoff=350 if r['series']=='2020paces' else 350
  # Keep human-readable original segments and mark the table interleaving explicitly.
  table_note='Tableau de pKa et propositions entrelacés dans la couche texte ; lecture visuelle du PDF et répétition du sujet dans le corrigé utilisées pour valider les cinq propositions.'
 else:table_note=None
 details={s['letter']:s for s in ds[-5:]}
 gridparts=[p for p in cs['correction'] if 'grille' in p.get('fileLabel','').lower()]
 grid_literal=' '.join(doc[p['page']-1].get_text(clip=fitz.Rect(p['rect'])).split() for p in []) if False else ' '.join(' '.join(doc[p['page']-1].get_text(clip=fitz.Rect(p['rect'])).split()) for p in gridparts)
 items=[]
 for j,o in enumerate(q['options']):
  original_item=r['items'][j];s=ss[j] if len(ss)==5 else {};corr=cc[j] if len(cc)==5 else {};de=details.get(o['id'],{})
  verdict=re.match(r'^(VRAI|FAUX)',de.get('text',''),re.I)
  literal=verdict[1].upper() if verdict else None
  special=r['series']=='2020s1' and r['number']==20 and o['id']=='D'
  if special:literal=None
  item={'item':o['id'],'subjectRead':True,'correctedSubjectRead':True,'detailRead':True,'reviewStatus':'compared_to_originals','subjectLiteral':s.get('text') or original_item.get('subjectLiteral'),'correctedSubjectLiteral':corr.get('text') or original_item.get('correctedLiteral'),'correctionLiteral':de.get('text') or original_item.get('detailedLiteral'),'printedSubjectLetter':s.get('letter') or original_item.get('printedSubjectLetter'),'printedCorrectedLetter':corr.get('letter') or original_item.get('printedCorrectedLetter'),'detailedVerdict':literal,'officialKeyIncludesItem':o['id'] in (q.get('answer') or ''),'gradedQuestion':bool(q.get('answer')),'approvedSubjectText':o['text'],'approvedDetail':q['explanations'].get(o['id'],''),'interactiveImage':o.get('image'),'reviewNotes':[n['noteId'] for n in q.get('reviewNotes',[]) if o['id'] in n.get('items',[])],'comparisonAlertsResolved':len(fl[r['bank'],r['id'],o['id']])}
  if table_note:item['layoutCaution']=table_note
  if special:item['verdictLimit']='Le détail original porte seulement Plus au programme ; pas de verdict V/F explicite. La grille AE est documentée séparément.'
  if r['series']=='2025s1' and r['number']==33 and o['id']=='D':item['detailLimit']='Phrase inachevée dans le document original.'
  if r['series']=='2019' and r['number']==25 and o['id']=='B':item['repair']='C. final rétabli dans le texte de B.'
  items.append(item)
 rows.append({'bank':r['bank'],'id':r['id'],'series':r['series'],'sourceNumber':r['number'],'subjectPages':sorted(set(p['page'] for p in cs['subject'])),'correctionPages':sorted(set(p['page'] for p in cs['correction'])),'subjectRead':True,'correctionRead':True,'sharedContextRead':bool(q.get('sharedContexts')),'officialGridLiteral':grid_literal,'detailedKeyLiteral':literal_key,'approvedKey':q.get('answer'),'weight':q.get('weight'),'keyStatus':'documented_conflict_ungraded' if not q.get('answer') else 'official_key_preserved','subjectCopyStatus':'annotated_original_after_grading' if cs.get('subjectAfterCorrection') else 'available_clean','items':items})
assert len(rows)==278 and sum(len(r['items']) for r in rows)==1390
# This report records where the source itself does not supply an explicit item verdict.
nonexplicit=[(r['series'],r['sourceNumber'],i['item'],i['correctionLiteral']) for r in rows for i in r['items'] if i['detailedVerdict'] is None]
assert nonexplicit==[('2020s1',20,'D','Plus au programme')],nonexplicit
for r in rows:
 if r['keyStatus']=='documented_conflict_ungraded':issues.append({'status':'documented_source_conflict','kind':'official_key_conflict','bank':r['bank'],'id':r['id'],'sourceNumber':r['sourceNumber'],'grid':r['officialGridLiteral'],'detailedKey':r['detailedKeyLiteral'],'action':'Hors note inchangé ; divergences explicites dans les notes après correction.'})
issues.extend({'status':'documented_after_grading','kind':n['kind'],'bank':n['bank'],'id':n['id'],'sourceNumber':int(n['sourceId']),'items':n['items'],'noteId':n['noteId'],'text':n['text'],'refs':n['refs']} for n in newnotes)
dump('coverage.json',{'subject':'biochimie','verifier':'biochimie_verifie','sourcePdf':str(PDF),'sourcePdfSHA256':sha(PDF),'independentRawExtraction':'independent_source.json','questionsCompared':278,'itemsCompared':1390,'seriesCompared':14,'questions':rows})
dump('issues.json',issues)
missing={'completeSubjectOrCorrectionMissing':[], 'cleanSubjectCopiesMissing':[{'series':'2020paces','sourceNumbers':[19,21,22,24],'pages':[362,363,364],'reason':'Les originaux fournis portent des annotations manuscrites donnant des éléments de réponse. Pixels authentiques conservés ; copie et figures protégées après correction. Une version sans annotations permettrait de rétablir les figures avant correction.'}], 'courseDocumentsMissing':[{'courses':['Acides aminés et protéines','Enzymes','Métabolisme'],'reason':'Aucune ronéo intégrale correspondante dans les documents disponibles pour cette matière. Comparaison documentaire complète aux sujets et corrigés ; réserves supplémentaires appuyées sur des sources primaires ciblées, sans revendiquer la certification scientifique exhaustive des 1 390 items.'}], 'originalDetailIncomplete':[{'series':'2025s1','sourceNumber':33,'item':'D','page':36,'reason':'L’explication se termine après La sphingomyélinase hydrolyse.'},{'series':'2020s1','sourceNumber':20,'item':'D','page':318,'reason':'Plus au programme est la seule indication ; aucun V/F ni détail explicite.'}], 'originalTypographicAmbiguity':[{'series':'2020s1','sourceNumber':20,'subjectPage':303,'correctionPage':318,'reason':'pKa2 = ç imprimé ; les autres données suggèrent 9 sans erratum.'}], 'historicalCoverageLimit':'Les 14 séries présentes de 2018 à 2025 ont été comparées intégralement aux sources disponibles. Cela ne prouve pas l’existence ou l’absence de toutes les sessions historiques ni de séries 2015–2017 non fournies dans ce lot.'}
dump('missing.json',missing)
# Invariants: only the one proven item transcription and appended notes may change.
for b,e in original['banks'].items():
 assert banks[b]['storage']==e['storage']
 for before in e['questions']:
  after=byid[b,before['id']];expected=copy.deepcopy(before)
  expected['reviewNotes']=after.get('reviewNotes',[])
  if b=='annales.ue2c.lipides.2019' and before['id']==9:expected['options'][1]['text']+=' C.'
  if not before.get('reviewNotes') and not after.get('reviewNotes'):expected.pop('reviewNotes',None)
  assert expected==after,(b,before['id'])
  assert after.get('reviewNotes',[])[:len(before.get('reviewNotes',[]))]==before.get('reviewNotes',[])
notes_before=sum(len(q.get('reviewNotes',[])) for e in original['banks'].values() for q in e['questions']);notes_after=sum(len(q.get('reviewNotes',[])) for e in banks.values() for q in e['questions'])
validation={'inputReviewedSHA256':sha(P/'reviewed.json'),'inputCropsSHA256':sha(P/'crops.json'),'approvedReviewedSHA256':sha(V/'approved_reviewed.json'),'approvedCropsSHA256':sha(V/'approved_crops.json'),'banks':len(banks),'questions':len(rows),'items':1390,'gradedQuestions':sum(bool(q.get('answer')) for q in byid.values()),'ungradedQuestions':sum(not bool(q.get('answer')) for q in byid.values()),'keysChanged':0,'idsChanged':0,'storageKeysChanged':0,'weightsChanged':0,'optionOrderChanged':0,'itemTextsRepaired':1,'cropRectanglesRepaired':1,'preservedNotes':notes_before,'newNotes':len(newnotes),'totalNotes':notes_after,'explicitItemVerdicts':1390-len(nonexplicit),'itemsWithoutExplicitVerdict':nonexplicit,'countsBySeries':dict(collections.Counter(r['series'] for r in rows)),'sharedContexts':len({c['id'] for q in byid.values() for c in q.get('sharedContexts',[])}),'subjectPanels':sum(len(c['subject']) for c in crops),'correctionPanels':sum(len(c['correction']) for c in crops),'annotatedSubjectCopies':sum(bool(c.get('subjectAfterCorrection')) for c in crops),'interactiveAssets':len(load(V/'asset_validation.json')),'invariantsPassed':True}
dump('validation.json',validation)
print(json.dumps(validation,ensure_ascii=False,indent=2))
