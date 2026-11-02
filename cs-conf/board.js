(()=>{
"use strict";
const $=id=>document.getElementById(id);
const STORE="cs-conf-submission-board-v3",COMP_STORE="cs-conf-competition-board-v1",OLD_STORE="cs-conf-opportunities-status-v1";
let board={},cboard={},old={},opps=[],comps=[],rates=[];
for(const [key,assign] of [[STORE,x=>board=x],[COMP_STORE,x=>cboard=x],[OLD_STORE,x=>old=x]]){
  try{const v=JSON.parse(localStorage.getItem(key)||"{}");assign(v&&typeof v==="object"?v:{});}catch(_){assign({});}
}
const actKinds=new Set(["abstract","arr-paper","extended-abstract","paper","demo","workshop-paper","workshop-proposal","registration","commitment","arr-commitment","other"]);
const paperKinds=new Set(["research","industry","paper","abstract","demo","workshop-paper"]);
const fmt=new Intl.DateTimeFormat("en-GB",{day:"numeric",month:"short",year:"numeric",timeZone:"UTC"});
const ist=()=>{const x={};new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Kolkata",year:"numeric",month:"2-digit",day:"2-digit"}).formatToParts(new Date()).forEach(p=>x[p.type]=p.value);return x.year+"-"+x.month+"-"+x.day;};
const addDays=(d,n)=>{const x=new Date(d+"T12:00:00Z");x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10);};
const daysApart=(a,b)=>Math.round((Date.parse(b+"T12:00:00Z")-Date.parse(a+"T12:00:00Z"))/86400000);
const fdate=d=>d?fmt.format(new Date(d+"T12:00:00Z")):"TBA";
const el=(tag,content,parent,className)=>{const z=document.createElement(tag);if(content!==null&&content!==undefined)z.textContent=String(content);if(className)z.className=className;if(parent)parent.append(z);return z;};
const link=(label,url,parent)=>{const x=el("a",label,parent);if(/^https:\/\//i.test(url||"")){x.href=url;x.target="_blank";x.rel="noopener noreferrer";}else x.removeAttribute("href");return x;};
const stageInstant=s=>{if(s.at){const d=new Date(s.at);if(!isNaN(d))return d;}if(s.date&&/AoE|anywhere on earth/i.test(s.cutoff||""))return new Date(s.date+"T23:59:00-12:00");return null;};
const isPast=(s,today)=>{if(!s.date)return false;const x=stageInstant(s);return x?x.getTime()<Date.now():s.date<today;};
const stages=o=>(o.stages||[]).filter(s=>s.date&&actKinds.has(s.kind)&&s.actionable!==false).sort((a,b)=>a.date.localeCompare(b.date));
const chooseStage=(o,today)=>{const all=stages(o).filter(s=>!isPast(s,today));return all.find(s=>!/optional|pre-submission mentorship/i.test(s.label||""))||all[0]||null;};
const paperStage=o=>{const p=(o.stages||[]).filter(s=>s.date&&/^(paper|demo|workshop-paper|arr-paper|extended-abstract)$/.test(s.kind));return p.sort((a,b)=>b.date.localeCompare(a.date))[0]||null;};
const stageDue=(s,today)=>{if(!s||!s.date)return "TBA";const x=stageInstant(s),n=x?Math.ceil((x.getTime()-Date.now())/86400000):daysApart(today,s.date);return (n<0?"past":n===0?"today":n===1?"1 day":"in "+n+" days");};
function areaOf(o){const s=(o.venue+" "+o.track+" "+o.category).toLowerCase();if(/speech|audio|acoustic|interspeech|icassp|eeg/.test(s))return "Speech";if(/robot|rss 2027|icra|iros|embodied/.test(s))return "Robotics";if(/medical|neuro|biolog|midl|miccai|recomb/.test(s))return "Medical / Bio";if(/vision|cvpr|image|3d|video/.test(s))return "Vision / 3D";if(/nlp|naacl|acl 2027|eacl|coling|language|linguist/.test(s))return "NLP / LLM";if(/search|retrieval|data mining|sigir|ecir|kdd|pakdd|database/.test(s))return "IR / Data";if(/icml|iclr|neurips|mlsys|learning|ai4science|ijcai|statistics/.test(s))return "AI / ML";return "Other CS";}
const selected=v=>["target","drafting","submitted"].includes(v||"");
function save(){try{localStorage.setItem(STORE,JSON.stringify(board));}catch(e){const n=$("copy-notice");if(n)n.textContent="Cannot save in this browser: "+e.message;}}
function saveComp(){try{localStorage.setItem(COMP_STORE,JSON.stringify(cboard));}catch(e){const n=$("copy-notice");if(n)n.textContent="Cannot save in this browser: "+e.message;}}
const oldStage=o=>old[o.id]||"";
const hasAbstract=o=>Boolean(board[o.id]&&board[o.id].abstractFiled)||oldStage(o)==="abstract-filed";
function gateInfo(o,today){
 const arr=String(o.prereg||"").toLowerCase();
 if(arr.includes("arr"))return {text:"Requires eligible ARR reviews and meta-review",risk:"alert"};
 const abs=(o.stages||[]).filter(s=>["abstract","extended-abstract"].includes(s.kind)).sort((a,b)=>a.date.localeCompare(b.date))[0];
 const explicit=(o.stages||[]).some(s=>s.requires==="abstract");
 if(abs||explicit){
  if(abs&&isPast(abs,today)&&!hasAbstract(o))return {text:"VERIFY prior abstract / registration filed ("+fdate(abs.date)+")",risk:"alert"};
  if(abs&&isPast(abs,today)&&hasAbstract(o))return {text:"Abstract filed (self-declared); verify author list",risk:"good"};
  if(abs)return {text:"Abstract / enrollment: "+fdate(abs.date),risk:"warn"};
  return {text:"Abstract gate required: check official CFP",risk:"alert"};
 }
 if(arr.includes("mandatory"))return {text:"Mandatory preregistration: verify CFP",risk:"warn"};
 return {text:"No mandatory abstract recorded; verify CFP",risk:""};
}
function acceptInfo(o){
 let v=(o.venue||"").toLowerCase();
 const rec=rates.find(a=>new RegExp("\\b"+a.venueKey.toLowerCase()+"\\b").test(v));
 if(!rec)return null;
 const exactly=/\bmain\b/i.test(o.track||"")&&o.kind==="research";
 return {rec,exactly};
}
function gateCell(o,s,today,tr){
 const td=el("td",null,tr),date=el("div",s?fdate(s.date):"TBA",td,"date row-strong");
 if(s){el("span",s.label||s.kind,td,"line");el("span",stageDue(s,today),td,"line");if(s.cutoff)el("span",s.cutoff,td,"line");
 if(s.verification&&s.verification!=="official")el("span","Date: "+s.verification,td,"flag warn");
 }else el("span","Next CFP not verified",td,"flag warn");
 return td;
}
function renderWatch(){
 const root=$("watch-list");if(!root)return;root.replaceChildren();
 const items=[
 ["NeurIPS","2027 main CFP TBA","https://neurips.cc/Conferences/2027",""],
 ["ICLR","2027 main papers closed","https://iclr.cc/Conferences/2027/CallForPapers",""],
 ["ICML","2027 main CFP to verify","https://icml.cc/Conferences/2027",""],
 ["CVPR","10 Nov register · 16 Nov paper","https://cvpr.thecvf.com/Conferences/2027/CallForPapers","soon"],
 ["IJCAI","4 Jan abstract · 11 Jan paper","https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/",""],
 ["SemEval","Jan 10–31 shared tasks","https://semeval.github.io/SemEval2027/",""]
 ];
 items.forEach(x=>{const e=el("div",null,root,"watch-item "+x[3]);link(x[0],x[2],e).style.fontWeight="700";el("span",x[1],e,"when");});
}
function rowStages(o,parent){
 const d=el("details",null,parent),su=el("summary","All dates & requirements",d),ul=el("ul",null,d);
 (o.stages||[]).forEach(s=>{const z=el("li",(s.date?fdate(s.date):"TBA")+" · "+(s.label||s.kind)+(s.requires?" · needs "+s.requires:"")+(s.verification&&s.verification!=="official"?" · "+s.verification:""),ul);});
 if(o.notes)el("p",o.notes,d,"line");
 return d;
}
function statusSelect(o,tr){
 const td=el("td",null,tr),sel=el("select",null,td,"status"),v=board[o.id]?.state||"";
 for(const [a,b] of [["","Unreviewed"],["watch","Watch"],["target","Target"],["drafting","Drafting"],["submitted","Submitted"],["skip","Strike through"]]){const opt=el("option",b,sel);opt.value=a;}
 sel.value=v;sel.setAttribute("aria-label","Plan status for "+o.venue+" "+o.track);
 sel.addEventListener("change",()=>{if(!board[o.id])board[o.id]={};board[o.id].state=sel.value;board[o.id].updatedAt=new Date().toISOString();save();renderBoard();});
 const s=oldStage(o);if(s&&s!=="")el("div","Previous status (other local board): "+s,td,"line");
 return td;
}
function drawConference(o,s,today,root){
 const mode=board[o.id]?.state||"";
 const tr=el("tr",null,root,["target","drafting"].includes(mode)?"target":mode==="submitted"?"submitted":mode==="skip"?"skip":"");
 statusSelect(o,tr);
 gateCell(o,s,today,tr);
 const name=el("td",null,tr);
 link(o.venue+" — "+o.track,o.source,name).className="track-name";
 el("div",areaOf(o)+" · "+(o.kind||"Research"),name,"line");
 if(/NeurIPS|ICLR|ICML|CVPR|IJCAI/i.test(o.venue))el("span","Priority venue",name,"flag warn");
 if(o.coreRankHint)el("span","CORE list "+o.coreRankHint+" (verify)",name,"flag");
 rowStages(o,name);
 const prereq=gateInfo(o,today),gt=el("td",null,tr);el("span",prereq.text,gt,"flag "+prereq.risk);
 if(prereq.risk==="alert"&&hasAbstract(o)===false&&/abstract/i.test(prereq.text)){
  const lb=el("label",null,gt),cb=el("input",null,lb);cb.type="checkbox";cb.checked=false;lb.append(document.createTextNode(" I filed this abstract"));cb.addEventListener("change",()=>{board[o.id]=board[o.id]||{};board[o.id].abstractFiled=cb.checked;save();renderBoard();});
 }
 const p=paperStage(o),pCell=el("td",null,tr);
 if(p){el("div",fdate(p.date),pCell,"date row-strong");el("span",p.label||"Paper stage",pCell,"line");}
 else el("span","TBA / see CFP",pCell,"muted");
 const a=acceptInfo(o),aCell=el("td",null,tr);
 if(a){link(a.rec.percent.toFixed(1)+"% · "+a.rec.year+" main",a.rec.source,aCell);el("div",a.exactly?"Historical main-track (same category)":"Parent main-track ONLY; not this track",aCell,"line");}
 else el("span","N/A — not verified",aCell,"muted");
 const e=el("td",null,tr);
 el("span",o.academicEligibility==="✓"?"✓ Academic teams allowed":o.academicEligibility==="✕"?"✕ Non-academic author rule":"? Check author rule",e,"flag "+(o.academicEligibility==="✓"?"good":o.academicEligibility==="✕"?"alert":"warn"));
 if(o.kind==="demo"||o.kind==="industry")el("div","Practical evidence / deployment rules are separate",e,"line");
 const c=el("td",null,tr);if(/ICASSP|SemEval|NeurIPS|PAIEC/i.test(o.venue+" "+o.track))link("Competition → paper routes","./competitions.html",c);else el("span","No confirmed linked contest",c,"muted");
 link("Official CFP",o.source,el("td",null,tr));
}
function renderBoard(){
 const table=$("conference-rows");if(!table)return;
 const now=ist(),mode=$("window").value,end=addDays(now,mode==="all"||mode==="archive"?36500:Number(mode));
 const area=$("area").value,kind=$("kind").value,q=$("search").value.trim().toLowerCase(),view=$("window").value,only=$("shortlisted").checked;
 const all=opps.map(o=>({o,s:chooseStage(o,now)}));
 const visible=all.filter(({o,s})=>{
  const live=s&&s.date<=end;
  if(view==="archive"){if(s)return false; if(!(o.stages||[]).some(v=>v.date&&actKinds.has(v.kind)))return false;}
  else if(view==="all"){/* include TBA */}
  else if(!live)return false;
  if(area!=="all"&&areaOf(o)!==area)return false;
  if(kind!=="all"&&(kind==="paper"? !paperKinds.has(o.kind):o.kind!==kind))return false;
  if(only&&!selected(board[o.id]?.state))return false;
  if(q&&!(o.venue+" "+o.track+" "+o.category+" "+o.notes).toLowerCase().includes(q))return false;
  return true;
 }).sort((a,b)=>(a.s?a.s.date:"9999-12-31").localeCompare(b.s?b.s.date:"9999-12-31")||(a.o.venue+" "+a.o.track).localeCompare(b.o.venue+" "+b.o.track));
 table.replaceChildren();
 visible.forEach(({o,s})=>drawConference(o,s,now,table));
 if(!visible.length)el("tr",null,table).append(el("td","No matching confirmed future stage. Try All dates/TBA or clear filters."));
 const candidates=all.filter(({o,s})=>s&&s.date<=addDays(now,90)&&paperKinds.has(o.kind));
 const planned=opps.filter(o=>selected(board[o.id]?.state));
 if($("candidate-count"))$("candidate-count").textContent=String(candidates.length);
 if($("target-count"))$("target-count").textContent=planned.length+" / 10";
 if($("deadline-stat"))$("deadline-stat").textContent=String(all.filter(({s})=>s&&s.date<=addDays(now,30)).length);
 if($("contest-stat"))$("contest-stat").textContent=String(comps.filter(c=>c.deadline&&c.deadline>=now&&c.deadline<=addDays(now,90)).length);
 if($("count-label"))$("count-label").textContent=visible.length+" visible of "+opps.length+" tracked routes. "+candidates.length+" paper/demo/industry/workshop candidate routes within 90 days (not 10 completed submissions).";
 if($("plan-note"))$("plan-note").textContent=planned.length<10?"Select "+(10-planned.length)+" more DISTINCT targets to plan 10 submissions; an abstract + its paper count once.":planned.length===10?"10 target routes selected. Verify every prerequisite and eliminate overlapping submissions.":"More than 10 targets selected. Consider narrowing the plan to a feasible 10.";
 renderPreview();
}
function renderPreview(){
 const root=$("contest-preview");if(!root)return;root.replaceChildren();const t=ist(),list=comps.filter(c=>c.deadline&&c.deadline>=t).sort((a,b)=>a.deadline.localeCompare(b.deadline)).slice(0,6);
 for(const c of list){const tr=el("tr",null,root);el("td",fdate(c.deadline),tr,"date");const td=el("td",null,tr);link(c.title,c.source,td);el("td",c.stage||"Challenge",tr);el("td",c.paperRouteStatus||"No verified paper route",tr);const last=el("td",null,tr);link("Details","./competitions.html",last);}
}
function renderCompetition(){
 const root=$("competition-rows");if(!root)return;root.replaceChildren();
 const now=ist(),window=$("comp-window").value,field=$("comp-field").value,paper=$("comp-paper").value,q=$("comp-query").value.toLowerCase().trim();
 const list=comps.filter(c=>{
  if(window==="90"&&(!c.deadline||c.deadline<now||c.deadline>addDays(now,90)))return false;
  if(window==="past"&&(!c.deadline||c.deadline>=now))return false;
  if(window==="all"){}else if(window!=="past"&&window!=="90"&&(!c.deadline||c.deadline<now))return false;
  if(field!=="all"&&!(c.field||"").toLowerCase().includes(field))return false;
  if(paper==="yes"&&/No confirmed|No automatic/i.test(c.paperRouteStatus||""))return false;
  if(q&&!(c.title+" "+c.series+" "+c.field+" "+c.notes).toLowerCase().includes(q))return false;
  return true;
 }).sort((a,b)=>(a.deadline||"9999").localeCompare(b.deadline||"9999")||a.title.localeCompare(b.title));
 for(const c of list){
  const state=cboard[c.id]||"",tr=el("tr",null,root,state==="skip"?"skip":selected(state)?"target":"");
  const date=el("td",null,tr);el("div",fdate(c.deadline),date,"date row-strong");el("span",c.deadlineAccuracy||"Verify organizer time",date,"line");if(c.opens)el("span","Opens "+fdate(c.opens),date,"line");
  const name=el("td",null,tr);link(c.title,c.source,name).className="track-name";el("div",c.series+" · "+(c.field||"ML"),name,"line");if(c.priority==="high")el("span","Priority",name,"flag warn");
  const stage=el("td",c.stage||"Evaluation / challenge submission",tr);if(c.registrationDeadline)el("div","Register by "+fdate(c.registrationDeadline),stage,"flag warn");if(c.notes)el("div",c.notes,stage,"line");
  const route=el("td",null,tr);el("div",c.paperRoute||"N/A",route,"row-strong");el("div",c.paperRouteStatus||"Verify organizer",route,"line");
  if(c.paperDue)el("div","Paper/report: "+fdate(c.paperDue),route,"line");
  if(c.paperUrl)link("Paper path",c.paperUrl,route);
  const elig=el("td",c.eligibility||"Verify rules",tr);
  const status=el("td",null,tr),sel=el("select",null,status,"status");
  [["","Unreviewed"],["watch","Watch"],["target","Target"],["drafting","Working"],["submitted","Submitted"],["skip","Strike through"]].forEach(([v,s])=>{const o=el("option",s,sel);o.value=v;});sel.value=state;
  sel.setAttribute("aria-label","Status for "+c.title);sel.addEventListener("change",()=>{cboard[c.id]=sel.value;saveComp();renderCompetition();});
  link("Official",c.source,el("td",null,tr));
 }
 if(!list.length){const tr=el("tr",null,root);const td=el("td","No matching competition (or official deadline not yet known).",tr);td.colSpan=7;}
 if($("competition-count"))$("competition-count").textContent=list.length+" visible of "+comps.length+" monitored";
 if($("comp-targets"))$("comp-targets").textContent=comps.filter(c=>selected(cboard[c.id])).length;
}
function attach(){
 if($("conference-rows")){
  ["window","area","kind","search","shortlisted"].forEach(id=>{const x=$(id);x.addEventListener(id==="search"?"input":"change",renderBoard);});
  $("review-button").addEventListener("click",()=>{board._lastReviewed=ist();save();showReview();});
  $("copy-plan").addEventListener("click",async()=>{
   const records=opps.filter(o=>selected(board[o.id]?.state)).map(o=>o.venue+" · "+o.track+" | "+board[o.id].state+" | "+o.source);
   const text="PRIVATE planning list — DO NOT publish\nReview "+ist()+"\n"+records.join("\n");
   try{await navigator.clipboard.writeText(text);$("copy-notice").textContent="Copied planned routes. Save only in your private GitHub repository.";}catch(_){$("copy-notice").textContent="Clipboard unavailable; use your browser's site permissions.";}
  });
  renderBoard();showReview();
 }
 if($("competition-rows")){["comp-window","comp-field","comp-paper","comp-query"].forEach(id=>$(id).addEventListener(id==="comp-query"?"input":"change",renderCompetition));renderCompetition();}
}
function showReview(){
 if(!$("review-due"))return;
 const date=typeof board._lastReviewed==="string"?board._lastReviewed:"2026-11-02";
 const due=addDays(date,30);
 $("review-due").textContent="30-day editorial review due "+fdate(due)+" · last marked "+fdate(date)+" (this browser only).";
}
async function init(){
 renderWatch();
 try{
  const [o,c,a]=await Promise.all(["./opportunities.json","./competitions.json","./acceptance.json"].map(x=>fetch(x,{cache:"no-store"}).then(r=>{if(!r.ok)throw new Error(x+": HTTP "+r.status);return r.json();})));
  opps=o.opportunities||[];comps=c.competitions||[];rates=a.records||[];
  if($("audit-date"))$("audit-date").textContent="Competition/priority sources checked "+c.checkedAt+"; existing track catalog last overall audit "+o.checkedAt+". Official organizer pages override these snapshots.";
  attach();
 }catch(e){const z=$("load-message");if(z)z.textContent="Could not load the tracked sources: "+e.message+". Use official CFP links or reload the page."; }
}
init();
})();
