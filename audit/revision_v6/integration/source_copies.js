// Original documents: subjects while answering, corrections only after grading.
function sharedOriginalReady(context){
 if(!context.imagesAfterCorrection)return true;
 const concerned=QUESTIONS.filter(q=>(q.sharedContexts||[]).some(c=>c.id===context.id));
 return concerned.length>0&&concerned.every(isCorrected);
}
function subjectOriginalReady(q){
 if(!q.sourceCopies?.subject?.afterCorrection&&!q.imagesAfterCorrection)return true;
 return isCorrected(q)&&(q.sharedContexts||[]).filter(c=>c.imagesAfterCorrection).every(sharedOriginalReady);
}
function histoSourceCopy(q, role){
 const source=q.sourceCopies?.[role];
 if(!source||(role==='correction'&&!isCorrected(q)))return '';
 const corrected=role==='correction',label=corrected?(source.mismatch?'Voir le corrigé fourni · énoncé différent':'Voir le corrigé original'):'Voir le sujet original';
 const captures=source.captures||[];
 if(source.afterCorrection&&!subjectOriginalReady(q))return `<details class="source-excerpt histo-source-copy" data-source-role="${role}" data-source-deferred="true"><summary>${label}</summary><p class="histo-source-note">Le document fourni comporte une annotation de correction. Sa copie sera accessible après validation des QCM concernés.</p></details>`;
 if(!captures.length){
  if(!source.missing)return '';
  return `<details class="source-excerpt histo-source-copy" data-source-role="${role}" data-source-missing="true"><summary>${label}</summary><p class="histo-source-note">${esc(source.reason||(corrected?'Le corrigé original correspondant n’est pas disponible dans les documents fournis.':'Le sujet non corrigé correspondant n’est pas disponible dans les documents fournis.'))}</p></details>`;
 }
 const pages=[...new Set(captures.map(c=>c.page))];
 const documents=source.documents?.length?source.documents:[{...source,pages}];
 const several=documents.length>1;
 const metadata=documents.map(doc=>{
  const pageList=doc.pages||pages;
  const pageLabel=(pageList.length>1?'pp. ':'p. ')+pageList.join(', ');
  const numberLabel=!several&&source.questionNumber?' · QCM source '+esc(source.questionNumber):'';
  return `<div class="histo-source-meta">${esc(doc.file||'Document fourni')}${numberLabel} · ${esc(pageLabel)}${doc.converted?' · pagination du PDF':''}</div>`;
 }).join('');
 const links=documents.map(doc=>{
  const first=doc.firstPage||(doc.pages||pages)[0];
  const pdfLink=doc.pdf?`<a href="${esc(doc.pdf)}#page=${first}" target="_blank" rel="noopener noreferrer">${several?'Ouvrir '+esc(doc.file):'Ouvrir le PDF complet'}</a>`:'';
  const originalLink=doc.original&&doc.original!==doc.pdf?`<a href="${esc(doc.original)}" download>${several?'Document original · '+esc(doc.file):'Télécharger le document original'}</a>`:'';
  return pdfLink+originalLink;
 }).join('');
 const figures=captures.map((capture,i)=>{
  const part=captures.length>1?' · partie '+(i+1)+'/'+captures.length:'';
  const documentLabel=several?esc(capture.file||'Document fourni')+' · ':'';
  const numberLabel=capture.questionNumber?' · QCM source '+esc(capture.questionNumber):'';
  const alt=(corrected?'Corrigé':'Sujet')+' original du QCM '+q.id+', page '+capture.page;
  return `<figure><a href="${esc(capture.src)}" target="_blank" rel="noopener noreferrer" aria-label="Agrandir ${esc(alt)}"><img loading="lazy" decoding="async" src="${esc(capture.src)}" alt="${esc(alt)}${part}"></a><figcaption>${documentLabel}Page ${capture.page}${numberLabel}${part} · Cliquer pour agrandir</figcaption></figure>`;
 }).join('');
 return `<details class="source-excerpt histo-source-copy" data-source-role="${role}"><summary>${label}</summary>${metadata}${source.note?`<p class="histo-source-note">${esc(source.note)}</p>`:''}<div class="source-excerpt-images">${figures}</div><div class="histo-source-links">${links}</div></details>`;
}
