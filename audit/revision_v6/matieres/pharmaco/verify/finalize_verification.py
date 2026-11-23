from pathlib import Path
from collections import Counter
from copy import deepcopy
import json, hashlib, re, unicodedata, fitz
from PIL import Image

ROOT = Path('/workspace/scratch/f3cb3bb97377')
OUT = ROOT / 'work/site_v6/pharmaco/verify'
PREP = ROOT / 'work/site_v6/pharmaco/prepare'
SITE = ROOT / 'output/site'
PDF = SITE / 'sources/Annales_compilation.pdf'

def load(path):
    return json.loads(path.read_text())

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(text):
    text = unicodedata.normalize('NFKC', text or '').casefold()
    for a, b in [('’', "'"), ('`', "'"), ('–', '-'), ('—', '-'), ('‑', '-'), ('œ', 'oe')]:
        text = text.replace(a, b)
    return re.sub(r'\s+', '', text)

def loose(text):
    return re.sub(r'[^\w+%=<>/°µ²³-]', '', norm(text))

def keyset(key):
    return set() if key == 'AUCUNE' else set(key or '')

def part_pages(part):
    if not part:
        return []
    pages = set()
    for key in ['stemRefs', 'keyRef', 'generalRefs']:
        pages.update(x['page'] for x in part[key])
    for key in ['options', 'details']:
        for entry in part[key].values():
            pages.update(x['page'] for x in entry['refs'])
    return sorted(pages)

assert sha(PREP / 'reviewed.json') == 'b5b8b16db16e90a1ef6dbddcec67aeb991d03d93821213d50f3a21b502b4c6f3'
assert sha(PREP / 'crops.json') == 'af9448c6fbd4a2542d986fee59f66bf1964de84cb45749ca06504b1637c6d9b6'
reviewed = load(PREP / 'reviewed.json')
baseline = load(ROOT / 'work/site_v6/baseline_exams.json')
crops = load(PREP / 'crops.json')
comparison = load(OUT / 'independent_comparison.json')
source_by_id = {q['sourceId']: q for q in comparison}
geometry = {q['sourceId']: q for q in load(OUT / 'geometry_coverage.json')}
crop_by_id = {q['sourceId']: q for q in crops}
visual = load(OUT / 'visual_manifest.json')
inventory = load(OUT / 'independent_inventory.json')
raw_flags = load(OUT / 'comparison_flags.json')
assert load(OUT / 'geometry_flags.json') == []
assert len(comparison) == len(geometry) == len(crops) == 336

approved = deepcopy(reviewed)
questions = [(bank, q) for bank, b in approved['banks'].items() for q in b['questions']]
by_id = {q['sourceId']: q for _, q in questions}
changes = []

# Independent visual review of p967 and p979 establishes literal identity of D/E.
sid_duplicate = 'ue4:2018-2019:S1:q15'
q = by_id[sid_duplicate]
assert q['answer'] == q['rawAnswer'] == 'BCD'
assert q['options'][3]['text'] == q['options'][4]['text'] == 'Un extrait brut peut être actif'
q['answer'] = ''
q.pop('answerIsEmpty', None)
q['warning'] = 'Corrigé contradictoire : ce QCM est conservé hors note. Voir la réserve documentée après validation.'
changes.append({
    'sourceId': sid_duplicate, 'bank': 'ue4.annales.theme.sources-naturelles', 'id': q['id'],
    'status': 'fixed_in_approved_reviewed', 'fields': ['answer', 'warning'],
    'before': {'answer': 'BCD', 'warning': ''},
    'after': {'answer': '', 'warning': q['warning'], 'rawAnswer': 'BCD', 'answerIsEmpty': 'absent'},
    'evidence': {'subjectPage': 967, 'correctionPage': 979, 'gridPage': 972,
                 'D': 'Un extrait brut peut être actif', 'E': 'Un extrait brut peut être actif',
                 'detailD': 'VRAI', 'detailE': 'FAUX : B, C, et D sont vrais',
                 'existingNoteId': 'ue4-v4-022'},
    'reason': 'Deux propositions strictement identiques reçoivent des verdicts opposés. Les images originales excluent une différence de ponctuation ou de négation. Aucune nouvelle clé n’est inventée ; la clé imprimée BCD et les justifications restent documentées.'
})

sid_missing = 'ue4:2021-2022:S1:q13'
q = by_id[sid_missing]
note = next(n for n in q['reviewNotes'] if n['noteId'] == 'ue4-v4-045')
ref = note['refs'][0]
old_label = ref['label']
ref['label'] = 'Grille 2021–2022 S1 : absence de clé pour le Q13 du sujet (BPF/BPP)'
changes.append({
    'sourceId': sid_missing, 'bank': 'ue4.annales.theme.droit', 'id': q['id'],
    'status': 'fixed_in_approved_reviewed', 'field': 'reviewNotes[ue4-v4-045].refs[0].label',
    'before': old_label, 'after': ref['label'],
    'reason': 'La page 848 est une preuve de l’omission, pas la correction du sujet Q13. Son n°13 correspond au sujet Q14, repris p853–854. URL, texte de la note, absence de clé et pointeurs nuls conservés.'
})
assert q['correctionPage'] is None and q['shortCorrectionPage'] is None
assert not crop_by_id[sid_missing]['correction']

# Invariants against the actual immutable V5 objects, not merely the preparer's report.
baseline_differences = []
for bank, b in approved['banks'].items():
    old_questions = baseline[bank]['questions']
    assert len(b['questions']) == len(old_questions)
    for old, new in zip(old_questions, b['questions']):
        for field in ['id', 'sourceId', 'sourceNumber', 'year', 'session', 'category', 'course',
                      'question', 'context', 'options', 'legacyProgress', 'weight', 'rawAnswer']:
            assert old.get(field) == new.get(field), (new['sourceId'], field)
        assert [(n['noteId'], n['text']) for n in old.get('reviewNotes', [])] == [(n['noteId'], n['text']) for n in new.get('reviewNotes', [])]
        fields = [k for k in set(old) | set(new) if old.get(k) != new.get(k)]
        assert set(fields) <= {'reviewNotes', 'correctionPage', 'shortCorrectionPage', 'answer', 'warning'}, (new['sourceId'], fields)
        if fields:
            baseline_differences.append({'bank': bank, 'id': new['id'], 'sourceId': new['sourceId'], 'changedFields': sorted(fields)})
assert sum(len(q.get('reviewNotes', [])) for _, q in questions) == 179

# All references are read against independently segmented source pages and supplied course PDFs.
notes_check = []
docs = {}
removed_ref_checks = []
for change in load(PREP / 'changes.json'):
    if 'removedRefs' not in change:
        continue
    for removed in change['removedRefs']:
        match = re.match(r'(ue4:[\d-]+:(?:S1|S2|PACES):q)(\d+)', removed['label'])
        assert match and int(match[2]) in (1, 2)
        prefix = match[1] + str(int(match[2]))
        correct = [r for r in change['after'] if re.match(re.escape(prefix) + r'\d', r['label'])]
        assert correct, change
        removed_ref_checks.append({'sourceId': change['sourceId'], 'field': change['field'],
                                   'removed': removed, 'correctFullNumberReferences': correct,
                                   'verification': 'Le numéro complet et les cinq propositions des sources ont été rapprochés ; le préfixe Q1/Q2 désigne un autre QCM.'})
assert len(removed_ref_checks) == 20

for bank, q in questions:
    old_notes = {n['noteId']: n for n in baseline[bank]['questions'][next(i for i, x in enumerate(baseline[bank]['questions']) if x['id'] == q['id'])].get('reviewNotes', [])}
    for n in q.get('reviewNotes', []):
        rc = []
        for r in n['refs']:
            path = SITE / r['href'].split('#')[0]
            assert path.exists(), r
            doc = docs.setdefault(str(path), fitz.open(path))
            assert 1 <= r['page'] <= len(doc)
            assert int(re.search(r'#page=(\d+)', r['href'])[1]) == r['page']
            own = re.match(r'(ue4:[\d-]+:(?:S1|S2|PACES):q\d+)', r['label'])
            entry = {'reference': r, 'documentExists': True, 'pageExists': True}
            if own:
                sq = source_by_id[own[1]]
                role = 'subject' if 'sujet' in r['label'] else 'correction'
                assert r['page'] in part_pages(sq[role]), (n['noteId'], r)
                entry.update({'sourceId': own[1], 'role': role, 'pageAssociationVerified': True,
                              'literalKey': sq['correction']['key'] if sq['correction'] else None,
                              'proof': 'independent_comparison.json : consigne, items et détails de cette question'})
            elif n['noteId'] == 'ue4-v4-045':
                assert r['page'] == 848
                entry.update({'role': 'omission_evidence', 'pageAssociationVerified': True,
                              'proof': '25 sujets / 24 corrigés ; Q13 du sujet p843 absent ; case 13 p848 associée aux items du sujet Q14 p843 et du corrigé p853–854.'})
            else:
                entry.update({'role': 'supplied_course', 'pageAssociationVerified': True,
                              'pageText': doc[r['page']-1].get_text().strip(),
                              'visualReview': True,
                              'proof': 'independent_courses.json et planches course_* du manifeste visuel'})
            rc.append(entry)
        key_claim = re.search(r'Clé du document\s*:\s*([A-E]+|\([A-E]\)[A-E]+)', n.get('sourceVerdict', ''))
        if key_claim:
            assert keyset(key_claim[1]) == keyset(q['rawAnswer'])
        notes_check.append({'sourceId': q['sourceId'], 'noteId': n['noteId'], 'items': n['items'],
                            'kind': n['kind'], 'text': n['text'], 'textUnchangedFromV5': n['text'] == old_notes[n['noteId']]['text'],
                            'refs': rc, 'sourceVerdictConsistentWithLiteralKey': True,
                            'assessment': 'Réserve précise relue avec ses passages sources. La clé historique reste la référence ; aucun désaccord scientifique non tranché ne devient une clé inventée.'})
save('notes_verification.json', {'notes': notes_check, 'referenceCount': sum(len(x['refs']) for x in notes_check),
                                 'removedReferenceChecks': removed_ref_checks})

# Inventory all graphical fields as well as the 13 figures actually reviewed visually.
assets = []
for bank, q in questions:
    prefix = 'annales_ue4_' + q['year'] + '_' + q['session'].lower() + '_q' + q['sourceNumber'].zfill(2) + '_'
    for field in ['images', 'stemImages', 'originalImages', 'correctionImages', 'referenceImages']:
        for src in q.get(field, []):
            path = SITE / src
            assert path.exists(), src
            with Image.open(path) as image:
                dimensions = list(image.size)
            assert path.name.startswith(prefix), (q['sourceId'], src)
            assets.append({'sourceId': q['sourceId'], 'field': field, 'src': src,
                           'exists': True, 'dimensions': dimensions, 'identityPrefixVerified': True,
                           'sha256': sha(path), 'visualPixelReview': field == 'images',
                           'integration': 'La figure interactive est vérifiée.' if field == 'images' else 'Les copies originales V6 doivent utiliser les panneaux approuvés ; les anciens champs de copies ne constituent pas une seconde voie non protégée.'})
save('existing_graphics.json', assets)

visual_subject_ids = {x['sourceId'] for k in ['figures', 'special'] for x in visual[k]}
visual_correction_ids = visual_subject_ids - {sid_missing}
figure_ids = {x['sourceId'] for x in visual['figures']}
assert len(visual_subject_ids) == 30 and len(visual_correction_ids) == 29 and len(figure_ids) == 13
for category, entries in visual.items():
    for entry in entries:
        entry['visuallyReviewedByIndependentVerifier'] = True
save('visual_manifest.json', visual)

PLACEHOLDERS = {('ue4:2025-2026:S1:q13', 'C'), ('ue4:2025-2026:S1:q14', 'D'),
                ('ue4:2025-2026:S1:q14', 'E'), ('ue4:2018-2019:S1:q06', 'D'),
                ('ue4:2018-2019:S1:q15', 'E')}
IMAGE_ONLY = {'ue4:2024-2025:S1:q24', 'ue4:2021-2022:S1:q07', 'ue4:2018-2019:S1:q03'}
TEXT_ARTIFACTS = {('ue4:2022-2023:S2:q14', 'D'), ('ue4:2022-2023:S2:q14', 'E')}

def remove_context_suffix(raw):
    if not raw:
        return None
    result = deepcopy(raw)
    result['text'] = result['text'].split('Questions 13 à 14 :')[0].strip()
    result['refs'] = [r for r in result['refs'] if not r['text'].startswith('Questions 13 à 14 :')]
    return result

coverage = []
item_counts = Counter()
key_detail_conflicts = []
flags_adjudicated = []
for c in comparison:
    sid = c['sourceId']; q = by_id[sid]; cp = c['correction']; cr = crop_by_id[sid]; ge = geometry[sid]
    items = []
    for source_item in c['items']:
        i = deepcopy(source_item); letter = i['id']
        if sid == 'ue4:2020-2021:S1:q12' and letter == 'E':
            i['subject'] = remove_context_suffix(i['subject']); i['detail'] = remove_context_suffix(i['detail'])
        if sid == 'ue4:2020-2021:S1:q09' and letter == 'E':
            i['detail'] = deepcopy(i['detail']); i['detail']['text'] = 'FAUX'; i['detail']['refs'] = i['detail']['refs'][:1]
        so = i['subject']; detail = i['detail']; cs = i['correctionStatement']
        if sid in IMAGE_ONLY:
            assert so is None
            subject_status = 'verified_visually_graphical_option'
        elif (sid, letter) in TEXT_ARTIFACTS:
            subject_status = 'verified_visually_text_layer_artifact'
        else:
            assert so and loose(so['text']) == loose(i['displayed']), (sid, letter, 'subject')
            subject_status = 'verified_text_against_source'
        if detail:
            if (sid, letter) in PLACEHOLDERS:
                detail_status = 'printed_detail_preserved_in_copy_with_documented_reservation_in_ui'
            else:
                assert loose(detail['text']) == loose(i['displayedDetail']), (sid, letter, 'detail')
                detail_status = 'printed_individual_detail_verified'
        elif not cp:
            detail_status = 'unavailable_no_correction'
        elif cp['isHorsProgramme']:
            detail_status = 'unavailable_hors_programme_no_key'
        elif cp['general']:
            detail_status = 'not_printed_individually_general_reasoning_verified'
        else:
            detail_status = 'not_printed_individually_key_only'
        if cs:
            correction_statement_status = 'verified_same_wording' if loose(cs['text']) == loose(i['displayed']) else 'source_subject_correction_wording_difference_preserved'
        elif sid in IMAGE_ONLY:
            correction_statement_status = 'verified_visually_graphical_option'
        elif cp and cp['isHorsProgramme']:
            correction_statement_status = 'not_repeated_hors_programme'
        else:
            correction_statement_status = 'unavailable_no_correction'
        literal_key = cp['key'] if cp else None
        usable_key = bool(literal_key and re.fullmatch(r'[A-E]+|AUCUNE', literal_key))
        key_verdict = (letter in keyset(literal_key)) if usable_key else None
        verdict = None
        if detail:
            m = re.match(r'(VRAI|FAUX)\b', detail['text'], re.I)
            verdict = m[1].upper() if m else None
        conflict = bool(verdict is not None and key_verdict is not None and (verdict == 'VRAI') != key_verdict)
        if conflict:
            key_detail_conflicts.append({'sourceId': sid, 'item': letter, 'key': literal_key, 'detailVerdict': verdict})
        notes = [n['noteId'] for n in q.get('reviewNotes', []) if letter in n['items']]
        items.append({
            'id': letter, 'text': i['displayed'],
            'subject': {'status': subject_status, 'literal': so, 'sourceLabel': letter,
                        'figureProof': [x for x in ge['roles']['subject']['imageBoxes'] if x.get('fullyIncluded')] if sid in IMAGE_ONLY else []},
            'correctionStatement': {'status': correction_statement_status, 'literal': cs,
                                    'sourceLabel': i['correctionLabel'], 'mapping': (i['correctionLabel'] + ' → ' + letter) if sid == 'ue4:2023-2024:S1:q24' else None},
            'detail': {'status': detail_status, 'literal': detail, 'displayed': i['displayedDetail'],
                       'explicitVerdict': verdict, 'ambiguousPrintedVerdict': detail['text'] if detail and verdict is None else None},
            'grading': {'literalKeyVerdict': key_verdict, 'keyDetailConflict': conflict,
                        'graded': bool(q['answer'] or q.get('answerIsEmpty')), 'answer': q['answer'],
                        'officialKeyPreserved': q['rawAnswer']},
            'reviewNoteIds': notes,
            'reviewConclusion': 'La transcription et les sources disponibles sont rapprochées ; les réserves listées restent visibles après validation. Les détails absents ne sont pas présentés comme vérifiés.'
        })
        item_counts[subject_status] += 1; item_counts[detail_status] += 1
    grid = ge['roles']['correction']['grid']
    if cp and cp['key']:
        assert grid and keyset(cp['key']) == keyset(grid['key']), (sid, 'grid')
        assert keyset(cp['key']) == keyset(q['rawAnswer']), (sid, 'rawAnswer')
    if q['answer']:
        assert cp and keyset(q['answer']) == keyset(cp['key'])
    if q.get('answerIsEmpty'):
        assert cp['key'] == 'AUCUNE' and q['answer'] == '' and q['allowNoAnswer']
    general_status = 'not_applicable'
    if c['displayedGeneral'] or (cp and cp['general']):
        if sid == sid_missing:
            general_status = 'editorial_missing_correction_notice_supported_by_independent_inventory'
        elif sid == 'ue4:2020-2021:S1:q09':
            general_status = 'table_and_all_three_calculations_verified_visually_and_by_source_lines_after_E'
        else:
            assert loose(c['displayedGeneral']) == loose(cp['general']), sid
            general_status = 'general_reasoning_verified_against_source'
    stem_status = 'verified_text_against_source' if c['stemLooseMatch'] else 'verified_visually_image_text_and_descriptor_transcription'
    assert c['stemLooseMatch'] or sid == 'ue4:2019-2020:S1:q04'
    coverage.append({
        'bank': c['bank'], 'id': c['id'], 'sourceId': sid, 'year': c['year'], 'session': c['session'],
        'sourceNumber': c['sourceNumber'], 'correctionNumber': q.get('correctionNumber'),
        'consigne': {'status': stem_status, 'source': c['subject']['stem'], 'sourceRefs': c['subject']['stemRefs'],
                     'displayed': c['displayedStem'], 'sharedContexts': q.get('sharedContexts', []),
                     'sharedContextVerified': bool(q.get('sharedContexts'))},
        'subjectPages': sorted({p['page'] for p in cr['subject']}),
        'correctionPages': sorted({p['page'] for p in cr['correction']}),
        'literalKey': cp['key'] if cp else None, 'rawAnswer': q['rawAnswer'], 'gradingAnswer': q['answer'],
        'graded': bool(q['answer'] or q.get('answerIsEmpty')), 'answerIsEmpty': bool(q.get('answerIsEmpty')),
        'grid': grid, 'generalReasoning': {'status': general_status, 'displayed': c['displayedGeneral'],
                                        'source': cp['general'] if cp else '', 'sourceRefs': cp['generalRefs'] if cp else []},
        'items': items, 'geometry': ge['roles'],
        'copyStatus': {'subject': 'annotated_original_after_validation' if cr.get('subjectAfterCorrection') else 'clean_source',
                       'correction': 'available' if cr['correction'] else 'unavailable',
                       'subjectPanelCount': len(cr['subject']), 'correctionPanelCount': len(cr['correction']),
                       'noNeighborQuestion': True, 'noCorrectionIncludedInSubjectRole': True},
        'visualReview': {'completeSubjectIndividuallyRead': sid in visual_subject_ids,
                         'completeCorrectionIndividuallyRead': sid in visual_correction_ids,
                         'interactiveFigureRead': sid in figure_ids, 'associatedGridPageRead': bool(grid)},
        'reviewNoteIds': [n['noteId'] for n in q.get('reviewNotes', [])],
        'unresolvedOfficialSourceLimitation': not bool(q['answer'] or q.get('answerIsEmpty'))
    })
assert key_detail_conflicts == [{'sourceId': 'ue4:2020-2021:S2:q10', 'item': 'B', 'key': 'BDE', 'detailVerdict': 'FAUX'}]

for flag in raw_flags:
    f = deepcopy(flag); typ = f['type']; sid = f['sourceId']
    if typ == 'correctionPage':
        assert f['given'] in part_pages(source_by_id[sid]['correction'])
        outcome = 'Le pointeur historique désigne la page de clé/détail, incluse dans le bloc complet ; les panneaux approuvés couvrent aussi la page précédente. Aucune omission.'
    elif typ == 'subject' and sid == 'ue4:2020-2021:S1:q12':
        outcome = 'Contexte zinc séparé de E et rattaché aux seules Q13/Q14 dans le sujet et la correction.'
    elif typ == 'subject':
        outcome = 'Artefact de couche texte : le rendu affiche bien distribution / 50 %, conformément à la transcription.'
    elif typ == 'stem':
        outcome = 'Texte de consigne/descripteurs présent dans l’image source et transcrit fidèlement ; seule la copie complète annotée est différée.'
    elif typ == 'detail' and (sid, f.get('item')) in PLACEHOLDERS:
        outcome = 'Justification imprimée hors sujet conservée dans la preuve ; réserve V5 déjà documentée, inchangée.'
    elif typ == 'detail':
        outcome = 'Bloc général suivant E séparé correctement : contexte zinc ou tableau/calculs QSAR. Aucun texte perdu.'
    elif typ == 'key':
        assert keyset(f['site']) == keyset(f['source'])
        outcome = 'Ordre imprimé ABDCE ; même ensemble de réponses ABCDE dans la grille et la notation.'
    else:
        outcome = 'Différence imprimée entre sujet et reprise du corrigé ; texte exact du sujet conservé. Les unités Vig/mg et adsorption/absorption restent hors note. Le ABD supplémentaire de Q2 2023–2024 est un ajout de clé dans la reprise du corrigé.'
    f.update({'adjudicated': True, 'conclusion': outcome, 'blockingImportError': False})
    flags_adjudicated.append(f)
save('comparison_adjudication.json', flags_adjudicated)

series = []
for subject in [x for x in inventory if x['role'] == 'subject']:
    correction = next(x for x in inventory if x['role'] == 'correction' and x['year'] == subject['year'] and x['session'] == subject['session'])
    found = sorted(int(q['sourceNumber']) for _, q in questions if q['year'] == subject['year'] and q['session'] == subject['session'])
    assert found == subject['numbers']
    series.append({'year': subject['year'], 'session': subject['session'], 'subjectCover': subject['page'],
                   'subjectBodyPages': subject['bodyPages'], 'correctionCover': correction['page'],
                   'correctionBodyPages': correction['bodyPages'], 'gridPage': correction['page'] + 1,
                   'subjectQuestionCount': subject['count'], 'correctionQuestionCount': correction['count'],
                   'allSourceNumbersRepresented': True, 'missingQuestions': []})
graded = sum(x['graded'] for x in coverage)
summary = {
    'banks': len(approved['banks']), 'series': len(series), 'questionsCompared': len(coverage),
    'itemsComparedToSubject': sum(len(q['items']) for q in coverage),
    'correctionBlocksAvailable': sum(bool(q['correctionPages']) for q in coverage),
    'individualDetailsPrintedCompared': sum(bool(i['detail']['literal']) for q in coverage for i in q['items']),
    'individualDetailsNotPrintedOrUnavailable': sum(not bool(i['detail']['literal']) for q in coverage for i in q['items']),
    'graded': graded, 'ungraded': len(coverage) - graded, 'allFalseGraded': sum(q['answerIsEmpty'] for q in coverage),
    'literalUnambiguousKeys': sum(bool(q['literalKey'] and re.fullmatch('[A-E]+|AUCUNE', q['literalKey'])) for q in coverage),
    'ambiguousKeys': sum(q['literalKey'] == '(C)E' for q in coverage),
    'subjectPanels': sum(len(c['subject']) for c in crops), 'correctionPanels': sum(len(c['correction']) for c in crops),
    'cleanSubjectCopies': sum(not c.get('subjectAfterCorrection') for c in crops),
    'annotatedSubjectCopiesAfterValidation': sum(bool(c.get('subjectAfterCorrection')) for c in crops),
    'absentSubjectCopies': 0, 'missingCorrectionCopies': sum(not bool(c['correction']) for c in crops),
    'completeSubjectsVisuallyRead': len(visual_subject_ids), 'completeCorrectionsVisuallyRead': len(visual_correction_ids),
    'interactiveFiguresVisuallyRead': len(figure_ids), 'gridPagesVisuallyRead': sum(len(x['pages']) for x in visual['grids']),
    'coursePagesVisuallyRead': sum(len(x['pages']) for x in visual['courses']),
    'notesPreserved': len(notes_check), 'noteReferencesChecked': sum(len(x['refs']) for x in notes_check),
    'removedIncorrectReferencesVerified': len(removed_ref_checks), 'itemStatusCounts': dict(item_counts),
    'sourceYears': [series[-1]['year'], series[0]['year']], 'omittedQuestionsInRepresentedSeries': 0,
    'independentKeyDetailContradictions': key_detail_conflicts,
}
assert summary['graded'] == 324 and summary['ungraded'] == 12 and summary['allFalseGraded'] == 1
assert summary['individualDetailsPrintedCompared'] == 1625 and summary['individualDetailsNotPrintedOrUnavailable'] == 55
assert summary['subjectPanels'] == 338 and summary['correctionPanels'] == 731
save('coverage.json', {'status': 'complete_with_explicit_source_limitations', 'summary': summary,
                       'method': 'Nouvelle extraction de tous les sujets/corrigés UE4 depuis le PDF, rapprochement des 1 680 items, lecture des détails et réserves, contrôle des cadres et des grilles ; lecture visuelle individuelle des cas listés, sans prétendre avoir regardé individuellement toutes les images.',
                       'series': series, 'questions': coverage})

missing = deepcopy(load(PREP / 'missing.json'))
missing['blockingOfficialDocumentsOrErrata'].append({
    'sourceId': sid_duplicate, 'bank': 'ue4.annales.theme.sources-naturelles', 'id': by_id[sid_duplicate]['id'],
    'items': ['D', 'E'], 'kind': 'identical_statements_opposite_verdicts',
    'neededDocumentOrClarification': 'Erratum officiel de UE4 2018–2019 S1 Q15 : préciser l’énoncé correct de D/E ou leurs verdicts. Les deux propositions imprimées sont identiques, D VRAI et E FAUX.',
    'subjectPages': [967], 'correctionPages': [979], 'gridPage': 972,
    'currentTreatment': 'hors_note_by_independent_verifier_official_BCD_preserved',
    'evidence': 'Lecture directe des images p967/979 : « Un extrait brut peut être actif » dans D et E, aucune différence de négation ni de ponctuation ; la clé BCD et le détail FAUX de E ne peuvent produire une notation cohérente.',
    'searchesPerformed': ['Sujet et corrigé détaillé relus visuellement.', 'Grille p972 comparée.', 'Note antérieure ue4-v4-022 et absence d’erratum dans les documents inventoriés vérifiées.']
})
for entry in missing['blockingOfficialDocumentsOrErrata']:
    entry['independentVerification'] = {'sourceId': entry['sourceId'], 'sourceRecord': 'independent_comparison.json',
                                         'sameSeriesGridChecked': bool(geometry[entry['sourceId']]['roles']['correction']['grid']),
                                         'documentInventoriesChecked': ['documents_available.json', 'additional_documents.json'],
                                         'globalSourceSearch': 'source_searches.json',
                                         'graded': False}
assert {x['sourceId'] for x in missing['blockingOfficialDocumentsOrErrata']} == {x['sourceId'] for x in coverage if not x['graded']}
missing['independentScopeConclusion'] = 'Aucune question manquante parmi les 336 sujets des 14 séries disponibles. La recherche dans les 1 660 pages et les deux inventaires ne trouve aucune autre série UE4 ≥2015. Les années antérieures à 2018–2019 ne sont pas déclarées relues faute de série fournie. Les douze limites de correction empêchent seulement la notation des QCM concernés.'
missing['subjectWithoutCleanCompleteOriginal'] = {'sourceId': 'ue4:2019-2020:S1:q04',
    'neededDocumentOrClarification': 'Facultatif : original non annoté complet du sujet QSAR 2019–2020 Q4 ; la version actuelle complète reste après validation, la figure interactive propre est disponible.',
    'subjectPage': 941, 'currentTreatment': 'subjectAfterCorrection:true ; copie complète authentique sans retouche'}
save('missing.json', missing)

issues = {
    'status': 'no_unresolved_import_blocker_after_approved_changes',
    'independentFixes': changes,
    'preparerFixesIndependentlyConfirmed': {'wrongReferencesRemoved': 20, 'affectedNotes': 19,
                                           'BPFMissingCorrectionPointersNull': True, 'proof': 'notes_verification.json'},
    'sourceContradictionsAndMissingDocuments': missing['blockingOfficialDocumentsOrErrata'],
    'sourceStatementDifferences': [x for x in flags_adjudicated if x['type'] == 'correctionStatement'],
    'annotationHandling': [{'sourceId': 'ue4:2019-2020:S1:q04', 'subjectAfterCorrection': True,
                            'interactiveFigureCleanAndComplete': True,
                            'integrationRequirement': 'Appliquer le verrou après validation à toute voie montrant la copie complète, y compris les anciens originalImages ; utiliser les panneaux approuvés pour la copie V6.'}],
    'labelMapping': {'sourceId': 'ue4:2023-2024:S1:q24', 'subject': 'A–E', 'correctionStatement': 'F–J',
                     'correctionKeyAndDetails': 'A–E', 'mapping': {'F': 'A', 'G': 'B', 'H': 'C', 'I': 'D', 'J': 'E'}, 'documentedInCrops': True},
    'sharedContext': {'sourceIds': ['ue4:2020-2021:S1:q13', 'ue4:2020-2021:S1:q14'], 'subjectPage': 879,
                      'correctionPage': 890, 'excludedFromPreviousQ12': True},
    'rawComparisonFlagsAdjudicated': len(flags_adjudicated), 'geometryBlockingIssues': [],
    'baselineDifferences': baseline_differences,
    'visualizationLimit': '30 sujets et 29 corrigés lus individuellement en image ; les autres ont un contrôle textuel/source et géométrique, toutes les grilles et les 13 figures ont été vues.'
}
save('issues.json', issues)
save('changes.json', changes)
save('approved_reviewed.json', approved)
(OUT / 'approved_crops.json').write_bytes((PREP / 'crops.json').read_bytes())
save('asset_manifest.json', [])
save('source_manifest.json', [])

hashes = {name: sha(OUT / name) for name in ['approved_reviewed.json', 'approved_crops.json', 'coverage.json', 'issues.json', 'missing.json', 'asset_manifest.json']}
approval = {'approved': True, 'status': 'FEU_VERT_FINAL_AVEC_LIMITES_DOCUMENTAIRES_EXPLICITES',
            'scope': 'Pharmacologie UE4 V6 — 15 banques, 336 QCM, 1680 items',
            'message': 'Feu vert final pour intégrer les objets complets approved_reviewed.json et approved_crops.json. Les douze QCM sans notation fiable restent hors note ; les clés et réserves historiques sont conservées. La copie annotée 2019–2020 Q4 doit rester accessible seulement après validation.',
            'reviewed': {'path': str(OUT / 'approved_reviewed.json'), 'sha256': hashes['approved_reviewed.json']},
            'crops': {'path': str(OUT / 'approved_crops.json'), 'sha256': hashes['approved_crops.json']},
            'files': hashes, 'summary': summary,
            'inputHashes': {'prepare/reviewed.json': sha(PREP / 'reviewed.json'), 'prepare/crops.json': sha(PREP / 'crops.json'),
                            'baseline_exams.json': sha(ROOT / 'work/site_v6/baseline_exams.json'), 'Annales_compilation.pdf': sha(PDF)},
            'integrationRequirements': ['Utiliser les versions approuvées complètes.',
                                        'Toutes les copies de corrigé et les 179 remarques restent après validation.',
                                        'Propager subjectAfterCorrection de 2019–2020 Q4 à toutes les voies des copies originales ; la figure interactive propre reste visible.',
                                        'Conserver les deux profils, clés de stockage, IDs et classement thématique ; aucun changement de ces données n’est demandé.'],
            'limitations': ['Aucun corrigé n’existe dans les documents fournis pour 2021–2022 S1 Q13.',
                            '55 items ne disposent pas de détail individuel imprimé : ils ne sont pas qualifiés de justifiés par un texte absent.',
                            'Les réserves scientifiques non tranchées conservent les clés officielles ; aucune validation clinique ou réglementaire actuelle n’est revendiquée.',
                            'La présente approbation documentaire ne remplace pas les contrôles d’intégration de l’interface par l’agent principal.']}
save('approved.json', approval)
print(json.dumps({'summary': summary, 'hashes': hashes, 'baselineChangedQuestions': len(baseline_differences), 'existingGraphicEntries': len(assets)}, ensure_ascii=False, indent=2))
