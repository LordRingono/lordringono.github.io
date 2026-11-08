(()=>{'use strict';
const D=window.COURSE_DATA;if(!D)return;
const $=s=>document.querySelector(s);const $$=s=>Array.from(document.querySelectorAll(s));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const resource=p=>'../../'+String(p||'').replace(/^\/+/, '');
const fileUrl=(p,n)=>encodeURI(resource(p))+(n&&Number.isFinite(+n)?'#page='+n:'');
const imgSrc=p=>encodeURI(resource(p));
const L=D.glossary||[];
const lexLookup=new Map();L.forEach((g,i)=>{const k=(g.term||'').trim().toLocaleLowerCase('fr-FR');if(k&&!lexLookup.has(k))lexLookup.set(k,i)});
const terms=[...lexLookup.keys()].filter(s=>s.length>3).sort((a,b)=>b.length-a.length).slice(0,360);
const reGloss=terms.length?new RegExp('(^|[^\\p{L}\\p{N}])('+terms.map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')(?![\\p{L}\\p{N}])','giu'):null;
function termText(s){let v=esc(s);if(reGloss) v=v.replace(reGloss,(total,before,term)=>{let key=term.toLocaleLowerCase('fr-FR'),ix=lexLookup.get(key);return ix==null?total:before+'<button class="term" type="button" data-lex="'+ix+'" title="Ouvrir la fiche détaillée">'+term+'</button>'});return v;}
const byGroup={};for(const l of D.lessons){(byGroup[l.group]??=[]).push(l)}
const sourceLink=(p,n,label)=>p?'<a href="'+esc(fileUrl(p,n))+'" target="_blank" rel="noopener">'+esc(label||'Voir dans la ronéo')+'</a>':'Source non associée';
const sourceLine=(p,n,filename)=>'<div class="source-ref">Source&nbsp;: '+(filename?esc(filename)+' · ':'')+sourceLink(p,n,(n?'page '+n:'ouvrir le document'))+'</div>';
let active='cours',bank='annales',quiz=[],submitted=false;
const progressKey='pass-ue5-cm:'+D.id;
let lastScore='';try{lastScore=localStorage.getItem(progressKey)||''}catch(_e){}
function setText(id,text){let e=document.getElementById(id);if(e)e.textContent=text}
function uniqueParas(arr){let used=[];const out=[];for(const str of arr){let s=String(str||'').trim();if(!s)continue;let nn=s.toLowerCase().replace(/\s+/g,' ').replace(/[^a-zà-ÿ0-9]+/g,' ');if(used.some(v=>(nn===v)||(nn.length>75&&v.includes(nn))||(v.length>75&&nn.includes(v))))continue;used.push(nn);out.push(s)}return out}
function findVisual(v,lessons){const text=(v.title+' '+(v.parts||[]).map(x=>x.name).join(' ')).toLowerCase();let best=0,bestl=lessons[0];for(const l of lessons){const tt=(l.title+' '+l.group).toLowerCase();let score=0;const s=[...new Set(text.match(/[a-zà-ÿ]{5,}/g)||[])];for(const k of s)if(tt.includes(k))score+=k.length>7?2:1;if(score>best){best=score;bestl=l}}return bestl?.id||null}
function diagramHTML(v){let parts=(v.parts||[]);return '<div class="diagram" data-viz="'+esc(v.id)+'"><div class="eyebrow">Schéma interactif · '+esc(D.code)+'</div><h3>'+esc(v.title)+'</h3><p class="small muted">'+esc(v.caption||'Clique sur une zone du schéma pour afficher son explication.')+'</p><div class="diagram-stage">'+v.svg+'</div><div class="diagram-explain" role="status">'+(parts[0]?'<strong>'+esc(parts[0].name)+'</strong> · '+esc(parts[0].explain):'Voir la légende du cours.')+'</div></div>'}
function tableHTML(t){if(!t||!Array.isArray(t.rows))return '';const h='<thead><tr>'+(t.headers||[]).map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead>';
 const body='<tbody>'+t.rows.map(row=>'<tr>'+row.map(x=>'<td>'+termText(x)+'</td>').join('')+'</tr>').join('')+'</tbody>';
 const citation=t.citation||{};return '<div class="panel"><div class="eyebrow">Tableau comparatif</div><h3>'+esc(t.title)+'</h3><div class="compare"><table>'+h+body+'</table></div>'+(t.note?'<p class="compare-note">'+esc(t.note)+'</p>':'')+(citation.sourcePath?sourceLine(citation.sourcePath,citation.sourcePage,citation.sourceName):'')+'</div>';
}
function renderCours(){const host=$('#coursContent');if(!host)return;
 const maps={};for(const v of D.visuals||[]){const id=findVisual(v,D.lessons);if(id)(maps[id]??=[]).push(v)}
 let html='<div class="section-intro"><div class="eyebrow">Ronéo prioritaire · contenus vérifiables</div><h2>Cours expliqué, notion par notion</h2><p>Chaque partie est indépendante. Les développements rédigés sont distincts du support intégral, consultable dans l’onglet « Ronéo originale ». Les schémas sont placés près des notions correspondantes.</p></div>';
 if(D.extra?.length)html+='<div class="panel" style="margin-bottom:18px"><div class="eyebrow">Compléments contrôlés sur la ronéo</div><h3>Notions détaillées relevées dans les sources</h3>'+D.extra.map(x=>'<details class="lesson"><summary>'+esc(x.title)+'</summary><div class="lesson-content">'+x.body.map(p=>'<p>'+termText(p)+'</p>').join('')+sourceLine(D.source?.path,x.page,D.source?.name)+'</div></details>').join('')+'</div>';
 let cid=0;
 for(const group of D.groups){const ls=byGroup[group]||[];if(!ls.length)continue;const assocTables=D.tables.filter(x=>x.group===group);
 html+='<details class="course-group" '+(cid++===0?'open':'')+'><summary><span class="section-pill" style="margin:0">'+String(cid).padStart(2,'0')+'</span>'+esc(group)+' <small class="muted">· '+ls.length+' sous-parties</small></summary><div class="group-body">';
 for(let k=0;k<ls.length;k++){
  const l=ls[k];let paras=uniqueParas([l.explain,...(l.more||[])]);
  html+='<details id="'+esc(l.id)+'" class="lesson" '+(k===0&&cid===1?'open':'')+'><summary>'+esc(l.title)+'</summary><div class="lesson-content">'+paras.map(t=>'<p>'+termText(t)+'</p>').join('');
  if(l.points?.length)html+='<div class="key-list"><strong>À retenir pour les QCM</strong><ul>'+l.points.map(p=>'<li>'+termText(p)+'</li>').join('')+'</ul></div>';
  if(l.trap)html+='<div class="trap"><strong>À ne pas confondre.</strong> '+termText(l.trap)+'</div>';
  // Exact excerpts are visibly distinguished from authored explanation; never claim that automated matching proves correctness.
  const exts=(l.sourcePassages||[]).filter(x=>x?.text&&x?.sourcePath);
  if(exts.length)html+='<details class="lesson-excerpts"><summary>Retrouver les passages associés dans la ronéo ('+exts.length+')</summary><div class="lesson-excerpts-body"><p class="tiny muted">Extraits textuels associés automatiquement. Vérifie toujours leur emplacement et leur sens dans le PDF d’origine ; ces extraits ne constituent pas une relecture scientifique certifiée.</p>'+exts.map(x=>'<blockquote class="audit-quote">'+esc(x.text)+'<div class="source-ref">'+sourceLink(x.sourcePath,x.page,'Page '+x.page+' de la ronéo')+'</div></blockquote>').join('')+'</div></details>';
  html+=sourceLine(l.sourcePath,l.sourcePage,l.sourceName);
  if(maps[l.id])html+=maps[l.id].map(diagramHTML).join('');
  html+='</div></details>';
 }
 if(assocTables?.length)html+='<div class="parthead"><h3>Comparer les notions de cette partie</h3></div>'+assocTables.map(tableHTML).join('');
 html+='</div></details>';
 }
 const mappedIds=new Set(Object.values(maps).flat().map(x=>x.id));const unmapped=D.visuals.filter(v=>!mappedIds.has(v.id));
 if(unmapped.length)html+='<section class="panel"><h3>Schémas complémentaires</h3>'+unmapped.map(diagramHTML).join('')+'</section>';
 host.innerHTML=html;
 $('#courseExpand')?.addEventListener('click',()=>$$('#coursContent details.course-group,#coursContent details.lesson').forEach(e=>e.open=true));
 $('#courseCollapse')?.addEventListener('click',()=>$$('#coursContent details.course-group,#coursContent details.lesson').forEach(e=>e.open=false));
}
function renderSheets(){let html='<div class="section-intro"><div class="eyebrow">Fiches de révision</div><h2>Comprendre, comparer, mémoriser</h2><p>Une fiche par mécanisme : un rappel complet, les idées à retenir et le piège correspondant. Les tableaux sont associés à la partie étudiée plutôt qu’accumulés au hasard.</p></div>';
 for(const g of D.groups){const sh=D.sheets.filter(x=>x.group===g);if(!sh.length)continue;html+='<h3 class="sheet-group">'+esc(g)+'</h3>';
 for(const s of sh){html+='<article class="sheet"><h3>'+esc(s.title)+'</h3><div class="sheet-copy">';for(const p of uniqueParas([s.overview,...(s.details||[])]))html+='<p>'+termText(p)+'</p>';html+='</div>';
  if(s.essentials?.length)html+='<strong class="headline">L’essentiel à maîtriser</strong><ul>'+s.essentials.map(x=>'<li>'+termText(x)+'</li>').join('')+'</ul>';
  if(s.trap)html+='<div class="trap"><strong>Piège récurrent.</strong> '+termText(s.trap)+'</div>';
  if(s.sourcePath)html+=sourceLine(s.sourcePath,s.sourcePage,s.sourceName);
  html+='</article>';
 }
 }
 $('#fichesContent').innerHTML=html;
}
function renderLexique(){const host=$('#lexContent');if(!host)return;const sorted=[...L].sort((a,b)=>(a.term||'').localeCompare(b.term||'','fr'));
 host.innerHTML='<div class="section-intro"><h2>Lexique technique</h2><p>Clique sur un terme pour voir sa définition, sa composition, son rôle et ses valeurs de référence quand la ronéo les donne. Un lien mène au support d’origine.</p></div><input class="searchfield" id="lexSearch" placeholder="Chercher un terme : exportine, caspase, desmosome…" aria-label="Rechercher dans le lexique" style="width:100%;margin-bottom:14px"><div class="glossary-list" id="lexEntries">'+sorted.map(g=>'<button class="glossary-btn" type="button" data-lex="'+L.indexOf(g)+'">'+esc(g.term)+'</button>').join('')+'</div>';
 $('#lexSearch').addEventListener('input',e=>{const q=e.target.value.toLowerCase();$$('#lexEntries button').forEach(b=>b.classList.toggle('hide',!b.textContent.toLowerCase().includes(q)))});
}
function showGlossary(idx){const g=L[idx];if(!g)return;const m=$('#lexModal');$('#lexInfo').innerHTML='<div class="dialog-top"><div><div class="eyebrow">Lexique du cours</div><h2>'+esc(g.term)+'</h2></div><button class="dialog-close" data-close-lex>Fermer ✕</button></div>'+[
 ['Définition',g.definition||g.def],['Composition / organisation',g.composition],['Fonction précise',g.role],['Tailles et valeurs de référence',g.numbers],['À distinguer',g.pitfall],['Complément du tutorat',g.notes]
 ].filter(x=>x[1]).map(x=>'<div class="fact"><strong>'+x[0]+'</strong><p>'+esc(x[1])+'</p></div>').join('')+(g.sourcePath?sourceLine(g.sourcePath,g.sourcePage,g.sourceName):'');if(m.showModal)m.showModal();else m.setAttribute('open','');}
function renderQuizBank(){const host=$('#qcmContent');if(!host)return;
 const avail={annales:D.official.filter(q=>q.type==='annales'&&q.scored),autotests:D.official.filter(q=>q.type==='autotests'&&q.scored),connaissances:D.knowledge.filter(q=>q.scored)};
 const counts={annales:avail.annales.length,autotests:avail.autotests.length,connaissances:avail.connaissances.length};
 let html='<div class="section-intro"><div class="eyebrow">Notation PASS Lyon-Sud</div><h2>Questions corrigées, figures incluses</h2><p>Trois banques séparées. Les annales et autotests sont issus des corrigés originaux ; les QCM de connaissances sont de nouveaux assemblages de propositions réellement corrigées, étiquetés comme non officiels. Barème : 0 erreur → 10, 1 → 5, 2 → 2, 3 ou plus → 0, puis conversion sur 20.</p></div><div class="banklist">';
 for(const [id,label] of [['annales','Annales'],['autotests','Autotests et colles'],['connaissances','Connaissances']])html+='<button type="button" data-bank="'+id+'" class="bank '+(id===bank?'active':'')+'"><strong>'+label+'</strong><span class="mono">'+counts[id]+' questions notables'+(id==='connaissances'?' · non officielles':'')+'</span></button>';
 html+='</div><div class="panel">'+(D.knowledgeStatus?'<div class="note" id="knowledgeNote" style="display:'+(bank==='connaissances'?'block':'none')+';margin-bottom:16px">'+esc(D.knowledgeStatus)+'</div>':'')+'<div class="quiz-setup"><label class="quiz-field">Nombre de QCM<input id="quizCount" type="number" min="1" max="'+Math.max(counts[bank],1)+'" value="'+Math.min(10,Math.max(counts[bank],1))+'"></label><button class="btn primary" id="startQuiz" '+(!counts[bank]?'disabled':'')+'>Tirer au sort</button><button class="btn secondary" id="resetQuiz">Effacer la série</button></div><p id="bankStatus" class="note">'+bankNote(bank,counts)+'</p>'+(lastScore?'<p class="small muted">Dernier résultat enregistré dans ce navigateur : '+esc(lastScore)+'</p>':'')+'</div><div id="quizQuestions"></div>';
 const flagged=D.official.filter(q=>!q.scored);
 if(flagged.length)html+='<details class="course-group" style="margin-top:24px"><summary>Questions dont la notation est suspendue · '+flagged.length+'</summary><div class="group-body"><p class="note">Ces questions proviennent des documents du cours, mais une image ou une transcription n’a pas pu être liée avec suffisamment de certitude. Elles ne sont pas incluses dans les notes.</p>'+flagged.map(q=>'<div class="subtle"><strong>'+esc(q.title)+'</strong><p class="small">'+esc(q.reviewFlag||'À vérifier dans le corrigé')+'</p>'+sourceLink(q.sourcePath,q.sourcePage,q.source)+'</div>').join('')+'</div></details>';
 host.innerHTML=html;
 $$('[data-bank]').forEach(b=>b.addEventListener('click',()=>{bank=b.dataset.bank;quiz=[];submitted=false;renderQuizBank()}));
 $('#startQuiz').addEventListener('click',()=>{let n=Math.max(1,Math.min(counts[bank],parseInt($('#quizCount').value)||10));const pool=[...avail[bank]];for(let j=pool.length-1;j>0;j--){const z=Math.floor(Math.random()*(j+1));[pool[j],pool[z]]=[pool[z],pool[j]]}quiz=pool.slice(0,n);submitted=false;renderCurrentQuiz();$('#quizQuestions')?.scrollIntoView({behavior:'smooth',block:'start'})});
 $('#resetQuiz').addEventListener('click',()=>{quiz=[];submitted=false;$('#quizQuestions').innerHTML=''});
}
function bankNote(b,count){if(count[b]>0)return b==='connaissances'?'Questions recomposées à partir de propositions corrigées, pas des annales officielles. Chaque proposition possède sa référence.': 'Le tirage ne contient que les questions avec clé de correction rattachable au support.';
 if(b==='autotests')return 'Aucun autotest corrigé distinct n’est présent pour cette unité précise dans l’archive. Vérifie les colles, TD et les unités voisines dans la bibliothèque.';
 if(b==='annales')return 'Aucune annale notée avec corrigé certain n’est disponible pour cette unité. Les annales et autres entraînements existants restent consultables dans l’onglet « Pages d’annales ».';
 return 'Pas assez de propositions corrigées distinctes pour créer un entraînement fiable.';
}
function renderCurrentQuiz(){const host=$('#quizQuestions');if(!quiz.length){host.innerHTML='';return;}
 let html='<div class="parthead"><div><div class="eyebrow">Session de '+quiz.length+' QCM</div><h2>Choisis toutes les réponses correctes</h2></div><span class="pill tint">Barème 10 / 5 / 2 / 0</span></div>';
 for(let i=0;i<quiz.length;i++){
  const q=quiz[i];html+='<section class="question" data-q="'+i+'"><div class="q-head"><div><div class="q-label">QUESTION '+(i+1)+' / '+quiz.length+'</div><h3>'+esc(q.title)+'</h3></div><span class="pill">'+(q.type==='connaissances'?'Entraînement créé':q.type==='annales'?'Annale originale':'Autotest / colle')+'</span></div>';
  if(q.figures?.length)html+='<div class="q-figure">'+q.figures.map((src,j)=>'<a href="'+esc(imgSrc(src))+'" target="_blank" title="Agrandir la figure du document original"><img loading="lazy" src="'+esc(imgSrc(src))+'" alt="Figure '+(j+1)+' extraite du document d’origine"></a>').join('')+'</div>';
  for(let j=0;j<q.options.length;j++){
   const opt=q.options[j];html+='<label class="opt" data-opt="'+j+'"><input type="checkbox" name="quiz-'+i+'" value="'+j+'" aria-label="Réponse '+esc(opt.label||String.fromCharCode(65+j))+'"><span class="letter">'+esc(opt.label||String.fromCharCode(65+j))+'</span><span class="statement">'+esc(opt.text)+'</span></label>';
  }
  if(q.type!=='connaissances')html+='<div class="q-source">'+sourceLink(q.sourcePath,q.sourcePage,q.source)+(q.pageImage?'<a href="'+esc(imgSrc(q.pageImage))+'" target="_blank">Voir la page originale illustrée</a>':'')+(q.shared?'<span>Banque commune au chapitre</span>':'')+'</div>';
  else html+='<div class="q-source">Question créée à partir de propositions du tutorat ; références détaillées dans la correction.</div>';
  html+='<div class="q-feedback" style="display:none"></div></section>';
 }
 html+='<div class="panel" id="submitPanel"><button class="btn primary" id="submitQuiz">Envoyer toutes mes réponses et corriger</button><p class="tiny muted" style="margin:10px 0 0">Une proposition correcte oubliée et une proposition fausse cochée comptent chacune pour une erreur.</p></div>';
 host.innerHTML=html;
 $('#submitQuiz').addEventListener('click',submitQuiz);
}
function submitQuiz(){if(submitted)return;submitted=true;let total=0,points=[];
 for(let i=0;i<quiz.length;i++){
  let q=quiz[i],node=$('[data-q="'+i+'"]');const checked=new Set($$('section[data-q="'+i+'"] input:checked').map(x=>parseInt(x.value)));
  let errors=0;
  for(let j=0;j<q.options.length;j++){
   const yes=!!q.options[j].correct;const selected=checked.has(j);
   if(yes!==selected)errors++;
   const opt=node.querySelector('[data-opt="'+j+'"]');
   if(yes&&selected)opt.classList.add('correct');else if(yes&&!selected)opt.classList.add('missed');else if(!yes&&selected)opt.classList.add('error');
   opt.querySelector('input').disabled=true;
   let exp=q.options[j].explanation||'';
   if(exp||q.type==='connaissances'){
    const ref=q.options[j].sourcePath?(' · '+sourceLink(q.options[j].sourcePath,q.options[j].sourcePage,q.options[j].source)) :'';
    opt.insertAdjacentHTML('afterend','<div class="opt-explain">'+(yes?'✓ Vrai':'✕ Faux')+(exp?' — '+esc(exp):'')+ref+'</div>');
   }
  }
  const note=errors===0?10:errors===1?5:errors===2?2:0;total+=note;points.push({errors,note});
  const feed=node.querySelector('.q-feedback');feed.style.display='block';feed.className='q-feedback '+(errors===0?'result':'no-grade');feed.innerHTML='<strong>'+note+' / 10</strong> · '+errors+' erreur'+(errors>1?'s':'')+' · Réponses exactes : '+q.options.filter(o=>o.correct).map(o=>o.label).join('');
 }
 const score=(total/quiz.length/10*20).toFixed(2);let html='<div class="result"><div class="row"><div><div class="eyebrow">Résultat de la session</div><big>'+score.replace('.',',')+' / 20</big><span class="muted">'+total+' / '+quiz.length*10+' points · '+quiz.length+' QCM</span></div><span class="score-pill">'+points.filter(x=>x.errors===0).length+' parfaitement réussis</span></div><p style="margin:12px 0 0" class="small">Vert = réponse cochée à juste titre ; orange = bonne réponse oubliée ; rouge = proposition fausse cochée. Chaque détail peut être contrôlé avec le document original.</p></div>';
 $('#submitPanel').innerHTML=html+'<button class="btn" id="newQuiz" style="margin-top:12px">Nouvelle série aléatoire</button>';
 $('#newQuiz').addEventListener('click',()=>$('#startQuiz').click());
 try{localStorage.setItem(progressKey,score.replace('.',',')+' / 20 · '+new Date().toLocaleDateString('fr-FR'))}catch(_e){}
 $('#submitPanel').scrollIntoView({behavior:'smooth',block:'center'});
}
function renderGallery(){const host=$('#annalesContent');if(!host)return;const docs=D.documents.filter(d=>['Annales','Autotests','Colles / TD'].includes(d.kind));
 let html='<div class="section-intro"><div class="eyebrow">Tous les originaux · aucune figure supprimée</div><h2>Pages d’annales et d’autotests</h2><p>Les pages des PDF sont conservées telles quelles, y compris les questions scannées et leurs images. Les documents DOCX sont accessibles directement ; leurs figures intégrées apparaissent aussi lorsque présentes. Cela complète les QCM interactifs, sans inventer de correction lorsque l’image ou le barème ne peut être transcrit.</p></div><div class="pdf-gallery">';
 if(!docs.length)html+='<p class="note">Aucun document classé annale/autotest dans cette unité, mais les autres supports sont disponibles dans la bibliothèque.</p>';
 for(const d of docs){html+='<details><summary><span><span class="pill '+(d.kind==='Annales'?'tint':'')+'">'+esc(d.kind)+'</span> '+esc(d.name)+'</span><span class="tiny muted">'+(d.rasterPages?.length||d.drawingImages?.length||'')+' images</span></summary><div class="group-body">'+sourceLink(d.path,null,'Ouvrir le document original');
  if(d.rasterPages?.length)html+='<div class="page-grid">'+d.rasterPages.map((im,i)=>'<a class="page-thumb" target="_blank" href="'+esc(fileUrl(d.path,i+1))+'"><img loading="lazy" alt="Page '+(i+1)+' du document '+esc(d.name)+'" src="'+esc(imgSrc(im))+'"><span>Page '+(i+1)+' · PDF original</span></a>').join('')+'</div>';
  if(d.drawingImages?.length)html+='<p class="small muted" style="margin:14px 0 2px">Figures extraites du fichier DOCX :</p><div class="page-grid">'+d.drawingImages.map((im,i)=>'<a class="page-thumb" href="'+esc(imgSrc(im))+'" target="_blank"><img loading="lazy" src="'+esc(imgSrc(im))+'"><span>Figure '+(i+1)+'</span></a>').join('')+'</div>';
  html+='</div></details>';
 }
 host.innerHTML=html+'</div>';
}
function renderSources(){const host=$('#sourcesContent');const docs=[...D.documents].sort((a,b)=>(a.kind+a.name).localeCompare(b.kind+b.name,'fr'));
 let h='<div class="section-intro"><div class="eyebrow">Bibliothèque documentaire</div><h2>Les supports transmis, sans remplacement</h2><p>Priorité aux ronéos pour le cours expliqué. Toutes les versions utiles — corrigées, non corrigées, annales, autotests, colles, fiches et diaporamas — sont conservées. Certains documents d’histologie sont communs à plusieurs parties et portent cette mention.</p></div><div class="doc-grid">';
 for(const d of docs)h+='<article class="doc-card"><span class="pill tag '+(d.kind==='Ronéos'?'tint':'')+'">'+esc(d.kind)+'</span> '+(d.shared?'<span class="pill tag">Support commun</span>':'')+'<strong>'+esc(d.name)+'</strong><small>'+(d.pages?d.pages+' pages · ':'')+(d.size?(d.size/1024/1024).toFixed(1)+' Mo':'')+'</small><div style="margin-top:13px">'+sourceLink(d.path,null,'Consulter le fichier')+'</div></article>';
 host.innerHTML=h+'</div>';
}
let readerPage=1;
function renderReader(){const host=$('#readerContent'),pages=D.primaryPages||[];
 if(!D.source?.path||!pages.length){host.innerHTML='<div class="note">Aucune ronéo PDF primaire indexée pour cette unité. Consulte la bibliothèque complète.</div>';return;}
 host.innerHTML='<div class="section-intro"><div class="eyebrow">Fidélité documentaire</div><h2>Ronéo originale, page par page</h2><p>Cette lecture est issue des images du PDF fourni, pas d’une retranscription automatique : tableaux, graphiques, légendes et détails restent exactement à leur place. Utilise le cours rédigé pour les explications, puis le document original pour vérifier l’exhaustivité.</p></div><div class="r-reader"><div class="reader-frame"><div class="reader-nav"><button class="btn" id="pgPrev">← Précédente</button><span class="pill mono" id="readerIndicator"></span><button class="btn" id="pgNext">Suivante →</button></div><img id="pageImg" alt="Page de la ronéo d’origine" loading="lazy"><div class="source-ref">'+sourceLink(D.source.path,null,D.source.name)+' · <a id="pageDirect" target="_blank">Ouvrir directement à cette page</a></div></div><div class="reader-side"><div class="eyebrow">Source primaire</div><h3>'+esc(D.source.name)+'</h3><label for="pageSlider">Aller à la page</label><input id="pageSlider" type="range" min="1" max="'+pages.length+'" value="1"><div style="margin-top:14px"><input id="pageField" type="number" min="1" max="'+pages.length+'" value="1" class="searchfield" style="width:100%"></div><p class="small muted" style="margin-top:20px">'+pages.length+' pages. Les autres versions de la ronéo sont dans la bibliothèque.</p></div></div>';
 const setPage=n=>{readerPage=Math.min(pages.length,Math.max(1,+n||1));const p=pages[readerPage-1];$('#pageImg').src=imgSrc(p.image);$('#readerIndicator').textContent='Page '+readerPage+' / '+pages.length;$('#pageSlider').value=readerPage;$('#pageField').value=readerPage;$('#pageDirect').href=fileUrl(D.source.path,readerPage);$('#pgPrev').disabled=readerPage===1;$('#pgNext').disabled=readerPage===pages.length;};
 $('#pgPrev').addEventListener('click',()=>setPage(readerPage-1));$('#pgNext').addEventListener('click',()=>setPage(readerPage+1));$('#pageSlider').addEventListener('input',e=>setPage(e.target.value));$('#pageField').addEventListener('change',e=>setPage(e.target.value));setPage(1);
}
function renderFidelityAudit(){
 const h=$('#auditContent');if(!h)return;
 const A=window.UE5_SOURCE_AUDIT;
 if(!A||!A.pages?.length){h.innerHTML='<div class="note">Aucune page de cours source n’a pu être indexée pour ce chapitre. Vérifier les documents dans la bibliothèque.</div>';return;}
 const source=A.source||{};const stats=A.stats||{};
 let body='<div class="section-intro"><div class="eyebrow">Contrôle documentaire · priorité à la ronéo</div><h2>Vérifier chaque détail du support</h2><p>Les '+A.pages.length+' pages du document source sont ici consultables <strong>en texte et en image</strong>. Les passages pointés ne sont pas nécessairement des oublis : la comparaison est lexicale et peut manquer les reformulations. Cette vue permet de reprendre aussi les chiffres, protéines, exceptions et légendes sans limiter le contrôle à ce qui tombe souvent.</p></div>';
 body+='<div class="audit-warning"><strong>Statut : contrôle scientifique exhaustif non certifié.</strong> La présence d’un mot dans une leçon ne suffit pas à valider sa définition. Les extraits ci-dessous sont issus du PDF (avec quelques retours à la ligne réassemblés) ; toute discordance se tranche sur <a href="'+esc(fileUrl(source.path))+'" target="_blank">le document original</a>.</div>';
 body+='<div class="audit-stats"><div><strong>'+A.pages.length+'</strong><small>pages source</small></div><div><strong>'+(stats.sentences_to_review||0)+'</strong><small>passages à confronter</small></div><div><strong>'+(stats.signals_num||0)+'</strong><small>valeurs à vérifier</small></div><div><strong>'+(stats.signals_acro||0)+'</strong><small>sigles à vérifier</small></div></div>';
 body+='<div class="audit-controls"><label class="quiz-field" style="flex:1">Rechercher dans toute la ronéo<input id="auditQuery" type="search" class="searchfield" placeholder="Ex. caspase, exportine, 40 kDa, ATP…"></label><label class="audit-check"><input type="checkbox" id="auditFlagged"> Pages avec points à contrôler</label><button class="btn" id="auditExpand">Déplier les pages visibles</button><button class="btn" id="auditCollapse">Tout replier</button></div><p class="small muted" id="auditVisible"></p>';
 A.pages.forEach((p,i)=>{
  const flags=p.flags||[];const nums=p.signals?.numbers||[];const acrs=p.signals?.acronyms||[];
  const review=flags.length||nums.length||acrs.length;
  body+='<details class="audit-page" data-page-index="'+i+'" data-flagged="'+(review?1:0)+'"><summary><span class="audit-page-title">Page '+p.page+' / '+A.pages.length+'</span><span class="audit-counters">'+(p.linkedLessons?.length?p.linkedLessons.length+' leçon(s) citant cette page · ':'')+(review?review+' signalements automatiques':'aucun signalement automatique')+'</span></summary><div class="audit-page-body">';
  if(p.lowText)body+='<div class="no-grade">Le texte extrait est insuffisant pour contrôler cette page. <strong>Lire absolument la page illustrée</strong>.</div>';
  body+='<div class="audit-split"><div><div class="eyebrow">Texte extrait de la source</div>'+(p.blocks?.length?p.blocks.map(x=>'<p class="audit-source-block">'+esc(x)+'</p>').join(''):'<p>Pas de transcription textuelle exploitable ; consulter l’image ci-contre.</p>')+'</div><aside class="audit-original"><div class="eyebrow">PDF original</div>'+(p.image?'<a target="_blank" href="'+esc(imgSrc(p.image))+'"><img loading="lazy" src="'+esc(imgSrc(p.image))+'" alt="Ronéo originale, page '+p.page+'"></a>':'<p>Image non indexée.</p>')+'<div>'+sourceLink(source.path,p.page,'Ouvrir la page '+p.page+' du PDF')+'</div></aside></div>';
  if(p.linkedLessons?.length)body+='<div class="audit-linked"><strong>Leçons actuellement associées à cette page</strong><div class="audit-tags">'+p.linkedLessons.map(x=>'<button type="button" class="btn" data-audit-lesson="'+esc(x.id)+'">'+esc(x.title)+'</button>').join('')+'</div></div>';
  if(flags.length)body+='<details class="audit-flags"><summary>Passages spécifiques à comparer aux explications ('+flags.length+')</summary><div class="audit-flags-inner"><p class="small muted">Cette liste est issue d’une recherche de termes et valeurs : elle sert d’aide à la relecture, <strong>pas de preuve d’une erreur</strong>.</p>'+flags.map(f=>'<blockquote class="audit-quote"><span>'+esc(f.text)+'</span><small>'+esc((f.reasons||[]).join(' · '))+'</small></blockquote>').join('')+'</div></details>';
  body+='</div></details>';
 });
 h.innerHTML=body;
 const query=$('#auditQuery'),only=$('#auditFlagged'),total=A.pages.length;
 const apply=()=>{const q=query.value.toLocaleLowerCase('fr-FR').trim();let shown=0;$$('#auditContent .audit-page').forEach((node,i)=>{const p=A.pages[i];const hay=(p.blocks||[]).join(' ').toLocaleLowerCase('fr-FR');let ok=(!q||hay.includes(q)||('page '+p.page).includes(q))&&(!only.checked||node.dataset.flagged==='1');node.classList.toggle('hide',!ok);if(ok)shown++});$('#auditVisible').textContent=shown+' / '+total+' pages affichées.'};
 query.addEventListener('input',apply);only.addEventListener('change',apply);apply();
 $('#auditExpand').addEventListener('click',()=>$$('#auditContent .audit-page:not(.hide)').forEach(x=>x.open=true));
 $('#auditCollapse').addEventListener('click',()=>$$('#auditContent .audit-page').forEach(x=>x.open=false));
 $$('[data-audit-lesson]').forEach(x=>x.addEventListener('click',()=>{tabTo('cours');let l=document.getElementById(x.dataset.auditLesson);if(l){l.parentElement.closest('details.course-group').open=true;l.open=true;l.scrollIntoView({behavior:'smooth',block:'center'});}}));
}

function tabTo(name){active=name;$$('.tab').forEach(e=>{e.classList.toggle('active',e.dataset.tab===name);e.setAttribute('aria-selected',e.dataset.tab===name?'true':'false')});$$('.tab-pane').forEach(e=>e.classList.toggle('hide',e.dataset.pane!==name));$$('.side-link[data-tab]').forEach(e=>e.classList.toggle('active',e.dataset.tab===name));window.scrollTo({top:0,behavior:'smooth'});}
function updateHeader(){setText('headerTitle',D.code+' · '+D.title);setText('heroCode',D.code);setText('heroTitle',D.title);setText('heroSubtitle',D.subtitle);setText('docCount',D.documentCount);setText('lessonCount',D.lessons.length);setText('quizCountTotal',D.qcmCounts.annales+D.qcmCounts.autotests+D.qcmCounts.connaissances);setText('imageCount',D.primaryPages?.length||0);document.title=D.code+' · '+D.title+' | PASS Studio UE5';}
function init(){updateHeader();renderCours();renderSheets();renderLexique();renderQuizBank();renderGallery();renderSources();renderReader();renderFidelityAudit();
 $$('.tab,.side-link[data-tab]').forEach(e=>e.addEventListener('click',event=>{event.preventDefault();tabTo(e.dataset.tab)}));
 document.body.addEventListener('click',event=>{
  const t=event.target.closest('[data-lex]');if(t){showGlossary(parseInt(t.dataset.lex));return}
  if(event.target.closest('[data-close-lex]')){$('#lexModal').close();return}
  const node=event.target.closest('[data-viz] .viz-part');if(node){const parent=node.closest('[data-viz]'),viz=D.visuals.find(x=>x.id===parent.dataset.viz),idx=parseInt(node.dataset.index);const part=viz?.parts?.[idx];if(part)parent.querySelector('.diagram-explain').innerHTML='<strong>'+esc(part.name)+'</strong> · '+esc(part.explain);}
 });
 document.body.addEventListener('keydown',event=>{if((event.key==='Enter'||event.key===' ')&&event.target.matches('.viz-part')){event.preventDefault();event.target.dispatchEvent(new MouseEvent('click',{bubbles:true}))}});
 $('#lexModal')?.addEventListener('click',e=>{if(e.target.id==='lexModal')e.target.close()});
 tabTo('cours');
}
init();
})();
