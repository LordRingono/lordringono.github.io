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

module.exports={load};
