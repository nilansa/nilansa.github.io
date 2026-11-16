(() => {
  'use strict';
  const BLUE = '#1E3AF5', INK = '#151515', GRAY = '#72736F', PALE = '#D6D7D2', PAPER = '#FAFAF8';
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const t = (x,y,s,size=24,fill=INK,weight=400,anchor='start',extra='') => `<text x="${x}" y="${y}" fill="${fill}" font-size="${size}" font-weight="${weight}" text-anchor="${anchor}" ${extra}>${esc(s)}</text>`;
  const line = (x1,y1,x2,y2,color=PALE,width=1,extra='') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
  const circle = (x,y,r=7,fill=PALE,extra='') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" ${extra}/>`;
  const rect = (x,y,w,h,fill=PAPER,stroke=PALE,sw=1,extra='') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" ${extra}/>`;
  const arr = (id,x1,y1,x2,y2,color=BLUE,width=2) => line(x1,y1,x2,y2,color,width,`marker-end="url(#a-${id})"`);
  const svg = (id,body,desc,h=360) => `<svg class="diagram" viewBox="0 0 1200 ${h}" role="img" aria-label="${esc(desc)}"><title>${esc(desc)}</title><defs><marker id="a-${id}" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L9,4.5 L0,9" fill="${BLUE}"/></marker></defs>${body}</svg>`;
  const brief = s => `<div class="visual-brief">${s}</div>`;
  const wrap = (kind,body,mobile='') => `<div class="viz viz-${kind}">${body}${mobile ? brief(mobile) : ''}</div>`;
  const note = s => `<div class="visual-caption">${s}</div>`;
  const math = s => `<div class="mathline">${s}</div>`;
  const smallTable = (headers,rows) => `<table class="compact-table"><thead><tr>${headers.map(x=>`<th>${esc(x)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(x=>`<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;

  function cover(s) {
    let b = '';
    [[650,70],[705,95],[760,45],[790,125],[840,90],[900,70],[950,130],[1010,80],[1060,140],[1100,60],[710,190],[815,210],[940,230],[1050,240],[1140,200],[660,285],[790,310],[890,290],[1020,310]].forEach(([x,y],i)=>{b+=circle(x,y,i%4===0?8:5,i%4===0?INK:PALE);});
    b += `<ellipse cx="785" cy="160" rx="130" ry="110" fill="none" stroke="${PALE}" stroke-width="2" stroke-dasharray="6 8"/>`;
    b += `<ellipse cx="985" cy="205" rx="150" ry="120" fill="none" stroke="${BLUE}" stroke-width="2"/>`;
    b += circle(740,175,11,INK)+circle(945,195,11,BLUE)+arr(s.id,755,175,928,194)+t(815,162,'+ v',36,BLUE,600)+t(708,214,'q',23,INK,500)+t(966,222,'q̃',23,BLUE,500);
    b += t(0,90,'A small vector.',44,INK,500)+t(0,145,'A different search.',44,BLUE,500)+t(0,215,'Nilanjan Sarkar · Raman Rayaprolu',23)+t(0,253,'IIIT Hyderabad',22,GRAY)+t(0,305,'IRE Project · 16 November 2026',20,GRAY);
    return wrap('cover',svg(s.id,b,'Illustration: an external vector changes a query and its retrieved neighborhood, with document vectors fixed.'),'<p><strong>A small vector. A different search.</strong></p><p>Nilanjan Sarkar · Raman Rayaprolu<br>IIIT Hyderabad</p>');
  }
  function origin(s) {
    let b='';
    const xs=[0,420,840];
    [['01','Select','Which pairs are worth scoring?'],['02','Learn','How should scores guide learning?'],['03','Spend','How much feedback can we afford?']].forEach((a,i)=>{
      b+=t(xs[i],70,a[0],62,BLUE,700)+line(xs[i],105,xs[i]+350,105,BLUE,2)+t(xs[i],170,a[1],40,INK,600)+t(xs[i],220,a[2],22,GRAY);
    });
    b+=line(0,290,1200,290,PALE)+t(0,337,'Our scope',20,GRAY)+t(185,337,'Useful adaptation after deployment, with model weights fixed.',29,BLUE,500);
    return wrap('origin',svg(s.id,b,'Three Microsoft research questions: data selection, learning loss, and computational efficiency.'),'<ol><li><strong>Select</strong> which pairs deserve scoring.</li><li><strong>Learn</strong> how scores guide adaptation.</li><li><strong>Spend</strong> feedback efficiently.</li></ol>');
  }
  function access(s) {
    let b='';
    [['Embedding model',0,'Returns a vector'],['Reranker',420,'Returns relevance scores'],['Document index',840,'Accepts a new search vector']].forEach(([label,x,output])=>{
      b+=rect(x,20,355,140,PAPER,PALE,1.5)+t(x+24,57,'FROZEN',17,GRAY,600)+t(x+24,101,label,30,INK,600)+t(x+24,138,output,19,GRAY);
    });
    b+=arr(s.id,180,177,180,245)+arr(s.id,600,177,600,245)+arr(s.id,1017,245,1017,177);
    b+=rect(0,265,1195,80,BLUE,BLUE)+t(27,315,'Editable external state',28,PAPER,600)+t(610,315,'query vector  q     or residual  v',31,PAPER,400);
    return wrap('access',svg(s.id,b,'Frozen embedding and reranker models expose outputs. The external vector is editable and searches the fixed index.'),'<p><strong>Frozen:</strong> encoder weights, reranker weights, document embeddings.</p><p><strong>Available:</strong> vectors, relevance scores, vector search.</p><p><strong>Editable:</strong> the query vector or an external residual.</p>');
  }
  function bottleneck(s) {
    let b=rect(0,25,535,275,PAPER,PALE)+t(20,60,'Full document corpus',23,GRAY);
    const pts=[[50,110],[120,100],[175,140],[245,95],[310,130],[380,110],[450,140],[70,190],[150,220],[230,190],[290,230],[375,205],[460,235],[105,270],[325,280]];
    pts.forEach(([x,y],i)=>b+=circle(x,y,7,i<5?BLUE:PALE));
    b+=`<ellipse cx="185" cy="135" rx="150" ry="65" fill="none" stroke="${BLUE}" stroke-width="2"/>`;
    b+=rect(437,220,30,30,BLUE,BLUE)+t(415,278,'Relevant, but missed',22,BLUE,500,'end');
    b+=arr(s.id,525,140,670,140)+t(598,109,'top K',20,GRAY,400,'middle');
    b+=t(700,70,'Reranker',30,INK,600);
    [0,1,2,3].forEach(i=>{b+=rect(705,100+i*47,235,33,i===0?'#e7eaff':PAPER,PALE)+t(725,124+i*47,['candidate B','candidate A','candidate D','candidate C'][i],21);});
    b+=t(980,144,'Better',30,BLUE,500)+t(980,182,'order',30,BLUE,500)+t(980,224,'Same set',23,GRAY);
    b+=`<path d="M830 300 L830 345 L260 345 L260 305" fill="none" stroke="${BLUE}" stroke-width="2" marker-end="url(#a-${s.id})"/>`;
    b+=t(570,334,'Can feedback guide a second search?',21,BLUE,500,'middle');
    return wrap('bottleneck',svg(s.id,b,'A relevant document outside the retrieved set cannot be recovered by reranking that same set.'),'<p>The retriever selects a candidate set from the corpus.</p><p>The reranker can improve the order inside that set.</p><p><strong>A missed document needs a new search.</strong></p>');
  }
  function tourLoop(s) {
    let b='';
    const xs=[0,320,640,960], labels=['Retrieve','Score','Move q','Retrieve again'], subs=['Fixed document index','Cross-encoder feedback','Vector-only gradient step','A new candidate set'];
    xs.forEach((x,i)=>{b+=t(x,40,String(i+1).padStart(2,'0'),19,GRAY)+line(x,62,x+235,62,i===2?BLUE:PALE,2)+t(x,113,labels[i],30,i===2?BLUE:INK,600)+t(x,151,subs[i],18,GRAY);if(i<3)b+=arr(s.id,x+250,105,x+298,105);});
    b+=line(20,315,500,315,PALE)+line(20,315,20,197,PALE);
    [[75,235],[120,280],[160,215],[210,270],[290,225],[335,280],[395,210],[455,255]].forEach(([x,y],i)=>b+=circle(x,y,6,i>3?BLUE:PALE));
    b+=circle(125,300,9,INK)+circle(355,253,9,BLUE)+arr(s.id,139,296,341,256)+t(108,342,'q₀',24)+t(348,292,'q₁',24,BLUE);
    b+=`<path d="M1085 190 L1085 250 L705 250 L705 195" fill="none" stroke="${BLUE}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a-${s.id})"/>`;
    b+=t(690,296,'Repeat as configured',24,BLUE,500)+t(690,330,'Cached scores and early stopping reduce repeated work.',18,GRAY);
    return wrap('tour-loop',svg(s.id,b,'TOUR retrieves, scores candidates, takes a vector gradient step, and retrieves again. Document points remain fixed.'),'<ol><li>Retrieve with q₀.</li><li>Score candidates with the fixed teacher.</li><li>Take a gradient step on q.</li><li>Search the same full index with q₁.</li></ol>');
  }
  function hardSoft(s) {
    const panel=(x,label,hard)=>{
      let b=t(x,32,label,30,BLUE,600); const vals=[.6,.3,.1];
      vals.forEach((v,i)=>{const bx=x+40+i*130;b+=rect(bx,210-v*210,65,v*210,i===2&&hard?PALE:BLUE,'none')+t(bx+32,195-v*210,v.toFixed(2),20,GRAY,500,'middle')+t(bx+32,244,['A','B','C'][i],22,INK,500,'middle');});
      if(hard)b+=`<path d="M${x+30} 260 v14 h216 v-14" fill="none" stroke="${BLUE}" stroke-width="2"/>`+t(x+30,312,'A and B selected at example threshold 0.8',19,GRAY,400);
      else b+=t(x+200,302,'Keep all three probability weights',21,GRAY,400,'middle');
      return b;
    };
    const b=panel(30,'Hard · select a pseudo-positive set',true)+line(585,0,585,330,PALE)+panel(660,'Soft · match the distribution',false);
    return wrap('hard-soft',svg(s.id,b,'Illustrative teacher probabilities .6, .3, .1. Hard feedback selects a set; soft feedback preserves all probability weights.')+`<div class="formula-pair"><div>${math('L<sub>hard</sub> = −log ∑<sub>i ∈ A</sub> p<sup>S</sup><sub>i</sub>')}<span>Increase the selected set’s probability.</span></div><div>${math('L<sub>soft</sub> = D<sub>KL</sub>(p<sup>T</sup> ∥ p<sup>S</sup>)')}<span>Match the teacher’s graded preferences.</span></div></div>`, '<p>Teacher probabilities: A .60, B .30, C .10.</p><p><strong>Hard:</strong> select A+B at illustrative threshold .8.</p><p><strong>Soft:</strong> fit all three probability weights.</p>');
  }
  function tourChart(s) {
    const a=[57.9,64.4,65.6,66.2],b=[70.8,70.8,71.9,72.5], names=['Retrieve','Rerank','TOUR hard','TOUR soft'];
    let q=t(50,20,'Answer-containing passage accuracy (%)',20,GRAY);
    for(let tick=0;tick<=80;tick+=20){const y=300-tick*3;q+=line(65,y,940,y,PALE)+t(50,y+7,String(tick),18,GRAY,400,'end');}
    names.forEach((n,i)=>{const x=105+i*210;[a[i],b[i]].forEach((v,j)=>{const bx=x+j*70;q+=rect(bx,300-v*3,50,v*3,j?BLUE:'#9A9B96','none')+t(bx+25,290-v*3,v.toFixed(1),20,j?BLUE:INK,600,'middle');});q+=t(x+60,332,n,21,INK,500,'middle');});
    q+=rect(991,62,14,14,'#9A9B96','none')+t(1017,77,'Acc@20',19)+rect(991,102,14,14,BLUE,'none')+t(1017,117,'Acc@100',19);
    q+=t(990,204,'+1.7',56,BLUE,600)+t(991,240,'points at depth 100',20,GRAY)+t(991,274,'TOUR soft vs rerank',18,GRAY);
    return wrap('chart',svg(s.id,q,'Published TOUR Table 3. EntityQuestions DPR. Acc20 and Acc100 grouped bars with a zero baseline.')+note('Source: TOUR, Table 3 · DPR multi · EntityQuestions. Values are published, not our measurements.'),smallTable(['Method','Acc@20','Acc@100'],names.map((n,i)=>[n,a[i].toFixed(1),b[i].toFixed(1)])));
  }
  function refitLoop(s) {
    let b='';
    [[0,'Retrieve 100','From the full corpus'],[320,'Score once','Cache teacher outputs'],[640,'Update q','100 inexpensive steps'],[960,'Search again','Over the full corpus']].forEach(([x,label,sub],i)=>{
      b+=t(x,85,label,29,i===2?BLUE:INK,600)+t(x,125,sub,20,GRAY)+line(x,155,x+232,155,i===2?BLUE:PALE,2);
      if(i<3)b+=arr(s.id,x+245,89,x+300,89);
    });
    b+=`<path d="M650 192 C650 255 875 255 875 192" fill="none" stroke="${BLUE}" stroke-width="3" marker-end="url(#a-${s.id})"/>`+t(762,217,'same scores',21,BLUE,500,'middle');
    b+=t(0,275,'Expensive operation',19,GRAY)+t(0,319,'Teacher inference',29,INK,500)+t(500,275,'Cheap inner operation',19,GRAY)+t(500,319,'Vector optimization',29,BLUE,500);
    return wrap('refit-loop',svg(s.id,b,'ReFIT scores 100 candidates once, performs 100 query-vector updates on cached scores, then searches the corpus again.'),'<ol><li>Retrieve 100 documents.</li><li>Score each once.</li><li>Use cached scores for 100 vector steps.</li><li>Search the full index again.</li></ol>');
  }
  function klPlot(s,after=false) {
    const target=[.6,.3,.1],student=after?[.5,.3,.2]:[.2,.3,.5];
    let b=t(8,27,'Illustrative probabilities',20,GRAY);
    for(let tick=0;tick<=.6+1e-7;tick+=.2){const y=260-tick*280;b+=line(65,y,700,y,PALE)+t(50,y+6,tick.toFixed(1),17,GRAY,400,'end');}
    target.forEach((v,i)=>{const x=125+i*205;[[v,BLUE],[student[i],'#969791']].forEach(([val,c],j)=>{b+=rect(x+j*56,260-val*280,40,val*280,c,'none')+t(x+j*56+20,249-val*280,val.toFixed(2),19,c,600,'middle');});b+=t(x+47,295,['A','B','C'][i],23,INK,500,'middle');});
    b+=rect(790,84,14,14,BLUE,'none')+t(821,99,'Teacher · fixed',22)+rect(790,125,14,14,'#969791','none')+t(821,140,after?'Student · illustrative closer fit':'Student · before',22);
    const kl=target.reduce((a,v,i)=>a+v*Math.log(v/student[i]),0);
    b+=t(790,225,'KL = '+kl.toFixed(3),43,BLUE,500)+t(790,263,'Smaller means closer agreement.',20,GRAY);
    return svg(s.id,b,'Toy teacher-student probabilities. Blue is fixed teacher, gray is student; the closer-fit option is illustrative, not measured.',320);
  }
  function kl(s) {
    return wrap('kl',`<div class="kl-plot">${klPlot(s)}</div><div class="kl-toolbar">${math('min<sub>q</sub> D<sub>KL</sub>(p<sup>T</sup> ∥ p<sup>S</sup>(q)) = min<sub>q</sub> ∑<sub>i</sub> p<sup>T</sup><sub>i</sub> log <span class="fraction"><span>p<sup>T</sup><sub>i</sub></span><span>p<sup>S</sup><sub>i</sub>(q)</span></span>')}<button type="button" class="viz-button" data-v-action="kl" data-slide="${s.id}" aria-pressed="false">Show closer fit <span aria-hidden="true">→</span></button></div>`+note('Equivalent for a fixed teacher: maximize ∑ pᵀᵢ log pˢᵢ. All probabilities shown are illustrative.'),'<p>Teacher: .60, .30, .10.<br>Student before: .20, .30, .50.</p><p><strong>Minimize KL(teacher ∥ student).</strong><br>The teacher is fixed; only the query vector changes.</p>');
  }
  function refitChart(s) {
    const names=['Retrieve','Rerank','TOUR hard','TOUR soft','ReFIT'],vals=[66.8,67.6,68.4,68.1,69.2];
    let b=t(180,22,'Recall@100 (%) · zero baseline',19,GRAY);
    for(let tick=0;tick<=80;tick+=20){const x=190+tick*9;b+=line(x,45,x,308,PALE)+t(x,334,String(tick),17,GRAY,400,'middle');}
    names.forEach((n,i)=>{let y=55+i*49;b+=t(166,y+24,n,21,INK,i===4?600:400,'end')+rect(190,y,vals[i]*9,31,i===4?BLUE:'#AFB0AA','none')+t(206+vals[i]*9,y+24,vals[i].toFixed(1),22,i===4?BLUE:INK,600);});
    b+=t(1010,120,'+1.6',54,BLUE,600)+t(1010,155,'points',23,GRAY)+t(1010,195,'ReFIT vs rerank',19,GRAY);
    const timing=`<div class="timing-strip"><span class="timing-label">Separate GPU timing<br><small>Table 1 · milliseconds/query</small></span><span>Rerank 100 <strong>400</strong></span><span>Rerank 125 <strong>490</strong></span><span class="blue">ReFIT 100 <strong>470</strong></span></div>`;
    return wrap('chart',svg(s.id,b,'Published BEIR Recall100 from ReFIT Table6: 66.8,67.6,68.4,68.1,69.2. All bars start at zero.')+timing,smallTable(['Method','Recall@100'],names.map((n,i)=>[n,vals[i].toFixed(1)])));
  }
  function ourChart(s) {
    const names=['Raw Contriever','Rerank 125','ReFIT attempt'],ours=[37.8067,38.3450,37.8717],paper=[37.8,38.3,40.1];
    let b=t(55,22,'Recall@100 (%) · full SCIDOCS corpus',20,GRAY);
    for(let tick=0;tick<=50;tick+=10){const y=275-tick*4.3;b+=line(70,y,870,y,PALE)+t(54,y+6,String(tick),17,GRAY,400,'end');}
    names.forEach((n,i)=>{const x=135+i*253;b+=rect(x,275-ours[i]*4.3,70,ours[i]*4.3,BLUE,'none')+rect(x+82,275-paper[i]*4.3,70,paper[i]*4.3,'none',GRAY,2)+t(x+35,263-ours[i]*4.3,ours[i].toFixed(4),18,BLUE,600,'middle')+t(x+117,263-paper[i]*4.3,paper[i].toFixed(1),18,GRAY,500,'middle')+t(x+76,310,n,22,INK,500,'middle');});
    b+=rect(920,50,15,15,BLUE,'none')+t(947,65,'Our recorded run',20)+rect(920,88,15,15,'none',GRAY,2)+t(947,103,'Paper v2 reference',20);
    b+=t(918,175,'+0.065 pp',38,BLUE,600)+t(920,211,'ReFIT minus raw',20,GRAY)+t(920,253,'95% CI  −0.180 to +0.325',19,GRAY)+t(920,285,'The interval spans zero.',19,INK,500);
    return wrap('chart',svg(s.id,b,'SCIDOCS recorded run versus ReFIT paper v2 reference. The local ReFIT gain over raw has a confidence interval spanning zero.',335)+note('Published reference: ReFIT v2 Table 2. Local values and 5,000-resample paired interval: recorded completed-run reports. Raw predictions not recomputed in this pass.'),smallTable(['Method','Our run','Paper v2'],names.map((n,i)=>[n,ours[i].toFixed(4),paper[i].toFixed(1)]))+'<p><strong>ReFIT − raw: +0.065 pp</strong><br>95% CI [−0.180, +0.325].</p>');
  }
  function reuse(s) {
    let b=t(0,50,'Query-private state',27,GRAY,500)+t(0,245,'Shared external state',27,BLUE,600);
    b+=t(350,50,'query A',26)+arr(s.id,480,43,575,43)+rect(600,10,210,70,PAPER,GRAY)+t(705,55,'update qᴬ',27,INK,500,'middle')+arr(s.id,835,43,925,43)+t(950,50,'serve A',27)+t(600,123,'State stays with this query.',21,GRAY);
    b+=t(350,245,'feedback',26)+arr(s.id,480,238,575,238)+rect(600,205,210,70,BLUE,BLUE)+t(705,250,'learn v',29,PAPER,600,'middle');
    b+=arr(s.id,835,238,940,183)+arr(s.id,835,238,940,238)+arr(s.id,835,238,940,293)+t(965,189,'query B',24)+t(965,245,'query C',24)+t(965,300,'query D',24)+t(600,329,'Reuse without changing encoder weights.',21,BLUE);
    return wrap('reuse',svg(s.id,b,'TTT-Embed authors contrast a query-private update with a shared residual reused by other queries.'),'<p><strong>TOUR and ReFIT:</strong> adapt the current query.</p><p><strong>TTT-Embed:</strong> study whether learned external state can persist across queries.</p><p>Attributed to TTT-Embed Appendix §8; not a new head-to-head experiment.</p>');
  }
  function scopes(s) {
    let b='';
    const cols=[['Global','One vector per model','All tasks → all queries'],['Task','One vector per task','One task → its queries'],['Query','One vector per query','One query → itself']];
    cols.forEach((a,i)=>{const x=i*410;b+=t(x,37,a[0],34,BLUE,600)+line(x,65,x+365,65,BLUE,2)+t(x,105,a[1],23,INK,500)+t(x,144,a[2],21,GRAY);
      for(let j=0;j<4;j++)b+=circle(x+40+j*90,195,8,j<2?BLUE:INK);
      if(i===0){b+=rect(x+135,243,95,46,BLUE,BLUE)+t(x+183,274,'v',26,PAPER,600,'middle');for(let j=0;j<4;j++)b+=arr(s.id,x+40+j*90,211,x+181,235);}
      if(i===1){[0,1].forEach(k=>{b+=rect(x+50+k*180,243,95,46,BLUE,BLUE)+t(x+98+k*180,274,'v'+(k+1),26,PAPER,600,'middle');for(let j=0;j<2;j++)b+=arr(s.id,x+40+(k*2+j)*90,211,x+97+k*180,235);});}
      if(i===2){for(let j=0;j<4;j++)b+=arr(s.id,x+40+j*90,211,x+40+j*90,235)+rect(x+15+j*90,243,50,46,BLUE,BLUE)+t(x+40+j*90,274,'v'+(j+1),23,PAPER,600,'middle');}
    });
    return wrap('scopes',svg(s.id,b,'Global shares one vector across tasks, task has one vector per task, query has one vector for each rewarded query.'),smallTable(['Scope','Learned state','Reuse'],[['Global','One per embedding model','Across tasks'],['Task','One per task','Within task'],['Query','One per rewarded query','Current query only']])+'<p>Unrewarded queries can use shared states, but have no query-private correction.</p>');
  }
  function residual(s) {
    return wrap('residual',`<div class="residual-top"><div><div class="formula-label">Learn outside the model</div>${math('v<sub>g</sub><sup>*</sup> = arg min<sub>v</sub> <span class="sum">∑<sub>q ∈ F<sub>g</sub></sub></span> w<sub>q</sub> D<sub>KL</sub>(p<sub>q</sub><sup>T</sup> ∥ p<sub>q</sub><sup>S</sup>(v)) + λ‖v‖²')}<div class="formula-explainer"><span>Match the fixed teacher</span><span>Limit the correction</span></div></div></div><div class="residual-bottom"><div><div class="formula-label">Deploy the corrected query</div>${math('x̃<sub>q</sub> = unit(x<sub>q</sub> + <span class="math-blue">α<sub>g</sub>v<sub>g</sub><sup>*</sup></span>)')}<p>Search the same full document index.</p></div><div><div class="formula-label">Shrink with limited evidence</div>${math('α<sub>g</sub> = <span class="fraction"><span>n<sub>g</sub></span><span>n<sub>g</sub> + 1</span></span>')}<p>n = distinct rewarded queries<br>Query-private state: n = 1, α = 0.5</p></div></div>`+note('During fitting, pˢ uses unit(x + v). Deployment shrinkage is applied after learning. Teacher and student have their respective softmax temperatures.'));
  }
  function tttChart(s) {
    const vals=[1.23,6.36,8.36],base=[-.01,3.21,7.8],labs=['Global · b ≈ 0.01','Task · b = 10','Query · b = 100'];
    let b=t(60,22,'Gain over raw retrieval · ΔnDCG@10 × 100',20,GRAY);
    for(let tick=0;tick<=10;tick+=2){const y=285-tick*22;b+=line(70,y,1195,y,PALE)+t(55,y+6,String(tick),18,GRAY,400,'end');}
    labs.forEach((n,i)=>{const x=170+i*365;[[vals[i],BLUE],[base[i],'#AAABA5']].forEach(([v,c],j)=>{const bx=x+j*95;const hh=Math.max(Math.abs(v)*22,1);b+=rect(bx,v>=0?285-hh:285,70,hh,c,'none')+t(bx+35,v>=0?272-hh:270,v.toFixed(2),22,c===BLUE?BLUE:INK,600,'middle');});b+=t(x+82,326,n,23,INK,500,'middle');});
    return wrap('chart',`<div class="chart-legend"><span><i style="background:${BLUE}"></i>TTT-Embed at the shown scope</span><span><i style="background:#AAABA5"></i>Direct reranking</span></div>`+svg(s.id,b,'TTT-Embed Table1 gains at three budgets: global1.23 versus rerank−.01, task6.36 versus3.21, query8.36 versus7.8.')+note('Three table entries, not a continuous curve. b = scored pairs per workload query. The left budget is exactly 150/12,263 ≈ 0.0122.'),smallTable(['Budget / scope','TTT gain','Rerank gain'],labs.map((n,i)=>[n,vals[i].toFixed(2),base[i].toFixed(2)])));
  }
  function status(s) {
    const labels=['Raw retrieval','Task residual'], values=[.46722,.46313];
    let b=t(60,22,'Held-out nDCG@10 · full FiQA corpus',20,GRAY);
    [0,.2,.4,.6].forEach(tick=>{const y=290-tick*390;b+=line(70,y,680,y,PALE)+t(55,y+7,tick.toFixed(1),18,GRAY,400,'end');});
    values.forEach((v,i)=>{const x=165+i*260;b+=rect(x,290-v*390,130,v*390,i?BLUE:'#9A9B96','none')+t(x+65,278-v*390,v.toFixed(5),24,i?BLUE:INK,600,'middle')+t(x+65,325,labels[i],23,INK,500,'middle');});
    b+=t(740,87,'−0.00408',52,BLUE,600)+t(740,127,'reported held-out ΔnDCG@10',20,GRAY)+t(740,176,'95% CI  −0.01072 to +0.00262',21,GRAY)+t(740,217,'The interval spans zero.',25,INK,500)+t(740,263,'648 queries · 57,638 documents',21,GRAY)+t(740,298,'5-fold cross-fit · one exposed task',20,GRAY);
    return wrap('chart',svg(s.id,b,'Reported FiQA task-wise TTT-Embed pilot: raw nDCG10 .46722 and adapted .46313. Reported delta minus.00408 with interval minus.01072 to plus.00262. No reliable held-out gain.',340)+note('Ceous working report, §4. The source’s rounded endpoints and stated delta differ in the last digit. Raw predictions not recomputed here. Complementary selection remains untested.'),smallTable(['FiQA held-out result','nDCG@10'],labels.map((label,i)=>[label,values[i].toFixed(5)]))+'<p><strong>Reported Δ −0.00408</strong><br>95% CI [−0.01072, +0.00262]. One exposed task, 5-fold cross-fit. Complementary selection remains untested.</p>');
  }
  function coverage(s) {
    const rows=[[.9,.2,.1],[.85,.25,.1],[.2,.8,.1],[.1,.2,.9]];
    const matrix=`<div class="coverage-matrix"><div class="coverage-head"><span></span><span>Facet A</span><span>Facet B</span><span>Facet C</span></div>${rows.map((r,i)=>`<div class="coverage-row${i===0?' fixed':''}${i===3?' chosen':''}" data-doc="d${i+1}"><strong>d<sub>${i+1}</sub>${i===0?'<small>chosen</small>':''}</strong>${r.map(v=>`<span style="--strength:${v}">${v.toFixed(2)}</span>`).join('')}</div>`).join('')}</div>`;
    return wrap('coverage',`<div class="coverage-layout">${matrix}<div class="coverage-insight"><div class="formula-label">After choosing d₁, add</div><div class="coverage-buttons">${[2,3,4].map(i=>`<button class="viz-button" type="button" data-v-action="coverage" data-doc="d${i}" aria-pressed="${i===4}">d<sub>${i}</sub></button>`).join('')}</div><div class="coverage-gain">+0.80</div><p>marginal coverage</p><div class="coverage-total">1.20 → 2.00 total coverage</div><div class="coverage-explain">Document 4 contributes the missing facet C.</div></div></div>${math('F(S,Q) = ∑<sub>q ∈ Q</sub> max<sub>x ∈ ∪<sub>c ∈ S</sub>X<sub>c</sub></sub> qᵀx')}`+note('Original teaching example. The complete DISCo method uses contextual token vectors and a specialized index; these are not measured embedding scores.'));
  }
  function gradient(s) {
    let b='';
    const plane=(x,label,spread)=>{
      let z=t(x,25,label,26,INK,500)+line(x+10,235,x+420,235,PALE)+line(x+10,235,x+10,55,PALE);
      const ends=spread?[[160,-165],[300,-65],[340,-120],[90,-90]]:[[280,-80],[340,-95],[210,-63],[380,-105]];
      ends.forEach(([dx,dy],i)=>z+=arr(s.id,x+35,220,x+35+dx,220+dy,i===3?GRAY:BLUE,2));
      return z;
    };
    b+=plane(0,'Similar candidate directions',false)+plane(690,'Additional useful directions?',true)+t(510,144,'?',84,BLUE,500);
    return wrap('gradient',svg(s.id,b,'Illustrative geometry: scored candidate vectors supply the directions available to a simplified gradient. Complementarity may help, but is unproved.',270)+`<div class="gradient-formula">${math('∇<sub>u</sub>L = ∑<sub>i</sub> (p<sub>i</sub><sup>S</sup> − p<sub>i</sub><sup>T</sup>) z<sub>i</sub>')}<span>Simplified dot-product softmax; no normalization.</span></div>`+note('Mechanism hypothesis, not an empirical result. Actual ReFIT and TTT-Embed normalization changes the exact derivative.'),'<p><strong>Gradient = weighted combination of scored candidate vectors.</strong></p><p>Complementary candidates may add useful directions, or may add noise.</p><p>This simplified explanation does not prove a retrieval gain.</p>');
  }
  function protocol(s) {
    let b=rect(0,20,240,260,PAPER,BLUE,2)+t(22,65,'Full corpus',31,BLUE,600)+t(22,105,'Keep every document.',20,GRAY)+t(22,168,'100–200',43,INK,600)+t(22,201,'prespecified queries',20,GRAY)+t(22,248,'Pilot, not full replication',18,GRAY);
    b+=arr(s.id,255,105,337,105)+arr(s.id,255,235,337,235);
    b+=rect(355,50,260,90,PAPER,PALE)+t(375,88,'Base top-K',28,INK,600)+t(375,120,'Feedback candidates',18,GRAY);
    b+=rect(355,185,260,90,PAPER,BLUE,2)+t(375,222,'Coverage selection',26,BLUE,600)+t(375,254,'Same pair budget',18,GRAY);
    b+=arr(s.id,630,105,710,164)+arr(s.id,630,235,710,176)+rect(730,112,230,116,BLUE,BLUE)+t(845,156,'Same learner',28,PAPER,600,'middle')+t(845,194,'Same frozen vectors',18,PAPER,400,'middle');
    b+=arr(s.id,977,170,1038,170)+t(1063,135,'Full-index',23,INK,500)+t(1063,165,'search',23,INK,500)+t(1063,213,'Paired',21,GRAY)+t(1063,242,'evaluation',21,GRAY);
    b+=line(0,315,1200,315,PALE)+t(0,350,'Controls: broader pool + random selection',21,GRAY)+t(645,350,'Also count selection cost and extra searches.',21,BLUE,500);
    return wrap('protocol',svg(s.id,b,'Proposed matched-budget experiment: keep full corpus, compare candidate selectors, then use the same residual learner and paired evaluation.'),'<ol><li>Keep the full corpus; prespecify 100–200 queries.</li><li>Compare top-K and coverage selection at equal teacher budget.</li><li>Hold the residual learner fixed.</li><li>Evaluate paired quality, discovery and total cost.</li></ol>');
  }
  function closing(s) {
    let b='';
    [['Established','Scores can guide','a query update.'],['Measured here','SCIDOCS and FiQA:','no reliable gain here.'],['To test','Coverage-aware feedback','for residual learning.']].forEach((r,i)=>{const x=i*410;b+=t(x,32,r[0].toUpperCase(),17,i===2?BLUE:GRAY,600)+line(x,58,x+365,58,i===2?BLUE:PALE,2)+t(x,119,r[1],29,i===2?BLUE:INK,500)+t(x,162,r[2],29,i===2?BLUE:INK,500);});
    b+=t(0,289,'Can each judgment teach us more?',54,BLUE,600)+t(0,340,'Queos Labs · IRE Project',22,GRAY);
    return wrap('closing',svg(s.id,b,'Conclusion: query adaptation is established; the reported SCIDOCS and FiQA runs show no reliable gains; coverage-aware feedback is the hypothesis to test.'),'<p><strong>Established:</strong> scores can guide query adaptation.</p><p><strong>Measured here:</strong> no reliable gain in the reported SCIDOCS and FiQA runs.</p><p><strong>To test:</strong> coverage-aware feedback for residual learning.</p>');
  }
  const renderers={cover,origin,access,bottleneck,'tour-loop':tourLoop,'hard-soft':hardSoft,'tour-chart':tourChart,'refit-loop':refitLoop,kl,'refit-chart':refitChart,'our-chart':ourChart,reuse,scopes,residual,'ttt-chart':tttChart,status,coverage,gradient,protocol,closing};
  window.renderVisual = s => (renderers[s.kind]||closing)(s);
  document.addEventListener('click',event=>{
    const btn=event.target.closest('[data-v-action]'); if(!btn)return;
    const root=btn.closest('.viz');if(!root)return;
    if(btn.dataset.vAction==='kl'){
      const after=btn.getAttribute('aria-pressed')!=='true';
      const slide=window.DECK.slides.find(s=>s.id===btn.dataset.slide);
      root.querySelector('.kl-plot').innerHTML=klPlot(slide,after);
      btn.setAttribute('aria-pressed',String(after));btn.innerHTML=after?'Show initial student <span aria-hidden="true">↶</span>':'Show closer fit <span aria-hidden="true">→</span>';
    }
    if(btn.dataset.vAction==='coverage'){
      const id=btn.dataset.doc, cfg={d2:['+0.05','1.20 → 1.25 total coverage','Document 2 mostly repeats the coverage of document 1.'],d3:['+0.60','1.20 → 1.80 total coverage','Document 3 contributes the missing facet B.'],d4:['+0.80','1.20 → 2.00 total coverage','Document 4 contributes the missing facet C.']}[id];
      root.querySelectorAll('[data-v-action="coverage"]').forEach(x=>x.setAttribute('aria-pressed',String(x===btn)));
      root.querySelectorAll('.coverage-row').forEach(x=>x.classList.toggle('chosen',x.dataset.doc===id));
      root.querySelector('.coverage-gain').textContent=cfg[0];root.querySelector('.coverage-total').textContent=cfg[1];root.querySelector('.coverage-explain').textContent=cfg[2];
    }
  });
  const style=document.createElement('style');style.textContent=`
    .viz{width:100%;height:100%;min-height:0;display:flex;flex-direction:column;justify-content:center;font-family:Arial,Helvetica,sans-serif;color:${INK}}
    .viz .diagram{display:block;width:100%;min-height:0;max-height:100%;flex:1;overflow:visible;font-family:Arial,Helvetica,sans-serif}
    .visual-caption{font-size:clamp(11px,.94vw,15px);line-height:1.4;color:${GRAY};padding-top:10px;max-width:1100px}
    .visual-brief{display:none;font-size:18px;line-height:1.5}
    .visual-brief ol{padding-left:22px;display:grid;gap:12px;margin:10px 0}
    .visual-brief p{margin:0 0 15px}.visual-brief strong{font-weight:600}
    .mathline{font-family:'Cambria Math','STIX Two Math',Georgia,serif;font-size:clamp(23px,2.2vw,38px);line-height:1.5;white-space:normal}
    .mathline sub,.mathline sup{font-size:.55em;line-height:0;position:relative}.mathline sub{vertical-align:sub}.mathline sup{vertical-align:super}
    .fraction{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.25;font-size:.85em;margin:0 .18em}.fraction>span:first-child{border-bottom:1px solid currentColor;padding:0 .14em .1em}.fraction>span:last-child{padding:.08em .14em 0}
    .math-blue{color:${BLUE}}.formula-label{font:600 13px/1.3 Arial,sans-serif;text-transform:uppercase;letter-spacing:.08em;color:${GRAY};margin-bottom:12px}
    .formula-pair{display:grid;grid-template-columns:1fr 1fr;gap:5%;padding-top:6px}.formula-pair>div{border-top:1px solid ${PALE};padding-top:8px}.formula-pair span{font-size:15px;color:${GRAY}}
    .formula-pair .mathline{font-size:clamp(23px,1.9vw,32px)}
    .kl-plot{flex:1;min-height:0;display:flex}.kl-toolbar{display:flex;align-items:center;justify-content:space-between;gap:20px;border-top:1px solid ${PALE};padding-top:10px}.kl-toolbar .mathline{font-size:clamp(22px,1.95vw,32px)}
    .viz-button{border:1px solid ${PALE};color:${BLUE};background:transparent;padding:10px 17px;font:500 15px/1.1 Arial,Helvetica,sans-serif;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s;min-height:42px}.viz-button:hover,.viz-button[aria-pressed=true]{background:${BLUE};border-color:${BLUE};color:${PAPER}}.viz-button:focus-visible{outline:2px solid ${BLUE};outline-offset:4px}
    .timing-strip{display:grid;grid-template-columns:1.35fr 1fr 1fr 1fr;align-items:center;gap:20px;border-top:1px solid ${PALE};padding-top:14px;font-size:15px}.timing-strip strong{font-size:29px;font-weight:600;margin-left:12px}.timing-strip small{font-size:11px;color:${GRAY}}.blue{color:${BLUE}}
    .chart-legend{display:flex;gap:28px;font-size:13px;margin-bottom:5px}.chart-legend span{display:flex;align-items:center;gap:8px}.chart-legend i{width:12px;height:12px;display:inline-block}
    .residual-top{border-bottom:1px solid ${PALE};padding-bottom:20px}.residual-top .mathline{font-size:clamp(24px,2.5vw,41px)}
    .formula-explainer{display:flex;justify-content:flex-end;gap:80px;max-width:1000px;font-size:15px;color:${GRAY};margin-top:10px}.residual-bottom{display:grid;grid-template-columns:1.2fr 1fr;gap:50px;padding-top:26px}.residual-bottom p{color:${GRAY};font-size:16px;line-height:1.5;margin:12px 0 0}.residual-bottom .mathline{font-size:clamp(30px,3vw,48px)}
    .sum{display:inline-block;position:relative;margin-right:24px}.sum>sub{position:absolute;left:50%;bottom:-12px;transform:translateX(-50%);white-space:nowrap;font-size:.32em}
    .coverage-layout{display:grid;grid-template-columns:1.15fr 1fr;gap:9%;align-items:center;min-height:0}.coverage-matrix{font-size:21px}.coverage-head,.coverage-row{display:grid;grid-template-columns:80px repeat(3,1fr);gap:8px}.coverage-head{font-size:14px;color:${GRAY};margin-bottom:12px;text-align:center}.coverage-row{padding:6px;border:2px solid transparent}.coverage-row.fixed{border-color:${INK}}.coverage-row.chosen{border-color:${BLUE}}.coverage-row>strong{display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:22px;font-weight:500}.coverage-row small{font-size:10px;line-height:1.3;color:${GRAY}}.coverage-row>span{background:rgba(30,58,245,calc(var(--strength)*.85));color:${INK};padding:12px 0;text-align:center;font-variant-numeric:tabular-nums}.coverage-row>span[style*="0.9"],.coverage-row>span[style*="0.8"]{color:white}
    .coverage-buttons{display:flex;gap:8px}.coverage-gain{font-size:clamp(48px,5vw,76px);letter-spacing:-.06em;font-weight:600;color:${BLUE};line-height:1.1;margin-top:12px}.coverage-insight p{font-size:17px;color:${GRAY};margin:0 0 12px}.coverage-total{font-size:20px;color:${INK}}.coverage-explain{font-size:16px;line-height:1.4;color:${GRAY};margin-top:12px;max-width:360px}.viz-coverage>.mathline{border-top:1px solid ${PALE};padding-top:12px;margin-top:15px;font-size:clamp(22px,1.9vw,32px)}
    .gradient-formula{display:flex;gap:30px;align-items:center;border-top:1px solid ${PALE};padding-top:10px}.gradient-formula>span{font-size:14px;color:${GRAY};max-width:220px}.gradient-formula .mathline{color:${BLUE}}
    .compact-table{width:100%;border-collapse:collapse;font-size:16px;line-height:1.4}.compact-table th{text-align:left;font-size:12px;font-weight:500;color:${GRAY};border-bottom:1px solid ${PALE};padding:8px 5px}.compact-table td{padding:10px 5px;border-bottom:1px solid ${PALE};font-variant-numeric:tabular-nums}.compact-table th:first-child,.compact-table td:first-child{padding-left:0}.compact-table td:not(:first-child){text-align:right}
    @media(max-width:700px) and (orientation:portrait){
      .viz .diagram{display:none}.visual-brief{display:block}.viz{height:auto}.visual-caption{font-size:11px;padding-top:12px}.viz-chart .visual-caption{order:2}.viz-chart .visual-brief{order:1}.viz-chart .timing-strip{order:3}
      .formula-pair{display:none}.kl-plot{display:none}.kl-toolbar{flex-direction:column;align-items:flex-start;order:2}.kl-toolbar .viz-button{display:none}.viz-kl .visual-caption{order:3}.viz-kl .visual-brief{order:1}
      .timing-strip{grid-template-columns:1fr 1fr;gap:14px;font-size:12px;margin-top:15px}.timing-strip strong{font-size:20px}.chart-legend{display:none}
      .residual-top{padding-bottom:18px}.residual-top .mathline{font-size:24px}.formula-explainer{display:none}.residual-bottom{grid-template-columns:1fr;gap:24px;padding-top:20px}.residual-bottom .mathline{font-size:28px}.residual-bottom p{font-size:15px}
      .coverage-layout{grid-template-columns:1fr;gap:20px}.coverage-head,.coverage-row{grid-template-columns:48px repeat(3,1fr);gap:5px}.coverage-matrix{font-size:18px}.coverage-row>span{padding:8px 0}.coverage-row>strong{font-size:19px}.coverage-head{font-size:12px}.coverage-insight{display:grid;grid-template-columns:1fr 1fr;align-items:center}.coverage-insight .formula-label{grid-column:1}.coverage-buttons{grid-column:2;grid-row:1}.coverage-buttons .viz-button{padding:8px 12px;min-height:36px}.coverage-gain{font-size:44px;grid-column:1;grid-row:2}.coverage-insight p{grid-column:2;grid-row:2;font-size:14px}.coverage-total,.coverage-explain{grid-column:1/-1}.coverage-total{font-size:17px}.coverage-explain{font-size:14px;margin-top:7px}.viz-coverage>.mathline{font-size:20px}
      .gradient-formula{flex-direction:column;align-items:flex-start;gap:8px;order:2}.gradient-formula .mathline{font-size:24px}.viz-gradient .visual-caption{order:3}.viz-gradient .visual-brief{order:1}
    }
    @media(prefers-reduced-motion:reduce){.viz-button{transition:none}}
  `;document.head.appendChild(style);
})();
