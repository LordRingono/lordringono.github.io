from pathlib import Path
import json,re,hashlib,unicodedata,zipfile
import fitz
from PIL import Image,ImageDraw
from lxml import etree

V=Path(__file__).resolve().parent;P=V.parent/'prepare';O=V/'visual';O.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text())
def write(name,data):(V/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
R=load(P/'reviewed.json')['banks']; C=load(P/'crops.json');A=load(P/'audit.json');M=load(P/'source_manifest.json');VM=load(V/'visual_manifest.json')
docs={}
def doc(path):
 if path not in docs:docs[path]=fitz.open(path)
 return docs[path]
def render(file,page,name,rect=None,scale=1.5):
 pg=doc(file)[page-1];pm=pg.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=fitz.Rect(rect) if rect else None,alpha=False)
 path=O/name;pm.save(path);return str(path)
critical=[]
for x in VM:
 if x.get('number') in [13,17,30,40,44,48,55]:
  p=x['capture'];path=render(p['file'],p['page'],'critical_figure_%02d_full.png'%x['number'])
  critical.append({'number':x['number'],'capture':p,'fullPageRender':path,'imageBoxes':[list(b['bbox']) for b in doc(p['file'])[p['page']-1].get_image_info()]})
for bank,role,page in [('bio.cm5','subject',3),('bio.cm6','subject',1),('bio.cm6','subject',2),('bio.cm3','subject',1),('bio.cm8','subject',2),('bio.cm6','correction',2)]:
 m=next(x for x in M if x.get('bank')==bank and x.get('role')==role)
 critical.append({'bank':bank,'role':role,'page':page,'fullPageRender':render(m['pdf'],page,bank+'_'+role+'_p'+str(page)+'.png')})
write('critical_visual_manifest.json',critical)

def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('−','-').replace('–','-').replace('’',"'")
 return re.sub(r'[^\w+<>-]','',s).casefold()
strong=[]
for row in load(V/'independent_extraction.json'):
 subj='\n'.join(x['text'] for x in row['roles']['subject']);corr='\n'.join(x['text'] for x in row['roles']['correction'])
 for i in row['items']:
  if not norm(i['statement']) in norm(subj):strong.append({'bank':row['bank'],'id':row['id'],'item':i['id'],'field':'statement','text':i['statement']})
  if i['explanation'] and not norm(i['explanation']) in norm(corr):strong.append({'bank':row['bank'],'id':row['id'],'item':i['id'],'field':'explanation','text':i['explanation']})
write('strong_symbol_mismatches.json',strong)

clean=[]
for r in A:
 if not r.get('cleanSubject'):continue
 b,i=r['bank'],r['id'];q=next(x for x in R[b]['questions'] if x['id']==i);cr=next(x for x in C if x['bank']==b and x['id']==i)
 fresh='\n'.join(doc(r['subject']['file'])[p-1].get_text(sort=True) for p in r['subject']['pages'])
 cps=[p for p in cr['subject'] if 'Annales_compilation' in p['file']]
 new='\n'.join(doc(p['file'])[p['page']-1].get_text(clip=fitz.Rect(p['rect']),sort=True) for p in cps)
 edition=[]
 for p in cps:
  full=doc(p['file'])[p['page']-1].get_text(sort=True)
  edition.extend(line for line in full.splitlines() if re.search('(?:Session|20[12][0-9]|201[0-9])',line))
 # Store fresh preceding headings from original, not audit text.
 original_head=[]
 for pn in range(max(1,min(r['subject']['pages'])-2),max(r['subject']['pages'])+1):
  for line in doc(r['subject']['file'])[pn-1].get_text(sort=True).splitlines():
   if re.search(r'(?:Annales|[Ss]ession|20[12][0-9]\s*[-–]\s*20[12][0-9])',line):original_head.append({'page':pn,'text':line})
 images=[]
 for j,p in enumerate(cps):images.append(render(p['file'],p['page'],'clean_%s_%s_%s.png'%(b,i,j),p['rect'],1.4))
 clean.append({'bank':b,'id':i,'originalFile':r['subject']['file'],'originalPages':r['subject']['pages'],'compilationPanels':cps,'freshCompilationHeaders':edition,'freshThematicHeaders':original_head,'itemChecks':[{'item':o['id'],'text':o['text'],'inFreshThematicPage':norm(o['text']) in norm(fresh),'inFreshCompilationPanel':norm(o['text']) in norm(new)} for o in q['options']],'renders':images})
write('clean_subject_checks.json',clean)
# One readable original crop per tile, never recompose a claimed original.
tiles=[]
for r in clean:
 ims=[Image.open(p).convert('RGB') for p in r['renders']]
 w=max(im.width for im in ims);h=sum(im.height for im in ims)
 full=Image.new('RGB',(w,h),'white');yy=0
 for im in ims:full.paste(im,(0,yy));yy+=im.height
 full.thumbnail((720,1400))
 tile=Image.new('RGB',(740,1450),'#eeeeee');ImageDraw.Draw(tile).text((10,5),r['bank']+'/'+str(r['id']),fill='black');tile.paste(full,(10,30));tiles.append(tile)
for j in range(0,len(tiles),2):
 sheet=Image.new('RGB',(1480,1450),'#dddddd')
 for k,t in enumerate(tiles[j:j+2]):sheet.paste(t,(k*740,0))
 sheet.save(O/('clean_sheet_%02d.jpg'%(j//2+1)),quality=92)

word=[]
for m in M:
 if not m.get('converted'):continue
 with zipfile.ZipFile(m['original']) as z:
  xml=etree.fromstring(z.read('word/document.xml'))
  texts=xml.xpath('//w:t/text()',namespaces={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
  rects=[dict(x.attrib) for x in xml.xpath('//*[local-name()="srcRect"]')]
 pdftext='\n'.join(p.get_text(sort=True) for p in doc(m['pdf']))
 entry={'bank':m['bank'],'role':m['role'],'original':m['original'],'pdf':m['pdf'],'shaOriginalMatches':hashlib.sha256(Path(m['original']).read_bytes()).hexdigest()==m['originalSha256'],'shaPdfMatches':hashlib.sha256(Path(m['pdf']).read_bytes()).hexdigest()==m['pdfSha256'],'wordImageSourceCropRectangles':rects,'paragraphCount':len(texts),'pdfPages':len(doc(m['pdf'])),'nonemptyWordTextRunsMissingInPdf':[t for t in texts if len(norm(t))>10 and norm(t) not in norm(pdftext)]}
 if m.get('providedPdf'):
  provided='\n'.join(p.get_text(sort=True) for p in doc(m['providedPdf']))
  entry['providedPdfNormalizedMatches']=norm(provided)==norm(pdftext)
 word.append(entry)
write('word_original_checks.json',word)
print(json.dumps({'critical':len(critical),'symbolMismatches':len(strong),'cleanSubjects':len(clean),'cleanItemFlags':sum(not x['inFreshThematicPage'] or not x['inFreshCompilationPanel'] for r in clean for x in r['itemChecks']),'wordDocuments':len(word),'wordRunsMissing':sum(len(r['nonemptyWordTextRunsMissingInPdf']) for r in word)},ensure_ascii=False))
