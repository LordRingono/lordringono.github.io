from pathlib import Path
import json,re,unicodedata,difflib
P=Path(__file__).resolve().parent
R=json.loads((P/'fresh_source_audit.json').read_text())
def norm(s):return re.sub(r'[^\w]','',unicodedata.normalize('NFKD',s).lower())
out=[]
for i,r in enumerate(R):
 if i+1==len(R) or R[i+1]['bank']!=r['bank']:continue
 nx=R[i+1];start=nx['subjectLocation']['start']
 prefix=[x['text'] for x in nx['prefixLines'] if (x['page'],x['rect'][1])<(start[0],start[1]-.7)]
 cand=[];last_e=-1
 for j,l in enumerate(r['detailLines']):
  if re.match(r'^E[.\-)]\s*(VRAI|FAUX)',l['text'],re.I):last_e=j
 for j,l in enumerate(r['detailLines']):
  if j<=last_e:continue
  t=l['text'];nt=norm(t)
  if re.match(r'^(?:Exercice\s*\d|Question\s+\d|Question à réponse)',t,re.I):cand.append((j,'titre_exercice',t))
  else:
   for x in prefix:
    ns=norm(x)
    if len(ns)>=30 and len(nt)>=25 and (nt==ns or (difflib.SequenceMatcher(None,ns,nt).ratio()>.84)):
     cand.append((j,'correspondance_contexte_sujet_suivant',t));break
 if cand:
  j,reason,text=min(cand)
  out.append({'bank':r['bank'],'id':r['id'],'next':nx['id'],'cutLine':j,'page':r['detailLines'][j]['page'],'y':r['detailLines'][j]['rect'][1]-3,'reason':reason,'tail':' '.join(x['text'] for x in r['detailLines'][j:]),'lastDetail':' '.join(x['text'] for x in r['detailLines'][max(0,j-3):j])})
(P/'boundary_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for x in out:print(f'{x["bank"]} Q{x["id"]}→{x["next"]} p{x["page"]}:{x["y"]:.1f}\n BEFORE {x["lastDetail"]}\n CUT {x["tail"][:260]}\n')
