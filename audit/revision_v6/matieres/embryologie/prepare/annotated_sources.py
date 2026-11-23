import fitz,json,pathlib,re,collections
P=pathlib.Path(__file__).parent;M=json.load(open(P/'source_manifest.json'));E=json.load(open(P/'extraction.json'))
for name,pages in E.items():
 d=fitz.open(M[name]['file'])
 for pi,p in enumerate(pages):
  page=d[pi];strike=[]
  for draw in page.get_drawings():
   for shape in draw['items']:
    if shape[0]=='re':
     r=shape[1]
     if 0<r.height<1.5 and r.width>1: strike.append(r)
    elif shape[0]=='l':
     a,b=shape[1:3]
     if abs(a.y-b.y)<1 and abs(a.x-b.x)>1:strike.append(fitz.Rect(min(a.x,b.x),a.y-.2,max(a.x,b.x),b.y+.2))
  raw={}
  for block in page.get_text('rawdict')['blocks']:
   for line in block.get('lines',[]):
    chars=[]
    for sp in line['spans']:
     for c in sp['chars']:
      r=fitz.Rect(c['bbox']);x=(r.x0+r.x1)/2
      st=any(z.x0-.5<=x<=z.x1+.5 and r.y0+.25*r.height<=(z.y0+z.y1)/2<=r.y0+.75*r.height for z in strike)
      chars.append({'c':c['c'],'color':sp['color'],'strike':st})
    raw[tuple(round(z,1) for z in line['bbox'])]=chars
  for l in p['lines']:
   chars=raw.get(tuple(round(z,1) for z in l['bbox']),[])
   l['originalText']=''.join(c['c'] for c in chars if c['color'] in [0,0xffffff] or c['strike']).strip()
   l['correctedText']=''.join(c['c'] for c in chars if not c['strike']).strip()
   def runs(test):
    chunks=[];chunk=[]
    for c in chars:
     if test(c):chunk.append(c['c'])
     elif chunk:chunks.append(''.join(chunk).strip());chunk=[]
    if chunk:chunks.append(''.join(chunk).strip())
    return ' '.join(x for x in chunks if x)
   l['struckText']=runs(lambda c:c['strike'])
   l['addedText']=runs(lambda c:c['color'] not in [0,0xffffff] and not c['strike'])
   l['hasStrike']=any(c['strike'] for c in chars)
(P/'extraction.json').write_text(json.dumps(E,ensure_ascii=False))
print('Annotated original spans and strikeouts classified from all 29 source PDF geometries.')
