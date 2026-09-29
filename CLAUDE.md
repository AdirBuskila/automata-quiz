# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

A Hebrew/RTL multiple-choice exam trainer for **Automata & Formal Languages (62208, HIT)** —
5th app of the quiz family (`data-science-quiz`, `software-engineering-quiz`,
`machine-learning-quiz`, `databases-quiz`). The shipped site is **100% static** —
`index.html` + `styles.css` + `app.js` + `questions.js` + `learn.js` + `images/`. No bundler,
no framework, no runtime deps, no math library at runtime; runs from `file://` and GitHub
Pages (`.nojekyll`). Everything under `tools/` is an offline pipeline.

Plan / scope / status: `docs/build_plan.md`. Per-file source triage: `docs/format_triage.md`.
Open questions for Adir: `docs/ASK_ADIR.md`.

## Commands

```bash
PY=/c/Users/Adir/AppData/Local/Programs/Python/Python313/python   # has PyMuPDF/Pillow; the PATH python does not
PYTHONUTF8=1 $PY tools/gen/<CODE>.py        # (if the exam has a generator) -> tools/raw/<CODE>.json
PYTHONUTF8=1 $PY tools/validate.py           # lint tools/raw/*.json
PYTHONUTF8=1 $PY tools/build_questions.py    # raw -> questions.json + questions.js + tools/build_report.md
node tools/smoke.js                          # integrity + 5000-shuffle scoring invariant + js≡json
node tools/verify_dom.js                     # jsdom: boot, practice, full replay = 100%, learn refs + peek
node tools/shoot.js <CODE> 1,2,3 [--theme light] [--answer]   # 390px Chrome shots; fails on overflow/clipped math
node tools/shoot_feedback.js <QID> [--wrong]                  # screenshot the feedback panel
node tools/verify_learn.js [--theme light]                    # every learn chapter @390px, fails on overflow
PYTHONUTF8=1 $PY tools/detect_keys.py <CODE> "<solution.pdf>" # yellow-highlight key cross-check
PYTHONUTF8=1 $PY tools/build_questions.py <CODE…> --check     # render one exam's math, write nothing
PYTHONUTF8=1 $PY tools/build_learn.py        # docs/briefs/*.md -> learn.js (needs `markdown`)
PYTHONUTF8=1 $PY tools/dump_topics.py        # bank grouped by topic -> tools/raw/_digest/ (for briefs)
```
Extraction of new exams: follow `tools/EXTRACTION_GUIDE.md` (one generator per exam in `tools/gen/`).
Node deps (gitignored manifest): `cd tools && npm install katex jsdom puppeteer-core`. Chrome is
hardcoded at `C:\Program Files\Google\Chrome\Application\chrome.exe`.

## Data flow

```
solution PDF (full exam + yellow highlight)  --render_pdf.py-->  tools/raw/<CODE>-SOL/page-NN.png  (read by eye)
exam PDF  --extract_figs.py (lossless xref)-->  images/exams/<CODE>-Q<n>.png
(transcribed)  tools/gen/<CODE>.py  -->  tools/raw/<CODE>.json   <- THE SOURCE OF TRUTH
build_questions.py (+ render_math.js / KaTeX -> MathML)  -->  questions.json + questions.js
```
**Never hand-edit `questions.js` / `questions.json` / `learn.js`.** Fix the raw file (or its
generator, then re-run it) and rebuild.

## Invariants (tests enforce most of them)

- **Answer by option id** (`correctId`, optional `acceptedIds`); options are shuffled on every
  render. Options whose text says "כל הטענות האחרות…" / "כל המחרוזות…" get `last:true` at build
  and **always render last** (they mean "the others"). `lockOrder` (source order) only when an
  option cites siblings by letter. smoke.js checks 5000 shuffles; verify_dom checks `last`.
- **No form-0 rule.** Every key comes from the sitting's solution PDF (yellow highlight),
  a content-matched other version, or a Moodle 100/feedback screenshot. `official:true` only
  for solution-file keys; Moodle keys are `official:false`. No reliable key → ASK_ADIR, not the bank.
- **Versions**: `גרסה 2` files and `2025 מועד ג` file 2 are the same exam with questions *and*
  options permuted (sometimes reworded). Match by content, never by letter/number.
- **Math is MathML built at build time.** TeX lives in `$…$` / `$$…$$` (stems, options,
  explanations) and in `type:"math"` options. **No Hebrew inside TeX** (validate.py). Every
  `<math>` gets `dir="ltr"`. Punctuation right after inline math is glued to it (`.nobr`).
- **Mobile width**: Chrome ignores MathML column alignment and a wide one-line display gets
  clipped at 390px. Multi-line blocks (grammars, two definitions) → `\begin{array}{l} … \\ … \end{array}`,
  which the builder emits as left-aligned rows. `\quad` in display math is a validate error.
  `shoot.js` fails on any page overflow or clipped formula.
- **Unique ids** `<CODE>-Q<num>`; duplicates across exams are kept (full-exam replay) and
  deduped at runtime in practice pools by `dedupKey`.
- **Topics are a closed set of 11** in `build_questions.py` TOPIC_LABEL, `validate.py` TOPICS,
  `app.js` TOPICS (+`all`), and `MANIFEST` in `build_learn.py`. No Turing-machine topic — TMs never
  appear in the MCQ exams.
- **Diagrams** are the original embedded rasters (`extract_figs.py --xref`), never redrawn.
  Upscaling a tiny raster 2× with Lanczos is fine; editing it is not.

## Build-time layout rules (build_questions.py)

- A `<math>` element never line-breaks. `split_inline()` cuts a long inline formula (> 26 chars)
  into separately rendered pieces joined by `<wbr>` — before relations, `\mid`, logic
  connectives, `\text{…}`, a top-level regex `+`, and between concatenated groups — only
  outside TeX `{…}` grouping and outside `\left…\right`, so every piece is valid TeX.
  Long display formulas (> 44 chars) wrap the same way (`.math-wrapd`).
- `dedupKey` = normalized stem + sorted options + a 12×12 average-hash of each diagram, so
  Moodle variants with the same text but different automata are NOT deduped. The same diagram
  cropped differently in two PDFs may hash differently — harmless (a drill may repeat it).
- `LOCK_RE` also catches "תשובות א + ב".

## Course conventions the keys depend on

- **PDA acceptance = accepting state AND empty stack** (formula sheet). Explanations must say so.
- Pumping constant: the formula sheet writes `ℓ` (and `n` for the exponent); exams write `n`.
- The formula sheet's "known languages" table (page 18 of any Sem-A solution) is the authority
  for classification: non-regular CFL = aⁿbⁿ, aⁿbᵐcᵐdⁿ, uuᴿ, complement of uu; non-CFL =
  aⁿbⁿcⁿ, aⁿbᵐcⁿdᵐ, uu, a^{n²}, a^{n!} and their complements.
- CNF with `S→ε`: sources disagree; `25A-A-Q15` assumes it's allowed (open in ASK_ADIR).

## Lessons so far

- The solution PDFs contain the whole exam; the exam PDF is only needed for clean figures and
  for 2019 option text (2019 solutions print counterexamples inline next to each claim).
- `detect_keys.py` misses highlights that cover only a math span (no letter in the box) — those
  show as "undetected"; confirm visually. Any *disagreement* is a hard stop.
- Some solutions' explanations are sloppy (26A-A Q17 wrote `k≥1` for `k≥2026`) — explanations
  are paraphrased and corrected, the key is not touched.
- Git-Bash heredocs mangle backslashes: write scripts containing regex/TeX with the file tool.
- jsdom re-serializes MathML, so tests identify questions/options by `data-qid` / `data-oid`,
  never by comparing `innerHTML`.
- `detect_keys.py` must take the number glued to "שאלה" (it used to read "שאלה 11" as 1 and
  report false disagreements). Some PDFs store text in visual order → no headings found → all
  "undetected"; then verify every highlight by eye.
- Several official explanations are sloppy (wrong acceptance convention, wrong bound, a
  counterexample that doesn't fit). Agents fix the explanation, never the key; a key that the
  printed question doesn't match (19B-A-Q10) is excluded, not guessed.
- Learn briefs cite question ids in backticks; `verify_dom.js` fails on any dangling id, so
  re-run `dump_topics.py` and re-check briefs whenever questions are added or renumbered.

## app.js conventions

DB-app engine, single file, no modules. `S` session state, `P` progress in `localStorage`
(`afq_progress_v1`, theme `afq_theme`). `startTopicPractice(topic)` (also on `window`) is the
single entry into a topic drill (`?practice=<key>`). CSS is token-driven: dark `:root` default,
`:root[data-theme="light"]`, and the same light palette under `prefers-color-scheme` — change a
color in all three. Bump `?v=N` in `index.html` when shipping CSS/JS changes.
