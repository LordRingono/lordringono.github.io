from pathlib import Path
import re, json, copy, hashlib
from docx import Document
import fitz

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'baseline_exams.json').read_text())
OUT=ROOT/'te_tech'
OUT.mkdir(exist_ok=True)

def clean(s): return re.sub(r'\s+',' ',s).strip()

def word_questions(file):
    data=[];q=None
    for pi,p in enumerate(Document(file).paragraphs):
        text=clean(p.text)
        if not text: continue
        m=re.match(r'^(QRM|QRU|QCM)\s*(\d+)\s*:?\s*(.*)',text)
        if m:
            q={'number':int(m[2]),'type':m[1],'stem':m[3],'paragraph':pi,'items':[]};data.append(q)
        elif q:q['items'].append({'text':text,'paragraph':pi})
    return data

def verdict(text):
    # V/F are standalone in these sources, Vrai/Faux may adjoin a final word.
    m=re.search(r'(Vrai|Faux|VRAI|FAUX|vrai|faux)|(?<!\w)([VF])(?!\w)',text)
    assert m, text
    return (m[0].lower().startswith('v'),clean(text[:m.start()]),clean(text[m.end():]).lstrip(' ,:.'),m[0])

def page_lines(page):
    rows=[]
    for b in page.get_text('dict')['blocks']:
        if b['type']!=0:continue
        for l in b['lines']:
            text=''.join(s['text'] for s in l['spans']).strip()
            if not text:continue
            rows.append({'text':text,'rect':list(l['bbox'])})
    return sorted(rows,key=lambda x:(x['rect'][1],x['rect'][0]))

def pdf_questions(file):
    d=fitz.open(file);heads=[];lines=[page_lines(p) for p in d]
    for pi,ls in enumerate(lines):
        for l in ls:
            m=re.match(r'^(?:QRM|QRU|QCM)\s*(\d+)\b',l['text'])
            if m:heads.append({'number':int(m[1]),'page':pi,'y':l['rect'][1]})
    out=[]
    for k,h in enumerate(heads):
        nxt=heads[k+1] if k+1<len(heads) else {'page':len(d)-1,'y':float('inf')}
        captures=[];texts=[]
        for pi in range(h['page'],nxt['page']+1):
            lower=h['y']-.5 if pi==h['page'] else 0
            upper=nxt['y']-1 if pi==nxt['page'] else d[pi].rect.height
            ls=[l for l in lines[pi] if lower<=l['rect'][1]<upper and not re.match(r'^(EMSLB|C\.ROCHET|20\d\d\s*$)',l['text'],re.I)]
            if not ls:continue
            rect=[max(0,min(l['rect'][0] for l in ls)-7),max(0,min(l['rect'][1] for l in ls)-5),min(d[pi].rect.width,max(l['rect'][2] for l in ls)+7),min(d[pi].rect.height,max(l['rect'][3] for l in ls)+5)]
            for im in d[pi].get_image_info():
                b=im['bbox']
                if lower<=b[1]<upper:
                    rect=[min(rect[0],max(0,b[0]-5)),min(rect[1],max(0,b[1]-5)),max(rect[2],min(d[pi].rect.width,b[2]+5)),max(rect[3],min(d[pi].rect.height,b[3]+5))]
            captures.append({'file':str(Path(file).resolve()),'page':pi+1,'rect':[round(v,3) for v in rect]})
            texts.extend(l['text'] for l in ls)
        out.append({'number':h['number'],'crops':captures,'text':'\n'.join(texts)})
    return out

def note(bank,q,item,text,kind='source_conflict',refs=None):
    q.setdefault('reviewNotes',[]).append({'bank':bank,'id':q['id'],'items':[item] if item else [],'kind':kind,'text':text,'refs':refs or [],'sourceVerdict':'Clé du corrigé : '+(q['answer'] or 'aucune proposition vraie'),'noteId':f'histo-v5-{bank}-{q["id"]}-{item or "q"}'})

def refresh_notes(q):
    for n in q.get('reviewNotes',[]):
        if 'reviewedItemText' in n:n['reviewedItemText']={i:next(o['text'] for o in q['options'] if o['id']==i) for i in n['reviewedItemText']}
        if 'reviewedExplanation' in n:n['reviewedExplanation']={i:q['explanations'].get(i,'') for i in n['reviewedExplanation']}

def review_te():
    banks={};audits=[];crops=[]
    for code,subject,correction in [
      ('te1','Colle orale non corrigée TE1(1).docx','Colle orale corrigée TE1(1).docx'),
      ('te2','autotest TE2 (2)(1).docx','correction autotest TE2 25(1).docx')]:
        bank='histo.'+code
        sub=word_questions(ROOT/'source'/subject);cor=word_questions(ROOT/'source'/correction)
        subpdf=next((ROOT/'render'/f'{code}_subject').glob('*.pdf'));corpdf=next((ROOT/'render'/f'{code}_correction').glob('*.pdf'))
        subc={q['number']:q for q in pdf_questions(subpdf)};corc={q['number']:q for q in pdf_questions(corpdf)}
        assert len(sub)==len(cor)==len(BASE[bank]['questions'])
        reviewed=[]
        for old,s,c in zip(BASE[bank]['questions'],sub,cor):
            assert s['number']==c['number'] and len(s['items'])==len(c['items'])==len(old['options'])==5
            q=copy.deepcopy(old);q['question']=s['stem'];q['sourceQuestionNumber']=s['number']
            q['explanations']={};keys=[];items=[]
            for opt,si,ci in zip(q['options'],s['items'],c['items']):
                val,prefix,detail,mark=verdict(ci['text']);oid=opt['id']
                opt['text']=si['text']
                if val: keys.append(oid)
                q['explanations'][oid]=('Vrai.' if val else 'Faux.')+(' '+detail if detail else '')
                items.append({'id':oid,'subject':si['text'],'corrected':ci['text'],'sourceVerdict':mark,'verdict':val,'explanation':detail,'subjectParagraph':si['paragraph'],'correctionParagraph':ci['paragraph'],'correctedStatement':prefix,'statementMatches':clean(si['text'])==clean(prefix)})
            q['answer']=''.join(keys)
            if bank=='histo.te2' and q['id']==11:
                q['warning']='';q.pop('answerIsEmpty',None)
                q['explanations']['C']='Faux. FI : filaments intermédiaires.'
            if bank=='histo.te2' and q['id']==6:
                q['reviewNotes'][0]['text']='Item D : les deux documents ne posent pas exactement la même proposition. Le sujet dit seulement « l’espace intercellulaire au niveau des desmosomes maculaires est élargie ». Le corrigé ajoute « à 10/20 nm », puis répond Faux et précise 20–30 nm. Ce Faux porte donc sur la valeur ajoutée dans le corrigé. La ronéo confirme un espace élargi de 20–30 nm. La clé officielle est conservée, mais elle ne répond pas fidèlement à l’item du sujet ; à vérifier dans la ronéo.'
            if bank=='histo.te2' and q['id']==9:
                q['options'][1]['text']='Elle est constitutivement ouverte'
                q['reviewNotes'][0]['text']='Item B : le sujet original s’arrête à « Elle est constitutivement ». Le corrigé donne la phrase complète « Elle est constitutivement ouverte », classée Faux car l’ouverture est régulée par le Ca2+ et le pH. Le mot « ouverte » est rétabli dans l’item interactif à partir du corrigé ; les deux captures originales permettent de vérifier cette différence.'
            if bank=='histo.te2' and q['id']==17:
                note(bank,q,'A','Item A : le corrigé retient Vrai pour « cellules caliciformes gastriques » et la ronéo emploie elle-même cette expression. La terminologie mérite toutefois une clarification : en histologie normale, les cellules mucosécrétantes de l’estomac se distinguent des cellules caliciformes ; la présence de cellules caliciformes dans la muqueuse gastrique est notamment un marqueur de métaplasie intestinale. La clé officielle est conservée. Vérifier ce vocabulaire avec la ronéo et l’enseignant, en distinguant tissu normal et contexte pathologique.','possible_error',[
                    {'file':'Tissu épithélial 2 - CG - ACTUALISE.pdf','page':15,'label':'Formulation de la ronéo, page imprimée 36','href':'sources/revision_v4/Tissu_epithelial_2_CG_ACTUALISE_934413563c.pdf#page=15'},
                    {'label':'Étude originale : cellules caliciformes et métaplasie intestinale gastrique (résumé, PMID 20059269)','href':'https://pubmed.ncbi.nlm.nih.gov/20059269/'}])
            refresh_notes(q)
            reviewed.append(q)
            audits.append({'bank':bank,'id':q['id'],'sourceNumber':s['number'],'subject':subject,'correction':correction,'oldAnswer':old['answer'],'answer':q['answer'],'items':items,'reviewed':True})
            crops.append({'bank':bank,'id':q['id'],'subject':subc[s['number']]['crops'],'correction':corc[c['number']]['crops']})
        banks[bank]={'questions':reviewed}
    return banks,audits,crops

def split_pdf_question(block):
    lines=block['text'].splitlines();stem=[];items=[]
    for line in lines:
        if line.strip()=='Document C':continue
        m=re.match(r'^([A-Z])\.\s*(.*)$',line)
        if m:
            if m[2].strip():items.append({'label':m[1],'text':m[2].strip()})
        elif items:items[-1]['text']+=' '+line
        else:stem.append(line)
    heading=clean(' '.join(stem))
    return re.sub(r'^(QRM|QRU|QCM)\s*\d+\s*:?\s*','',heading),items

def review_tech():
    bank='histo.autotech';old_by_id={q['id']:q for q in BASE[bank]['questions']}
    subject=ROOT/'old_source/Autotest.pdf';correction=ROOT/'old_source/autotest correction.pdf'
    sub=pdf_questions(subject);cor=pdf_questions(correction)
    assert [q['number'] for q in sub]==[q['number'] for q in cor]==[1,2,3,4,5,7,8,9,10,13,14,16,17]
    source_to_id={1:1,2:2,3:3,4:4,5:5,7:6,8:12,9:7,10:8,13:9,14:10,16:13,17:11}
    out=[];audits=[];crops=[]
    for s,c in zip(sub,cor):
        num=s['number'];id=source_to_id[num];stem,si=split_pdf_question(s);cstem,ci=split_pdf_question(c)
        assert len(si)==len(ci)==5,(num,si,ci)
        old=old_by_id.get(id)
        q=copy.deepcopy(old) if old else {'id':id,'category':'Autotest techniques histologiques','course':'Techniques histologiques','question':stem,'options':[],'answer':'','explanations':{},'warning':'','images':[],'weight':1}
        q['question']=stem;q['options']=[];q['explanations']={};q['sourceQuestionNumber']=num
        q['sourceSubject']='Autotest.pdf';q['sourceCorrection']='autotest correction.pdf'
        q['subjectPage']=s['crops'][0]['page'];q['correctionPage']=c['crops'][0]['page']
        keys=[];rows=[]
        for i,(so,co) in enumerate(zip(si,ci)):
            oid=co['label'];v,prefix,detail,mark=verdict(co['text'])
            q['options'].append({'id':oid,'text':clean(so['text'])})
            if v:keys.append(oid)
            q['explanations'][oid]=('Vrai.' if v else 'Faux.')+(' '+detail if detail else '')
            rows.append({'id':oid,'sourceLabel':so['label'],'correctionLabel':co['label'],'subject':so['text'],'corrected':co['text'],'correctedStatement':prefix,'sourceVerdict':mark,'verdict':v,'explanation':detail,'statementMatches':clean(so['text'])==clean(prefix)})
        q['answer']=''.join(keys)
        if num==8:
            note(bank,q,None,'Le sujet original porte les lettres A, B, C, A, D. Le corrigé reprend les cinq mêmes propositions dans le même ordre sous les lettres A, B, C, D, E. Cette numérotation du corrigé est utilisée ici pour éviter deux items A ; la clé est ABDE.')
        if num==2:
            q['reviewNotes'][0]['text']='Item E : le sujet dit « L’éosine est un colorant acide », tandis que le corrigé remplace « acide » par « acidophile », puis indique « Faux, basophile ». La ronéo classe l’éosine parmi les colorants acides. Le vocabulaire varie donc entre les deux documents, et le verdict officiel conservé ici contredit la formulation du sujet. À vérifier dans la ronéo : distinguer la nature acide du colorant et l’affinité tinctoriale des structures.'
        refresh_notes(q);out.append(q)
        audits.append({'bank':bank,'id':id,'sourceNumber':num,'subject':subject.name,'correction':correction.name,'oldAnswer':old['answer'] if old else None,'answer':q['answer'],'newQuestion':old is None,'items':rows,'reviewed':True})
        crops.append({'bank':bank,'id':id,'subject':s['crops'],'correction':c['crops']})
    return {bank:{'questions':out}},audits,crops

def main():
    b,a,c=review_te();tb,ta,tc=review_tech();b.update(tb);a+=ta;c+=tc
    (OUT/'reviewed.json').write_text(json.dumps({'banks':b},ensure_ascii=False,indent=2))
    (OUT/'audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
    (OUT/'crops.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
    print('TE + techniques',sum(len(x['questions']) for x in b.values()),'QCM',sum(len(q['items']) for q in a),'items',sum(len(x['subject'])+len(x['correction']) for x in c),'captures')

if __name__=='__main__':main()
