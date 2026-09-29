// Headless-Chrome screenshots of chosen questions of one exam (mobile by default).
//   node tools/shoot.js <EXAM> <n,n,...> [--width 390] [--theme dark|light] [--answer]
// Writes tools/raw/shots/<EXAM>-Q<n>-<theme>-<width>.png and reports horizontal overflow.
const path=require("path"), fs=require("fs");
const puppeteer=require("puppeteer-core");
const CHROME="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const args=process.argv.slice(2);
const exam=args[0], nums=(args[1]||"1").split(",").map(Number);
const opt=(k,d)=>{ const i=args.indexOf("--"+k); return i>=0 ? args[i+1] : d; };
const width=+opt("width",390), theme=opt("theme","dark"), answer=args.includes("--answer");
const OUT=path.join(__dirname,"raw","shots"); fs.mkdirSync(OUT,{recursive:true});

(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME, headless:"new"});
  const p=await b.newPage();
  await p.setViewport({width, height:900, deviceScaleFactor:2});
  const errs=[]; p.on("pageerror",e=>errs.push(String(e))); p.on("console",m=>{ if(m.type()==="error") errs.push(m.text()); });
  await p.evaluateOnNewDocument(t=>{ try{ localStorage.setItem("afq_theme",t); }catch(e){} }, theme);
  await p.goto("file:///"+path.join(__dirname,"..","index.html").replace(/\\/g,"/"));
  await p.click('input[name=mode][value="exam"]');
  await p.select("#examPick", exam);
  await p.click("#startBtn");
  let at=1;
  for(const n of nums.sort((a,b)=>a-b)){
    while(at<n){ await p.evaluate(()=>document.querySelector("#nextBtn").click()); at++; }
    if(answer){ // practice-style reveal isn't available in exam mode; mark the correct option instead
      await p.evaluate(()=>{ const q=window.AUTOMATA_QUIZ.questions.find(x=>x.id===document.querySelector("#questionText").dataset.qid);
        document.querySelector(`.opt[data-oid="${q.correctId}"]`).classList.add("correct"); });
    }
    const over=await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    // a display formula wider than its box scrolls sideways — readable, but easy to miss
    const clipped=await p.evaluate(()=>[...document.querySelectorAll(".question-card .math-block, .question-card .math-lines, .question-card .opt .txt")]
      .filter(e=>e.scrollWidth>e.clientWidth+1).length);
    const card=await p.$(".question-card");
    const f=path.join(OUT,`${exam}-Q${n}-${theme}-${width}.png`);
    await card.screenshot({path:f});
    console.log(`Q${n}: ${path.basename(f)}  overflow=${over}px  clipped=${clipped}`);
    if(over>0||clipped>0) process.exitCode=1;
  }
  if(errs.length) console.log("PAGE ERRORS:\n"+errs.join("\n"));
  await b.close();
})();
