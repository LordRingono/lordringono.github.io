"""An explicit source boundary for the unnumbered J13 diagram on S2 p.4.

The source has no question number before the stem, only before its answer key.
Keep the two adjacent questions independent before building the reviewed data.
"""
import copy,json,pathlib
P=pathlib.Path(__file__).parent
S=json.load(open(P/'segments.json'));E=json.load(open(P/'extraction.json'))
name='2. Annales S2 LS Correction.pdf'
a,b=S[name][11],S[name][12]
assert a['num']==3 and b['num']==7 and a['page']==b['page']==4
for block in (a,a['correctionPart']):
 block['lines']=[l for l in block['lines'] if l['page']==4 and l['bbox'][1]<290]
cp=copy.deepcopy(b.get('correctionPart',b))
cp['lines']=[l for l in cp['lines'] if l['page']==4 and l['bbox'][1]>=660]
lines=[dict(l,page=4) for l in E[name][3]['lines'] if 330<l['bbox'][1]<650]
subject={'num':7,'index':None,'page':4,'y':lines[0]['bbox'][1],'text':lines[0]['text'],'groupSecond':None,'lines':lines}
b.update(page=4,y=subject['y'],text=subject['text'],lines=lines+cp['lines'],subjectPart=subject,correctionPart=cp)
(P/'segments.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Explicit unnumbered subject boundary repaired: S2 p.4 / IDs12–13')
