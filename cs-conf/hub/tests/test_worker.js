/* Run: node cs-conf/hub/tests/test_worker.js */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const code = fs.readFileSync(path.join(root, "search-worker.js"), "utf8");
const workerContext = vm.createContext({URL, setTimeout, self: {postMessage(){}}});
vm.runInContext(code, workerContext);
const workerSafe = (url,venue,ext="")=>vm.runInContext("safeUrl("+JSON.stringify(url)+","+JSON.stringify(venue)+","+JSON.stringify(ext)+")",workerContext);
const appCode = fs.readFileSync(path.join(root,"app.js"),"utf8");
const hosts=appCode.match(/const hosts=(\{[^\n]+\});/);
assert(hosts,"app host map found");
const fnStart=appCode.indexOf("  function safeUrl("),fnEnd=appCode.indexOf("  function cleanPaper(",fnStart);
assert(fnStart>=0&&fnEnd>fnStart,"app safeUrl function found");
const appContext=vm.createContext({URL});
vm.runInContext("const hosts="+hosts[1]+";\n"+appCode.slice(fnStart,fnEnd),appContext);
const appSafe=(url,venue,ext="")=>vm.runInContext("safeUrl("+JSON.stringify(url)+","+JSON.stringify(venue)+","+JSON.stringify(ext)+")",appContext);
const catalog=JSON.parse(fs.readFileSync(path.join(root,"catalog.json"),"utf8"));
let links=0,shards=0;
for(const [venue,meta] of Object.entries(catalog.venues)){
 for(const [year,item] of Object.entries(meta.years)){
  const data=JSON.parse(fs.readFileSync(path.join(root,item.file),"utf8"));
  assert.equal(data.year,Number(year));
  for(const p of data.papers){
   const url=p.paper_url||p.cvf_url||"";
   if(url){
    assert.equal(workerSafe(url,venue),url,"worker link "+venue+" "+year+" "+url);
    assert.equal(appSafe(url,venue),url,"app link "+venue+" "+year+" "+url);
    links++;
   }
  }
  shards++;
 }
}
const good="https://openreview.net/forum?id=6T3wJQhvc3";
assert.equal(workerSafe(good,"ICLR"),good);
assert.equal(workerSafe(good+"&next=https://evil.test","ICLR"),"");
assert.equal(appSafe("https://eccv.ecva.net/virtual/2026/poster/4225","ECCV"),"https://eccv.ecva.net/virtual/2026/poster/4225");
const paper={title:"Scene geometry reasoning",authors:"",abstract:"3D spatial relations",cluster:"3D & geometry",primary_area:"3D"};
const scorer=(terms,topic)=>vm.runInContext("scorePaper("+JSON.stringify(paper)+","+JSON.stringify(terms)+",[],"+JSON.stringify(topic)+")",workerContext);
assert.equal(scorer([],"geometry"),0,"topic-only match remains eligible");
assert.equal(scorer([],"speech"),-1,"topic-only mismatch is excluded");
assert(scorer(["geometry"],"geometry")>0);
console.log("JS URL allowlists verified: "+links+" source URLs in "+shards+" shards; topic-only filtering correct.");
