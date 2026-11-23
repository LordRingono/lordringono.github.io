/* Independent integration checks against output/site/index.html after build.
 * This is a JavaScript VM and a DOM adapter, never a graphical browser check. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),workspace=path.resolve(root,'../..');
const site=path.join(workspace,'output/site'),filename=path.join(site,'index.html');
const {load}=require(path.join(site,'audit/revision_v4/production/dom_adapter.cjs'));
const clone=x=>JSON.parse(JSON.stringify(x)),quoted=x=>JSON.stringify(x);
const baseline=JSON.parse(fs.readFileSync(path.join(root,'baseline_exams.json'),'utf8'));
const html=fs.readFileSync(filename,'utf8');
assert(html.includes('const V6_ITEM_REPAIRS='),'Wait for the authorized V6 build before this test.');
const app=load(filename),data=clone(app.run('EXAMS'));
const report={method:'Actual release JavaScript executed by the V4 DOM adapter in Node VM; no browser pixels',siteSha256:crypto.createHash('sha256').update(html).digest('hex'),result:'RUNNING',groups:[],migrationCases:[],annotatedPdfCases:0,errors:[]};
function switchBank(bank,mode=true){app.run(`switchProfile(${mode});switchExam(${quoted(bank)});reset();`);}
function sourceMenu(card,role){return card.match(new RegExp('<details[^>]*data-source-role="'+role+'"[\\s\\S]*?</details>'))?.[0]||'';}
try{
 const groups=new Map();
 for(const [bank,exam] of Object.entries(data))for(const q of exam.questions)for(const c of q.sharedContexts||[])if(c.imagesAfterCorrection){
  const key=bank+'/'+c.id;const group=groups.get(key)||{bank,context:c,ids:[]};group.ids.push(q.id);groups.set(key,group);
 }
 for(const group of groups.values()){
  assert.equal(group.ids.length,2,'Current approved annotated groups have two questions');
  for(const order of [group.ids,[...group.ids].reverse()]){
   switchBank(group.bank);
   const q1=group.ids[0],context=group.context;
   const shared=(ids)=>app.run(`renderQuestionList(QUESTIONS.filter(q=>${quoted(ids)}.includes(q.id)))`);
   const checkGroup=(ready)=>{
    for(const id of group.ids){
     const block=app.run(`sharedStatement(${quoted(context)},QUESTIONS.find(q=>q.id===${id}),'independent-gate')`);
     for(const src of context.images||[])assert.equal(block.includes(src),ready,`${group.bank}/${id} shared image`);
     if(!ready)assert(!block.includes('href='),`${group.bank}/${id} shared source PDF gate`);
     const q=data[group.bank].questions.find(q=>q.id===id);
     const card=app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${id}))`);
     const subject=sourceMenu(card,'subject');
     for(const capture of q.sourceCopies.subject.captures||[])assert.equal(subject.includes(capture.src),ready,`${group.bank}/${id} grouped subject copy`);
     if(!ready){
      const metadata=card.match(/<div class="qsource">[\s\S]*?<\/div>/)?.[0]||'';
      assert(!metadata.includes('<a href='),`${group.bank}/${id} grouped direct PDF gate`);
     }
    }
   };
   checkGroup(false);
   app.run(`answers[${order[0]}]='∅';gradeAll();`);
   checkGroup(false);
   for(const id of group.ids){
    const block=shared([id]);
    // The context rendered outside the card must remain protected even if the
    // other question is hidden by search, theme, status, or any list filtering.
    const prefix=block.slice(0,block.indexOf('<article'));
    for(const src of context.images||[])assert(!prefix.includes(src),`${group.bank}/${id} filtered shared image gate`);
   }
   const doneCard=app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${order[0]}))`);
   assert(sourceMenu(doneCard,'correction').includes('data-source-role="correction"'),'the individually validated correction remains available');
   app.run(`answers[${order[1]}]='∅';gradeAll();`);
   checkGroup(true);
   app.run(`correctedIds.delete(${order[0]});submitted=correctedIds.size>0;`);
   checkGroup(false);
  }
  switchBank(group.bank,false);
  for(const src of group.context.images||[])assert(!app.run(`sharedStatement(${quoted(group.context)},QUESTIONS.find(q=>q.id===${group.ids[0]}),'classic-before')`).includes(src));
  app.run('gradeAll();');
  for(const src of group.context.images||[])assert(app.run(`sharedStatement(${quoted(group.context)},QUESTIONS.find(q=>q.id===${group.ids[0]}),'classic-after')`).includes(src));
  report.groups.push({bank:group.bank,id:group.context.id,questions:group.ids,orders:2,filtered:true,relocked:true,classic:true,result:'PASS'});
 }
 for(const [bank,exam] of Object.entries(data)){
  const protectedQs=exam.questions.filter(q=>q.sourceCopies.subject.afterCorrection||q.imagesAfterCorrection);
  if(!protectedQs.length)continue;switchBank(bank);
  for(const q of protectedQs){
   const card=app.run(`renderQuestionCard(QUESTIONS.find(q=>q.id===${q.id}))`);
   const metadata=card.match(/<div class="qsource">[\s\S]*?<\/div>/)?.[0]||'';
   assert(!metadata.includes('<a href='),bank+'/'+q.id+' direct annotated source link');
   assert(!sourceMenu(card,'subject').includes('<a href='),bank+'/'+q.id+' annotated source menu links');
   report.annotatedPdfCases++;
  }
 }
 // Independently derive changed item schemas and new IDs from the two datasets.
 const structural={};
 for(const [bank,exam] of Object.entries(data)){
  const old=new Map(baseline[bank].questions.map(q=>[q.id,q]));
  const changed=exam.questions.filter(q=>!old.has(q.id)||JSON.stringify(q.options.map(o=>o.id))!==JSON.stringify(old.get(q.id).options.map(o=>o.id))).map(q=>q.id);
  if(changed.length)structural[bank]=changed;
 }
 const declared=clone(app.run('V6_ITEM_REPAIRS'));
 assert.deepEqual(Object.keys(declared).sort(),Object.keys(structural).sort());
 for(const [bank,affected] of Object.entries(structural)){
  assert.deepEqual(Object.keys(declared[bank]).map(Number).sort((a,b)=>a-b),[...affected].sort((a,b)=>a-b));
  const old=baseline[bank],answers=Object.fromEntries(old.questions.filter((q,i)=>i%3!==0).map(q=>[q.id,q.options[0]?.id||'∅']));
  const corrected=old.questions.filter((q,i)=>i%3===1).map(q=>q.id);
  for(const mode of [true,false])for(const oldShape of ['partial','legacy','unfinished']){
   const before={answers:clone(answers),submitted:oldShape!=='unfinished'};
   if(oldShape==='partial')before.correctedIds=corrected.map(String);
   const key=old.storage+(mode?'':'_profil_2_v1');
   const seed={ssh_pass_selected_exam_v1:bank,ssh_pass_only_filled_mode_v1:String(mode),[key]:JSON.stringify(before)};
   const instance=load(filename,seed);
   const state=clone(instance.run('({answers,done:QUESTIONS.filter(isCorrected).map(q=>q.id)})'));
   const expected=oldShape==='unfinished'?[]:(mode?(oldShape==='partial'?corrected:old.questions.filter(q=>answers[q.id]).map(q=>q.id)):old.questions.map(q=>q.id)).filter(id=>!affected.includes(id));
   assert.deepEqual([...state.done].sort((a,b)=>a-b),expected.sort((a,b)=>a-b),`${bank}/${mode}/${oldShape} preserved correction states`);
   assert.deepEqual(JSON.parse(instance.data[key+'_before_v6_item_repair']),before,'original progress is backed up exactly');
   for(const q of old.questions.filter(q=>!affected.includes(q.id)))assert.equal(state.answers[q.id]||'',answers[q.id]||'',bank+'/'+q.id+' unchanged answers');
   instance.run('save();');
   const reload=load(filename,instance.data);
   assert.deepEqual(clone(reload.run('({answers,done:QUESTIONS.filter(isCorrected).map(q=>q.id)})')),state,'migration is idempotent after normal save and reload');
   report.migrationCases.push({bank,mode:mode?'selective':'classic',oldShape,result:'PASS'});
  }
 }
 report.result='PASS';
}catch(error){report.result='FAIL';report.errors.push(error.stack||String(error));process.exitCode=1;}
fs.writeFileSync(path.join(__dirname,'release_test_result.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,groups:report.groups.length,migrationCases:report.migrationCases.length},null,2));
