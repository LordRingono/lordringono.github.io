import json,re,unicodedata,difflib,hashlib
from pathlib import Path
from collections import Counter
import fitz
V=Path(__file__).parent;P=V.parent/'prepare';WS=V.parents[3]
R=json.loads((V/'working_reviewed.json').read_text());C=json.loads((V/'working_crops.json').read_text());D=fitz.open(WS/'output/site/sources/Annales_compilation.pdf')
N={(n['bank'],n['id']):n for n in json.loads((V/'native_comparison.json').read_text())}
def norm(s):
 s=unicodedata.normalize('NFKC',s).lower().replace('’',"'").replace('–','-').replace('‐','-').replace('−','-').replace('“','"').replace('”','"')
 return re.sub(r'\s+','',s).rstrip('.')
def save(n,x):(V/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[];diffs=[];verdict_diff=[]
for c in C:
 q=next(x for x in R['banks'][c['bank']]['questions'] if x['id']==c['id']); key=q['answer'] or q.get('rawAnswer',''); code=all('Lettre ' in x.get('text','') for x in q['options'])
 cor='\n'.join(D[x['page']-1].get_text('text',clip=fitz.Rect(x['rect']),sort=True) for x in c['correction'])
 # Standalone official key separates original propositions from explanations.
 bounds=[m.start() for m in re.finditer(r'^\s*'+key+r'\s*$',cor,re.M)] if key else []
 bounds += [m.start() for m in re.finditer(r'\b[A-E]\s*[.)]\s*(?:VRAI|FAUX)\b',cor,re.I)]
 before=cor[:min(bounds)] if bounds else cor
 opts=list(re.finditer(r'^\s*([A-E])\s*[.)]\s*',before,re.M))
 cms=list(re.finditer(r'\b([A-E])\s*[.)]\s*(VRAI|FAUX)\b',cor,re.I))
 det={m[1]:m[2].upper() for m in cms}
 if c['bank']=='annales.ue3.2024-2025.s1' and q['id']==10:det['A']='FAUX'
 if c['bank']=='annales.ue3.2023-2024.s2' and q['id']==1:det={a:('VRAI' if a=='D' else 'FAUX') for a in 'ABCDE'}
 subjects={m[1]:before[m.end():opts[i+1].start() if i+1<len(opts) else len(before)].strip() for i,m in enumerate(opts)}
 row={'bank':c['bank'],'id':q['id'],'source_key':key,'items':[],'code':code}
 for o in q['options']:
  l=o['id'];prior=next(t for t in N[(c['bank'],q['id'])]['items'] if t['letter']==l)
  origin=prior['source'];corrsub=subjects.get(l)
  comparable=not code and not o.get('image') and corrsub is not None
  identical=norm(origin)==norm(corrsub or '') if comparable else None
  obj={'letter':l,'source_subject':origin,'corrected_subject':corrsub,'subject_correction_identical':identical,'detail_verdict':det.get(l),'key_verdict':'VRAI' if l in key else 'FAUX','rendered_detail':q.get('explanations',{}).get(l),'code_letter':code}
  row['items'].append(obj)
  if comparable and not identical:diffs.append({'bank':c['bank'],'id':q['id'],**obj,'ratio':round(difflib.SequenceMatcher(None,norm(origin),norm(corrsub)).ratio(),4)})
  if not code and det.get(l) !=obj['key_verdict']:verdict_diff.append({'bank':c['bank'],'id':q['id'],**obj})
 rows.append(row)
save('final_source_comparison.json',rows);save('corrected_subject_differences.json',diffs);save('verdict_differences.json',verdict_diff)
print(json.dumps({'repeat_subject_differences':len(diffs),'verdict_differences':len(verdict_diff),'rows':len(rows)},ensure_ascii=False))
for x in diffs:print(x['bank'],x['id'],x['letter'],x['ratio'],repr(x['source_subject']),repr(x['corrected_subject']))
for x in verdict_diff:print('VERDICT',x['bank'],x['id'],x['letter'],x['detail_verdict'],x['key_verdict'])
