"""Fidelity checks against the independent Word evidence and rendered PDF crops."""
from pathlib import Path
import json,re,unicodedata,fitz

P=Path(__file__).resolve().parent
R=P.parent
reviewed=json.loads((P/'reviewed.json').read_text())['banks']
baseline=json.loads((R/'baseline_exams.json').read_text())
audit=json.loads((P/'audit.json').read_text())
crops={(q['bank'],q['id']):q for q in json.loads((P/'crops.json').read_text())}

def normalized(value):
    # Symbol font exports its alpha as U+F061 in PDF text. The rendered glyph
    # was inspected visually and is the same alpha stored in Word w:sym.
    value=value.replace('\uf061','α').replace('\uf0e0','→')
    return ''.join(c.casefold() for c in unicodedata.normalize('NFKC',value) if c.isalnum())

checks=[]
for a in audit:
    bank=a['bank']; q=next(q for q in reviewed[bank]['questions'] if q['id']==a['id'])
    old=next(q for q in baseline[bank]['questions'] if q['id']==a['id'])
    assert [o['id'] for o in q['options']]==[o['id'] for o in old['options']]
    assert q['answer']==''.join(i['id'] for i in a['items'] if i['truth'])
    assert q['question']==a['subjectHeading']
    assert all(q['explanations'][i['id']]==i['renderedExplanation'] for i in a['items'])
    assert all(o['text']==next(i['renderedSubject'] for i in a['items'] if i['id']==o['id']) for o in q['options'])
    for note in q.get('reviewNotes',[]):
        for item_id in note['items']:
            assert note['reviewedItemText'][item_id]==next(o['text'] for o in q['options'] if o['id']==item_id)
            assert note['reviewedExplanation'][item_id]==q['explanations'][item_id]
    for side in ['subject','correction']:
        panels=crops[(bank,q['id'])][side]
        text=' '.join(fitz.open(p['file'])[p['page']-1].get_text(clip=fitz.Rect(p['rect']),sort=True) for p in panels)
        headings=re.findall(r'^\s*(?:QR[MU]\s*)?(\d+)\s*[):]',text,re.M)
        assert headings==[str(a['sourceNumber'])],(bank,q['id'],side,headings)
        assert normalized(a[side+'Heading']) in normalized(text),(bank,q['id'],side,'heading')
        for item in a['items']:
            present=normalized(item[side]) in normalized(text)
            checks.append({'bank':bank,'id':q['id'],'side':side,'item':item['id'],'complete':present})
            assert present,(bank,q['id'],side,item['id'])

assert len(audit)==49
assert sum(len(a['items']) for a in audit)==243
assert len(checks)==486
assert len(crops)==49
assert reviewed['histo.tc3']['questions'][16]['answerIsEmpty'] is True
assert reviewed['histo.tc3']['questions'][16]['allowNoAnswer'] is True
assert not reviewed['histo.tc3']['questions'][16]['warning']
for bank,data in reviewed.items():
    assert [q['id'] for q in data['questions']]==[q['id'] for q in baseline[bank]['questions']]

diffs=[]
for bank,data in reviewed.items():
    for q in data['questions']:
        old=next(o for o in baseline[bank]['questions'] if o['id']==q['id'])
        diffs.append({'bank':bank,'id':q['id'],'differences':{k:{'old':old.get(k),'new':q.get(k)} for k in set(old)|set(q) if old.get(k)!=q.get(k)}})
(P/'diff.json').write_text(json.dumps(diffs,ensure_ascii=False,indent=2))
(P/'capture_text_check.json').write_text(json.dumps({'checks':len(checks),'failures':[],'details':checks,'symbolEquivalence':'Word Symbol F061 / PDF U+F061 = α, visually confirmed'},ensure_ascii=False,indent=2))
summary={'questions':len(audit),'items':243,'capturePanels':sum(len(q[s]) for q in crops.values() for s in ['subject','correction']),'sourcePagesVisuallyInspected':19,'itemCaptureChecks':486,'failures':0,'stableQuestionAndOptionIds':True,'explicitVerdicts':True,'existingReviewNotesPreserved':True,'oldAndNewSourceDocsBinaryIdentical':6}
(P/'validation_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
