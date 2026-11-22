"""Write the current delivery report and preserve the earlier integration audit."""
from pathlib import Path
import collections, csv, json, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SITE=ROOT/'output/site'
AUDIT=SITE/'audit'

def read(name):return json.loads((HERE/name).read_text())
def escape(value):return str(value).replace('|','\\|').replace('\n',' ')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(escape(x) for x in row)+' |' for row in rows])
def graded(q):return bool(q.get('answer')) or bool(q.get('answerIsEmpty'))
def reference(q,bank=None):
    if bank and bank['ue']!='ue4':return f"{bank['seriesLabel'].replace('-','–')} · Q{q.get('printedSourceNumber') or q['sourceNumber']}"
    return f"{str(q['year']).replace('-','–')} · {q['session']} · Q{q['sourceNumber']}"

def main():
    data=read('data_audit.json');logic=read('logic_checks.json');build=read('build_manifest.json');exams=read('exams_v3.json');mapping=read('question_map.json')
    assert data['status']==logic['result']=='PASS'
    qlist=[q for b in exams.values() if b['ue']=='ue4' for q in b['questions']]
    qmap={q['sourceId']:q for q in qlist}
    reviews={r['sourceId']:r for lot in ['recent','middle','older'] for r in read(lot+'/reviews.json')}
    notes=[(q,n) for q in qlist for n in q['reviewNotes']]
    history=AUDIT/'historique_2026-11-21';history.mkdir(exist_ok=True)
    for old,new in [('baseline_report.md','CONTROLE_ANNALES.md'),('baseline_maintenance.md','MAINTENANCE.md'),('baseline_readme.md','LIRE_DABORD.md'),('baseline_inventory.csv','inventaire_838_qcm.csv'),('baseline_files.json','fichiers_sha256.json')]:shutil.copy2(HERE/old,history/new)
    trace=AUDIT/'pharmaco_2026-11-22';trace.mkdir(exist_ok=True)
    # Enough immutable inputs and instructions to reproduce this targeted revision.
    for name in ['CONTRACT.md','themes.json','baseline_index.html','baseline_exams.json','questions_v2.json','baseline_inventory.csv','baseline_files.json','build_pharma.py','pharma_runtime.js','pharma_style.css','test_pharma.cjs','audit_pharma.py','write_report.py','patch_decisions.json','warning_coverage.json','build_manifest.json','question_map.json','data_audit.json','logic_checks.json']:
        shutil.copy2(HERE/name,trace/name)
    for lot in ['recent','middle','older']:
        dest=trace/lot;dest.mkdir(exist_ok=True)
        for name in ['reviews.json','review.md','validation.json','audit.json','text_verification.json','assets_manifest.json','independent_q5_check.md']:
            if (HERE/lot/name).exists():shutil.copy2(HERE/lot/name,dest/name)
    theme_rows=[]
    for theme,label in read('themes.json'):
        qs=[q for q in qlist if mapping[q['sourceId']]['themeId']==theme]
        theme_rows.append([label,len(qs),sum(graded(q) for q in qs),sum(not graded(q) for q in qs),sum(bool(q['reviewNotes']) for q in qs)])
    changes=collections.defaultdict(list)
    for patch in build['appliedPatches']:changes[patch['sourceId']].append(patch['field'])
    changes_rows=[[reference(qmap[sid]),', '.join(fields),qmap[sid]['subjectPage'],qmap[sid]['correctionPage']] for sid,fields in changes.items()]
    subjects=collections.defaultdict(list)
    for q in qlist:subjects[(q['year'],q['session'])].append(q)
    subject_rows=[]
    for (year,session),qs in sorted(subjects.items(),reverse=True):
        subject_rows.append([year.replace('-','–'),session,len(qs),len(qs)*5,min(q['subjectPage'] for q in qs),max(q['sourceEndPage'] for q in qs),sum(bool(q['reviewNotes']) for q in qs)])
    ungraded_rows=[]
    for bank,b in exams.items():
        if b['ue'] not in {'ue2c','ue3','ue4'}:continue
        for q in b['questions']:
            if graded(q):continue
            ungraded_rows.append([b['ue'].upper(),reference(q,b),q.get('category',''),q.get('subjectPage',''),q.get('correctionPage',''),q.get('warning','')])
    report=f'''# Site PASS — pharmacologie reclassée et relue

Mise à jour du **22 novembre 2026**. Cette version remplace le classement annuel de pharmacologie par les quinze thèmes de la nomenclature fournie.

## Résultat

Le site complet contient **{data['total_site_qcm']} QCM dans {data['total_site_banks']} banques**. La pharmacologie représente **336 QCM, 1680 propositions A–E et 14 sujets**. Elle est désormais organisée en **15 séries thématiques**, avec toutes les années réunies dans chaque thème. L’année, la session, le numéro original et les pages restent des références discrètes sous la consigne.

Les **202 banques et 2452 QCM hors UE4** sont strictement identiques à la version précédente. Cela inclut l’UE1, l’UE5, la biomol/ED en UE2, la biochimie et les biostatistiques. Les images et PDF déjà livrés sont conservés octet pour octet. Aucun QCM n’a été ajouté ou supprimé pendant ce reclassement ; aucun QCM antérieur à 2015 n’est introduit. Les sujets de pharmacologie disponibles vont de 2018–2019 à 2025–2026.

**{data['questions_with_new_notes']} QCM comportent {data['new_note_count']} commentaires de relecture.** Ils indiquent les items litigieux, le motif précis et la ronéo à consulter. Ils apparaissent seulement après correction, dans un petit encadré « À vérifier dans la ronéo ». Les réserves préexistantes restent documentées ; quand un nouveau commentaire reprend déjà leur motif, elles ne sont pas répétées dans l’interface.

## Classement demandé

Un QCM reste indivisible : sa consigne, ses cinq propositions, ses figures et sa correction sont conservées ensemble. Lorsqu’il couvre plusieurs domaines, le thème retenu correspond à la compétence principale ; le motif figure dans l’inventaire complet. Les thèmes et leur ordre reprennent la capture fournie.

{table(['Thème','QCM','Notés','Hors note','Avec commentaire'],theme_rows)}

Les sélecteurs d’année et de série annuelle ont été retirés de la navigation UE4. La sélection d’un thème ouvre directement toutes ses annales. Les questions restent ordonnées à l’intérieur du thème et peuvent être recherchées/filtrées comme auparavant.

## Réparations de restitution

### Mauvais appariement du Q5, session 2 de 2023–2024

Le sujet p790 pose un QCM de pharmacocinétique. La grille p794 et l’encadré détaillé p796 donnent tous deux **ACE**. L’ancienne restitution utilisait par erreur les justifications **AB** du Q6 suivant, situé p797 et portant sur les effets indésirables graves. Cette erreur créait une fausse contradiction et avait placé Q5 hors note.

La clé ACE, les justifications B–E de p796 et la bonne capture sont rétablies. La capture du Q6 est retirée des références de Q5. Le faux avertissement est supprimé. La vérification a été faite sur le sujet, la grille, l’encadré détaillé et les deux images, puis par une contrelecture indépendante. **Ce QCM redevient noté : 325 QCM de pharmacologie sont maintenant notés et 11 restent hors note.** Les réponses et états déjà enregistrés sont conservés ; leur résultat est recalculé avec la clé source rétablie.

### Justifications étrangères à leur item

Cinq justifications imprimées sans rapport avec leur proposition ont été remplacées, dans la restitution textuelle, par un message neutre renvoyant au commentaire : 2025–2026 S1 Q13C et Q14D/E ; 2018–2019 Q6D et Q15E. Les extraits originaux, leurs textes dans l’audit et les clés du tutorat restent accessibles. Aucune explication scientifique n’a été inventée pour les remplacer.

Le bloc de calcul QSAR commun au Q9 de 2020–2021 S1 a été replacé dans l’explication générale de la correction, au lieu d’être présenté comme une justification propre à E. Son contenu source et la clé restent conservés.

{table(['QCM source','Champs corrigés','Page sujet','Page corrigé'],changes_rows)}

Ces réparations concernent **{len(changes)} QCM**. Les textes des consignes et des **1680 propositions** restent ceux du sujet ; ils n’ont pas été réécrits pour les faire correspondre à une réponse supposée. Les énoncés communs et figures associés restent présents avant les QCM concernés. La seule clé modifiée est le rétablissement documenté ACE du Q5 ci-dessus.

## Commentaires sur les corrigés litigieux

Les commentaires distinguent les contradictions internes, les divergences entre annales, les formulations ambiguës et les hésitations explicitement présentes dans le tutorat. Ils ne prétendent pas remplacer la ronéo du cours ni une réponse de l’enseignant.

Exemples : justifications de thérapie cellulaire recopiées sous des items de sources naturelles ; deux propositions identiques recevant des verdicts opposés ; étapes de l’éducation thérapeutique ou caractère qualitatif/quantitatif de la chromatographie traités différemment selon l’annale. Dans ces cas, la clé du document est conservée et la réserve est visible après correction. Les questions déjà hors note restent hors note, sauf le mauvais appariement résolu ci-dessus.

La liste intégrale figure plus bas ainsi que dans `audit/PHARMACO_reserves.json`. L’inventaire `audit/PHARMACO_relecture_1680_items.csv` réunit, pour chaque item, son texte, la justification précédemment importée, celle affichée, les commentaires et les pages de contrôle. Les justifications remplacées restent donc traçables.

## Relecture sujet par sujet

Première passe : consigne, contexte éventuel, cinq propositions, figures, grille et correction détaillée. Deuxième passe : correspondance des lettres, quantificateurs/négations, numérotation, calculs et frontières entre QCM. Une passe transversale harmonise les thèmes et repère les affirmations traitées différemment entre sujets. Les cas d’appariement et de remplacement de justification ont en plus été contre-vérifiés avant fusion.

{table(['Année','Session','QCM','Items','Première page sujet','Dernière page QCM','QCM commentés'],subject_rows)}

Chaque QCM possède une fiche de contrôle A–E dans `audit/pharmaco_2026-11-22/`. La validation porte sur la complétude de ces fiches et la fidélité à la source, et non sur la validité scientifique absolue des réponses du tutorat. La ronéo actuelle n’a pas été fournie ; les points discutables restent expressément signalés.

## Progressions et deux profils

La sauvegarde de pharmacologie suit désormais l’identifiant stable de la question source, indépendamment de son nouveau thème ou numéro d’affichage. À l’ouverture, les anciennes réponses annuelles et leurs états corrigés sont récupérés automatiquement dans chaque profil. Les anciennes sauvegardes ne sont pas supprimées.

Interrupteur activé : profil 1, correction des QCM renseignés. Interrupteur désactivé : profil 2, correction globale du thème. Les progressions restent indépendantes. Si seules certaines anciennes séries avaient été corrigées, leurs questions restent corrigées après regroupement ; les autres ne dévoilent pas leurs réponses. Recommencer remet uniquement le thème et le profil courants à zéro.

Pour retrouver les sauvegardes locales, ouvrir le site dans le même navigateur et remplacer les fichiers à leur emplacement habituel en conservant le nom `index.html`. Le ZIP ne contient pas les réponses personnelles du navigateur.

## Contrôles de livraison

- **336 identifiants sources uniques**, 1680 items A–E et quinze banques UE4 ; aucun doublon ni perte de QCM.
- **2452 QCM protégés /202 banques** : données inchangées ; {logic['protectedRenderedStates']} états de cartes rendues et {logic['protectedScores']} résultats comparés à la version précédente.
- **672 réponses et 672 états de correction** vérifiés lors de la migration des deux profils, puis après rechargement.
- Correction sélective, correction globale, états partiels, remise à zéro limitée au profil/thème et absence de résurrection des anciennes réponses vérifiés.
- Les commentaires, clés, points et réserves des QCM non corrigés restent masqués dans l’interface et l’export UE4.
- **{data['protected_image_pdf_files']} images/PDF existants** contrôlés par empreinte ; les **{data['decoded_images']} images matricielles référencées et présentes** sont décodables. Tous les médias référencés de pharmacologie sont présents. Le PDF compilé est inchangé.
- Énoncés communs UE4 contrôlés lors du filtrage ; la révision antérieure des énoncés communs biomol, biochimie et biostatistiques reste intacte.

Les tests utilisent le script réel de la page et un adaptateur DOM. Ils ne constituent pas une inspection visuelle complète dans un navigateur ; aucune nouvelle vérification visuelle ordinateur/mobile du site n’est revendiquée. Les pages et captures PDF sensibles ont en revanche été examinées visuellement.

Une référence ancienne à `static/docx_3ec65cccd480.emf`, dans `bio.cm6`, pointe vers un fichier déjà absent de la version de départ. Elle ne concerne pas la pharmacologie ; la banque est conservée exactement conformément au périmètre demandé. Ce constat est distingué des contrôles UE4 dans l’audit.

## Questions de l’import conservées hors note

Le lot d’annales importé précédemment compte toujours **838 QCM**, dont **{data['new_import_ungraded_total']} hors note** après réparation de Q5. Cette liste concerne ce lot, pas d’éventuelles réserves d’autres banques historiques.

{table(['Unité','QCM source','Thème','Page sujet','Page corrigé','Motif'],ungraded_rows)}

## Documents de suivi

- `audit/PHARMACO_classement_336_QCM.csv` : classement et motif pour chaque QCM.
- `audit/PHARMACO_relecture_1680_items.csv` : contrôle complet de chaque item et de sa correction.
- `audit/PHARMACO_reserves.json` : tous les commentaires affichés.
- `audit/pharmaco_2026-11-22/` : fiches par sujet, décisions documentées, fichiers de validation et code de la révision.
- `audit/historique_2026-11-21/` : rapport précédent conservé pour la traçabilité ; ses anciens nombres de banques UE4 et de hors-note ne décrivent plus le classement courant.
- `audit/inventaire_838_qcm.csv` : inventaire de l’import actualisé pour les nouveaux thèmes et numéros UE4.
- `MAINTENANCE.md` : règles et structure à préserver lors de la prochaine modification.

## Liste intégrale des réserves de pharmacologie

Les pages ci-dessous sont celles du PDF compilé, en base 1. Chaque remarque est aussi affichée après correction du QCM correspondant.
'''
    for _,label in read('themes.json'):
        selected=[q for q in qlist if q['category']==label and q['reviewNotes']]
        if not selected:continue
        report+='\n### '+label+'\n'
        for q in selected:
            report+=f"\n#### {reference(q)} — sujet p{q['subjectPage']}, corrigé p{q['correctionPage']}\n\n"
            report+='\n'.join('- '+('**Item '+','.join(n['items'])+'** : ' if n.get('items') else '')+n['text'] for n in q['reviewNotes'])+'\n'
    (SITE/'CONTROLE_ANNALES.md').write_text(report)
    (ROOT/'output/Controle_integration_annales_PASS.md').write_text(report)
    readme=f'''# Site de révision PASS

Version du 22 novembre 2026 — pharmacologie reclassée et relue.

## Ouvrir le site

1. Décompressez entièrement l’archive.
2. Ouvrez `index.html` dans votre navigateur.
3. Conservez les dossiers `static/` et `sources/` à côté du fichier.

Le site fonctionne localement, sans compte ni serveur. Il comprend **2788 QCM**. En pharmacologie, les **336 QCM** sont réunis dans les **15 thèmes** de la nomenclature demandée ; toutes les années d’un thème sont accessibles ensemble. La date et la page figurent discrètement sous la consigne.

## Corrections et commentaires

Les **1680 items de pharmacologie** ont été repris avec leurs sujets et corrigés. Les points discutables comportent une remarque « À vérifier dans la ronéo », visible après correction. Le Q5 de pharmacocinétique 2023–2024 S2 a retrouvé sa bonne correction ACE et redevient noté. La pharmacologie contient donc **325 QCM notés et 11 hors note**.

Les autres unités et la révision antérieure des énoncés communs sont conservées. Les sujets, images et corrigés originaux restent consultables depuis la page. Les extraits de correction ne s’affichent qu’après validation.

## Retrouver sa progression

Les réponses et les QCM corrigés des anciennes séries annuelles de pharmacologie sont récupérés automatiquement dans les deux profils, puis sauvegardés indépendamment du nouveau classement.

- Interrupteur activé : profil 1, seuls les QCM renseignés sont corrigés.
- Interrupteur désactivé : profil 2, correction globale du thème.
- Recommencer remet uniquement le thème et le profil courants à zéro.

Utilisez le même navigateur et remplacez le site à son emplacement habituel en conservant le nom `index.html`. Les réponses sont dans le navigateur, pas dans le ZIP. « Exporter mes résultats » conserve un bilan.

« Aucune proposition » est une réponse volontaire, différente d’un QCM laissé vide.

## Vérification détaillée

`CONTROLE_ANNALES.md` présente le classement, les réparations, toutes les réserves et la portée des contrôles. Le dossier `audit/` contient les inventaires QCM et items ; `MAINTENANCE.md` décrit la structure pour les futures modifications. Les sources ne fournissent pas la ronéo actuelle : les remarques signalent les points à vérifier et ne constituent pas une correction scientifique de remplacement.
'''
    (SITE/'LIRE_DABORD.md').write_text(readme);(SITE/'README.md').write_text(readme)
    maintenance='''# Maintenance — état du 22 novembre 2026

## Périmètre à préserver

Le site contient 2788 QCM /217 banques. La dernière révision est limitée aux 336 QCM de pharmacologie UE4 : quinze banques par thème, toutes années réunies. Les 2452 autres QCM /202 banques restent identiques à la version du 21 novembre. Ne modifier ni UE1, ni UE5, ni biomol/ED, biochimie ou biostatistiques sans nouvelle instruction.

Ne pas introduire de QCM antérieur à 2015. Traiter un sujet et son corrigé à la fois. Relire les cinq items, la consigne, les contextes de la page précédente, les figures et les limites entre QCM. Les titres reprennent la consigne ; fichier et page restent discrets. Une question conserve ses cinq propositions ensemble, même si son contenu couvre plusieurs thèmes.

## Données et interface

`index.html` regroupe CSS, interface et JavaScript. `const EXAMS=` est du JSON. Chaque banque possède `ue`, `courseId`, `kind`, `questions`, des libellés et une ancienne clé `storage`. Les banques UE4 sont `ue4.annales.theme.<themeId>`, avec `pharmaGrouped:true` et `kind:annales`. Les quinze libellés et leur ordre sont figés dans le fichier de thèmes de l’audit courant.

Les champs `question` et `options[].text` sont exclusivement des énoncés. Les champs `explanations`, `generalExplanation`, `correctionImages` et `reviewNotes` sont des corrections et ne s’affichent qu’après validation. Les `reviewNotes` ont les champs `items`, `text`, `kind` : motif précis, pas de correction inventée, et invitation à vérifier la ronéo. `pharmaWarningCovered` signifie que la nouvelle réserve reprend déjà le motif du champ historique `warning` ; ce dernier reste conservé dans les données et l’audit.

Identité de contenu : `sourceId`, par exemple `ue4:2023-2024:S2:q05`. Le champ `id` est seulement le numéro local d’affichage dans le thème. `sourceNumber` et, le cas échéant, `printedSourceNumber` restent les numéros du sujet. `correctionNumber` peut être différent (décalage de numérotation documenté en 2021–2022 S1).

## Source et notation

Les pages de `subjectPage`, `sourceStartPage`, `sourceEndPage`, `correctionPage` sont en base 1 dans `sources/Annales_compilation.pdf`, sauf banques historiques avec `sourcePdf`/`correctionPdf` distincts. Ne pas mélanger PASS et PACES d’une même année.

`answer` est la clé retenue ; vide signifie hors note sauf `answerIsEmpty:true`. `rawAnswer` conserve la clé imprimée quand elle est disponible. 325 QCM UE4 sont notés et 11 sont hors note. Le seul changement de clé de cette révision est 2023–2024 S2 Q5 : vide → ACE, confirmé par la grille p794 et l’encadré p796 ; les justifications de Q6 avaient été importées par erreur. Les autres clés sont inchangées. Une réserve scientifique nouvelle ne doit pas être présentée comme une résolution de la contradiction : conserver la clé source et signaler le problème, sauf nouvelle décision étayée et documentée.

Barème existant : 10/5/2/0 points pour 0/1/2/3+ erreurs, conversion sur20, coefficients éventuels. `∅` distingue une réponse volontaire « aucune proposition » d’un blanc. L’option est affichée à tous les QCM importés, pas seulement lorsque la clé est vide.

## Sauvegarde UE4 après reclassement

La progression est indexée par `sourceId` dans `qcm-pass-ls-ue4-progress-by-source-v1` (profil1) et la même clé suivie de `_profil_2_v1` (profil2). Schéma : `{version:1,bySource:{sourceId:{answer,corrected}}}`. Les anciennes correspondances sont dans `PHARMA_PROGRESS_LINKS` et `legacyProgress` ; `PHARMA_EXAM_ALIASES` retrouve un thème depuis une ancienne banque sélectionnée.

La migration ne remplit que les identités absentes ; elle conserve les anciennes clés de stockage sans les écraser. Une entrée vide après réinitialisation est volontaire : ne pas l’interpréter comme un motif de réimportation. La sauvegarde ne met à jour que les QCM du thème courant. Les deux profils sont indépendants. Les états corrigés partiels sont conservés même dans le profil2, car plusieurs anciennes séries annuelles peuvent être réunies dans un thème ; la correction globale termine les questions restantes du thème. La note ne compte que les QCM corrigés tant que le thème n’est pas entièrement corrigé.

Hors UE4, les clés et le fonctionnement antérieurs sont inchangés : profil1 `storage`, profil2 `storage+'_profil_2_v1'`. Préférence `ssh_pass_only_filled_mode_v1`, banque sélectionnée `ssh_pass_selected_exam_v1`.

## Énoncés communs et images

`sharedContexts` contient les données partagées (id, text, images, questionNumbers, questionIds, pages et source). Le bloc est affiché avant le premier membre visible, y compris en recherche/filtrage. Une reclassification peut changer `questionIds`, jamais les numéros sources ou le contenu partagé. `references` et `referenceImages` sont les annexes ; les données indispensables restent visibles dans le bloc commun.

`images`, `stemImages`, `options[].image` et `originalImages` contiennent les éléments de sujet ; aucune réponse ne doit y être introduite. `correctionImages` est réservé à l’après-correction. Les fichiers source doivent rester exacts. Ne jamais reconstituer par génération une figure médicale ou chimique précise. La révision du 22 novembre n’a créé aucun asset et n’a modifié aucun octet d’image/PDF ; elle a retiré un mauvais rattachement de capture au Q5 2023–2024 S2.

Les réparations antérieures des énoncés communs biomol/ED, biochimie et biostatistiques restent applicables. Les détails sont dans l’historique du 21 novembre et les manifestes dédiés. Les quatre clés ED réappariées à cette date ne doivent pas être régressées.

## Reproduction et contrôles

Le dossier `audit/pharmaco_2026-11-22/` conserve les instructions, le cliché immuable de la version précédente, les fiches par sujet, les décisions de patch et les scripts de cette révision. Les chemins d’exécution sont ceux du workspace de production ; adapter les racines si le dossier est déplacé. Ne pas relancer l’ancien constructeur général sans porter les changements UE4 : il rétablirait le classement annuel.

Ordre de la révision courante : `build_pharma.py` → `test_pharma.cjs` → `audit_pharma.py` → `write_report.py` → conditionnement ZIP et manifeste SHA256. Le mode `--draft` du constructeur/tests est seulement une simulation de migration avec un classement provisoire : ne jamais le livrer.

Avant livraison, préserver exactement les données hors périmètre, contrôler tous les identifiants, les références d’images, l’absence de fuite de correction, les deux profils, la migration et la remise à zéro. Les contrôles JavaScript actuels utilisent un adaptateur DOM ; ils ne certifient pas la mise en page d’un navigateur. La revue documentaire ne certifie pas la justesse scientifique des corrigés litigieux : leurs réserves doivent rester visibles après correction.
'''
    (SITE/'MAINTENANCE.md').write_text(maintenance)
    print(json.dumps({'report_bytes':len(report.encode()),'review_notes':len(notes),'repaired_questions':len(changes),'themes':len(theme_rows),'ungraded_import':len(ungraded_rows)},ensure_ascii=False))

if __name__=='__main__':main()
