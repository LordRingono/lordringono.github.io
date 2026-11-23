from pathlib import Path
import json,re,unicodedata,collections,difflib,fitz
ROOT=Path('/workspace/scratch/f3cb3bb97377');V=ROOT/'work/site_v6/embryologie/verify';P=ROOT/'work/site_v6/embryologie/prepare'
base=json.loads((ROOT/'work/site_v6/baseline_exams.json').read_text());new=json.loads((P/'reviewed.json').read_text())['banks'];blocks=json.loads((V/'sourceblocks.json').read_text());ci=json.loads((V/'coverage_initial.json').read_text());cis={(r['bank'],r['id']):r for r in ci}
def norm(t):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t.replace('œ','oe')).encode('ascii','ignore').decode().lower())
proof=[];flags=[]
for bank,b in new.items():
 for q in b['questions']:
  old=next(z for z in base[bank]['questions'] if z['id']==q['id']);ini=cis[bank,q['id']]
  block=next(bl for bl in blocks[bank] if bl['i']==next(x['i'] for x in blocks[bank] if x['num']==int(q['sourceNumber']) and x['page']==ini['page']))
  for k,exp in q.get('explanations',{}).items():
   if exp==old.get('explanations',{}).get(k):continue
   srcitem=next((x for x in ini['items'] if x['id']==k),None)
   segs=srcitem['sourceSegments'] if srcitem else []
   raw=' | '.join(x['text'] for x in segs);colored=' | '.join(c['text'] for s in segs for c in s['colored']);quotes=re.findall('« ([^»]+) »',exp)
   sourceMatched=all(norm(t) in norm(raw) for t in quotes) if quotes else norm(exp) in norm(raw)
   if not sourceMatched:flags.append({'bank':bank,'id':q['id'],'item':k,'detail':exp,'raw':raw})
   proof.append({'bank':bank,'id':q['id'],'item':k,'newDetail':exp,'rawSourceSegments':raw,'coloredSpans':colored,'sourcePage':ini['page'],'literalTextMatched':sourceMatched})
(V/'detail_proofs.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2));(V/'detail_flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('changed details',len(proof),'literal source matched',sum(p['literalTextMatched'] for p in proof),'flags',len(flags))
for x in flags:print(x)
