from pathlib import Path
import json,re,unicodedata,difflib
V=Path(__file__).resolve().parent
rows=json.loads((V/'independent_extraction.json').read_text())
def n(s):return re.sub(r'[^\w]','',unicodedata.normalize('NFKC',s)).casefold()
flags=[];checked=[]
for r in rows:
 text='\n'.join(x['text'] for x in r['roles']['correction'])
 matches=list(re.finditer(r'(?m)^\s*([A-J])\s*[.)]\s*',text))
 blocks=[]
 for j,m in enumerate(matches):
  t=text[m.end():matches[j+1].start() if j+1<len(matches) else len(text)].strip()
  vs=list(re.finditer(r'\b(?:VRAI|FAUX|[VF])\b',t,re.I))
  if vs:
   vm=vs[0];blocks.append({'label':m[1],'verdict':vm.group(),'detail':t[vm.end():].lstrip(' \n,:;.')})
 for it in r['items']:
  opts=[x for x in blocks if x['label']==it['id']]
  if not opts:continue
  best=min(opts,key=lambda x:abs(len(n(x['detail']))-len(n(it['explanation']))))
  # Direct exact/case/spacing agreement is strong; exceptional native layouts are reported.
  ok=n(best['detail'])==n(it['explanation'])
  row={'bank':r['bank'],'id':r['id'],'item':it['id'],'current':it['explanation'],'extracted':best['detail'],'verdict':best['verdict'],'exactIgnoringTypography':ok}
  checked.append(row)
  if not ok:flags.append(row)
(V/'detail_completeness_checks.json').write_text(json.dumps(checked,ensure_ascii=False,indent=2))
(V/'detail_completeness_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('parsed',len(checked),'flags',len(flags))
for x in flags:
 print(x['bank'],x['id'],x['item'],'CURRENT:',x['current'],'\nSOURCE:',x['extracted'],'\n')
