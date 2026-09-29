// Screenshot the practice-mode feedback panel of one question (explanation + source note).
//   node tools/shoot_feedback.js <QID> [--width 390] [--theme dark|light] [--wrong]
const path=require("path"), fs=require("fs"), puppeteer=require("puppeteer-core");
const CHROME="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const args=process.argv.slice(2), qid=args[0];
const opt=(k,d)=>{ const i=args.indexOf("--"+k); return i>=0 ? args[i+1] : d; };
const width=+opt("width",390), theme=opt("theme","dark"), wrong=args.includes("--wrong");
const OUT=path.join(__dirname,"raw","shots"); fs.mkdirSync(OUT,{recursive:true});
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME, headless:"new"});
  const p=await b.newPage(); await p.setViewport({width, height:900, deviceScaleFactor:2});
  await p.evaluateOnNewDocument(t=>{ try{ localStorage.setItem("afq_theme",t); }catch(e){} }, theme);
  const url="file:///"+path.join(__dirname,"..","index.html").split(path.sep).join("/");
  await p.goto(url);
  const topic=await p.evaluate(id=>window.AUTOMATA_QUIZ.questions.find(q=>q.id===id).topic, qid);
  await p.goto(url+"?practice="+topic);
  for(let i=0;i<200;i++){
    if(await p.$eval("#questionText",e=>e.dataset.qid)===qid) break;
    await p.click(".opt"); await p.click("#nextBtn");
  }
  const correct=await p.evaluate(id=>window.AUTOMATA_QUIZ.questions.find(q=>q.id===id).correctId, qid);
  await p.click(wrong ? `.opt:not([data-oid="${correct}"])` : `.opt[data-oid="${correct}"]`);
  const f=path.join(OUT,`${qid}-feedback-${theme}-${width}.png`);
  await (await p.$(".question-card")).screenshot({path:f});
  console.log(f); await b.close();
})();
