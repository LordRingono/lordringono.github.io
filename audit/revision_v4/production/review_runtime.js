// Review notes are rendered only by the correction panel, after grading.
// A uniform explicit empty selection avoids revealing all-false answer keys.
function allowsNoAnswer(q){return Array.isArray(q.options)&&q.options.length>0;}
function reviewRefHtml(ref){
 const label=[ref.label||ref.file||'Référence',ref.page?'p. '+ref.page:''].filter(Boolean).join(' · ');
 const href=ref.href||ref.url||'';
 return href&&(/^(https?:\/\/|sources\/)/.test(href))?`<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`:`<span>${esc(label)}</span>`;
}
function reviewHtml(q){
 const labels={scientific_conflict:'Erreur scientifique repérée',roneo_conflict:'Désaccord avec le cours',source_conflict:'Contradiction dans les sources',possible_error:'Point à vérifier',outdated_reference:'Référence à actualiser',missing_reference:'Source insuffisante'};
 const notes=(q.reviewNotes||[]).filter(n=>n.text);
 const legacy=q.warning&&!q.reviewWarningCovered&&!q.pharmaWarningCovered&&!notes.some(n=>n.text.includes(q.warning))?q.warning:'';
 if(!notes.length&&!legacy)return '';
 return `<aside class="pharma-review" aria-label="Remarques sur la correction"><div class="pharma-review-title">À vérifier dans la ronéo</div>${notes.map(n=>`<div class="review-note"><p><span class="review-kind">${esc(labels[n.kind]||'Point à vérifier')}</span>${n.items?.length?` <strong>${n.items.length===1?'Item':'Items'} ${esc(n.items.join(', '))}.</strong>`:''} ${esc(n.text)}</p>${n.sourceVerdict||n.courseVerdict||n.refs?.length?`<details class="review-evidence"><summary>Sources et comparaison</summary>${n.sourceVerdict?`<p><strong>Document fourni :</strong> ${esc(n.sourceVerdict)}</p>`:''}${n.courseVerdict?`<p>${esc(n.courseVerdict)}</p>`:''}${n.refs?.length?`<div class="review-references">${n.refs.map(reviewRefHtml).join('')}</div>`:''}</details>`:''}</div>`).join('')}${legacy?`<p class="review-legacy"><strong>Réserve du document.</strong> ${esc(legacy)}</p>`:''}</aside>`;
}

function pharmaCatalogEntries(){
 return Object.entries(EXAMS).filter(([,e])=>e.ue==='ue4').flatMap(([bank,e])=>e.questions.map(q=>({bank,theme:e.courseId,q})));
}
function pharmaPrintedSession(q){
 // These two cover pages name only the academic year; historical storage IDs stay intact.
 if(['2018-2019','2019-2020'].includes(q.year))return 'Session non précisée';
 return q.session==='S1'?'Session 1':q.session==='S2'?'Session 2':q.session||'';
}
function pharmaCatalogMatches(entry,query){
 const q=entry.q;
 const session=pharmaPrintedSession(q),normalSearch=s=>normal(s).replace(/[–—‑]/g,'-');
 const text=normalSearch([q.year,session,session==='Session non précisée'?'':q.session,q.printedSourceNumber||q.sourceNumber,'QCM '+(q.printedSourceNumber||q.sourceNumber),'QCM'+(q.printedSourceNumber||q.sourceNumber),'Q'+(q.printedSourceNumber||q.sourceNumber),q.question,...q.options.map(o=>o.text),entry.theme,q.category,...(q.relatedThemes||[]).map(id=>UNIT_COURSES.ue4.find(t=>t[0]===id)?.[1]||id)].join(' '));
 return normalSearch(query).split(/\s+/).filter(Boolean).every(word=>text.includes(word));
}
function renderPharmaCatalog(){
 const host=$('#pharma-catalog'),results=$('#pharma-catalog-results');
 host.classList.toggle('hidden',currentUnit()!=='ue4');
 if(currentUnit()!=='ue4')return;
 const query=$('#pharma-catalog-search').value||'';
 const entries=pharmaCatalogEntries().filter(entry=>pharmaCatalogMatches(entry,query));
 $('#pharma-catalog-count').textContent=entries.length+' QCM'+(query?' trouvés':' dans les sujets fournis');
 const current=EXAMS[activeExam].courseId;
 results.innerHTML=UNIT_COURSES.ue4.map(([theme,label])=>{
  const primary=entries.filter(e=>e.theme===theme);
  const related=entries.filter(e=>e.theme!==theme&&(e.q.relatedThemes||[]).includes(theme));
  const all=[...primary,...related];
  if(!all.length)return '';
  return `<details class="pharma-catalog-group" ${query||theme===current?'open':''}><summary>${esc(label)} <span>${primary.length} QCM${related.length?' · '+related.length+' renvoi'+(related.length>1?'s':''):''}</span></summary><div class="pharma-catalog-list">${all.map(({bank,q,theme:home})=>`<button type="button" class="pharma-catalog-result" data-pharma-bank="${esc(bank)}" data-pharma-q="${q.id}"><span>${esc(q.question)}</span><small>${esc(String(q.year||'').replaceAll('-','–'))} · ${esc(pharmaPrintedSession(q))} · QCM source ${esc(q.printedSourceNumber||q.sourceNumber)}${home!==theme?' · Classé dans '+esc(UNIT_COURSES.ue4.find(t=>t[0]===home)?.[1]||home):''}</small></button>`).join('')}</div></details>`;
 }).join('')||'<p class="pharma-catalog-empty">Aucun QCM ne correspond à cette recherche.</p>';
}
