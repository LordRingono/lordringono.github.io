from pathlib import Path
from collections import Counter
import copy
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
PREP = HERE.parent / 'prepare'

def read(path):
    return json.loads(Path(path).read_text())

def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

expected = {
    'reviewed.json': 'f2027d139a34660c33b47600660ab9169d2c6efeaa4d75905fa3b0c60dc60a78',
    'crops.json': '57624752bf5c6e07a00777b30baa779ef7101944d9abe818aed947f6962e626d',
}
for name, digest in expected.items():
    assert sha(PREP / name) == digest, (name, sha(PREP / name))

before = read(PREP / 'reviewed.json')
approved = copy.deepcopy(before)
crops = read(PREP / 'crops.json')
source = read(HERE / 'independent_source.json')
grids = read(HERE / 'grids_verified.json')
assets = read(HERE / 'assets_verified.json')
audit = read(PREP / 'audit.json')
prepared_changes = read(PREP / 'changes.json')
changes = []

def getq(bank, ident):
    return next(q for q in approved['banks'][bank]['questions'] if q['id'] == ident)

def ref_original(page, label):
    return {'file': 'Sujets + corrections compilés.pdf', 'page': page, 'label': label,
            'href': f'sources/Annales_compilation.pdf#page={page}'}

COURSE = 'Chap_1_et_2_chimie_phy_260918_170147_9d9e60bef2.pdf'

def ref_course(page, label):
    return {'file': COURSE, 'page': page, 'label': label,
            'href': f'sources/revision_v4/{COURSE}#page={page}'}

def ref_web(label, href):
    return {'file': label, 'label': label, 'href': href}

ENDING = ' La clé officielle est conservée ; vérifier ce point dans la ronéo et, si nécessaire, le faire préciser par l’enseignant.'

def add_note(bank, ident, items, text, refs, kind='possible_error'):
    q = getq(bank, ident)
    note = {
        'bank': bank, 'id': ident, 'sourceId': str(q['sourceNumber']),
        'items': items, 'kind': kind, 'text': text + ENDING, 'refs': refs,
        'sourceVerdict': q['answer'], 'courseVerdict': None,
        'noteId': f"review-v6-chimie-verification-{q['sourceSet']}-{q['sourceNumber']}-{''.join(items)}",
    }
    assert all(n.get('noteId') != note['noteId'] for n in q.get('reviewNotes', []))
    q.setdefault('reviewNotes', []).append(note)
    changes.append({'bank': bank, 'id': ident, 'sourceNumber': q['sourceNumber'],
                    'items': items, 'type': 'scientific_note', 'note': note,
                    'status': 'signalement_source_apres_correction_cle_conservee'})

# Deux erreurs d'import certaines : le numérateur Z² appartient à B, non à A.
b = 'annales.ue2c.atomistique.2020s1'
q = getq(b, 1)
for letter, text in {
    'A': 'VRAI : (cf schéma p8).',
    'B': 'FAUX : La bonne formule est Eₙ = −h × c × R_H × (Z²/n²).',
}.items():
    old = q['explanations'][letter]
    q['explanations'][letter] = text
    changes.append({'bank': b, 'id': 1, 'sourceNumber': 43, 'item': letter,
                    'type': 'import_repair', 'field': 'explanations', 'before': old,
                    'after': text, 'sourcePage': 328,
                    'reason': 'La fraction Z²/n² est celle du détail B dans le rendu original. Le numérateur avait été rattaché au détail A.',
                    'status': 'corrige_et_relu_dans_original'})

add_note(b, 1, ['D'],
    'La configuration imprimée pour P, 1s² 2p⁶ 3s¹ 3p³ 4s¹, ne contient que 13 électrons, alors que l’atome neutre de phosphore (Z=15) en possède 15. Le détail « état excité » ne résout pas cette différence : une excitation conserve le nombre d’électrons. Une omission de 2s² est plausible, mais cette sous-couche ne figure pas dans l’item original et ne doit pas être ajoutée silencieusement.',
    [ref_original(308, 'Sujet original, Q43 D'), ref_original(328, 'Corrigé original, Q43 D'),
     ref_course(13, 'Ronéo — configurations électroniques et nombre d’électrons'),
     ref_course(15, 'Ronéo — configurations des atomes neutres')])

add_note('annales.ue2c.atomistique.2023s2', 1, ['D'],
    'L’item porte sur F⁸⁺ au niveau n=9. Son seuil d’ionisation est bien 13,6 × 9²/9² = 13,6 eV. En revanche, le détail propose de partir de l’énergie fondamentale : pour n=1, ce même ion aurait un seuil de 1 101,6 eV. Il faut donc utiliser E₉ dans Eᵢ = 0 − E₉ ; le mot « fondamental » du corrigé est incorrect ici.',
    [ref_original(158, 'Sujet original, Q29 D'), ref_original(173, 'Corrigé original, Q29 D'),
     ref_course(8, 'Ronéo — énergie des hydrogénoïdes'), ref_course(9, 'Ronéo — transitions et ionisation')])

add_note('annales.ue2c.chimie_org.2024s1', 4, ['B'],
    'Le détail B appelle la structure 1 une « cétone énolisable », alors que le dessin et le détail A identifient un aldéhyde. La formation d’un aldol à partir de cet aldéhyde énolisable reste cohérente avec le verdict vrai ; c’est le nom de la fonction de départ dans la justification B qui est à rectifier.',
    [ref_original(58, 'Sujet original, structure 1 et Q47'), ref_original(81, 'Corrigé original, Q47 A et B'),
     ref_web('OpenStax — réaction aldolique', 'https://openstax.org/books/organic-chemistry/pages/23-1-carbonyl-condensations-the-aldol-reaction')])

add_note('annales.ue2c.chimie_org.2024s2', 1, ['C'],
    'Sur la structure 1, le carbone de droite porte deux groupes éthyle identiques : celui noté C₂H₅ et celui dessiné à gauche (CH₂–CH₃). Il ne possède donc pas quatre substituants différents et n’est pas asymétrique. La structure 1 n’a aucun C*, tandis que la structure 2 en a un. L’item « deux carbones asymétriques » reste faux, mais le comptage « un dans chaque structure » du détail est erroné.',
    [ref_original(90, 'Sujet original, structures 1 et 2'), ref_original(108, 'Corrigé original, Q27 C'),
     ref_web('OpenStax — carbone asymétrique et groupes différents', 'https://openstax.org/books/organic-chemistry/pages/5-2-the-reason-for-handedness-in-molecules-chirality')])

add_note('annales.ue2c.atomistique.2021s1', 2, ['D'],
    'Pour le chrome fondamental [Ar] 4s¹ 3d⁵, la règle de Hund place un électron dans chacune des cinq orbitales d. Dans ce modèle, m = −1 compte donc 2 électrons en 2p, 2 en 3p et 1 en 3d, soit 5. L’item « 6 électrons » est bien faux ; l’argument du détail selon lequel on ne pourrait pas déterminer ce nombre parce que 3d est incomplète ne convient pas à cette sous-couche demi-pleine.',
    [ref_original(247, 'Sujet original, Q44 D'), ref_original(274, 'Corrigé original, Q44 D'),
     ref_course(13, 'Ronéo — Hund et remplissage à l’état fondamental'),
     ref_course(16, 'Ronéo — configuration d’exception du chrome')])

add_note('annales.ue2c.atomistique.2022s2', 1, ['D'],
    'La tendance périodique invoquée dans le corrigé ne suffit pas à conclure que Cu est plus électronégatif que Ni. Dans l’échelle de Pauling publiée par la Royal Society of Chemistry, Cu vaut 1,90 et Ni 1,91, soit l’ordre inverse. L’échelle ou l’approximation attendue dans le cours doit être précisée avant d’interpréter le verdict vrai.',
    [ref_original(219, 'Sujet original, Q27 D'), ref_original(233, 'Corrigé original, Q27 D'),
     ref_web('Royal Society of Chemistry — cuivre, Pauling 1,90', 'https://periodic-table.rsc.org/element/29/copper'),
     ref_web('Royal Society of Chemistry — nickel, Pauling 1,91', 'https://periodic-table.rsc.org/element/28/nickel')])

add_note('annales.ue2c.atomistique.2018', 1, ['D'],
    'L’argument « cela pourrait très bien être une 2pz » est problématique : dans la convention usuelle où l’axe de quantification est z, l’orbitale pz correspond à m = 0. Les orbitales réelles px et py et les états de m = ±1 nécessitent de préciser la base utilisée ; cette nuance ne justifie pas d’attribuer pz à m = −1. Faire clarifier la convention du cours et la justification du verdict faux.',
    [ref_original(458, 'Sujet original, Q47 imprimé / Q46 corrigé'), ref_original(483, 'Corrigé original, Q46 D'),
     ref_web('MIT OpenCourseWare — orbitales p et nombres quantiques, p. 1', 'https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/5c828fce769b146e5820a7d6ed0abfc2_MIT5_111F14_Lec6.pdf#page=1')])

add_note('annales.ue2c.chimie_org.2018', 5, ['A', 'B'],
    'Le caractère tertiaire du dérivé halogéné ne suffit pas, à lui seul, à imposer SN1. Les alcoolates cités sont aussi des bases et une élimination E2 peut concurrencer la substitution ; le solvant et la température influencent le résultat. La stabilisation du carbocation par les noyaux aromatiques doit également être prise en compte. Les conditions données et l’argument « tertiaire donc SN1 » sont trop sommaires pour exclure cette concurrence : faire confirmer l’hypothèse retenue pour A et B.',
    [ref_original(457, 'Sujet original, Q46 imprimé / Q45 corrigé'), ref_original(482, 'Corrigé original, Q45 A et B'),
     ref_web('OpenStax — concurrence SN1, SN2, E1 et E2', 'https://openstax.org/books/organic-chemistry/pages/11-12-a-summary-of-reactivity-sn1-sn2-e1-e1cb-and-e2')])

add_note('annales.ue2c.atomistique.2019', 2, ['C'],
    'Le mot « hyperconjugué » appliqué aux cycles B, A et C appelle la même réserve de vocabulaire que dans D. Le schéma montre un réseau de liaisons π conjuguées ; l’hyperconjugaison au sens IUPAC désigne l’interaction de liaisons σ avec un réseau π ou une orbitale p. Le corrigé donne seulement « VRAI » pour C et n’explicite pas l’interaction σ visée. Vérifier si le cours emploie ici ce terme pour la conjugaison étendue.',
    [ref_original(413, 'Sujet original, Q47 C'), ref_original(443, 'Corrigé original, Q47 C'),
     ref_web('IUPAC Gold Book — hyperconjugation', 'https://goldbook.iupac.org/terms/view/H02924')])

add_note('annales.ue2c.atomistique.2019', 2, ['E'],
    'Le détail E affirme que tous les carbones hors carboxylate sont sp². Or le carbone du cycle A portant le carboxylate a quatre liaisons simples et est sp³ ; le détail B le reconnaît lui-même. La justification de la planéité par « tous les carbones sont sp² » est donc incorrecte. Il faut faire préciser si l’énoncé parle du squelette des cycles ou de tous les atomes de la molécule, sans déduire la géométrie complète de cette seule phrase.',
    [ref_original(413, 'Sujet original, Q47 E'), ref_original(443, 'Corrigé original, Q47 B et E'),
     ref_web('OpenStax — hybridation sp³ et géométrie tétraédrique', 'https://openstax.org/books/organic-chemistry/pages/1-6-sp3-hybrid-orbitals-and-the-structure-of-methane')])

# Les champs structurels et les notes existantes sont préservés à l'identique.
allowed = {'explanations', 'reviewNotes'}
for bank, old_b in before['banks'].items():
    new_b = approved['banks'][bank]
    assert {k:v for k,v in old_b.items() if k!='questions'} == {k:v for k,v in new_b.items() if k!='questions'}
    assert len(old_b['questions']) == len(new_b['questions'])
    for old_q, new_q in zip(old_b['questions'], new_b['questions']):
        assert {k:v for k,v in old_q.items() if k not in allowed} == {k:v for k,v in new_q.items() if k not in allowed}
        for old_note in old_q.get('reviewNotes', []):
            assert old_note in new_q.get('reviewNotes', [])

dump('approved_reviewed.json', approved)
shutil.copyfile(PREP / 'crops.json', HERE / 'approved_crops.json')
dump('verifier_changes.json', changes)

subject_visual = [16,17,18,57,58,90,91,112,113,157,158,186,187,219,246,247,283,307,308,337,338,368,369,370,411,412,413,414,456,457,458]
correction_visual = sorted([80,81,108,127,130,172,173,211,233,272,274,298,328,355,395,396,439,441,443,480,483,482,484,460])
individual_asset_views = [
    'static/annales_ue2_219_2559293f21.webp',
    'static/annales_ue2_219_d7c1228b3d.webp',
    'static/annales_ue2_187_502fe90567.webp',
    'static/annales_ue2_413_45ec57a90b.webp',
    'static/annales_ue2_v2_368_ea3504521234.webp',
]

indexed_source = {(r['bank'],r['id']): r for r in source}
indexed_audit = {(r['bank'],r['id']): r for r in audit}
indexed_crops = {(r['bank'],r['id']): r for r in crops}
indexed_grids = {(r['bank'],r['id']): r for r in grids}
repaired = {(r['bank'],r['id'],r['item']) for r in changes if r['type']=='import_repair'}
prep_repaired = {(r['bank'],r['id'],r.get('item')) for r in prepared_changes if r.get('field')=='explanations'}
coverage_rows=[]
for bank, b in approved['banks'].items():
    for q in b['questions']:
        key=(bank,q['id'])
        raw=indexed_source[key]
        pre=indexed_audit[key]
        crop=indexed_crops[key]
        grid=indexed_grids[key]
        item_rows=[]
        for o in q['options']:
            letter=o['id']
            pre_item=next(i for i in pre['items'] if i['id']==letter)
            detail=q.get('explanations',{}).get(letter,'')
            detail_kind=('detail_graphique_ou_general_dans_copie_originale' if not detail else
                         'verdict_sans_justification_textuelle' if re.fullmatch(r'(?:VRAI|FAUX|V|F)\s*[.!:]?',detail.strip(),re.I) else
                         'justification_textuelle_presente')
            notes=[n['noteId'] for n in q.get('reviewNotes',[]) if letter in n.get('items',[])]
            item_rows.append({
                'id':letter,
                'sourceSubjectText':pre_item.get('sourceText'),
                'sourceCorrectedSubjectText':pre_item.get('correctedSourceText'),
                'siteOption':o,
                'subjectOriginalRead':True,'correctedOriginalRead':True,
                'subjectComparison':'conforme_apres_comparaison_independante_texte_et_page_source',
                'shortKeyVerdict': letter in grid['independentReadKey'],
                'detailedKeyVerdict': letter in q['detailedKey'] if q.get('detailedKey') else None,
                'gradedVerdict': letter in q['answer'] if q['answer'] else None,
                'detail':detail,'detailKind':detail_kind,
                'detailComparedIndependently':True,
                'detailImportStatus': 'repare_par_verificateur' if (bank,q['id'],letter) in repaired else
                    'reparation_preparateur_validee' if (bank,q['id'],letter) in prep_repaired else 'conforme_a_original',
                'scientificReview':'reserve_documentee' if notes else 'aucune_anomalie_supplementaire_identifiee',
                'scientificNoteIds':notes,
                'sourceProof': {'file':'independent_source.json','bank':bank,'id':q['id'],
                    'subjectPages':[p['page'] for p in raw['source']['subject']],
                    'correctionPages':[p['page'] for p in raw['source']['correction']]},
            })
        coverage_rows.append({
            'bank':bank,'id':q['id'],'sourceSet':q['sourceSet'],'sourceNumber':q['sourceNumber'],
            'printedSubjectNumber':crop['subjectNumber'],
            'independentOriginalComparisonComplete':True,
            'shortKeyReadIndependently':grid['independentReadKey'],
            'detailedKey':q.get('detailedKey'), 'gradedKey':q['answer'],
            'keyStatus':'conflit_original_hors_note' if not q['answer'] else 'grille_et_detail_concordants',
            'subjectCopies':len(crop['subject']),'correctionCopies':len(crop['correction']),
            'subjectCopyStatus':'original_propre_sans_correction',
            'subjectPagesVisuallyRead':sorted({p['page'] for p in crop['subject']}),
            'correctionPagesVisuallyRead':sorted({p['page'] for p in crop['correction']} & set(correction_visual)),
            'allCorrectionTextRead':True,
            'questionAndFollowingQuestionBoundariesChecked':True,
            'sharedContextChecked':True,
            'assetSources': [a['src'] for a in assets if any(u['bank']==bank and u['id']==q['id'] for u in a['uses'])],
            'items':item_rows,
        })

detail_counts=Counter(i['detailKind'] for r in coverage_rows for i in r['items'])
all_notes=[n for b in approved['banks'].values() for q in b['questions'] for n in q.get('reviewNotes',[])]
summary={
    'banks':38,'series':14,'questionsCompared':86,'itemsCompared':430,
    'subjectCopiesClean':86,'subjectCopiesAnnotated':0,'subjectCopiesMissing':0,
    'correctionCopies':86,'correctionCopiesMissing':0,
    'subjectPanels':89,'correctionPanels':116,'panelsGeometryChecked':205,
    'gradedQuestions':85,'ungradedSourceKeyConflict':1,'keysModified':0,
    'itemsWithoutAnyUsableSourceCorrection':0,
    'itemsWithoutSeparateTextDetailButWithGlobalOrGraphicalCorrection':25,
    'textDetailKinds':dict(detail_counts),
    'preparerDetailRepairsValidated':20,'verifierDetailRepairs':2,
    'preexistingScientificNotesPreserved':30,'verifierScientificNotesAdded':10,
    'finalScientificNotes':len(all_notes),
    'subjectPagesVisuallyRead':subject_visual,'correctionPagesVisuallyRead':correction_visual,
    'allSubjectAndCorrectionTextRead':True,
    'shortGridsReadIndependently':sorted({g['page'] for g in grids}),
    'uniqueAssetsVerifiedAgainstFreshPDFRender':372,
    'assetsIndividuallyViewed':individual_asset_views,
    'assetsIndividualVisualReviewNotClaimedForAll':True,
    'newQuestions':0,'questionsRemoved':0,'questionIdsOrOrderModified':False,
}
assert len(coverage_rows)==86 and sum(len(r['items'])for r in coverage_rows)==430
assert len(all_notes)==40 and len(changes)==12
dump('coverage.json',{'verifier':'/root/chimie_verifie','summary':summary,'questions':coverage_rows})

panels=read(HERE/'crops_verified.json')
for panel in panels:
    assert panel['insidePage']
    if panel['unrelatedHeadingCandidates']:
        assert panel['bank']=='annales.ue2c.chimie_org.2021s1' and panel['id']==2 and panel['role']=='subject'
        panel['candidateResolution']='contexte_commun_explicitement_destine_aux_deux_questions_40_et_41_sans_items_du_Q40'
    panel['finalStatus']='valide'
dump('crops_verified.json',panels)

issues=[]
for n,change in enumerate(prepared_changes,1):
    issues.append({'issueId':f'prep-{n:03d}','origin':'preparateur','status':'valide_independamment','change':change})
for n,change in enumerate(changes,1):
    issues.append({'issueId':f'verifier-{n:03d}','origin':'verificateur','status':change['status'],'change':change})
issues.append({'issueId':'source-key-2018-49','origin':'source','bank':'annales.ue2c.atomistique.2018','id':4,
    'subjectPrintedNumber':50,'correctedNumber':49,'shortKey':'A','detailedKey':'C',
    'evidencePages':[458,460,484],'status':'hors_note_maintenu_attente_erratum'})
issues.append({'issueId':'rejected-alert-Mg','origin':'verificateur','bank':'annales.ue2c.atomistique.2022s2','id':2,'item':'A',
    'status':'fausse_alerte_rejetee_aucune_modification',
    'reason':'Mg : 1s² 2s² 2p⁶ 3s² donne bien 2+2+2=6 électrons s. La supposition provisoire de 8 était une erreur du vérificateur, rectifiée avant publication. A reste vrai et aucun commentaire erroné n’est ajouté.',
    'evidencePages':[219,233],'coursePage':15})
issues.append({'issueId':'rejected-alert-biochem-Q40C','origin':'verificateur','scope':'hors_matiere_biochimie','series':'2019','sourceNumber':40,'item':'C',
    'status':'fausse_alerte_rejetee_aucune_modification',
    'reason':'Le grossissement du corrigé p. 439 montre bien « complexe II » pour la succinate déshydrogénase. Lecture des deux I confirmée sur la capture produite par le préparateur biochimie ; le signalement provisoire de complexe I était incorrect.',
    'evidence':'work/site_v6/biochimie/prepare/visual/2019_q40_detail.png'})
dump('issues.json',issues)

missing=read(PREP/'missing.json')
missing.append({'type':'cours_pour_arbitrage_scientifique','request':'Ronéos de chimie organique (stéréochimie, réactivité des carbonyles, substitutions/éliminations) et éventuels errata officiels : les sujets et corrigés sont disponibles, mais ces chapitres de cours permettraient de préciser les conventions pédagogiques signalées. Les commentaires actuels citent les originaux et des références primaires.'})
dump('missing.json',missing)

dump('external_sources_consulted.json',[
 {'url':'https://periodic-table.rsc.org/element/29/copper','finding':'Électronégativité de Pauling du cuivre : 1,90.','sourceRef':'turn115970371view0'},
 {'url':'https://periodic-table.rsc.org/element/28/nickel','finding':'Électronégativité de Pauling du nickel : 1,91.','sourceRef':'turn809427019view0'},
 {'url':'https://openstax.org/books/organic-chemistry/pages/11-12-a-summary-of-reactivity-sn1-sn2-e1-e1cb-and-e2','finding':'La base et les conditions orientent la concurrence substitution/élimination des halogénures tertiaires.','sourceRef':'turn809427019view1'},
 {'url':'https://openstax.org/books/organic-chemistry/pages/5-2-the-reason-for-handedness-in-molecules-chirality','finding':'Le carbone asymétrique doit porter quatre groupes différents.','sourceRef':'turn421481226view0'},
 {'url':'https://openstax.org/books/organic-chemistry/pages/23-1-carbonyl-condensations-the-aldol-reaction','finding':'Les aldéhydes énolisables participent à la réaction aldolique.','sourceRef':'turn421481226view1'},
 {'url':'https://goldbook.iupac.org/terms/view/H02924','finding':'Distinction entre réseau π conjugué et hyperconjugaison impliquant des liaisons σ.','sourceRef':'turn635378809search0'},
 {'url':'https://openstax.org/books/organic-chemistry/pages/1-6-sp3-hybrid-orbitals-and-the-structure-of-methane','finding':'Hybridation sp³ et quatre liaisons tétraédriques.','sourceRef':'turn635378809search2'},
 {'url':'https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/5c828fce769b146e5820a7d6ed0abfc2_MIT5_111F14_Lec6.pdf','finding':'Convention z : pz correspond à m=0, page 1.','sourceRef':'turn996669001view0'},
])

assert all(a['verifierFileDecodes'] and a['verifierShaMatches'] for a in assets)
assert all(g['equalPreparedGrid'] for g in grids)
assert sum(bool(q['answer']) for b in approved['banks'].values()for q in b['questions'])==85
assert sha(HERE/'approved_crops.json')==expected['crops.json']
for name,digest in expected.items():
    assert sha(PREP/name)==digest

dump('approved.json',{
 'status':'APPROVED','verifier':'/root/chimie_verifie',
 'scope':'Chimie UE2c, 38 banques, 14 séries, 86 QCM, 430 propositions',
 'preparedHashes':expected,
 'approvedReviewed':{'file':str(HERE/'approved_reviewed.json'),'sha256':sha(HERE/'approved_reviewed.json')},
 'approvedCrops':{'file':str(HERE/'approved_crops.json'),'sha256':sha(HERE/'approved_crops.json')},
 'sourceCompilationSha256':'f4bd0582c8d110fe22561066a89ad5ecf458207cd212765ce007e6d41e9273ec',
 'keysAndIdsPreserved':True,'preexistingNotesPreserved':True,'missingSources':0,
 'sourceConflictRemainsUngraded':'2018, sujet Q50 / corrigé Q49, grille A contre détail C',
 'integrationRequired':'Intégrer ces deux fichiers complets ; conserver le rendu après correction des reviewNotes et la protection des corrections dans le builder. La vérification fonctionnelle du site assemblé reste au responsable d’intégration.',
})
print(json.dumps({'summary':summary,'approved':read(HERE/'approved.json')},ensure_ascii=False,indent=2))
