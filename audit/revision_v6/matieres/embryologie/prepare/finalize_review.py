"""Evidence-backed final manual fixes after the deterministic draft builders.

Run after review_builder.py and build_crops.py. This script does not change
any source PDF or any deployed site file.
"""
import json,pathlib,copy,re,unicodedata,hashlib,collections
P=pathlib.Path(__file__).parent;ROOT=P.parents[3]
def read(n):return json.load(open(P/n))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
D=read('reviewed.json');B=D['banks'];A=read('audit.json');C=read('crops.json');CH=read('changes.json');M=read('source_manifest.json');F=read('residual_flags.json')
def qget(b,i):return next(q for q in B[b]['questions'] if q['id']==i)
def aget(b,i):return next(q for q in A if q['bank']==b and q['id']==i)
def cget(b,i):return next(q for q in C if q['bank']==b and q['id']==i)
def change(b,q,f,v,why):
 if q.get(f)==v:return
 CH.append({'bank':b,'id':q['id'],'field':f,'old':copy.deepcopy(q.get(f)),'new':copy.deepcopy(v),'reason':why});q[f]=v
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s or '').lower().replace('œ','oe'))

# Original 2018 subject recovered independently from the general compilation.
supp=json.load(open(P.parent/'verify/compilation_supplements.json'))
sp=next(r for r in supp if r['bank']=='embryo.ann.gamet' and r['id']==13)
b='embryo.ann.gamet';q=qget(b,13);opts=copy.deepcopy(q['options'])
for o in opts:
 if o['id'] in ['A','B','D']:o['text']=sp['subject']['items'][o['id']]
change(b,q,'options',opts,'Sujet original 2018–2019, compilation p.1604 : précision métaphase I restituée en A ; commentaires du corrigé retirés des items B et D et conservés après correction.')
for f,v in [('sourceSubject','Annales_compilation.pdf'),('subjectPage',1604),('sourceEndPage',1604),('warning','')]:change(b,q,f,v,'Provenance exacte du sujet non corrigé retrouvé dans la compilation générale.')
note={'bank':b,'id':13,'items':['A','B','D'],'kind':'source_conflict','noteId':'embryo-v6-ann-gamet13-original-subject','text':'L’énoncé original 2018–2019 retrouvé dans la compilation précise « ovocyte I en métaphase I » en A. Les phrases explicatives sur la spermatogonie et les cellules somatiques, ajoutées en couleur dans le corrigé thématique, appartiennent aux explications de B et D et sont retirées des propositions. La clé du corrigé thématique reste inchangée ; sa contradiction sur E est signalée séparément.','refs':[{'file':'Annales_compilation.pdf','page':1604,'label':'Sujet UE5 2018–2019 — Q3, compilation p. 1604','href':'sources/Annales_compilation.pdf#page=1604'}]}
q.setdefault('reviewNotes',[]).append(note)
row=cget(b,13);row.update(subject=[{'file':sp['file'],'page':1604,'rect':sp['subject']['rect']}],subjectFile='Annales_compilation.pdf',subjectNote='Sujet original 2018–2019 provenant de la compilation générale, Q3 p.1604. Le corrigé thématique demeure une édition distincte et conserve sa propre clé.');row.pop('subjectMissing',None)
ar=aget(b,13);ar.update(sourceSubject='Annales_compilation.pdf',subjectPages=[1604],status='subject_and_correction_compared',subjectEvidence='Sujet complet rendu et relu visuellement, compilation p.1604 ; appariement indépendant du vérificateur.')
for r in ar['items']:
 r['siteStatement']=next(o['text'] for o in opts if o['id']==r['id']);r['subjectStatement']=sp['subject']['items'][r['id']];r['status']='matched_subject';r['subjectPages']=[1604]

# Repairs explicitly read in the source images by both members of the binôme.
for b,i,letters in [
 ('embryo.ann.s1',12,{
 'B':'Vrai : c’est bien à J3, lors de la TME, qu’on passe du génome maternel au génome embryonnaire.',
 'D':'Vrai : en effet les cellules sont totipotentes jusqu’à J4 (=morula), où elles deviennent alors pluripotentes.',
 'E':'Faux : les gènes soumis à l’empreinte parentale ne subissent pas de reprogrammation épigénétique'}),
 ('embryo.ann.s3',13,{'E':'Dans le corrigé, « phénomènes de segmentation. » est barré. Annotation ajoutée : « par la chorde et la plaque préchordale par SHH ».'})]:
 q=qget(b,i);ex=copy.deepcopy(q['explanations']);ex.update(letters);change(b,q,'explanations',ex,'Relecture visuelle indépendante du PDF : caractères omis et fin de ligne rétablis littéralement.')
 for r in aget(b,i)['items']:
  if r['id'] in letters:r['sourceDetail']=letters[r['id']];r['visualDetailChecked']=True

# The original documents called ENONCE already contain answer-bearing labels.
for b,ids,note in [
 ('embryo.aut.s4',[23,24],'Le document fourni comme sujet comporte déjà l’annotation « Là où se trouvent les IWP », qui donne un indice sur l’item E du QCM24. La copie originale est conservée intacte et accessible après correction.'),
 ('embryo.aut.coeur',[5,6],'Le schéma du document fourni comme sujet est déjà légendé avec les noms des vaisseaux. La copie originale est conservée intacte et accessible après correction.')]:
 for i in ids:
  q=qget(b,i);change(b,q,'imagesAfterCorrection',True,'Schéma source déjà annoté, à afficher après correction seulement.')
  contexts=copy.deepcopy(q.get('sharedContexts',[]))
  for ctx in contexts:ctx['imagesAfterCorrection']=True
  change(b,q,'sharedContexts',contexts,'Le schéma commun annoté suit la même restriction d’affichage que sa copie originale.')
  row=cget(b,i);row['subjectAfterCorrection']=True;row['subjectNote']=(row.get('subjectNote','')+' '+note).strip()
  aget(b,i)['subjectDisclosure']='original_annotated_available_after_correction'
  assert not q.get('originalImages') and not q.get('stemImages'),(b,i,'unprotected alternate image list')

# The J13 stem had no printed question number. It is now separated from the
# preceding 3.CD correction in segments.json, with its own subject and full crop.
ar=aget('embryo.ann.s2',13)
ar['manualBoundary']='PDF p.4 : sujet sans numéro à y=332.32, items A–E à y=569.82–646.61 ; clé 7.AB à y=666.81. Aucun élément ne doit être ajouté à la correction du QCM précédent.'
for r in ar['items']:
 r['sourceHeaderKey']='AB'
 if r['id'] in ['A','B']:
  r['rawVerdict']='Vrai selon la clé AB';r['sourcePages']=[4];r['status']='matched_subject_key_only';r['sourceText']='Clé imprimée 7. AB ; aucun détail propre à cet item dans le corrigé.'

# Resolve only exact extraction-layout differences or identified source typos.
E=read('extraction.json')
typos={('embryo.aut.coeur',9,'N'):'Le sujet omet le a de extra ; le corrigé donne extra-embryonnaire.',('embryo.ann.s2',11,'E'):'Accents/pluriels et coquille grosses/grossesses, sans changement de sens.',('embryo.ann.coeur',15,'C'):'Le sujet contient l s ; Les deux est lisible dans le corrigé.',('embryo.ann.coeur',18,'E'):'RAS isolé dans le sujet est une note parasite ; la phrase du corrigé ne le contient pas.',('embryo.col.s4',48,'C'):'Nom Hensen rétabli depuis le corrigé, lettres manquantes dans le sujet.',('embryo.col.s4',54,'A'):'Ordinal 4e rétabli depuis le corrigé.'}
for flag in F:
 key=(flag['bank'],flag['id'],flag['item']);ar=aget(key[0],key[1]);it=next(x for x in ar['items'] if x['id']==key[2]);source=ar['sourceSubject']
 alltext=' '.join(l['text'] for page in E.get(source,[]) for l in page['lines'])
 if key in typos:
  flag['resolution']=typos[key];flag['status']='resolved_source_typo';it['status']='source_typo_repaired';it['resolution']=typos[key]
 elif norm(flag['site']) in norm(alltext):
  flag['resolution']='La phrase complète est présente dans le sujet. La différence vient de plusieurs items extraits sur une même ligne, d’une lettre isolée ou d’un en-tête commun adjacent.';flag['status']='resolved_line_layout';it['status']='matched_subject_after_line_split';it['resolution']=flag['resolution']
 else:
  flag['status']='pending_independent_verifier';flag['resolution']='Ne pas déclarer ce rapprochement acquis sans la dernière passe du vérificateur.'

# Give every newly created correction note a functional exact PDF link.
hashpaths={hashlib.sha256(f.read_bytes()).hexdigest():'sources/revision_v4/'+f.name for f in (ROOT/'output/site/sources/revision_v4').glob('*.pdf')}
for b in B.values():
 for q in b['questions']:
  for n in q.get('reviewNotes',[]):
   for ref in n.get('refs',[]):
    if not ref.get('href') and ref.get('file') in M:
     dest=hashpaths.get(M[ref['file']]['sha256'])
     if dest:ref['href']=dest+'#page='+str(ref['page'])

missing=[]
for b,bank in B.items():
 ids=[r['id'] for r in C if r['bank']==b and r.get('subjectMissing')]
 if ids:missing.append({'bank':b,'role':'subject','questionIds':ids,'reason':'Aucun sujet propre correspondant dans les PDF thématiques ; cette liste de préparation précède la fusion des 60 sujets retrouvés dans la compilation par le vérificateur (un, ann.gamet13, est déjà intégré ici).','searched':['29 PDF originaux Embryo.zip','7 sujets distincts','parties énoncé des PDF mixtes','compilation : résultats du vérificateur à fusionner'],'pendingSupplement':'work/site_v6/embryologie/verify/compilation_supplements.json'})
write('reviewed.json',D);write('audit.json',A);write('crops.json',C);write('changes.json',CH);write('residual_flags.json',F);write('missing.json',missing)
summary={'questions':len(A),'items':sum(len(x['items']) for x in A),'banks':len(B),'subjectCopies':sum(bool(x['subject']) for x in C),'correctionCopies':sum(bool(x['correction']) for x in C),'panels':sum(len(x[r]) for x in C for r in ['subject','correction']),'annotatedSubjectsAfterCorrection':sum(bool(x.get('subjectAfterCorrection')) for x in C),'pendingFlags':sum(x['status']=='pending_independent_verifier' for x in F),'fieldChanges':len(CH),'changesByField':dict(collections.Counter(x['field'] for x in CH))}
summary['banksCoverage']=[{'bank':b,'questions':len(v['questions']),'items':sum(len(q['options']) for q in v['questions']),'subjects':sum(bool(c['subject']) for c in C if c['bank']==b),'corrections':sum(bool(c['correction']) for c in C if c['bank']==b),'preparerCheckpoint':'complete_pending_independent_verification'} for b,v in B.items()]
write('coverage_preparer.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
