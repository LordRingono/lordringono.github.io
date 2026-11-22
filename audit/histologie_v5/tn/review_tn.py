from pathlib import Path
from copy import deepcopy
import json
import re
import fitz
from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tn'
BASE = json.loads((ROOT / 'baseline_exams.json').read_text())

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def paragraph_text(p):
    # python-docx omits the six original Wingdings right arrows.
    parts = []
    for node in p._p.iter():
        if node.tag == qn('w:t'):
            parts.append(node.text or '')
        elif node.tag == qn('w:sym'):
            assert node.get(qn('w:font')) == 'Wingdings'
            assert node.get(qn('w:char')) == 'F0E0'
            parts.append('→')
        elif node.tag in (qn('w:tab'), qn('w:br')):
            parts.append(' ')
    return norm(''.join(parts))

CONFIG = {
    'tn1': {
        'subject': 'autotest TN1(1).docx',
        'correction': 'CORRECTION autotest TN1(2).docx',
        's_heads': [2,9,16,23,30,37,44,51,61,68,75,82,89,96,103,110],
        'c_heads': [1,8,15,22,29,36,43,50,57,64,71,78,85,92,99,106],
        'counts': [5]*16,
    },
    'tn2': {
        'subject': 'AUTOTEST TN2(1).docx',
        'correction': 'correction autotest TN2(3).docx',
        's_heads': [1,8,15,22,30,39,48,60,68,77],
        'c_heads': [1,7,13,19,27,36,44,56,64,72],
        's_items': [2,9,16,23,31,40,54,61,69,78],
        'c_items': [2,8,14,20,28,37,50,57,65,73],
        'counts': [5,5,5,6,7,7,5,6,7,8],
    },
    'tn3': {
        'subject': 'AUTOTEST TN3(1).docx',
        'correction': 'CORRECTION AUTOTEST TN3(1).docx',
        's_heads': [1,8,15,22,29,36,44,66],
        'c_heads': [1,8,15,22,29,36,45,61],
        's_items': [2,9,16,23,30,38,60,68],
        'c_items': [2,9,16,23,30,39,55,63],
        'counts': [5]*8,
    },
}

def make_crops(code, role):
    pdf = next((ROOT/'render'/f'{code}_{role}').glob('*.pdf'))
    doc = fitz.open(pdf)
    pages = []
    headings = []
    for pi, page in enumerate(doc):
        elements = []
        for block in page.get_text('dict')['blocks']:
            if block['type'] == 1:
                elements.append((fitz.Rect(block['bbox']), '[image]'))
            for line in block.get('lines', []):
                txt = ''.join(s['text'] for s in line['spans']).strip()
                if not txt or txt.startswith(('EMSLB_', 'L. Bastin', 'C.ROCHET')):
                    continue
                bbox = fitz.Rect(line['bbox'])
                if txt.isdigit() and bbox.x0 > 500 and bbox.y0 > 770:
                    continue  # original page number in the footer
                elements.append((bbox, txt))
                pattern = r'^(\d+)\)' if code == 'tn1' else r'^QCM\s*(\d+)'
                m = re.match(pattern, txt)
                if m:
                    headings.append({'id': int(m.group(1)), 'page': pi, 'y': bbox.y0})
        pages.append(elements)
    assert [x['id'] for x in headings] == list(range(1,len(CONFIG[code]['counts'])+1))
    # Consistent full text width per document also preserves floating Word labels.
    all_rects = [r for p,els in enumerate(pages) for r,t in els
                 if (p, r.y0) >= (headings[0]['page'], headings[0]['y']-0.1)]
    x0 = max(0, min(r.x0 for r in all_rects)-7)
    x1 = min(doc[0].rect.width, max(r.x1 for r in all_rects)+7)
    result = {}
    for i, h in enumerate(headings):
        nxt = headings[i+1] if i+1 < len(headings) else None
        last_page = nxt['page'] if nxt else len(doc)-1
        parts = []
        for pi in range(h['page'], last_page+1):
            lo = h['y']-0.2 if pi == h['page'] else 18
            hi = nxt['y']-0.2 if nxt and pi == nxt['page'] else doc[pi].rect.height-15
            selected = [(r,t) for r,t in pages[pi] if r.y0 >= lo and r.y0 < hi]
            if not selected:
                continue
            y0 = max(0, min(r.y0 for r,t in selected)-5)
            y1 = min(doc[pi].rect.height, max(r.y1 for r,t in selected)+5)
            if code == 'tn1' and role == 'correction' and h['id'] == 1:
                # The document title frame ends immediately above Q1 (51.65 pt).
                y0 = h['y']
            if nxt and pi == nxt['page']:
                y1 = min(y1, nxt['y']-2)
            parts.append({'file':str(pdf.resolve()),'page':pi+1,
                          'rect':[round(x0,2),round(y0,2),round(x1,2),round(y1,2)]})
        result[h['id']] = parts
    return result

CROPS = {}
for code in CONFIG:
    CROPS[code] = {role:make_crops(code,role) for role in ('subject','correction')}

reviewed = {'banks': {}}
audit = {'scope':'Autotests histologie TN1, TN2, TN3',
         'sourcesCompared':json.loads((OUT/'source_comparison.json').read_text()),
         'method':'Comparaison exhaustive des paragraphes, des runs Word et du rendu original. Les verdicts sont transcrits explicitement et les flèches Wingdings conservées. Toutes les pages originales ont été inspectées visuellement.',
         'questions': []}

for code, cfg in CONFIG.items():
    bank = 'histo.'+code
    sp = Document(ROOT/'source'/cfg['subject']).paragraphs
    cp = Document(ROOT/'source'/cfg['correction']).paragraphs
    questions = deepcopy(BASE[bank]['questions'])
    assert len(questions)==len(cfg['counts'])
    for i,q in enumerate(questions):
        qid=i+1
        assert q['id']==qid
        count=cfg['counts'][i]
        si=cfg.get('s_items',[x+1 for x in cfg['s_heads']])[i]
        ci=cfg.get('c_items',[x+1 for x in cfg['c_heads']])[i]
        sh=cfg['s_heads'][i];ch=cfg['c_heads'][i]
        st=paragraph_text(sp[sh]);ct=paragraph_text(cp[ch])
        if code=='tn3' and qid==8:
            st+=' '+paragraph_text(sp[sh+1]);ct+=' '+paragraph_text(cp[ch+1])
        assert norm(st)==norm(ct), (bank,qid,st,ct)
        cleanstem=re.sub(r'^QCM\s*\d+\s*:?\s*','',st)
        assert norm(q['question'])==cleanstem, (bank,qid,q['question'],cleanstem)
        row={'bank':bank,'id':qid,'sourceSubject':cfg['subject'],'sourceCorrection':cfg['correction'],
             'subjectHeadingParagraph':sh,'correctionHeadingParagraph':ch,
             'subjectHeadingVerbatim':st,'correctionHeadingVerbatim':ct,
             'oldAnswer':q['answer'],'items':[],
             'subjectCaptures':CROPS[code]['subject'][qid],
             'correctionCaptures':CROPS[code]['correction'][qid],
             'visualReview':'Contrôlé sur les pages originales : consigne, tous les items, éventuelles figures et toutes les justifications.',
             'changes':[]}
        answer=''
        assert len(q['options'])==count
        for j,option in enumerate(q['options']):
            letter=chr(65+j)
            assert option['id']==letter
            original=paragraph_text(sp[si+j])
            corrected=paragraph_text(cp[ci+j])
            assert norm(option['text'])==original, (bank,qid,letter,option['text'],original)
            m=re.search(r'\b(vrai|faux)\b',corrected,re.I)
            mode='verdict explicite dans le corrigé'
            if m:
                literal=m.group(1)
                verdict=literal.lower()=='vrai'
                prefix=corrected[:m.start()].strip()
                detail=corrected[m.end():].strip().lstrip(',').strip()
                allowed=(code=='tn2' and qid==1 and letter=='D' and prefix==original.replace('Lipofuschine','Lipofuscine')) or (code=='tn3' and qid==5 and letter=='A' and prefix==original.replace('1présentent','1 présentent'))
                assert prefix==original or allowed, (bank,qid,letter,original,prefix)
                explanation=('Vrai.' if verdict else 'Faux.')+(' '+detail if detail else '')
                if code=='tn2' and qid==7:
                    explanation='Vrai. Le corrigé désigne explicitement cet ordre : 1-5-4-3-2.'
            else:
                assert code=='tn2' and qid==7 and letter in 'ABCD'
                assert corrected==original
                literal=None;verdict=False;prefix=corrected;detail=''
                mode='ordre non retenu : la consigne demande l’ordre correct et seule la proposition E est marquée Vrai'
                explanation='Faux. Cet ordre n’est pas celui retenu dans le corrigé, qui indique E : 1-5-4-3-2.'
            if verdict:answer+=letter
            old_explanation=q['explanations'].get(letter,'')
            item={'id':letter,'subjectParagraph':si+j,'correctionParagraph':ci+j,
                  'subjectVerbatim':original,'correctionVerbatim':corrected,
                  'correctionStatementVerbatim':prefix,'sourceVerdictLiteral':literal,
                  'verdict':verdict,'verdictBasis':mode,'sourceExplanation':detail,
                  'boldSourceRuns':[r.text for r in cp[ci+j].runs if r.bold],
                  'oldVerdict':letter in q['answer'],'oldItemText':option['text'],
                  'oldExplanation':old_explanation,'newExplanation':explanation,
                  'subjectCorrectionTextMatch':prefix==original,
                  'matchNote':('Identique après normalisation des espaces.' if prefix==original else 'Seule différence typographique du document corrigé : '+prefix),
                  'sourceSymbolsRestored':'→' in corrected,
                  'reviewResult':'conforme à la source'}
            if code=='tn3' and qid==5 and letter=='A':
                option['text']=option['text'].replace('1présentent','1 présentent')
                item['newItemText']=option['text']
                item['textEditReason']='Espace typographique confirmé dans le corrigé ; le sens de l’énoncé ne change pas.'
            q['explanations'][letter]=explanation
            row['items'].append(item)
        assert answer==q['answer'], (bank,qid,answer,q['answer'])
        row['newAnswer']=answer
        row['answerChanged']=False
        row['changes'].append('Verdict Vrai/Faux rendu explicite pour chaque item ; détail du corrigé intégral conservé.')
        if code=='tn2' and qid==7:
            row['oldWarning']=q['warning']
            q['warning']=''
            q['generalExplanation']='Le corrigé retient E : 1-5-4-3-2. Les cinq événements à ordonner restent affichés au-dessus des propositions.'
            assert all(paragraph_text(sp[k])==paragraph_text(cp[k-4]) for k in range(49,54))
            row['sharedContextVerified']=[paragraph_text(sp[k]) for k in range(49,54)]
            row['changes'].append('Suppression de l’ancien avertissement hors note : la clé E et les cinq propositions sont confirmées dans le corrigé.')
        q['sourceSubject']=cfg['subject'];q['sourceCorrection']=cfg['correction']
        q['subjectPage']=CROPS[code]['subject'][qid][0]['page']
        q['correctionPage']=CROPS[code]['correction'][qid][0]['page']
        q['approximateDocxPage']=False
        for note in q.get('reviewNotes',[]):
            note['reviewedItemText']={o['id']:o['text'] for o in q['options'] if o['id'] in note['items']}
            note['reviewedExplanation']={l:q['explanations'][l] for l in note['items']}
        audit['questions'].append(row)
    reviewed['banks'][bank]={'questions':questions}

def add_note(bank,qid,letter,kind,text,sourcefile,sourcepath,page,label,noteid):
    q=next(q for q in reviewed['banks'][bank]['questions'] if q['id']==qid)
    note={'bank':bank,'id':qid,'items':[letter],'kind':kind,'text':text,
          'refs':[{'file':sourcefile,'page':page,'label':label,'href':f'sources/revision_v4/{sourcepath}#page={page}'}],
          'sourceVerdict':'Clé de référence : '+q['answer'],
          'reviewedItemText':{letter:next(o['text'] for o in q['options'] if o['id']==letter)},
          'reviewedExplanation':{letter:q['explanations'][letter]},'noteId':noteid}
    q.setdefault('reviewNotes',[]).append(note)
    row=next(r for r in audit['questions'] if r['bank']==bank and r['id']==qid)
    row.setdefault('scientificNotesAdded',[]).append(note)

add_note('histo.tn1',7,'D','possible_error',
    'Item D : le corrigé retient Vrai et ajoute « + la dure mère ». La formulation de l’énoncé est donc incomplète si elle est comprise comme une liste exhaustive : la ronéo décrit trois méninges, la dure-mère, l’arachnoïde et la pie-mère. La clé officielle est conservée ; vérifier cette nuance dans la ronéo.',
    'TN1 - Ronéo 2026 - ACTUALISEE.pdf','TN1_Roneo_2026_ACTUALISEE_629067c364.pdf',5,
    'Trois méninges autour du système nerveux central','v5-histo-tn1-q7-d')
add_note('histo.tn2',2,'D','possible_error',
    'Item D : Vrai est conservé. Le détail du corrigé décrivant un déplacement de l’extrémité − vers l’extrémité + correspond au transport antérograde. Il ne faut pas en déduire que tout transport axonal suit ce sens : la ronéo distingue aussi le transport rétrograde, dans l’autre sens, assuré par la dynéine. Vérifier cette distinction dans la ronéo.',
    'TN2 - Ronéo 2026 - Actualisée.pdf','TN2_Roneo_2026_Actualisee_660afa6a3c.pdf',7,
    'Deux sens du transport axonal','v5-histo-tn2-q2-d')
add_note('histo.tn2',6,'D','possible_error',
    'Item D : Faux est cohérent avec « très présentes », mais le détail « SNP » du corrigé est trop abrégé. La ronéo indique que les synapses électriques sont très rares dans le SNC et en donne un exemple dans l’olive bulbaire inférieure. Ne pas comprendre ce détail comme une absence totale dans le SNC ; vérifier le passage de la ronéo.',
    'TN2 - Ronéo 2026 - Actualisée.pdf','TN2_Roneo_2026_Actualisee_660afa6a3c.pdf',11,
    'Synapses électriques : présence rare dans le SNC','v5-histo-tn2-q6-d')
add_note('histo.tn3',5,'B','roneo_conflict',
    'Item B : le corrigé retient Vrai mais reprend le mot « récepteurs ». La ronéo parle de transporteurs spécifiques GLUT1 et GLUT4. Le terme transporteur est donc à retenir pour ce mécanisme ; vérifier la terminologie dans la ronéo. La clé du corrigé est conservée.',
    'TN3 - Ronéo 2026.pdf','TN3_Roneo_2026_252c9211d9.pdf',11,
    'Transporteurs GLUT1 et GLUT4 des astrocytes','v5-histo-tn3-q5-b')

crops=[{'bank':'histo.'+code,'id':qid,
        'subject':CROPS[code]['subject'][qid],
        'correction':CROPS[code]['correction'][qid]}
       for code in CONFIG for qid in CROPS[code]['subject']]
audit['summary']={'questions':len(audit['questions']),
                  'items':sum(len(q['items']) for q in audit['questions']),
                  'answerKeysChanged':0,'existingScientificNotesPreserved':2,
                  'newScientificNotes':4,'sourceArrowsRestored':6,
                  'originalPagesVisuallyInspected':16,
                  'obsoleteWarningsRemoved':1,'typographicItemRepairs':1,
                  'captureParts':sum(len(q['subject'])+len(q['correction']) for q in crops)}
audit['captureVisualQA'] = {
    'inspectedParts':75,
    'qaSheetsDirectory':'work/histo_v5/tn/crop_qa',
    'outcome':'Toutes les découpes inspectées. Consignes, items et détails complets ; figures et lettres Word présentes. L’amorce du cadre de titre au-dessus de TN1 Q1 corrigé a été exclue après inspection.',
}
for name,data in [('reviewed.json',reviewed),('audit.json',audit),('crops.json',crops)]:
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(audit['summary'],ensure_ascii=False,indent=2))
for q in crops:
    print(q['bank'],q['id'],[(r,[f"p{x['page']}:{x['rect'][1]}-{x['rect'][3]}" for x in q[r]]) for r in ['subject','correction']])
