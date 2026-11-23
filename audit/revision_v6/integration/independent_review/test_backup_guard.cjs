/* Regression test for V6 original-progress backup, executed without a browser. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const script=fs.readFileSync(path.join(root,'progress_migration.js'),'utf8');
const clone=x=>JSON.parse(JSON.stringify(x));
const results=[];
function fixture(backupFailure){
 const data={},writes=[];let failure=backupFailure;
 const context=vm.createContext({
  activeExam:'histo.ann.tech',onlyFilledMode:true,QUESTIONS:[{id:1},{id:2}],
  STORAGE_KEY:'',fallbackSessions:{},syncCalls:0,
  uniqueSortedLetters:v=>[...new Set([...String(v)].filter(c=>'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.includes(c)))].sort().join(''),
  localStorage:{getItem:k=>data[k]??null,setItem:(k,v)=>{
   writes.push(k);
   if(k.endsWith('_before_v6_item_repair')){
    if(failure==='throw')throw new Error('QuotaExceededError');
    if(failure==='silent')return;
   }
   data[k]=String(v);
  }}
 });
 vm.runInContext("function profileKey(){return (onlyFilledMode?'filled:':'classic:')+activeExam;} function syncProfileSwitch(){syncCalls++;}",context);
 vm.runInContext(script,context);
 return {context,data,writes,run:code=>vm.runInContext(code,context),restore:()=>failure=null};
}
for(const failure of ['throw','silent']){
 const f=fixture(failure);
 const cases=[
  {mode:true,key:'qcm-pass-histo-tech',original:{answers:{1:'BCD',2:'A'},submitted:true,correctedIds:[1,2]},expected:'CDE'},
  {mode:false,key:'qcm-pass-histo-tech_profil_2_v1',original:{answers:{1:'D',2:'B'},submitted:true},expected:'E'}
 ];
 for(const c of cases){
  f.data[c.key]=JSON.stringify(c.original);
  f.context.onlyFilledMode=c.mode;f.context.STORAGE_KEY=c.key;f.context.original=clone(c.original);
  const next=f.run('migrateV6Progress(original)');
  assert.equal(next.answers[1],c.expected);
  assert.deepEqual(JSON.parse(f.data[c.key]),c.original,'old persistent progress remains intact');
  assert.equal(f.data[c.key+'_before_v6_item_repair'],undefined);
  assert(f.run('v6PendingBackups.has(STORAGE_KEY)'));
  f.context.next=next;
  assert.equal(f.run('persistV6Progress(next)'),false,'a normal later save must also be blocked');
  assert.deepEqual(JSON.parse(f.data[c.key]),c.original);
  assert.equal(f.run('migrateV6Progress(fallbackSessions[profileKey()]).answers[1]'),c.expected,'memory re-entry is idempotent');
 }
 f.restore();
 for(const c of cases){
  f.context.onlyFilledMode=c.mode;f.context.STORAGE_KEY=c.key;
  assert.equal(f.run('persistV6Progress(fallbackSessions[profileKey()])'),true);
  assert.deepEqual(JSON.parse(f.data[c.key+'_before_v6_item_repair']),c.original);
  assert.equal(JSON.parse(f.data[c.key]).answers[1],c.expected);
  assert.equal(f.run('v6PendingBackups.has(STORAGE_KEY)'),false);
  const backup=f.data[c.key+'_before_v6_item_repair'];
  assert.equal(f.run('persistV6Progress(fallbackSessions[profileKey()])'),true);
  assert.equal(f.data[c.key+'_before_v6_item_repair'],backup,'original backup is immutable');
 }
 results.push({failure,profiles:2,result:'PASS',syncCalls:f.context.syncCalls});
}
const report={method:'Node VM running the current progress_migration.js, with quota and silent-write-failure mocks; not a browser',result:'PASS',results};
fs.writeFileSync(path.join(__dirname,'backup_guard_result.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
