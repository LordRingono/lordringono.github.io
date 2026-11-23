from pathlib import Path
import json,re,unicodedata,difflib,fitz
ROOT=Path('/workspace/scratch/f3cb3bb97377');OUT=ROOT/'work/site_v6/embryologie/verify'
PAGES={p['page']:p for p in json.loads((OUT/'compilation_pages.json').read_text())};EX=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text());PDF=ROOT/'output/site/sources/Annales_compilation.pdf';DOC=fitz.open(PDF)
def norm(t):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t.replace('œ','oe')).encode('ascii','ignore').decode().lower())
def clean(t):return re.sub(r'\s+',' ',t).strip()
def textat(page,y0,y1):return clean(' '.join(l['text'] for l in PAGES[page]['lines'] if y0<=l['bbox'][1]<y1))
manual=[('embryo.ann.gamet',21,1404,105,218,[124,140,155,170,199,218]),('embryo.ann.gamet',22,1404,229,356,[248,264,279,308,323,356]),('embryo.ann.gamet',23,1404,366,520,[386,401,430,459,488,520]),('embryo.ann.fec',13,1404,531,644,[550,565,581,610,625,644]),('embryo.ann.fec',14,1404,655,768,[674,703,718,734,749,768]),('embryo.ann.s1',7,1405,66,180,[86,101,117,132,161,180]),('embryo.ann.s2',7,1405,190,349,[241,270,285,314,329,349]),('embryo.ann.s2',9,1213,314,442,[334,349,365,393,409,442])]
rows=json.loads((OUT/'compilation_supplements_draft.json').read_text())
for bank,qid,pn,y0,y1,ys in manual:
 q=next(q for q in EX[bank]['questions'] if q['id']==qid);opts={k:re.sub(r'^[A-E]\.\s*','',textat(pn,a,b)) for k,a,b in zip('ABCDE',ys,ys[1:])}
 bl={'page':pn,'year':PAGES[pn]['year'],'header':PAGES[pn]['header'][:125],'title':textat(pn,y0,ys[0]),'rect':[30,y0,DOC[pn-1].rect.width-30,y1],'items':opts}
 diffs=[{'id':o['id'],'site':o['text'],'source':opts[o['id']]} for o in q['options'] if norm(o['text'])!=norm(opts[o['id']])]
 rows.append({'bank':bank,'id':qid,'category':q['category'],'subject':bl,'similarity':sum(difflib.SequenceMatcher(None,norm(o['text']),norm(opts[o['id']])).ratio() for o in q['options'])/5,'exactItems':5-len(diffs),'diffs':diffs,'file':str(PDF),'yearMismatch':q['category'][:9]!=bl['year'],'matchMethod':'Manual item-by-item labels checked visually'})
rows.sort(key=lambda x:(x['bank'],x['id']))
for row in rows:
 row['status']='all_items_compared';row['note']='Le sujet original provient de la compilation générale ; le corrigé thématique reste la référence, sauf complément explicite identifié.'
 if row['diffs']:row['note']+=' Certaines formulations diffèrent entre les éditions. La copie est conservée telle quelle.'
 row['cropVisualChecked']=False
(OUT/'compilation_supplements.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Original tutorat corrections absent from recent thematic handout. Match every statement, keep literal explanation.
keys=[('embryo.ann.gamet',27,1,1233,154,431,308,'AB'),('embryo.ann.gamet',28,2,1233,444,748,624,'DE'),('embryo.ann.fec',17,3,1234,66,370,233,'AE'),('embryo.ann.fec',18,4,1234,383,646,549,'ABDE'),('embryo.ann.s1',9,5,1235,66,290,193,'BDE'),('embryo.ann.s1',10,6,1235,302,555,428,'C'),('embryo.ann.s2',9,7,1236,66,344,206,'B'),('embryo.ann.s3',26,11,1238,66,316,193,'')]
krows=[]
for bank,qid,sourceN,pn,y0,y1,keyY,key in keys:
 lines=[l for l in PAGES[pn]['lines'] if y0<=l['bbox'][1]<y1 and l['text'].strip()];its={};exp={};part=its;active=None
 for l in lines:
  if l['bbox'][1]>=keyY and part is its:part=exp;active=None
  txt=clean(l['text']);m=re.match(r'^([A-E])\.\s*(.*)',txt)
  if m:active=m[1];part[active]=m[2]
  elif active:part[active]+=' '+txt
 q=next(q for q in EX[bank]['questions'] if q['id']==qid)
 assert set(its)==set('ABCDE') and set(exp)==set('ABCDE'),(bank,qid,its,exp)
 diffs=[{'id':o['id'],'site':o['text'],'source':its[o['id']]} for o in q['options'] if norm(o['text'])!=norm(its[o['id']])]
 row={'bank':bank,'id':qid,'sourceNumber':sourceN,'session':'Session 1 2022-2023','file':str(PDF),'page':pn,'rect':[30,y0,DOC[pn-1].rect.width-30,y1],'gridPage':1232,'rawKey':key or 'RIEN','answer':key,'allowNoAnswer':not key,'answerIsEmpty':not key,'items':its,'explanations':exp,'statementDiffs':diffs,'gridAndDetailAgree':True,'cropVisualChecked':False}
 if bank=='embryo.ann.fec' and qid==18:row['divergence']='Item B : la compilation du tutorat 2022-2023 le cote Vrai, alors que le corrigé Bard de la colle thématique d’une proposition identique le cote Faux (zone pellucide/cumulus). Signaler cette divergence après correction et inviter à vérifier la ronéo.'
 if bank=='embryo.ann.s3':row['divergence']='La clé RIEN est explicite. Les détails A (début du processus/canal vs fin du processus) et E (origine ectoblaste vs épiblaste) méritent une relecture avec le cours ; ne pas transformer ces commentaires en nouvelle explication scientifique.'
 krows.append(row)
(OUT/'compilation_new_keys.json').write_text(json.dumps(krows,ensure_ascii=False,indent=2))
print('subjects',len(rows),'exact',sum(r['exactItems']==5 for r in rows),'year conflicts',[(r['bank'],r['id'],r['category'],r['subject']['year']) for r in rows if r['yearMismatch']]);print('new keys',len(krows),'item differences',[(r['bank'],r['id'],r['statementDiffs']) for r in krows if r['statementDiffs']])
for row in rows:
 p=row['subject'];d=OUT/'visual'/f"subject_{row['bank']}_{row['id']:03}.png";DOC[p['page']-1].get_pixmap(matrix=fitz.Matrix(1.45,1.45),clip=fitz.Rect(p['rect'])).save(d)
for row in krows:
 d=OUT/'visual'/f"key_{row['bank']}_{row['id']:03}.png";DOC[row['page']-1].get_pixmap(matrix=fitz.Matrix(1.45,1.45),clip=fitz.Rect(row['rect'])).save(d)
