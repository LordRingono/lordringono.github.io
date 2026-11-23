/* Execute the actual release script. DOM adapter checks behavior, not browser pixels. */
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=__dirname,workspace=path.resolve(root,'../..');
const site=path.join(workspace,'output/site'),filename=path.join(site,'index.html');
const {load}=require(path.join(site,'audit/revision_v4/production/dom_adapter.cjs'));
const baseline=JSON.parse(fs.readFileSync(path.join(root,'baseline_exams.json'),'utf8'));
const app=load(filename),data=JSON.parse(JSON.stringify(app.run('EXAMS')));
const clone=x=>JSON.parse(JSON.stringify(x)),quoted=x=>JSON.stringify(x);
const report={method:'Actual site JavaScript with V4 DOM adapter; no browser pixel rendering claimed.',errors:[],banks:[],cardStates:0,keys:0,files:0,profiles:0};
const checkedFiles=new Set();
function file(p){
 if(!p||checkedFiles.has(p))return;
 const x=path.resolve(site,p.split('#')[0]);assert(x.startsWith(site+path.sep),p);assert(fs.existsSync(x),p);
 checkedFiles.add(p);report.files++;
}
function cardCheck(q,html,done,bank){
 const roles=[...html.matchAll(/data-source-role="(subject|correction)"/g)].map(m=>m[1]);
 assert.deepEqual(roles,done?['subject','correction']:['subject'],bank+'/'+q.id+' source menus');
 for(const role of ['subject','correction']){
  const copy=q.sourceCopies[role];const subjectReady=app.run(`subjectOriginalReady(QUESTIONS.find(q=>q.id===${q.id}))`);
  const visible=role==='subject'?(!copy.afterCorrection||subjectReady):done;
  const menu=html.match(new RegExp('<details[^>]*data-source-role="'+role+'"[\\s\\S]*?</details>'))?.[0]||'';
  for(const c of copy.captures||[])assert.equal(menu.includes(c.src),visible,bank+'/'+q.id+'/'+role+' exposure');
 }
 if(q.imagesAfterCorrection)for(const src of [...(q.images||[]),...(q.stemImages||[])])assert.equal(html.includes(src),app.run(`subjectOriginalReady(QUESTIONS.find(q=>q.id===${q.id}))`),bank+'/'+q.id+' annotated figure gate');
 if((q.sourceCopies.subject.afterCorrection||q.imagesAfterCorrection)&&!done){
  const metadata=html.match(/<div class="qsource">[\s\S]*?<\/div>/)?.[0]||'';
  assert(!metadata.includes('<a href='),bank+'/'+q.id+' annotated direct PDF link gate');
 }
 assert.equal(html.includes('class="correction"'),done,bank+'/'+q.id+' correction gate');
 if(!done){assert(!html.includes('class="pharma-review"'));assert(!html.includes('review-opt-flag'));}
 report.cardStates++;
}
function switchBank(bank,mode){app.run(`switchProfile(${mode});switchExam(${quoted(bank)});`);}
function snap(){return clone(app.run(`({mode:onlyFilledMode,bank:activeExam,questions:QUESTIONS.map(q=>({id:q.id,chosen:selected(q),corrected:isCorrected(q)})),grade:results().grade})`));}
function choose(qid,letter,checked=true){
 const handler=app.elements.get('#questions').handlers.change?.[0];assert(handler);
 const input={dataset:{q:String(qid)},value:letter,checked,closest(s){if(s==='input[data-q]')return this;if(s==='.option')return {classList:{toggle(){}}};return null;}};
 handler({target:input});
}
const snapshots={};
try{
 assert.deepEqual(Object.keys(data).sort(),Object.keys(baseline).sort());
 for(const [bank,exam] of Object.entries(data)){
  assert.equal(exam.storage,baseline[bank].storage,bank+' progress storage');
  const ids=new Set(exam.questions.map(q=>q.id));assert.equal(ids.size,exam.questions.length);
  for(const q of baseline[bank].questions)assert(ids.has(q.id),bank+'/'+q.id+' lost');
  for(const q of exam.questions){
   assert.equal(new Set(q.options.map(o=>o.id)).size,q.options.length,bank+'/'+q.id+' duplicate labels');
   for(const role of ['subject','correction']){
    const copy=q.sourceCopies?.[role];assert(copy,bank+'/'+q.id+'/'+role+' missing metadata');
    if(copy.missing){assert(copy.reason);assert.equal(copy.captures.length,0);}
    else{assert(copy.captures?.length>0);file(copy.pdf);file(copy.original);for(const doc of copy.documents||[]){file(doc.pdf);file(doc.original);}for(const c of copy.captures){assert(Number.isInteger(c.page)&&c.page>0);file(c.src);file(c.pdf);}}
   }
  }
  switchBank(bank,true);app.run('reset()');
  for(const q of exam.questions)cardCheck(q,app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`),false,bank);
  for(const q of exam.questions.filter(q=>q.options.length===0)){
   assert(app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`).includes('J’ai fait cet exercice (hors note)'));
   choose(q.id,'∅');app.run('gradeAll()');
   assert(app.run(`isCorrected(QUESTIONS.find(q=>q.id===${q.id}))`));
   assert.equal(app.run('results().ratedCount'),0);
   cardCheck(q,app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`),true,bank);
   app.run('reset()');
  }
  for(const q of exam.questions)for(const context of q.sharedContexts||[])if(context.imagesAfterCorrection){
   const contextHTML=app.run(`sharedStatement(${quoted(context)},QUESTIONS.find(q=>q.id===${q.id}),'gate-test')`);
   for(const src of context.images||[])assert(!contextHTML.includes(src),bank+'/'+q.id+' shared annotated figure gate');
   assert(!contextHTML.includes('<a href='),bank+'/'+q.id+' shared annotated source link gate');
   const ids=exam.questions.filter(other=>(other.sharedContexts||[]).some(c=>c.id===context.id)).map(other=>other.id);
   app.run(`correctedIds=new Set([${ids[0]}]);submitted=true;`);
   const partial=app.run(`sharedStatement(${quoted(context)},QUESTIONS.find(q=>q.id===${q.id}),'gate-partial')`);
   if(ids.length>1){for(const src of context.images||[])assert(!partial.includes(src),bank+'/'+q.id+' partial shared figure gate');assert(!partial.includes('<a href='));}
   app.run(`correctedIds=new Set(${quoted(ids)});`);
   const complete=app.run(`sharedStatement(${quoted(context)},QUESTIONS.find(q=>q.id===${q.id}),'gate-complete')`);
   for(const src of context.images||[])assert(complete.includes(src),bank+'/'+q.id+' completed shared figure access');
   app.run('correctedIds.clear();submitted=false;');
  }
  const rated=clone(app.run('QUESTIONS.filter(isGradable).map(q=>q.id)'));
  const first=exam.questions.find(q=>rated.includes(q.id));
  if(first){
   const key=first.answerIsEmpty?['∅']:(first.tokenMode?first.answer.split(','):first.answer.split(''));
   for(const letter of key)choose(first.id,letter);
   app.run('gradeAll()');assert.equal(app.run('results().ratedCount'),1);assert.equal(app.run('results().grade'),20);
   for(const q of exam.questions)cardCheck(q,app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`),q.id===first.id,bank);
  }
  app.run(`answers=Object.fromEntries(QUESTIONS.map(q=>[q.id,isGradable(q)?(q.answerIsEmpty?'∅':q.tokenMode?cleanPharmaAnswer(q,q.answer):uniqueSortedLetters(q.answer)):(q.options[0]?.id||'')]));gradeAll();`);
  const selective=clone(app.run('results()'));
  assert.equal(selective.ratedCount,rated.length);
  if(rated.length)assert.equal(selective.grade,20);
  for(const row of selective.data)if(!row.nonGraded){assert.equal(row.points,10);assert.equal(row.errors,0);report.keys++;}
  snapshots[bank]={selective:snap()};
  switchBank(bank,false);assert.equal(app.run('answeredCount()'),0,bank+' profile contamination');
  for(const q of exam.questions)cardCheck(q,app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`),false,bank);
  app.run(`answers=Object.fromEntries(QUESTIONS.map(q=>[q.id,isGradable(q)?(q.answerIsEmpty?'∅':q.tokenMode?cleanPharmaAnswer(q,q.answer):uniqueSortedLetters(q.answer)):(q.options[0]?.id||'')]));gradeAll();`);
  if(rated.length)assert.equal(app.run('results().grade'),20);
  for(const q of exam.questions)cardCheck(q,app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`),true,bank);
  // Exercise 0/1/2/3 errors for every rated question, preserving official keys.
  for(const q of exam.questions.filter(q=>rated.includes(q.id))){
   const available=q.options.filter(o=>!(q.ignoredOptions||[]).includes(o.id));
   const truth=new Set(q.answerIsEmpty?[]:(q.tokenMode?q.answer.split(','):q.answer.split('')));
   for(let count=0;count<=Math.min(3,available.length);count++){
    const selection=new Set(truth);for(const o of available.slice(0,count)){if(selection.has(o.id))selection.delete(o.id);else selection.add(o.id);}
    const value=selection.size?[...selection].join(q.tokenMode?',':''):'∅';
    const result=clone(app.run(`answers[${q.id}]=${quoted(value)};assessed(QUESTIONS.find(q=>q.id===${q.id}))`));
    assert.equal(result.errors,count,bank+'/'+q.id+' error count');assert.equal(result.points,[10,5,2,0][count]);
   }
  }
  app.run(`answers=Object.fromEntries(QUESTIONS.map(q=>[q.id,isGradable(q)?(q.answerIsEmpty?'∅':q.tokenMode?cleanPharmaAnswer(q,q.answer):uniqueSortedLetters(q.answer)):(q.options[0]?.id||'')]));save();`);
  if(first){app.run(`modify();answers[${first.id}]='';gradeAll();`);assert(app.run('results().grade')<20);}
  snapshots[bank].classic=snap();
  switchBank(bank,true);assert.deepEqual(snap(),snapshots[bank].selective,bank+' selective profile changed');
  report.banks.push({bank,questions:exam.questions.length,graded:rated.length,passed:true});
 }
 const reloaded=load(filename,app.data);
 for(const bank of Object.keys(data))for(const [mode,key] of [[true,'selective'],[false,'classic']]){
  reloaded.run(`switchProfile(${mode});switchExam(${quoted(bank)});`);
  const state=clone(reloaded.run(`({mode:onlyFilledMode,bank:activeExam,questions:QUESTIONS.map(q=>({id:q.id,chosen:selected(q),corrected:isCorrected(q)})),grade:results().grade})`));
  assert.deepEqual(state,snapshots[bank][key],bank+' persistence '+key);report.profiles++;
 }
 // Real V5 saves: letter meaning is preserved in both profiles, and only the
 // questions whose options changed must be validated again.
 report.migrationProfiles=0;
 const migrations={
  'histo.ann.tech':{1:['BCD','CDE'],5:['D','E'],6:['D','D'],7:['CD','DE']},
  'histo.ann.tc':{5:['ACE','ACE']},
  'bio.cm4':{5:['ACE','BDF']},
  'bio.cm5':{13:['BD','CE']},
  'bio.cm7':{12:['',''],13:['',''],14:['','']},
  'bio.cm8':{10:['AG','BH'],13:['ABCFIJ','BCD'],15:['AB','BC'],16:['AH','BI'],17:['','ADE']},
  'bio.ann.cm4':{9:['','']},
  'bio.ann.cm9':{10:['','']},
  'embryo.aut.meiose':{5:['KN','KN']},
  'embryo.aut.fec':{23:['BM','BM']}
 };
 for(const [bank,repairs] of Object.entries(migrations)){
  const exam=baseline[bank],oldAnswers=Object.fromEntries(exam.questions.map(q=>[q.id,q.options[0].id]));
  for(const [id,[before]] of Object.entries(repairs))oldAnswers[id]=before;
  const oldSave={answers:oldAnswers,submitted:true,correctedIds:exam.questions.map(q=>q.id)};
  const seed={ssh_pass_selected_exam_v1:bank,ssh_pass_only_filled_mode_v1:'true',[exam.storage]:JSON.stringify(oldSave),[exam.storage+'_profil_2_v1']:JSON.stringify(oldSave)};
  const migrated=load(filename,seed);
  for(const mode of [true,false]){
   migrated.run(`switchProfile(${mode});`);
   const state=clone(migrated.run('({answers,done:QUESTIONS.filter(isCorrected).map(q=>q.id)})'));
   for(const q of exam.questions){
    assert.equal(state.answers[q.id],repairs[q.id]?.[1]||oldAnswers[q.id],bank+'/'+q.id+' saved letter mapping');
    assert.equal(state.done.includes(q.id),!Object.hasOwn(repairs,q.id),bank+'/'+q.id+' targeted revalidation');
   }
   for(const [id,[,after]] of Object.entries(repairs)){
    assert.equal(state.answers[id]||'',after,bank+'/'+id+' restored question choice');
    assert(!state.done.includes(Number(id)),bank+'/'+id+' new/repaired question pending');
   }
   migrated.run('save()');
   const stored=JSON.parse(migrated.data[exam.storage+(mode?'':'_profil_2_v1')]);
   assert.equal(stored.itemSchemaVersion,6);
   assert.deepEqual(JSON.parse(migrated.data[exam.storage+(mode?'':'_profil_2_v1')+'_before_v6_item_repair']),oldSave,'original progress backup');
   report.migrationProfiles++;
  }
  const again=load(filename,migrated.data);
  for(const mode of [true,false]){
   again.run(`switchProfile(${mode});`);
   for(const [id,[,after]] of Object.entries(repairs))assert.equal(again.run(`answers[${id}]`)||'',after,'migration must run once');
  }
  // Finishing a migrated classic session grades every question, exactly as
  // the original classic profile does, then persists this normal state.
  again.run('switchProfile(false);gradeAll();');
  assert(again.run('QUESTIONS.every(isCorrected)'));
  const completed=load(filename,again.data);
  assert(completed.run('QUESTIONS.every(isCorrected)'));
 }
 report.result='PASS';
}catch(error){report.errors.push(error.stack||String(error));report.result='FAIL';}
fs.writeFileSync(path.join(root,'runtime_report.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,banks:report.banks.length,errors:report.errors},null,2));
if(report.result!=='PASS')process.exitCode=1;
