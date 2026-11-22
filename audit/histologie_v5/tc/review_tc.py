from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
import json,re,copy,hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
PAIRS={
 'histo.tc1':['Autotest TC1 nonCO(1).docx','correction autotest TC1(1).docx'],
 'histo.tc2':['autotest TC2(1).docx','CORRECTION autotest TC2(1).docx'],
 'histo.tc3':['AUTOTEST TC3 2025(1).docx','CORRECTION AUTOTEST TC3 OS(2).docx'],
}
def norm(s):return re.sub(r'\s+',' ',s).strip()
def text(p):
 s=''
 for e in p._p.iter():
  if e.tag in {qn('w:t'),qn('m:t')}:s+=e.text or ''
  elif e.tag==qn('w:sym'):
   font=e.get(qn('w:font'));char=e.get(qn('w:char'))
   symbols={('Symbol','F061'):'α',('Wingdings','F0E0'):'→'}
   assert (font,char) in symbols,(font,char)
   s+=symbols[font,char]
 return norm(s)
def parse(bank,filename):
 doc=Document(ROOT/'source'/filename);questions=[];current=None
 for i,p in enumerate(doc.paragraphs):
  s=text(p)
  if not s:continue
  heading=None
  m=re.match(r'(?:(QR[MU])\s*)?(\d+)\s*[):]\s*(.*)',s)
  if m:heading={'type':m[1] or 'QCM','number':int(m[2]),'stem':m[3]}
  elif bank=='histo.tc2' and s in ['Le tissu adipeux brun est caractérisé par :','A propos du tissu adipeux']:
   heading={'type':'QCM','number':len(questions)+1,'stem':s}
  if heading:
   current={**heading,'paragraph':i,'items':[]};questions.append(current)
  elif current:
   current['items'].append({'paragraph':i,'text':s})
 return questions

def main():
 baseline=json.loads((ROOT/'baseline_exams.json').read_text());reviewed={'banks':{}};audit=[];diffs=[]
 for bank,(subjectfile,correctionfile) in PAIRS.items():
  subj=parse(bank,subjectfile);corr=parse(bank,correctionfile)
  assert len(subj)==len(corr)==len(baseline[bank]['questions'])
  reviewed['banks'][bank]={'questions':[]}
  for old,s,c in zip(baseline[bank]['questions'],subj,corr):
   assert s['number']==c['number']
   assert len(s['items'])==len(c['items'])==len(old['options']),(bank,s['number'],len(s['items']),len(c['items']))
   q=copy.deepcopy(old);q['question']=s['stem'];q['sourceQuestionNumber']=s['number']
   q['sourceSubject']=subjectfile;q['sourceCorrection']=correctionfile
   q['explanations']={};answer='';items=[]
   for opt,si,ci in zip(q['options'],s['items'],c['items']):
    original=si['text'];ctext=ci['text'];matches=list(re.finditer(r'\b(VRAI|FAUX|V|F)\b',ctext,re.I));assert matches,(bank,s['number'],ctext)
    # Verdict appears after the proposition. Full word check prevents matching plurals in the proposition.
    m=matches[0];verdict=m.group(1);before=norm(ctext[:m.start()]);detail=norm(ctext[m.end():]).lstrip(' ,.')
    truth=verdict.upper() in ['V','VRAI']
    if truth:answer+=opt['id']
    opt['text']=original
    subject_normalization=''
    if bank=='histo.tc1' and s['number']==11 and opt['id']=='B':
     opt['text']=original.replace('αprésentent','α présentent')
     subject_normalization='Espace typographique rétabli entre le symbole α et « présentent » ; aucun changement de fond.'
    explanation=('Vrai.' if truth else 'Faux.')+(' '+detail if detail else '')
    variant=''
    if before!=original:
     if bank=='histo.tc1' and s['number']==11 and opt['id']=='E':
      variant='Le corrigé précise que la striation est visible en MET.'
      explanation+=' '+variant
     else:variant='Variation de formulation du corrigé conservée dans la capture ; énoncé du sujet non corrigé conservé.'
    q['explanations'][opt['id']]=explanation
    items.append({'id':opt['id'],'subject':original,'renderedSubject':opt['text'],'subjectNormalization':subject_normalization,'subjectParagraph':si['paragraph'],'correction':ctext,'correctionParagraph':ci['paragraph'],'correctionStatement':before,'literalVerdict':verdict,'truth':truth,'detail':detail,'renderedExplanation':explanation,'variation':variant,'oldStatement':next(o['text'] for o in old['options'] if o['id']==opt['id']),'oldExplanation':old.get('explanations',{}).get(opt['id'],''),'oldTruth':opt['id'] in (old.get('answer') or '')})
   q['answer']=answer
   if not answer:
    q['answerIsEmpty']=True;q['allowNoAnswer']=True
    if q.get('warning')=='Cette question est conservée hors note faute de correction exploitable.':q['warning']=''
   if bank=='histo.tc1' and s['number']==11:
    q.setdefault('reviewNotes',[]).append({
     'bank':bank,'id':q['id'],'items':['E'],'kind':'source_conflict',
     'text':'Le sujet écrit « 67nM » et le corrigé « 67Nm ». La ronéo TC1 indique une périodicité de 67 nm : l’unité attendue est le nanomètre (nm). La réponse Vrai du corrigé est conservée ; vérifiez cette unité dans la ronéo en cas de doute.',
     'refs':[
      {'file':subjectfile,'page':2,'label':'Question 11 E : unité du sujet original'},
      {'file':correctionfile,'page':2,'label':'Question 11 E : unité du corrigé original'},
      {'file':'TC1 2026 - CG non corrigées - ACTUALISE.pdf','page':13,'label':'Périodicité de 67 nm des fibrilles de collagène','href':'sources/revision_v4/TC1_2026_CG_non_corrigees_ACTUALISE_4b0f419e52.pdf#page=13'}
     ],
     'sourceVerdict':'Item E : Vrai selon le corrigé original',
     'reviewedItemText':{'E':next(o['text'] for o in q['options'] if o['id']=='E')},
     'reviewedExplanation':{'E':q['explanations']['E']},
     'noteId':'histo-v5-tc1-q11'
    })
   if bank=='histo.tc3' and s['number']==8:
    q.setdefault('reviewNotes',[]).append({
     'bank':bank,'id':q['id'],'items':['D','E'],'kind':'source_conflict',
     'text':'Le sujet présente cette question comme une QRU, mais le corrigé original indique explicitement « Vrai » pour D et pour E. La clé DE est donc conservée. Vérifiez dans la ronéo ou auprès de l’enseignant si la mention QRU est une erreur de titre.',
     'refs':[
      {'file':subjectfile,'page':1,'label':'QRU 8 : titre du sujet original'},
      {'file':correctionfile,'page':2,'label':'Question 8 : D et E explicitement marqués Vrai'}
     ],
     'sourceVerdict':'Clé de référence : DE',
     'reviewedItemText':{i:next(o['text'] for o in q['options'] if o['id']==i) for i in ['D','E']},
     'reviewedExplanation':{i:q['explanations'][i] for i in ['D','E']},
     'noteId':'histo-v5-tc3-q8'
    })
   if bank=='histo.tc3' and s['number']==9:
    q['generalExplanation']='Attention : ne pas confondre l’ossification primaire avec les centres d’ossification primaire (précision du corrigé original).'
   for note in q.get('reviewNotes',[]):
    if 'reviewedItemText' in note:note['reviewedItemText']={i:next(o['text'] for o in q['options'] if o['id']==i) for i in note['items']}
    if 'reviewedExplanation' in note:note['reviewedExplanation']={i:q['explanations'][i] for i in note['items']}
   record={'bank':bank,'id':q['id'],'sourceNumber':s['number'],'sourceType':s['type'],'subjectFile':subjectfile,'correctionFile':correctionfile,'subjectHeadingParagraph':s['paragraph'],'correctionHeadingParagraph':c['paragraph'],'subjectHeading':s['stem'],'correctionHeading':c['stem'],'answer':answer,'oldAnswer':old.get('answer'),'items':items,'subjectCompared':True,'correctionCompared':True}
   audit.append(record);reviewed['banks'][bank]['questions'].append(q)
   differences={k:{'old':old.get(k),'new':q.get(k)} for k in set(old)|set(q) if old.get(k)!=q.get(k)}
   diffs.append({'bank':bank,'id':q['id'],'differences':differences})
 for fn,obj in [('reviewed.json',reviewed),('audit.json',audit),('diff.json',diffs)]: (OUT/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
 print(json.dumps({'questions':len(audit),'items':sum(len(q['items']) for q in audit),'keyChanges':[{'bank':q['bank'],'id':q['id'],'old':q['oldAnswer'],'new':q['answer']} for q in audit if q['oldAnswer']!=q['answer']],'statementVariations':[{'bank':q['bank'],'id':q['id'],'item':i['id'],'subject':i['subject'],'correction':i['correctionStatement']} for q in audit for i in q['items'] if i['variation']]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
