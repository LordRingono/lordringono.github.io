from pathlib import Path
import hashlib,json,math
import fitz
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent;R=H.parents[1];W=R.parents[1]
load=lambda f:json.loads(f.read_text())
b=load(R/'baseline_exams.json');r=load(H/'reviewed.json')['banks'];a=load(H/'audit.json');c=load(H/'crops.json')
assert len(r)==70 and len(a)==len(c)==278
assert sum(len(z['items']) for z in a)==1390
seen=set();notes=0
for k,v in r.items():
    assert {x['id'] for x in v['questions']}=={x['id'] for x in b[k]['questions']}
    assert {z:v[z] for z in v if z!='questions'}=={z:b[k][z] for z in b[k] if z!='questions'}
    old={q['id']:q for q in b[k]['questions']}
    for q in v['questions']:
        key=(k,q['id']);assert key not in seen;seen.add(key)
        o=old[q['id']]
        assert q['answer']==o['answer'] and q['weight']==o['weight']
        assert [x['id'] for x in q['options']]==[x['id'] for x in o['options']]
        assert q['question']==o['question'] and q.get('generalExplanation')==o.get('generalExplanation')
        for note in o.get('reviewNotes',[]):assert note in q.get('reviewNotes',[]);notes+=1
assert notes==35
assert seen=={(x['bank'],x['id']) for x in a}=={(x['bank'],x['id']) for x in c}
assert all(len(q['items'])==5 for q in a)
assert all(i['subjectLiteral'] is not None and i['correctedStatementLiteral'] is not None and i['detailedLiteral'] for q in a for i in q['items'])
d=fitz.open(W/'output/site/sources/Annales_compilation.pdf')
for cp in c:
    assert cp['subject'] and cp['correction']
    for role in ('subject','correction'):
        for p in cp[role]:
            rect=fitz.Rect(p['rect']);page=d[p['page']-1]
            assert Path(p['file']).exists() and rect.width>10 and rect.height>2
            assert -0.1<=rect.x0<=rect.x1<=page.rect.width+.1
            assert -0.1<=rect.y0<=rect.y1<=page.rect.height+.1
assert sum(x.get('subjectAfterCorrection',False) for x in c)==4
assert sum(not z['graded'] for z in a)==5
for manifest in ['source_manifest.json','asset_manifest.json']:
    for x in load(H/manifest):
        p=Path(x.get('absolute') or x['file']);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
# Recalculate only the repaired numerical passages, independently of layout code.
calculations={
 '2022s1_Q24_Km':(5e4+1e2)/5e9,
 '2022s1_Q24_Vmax':30e-6*(1e-5+5e-5)/5e-5,
 '2021s1_Q24_Km':(2e4+1e2)/8e9,
 '2021s1_Q24_Vmax':25e-6*(2.5e-6+2.5e-6)/2.5e-6,
 '2021s1_Q24_D_true_calculation':50e-6*4/5,
 '2020paces_Q35_Km':(1e4+1e2)/1e9,
 '2020paces_Q35_Vmax':1e-5*(1e-5+1e-4)/1e-4,
 '2025s1_Q26_Ki':4e-5/((1/(2e6))/(1/(4e6))-1)
}
assert math.isclose(calculations['2021s1_Q24_D_true_calculation'],40e-6)
assert math.isclose(calculations['2025s1_Q26_Ki'],4e-5)
(H/'validation.json').write_text(json.dumps({'status':'passed','scope':'invariants, source geometry, manifests, repaired calculations; not an independent verifier approval','questions':278,'items':1390,'oldNotesPreserved':35,'keyChanges':0,'calculations':calculations},ensure_ascii=False,indent=2)+'\n')

# Fresh render of the boundary cases introduced by the final crop recipes.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
cases=[('2021s1',32,'subject'),('2020s1',25,'subject'),('2018',34,'correction'),('2022s2',16,'correction'),('2020s1',30,'subject')]
for s,n,role in cases:
    aq=next(x for x in a if(x['sourceSet'],x['sourceNumber'])==(s,n));cp=next(x for x in c if(x['bank'],x['id'])==(aq['bank'],aq['id']))
    panes=[]
    for p in cp[role]:
        # Grid crops are checked separately on all 14 grid pages, not expanded here.
        if p['fileLabel']=='Grille récapitulative de correction':continue
        pm=d[p['page']-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5),clip=fitz.Rect(p['rect']),alpha=False)
        im=Image.frombytes('RGB',[pm.width,pm.height],pm.samples)
        im.thumbnail((900,1600))
        pane=Image.new('RGB',(920,im.height+32),'white');ImageDraw.Draw(pane).text((8,4),f'{s} Q{n} {role} — page {p["page"]}',font=font,fill='black');pane.paste(im,(10,28));panes.append(pane)
    out=Image.new('RGB',(920,sum(i.height for i in panes)+12*(len(panes)-1)),(210,220,225));y=0
    for im in panes:out.paste(im,(0,y));y+=im.height+12
    out.save(H/'visual'/f'final_{s}_q{n}_{role}.jpg',quality=93)
print('Validation passed; rendered 5 boundary checks.')
