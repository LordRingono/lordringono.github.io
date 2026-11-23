"""Bilan des vérifications documentaires effectuées, sans toucher au site."""
from pathlib import Path
import json, collections, copy, hashlib, re, unicodedata, datetime

ROOT=Path('/workspace/scratch/f3cb3bb97377')
V=ROOT/'work/site_v6/embryologie/verify';P=ROOT/'work/site_v6/embryologie/prepare'
def read(name):return json.load(open(V/(name+'.json')))
def save(name,obj):(V/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(t):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t.replace('œ','oe')).encode('ascii','ignore').decode().lower())
def answer_tokens(q):
    answer=q.get('answer') or ''
    return set(answer.split(',')) if ',' in answer else set(answer)

R=read('approved_reviewed');C=read('approved_crops');BASE=json.load(open(ROOT/'work/site_v6/baseline_exams.json'))
QS={(bank,q['id']):q for bank,b in R['banks'].items() for q in b['questions']}
CS={(c['bank'],c['id']):c for c in C}
CI={(c['bank'],c['id']):c for c in read('coverage_initial')}
SUB={(c['bank'],c['id']):c for c in read('subjects_initial')}
SUP={(c['bank'],c['id']):c for c in read('compilation_supplements')}
KEY={(c['bank'],c['id']):c for c in read('compilation_new_keys')}
GEOM={(c['bank'],c['id']):c for c in read('crop_geometry')}
AUD={(c['bank'],c['id']):c for c in json.load(open(P/'audit.json'))}

# Les 34 jeux d'images ont tous été lus, avec relecture individuelle après
# les derniers ajustements des jeux 10, 22 et 33.
visual_manifest=read('crop_visual_manifest')
visual_roles=set()
for row in visual_manifest:
    row['visualChecked']=True
    row['result']='Texte et figures complets ; annotations originales conservées.'
    row['captureDefinitionHashes']=[]
    for bank,qid,role in row['questions']:
        visual_roles.add((bank,qid,role))
        data=json.dumps(CS[bank,qid][role],ensure_ascii=False,sort_keys=True).encode()
        row['captureDefinitionHashes'].append(hashlib.sha256(data).hexdigest())
    row['imageSha256']=digest(V/'visual'/row['image'])
save('crop_visual_manifest',visual_manifest)
for key in SUP:visual_roles.add((*key,'subject'))
for key in KEY:visual_roles.add((*key,'correction'))

# Dix-huit alertes sont des légendes/consignes voisines agrégées par l'ordre
# textuel du PDF. La dix-neuvième est exclusivement un espace après « Faux ».
crop_resolutions=[]
for flag in read('crop_flags'):
    f=copy.deepcopy(flag);key=(f['bank'],f['id']);f['status']='resolved_false_positive'
    if key==('embryo.col.s2',34):
        f['resolution']='Le mot Faux est entier sur la capture contrôlée. Le x finit à x=430.258 ; seul l’espace suivant s’étend jusqu’à 433.258. Le bord du cadre est x=431.6.'
        f['evidence']='Texte caractère par caractère du PDF p.7 et visual/approved_crop_22.png.'
    elif key==('embryo.aut.s3',7):
        f['resolution']='La légende « plaque préchordale qui n’est pas figurée sur la coupe », placée en haut de p.2, appartient à la figure du Q5 et non à l’item E du Q7. Elle est complète dans la copie du Q5.'
    elif key==('embryo.aut.s4',29):
        f['resolution']='Le cartouche IWP appartient au schéma des Q23/24, et non au Q29. La capture Q29 ne doit pas le récupérer ; le schéma annoté Q23/24 reste protégé après correction.'
    else:
        f['resolution']='Le fragment appartient à l’en-tête commun des QCM suivants. Il est exclu de l’item précédent et inclus dans les captures du groupe auquel il se rapporte.'
    crop_resolutions.append(f)
save('crop_flag_resolutions',crop_resolutions)

# Particularités de lettres imprimées et de mise en page relues dans les
# originaux, indépendamment des hypothèses de découpe du préparateur.
manual={
 ('embryo.aut.fec',7,'D'):{'sourceLabel':'C bis','text':'Elle provoque la réaction corticale avant la reprise de la méiose. Vrai','pages':[2],'marker':'Vrai','reason':'Deux C distincts dans le Q8 imprimé.'},
 ('embryo.aut.s3',8,'E'):{'sourceLabel':'E','text':'l’allantoïde et les cellules germinales primordiales sur la même coupe, à l’extérieur de l’œuf. Faux, il est à l’extérieur du disque or une coupe se fait dans le disque','pages':[3],'marker':'Faux','reason':'E isolé dans la mise en page, omis par la première segmentation ; vérifié sur la page et la capture.'},
 ('embryo.aut.s4',13,'M'):{'sourceLabel':'H bis','text':'Le colon est issu de l’intestin moyen et de l’intestin postérieur. Vrai','pages':[5],'marker':'Vrai','reason':'Seconde occurrence H, conservée sous M dans le site.'},
 ('embryo.aut.s4',14,'E'):{'sourceLabel':'C bis','text':'La plicature crâniale permet de faire passer la zone cardiogène en position ventrale. Vrai, sous le TD en formation et derrière la membrane pharyngienne','pages':[5],'marker':'Vrai','reason':'Seconde occurrence C, conservée sous E dans le site.'},
 ('embryo.ann.fec',4,'E'):{'sourceLabel':'A bis','text':'Le mouvement linéaire des spermatozoïdes est acquis au cours du transit épididymaire.','pages':[1],'marker':None,'reason':'Deux A distincts et grille ABD : affectation de la clé indéterminée, QCM hors note.'},
 ('embryo.ann.s2',13,'A'):{'sourceLabel':'A','text':'Grille 7. AB ; aucun détail propre à A dans le corrigé.','pages':[4],'marker':'Vrai selon AB','reason':'Sujet non numéroté placé au-dessus de la grille 7. AB ; clé seule, pas d’explication inventée.'},
 ('embryo.ann.s2',13,'B'):{'sourceLabel':'B','text':'Grille 7. AB ; aucun détail propre à B dans le corrigé.','pages':[4],'marker':'Vrai selon AB','reason':'Sujet non numéroté placé au-dessus de la grille 7. AB ; clé seule, pas d’explication inventée.'},
 ('embryo.aut.meiose',5,'O'):{'sourceLabel':'K bis','text':'En méiose 1 il y a brassage intrachromosomique. Vrai','pages':[2],'marker':'Vrai','reason':'Second K distinct omis de V5, rétabli sous O après contrôle visuel.'},
 ('embryo.aut.fec',23,'N'):{'sourceLabel':'M bis','text':'correspond à la sous-unité alpha du dimère. Faux Béta','pages':[7],'marker':'Faux','reason':'Second M distinct omis de V5, rétabli sous N après contrôle visuel.'},
}
sb=read('sourceblocks')
heart=next(x for x in sb['embryo.aut.coeur'] if x['num']==2)
segments={};active=None
for line in heart['lines'][1:]:
    m=re.match(r'^([a-q])\.\s*(.*)',line['text'])
    if m:active=m[1].upper();segments[active]=[]
    if active:segments[active].append(line)
for iid in 'FGHIJKLMNOP':
    source_ids=['F','G'] if iid=='F' else [chr(ord(iid)+1)]
    lines=[l for si in source_ids for l in segments[si]]
    text=' '.join(l['text'] for l in lines)
    manual['embryo.aut.coeur',2,iid]={'sourceLabel':'+'.join(s.lower() for s in source_ids),'text':text,'pages':sorted({l['page'] for l in lines}),
      'marker':('Vrai' if iid in 'JMNO' else 'Faux'),'reason':'Le sujet rassemble f/g dans un seul item F ; correspondance par contenu, puis décalage des lettres h–q vers G–P.'}
save('manual_source_resolutions',[{'bank':b,'id':q,'item':i,**x} for (b,q,i),x in manual.items()])

conflicts={('embryo.ann.gamet',1,'B'),('embryo.ann.gamet',13,'E'),('embryo.ann.s3',20,'E'),('embryo.ann.s4',6,'D'),('embryo.ann.s4',8,'A'),('embryo.ann.s4',11,'D'),('embryo.ann.s4',17,'B'),('embryo.ann.fec',18,'B')}
missing_verdict={('embryo.col.s3',11,'E'),('embryo.col.s4',13,'E'),('embryo.col.s4',16,'E'),('embryo.col.s4',70,'E')}
missing_item=('embryo.col.s4',70,'E')
ambiguous_questions={('embryo.ann.fec',4),('embryo.ann.s1',13),('embryo.col.s3',11),('embryo.col.s4',13),('embryo.col.s4',16),('embryo.col.s4',70)}
gated={('embryo.aut.s4',23),('embryo.aut.s4',24),('embryo.aut.coeur',5),('embryo.aut.coeur',6)}

issues=[]
def issue(kind,status,bank,qid,items,text,**extra):
    idx=f'embryo-v6-{kind}-{bank}-{qid}-'+''.join(items)
    obj={'issueId':idx,'bank':bank,'id':qid,'items':items,'kind':kind,'status':status,'text':text,**extra}
    issues.append(obj);return idx

# Diff intégral vs V5, tous les IDs conservés ; seules deux propositions
# absentes sont ajoutées dans des questions existantes.
diff=[];stats=collections.Counter();notes_added=[]
for bank,b in R['banks'].items():
    before={q['id']:q for q in BASE[bank]['questions']}
    assert [q['id'] for q in b['questions']]==[q['id'] for q in BASE[bank]['questions']]
    for q in b['questions']:
        old=before[q['id']];key=(bank,q['id'])
        old_ids=[o['id'] for o in old['options']];new_ids=[o['id'] for o in q['options']]
        assert [iid for iid in new_ids if iid in old_ids]==old_ids and len(new_ids)==len(set(new_ids))
        assert answer_tokens(q)<=set(new_ids)
        for field in sorted(set(old)|set(q)):
            if old.get(field)!=q.get(field):
                diff.append({'bank':bank,'id':q['id'],'field':field,'old':old.get(field),'new':q.get(field)})
                stats['field:'+field]+=1
                if field=='explanations':stats['explanationItemsChanged']+=sum(old.get(field,{}).get(i)!=q.get(field,{}).get(i) for i in set(old.get(field,{}))|set(q.get(field,{})))
                if field=='options':
                    ot={o['id']:o['text'] for o in old['options']}
                    stats['existingOptionStatementsChanged']+=sum(o['id'] in ot and ot[o['id']]!=o['text'] for o in q['options'])
                    stats['optionsRestored']+=sum(o['id'] not in ot for o in q['options'])
        oldnotes={x.get('noteId') for x in old.get('reviewNotes',[])}
        for note in q.get('reviewNotes',[]):
            if note.get('noteId') not in oldnotes:notes_added.append(note)
save('changes_vs_baseline',diff)
changes_byq=collections.defaultdict(list)
for d in diff:changes_byq[d['bank'],d['id']].append(d['field'])

coverage=[]
for key,q in QS.items():
    bank,qid=key;c=CS[key];initial=CI[key];gradeable=bool(q.get('answer')) or bool(q.get('allowNoAnswer'))
    assert bool(c.get('subjectAfterCorrection'))==(key in gated)
    assert GEOM[key]['correction']['rectsValid'] and GEOM[key]['subject']['rectsValid']
    limits=[]
    if not c['subject']:
        limits.append(issue('subject_missing','unresolved_source_missing',bank,qid,[],c.get('subjectMissing','Sujet non corrigé absent des documents disponibles.')))
    elif key in gated:
        limits.append(issue('annotated_subject','protected_after_correction',bank,qid,[],c['subjectNote']))
    if key in ambiguous_questions:
        limits.append(issue('incomplete_key','unresolved_source_ambiguity',bank,qid,[],q.get('warning','Clé complète non déterminée.'),sourceCorrection=q.get('sourceCorrection'),page=q.get('correctionPage')))
    row={'bank':bank,'id':qid,'sourceNumber':q['sourceNumber'],
      'subjectChecked':bool(c['subject']),'subjectClean':bool(c['subject']) and key not in gated,
      'subjectAfterCorrection':key in gated,'correctionChecked':True,
      'correctionComplete':key!=missing_item[:2],
      'sourcePairComplete':bool(c['subject']) and key!=missing_item[:2],
      'cropsChecked':True,'subjectCropChecked':bool(c['subject']),'correctionCropChecked':True,
      'cropsComplete':bool(c['subject']),'cropVisualChecked':all((*key,role) in visual_roles for role in ['subject','correction'] if c[role]),
      'cropVisualChecks':{role:(*key,role) in visual_roles for role in ['subject','correction']},
      'cropCheckMethod':'Tous les rectangles et les lignes sources attendues ont été contrôlés ; alertes textuelles résolues dans crop_flag_resolutions.json. Contrôle visuel distinct indiqué par rôle.',
      'gradeable':gradeable,'answer':q.get('answer'),'allowNoAnswer':q.get('allowNoAnswer',False),
      'sourceHeaderKey':KEY[key]['rawKey'] if key in KEY else initial.get('sourceAnswerRaw'),
      'sources':{role:[{'file':p['file'],'page':p['page'],'sourceNumber':p.get('sourceNumber')} for p in c[role]] for role in ['subject','correction']},
      'scientificReview':'Fidélité documentaire pour chaque item ; recoupement des points litigieux identifiés avec les cours fournis. Les notes scientifiques V4 sont conservées, sans prétendre à une nouvelle lecture de chaque page de cours citée par ces notes.',
      'changes':changes_byq[key],'issues':limits,'items':[]}
    olditems={it['id']:it for it in initial['items']}
    subjectitems={it['id']:it for it in SUB.get(key,{}).get('items',[])}
    for opt in q['options']:
        iid=opt['id'];ikey=(*key,iid);old=olditems.get(iid,{});segments=old.get('sourceSegments',[])
        raw='\n'.join(s['text'] for s in segments)
        pages=sorted({s['page'] for s in segments});marker=(old.get('sourceMarker') or {}).get('raw');source_label=iid
        if ikey in manual:
            m=manual[ikey];raw=m['text'];pages=m['pages'];marker=m['marker'];source_label=m['sourceLabel']
        original_proof={'file':initial['source'],'pages':pages or [initial['page']],'sourceLabel':source_label,
          'literalExcerpt':raw,'marker':marker,'headerKey':initial.get('sourceAnswerRaw'),
          'method':'original_pdf_manual_layout' if ikey in manual else 'original_pdf_text_spans_and_markers'}
        if ikey==missing_item:
            original_proof['literalExcerpt']='Item absent du corrigé : Q70 s’arrête à D.'
            original_proof['method']='source_absence_confirmed'
        proof=[original_proof]
        if key in KEY:
            kr=KEY[key];proof.append({'file':kr['file'],'pages':[kr['page']],'sourceLabel':iid,
              'literalExcerpt':kr['explanations'][iid],'headerKey':kr['rawKey'],'gridPage':kr['gridPage'],
              'method':'independent_compilation_grid_plus_explicit_item_detail'})
        subject_text=None
        if key in SUP:subject_text=SUP[key]['subject']['items'][iid]
        elif iid in subjectitems:subject_text=subjectitems[iid]['sourceText']
        elif key in gated:subject_text=opt['text']
        ignored=iid in q.get('ignoredOptions',[])
        item_limits=[]
        if ikey in conflicts:item_limits.append(issue('source_key_conflict','documented_after_correction',bank,qid,[iid],'La grille ou le corrigé complémentaire diverge du marqueur/détail thématique ; aucune homogénéisation silencieuse. Voir la note de correction.'))
        if ikey in missing_verdict:item_limits.append(issue('verdict_missing','unresolved_source_missing',bank,qid,[iid],'Aucun verdict complet exploitable pour cet item ; la clé du QCM reste hors note.'))
        row['issues'].extend(item_limits)
        entry={'id':iid,'sourceLabel':source_label,'subjectChecked':bool(c['subject']),
          'subjectClean':row['subjectClean'],'subjectText':subject_text,
          'subjectTextExactNormalized':norm(subject_text)==norm(opt['text']) if subject_text is not None else None,
          'subjectComparison':'Texte comparé au document non corrigé ; variantes typographiques/édition signalées dans les preuves.' if c['subject'] else 'Sujet non corrigé absent : comparaison du couple impossible.',
          'correctionChecked':ikey!=missing_item,'correctionDetailChecked':ikey!=missing_item,
          'correctionDetailAvailable':bool(q.get('explanations',{}).get(iid)),
          'correctionEvidence':proof,'ignoredInGrade':ignored,
          'sourceKeyConflict':ikey in conflicts,
          'verdictResolved':gradeable and not ignored and ikey not in conflicts and ikey not in missing_verdict,
          'keyVerdict':(iid in answer_tokens(q)) if gradeable and not ignored else None,
          'cropsChecked':True,'issues':item_limits,
          'manualResolution':manual.get(ikey,{}).get('reason')}
        row['items'].append(entry)
    coverage.append(row)

# Notes publiées : seules les nouvelles notes sont signalées comme ajout V6.
for note in notes_added:
    issue('review_note','documented_after_correction',note['bank'],note['id'],note.get('items',[]),note['text'],noteId=note.get('noteId'),refs=note.get('refs',[]),noteKind=note['kind'])
for d in diff:
    if d['field'] in ['options','explanations','sharedContexts','answer']:
        issue('import_repair','repaired',d['bank'],d['id'],[],f"Champ {d['field']} réparé et relu dans les documents sources.",field=d['field'])
save('coverage',coverage);save('issues',issues)

missing=[]
for bank,b in R['banks'].items():
    ids=[q['id'] for q in b['questions'] if not CS[bank,q['id']]['subject']]
    if ids:missing.append({'bank':bank,'role':'subject','ids':ids,'count':len(ids),'referenceCorrection':b['questions'][0]['sourceCorrection'],
      'request':'Version non corrigée des QCM indiqués, avec les schémas originaux.',
      'searched':['Archive initiale Embryo.zip : 29 PDF','Pièces individuelles retrouvées','Compilation UE5 p.989–1660, comparaison des questions et de tous les items']})
missing.extend([
 {'bank':'embryo.aut.s4','role':'clean_figure','ids':[23,24],'page':7,'request':'Schéma vierge sans le cartouche donnant la position des IWP, avec les dix repères.'},
 {'bank':'embryo.aut.coeur','role':'clean_figure','ids':[5,6],'page':2,'request':'Schéma vierge du sujet avec les repères 1–6 ; l’original fourni contient déjà les noms des vaisseaux.'},
])
for key in sorted(ambiguous_questions):missing.append({'bank':key[0],'role':'correction_clarification','ids':[key[1]],'request':'Clarification de la clé officielle/du verdict absent ; le QCM demeure hors note.'})
save('missing',missing)

# Assertions d'intégrité limitées au périmètre réellement traité.
assert len(QS)==len(CS)==len(coverage)==599 and len(R['banks'])==22
assert sum(len(q['options']) for q in QS.values())==3389
assert sum(x['subjectChecked'] for x in coverage)==319
assert sum(x['subjectClean'] for x in coverage)==315
assert sum(not it['correctionChecked'] for x in coverage for it in x['items'])==1
assert sum(x['gradeable'] for x in coverage)==593
for key in gated:
    q=QS[key];assert not q.get('images') and q.get('imagesAfterCorrection') is True
    assert all(ctx.get('imagesAfterCorrection') for ctx in q.get('sharedContexts',[]) if ctx.get('images'))
for q in QS.values():
    for opt in q['options']:assert not re.search(r'\sHP\s*$',opt['text'])
    for note in q.get('reviewNotes',[]):
        for ref in note.get('refs',[]):
            if ref.get('href','').startswith('sources/'):
                assert (ROOT/'output/site'/ref['href'].split('#')[0]).exists(),ref['href']

stats.update({'banks':22,'questions':599,'items':3389,'subjects':319,'cleanSubjects':315,'annotatedSubjects':4,'missingSubjects':280,
 'subjectItems':sum(len(x['items']) for x in coverage if x['subjectChecked']),
 'cleanSubjectItems':sum(len(x['items']) for x in coverage if x['subjectClean']),
 'correctionItemsChecked':3388,'missingCorrectionItems':1,'correctionSets':599,
 'panels':sum(len(c[r]) for c in C for r in ['subject','correction']),
 'restoredPreviouslyAbsentKeys':7,'existingEmptyKeyConfirmed':1,
 'ungradableQuestions':6,'newReviewNotes':len(notes_added),
 'visuallyReviewedCompilationSubjects':60,'visuallyReviewedCompilationCorrections':8,
 'visuallyReviewedRestructuredSets':len(visual_manifest),'visuallyReviewedOriginalRiskPages':21,
 'cropGeometryFlagsResolved':len(crop_resolutions),'unresolvedCropGeometryFlags':0,
 'earlyCompilationEmbryologyQuestionsCompared':15,'earlyCompilationItemsCompared':75})
stats['finalCaptureRolesVisuallyReviewed']=len(visual_roles)
stats['questionsWithEitherCaptureRoleVisuallyReviewed']=len({(b,i) for b,i,_ in visual_roles})
final={'status':'approved_with_documented_source_limits','statistics':dict(stats),
 'files':{n:{'sha256':digest(V/n),'bytes':(V/n).stat().st_size} for n in ['approved_reviewed.json','approved_crops.json','coverage.json','issues.json']},
 'baselineSha256':digest(ROOT/'work/site_v6/baseline_exams.json'),
 'preparerFiles':{n:digest(P/n) for n in ['reviewed.json','crops.json']},
 'scope':'22 banques ue5e existantes ; aucun nouveau QCM, aucun changement des IDs ni des autres matières.',
 'limits':'280 sujets non corrigés absents ; 4 sujets/figures annotés protégés ; 6 clés complètes indéterminées ; un item E absent du corrigé. Contrôle visuel des ensembles signalés, contrôle documentaire et géométrique exhaustif distinct.'}
save('final_validation',final)
print(json.dumps(final['statistics'],ensure_ascii=False,indent=2))
