from pathlib import Path
import re,json,hashlib,unicodedata,difflib
import fitz
ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'prepare'
SITE=ROOT.parents[3]/'output/site'
def dump(name,data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
def normal(t):
    t=unicodedata.normalize('NFKC',t).casefold().replace('−','-').replace('–','-').replace('’',"'")
    return re.sub(r'[^\w+<>=−-]','',t)
def lines(part):
    page=DOC[part['page']-1];rect=fitz.Rect(part['rect']);out=[]
    for b in page.get_text('dict',clip=rect)['blocks']:
      for line in b.get('lines',[]):
        text=''.join(s['text'] for s in line['spans']).strip()
        if text:out.append({'text':text,'rect':line['bbox'],'page':part['page'],'spans':line['spans']})
    return sorted(out,key=lambda a:(round(a['rect'][1],1),a['rect'][0]))
def segments(ls):
    starts=[(i,re.match(r'^\s*([A-E])\s*[.\)]\s*(.*)',l['text'])) for i,l in enumerate(ls)]
    starts=[(i,m) for i,m in starts if m]
    out=[]
    for j,(i,m) in enumerate(starts):
        end=starts[j+1][0] if j+1<len(starts) else len(ls)
        rows=ls[i:end]
        out.append({'letter':m[1],'text':' '.join([m[2]]+[l['text'] for l in rows[1:]]).strip(),'lines':rows})
    return out

if __name__=='__main__':
 DOC=fitz.open(SITE/'sources/Annales_compilation.pdf')
 prepared=json.loads((PREP/'reviewed.json').read_text())['banks'];cr=json.loads((PREP/'crops.json').read_text())
 lookup={(r['bank'],r['id']):r for r in cr};rows=[];flags=[];group={}
 for bank,exam in prepared.items():
  for q in exam['questions']:
   source=lookup[bank,q['id']];sub=[];cor=[];grid=[]
   for part in source['subject']:sub.extend(lines(part))
   for part in source['correction']:
    (grid if 'grille' in part.get('fileLabel','').lower() else cor).extend(lines(part))
   # Split on the stand-alone key printed between repeated options and details.
   keys=[i for i,l in enumerate(cor) if re.fullmatch(r'[ABCDE]{1,5}',l['text'])]
   keyi=next((i for i in keys if any(re.match(r'A\s*[.)]\s*(VRAI|FAUX)',l['text'],re.I) for l in cor[i+1:i+12])),None)
   first=cor[:keyi] if keyi is not None else cor
   detail=cor[keyi+1:] if keyi is not None else []
   subj_segments=segments(sub);corrected_segments=segments(first);detail_segments=segments(detail)
   # Source frames may include shared contexts before the question: the final
   # A–E run is the one attached to the numbered question, not figure labels.
   ss=subj_segments[-5:];cc=corrected_segments[-5:];dd=detail_segments[-5:]
   grid_text=' '.join(l['text'] for l in grid)
   row={'bank':bank,'id':q['id'],'series':q['sourceSet'],'number':q['sourceNumber'],'subjectLines':sub,'correctedLines':cor,'gridLines':grid,'gridLiteral':grid_text,'detailedKey':cor[keyi]['text'] if keyi is not None else None,'subjectItems':ss,'correctedItems':cc,'detailItems':dd,'preparedAnswer':q.get('answer'),'preparedNotes':q.get('reviewNotes',[]),'items':[]}
   for j,o in enumerate(q['options']):
    s=ss[j] if len(ss)==5 else {};c=cc[j] if len(cc)==5 else {};d=dd[j] if len(dd)==5 else {}
    entry={'letter':o['id'],'preparedText':o['text'],'subjectLiteral':s.get('text'),'correctedLiteral':c.get('text'),'detailedLiteral':d.get('text'),'preparedDetail':q.get('explanations',{}).get(o['id'],''),'image':o.get('image'),'printedSubjectLetter':s.get('letter'),'printedCorrectedLetter':c.get('letter'),'printedDetailLetter':d.get('letter')}
    for label,a,b in [('subject',s.get('text',''),o['text']),('detail',d.get('text',''),entry['preparedDetail'])]:
      if normal(a)!=normal(b):flags.append({'bank':bank,'id':q['id'],'series':q['sourceSet'],'number':q['sourceNumber'],'item':o['id'],'kind':label,'fresh':a,'prepared':b,'similarity':difflib.SequenceMatcher(None,normal(a),normal(b)).ratio(),'image':o.get('image')})
    row['items'].append(entry)
   rows.append(row);group.setdefault(q['sourceSet'],[]).append(row)
 (ROOT/'readings').mkdir(exist_ok=True)
 for series,rs in group.items():
  chunks=[]
  for r in sorted(rs,key=lambda r:r['number']):
   chunks.append(f"\n## Q{r['number']} | {r['bank']} id{r['id']} | grille {r['gridLiteral']} | détail {r['detailedKey']} | site {r['preparedAnswer']}\n")
   used=len(r['subjectItems'])==5 and len(r['detailItems'])==5
   if used:
    chunks.append('CONSIGNE/CONTEXTE: '+' '.join(l['text'] for l in r['subjectLines'][:next(i for i,l in enumerate(r['subjectLines']) if re.match(r'A\s*[.)]',l['text']))]))
    for item in r['items']:
     chunks.append(f"{item['letter']}: {item['subjectLiteral']}\n→ {item['detailedLiteral']}")
     if normal(item['subjectLiteral'] or '')!=normal(item['correctedLiteral'] or ''):chunks.append('RÉPÉTITION CORRIGÉ: '+str(item['correctedLiteral']))
   else:chunks.append('SUJET BRUT:\n'+'\n'.join(l['text'] for l in r['subjectLines'])+'\nCORRIGÉ BRUT:\n'+'\n'.join(l['text'] for l in r['correctedLines']))
   chunks.extend('NOTE: '+n['text'] for n in r['preparedNotes'])
  (ROOT/'readings'/f'{series}.txt').write_text('\n'.join(chunks))
 dump('independent_source.json',rows);dump('comparison_flags.json',flags)
 print({'questions':len(rows),'items':sum(len(r['items']) for r in rows),'flags':len(flags),'series':{k:len(v) for k,v in group.items()}})
