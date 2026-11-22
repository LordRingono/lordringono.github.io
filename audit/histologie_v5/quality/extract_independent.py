from pathlib import Path
from docx import Document
import json,re,difflib,unicodedata

ROOT=Path(__file__).resolve().parents[1]
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
PAIRS={
 'te1':['Colle orale non corrigée TE1(1).docx','Colle orale corrigée TE1(1).docx'],
 'te2':['autotest TE2 (2)(1).docx','correction autotest TE2 25(1).docx'],
 'tc1':['Autotest TC1 nonCO(1).docx','correction autotest TC1(1).docx'],
 'tc2':['autotest TC2(1).docx','CORRECTION autotest TC2(1).docx'],
 'tc3':['AUTOTEST TC3 2025(1).docx','CORRECTION AUTOTEST TC3 OS(2).docx'],
 'tn1':['autotest TN1(1).docx','CORRECTION autotest TN1(2).docx'],
 'tn2':['AUTOTEST TN2(1).docx','correction autotest TN2(3).docx'],
 'tn3':['AUTOTEST TN3(1).docx','CORRECTION AUTOTEST TN3(1).docx'],
}
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).strip()
def letters(s):return ''.join(c for c in norm(s).lower() if c.isalnum())
def paras(file):
 result=[]
 for i,p in enumerate(Document(file).paragraphs):
  text=''
  for el in p._p.iter():
   local=el.tag.split('}')[-1]
   if local=='t':text+=el.text or ''
   elif local=='sym':
    sym={k.split('}')[-1]:v for k,v in el.attrib.items()}
    text+= {('Symbol','F061'):'α',('Wingdings','F0E0'):' → '}.get((sym.get('font'),sym.get('char')),'[sym:'+sym.get('char','')+']')
  if not text.strip() or (not p.text.strip() and not p._p.xpath('.//*[local-name()="oMath"]')):continue
  result.append({'paragraph':i,'text':text,'plain_text':p.text,'math':bool(p._p.xpath('.//*[local-name()="oMath"]')),'runs':[{'text':r.text,'bold':r.bold,'color':str(r.font.color.rgb) if r.font.color and r.font.color.rgb else None} for r in p.runs if r.text]})
 return result
def blocks(bank,ps):
 if bank in {'tc2','tn1'}:
  ps=ps[1:];assert len(ps)%6==0
  return [{'source_number':i//6+1,'heading':ps[i],'items':ps[i+1:i+6]} for i in range(0,len(ps),6)]
 starts=[]
 regex=r'^(\d+)\)' if bank=='tc1' else r'^Q(?:CM|RM|RU)\s*(\d+)'
 for i,p in enumerate(ps):
  m=re.match(regex,norm(p['text']))
  if m:starts.append((i,int(m[1])))
 out=[]
 for n,(i,num) in enumerate(starts):
  j=starts[n+1][0] if n+1<len(starts) else len(ps)
  items=ps[i+1:j];context=[];heading=ps[i]
  if bank=='tn2' and num==7:context=items[:5];items=items[5:]
  if bank=='tn3' and num==8:heading=dict(heading,text=heading['text']+' '+items[0]['text']);items=items[1:]
  out.append({'source_number':num,'heading':heading,'items':items,'context':context})
 return out

records=[];diffs=[]
for bank,(subject,correction) in PAIRS.items():
 sb=blocks(bank,paras(ROOT/'source'/subject));cb=blocks(bank,paras(ROOT/'source'/correction));bq=BASE['histo.'+bank]['questions']
 assert len(sb)==len(cb)==len(bq),(bank,len(sb),len(cb),len(bq))
 for s,c,q in zip(sb,cb,bq):
  assert s['source_number']==c['source_number'];assert len(s['items'])==len(c['items'])==len(q['options']),(bank,s['source_number'],len(s['items']),len(c['items']),len(q['options']))
  rec={'bank':'histo.'+bank,'id':q['id'],'source_number':s['source_number'],'subject_file':subject,'correction_file':correction,'subject_heading':s['heading'],'correction_heading':c['heading'],'subject_context':s.get('context',[]),'correction_context':c.get('context',[]),'baseline_key':q['answer'],'items':[]}
  for sub,corr,opt in zip(s['items'],c['items'],q['options']):
   ct=corr['text'];tokens=list(re.finditer(r'\b(vrai|faux|v|f)\b',ct,re.I));tok=tokens[0] if tokens else None
   verdict=None;method='explicit_marker';prefix=ct;detail='';literal=None
   if tok:
    literal=tok[0];verdict=literal.lower() in {'vrai','v'};prefix=ct[:tok.start()].strip();detail=ct[tok.end():].strip(' .,;:')
   elif bank=='tn2' and s['source_number']==7:
    verdict=False;method='order_question_only_E_marked_true'
   item={'id':opt['id'],'subject':sub,'corrected':corr,'literal_marker':literal,'verdict':verdict,'verdict_method':method,'corrected_statement':prefix,'source_explanation':detail,'baseline_statement':opt['text'],'baseline_explanation':q.get('explanations',{}).get(opt['id'],''),'baseline_verdict':opt['id'] in q['answer'],'statement_same_as_subject':letters(sub['text'])==letters(opt['text']),'correction_statement_matches_subject':letters(sub['text'])==letters(prefix),'explanation_same_as_baseline':letters(detail)==letters(q.get('explanations',{}).get(opt['id'],''))}
   rec['items'].append(item)
   if verdict is None or not item['statement_same_as_subject'] or not item['correction_statement_matches_subject'] or verdict!=item['baseline_verdict'] or not item['explanation_same_as_baseline']:
    diffs.append({'bank':'histo.'+bank,'id':q['id'],'source_number':s['source_number'],'item':opt['id'],'subject':sub['text'],'corrected':ct,'baseline_statement':opt['text'],'baseline_explanation':item['baseline_explanation'],'independent_explanation':detail,'independent_verdict':verdict,'baseline_verdict':item['baseline_verdict'],'math':sub['math'] or corr['math'],'statement_same':item['statement_same_as_subject'],'corrected_prefix_same':item['correction_statement_matches_subject'],'explanation_same':item['explanation_same_as_baseline']})
  rec['independent_key']=''.join(x['id'] for x in rec['items'] if x['verdict'])
  rec['unknown_items']=[x['id'] for x in rec['items'] if x['verdict'] is None]
  records.append(rec)

OUT=ROOT/'quality';(OUT/'independent_keys.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(OUT/'baseline_differences.json').write_text(json.dumps(diffs,ensure_ascii=False,indent=2))
print(json.dumps({'questions':len(records),'items':sum(len(x['items']) for x in records),'differences':len(diffs),'key_differences':[(x['bank'],x['id'],x['baseline_key'],x['independent_key']) for x in records if x['baseline_key']!=x['independent_key']]},ensure_ascii=False,indent=2))
for d in diffs:print(json.dumps(d,ensure_ascii=False))
