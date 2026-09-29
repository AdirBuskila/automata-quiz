# Exam extraction guide (M2 — one agent per batch of exams)

You extract Automata & Formal Languages MCQ exams into `tools/raw/<CODE>.json` for a Hebrew quiz app.
App dir: `C:\Users\Adir\Desktop\Coding\Dev\automata-quiz` (read `CLAUDE.md` first).
Sources: `C:\Users\Adir\Desktop\BSC\שנה ג\אוטומטים ושפות פורמליות\מבחנים ופתרונות\…` (READ-ONLY).
**Gold template: `tools/gen/26A-A.py` → `tools/raw/26A-A.json`.** Mirror its structure, tone and TeX style exactly.

Python: `PY=/c/Users/Adir/AppData/Local/Programs/Python/Python313/python`, always `PYTHONUTF8=1`.
**Write scripts with the Write tool, not bash heredocs** (heredocs mangle backslashes).

## NON-NEGOTIABLE RULES
1. **Character-exact.** A missing `*`, swapped `a`/`b`, `+` vs `*`, `≤` vs `<`, `i` vs `j` flips the answer.
   Read every stem/option from the rendered page IMAGE (text layer is only a typing aid — its Hebrew
   and math order is scrambled). If you are not 100% sure of a token → do NOT guess: put the question
   in your `askAdir` list and leave it OUT of the JSON.
2. **Answers only from the real key**: the yellow highlight in the sitting's solution PDF. No form-0
   rule, never "first option". Re-derive each answer yourself as a sanity check. If your derivation
   disagrees with the highlight, re-read; if still disagreeing, flag it (keep the highlighted answer
   only if you are sure you misread; otherwise leave it out and ask).
3. **Versions** (`גרסה 2`, 2025 מועד ג file `2…`): same exam, questions AND options permuted and
   sometimes reworded. Use them ONLY as a content-matched cross-check; never map letters or numbers.
4. Never fabricate or "fix" a question, option, regex, grammar or diagram. Never redraw a diagram.
5. Do NOT run `build_questions.py` without `--check`, and never touch `questions.js/json`,
   other agents' codes, `app.js`, `styles.css`, `index.html`.

## STEPS (per exam)
1. Render: `$PY tools/render_pdf.py "<solution.pdf>" <CODE>-SOL --dpi 200` (and the exam PDF as `<CODE>`
   when it exists). View EVERY question page (skip cover, scratch "דף טיוטא" and formula-sheet pages).
   For small print, re-render a page at `--dpi 300 --pages N` and crop with Pillow; view the crop.
2. Figures: `$PY tools/extract_figs.py "<exam.pdf or solution.pdf>"` lists embedded images with page,
   xref and nearest question; extract with `--xref N --out images/exams/<CODE>-Q<n>.png` (prefer the
   clean exam PDF; the solution copy may carry highlights). **View every extracted PNG.** If a diagram
   is tiny (< ~400 px wide) upscale 2× with Pillow `Image.LANCZOS` — nothing else. If a figure is vector
   (not listed) render the page region at 300 DPI and crop tightly. A diagram shared by 2+ questions →
   a context: `"contexts": {"pda1": {"kind":"image","title":"…","image":"images/exams/<CODE>-ctx-pda1.png"}}`
   and `"contextId":"pda1"` on each question. A diagram that IS an option → `{"type":"image","value":"images/exams/<CODE>-Q<n>-<letter>.png"}`.
3. Write `tools/gen/<CODE>.py` (copy the 26A-A structure) and run it → `tools/raw/<CODE>.json`.
4. `$PY tools/validate.py <CODE>` → 0 problems. `$PY tools/build_questions.py <CODE> --check` → no math errors.
5. `$PY tools/detect_keys.py <CODE> "<solution.pdf>"` → **0 disagree**. Undetected ones: confirm by eye
   and say so in your report. If a solution numbers questions differently, pass `--renumber raw:pdf,…`.
6. Report (compact): per exam — label/date, #questions kept, #skipped with reasons, key source,
   detector result, answers you had to think hard about, and the full **askAdir** list (file + page +
   question number + exactly what is unclear).

## JSON (see 26A-A.json)
Exam: `examCode, examLabel` (e.g. `"2025 סמסטר א׳ מועד ב׳"`, `"2024 סמסטר א׳ (קצר) מועד א׳"`,
`"2021 קיץ מועד א׳"`, `"2019 מבחן לדוגמה"`), `year, examDate, course:"62208", source:"exam",
files:{exam, solution, crossChecks}, contexts, questions`.
Question: `num` (the exam's own number), `topic`, `question`, `options` (ids `a,b,c,d` = א,ב,ג,ד in
the PRINTED order of the exam), `correctId`, `answerSource:"solution-pdf"`, `official:true`,
`confidence:"high"` (use `"med"` only with a note in the report), `explanation`, optional `image`,
`contextId`.

**Topics (closed set):** `basics` (strings, language ops, concatenation/power/reverse, membership in
set-built languages) · `dfa` (reading/designing DFAs, product automaton) · `nfa` (NFA/ε-NFA semantics,
subset construction, run counting) · `regex` (regex ↔ language, automaton → regex, regex equality/containment)
· `reg_closure` (closure/non-closure of REGULAR languages, constructions) · `pumping_reg` (pumping lemma
for regular languages) · `nerode` (separating sets, Rank(L), Myhill–Nerode, minimal DFA size) · `cfg`
(grammars: generated language, derivations, ambiguity, CNF, right-linear) · `pda` (pushdown automata) ·
`cfl_props` (CFL closure, pumping lemma for CFLs, statements I/II about CFLs) · `classify` ("finite /
regular-infinite / CFL-not-regular / not-CFL" and similar classification questions).

## TEXT & TeX CONVENTIONS
- Stems/explanations are richText: Hebrew text + `$inline TeX$` + `$$display TeX$$` + `**bold**`
  (bold what the exam bolds/underlines: **לא**, **שייכת**, **מינימלי**). `"\n"` between lines.
- **NO Hebrew inside `$…$`.** Every variable/symbol, even a lone `$L$`, `$n$`, `$A$`, goes in math.
- TeX: `\Sigma`, `\varepsilon` (ε), `\emptyset`, `^*`, `\{…\}`, `\mid`, `\#_a(w)`, `\cdot`, `\to`,
  `\subseteq`, `\subsetneq`, `\in`, `\notin`, `\cap`, `\cup`, `\overline{L}`, `\mathrm{Rank}(L)`,
  `L^R`, `a^{2n}`, `\le`, `\ge`, `\ne`, `\delta(q,a)`, regex union as the exam writes it (`+`).
- Pure-math options → `{"type":"math","value":"(a+b)^*c^*"}`. Mixed Hebrew+math → `type:"text"` with `$…$`.
- Grammars / several definitions → ONE display block with rows:
  `$$\begin{array}{l}S\to aSb\mid\varepsilon\\ A\to aA\mid b\end{array}$$` (never `aligned`, never `\quad`).
- Transition tables → a context with `"table":{"head":[…],"rows":[[…]]}` (cells may use `$…$`).
- "כל הטענות האחרות לא נכונות." / "כל המחרוזות שייכות לשפה $L$" options: copy verbatim (the builder pins them last).
- Claims I / II: put them in the stem as lines `$I$. …` / `$II$. …` (see 26A-A Q4, Q12).
- Explanation: 1–3 Hebrew sentences paraphrasing the blue solution text — why the right one is
  right and briefly why the others fail. Fix obvious slips in the explanation (say "לפי הפתרון…" if
  you keep its reasoning) but NEVER change the key.
- 2019 solutions print counterexamples next to each claim: take option text from the clean EXAM PDF.
