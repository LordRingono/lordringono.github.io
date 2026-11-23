// Only questions with restored/moved item labels need saved-answer migration.
// The original storage keys and both independent profiles are retained.
const V6_ITEM_REPAIRS={
 'histo.ann.tech':{
  1:{A:'A',B:'C',C:'D',D:'E'},
  5:{A:'A',B:'B',C:'C',D:'E'},
  6:{A:'A',B:'B',C:'C',D:'D'},
  7:{A:'A',B:'B',C:'D',D:'E'}
 },
 'histo.ann.tc':{5:{A:'A',B:'B',C:'C',E:'E'}},
 'bio.cm4':{5:{A:'B',B:'C',C:'D',D:'E',E:'F'}},
 'bio.cm5':{13:{A:'B',B:'C',C:'D',D:'E',E:'F'}},
 'bio.cm7':{12:{},13:{},14:{}},
 'bio.cm8':{
  10:{A:'B',B:'C',C:'D',D:'E',E:'F',F:'G',G:'H'},
  13:{A:'B',B:'C',C:'D',D:'E'},
  15:{A:'B',B:'C',C:'D',D:'E',E:'F'},
  16:{A:'B',B:'C',C:'D',D:'E',E:'F',F:'G',G:'H',H:'I'},
  17:{}
 },
 'bio.ann.cm4':{9:{}},
 'bio.ann.cm9':{10:{}},
 'embryo.aut.meiose':{5:Object.fromEntries([...'ABCDEFGHIJKLMN'].map(x=>[x,x]))},
 'embryo.aut.fec':{23:Object.fromEntries([...'BCDEFGHIJKLM'].map(x=>[x,x]))}
};
const v6PendingBackups=new Map();
function persistV6Progress(snapshot){
 try{
  const original=v6PendingBackups.get(STORAGE_KEY);
  if(original!==undefined){
   const backupKey=STORAGE_KEY+'_before_v6_item_repair';
   if(localStorage.getItem(backupKey)===null){
    localStorage.setItem(backupKey,original);
    if(localStorage.getItem(backupKey)!==original)throw new Error('Original progress backup was not stored');
   }
   v6PendingBackups.delete(STORAGE_KEY);
  }
  localStorage.setItem(STORAGE_KEY,JSON.stringify(snapshot));
  syncProfileSwitch();
  return true;
 }catch(e){
  // Keep the old persistent record untouched while its backup is pending.
  // The correctly remapped session remains usable in memory and can retry.
  syncProfileSwitch();
  return false;
 }
}
function migrateV6Progress(obj){
 const changes=V6_ITEM_REPAIRS[activeExam];
 if(!changes||!obj||!obj.answers||obj.itemSchemaVersion===6)return obj;
 const next={...obj,answers:{...obj.answers},itemSchemaVersion:6};
 const affected=new Set(Object.keys(changes).map(Number));
 for(const [id,letters] of Object.entries(changes)){
  const old=obj.answers[id];
  if(old&&old!=='∅')next.answers[id]=uniqueSortedLetters([...String(old)].map(letter=>letters[letter]||'').join(''));
 }
 // The former CM8 Q13 also contained Q14 under F–J. Keep those choices with
 // the newly restored stable question ID 17, without treating it as corrected.
 if(activeExam==='bio.cm8'){
  const mitophagy={F:'A',G:'B',H:'C',I:'D',J:'E'};
  const recovered=uniqueSortedLetters([...String(obj.answers[13]||'')].map(letter=>mitophagy[letter]||'').join(''));
  if(obj.answers[13])next.answers[17]=recovered||'∅';
 }
 if(onlyFilledMode){
  const oldIds=Array.isArray(obj.correctedIds)?obj.correctedIds:(obj.submitted?QUESTIONS.filter(q=>obj.answers[q.id]).map(q=>q.id):[]);
  next.correctedIds=oldIds.map(Number).filter(id=>!affected.has(id));
  next.submitted=next.correctedIds.length>0;
 }else if(obj.submitted){
  const oldIds=obj.revision6Partial&&Array.isArray(obj.correctedIds)?obj.correctedIds:QUESTIONS.map(q=>q.id);
  next.correctedIds=oldIds.map(Number).filter(id=>!affected.has(id));
  next.revision6Partial=true;
  next.submitted=next.correctedIds.length>0;
 }
 fallbackSessions[profileKey()]=next;
 if(!v6PendingBackups.has(STORAGE_KEY))v6PendingBackups.set(STORAGE_KEY,JSON.stringify(obj));
 persistV6Progress(next);
 return next;
}
