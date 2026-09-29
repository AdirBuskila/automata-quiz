"use strict";
/* Automata quiz — vanilla JS. Loads window.AUTOMATA_QUIZ = {meta, contexts, questions} from questions.js.
   Built on the databases-quiz engine:
   - shared context blocks referenced by contextId (a diagram / grammar / table used by several questions)
   - option objects {id, type, value, html}; all math is pre-rendered to MathML at build time,
     so this file never parses TeX — it only drops in the *Html strings the pipeline produced
   - answers stored by stable option id (correctId); options shuffled on every render, except
     `lockOrder` questions, and options flagged `last` ("כל הטענות האחרות…") always render last
   - duplicates are kept for full-exam replay; practice pools are de-duplicated by dedupKey      */

const DATA = (window.AUTOMATA_QUIZ && typeof window.AUTOMATA_QUIZ === "object") ? window.AUTOMATA_QUIZ : { contexts:{}, questions:[] };
const QS  = Array.isArray(DATA.questions) ? DATA.questions : [];
const CTX = (DATA.contexts && typeof DATA.contexts === "object") ? DATA.contexts : {};
const HE_KEYS = ["א","ב","ג","ד","ה","ו","ז","ח"];
const STORE = "afq_progress_v1";

// keep in sync with tools/build_questions.py TOPIC_LABEL and tools/validate.py TOPICS
const TOPICS = [
  ["all","כל הנושאים"],
  ["basics","מחרוזות, שפות ופעולות"],
  ["dfa","אס״ד"],
  ["nfa","אסל״ד ומסעי ε"],
  ["regex","ביטויים רגולריים"],
  ["reg_closure","תכונות סגירות (רגולריות)"],
  ["pumping_reg","למת הניפוח (רגולריות)"],
  ["nerode","נרוד · Rank · מינימיזציה"],
  ["cfg","דקדוקים חסרי הקשר"],
  ["pda","אוטומט מחסנית"],
  ["cfl_props","תכונות שפות ח״ה"],
  ["classify","סיווג שפות"],
];
const TOPIC_LABEL = Object.fromEntries(TOPICS.map(([k,l])=>[k,l]));

const SRC_NOTE = {
  "solution-pdf":"מקור התשובה: פתרון רשמי של המבחן",
  "solution-pdf-v2":"מקור התשובה: פתרון רשמי (גרסה אחרת של אותו מבחן, הותאם לפי תוכן)",
  "merged-pdf":"מקור התשובה: קובץ איגוד מבחנים עם תשובות",
  "moodle-feedback":"מקור התשובה: משוב \"התשובה הנכונה\" במודל",
  "moodle-100":"מקור התשובה: ניסיון במודל שקיבל ציון 100",
};

/* ---------- storage ---------- */
function loadProgress(){
  try{ return JSON.parse(localStorage.getItem(STORE)) || {stats:{answered:0,correct:0},perQ:{}}; }
  catch(e){ return {stats:{answered:0,correct:0},perQ:{}}; }
}
function saveProgress(){ try{ localStorage.setItem(STORE, JSON.stringify(P)); }catch(e){} }
let P = loadProgress();

/* ---------- helpers ---------- */
const $ = s => document.querySelector(s);
function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function show(id){ document.querySelectorAll(".screen").forEach(s=>s.classList.add("hidden")); $("#"+id).classList.remove("hidden"); window.scrollTo({top:0,behavior:"smooth"}); }
function escapeHtml(s){ return String(s).replace(/[&<>]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[m])); }
function optById(q,id){ return (q.options||[]).find(o=>o.id===id); }
function acceptedIdsOf(q){ return (Array.isArray(q.acceptedIds) && q.acceptedIds.length) ? q.acceptedIds : [q.correctId]; }
function isAccepted(q,id){ return id!=null && acceptedIdsOf(q).includes(id); }

function filterMatch(q, topic, opts){
  if(topic!=="all" && q.topic!==topic) return false;
  if(opts.officialOnly && !q.official) return false;
  if(opts.mistakesOnly){ const r=P.perQ[q.id]; if(!r || r.correct) return false; }
  return true;
}
/* The same question can appear in several exams (and in Moodle). Whole-exam mode replays
   every copy; practice pools keep one per dedupKey so a drill doesn't repeat itself. */
function dedupePool(arr){
  const seen=new Set();
  return arr.filter(q=>{ const k=q.dedupKey||q.id; if(seen.has(k)) return false; seen.add(k); return true; });
}
function filteredPool(topic, opts){ return dedupePool(QS.filter(q=>filterMatch(q, topic, opts))); }
function countFor(topic, opts){ return filteredPool(topic, opts).length; }

/* ---------- rendering (HTML comes pre-built from the pipeline) ---------- */
function contextHtml(ctx){ return ctx ? `<div class="ctx ctx-${ctx.kind||"text"}">${ctx.html}</div>` : ""; }
function extrasHtml(q){
  return q.image ? `<figure class="q-fig"><img class="q-img" src="${q.image}" alt="תרשים לשאלה" loading="lazy"></figure>` : "";
}
function optionHtml(o){ return o ? (o.html || escapeHtml(o.value)) : ""; }

/* ---------- session state ---------- */
const S = { mode:"practice", topic:"all", pool:[], pos:0, current:null,
  exam:{count:18, minutes:150, answers:{}, endAt:0, timer:null} };

/* ---------- start screen ---------- */
function renderTopStats(){
  const a=P.stats.answered, c=P.stats.correct;
  const pct=a?Math.round(c/a*100):0;
  $("#topStats").innerHTML =
    `<div class="stat">נענו <b>${a}</b></div>`+
    `<div class="stat">דיוק <b>${pct}%</b></div>`+
    `<div class="stat">במאגר <b>${QS.length}</b></div>`;
}
function selectedOpts(){ return { officialOnly: $("#officialOnly").checked, mistakesOnly: $("#mistakesOnly").checked }; }
function renderTopicGrid(){
  const opts=selectedOpts();
  $("#topicGrid").innerHTML = TOPICS.map(([k,label])=>{
    const n=countFor(k, opts);
    const active = k===S.topic ? "active":"";
    const dis = n===0 && k!=="all" ? "disabled":"";
    return `<button class="topic-btn ${active}" data-topic="${k}" ${dis}>
      <span>${label}</span><span class="cnt">${n}</span></button>`;
  }).join("");
  document.querySelectorAll(".topic-btn").forEach(b=>{
    b.onclick=()=>{ S.topic=b.dataset.topic; renderTopicGrid(); updatePoolInfo(); };
  });
}
function selectedExam(){ const el=$("#examPick"); return (S.mode==="exam" && el) ? el.value : ""; }
function examQuestions(code){ return QS.filter(q=>q.examCode===code); }
function examLabelOf(q){ return q.examLabel || q.examCode || ""; }
/* Exam-picker order: sample papers and Moodle quizzes first (no place in the chronology),
   then real exams oldest→newest, newest at the bottom — same rule as the sibling apps. */
function examOrder(code){
  const c=String(code);
  if(/^(SAMP|MQ)/.test(c)) return [0, /^MQ/.test(c)?1:0, c];
  const m=c.match(/^(\d{2})/);
  return [1, m?2000+parseInt(m[1],10):9999, c];
}
function byExamOrder(a,b){
  const x=examOrder(a), y=examOrder(b);
  return (x[0]-y[0]) || (x[1]-y[1]) || String(x[2]).localeCompare(String(y[2]));
}
function populateExamPick(){
  const sel=$("#examPick"); if(!sel) return;
  const seen=new Map();
  QS.forEach(q=>{ if(q.examCode && !seen.has(q.examCode)) seen.set(q.examCode, examLabelOf(q)); });
  sel.innerHTML = `<option value="">אקראי (כל המאגר)</option>` +
    [...seen.entries()].sort((a,b)=>byExamOrder(a[0],b[0]))
      .map(([code,label])=>`<option value="${code}">${escapeHtml(label)} (${examQuestions(code).length})</option>`).join("");
  sel.onchange=()=>{ syncExamOpts(); updatePoolInfo(); };
}
function syncExamOpts(){ const wrap=$("#examCountWrap"); if(wrap) wrap.style.display = selectedExam() ? "none" : ""; }
function updatePoolInfo(){
  const code=selectedExam();
  if(code){
    const n=examQuestions(code).length;
    const label=examLabelOf(QS.find(q=>q.examCode===code)||{});
    $("#poolInfo").textContent = `מבחן ${label} — ${n} שאלות (מבחן מלא).`;
    $("#startBtn").disabled = n===0;
    return;
  }
  const opts=selectedOpts();
  const pool=filteredPool(S.topic,opts);
  const off=pool.filter(q=>q.official).length;
  $("#poolInfo").textContent = `נבחרו ${pool.length} שאלות (${off} מפתרון רשמי של מבחן, ${pool.length-off} ממבדקי מודל).`;
  $("#startBtn").disabled = pool.length===0;
}
function initStart(){
  renderTopStats();
  populateExamPick();
  renderTopicGrid();
  syncExamOpts();
  updatePoolInfo();
  document.querySelectorAll('input[name=mode]').forEach(r=>{
    r.onchange=()=>{ S.mode=document.querySelector('input[name=mode]:checked').value;
      $("#examOpts").classList.toggle("hidden", S.mode!=="exam");
      $("#mistakesOnly").parentElement.style.display = S.mode==="exam"?"none":"";
      syncExamOpts(); updatePoolInfo();
    };
  });
  $("#officialOnly").onchange = ()=>{ renderTopicGrid(); updatePoolInfo(); };
  $("#mistakesOnly").onchange = ()=>{ renderTopicGrid(); updatePoolInfo(); };
  $("#startBtn").onclick = startSession;
  const years=QS.map(q=>q.year).filter(Boolean);
  $("#datasetInfo").textContent = `${QS.length} שאלות` + (years.length?` · ${Math.min(...years)}–${Math.max(...years)}`:"");
}

/* ---------- session ---------- */
function startSession(){
  S._views=null;
  const opts=selectedOpts();
  const pickedExam = selectedExam();
  let pool;
  if(pickedExam){
    pool = examQuestions(pickedExam).slice().sort((a,b)=>a.num-b.num);
  } else {
    pool = shuffle(filteredPool(S.topic, opts));
  }
  if(S.mode==="exam"){
    if(pickedExam){ S.exam.count = pool.length; }
    else { S.exam.count = Math.min(parseInt($("#examCount").value,10), pool.length); pool = pool.slice(0, S.exam.count); }
    S.exam.minutes = parseInt($("#examMinutes").value,10);
    S.exam.answers = {};
    S.exam.endAt = Date.now() + S.exam.minutes*60000;
    startTimer();
  }
  S.pool = pool; S.pos = 0;
  $("#prevBtn").classList.toggle("hidden", S.mode!=="exam");
  show("screen-quiz");
  renderQuestion();
}
/* single entry point into a topic drill: ?practice=<key>, learn-mode buttons */
function startTopicPractice(t){
  if(!TOPICS.some(([k])=>k===t)) return;
  S.mode="practice"; S.topic=t;
  const r=document.querySelector('input[name=mode][value="practice"]'); if(r) r.checked=true;
  $("#examOpts").classList.add("hidden");
  $("#officialOnly").checked=false; $("#mistakesOnly").checked=false;
  renderTopicGrid(); updatePoolInfo();
  startSession();
}

window.startTopicPractice = startTopicPractice;   // used by learn mode + tests

/* Display order: shuffle by stable option id, then append the `last` options
   ("כל הטענות האחרות לא נכונות") so they keep meaning "the others". lockOrder = source order. */
function viewOrder(q){
  const opts=q.options||[];
  if(q.lockOrder) return opts.map(o=>o.id);
  const free=opts.filter(o=>!o.last).map(o=>o.id), pinned=opts.filter(o=>o.last).map(o=>o.id);
  return shuffle(free).concat(pinned);
}
function makeView(q){
  const order = viewOrder(q);
  const correctSet = new Set(order.map((id,i)=>isAccepted(q,id)?i:-1).filter(i=>i>=0));
  return { q, order, correctSet, answered:false, chosen:null };
}

function renderQuestion(){
  const q = S.pool[S.pos];
  if(S.mode==="exam"){
    S.current = S._views?.[q.id] || makeView(q);
    (S._views ||= {})[q.id] = S.current;
  } else {
    S.current = makeView(q);
  }
  const v=S.current;

  $("#qTopic").textContent = q.topicLabel || TOPIC_LABEL[q.topic] || q.topic;
  $("#qSource").textContent = `${examLabelOf(q)} · שאלה ${q.num}`;
  const badge=$("#qBadge");
  badge.textContent = q.official ? "מפתרון רשמי" : "מפתח מודל";
  badge.className = "chip " + (q.official?"official":"unofficial");

  $("#qContext").innerHTML = q.contextId ? contextHtml(CTX[q.contextId]) : "";
  $("#questionText").innerHTML = q.questionHtml;
  $("#questionText").dataset.qid = q.id;
  $("#qExtras").innerHTML = extrasHtml(q);

  $("#optionsList").innerHTML = v.order.map((oid,disp)=>
    `<button class="opt" data-disp="${disp}" data-oid="${oid}">
       <span class="key">${HE_KEYS[disp]||disp+1}</span>
       <span class="txt">${optionHtml(optById(q,oid))}</span>
     </button>`).join("");
  document.querySelectorAll(".opt").forEach(b=> b.onclick=()=>choose(parseInt(b.dataset.disp,10)));

  const fb=$("#feedback"); fb.className="feedback hidden";

  if(S.mode==="exam" && q.id in S.exam.answers){
    markExamChoice(v.order.indexOf(S.exam.answers[q.id]));
  }

  $("#progressFill").style.width = ((S.pos)/(S.pool.length))*100 + "%";
  if(S.mode==="exam"){
    $("#quizMeta").innerHTML = `שאלה ${S.pos+1}/${S.pool.length} <span id="tmr" class="timer"></span>`;
    renderTimer();
    $("#nextBtn").classList.toggle("hidden", S.pos>=S.pool.length-1);
    $("#submitExamBtn").classList.toggle("hidden", S.pos<S.pool.length-1);
    $("#prevBtn").disabled = S.pos===0;
    $("#streakBox").textContent = `נענו ${Object.keys(S.exam.answers).length}/${S.pool.length}`;
  } else {
    $("#quizMeta").textContent = `שאלה ${S.pos+1}`;
    $("#nextBtn").classList.add("hidden");
    $("#submitExamBtn").classList.add("hidden");
    const a=P.stats.answered,c=P.stats.correct;
    $("#streakBox").textContent = `רצף נכון: ${S.streak||0} · דיוק כולל ${a?Math.round(c/a*100):0}%`;
  }
}

/* ---------- answering ---------- */
function choose(disp){
  const v=S.current, q=v.q;
  if(S.mode==="exam"){
    S.exam.answers[q.id] = v.order[disp];   // store chosen option id
    markExamChoice(disp);
    $("#streakBox").textContent = `נענו ${Object.keys(S.exam.answers).length}/${S.pool.length}`;
    return;
  }
  if(v.answered) return;
  v.answered=true; v.chosen=disp;
  const correct = v.correctSet.has(disp);
  document.querySelectorAll(".opt").forEach((b,i)=>{
    b.disabled=true;
    if(v.correctSet.has(i)) b.classList.add("correct");
    else if(i===disp) b.classList.add("wrong");
  });
  recordAnswer(q, correct);
  S.streak = correct ? (S.streak||0)+1 : 0;
  const fb=$("#feedback");
  fb.className = "feedback " + (correct?"good":"bad");
  const srcNote = SRC_NOTE[q.answerSource] || "";
  fb.innerHTML = `<div class="verdict">${correct?"✓ נכון":"✗ לא נכון"}</div>`+
    `<div class="expl">${q.explanationHtml||""}</div>`+
    (srcNote?`<span class="note">${escapeHtml(srcNote)}</span>`:"")+
    `<span class="note">מקור: ${escapeHtml(examLabelOf(q))}, שאלה ${q.num}</span>`;
  $("#nextBtn").classList.remove("hidden");
  $("#nextBtn").focus();
  renderTopStats();
  const a=P.stats.answered,c=P.stats.correct;
  $("#streakBox").textContent = `רצף נכון: ${S.streak} · דיוק כולל ${a?Math.round(c/a*100):0}%`;
}
function markExamChoice(disp){ document.querySelectorAll(".opt").forEach((b,i)=> b.classList.toggle("chosen-exam", i===disp)); }
function recordAnswer(q, correct){ P.stats.answered++; if(correct) P.stats.correct++; P.perQ[q.id]={correct, t:Date.now()}; saveProgress(); }

/* ---------- navigation ---------- */
function next(){
  if(S.mode==="practice"){
    if(!S.current.answered) return;
    if(S.pos>=S.pool.length-1){ S.pool = shuffle(S.pool); S.pos=0; } else S.pos++;
    renderQuestion();
  } else {
    if(S.pos<S.pool.length-1){ S.pos++; renderQuestion(); }
  }
}
function prev(){ if(S.mode==="exam" && S.pos>0){ S.pos--; renderQuestion(); } }

/* ---------- timer (exam) ---------- */
function startTimer(){ clearInterval(S.exam.timer); S.exam.timer=setInterval(renderTimer,1000); }
function renderTimer(){
  const el=$("#tmr"); if(!el) return;
  let ms=S.exam.endAt-Date.now();
  if(ms<=0){ ms=0; clearInterval(S.exam.timer); submitExam(true); return; }
  const m=Math.floor(ms/60000), s=Math.floor(ms%60000/1000);
  el.textContent = `⏱ ${m}:${String(s).padStart(2,"0")}`;
  el.classList.toggle("danger", ms<60000);
}

/* ---------- exam grading ---------- */
function submitExam(auto){
  clearInterval(S.exam.timer);
  if(!auto){
    const unans=S.pool.length-Object.keys(S.exam.answers).length;
    if(unans>0 && !confirm(`נותרו ${unans} שאלות ללא מענה. להגיש בכל זאת?`)){ startTimer(); return; }
  }
  let correct=0; const byTopic={}; const review=[];
  S.pool.forEach(q=>{
    const chosen = q.id in S.exam.answers ? S.exam.answers[q.id] : null;  // option id or null
    const ok = isAccepted(q, chosen);
    if(ok) correct++;
    recordAnswer(q, ok);
    (byTopic[q.topic] ||= {n:0,c:0}); byTopic[q.topic].n++; if(ok) byTopic[q.topic].c++;
    review.push({q, chosen, ok});
  });
  renderResults(correct, byTopic, review);
  renderTopStats();
  show("screen-results");
}
function renderResults(correct, byTopic, review){
  const total=S.pool.length, pct=Math.round(correct/total*100);
  $("#resultsSummary").innerHTML =
    `<div class="scorering" style="--p:${pct}"><span>${pct}%</span></div>`+
    `<div class="txt"><b>${correct} / ${total}</b> תשובות נכונות<br>`+
    `<span style="color:var(--muted)">${pct>=60?"עברת! 🎉":"עוד קצת תרגול 💪"}</span></div>`;
  $("#resultsByTopic").innerHTML = Object.entries(byTopic).map(([t,o])=>{
    const lbl=TOPIC_LABEL[t]||t; const p=Math.round(o.c/o.n*100);
    return `<div class="tline"><span>${lbl}</span><span class="tbar"><i style="width:${p}%"></i></span><span>${o.c}/${o.n}</span></div>`;
  }).join("");
  $("#resultsReview").innerHTML = review.map(r=>{
    const v=r.q;
    const chosenTxt = r.chosen!=null ? optionHtml(optById(v,r.chosen)) : "— לא נענתה —";
    const acc = acceptedIdsOf(v);
    const correctTxt = acc.map(id=>optionHtml(optById(v,id))).join(`<span class="or">או</span>`);
    return `<div class="rev ${r.ok?"ok":"bad"}">
      <div class="rq">${v.questionHtml}</div>
      ${v.contextId?contextHtml(CTX[v.contextId]):""}
      ${extrasHtml(v)}
      <div class="ra"><span class="${r.ok?"good":"miss"}">תשובתך: ${chosenTxt}</span>`+
      (r.ok?"":` · <span class="good">${acc.length>1?"נכונות":"הנכונה"}: ${correctTxt}</span>`)+
      `<br>${v.explanationHtml||""}</div></div>`;
  }).join("");
}

/* ---------- controls ---------- */
function quit(){ clearInterval(S.exam.timer); S._views=null; S.streak=0; initStart(); show("screen-start"); }
function bindGlobal(){
  $("#nextBtn").onclick=next;
  $("#prevBtn").onclick=prev;
  $("#submitExamBtn").onclick=()=>submitExam(false);
  $("#quitBtn").onclick=()=>{ if(S.mode!=="exam"||confirm("לצאת מהמבחן? ההתקדמות לא תישמר.")) quit(); };
  $("#backHomeBtn").onclick=quit;
  function goHome(){
    const inExamQuiz = S.mode==="exam" && !$("#screen-quiz").classList.contains("hidden");
    if(inExamQuiz && !confirm("לצאת מהמבחן? ההתקדמות לא תישמר.")) return;
    quit();
  }
  const brand=$("#brandHome");
  if(brand){
    brand.style.cursor="pointer";
    brand.onclick=goHome;
    brand.onkeydown=e=>{ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); goHome(); } };
  }
  $("#resetProgress").onclick=()=>{ if(confirm("לאפס את כל ההתקדמות וההיסטוריה?")){ P={stats:{answered:0,correct:0},perQ:{}}; saveProgress(); renderTopStats(); renderTopicGrid(); updatePoolInfo(); } };
  // click any figure (question / context / option) to zoom
  const lb=$("#lightbox"), lbImg=$("#lightboxImg"), lbClose=$("#lightboxClose");
  document.addEventListener("click", e=>{
    const img=e.target.closest(".q-img"); if(!img || e.target.closest(".opt:not(:disabled)")) return;
    lbImg.src=img.src; lbImg.alt=img.alt||""; lb.classList.remove("hidden");
  });
  function closeLb(){ lb.classList.add("hidden"); lbImg.src=""; }
  lb.addEventListener("click", e=>{ if(e.target===lb) closeLb(); });
  lbClose.onclick=closeLb;
  document.addEventListener("keydown",e=>{
    if(!lb.classList.contains("hidden")){ if(e.key==="Escape") closeLb(); return; }
    if($("#screen-quiz").classList.contains("hidden")) return;
    if(/^[1-8]$/.test(e.key)){ const b=document.querySelector(`.opt[data-disp="${+e.key-1}"]`); if(b && !b.disabled) b.click(); }
    else if(e.key==="Enter"){ if(!$("#nextBtn").classList.contains("hidden")) next(); else if(!$("#submitExamBtn").classList.contains("hidden")) submitExam(false); }
    else if(e.key==="ArrowLeft" && !$("#nextBtn").classList.contains("hidden")) next();
    else if(e.key==="ArrowRight" && S.mode==="exam") prev();
  });
}

/* ---------- theme toggle ---------- */
(function initTheme(){
  const THEME_KEY = "afq_theme";
  const btn = document.getElementById("themeToggle");
  if(!btn) return;
  const root = document.documentElement;
  const systemDark = () => !window.matchMedia || !window.matchMedia("(prefers-color-scheme: light)").matches;
  const effective = () => root.dataset.theme || (systemDark() ? "dark" : "light");
  const paint = () => { btn.textContent = effective()==="dark" ? "🌙" : "☀️"; };
  paint();
  btn.addEventListener("click", () => {
    const next = effective()==="dark" ? "light" : "dark";
    root.dataset.theme = next;
    try{ localStorage.setItem(THEME_KEY, next); }catch(e){}
    paint();
  });
  if(window.matchMedia){
    window.matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => { if(!root.dataset.theme) paint(); });
  }
})();

/* ---------- learning section (docs/briefs -> learn.js; ported from machine-learning-quiz) ---------- */
(function initLearn(){
  const data = Array.isArray(window.LEARN) ? window.LEARN : [];
  const entry = document.getElementById("learnEntry");
  const screen = document.getElementById("screen-learn");
  if(!entry || !screen) return;
  if(!data.length){ entry.style.display = "none"; return; }

  const toc=$("#learnToc"), content=$("#learnContent"), fill=$("#learnProgressFill"), pos=$("#learnPos");
  const prevB=$("#learnPrev"), nextB=$("#learnNext"), toggle=$("#learnTocToggle"), backdrop=$("#learnBackdrop");
  const backB=$("#learnBackBtn"), lb=$("#lightbox"), lbImg=$("#lightboxImg");
  const ALL={officialOnly:false, mistakesOnly:false};
  let idx=0, built=false;

  function buildToc(){
    toc.innerHTML = data.map((s,i)=>`<button data-i="${i}"${s.sub?' class="sub"':''}>${escapeHtml(s.title)}</button>`).join("");
    toc.querySelectorAll("button").forEach(b=> b.onclick=()=>{ go(+b.dataset.i); closeDrawer(); });
    built=true;
  }
  function go(i){
    idx=Math.max(0,Math.min(data.length-1,i));
    const s=data[idx];
    // each brief is written to be read then drilled, so surface the drill entry point
    const n = s.topic ? countFor(s.topic, ALL) : 0;
    const drill = n ? `<button class="btn primary learn-drill" data-topic="${s.topic}">תרגל נושא זה ▶ <span class="n">${n}</span></button>` : "";
    content.innerHTML = `<div class="learn-head"><h2 class="learn-h">${escapeHtml(s.title)}</h2>${drill}</div>` + s.html;
    toc.querySelectorAll("button").forEach((b,j)=> b.classList.toggle("active", j===idx));
    const active=toc.querySelector("button.active"); if(active) active.scrollIntoView({block:"nearest"});
    markScrollable();
    fill.style.width = ((idx+1)/data.length*100)+"%";
    pos.textContent = `${idx+1} / ${data.length}`;
    prevB.disabled=idx===0; nextB.disabled=idx===data.length-1;
    window.scrollTo({top:0,behavior:"smooth"}); content.focus({preventScroll:true});
  }
  /* a clipped formula or table reads as broken unless it shows it scrolls (edge shadow) */
  function markScrollable(){
    content.querySelectorAll(".math-block,.tbl-wrap").forEach(el=>
      el.classList.toggle("scrollable", el.scrollWidth > el.clientWidth + 1));
  }
  let rzT;
  window.addEventListener("resize", ()=>{ clearTimeout(rzT); rzT=setTimeout(()=>{ if(!screen.classList.contains("hidden")) markScrollable(); },150); });

  function openLearn(){ if(!built) buildToc(); show("screen-learn"); go(idx); }
  function setDrawer(open){ toc.classList.toggle("open",open); backdrop.classList.toggle("hidden",!open); toggle.setAttribute("aria-expanded", open?"true":"false"); }
  function closeDrawer(){ setDrawer(false); }

  entry.onclick=openLearn;
  backB.onclick=()=>{ closeDrawer(); show("screen-start"); };
  prevB.onclick=()=>go(idx-1);
  nextB.onclick=()=>go(idx+1);
  toggle.onclick=()=>setDrawer(!toc.classList.contains("open"));
  backdrop.onclick=closeDrawer;

  /* ----- question peek: click a `26A-A-Q7` chip inside a brief ----- */
  const peek=$("#qpeek"), peekBody=$("#qpeekBody"), peekDrill=$("#qpeekDrill");
  let peekTopic=null;
  function openPeek(id){
    const q=QS.find(x=>x.id===id); if(!q) return;
    $("#qpeekId").textContent = q.id;
    $("#qpeekSource").textContent = `${examLabelOf(q)} · שאלה ${q.num}`;
    const badge=$("#qpeekBadge");
    badge.textContent = q.official ? "מפתרון רשמי" : "מפתח מודל";
    badge.className = "chip " + (q.official?"official":"unofficial");
    // printed order with the answer marked — the brief discusses this exact question
    const acc=acceptedIdsOf(q);
    peekBody.innerHTML =
      (q.contextId?contextHtml(CTX[q.contextId]):"") +
      `<div class="qpeek-q">${q.questionHtml}</div>` + extrasHtml(q) +
      `<ol class="qpeek-opts">` + q.options.map((o,i)=>
        `<li class="${acc.includes(o.id)?"right":""}" data-oid="${o.id}"><span class="key">${HE_KEYS[i]||i+1}</span>`+
        `<span class="txt">${optionHtml(o)}</span></li>`).join("") + `</ol>` +
      (q.explanationHtml ? `<div class="qpeek-exp"><strong>הסבר:</strong> ${q.explanationHtml}</div>` : "");
    peekTopic=q.topic;
    peekDrill.classList.toggle("hidden", !countFor(q.topic, ALL));
    peek.classList.remove("hidden");
    $("#qpeekClose").focus({preventScroll:true});
  }
  function closePeek(){ peek.classList.add("hidden"); peekBody.innerHTML=""; peekTopic=null; }
  const peekOpen=()=>!peek.classList.contains("hidden");
  peek.addEventListener("click", e=>{ if(e.target===peek) closePeek(); });
  $("#qpeekClose").onclick=closePeek;
  peekDrill.onclick=()=>{ const t=peekTopic; closePeek(); closeDrawer(); startTopicPractice(t); };

  content.addEventListener("click", e=>{
    const img=e.target.closest(".learn-fig img");
    if(img){ lbImg.src=img.src; lbImg.alt=img.alt||""; lb.classList.remove("hidden"); return; }
    const qref=e.target.closest(".qref"); if(qref){ openPeek(qref.dataset.q); return; }
    const xref=e.target.closest(".xref");
    if(xref){ const j=data.findIndex(c=>c.id===xref.dataset.chapter); if(j>=0) go(j); return; }
    const drill=e.target.closest(".learn-drill"); if(drill){ closeDrawer(); startTopicPractice(drill.dataset.topic); }
  });
  document.addEventListener("keydown", e=>{
    if(!lb.classList.contains("hidden")) return;           // bindGlobal handles the lightbox
    if(peekOpen()){ if(e.key==="Escape") closePeek(); return; }
    if(screen.classList.contains("hidden")) return;
    if(e.key==="ArrowLeft") go(idx+1);
    else if(e.key==="ArrowRight") go(idx-1);
    else if(e.key==="Escape"){ closeDrawer(); show("screen-start"); }
  });
})();

/* ---------- deep link (index.html?practice=<topicKey>) ---------- */
function autoStartFromURL(){
  let t;
  try{ t = new URLSearchParams(location.search).get("practice"); }catch(e){ return; }
  if(!t || !TOPICS.some(([k])=>k===t)) return;
  if(countFor(t,{officialOnly:false,mistakesOnly:false})===0) return;
  startTopicPractice(t);
}

/* ---------- boot ---------- */
if(!QS.length){
  document.getElementById("app").innerHTML="<div class='card'><h2>לא נטענו שאלות</h2><p>ודאו ש-<code>questions.js</code> נמצא לצד הדף.</p></div>";
}else{
  initStart(); bindGlobal(); autoStartFromURL();
}
