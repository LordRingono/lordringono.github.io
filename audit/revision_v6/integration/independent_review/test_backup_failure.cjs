/* Independent regression: a quota can prevent adding the backup while permitting
 * replacement of the original key. This executes the actual migration source. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const key='qcm-pass-legacy-example';
const original={answers:{1:'BCD',2:'A'},submitted:true,correctedIds:[1,2]};
const data={[key]:JSON.stringify(original)};
const writes=[];
const context=vm.createContext({
  activeExam:'histo.ann.tech',onlyFilledMode:true,
  QUESTIONS:[{id:1},{id:2}],STORAGE_KEY:key,fallbackSessions:{},
  profileKey:()=> 'filled:histo.ann.tech',syncProfileSwitch:()=>{},
  uniqueSortedLetters:v=>[...new Set([...String(v)].filter(c=>'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.includes(c)))].sort().join(''),
  localStorage:{
    getItem:k=>data[k]??null,
    setItem:(k,v)=>{writes.push(k);if(k.endsWith('_before_v6_item_repair'))throw new Error('QuotaExceededError');data[k]=String(v);}
  }
});
vm.runInContext(fs.readFileSync(path.join(root,'progress_migration.js'),'utf8'),context);
context.original=original;
const migrated=vm.runInContext('migrateV6Progress(original)',context);
// Follow the current normal save() persistence route. Before the fix it wrote
// directly; after the fix it must go through persistV6Progress().
context.next=migrated;
vm.runInContext("if(typeof persistV6Progress==='function')persistV6Progress(next);else localStorage.setItem(STORAGE_KEY,JSON.stringify(next));",context);
const result={
  method:'Node VM; actual progress_migration.js; deterministic quota mock',
  originalAnswer:original.answers[1],migratedAnswer:migrated.answers[1],
  backupExists:Object.hasOwn(data,key+'_before_v6_item_repair'),
  originalKeyAfterNormalSave:JSON.parse(data[key]),writes,
  backupRequirementPreserved:!!data[key+'_before_v6_item_repair']||JSON.parse(data[key]).answers[1]===original.answers[1]
};
fs.writeFileSync(path.join(__dirname,'backup_failure_result.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
