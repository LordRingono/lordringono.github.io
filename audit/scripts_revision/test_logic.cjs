// Execute the unchanged application script with a small deterministic DOM adapter.
// This verifies rendering strings and state transitions; it is not a browser layout test.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const crypto=require('crypto');
const assert=require('assert/strict');
const root=path.resolve(__dirname,'..');

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
 const context=vm.createContext({document,window,localStorage,console,Blob,URL,setTimeout:()=>0});
 const html=fs.readFileSync(filename,'utf8');const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
 assert.equal(scripts.length,1);vm.runInContext(scripts[0][1],context,{timeout:20000});
 return {context,elements,data,run:code=>vm.runInContext(code,context,{timeout:20000})};
}
const sha=value=>crypto.createHash('sha256').update(typeof value==='string'?value:JSON.stringify(value)).digest('hex');
const baseline=load(path.join(root,'baseline/site/index.html'));
const revised=load(path.join(root,'output/site/index.html'));
const keys=baseline.run('Object.keys(EXAMS)');
const revisedED=['ue2.ed.annales','ue2.ed.2025-2026','ue2.ed.2026-2027'];
const repairedKeys={6:['','C'],7:['A','B'],8:['','BC'],13:['','BD']};
const protectedReport={banks:keys.length-revisedED.length,questions:0,assets:0,rendered_states:0,score_checks:0,revised_ED_banks:3,revised_ED_questions:0,revised_ED_score_checks:0,documented_ED_key_repairs:repairedKeys};
for(const key of keys){
 const qkey=JSON.stringify(key);
 const ed=revisedED.includes(key);
 if(!ed){
  assert.equal(sha(baseline.run(`EXAMS[${qkey}]`)),sha(revised.run(`EXAMS[${qkey}]`)),key+' data changed');
  protectedReport.questions+=baseline.run(`EXAMS[${qkey}].questions.length`);
 }else{
  const invariant=`({storage:EXAMS[${qkey}].storage,questions:EXAMS[${qkey}].questions.map(q=>({id:q.id,answer:${key==='ue2.ed.annales'?"[6,7,8,13].includes(q.id)?'DOCUMENTED_REPAIR':q.answer":'q.answer'},answerIsEmpty:q.answerIsEmpty,weight:q.weight,tokenMode:q.tokenMode,ignoredOptions:q.ignoredOptions,optionIds:q.options.map(o=>o.id)}))})`;
  assert.equal(sha(baseline.run(invariant)),sha(revised.run(invariant)),key+' identifiers, key or scoring changed');
  if(key==='ue2.ed.annales')for(const [id,[oldKey,newKey]] of Object.entries(repairedKeys)){
   assert.equal(baseline.run(`EXAMS[${qkey}].questions.find(q=>q.id===${id}).answer`),oldKey);
   assert.equal(revised.run(`EXAMS[${qkey}].questions.find(q=>q.id===${id}).answer`),newKey);
  }
  protectedReport.revised_ED_questions+=baseline.run(`EXAMS[${qkey}].questions.length`);
 }
 for(const state of ['blank','answered','corrected']){
  for(const app of [baseline,revised])app.run(`activeExam=${qkey};onlyFilledMode=true;loadExam();answers={};correctedIds=new Set();submitted=false;${state!=='blank'?"for(const q of QUESTIONS)answers[q.id]='A';":''}${state==='corrected'?'correctedIds=new Set(QUESTIONS.map(q=>q.id));submitted=true;':''}`);
  if(!ed)assert.equal(sha(baseline.run('QUESTIONS.map(renderQuestionCard)')),sha(revised.run('QUESTIONS.map(renderQuestionCard)')),key+' '+state+' markup changed');
  const scoreExpression=ed?'(()=>{const r=results();r.data=r.data.map(({q,...v})=>({id:q.id,...v}));return r;})()':'results()';
  if(key!=='ue2.ed.annales')assert.equal(sha(baseline.run(scoreExpression)),sha(revised.run(scoreExpression)),key+' '+state+' score changed');
  if(!ed){protectedReport.rendered_states+=baseline.run('QUESTIONS.length');protectedReport.score_checks++;}
  else if(key!=='ue2.ed.annales')protectedReport.revised_ED_score_checks++;
 }
}
for(const name of fs.readdirSync(path.join(root,'baseline/site/static'))){
 const bp=path.join(root,'baseline/site/static',name);if(!fs.statSync(bp).isFile())continue;
 assert.equal(sha(fs.readFileSync(bp)),sha(fs.readFileSync(path.join(root,'output/site/static',name))),name+' changed');protectedReport.assets++;
}
protectedReport.result='PASS';

for(const key of revisedED){
 const oldApp=load(path.join(root,'baseline/site/index.html'));
 oldApp.run(`switchExam(${JSON.stringify(key)});answers={1:'A'};correctedIds=new Set([1]);submitted=true;save();`);
 const migrated=load(path.join(root,'output/site/index.html'),oldApp.data);
 assert.equal(migrated.run('selected(QUESTIONS[0])'),'A',key+' saved answer lost');
 assert.equal(migrated.run('isCorrected(QUESTIONS[0])'),true,key+' corrected state lost');
 migrated.run("answers={};correctedIds=new Set();submitted=false;for(const q of QUESTIONS)answers[q.id]=q.answer||'A';gradeAll();");
 assert.equal(migrated.run('results().grade'),20,key+' correct ED answers not perfect');
}
protectedReport.ED_saved_progress_migrations=3;
fs.writeFileSync(path.join(root,'work/review/protected_check.json'),JSON.stringify(protectedReport,null,2));
console.log('Protected content:',JSON.stringify(protectedReport));

const newKeys=revised.run('Object.keys(EXAMS).filter(k=>EXAMS[k].questions.some(q=>q.fromCompilation))');
if(newKeys.length){
 const errors=[];
 for(const key of newKeys){
  revised.run(`activeExam=${JSON.stringify(key)};onlyFilledMode=true;loadExam();answers={};correctedIds=new Set();submitted=false;renderTabs();render();`);
  const firstRender=revised.elements.get('#questions').innerHTML;
  assert(!firstRender.includes('class="correction"'),key+' exposes correction before submit');
  assert(!firstRender.includes('annales-correction-images'),key+' exposes correction image before submit');
  assert.equal((firstRender.match(/class="option option-none/g)||[]).length,revised.run('TOTAL'));
  revised.run("for(const q of QUESTIONS)answers[q.id]=q.answerIsEmpty?'∅':q.answer||'A';gradeAll();");
  assert.equal(revised.run('results().grade'),revised.run('GRADED')?20:0,key+' answer key not perfect');
  const result=revised.run('results()');assert.equal(result.ratedCount,revised.run('GRADED'));
  revised.run('switchProfile(false)');assert.equal(revised.run('answeredCount()'),0,key+' profiles contaminated');
  revised.run('switchProfile(true)');assert.equal(revised.run('results().grade'),revised.run('GRADED')?20:0,key+' selective history lost');
 }
 const key=newKeys[0];
 const app=load(path.join(root,'output/site/index.html'));
 app.run(`switchExam(${JSON.stringify(key)});answers={};correctedIds=new Set();submitted=false;render();`);
 const handler=app.elements.get('#questions').handlers.change[0];
 function change(qid,id,checked){const row=new Element();const input={value:id,checked,dataset:{q:String(qid)},closest:s=>s==='input[data-q]'?input:row};handler({target:input});}
 change(1,'∅',true);assert.equal(app.run('selected(QUESTIONS[0])'),'∅');
 change(1,'A',true);assert.equal(app.run('selected(QUESTIONS[0])'),'A');
 change(1,'∅',true);assert.equal(app.run('selected(QUESTIONS[0])'),'∅');
 change(1,'∅',false);assert.equal(app.run('selected(QUESTIONS[0])'),'');
 change(1,'A',true);app.run('gradeAll()');assert.equal(app.run('correctedIds.size'),1);
 if(app.run('QUESTIONS.length')>1){assert.equal(app.run('isCorrected(QUESTIONS[1])'),false);assert(!app.run('renderQuestionCard(QUESTIONS[1])').includes('class="correction"'));}
 app.run('switchProfile(false)');assert.equal(app.run('answeredCount()'),0);change(1,'B',true);app.run('gradeAll()');
 app.run('switchProfile(true)');assert.equal(app.run('selected(QUESTIONS[0])'),'A');
 app.run('switchProfile(false)');assert.equal(app.run('selected(QUESTIONS[0])'),'B');
 const restored=load(path.join(root,'output/site/index.html'),app.data);assert.equal(restored.run('selected(QUESTIONS[0])'),'B');
 restored.run('switchProfile(true)');assert.equal(restored.run('selected(QUESTIONS[0])'),'A');
 const emptyBank=newKeys.find(k=>revised.run(`EXAMS[${JSON.stringify(k)}].questions.some(q=>q.answerIsEmpty)`));
 if(emptyBank){const app=load(path.join(root,'output/site/index.html'));app.run(`switchExam(${JSON.stringify(emptyBank)});const emptyQ=QUESTIONS.find(q=>q.answerIsEmpty);answers[emptyQ.id]='∅';gradeAll();`);assert.equal(app.run('results().grade'),20);assert.equal(app.run('results().ratedCount'),1);assert.equal(app.run('results().unanswered'),app.run('TOTAL')-1);}
 const report={result:'PASS',new_banks:newKeys.length,checks:['Every bank renders with correction hidden','All expected answers score20','All new questions have explicit empty-response control','Profiles independent and restored after reload','Selective grading leaves blank QCM uncorrected','Explicit empty answer distinct from blank','Answer/image markup generated without runtime error'],limitation:'State and HTML checks run with a deterministic DOM adapter; native browser launch was unavailable in this executor.'};
 fs.writeFileSync(path.join(root,'work/review/new_logic_check.json'),JSON.stringify(report,null,2));console.log('New content:',JSON.stringify(report));
}

// Verify the bug's actual failure modes: grouping, a hidden first member,
// nested statements, shared-text search and navigation back to the data.
const contextApp=load(path.join(root,'output/site/index.html'));
const contextKeys=contextApp.run('Object.keys(EXAMS).filter(k=>EXAMS[k].questions.some(q=>q.sharedContexts?.length))');
let contextsChecked=0,filteredChecks=0;
for(const key of contextKeys){
 contextApp.run(`activeExam=${JSON.stringify(key)};loadExam();answers={};correctedIds=new Set();submitted=false;category='all';statusFilter='all';searchTerm='';renderQuestions();`);
 const questions=contextApp.run('JSON.parse(JSON.stringify(QUESTIONS))');
 const markup=contextApp.elements.get('#questions').innerHTML;
 const contextIds=[...new Set(questions.flatMap(q=>(q.sharedContexts||[]).map(c=>c.id)))];
 assert(!markup.includes('class="correction"'),key+' exposes correction');
 for(const id of contextIds){
  const members=questions.filter(q=>(q.sharedContexts||[]).some(c=>c.id===id));
  const stem=members[0].sharedContexts.find(c=>c.id===id);
  const escaped=contextApp.run(`esc(${JSON.stringify(id)})`);
  const blockIndex=markup.indexOf(`data-context-key="${escaped}"`);
  assert(blockIndex>=0&&blockIndex<markup.indexOf(`id="q${members[0].id}"`),key+' missing stem before first question '+id);
  const lastId=members.at(-1).id;
  const lastOnly=contextApp.run(`renderQuestionList(QUESTIONS.filter(q=>q.id===${lastId}))`);
  assert(lastOnly.includes(`data-context-key="${escaped}"`),key+' context lost after hiding first member');
  assert(lastOnly.includes('class="shared-statement-links"'),key+' no link back to the context');
  for(const image of stem.images||[])assert(lastOnly.includes(`src="${image}"`),key+' shared image missing');
  if(stem.text){
   contextApp.run(`searchTerm=${JSON.stringify(stem.text)};renderQuestions();`);
   const searched=contextApp.elements.get('#questions').innerHTML;
   for(const member of members)assert(searched.includes(`id="q${member.id}"`),key+' shared text not searchable');
   contextApp.run("searchTerm='';");
  }
  contextsChecked++;filteredChecks++;
 }
}
contextApp.run(`
 const template=JSON.parse(JSON.stringify(QUESTIONS[0]));
 const parent={id:'test-parent',text:'Données partagées',questionNumbers:[1,2,3,4]};
 const child={id:'test-child',text:'Précision pour le sous-groupe',questionNumbers:[2,3]};
 QUESTIONS=[1,2,3,4].map(id=>({...template,id,sharedContexts:id===2||id===3?[parent,child]:[parent]}));
 answers={};correctedIds=new Set();submitted=false;
`);
const nested=contextApp.run('renderQuestionList(QUESTIONS)');
assert.equal((nested.match(/data-context-key="test-parent"/g)||[]).length,1);
assert.equal((nested.match(/data-context-key="test-child"/g)||[]).length,1);
assert(nested.indexOf('data-context-key="test-child"')>nested.indexOf('id="q1"'));
assert(nested.indexOf('data-context-key="test-child"')<nested.indexOf('id="q2"'));
const partial=contextApp.run('renderQuestionList(QUESTIONS.filter(q=>q.id===3))');
assert(partial.includes('data-context-key="test-parent"')&&partial.includes('data-context-key="test-child"'));
contextApp.run('QUESTIONS[2].sharedContexts=[];');
const discontinuous=contextApp.run('renderQuestionList(QUESTIONS)');
assert.equal((discontinuous.match(/data-context-key="test-parent"/g)||[]).length,2);
const contextReport={result:'PASS',banks:contextKeys.length,contexts_checked:contextsChecked,filtered_group_checks:filteredChecks,checks:['Shared block precedes first visible question','Shared text search retains all group members','Filtering retains common images and text','Nested context shown only for its subgroup','One block per contiguous group','Context link present for direct question navigation'],limitation:'Application HTML/state validation with deterministic DOM; no native browser layout test.'};
fs.writeFileSync(path.join(root,'work/review/context_logic_check.json'),JSON.stringify(contextReport,null,2));
console.log('Shared statements:',JSON.stringify(contextReport));
