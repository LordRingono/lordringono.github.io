import json, copy, hashlib, re, shutil
from pathlib import Path
import fitz
from independent_extract import norm

ROOT=Path('/workspace/scratch/f3cb3bb97377')
BASE=ROOT/'work/site_v6/ssh'; PREP=BASE/'prepare'; OUT=BASE/'verify'
def read(p):return json.loads(p.read_text())
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(PREP/'reviewed.json')=='3817b079f8f00bfe548da0efdf5d9b918afd7a2fa27538c5fbfbe5d2a67125c4'
assert sha(PREP/'crops.json')=='a439d5c05e0d2afe1bc3f2868e7a9e8c90ffef6dde5672f014d024e0fa277d23'
original=read(PREP/'reviewed.json'); approved=copy.deepcopy(original)
manifest=read(PREP/'source_manifest.json')
sources={(s['bank'],s['role']):s for s in manifest}
new_notes=[]
def annotate(bank,id,item,kind,text,external=()):
    q=next(q for q in approved['banks'][bank]['questions'] if q['id']==id)
    refs=[]
    for role,pkey,label in [('subject','subjectPage','Sujet fourni'),('correction','correctionPage','Corrigé fourni')]:
        s=sources[(bank,role)]
        refs.append({'file':Path(s['absolute']).name,'page':q[pkey],'label':label,'href':s['packaged']+'#page='+str(q[pkey])})
    refs.extend({'label':label,'href':url,'referenceType':'external_primary'} for label,url in external)
    note={'noteId':f'ssh-v6-verify-{bank}-{id}-{item}','kind':kind,'items':[item],'text':text+' Vérifier ce point dans la ronéo du cours correspondant.','refs':refs,'sourceVerdict':q['answer'],'courseVerdict':None,'coversWarning':False}
    q.setdefault('reviewNotes',[]).append(note)
    new_notes.append({'bank':bank,'id':id,**note})

annotate('colle2',73,'B','scientific_reserve',
    'Le verdict FAUX est conservé, mais son explication reprend un ancien cadre. Depuis le 26 décembre 2021, l’article L1412-2 prévoit un président et 45 autres membres, avec un mandat de trois ans renouvelable une fois pour chacun. Les indications « président : deux ans » et « 39 membres : quatre ans » ne décrivent donc pas le droit applicable au sujet 2026–2027.',
    [('Code de la santé publique — L1412-2, version depuis le 26 décembre 2021','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043896447/2026-07-31')])
annotate('colle2',74,'C','scientific_reserve',
    'Le détail est trop général lorsqu’il présente toute recherche sur les iPS comme relevant d’une simple déclaration. La loi de 2021 soumet à déclaration auprès de l’ABM certains protocoles précisément définis : différenciation en gamètes, modèles de développement embryonnaire in vitro ou insertion dans un embryon animal destiné à être transféré chez la femelle. L’ABM peut s’y opposer, les suspendre ou les interdire. Le verdict FAUX de l’item est conservé.',
    [('Loi du 2 août 2021, article 21 — régime des recherches sur les iPS','https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000043884428')])
annotate('colle2',39,'A','scientific_reserve',
    'La date de 2003 donnée dans le détail correspond à l’achèvement du Projet génome humain, dont la séquence restait lacunaire. Le NHGRI distingue cette étape des travaux T2T de 2022 qui ont comblé les régions encore manquantes. Le terme « complet » doit donc être situé dans son contexte historique. L’item proposant 1995 reste FAUX.',
    [('NHGRI — Human Genome Project, achèvement de 2003 et travaux T2T','https://www.genome.gov/about-genomics/educational-resources/fact-sheets/human-genome-project')])
annotate('colle1',43,'E','scientific_reserve',
    'Le verdict FAUX est conservé. En revanche, le mot « automatiquement » dans le détail appelle une réserve : l’article L1142-1 prévoit la responsabilité des établissements pour les dommages résultant d’infections nosocomiales, sauf s’ils rapportent la preuve d’une cause étrangère. Le régime sans faute ne doit pas être présenté comme dépourvu de toute exception.',
    [('Code de la santé publique — L1142-1, responsabilité pour infection nosocomiale','https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072665/LEGISCTA000006185260/2026-05-24/')])
annotate('colle1',55,'C','source_ambiguity',
    'Le correcteur déclare cet item FAUX à cause de la formulation « d’autres troubles », qu’il interprète comme qualifiant le HPI de trouble. Il précise lui-même que l’idée de troubles moins repérés serait admise avec une autre formulation. Il ne faut donc pas transformer ce verdict en affirmation selon laquelle une dyslexie serait toujours aussi facilement repérée chez un enfant HPI. Il s’agit ici d’un piège de rédaction propre au corrigé fourni.')
annotate('colle1',69,'D','source_ambiguity',
    'Le sujet et le corrigé comparent tous deux une probabilité « a posteriori » à la même probabilité « a posteriori ». Cette répétition rend la formulation incohérente. Le détail semble viser la comparaison avec la probabilité a priori, qui peut augmenter ou diminuer après une information nouvelle, mais l’original institutionnel manque pour confirmer cette intention. Le texte et le verdict FAUX fournis sont conservés.')
annotate('eb',37,'D','scientific_reserve',
    'L’item est compté VRAI dans la source, mais la mention « premiers hôpitaux » ne peut pas désigner l’apparition des hôpitaux en général après la peste de 1347 : l’Hôtel-Dieu de Paris existait dès le VIIe siècle. La portée attendue est peut-être celle d’institutions spécialement destinées aux épidémies ; le corrigé ne l’explique pas. Ne pas retenir cette formulation comme une chronologie générale de l’hôpital.',
    [('Ville de Paris — histoire de l’Hôtel-Dieu et des hôpitaux parisiens','https://www.paris.fr/pages/grandes-et-petites-histoires-sur-les-hopitaux-parisiens-7694')])

# The old AP-HP PDF URL in one new preparer note returns 404. Preserve the note,
# its identifier and evidence type; point the link to the AP-HP history consulted.
ref_repairs=[]
for bank,b in approved['banks'].items():
    for q in b['questions']:
        for n in q.get('reviewNotes',[]):
            for r in n.get('refs',[]):
                if 'Une-page-dhistoire.pdf' in r.get('href',''):
                    old=r['href']; r['href']='https://pitiesalpetriere.aphp.fr/chapelle-saint-louis-histoire-de-la-chapelle-de-la-pitie-salpetriere'
                    r['label']='AP-HP — histoire de la Pitié-Salpêtrière, création de l’Hôpital général en 1656'
                    ref_repairs.append({'bank':bank,'id':q['id'],'noteId':n['noteId'],'oldHref':old,'newHref':r['href'],'reason':'Ancien PDF 404 ; autre publication de la même institution consultée.'})

# All pre-existing 39 note objects remain byte-for-byte equivalent as JSON.
old=read(PREP/'reviewed_initial.json')
for bank,b in old['banks'].items():
    for q in b['questions']:
        new=next(x for x in approved['banks'][bank]['questions'] if x['id']==q['id'])
        for n in q.get('reviewNotes',[]):
            assert n in new.get('reviewNotes',[]),(bank,q['id'],n['noteId'])
for bank,b in original['banks'].items():
    for before,after in zip(b['questions'],approved['banks'][bank]['questions']):
        for k,v in before.items():
            if k!='reviewNotes':assert after[k]==v,(bank,before['id'],k)
write('approved_reviewed.json',approved)
shutil.copyfile(PREP/'crops.json',OUT/'approved_crops.json')

ind=read(OUT/'independent_sources.json'); comp=read(OUT/'independent_comparison.json')
crop_audit={(x['bank'],x['id']):x for x in read(OUT/'crop_audit.json')}
crop_definitions={(x['bank'],x['id']):x for x in read(PREP/'crops.json')}
visual_seen={
    'acc':[1,9,15,16,25,26,34,38],
    'colle2':[10,11,12,39,73,74,76],
    'colle1':[12,43,55,69],
    'eb':[6,37,54,77]
}
assert sum(map(len,visual_seen.values()))==23
read_batches={'acc':[[1,19],[20,38]],'colle2':[[1,20],[21,40],[41,60],[61,79]],'colle1':[[1,26],[27,52],[53,78]],'eb':[[1,27],[28,54],[55,79]]}

# Independent comparison against the whole 79-entry summary grid, rather than
# trusting either the prepared JSON or the detailed text sequence alone.
grid_doc=fitz.open(sources[('colle2','correction')]['absolute'])
grid_pairs=re.findall(r'N°(\d+)\s+([A-E]{1,5}|—)',grid_doc[1].get_text())
grid={int(n):k for n,k in grid_pairs if int(n)<=79}
assert len(grid)==79
for n,key in grid.items():assert key==ind['colle2'][str(n)]['correction']['keys'][0],n
write('independent_grid_check.json',{'bank':'colle2','page':2,'entries':grid,'all79MatchDetailedKeys':True,'q11q12KeysNotApplicableToSuppliedSubject':True})

coverage=[]; issues=[]; per_item=[]
accepted_subject={('acc',5,'E'):'Pluriel « sexuelle » / « sexuelles » ; sens identique et version importée conforme à la répétition corrigée.',('acc',29,'A'):'Singulier/pluriel « erreur » / « erreurs » ; sens identique.',('acc',31,'D'):'Singulier/pluriel « motivations » / « motivation » ; sens identique.'}
for cr in comp:
    bank=cr['bank']; id=cr['id']; q=next(x for x in approved['banks'][bank]['questions'] if x['id']==id)
    src=ind[bank][str(id)]; ca=crop_audit[(bank,id)]
    mismatch=bank=='colle2' and id in [11,12]
    assert mismatch or q['answer']==src['correction']['keys'][0]
    if mismatch:
        assert q['answer']=='' and not q.get('answerIsEmpty') and crop_definitions[(bank,id)]['correctionMismatch']
    assert norm(q.get('generalExplanation','')) in norm(src['correction'].get('generalDetail',''))
    # ACC 3 has a pre-existing harmless article mismatch le/la, accepted explicitly.
    stem_exact=norm(q['question']) in norm(src['subject']['text'])
    assert stem_exact or (bank,id)==('acc',3)
    for c in q.get('sharedContexts',[]):assert norm(c['text']) in norm(src['subject']['text'])
    citems=[]
    for it in cr['perItem']:
        letter=it['item']; key=(bank,id,letter)
        assert it['subjectContainsExact'] or key in accepted_subject
        assert mismatch or it['verdict']==it['importedVerdict']
        assert mismatch or it['explanationExact']
        assert ca['subjectOptionsInCrops'][letter] or key in accepted_subject
        assert ca['correctionDetailsInCrops'].get(letter,True)
        record={
            'bank':bank,'id':id,'item':letter,
            'textReadIndependently':True,'subjectCompared':True,'correctionCompared':True,
            'subjectTextStatus':'exact_normalized' if it['subjectContainsExact'] else 'minor_grammar_accepted',
            'subjectTextException':accepted_subject.get(key),
            'repeatedStatementStatus':'non_corresponding_question' if mismatch else ('exact_normalized' if it['repeatedOptionExact'] else 'minor_source_wording_difference_reviewed'),
            'importedText':it['importedItem'],'correctedDocumentRepeatedText':it['originalRepeatedItem'],
            'printedVerdictObserved':'VRAI' if it['verdict'] else 'FAUX',
            'applicableSourceVerdict':None if mismatch else ('VRAI' if it['verdict'] else 'FAUX'),
            'gradingStatus':'excluded_no_matching_correction' if mismatch else 'matches_source',
            'correctionDetailStatus':'non_corresponding_detail_excluded' if mismatch else ('verbatim_normalized' if it['originalDetail'] else 'no_detail_in_source'),
            'sourceDetail':it['originalDetail'],'siteDetail':it['importedDetail'],
            'sourceDetailInvented':False,
            'subjectPages':sorted({x['page'] for x in ca['panels'] if x['role']=='subject'}),
            'correctionPages':sorted({x['page'] for x in ca['panels'] if x['role']=='correction'}),
            'cropTextCoverageChecked':True,'cropGeometryChecked':True,'sourceCropsRendered':True,
            'visualContactSheetRead':id in visual_seen[bank],
            'noteIds':[n['noteId'] for n in q.get('reviewNotes',[]) if letter in n.get('items',list('ABCDE'))]
        }
        citems.append(record);per_item.append(record)
        if not it['subjectContainsExact'] or not it['repeatedOptionExact']:
            issues.append({'bank':bank,'id':id,'item':letter,'type':'source_text_comparison','status':'accepted_source_mismatch_excluded' if mismatch else 'accepted_minor_wording','subjectException':accepted_subject.get(key),'siteText':it['importedItem'],'repeatedCorrectionText':it['originalRepeatedItem']})
    coverage.append({
        'bank':bank,'id':id,'status':'verified_source_missing_correction' if mismatch else 'verified_source_fidelity',
        'subjectSha256':sources[(bank,'subject')]['sha256'],'correctionSha256':sources[(bank,'correction')]['sha256'],
        'stemStatus':'exact_normalized' if stem_exact else 'minor_article_le_la_accepted',
        'sharedContextsVerified':len(q.get('sharedContexts',[])),
        'itemSequence':'ABCDE','keyImported':q['answer'],'printedKeyObserved':src['correction']['keys'][0],
        'summaryGridChecked':bank=='colle2','generalExplanationVerified':bool(q.get('generalExplanation')),
        'manualTextReadBatch':next(r for r in read_batches[bank] if r[0]<=id<=r[1]),
        'sourceSubjectAuthenticToSuppliedDocument':True,'sourceCorrectionAuthenticToSuppliedDocument':True,
        'institutionalOriginalAvailable':bank in ['acc','colle2'],
        'visualContactSheetRead':id in visual_seen[bank],
        'cropPanelCount':len(ca['panels']),'perItem':citems,
        'noteIds':[n['noteId'] for n in q.get('reviewNotes',[])],
        'scientificReview':'Reservations documented separately; source key retained; ronéo not supplied.'
    })
assert len(coverage)==274 and len(per_item)==1370
write('coverage.json',coverage)
issues.extend({'bank':n['bank'],'id':n['id'],'items':n['items'],'type':n['kind'],'noteId':n['noteId'],'status':'annotated_after_correction','text':n['text'],'refs':n['refs']} for n in new_notes)
issues.append({'type':'reference_link_repair','status':'repaired','changes':ref_repairs})
issues.append({'type':'source_no_explanatory_detail','status':'preserved_without_invention','originalAllItemsWithoutDetail':752,'applicableItemsWithoutDetail':746,'siteBlankExplanations':756,'explanation':'746 items dans les 272 QCM assortis du bon corrigé ; 10 items des deux QCM sans corrigé correspondant restent également sans détail dans le site.'})
issues.append({'bank':'acc','id':3,'type':'minor_stem_wording','status':'accepted','detail':'le/la dans « Cochez le ou les item(s) » ; aucune incidence sur les propositions ou la clé.'})
write('issues.json',issues)
missing=read(PREP/'missing.json')
for m in missing:
    if m['type']=='roneos':m['questions']=[{'bank':bank,'id':q['id'],'noteIds':[n['noteId'] for n in q['reviewNotes']]} for bank,b in approved['banks'].items() for q in b['questions'] if q.get('reviewNotes')]
write('missing.json',missing)
write('added_notes.json',new_notes)

external=read(PREP/'external_sources.json')
alt={
 'ebm':('https://www.dcscience.net/sackett-BMJ-1996.pdf','Reproduction du texte original Sackett et al. 1996 ; site BMJ renvoie 403.'),
 'salpetriere':('https://pitiesalpetriere.aphp.fr/chapelle-saint-louis-histoire-de-la-chapelle-de-la-pitie-salpetriere','Publication AP-HP accessible ; ancien PDF 404. Lien de note remplacé.'),
 'madrid':('https://imserso.es/eu/-/informe-anual-2002','Compte rendu annuel 2002 de l’institution espagnole organisatrice : congrès 20–23 mars et Déclaration de Madrid.'),
 'wisc':('https://www.pearsonclinical.fr/wisc-v','Page éditeur et présentation du WISC-V : 5 indices et 10 sous-tests principaux.')
}
for s in external:
    s['independentlyReconsulted']=True
    s['scope']='Pertinence pour la réserve nouvelle du préparateur ; ne remplace pas la ronéo.'
    if s['key'] in alt:s['consultedAlternativeUrl'],s['accessNote']=alt[s['key']]
write('external_source_checks.json',{'preparerReferences':external,'verifierNewPrimaryReferences':[r for n in new_notes for r in n['refs'] if r.get('referenceType')=='external_primary'],'verificationDate':'2026-11-22'})

notes=sum(len(q.get('reviewNotes',[])) for b in approved['banks'].values() for q in b['questions'])
assert notes==104
summary={'questions':274,'items':1370,'sourceDocuments':8,'sourcePages':184,'gradedQuestions':272,'excludedQuestions':2,'independentTextReadQuestions':274,'independentComparedItems':1370,'renderedCropPanels':559,'visualContactSheetsRead':23,'originalNotesPreserved':39,'preparerNewNotesPreserved':58,'verifierNewNotes':7,'totalNotes':104,'referenceRepairs':1,'keysChangedByVerifier':0,'itemTextsChangedByVerifier':0,'cropChangesByVerifier':0,'externalPreparerSourcesReconsulted':34,'sourceDetailsAbsent':752,'siteDetailsBlank':756}
write('summary.json',summary)
report='''# SSH — vérification indépendante finale V6

**Feu vert pour intégration des fichiers approuvés ci-dessous**, avec les limites de provenance et les deux exclusions de notation explicitement conservées.

## Périmètre réellement contrôlé

| Série | QCM | Items | QCM notables |
|---|---:|---:|---:|
| ACC | 38 | 190 | 38 |
| Colle 2 | 79 | 395 | 77 |
| Colle 1 | 78 | 390 | 78 |
| EB blanc | 79 | 395 | 79 |
| Total | 274 | 1 370 | 272 |

J’ai extrait directement et indépendamment les huit PDF fournis (184 pages), puis lu les 274 énoncés, les 1 370 propositions et leurs verdicts/détails, dans douze lots de lecture. `independent_sources.json` conserve les lignes et leurs coordonnées ; `coverage.json` consigne le contrôle de chaque QCM et de chaque item. Le contrôle ne repose pas seulement sur le rapport du préparateur.

Les 272 clés applicables correspondent aux verdicts de la source. Les symboles cochés/croisés de Colle 1 et EB ont été confrontés à leurs clés récapitulatives ; les VRAI/FAUX d’ACC et Colle 2 ont été confrontés à leurs clés. La grille courte de Colle 2 a été extraite séparément : ses 79 entrées correspondent au détail du corrigé, sans rendre applicables les clés des questions 11 et 12 à un autre sujet.

## Résultat de la comparaison systématique

- 1 367 propositions importées correspondent exactement au texte non corrigé après normalisation des espaces, accents et ponctuation. Trois accords grammaticaux sans changement de sens sont acceptés : ACC 5E, 29A et 31D. ACC 3 conserve un écart d’article le/la sans incidence pédagogique.
- Neuf autres différences mineures entre sujet et répétition du corrigé sont documentées ; elles ne changent pas la correspondance des items. Les dix propositions de Colle 2 Q11/Q12 appartiennent en revanche à des questions différentes dans le corrigé.
- Tous les détails applicables correspondent au PDF. Les quatre détails non vides du mauvais couple Colle 2 Q11/Q12 restent exclus. Les 752 absences de détail dans les sources n’ont pas été comblées par une explication inventée ; 746 concernent les 272 QCM assortis du bon corrigé. Le site a 756 champs de détail vides, dont les dix items des deux QCM exclus.
- Le contexte commun ACC 25–26 est présent et fidèle au sujet. Les coupures multipages et le commentaire général ACC 38 ont été vérifiés. Les intitulés des cours suivants n’entrent pas dans les détails ACC 16E et 26E.
- Les 559 panneaux ont tous été rendus et contrôlés pour leurs coordonnées, leur contenu textuel et l’absence d’image vide. J’ai lu visuellement 23 planches ciblées, listées dans `coverage.json` ; je ne présente pas les 559 panneaux comme ayant tous fait l’objet d’une lecture visuelle individuelle.

## Compléments du vérificateur

Sept notes apparaissent uniquement dans la correction, sans modification de clé :

| QCM/item | Réserve ajoutée |
|---|---|
| Colle 2 73B | Composition et durée des mandats du CCNE : ancien cadre dans le détail, comparé à L1412-2 depuis 2021. |
| Colle 2 74C | Déclaration des recherches sur iPS : portée limitée à certains protocoles, avec pouvoirs d’opposition de l’ABM. |
| Colle 2 39A | Distinguer l’achèvement du Projet génome humain en 2003 des travaux T2T de 2022. |
| Colle 1 43E | Responsabilité pour infection nosocomiale : exception de la cause étrangère. |
| Colle 1 55C | Le verdict repose sur les mots « d’autres troubles » ; ne pas en déduire une négation du masquage évoqué par le correcteur. |
| Colle 1 69D | Le sujet compare a posteriori à a posteriori ; intention a priori supposée mais non substituée. |
| EB 37D | Les premiers hôpitaux ne datent pas, en général, de la peste de 1347. |

Les 39 anciennes notes sont inchangées. Les 58 notes du préparateur sont conservées, avec remplacement d’un lien AP-HP 404 par une autre publication de l’AP-HP. Les 34 références primaires mobilisées pour les nouvelles réserves du préparateur ont été reconsultées, au besoin via le texte original ou une publication institutionnelle de remplacement ; `external_source_checks.json` trace ces cas. La réserve sur l’hématome sous-dural de Colle 1 Q70 existait déjà : elle est pertinente et n’a pas été dupliquée. Total : 104 notes.

## Limites et documents encore nécessaires

1. **Colle 2 Q11/Q12 : corrigés correspondants manquants.** Le corrigé au même numéro porte sur d’autres propositions, retrouvées dans EB 54–55. Les deux QCM gardent une réponse vide, sans `answerIsEmpty`, et `correctionMismatch:true` avec un avertissement explicite. Le document non correspondant peut être montré pour transparence, mais ne doit jamais être présenté comme une clé validée de ces sujets.
2. **Colle 1 et EB : originaux institutionnels non remis en page manquants.** Les PDF fournis contiennent déjà des commentaires personnalisés et une présentation reconstruite. La fidélité à ces pièces est vérifiée ; la fidélité de leur transcription initiale à des originaux absents ne peut pas l’être. Demander notamment le texte complet d’EB 6B et la consigne d’origine d’EB 77.
3. **Ronéos et errata du tutorat non fournis.** Les notes signalent des contradictions ou des conventions à faire confirmer. Les références externes ne sont pas présentées comme les ronéos du cours.

`missing.json` liste ces pièces. Aucun autre lot ni fichier du site final n’a été modifié par ce vérificateur. Les contrôles du rendu de l’interface, du masquage avant correction et des profils restent à l’intégrateur.

## Fichiers approuvés

'''
for f in ['approved_reviewed.json','approved_crops.json','coverage.json','issues.json','missing.json']:
    report+=f'- `{f}` — SHA256 `{sha(OUT/f)}`\n'
(OUT/'REPORT.md').write_text(report)
approval={'status':'approved_with_documented_source_limits','explicitApproval':'Feu vert pour intégration ; 272 QCM notables et 2 hors notation, avec les sept notes ajoutées et les limites affichées.','files':{f:{'path':str(OUT/f),'sha256':sha(OUT/f)} for f in ['approved_reviewed.json','approved_crops.json','coverage.json','issues.json','missing.json','REPORT.md']},'summary':summary}
write('approved.json',approval)
print(json.dumps(approval,ensure_ascii=False,indent=2))
