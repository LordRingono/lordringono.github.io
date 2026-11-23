"""Audit SSH V6 : comparaison des huit documents et relecture des 274 QCM."""
from pathlib import Path
import json,copy,re,hashlib,unicodedata,difflib
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
R=json.loads((HERE/'reviewed_initial.json').read_text())
BASE=copy.deepcopy(R)
A=json.loads((HERE/'fresh_source_audit.json').read_text())
C=json.loads((HERE/'crops_initial.json').read_text())
M=json.loads((HERE/'source_manifest.json').read_text())
Q={(b,q['id']):q for b,v in R['banks'].items() for q in v['questions']}
ROWS={(a['bank'],a['id']):a for a in A};CROPS={(a['bank'],a['id']):a for a in C}
MAN={(m['bank'],m['role']):m for m in M}
changes=[]
def dump(f,x):(HERE/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',(s or '').lower()))
def crop(file,lines):
 return [{'file':file,'fileLabel':Path(file).name,'page':p,'rect':[30,min(l['rect'][1] for l in lines if l['page']==p)-3,570,max(l['rect'][3] for l in lines if l['page']==p)+3]} for p in sorted({l['page'] for l in lines})]
def source_ref(b,n,role):
 a=ROWS[b,n];m=MAN[b,role]
 p=(a['subjectLines'] if role=='subject' else a['correctionLines'])[0]['page']
 return {'file':Path(m['absolute']).name,'page':p,'label':'Sujet fourni' if role=='subject' else 'Corrigé fourni','href':m['packaged']+'#page='+str(p)}
URLS={
 'confiance':('Code de la santé publique — L1111-6','https://www.legifrance.gouv.fr/affichCodeArticle.do?categorieLien=id&cidTexte=LEGITEXT000006072665&dateTexte=&idArticle=LEGIARTI000049391677'),
 'don':('Code de la santé publique — L1232-1','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031931933/2026-09-11'),
 'refus_don':('Code de la santé publique — R1232-4-4','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033038931/2026-01-01'),
 'vote2025':('Assemblée nationale — dossier législatif fin de vie','https://www.assemblee-nationale.fr/dyn/17/dossiers/fin_de_vie_17e'),
 'diamond':('UNESCO — Diamond Open Access','https://www.unesco.org/en/diamond-open-access'),
 'clb':('Centre Léon Bérard — mentions légales','https://www.centreleonberard.fr/mentions-legales'),
 'turing':('Turing, 1950 — Computing machinery and intelligence','https://www2.cs.sfu.ca/~vaughan/teaching/415/papers/turing1950.html'),
 'striatum':('Expérience sur le contrôle cortical de la libération de dopamine, 2020','https://pubmed.ncbi.nlm.nih.gov/32859717/'),
 'cannon':('Cannon, 1929 — Organization for physiological homeostasis','https://journals.physiology.org/doi/abs/10.1152/physrev.1929.9.3.399'),
 'nosocomial':('Ministère de la santé — infections nosocomiales, questions-réponses','https://sante.gouv.fr/IMG/pdf/Questions_-_reponses_sur_les_infections_nosocomiales.pdf'),
 'justesse':('BIPM — vocabulaire international de métrologie, justesse','https://jcgm.bipm.org/vim/fr/2.14.html'),
 'fidelite':('BIPM — fidélité de mesure','https://jcgm.bipm.org/vim/fr/2.15.html'),
 'ovocyte':('Service public — don d’ovocytes et prise en charge des frais','https://www.service-public.gouv.fr/particuliers/vosdroits/F24586'),
 'gpa':('Gouvernement britannique — cadre juridique de la gestation pour autrui','https://www.gov.uk/government/publications/having-a-child-through-surrogacy/the-surrogacy-pathway-surrogacy-and-the-legal-process-for-intended-parents-and-surrogates-in-england-and-wales'),
 'jenner':('OMS — histoire de la vaccination contre la variole','https://www.who.int/news-room/spotlight/history-of-vaccination/history-of-smallpox-vaccination/'),
 'ebm':('Sackett et al., BMJ, 1996 — Evidence based medicine','https://www.bmj.com/content/312/7023/71'),
 'embryon2013':('Loi du 6 août 2013 — recherche sur l’embryon','https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000027811435'),
 'tetanus':('OMS — protection contre le tétanos, absence d’immunité collective','https://www.who.int/docs/default-source/tetanus/9789241509237-eng.pdf'),
 'dale':('Subramony et al., 2014 — étude documentaire du cône de Dale','https://eric.ed.gov/?id=EJ1057220'),
 'biodiversite':('Convention sur la diversité biologique, article 2','https://www.cbd.int/doc/legal/cbd-en.pdf'),
 'directives':('Code de la santé publique — L1111-11','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054137791/2026-06-18'),
 'resistance1940':('Abraham et Chain, Nature, 1940 — enzyme détruisant la pénicilline','https://www.nature.com/articles/146837a0'),
 'consentement':('Code de la santé publique — L1111-4','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041721056/2024-02-17'),
 'shock':('Consensus ESICM, 2014 — définition du choc circulatoire','https://pmc.ncbi.nlm.nih.gov/articles/PMC4239778/'),
 'anchoring':('Tversky et Kahneman, Science, 1974 — ancrage et ajustement','https://pages.ucsd.edu/~mckenzie/TverskyKahneman1974Science.pdf'),
 'wisc':('Pearson — présentation du WISC-V','https://www.pearsonclinical.fr/mwdownloads/download/link/id/709'),
 'transaction':('Code civil — article 2044','https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033458766/2026-11-11'),
 'deonto1995':('Décret du 6 septembre 1995 portant code de déontologie médicale','https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000555170'),
 'salpetriere':('Archives AP-HP — histoire de la Salpêtrière','https://pitiesalpetriere.aphp.fr/wp-content/blogs.dir/58/files/2016/12/Une-page-dhistoire.pdf'),
 'invalides':('Musée de l’Armée — fondation des Invalides en 1670','https://www.musee-armee.fr/au-programme/350-ans-du-musee-de-larmee/1670-2020-les-invalides-dhier-a-aujourdhui.html'),
 'emploi':('Service public — obligation d’emploi des travailleurs handicapés','https://entreprendre.service-public.gouv.fr/vosdroits/F22523'),
 'madrid':('Fondation ONCE — Déclaration de Madrid, 20–23 mars 2002','https://www.fundaciononce.es/sites/default/files/docs/Educaci%C3%B3n%2520y%2520Personas%2520con%2520Discapacidad_Presente%2520y%2520Futuro_1.pdf'),
 'nagi':('Saad Z. Nagi, 1991 — Disability concepts revisited','https://www.nationalacademies.org/read/1579/chapter/13'),
 'empathy':('Singer et al., Science, 2004 — réseaux de l’empathie pour la douleur','https://pubmed.ncbi.nlm.nih.gov/14976305/')
}
covered=set()
def note(b,n,items,text,urls=(),kind='scientific_reserve',covers=False):
 q=Q[b,n]
 obj={'noteId':f'ssh-v6-{b}-{n}-{items}-{len(q.get("reviewNotes",[]))+1}','kind':kind,'items':list(items) if items!='all' else [o['id'] for o in q['options']],
 'text':text+' Vérifier ce point dans la ronéo du cours correspondant.',
 'refs':[source_ref(b,n,'subject'),source_ref(b,n,'correction')]+[{'label':URLS[u][0],'href':URLS[u][1],'referenceType':'external_primary'} for u in urls],
 'sourceVerdict':ROWS[b,n]['sourceKey'],'courseVerdict':None,'coversWarning':covers}
 q.setdefault('reviewNotes',[]).append(obj)
 if covers:covered.add((b,n))
 changes.append({'bank':b,'id':n,'type':'note_after_correction','note':obj})

# Les rubriques bleues annoncent le cours du QCM suivant, pas la fin de E.
for n in [2,4,6,7,9,10,13,16,17,21,26,29,32,34,36]:
 a=ROWS['acc',n];heading=a['correctionLines'][-1]
 a['correctionLines']=a['correctionLines'][:-1]
 e=a['correctionItems'][-1]
 e['lines']=[l for l in e['lines'] if l!=heading]
 if e['detail'] and e['detail'].endswith(heading['text']):e['detail']=e['detail'][:-len(heading['text'])].rstrip()
 CROPS['acc',n]['correction']=crop(a['correctionFile'],a['correctionLines'])
 changes.append({'bank':'acc','id':n,'type':'crop_remove_next_course_heading','removed':heading['text']})
# Le PDF place D et E sur la même ligne : ne pas laisser E attaché à D.
a=ROWS['acc',34];ci={o['id']:o for o in a['correctionItems']}
assert 'E.' in ci['D']['subjectText']
d,e=ci['D']['subjectText'].split('E.',1);ci['D']['subjectText']=d.strip();ci['E']['subjectText']=e.strip()
a['inlineMarkerVerifiedVisually']='D et E imprimés sur la même ligne p.19, séparation confirmée.'
# Le contexte est identique dans les deux questions originales.
q25,q26=Q['acc',25],Q['acc',26]
assert norm(q25['context'])==norm(q26['context']) and q25['context']
shared={'id':'ssh-v6-acc-greffe-25-26','text':q25['context'],'images':[],
 'sourceFile':Path(MAN['acc','subject']['absolute']).name,'sourceStartPage':10,'sourceEndPage':10}
for n in (25,26):Q['acc',n]['sharedContexts']=[copy.deepcopy(shared)];Q['acc',n]['context']=''
changes.append({'bank':'acc','ids':[25,26],'type':'restore_shared_context_block'})
# Les deux questions du corrigé sont différentes : montrer la pièce, sans noter.
for n in (11,12):
 q=Q['colle2',n];q['answer']='';q.pop('answerIsEmpty',None)
 q['rawAnswer']=ROWS['colle2',n]['sourceKey'];q['explanations']={}
 CROPS['colle2',n]['correctionNote']='Attention : le QCM portant ce numéro dans le corrigé fourni a un autre énoncé. Cette copie documente le décalage ; elle ne constitue pas la correction de la question affichée. Question hors note.'
 CROPS['colle2',n]['correctionMismatch']=True
 note('colle2',n,'all',q['warning'],kind='source_mismatch',covers=True)

# Réserves motivées : la clé fournie ne devient pas une clé reconstruite.
note('acc',4,'B','Le détail réfute un comportement agressif envers le patient alors que l’item porte sur les émotions éprouvées. L’interdiction d’agir agressivement ne démontre pas l’absence possible d’une émotion agressive. La clé CDE est conservée ; distinguer ressenti et conduite professionnelle.',kind='source_ambiguity')
note('acc',14,'E','Le 27 mai 2025 correspond à l’adoption en première lecture à l’Assemblée nationale de la proposition sur l’aide à mourir, pas à une loi déjà promulguée. Le détail mentionne d’ailleurs un projet. E reste la réponse attendue dans le document, avec cette imprécision chronologique.',('vote2025',),covers=True)
note('acc',15,'D','D est bien faux dans la clé : la personne de confiance ne décide pas des traitements. Le détail disant qu’elle donne seulement son avis est réducteur : sa mission est de témoigner de la volonté du patient, et non d’exprimer sa préférence personnelle.',('confiance',))
note('acc',25,'D','Le prélèvement repose sur l’absence de refus exprimé par le défunt. Les proches témoignent d’un éventuel refus du défunt ; leurs propres souhaits ne remplacent pas sa volonté. La formulation « leurs volontés » est donc ambiguë. La clé ACDE est conservée.',('don','refus_don'))
note('colle2',13,'DE','L’accès ouvert n’impose pas toujours des frais aux auteurs : le modèle diamant est gratuit pour auteurs et lecteurs. D, coché vrai, est trop général. Pour E, le Centre Léon Bérard est un établissement privé d’intérêt collectif ; ce statut ne découle pas simplement de sa spécialisation.',('diamond','clb'),covers=True)
note('colle2',15,'B','Le seuil de 50 % de réussite n’est pas un critère universel fixé par le texte de Turing. Son article de 1950 expose un jeu d’imitation et une prévision à cinq minutes, sans poser cette règle générale. La clé du tutorat est conservée ; retrouver la convention présentée dans le cours.',('turing',))
note('colle2',21,'BD','Le détail résume excessivement le circuit cortex–striatum : des projections corticales glutamatergiques peuvent moduler la libération de dopamine striatale. Le striatum est une structure impliquée dans le renforcement ; le qualifier de renforceur primaire peut confondre la structure et le stimulus renforçateur. La clé A est conservée.',('striatum',))
note('colle2',48,'B','Claude Bernard a développé la notion de milieu intérieur, précurseur de l’homéostasie ; Walter Cannon a formulé le concept sous ce nom. L’attribution abrégée du détail demande cette distinction historique. Le rejet de Louis Pasteur reste cohérent.',('cannon',))
note('colle2',48,'E','L’expression « dans les 48 h » inverse le repère usuel : si le statut initial est inconnu, un délai d’au moins 48 h est généralement retenu, en tenant compte de l’incubation et de l’infection concernée. Le principe est une infection absente et non incubante à l’admission. E reste vrai dans la clé fournie, malgré cette réserve.',('nosocomial',),covers=True)
note('colle2',50,'AC','La justesse concerne l’écart entre la moyenne des mesures et la référence ; le caractère groupé décrit la fidélité. Des tirs groupés au centre associent ces deux propriétés. Le détail de C contient aussi un renvoi circulaire à C. La clé ADE est conservée.',('justesse','fidelite'),covers=True)
note('colle2',63,'C','Le don d’ovocytes n’est pas rémunéré. La prise en charge des frais médicaux et le remboursement justifié de certains frais ne sont pas une rétribution de la pénibilité. Le verdict C Faux est conservé avec cette distinction.',('ovocyte',),covers=True)
note('colle2',64,'ACE','Il n’existe pas une interdiction uniforme de la GPA dans toute l’Europe : elle est juridiquement possible, notamment au Royaume-Uni. Selon le dispositif, les gamètes peuvent provenir des parents d’intention ou de donneurs. La clé ABC correspond à une définition restrictive de cours ; ses formulations générales et le détail de E doivent être nuancés.',('gpa',),covers=True)
note('colle2',68,'A','L’OMS attribue à Jenner le premier vaccin efficace contre la variole humaine, à partir de matériel de vaccine. L’item confond la maladie ciblée et le matériel utilisé ; l’argument du détail selon lequel ce n’était pas encore un vaccin est contestable. Le verdict Faux est conservé.',('jenner',),covers=True)
note('colle2',69,'B','L’Evidence-Based Medicine désigne une démarche de décision intégrant les meilleures données disponibles et l’expertise clinique, pas une base de données. B est néanmoins coché vrai dans le document ; la clé BE est conservée avec cette réserve explicite.',('ebm',),covers=True)
note('colle2',74,'B','Le régime d’autorisation de la recherche sur l’embryon existe depuis la loi du 6 août 2013. Le situer pour la première fois en 2021, comme le fait le détail, est inexact. L’item décrivant la situation en 2021 peut rester vrai.',('embryon2013',))
note('colle1',12,'A','Le détail ne doit pas faire retenir que tous les vaccins protègent seulement des formes graves. Le type et l’ampleur de protection dépendent du vaccin et de la maladie ; par exemple la vaccination antitétanique prévient le tétanos. La formulation absolue de A et la clé D du document sont conservées.',('tetanus',))
note('colle1',13,'CE','Le mot « systématiquement » du détail de E est trop général. Pour le tétanos, il n’existe pas de transmission interhumaine ni d’immunité collective : chacun doit être protégé. Les effets sur la circulation d’un agent et sur l’ensemble de la population dépendent donc de la maladie et du vaccin.',('tetanus',))
note('colle1',26,'all','Les pourcentages de rétention associés au cône de Dale ne constituent pas des mesures scientifiques établies. Les travaux documentaires sur cette attribution mettent en évidence un assemblage trompeur entre le cône et des taux de mémorisation. La clé ABCDE reste celle de l’épreuve ; distinguer réponse de cours et preuve expérimentale.',('dale',),covers=True)
note('colle1',32,'E','Le verdict Faux est justifié par le caractère incomplet de l’item. Toutefois, le détail réduit lui aussi la biodiversité aux interactions : la définition de la Convention comprend la diversité au sein des espèces, entre espèces et des écosystèmes.',('biodiversite',))
note('colle1',39,'D','Un désaccord personnel du médecin ne suffit pas à écarter des directives anticipées. Elles s’imposent en principe, avec les exceptions légales, notamment l’urgence pendant l’évaluation ou leur caractère manifestement inapproprié, encadré par une procédure collégiale. Le détail ne doit pas faire oublier ces exceptions.',('directives',))
note('colle1',49,'AB','La campagne française des années 2000 correspond à une sensibilisation du public ; elle n’est pas la découverte scientifique de l’antibiorésistance. Des observations expérimentales de résistance à la pénicilline existaient dès 1940. La clé BE est conservée selon le repère de cours.',('resistance1940',))
note('colle1',60,'C','Le verdict Faux est conservé. La justification affirmant que les lois relatives à la fin de vie ne couvrent que les personnes dont le pronostic vital est engagé est trop générale : les dispositions sur le consentement et le refus de traitement ont une portée plus large. Certaines mesures particulières ont des critères propres.',('consentement',))
note('colle1',62,'A','L’hypotension est fréquente dans le choc, mais elle n’est pas indispensable à sa définition : une hypoperfusion peut exister malgré une pression encore maintenue. Le consensus ESICM décrit une défaillance circulatoire aiguë avec utilisation inadéquate de l’oxygène. A reste coché vrai dans la clé fournie.',('shock',))
note('colle1',66,'E','La demande familiale ne suffit pas à imposer un traitement, mais l’arrêt d’un traitement ne repose pas sur le seul désaccord de l’équipe avec la famille. Il faut rechercher la volonté du patient et respecter les conditions légales, dont la procédure collégiale quand elle est requise. Le verdict E Faux est conservé.',('consentement','directives'))
note('colle1',68,'CD','La question demande une seule définition exactement donnée dans le cours : B reste attendue. C et D évoquent aussi des mécanismes d’ancrage au sens général, en particulier l’ajustement insuffisant depuis une estimation initiale décrit par Tversky et Kahneman. Leur exclusion ne doit pas faire croire que ces mécanismes sont étrangers à l’ancrage.',('anchoring',),kind='source_ambiguity')
note('eb',4,'B','Le nombre de scores dépend de l’échelle et de sa version. Le WISC-V comporte notamment cinq indices principaux et un quotient intellectuel total ; « trois QI » n’est donc pas une description universelle du test. La clé BE est conservée ; identifier l’échelle visée dans la ronéo.',('wisc',))
note('eb',19,'B','Le classement d’un pays comme le plus hésitant dépend de l’année, de l’enquête et de la question posée. Aucune étude ni période n’est précisée ici. Le verdict du document ne doit pas être interprété comme un classement universel et permanent.',kind='source_ambiguity')
note('eb',24,'E','Une transaction peut terminer une contestation déjà née : une solution amiable reste donc possible après l’engagement d’une voie contentieuse. Le rejet général de E est litigieux. La clé AD est conservée, en attendant de préciser le cadre particulier éventuellement visé par le cours.',('transaction',))
note('eb',25,'A','Le code de déontologie était déjà porté par un décret avant sa codification dans le Code de la santé publique, notamment en 1995. Si « valeur juridique interne » entend exclure toute valeur réglementaire avant 2004, cette interprétation est inexacte. La clé fournie est conservée.',('deonto1995',),kind='source_ambiguity')
note('eb',50,'C','Les deux exemples relèvent du XVIIe siècle : création de l’Hôpital général intégrant la Salpêtrière en 1656 et fondation des Invalides en 1670. Les situer à la Renaissance est chronologiquement discutable. Le verdict C Vrai est conservé avec les dates des institutions.',('salpetriere','invalides'))
note('eb',51,'B','L’obligation d’emploi à hauteur de 6 % concerne les employeurs atteignant le seuil légal de 20 salariés, selon les règles applicables ; elle ne s’applique pas indistinctement à toute entreprise. Le verdict B Vrai est conservé avec cette condition.',('emploi',))
note('eb',52,'A','La Déclaration de Madrid sur le handicap est issue du congrès des 20–23 mars 2002. Le mois de mai écrit dans A est une erreur de date, même si son contenu général reprend l’évolution vers l’inclusion. La clé ABD est conservée.',('madrid',))
note('eb',52,'B','Le modèle de Saad Nagi distingue pathologie, déficience, limitation fonctionnelle et handicap dans les rôles sociaux. La liste faisant de la subjectivité un quatrième niveau ne correspond pas à cette présentation originale. Vérifier l’auteur et le schéma réellement exposés dans le cours ; B reste vrai dans la clé fournie.',('nagi',))
note('eb',65,'A','Assimiler les neurones miroirs aux seuls neurones de l’empathie est une simplification. L’empathie implique plusieurs réseaux ; une étude expérimentale sur la douleur d’autrui met notamment en jeu l’insula antérieure et le cortex cingulaire antérieur. La réponse attendue A est conservée, sans en faire une définition exclusive.',('empathy',))

# Tous les avertissements donnant une réponse deviennent des notes après validation.
# Les anciennes notes sourcées et leurs identifiants sont préservés.
for (b,n),q in Q.items():
 w=q.get('warning','')
 if not w:continue
 if (b,n) not in covered and not any(v.get('coversWarning') for v in q.get('reviewNotes',[])):
  if (b,n)==('colle2',54):
   w='Le document affirme une baisse de mortalité dans les deux groupes après l’usage de chlorure de chaux, sans fournir le tableau ni la période. Le contraste historique entre les deux cliniques demande à être vérifié ; aucune nouvelle clé n’est déduite de cette réserve.'
  if (b,n)==('colle1',69):
   w='Le détail oppose ici « inductif » à « probabiliste/bayésien » sans définir ces termes. La clé AC est conservée comme convention de cette épreuve ; vérifier la portée terminologique de cette distinction dans le cours.'
  note(b,n,'all',w,kind='source_ambiguity',covers=True)
 q['warning']='Question hors note : le sujet et le corrigé portant ce numéro ne correspondent pas. Voir les documents et la remarque après correction.' if b=='colle2' and n in (11,12) else ''
 changes.append({'bank':b,'id':n,'type':'move_warning_after_grading','before':w})

# Provenance des documents remis en page : les pixels fournis restent intacts.
for c in C:
 if c['bank'] in ('colle1','eb'):
  c['subjectNote']='Copie du PDF fourni, remis en page. Une version officielle non remaniée permettrait un contrôle supplémentaire de provenance.'
  c['correctionNote']='Copie du corrigé fourni, remis en page et comportant déjà certains commentaires. Les annotations du PDF sont conservées telles quelles ; les remarques de la présente vérification sont distinguées dans la correction interactive.'

# Preuve par item : réextraction neuve, comparaison de chaque texte et verdict.
audit=[];details_missing=[];unexplained=[]
for a in A:
 b,n=a['bank'],a['id'];q=Q[b,n];same=(b,n) not in [('colle2',11),('colle2',12)]
 si={x['id']:x for x in a['subjectItems']};ci={x['id']:x for x in a['correctionItems']}
 items=[]
 for o in q['options']:
  l=o['id'];s=si[l];d=ci[l];assert s['similarity']>=.96
  if same:
   assert (d['verdict'] in ('VRAI','V'))==(l in a['sourceKey']) or d['verdict'] is None,(b,n,l,d)
   assert norm(d['subjectText'])==norm(s['sourceText']) or difflib.SequenceMatcher(None,norm(d['subjectText']),norm(s['sourceText'])).ratio()>.94,(b,n,l,'repeated subject mismatch')
   exp=q['explanations'].get(l,'')
   if d['detail'] is not None and norm(exp)!=norm(d['detail']):unexplained.append([b,n,l,exp,d['detail']])
  if not d['detail']:details_missing.append([b,n,l])
  items.append({'id':l,'siteText':o['text'],'subjectText':s['sourceText'],'subjectTextSimilarity':s['similarity'],
    'subjectLocations':[{'page':v['page'],'rect':v['rect']} for v in s['lines']],
    'correctionRepeatedText':d['subjectText'],'correspondingCorrection':same,'sourceVerdict':d['verdict'],
    'sourceDetail':d['detail'],'siteDetail':q['explanations'].get(l,''),
    'correctionLocations':[{'page':v['page'],'rect':v['rect']} for v in d['lines']],
    'status':'source_compared' if same else 'correction_for_other_question'})
 audit.append({'bank':b,'id':n,'subjectFile':a['subjectFile'],'correctionFile':a['correctionFile'],
 'sourceKey':a['sourceKey'],'shortGrid':a['sourceShortKey'],'siteKey':q['answer'],'scored':bool(q['answer']),
 'correctionMatches':same,'items':items,'generalExplanation':q.get('generalExplanation',''),
 'subjectFullLines':a['subjectLines'],'correctionFullLines':a['correctionLines'],
 'notes':[z['noteId'] for z in q.get('reviewNotes',[])]})
assert not unexplained,unexplained
# Tous les panneaux doivent rendre des pixels et rester dans la page.
docs={};panels=0
for c in C:
 for role in ('subject','correction'):
  for p in c[role]:
   d=docs.setdefault(p['file'],fitz.open(p['file']));page=d[p['page']-1];rect=fitz.Rect(p['rect'])
   assert page.rect.contains(rect) and rect.height>8,(c['bank'],c['id'],role,p)
   pix=page.get_pixmap(matrix=fitz.Matrix(.4,.4),clip=rect,alpha=False)
   assert pix.width and pix.height
   panels+=1
# Aucun champ graphique interactif inattendu n'est laissé sans contrôle.
figs=[(b,q['id'],k) for b,v in R['banks'].items() for q in v['questions'] for k in ('images','stemImages','originalImages','referenceImages') if q.get(k)]
assert not figs,figs
missing=[
 {'type':'corrige_correspondant','document':'Correction Colle 2 SSH — QCM 11 et 12 du sujet fourni','questions':[{'bank':'colle2','id':11},{'bank':'colle2','id':12}],
  'reason':'La grille et le détail fournis corrigent d’autres énoncés. Les sujets de greffe/prélèvement ne disposent pas de correction correspondante. Les deux fichiers et les quatre séries ont été rapprochés ; les items du corrigé se retrouvent dans EB 54–55, pas dans ces deux sujets.'},
 {'type':'original_non_remanie','document':'Colle 1 SSH : sujet et corrigé officiels non remis en page','questions':'colle1, 78 QCM','reason':'Les PDF fournis sont remis en page et le corrigé contient des commentaires personnalisés antérieurs. Comparaison complète faite sur ces pièces, sans certification de la transcription initiale.'},
 {'type':'original_non_remanie','document':'EB blanc SSH : sujet et corrigé officiels non remis en page','questions':'eb, 79 QCM','reason':'Même limite de provenance ; demander notamment le texte complet de EB 6B et la consigne de EB 77 dans le sujet initial.'},
 {'type':'roneos','document':'Ronéos SSH des cours cités dans les remarques et errata du tutorat','questions':[{'bank':b,'id':n,'noteIds':[x['noteId'] for x in q.get('reviewNotes',[])]} for (b,n),q in Q.items() if q.get('reviewNotes')],
  'reason':'Arbitrer les conventions du cours, les données datées et les réserves scientifiques documentées ; les clés fournies sont préservées hors absence de correspondance.'}
]
visual=json.loads((HERE/'visual/manifest.json').read_text())
counts={'banks':4,'questions':len(A),'items':sum(len(q['options']) for q in Q.values()),'sourceDocuments':8,'scored':272,'notScored':2,
 'subjectCopies':274,'correctionCopies':274,'correspondingCorrections':272,'mismatchedCorrections':2,'panelsRenderedGeometryChecked':panels,
 'visualContactSheetsViewed':21,'detailsAbsentInOriginal':len(details_missing),'notesBefore':sum(len(q.get('reviewNotes',[])) for b in BASE['banks'].values() for q in b['questions']),
 'notesAfter':sum(len(q.get('reviewNotes',[])) for q in Q.values()),'notesAdded':sum(x['type']=='note_after_correction' for x in changes),'sourceHeadingBoundariesFixed':15,
 'warningHintsMoved':sum(x['type']=='move_warning_after_grading' for x in changes),'sharedContextQuestions':2,'omittedQuestionsProven':0}
dump('reviewed.json',R);dump('crops.json',C);dump('audit.json',audit);dump('missing.json',missing);dump('changes.json',changes);dump('coverage_summary.json',counts)
dump('external_sources.json',[{'key':k,'label':v[0],'url':v[1],'consulted':'2026-11-22'} for k,v in URLS.items()])
dump('reading_decisions.json',{'read_ranges':{b:[1,len(v['questions'])] for b,v in R['banks'].items()},'all_source_and_correction_items_read':True,'visualContactSheetsViewed':[p.name for p in sorted((HERE/'visual').glob('*.jpg'))],'limits':missing})
dump('details_absent_in_original.json',details_missing)
(HERE/'REPORT.md').write_text(f'''# SSH — préparation V6\n\n274 QCM et 1 370 propositions des quatre séries ont été comparés un par un aux huit PDF fournis. Les textes, clés et détails ont été relus dans leur intégralité. Les glyphes absents de l’extraction et la ligne D/E de l’ACC 34 ont été contrôlés sur les rendus. Aucune omission supplémentaire de QCM n’est prouvée dans ces quatre séries.\n\n## Résultat\n\n- 272 clés utilisables, deux questions hors note : colle 2, QCM 11–12, dont le corrigé concerne un autre sujet.\n- 274 copies sujet et 274 copies du document de correction ; deux de ces dernières sont explicitement signalées comme non correspondantes.\n- 15 limites de capture corrigées pour exclure les titres de cours du QCM suivant.\n- Énoncé commun ACC 25–26 placé dans un bloc partagé.\n- {counts['notesAdded']} nouvelles notes après correction ; les {counts['notesBefore']} notes antérieures et leurs identifiants sont conservés. {counts['warningHintsMoved']} avertissements dévoilant une réponse déplacés après validation.\n- Aucun changement arbitraire de clé, de question, de proposition, d’ID ou de barème. Les deux clés inutilisables restent hors note.\n\n## Contrôles et limites\n\nLes {panels} panneaux ont été rendus pour vérifier leur géométrie et leur lisibilité technique. 21 planches de pages originales appariées ont été vues : les cas multipages, les bornes et les ambiguïtés, sans prétendre avoir vu individuellement chacun des panneaux. La seconde lecture indépendante doit vérifier l’ensemble.\n\nLa colle 1 et l’EB sont des PDF remis en page déjà présents parmi les documents fournis. Ils contiennent des commentaires antérieurs, parfois personnalisés. Les copies montrent exactement ces pièces ; elles ne sont pas présentées comme une certification d’originaux institutionnels. Leurs versions officielles non remaniées, la correction adéquate de colle 2 Q11–12 et les ronéos pour arbitrer les réserves sont demandées dans missing.json. Aucun détail explicatif n’est inventé lorsque le document se limite à un verdict.\n''')
print(json.dumps(counts,ensure_ascii=False,indent=2))
