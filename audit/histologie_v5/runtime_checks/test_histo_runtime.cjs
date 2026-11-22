/* Runs the actual site script through the immutable V4 DOM adapter.
 * Does not write to the site. Reports are confined to this directory. */
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert/strict');
const taskRoot=path.resolve(__dirname,'..');
const workspace=path.resolve(taskRoot,'../..');
const baselineDir=path.join(taskRoot,'baseline_site');
const target=path.resolve(process.argv[2]||path.join(workspace,'output/site/index.html'));
const siteDir=path.dirname(target);
const {load}=require(path.join(baselineDir,'audit/revision_v4/production/dom_adapter.cjs'));
const baseline=JSON.parse(fs.readFileSync(path.join(taskRoot,'baseline_exams.json'),'utf8'));
const banks=['histo.te1','histo.te2','histo.tc1','histo.tc2','histo.tc3','histo.tn1','histo.tn2','histo.tn3','histo.autotech'];
const counts=[13,19,12,13,24,16,10,8,13];
const clean=value=>JSON.parse(JSON.stringify(value));
const quote=value=>JSON.stringify(value);
const sha=filename=>crypto.createHash('sha256').update(fs.readFileSync(filename)).digest('hex');
const report={result:'RUNNING',site:target,siteSHA256:fs.existsSync(target)?sha(target):null,
  adapter:'V4 audit/revision_v4/production/dom_adapter.cjs',
  scope:'128 QCM de 9 banques histologiques ; notation, profils, copies des sources et conservation de V4.',
  limitation:'Le script et les chaînes HTML réels sont exécutés avec l’adaptateur DOM V4. Ce contrôle ne mesure pas le rendu graphique ou les pixels d’un navigateur.',
  errors:[],bankChecks:[],cardChecks:[],profileReloadChecks:[],conservation:{},specialCases:{}};
const failures=report.errors;
function phase(name,fn){try{fn();return true;}catch(error){failures.push({phase:name,message:error.message,stack:error.stack});return false;}}
function readCards(app){return clean(app.run('QUESTIONS.map(q=>({id:q.id,html:renderQuestionCard(q)}))'));}
function copies(html){
  return [...html.matchAll(/<details\b[^>]*>/g)].map(m=>m[0]).filter(tag=>/\bclass="[^"]*\bhisto-source-copy\b/.test(tag)).map(tag=>{
    const role=tag.match(/data-source-role="([^"]+)"/)?.[1];
    assert(role,'Copie sans data-source-role explicite');
    assert(!/\sopen(?:[\s=>])/.test(tag),'Copie originale dépliée par défaut');
    return role;
  });
}
function localPath(src){
  assert.equal(typeof src,'string','Référence de fichier manquante');
  assert(src.length>0,'Référence de fichier vide');
  assert(!/^(?:https?:|data:|blob:)/.test(src),'La copie originale doit être livrée avec le site');
  const resolved=path.resolve(siteDir,src.split('#')[0]);
  assert(resolved.startsWith(siteDir+path.sep),'Chemin hors du site : '+src);
  assert(fs.statSync(resolved).isFile(),'Fichier absent : '+src);
  return resolved;
}
function choose(app,qid,letter,checked=true){
  const listener=app.elements.get('#questions').handlers.change?.[0];
  assert(listener,'Gestionnaire réel des cases absent');
  const input={dataset:{q:String(qid)},value:letter,checked,
    closest(selector){if(selector==='input[data-q]')return this;if(selector==='.option')return {classList:{toggle(){}}};return null;}};
  listener({target:input});
}
function chooseKey(app,q){
  if(q.answerIsEmpty)choose(app,q.id,'∅');
  else for(const letter of (q.tokenMode?q.answer.split(','):q.answer.split('')))choose(app,q.id,letter);
}
function switchTo(app,bank,filled){app.run(`switchProfile(${filled});switchExam(${quote(bank)});`);}
function snapshot(app){return clean(app.run(`({mode:onlyFilledMode,bank:activeExam,grade:results().grade,
  questions:QUESTIONS.map(q=>({id:q.id,chosen:selected(q),corrected:isCorrected(q),points:assessed(q).points}))})`));}
function checkCard(app,bank,q,html,done,stage){
  assert.deepEqual(copies(html),done?['subject','correction']:['subject'],`${bank}/${q.id} copies incorrectes (${stage})`);
  assert(q.sourceCopies?.subject&&q.sourceCopies?.correction,`${bank}/${q.id} paire de sources absente`);
  for(const src of q.sourceCopies.subject.captures)assert(html.includes(src.src),`${bank}/${q.id} capture du sujet absente (${stage})`);
  for(const src of q.sourceCopies.correction.captures)assert.equal(html.includes(src.src),done,`${bank}/${q.id} fuite/absence du corrigé (${stage})`);
  assert.equal(html.includes('class="correction"'),done,`${bank}/${q.id} panneau de correction prématuré/manquant (${stage})`);
  if(!done){
    assert(!html.includes('review-opt-flag'),`${bank}/${q.id} réserve révélée avant correction`);
    assert(!html.includes('class="pharma-review"'),`${bank}/${q.id} commentaire révélé avant correction`);
  }
  report.cardChecks.push({bank,id:q.id,stage,corrected:done,sourceRoles:copies(html),pass:true});
}

let app,current;
phase('Charger le site final',()=>{assert(fs.existsSync(target),'Site final absent');app=load(target);current=clean(app.run('EXAMS'));});
if(current){
  phase('Périmètre et conservation des autres banques',()=>{
    assert.deepEqual(Object.keys(current).sort(),Object.keys(baseline).sort(),'Une banque a été ajoutée/supprimée');
    const unchanged=[];
    for(const bank of Object.keys(baseline)){
      if(banks.includes(bank)){assert.equal(current[bank].storage,baseline[bank].storage,'Clé de profil modifiée : '+bank);continue;}
      assert.deepEqual(current[bank],baseline[bank],'Banque hors périmètre modifiée : '+bank);
      unchanged.push({bank,questions:current[bank].questions.length});
    }
    for(let i=0;i<banks.length;i++)assert.equal(current[banks[i]].questions.length,counts[i],banks[i]+' nombre de QCM incorrect');
    const total=banks.reduce((n,b)=>n+current[b].questions.length,0);
    assert.equal(total,128);
    const sourceCopyBanks=Object.entries(current).filter(([,e])=>e.questions.some(q=>q.sourceCopies)).map(([b])=>b).sort();
    assert.deepEqual(sourceCopyBanks,banks.slice().sort(),'Copies ajoutées hors des neuf banques ciblées');
    report.conservation.unchangedBanks=unchanged;
    report.conservation.unchangedBankCount=unchanged.length;
    report.conservation.unchangedQuestionCount=unchanged.reduce((n,e)=>n+e.questions,0);
    report.conservation.profileStorageKeysUnchanged=true;
    report.questions=total;
  });
  phase('Conserver tous les anciens assets, sources et audits',()=>{
    const roots=['static','assets','sources','audit'];const checked=[];const missing=[];const changed=[];
    function walk(dir){if(!fs.existsSync(dir))return;for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      const full=path.join(dir,entry.name);if(entry.isDirectory()){walk(full);continue;}if(!entry.isFile())continue;
      const relative=path.relative(baselineDir,full);const final=path.join(siteDir,relative);
      if(!fs.existsSync(final)){missing.push(relative);continue;}
      const hash=sha(full);if(sha(final)!==hash)changed.push(relative);
      checked.push({file:relative,sha256:hash});
    }}
    roots.forEach(root=>walk(path.join(baselineDir,root)));
    report.conservation.oldFileCount=checked.length;
    report.conservation.oldAuditFileCount=checked.filter(f=>f.file.startsWith('audit'+path.sep)).length;
    report.conservation.missingOldFiles=missing;report.conservation.changedOldFiles=changed;
    fs.writeFileSync(path.join(__dirname,'preserved_files.json'),JSON.stringify(checked,null,2));
    assert.deepEqual(missing,[],'Fichiers V4 perdus');assert.deepEqual(changed,[],'Fichiers V4 modifiés');
  });
  phase('Vérifier les paires de sources et leurs fichiers',()=>{
    let captureCount=0;
    for(const bank of banks)for(const q of current[bank].questions){
      assert(q.sourceCopies,`${bank}/${q.id} sourceCopies absent`);
      for(const role of ['subject','correction']){
        const copy=q.sourceCopies[role];assert(copy,`${bank}/${q.id}/${role} absent`);
        assert(copy.file,`${bank}/${q.id}/${role} nom du document absent`);
        localPath(copy.pdf);localPath(copy.original);
        assert(Array.isArray(copy.captures)&&copy.captures.length>0,`${bank}/${q.id}/${role} captures absentes`);
        for(const cap of copy.captures){assert(Number.isInteger(cap.page)&&cap.page>0);localPath(cap.src);captureCount++;}
      }
    }
    report.captureReferencesChecked=captureCount;
  });
  phase('Cas particuliers documentés',()=>{
    const none=current['histo.tc3'].questions.find(q=>q.id===17);
    assert.equal(none.answer,'');assert.equal(none.answerIsEmpty,true);assert.equal(none.allowNoAnswer,true);
    assert(!/hors note/i.test(none.warning||''));
    for(const o of none.options)assert.match(none.explanations[o.id],/^Faux\./i);
    const fj=current['histo.autotech'].questions.find(q=>q.id===13);
    assert.deepEqual(fj.options.map(o=>o.id),['F','G','H','I','J']);assert.equal(fj.answer,'GIJ');
    const oldIds=baseline['histo.autotech'].questions.map(q=>q.id);
    assert(oldIds.every(id=>current['histo.autotech'].questions.some(q=>q.id===id)),'Ancien identifiant autotech perdu');
    report.specialCases.allFalse={bank:'histo.tc3',id:17,expected:'∅',pass:true};
    report.specialCases.optionsFtoJ={bank:'histo.autotech',id:13,options:'FGHIJ',answer:'GIJ',pass:true};
  });

  // Every question is exercised through the real checkbox change listener.
  // First only one question is graded, so global "submitted" cannot leak the
  // other original corrections in selective mode.
  for(const bank of banks)phase('Profil 1, copies et clé complète — '+bank,()=>{
    switchTo(app,bank,true);app.run('reset()');
    const questions=current[bank].questions;
    for(const card of readCards(app))checkCard(app,bank,questions.find(q=>q.id===card.id),card.html,false,'blank-profile-1');
    chooseKey(app,questions[0]);app.run('gradeAll()');
    const partial=clean(app.run('results()'));
    assert.equal(partial.grade,20);assert.equal(partial.ratedCount,1);
    assert.equal(partial.unanswered,questions.length-1);
    for(const card of readCards(app))checkCard(app,bank,questions.find(q=>q.id===card.id),card.html,card.id===questions[0].id,'selective-one-question');
    for(const q of questions.slice(1))chooseKey(app,q);
    app.run('gradeAll()');
    const result=clean(app.run('results()'));
    assert.equal(result.grade,20,bank+' clé non notée 20/20');assert.equal(result.ratedCount,questions.length);
    assert.equal(result.nonGraded,0);assert.equal(result.unanswered,0);
    for(const row of result.data){assert.equal(row.points,10,bank+'/'+row.q.id+' clé non notée 10/10');assert.equal(row.errors,0);}
    for(const card of readCards(app))checkCard(app,bank,questions.find(q=>q.id===card.id),card.html,true,'full-key-profile-1');
    report.bankChecks.push({bank,profile:1,questions:questions.length,grade:result.grade,allItemsSelectedViaRealChangeHandler:true,pass:true});
  });

  const expected={filled:{},classic:{}};
  for(const bank of banks)phase('Profil 2 indépendant — '+bank,()=>{
    switchTo(app,bank,false);
    assert.equal(app.run('answeredCount()'),0,bank+' réponses du profil 1 mêlées au profil 2');
    assert.equal(app.run('submitted'),false,bank+' correction du profil 1 mêlée au profil 2');
    const questions=current[bank].questions;
    for(const card of readCards(app))checkCard(app,bank,questions.find(q=>q.id===card.id),card.html,false,'blank-profile-2');
    chooseKey(app,questions[0]);app.run('gradeAll()');
    assert.equal(app.run('results().unanswered'),questions.length-1,'Mode classique : les QCM blancs doivent être comptés');
    for(const card of readCards(app))checkCard(app,bank,questions.find(q=>q.id===card.id),card.html,true,'classic-global-correction');
    app.run('modify()');
    for(const q of questions.slice(1))chooseKey(app,q);
    app.run('gradeAll()');
    const result=clean(app.run('results()'));
    assert.equal(result.grade,20,bank+' clé du profil 2 non notée 20/20');
    assert.equal(result.ratedCount,questions.length);
    for(const row of result.data){assert.equal(row.points,10);assert.equal(row.errors,0);}
    report.bankChecks.push({bank,profile:2,questions:questions.length,grade:result.grade,pass:true});
    // Make profile 2 deliberately different, then return to the saved profile 1.
    app.run('modify()');
    const first=questions[0],changed=first.options[0].id;
    const wasChosen=app.run(`selected(QUESTIONS.find(q=>q.id===${first.id})).includes(${quote(changed)})`);
    choose(app,first.id,changed,!wasChosen);app.run('gradeAll()');
    assert(app.run('results().grade')<20,bank+' modification du profil 2 non appliquée');
    expected.classic[bank]=snapshot(app);
    switchTo(app,bank,true);assert.equal(app.run('results().grade'),20,bank+' profil 1 altéré par le profil 2');
    expected.filled[bank]=snapshot(app);
    assert.notEqual(expected.classic[bank].questions[0].chosen,expected.filled[bank].questions[0].chosen);
  });
  phase('Rechargement et persistance des deux profils',()=>{
    app.run('save()');const persisted=load(target,app.data);
    for(const [mode,filled] of [['filled',true],['classic',false]])for(const bank of banks){
      switchTo(persisted,bank,filled);
      assert.deepEqual(snapshot(persisted),expected[mode][bank],bank+' état perdu ou mélangé après rechargement ('+mode+')');
      const q17=bank==='histo.tc3'?current[bank].questions.find(q=>q.id===17):null;
      if(q17){assert.equal(persisted.run('answers[17]'),'∅');assert.equal(persisted.run('assessed(QUESTIONS.find(q=>q.id===17)).points'),10);}
      if(bank==='histo.autotech'){
        assert.equal(persisted.run('answers[13]'),'GIJ');
        assert.equal(persisted.run('assessed(QUESTIONS.find(q=>q.id===13)).points'),10);
        const card=persisted.run('renderQuestionCard(QUESTIONS.find(q=>q.id===13))');
        for(const id of ['F','G','H','I','J'])assert(card.includes(`value="${id}"`),'Case F–J perdue après rechargement');
      }
      report.profileReloadChecks.push({bank,mode,questions:current[bank].questions.length,pass:true});
    }
  });
  phase('Réponse vide et réponse explicite aucune proposition',()=>{
    const blank=load(target);switchTo(blank,'histo.tc3',true);blank.run('reset()');
    const before=clean(blank.run('assessed(QUESTIONS.find(q=>q.id===17))'));
    assert.equal(before.unanswered,true);assert.equal(before.points,0);
    blank.run('gradeAll()');assert.equal(blank.run('correctedIds.size'),0);
    choose(blank,17,'∅');blank.run('gradeAll()');
    const after=clean(blank.run('assessed(QUESTIONS.find(q=>q.id===17))'));
    assert.equal(after.unanswered,false);assert.equal(after.points,10);
    assert.equal(blank.run('results().grade'),20);assert.equal(blank.run('results().ratedCount'),1);
    report.specialCases.explicitNoneDistinctFromBlank={blankUncorrected:true,explicitNoneGrade:20,ratedQuestions:1,pass:true};
  });
}

report.result=failures.length?'FAIL':'PASS';
report.completedAt=new Date().toISOString();
report.summary={targetQuestions:report.questions||0,gradedBankProfiles:report.bankChecks.length,cardStates:report.cardChecks.length,
  reloadedBankProfiles:report.profileReloadChecks.length,errors:failures.length};
fs.writeFileSync(path.join(__dirname,'runtime_report.json'),JSON.stringify(report,null,2));
const message=[
  '# Contrôle du site — autotests histologiques',
  '',`Résultat : **${report.result}**.`,
  '',`Fichier testé : \`${target}\`.`,
  '',`Empreinte SHA256 : \`${report.siteSHA256}\`.`,
  '',`- ${report.questions||0} QCM ciblés dans neuf banques.`,
  `- ${report.bankChecks.length} couples banque/profil vérifiés avec une clé donnant 20/20.`,
  `- ${report.cardChecks.length} états de carte vérifiés : sujet avant correction ; sujet et corrigé après correction.`,
  `- ${report.profileReloadChecks.length} couples banque/profil vérifiés après fermeture logique et rechargement de l’application.`,
  `- ${report.conservation.unchangedBankCount||0} banques hors périmètre inchangées (${report.conservation.unchangedQuestionCount||0} QCM).`,
  `- ${report.conservation.oldFileCount||0} anciens fichiers conservés à l’identique, dont ${report.conservation.oldAuditFileCount||0} fichiers d’audit.`,
  '', '## Méthode', '',
  'Le JavaScript réel du site est exécuté avec le dom_adapter.cjs livré dans V4. Les réponses passent par le gestionnaire réel de changement des cases ; les fonctions réelles de correction, de rendu et de sauvegarde sont exécutées. Les copies de sources sont contrôlées dans le HTML produit pour chaque carte, y compris les QCM encore vides après une correction sélective partielle.',
  '', 'Les deux profils ont des réponses différentes, puis un nouvel environnement recharge leurs sauvegardes. TC3 Q17 est contrôlé avec une case « aucune proposition » explicitement choisie, distincte d’un QCM laissé vide. Le nouvel autotech ID 13 est contrôlé avec les lettres F–J et la clé GIJ.',
  '', '## Portée', '', report.limitation,
  ...(failures.length?['','## Échecs','',...failures.map(f=>`- **${f.phase}** : ${f.message}`)]:[]),''
].join('\n');
fs.writeFileSync(path.join(__dirname,'REPORT.md'),message);
console.log(JSON.stringify({result:report.result,...report.summary,errors:failures.map(({phase,message})=>({phase,message}))},null,2));
process.exitCode=failures.length?1:0;
