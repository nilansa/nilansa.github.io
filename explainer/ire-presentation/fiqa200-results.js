/* FiQA-200 H100 experimental addendum. Audited exploratory v3 outputs; no model execution. */
(function () {
  'use strict';
  var d = window.DECK;
  if (!d || !Array.isArray(d.slides)) return;
  if (d.slides.some(function (s) { return s.id === 's21-fiqa200'; })) return;
  var archive = 'https://drive.google.com/file/d/14V09TR4oi412cUU6gIeZvIEx31zb1Hor/view';
  var coverage = 'https://drive.google.com/file/d/1StPZn0POnTGSGJZCE6OmkcCTxQXv02C_/view';
  d.sources.FIQA200_V3 = {title:'FiQA-200 H100 accepted v3 · results and independent audit',url:archive,locator:'RESULTS.md, Accepted v3 results; evaluation_summary.json; independent_metrics_audit.json. Task ire-fiqa200-complementary-baselines-20261116-1517; transfer index revision 4, 16 Nov 2026.'};
  d.sources.FIQA200_COV = {title:'FiQA-200 H100 coverage/MaxSim · completed handoff',url:coverage,locator:'CLAUDE_SCIENCE_HANDOFF-r9.md, 16 Nov 2026; dense, coverage and BERT MaxSim TTT arms; exploratory 200-query results.'};
  d.meta.version = 'FiQA-200 final H100 results addendum';
  d.meta.sourceCutoff = 'Completed exploratory FiQA-200 H100 runs were audited on 16 November 2026. The new final slide supersedes the older proposal-only status of complementary candidate selection; no improvement over dense feedback was demonstrated.';
  var notes = [
    'After the earlier experiments, we also tested our actual complementary-feedback proposal on two hundred FiQA queries using the complete fifty-seven-thousand-six-hundred-thirty-eight-document corpus.',
    'The frozen model was Qwen3 Embedding zero point six billion, with feedback from Qwen3 Reranker four billion. All compared adaptation arms scored ten selected documents per query and performed a full-corpus retrieval after their query-vector update.',
    'Dense top-ten feedback with TTT achieved point five-zero-five-nine-six nDCG at ten. MMR was nearly tied at point five-zero-four-five-nine; hybrid dense plus BM25 achieved point five-zero-zero-one-nine; BM25 alone point four-six-two-eight-zero.',
    'Our earlier DISCo-inspired contextual coverage plus TTT result was point four-eight-zero-seven-zero, and independent BERT MaxSim achieved point four-eight-eight-zero-seven, on the same selected two-hundred-query FiQA setting.',
    'MMR produced the highest reported recall at one hundred, point eight-one-three-five-three versus dense at point eight-zero-three-seven-eight, although this is not an established statistically significant win.',
    'The paired nDCG intervals for MMR and hybrid versus dense include zero. BM25 was clearly worse within this exploratory sample. We therefore cannot claim that complementarity improves TTT. Full official DISCo and trained ColBERT remain untested.',
    'This is an exploratory, previously exposed test-query set—not a new blind holdout. Its lesson is that selection matters, but simple dense feedback remained the strongest of these arms on nDCG at ten.'
  ];
  d.slides.push({
    number:21,id:'s21-fiqa200',chapter:'Measured follow-up',
    title:'What did complementary\nfeedback actually achieve?',
    subtitle:'FiQA-200 · H100 · frozen Qwen3 embeddings · 10 teacher-scored pairs per query',
    kind:'fiqa200-results',evidence:'Completed exploratory experiment',
    takeaway:'None beat dense10 + TTT on nDCG@10; MMR had the highest observed Recall@100.',
    visual:{},
    notes:notes.map(function (text,i) {return {id:'S21.'+String(i+1).padStart(2,'0'),text:text,refs:i===3||i===5?['FIQA200_COV','FIQA200_V3']:['FIQA200_V3'],type:'Audited exploratory evidence',exactLocation:'Accepted v3 RESULTS.md and evaluation_summary.json; earlier FiQA200 coverage handoff.'};}),
    pointers:['Compare the nDCG bars first: the plain dense feedback arm remains highest.','Then point to Recall@100: the MMR increase is descriptive, not a confirmed superiority claim.','Close by distinguishing the DISCo-inspired fixed-pool approximation from official DISCo.'],
    refs:['FIQA200_V3','FIQA200_COV'],
    caveat:'200 previously exposed FiQA test queries; exploratory comparison. Not official DISCo or trained ColBERT.',
    wordCount:notes.join(' ').split(/\s+/).length,secondsAt130Wpm:Math.round(notes.join(' ').split(/\s+/).length/130*60)
  });
  var old = window.renderVisual;
  window.renderVisual = function(s) {
    if(s.kind !== 'fiqa200-results') return typeof old === 'function' ? old(s) : '';
    var a=[['Dense10 + TTT',.50596],['MMR + TTT',.50459],['Hybrid + TTT',.50019],['BERT MaxSim + TTT',.48807],['DISCo-style coverage + TTT',.48070],['BM25 + TTT',.46280]];
    var bars=a.map(function(x,i) {
      var y=25+i*48, width=x[1]/.54*500;
      return '<text x="5" y="'+(y+18)+'" font-size="18" fill="#151515">'+x[0]+'</text><rect x="410" y="'+y+'" width="'+width.toFixed(1)+'" height="27" fill="'+(i===0?'#1E3AF5':i===1?'#6878F1':'#D6D7D2')+'"/><text x="'+(420+width)+'" y="'+(y+20)+'" font-size="18" font-weight="'+(i===0?'700':'400')+'" fill="#151515">'+x[1].toFixed(5)+'</text>';
    }).join('');
    return '<div class="viz viz-chart"><div class="chart-legend"><span><i style="background:#1E3AF5"></i> Highest nDCG@10: dense feedback</span><span>200 previously exposed queries</span></div>'+
      '<svg class="diagram" viewBox="0 0 1200 355" role="img" aria-label="nDCG at 10: dense ten TTT 0.50596, MMR 0.50459, hybrid 0.50019, BERT MaxSim 0.48807, DISCo-inspired coverage 0.48070, BM25 0.46280.">'+bars+'</svg>'+
      '<div style="display:flex;gap:32px;flex-wrap:wrap;border-top:1px solid #D6D7D2;padding-top:10px;font-size:clamp(13px,1.2vw,19px)"><span><b>Recall@100:</b> Dense 0.80378</span><span><b style="color:#1E3AF5">MMR 0.81353</b> (descriptive)</span><span><b>MMR ΔnDCG:</b> −0.00136; 95% CI [−0.01215,+0.00938]</span></div>'+
      '<div class="visual-caption">Same frozen Qwen3 index and teacher; 10 feedback pairs/query. DISCo-inspired fixed-pool method ≠ official DISCo. Source: audited FiQA-200 Modal H100 runs, 16 Nov 2026.</div>'+
      '<div class="visual-brief"><p>nDCG@10: dense .50596; MMR .50459; hybrid .50019; BERT MaxSim .48807; DISCo-inspired coverage .48070; BM25 .46280.</p><p>MMR Recall@100 .81353 versus dense .80378. Exploratory, not blind.</p></div></div>';
  };
})();
