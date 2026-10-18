// Guided courses ("צריך עזרה?"): data lint + index.html script-tag sync.
// usage: node tools/course_check.js            lint every course, fail on any error
//        node tools/course_check.js --sync     also rewrite the COURSE LEVELS script block in index.html
//        node tools/course_check.js --dump fa [F03]   print the questions with their keyed answer, for review
// The level files are GENERATED (tools/build_courses.py from tools/needhelp/<course>/<ID>.py).
const fs = require("fs"), path = require("path"), vm = require("vm");
const ROOT = path.join(__dirname, "..");
const args = process.argv.slice(2);

const COURSE_TOPICS = { fa: ["dfa", "nfa", "regex"], nerode: ["nerode"],
  classify: ["classify", "pumping_reg", "reg_closure", "cfl_props"], cf: ["cfg", "pda"] };
const PREFIX = { fa: "F", nerode: "N", classify: "K", cf: "G" };

const files = Object.keys(COURSE_TOPICS).flatMap(c => {
  const dir = path.join(ROOT, "courses", c);
  return fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /\.js$/.test(f)).sort().map(f => `courses/${c}/${f}`) : [];
});

const ctx = { console }; ctx.window = ctx;   // browser globals: window.X and bare X are the same
vm.createContext(ctx);
const load = f => vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
load("questions.js"); load("courses.js");
files.forEach(load);
const BANK = ctx.window.AUTOMATA_QUIZ.questions, byId = new Map(BANK.map(q => [q.id, q]));
const COURSES = ctx.window.COURSES;

let bad = 0; const err = (...a) => { console.log("ERROR", ...a); bad++; };
const warn = (...a) => console.log("warn ", ...a);
const QID = /\b[A-Z0-9]+(?:-[A-Z0-9]+)?-Q\d+\b/g;
const strip = h => String(h || "").replace(/<annotation[\s\S]*?<\/annotation>/g, "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
const refsIn = h => [...strip(h).matchAll(QID)].map(m => m[0]).filter(id => byId.has(id));
const tagBalance = html => {
  const T = "div|table|ul|ol|p|h3|h4|b|strong|code|span|li|tr|td|th|thead|tbody|math|mrow|bdi";
  const opens = (html.match(new RegExp(`<(${T})\\b[^>]*?(?<!/)>`, "g")) || []).length;
  const closes = (html.match(new RegExp(`</(${T})>`, "g")) || []).length;
  return [opens, closes];
};
const RAW = /\$|\*\*|\\[a-zA-Z]{2,}|\^\{|_\{|&amp;|&lt;[a-z]/;   // unrendered TeX / markdown in a rendered string

let total = 0, totalBank = 0, nMath = 0; const cited = new Set(), qIds = new Set(), bossIds = new Set(), lessonCited = new Set();
Object.keys(COURSE_TOPICS).forEach(cid => {
  const LV = (COURSES[cid] || { levels: [] }).levels;
  if (!LV.length) { warn(cid, "has no levels yet"); return; }
  if (LV.length < 6 || LV.length > 10) err(cid, `${LV.length} levels (want 6-10)`);
  const lvIds = new Set(), orders = new Set();
  LV.forEach((L, i) => {
    const W = `${cid}/${L.id}`;
    if (!new RegExp(`^${PREFIX[cid]}\\d\\d$`).test(L.id)) err(W, `level id must look like ${PREFIX[cid]}01`);
    if (lvIds.has(L.id)) err(W, "duplicate level id"); lvIds.add(L.id);
    if (orders.has(L.order)) err(W, "duplicate order"); orders.add(L.order);
    if (L.order !== i + 1) err(W, `order ${L.order} but position ${i + 1} (orders must be 1..n)`);
    ["title", "goal", "icon"].forEach(k => { if (!L[k]) err(W, "missing", k); });
    if (L.boss && i !== LV.length - 1) err(W, "boss level must be last");
    if (i === LV.length - 1 && !L.boss) err(W, "the last level must be the boss");
    const html = L.lessonHtml || "";
    if (html.length < 600) err(W, `lesson too short (${html.length} chars)`);
    if (RAW.test(strip(html).replace(/·/g, ""))) err(W, "lesson has unrendered TeX/markdown:", (strip(html).match(RAW) || [])[0]);
    const [o, c] = tagBalance(html);
    if (o !== c) err(W, `lesson html tag balance off: ${o} opens vs ${c} closes`);
    nMath += (html.match(/<math\b/g) || []).length;
    const lref = refsIn(html);
    lref.forEach(id => { cited.add(id); lessonCited.add(id); });
    if (!L.boss && lref.length < 2) err(W, "lesson cites fewer than 2 exam questions (ground it in the exams)");
    const qs = L.questions || [];
    if (qs.length < 4 || qs.length > 6) err(W, `has ${qs.length} questions (want 4-6)`);
    if (L.boss && !qs.every(q => q.bankId)) err(W, "boss level must be bank questions only");
    if (!L.boss && qs.some(q => q.bankId)) err(W, "only the boss level pulls bank questions");
    qs.forEach((q, j) => {
      total++;
      if (q.bankId) {
        totalBank++;
        const b = byId.get(q.bankId), w = `${W} bank ${q.bankId}`;
        if (!b) return err(w, "unknown bank question");
        if (!COURSE_TOPICS[cid].includes(b.topic)) warn(w, `bank topic ${b.topic} is outside this course`);
        if (!q.recapHtml) err(w, "missing recap");
        if (qIds.has(`${L.id}:${q.bankId}`)) err(w, "same exam question twice in a level"); qIds.add(`${L.id}:${q.bankId}`);
        bossIds.add(q.bankId); cited.add(q.bankId);
        return;
      }
      const w = `${W} ${q.id || "#" + (j + 1)}`;
      if (!q.id || !q.id.startsWith(L.id + "-Q")) err(w, `question id must start with ${L.id}-Q`);
      if (qIds.has(q.id)) err(w, "duplicate question id"); qIds.add(q.id);
      if (!q.questionHtml) err(w, "missing question");
      if (!q.recapHtml) err(w, "missing recap");
      if (strip(q.explanationHtml).length < 40) err(w, "missing/short explanation");
      const op = q.options || [];
      if (op.length < 3 || op.length > 5) err(w, `${op.length} options (want 3-5)`);
      if (op.filter(x => x.id === q.correctId).length !== 1) err(w, "correctId does not name exactly one option:", q.correctId);
      if (new Set(op.map(x => x.id)).size !== op.length) err(w, "duplicate option ids");
      op.forEach((x, k) => { if (!x.html || !strip(x.html)) err(w, "empty option", k); });
      if (new Set(op.map(x => strip(x.html))).size !== op.length) err(w, "two options have identical text");
      if (op.some(x => /^(תשובות?|אפשרויות?) [א-ו]( |$)|[א-ו] ו-?[א-ו] נכונות/.test(strip(x.html)))) err(w, "option cites siblings by letter (options are shuffled)");
      if (refsIn(q.questionHtml).length) err(w, "question stem cites an exam id (the peek would reveal the answer)");
      refsIn(q.explanationHtml).forEach(id => cited.add(id));
      ["questionHtml", "explanationHtml", "recapHtml"].concat(op.map((_, k) => `opt${k}`)).forEach(k => {
        const s = k.startsWith("opt") ? op[+k.slice(3)].html : q[k];
        if (RAW.test(strip(s))) err(w, k, "has unrendered TeX/markdown:", (strip(s).match(RAW) || [])[0]);
      });
      nMath += (JSON.stringify(q).match(/<math\b/g) || []).length;
    });
  });
});
// a boss question must not be revealed by a lesson or an explanation elsewhere (the peek shows the answer)
bossIds.forEach(id => { if (lessonCited.has(id)) err("boss question", id, "is cited in a lesson (the peek would reveal it)"); });

// index.html must load every level file, exactly once
const IDX = path.join(ROOT, "index.html");
let html = fs.readFileSync(IDX, "utf8");
const block = files.map(f => `<script src="${f}?v=1"></script>`).join("\n");
const re = /(<!-- COURSE LEVELS -->\r?\n)([\s\S]*?)(<!-- \/COURSE LEVELS -->)/;   // \r?: autocrlf checkouts
if (!re.test(html)) err("index.html has no COURSE LEVELS block");
else if (args.includes("--sync")) {
  html = html.replace(re, (m, a, b, c) => a + (block ? block + "\n" : "") + c);
  fs.writeFileSync(IDX, html);
  console.log(`index.html: ${files.length} level scripts`);
} else {
  const listed = [...html.match(re)[2].matchAll(/src="([^"?]+)/g)].map(m => m[1]);
  files.forEach(f => { if (!listed.includes(f)) err("index.html does not load", f, "(run with --sync)"); });
  listed.forEach(f => { if (!files.includes(f)) err("index.html loads a missing file", f); });
}

const di = args.indexOf("--dump");
if (di >= 0) {
  const cid = args[di + 1], only = args[di + 2];
  (COURSES[cid] || { levels: [] }).levels.filter(L => !only || L.id === only).forEach(L => {
    console.log(`\n=== ${L.id} ${L.title}`);
    L.questions.forEach(q => {
      if (q.bankId) { const b = byId.get(q.bankId); console.log(`\n[BANK ${q.bankId}] ${strip(b.questionHtml)}\n` + b.options.map(o => `  ${o.id === b.correctId ? "*" : " "} ${strip(o.html)}`).join("\n")); return; }
      console.log(`\n[${q.id}] ${strip(q.questionHtml)}\n` +
        q.options.map(o => `  ${o.id === q.correctId ? "*" : " "} ${strip(o.html)}`).join("\n") + `\n  -> ${strip(q.explanationHtml)}`);
    });
  });
}

const per = Object.keys(COURSE_TOPICS).map(c => { const L = (COURSES[c] || { levels: [] }).levels; return `${c}: ${L.length} levels / ${L.reduce((n, l) => n + l.questions.length, 0)} q`; });
console.log(`\n${per.join(" · ")}\ntotal ${total} questions (${totalBank} real exam questions), ${cited.size} distinct exam ids cited, ${nMath} MathML snippets`);
if (bad) { console.log(`\nCOURSE CHECK FAILED: ${bad} error(s)`); process.exit(1); }
console.log("COURSE CHECK PASSED");
