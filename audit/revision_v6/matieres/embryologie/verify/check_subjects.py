import independent_review as R
import json,collections,re
out=[];issues=[]
for bid,b in R.BANKS.items():
 if b['questions'][0]['sourceSubject']==b['questions'][0]['sourceCorrection']:continue
 file=R.MAN[b['questions'][0]['sourceSubject']];bb=R.blocks(file)
 print('SUBJECT',bid,len(bb),'vs',len(b['questions']))
 pool=collections.defaultdict(list)
 for block in bb:pool[block['num']].append(block)
 for q in b['questions']:
  num=int(q['sourceNumber']);arr=pool[num]
  if not arr:issues.append({'bank':bid,'id':q['id'],'kind':'subject_block_unmatched'});continue
  bl=arr.pop(0);its=R.items(bl,bid=='embryo.aut.coeur');r={'bank':bid,'id':q['id'],'sourceNumber':num,'file':file,'page':bl['page'],'endPage':bl['endPage'],'head':bl['text'],'items':[]}
  for o in q['options']:
   ss=its.get(o['id'],[]);s=ss[0]['text'] if ss else '';ns=R.norm(s);no=R.norm(o['text'])
   x={'id':o['id'],'sourceText':s,'siteText':o['text'],'exact':no==ns,'contained':no in ns if no else False}
   if not x['exact']:
    issues.append({'bank':bid,'id':q['id'],'item':o['id'],'kind':'subject_item_diff','site':o['text'],'source':s})
   r['items'].append(x)
  out.append(r)
R.dump('subjects_initial.json',out);R.dump('subject_issues_initial.json',issues)
print('SUBJECTS',len(out),'ISSUES',dict(collections.Counter(x['kind'] for x in issues)))
for x in issues:print(json.dumps(x,ensure_ascii=False))
