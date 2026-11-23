import json, hashlib, re
from pathlib import Path
from collections import Counter
import fitz
from PIL import Image
V=Path(__file__).parent; P=V.parent/'prepare'; WS=V.parents[3]
D=fitz.open(WS/'output/site/sources/Annales_compilation.pdf')
R=json.loads((P/'reviewed.json').read_text())
C=json.loads((V/'proposed_crops.json').read_text())
CM={(c['bank'],c['id']):c for c in C}
A=json.loads((P/'asset_audit.json').read_text())
H={a['src'] for a in json.loads((V/'horizontal_candidates.json').read_text())}
AM={a['src']:a for a in A}
out=V/'assets'; out.mkdir(exist_ok=True)
manifest=[]; repairs=[]; replacements={}; removed=set()

def q(bank,n):return next(q for q in R['banks'][bank]['questions'] if q['id']==n)
def save(name, data):(V/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

# Independent matching of the unlabeled A in the source, followed by the explicit B-E.
x=q('annales.ue3.2024-2025.s1',10)
x['explanations']={
 'A':"FAUX : Comme le suivi s’arrête lors du diagnostic de métastases, certains patients parmi les 100 ont été suivi sur une période inférieure à 10 ans. Le nombre de personne-année est inférieur à 10 x 100.",
 'B':"VRAI : Le risque de survenue de métastases durant les 10 ans correspond à l’incidence, ce qu’une étude de cohorte (suivi de patients indemnes dans le temps) permet d’obtenir.",
 'C':"FAUX : L’étude se base sur 100 patients sélectionnés indemnes, ils ne sont pas représentatifs de la population générale. De plus, l’étude de cohorte ne permet pas de calculer une prévalence, c’est une étude transversale qui nous aurait fallu.",
 'D':"VRAI : L’incidence de métastase est plus élevée chez les hommes que chez les femmes (l’ordre des mots dans la phrase est important, on parle du RR homme sur femme donc le risque des homme sur le risque des femmes). Donc RR > 1.",
 'E':"VRAI : Toujours en respectant l’ordre de la phrase, DR = Risque homme – Risque femme."
}
repairs.append({'bank':'annales.ue3.2024-2025.s1','id':10,'type':'restore_item_explanations','items':list('ABCDE'),'page':519,'evidence':'Ligne FAUX non lettrée immédiatement après la clé BDE, puis B–E explicitement imprimés.'})
x=q('annales.ue3.2023-2024.s2',1)
x['explanations']={
 'A':"FAUX : 75% des valeurs d’un échantillon sont supérieurs au 1° quartile (=25% sont donc inférieurs)",
 'B':"FAUX : 25% des valeurs d’un échantillon sont supérieur au 3° quartile (=75% sont donc inférieures)",
 'C':"FAUX : 50% des valeurs d’un échantillon sont supérieures à la médiane et non à la moyenne",
 'D':"VRAI : l’item reste vrai même en remplaçant “supérieures“ par “inférieures dans la question“",
 'E':"FAUX : l’IQR contient 50% d’un échantillon donc les 50% restant sont en dehors de l’IQR"
}
repairs.append({'bank':'annales.ue3.2023-2024.s2','id':1,'type':'restore_item_explanations','items':list('ABCDE'),'page':555,'evidence':'Cinq verdicts FAUX, FAUX, FAUX, VRAI, FAUX sans lettres, dans l’ordre A–E et concordant avec la clé D. La réserve sur les égalités de quantiles est conservée.'})
note=next(n for n in q('annales.ue3.2020-2021.s1',3)['reviewNotes'] if n['noteId']=='biostat-v6-2020-2021.s1-3-D')
old=note['text']
note['text']='Passer de 36 à 144 sujets multiplie l’effectif par 4 et divise l’erreur type ainsi que la demi-largeur de l’intervalle par √4 = 2. Avec les valeurs de cet exercice, la demi-largeur passe de 1/3 à 1/6, et non à 1/12 comme indiqué dans le détail du corrigé. Le verdict D est conservé. Vérifier ce point dans la ronéo UE3 correspondante.'
repairs.append({'bank':'annales.ue3.2020-2021.s1','id':3,'type':'repair_scientific_reserve_arithmetic','items':['D'],'source_pages':[635,642],'before':old,'after':note['text']})

# Keep every original correction pixel belonging to the current Q; remove only the
# following Q's context already delimited independently in the original PDF.
for src,a in AM.items():
    correction=a['field']=='correctionImages'
    if not correction and src not in H: continue
    x0,y0,x1,y1=a['rect']
    rect=[30,y0,570,y1]
    if correction:
        ps=[p for p in CM[(a['bank'],a['id'])]['correction'] if p['page']==a['page']]
        if not ps:
            removed.add(src)
            repairs.append({'bank':a['bank'],'id':a['id'],'type':'remove_next_question_only_image','src':src,'page':a['page'],'source_text':D[a['page']-1].get_text('text',clip=fitz.Rect(a['rect']),sort=True).strip()})
            continue
        rect[1]=max(rect[1],min(p['rect'][1] for p in ps))
        rect[3]=min(rect[3],max(p['rect'][3] for p in ps))
        assert rect[3]>rect[1]
    pix=D[a['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(rect),colorspace=fitz.csRGB)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    name='verified_'+Path(src).stem+'.webp'; file=out/name; im.save(file,'WEBP',lossless=True)
    new='static/revision_v6/biostat/'+name
    replacements[src]=new
    manifest.append({'file':str(file.resolve()),'src':new})
    repairs.append({'bank':a['bank'],'id':a['id'],'type':'authentic_asset_recrop','old_src':src,'src':new,'page':a['page'],'old_rect':a['rect'],'rect':rect,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'reason':'Restore full line width; correction boundaries restricted to current Q.' if correction else 'Restore full line width (printed span crossed x=550).','format':'lossless WebP, PDF pixels 2×, no retouch'})

def walk(value):
    if isinstance(value,str):return replacements.get(value,value)
    if isinstance(value,list):return [walk(v) for v in value if not isinstance(v,str) or v not in removed]
    if isinstance(value,dict):return {k:walk(v) for k,v in value.items()}
    return value
R=walk(R)
save('working_reviewed.json',R)
save('working_crops.json',C)
save('asset_manifest.json',manifest)
save('repairs.json',repairs)
print(json.dumps({'assets':len(manifest),'removed_images':len(removed),'repairs':Counter(r['type'] for r in repairs)},ensure_ascii=False))
