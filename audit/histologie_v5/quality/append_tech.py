from pathlib import Path
import json,re,unicodedata

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'quality'
base=json.loads((ROOT/'baseline_exams.json').read_text())['histo.autotech']['questions']
records=[r for r in json.loads((OUT/'independent_keys.json').read_text()) if r['bank']!='histo.autotech']
source_to_id={1:1,2:2,3:3,4:4,5:5,7:6,8:12,9:7,10:8,13:9,14:10,16:13,17:11}

def norm(s):return re.sub(r'\s+',' ',s).strip()
def letters(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).lower() if c.isalnum())
def extract(name):
    raw=(OUT/name).read_text()
    lines=[];page=0
    for line in raw.splitlines():
        m=re.match(r'^PAGE (\d+)',line)
        if m:page=int(m[1]);continue
        if line.strip() and line.strip()!='Document C':lines.append((line,page))
    starts=[]
    for i,(line,page) in enumerate(lines):
        m=re.match(r'^Q(?:RM|RU)\s*(\d+)',line)
        if m:starts.append((i,int(m[1])))
    questions={}
    for ix,(start,num) in enumerate(starts):
        stop=starts[ix+1][0] if ix+1<len(starts) else len(lines)
        chunk=lines[start:stop];items=[];heading=[]
        for line,page in chunk:
            m=re.match(r'^([A-J])\.\s*(.*)$',line)
            if m:
                if not m[2].strip():continue
                items.append({'label':m[1],'text':m[2],'pages':[page]})
            elif items:
                items[-1]['text']+=' '+line
                if page not in items[-1]['pages']:items[-1]['pages'].append(page)
            else:heading.append(line)
        for item in items:item['text']=norm(item['text'])
        assert len(items)==5,(name,num,len(items))
        questions[num]={'heading':{'text':norm(' '.join(heading)),'page':lines[start][1]},'items':items}
    assert set(questions)==set(source_to_id)
    return questions

subject=extract('Autotest_raw.txt');correction=extract('autotest correction_raw.txt')
for num,s in subject.items():
    c=correction[num];qid=source_to_id[num]
    bq=next((q for q in base if q['id']==qid),None)
    rec={'bank':'histo.autotech','id':qid,'source_number':num,'subject_file':'Autotest.pdf','correction_file':'autotest correction.pdf','subject_heading':s['heading'],'correction_heading':c['heading'],'subject_context':[],'correction_context':[],'baseline_key':bq['answer'] if bq else None,'items':[],'newly_recovered':bq is None}
    for sub,corr in zip(s['items'],c['items']):
        # Q8's patientVrai is intentionally unseparated in the original PDF.
        marker=re.search(r'(vrai|faux)',corr['text'],re.I)
        assert marker,(num,corr)
        verdict=marker[0].lower()=='vrai';prefix=corr['text'][:marker.start()].strip();detail=corr['text'][marker.end():].strip(' .,;:')
        letter=corr['label']
        bo=next((o for o in bq['options'] if o['id']==letter),None) if bq else None
        ex=bq.get('explanations',{}).get(letter,'') if bq else None
        rec['items'].append({'id':letter,'subject':sub,'corrected':corr,'literal_marker':marker[0],'verdict':verdict,'verdict_method':'explicit_marker','corrected_statement':prefix,'source_explanation':detail,'baseline_statement':bo['text'] if bo else None,'baseline_explanation':ex,'baseline_verdict':letter in bq['answer'] if bq else None,'statement_same_as_subject':letters(sub['text'])==letters(bo['text']) if bo else None,'correction_statement_matches_subject':letters(sub['text'])==letters(prefix),'explanation_same_as_baseline':letters(detail)==letters(ex) if bq else None,'subject_label':sub['label'],'correction_label':corr['label']})
    rec['independent_key']=''.join(i['id'] for i in rec['items'] if i['verdict'])
    rec['unknown_items']=[]
    records.append(rec)

(OUT/'independent_keys.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(f'{len(records)} questions, {sum(len(r["items"]) for r in records)} items')
