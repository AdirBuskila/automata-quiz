# Build plan — Automata & Formal Languages MCQ Quiz (62208)

Phase-0 deliverable and resume point. 5th app in the quiz family; **template = `databases-quiz`**
(data model, contexts, typed options), **rules = `machine-learning-quiz/CLAUDE.md`** (pipeline,
invariants, build-time MathML). Status markers: ⏳ pending approval · ✅ done.

Source folder: `C:\Users\Adir\Desktop\BSC\שנה ג\אוטומטים ושפות פורמליות` (read-only).
App folder: `C:\Users\Adir\Desktop\Coding\Dev\automata-quiz`.

## Key facts from triage (see `format_triage.md` for the per-file table)
- **Two exam families.** Semester-A papers (and all 2019 + 2021-summer papers) are **MCQ**:
  18 or 25 questions × 4 claims, one correct. Every Semester-B paper (2023–2026) and all of
  2016–2018 are **open-ended proofs** ("נמקו", "בנו אוטומט", "הוכיחו בעזרת למת הניפוח") → not
  convertible to MCQ without inventing options → **excluded**. That includes the 2026 Semester-B
  paper, so the flagship is **2026 Semester A (`26A-A`)**.
- **Every MCQ solution PDF is a full copy of the exam** with the correct claim **highlighted
  yellow** and a worked explanation (blue). All MCQ PDFs have a real text layer (not scans).
  The yellow fill is detectable in the PDF drawing list, so each key is read **twice**: visually
  and by `tools/detect_keys.py` — disagreement → ask list.
- **Versions.** `גרסה 2` files (2019 מועד א/ב) and `2025 מועד ג` file `2…` are the same exam with
  questions **and** options permuted (and occasionally reworded, e.g. `((b)(ab))*`→`((ba)(b))*`).
  Never map by letter/number across versions; match by content; use them as cross-checks only.
- **Mis-filed:** `2019/סמסטר א/…27.6.19 פתרון.pdf` is the **version-1 solution of 2019 Sem-B מועד א**
  (its own cover and the merged PDF both say so).
- **`איגוד מבחנים עם תשובות.pdf`** = byte-for-content copies of the 2019 sample, 2019-B-A and
  2019-B-B solutions + homework solutions → cross-check only, adds no questions.
- **Turing machines never appear** in any MCQ exam → no TM topic (see taxonomy).

## Architecture (same as siblings)
Static, no CDN, works from `file://` and GitHub Pages (`.nojekyll`). Runtime: `index.html`,
`styles.css`, `app.js`, `learn.js`, `questions.js`, `images/`, `favicon.svg`. Offline pipeline in
`tools/` (Python + Node). Python = `C:\Users\Adir\AppData\Local\Programs\Python\Python313\python`
(has PyMuPDF/pdfplumber/python-docx/Pillow; the first `python` on PATH does not), always with
`PYTHONUTF8=1`.

## Data model (DB model + build-time math)
`window.AUTOMATA_QUIZ = { meta, contexts, questions }` (`questions.json` identical content).

**Raw per-exam file `tools/raw/<CODE>.json` — THE source of truth:**
```
{ examCode, examLabel, year, examDate, source: "exam"|"moodle",
  files: { exam, solution, crossChecks:[…] },
  contexts: { <localId>: { kind: image|table|text|math, title, image?, caption?,
                           table?: {head:[…], rows:[[…]]}, text?, tex? } },
  questions: [ { num, topic, contextId?, question,            // richText: $tex$, $$tex$$, `code`, **b**
                 options: [ {id:"a", type:"text"|"math"|"code"|"image", value} ],  // a,b,c,d = א,ב,ג,ד
                 correctId, acceptedIds?, lockOrder?,         // lockOrder: "כל הטענות האחרות…" etc.
                 answerSource, official, confidence, explanation, crossCheck? } ] }
```
**Generated `questions.json`/`.js`:** build adds `id` (`<CODE>-Q<num>`), `topicLabel`,
`examLabel`, `dedupKey`, namespaced `contextId`, and **pre-rendered HTML**: `questionHtml`,
`explanationHtml`, each option's `html`, each context's `html`. All TeX goes through
`tools/render_math.js` (KaTeX, `output:"mathml"`, `dir="ltr"` on every `<math>`) — the site
ships **no** math library. **No Hebrew inside TeX** (KaTeX chokes on it; see DB build_plan) —
Hebrew stays in the surrounding richText.

**Notation conventions (character-exact):** `\varepsilon` for ε, `\Sigma^*`, `a^nb^n`,
`\#_a(w)`, `L_1\cdot L_2`, `\{w\in\{a,b\}^*\mid …\}`, grammar arrows `S\to aSb\mid\varepsilon`,
`\delta(q,a)`, `Rank(L)` as `\mathrm{Rank}(L)`, regex union written as the exam writes it (`+`).
Transition tables → `kind:"table"` HTML. Anything I can't capture 100% → image option / ask list.

## Answer rules (no form-0 here)
- `correctId` only from: the sitting's solution PDF (yellow highlight) · a content-matched
  version-2 / merged-collection copy · a Moodle score-100 attempt or explicit
  "התשובה הנכונה היא" feedback. Stored **by option id**; options shuffled at render time.
- `official:true` only for solution-PDF keys. Moodle keys: `answerSource:"moodle-100"` /
  `"moodle-feedback"`, `official:false`, confidence high when unambiguous.
- `lockOrder:true` when an option references siblings ("כל הטענות האחרות לא נכונות",
  "תשובות א ו-ג", "כל המחרוזות שייכות") — **very common in this course**, the builder detects
  the phrases and `validate.py` flags any it misses.
- Two sources disagree / key unclear / notation unsure → `docs/ASK_ADIR.md`, not the bank.

## Extraction method (per sitting)
1. `render_pdf.py` exam + solution → `tools/raw/<CODE>/page-NN.png` @200 DPI; **look at every page**.
2. Text layer (`get_text`) as a typing aid only — the Hebrew/math order is scrambled in it.
3. Option text from the **clean exam file** where the solution annotates options inline
   (2019 solutions put counterexamples next to each claim); stems/options verified against the image.
4. Diagrams: extract the embedded raster **losslessly** (`extract_image(xref)`) →
   `images/exams/<CODE>-Q<n>.png` (or `-ctx-<id>.png` when shared); view each crop.
5. Explanation = short Hebrew paraphrase of the blue solution text (math in `$…$`).
6. `validate.py` → `build_questions.py` → `smoke.js` / `verify_dom.js`.

Batches for parallel subagents after the flagship is approved: (1) 2025 A-A/B/C ·
(2) 2024 A-A/B/C + short-semester A/C · (3) 2023 A-A/B + 2021 S-A/B · (4) 2019 B-A/B + sample ·
(5) Moodle MQ1–MQ3 + תשפ״ה set. One agent per batch, crash-safe (write each exam file as done).

## Exam codes
`YY` + semester (`A`=א, `B`=ב, `S`=קיץ, `X`=סמסטר קצר) + `-` + moed (`A|B|C`); `SAMP-19` = 2019 sample;
`MQ1..MQ3` = Moodle quizzes, `MQ-T` = "שאלות תשפ״ה".

## Topic taxonomy (closed set — 11 keys, synced in build_questions.py / validate.py / app.js / learn)
| key | Hebrew label | covers |
|---|---|---|
| `basics` | מחרוזות, שפות ופעולות | Σ*, concatenation, power, reverse, prefix, language ops |
| `dfa` | אס״ד | DFA design/reading, product automaton |
| `nfa` | אסל״ד ומסעי ε | NFA, ε-moves, subset construction, run counting |
| `regex` | ביטויים רגולריים | regex ↔ language, regex ↔ automaton |
| `reg_closure` | תכונות סגירות (רגולריות) | closure/non-closure of REG, constructions |
| `pumping_reg` | למת הניפוח (רגולריות) | choosing the word, decompositions |
| `nerode` | משפט נרוד / Rank / מינימיזציה | separating sets, Rank(L), minimal DFA size |
| `cfg` | דקדוקים חסרי הקשר | derivations, generated language, ambiguity, CNF, right-linear |
| `pda` | אוטומט מחסנית | PDA reading/design, acceptance |
| `cfl_props` | תכונות שפות ח״ה ולמת הניפוח לח״ה | CFL closure, CFL pumping |
| `classify` | סיווג שפות | finite / regular / CFL-not-REG / not-CFL questions |
Final lecture cross-check (תשפ״ו slides + Noa Erlichman's semester-A 2025 lectures) during M1.

## Learn mode (M3)
ML-app pattern: per-topic Hebrew briefs in `docs/briefs/*.md` → `build_learn.py` → `learn.js`,
with clickable question ids (`.qref`), "תרגל נושא זה", pumping-lemma templates (REG + CFL),
closure-property tables, a language-classification cheat-sheet. Sources: `סיכום סמסטר א 2025-
נועה ארליכמן.pdf`, `סיכום אוטומטים סמסטר א 2025.pdf`, `Tutorials & Lectures Summary.pdf`,
`נקודות חשובות ומשפטים…`, `סיווג שפות…`, `נקודות חשובות מאוד.pdf`, `תרגולים תשפו` solutions,
`תרגילים נוספים בלמת הניפוח.pdf`, and the formula-sheet pages at the end of each exam.
(Noa's lecture PDFs are handwritten scans — visual reading only.)

## Milestones
- **M0 — Scaffold** ✅: DB engine adapted (pre-rendered HTML, `last` options, runtime dedup,
  topic deep-link), teal theme, `render_math.js`, `validate.py`, `build_questions.py`,
  `detect_keys.py`, `extract_figs.py`, `smoke.js`, `verify_dom.js`, `shoot.js`, `shoot_feedback.js`.
- **M1 — Flagship `26A-A`** ✅ (2026-09-29, awaiting Adir's sign-off): 18 Q, all keys from the
  solution PDF, re-derived by hand (18/18 agree) and by `detect_keys.py` (17 agree, Q11
  undetected → visually confirmed, 0 disagree). 3 lossless diagrams (Q7 PDA, Q11/Q16 ε-NFA),
  ~290 MathML formulas, 9 "all others" options pinned last. validate 0 · smoke PASSED ·
  verify_dom PASSED (incl. full replay 18/18) · 36 Chrome renders (18 Q × 2 themes @390px):
  0 overflow, 0 clipped formulas. Decisions: approved scope/flagship; Moodle keys are
  `official:false`; Moodle ask-list answered later.
- **M2 — Scale** ✅: 7 parallel agents (2025 A · 2024 A · 2024 short · 2023 A · 2021 summer ·
  2019 + sample · Moodle). Every key re-derived by the extracting agent; `detect_keys.py`
  0 disagreements on all 16 exams (undetected ones confirmed by eye); version-2 / file-2
  content cross-checks: 19B-B 25/25, 25A-C 18/18, 19B-A all comparable agree. Only exclusion:
  `19B-A-Q10` (printed question ≠ the question both solutions key) → ASK_ADIR.
- **M3 — Learn mode** ✅: 11 briefs (`docs/briefs/`, ~3,300 lines) written from the formula
  sheet + course summaries + tutorials, citing every bank question of their topic
  (1,146 linked refs), 3,059 formulas → MathML, peek + drill wired.
- **M4 — Verify & report** ✅: see below.

## Final state (2026-09-30)
**349 questions** (336 exam + 13 Moodle; 340 unique after runtime dedup), 69 diagram images.
Keys: 336 `solution-pdf` (official) · 7 `moodle-feedback` · 6 `moodle-100`. All `confidence:high`;
1 question with two accepted answers (`21S-A-Q7`, as the solution marks). 29 `lockOrder`,
110 "all others" options pinned last.

| topic | n | | exam | n | | exam | n |
|---|---|---|---|---|---|---|---|
| basics | 11 | | 19B-A | 24 | | 24A-C | 18 |
| dfa | 12 | | 19B-B | 25 | | 24X-A | 18 |
| nfa | 23 | | SAMP-19 | 25 | | 24X-C | 18 |
| regex | 44 | | 21S-A | 25 | | 25A-A | 18 |
| reg_closure | 20 | | 21S-B | 25 | | 25A-B | 18 |
| pumping_reg | 9 | | 23A-A | 25 | | 25A-C | 18 |
| nerode | 62 | | 23A-B | 25 | | 26A-A | 18 |
| cfg | 39 | | 24A-A | 18 | | MQ1 | 9 |
| pda | 36 | | 24A-B | 18 | | MQ3 | 4 |
| cfl_props | 23 | | | | | | |
| classify | 70 | | | | | | |

Checks: `validate.py` 0 problems · `smoke.js` PASSED (5000 shuffles, 0 mismatches, 0 displaced
"last" options) · `verify_dom.js` PASSED (incl. 26A-A replay 18/18, learn refs all resolve,
peek→drill) · `shoot.js` over all 349 questions @390px dark: 0 page overflow, 0 clipped
formulas · `verify_learn.js` all 11 chapters @390px, both themes: 0 overflow.

Build-time layout helpers added during M2 (see CLAUDE.md): long inline formulas split into
wrapping MathML pieces at relations / `\mid` / connectives / top-level regex `+` and group
joins; long display formulas wrap; `array{l}` → aligned rows; punctuation glued to math;
dedupKey includes a perceptual hash of the diagram (Moodle variants share text but not figure).
