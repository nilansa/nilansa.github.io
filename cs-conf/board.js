(()=>{
"use strict";
const $=id=>document.getElementById(id);
const STORE="cs-conf-submission-board-v3",COMP_STORE="cs-conf-competition-board-v1",OLD_STORE="cs-conf-opportunities-status-v1";
let board={},cboard={},old={},opps=[],comps=[],rates=[],viewLimit=25;
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
const stageInstant=s=>{
 if(s.at){const d=new Date(s.at);if(!isNaN(d.getTime()))return d;}
 if(s.date&&/\bAoE\b|anywhere on earth/i.test(s.cutoff||""))return new Date(s.date+"T23:59:00-12:00");
 return null;
};
const isPast=(s,today)=>{if(!s.date)return false;const x=stageInstant(s);return x?x.getTime()<Date.now():s.date<today;};
const stages=o=>(o.stages||[]).filter(s=>s.date&&actKinds.has(s.kind)&&s.actionable!==false).sort((a,b)=>a.date.localeCompare(b.date));
const chooseStage=(o,today)=>{
 const done=["paper-filed","done"].includes(oldStage(o))||effectiveState(o)==="submitted";
 const all=stages(o).filter(s=>!isPast(s,today))
   .filter(s=>!(s===mandatoryAbstract(o)&&hasAbstract(o)))
   .filter(s=>!(done&&["paper","demo","workshop-paper","arr-paper"].includes(s.kind)));
 return all.find(s=>!/optional|pre-submission mentorship/i.test(s.label||""))||all[0]||null;
};
const paperStage=o=>{const p=(o.stages||[]).filter(s=>s.date&&/^(paper|demo|workshop-paper|arr-paper|extended-abstract)$/.test(s.kind));return p.sort((a,b)=>b.date.localeCompare(a.date))[0]||null;};
const stageDue=(s,today)=>{if(!s||!s.date)return "TBA";const x=stageInstant(s),ms=x?x.getTime()-Date.now():null,n=x?Math.ceil(ms/86400000):daysApart(today,s.date);return x&&ms>0&&ms<172800000?"in "+Math.ceil(ms/3600000)+" hours":(n<0?"past":n===0?"today":n===1?"1 day":"in "+n+" days");};
function areaOf(o){const s=(o.venue+" "+o.track+" "+o.category).toLowerCase();if(/speech|audio|acoustic|interspeech|icassp|eeg/.test(s))return "Speech";if(/robot|rss 2027|icra|iros|embodied/.test(s))return "Robotics";if(/medical|neuro|biolog|midl|miccai|recomb/.test(s))return "Medical / Bio";if(/vision|cvpr|image|3d|video/.test(s))return "Vision / 3D";if(/nlp|naacl|acl 2027|eacl|coling|language|linguist/.test(s))return "NLP / LLM";if(/search|retrieval|data mining|sigir|ecir|kdd|pakdd|database/.test(s))return "IR / Data";if(/icml|iclr|neurips|mlsys|learning|ai4science|ijcai|statistics/.test(s))return "AI / ML";return "Other CS";}
const selected=v=>["target","drafting","submitted"].includes(v||"");
function save(){try{localStorage.setItem(STORE,JSON.stringify(board));}catch(e){const n=$("copy-notice");if(n)n.textContent="Cannot save in this browser: "+e.message;}}
function saveComp(){try{localStorage.setItem(COMP_STORE,JSON.stringify(cboard));}catch(e){const n=$("copy-notice");if(n)n.textContent="Cannot save in this browser: "+e.message;}}
const oldStage=o=>old[o.id]||"";
const isMandatoryPrereg=o=>["mandatory","mandatory-abstract"].includes(String(o.prereg||"").toLowerCase());
const mandatoryAbstract=o=>{
 const abstracts=(o.stages||[]).filter(s=>s.kind==="abstract"&&s.date);
 const marked=abstracts.filter(s=>s.mandatory===true).sort((a,b)=>a.date.localeCompare(b.date));
 if(marked.length)return marked[0];
 return isMandatoryPrereg(o)&&abstracts.length===1?abstracts[0]:null;
};
function effectiveState(o){
 const detail=oldStage(o),plan=board[o.id]?.state||"";
 if(["excluded","withdrawn","done"].includes(detail))return "skip";
 if(plan==="skip")return "skip";
 if(plan)return plan;
 return detail==="paper-filed"?"submitted":detail==="interested"?"watch":"";
}
const hasAbstract=o=>Boolean(board[o.id]?.abstractFiled)||["abstract-filed","paper-filed","done"].includes(oldStage(o));
function storePlanningStatus(o,state){
 const prev=oldStage(o);
 board[o.id]={...(board[o.id]||{}),state,updatedAt:new Date().toISOString()};
 if(state==="skip"){
  if(["","interested","excluded","withdrawn","done"].includes(prev))old[o.id]="excluded";
 }else if(["excluded","withdrawn","done"].includes(prev)){
  if(!state)delete old[o.id];else old[o.id]=state==="submitted"?"paper-filed":"interested";
 }else if(state==="submitted"&&["","interested"].includes(prev)){
  old[o.id]="paper-filed";
 }
 save();try{localStorage.setItem(OLD_STORE,JSON.stringify(old));}catch(e){
  const n=$("copy-notice");if(n)n.textContent="Detailed-status sync unavailable: "+e.message;
 }
 renderBoard();renderWatch();
}
function gateInfo(o,today,stage=null){
 const detail=oldStage(o);
 if(detail==="missed-abstract")return {text:"BLOCKED — you marked the mandatory abstract missed",risk:"alert",blocked:true};
 if(o.prereg==="arr-required")return {text:"VERIFY eligible ARR submission / reviews before commitment",risk:"alert"};
 if(o.prereg==="stage1-required"){
  if(["stage1-filed","paper-filed"].includes(detail))return {text:"Stage 1 marked filed; verify organizer invitation",risk:"good"};
  const first=(o.stages||[]).find(s=>s.kind==="extended-abstract"&&s.mandatory);
  return {text:first&&isPast(first,today)?"VERIFY prior Stage 1/invitation":"Stage 1 proposal and invitation required",risk:"alert"};
 }
 if(isMandatoryPrereg(o)){
  const abs=mandatoryAbstract(o);
  if(!abs)return {text:"VERIFY exact mandatory abstract / enrollment stage",risk:"alert"};
  if(hasAbstract(o))return {text:"Mandatory abstract marked filed (this browser)",risk:"good"};
  if(isPast(abs,today))return {text:"VERIFY mandatory abstract filed — "+fdate(abs.date),risk:"alert"};
  return {text:"Mandatory abstract first — "+fdate(abs.date),risk:"warn"};
 }
 if(stage&&(stage.kind==="arr-commitment"||stage.requires==="arr"))
  return {text:"VERIFY eligible ARR reviews before commitment",risk:"alert"};
 if(o.prereg==="check-workshop")return {text:"VERIFY this individual workshop CFP",risk:"warn"};
 if(o.prereg==="unknown")return {text:"Preregistration policy not verified",risk:"warn"};
 if(o.prereg==="none-listed")return {text:"No mandatory abstract listed; confirm CFP",risk:""};
 return {text:"Verify organizer rules",risk:"warn"};
}

function acceptInfo(o){
 let v=(o.venue||"").toLowerCase();
 const rec=rates.find(a=>new RegExp("\\b"+a.venueKey.toLowerCase()+"\\b").test(v));
 if(!rec)return null;
 const exactly=/\bmain\b/i.test(o.track||"")&&o.kind==="research";
 return {rec,exactly};
}
function gateCell(o,s,today,tr){
 const td=el("td",null,tr),last=stages(o).filter(x=>isPast(x,today)).at(-1);el("div",s?fdate(s.date):last?"Closed "+fdate(last.date):"TBA",td,"date row-strong");
 if(s){el("span",s.label||s.kind,td,"line");el("span",stageDue(s,today),td,"line");if(s.cutoff)el("span",s.cutoff,td,"line");
 if(s.verification&&s.verification!=="official")el("span","Date: "+s.verification,td,"flag warn");
 }else if(last){el("span","Last deadline closed · "+last.label,td,"flag alert");}else el("span","Next CFP not verified",td,"flag warn");
 return td;
}
function renderRates(){
 const root=$("rate-rows");if(!root)return;root.replaceChildren();
 rates.slice().sort((a,b)=>b.percent-a.percent).forEach(x=>{
 const tr=el("tr",null,root);
 el("td",x.venueKey+" · "+x.year,tr,"row-strong");
 el("td",x.track+" (NOT industry, demo or workshop)",tr);
 el("td",x.accepted.toLocaleString()+" / "+x.submissions.toLocaleString(),tr,"date");
 el("td",x.percent.toFixed(1)+"%",tr,"row-strong");
 const td=el("td",null,tr);link("Source",x.source,td);if(x.note)el("div",x.note,td,"line");
 });
}
function renderWatch(){
 const root=$("watch-list");if(!root)return;root.replaceChildren();
 const now=ist(),next=opps.map(o=>({o,s:chooseStage(o,now)}))
  .filter(({o,s})=>s&&s.verification==="official"&&o.academicEligibility!=="✕"&&!["skip","submitted"].includes(effectiveState(o))&&oldStage(o)!=="missed-abstract")
  .sort((a,b)=>a.s.date.localeCompare(b.s.date)).slice(0,4);
 if(!next.length){el("span","No verified future actions in this snapshot.",root,"muted");return;}
 for(const {o,s} of next){
  const gate=gateInfo(o,now,s);
  const a=el("a",null,root,"watch-item");a.href=o.source;a.target="_blank";a.rel="noopener noreferrer";
  el("span",fdate(s.date),a,"watch-date");
  el("span",(gate.risk==="alert"?"VERIFY prerequisite · ":"")+(s.label||s.kind),a,"watch-stage");
  el("span",o.venue+" · "+o.track,a,"watch-venue");
  el("span",stageDue(s,now),a,"watch-days");
  if(s.at||stageInstant(s))el("span",new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Kolkata",day:"numeric",month:"short",hour:"2-digit",minute:"2-digit",hour12:false}).format(stageInstant(s))+" IST",a,"watch-days");
 }
}
function rowStages(o,parent){
 const d=el("details",null,parent),su=el("summary","All dates & requirements",d),ul=el("ul",null,d);
 (o.stages||[]).forEach(s=>{const z=el("li",(s.date?fdate(s.date):"TBA")+" · "+(s.label||s.kind)+(s.requires?" · needs "+s.requires:"")+(s.verification&&s.verification!=="official"?" · "+s.verification:""),ul);});
 if(o.notes)el("p",o.notes,d,"line");
 return d;
}
function statusSelect(o,tr){
 const td=el("td",null,tr),sel=el("select",null,td,"status"),v=effectiveState(o);
 for(const [a,b] of [["","Unreviewed"],["watch","Watch"],["target","Target"],["drafting","Drafting"],["submitted","Submitted"],["skip","Strike through"]]){
  const opt=el("option",b,sel);opt.value=a;
 }
 sel.value=v;sel.setAttribute("aria-label","Plan status for "+o.venue+" "+o.track);
 sel.addEventListener("change",()=>storePlanningStatus(o,sel.value));
 const d=oldStage(o);
 if(["abstract-filed","arr-filed","stage1-filed","paper-filed","registered","missed-abstract"].includes(d))
  el("span","Detailed stage: "+d.replaceAll("-"," ")+" (this browser)",td,"line");
 return td;
}
function drawConference(o,s,today,root){
 const mode=effectiveState(o);
 const tr=el("tr",null,root,["target","drafting"].includes(mode)?"target":mode==="submitted"?"submitted":mode==="skip"?"skip":"");
 const name=el("td",null,tr);name.dataset.label="Conference";
 link(o.venue+" · "+o.track,o.source,name).className="track-name";
 el("span",areaOf(o)+" · "+(o.kind||"Research"),name,"line");
 if(o.coreRankHint)el("span","CORE "+o.coreRankHint+" · venue hint",name,"flag");
 const history=acceptInfo(o),detail=rowStages(o,name);
 if(history){
  const note=el("p",null,detail,"line");link(history.rec.percent.toFixed(1)+"% past main-track rate",history.rec.source,note);
  el("span",history.exactly?" · comparable research category":" · not this track's rate",note);
 }
 const g=gateInfo(o,today,s),date=gateCell(o,s,today,tr);date.dataset.label="Next cutoff";
 if(g.risk==="alert")el("span",g.blocked?"BLOCKED — mandatory abstract missed":"VERIFY prerequisite before submitting",date,"flag alert");
 const sub=el("td",null,tr);sub.dataset.label="Submission";
 const type=o.kind==="workshop-proposal"?"Workshop organizer proposal":o.kind==="demo"?"System demo":o.kind==="industry"?"Industry / applied":o.kind==="workshop-paper"?"Workshop paper":"Research paper";
 el("div",type,sub,"row-strong");const paper=paperStage(o);
 el("span",paper?"Paper/demo stage "+fdate(paper.date):"Paper stage TBA / see CFP",sub,"line");
 const prereq=el("td",null,tr);prereq.dataset.label="Before submitting";
 el("span",g.text,prereq,"flag "+g.risk);
 el("span",o.academicEligibility==="✓"?"Academic team allowed":o.academicEligibility==="✕"?"Industry affiliation required":"Academic eligibility to verify",prereq,"line");
 if(g.risk==="alert"&&!hasAbstract(o)&&/abstract/i.test(g.text)&&!g.blocked){
  const label=el("label",null,prereq),box=el("input",null,label);box.type="checkbox";box.checked=false;
  label.append(document.createTextNode(" I filed the abstract"));
  box.addEventListener("change",()=>{board[o.id]=board[o.id]||{};board[o.id].abstractFiled=box.checked;if(box.checked&&!oldStage(o))old[o.id]="abstract-filed";save();try{localStorage.setItem(OLD_STORE,JSON.stringify(old));}catch(_){}renderBoard();renderWatch();});
 }
 statusSelect(o,tr);tr.lastElementChild.dataset.label="My plan";
 const source=el("td",null,tr);source.dataset.label="Source";link("Official CFP",o.source,source);
}

function renderBoard(){
 const table=$("conference-rows");if(!table)return;
 const now=ist(),mode=$("window").value,end=addDays(now,mode==="all"||mode==="archive"?36500:Number(mode));
 const area=$("area").value,kind=$("kind").value,q=$("search").value.trim().toLowerCase(),view=$("window").value,only=$("shortlisted").checked;
 const all=opps.map(o=>({o,s:chooseStage(o,now)}));
 const candidates=all.filter(({o,s})=>s&&s.date<=addDays(now,90)&&paperKinds.has(o.kind)&&o.academicEligibility!=="✕");
 const priority=/\b(NAACL|COLING|ACL|EACL|CVPR|IJCAI|ICML|ICLR|NEURIPS|RSS|PAKDD|WSDM|SIGIR|MIDL|ICASSP|ICDE)\b/i;
 const score=({o,s})=>(o.academicEligibility==="✓"?7:0)+(priority.test(o.venue)?6:0)+(s.verification==="official"?6:-7)+(o.kind==="industry"||o.kind==="demo"?5:0)+(o.kind==="workshop-paper"?3:0)+(areaOf(o)==="NLP / LLM"||areaOf(o)==="AI / ML"||areaOf(o)==="Vision / 3D"||areaOf(o)==="IR / Data"?4:0)-(gateInfo(o,now).risk==="alert"?4:0);
 const pool=new Set(candidates.slice().sort((a,b)=>score(b)-score(a)||a.s.date.localeCompare(b.s.date)).slice(0,40).map(x=>x.o.id));
 const visible=all.filter(({o,s})=>{
  const live=s&&s.date<=end;
  if(view==="archive"){if(s)return false; if(!(o.stages||[]).some(v=>v.date&&actKinds.has(v.kind)))return false;}
  else if(view==="all"){/* include TBA */}
  else if(!live)return false;
  if(view==="90"&&$("focus-pool")?.checked&&!pool.has(o.id)&&!selected(effectiveState(o)))return false;
  if(area!=="all"&&areaOf(o)!==area)return false;
  if(kind!=="all"&&(kind==="paper"? !paperKinds.has(o.kind):o.kind!==kind))return false;
  if(only&&!selected(effectiveState(o)))return false;
  if(q&&!(o.venue+" "+o.track+" "+o.category+" "+o.notes).toLowerCase().includes(q))return false;
  return true;
 }).sort((a,b)=>(a.s?a.s.date:"9999-12-31").localeCompare(b.s?b.s.date:"9999-12-31")||(a.o.venue+" "+a.o.track).localeCompare(b.o.venue+" "+b.o.track));
 const progressive=view==="90"&&!q&&area==="all"&&kind==="all"&&!only&&!$("focus-pool").checked;
 const showing=progressive?visible.slice(0,viewLimit):visible;
 table.replaceChildren();
 showing.forEach(({o,s})=>drawConference(o,s,now,table));
 if(!visible.length){
  const tr=el("tr",null,table),td=el("td","No matching future stage. Try All dates/TBA or clear filters.",tr);td.colSpan=6;
 }
 const more=$("show-more");
 if(more){
  more.hidden=!progressive||showing.length===visible.length;
  if(!more.hidden)more.textContent="Show next "+Math.min(25,visible.length-showing.length)+" of "+(visible.length-showing.length)+" remaining routes";
 }
 const planned=opps.filter(o=>selected(effectiveState(o)));
 if($("candidate-count"))$("candidate-count").textContent=String(pool.size);
 if($("target-count"))$("target-count").textContent=planned.length+" / 10";
 if($("deadline-stat"))$("deadline-stat").textContent=String(all.filter(({o,s})=>s&&s.date<=addDays(now,30)&&!["skip","submitted"].includes(effectiveState(o))&&oldStage(o)!=="missed-abstract").length);
 if($("contest-stat"))$("contest-stat").textContent=String(comps.filter(c=>c.deadline&&c.deadline>=now&&c.deadline<=addDays(now,90)).length);
 if($("count-label"))$("count-label").textContent=showing.length+" shown / "+visible.length+" matching routes · "+opps.length+" tracked overall. All 90-day results remain accessible.";
 if($("plan-note"))$("plan-note").textContent=planned.length<10?"Select "+(10-planned.length)+" more DISTINCT targets to plan 10 submissions; an abstract + its paper count once.":planned.length===10?"10 target routes selected. Verify every prerequisite and eliminate overlapping submissions.":"More than 10 targets selected. Consider narrowing the plan to a feasible 10.";
 renderPreview();renderSlate();
}
function renderPreview(){
 const root=$("contest-preview");if(!root)return;root.replaceChildren();
 const now=ist(),upcoming=comps.filter(c=>c.deadline&&c.deadline>=now);
 const items=upcoming.filter(c=>c.series!=="SemEval 2027").map(c=>({c,when:c.registrationDeadline&&c.registrationDeadline>=now&&c.registrationDeadline<c.deadline?c.registrationDeadline:c.deadline}));
 const sem=upcoming.filter(c=>c.series==="SemEval 2027");
 if(sem.length)items.push({family:sem,when:sem.map(c=>c.registrationDeadline||c.deadline).sort()[0]});
 items.sort((a,b)=>a.when.localeCompare(b.when));
 for(const item of items.slice(0,6)){
  const tr=el("tr",null,root);
  el("td",fdate(item.when),tr,"date");
  const title=el("td",null,tr);
  if(item.family){
   link("SemEval 2027 · 12 task family","./semeval.html",title);
   el("td","Choose individual shared task and verify its registration gate",tr);
   el("td","System-description papers; separate submission (tentative Feb)",tr);
   link("Task directory","./semeval.html",el("td",null,tr));
  }else{
   const c=item.c;link(c.title,c.source,title);
   el("td",c.stage||"Challenge",tr);
   el("td",c.paperRouteStatus||"No verified paper route",tr);
   link("Details","./competitions.html",el("td",null,tr));
  }
 }
}
const slate=[
 ["legacy-wsdm-2027","IR / short research paper · verify exact short-track CFP and evidence"],
 ["legacy-pakdd-2027","Applied data science · retrieval / entity resolution with practical validation"],
 ["legacy-icde-2027-demonstrations","System demo · live retrieval or data tooling"],
 ["coling27-industry","NLP industry · measured real-world system pathway"],
 ["naacl27-demo","NLP demo · working prototype, video, repeatable evaluation"],
 ["rss27-main","Robotics/physical AI · two-stage, high scientific burden"],
 ["eacl27-workshop-chomps","LLM hallucination · direct workshop route"],
 ["eacl27-workshop-linda","Downstream NLP · direct workshop route"],
 ["ijcai27-ai4science","AI4Science · Jan abstract + Jan full paper; special CFP needs verification"],
 ["naacl27-student-workshop","Student research · independent study or thesis research"]
];
function renderSlate(){
 const root=$("slate-rows");if(!root)return;root.replaceChildren();const today=ist();
 slate.forEach(([id,fit])=>{
 const o=opps.find(o=>o.id===id);if(!o)return;
 const s=chooseStage(o,today),tr=el("tr",null,root),tc=el("td",null,tr);
 link(o.venue+" · "+o.track,o.source,tc);
 el("td",s?fdate(s.date)+" · "+(s.label||"Submission"):"Closed / TBA",tr);
 el("td",fit,tr);
 const gate=gateInfo(o,today);el("td",gate.text,tr);
 const td=el("td",null,tr),selectedNow=selected(effectiveState(o)),b=el("button",selectedNow?"Remove target":"Add target",td);
 b.type="button";b.setAttribute("aria-label",(selectedNow?"Remove":"Add")+" target "+o.venue+" "+o.track);
 b.addEventListener("click",()=>storePlanningStatus(o,selectedNow?"watch":"target"));
 });
}
function renderCompetition(){
 const root=$("competition-rows");if(!root)return;root.replaceChildren();
 const today=ist(),view=$("comp-window").value,field=$("comp-field").value,paper=$("comp-paper").value,q=$("comp-query").value.toLowerCase().trim();
 const filtered=comps.filter(c=>{
  if(view==="90"&&(!c.deadline||c.deadline<today||c.deadline>addDays(today,90)))return false;
  if(view==="past"&&(!c.deadline||c.deadline>=today))return false;
  if(view!=="90"&&view!=="past"&&view!=="all"&&(!c.deadline||c.deadline<today))return false;
  if(field!=="all"&&!(c.field||"").toLowerCase().includes(field))return false;
  if(paper==="yes"&&/No confirmed|No automatic/i.test(c.paperRouteStatus||""))return false;
  if(q&&!(c.title+" "+c.series+" "+c.field+" "+c.notes).toLowerCase().includes(q))return false;
  return true;
 });
 const sems=filtered.filter(x=>x.series==="SemEval 2027");
 const rows=filtered.filter(x=>x.series!=="SemEval 2027").map(c=>({c,date:c.deadline||"9999"}));
 if(sems.length)rows.push({sems,date:sems.map(c=>c.registrationDeadline||c.deadline||"9999").sort()[0]});
 rows.sort((a,b)=>a.date.localeCompare(b.date));
 for(const item of rows){
  const tr=el("tr",null,root);
  if(item.sems){
   let td=el("td",null,tr);td.dataset.label="Challenge";link("SemEval 2027 · one workshop family","./semeval.html",td).className="track-name";
   el("span",sems.length+" matching of 12 independent shared tasks",td,"line");
   td=el("td",null,tr);td.dataset.label="Next cutoff";el("span","Task-specific",td,"date");el("span","Evaluation generally 10–31 Jan 2027; task cutoff can be earlier",td,"line");
   td=el("td","Select an individual task; follow its registration instructions",tr);td.dataset.label="What to submit";
   el("span","CLaS registration 31 Dec 2026 applies only to CLaS",td,"line");
   td=el("td",null,tr);td.dataset.label="Paper pathway";el("div","System-description paper",td,"row-strong");el("span","Separate Feb 2027 submission · exact date unverified",td,"line");
   td=el("td",null,tr);td.dataset.label="My plan";link("Browse 12 tasks","./semeval.html",td);
   td=el("td",null,tr);td.dataset.label="Source";link("SemEval official hub","https://semeval.github.io/SemEval2027/",td);
   continue;
  }
  const c=item.c,state=cboard[c.id]||"";tr.className=state==="skip"?"skip":selected(state)?"target":"";
  let td=el("td",null,tr);td.dataset.label="Challenge";link(c.title,c.source,td).className="track-name";el("span",c.series+" · "+c.field,td,"line");
  td=el("td",null,tr);td.dataset.label="Next cutoff";
  const next=c.registrationDeadline&&c.registrationDeadline>=today&&(!c.deadline||c.registrationDeadline<c.deadline)?c.registrationDeadline:c.deadline;
  el("div",fdate(next),td,"date");el("span",next===c.registrationDeadline?"Registration":"Challenge submission",td,"line");
  if(c.deadlineAccuracy)el("span",c.deadlineAccuracy,td,"line");
  td=el("td",c.stage||"Challenge submission",tr);td.dataset.label="What to submit";
  if(c.registrationDeadline)el("span","Register by "+fdate(c.registrationDeadline),td,"line");
  if(c.notes){const d=el("details",null,td);el("summary","Requirements",d);el("p",c.notes,d,"line");}
  td=el("td",null,tr);td.dataset.label="Paper pathway";el("div",c.paperRoute||"Not verified",td,"row-strong");
  el("span",c.paperRouteStatus||"Check organizer",td,"line");if(c.paperDue)el("span","Paper / report: "+fdate(c.paperDue),td,"line");
  td=el("td",null,tr);td.dataset.label="My plan";const select=el("select",null,td,"status");
  [["","Unreviewed"],["watch","Watch"],["target","Target"],["drafting","Working"],["submitted","Submitted"],["skip","Strike through"]].forEach(([value,label])=>{const opt=el("option",label,select);opt.value=value;});
  select.value=state;select.setAttribute("aria-label","Status for "+c.title);
  select.addEventListener("change",()=>{cboard[c.id]=select.value;saveComp();renderCompetition();});
  td=el("td",null,tr);td.dataset.label="Source";link("Organizer CFP",c.source,td);
 }
 if(!rows.length){const tr=el("tr",null,root),td=el("td","No matching entries; adjust search or deadline window.",tr);td.colSpan=6;}
 if($("competition-count"))$("competition-count").textContent=rows.length+" programmes visible · "+filtered.length+" underlying tasks/challenges";
 if($("comp-targets"))$("comp-targets").textContent=comps.filter(c=>selected(cboard[c.id])).length;
 if($("comp-challenges"))$("comp-challenges").textContent=comps.filter(c=>c.series!=="SemEval 2027").length;
 if($("comp-families"))$("comp-families").textContent=String(new Set(comps.filter(c=>c.series==="SemEval 2027").map(c=>c.series)).size);
}
function attach(){
 if($("conference-rows")){
  ["window","area","kind","search","shortlisted","focus-pool"].forEach(id=>{const x=$(id);x.addEventListener(id==="search"?"input":"change",()=>{viewLimit=25;renderBoard();});});
  if($("show-more"))$("show-more").addEventListener("click",()=>{viewLimit+=25;renderBoard();});
  $("review-button").addEventListener("click",()=>{board._lastReviewed=ist();save();showReview();});
  $("copy-plan").addEventListener("click",async()=>{
   const detail=Object.entries(old).filter(([id,v])=>v&&opps.some(o=>o.id===id)).sort(([a],[b])=>a.localeCompare(b));
   const planning=Object.entries(board).filter(([id,v])=>id!=="_lastReviewed"&&v&&(v.state||v.abstractFiled)&&opps.some(o=>o.id===id)).sort(([a],[b])=>a.localeCompare(b));
   const lines=["CS_CONF_PRIVATE_DECISIONS v1","Task: cs-confs-daily-deadline-review-20261028-001","Generated: "+new Date().toISOString(),"Private status export; do not publish in the public repo.","Detailed submission decisions:"];
   detail.forEach(([id,v])=>lines.push("- "+id+" | "+v));
   lines.push("Main planner states:");
   planning.forEach(([id,v])=>lines.push("- "+id+" | plan="+(v.state||"")+(v.abstractFiled?" | abstractFiled=true":"")));
   if(detail.length+planning.length===0)lines.push("(No local changes)");
   const text=lines.join("\n");
   try{await navigator.clipboard.writeText(text);$("copy-notice").textContent="Copied all local decisions; paste into your private GitHub issue."; }
   catch(_){$("copy-notice").textContent="Clipboard unavailable; enable browser clipboard permission."; }
  });

  renderBoard();renderRates();showReview();
 }
 if($("competition-rows")){["comp-window","comp-field","comp-paper","comp-query"].forEach(id=>$(id).addEventListener(id==="comp-query"?"input":"change",renderCompetition));renderCompetition();}
}
function showReview(){
 if(!$("review-due"))return;
 const date=typeof board._lastReviewed==="string"?board._lastReviewed:null;
 const due=addDays(date||"2026-11-02",30);
 $("review-due").textContent=(date?"Last manually marked "+fdate(date)+" · next local review "+fdate(due):"First 30-day review due "+fdate(due)+" · not yet manually marked on this device")+". Scheduled ChatGPT review is separate from this browser marker.";
}
async function init(){
 try{
  const [o,c,a]=await Promise.all(["./opportunities.json","./competitions.json","./acceptance.json"].map(x=>fetch(x,{cache:"no-store"}).then(r=>{if(!r.ok)throw new Error(x+": HTTP "+r.status);return r.json();})));
  opps=o.opportunities||[];comps=c.competitions||[];rates=a.records||[];
  renderWatch();
  if($("audit-date"))$("audit-date").textContent="Competition/priority sources checked "+c.checkedAt+"; existing track catalog last overall audit "+o.checkedAt+". Official organizer pages override these snapshots.";
  attach();
 }catch(e){const z=$("load-message");if(z)z.textContent="Could not load the tracked sources: "+e.message+". Use official CFP links or reload the page."; }
}
init();
})();
