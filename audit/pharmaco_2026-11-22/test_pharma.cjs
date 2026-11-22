const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
class Element {
 constructor(){this.innerHTML='';this.textContent='';this.value='';this.style={};this.dataset={};this.handlers={};this.checked=false;this.attrs={};this.classes=new Set();this.classList={toggle:(x,on)=>{if(on===undefined)on=!this.classes.has(x);if(on)this.classes.add(x);else this.classes.delete(x)},add:x=>this.classes.add(x),remove:x=>this.classes.delete(x)};}
 addEventListener(type,fn){(this.handlers[type]??=[]).push(fn)}
 setAttribute(k,v){this.attrs[k]=v}
 getAttribute(k){return this.attrs[k]}
 scrollIntoView(){}
 focus(){}
 click(){}
 remove(){}
 append(){}
}
function load(filename,initial={}){
 const elements=new Map();const element=k=>{if(!elements.has(k))elements.set(k,new Element());return elements.get(k)};
 const data={...initial};const localStorage={getItem:k=>data[k]??null,setItem:(k,v)=>data[k]=String(v),removeItem:k=>delete data[k]};
 const document={querySelector:element,querySelectorAll:()=>[],body:new Element(),addEventListener(){},getElementById:k=>element('#'+k),createElement:()=>new Element()};
 const window={scrollTo(){},addEventListener(){},confirm:()=>true,print(){}};
 let exportText='';
 class ExportBlob {constructor(parts){exportText=parts.join('')}}
 const exportURL={createObjectURL:()=> 'blob:test-export',revokeObjectURL(){}};
 const context=vm.createContext({document,window,localStorage,console,Blob:ExportBlob,URL:exportURL,setTimeout:()=>0});
 const html=fs.readFileSync(filename,'utf8');const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
 assert.equal(scripts.length,1);vm.runInContext(scripts[0][1],context,{timeout:20000});
 return {context,elements,data,readExport:()=>JSON.parse(exportText),run:code=>vm.runInContext(code,context,{timeout:20000})};
}
const sha=value=>crypto.createHash('sha256').update(typeof value==='string'?value:(JSON.stringify(value)??'__undefined__')).digest('hex');
const draft=process.argv.includes('--draft');
const target=path.join(root,draft?'work/pharma_v3/draft_index.html':'output/site/index.html');
const baseline=load(path.join(root,'work/pharma_v3/baseline_index.html'));
const revised=load(target);
const old=JSON.parse(fs.readFileSync(path.join(root,'work/pharma_v3/baseline_exams.json')));
const record=JSON.parse(fs.readFileSync(path.join(root,'work/pharma_v3/questions_v2.json')));
const themes=JSON.parse(fs.readFileSync(path.join(root,'work/pharma_v3/themes.json')));
const newKeys=Array.from(revised.run('Object.keys(EXAMS).filter(k=>EXAMS[k].ue===\'ue4\')'));
const report={result:'RUNNING',draft,protectedBanks:0,protectedQuestions:0,protectedRenderedStates:0,protectedScores:0,ue4Questions:336,ue4Items:1680,themeCount:newKeys.length,migratedAnswers:0,migratedCorrectedStates:0,classicPartialThemes:0};
assert.equal(newKeys.length,15);
assert.equal(sha(revised.run('UNIT_COURSES.ue4')),sha(themes));
assert.equal(revised.run('Object.values(EXAMS).reduce((n,b)=>n+b.questions.length,0)'),2788);
assert.equal(revised.run('Object.keys(EXAMS).length'),217);
const bySource=new Map(record.map(r=>[r.question.sourceId,r]));
const seen=new Set();
for(const key of newKeys){
 const b=revised.run(`EXAMS[${JSON.stringify(key)}]`);
 assert(b.pharmaGrouped);
 for(const field of ['label','title','subtitle','seriesLabel'])assert(!/20\d\d/.test(b[field]),key+' still split by year');
 assert.equal(b.year,undefined);assert.equal(b.session,undefined);
 assert.equal(b.questions.length,new Set(b.questions.map(q=>q.id)).size);
 for(const q of b.questions){
  assert(!seen.has(q.sourceId));seen.add(q.sourceId);
  const r=bySource.get(q.sourceId);assert(r);
  for(const field of ['answer','rawAnswer','answerIsEmpty','weight','sourceNumber','subjectPage','correctionNumber','correctionPage','allowNoAnswer']){
   const expectedValue=!draft&&q.sourceId==='ue4:2023-2024:S2:q05'&&field==='answer'?'ACE':r.question[field];
   assert.equal(sha(q[field]),sha(expectedValue),q.sourceId+' '+field);
  }
  assert.equal(q.legacyProgress.storage,r.legacyStorage);assert.equal(q.legacyProgress.id,r.legacyId);
  assert.equal(q.options.map(o=>o.id).join(''),'ABCDE');
 }
}
assert.equal(seen.size,336);
for(const [key,bank] of Object.entries(old)){
 if(bank.ue==='ue4')continue;
 assert.equal(sha(bank),sha(revised.run(`EXAMS[${JSON.stringify(key)}]`)),key+' data altered');
 report.protectedBanks++;report.protectedQuestions+=bank.questions.length;
 for(const state of ['blank','answered','corrected']){
  for(const app of [baseline,revised])app.run(`activeExam=${JSON.stringify(key)};onlyFilledMode=true;loadExam();answers={};correctedIds=new Set();submitted=false;${state==='blank'?'':"for(const q of QUESTIONS)answers[q.id]='A';"}${state==='corrected'?'correctedIds=new Set(QUESTIONS.map(q=>q.id));submitted=true;':''}`);
  assert.equal(sha(baseline.run('QUESTIONS.map(renderQuestionCard)')),sha(revised.run('QUESTIONS.map(renderQuestionCard)')),key+' '+state+' rendering altered');
  assert.equal(sha(baseline.run('results()')),sha(revised.run('results()')),key+' scoring altered');
  report.protectedRenderedStates+=bank.questions.length;report.protectedScores++;
 }
}

// Import all original annual storage keys in both profiles. Each answer carries
// a distinct pattern and classic correction is deliberately partial by theme.
const seeded={ssh_pass_selected_exam_v1:record[0].legacyBank,ssh_pass_only_filled_mode_v1:'true'};
const expected={filled:{},classic:{}};
const oldBanks=Object.entries(old).filter(([,b])=>b.ue==='ue4');
for(let bi=0;bi<oldBanks.length;bi++){
 const [key,b]=oldBanks[bi];
 for(const mode of ['filled','classic']){
  const answers={},correctedIds=[];
  b.questions.forEach((q,i)=>{
   const code=(bi*3+i+(mode==='classic'?2:0))%7;
   const answer=['A','BC','DE','ABCDE','∅','','AC'][code];answers[q.id]=answer;
   const corrected=mode==='filled'?!!answer&&(bi+i)%2===0:bi%3===0;
   if(corrected)correctedIds.push(q.id);
   expected[mode][q.sourceId]={answer,corrected};
  });
  const snap={answers,submitted:mode==='filled'?correctedIds.length>0:bi%3===0};
  if(mode==='filled')snap.correctedIds=correctedIds;
  seeded[b.storage+(mode==='classic'?'_profil_2_v1':'')]=JSON.stringify(snap);
 }
}
const migration=load(target,seeded);
assert(migration.run('groupedPharma()'),'old active annual bank did not resolve to its theme');
for(const mode of ['filled','classic']){
 migration.run(`switchProfile(${mode==='filled'})`);
 for(const key of newKeys){
  migration.run(`switchExam(${JSON.stringify(key)})`);
  const states=migration.run('QUESTIONS.map(q=>({sourceId:q.sourceId,answer:selected(q),corrected:isCorrected(q)}))');
  for(const item of states){
   assert.equal(item.answer,expected[mode][item.sourceId].answer,item.sourceId+' '+mode+' answer');
   assert.equal(item.corrected,expected[mode][item.sourceId].corrected,item.sourceId+' '+mode+' correction');
   report.migratedAnswers++;report.migratedCorrectedStates++;
  }
  migration.run('exportResults()');
  const exported=migration.readExport();
  for(const item of exported.questions){
   const wanted=expected[mode][item.identifiant_source];
   assert.equal(item.corrige_effectue,wanted.corrected);
   if(!wanted.corrected){
    assert.equal(item.corrige,null);assert.equal(item.erreurs,null);assert.equal(item.points,null);
    assert.equal(item.commentaires,undefined);assert.equal(item.remarque_corrige,undefined,'source warning leaked before correction');
   }
  }
  if(mode==='classic'&&states.some(x=>x.corrected)&&states.some(x=>!x.corrected)){
   report.classicPartialThemes++;
   assert(migration.elements.get('#toolbar-content').innerHTML.includes('id="submit-all"'),key+' cannot finish a partially migrated classic theme');
   const html=migration.elements.get('#questions').innerHTML;
   assert.equal((html.match(/<details class="correction"/g)||[]).length,states.filter(x=>x.corrected).length,key+' classic exposed uncorrected answers');
  }
 }
}
assert(report.classicPartialThemes>0);
for(const [key,value] of Object.entries(seeded))if(!key.startsWith('ssh_pass_'))assert.equal(migration.data[key],value,'legacy store overwritten: '+key);
const reload=load(target,migration.data);
for(const mode of ['filled','classic']){
 reload.run(`switchProfile(${mode==='filled'})`);
 for(const key of newKeys){
  reload.run(`switchExam(${JSON.stringify(key)})`);
  for(const item of reload.run('QUESTIONS.map(q=>({sourceId:q.sourceId,answer:selected(q),corrected:isCorrected(q)}))'))assert.deepEqual(JSON.parse(JSON.stringify({answer:item.answer,corrected:item.corrected})),expected[mode][item.sourceId]);
 }
}

let gradedThemes=0,noteQuestions=0,groupChecks=0;
for(const key of newKeys){
 const app=load(target);
 app.run(`switchExam(${JSON.stringify(key)});answers={};correctedIds=new Set();submitted=false;render();`);
 const initial=app.elements.get('#questions').innerHTML;
 assert(!initial.includes('class="correction"')&&!initial.includes('class="pharma-review"'),key+' exposes review or correction before grading');
 if(!app.run('TOTAL')){assert(!/NaN|Infinity/.test(app.elements.get('#side-track').style.width));continue;}
 app.run("for(const q of QUESTIONS)answers[q.id]=q.answerIsEmpty?'∅':q.answer||'A';gradeAll();");
 assert.equal(app.run('results().grade'),app.run('GRADED')?20:0,key+' expected key not 20');
 assert.equal(app.run('results().ratedCount'),app.run('GRADED'));
 for(const q of app.run('QUESTIONS')){
  const markup=app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`);
  if(q.warning||q.reviewNotes?.length){noteQuestions++;assert(markup.includes('class="pharma-review"'));assert(markup.includes('ronéo'));}
  if(q.sharedContexts?.length){
   const filtered=app.run(`renderQuestionList([QUESTIONS.find(q=>q.id===${q.id})])`);
   assert(filtered.indexOf('class="shared-statement"')<filtered.indexOf('class="qcard'));
   for(const c of q.sharedContexts)for(const image of c.images||[])assert(filtered.includes(image));
   groupChecks++;
  }
 }
 app.run('switchProfile(false)');assert.equal(app.run('answeredCount()'),0,'profiles contaminated');
 app.run('gradeAll()');assert.equal(app.run('correctedIds.size'),app.run('TOTAL'));assert.equal(app.run('results().grade'),0,'blank classic answers are not 0');
 app.run('switchProfile(true)');assert.equal(app.run('results().grade'),app.run('GRADED')?20:0,'selective grade lost');
 gradedThemes++;
}

// Reset only one theme/profile, then reload: old bank state must not resurrect.
for(const mode of ['filled','classic']){
 const app=load(target,seeded);app.run(`switchProfile(${mode==='filled'})`);
 const key=newKeys.find(k=>app.run(`EXAMS[${JSON.stringify(k)}].questions.length>0`));
 app.run(`switchExam(${JSON.stringify(key)})`);
 const ids=Array.from(app.run('QUESTIONS.map(q=>q.sourceId)'));
 app.run('reset()');
 const next=load(target,app.data);next.run(`switchProfile(${mode==='filled'});switchExam(${JSON.stringify(key)})`);
 assert.equal(next.run('answeredCount()'),0);assert.equal(next.run('correctedIds.size'),0);
 const snapshot=next.run('readPharmaProgress()');
 for(const [sid,value] of Object.entries(expected[mode])){
  const wanted=ids.includes(sid)?{answer:'',corrected:false}:value;
  assert.deepEqual(JSON.parse(JSON.stringify(snapshot.bySource[sid])),wanted,'reset touched another theme or restored old answers: '+sid);
 }
 const other=mode==='filled'?'classic':'filled';next.run('switchProfile(!onlyFilledMode)');
 const otherSnapshot=next.run('readPharmaProgress()');
 for(const sid of ids)assert.deepEqual(JSON.parse(JSON.stringify(otherSnapshot.bySource[sid])),expected[other][sid],'reset affected other profile');
}
Object.assign(report,{result:'PASS',themesScored:gradedThemes,reviewBoxesChecked:noteQuestions,sharedContextQuestionsChecked:groupChecks,sourceAnswersReloaded:true,resetDoesNotResurrectLegacy:true,otherProfilesAndThemesPreserved:true,exportsHideUncorrectedAnswersAndNotes:true,limitation:'Application script and HTML are tested using a deterministic DOM adapter; this is not a browser layout test.'});
fs.writeFileSync(path.join(root,'work/pharma_v3/'+(draft?'draft_':'')+'logic_checks.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
