from pathlib import Path
import json,re,unicodedata

ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'quality/independent_keys.json').read_text())
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).lower() if c.isalnum())
def main(group):
    p=ROOT/group/'reviewed.json'
    if not p.exists():return
    banks=json.loads(p.read_text())['banks'];differences=[];covered=[]
    for r in records:
        if r['bank'] not in banks:continue
        q=next(q for q in banks[r['bank']]['questions'] if q['id']==r['id'])
        if r['independent_key']!=q['answer']:differences.append({'bank':r['bank'],'id':r['id'],'type':'key','expected':r['independent_key'],'actual':q['answer']})
        assert len(r['items'])==len(q['options'])
        for i,o in zip(r['items'],q['options']):
            assert i['id']==o['id'],(r['bank'],r['id'],i['id'],o['id'])
            ex=q.get('explanations',{}).get(i['id'],'')
            trimmed=re.sub(r'^(Vrai|Faux)\s*\.\s*','',ex,flags=re.I)
            statement_same=norm(o['text'])==norm(i['subject']['text'])
            detail_same=norm(trimmed)==norm(i['source_explanation'])
            record={'bank':r['bank'],'id':r['id'],'source_number':r['source_number'],'item':i['id'],'subject_original':i['subject']['text'],'subject_final':o['text'],'detail_original':i['source_explanation'],'detail_final':ex,'verdict_original':i['verdict'],'verdict_final':i['id'] in q['answer'],'statement_same':statement_same,'detail_same':detail_same}
            covered.append(record)
            if not statement_same or not detail_same:differences.append(record)
    (ROOT/'quality'/f'{group}_comparison.json').write_text(json.dumps({'questions':len({(r['bank'],r['id']) for r in covered}),'items':len(covered),'differences':differences,'all_item_comparisons':covered},ensure_ascii=False,indent=2))
    print(group,len(covered),'items',len(differences),'differences')
    print(json.dumps(differences,ensure_ascii=False,indent=2))

for group in ['tc','tn','te_tech']:main(group)
