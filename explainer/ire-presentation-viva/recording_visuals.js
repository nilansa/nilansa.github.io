(function(){
const paperVisual = window.renderVisual;
/** COEOUS visual assets. ES module; functions return self-contained SVG markup. */
const svg = (label, content) => `<svg class="coeus-viz" viewBox="0 0 1200 600" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${content}</svg>`;
const text = (x,y,s,cls='body',anchor='start') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${s}</text>`;
const line = (x1,y1,x2,y2,cls='rule') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
const box = (x,y,w,h,cls='box') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" class="${cls}"/>`;
const arrow = (x,y) => `<path d="M${x} ${y}h38m-11 -10 11 10-11 10" class="arrow"/>`;

function pipeline() {
  const nodes = [
    ['01 · ENCODE','Query text → vector','Frozen Qwen embedder'],
    ['02 · RETRIEVE','Full corpus → top 50','Frozen document index'],
    ['03 · SELECT','50 candidates → 10','Dense or coverage'],
    ['04 · SCORE','10 pairs → P(yes)','Frozen Qwen reranker'],
    ['05 · ADAPT','Fit query residual','300 Adam steps'],
    ['06 · SEARCH','Updated query → top 10','Full corpus searched again']
  ];
  let s=text(35,52,'ONE QUERY · ONE FEEDBACK ROUND','eyebrow');
  nodes.forEach((n,i)=>{const col=i%3,row=Math.floor(i/3),x=35+col*390,y=90+row*220;s+=box(x,y,340,150)+text(x+22,y+36,n[0],'small blue')+text(x+22,y+78,n[1],'node')+text(x+22,y+115,n[2],'small');if(col<2)s+=arrow(x+347,y+75);});
  s+=`<path d="M1155 165 H1180 V275 H15 V385 H35 M25 375 L35 385 L25 395" class="arrow"/>`;
  s+=text(35,557,'Only an external query vector changes; encoder, reranker and document vectors stay fixed.','caption');
  return svg('Query encoding, full-corpus retrieval, selection, teacher scoring, query-vector update and full-corpus re-search.',s);
}

function probabilities() {
  const target=[.6,.3,.1], before=[.2,.3,.5], after=[.5,.3,.2];
  let s=text(35,50,'TOY EXAMPLE · THREE CANDIDATES','eyebrow')+text(35,94,'Teacher stays fixed; student moves closer.','heading');
  const panel=(x,title,student)=>{let p=text(x,150,title,'node')+line(x,440,x+440,440);for(let i=0;i<3;i++){const bx=x+45+i*140; [[target[i],'bar-blue'],[student[i],'bar-brown']].forEach(([v,c],j)=>{let xx=bx+j*42,h=v*330;p+=`<rect x="${xx}" y="${440-h}" width="32" height="${h}" class="${c}"/>`+text(xx+16,430-h,v.toFixed(1),'small','middle');});p+=text(bx+37,480,['A','B','C'][i],'body','middle');}return p;};
  s+=panel(35,'Before',before)+panel(630,'After',after);
  s+=`<rect x="36" y="530" width="18" height="18" class="bar-blue"/>`+text(65,546,'Teacher probability','small')+`<rect x="325" y="530" width="18" height="18" class="bar-brown"/>`+text(355,546,'Student probability','small');
  s+=text(660,546,'Each probability list sums to 1.','small');
  return svg('Illustrative softmax probabilities for three candidates. Teacher .6, .3, .1. Student before .2, .3, .5 and after .5, .3, .2.',s);
}

function residual() {
  let s=text(35,48,'TOY GEOMETRY · NOT MEASURED','eyebrow')+text(35,92,'Learn a correction in query-vector space.','heading');
  s+=line(160,460,1020,460)+line(160,460,160,135);
  s+=`<path d="M160 460 L670 320 M652 317 L670 320 L656 333" class="vector-ink"/><path d="M670 320 L800 220 M782 225 L800 220 L793 237" class="vector-brown"/><path d="M160 460 L800 220 M782 219 L800 220 L787 234" class="vector-blue"/>`;
  s+=text(340,442,'original query x','body')+text(715,278,'half correction 0.5v','body brown')+text(355,285,'updated direction','body blue');
  s+=text(35,530,'Training reduces teacher–student KL plus a penalty on correction size.','caption');
  s+=text(35,563,'At deployment: normalize x + 0.5v; the picture shows direction only.','caption');
  return svg('Illustrative query vector and correction: the original query x plus half the residual v gives the updated direction. This is a conceptual sketch, not measured geometry.',s);
}

function coverage() {
  const rows=[['A','✓','✓','—','—'],['B','✓','—','✓','—'],['C','—','—','✓','✓']];
  let s=text(35,48,'TOY EXAMPLE · FIXED CANDIDATE POOL','eyebrow')+text(35,90,'Greedy selection rewards newly covered query tokens.','heading');
  const xs=[430,600,770,940];
  ['token 1','token 2','token 3','token 4'].forEach((a,i)=>s+=text(xs[i],165,a,'small','middle'));
  rows.forEach((r,i)=>{let y=215+i*85;s+=text(45,y+27,'Candidate '+r[0],'body');for(let j=0;j<4;j++){s+=box(xs[j]-42,y-5,84,52,r[j+1]==='✓'?'cell-blue':'cell-empty')+text(xs[j],y+30,r[j+1],'body','middle');}});
  s+=text(35,518,'First A covers tokens 1–2; then C adds tokens 3–4.','caption');
  s+=text(35,555,'Real selection uses BERT token similarities and marginal coverage, not binary matches.','caption');
  return svg('Illustration of greedy token coverage: candidate A covers tokens 1 and 2; candidate C then adds tokens 3 and 4. Binary matches are schematic.',s);
}

function fiqa() {
  const rows=[['Raw dense',.4618,'bar-gray'],['Teacher rerank · dense 10',.4856,'bar-brown'],['Teacher rerank · coverage 10',.3857,'bar-brown'],['Standard TTT · dense 10',.5060,'bar-blue'],['Coverage TTT · greedy',.4807,'bar-blue'],['Independent MaxSim TTT',.4881,'bar-blue'],['Rank-matched TTT · mean of 3',.4761,'bar-blue']];
  let s=text(35,43,'FIQA · 200 PREVIOUSLY EXPOSED QUERIES · EXPLORATORY','eyebrow')+text(35,79,'nDCG@10 · higher is better','heading');
  const x=465, width=615, scale=width/.6;
  [0,.2,.4,.6].forEach(v=>{let xx=x+v*scale;s+=line(xx,104,xx,452,'grid')+text(xx,479,v.toFixed(1),'small','middle');});
  rows.forEach(([name,v,c],i)=>{const y=112+i*48;s+=text(x-22,y+24,name,'small','end')+`<rect x="${x}" y="${y}" width="${v*scale}" height="27" class="${c}"/>`+text(x+v*scale+12,y+23,v.toFixed(4),'small');});
  s+=text(35,525,'Coverage − standard TTT: −0.0253 · paired 95% CI [−0.0438, −0.0070]','caption');
  s+=text(35,558,'PARK · direct rerank returns only the selected ten; TTT re-searches all 57,638 documents.','caption');
  return svg('FiQA exploratory nDCG at 10: raw .4618; teacher rerank dense .4856; rerank coverage .3857; standard TTT .5060; coverage TTT .4807; independent MaxSim TTT .4881; rank matched .4761. Coverage minus standard is negative, confidence interval excludes zero. Park.',s);
}

function scopes() {
  const cols=[['GLOBAL','One residual across tasks','Shared across queries'],['TASK','One residual per task','Shared within a task'],['QUERY','One residual per query','Used for that query only']];
  let s=text(35,48,'THREE SCOPES · DIFFERENT SHARING','eyebrow')+text(35,90,'What gets reused?','heading');
  cols.forEach((a,i)=>{const x=35+i*390;s+=box(x,125,350,225)+text(x+22,166,a[0],'node blue')+line(x+22,187,x+328,187)+text(x+22,232,a[1],'body')+text(x+22,275,a[2],'small');});
  s+=text(35,418,'Local query-wise experiment','node')+text(35,461,'Top 50 → 10 teacher scores → 300 Adam steps → full-corpus re-search','caption');
  s+=text(35,507,'α = 0.5: correction weight for one rewarded query; no model weights are trained.','caption');
  s+=text(35,550,'Paper budgets vary by scope; these local settings are not universal paper budgets.','caption');
  return svg('Global residual shared across tasks, task residual shared within a task, and query residual private to one query. Local query-wise experiment uses fifty candidates, ten teacher scores, three hundred steps and full-corpus re-search.',s);
}

function fiqaCI() {
 let s=text(35,50,'FIQA-200 · PAIRED UNCERTAINTY','eyebrow')+text(35,110,'Coverage TTT − standard TTT = −0.0253','heading');
 const zero=980,scale=9500;let ticks=[-.05,-.04,-.03,-.02,-.01,0];
 ticks.forEach(v=>{let x=zero+v*scale;s+=line(x,175,x,404,v===0?'arrow':'grid')+text(x,440,v.toFixed(2),'small','middle');});
 let l=zero-.0438*scale,r=zero-.007*scale,m=zero-.0253*scale;
 s+=line(l,295,r,295,'arrow')+line(l,270,l,320,'arrow')+line(r,270,r,320,'arrow')+`<circle cx="${m}" cy="295" r="15" class="bar-blue"/>`;
 s+=text(m,250,'−0.0253','node','middle');
 s+=text(35,512,'95% paired bootstrap interval [−0.0438, −0.0070]','caption');
 s+=text(35,558,'Entire interval below zero: this selected FiQA method is PARK, not a positive result.','caption');
 return svg('FiQA coverage minus standard TTT nDCG at ten is minus 0.0253 with 95 percent interval minus 0.0438 to minus 0.0070.',s);
}
function controlsH8() {
 let s=text(35,48,'CONTROL EVIDENCE · NOT CROSS-DATASET COMPARABLE','eyebrow');
 s+=text(35,100,'FiQA-200 nDCG@10','heading');
 const a=[['Standard TTT',.5060],['Independent MaxSim',.4881],['Rank-matched',.4761]];
 a.forEach(([n,v],i)=>{const y=145+i*74;s+=text(35,y+27,n,'body')+`<rect x="365" y="${y+2}" width="${(v/.6)*620}" height="30" class="bar-blue"/>`+text(1007,y+26,v.toFixed(4),'small');});
 s+=line(35,415,1160,415,'grid');
 s+=text(35,468,'HotpotQA H8 · pooled descriptive nDCG@10','node');
 s+=text(35,514,'Standard 0.7346  →  Coverage 0.7496','body');
 s+=text(35,562,'DEV400 +0.0103 · 95% CI [−0.0041, +0.0251] includes zero · PARK','caption');
 return svg('FiQA controls and separate HotpotQA descriptive comparison with a development confidence interval spanning zero.',s);
}

function cards(s) {
  const safe = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  return '<div class="record-cards">' + (s.items || []).map((item,i) => '<div class="record-card"><span class="record-number">0'+(i+1)+'</span><p>'+safe(item)+'</p></div>').join('') + '</div>';
}
function mobileVisual(s) {
  if (s.number === 6) {
    const labels=['A','B','C'], teacher=[.6,.3,.1], before=[.2,.3,.5], after=[.5,.3,.2];
    const panel=(title,values)=>'<div class="m-prob-panel"><b>'+title+'</b>'+labels.map((label,i)=>'<div class="m-prob-row"><span>'+label+'</span><span class="m-pair"><i class="m-blue" style="width:'+teacher[i]*100+'%"></i><i class="m-brown" style="width:'+values[i]*100+'%"></i></span><span>'+teacher[i].toFixed(1)+' / '+values[i].toFixed(1)+'</span></div>').join('')+'</div>';
    return '<div class="m-prob">'+panel('Before',before)+panel('After',after)+'</div><div class="m-caption"><span class="m-dot blue"></span>Teacher <span class="m-dot brown"></span>Student · toy probabilities</div>';
  }
  if (s.number === 7) return '<svg class="m-vector" viewBox="0 0 800 150" role="img" aria-label="Original query x plus half the correction v gives the updated direction; normalize before search."><path d="M40 125 L415 88 M398 82 L415 88 L400 97" stroke="#151515"/><path d="M415 88 L550 35 M532 36 L550 35 L539 50" stroke="#875e3c"/><path d="M40 125 L550 35 M533 33 L550 35 L536 47" stroke="#1e3af5"/><text x="95" y="148">original query x</text><text x="560" y="65">half correction 0.5v</text><text x="190" y="70">updated direction</text></svg><div class="m-caption">Normalize x + 0.5v before full-corpus search · illustration</div>';
  if (s.number === 9) return '<div class="m-coverage" role="img" aria-label="Toy coverage. Candidate A covers tokens one and two. Candidate C adds tokens three and four."><div></div><b>Token 1</b><b>Token 2</b><b>Token 3</b><b>Token 4</b><strong>Candidate A</strong><i>✓</i><i>✓</i><i>—</i><i>—</i><strong>Candidate B</strong><i>✓</i><i>—</i><i>✓</i><i>—</i><strong>Candidate C</strong><i>—</i><i>—</i><i>✓</i><i>✓</i></div><div class="m-caption">A covers tokens 1–2; C adds 3–4 · toy example</div>';
  if (s.number === 10) {
    const rows=[['Raw dense',.4618],['Standard TTT',.5060],['Coverage TTT',.4807]];
    return '<div class="m-result" aria-label="FiQA exploratory nDCG at ten: raw 0.4618, standard TTT 0.5060, coverage TTT 0.4807.">'+rows.map(([name,v])=>'<div><b>'+name+'</b><span><i style="width:'+(v/.6*100)+'%"></i></span><strong>'+v.toFixed(4)+'</strong></div>').join('')+'</div><div class="m-caption">nDCG@10 · exploratory · higher is better</div>';
  }
  return cards(s);
}
window.renderVisual = function(s) {
  const diagrams = {5:scopes,6:probabilities,7:residual,8:pipeline,9:coverage,10:fiqa,11:fiqaCI,12:controlsH8};
  const mapped={1:"cover",2:"bottleneck",3:"tour-loop",4:"refit-loop"};
  if(mapped[s.number])return paperVisual({...s,kind:mapped[s.number]});
  if (!diagrams[s.number]) return cards(s);
  let graphic = diagrams[s.number]();
  const formulas = {
    6: 'p<sub>T</sub>=softmax(r/0.02) &nbsp; p<sub>S</sub>(v)=softmax(sim(unit(x+v),z)/0.05) &nbsp; L=KL(p<sub>T</sub>∥p<sub>S</sub>(v))+0.3‖v‖²',
    7: 'g<sub>t</sub>=∇<sub>v</sub>L(v<sub>t</sub>) &nbsp; m<sub>t</sub>=β₁m<sub>t−1</sub>+(1−β₁)g<sub>t</sub> &nbsp; v<sub>t+1</sub>=v<sub>t</sub>−ηm̂<sub>t</sub>/(√û<sub>t</sub>+ε)',
    9: 'h<sub>j</sub>(d)=max<sub>t∈d</sub> sim(u<sub>j</sub>,t) &nbsp; F<sub>q</sub>(S)=∑<sub>j</sub> max(0,max<sub>d∈S</sub> h<sub>j</sub>(d))'
  };
  const notes = {
    6:'Teacher and student share ten candidates. Only the external residual is optimized; teacher scores are fixed.',
    7:'Adam second moment u follows uₜ=β₂uₜ₋₁+(1−β₂)gₜ²; 300 steps at η=.01. Search unit(x+0.5v*).',
    9:'Greedy coverage selects the greatest marginal gain F(S∪{d})−F(S). Frozen BERT tokens; not full DISCo indexing.'
  };
  if (formulas[s.number]) graphic+='<div class="math-foot">'+formulas[s.number]+'<small>'+notes[s.number]+'</small></div>';
  return '<div class="record-diagram">'+graphic+'</div><div class="record-mobile">'+mobileVisual(s)+'</div>';
};

})();
