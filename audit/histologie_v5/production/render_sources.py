from pathlib import Path
import json, subprocess, os
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parent
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
def render(task):
 bank,role,name=task;out=ROOT/'render'/f'{bank}_{role}';out.mkdir(parents=True,exist_ok=True)
 cmd=[os.environ['CODEX_PRIMARY_RUNTIME_PYTHON'],'/home/agent/.codex/skills/builtins/documents/render_docx.py',str(ROOT/'source'/name),'--output_dir',str(out),'--emit_pdf','--dpi','130']
 r=subprocess.run(cmd,capture_output=True,text=True)
 (out/'render.log').write_text(r.stdout+'\n'+r.stderr)
 pdf=out/(Path(name).stem+'.pdf')
 result={'bank':'histo.'+bank,'role':role,'source':name,'pdf':str(pdf),'pages':len(list(out.glob('page-*.png'))),'ok':r.returncode==0 and pdf.exists()}
 print(json.dumps(result,ensure_ascii=False),flush=True)
 return result

if __name__=='__main__':
 tasks=[(b,role,name) for b,names in PAIRS.items() for role,name in zip(['subject','correction'],names)]
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(render,tasks))
 (ROOT/'render_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 assert all(r['ok'] for r in results)
