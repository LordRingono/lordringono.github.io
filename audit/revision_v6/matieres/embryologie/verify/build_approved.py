"""Fusion documentaire indépendante, limitée aux 22 banques d'embryologie.

Entrées figées du préparateur + preuves et rectangles contrôlés par le vérificateur.
Ne modifie jamais le site de sortie.
"""
from pathlib import Path
import json, copy, fitz, re, unicodedata, collections

ROOT=Path('/workspace/scratch/f3cb3bb97377')
V=ROOT/'work/site_v6/embryologie/verify'; P=ROOT/'work/site_v6/embryologie/prepare'
R=json.load(open(P/'reviewed.json')); C=json.load(open(P/'crops.json'))
QS={(b,q['id']):q for b,bank in R['banks'].items() for q in bank['questions']}
CS={(c['bank'],c['id']):c for c in C}
changes=[]
def norm(t): return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t.replace('œ','oe')).encode('ascii','ignore').decode().lower())
def ref(file,page,label=None):
    return {'file':file,'page':page,'label':label or f'{file} — p. {page}',
            'href':f'sources/{file if file=="Annales_compilation.pdf" else "revision_v4/"+file}#page={page}'}
def note(q,bank,items,nid,text,refs,kind='source_conflict'):
    notes=q.setdefault('reviewNotes',[])
    if not any(n.get('noteId')==nid for n in notes):
        notes.append({'bank':bank,'id':q['id'],'items':items,'kind':kind,'noteId':nid,'text':text,'refs':refs})
def change(q,bank,field,new,reason):
    old=copy.deepcopy(q.get(field))
    if old!=new:
        q[field]=new; changes.append({'bank':bank,'id':q['id'],'field':field,'old':old,'new':copy.deepcopy(new),'reason':reason})
def missing_warning_removed(t):
    t=re.sub(r'Sujet non corrigé absent de l’archive\s*:\s*[^.]*\.?\s*','',t)
    t=re.sub(r'Consigne non récupérable automatiquement\.\s*Voir la page source\.\s*','',t)
    return t.strip()

for qid in [54,55,68]:
    q=QS['embryo.col.s4',qid]
    change(q,'embryo.col.s4','warning',missing_warning_removed(q.get('warning','')),
           'La consigne et le schéma commun sont désormais rétablis ; avertissement ancien retiré.')
for ids,page in [([31,32],7),([41,42],9)]:
    for qid in ids:
        q=QS['embryo.col.s3',qid];contexts=copy.deepcopy(q['sharedContexts'])
        for context in contexts:context['sourceStartPage']=page;context['sourceEndPage']=page
        change(q,'embryo.col.s3','sharedContexts',contexts,'Pagination du bloc commun vérifiée dans le PDF original.')
for qid,iid in [(2,'C'),(3,'B')]:
    q=QS['embryo.ann.s1',qid];ops=copy.deepcopy(q['options'])
    for opt in ops:
        if opt['id']==iid:opt['text']=re.sub(r'\s+HP\s*$','',opt['text'])
    change(q,'embryo.ann.s1','options',ops,
           'Le marqueur HP du corrigé est une annotation de notation ; il demeure dans ignoredOptions et la correction, sans contaminer l’item.')
q=QS['embryo.aut.s3',8];ex=copy.deepcopy(q['explanations'])
ex['D']='Vrai, très réduite (relativement = 0,15 mm), avec une coupe transversale dans la partie caudale, entre la membrane cloacale et le nœud de Hensen (pas comme sur votre schéma qui est une coupe en avant de la ligne primitive).'
change(q,'embryo.aut.s3','explanations',ex,
       'La fin du détail D, qui distingue la coupe figurée de la coupe décrite, avait été omise ; relue sur le corrigé p.3 sans englober E.')

# Réparation prouvée visuellement : le morceau barré est l'énoncé original,
# et non un texte à supprimer avec la correction ajoutée « à 21 J ».
q=QS['embryo.ann.gamet',10]
ops=copy.deepcopy(q['options']);ops[0]['text']='L’ovogénèse est un phénomène discontinu qui débute avec la différenciation de la crête génitale à la 8ème semaine du développement embryonnaire.'
change(q,'embryo.ann.gamet','options',ops,'Phrase originale barrée relue visuellement dans le corrigé p.2 ; restauration de la portion omise, item toujours HP.')
ex=copy.deepcopy(q['explanations']);ex['A']='Hors programme dans la source. Le corrigé barre « avec la différenciation de la crête génitale à la 8ème semaine » et ajoute « à 21 J ».'
change(q,'embryo.ann.gamet','explanations',ex,'Restitution littérale de la correction et du marqueur HP, sans modifier la clé.')

# Les 60 sujets sont authentiques et sans correction. Vingt recoupent des
# copies issues des PDF mixtes ; les remplacer élimine notamment le corrigé
# placé à côté de la figure de l'annale S2 ID14.
supp=json.load(open(V/'compilation_supplements.json'))
for s in supp:
    bank=s['bank'];q=QS[bank,s['id']];cr=CS[bank,s['id']];sub=s['subject']
    if (bank,s['id'])==('embryo.ann.gamet',23):
        # Le marqueur D est décalé dans l'ordre du texte PDF, contrôle visuel
        # du sujet p.1404 : la phrase complète appartient bien à D.
        sub['items']['C']='Le blocage de la méiose en prophase I est, entre autres, contrôlé par les cellules folliculeuses qui établissent des jonctions avec l’ovocyte I.'
        sub['items']['D']='Le 1er globule polaire et l’ovocyte II sont des cellules haploïdes, chaque chromosome est constitué de 2 chromatides.'
        s['diffs']=[];s['exactItems']=5;s['parserRepair']='La ligne D était extraite après le début de sa phrase ; séparation C/D vérifiée visuellement.'
    printed=re.match(r'^\s*(\d+)\.',sub['title'])
    source_number=int(printed.group(1)) if printed else q['sourceNumber']
    cr['subject']=[{'file':s['file'],'page':sub['page'],'rect':sub['rect'],
                    'fileLabel':'Annales_compilation.pdf — sujet original','sourceNumber':source_number}]
    cr.pop('subjectMissing',None);cr.pop('subjectAfterCorrection',None)
    cr['subjectFile']='Annales_compilation.pdf'
    cr['subjectNote']='Sujet original de la compilation générale, rapproché de la session et de chacun des cinq items. Le corrigé thématique demeure la référence, sauf complément de correction explicitement identifié.'
    if source_number!=q['sourceNumber']:
        cr['subjectNote']+=f" Le QCM porte le numéro {source_number} dans cette compilation et le numéro {q['sourceNumber']} dans le document thématique."
    if s['diffs'] and (bank,s['id'])!=('embryo.ann.gamet',13):
        cr['subjectNote']+=' De petites différences de formulation entre les éditions sont conservées dans les documents originaux.'
    change(q,bank,'sourceSubject','Annales_compilation.pdf','Sujet non corrigé retrouvé et comparaison de chaque item.')
    change(q,bank,'subjectPage',sub['page'],'Pagination exacte du sujet retrouvé.')
    change(q,bank,'sourceEndPage',sub['page'],'Pagination exacte du sujet retrouvé.')
    change(q,bank,'warning',missing_warning_removed(q.get('warning','')),'Retrait de l’avertissement obsolète de sujet absent.')
    if s.get('yearMismatch'):
        change(q,bank,'category',sub['year'],'Le cartouche de session du sujet original indique 2020–2021, et non 2019–2020.')
    if (bank,s['id']) in [('embryo.ann.gamet',15),('embryo.ann.s2',14)]:
        opt='E' if bank.endswith('gamet') else 'B'
        ops=copy.deepcopy(q['options'])
        for o in ops:
            if o['id']==opt:o['text']=sub['items'][opt].rstrip('.')+'.'
        change(q,bank,'options',ops,'Précision de l’énoncé original : ovocytes I / lame choriale, contrôlée visuellement sur la copie non corrigée.')

# Sept clés absentes rétablies et une clé « RIEN » confirmée ; les détails
# du tutorat et les annotations thématiques restent explicitement séparés.
keyrows=json.load(open(V/'compilation_new_keys.json'))
for k in keyrows:
    bank=k['bank'];q=QS[bank,k['id']];cr=CS[bank,k['id']]
    oldfile=q['sourceCorrection'];oldpage=q.get('correctionPage')
    ex=copy.deepcopy(q.get('explanations',{}))
    for iid,detail in k['explanations'].items():
        before=ex.get(iid,'')
        ex[iid]=f'Corrigé du tutorat — session 1 2022–2023 : {detail}'
        if before and norm(before)!=norm(detail):
            ex[iid]+=f'\n\nAnnotation du corrigé thématique : {before}'
    change(q,bank,'explanations',ex,'Les cinq verdicts/détails ont été lus dans le corrigé de la compilation ; annotations thématiques conservées et attribuées.')
    change(q,bank,'answer',k['answer'],'Grille p.1232 et cinq verdicts détaillés concordants, après appariement du sujet.')
    change(q,bank,'rawAnswer',k['rawKey'],'Clé littérale de la grille officielle de la compilation.')
    if k['allowNoAnswer']:
        q['allowNoAnswer']=True;q['answerIsEmpty']=True
    else:
        q.pop('allowNoAnswer',None);q.pop('answerIsEmpty',None)
    q['uncorrected']=False
    change(q,bank,'warning',re.sub(r'Réponse officielle non identifiable avec certitude\s*:\s*ce QCM est hors note\.\s*','',q.get('warning','')).strip(),'Clé de correction identifiée, avertissement ancien retiré.')
    cr['correction'].append({'file':k['file'],'page':k['page'],'rect':k['rect'],
                              'fileLabel':'Annales_compilation.pdf — corrigé du tutorat, session 1 2022–2023','sourceNumber':k['sourceNumber']})
    for panel in cr['correction']:
        panel.setdefault('fileLabel',Path(panel['file']).name+' — corrigé thématique')
        panel.setdefault('sourceNumber',q['sourceNumber'])
    cr['correctionNote']='Deux documents sont conservés : le corrigé thématique puis le corrigé détaillé du tutorat 2022–2023 retrouvé dans la compilation. La clé de la compilation concorde avec sa grille p.1232. Les annotations sont attribuées à leur document ; les divergences sont signalées après correction.'
    note(q,bank,list(k['items']),f'embryo-v6-compilation-key-{bank}-{q["id"]}',
         f'La grille de la session 1 2022–2023 (compilation p.1232) et les cinq verdicts détaillés p.{k["page"]} donnent la clé « {k["rawKey"]} ». Ce complément est utilisé pour la notation ; les annotations du corrigé thématique sont reproduites séparément.',
         [ref('Annales_compilation.pdf',1232,'Grille du tutorat — session 1 2022–2023'),ref('Annales_compilation.pdf',k['page'],'Corrigé détaillé du tutorat')])

q=QS['embryo.ann.fec',18]
note(q,'embryo.ann.fec',['B'],'embryo-v6-fec18-key-divergence',
     'Divergence entre deux corrigés du même item B : la grille ABDE et le détail du tutorat le donnent Vrai, tandis que le corrigé thématique barre « les cellules du cumulus » et le remplace par « la zone pellucide ». La notation reprend la grille explicite du tutorat ; cette divergence reste à vérifier dans la ronéo. Les deux originaux sont disponibles dans le menu de correction.',
     [ref('Annales_compilation.pdf',1234),ref('2_Annales_Fecondation_LS_correction_56ee0ecad9.pdf',4)],'roneo_conflict')

# Points scientifiques relus dans les documents de cours fournis : les clés
# officielles ne sont pas remplacées par une opinion du vérificateur.
newnotes=[
('embryo.ann.gamet',25,['D'],'centriole-axoneme',
 'L’annotation remplace les triplets par des doublets dans la structure dite « centriole distal ». La fiche de cours distingue le centriole proximal (9 triplets) de l’axonème provenant du centriole distal (9 doublets périphériques et un doublet central). Le terme « centriole distal » utilisé comme synonyme de cet axonème mérite donc une vérification dans la ronéo ; la clé du corrigé est conservée.',
 [ref('3_FS_gametogenese_LS_423b1d6f34.pdf',4),ref('2_Annales_meiose_et_gametogenese_LS_CORRECTION_3f2ba9f3b8.pdf',6)]),
('embryo.ann.s3',11,['E'],'barriere-contact',
 'Le corrigé remplace « empêche le contact » par « favorise ». La ronéo précise pourtant que la barrière sépare les circulations maternelle et embryonnaire et empêche leur communication directe, tout en permettant les échanges. Ne pas confondre contact direct des sangs et échanges à travers la barrière. La date S2 rend également l’item faux dans la clé ; vérifier l’explication dans la ronéo.',
 [ref('Roneo_S3_05579bfe1f.pdf',7),ref('Roneo_S3_05579bfe1f.pdf',11),ref('2_Annales_3e_semaine_de_devlp_emb_LS_Enonce_et_correction_1_6e7bec8576.pdf',3)]),
('embryo.ann.s3',26,['A'],'processus-chordal-terme',
 'La clé « RIEN » est explicite dans la compilation. Pour A, les justifications datent la fin du processus chordal de J16, tandis que la ronéo présente sa transformation en canal à J16, en plaque à J17–18 puis en chorde à J18–22. Le sens donné à « processus chordal » (structure initiale ou ensemble de son évolution) doit être relu dans la ronéo ; aucune clé n’est déduite de cette ambiguïté. La formulation ectoblaste/épiblaste de l’item E est, elle, explicitement admise dans la ronéo p.47.',
 [ref('Annales_compilation.pdf',1238),ref('Roneo_S3_05579bfe1f.pdf',22),ref('Roneo_S3_05579bfe1f.pdf',47)]),
('embryo.ann.s3',29,['B'],'plaque-prechordale',
 'L’explication imprimée semble confondre plaque préchordale et plaque chordale lorsqu’elle décrit une disparition et un détachement donnant la chorde. La ronéo indique que la plaque préchordale reste présente même lorsqu’elle n’est plus dessinée ; elle distingue son rôle de celui de la plaque chordale. La réponse B reste celle du corrigé, mais sa justification doit être vérifiée dans la ronéo.',
 [ref('Roneo_S3_05579bfe1f.pdf',24),ref('Roneo_S3_05579bfe1f.pdf',25),ref('Roneo_S3_05579bfe1f.pdf',27),ref('2_Annales_3e_semaine_de_devlp_emb_LS_Enonce_et_correction_1_6e7bec8576.pdf',7)]),
('embryo.ann.s3',30,['D'],'wolff-tubules',
 'Le détail du corrigé discute surtout le caractère supposé exclusif de l’énumération, mais l’item écrit aussi « tubules pronéphrotiques ». La ronéo décrit le corps de Wolff avec les tubules mésonéphrotiques, le canal de Wolff et du tissu mésoblastique. Cette différence de nom est à vérifier dans la ronéo ; la clé officielle, qui compte D faux, est conservée.',
 [ref('1_2_Roneo_CG_corrigees_S4_du_DE_LS_35a5fce5f2.pdf',27),ref('1_2_Roneo_CG_corrigees_S4_du_DE_LS_35a5fce5f2.pdf',28),ref('2_Annales_3e_semaine_de_devlp_emb_LS_Enonce_et_correction_1_6e7bec8576.pdf',8)])]
for bank,qid,items,nid,txt,refs in newnotes:
    note(QS[bank,qid],bank,items,'embryo-v6-'+nid,txt,refs,'roneo_conflict')

# Cadrages : huit fins de ligne touchent la marge basse fixe ; les copier
# jusqu'à la fin réelle de la ligne. Le cadre commun Q31/32 était anonyme.
CI=json.load(open(V/'coverage_initial.json'))
for ir in CI:
    row=CS[ir['bank'],ir['id']]
    for panel in row['correction']:
        if Path(panel['file']).name!=Path(ir['source']).name:continue
        ends=[l['bbox'][3] for it in ir['items'] for seg in it['sourceSegments'] for l in seg['lines']
              if l['page']==panel['page'] and 790<l['bbox'][1]<panel['rect'][3]+2]
        if ends and max(ends)>panel['rect'][3]-.2: panel['rect'][3]=max(ends)+4
for qid in [31,32]:
    CS['embryo.col.s3',qid]['correction'][0]['rect'][1]=17.83

# Mise en page originale en colonnes : une figure peut dépasser les items.
# Les rectangles texte sont alors séparés de la figure entière, sans effacer
# le moindre pixel de l'original ni inclure les items voisins.
docs={};repair_log=[]
def doc(file):
    if file not in docs:docs[file]=fitz.open(file)
    return docs[file]
def subtract(rect,img):
    hit=rect&img
    if hit.is_empty:return [rect]
    out=[fitz.Rect(rect.x0,rect.y0,rect.x1,hit.y0),fitz.Rect(rect.x0,hit.y1,rect.x1,rect.y1),
         fitz.Rect(rect.x0,hit.y0,hit.x0,hit.y1),fitz.Rect(hit.x1,hit.y0,rect.x1,hit.y1)]
    return [r for r in out if r.width>2 and r.height>2]
for row in C:
    for role in ['subject','correction']:
        newpanels=[]
        for panel in row[role]:
            page=doc(panel['file'])[panel['page']-1];rect=fitz.Rect(panel['rect'])
            # Compilation crops have all been visually verified separately.
            if Path(panel['file']).name=='Annales_compilation.pdf':newpanels.append(panel);continue
            images=[]
            for im in page.get_image_info():
                r=fitz.Rect(im['bbox']) & page.rect
                if r.width>30 and r.height>20 and (r&rect).get_area()>0:
                    ratio=(r&rect).get_area()/r.get_area()
                    images.append((r,ratio))
            if not any(.03<ratio<.999 for _,ratio in images):newpanels.append(panel);continue
            owned=[r for r,ratio in images if ratio>.5]
            # Les bandes sont alignées sur des lignes ENTIÈRES, jamais sur
            # l'arête d'une image qui peut traverser l'ascendante d'une lettre.
            textlines=[]
            for block in page.get_text('dict')['blocks']:
                if block.get('type')!=0:continue
                for line in block['lines']:
                    lr=fitz.Rect(line['bbox'])
                    if not ''.join(s['text'] for s in line['spans']).strip():continue
                    if not (rect.y0 <= (lr.y0+lr.y1)/2 <= rect.y1):continue
                    if (lr&rect).get_area()/max(lr.get_area(),1)<.5:continue
                    # Text labels drawn over a figure remain in its own crop.
                    if any((lr&r).get_area()/max(lr.get_area(),1)>.98 for r,_ in images):continue
                    left,right=rect.x0,rect.x1
                    for im,_ in images:
                        if im.y0<lr.y1 and im.y1>lr.y0:
                            if lr.x1<=im.x0+1:right=min(right,im.x0-1)
                            elif lr.x0>=im.x1-1:left=max(left,im.x1+1)
                    left=min(left,lr.x0-2);right=max(right,lr.x1+2)
                    textlines.append((lr,left,right))
            textlines.sort(key=lambda x:(x[0].y0,x[0].x0))
            parts=[]
            for lr,left,right in textlines:
                box=fitz.Rect(max(0,left),max(rect.y0,lr.y0-2),min(page.rect.x1,right),min(page.rect.y1,lr.y1+2))
                if parts and abs(parts[-1].x0-box.x0)<1 and abs(parts[-1].x1-box.x1)<1 and box.y0-parts[-1].y1<20:
                    parts[-1]=parts[-1]|box
                else:parts.append(box)
            for r in parts:
                np=copy.deepcopy(panel);np['rect']=[round(v,3) for v in r];newpanels.append(np)
            for r in owned:
                r=fitz.Rect(r.x0-1,r.y0-1,r.x1+1,r.y1+1)&page.rect
                np=copy.deepcopy(panel);np['rect']=[float(v) for v in r];np['panelLabel']='Schéma original complet';newpanels.append(np)
            repair_log.append({'bank':row['bank'],'id':row['id'],'role':role,'page':panel['page'],
                               'originalRect':panel['rect'],'textPanels':len(parts),'completeFigures':len(owned)})
        row[role]=newpanels
        if any(x.get('panelLabel') for x in newpanels):
            row[role+'Note']=(row.get(role+'Note','')+' La disposition en colonnes nécessite plusieurs captures : texte puis schéma original complet.').strip()

# Ajustements visuels : le cartouche IWP est un objet vectoriel qui dépasse
# le bitmap ; la copie complète doit conserver également ce cartouche.
for qid in [23,24]:
    for panel in CS['embryo.aut.s4',qid]['correction']:
        if panel.get('panelLabel')=='Schéma original complet' and panel['page']==8:
            panel['rect'][2]=579.0
# Q30 imprimé (ID34) longe la figure du Q29. Les espaces de fin de ligne
# débordent légèrement sur cette figure et provoquaient des panneaux doublés.
row=CS['embryo.col.s2',34]
base=copy.deepcopy(row['correction'][0])
row['correction']=[]
for rect in [[24.0,130.848,431.6,226.5],[24.0,226.8,575.32,322.522]]:
    panel=copy.deepcopy(base);panel['rect']=rect;row['correction'].append(panel)
for qid in [54,55]:
    row=CS['embryo.col.s4',qid]
    row['correction'][1]['rect'][3]=row['correction'][2]['rect'][3]
    del row['correction'][2]

for row in C:
    q=QS[row['bank'],row['id']]
    for role in ['subject','correction']:
        for panel in row[role]:
            panel.setdefault('fileLabel',Path(panel['file']).name)
            panel.setdefault('sourceNumber',q['sourceNumber'])
    if (row['bank'],row['id']) in [('embryo.aut.s4',23),('embryo.aut.s4',24),('embryo.aut.coeur',5),('embryo.aut.coeur',6)]:
        assert row.get('subjectAfterCorrection') is True
        assert q.get('imagesAfterCorrection') is True
        assert all(ctx.get('imagesAfterCorrection') for ctx in q.get('sharedContexts',[]) if ctx.get('images'))

(V/'approved_reviewed.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
(V/'approved_crops.json').write_text(json.dumps(C,ensure_ascii=False,indent=2))
(V/'verifier_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
(V/'crop_repairs.json').write_text(json.dumps(repair_log,ensure_ascii=False,indent=2))
(V/'compilation_supplements.json').write_text(json.dumps(supp,ensure_ascii=False,indent=2))
print('Approved',len(QS),'QCM',sum(len(q['options']) for q in QS.values()),'items')
print('Subject',sum(bool(c['subject']) for c in C),'correction',sum(bool(c['correction']) for c in C),'panels',sum(len(c[r]) for c in C for r in ['subject','correction']))
print('Changes',len(changes),'rectangle restructurings',len(repair_log))
