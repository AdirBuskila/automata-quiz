// Mobile guard for learn mode: open every chapter at 390px in headless Chrome, fail on any
// page-level horizontal overflow, report boxes that scroll (allowed — they get an edge
// shadow), screenshot each chapter top to tools/raw/shots/learn-<i>-<theme>.png.
//   node tools/verify_learn.js [--theme dark|light] [--width 390]
const path=require("path"), fs=require("fs"), puppeteer=require("puppeteer-core");
const CHROME="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const args=process.argv.slice(2);
const opt=(k,d)=>{ const i=args.indexOf("--"+k); return i>=0 ? args[i+1] : d; };
const width=+opt("width",390), theme=opt("theme","dark");
const OUT=path.join(__dirname,"raw","shots"); fs.mkdirSync(OUT,{recursive:true});
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME, headless:"new"});
  const p=await b.newPage(); await p.setViewport({width, height:900, deviceScaleFactor:1});
  const errs=[]; p.on("pageerror",e=>errs.push(String(e)));
  await p.evaluateOnNewDocument(t=>{ try{ localStorage.setItem("afq_theme",t); }catch(e){} }, theme);
  await p.goto("file:///"+path.join(__dirname,"..","index.html").split(path.sep).join("/"));
  await p.evaluate(()=>document.querySelector("#learnEntry").click());
  const n=await p.evaluate(()=>window.LEARN.length);
  let bad=0;
  for(let i=0;i<n;i++){
    if(i) await p.evaluate(()=>document.querySelector("#learnNext").click());
    await new Promise(r=>setTimeout(r,120));
    const r=await p.evaluate(()=>({
      title:document.querySelector(".learn-h").textContent,
      over:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      scroll:[...document.querySelectorAll("#learnContent .scrollable")].length,
      unmarked:[...document.querySelectorAll("#learnContent .math-block,#learnContent .tbl-wrap")]
        .filter(e=>e.scrollWidth>e.clientWidth+1 && !e.classList.contains("scrollable")).length,
    }));
    await p.screenshot({path:path.join(OUT,`learn-${String(i+1).padStart(2,"0")}-${theme}.png`)});
    const ok=r.over<=0 && r.unmarked===0; if(!ok) bad++;
    console.log(`${ok?"ok  ":"FAIL"} ${i+1} ${r.title}  overflow=${r.over}px  scrollable=${r.scroll}  unmarked=${r.unmarked}`);
  }
  if(errs.length){ console.log("PAGE ERRORS:\n"+errs.join("\n")); bad++; }
  await b.close();
  console.log(bad?`\nLEARN VERIFY FAILED (${bad})`:"\nLEARN VERIFY PASSED"); process.exit(bad?1:0);
})();
