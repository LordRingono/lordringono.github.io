from pathlib import Path
import fitz, json, subprocess, concurrent.futures
BASE=Path(__file__).resolve().parent
sources=json.loads((BASE/'roneo_inventory.json').read_text())
def run(src):
 d=fitz.open(src['file']);parts=[]
 for i,p in enumerate(d):
  pix=p.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
  proc=subprocess.run(['tesseract','stdin','stdout','-l','eng','--psm','3'],input=pix.tobytes('png'),capture_output=True)
  parts.append(f'PAGE {i+1}\n'+proc.stdout.decode())
 out=BASE/'readings'/(Path(src['file']).stem+'_ocr.txt');out.write_text('\n\n'.join(parts));return out.name
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for name in ex.map(run,sources): print(name,flush=True)
