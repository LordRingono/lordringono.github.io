"""Build the user-facing release report from the approved, integrated site."""
from pathlib import Path
import json, re, shutil

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent.parent/'output'
SITE=OUT/'site'
NAMES={'ssh':'SSH','histologie':'Histologie','biocell':'Biologie cellulaire','embryologie':'Embryologie','biomol':'Biologie moléculaire','biochimie':'Biochimie','chimie':'Chimie','biostat':'Biostatistiques','pharmaco':'Pharmacologie'}
ORDER=['ssh','biomol','biochimie','chimie','biostat','pharmaco','histologie','biocell','embryologie']

def load(p):return json.loads(Path(p).read_text())
def clean(v):return re.sub(r'\s+',' ',str(v or '')).strip().replace('|','\\|')
def num(n):return f'{n:,}'.replace(',','\u202f')
def qref(bank,q):
    label=EXAMS[bank]['label']
    year=str(q.get('year') or '')
    if year and year not in label and year.replace('-','–') not in label:
        session='session non précisée' if q.get('pharmaReviewed') and year in ['2018-2019','2019-2020'] else q.get('session','')
        label+=' · '+year.replace('-','–')+(' · '+session if session else '')
    original=q.get('printedSourceNumber') or q.get('sourceNumber') or q.get('sourceQuestionNumber')
    extra=f' ; n° source {original}' if original and str(original)!=str(q['id']) else ''
    return f"{label} — QCM {q['id']}{extra}"
def ids(v):
    vals=sorted(set(v));out=[]
    for n in vals:
        if not out or n!=out[-1][-1]+1:out.append([n])
        else:out[-1].append(n)
    return ', '.join(str(a[0]) if len(a)==1 else f'{a[0]}–{a[-1]}' for a in out)
def source(copy):
    if not copy or not copy.get('captures'):return 'Original correspondant absent'
    documents=copy.get('documents') or [copy]
    parts=[]
    for document in documents:
        pages=sorted(set(c['page'] for c in copy['captures'] if c.get('pdf')==document.get('pdf')))
        if not pages:pages=sorted(set(c['page'] for c in copy['captures']))
        parts.append(clean(document.get('file','Document fourni'))+' ; p. '+ids(pages))
    return ' / '.join(parts)

if __name__=='__main__':
    EXAMS=load(ROOT/'current_exams.json')
    summary=load(ROOT/'build_summary.json');signoffs=load(ROOT/'signoffs.json')
    runtime=load(ROOT/'runtime_report.json');integrity=load(ROOT/'integrity_report.json')
    assert set(signoffs)==set(ORDER) and runtime['result']=='PASS' and integrity['result']=='PASS'
    roster=load(ROOT/'roster.json');owner={b:s for s in ORDER for b in roster[s]['banks']}
    questions=[(b,q) for b,e in EXAMS.items() for q in e['questions']]
    notes=sum(len(q.get('reviewNotes',[])) for _,q in questions)
    scored=sum(bool(q.get('answer')) or q.get('answerIsEmpty') is True for _,q in questions)
    mismatch=[(b,q) for b,q in questions if q['sourceCopies']['correction'].get('mismatch')]
    missing_sub=[(b,q) for b,q in questions if q['sourceCopies']['subject'].get('missing')]
    missing_cor=[(b,q) for b,q in questions if q['sourceCopies']['correction'].get('missing')]
    annotated=[(b,q) for b,q in questions if q['sourceCopies']['subject'].get('afterCorrection')]
    missing_all={}
    for s in ORDER:
        p=ROOT/s/'verify/missing.json'
        if not p.exists():p=ROOT/s/'prepare/missing.json'
        missing_all[s]=load(p)
    (SITE/'audit/revision_v6/documents_et_arbitrages_manquants.json').write_text(json.dumps(missing_all,ensure_ascii=False,indent=2))

    lines=['# Vérification complète du site PASS — version 6','',
      f"**{num(summary['questionsAfter'])} QCM/fiches, {num(summary['items'])} items ou choix et {summary['banks']} banques.** Les neuf matières ont reçu une préparation puis une vérification documentaire par un autre agent. {num(scored)} QCM sont notables ; {len(questions)-scored} restent hors note, dont un exercice sans options A–E. Le compte des choix inclut les quinze lettres de codage de trois questions numériques en biostatistiques.",'',
      'Le contrôle porte sur les documents disponibles, anciens et récents. Les limites des originaux sont conservées et documentées ; la présence d’une ligne dans le tableau ne certifie pas l’existence d’un sujet non corrigé pour chaque question.','',
      '## Couverture et binômes','',
      '| Matière | QCM/fiches | Items/choix | Notables | Hors note | Préparation / vérification |',
      '|---|---:|---:|---:|---:|---|']
    for s in ORDER:
        st=summary['subjects'][s];sig=signoffs[s]
        actors=sig['preparer'].replace('/root/','')+' / '+sig['verifier'].replace('/root/','')
        lines.append(f"| {NAMES[s]} | {num(st['questions'])} | {num(st['items'])} | {num(st['graded'])} | {st['ungraded']} | {actors.replace('/root','agent principal')} |")
    lines+=['','Les rapports distincts des préparateurs et vérificateurs sont inclus sous `audit/revision_v6/matieres/`. Les signatures portent sur les empreintes exactes des données intégrées.','',
      '## Accès aux preuves','',
      f"- {num(len(questions)-len(missing_sub))} QCM disposent de copies du sujet fourni ; {len(annotated)} de ces copies sont différées car les originaux portent déjà des annotations.",
      f"- {num(len(questions)-len(missing_cor)-len(mismatch))} QCM disposent de copies du corrigé correspondant. Pour {len(mismatch)} autres, le document de correction fourni est montré avec une mention explicite d’énoncé différent ; {len(missing_cor)} corrigé correspondant est absent.",
      f"- {num(len(missing_sub))} QCM n’ont pas de copie exploitable d’un sujet non corrigé : ces manques sont indiqués dans les menus et regroupés dans la liste des pièces à compléter.",
      f"- {num(notes)} remarques de vérification, anciennes conservées et nouvelles, se trouvent après correction. Ce nombre inclut les conflits documentaires et les précisions de cours ; il ne représente pas un nombre d’erreurs scientifiques certaines.",'',
      'La liste exacte des manques et arbitrages est jointe dans **Documents_a_completer_PASS_v6.md**. Les références relatives de ce rapport sont à lire depuis le dossier de l’archive extraite.','',
      (ROOT/'release_notes_sections.md').read_text(),'',
      '## Contrôles de l’intégration','',
      f"Le script réel du site a été exécuté pour les {len(runtime['banks'])} banques. Les états avant/après correction, les menus de sources, le barème 10/5/2/0 et ses pondérations, les réponses entièrement fausses et l’exercice sans options ont été vérifiés. Les {runtime['profiles']} états de profils rechargés ont été comparés aux sauvegardes.",'',
      f"Les migrations de réponses ont été exercées sur {runtime.get('migrationProfiles',0)} profils de banques concernées, avec contrôle de la correspondance des lettres, de la remise en attente des seules questions réparées et de l’absence de second remappage au rechargement.",'',
      'Les fichiers locaux référencés ont été contrôlés, les nouvelles captures décodées et un échantillon de rendus comparé aux pixels du PDF. Les documents et assets de la version précédente demeurent intacts, à l’exception de la page principale expressément mise à jour.','',
      'Ces contrôles fonctionnels utilisent le JavaScript réel avec un adaptateur DOM. Ils ne sont pas présentés comme une capture d’écran du site dans un navigateur graphique. Les inspections visuelles documentaires sont détaillées dans les rapports par matière.','',
      '## Où retrouver le détail','']
    for s in ORDER:
        lines.append(f"- **{NAMES[s]}** : [vérification indépendante](audit/revision_v6/matieres/{s}/verify/REPORT.md), données approuvées et couverture par QCM/item dans le même dossier.")
    lines+=['','Les fichiers `statistiques.json`, `modifications.json`, `approbations_binomes.json`, `captures.json` et `documents.json` sous `audit/revision_v6/` permettent de retrouver les modifications et leurs preuves.','']
    report='\n'.join(lines)
    for dest in [OUT/'Verification_complete_PASS_v6.md',SITE/'Verification_complete_PASS_v6.md']:dest.write_text(report)

    lines=['# Documents et arbitrages à compléter — PASS V6','',
      'Les originaux présents ont déjà été utilisés. Les demandes ci-dessous portent sur des absences précises, des fichiers annotés ou des contradictions que les documents disponibles ne permettent pas d’arbitrer. Les nombres de QCM désignent les identifiants affichés dans le site, sauf mention d’un numéro source.','',
      '## Priorité 1 — sujets non corrigés absents','',
      '| Ensemble | QCM concernés | Nombre | Pièce demandée |','|---|---|---:|---|']
    bybank={}
    for b,q in missing_sub:bybank.setdefault(b,[]).append(q)
    for b,qs in bybank.items():
        lines.append(f"| {clean(EXAMS[b]['label'])} | {ids([q['id'] for q in qs])} | {len(qs)} | Sujet non corrigé complet, avec figures et consignes communes |")
    lines+=['','## Priorité 2 — corrections absentes ou ne correspondant pas au sujet','',
      '| QCM | Problème |','|---|---|']
    for b,q in missing_cor+mismatch:
        cp=q['sourceCopies']['correction'];why=cp.get('reason') or cp.get('note') or 'Le corrigé porte un autre énoncé.'
        lines.append(f'| {clean(qref(b,q))} | {clean(why)} |')
    lines+=['','## Clés à faire confirmer officiellement','',
      'Ces questions restent hors note. Il faut un erratum, un corrigé harmonisé ou une confirmation du tutorat/enseignant portant sur la même version du sujet. Les copies déjà présentes permettent de voir les divergences.','',
      '| Matière | Question dans le site | Référence du corrigé fourni |','|---|---|---|']
    for s in ORDER:
        for b,q in questions:
            if owner[b]!=s or bool(q.get('answer')) or q.get('answerIsEmpty') is True or not q['options']:continue
            lines.append(f"| {NAMES[s]} | {clean(qref(b,q))} | {source(q['sourceCopies']['correction'])} |")
    lines+=['','## Versions vierges et figures à compléter','',
      'Les copies suivantes sont protégées jusqu’à la correction parce que le document fourni contient déjà une annotation. Une version réellement non annotée permettrait de les afficher pendant l’entraînement.','',
      '| Question | Original concerné |','|---|---|']
    for b,q in annotated:lines.append(f"| {clean(qref(b,q))} | {source(q['sourceCopies']['subject'])} |")
    lines+=['',
      '- **Histologie, autotest TN1 Q13** : si possible, fournir la version complète du schéma explicatif de myélinisation. Les légendes de gauche sont déjà rognées dans l’EMF inclus dans le Word original ; la capture reproduit ce défaut sans inventer le texte manquant.',
      '- **SSH, colle 1 et EB blanc** : fournir les sujets et corrigés officiels avant remise en page, si disponibles. Les pièces actuellement fournies contiennent déjà des commentaires ; en particulier, EB Q6B et la consigne initiale de Q77 appellent une confirmation.','',
      '## Biologie moléculaire — formulations et clés ambiguës dans les originaux','',
      'Les 46 PDF sont disponibles : il n’est pas nécessaire de les renvoyer à l’identique. Les compléments attendus sont les passages rectifiés ou les arbitrages suivants.','']
    bm=missing_all['biomol']
    for row in bm.get('originalContentToClarify',[]):
        b=row['bank'];label=EXAMS[b]['label'];detail=row.get('detail') or row.get('reason') or row.get('request') or ''
        item=' (consigne)' if row.get('item')=='stem' else ' '+str(row['item']) if row.get('item') else ''
        lines.append(f"- **{clean(label)}, QCM {row['id']}{item}** : {clean(detail)}")
    for row in bm.get('ambiguousOfficialKeys',[]):
        lines.append(f"- **{clean(EXAMS[row['bank']]['label'])}, QCM {row['id']}** : préciser la clé officielle « {clean(row.get('key'))} ».")
    lines+=['','## Ronéos utiles aux arbitrages scientifiques','',
      '- **Pharmacologie** : chapitres spécialisés des quinze thèmes, en priorité ceux associés aux remarques. Les documents de droit et de cycle de vie déjà disponibles ont été utilisés ; ils ne remplacent pas les cours spécialisés de PK/PD, cibles, iatrogénie, BUM, sources naturelles, galénique, conception/identification, développement clinique, biotechnologies et analyse/contrôle.',
      '- **Biostatistiques** : estimation, tests, régression, évaluation diagnostique et essais cliniques. Les sujets et corrigés sont disponibles, mais aucune ronéo UE3 ne l’est.',
      '- **Biochimie** : protéines, enzymologie et métabolisme. Les six ronéos disponibles de glucides/lipides ont déjà été consultées.',
      '- **Chimie** : stéréochimie, réactivité des carbonyles, substitutions et éliminations, ainsi que les errata des sujets signalés. La ronéo d’atomistique disponible a déjà été utilisée.',
      '- **Biologie cellulaire** : cours CM10 mort/sénescence pour les formulations litigieuses sur les cytokines et p16/cycline D ; versions harmonisées des autotests CM6 Q7 et CM10 Q1.',
      '- **SSH** : ronéos et errata portant sur les conventions de cours et les données datées signalées après correction.',
      '- **Histologie, embryologie et biomol** : errata ou passages de cours précis des questions figurant dans la table des clés à confirmer.','',
      '## Années non présentes et séries distinctes','',
      'Pour compléter les annales à partir de 2015, les séries 2015–2016, 2016–2017 et 2017–2018 absentes des ensembles de pharmacologie/chimie analysés doivent être fournies. Elles n’ont pas été déclarées vérifiées ni ajoutées sans document. Les recherches d’exhaustivité se limitent aux séries effectivement fournies.','',
      'Le rapport d’embryologie identifie aussi une série distincte de quinze QCM 2025–2026 dans la compilation ; elle est recensée et n’est pas présentée comme importée dans la banque thématique existante. Les réparations de cette livraison restaurent les omissions prouvées au sein des séries déjà représentées.','',
      'La liste documentaire structurée complète, y compris les sources déjà recherchées et les réserves par item, est incluse dans `audit/revision_v6/documents_et_arbitrages_manquants.json`.','']
    missing_report='\n'.join(lines)
    for dest in [OUT/'Documents_a_completer_PASS_v6.md',SITE/'Documents_a_completer_PASS_v6.md']:dest.write_text(missing_report)
    readme='''# Site PASS — version 6\n\n## Installation des deux archives\n\n1. Extraire **Site_revision_PASS_UE1_UE2_UE3_UE4_UE5_annales.zip**.\n2. Extraire **Sources_originales_PASS_v6.zip** dans le même dossier. Si deux dossiers séparés ont été créés, déplacer le dossier `sources` du second à côté d’`index.html` dans le premier.\n3. Ouvrir **index.html**. Les dossiers `sources` et `static` doivent rester à côté de la page.\n\nLes deux ZIP réunissent le site complet et tous ses documents. Aucun logiciel d’assemblage d’archives fractionnées n’est nécessaire.\n\n## Rapports\n\n- `Verification_complete_PASS_v6.md` : résultats de la double vérification par matière, modifications, portée et tests.\n- `Documents_a_completer_PASS_v6.md` : originaux manquants et arbitrages à demander.\n- `audit/revision_v6/` : preuves détaillées, rapports des binômes, données et empreintes.\n\nLes menus des copies restent fermés. Les corrigés et les remarques se lisent après validation. L’interrupteur conserve deux progressions indépendantes. Les réponses sont enregistrées localement par le navigateur : conserver le même navigateur et le même emplacement pour retrouver la progression existante.\n\nLa documentation plus ancienne du dossier est conservée pour l’historique ; les deux rapports V6 ci-dessus décrivent la livraison actuelle.\n'''
    (SITE/'LIRE_MOI_V6.md').write_text(readme)
    print(json.dumps({'questions':len(questions),'items':summary['items'],'scored':scored,'ungraded':len(questions)-scored,'notes':notes,'subjectMissing':len(missing_sub),'correctionMissing':len(missing_cor),'correctionMismatch':len(mismatch),'subjectAnnotated':len(annotated)},ensure_ascii=False))
