// Node smoke test: data integrity + shuffle/scoring invariant + js≡json sync.
const fs=require("fs"),path=require("path"),vm=require("vm");
const ROOT=path.join(__dirname,"..");
const code=fs.readFileSync(path.join(ROOT,"questions.js"),"utf8");
const sandbox={window:{}}; vm.createContext(sandbox); vm.runInContext(code,sandbox);
const DATA=sandbox.window.AUTOMATA_QUIZ, QS=DATA.questions, CTX=DATA.contexts;
let bad=0; const topics={};
const fail=(...m)=>{console.log(...m);bad++;};
for(const q of QS){
  topics[q.topic]=(topics[q.topic]||0)+1;
  const ids=(q.options||[]).map(o=>o.id);
  if(ids.length<2) fail("BAD options",q.id);
  if(new Set(ids).size!==ids.length) fail("DUP option id",q.id);
  if(!ids.includes(q.correctId)) fail("BAD correctId",q.id);
  for(const a of q.acceptedIds||[]) if(!ids.includes(a)) fail("BAD acceptedId",q.id);
  if(!q.questionHtml||!q.questionHtml.trim()) fail("EMPTY q",q.id);
  if(q.options.some(o=>!String(o.html||"").trim())) fail("BLANK opt html",q.id);
  if(q.contextId && !CTX[q.contextId]) fail("MISSING ctx",q.id);
  const all=[q.questionHtml,q.explanationHtml,...q.options.map(o=>o.html)].join("");
  if(/\u0000M\d+\u0000/.test(all)) fail("UNFILLED math placeholder",q.id);
  if(/\$[^$<]+\$/.test(all)) fail("RAW $tex$ leaked",q.id);
  const m=all.match(/<math /g)||[], l=all.match(/<math dir="ltr"/g)||[];
  if(m.length!==l.length) fail("math not dir=ltr",q.id);
  if(q.official && String(q.answerSource).startsWith("moodle")) fail("moodle key marked official",q.id);
}
// unique ids: app.js keys the exam answer map by q.id
const seen={}; let dupIds=0;
for(const q of QS){ if(seen[q.id]){fail("DUP id",q.id);dupIds++;} seen[q.id]=1; }
// questions.js is the only file the browser loads; questions.json must not drift from it
const synced=JSON.stringify(DATA)===JSON.stringify(JSON.parse(fs.readFileSync(path.join(ROOT,"questions.json"),"utf8")));
if(!synced) fail("OUT OF SYNC questions.js vs questions.json (rebuild with build_questions.py)");
// shuffle/scoring invariant — mirrors app.js viewOrder()/makeView()
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function viewOrder(q){ if(q.lockOrder) return q.options.map(o=>o.id);
  return shuffle(q.options.filter(o=>!o.last).map(o=>o.id)).concat(q.options.filter(o=>o.last).map(o=>o.id)); }
let mismatch=0, lastMoved=0, trials=0; const pos=[0,0,0,0];
for(let t=0;t<5000;t++){
  const q=QS[t%QS.length], order=viewOrder(q);
  const acc=(q.acceptedIds&&q.acceptedIds.length)?q.acceptedIds:[q.correctId];
  const correctSet=new Set(order.map((id,i)=>acc.includes(id)?i:-1).filter(i=>i>=0));
  const disp=order.indexOf(q.correctId);
  if(!correctSet.has(disp) || order[disp]!==q.correctId) mismatch++;       // click → id must round-trip
  if(order.length!==q.options.length || new Set(order).size!==order.length) mismatch++;
  const nLast=q.options.filter(x=>x.last).length;
  q.options.forEach(o=>{ if(o.last && order.indexOf(o.id)<order.length-nLast) lastMoved++; });
  if(q.options.length===4 && !nLast && !q.lockOrder){pos[disp]++;trials++;}
}
console.log("total questions:",QS.length," contexts:",Object.keys(CTX).length);
console.log("by topic:",topics);
console.log("integrity problems:",bad);
console.log("duplicate ids:",dupIds,"(must be 0)");
console.log("questions.js === questions.json:",synced);
console.log("scoring-map mismatches:",mismatch,"(must be 0)");
console.log("'last' options displaced:",lastMoved,"(must be 0)");
if(trials) console.log("correct display position (free 4-opt, ~even):",pos.map(c=>(c/trials*100).toFixed(1)+"%").join(" / "));
const ok=bad===0&&mismatch===0&&lastMoved===0;
console.log(ok?"\nSMOKE TEST PASSED":"\nSMOKE TEST FAILED"); process.exit(ok?0:1);
