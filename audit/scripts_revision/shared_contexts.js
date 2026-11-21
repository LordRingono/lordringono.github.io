// Shared source statements are rendered outside the individual QCM cards.
// The target map is rebuilt for the visible list so filtering never hides a stem.
const sharedContextTargets=new Map();
function revisedSource(q){return q.fromCompilation||q.contextRevised;}
function sourcePdfFor(q,correction=false){
 return (correction?q.correctionPdf:q.sourcePdf)||(q.fromCompilation?'sources/Annales_compilation.pdf':'');
}
function sourceReference(text,pdf,first,last){
 const pages=first?(first===last||!last?' · p. '+first:' · pp. '+first+'–'+last):'';
 const label=esc(text||'Sujet fourni')+pages;
 return pdf?`<a href="${esc(pdf)}#page=${Number(first)||1}" target="_blank" rel="noopener noreferrer">${label}</a>`:label;
}
function contextQuestionLabel(context){
 const ids=QUESTIONS.filter(q=>(q.sharedContexts||[]).some(c=>c.id===context.id)).map(q=>q.id);
 const groups=[];
 for(let i=0;i<ids.length;i++){
  const first=ids[i];let last=first;
  while(i+1<ids.length&&ids[i+1]===last+1)last=ids[++i];
  groups.push(first===last?String(first):first+'–'+last);
 }
 return 'QCM '+groups.join(', ');
}
function sharedStatement(context,q,anchor){
 const label=contextQuestionLabel(context);
 return `<section class="shared-statement" id="${anchor}" aria-labelledby="${anchor}-title" data-context-key="${esc(context.id)}"><div class="shared-statement-head"><h3 id="${anchor}-title">Énoncé commun</h3><span>${esc(label)}</span></div>${context.text?`<div class="shared-statement-text">${esc(context.text)}</div>`:''}${annalesImages(context.images,'Énoncé commun · '+label)}<div class="shared-statement-source">${sourceReference(context.sourceFile||q.sourceSubject,context.sourcePdf||sourcePdfFor(q),context.sourceStartPage||q.subjectPage,context.sourceEndPage||context.sourceStartPage||q.subjectPage)}</div></section>`;
}
function sharedStatementLinks(q){
 const links=(q.sharedContexts||[]).map(c=>{
  const target=sharedContextTargets.get(c.id);
  return target?`<a href="#${target}" aria-label="Relire l’énoncé commun aux ${esc(contextQuestionLabel(c))}">Énoncé commun · ${esc(contextQuestionLabel(c))}</a>`:'';
 }).filter(Boolean);
 return links.length?`<nav class="shared-statement-links" aria-label="Énoncés communs à cette question">${links.join('')}</nav>`:'';
}
function renderQuestionList(matching){
 sharedContextTargets.clear();let previous=[];let serial=0;
 return matching.map(q=>{
  const contexts=q.sharedContexts||[];let common=0;
  while(common<previous.length&&common<contexts.length&&previous[common]===contexts[common].id)common++;
  const blocks=contexts.slice(common).map(context=>{
   const anchor='shared-context-'+(++serial);
   sharedContextTargets.set(context.id,anchor);
   return sharedStatement(context,q,anchor);
  }).join('');
  previous=contexts.map(c=>c.id);
  return blocks+renderQuestionCard(q);
 }).join('');
}
function questionReferences(q){
 return (q.references||[]).map(ref=>`<details class="source-excerpt annales-references"><summary>${esc(ref.title||'Annexe fournie avec le sujet')}</summary><div class="annales-correction-source">${sourceReference(ref.sourceFile||q.sourceSubject,ref.sourcePdf||sourcePdfFor(q),ref.sourceStartPage,ref.sourceEndPage)}</div>${ref.text?`<div class="shared-statement-text">${esc(ref.text)}</div>`:''}${annalesImages(ref.images,ref.title||'Annexe du sujet')}</details>`).join('');
}
