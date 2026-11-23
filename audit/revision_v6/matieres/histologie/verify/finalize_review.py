"""Assemble the verifier's decisions; never writes outside this verify directory."""
import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path

P = Path(__file__).resolve().parent
B = P.parent / 'prepare'
ROOT = P.parents[1]
J = lambda path: json.loads(Path(path).read_text())
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(name, value):
    (P / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text)).lower().replace('œ','oe').replace('æ','ae') if c.isalnum())

input_hashes = {
    'reviewed.json': '96011ffc9d44898ada0ad9c759e075525a945c528cdf0b01664e0976fa529d69',
    'crops.json': '1996925b232a018193748ebc0aa2b48ea44da10a31fe7505c80895be2c4b12d9',
}
for name, digest in input_hashes.items():
    assert sha(B/name) == digest, ('Input changed during independent verification', name)
original = J(B/'reviewed.json')
approved = copy.deepcopy(original)
banks = approved['banks']
baseline = J(ROOT/'baseline_exams.json')
qmap = {(b,q['id']):q for b,bank in banks.items() for q in bank['questions']}
audit = {(x['bank'],x['id']):x for x in J(B/'audit.json')}
copies = {(x['bank'],x['id']):x for x in J(P/'copies_verification.json')}
editions = {(x['bank'],x['id']):x for x in J(P/'edition_verification.json') if x.get('selected')}
fresh = {(x['bank'],x['id']):x for x in J(P/'fresh_evidence.json')}
inventory = J(B/'source_inventory.json')
issues = []

# Notes shown to the pupil must describe the integration actually chosen by root.
old_sentence = 'Les réponses enregistrées à cette ancienne version doivent être effacées pour ce seul QCM dans les deux profils.'
new_sentence = 'Les choix déjà enregistrés sont conservés et remappés vers les nouvelles lettres dans les deux profils ; ce QCM est remis en attente de validation.'
for n in (1,5,6,7):
    q = qmap['histo.ann.tech',n]
    matches = [note for note in q.get('reviewNotes',[]) if old_sentence in note['text']]
    assert len(matches) == 1
    matches[0]['text'] = matches[0]['text'].replace(old_sentence,new_sentence)
    issues.append({'id':f'histo-verify-migration-{n}','bank':'histo.ann.tech','questionId':n,'kind':'presentation','status':'repaired','finding':'Le texte annonçait à tort un effacement des réponses.','resolution':'Choix conservés et remappés ; validation retirée seulement pour le QCM concerné dans les deux profils, selon la décision de l’intégrateur.'})

for n, wording in {
    1:'Ancienne clé thématique ABD, lettres de l’édition à quatre propositions ; QCM complet hors note.',
    5:'Clé complète retenue : BCD. Ancienne clé thématique : BC, édition à quatre propositions.',
}.items():
    note = next(x for x in qmap['histo.ann.tech',n]['reviewNotes'] if x['noteId']==f'histo-v6-histo.ann.tech-{n}-2')
    note['sourceVerdict'] = wording
    issues.append({'id':f'histo-verify-legacy-key-label-{n}','bank':'histo.ann.tech','questionId':n,'kind':'presentation','status':'repaired','finding':'Une seconde remarque présentait la clé de l’ancienne édition comme encore conservée.','resolution':wording})

new_notes = [
    {
        'bank':'histo.ann.tn','id':3,'items':['D'],'kind':'possible_error',
        'text':'Le détail du corrigé et la ronéo TN3 p. 3 reprennent un rapport de dix cellules gliales pour un neurone. Cette généralisation est scientifiquement à nuancer : une étude de comptage du cerveau humain adulte rapporte des nombres globaux voisins de neurones et de cellules non neuronales. Ces dernières ne sont pas toutes gliales, et le rapport dépend de la région étudiée. Cela ne permet pas de transformer automatiquement D en Vrai, mais le rapport global 10:1 mérite une clarification. La clé officielle C reste conservée ; vérifier l’attendu et le périmètre de cette comparaison dans la ronéo et avec l’enseignant.',
        'refs':[
            {'file':'annales TISSU NERVEUX 2018 2025 CORRECTION.pdf','page':2,'label':'Détail officiel, question 40, item D','href':'sources/revision_v4/annales_TISSU_NERVEUX_2018_2025_CORRECTION_25bc666fc1.pdf#page=2'},
            {'file':'TN3 Ronéo 2026.pdf','page':3,'label':'Rapport repris dans la ronéo TN3','href':'sources/revision_v4/TN3_Roneo_2026_252c9211d9.pdf#page=3'},
            {'label':'Azevedo et al., étude de comptage originale, 2009 (PMID 19226510)','href':'https://pubmed.ncbi.nlm.nih.gov/19226510/'},
        ],
        'sourceVerdict':'Clé officielle conservée : C ; item D Faux dans le corrigé.',
        'noteId':'histo-v6-verify-tn3d',
    },
    {
        'bank':'histo.ann.tn','id':7,'items':['C'],'kind':'possible_error',
        'text':'Le corrigé imprime VRAI pour C, mais toute cette proposition, marqueur compris, est barrée sans légende : on ne peut pas en déduire un nouvel erratum. Le vocabulaire mérite aussi vérification : l’épaississement décrit correspond à la densité postsynaptique (ronéo TN2 p. 14), tandis que l’appareil épineux est une structure distincte, en continuité avec le réticulum endoplasmique lisse dans les reconstructions ultrastructurales. La clé CE de l’import et les marques originales sont conservées, sans inventer une clé E. Consulter la copie et demander la ronéo ou un erratum de mai 2019 pour clarifier C et la portée de la rature.',
        'refs':[
            {'file':'annales TISSU NERVEUX 2018 2025 CORRECTION.pdf','page':4,'label':'Question 35, item C barré, VRAI imprimé','href':'sources/revision_v4/annales_TISSU_NERVEUX_2018_2025_CORRECTION_25bc666fc1.pdf#page=4'},
            {'file':'TN2 Ronéo 2026 Actualisée.pdf','page':14,'label':'Densité postsynaptique','href':'sources/revision_v4/TN2_Roneo_2026_Actualisee_660afa6a3c.pdf#page=14'},
            {'label':'Spacek, reconstructions ultrastructurales originales, 1985 (PMID 3985372)','href':'https://pubmed.ncbi.nlm.nih.gov/3985372/'},
        ],
        'sourceVerdict':'Clé conservée CE, d’après les verdicts littéraux imprimés ; portée de la rature de C non explicitée.',
        'noteId':'histo-v6-verify-tn7c',
    },
    {
        'bank':'histo.ann.tc','id':42,'items':['D'],'kind':'possible_error',
        'text':'La clé ABE et le verdict Faux de D concordent. En revanche, le détail de D dans la compilation p. 1078 affirme trop largement que le cartilage hyalin n’a pas de périchondre. La ronéo TC2 p. 13 distingue les exceptions : cartilage articulaire et fibrocartilage. L’exception ne doit pas être étendue à tout cartilage hyalin. Cette réserve concerne le détail de la copie complémentaire ; la clé officielle reste inchangée. Vérifier cette distinction dans la ronéo.',
        'refs':[
            {'file':'Annales_compilation.pdf','page':1078,'label':'Question 25, détail D','href':'sources/Annales_compilation.pdf#page=1078'},
            {'file':'TC2 2026 Partie 1 Actualisé.pdf','page':13,'label':'Périchondre : exceptions, page imprimée 26','href':'sources/revision_v4/TC2_2026_Partie_1_ACTUALISE_884b289825.pdf#page=13'},
        ],
        'sourceVerdict':'Clé officielle ABE conservée ; D Faux.',
        'noteId':'histo-v6-verify-tc42d',
    },
]
for note in new_notes:
    qmap[note['bank'],note['id']].setdefault('reviewNotes',[]).append(note)
    issues.append({'id':note['noteId'],'bank':note['bank'],'questionId':note['id'],'items':note['items'],'kind':'scientific_or_documentary_reservation','status':'flagged_in_correction','finding':note['text'],'refs':note['refs'],'resolution':'Remarque sourcée ajoutée après correction. Aucune clé réécrite.'})

# File names, rather than generic role descriptions, are displayed by the menus.
approved_crops = copy.deepcopy(J(B/'crops.json'))
names = {x['usedPDF']:Path(x.get('identicalOldOriginal') or x['original']).name for x in inventory['firstUploadComparisons']}
names[str((P.parents[3]/'output/site/sources/Annales_compilation.pdf').resolve())] = 'Annales_compilation.pdf'
label_changes = []
order_changes = []
for row in approved_crops:
    if row.get('reuseExisting'):
        continue
    context_panels = [p for p in row['correction'] if p.get('fileLabel','').startswith(('Contexte','Consigne générale'))]
    main_panels = [p for p in row['correction'] if p not in context_panels]
    if context_panels and main_panels and row['correction'][0] in context_panels:
        order_changes.append({'bank':row['bank'],'id':row['id'],'primaryCorrectionFile':main_panels[0]['file'],'primaryCorrectionPage':main_panels[0]['page'],'contextFiles':[{'file':p['file'],'page':p['page']} for p in context_panels]})
        row['correction'] = main_panels + context_panels
        row['correctionNote'] = ' '.join(filter(None,[row.get('correctionNote'),'Le corrigé apparaît en premier. Les contextes communs reproduits depuis le sujet suivent, avec leur fichier et leur page.']))
    for role in ('subject','correction'):
        for panel in row[role]:
            label = names.get(panel['file'],Path(panel['file']).name)
            if panel.get('fileLabel') != label:
                label_changes.append({'bank':row['bank'],'id':row['id'],'role':role,'file':panel['file'],'page':panel['page'],'before':panel.get('fileLabel'),'after':label})
                panel['fileLabel'] = label
issues.append({'id':'histo-verify-file-labels','kind':'presentation','status':'repaired','finding':'Les libellés génériques « Sujet thématique » et « Corrigé thématique » remplaçaient les vrais noms de fichiers.','resolution':'Chaque panneau d’annale porte le nom du document réel. La page et le numéro original restent inchangés.','panels':len(label_changes),'questionCount':len({(x['bank'],x['id']) for x in label_changes})})
save('file_label_changes.json',label_changes)
save('copy_order_changes.json',order_changes)
issues.append({'id':'histo-verify-correction-primary-source','kind':'presentation','status':'repaired','finding':'Le premier panneau de correction était parfois un contexte venant du sujet, ce qui aurait donné un mauvais lien principal au menu du corrigé.','resolution':'Corrigé en premier, puis contextes du sujet, avec note explicite et vrais noms de fichiers.','affectedQuestions':order_changes})

# The independent textual evidence is reopened from the source PDFs by
# check_sources.py. Parent audit positions serve only as locators.
normalized_exceptions = {
    ('histo.ann.tc',31,'D'):'Coquille OCR « g0 o/o » normalisée en 90 %, confirmée par le corrigé et l’autre édition.',
    ('histo.ann.tc',33,'A'):'Coquilles « L, composante » / « collagène L » normalisées en La / collagène I par concordance documentaire.',
    ('histo.ann.tn',45,'C'):'Sujet propre de la compilation ; différence de casse Il/ll sans modification sémantique, annotation du thématique déplacée après correction.',
    ('histo.ann.tech',8,'B'):'Signe degré de 56 °C normalisé, sans changement de valeur.',
    ('histo.te2',9,'B'):'Le sujet omet « ouverte » ; complément documenté depuis la même proposition du corrigé, déjà signalé dans la V5.',
    ('histo.tc1',11,'A'):'Glyphe privé du Word normalisé en α.',
    ('histo.tc1',11,'B'):'Glyphe privé du Word normalisé en α.',
}
critical = {('histo.ann.tech',n) for n in (1,5,6,7)} | {('histo.ann.tc',n) for n in (5,10,42)} | {('histo.ann.tn',n) for n in (22,30,45,63)} | {('histo.te2',17),('histo.tn2',7),('histo.autotech',12)}
fig_sources = {(x['source'],x['page']) for x in inventory['primaryFigurePagesViewed']}
coverage = []
crop_geometry_flags = []
for key,q in qmap.items():
    a = audit[key]; f = fresh[key]; c = copies[key]
    graded = bool(q['answer']) or q.get('answerIsEmpty') is True
    noted = bool(q.get('reviewNotes'))
    row = {
        'bank':key[0], 'id':key[1], 'status':'verified_with_documented_limit' if not graded else ('verified_with_notes' if noted else 'verified'),
        'questionTextCompared':True, 'sharedContextsCompared':True, 'questionBoundariesCompared':True,
        'subjectSource':a['subject']['file'], 'correctionSource':a['correction']['file'],
        'answer':q['answer'], 'graded':graded, 'allFalseExplicit':q.get('answerIsEmpty') is True,
        'answerPolarity':q.get('answerPolarity','true'),
        'keyDecision':copy.deepcopy(a['key']),
        'items':[],
        'copies':{
            'subjectClean':True,'subjectAvailable':True,'correctionAvailable':True,
            'sourcePDFsReopened':True, 'sourceTextAndGeometryChecked':True,
            'pairVisuallyChecked':key in critical,
            'extraCorrectionVisuallyChecked':key==('histo.ann.tn',7),
            'reusedV5':c['reuseExisting'],
            'panelsWithinPage':all(panel['rectInPage'] for role in c['roles'].values() for panel in role['panels']),
            'subjectStemLiteralIncluded':c['subjectStemLiteralIncluded'],
            'panels':{role:[{k:panel[k] for k in ('file','page','rect','rectInPage')} for panel in c['roles'][role]['panels']] for role in ('subject','correction')},
            'methodLimit':'Les autres paires ont été contrôlées textuellement et géométriquement ; elles ne sont pas toutes annoncées comme vues une à une.',
            'correctionPanelsReorderedForPrimaryLink':any(x['bank']==key[0] and x['id']==key[1] for x in order_changes),
        },
        'figures':{
            'interactiveAssetsChecked':True,
            'interactiveAssetSources':[{'src':x['src'],'source':x['source'],'page':x['page'],'rect':x['rect'],'sha256':sha(x['file']),'visuallyComparedWithOriginal':True} for x in a['figures']['interactiveAssets']],
            'sourceFigurePagesViewed':[{'file':x['file'],'page':x['page']} for x in a['figures']['sourceImages'] if (x['file'],x['page']) in fig_sources],
        },
        'reviewNoteIds':[note['noteId'] for note in q.get('reviewNotes',[])],
        'scientificReviewScope':'Lecture critique de chaque énoncé et détail ; réserves sourcées affichées après correction. L’absence de remarque ne constitue pas une certification scientifique universelle.',
    }
    if key==('histo.ann.tn',30):
        row['copies']['stemDifference']='La mention (1 point) du thématique n’est pas dans le sujet propre de la compilation ; la consigne complète est conservée.'
    if key in editions:
        ed=editions[key]
        row['editionComparison']={'status':'all_available_items_and_session_independently_compared','session':ed['session'],'itemsCompared':len(ed['items']),'keyLineConfirmed':ed['keyConfirmed'],'sessionHeadingConfirmed':ed['headerConfirmed'],'compilationPage':ed['selected']['page'],'compilationKey':ed['selected']['key'],'trace':'edition_verification.json'}
    elif key[0].startswith('histo.ann.'):
        row['editionComparison']={'status':'no_confirmed_same_session_counterpart','decision':'Aucun transfert de clé depuis une simple ressemblance de phrase ; source thématique conservée.'}
    for item in f['items']:
        item_key = (*key,item['id'])
        ai = next(x for x in a['items'] if x['id']==item['id'])
        positions_ok = True
        for role,field in (('subject','source'),('correction','correction')):
            actual = c['roles'][role]['panels']
            # Superseded/annotated thematic subjects are deliberately available
            # only in the correction menu when a clean full edition replaces them.
            if role=='subject': actual = actual + c['roles']['correction']['panels']
            for ev in item[field]:
                for line in ev['lines']:
                    x0,y0,x1,y1=line['rect']
                    included=any(panel['file']==ev['file'] and panel['page']==line['page'] and panel['rect'][0]<=x0+.75 and panel['rect'][1]<=y0+.75 and panel['rect'][2]>=x1-.75 and panel['rect'][3]>=y1-.75 for panel in actual)
                    if not included:
                        positions_ok=False
                        crop_geometry_flags.append({'bank':key[0],'id':key[1],'item':item['id'],'role':role,'source':ev['file'],'line':line})
        declaration = {
            'id':item['id'], 'status':'verified_with_reservation' if any(item['id'] in n.get('items',[]) for n in q.get('reviewNotes',[])) else 'verified',
            'siteText':item['siteText'], 'siteExplanation':item['siteExplanation'],
            'sourceTextCompared':True, 'correctionTextCompared':True, 'correctionDetailCompared':True,
            'originalSubjectEvidence':item['source'], 'originalCorrectionEvidence':item['correction'],
            'literalVerdict':ai['literalVerdict'], 'literalTruthValue':ai['literalTruthValue'],
            'verdictMeaning':ai['verdictMeaning'],
            'selectedByRetainedKey':item['id'] in q['answer'] if graded else None,
            'markingDecision':ai['status'],
            'subjectExactAfterNormalization':item['subjectExactNormalized'],
            'capturePositionsIncluded':positions_ok,
            'normalizationExplanation':normalized_exceptions.get(item_key),
        }
        if key==('histo.ann.tn',7) and item['id']=='C':
            declaration['documentaryReservation']='VRAI imprimé, mais proposition et marqueur barrés sans légende. Aucune clé nouvelle déduite de la rature ; remarque de clarification ajoutée.'
        if key==('histo.tn2',7):
            declaration['markingDecision']='Séquence unique : E porte Vrai, A–D sont les autres ordres proposés, sans marqueur V/F imprimé. Les cinq séquences ont été comparées dans le même contexte.'
        if key==('histo.te2',17):
            declaration['sourceLetterMapping']='A–E du sujet correspondent respectivement à F–J du corrigé ; le F initial est une lettre de proposition et ne signifie pas Faux.'
        if key==('histo.autotech',12):
            declaration['sourceLetterMapping']='Le sujet imprime deux fois A puis D ; les cinq énoncés correspondent dans l’ordre à A–E du corrigé, comparaison par texte intégral.'
        row['items'].append(declaration)
    coverage.append(row)

missing = copy.deepcopy(J(B/'missing.json'))
missing.append({
    'kind':'unexplained_strikethrough','priority':'clarification','bank':'histo.ann.tn','ids':[7],'items':['C'],
    'needed':'Erratum ou consigne de la session de mai 2019 expliquant la rature de la proposition C et du marqueur VRAI dans la question 35.',
    'reason':'La rature n’a pas de légende. La ronéo 2026 distingue la densité postsynaptique et les sources ultrastructurales distinguent l’appareil épineux. Aucune clé E personnelle n’est substituée à la clé CE importée.',
    'searchesPerformed':'Sujet et corrigé thématiques originaux, identité du premier envoi, recherche de correspondance intégrale de même session dans la compilation, ronéo TN2 p. 14 et publication primaire PMID 3985372.',
    'resolution':'Clé CE conservée conformément aux marqueurs littéraux ; réserve précise dans la correction et copie authentique montrant la rature.',
})
for m in missing:
    if m.get('kind')=='official_arbitration_required':
        issues.append({'id':'histo-verify-limitation-'+m['bank']+'-'+str(m['ids'][0]),'bank':m['bank'],'questionId':m['ids'][0],'kind':m['kind'],'status':'unresolved_source_limit_withheld_from_score','finding':m['reason'],'resolution':m['resolution']})

# Invariants checked against the actual immutable baseline, not report counts.
old_notes=0
for b,bank in banks.items():
    assert [q['id'] for q in bank['questions']]==[q['id'] for q in baseline[b]['questions']]
    base={q['id']:q for q in baseline[b]['questions']}
    prepared={q['id']:q for q in original['banks'][b]['questions']}
    for q in bank['questions']:
        for note in base[q['id']].get('reviewNotes',[]):
            assert note in q.get('reviewNotes',[]), ('Prior scientific note changed',b,q['id'],note.get('noteId'))
            old_notes+=1
        for field in ('id','question','options','answer','explanations','answerIsEmpty','allowNoAnswer','answerPolarity','weight'):
            assert q.get(field)==prepared[q['id']].get(field),(b,q['id'],field)
assert len(qmap)==321
assert sum(len(q['options']) for q in qmap.values())==1614
assert old_notes==59
assert sum(x['graded'] for x in coverage)==316
assert not crop_geometry_flags,crop_geometry_flags[:5]
assert all(x['copies']['panelsWithinPage'] for x in coverage)
assert len(critical)==14
assert len(fig_sources)==39

save('approved_reviewed.json',approved)
save('approved_crops.json',approved_crops)
save('coverage.json',coverage)
save('issues.json',issues)
save('missing.json',missing)
save('geometry_verification.json',{'questions':321,'items':1614,'allItemSourcePositionsIncluded':True,'flags':crop_geometry_flags})
summary = {
    'approved':True, 'verifier':'/root/histologie_verifie',
    'inputSHA256':input_hashes,
    'approvedSHA256':{name:sha(P/name) for name in ('approved_reviewed.json','approved_crops.json')},
    'banks':13,'questions':321,'items':1614,'gradable':316,'ungraded':5,
    'sourceCleanCopies':321,'correctionCopies':321,'reusedV5Pairs':128,'newAnnalesPairs':193,
    'sameSessionWholeQuestionComparisons':len(editions),'sameSessionItemComparisons':sum(len(x['items']) for x in editions.values()),
    'individuallyViewedCriticalPairs':14,'additionalIndividuallyViewedCorrectionQuestions':1,
    'sourceFigurePagesVisuallyViewed':39,'interactiveFigureAssetsVisuallyCompared':21,
    'baselineNotesPreserved':old_notes,'preparerNotesPreservedOrClarified':53,'newVerifierNotes':3,
    'notesTotal':sum(len(q.get('reviewNotes',[])) for q in qmap.values()),
    'correctedSourceFileLabels':len(label_changes),'correctionMenusReordered':len(order_changes),
    'newVerifierNotesIds':[n['noteId'] for n in new_notes],
    'bankCounts':[{'bank':b,'questions':len(bank['questions']),'items':sum(len(q['options']) for q in bank['questions'])} for b,bank in banks.items()],
    'scopeLimit':'Les textes, clés et détails ont été relus pour tous les QCM. Toutes les paires de captures ont un contrôle documentaire et géométrique. Seules les paires et pages indiquées ont été inspectées visuellement une à une. Les réserves des documents ne sont pas assimilées à une clé scientifique personnelle.',
}
save('approval.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
