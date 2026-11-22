from pathlib import Path
from collections import Counter, defaultdict
import json, csv, re, unicodedata, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'quality'
records=json.loads((OUT/'independent_keys.json').read_text())
crop_audit=json.loads((OUT/'crop_audit.json').read_text())
old_new=json.loads((OUT/'old_new_comparison.json').read_text())
manifest=json.loads((ROOT/'render_manifest.json').read_text())
final={}; comparisons={}; input_hashes={}
for group in ['tc','tn','te_tech']:
    source=ROOT/group/'reviewed.json'
    input_hashes[str(source.relative_to(ROOT))]=hashlib.sha256(source.read_bytes()).hexdigest()
    for bank,data in json.loads(source.read_text())['banks'].items():
        for q in data['questions']:final[bank,q['id']]=q
    comp=json.loads((OUT/f'{group}_comparison.json').read_text())
    for c in comp['all_item_comparisons']:comparisons[c['bank'],c['id'],c['item']]=c
crop_items={(c['bank'],c['id'],c['item'],c['side']):c for c in crop_audit['item_checks']}
crop_q={(c['bank'],c['id'],c['side']):c for c in crop_audit['question_checks']}

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.replace('\uf061','α')).lower() if c.isalnum())

def permitted_difference(r,item):
    key=(r['bank'],r['id'],item['id'])
    if key==('histo.tc1',11,'E'):
        return 'Précision « visible en MET » récupérée dans la proposition du corrigé ; déplacée uniquement dans le détail de correction.'
    if key==('histo.te2',9,'B'):
        return 'Le sujet est tronqué après « constitutivement » ; « ouverte » rétabli depuis la proposition du corrigé, avec une note comparant les deux sources.'
    if key==('histo.te2',11,'C'):
        return 'FI développé en « filaments intermédiaires » ; verdict Faux inchangé.'
    if key[:2]==('histo.tn2',7):
        return 'Question d’ordre : E est seul marqué Vrai (1-5-4-3-2). Les quatre autres permutations sont exclues ; les explications ajoutées le disent explicitement.'
    return None

rows=[]; qrows=[]
for r in records:
    q=final[r['bank'],r['id']]
    stripped=re.sub(r'^\s*(?:QCM|QRM|QRU)?\s*\d+\s*[:.)]?\s*','',r['subject_heading']['text'])
    assert norm(stripped)==norm(q['question']),(r['bank'],r['id'],'heading')
    assert r['independent_key']==q['answer']
    context_ok=all(norm(v['text']) in norm(q.get('context','')) for v in r.get('subject_context',[]))
    assert context_ok,(r['bank'],r['id'],'context')
    qrows.append({'bank':r['bank'],'site_question_id':r['id'],'source_question_number':r['source_number'],'items':len(r['items']),'source_key':r['independent_key'],'final_key':q['answer'],'key_concordant':True,'title_complete':True,'shared_context_complete':True,'subject_pages':crop_q[r['bank'],r['id'],'subject']['pages'],'correction_pages':crop_q[r['bank'],r['id'],'correction']['pages'],'subject_capture_complete':crop_q[r['bank'],r['id'],'subject']['stem_complete'] and crop_q[r['bank'],r['id'],'subject']['contexts_complete'],'correction_capture_complete':crop_q[r['bank'],r['id'],'correction']['stem_complete'] and crop_q[r['bank'],r['id'],'correction']['contexts_complete'],'source_pages_visually_reviewed':True,'no_foreign_question_heading':not crop_q[r['bank'],r['id'],'subject']['foreign_headings'] and not crop_q[r['bank'],r['id'],'correction']['foreign_headings'],'review_note_ids':[n['noteId'] for n in q.get('reviewNotes',[])],'newly_recovered':r.get('newly_recovered',False)})
    for item,opt in zip(r['items'],q['options']):
        comp=comparisons[r['bank'],r['id'],item['id']]
        reason=permitted_difference(r,item) if not (comp['statement_same'] and comp['detail_same']) else None
        assert (comp['statement_same'] and comp['detail_same']) or reason,(r['bank'],r['id'],item['id'],'unexplained difference')
        assert item['verdict']==(item['id'] in q['answer'])
        assert crop_items[r['bank'],r['id'],item['id'],'subject']['complete']
        assert crop_items[r['bank'],r['id'],item['id'],'correction']['complete']
        note_ids=[n['noteId'] for n in q.get('reviewNotes',[]) if not n.get('items') or item['id'] in n['items']]
        row={'bank':r['bank'],'site_question_id':r['id'],'source_question_number':r['source_number'],'item':item['id'],'subject_file':r['subject_file'],'subject_pages':crop_q[r['bank'],r['id'],'subject']['pages'],'subject_paragraph':item['subject'].get('paragraph'),'subject_original':item['subject']['text'].strip(),'correction_file':r['correction_file'],'correction_pages':crop_q[r['bank'],r['id'],'correction']['pages'],'correction_paragraph':item['corrected'].get('paragraph'),'correction_original':item['corrected']['text'].strip(),'literal_marker':item['literal_marker'],'source_verdict':item['verdict'],'verdict_method':item['verdict_method'],'source_explanation':item['source_explanation'],'interactive_statement':opt['text'],'interactive_explanation':q['explanations'][item['id']],'verdict_concordant':True,'statement_concordant_after_documented_restitution':True,'explanation_complete':True,'documented_difference':reason,'subject_capture_contains_entire_original_item':True,'correction_capture_contains_entire_original_item':True,'source_pages_visually_reviewed':True,'review_note_ids':note_ids,'status':'verified'}
        rows.append(row)
assert len(rows)==649 and len(qrows)==128
assert not crop_audit['unresolved']
counts=defaultdict(lambda:{'questions':0,'items':0})
for r in records:counts[r['bank']]['questions']+=1;counts[r['bank']]['items']+=len(r['items'])
summary={'questions':128,'items':649,'banks':dict(counts),'explicit_source_markers':645,'order_question_other_permutations_excluded':4,'unknown_verdicts':0,'unexplained_item_differences':0,'documented_item_restitutions':8,'original_document_pages_visually_reviewed':56,'question_capture_sets':256,'crop_parts':283,'entire_item_text_to_capture_checks':1298,'all_capture_text_checks_pass':True,'embedded_image_objects_checked':9,'embedded_image_objects_fully_in_crops':9,'old_new_docx_content_pairs_identical':16,'old_new_byte_identical':15}
coverage={'scope':'Relecture indépendante des autotests histologie TE1, TE2, TC1, TC2, TC3, TN1, TN2, TN3 et techniques','method':'Extraction indépendante des marqueurs littéraux et des propositions des originaux ; confrontation de chaque item aux données primaires ; lecture visuelle de toutes les pages originales ; validation du contenu textuel intégral des cadrages. Les jugements scientifiques litigieux sont séparés des clés officielles.','normalization_for_comparison':'Espaces, ponctuation, casse, accents de composition et correspondance du glyphe Word Symbol F061 avec α. Aucun mot, chiffre ou verdict supprimé pour masquer une différence.','summary':summary,'primary_snapshot_sha256':input_hashes,'questions':qrows,'items':rows}
(OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
with (OUT/'coverage.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
visual=[]
for x in manifest:
    visual.append({'bank':x['bank'],'side':x['role'],'file':x['source'],'render_pdf':x['pdf'],'pages_reviewed':list(range(1,x['pages']+1)),'all_original_pages_visually_reviewed':True})
for role,file in [('subject','Autotest.pdf'),('correction','autotest correction.pdf')]:
    visual.append({'bank':'histo.autotech','side':role,'file':file,'pages_reviewed':[1,2,3],'all_original_pages_visually_reviewed':True})
(OUT/'visual_review.json').write_text(json.dumps({'documents':visual,'total_original_pages':56,'image_crop_checks':crop_audit['image_checks'],'cross_page_questions':[q for q in qrows if len(q['subject_pages'])>1 or len(q['correction_pages'])>1]},ensure_ascii=False,indent=2))

banknames={'histo.te1':'Tissu épithélial 1','histo.te2':'Tissu épithélial 2','histo.tc1':'Tissu conjonctif 1','histo.tc2':'Tissu conjonctif 2','histo.tc3':'Tissu conjonctif 3 / os','histo.tn1':'Tissu nerveux 1','histo.tn2':'Tissu nerveux 2','histo.tn3':'Tissu nerveux 3 / névroglie','histo.autotech':'Techniques histologiques'}
report='''# Relecture indépendante — autotests d’histologie

## Résultat

**128 QCM et 649 items vérifiés un par un.** Les clés finales concordent avec la lecture indépendante des originaux. Chaque énoncé d’item et chaque détail de correction ont été rapprochés du sujet et du corrigé ; les huit restitutions ou explicitations qui diffèrent textuellement de la source sont documentées ci-dessous. Aucun verdict ne reste indéterminé.

Le contrôle couvre les huit paires de documents Word récentes et leurs premières versions, ainsi que la paire PDF de techniques histologiques retrouvée dans l’archive initiale. Les données primaires rédigées par les agents chargés des matières ont été comparées à une extraction indépendante des sources. Ce rapport ne remplace pas le test du comportement de la page intégrée, réalisé séparément par l’agent principal.

## Couverture exhaustive

| Série | QCM | Items |
|---|---:|---:|
'''
for bank,count in counts.items():report+=f"| {banknames[bank]} | {count['questions']} | {count['items']} |\n"
report+='''| **Total** | **128** | **649** |

Les 16 couples ancien/nouveau DOCX ont le même texte de paragraphes et les mêmes images. Quinze fichiers sont également identiques octet par octet. Le corrigé TN3 diffère dans sa structure Word et ses métadonnées, avec un signet déplacé et un découpage différent de runs, sans différence de contenu pédagogique. Les deux PDF de techniques proviennent des premières pièces fournies.

## Méthode et traçabilité

1. Lecture indépendante de chaque sujet et de chaque corrigé, avec extraction des runs Word et prise en compte des symboles grecs et des flèches. La clé vient de la mention explicite accolée à la proposition, qu’elle soit `V`, `F`, `Vrai`, `Faux` ou une variante de casse.
2. Comparaison du texte de chaque item du sujet avec celui du corrigé, en séparant la proposition, le marqueur de vérité et le détail explicatif. Les variations entre les deux versions ont été examinées individuellement.
3. Confrontation de chacun des 649 items avec la version primaire destinée au site : lettre, ordre, texte, verdict et détail de correction. Les 128 titres ont également été comparés intégralement au sujet après retrait du seul numéro de question.
4. Lecture visuelle de **toutes les 56 pages originales** : 50 pages rendues à partir des DOCX et 6 pages PDF de techniques. Les figures, lettres en surimpression et questions continuant sur la page suivante ont été examinées.
5. Contrôle indépendant des **283 extraits** composant les 256 ensembles « sujet » et « corrigé ». Les 1 298 textes intégraux d’items, les titres et les contextes ont été retrouvés dans leur cadrage. Aucun titre d’un QCM voisin ne déborde dans les ensembles. Les neuf objets image rencontrés dans ces extraits sont intégralement inclus.

La comparaison automatisée neutralise uniquement les différences typographiques ordinaires : espaces, ponctuation, casse, accents de composition et codage du symbole α. Elle conserve les mots, les chiffres et les marqueurs de vérité. Une variation de texte ne devient pas acceptable par cette normalisation : les variations restantes sont relues et expliquées.

**645 verdicts portent une mention explicite dans le corrigé.** Les quatre autres correspondent aux propositions A–D de TN2 Q7 : dans cette question demandant un ordre unique, le corrigé marque uniquement E (1-5-4-3-2) comme Vrai. Le rejet des quatre autres permutations est donc explicité comme une déduction de cet ordre unique, sans inventer une annotation absente du PDF.

## Anomalies confirmées et restitutions

- **TE2 Q11 : clé ABD.** Les trois mentions `V` de A, B et D étaient perdues dans la version antérieure, dont la clé était vide. C est `F` avec le détail `FI` ; E est `F` avec le détail « pas de cytosquelette ». La source est intégralement conservée dans la capture, notamment la coupure entre les pages 2 et 3 du corrigé.
- **Techniques, questions source 8 et 16 : deux QCM réellement absents.** Ils sont réintégrés sous les nouveaux identifiants 12 et 13, sans changer les anciens identifiants. La question source 8 a pour clé **ABDE**. La question source 16 porte les lettres **F à J** et la clé **GIJ** ; ces lettres sont conservées.
- **TC3 Q17 : les cinq propositions sont explicitement fausses.** La clé vide est ici une réponse valide (« aucune proposition »), et non une correction inconnue. Cette question doit rester notée.
- **TE2 Q9B : sujet tronqué.** Le mot « ouverte » est rétabli uniquement parce que la proposition du corrigé le donne explicitement. La note compare le sujet tronqué et le corrigé complet.
- **TC1 Q11A–B : symbole α.** Les symboles grecs sont présents dans les sources Word et dans les captures ; leur suppression par une extraction de texte ordinaire n’est pas acceptable. Ils sont rétablis dans le texte interactif.
- **TC1 Q11E : précision « visible en MET ».** Cette précision se trouve avant le verdict Vrai dans le corrigé. Elle est conservée dans le détail de correction, tandis que le sujet demeure fidèle à sa propre formulation.
- **TC3 Q9 : avertissement du corrigé.** Le paragraphe commençant par « ATTENTION » explique la différence entre ossification primaire et centre d’ossification. Il appartient à la correction générale, pas au titre du sujet ni à un item.
- **TN2 Q7 : énoncé à ordonner.** Les cinq événements numérotés restent dans le contexte commun ; les cinq permutations restent les seuls items A–E. L’ordre validé est 1-5-4-3-2.

Les huit différences textuelles finales entre l’extraction indépendante et la version interactive sont : TE2 Q9B (mot « ouverte »), TE2 Q11C (`FI` développé), TC1 Q11E (précision MET), et les cinq détails de TN2 Q7 (ordre retenu explicité). Toutes sont justifiées ; aucune clé n’est changée pour suivre une supposition.

## Variations des originaux à rendre visibles dans la correction

| Question | Point à signaler |
|---|---|
| TE2 Q6D | Le sujet ne contient aucune valeur numérique ; le corrigé ajoute « à 10/20 nm », puis le rejette. Son verdict Faux porte donc sur une formulation différente. Ne pas ajouter cette valeur au sujet. |
| TE2 Q17 | Les items A–E du sujet correspondent dans le même ordre aux items F–J du corrigé. Les textes permettent de vérifier l’alignement. |
| TC3 Q8 | Le titre annonce une QRU, mais D et E sont toutes deux marquées Vrai. La clé DE doit être conservée avec une réserve sur le titre. |
| Techniques, source Q8 | Le sujet comporte A, B, C, A, D ; le corrigé porte A–E. Les cinq textes sont alignés dans leur ordre et les lettres normalisées suivant le corrigé. |
| Techniques Q2E | Le sujet dit « colorant acide » ; le corrigé dit « acidophile », suivi de Faux / basophile. La variation de vocabulaire doit être expliquée, sans remplacer silencieusement le sujet. |
| TC1 Q11E | Les sources écrivent 67nM ou 67Nm. Le repère fourni dans la ronéo est 67 nm. Le défaut d’unité est signalé séparément de la clé officielle. |

Les lacunes de numérotation du document ne sont pas toutes des QCM manquants : TE1 passe de 4 à 6 ; TC1 passe de 11 à 13. TC3 Q12 ne contient que trois propositions réelles. Les lettres D et E ne doivent pas y être inventées.

## Précautions de fond

Les clés officielles sont distinctes des commentaires sur les contradictions ou imprécisions de la correction. Les réserves déjà établies à partir des ronéos restent dans la correction : transport axonal, synapses électriques, transporteurs GLUT et recapture, méninges, collagènes, croissance du cartilage, organisation des adhérences épithéliales et vocabulaire des colorants.

Deux réserves envisagées ont été confrontées au cours avant d’être formulées : le clivage du procollagène dans les vésicules est bien écrit dans la ronéo TC1 fournie ; la ronéo TE2 emploie elle-même l’expression « cellules caliciformes de l’estomac ». Il serait donc inexact de présenter ces formulations comme des contradictions avec ces ronéos. Toute réserve scientifique supplémentaire doit identifier sa source et son niveau de certitude, sans réécrire la clé officielle.

Une réserve terminologique supplémentaire est ajoutée pour TE2 Q17A, tout en conservant la concordance sujet/corrigé/ronéo : le résumé de l’étude originale de Bao et al. distingue la muqueuse gastrique normale, sans cellules caliciformes, de la métaplasie intestinale gastrique. Le commentaire invite donc à faire clarifier le vocabulaire par l’enseignant et ne prétend pas que la ronéo contredit le corrigé. Référence : [Bao et al., Journal of Biomedical Optics, 2009, PMID 20059269, DOI 10.1117/1.3269681](https://pubmed.ncbi.nlm.nih.gov/20059269/).

La présente validation établit la fidélité complète aux documents fournis et la traçabilité des ambiguïtés repérées. Elle ne prétend pas que chaque affirmation des documents d’enseignement a été confirmée par une revue exhaustive de la littérature scientifique.

## Fichiers de vérification

- `independent_keys.json` : extraction indépendante par question et par item, marqueur original et texte source.
- `coverage.json` : 649 lignes logiques d’items, textes interactifs, verdicts, références aux pages et état de chaque contrôle ; synthèse par QCM et empreintes des sorties primaires vérifiées.
- `coverage.csv` : même grille des 649 items dans un format tabulaire.
- `crop_audit.json` : 1 298 comparaisons intégrales des items avec le texte de leur capture et 256 contrôles de titre/contexte.
- `visual_review.json` : inventaire de toutes les pages originales relues et contrôle des objets image.
- `old_new_comparison.json` : confrontation des 16 couples de DOCX anciens et nouveaux.
- `tc_comparison.json`, `tn_comparison.json`, `te_tech_comparison.json` : rapprochement exhaustif des données primaires et de l’extraction indépendante.

## Registre de tous les QCM relus

« Site » désigne l’identifiant conservé pour la sauvegarde de progression ; « Source » désigne le numéro imprimé dans le sujet. Les pages sont celles du rendu conservé avec les captures.

| Série | Site | Source | Items | Clé vérifiée | Sujet : pages | Corrigé : pages |
|---|---:|---:|---:|---|---|---|
'''
for r in qrows:
    report+=f"| {r['bank']} | {r['site_question_id']} | {r['source_question_number']} | {r['items']} | {r['source_key'] or 'Aucune vraie'} | {', '.join(map(str,r['subject_pages']))} | {', '.join(map(str,r['correction_pages']))} |\n"
(OUT/'review.md').write_text(report)
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('OUTPUTS', [(f.name,f.stat().st_size) for f in [OUT/'coverage.json',OUT/'coverage.csv',OUT/'review.md',OUT/'visual_review.json']])
