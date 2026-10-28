// Headless DOM test (jsdom): boots index.html with questions.js + learn.js + app.js, renders
// topics, runs a practice question, a full-exam replay with grading, and checks figures/math.
const fs=require("fs"), path=require("path"); const { JSDOM } = require("jsdom");
const ROOT=path.join(__dirname,"..");
const dom=new JSDOM(fs.readFileSync(path.join(ROOT,"index.html"),"utf8"),{pretendToBeVisual:true,runScripts:"outside-only",url:"http://localhost/"});
const { window }=dom;
window.scrollTo=()=>{}; window.HTMLElement.prototype.scrollIntoView=()=>{}; window.confirm=()=>true;
window.matchMedia=window.matchMedia||(q=>({matches:false,media:q,addEventListener(){},removeEventListener(){}}));
for(const f of ["questions.js","learn.js","app.js"]) window.eval(fs.readFileSync(path.join(ROOT,f),"utf8"));
const $=s=>window.document.querySelector(s), $$=s=>[...window.document.querySelectorAll(s)];
let fail=0; const assert=(c,m)=>{console.log((c?"  ok  ":"FAIL  ")+m); if(!c) fail++;};
const QS=window.AUTOMATA_QUIZ.questions;

assert(QS.length>0, `questions loaded: ${QS.length}`);
assert($$("#topicGrid .topic-btn").length===12, `topic buttons: ${$$("#topicGrid .topic-btn").length} (11 topics + all)`);
assert(QS.every(q=>q.topicLabel), "every question has a topic label");
assert(/\d/.test($("#datasetInfo").textContent), `datasetInfo: "${$("#datasetInfo").textContent}"`);
assert($("#learnEntry").style.display==="none" || (window.LEARN||[]).length>0, "learn entry hidden while learn.js is empty");

// every referenced figure exists on disk
const refs=[]; for(const q of QS){ if(q.image) refs.push(q.image); for(const o of q.options) if(o.type==="image") refs.push(o.value); }
for(const c of Object.values(window.AUTOMATA_QUIZ.contexts)) for(const m of c.html.matchAll(/src="([^"]+)"/g)) refs.push(m[1]);
const missing=refs.filter(r=>!fs.existsSync(path.join(ROOT,r)));
assert(missing.length===0, `all ${refs.length} figure files exist${missing.length?" MISSING: "+missing.join(", "):""}`);

// math: rendered MathML, always LTR, no raw TeX
const html=QS.map(q=>q.questionHtml+q.explanationHtml+q.options.map(o=>o.html).join("")).join("");
const nm=(html.match(/<math /g)||[]).length, nl=(html.match(/<math dir="ltr"/g)||[]).length;
assert(nm>0 && nm===nl, `MathML formulas: ${nm}, all dir="ltr"`);
assert(!/katex-error/.test(html) && !/\$[^$<]+\$/.test(html), "no KaTeX error / raw $TeX$ in rendered HTML");

// practice: start, answer, feedback
$("#startBtn").click();
assert(!$("#screen-quiz").classList.contains("hidden"), "quiz screen shown");
assert($("#questionText").textContent.trim().length>0, "question text rendered");
const opts=$$("#optionsList .opt"); assert(opts.length>=2, `options rendered: ${opts.length}`);
opts[0].click();
assert(!$("#feedback").classList.contains("hidden"), "feedback after answering");
assert($$("#optionsList .opt.correct").length===1, "exactly one option marked correct");
// practice history: "back" replays the answered question as it was, "next" returns to where you were
{
  const qq = s => [...window.document.querySelectorAll(s)];
  const snap = () => $("#questionText").textContent + "|" + qq("#optionsList .opt").map(b => b.dataset.oid || b.textContent).join("|");
  const first = snap(), firstVerdict = $("#feedback .verdict").textContent;
  assert(!$("#prevBtn").classList.contains("hidden") && $("#prevBtn").disabled, "practice: back button visible but disabled on the first question");
  $("#nextBtn").click();
  const second = snap();
  assert(second !== first && $("#feedback").classList.contains("hidden"), "practice: next shows a fresh, unanswered question");
  assert(!$("#prevBtn").disabled, "practice: back button enabled after moving on");
  $("#prevBtn").click();
  assert(snap() === first, "practice: back shows the previous question with the same option order");
  assert(!$("#feedback").classList.contains("hidden") && $("#feedback .verdict").textContent === firstVerdict, "practice: previous question is shown as answered, with its feedback");
  assert(qq("#optionsList .opt").every(b => b.disabled) && !$("#nextBtn").classList.contains("hidden"), "practice: previous question is locked and next is available");
  $("#nextBtn").click();
  assert(snap() === second, "practice: next returns to the question you were on, same option order");
  window.document.dispatchEvent(new window.KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }));
  assert(snap() === first, "practice: ArrowRight goes back too");
}
$("#quitBtn").click();

// 'all others' option always renders last (check every question that has one)
let lastOk=true, checked=0;
for(const q of QS.filter(q=>q.options.some(o=>o.last))){
  window.startTopicPractice(q.topic);
  for(let k=0;k<60;k++){
    const shown=QS.find(x=>x.id===$("#questionText").dataset.qid);
    if(!shown){ lastOk=false; break; }
    if(shown.options.some(o=>o.last)){
      checked++;
      if($$("#optionsList .opt").pop().dataset.oid!==shown.options.find(o=>o.last).id) lastOk=false;
    }
    $$("#optionsList .opt")[0].click(); $("#nextBtn").click();
  }
  $("#quitBtn").click(); break;
}
assert(lastOk && checked>0, `'all others' option rendered last (${checked} renders checked)`);

// full exam replay of the first exam, answer every question correctly → full score
const code=QS[0].examCode, exam=QS.filter(q=>q.examCode===code);
const examRadio=$('input[name=mode][value="exam"]'); examRadio.checked=true; examRadio.dispatchEvent(new window.Event("change"));
$("#examPick").value=code; $("#examPick").dispatchEvent(new window.Event("change"));
$("#startBtn").click();
for(let i=0;i<exam.length;i++){
  const q=exam.find(x=>x.id===$("#questionText").dataset.qid);
  $$("#optionsList .opt").find(b=>b.dataset.oid===q.correctId).click();
  if(i<exam.length-1) $("#nextBtn").click();
}
$("#submitExamBtn").click();
assert(!$("#screen-results").classList.contains("hidden"), "results screen shown");
assert($("#resultsSummary").textContent.includes(`${exam.length} / ${exam.length}`), `perfect replay of ${code} scores ${exam.length}/${exam.length}`);
assert($$("#resultsReview .rev").length===exam.length, "review lists every question");
const imgQ=exam.filter(q=>q.image).length;
assert($$("#resultsReview .q-img").length===imgQ, `review shows all ${imgQ} diagrams`);

// ---- learn section (only once learn.js has been built from docs/briefs) ----
const LEARN=window.LEARN||[];
if(LEARN.length){
  const qIds=new Set(QS.map(q=>q.id)), topics=new Set(QS.map(q=>q.topic));
  const bh=LEARN.map(c=>c.html).join("");
  assert(LEARN.length===11, `learn chapters: ${LEARN.length}`);
  assert(LEARN.every(c=>c.html.length>2000), "every chapter has substantial content");
  assert(LEARN.every(c=>topics.has(c.topic)), "every chapter maps to a topic that has questions");
  assert(!/@@MATH\d+@@|math-fail/.test(bh), "all brief math rendered");
  const m1=(bh.match(/<math /g)||[]).length, m2=(bh.match(/<math dir="ltr"/g)||[]).length;
  assert(m1>100 && m1===m2, `brief MathML: ${m1}, all dir="ltr"`);
  const refs=[...bh.matchAll(/class="qref" data-q="([^"]+)"/g)].map(m=>m[1]);
  const dangling=[...new Set(refs)].filter(id=>!qIds.has(id));
  assert(refs.length>100, `question refs linked: ${refs.length}`);
  assert(dangling.length===0, `all question refs resolve${dangling.length?" DANGLING: "+dangling.slice(0,5).join(", "):""}`);
  const cids=new Set(LEARN.map(c=>c.id));
  const xr=[...new Set([...bh.matchAll(/class="xref" data-chapter="([^"]+)"/g)].map(m=>m[1]))];
  assert(xr.every(id=>cids.has(id)), `all ${xr.length} chapter cross-links resolve`);
  // open learn, peek a cited question, check it marks the right option, drill the topic
  $("#backHomeBtn").click();
  assert($("#learnEntry").style.display!=="none", "learn entry visible");
  $("#learnEntry").click();
  assert(!$("#screen-learn").classList.contains("hidden"), "learn screen shown");
  assert($$("#learnToc button").length===11, "TOC lists 11 chapters");
  const qr=$("#learnContent .qref"); assert(!!qr, "question chips render in the brief");
  qr.click();
  const pk=QS.find(q=>q.id===$("#qpeekId").textContent.trim());
  assert(!!pk && !$("#qpeek").classList.contains("hidden"), `peek opens on ${pk&&pk.id}`);
  const right=$$("#qpeekBody .qpeek-opts li.right").map(li=>li.dataset.oid);
  assert(right.length>=1 && right.includes(pk.correctId), "peek marks the correct option");
  $("#qpeekDrill").click();
  assert(!$("#screen-quiz").classList.contains("hidden") && QS.find(q=>q.id===$("#questionText").dataset.qid).topic===pk.topic,
    "peek → drill starts a practice session of that topic");
}

// ---- video course ("🎬 קורס וידאו"): boot the full page (every local script of index.html, in order) ----
{
  const html=fs.readFileSync(path.join(ROOT,"index.html"),"utf8");
  const vd=new JSDOM(html,{pretendToBeVisual:true,runScripts:"outside-only",url:"http://localhost/"});
  const w=vd.window; w.scrollTo=()=>{}; w.HTMLElement.prototype.scrollIntoView=()=>{}; w.confirm=()=>true;
  w.matchMedia=w.matchMedia||(q=>({matches:false,media:q,addEventListener(){},removeEventListener(){}}));
  const srcs=[...html.matchAll(/<script src="([^"?]+)(?:\?[^"]*)?"/g)].map(m=>m[1]).filter(s=>!/^https?:/.test(s));
  // one eval: app.js's top-level consts (QS, S, …) must be visible to the course/video scripts, as in a browser
  w.eval(srcs.map(s=>fs.readFileSync(path.join(ROOT,s),"utf8")).join("\n;\n"));
  const v$=s=>w.document.querySelector(s), v$$=s=>[...w.document.querySelectorAll(s)];
  const VC=w.VIDEO_COURSE, nV=VC?VC.courses.reduce((n,c)=>n+c.videos.length,0):0;
  assert(srcs.includes("videos.js") && srcs.includes("video-ui.js"), "index.html loads videos.js and video-ui.js");
  assert(nV===34 && VC.courses.map(c=>c.id).join()==="fa,nerode,classify,cf", `video manifest: ${nV} videos in 4 courses`);
  const lv=new Set(Object.values(w.COURSES).flatMap(c=>c.levels.map(L=>L.id)));
  assert(VC.courses.every(c=>c.videos.every(v=>lv.has(v.level))), "every video maps to an existing guided level");
  v$("#vidEntry").click();
  assert(!v$("#screen-video").classList.contains("hidden") && !v$("#vidListView").classList.contains("hidden"), "header entry opens the video list");
  const rows=v$$("#vidCourses .vid-row");
  assert(rows.length===34, `video list shows ${rows.length} videos`);
  const order=rows.map(r=>r.dataset.vid), k6=order.indexOf("K06");
  assert(order[k6+1]==="K06a" && order[k6+2]==="K06b" && order[k6+3]==="K07", "K06a/K06b listed right after K06");
  // player without a youtube id: local <video>, and on error the "not uploaded" note
  const noYt=VC.courses.flatMap(c=>c.videos).find(v=>!v.youtube);
  if(noYt){
    v$(`.vid-row[data-vid="${noYt.id}"]`).click();
    assert(!v$("#vidPlayView").classList.contains("hidden"), `player opens for ${noYt.id}`);
    const vel=v$("#vidFrame video");
    assert(!!vel && vel.getAttribute("src")===`videos/out/${noYt.id}/${noYt.id}.mp4` && !v$("#vidFrame iframe"), "no youtube id → local <video> fallback");
    vel.dispatchEvent(new w.Event("error"));
    assert(!!v$("#vidFrame .vid-missing") && /עוד לא הועלה/.test(v$("#vidFrame").textContent), "video load error → 'not uploaded yet' note");
  }
  // youtube embed (simulate an id), prev/next, watched mark, level link
  const first=w.VIDEO_UI.all[0]; first.youtube="AbCdEfGhIjK";
  w.VIDEO_UI.openVideo(first.id);
  const ifr=v$("#vidFrame iframe");
  assert(!!ifr && ifr.getAttribute("src").startsWith("https://www.youtube-nocookie.com/embed/AbCdEfGhIjK"), "youtube id → youtube-nocookie embed");
  delete first.youtube;
  assert(v$("#vidPrev").disabled && !v$("#vidNext").disabled, "first video: prev disabled, next enabled");
  v$("#vidNext").click();
  assert(v$("#vidHead").textContent.includes(w.VIDEO_UI.all[1].id), "next → second video");
  v$("#vidWatchBtn").click();
  const st=JSON.parse(w.localStorage.getItem("afq_video_v1")||"{}");
  assert(st.watched && st.watched[w.VIDEO_UI.all[1].id], "watched mark saved in afq_video_v1");
  assert(!w.localStorage.getItem("afq_progress_v1") || !/F0/.test(w.localStorage.getItem("afq_progress_v1")), "videos don't touch bank progress");
  v$("#vidBack").click();
  assert(v$(`.vid-row[data-vid="${w.VIDEO_UI.all[1].id}"]`).classList.contains("watched"), "list shows the ✓ for a watched video");
  w.VIDEO_UI.openVideo("K06b"); v$("#vidLevel").click();
  assert(!v$("#screen-course").classList.contains("hidden") && /K06|סגיר/.test(v$("#crsLesson").textContent), "bonus K06b → practice opens guided level K06");
  // lesson screen: K06 offers its video + both bonus videos; clicking opens the player, back returns to the lesson
  const lb=v$$("#crsLesson .vid-open").map(b=>b.dataset.vid);
  assert(lb.join()==="K06,K06a,K06b", `K06 lesson video buttons: ${lb.join()}`);
  v$('#crsLesson .vid-open[data-vid="K06"]').click();
  assert(!v$("#vidPlayView").classList.contains("hidden") && v$("#vidBack").textContent.includes("לשיעור"), "lesson button opens the K06 video");
  v$("#vidBack").click();
  assert(!v$("#crsLessonView").classList.contains("hidden"), "back from the player returns to the lesson");
  w.COURSE.openMap("fa"); w.COURSE.openLesson(w.COURSES.fa.levels[0]);
  assert(v$$("#crsLesson .vid-open").length===1, "F01 lesson has one video button");
  w.VIDEO_UI.openVideo("F01"); v$("#brandHome").click();
  assert(v$("#screen-video").classList.contains("hidden") && !v$("#screen-start").classList.contains("hidden"), "brand click from the player goes home");
}

console.log(fail===0?"\nDOM VERIFY PASSED":`\nDOM VERIFY FAILED (${fail})`); process.exit(fail?1:0);
