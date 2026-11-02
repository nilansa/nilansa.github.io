/* Searches one selected venue/year shard at a time and retains at most 200 hits per shard. */
const cancelled = new Set();
const wordPattern = /[\p{L}\p{N}_+#.-]+/gu;
const HOSTS = {CVPR:["openaccess.thecvf.com"],ICCV:["openaccess.thecvf.com"],ECCV:["openaccess.thecvf.com","ecva.net","www.ecva.net","eccv.ecva.net","eccv2024.ecva.net","eccv2022.ecva.net"],NeurIPS:["openreview.net","proceedings.neurips.cc"],ICML:["openreview.net","proceedings.mlr.press"],ICLR:["openreview.net"],AAAI:["ojs.aaai.org"],ACL:["aclanthology.org"],EMNLP:["aclanthology.org"],NAACL:["aclanthology.org"],ICRA:["ieeexplore.ieee.org","doi.org"],ICASSP:["ieeexplore.ieee.org","doi.org","cmsworkshops.com"]};
function words(value){return(String(value||"").toLocaleLowerCase().match(wordPattern)||[]).map(w=>w.replace(/^[.-]+|[.-]+$/g,"")).filter(Boolean)}
function norm(value){return words(value).join(" ")}
function safeUrl(value,venue,ext=""){
    try {
      const u=new URL(value);
      const listing=venue==="CVPR"&&/^\/CVPR20\d{2}$/i.test(u.pathname)&&u.search==="?day=all";
      const forum=["NeurIPS","ICML","ICLR"].includes(venue)&&u.hostname==="openreview.net"&&["/forum","/pdf"].includes(u.pathname)&&/^\?id=[A-Za-z0-9_-]{6,80}$/.test(u.search);
      const icassp=venue==="ICASSP"&&u.hostname==="cmsworkshops.com"&&/^\/ICASSP20\d{2}\/view_paper\.php$/.test(u.pathname)&&/^\?PaperNum=\d{1,10}$/.test(u.search);
      const aaaiPdf=venue==="AAAI"&&ext===".pdf"&&/^\/index\.php\/AAAI\/article\/download\/\d+\/\d+$/.test(u.pathname);
      return u.protocol==="https:"&&HOSTS[venue]?.includes(u.hostname)&&!u.username&&!u.password&&!u.hash&&(!u.search||listing||forum||icassp)&&(!ext||u.pathname.toLowerCase().endsWith(ext)||listing||aaaiPdf)?u.href:"";
    }catch{return ""}
  }
  function normalize(p,venue,year){
 const paperUrl=safeUrl(p.paper_url||p.cvf_url,venue,".html")||safeUrl(p.paper_url||p.cvf_url,venue);
 const pdfUrl=safeUrl(p.pdf_url,venue,".pdf");
 return {...p,venue,year,title:String(p.title||""),authors:String(p.authors||""),abstract:String(p.abstract||""),paper_url:paperUrl,pdf_url:pdfUrl,source:String(p.source||"Curated venue record"),cluster:String(p.cluster||p.primary_area||"Other"),track_status:String(p.track_status||"Curated venue record; track not independently verified")};
}
function scorePaper(p,terms,phrases,topic){
 const area=norm(`${p.cluster} ${p.primary_area||""}`), areaTerms=words(topic);if(areaTerms.length&&!areaTerms.every(t=>area.includes(t)))return -1;
 const title=norm(p.title), authors=norm(p.authors), abstract=norm(p.abstract), all=[title,authors,abstract];
 let score=0;
 for(const t of terms){if(title.includes(t))score+=3;if(authors.includes(t))score+=1.2;if(abstract.includes(t))score+=1}
 for(const phrase of phrases){if(title.includes(phrase))score+=10;else if(all.some(f=>` ${f} `.includes(` ${phrase} `)))score+=5}
 for(let i=0;i<terms.length-1;i++)if(all.some(f=>` ${f} `.includes(` ${terms[i]} ${terms[i+1]} `)))score+=1.6;
 return score;
}
async function yieldWorker(){await new Promise(resolve=>setTimeout(resolve,0))}
async function run(m){const terms=[...new Set(words(m.query))], phrases=[...String(m.query||"").matchAll(/"([^\"]+)"/g)].map(x=>norm(x[1])).filter(Boolean), rest=String(m.query||"").replace(/"[^\"]+"/g," ").trim();if(words(rest).length>1)phrases.push(norm(rest));
 const allHits=[];let totalHits=0, processed=0;const shards=m.shards||[];
 for(let si=0;si<shards.length;si++){
  if(cancelled.has(m.requestId))return;
  const {venue,year}=shards[si]; self.postMessage({type:"progress",requestId:m.requestId,current:si+1,total:shards.length,venue,year,stage:"download"});
  const url=new URL(venue==="CVPR"?`data/${year}.json`:`data/venues/${venue}/${year}.json`,self.location.href);
  const response=await fetch(url);if(!response.ok)throw new Error(`${venue} ${year} unavailable (HTTP ${response.status}).`);
  const bundle=await response.json();const rows=venue==="CVPR"?bundle.papers:bundle.papers;
  if(!Array.isArray(rows))throw new Error(`${venue} ${year} shard has invalid format.`);
  let shardHits=[];
  for(let i=0;i<rows.length;i++){
   if(i%500===0){if(cancelled.has(m.requestId))return;processed+=Math.min(500,rows.length-i);self.postMessage({type:"progress",requestId:m.requestId,current:si+1,total:shards.length,venue,year,stage:"scan",scanned:Math.min(i+500,rows.length)});await yieldWorker()}
   const p=normalize(rows[i],venue,year); if(!p.title)continue;
   const score=scorePaper(p,terms,phrases,m.topic||"");
   if(score<0)continue;
   if(!terms.length&&!phrases.length&&!String(m.topic||"").trim())continue;
   if(score>0||(!terms.length&&!phrases.length&&String(m.topic||"").trim())){totalHits++;shardHits.push({...p,score:Math.round(score*10000)/10000})}
  }
  shardHits.sort((a,b)=>b.score-a.score||b.year-a.year||a.title.localeCompare(b.title));
  allHits.push(...shardHits.slice(0,200));
  self.postMessage({type:"progress",requestId:m.requestId,current:si+1,total:shards.length,venue,year,stage:"indexed",yearCount:rows.length,matchCount:shardHits.length});
  // Drop each parsed shard before requesting the next one.
 }
 if(cancelled.has(m.requestId))return;
 const sort=m.sort||"relevance";allHits.sort((a,b)=>sort==="newest"?b.year-a.year||a.venue.localeCompare(b.venue)||a.title.localeCompare(b.title):sort==="oldest"?a.year-b.year||a.venue.localeCompare(b.venue)||a.title.localeCompare(b.title):sort==="title"?a.title.localeCompare(b.title)||a.venue.localeCompare(b.venue):b.score-a.score||b.year-a.year||a.title.localeCompare(b.title));
 const offset=Math.max(0,Number(m.offset)||0), limit=Math.max(1,Number(m.limit)||40);
 self.postMessage({type:"results",requestId:m.requestId,total:totalHits,retained:allHits.length,offset,results:allHits.slice(offset,offset+limit),shards:shards.length});
}
self.onmessage=event=>{const m=event.data||{};if(m.type==="cancel"){cancelled.add(m.requestId);return}if(m.type==="search")run(m).catch(error=>{if(!cancelled.has(m.requestId))self.postMessage({type:"error",requestId:m.requestId,message:error.message||"Search failed."})}).finally(()=>cancelled.delete(m.requestId))};
