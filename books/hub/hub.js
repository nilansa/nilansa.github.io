(() => {
"use strict";
const $ = (s) => document.querySelector(s);
const STORE = "bookhub.workspaces.v1";
const ACTIVE = "bookhub.active.v1";
const PINS = "cs-conference-hub-pins-v1";
const NS = "http://www.w3.org/2000/svg";
const featureIds = ["principles-of-visual-information-retrieval","video-mining-rosenfeld-doermann-dementhon","visual-question-answering-wu-2022"];
const positions = {
  descriptors:[92,92],segmentation:[265,89],browsing:[451,67],summarization:[646,103],
  multimodal:[93,216],retrieval:[273,207],feedback:[474,211],semantics:[642,244],
  statistics:[92,344],representation:[270,344],"question-answering":[458,332],
  attention:[626,349],knowledge:[433,425],"video-qa":[656,427]
};
let atlas=null,books=[],papers=[],records=[],spaces=[],selected="",activeFilter="all",visible=11,selectedConcept="retrieval";
function el(tag,cls,txt) { const e=document.createElement(tag); if(cls)e.className=cls;if(txt!==undefined)e.textContent=String(txt);return e; }
function link(label,url,cls) { const a=el("a",cls,label);a.href=url;a.target="_blank";a.rel="noopener noreferrer";return a; }
function external(url) { try { const u=new URL(url);return u.protocol==="https:"&&!u.username&&!u.password?u.href:""; }catch{return "";} }
function fromBook(id){return books.find(x=>x.slug===id);}
function goodText(v,max){return typeof v==="string"?v.slice(0,max):"";}
function safeArray(x,max){return Array.isArray(x)?x.slice(0,max):[];}
function loadPins(){
  try {
    const v=JSON.parse(localStorage.getItem(PINS)||"[]");
    return safeArray(v,350).filter(p=>p&&typeof p.title==="string"&&p.id!==undefined)
      .map(p=>({id:String(p.id).slice(0,150),title:goodText(p.title,400),authors:goodText(p.authors,700),year:p.year,
        venue:goodText(p.venue,25),abstract:goodText(p.abstract,3000),url:external(p.paper_url||p.cvf_url||"")}))
      .filter(p=>p.url);
  }catch{return [];}
}
function makeRecords(){
 const out=[];
 for(const b of books){
   out.push({id:"book:"+b.slug,type:"book",title:b.title,subtitle:(b.creator||"")+" · "+(b.year||"Year unknown"),
     description:b.topic||b.why||"",detail:b.category||"",url:external(b.pdfUrl)||external(b.publisherUrl)||"",
     search:[b.title,b.creator,b.year,b.topic,b.category,...(b.tags||[])].join(" ")});
 }
 for(const c of atlas.concepts){
   out.push({id:"concept:"+c.id,type:"concept",title:c.title,subtitle:"Curated concept",description:c.definition,
     detail:"Study map",url:"",search:[c.title,c.definition,c.question,c.route].join(" ")});
 }
 for(const c of atlas.chapters){
   const b=fromBook(c.book);
   out.push({id:"chapter:"+c.id,type:"chapter",title:c.title,
     subtitle:(b?b.title:"Unknown book")+" · Ch. "+c.number+(c.page?" · printed p. "+c.page:""),
     description:"Chapter heading from the source table of contents.",detail:"Verified contents heading",
     url:b?(external(b.pdfUrl)||external(b.publisherUrl)||""):"",
     search:[c.title,b?.title||"",...(c.concepts||[])].join(" ")});
 }
 for(const p of papers){
   out.push({id:"paper:"+p.id,type:"paper",title:p.title,subtitle:p.venue+" "+p.year+" · ConfHub pin",
     description:p.abstract||"Previously pinned in ConfHub.",detail:p.authors,url:p.url,
     search:[p.title,p.authors,p.abstract,p.venue,p.year].join(" ")});
 }
 return out;
}
function textMatch(r,q) { const tokens=q.toLowerCase().split(/\s+/).filter(Boolean);const corpus=(r.search+" "+r.title+" "+r.subtitle).toLowerCase();return tokens.every(t=>corpus.includes(t)); }
function score(r,q) {
 if(!q){if(r.type==="book")return featureIds.includes(r.id.slice(5))?100-featureIds.indexOf(r.id.slice(5)):60;
   return r.type==="concept"?42:r.type==="chapter"?25:10;}
 let points=0,terms=q.toLowerCase().split(/\s+/).filter(Boolean),title=r.title.toLowerCase();
 if(title===q.toLowerCase())points+=100;
 if(title.includes(q.toLowerCase()))points+=50;
 for(const t of terms){if(title.includes(t))points+=9;if(r.subtitle.toLowerCase().includes(t))points+=3;}
 return points+(r.type==="concept"?2:0);
}
function current(){return spaces.find(s=>s.id===selected)||spaces[0];}
function record(id){
  const r=records.find(x=>x.id===id);
  if(r)return r;
  const s=current(),p=s?.paperSnapshots?.[id];
  if(p)return {...p,id,type:"paper"};
  return null;
}
function setStatus(s){$("#save-status").textContent=s;}
function save() {
 try{
   localStorage.setItem(STORE,JSON.stringify({schema:"bookhub-workspaces-v1",spaces}));
   localStorage.setItem(ACTIVE,selected);
   setStatus("Saved in this browser. Export JSON for a portable copy.");
   return true;
 }catch{setStatus("Could not save to browser storage. Export and free space before continuing.");return false;}
}
function normalizeSpace(s) {
 if(!s||typeof s!=="object"||typeof s.id!=="string")return null;
 const name=goodText(s.name,80).trim()||"Untitled",items=safeArray(s.items,120).filter(x=>typeof x==="string"&&/^(book|chapter|concept|paper):/.test(x)).map(x=>x.slice(0,230));
 const ps={};
 if(s.paperSnapshots&&typeof s.paperSnapshots==="object"){
   for(const [k,v] of Object.entries(s.paperSnapshots).slice(0,120)){
     if(!k.startsWith("paper:")||!v||typeof v.title!=="string")continue;
     const url=external(v.url||"");
     ps[k]={type:"paper",title:goodText(v.title,400),subtitle:goodText(v.subtitle,240),description:goodText(v.description,1500),url};
   }
 }
 const reviews={};
 if(s.reviews&&typeof s.reviews==="object")for(const [key,v] of Object.entries(s.reviews).slice(0,120)){
   if(!atlas.concepts.some(c=>c.id===key)||!v||typeof v!=="object")continue;
   const due=goodText(v.due,10),reviewed=goodText(v.reviewed,10);
   if(!/^\d{4}-\d{2}-\d{2}$/.test(due))continue;
   reviews[key]={due,reviewed:/^\d{4}-\d{2}-\d{2}$/.test(reviewed)?reviewed:"",rating:v.rating==="needs-work"?"needs-work":"self-reviewed",attempts:Math.min(999,Math.max(0,Number(v.attempts)||0))};
 }
 return {id:goodText(s.id,100),name,notes:goodText(s.notes,50000),items:[...new Set(items)],paperSnapshots:ps,reviews};
}
function loadSpaces() {
 try{
   const raw=JSON.parse(localStorage.getItem(STORE)||"null");
   const valid=raw?.schema==="bookhub-workspaces-v1"?safeArray(raw.spaces,35).map(normalizeSpace).filter(Boolean):[];
   if(valid.length)return valid;
 }catch{}
 return [{id:"video-understanding",name:atlas.starter.name,notes:"Research question:\n\nWhat connects video retrieval, video mining and video question answering?\n\nAssumptions to check:\n\nPossible falsification test:\n",items:atlas.starter.items.slice(),paperSnapshots:{},reviews:{}}];
}
function filters() {
 for(const b of document.querySelectorAll("[data-filter]"))b.setAttribute("aria-pressed",String(b.dataset.filter===activeFilter));
}
function renderSearch(){
 const q=$("#search").value.trim(),raw=records.filter(r=>(activeFilter==="all"||r.type===activeFilter)&&textMatch(r,q));
 raw.sort((a,b)=>score(b,q)-score(a,q)||a.title.localeCompare(b.title));
 $("#result-count").textContent=raw.length+" match"+(raw.length===1?"":"es")+(q?' for "'+q+'"':" in the collection");
 const root=$("#results");root.replaceChildren();
 if(!raw.length)root.append(el("p","empty-results","No matching records. Try fewer words or another type."));
 const saved=new Set(current()?.items||[]);
 for(const r of raw.slice(0,visible)){
   const card=el("article","result-row"),type=el("span","result-type",r.type==="paper"?"ConfHub pin":r.type);
   const body=el("div","result-content"),title=el("h3",null,r.title),desc=el("p",null,r.subtitle),small=el("small",null,r.description),actions=el("div","result-actions");
   body.append(title,desc,small);
   const btn=el("button",saved.has(r.id)?"is-saved":"",saved.has(r.id)?"In desk ✓":"Add to desk");
   btn.type="button";btn.setAttribute("aria-pressed",String(saved.has(r.id)));btn.addEventListener("click",()=>toggleItem(r.id));
   actions.append(btn);
   if(r.url)actions.append(link("Open source ↗",r.url));
   if(r.type==="concept"){const inspect=el("button",null,"Inspect concept");inspect.type="button";inspect.addEventListener("click",()=>{selectConcept(r.id.slice(8));$("#connect").scrollIntoView({behavior:"smooth"})});actions.append(inspect);}
   card.append(type,body,actions);root.append(card);
 }
 $("#show-more").hidden=raw.length<=visible;
}
function toggleItem(id){
 const s=current();if(!s)return;
 const at=s.items.indexOf(id);
 if(at>=0){s.items.splice(at,1);}else{
   if(s.items.length>=120){setStatus("Workspace limit: 120 items. Remove an item first.");return;}
   s.items.push(id);
   const r=records.find(x=>x.id===id);
   if(r?.type==="paper")s.paperSnapshots[id]={type:"paper",title:r.title,subtitle:r.subtitle,description:r.description,url:r.url};
 }
 save();renderDesk();renderSearch();if(id.startsWith("concept:"))renderDetail();
}
function renderDesk(){
 const select=$("#workspace-select");select.replaceChildren();
 for(const s of spaces){const o=el("option",null,s.name);o.value=s.id;select.append(o);}select.value=selected;
 const s=current();if(!s)return;
 $("#workspace-notes").value=s.notes;
 $("#stack-count").textContent=s.items.length+" saved";
 const root=$("#saved-items");root.replaceChildren();
 if(!s.items.length)root.append(el("p","aside-empty","Your reading stack is empty. Add an item from search or the concept map."));
 for(const id of s.items){
   const r=record(id),row=el("div","saved-item"),main=el("div"),del=el("button",null,"×");
   main.append(el("strong",null,r?.title||id),el("span",null,r?.type||id.split(":")[0]));
   del.type="button";del.setAttribute("aria-label","Remove "+(r?.title||id));del.addEventListener("click",()=>toggleItem(id));
   row.append(main,del);root.append(row);
 }
 renderReviewQueue();
}
function localDay(offset=0){const d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate()+offset);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");}
function markReview(id,rating){
 const s=current(),key="concept:"+id;if(!s)return;
 if(!s.items.includes(key)){if(s.items.length>=120){setStatus("Reading stack is full. Remove an item first.");return;}s.items.push(key);}
 if(!s.reviews)s.reviews={};
 const prev=s.reviews[id];s.reviews[id]={rating,reviewed:localDay(),due:localDay(rating==="needs-work"?1:7),attempts:(prev?.attempts||0)+1};
 save();renderDesk();renderSearch();renderDetail();
}
function renderReviewQueue(){
 const s=current(),root=$("#review-list"),count=$("#due-count");if(!root||!count||!s)return;
 root.replaceChildren();const today=localDay();
 const concepts=s.items.filter(id=>id.startsWith("concept:")).map(id=>atlas.concepts.find(c=>c.id===id.slice(8))).filter(Boolean);
 const due=concepts.filter(c=>!s.reviews?.[c.id]||s.reviews[c.id].due<=today);
 count.textContent=due.length+" to check · "+concepts.length+" tracked";
 if(!concepts.length){root.append(el("p","aside-empty","Save a concept from the map to begin a review queue."));return;}
 const ranked=concepts.sort((a,b)=>((s.reviews?.[a.id]?.due||"0000")>(s.reviews?.[b.id]?.due||"0000")?1:-1));
 for(const c of ranked){const v=s.reviews?.[c.id],row=el("div","review-row"),summary=el("div"),btn=el("button",null,"Practice ↗");
   summary.append(el("strong",null,c.title),el("span",null,!v?"Not assessed":v.due<=today?"Review due": "Next check "+v.due));
   btn.type="button";btn.setAttribute("aria-label","Practice "+c.title);
   btn.addEventListener("click",()=>{selectConcept(c.id);$("#connect").scrollIntoView({behavior:"smooth"});});row.append(summary,btn);root.append(row);
 }
}
function ensureName(value){return typeof value==="string"?value.trim().replace(/\s+/g," ").slice(0,80):"";}
function newSpace(){
 if(spaces.length>=30){setStatus("Limit reached: export or remove a workspace.");return;}
 const name=ensureName(prompt("Name the new research workspace:","New research question"));if(!name)return;
 const s={id:"ws-"+Date.now()+"-"+Math.random().toString(36).slice(2,8),name,notes:"Research question:\n\nSources to compare:\n\nWhat would falsify this idea?\n",items:[],paperSnapshots:{},reviews:{}};
 spaces.push(s);selected=s.id;save();renderDesk();renderSearch();
}
function renameSpace(){const s=current();if(!s)return;const name=ensureName(prompt("Rename this workspace:",s.name));if(!name)return;s.name=name;save();renderDesk();}
function deleteSpace(){const s=current();if(!s)return;if(!confirm('Delete the workspace "'+s.name+'"? Export it first if you need the notes.'))return;
 if(spaces.length===1){spaces=[{id:"empty-"+Date.now(),name:"New research workspace",notes:"",items:[],paperSnapshots:{},reviews:{}}];}
 else spaces=spaces.filter(x=>x.id!==s.id);
 selected=spaces[0].id;save();renderDesk();renderSearch();
}
function downloadJSON(){
 const s=current();if(!s)return;
 const data={schema:"bookhub-workspaces-v1",exportedAt:new Date().toISOString(),spaces:[s]};
 const blob=new Blob([JSON.stringify(data,null,2)+"\n"],{type:"application/json"}),a=el("a");
 a.href=URL.createObjectURL(blob);a.download="bookhub-"+s.name.toLowerCase().replace(/[^a-z0-9]+/g,"-").slice(0,42)+".json";
 document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),5000);
 setStatus("Exported workspace JSON. It contains your notes—keep the file private.");
}
async function importJSON(file){
 if(!file)return;
 if(file.size>1500000){setStatus("Import file too large (limit 1.5 MB).");return;}
 try{
   const raw=JSON.parse(await file.text());
   if(raw.schema!=="bookhub-workspaces-v1"||!Array.isArray(raw.spaces))throw Error("Unrecognized workspace schema");
   const incoming=raw.spaces.slice(0,25).map(normalizeSpace).filter(Boolean);
   if(!incoming.length)throw Error("No valid workspaces");
   if(spaces.length+incoming.length>30)throw Error("Workspace limit exceeded");
   for(const x of incoming){x.id="imported-"+Date.now()+"-"+Math.random().toString(36).slice(2,7);spaces.push(x);}
   selected=spaces[spaces.length-1].id;save();renderDesk();renderSearch();setStatus("Imported "+incoming.length+" workspace(s). Stored in this browser.");
 }catch(err){setStatus("Import failed: "+err.message);}
 finally{$("#import-workspace").value="";}
}
function brief(){
 const s=current();if(!s)return "";
 const lines=["# "+s.name,"","## Research notes",s.notes||"(No notes yet)","","## Selected sources"];
 for(const id of s.items){
   const r=record(id);
   if(!r){lines.push("- "+id+" (source not found in this catalog)");continue;}
   lines.push("- ["+r.type+"] "+r.title+" — "+r.subtitle+(r.url?" — "+r.url:""));
   if(r.type==="concept"){
     const c=atlas.concepts.find(x=>x.id===id.slice(8)),v=s.reviews?.[id.slice(8)];
     if(c)lines.push("  - Learning check: "+c.question+(v?" | Self-rating: "+v.rating+", next review "+v.due:" | Not self-assessed"));
   }
 }
 lines.push("","## Required research method","1. Separate direct source evidence from editorial study notes and hypotheses.","2. Verify printed book page numbers against the source; they differ from PDF page offsets.","3. Find newer related papers in ConfHub. Compare assumptions, dataset, baselines and evaluation.","4. Mark unsupported conclusions as unverified. Design a test that could falsify the hypothesis.","","BookHub export: metadata and user notes only; full PDF text not included.");
 return lines.join("\n");
}
async function copyBrief(){
 try{await navigator.clipboard.writeText(brief());setStatus("Study brief copied. Paste it into your research agent.");}
 catch{const ta=el("textarea");ta.value=brief();document.body.append(ta);ta.select();const ok=document.execCommand("copy");ta.remove();setStatus(ok?"Study brief copied.":"Clipboard unavailable; use JSON export.");}
}
function svg(name,attrs){const e=document.createElementNS(NS,name);for(const [k,v] of Object.entries(attrs||{}))e.setAttribute(k,String(v));return e;}
function selectConcept(id){if(!atlas.concepts.some(c=>c.id===id))return;selectedConcept=id;drawGraph();renderDetail();}
function drawGraph(){
 const host=$("#graph-visual");host.replaceChildren();
 const root=svg("svg",{viewBox:"0 0 740 470",role:"img","aria-label":"Concept graph with selectable nodes and related learning topics"});
 for(const edge of atlas.edges){
   if(!positions[edge.from]||!positions[edge.to])continue;
   const a=positions[edge.from],b=positions[edge.to];
   root.append(svg("line",{x1:a[0],y1:a[1],x2:b[0],y2:b[1],class:"edge"+(edge.from===selectedConcept||edge.to===selectedConcept?" active":"")}));
 }
 for(const c of atlas.concepts){
   const p=positions[c.id];if(!p)continue;
   const group=svg("g",{class:"graph-node"+(selectedConcept===c.id?" active":""),role:"button",tabindex:0,
     "aria-label":"Inspect "+c.title});
   const dot=svg("circle",{cx:p[0],cy:p[1],r:selectedConcept===c.id?8:5,class:"node-dot"});
   const title=svg("title");title.textContent=c.title;dot.append(title);
   const caption=svg("text",{x:p[0],y:p[1]-15,"text-anchor":"middle",class:"node-label"});
   caption.textContent=c.title.length>21?c.title.slice(0,21)+"…":c.title;
   group.append(dot,caption);
   group.addEventListener("click",()=>selectConcept(c.id));
   group.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();selectConcept(c.id);}});
   root.append(group);
 }
 host.append(root);
 const menu=$("#concepts-list");menu.replaceChildren();
 for(const c of atlas.concepts){
   const b=el("button",selectedConcept===c.id?"active":"",c.title);b.type="button";b.setAttribute("aria-pressed",String(selectedConcept===c.id));
   b.addEventListener("click",()=>selectConcept(c.id));menu.append(b);
 }
}
function renderDetail(){
 const c=atlas.concepts.find(x=>x.id===selectedConcept);if(!c)return;
 const target=$("#concept-detail");target.replaceChildren(el("p","small-label","Selected concept"));
 target.append(el("h3",null,c.title),el("p",null,c.definition),el("h4",null,"Question to test"),el("blockquote",null,c.question),el("h4",null,"Where to read"));
 const ul=el("ul","concept-sources");
 for(const s of atlas.chapters.filter(x=>x.concepts.includes(c.id))){
   const b=fromBook(s.book),item=el("li"),source=external(b?.pdfUrl)||external(b?.publisherUrl)||"";
   if(source)item.append(link("Chapter "+s.number+" · "+s.title,source));
   else item.append(el("span",null,"Chapter "+s.number+" · "+s.title));
   item.append(el("small",null,(b?.title||"Book")+(s.page?" · printed page "+s.page:" · page not verified")));
   ul.append(item);
 }
 target.append(ul);
 const actions=el("div","detail-actions"),btn=el("button",null,current()?.items.includes("concept:"+c.id)?"Remove from desk":"Add to desk");
 btn.type="button";btn.addEventListener("click",()=>toggleItem("concept:"+c.id));
 const linkToPapers=el("a",null,"Find papers in ConfHub ↗");linkToPapers.href="../../cs-conf/hub/?q="+encodeURIComponent(c.title);linkToPapers.title="Prefill a ConfHub search with this concept";
 actions.append(btn,linkToPapers);target.append(actions);
 const self=el("div","self-check"),label=el("h4",null,"Active recall"),instruction=el("p",null,"Answer the question without looking at the chapter, then verify your explanation. Self-rate only after checking; no AI grades this.");
 const rate=el("div","detail-actions");for(const [kind,name] of [["needs-work","Needs another pass · tomorrow"],["self-reviewed","Explained and checked · 7 days"]]){
   const b=el("button",null,name);b.type="button";b.addEventListener("click",()=>markReview(c.id,kind));rate.append(b);
 }
 const v=current()?.reviews?.[c.id];self.append(label,instruction,rate,el("p","review-state",v?"Last self-rating: "+v.rating+" · review on "+v.due:"No review scheduled yet."));target.append(self);
 target.append(el("p","curation-note","Learning relation, not an empirical or novelty claim. The book sources indicate where a topic is discussed; read the chapter before citing a specific claim."));
}
function wire(){
 $("#search").addEventListener("input",()=>{visible=11;renderSearch();});
 $("#clear-search").addEventListener("click",()=>{$("#search").value="";visible=11;activeFilter="all";filters();renderSearch();$("#search").focus();});
 $("#show-more").addEventListener("click",()=>{visible+=20;renderSearch();});
 for(const b of document.querySelectorAll("[data-filter]"))b.addEventListener("click",()=>{activeFilter=b.dataset.filter;visible=11;filters();renderSearch();});
 $("#workspace-select").addEventListener("change",e=>{selected=e.target.value;save();renderDesk();renderSearch();renderDetail();});
 $("#workspace-notes").addEventListener("input",e=>{const s=current();if(s){s.notes=e.target.value.slice(0,50000);save();}});
 $("#new-workspace").addEventListener("click",newSpace);
 $("#rename-workspace").addEventListener("click",renameSpace);
 $("#delete-workspace").addEventListener("click",deleteSpace);
 $("#export-workspace").addEventListener("click",downloadJSON);
 $("#import-workspace").addEventListener("change",e=>importJSON(e.target.files[0]));
 $("#copy-brief").addEventListener("click",copyBrief);
}
async function start(){
 try{
   const responses=await Promise.all([fetch("../books.json",{cache:"no-cache"}),fetch("./atlas.json",{cache:"no-cache"})]);
   if(responses.some(x=>!x.ok))throw Error("The library or atlas could not be fetched.");
   const data=await Promise.all(responses.map(x=>x.json()));
   if(!Array.isArray(data[0]?.books)||!Array.isArray(data[1]?.concepts)||!Array.isArray(data[1]?.chapters))throw Error("Unexpected catalog data.");
   books=data[0].books;atlas=data[1];papers=loadPins();records=makeRecords();spaces=loadSpaces();
   try{selected=localStorage.getItem(ACTIVE)||spaces[0].id;}catch{selected=spaces[0].id;}
   if(!spaces.find(s=>s.id===selected))selected=spaces[0].id;
   const q=new URLSearchParams(location.search).get("q");if(q)$("#search").value=q.slice(0,150);
   $("#summary").replaceChildren();
   for(const [n,label] of [[books.length,"books"],[atlas.chapters.length,"indexed chapters"],[atlas.concepts.length,"concepts"],[papers.length,"ConfHub pins on this device"]]){
     const item=el("span"),strong=el("strong",null,n);item.append(strong,document.createTextNode(label));$("#summary").append(item);
   }
   wire();filters();renderDesk();renderSearch();selectConcept(selectedConcept);
 }catch(err){
   $("#summary").textContent="Library temporarily unavailable.";
   $("#result-count").textContent="Could not load the catalog.";
   $("#results").append(el("p","empty-results",err.message+" Reload this page or check the published JSON files."));
   $("#save-status").textContent="Workspace data not loaded.";
   for(const x of document.querySelectorAll("button,input,select,textarea"))if(x.id!=="clear-search")x.disabled=true;
 }
}
start();
})();
