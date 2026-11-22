// Original histology documents: subject available while answering, correction after grading.
function histoSourceCopy(q, role){
 const source=q.sourceCopies?.[role];
 if(!source?.captures?.length||(role==='correction'&&!isCorrected(q)))return '';
 const corrected=role==='correction',label=corrected?'Voir le corrigé original':'Voir le sujet original';
 const pages=[...new Set(source.captures.map(c=>c.page))];
 const pageLabel=(pages.length>1?'pp. ':'p. ')+pages.join(', ');
 const sourceNumber=q.sourceQuestionNumber||q.id;
 return `<details class="source-excerpt histo-source-copy" data-source-role="${role}"><summary>${label}</summary><div class="histo-source-meta">${esc(source.file)} · QCM source ${esc(sourceNumber)} · ${esc(pageLabel)}${source.converted?' · pagination du PDF':''}</div>${source.note?`<p class="histo-source-note">${esc(source.note)}</p>`:''}<div class="source-excerpt-images">${source.captures.map((capture,i)=>`<figure><a href="${esc(capture.src)}" target="_blank" rel="noopener noreferrer" aria-label="Agrandir ${corrected?'le corrigé':'le sujet'} original du QCM ${esc(sourceNumber)}, page ${capture.page}"><img loading="lazy" decoding="async" src="${esc(capture.src)}" alt="${corrected?'Corrigé':'Sujet'} original du QCM ${esc(sourceNumber)}, page ${capture.page}${source.captures.length>1?', partie '+(i+1)+' sur '+source.captures.length:''}"></a><figcaption>Page ${capture.page}${source.captures.length>1?' · partie '+(i+1)+'/'+source.captures.length:''} · Cliquer pour agrandir</figcaption></figure>`).join('')}</div><div class="histo-source-links"><a href="${esc(source.pdf)}#page=${pages[0]}" target="_blank" rel="noopener noreferrer">Ouvrir le PDF complet</a>${source.original!==source.pdf?`<a href="${esc(source.original)}" download>Télécharger le Word original</a>`:''}</div></details>`;
}
