const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {load}=require('./dom_adapter.cjs');
const root=path.resolve(__dirname,'../..'),target=path.join(root,'output/site/index.html');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const clean=x=>JSON.parse(JSON.stringify(x));
const old=read('work/review_v4/baseline_exams.json'),current=read('work/review_v4/current_exams.json');
const audit='output/site/audit/revision_v4/';
const changes=read(audit+'reparations.json'),adds=read(audit+'ajouts.json'),stats=read(audit+'statistiques.json');
const coverage=read(audit+'couverture.json');
const draft=process.argv.includes('--draft');
const report={result:'RUNNING',draft,questionCount:0,oldQuestionIdentitiesPreserved:0,fieldChangesAccountedFor:0,blankCards:0,correctedCards:0,gradedBanks:0,blankExportsChecked:0,correctedExportsChecked:0,sharedContextChecks:0,profileChecks:0,notesChecked:0};
assert.equal(Object.keys(old).length,Object.keys(current).length);
const expectedChanges=new Map();
for(const c of changes){
 if(c.sourceId)continue;
 const key=c.bank+'/'+c.id,set=expectedChanges.get(key)||new Set();
 for(const field of Object.keys(c.fields||{}))set.add(field);
 expectedChanges.set(key,set);
}
const newSource=new Map(Object.entries(current).flatMap(([b,e])=>e.ue==='ue4'?e.questions.map(q=>[q.sourceId,{b,q}]):[]));
const addedKeys=new Set(adds.map(a=>a.bank+'/'+a.question.id));
const annotationFields=new Set(['reviewNotes','reviewWarningCovered']);
for(const [b,e]of Object.entries(old)){
 for(const before of e.questions){
  const after=e.ue==='ue4'?newSource.get(before.sourceId)?.q:current[b].questions.find(q=>q.id===before.id);
  assert(after,'Lost existing question '+b+'/'+before.id);report.oldQuestionIdentitiesPreserved++;
  const allowed=expectedChanges.get(b+'/'+before.id)||new Set();
  for(const field of new Set([...Object.keys(before),...Object.keys(after)])){
   if(annotationFields.has(field))continue;
   if(e.ue==='ue4'&&['id','category','course','relatedThemes'].includes(field))continue;
   if(field==='allowNoAnswer'&&after.answerIsEmpty&&after.allowNoAnswer===true)continue;
   if(allowed.has(field)){report.fieldChangesAccountedFor++;continue;}
   assert.deepEqual(after[field],before[field],'Unaccounted change '+b+'/'+before.id+'/'+field);
  }
 }
}
for(const [b,e]of Object.entries(current)){
 assert.equal(e.questions.length,new Set(e.questions.map(q=>q.id)).size,b+' duplicate question IDs');
 for(const q of e.questions){
  report.questionCount++;
  assert.equal(q.options.length,new Set(q.options.map(o=>o.id)).size,b+'/'+q.id+' duplicate option IDs');
  if(q.answer){
   const ids=q.tokenMode?q.answer.split(','):q.answer.split('');
   for(const id of ids)assert(q.options.some(o=>o.id===id),b+'/'+q.id+' expected option missing: '+id);
  }
  if(q.answerIsEmpty)assert(q.allowNoAnswer&&q.answer==='',b+'/'+q.id+' all-false must be selectable');
  if(!old[b].questions.some(x=>x.id===q.id)&&e.ue!=='ue4')assert(addedKeys.has(b+'/'+q.id),'Undocumented addition');
 }
}
assert.equal(report.questionCount,report.oldQuestionIdentitiesPreserved+adds.length);
assert.equal(newSource.size,336);
if(!draft){assert.deepEqual(stats.missingCoverage,[]);assert.deepEqual(stats.extraCoverage,[]);}
assert.equal(coverage.length,new Set(coverage.map(c=>c.bank+'/'+c.id)).size,'Duplicate review coverage');
for(const c of coverage){
 const q=current[c.bank]?.questions.find(q=>q.id===c.id);assert(q,'Coverage for absent question');
 assert(Number.isInteger(c.itemsReviewedCount)&&c.itemsReviewedCount>=0&&c.itemsReviewedCount<=q.options.length,'Invalid reviewed item count '+c.bank+'/'+c.id);
}
assert.deepEqual(stats.missingReferences,[]);assert.deepEqual(stats.unresolvedDecisions,[]);

const app=load(target),keys=Object.keys(current);
for(const b of keys){
 app.run(`activeExam=${JSON.stringify(b)};onlyFilledMode=true;loadExam();answers={};correctedIds=new Set();submitted=false;category='all';searchTerm='';statusFilter='all';renderTabs();render();`);
 const cards=app.run('QUESTIONS.map(renderQuestionCard)');
 for(const html of cards){
  assert(!html.includes('class="correction"')&&!html.includes('class="pharma-review"')&&!html.includes('review-opt-flag'),b+' correction leaked before grading');
  report.blankCards++;
 }
 for(let i=0;i<current[b].questions.length;i++)assert.equal(cards[i].includes('class="option option-none'),current[b].questions[i].options.length>0,b+' empty choice must not reveal an all-false key');
 app.run('exportResults()');
 for(const q of app.readExport().questions){
  assert.equal(q.corrige,null);assert.equal(q.erreurs,null);assert.equal(q.points,null);assert.equal(q.commentaires,undefined);assert.equal(q.remarque_corrige,undefined);report.blankExportsChecked++;
 }
 app.run("for(const q of QUESTIONS)answers[q.id]=q.answerIsEmpty?'∅':q.answer||(q.options[0]?.id||'A');gradeAll();");
 const result=clean(app.run('results()'));
 assert.equal(result.ratedCount,app.run('GRADED'),b+' incorrect denominator');
 assert.equal(result.grade,app.run('GRADED')?20:0,b+' reference answers not full score');
 assert.equal(app.run('correctedIds.size'),app.run('TOTAL'));
 report.gradedBanks++;
 for(const q of current[b].questions){
  const html=app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`);
  assert(html.includes('class="correction"'),b+'/'+q.id+' no corrected panel');report.correctedCards++;
  if(q.answerPolarity==='false')for(const o of q.options)assert(html.includes(o.id+' · '+(q.answer.includes(o.id)?'À COCHER':'NE PAS COCHER')),b+'/'+q.id+' incorrect truth label for a negative question');
  if(q.reviewNotes?.length){
   assert(html.includes('class="pharma-review"'));
   for(const n of q.reviewNotes){assert(html.includes(app.run(`esc(${JSON.stringify(n.text)})`)),n.noteId+' missing note');report.notesChecked++;}
  }
  if(q.sharedContexts?.length){
   const filtered=app.run(`renderQuestionList([QUESTIONS.find(q=>q.id===${q.id})])`);
   assert(filtered.indexOf('class="shared-statement"')<filtered.indexOf('class="qcard'),b+'/'+q.id+' common stem missing in filtered view');
   for(const c of q.sharedContexts)for(const im of c.images||[])assert(filtered.includes(im));
   report.sharedContextChecks++;
  }
 }
 app.run('exportResults()');
 for(const q of app.readExport().questions){assert.equal(q.corrige_effectue,true);report.correctedExportsChecked++;}
 app.run('switchProfile(false)');
 assert.equal(app.run('answeredCount()'),0,b+' profiles mixed');
 app.run('exportResults()');
 for(const q of app.readExport().questions){assert.equal(q.corrige,null);assert.equal(q.commentaires,undefined);assert.equal(q.remarque_corrige,undefined);}
 app.run('gradeAll()');assert.equal(app.run('results().grade'),0,b+' blank classic score');
 app.run('switchProfile(true)');assert.equal(app.run('results().grade'),app.run('GRADED')?20:0,b+' saved selective score lost');report.profileChecks++;
}

// Real storage migration: all annual pharmacology answers in both profiles,
// including partial classic corrections and the 25 changes of primary theme.
const annual=read('work/pharma_v3/baseline_exams.json');
const seeded={ssh_pass_selected_exam_v1:Object.entries(annual).find(([,e])=>e.ue==='ue4')[0],ssh_pass_only_filled_mode_v1:'true'};
const expected={filled:{},classic:{}};
for(const [bi,[b,e]]of Object.entries(annual).filter(([,e])=>e.ue==='ue4').entries()){
 for(const mode of ['filled','classic']){
  const answers={},correctedIds=[];
  e.questions.forEach((q,i)=>{
   const answer=['A','BC','DE','ABCDE','∅','','AC'][(bi*3+i+(mode==='classic'?2:0))%7];answers[q.id]=answer;
   const corrected=mode==='filled'?!!answer&&(bi+i)%2===0:bi%3===0;
   if(corrected)correctedIds.push(q.id);
   expected[mode][q.sourceId]={answer,corrected};
  });
  const snap={answers,submitted:mode==='filled'?correctedIds.length>0:bi%3===0};if(mode==='filled')snap.correctedIds=correctedIds;
  seeded[e.storage+(mode==='classic'?'_profil_2_v1':'')]=JSON.stringify(snap);
 }
}
const migrated=load(target,seeded);report.migratedPharmaStates=0;
const pharmaKeys=keys.filter(b=>current[b].ue==='ue4');
for(const mode of ['filled','classic']){
 migrated.run(`switchProfile(${mode==='filled'})`);
 for(const b of pharmaKeys){
  migrated.run(`switchExam(${JSON.stringify(b)})`);
  for(const s of clean(migrated.run('QUESTIONS.map(q=>({sourceId:q.sourceId,answer:selected(q),corrected:isCorrected(q)}))'))){
   assert.deepEqual({answer:s.answer,corrected:s.corrected},expected[mode][s.sourceId]);report.migratedPharmaStates++;
  }
  migrated.run('exportResults()');
  for(const q of migrated.readExport().questions)if(!q.corrige_effectue){assert.equal(q.corrige,null);assert.equal(q.commentaires,undefined);assert.equal(q.remarque_corrige,undefined);}
 }
}
const reloaded=load(target,migrated.data);
for(const mode of ['filled','classic']){
 reloaded.run(`switchProfile(${mode==='filled'})`);
 for(const b of pharmaKeys){
  reloaded.run(`switchExam(${JSON.stringify(b)})`);
  for(const s of clean(reloaded.run('QUESTIONS.map(q=>({sourceId:q.sourceId,answer:selected(q),corrected:isCorrected(q)}))')))assert.deepEqual({answer:s.answer,corrected:s.corrected},expected[mode][s.sourceId]);
 }
}
// Independent non-pharmacology persistence, including existing all-false choices.
const persisted=load(target,app.data);report.reloadedOtherQuestions=0;
for(const b of keys.filter(b=>current[b].ue!=='ue4')){
 persisted.run(`activeExam=${JSON.stringify(b)};onlyFilledMode=true;loadExam()`);
 for(const s of clean(persisted.run('QUESTIONS.map(q=>({id:q.id,answer:selected(q),corrected:isCorrected(q),tokenMode:q.tokenMode,expected:q.answerIsEmpty?"∅":q.answer||(q.options[0]?.id||"A")}))'))){assert.deepEqual(s.answer.split(s.tokenMode?',':'').sort(),s.expected.split(s.tokenMode?',':'').sort());assert(s.corrected);report.reloadedOtherQuestions++;}
}

// Catalogue content, search and theme links never reveal answers or duplicate grading.
app.run(`switchExam(${JSON.stringify(pharmaKeys[0])});renderTabs()`);
const entries=clean(app.run('pharmaCatalogEntries()'));
assert.equal(entries.length,336);assert.equal(new Set(entries.map(e=>e.q.sourceId)).size,336);
const catalog=app.elements.get('#pharma-catalog-results').innerHTML;
assert(!/pharma-review|correction-body|Réponses attendues/.test(catalog));
report.catalogReferences=(catalog.match(/data-pharma-bank=/g)||[]).length;
assert.equal(report.catalogReferences,336+entries.reduce((n,e)=>n+(e.q.relatedThemes||[]).length,0));
for(const year of [...new Set(entries.map(e=>e.q.year))]){
 const count=app.run(`pharmaCatalogEntries().filter(e=>pharmaCatalogMatches(e,${JSON.stringify(year)})).length`);
 assert.equal(count,entries.filter(e=>e.q.year===year).length,'year search misses source year '+year);
}
for(const b of pharmaKeys)for(const field of ['label','title','subtitle','seriesLabel'])assert(!/20\d\d/.test(current[b][field]),b+' still grouped by year');
report.themeCount=pharmaKeys.length;
// Explicit "none" is a real attempted response on ordinary questions too,
// and survives saving/reloading independently of the expected key.
const noneCheck=load(target);
const noneBank=keys.find(b=>current[b].ue!=='ue4'&&current[b].questions.some(q=>q.answer&&!q.tokenMode));
const noneQ=current[noneBank].questions.find(q=>q.answer&&!q.tokenMode);
noneCheck.run(`activeExam=${JSON.stringify(noneBank)};onlyFilledMode=true;loadExam();answers={};correctedIds=new Set();answers[${noneQ.id}]='∅';save();`);
const noneReload=load(target,noneCheck.data);
noneReload.run(`activeExam=${JSON.stringify(noneBank)};onlyFilledMode=true;loadExam();`);
assert.equal(noneReload.run(`selected(QUESTIONS.find(q=>q.id===${noneQ.id}))`),'∅');
const noneResult=clean(noneReload.run(`assessed(QUESTIONS.find(q=>q.id===${noneQ.id}))`));
assert.equal(noneResult.unanswered,false);assert(noneResult.errors>0);
report.uniformNoneChoice='PASS';
report.result='PASS';report.limitation='Script de l’application et HTML contrôlés dans un adaptateur DOM déterministe ; pas de contrôle de mise en page dans un navigateur.';
fs.writeFileSync(path.join(__dirname,(draft?'draft_':'')+'logic_checks.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
