// Pharmacology progress follows the source question, independently of its theme.
const PHARMA_PROGRESS_KEY='qcm-pass-ls-ue4-progress-by-source-v1';
const pharmaMemory={};
const pharmaVolatile={};
function groupedPharma(){return EXAMS[activeExam]?.pharmaGrouped===true;}
function perQuestionCorrection(){return onlyFilledMode||groupedPharma();}
function pharmaProgressKey(){return PHARMA_PROGRESS_KEY+(onlyFilledMode?'':'_profil_2_v1');}
function writePharmaProgress(snapshot){
 const key=pharmaProgressKey();pharmaMemory[key]=snapshot;
 try{localStorage.setItem(key,JSON.stringify(snapshot));pharmaVolatile[key]=false;}catch(e){pharmaVolatile[key]=true;}
}
function readPharmaProgress(){
 const key=pharmaProgressKey();let snapshot=pharmaMemory[key]||null;
 if(!pharmaVolatile[key]){try{const stored=JSON.parse(localStorage.getItem(key)||'null');if(stored)snapshot=stored;}catch(e){}}
 if(!snapshot||typeof snapshot!=='object'||!snapshot.bySource||typeof snapshot.bySource!=='object'||Array.isArray(snapshot.bySource))snapshot={version:1,bySource:{}};
 const oldStates=new Map();let migrated=false;
 for(const link of PHARMA_PROGRESS_LINKS){
  if(Object.prototype.hasOwnProperty.call(snapshot.bySource,link.sourceId))continue;
  const oldKey=link.storage+(onlyFilledMode?'':'_profil_2_v1');
  if(!oldStates.has(oldKey)){let old=null;try{old=JSON.parse(localStorage.getItem(oldKey)||'null');}catch(e){}oldStates.set(oldKey,old);}
  const old=oldStates.get(oldKey),answer=String(old?.answers?.[link.id]||'');
  const corrected=onlyFilledMode?!!answer&&(Array.isArray(old?.correctedIds)?old.correctedIds.map(Number).includes(link.id):!!old?.submitted):!!old?.submitted;
  snapshot.bySource[link.sourceId]={answer,corrected};migrated=true;
 }
 if(migrated)writePharmaProgress(snapshot);
 return snapshot;
}
function cleanPharmaAnswer(q,value){
 if(q.allowNoAnswer&&value==='∅')return '∅';
 if(q.tokenMode){const values=String(value||'').split(',');return q.options.map(o=>o.id).filter(id=>values.includes(id)).join(',');}
 return q.options.map(o=>o.id).filter(id=>String(value||'').includes(id)).join('');
}
function loadPharmaProgress(){
 const snapshot=readPharmaProgress();
 for(const q of QUESTIONS){
  const item=snapshot.bySource[q.sourceId]||{};
  answers[q.id]=cleanPharmaAnswer(q,item.answer);
  if(item.corrected&&(!onlyFilledMode||answers[q.id]))correctedIds.add(q.id);
 }
 submitted=correctedIds.size>0;
}
function savePharmaProgress(){
 const snapshot=readPharmaProgress();
 for(const q of QUESTIONS)snapshot.bySource[q.sourceId]={answer:cleanPharmaAnswer(q,answers[q.id]),corrected:correctedIds.has(q.id)&&(!onlyFilledMode||!!answers[q.id])};
 writePharmaProgress(snapshot);
}
function pharmaReviewHtml(q){
 if(!q.pharmaReviewed)return '';
 const notes=(q.reviewNotes||[]).map(n=>({items:n.items||[],text:n.text})).filter(n=>n.text);
 if(q.warning&&!q.pharmaWarningCovered&&!notes.some(n=>n.text.includes(q.warning)))notes.push({items:[],text:q.warning+( /ronéo/i.test(q.warning)?'':' Vérifie ce point dans la ronéo correspondante.')});
 if(!notes.length)return '';
 return `<aside class="pharma-review" aria-label="Points à vérifier dans la ronéo"><div class="pharma-review-title">À vérifier dans la ronéo</div>${notes.map(n=>`<p>${n.items.length?`<strong>${n.items.length===1?'Item':'Items'} ${esc(n.items.join(', '))}.</strong> `:''}${esc(n.text)}</p>`).join('')}</aside>`;
}
function pharmaSourceLabel(q){
 if(!q.pharmaReviewed)return '';
 const session=q.session==='S1'?'Session 1':q.session==='S2'?'Session 2':q.session;
 return ' · '+esc(String(q.year||'').replaceAll('-','–'))+' · '+esc(session||'');
}
function renderPharmaClassicToolbar(){
 const bar=$('#toolbar-content'),done=correctedIds.size,remaining=TOTAL-done,s=results();
 if(!TOTAL){bar.innerHTML='<div class="toolbar-info"><strong>Aucun QCM disponible dans les sujets fournis pour ce thème.</strong></div>';return;}
 const headline=done?(s.ratedCount?`Note des ${s.ratedCount} QCM corrigés : ${fmt(s.grade)} / 20`:`${done} QCM corrigés · hors note`):`${answeredCount()} / ${TOTAL} QCM renseignés`;
 bar.innerHTML=`<div class="toolbar-info"><strong>${headline}</strong><small>Profil 2 · correction globale du thème${done&&remaining?` · ${done} corrections déjà enregistrées`:''}</small></div><div style="display:flex;gap:7px;flex-wrap:wrap">${remaining?`<button class="primary-btn" id="submit-all" type="button">Corriger les ${TOTAL} QCM</button>`:''}${done?'<button class="secondary-dark" id="modify" type="button">Modifier</button><button class="secondary-dark" id="back-to-results" type="button">Voir mon bilan</button>':''}</div>`;
}
