# Video course for the guided levels — design

Status: draft for Adir's approval (2026-10-28). Nothing is built until approved; then a plan, then the pilot F01.

## Intent

Adir is studying for Automata & Formal Languages (HIT 62208). YouTube (Neso Academy) helped, but it uses
different terms and notation and skips topics the exam tests. Goal: a **Hebrew video course, one short video per
guided level**, that teaches exactly what this course tests, in its exact terms and notation, and prepares for the
real exam questions of each topic. Success = after watching a video, the level's quiz and the bank questions of
that topic feel familiar; nothing in a video contradicts the course or the keys.

## Goals

- 34 videos, 5–8 min each, 16:9 1920×1080, watched mostly on a laptop.
  - 32 = one per level: `fa` F01–F08, `nerode` N01–N08, `classify` K01–K08, `cf` G01–G08.
  - 2 bonus closure videos: **K06a** closure of regular languages, **K06b** closure of CFLs (43 closure questions
    in the bank, only 9 cited by K06; the 31 uncited ones are listed below). K06 itself stays the overview.
- Every video has the same four beats:
  1. **Concept**: the level's lessonHtml, in its own words and notation, expanded.
  2. **1–2 worked examples, animated step by step** (DFA run letter by letter, subset construction state by
     state, regex elimination with a short word, "רישא וסיבובים", a separating set filled in pair by pair,
     a derivation tree growing, a PDA's stack pushing/popping, the pumping game's split).
  3. **One real exam question** (id shown on screen, e.g. `24X-A-Q9`), solved by elimination, with **the trap**
     named explicitly (the wrong option a student picks, and why it is wrong).
  4. **~20 s recap**: the level's 🔑 rules.
- Hebrew narration (edge-tts, `he-IL-HilaNeural` — chosen by Adir), Hebrew subtitles burned in, RTL-correct, all
  math LTR.
- Extra care (more examples, more exam questions) for Myhill–Nerode / Rank / separating sets (N01–N08) and closure
  (K06, K06a, K06b).

## Non-goals

- No new course levels in the app (K06a/K06b are videos only). No Turing machines (never on the MCQ exams).
- No avatar/talking head, no B-roll, no music bed beyond an optional quiet intro sting.
- No uploading on Adir's behalf.

## Anti-goals (would make it a failure even if it renders)

- Any definition, term or convention not in the course: e.g. PDA acceptance by final state only (course:
  **accepting state AND empty stack**), Arden's lemma (course: **רישא וסיבובים**), pumping constant notation
  other than the exam's `n`, a classification contradicting the formula-sheet "known languages" table.
- An example automaton/grammar/regex/PDA that is not machine-verified, or a drawn diagram that differs from the
  verified definition.
- Solving a boss level's own quiz questions (spoils the boss).
- Hebrew in scrambled bidi order, math rendered RTL, subtitles clipped or overlapping the animation.
- Mispronounced course terms (אס״ד read as "a-s-d", etc.).

## Sources of truth (in order)

1. `lessonHtml` / `goal` of each level: `tools/needhelp/<course>/<ID>.py` (generated `courses/<course>/<ID>.js`).
2. `questions.json`: the real questions of the topic; every exam question used in a video keeps its official key
   and the bank's (corrected) explanation logic.
3. Course terminology and conventions from `CLAUDE.md` (אס״ד, אסל״ד, סיפא מפרידה, Rank, אוטומט החזקה, ח״ה, PDA
   acceptance, רישא וסיבובים, formula-sheet language table).

Nothing is invented: a claim in narration must be traceable to the lesson, a bank explanation, or a simulator check.

## Video outline (34)

Exam anchors: each normal video picks its solved exam question from the ids that level already cites (listed by
`node` dump in the brainstorming session; re-derive with the citation scan over `courses/*/*.js`). Boss videos
(F08, N08, K08, G08) solve **3–4 other uncited** bank questions of their topics under "exam conditions" and must
not use the ids their boss quiz cites:

- F08 boss ids (excluded): 21S-A-Q24 MQ1-Q7 21S-B-Q4 24A-A-Q1 19B-A-Q17
- N08: 21S-A-Q6 23A-A-Q11 23A-A-Q14 21S-A-Q21 25A-C-Q7
- K08: 24A-B-Q8 26A-A-Q17 21S-A-Q3 25A-B-Q12 26A-A-Q12
- G08: 19B-B-Q8 25A-C-Q18 19B-B-Q23 25A-C-Q3 24A-B-Q18

| Video | Level title (app) | Animated core |
|---|---|---|
| F01 | הרצת אס״ד על מילה | run a DFA letter by letter; filter options (ε ↔ start accepting, last letter, sink) |
| F02 | מבנה של אס״ד: בור, משלים, מכפלה | complement by flipping, product automaton pairs, pigeonhole |
| F03 | אסל״ד, מסעי ε והשוואת שפות | all runs as a tree; ε-closure; "one accepting path suffices" |
| F04 | אוטומט החזקה וגדלים | subset construction built row by row; counting states/accepting |
| F05 | ביטויים רגולריים: לקרוא ולכתוב | regex → words in plain Hebrew; kill options with a short word |
| F06 | השוואת ביטויים | separating word for =, ⊂, neither; how many words prove each |
| F07 | מאוטומט לביטוי רגולרי | רישא וסיבובים on the automaton, then kill options |
| F08 | מבחן גמר (walkthrough) | 3–4 uncited dfa/nfa/regex questions under a timer |
| N01 | סיפא מפרידה ומחלקות שקילות | two words, try suffixes until one separates |
| N02 | Rank של שפות קטנות ומצב הבור | classes of a finite language + the sink class |
| N03 | כמה מצבים באס״ד המינימלי? | ends-with / starts-with / k-th letter / parity patterns |
| N04 | להוכיח Rank = k | upper bound (DFA) + lower bound (separating set of size k) |
| N05 | משפחת x ו-y | "all words in L in one class?" two-line solutions |
| N06 | Rank של פעולות על שפות | complement/union/∩/reverse/star; the fixed counterexamples |
| N07 | Rank אינסופי וקבוצה מפרידה אינסופית | infinite separating set; infinite-but-not-separating traps |
| N08 | מבחן גמר (walkthrough) | 3–4 uncited nerode questions |
| K01 | ההיררכיה ואלגוריתם הסיווג | the ladder finite ⊂ regular ⊂ CFL; simplify first |
| K02 | שפות שנראות קשות ובעצם רגולריות | mod, bounded count, fixed pattern, absorbing "or" |
| K03 | להוכיח שפה לא רגולרית | infinite separating set; intersect with a regular language |
| K04 | משחק למת הניפוח לרגולריות | the game: choose w, adversary splits, pump to contradiction |
| K05 | ח״ה מול לא ח״ה: מקונן וחוצה | nested vs crossing comparisons; intersect to prove non-CFL |
| K06 | סגירויות: מה נשמר ומה נשבר | the closure table + fixed counterexamples (overview) |
| K06a | (bonus) סגירות של שפות רגולריות | worked uncited reg_closure questions |
| K06b | (bonus) סגירות של שפות חסרות הקשר | worked uncited cfl_props questions |
| K07 | למת הניפוח לח״ה | window of p letters touches ≤ 2 blocks |
| K08 | מבחן גמר (walkthrough) | 3–4 uncited classify/cfl_props questions |
| G01 | לקרוא דקדוק | variable by variable; shortest words |
| G02 | פענוח דקדוקים | nesting, concatenation, union, substitution; two independent params |
| G03 | איזה דקדוק יוצר את L | short word that falls; strict containment |
| G04 | חומסקי, ליניארי ימני, רב-משמעיות | two derivation trees side by side; pigeonhole on variables |
| G05 | אוטומט מחסנית: ריצה ו״מתקבלת״ | `σ,x→y` edges, live stack; accept = accepting state AND empty stack |
| G06 | מהי L(M)? משוואת איזון | state order + push/pop balance equation |
| G07 | אוטומט מחסנית: סיווג, מודלים ותיאוריה | model questions (states needed, flipping states, restricted models) |
| G08 | מבחן גמר (walkthrough) | 3–4 uncited cfg/pda questions |

Uncited closure questions for K06a/K06b (pick the clearest; none may contradict the formula-sheet table):
reg_closure: 19B-A-Q5 19B-A-Q19 21S-B-Q17 23A-A-Q24 23A-B-Q24 24A-A-Q3 24A-A-Q10 24X-A-Q3 24X-A-Q11 25A-A-Q6
25A-B-Q6 25A-C-Q16 SAMP-19-Q6 SAMP-19-Q15.
cfl_props: 19B-B-Q17 19B-B-Q22 21S-A-Q15 21S-A-Q22 21S-B-Q15 23A-A-Q15 23A-A-Q19 23A-B-Q10 23A-B-Q15 24A-B-Q6
24A-B-Q15 24A-C-Q15 24X-A-Q16 24X-C-Q10 25A-A-Q12 25A-B-Q14 26A-A-Q4.

## Tools (all free, decided)

- **Animation: HyperFrames** (HeyGen, Apache-2.0, npm `hyperframes`, Node ≥ 22 + FFmpeg — both present).
  HTML/CSS/GSAP scenes rendered deterministically to MP4 in headless Chrome. Chosen over Manim because scenes are
  HTML: they reuse the bank's KaTeX→MathML pipeline (`tools/render_math.js`), `bidi.js`, and the app's color
  tokens, and the browser does Hebrew RTL + LTR math correctly. Manim needs a LaTeX install and handles Hebrew
  poorly. **Fallback** if HyperFrames blocks us: an in-repo puppeteer-core frame stepper + FFmpeg, same HTML.
- OneTake / "Collage B-roll" / "Claude Animation Base": not verifiable as real products, and B-roll/avatars don't
  serve step-by-step math. Not used.
- **Voice: edge-tts**, `he-IL-HilaNeural`. Its word-boundary events time the subtitles and the animation cues.
  Backup only if edge-tts is unusable: Phonikud (open Hebrew G2P) + an open TTS model.
- FFmpeg for muxing, loudness normalization (EBU R128, −16 LUFS), and burning subtitles if not done in HTML.

## How a video is built (shape, details left to the builder)

- One folder per video: `videos/<course>/<ID>/`, committed. Contains a Python script source (raw strings, like
  `tools/needhelp`) that:
  - imports the level's verified machines from `tools/needhelp/<course>/<ID>.py` / `tools/verify/needhelp/lib.py`
    and asserts every new example (language, run trace, subset table, derivation, stack trace) with the
    simulators — the build fails on any mismatch, like `Q()` does;
  - holds the narration as a list of **beats**; each beat has `say` (phonetic text sent to TTS), `sub` (the course
    spelling shown as subtitle, `$TeX$` allowed) and the animation cue(s) it drives.
- Diagrams in animations are **SVG generated from the verified definitions** (layout positions given by hand per
  example). Exam questions whose diagram is a raster show the original `images/exams/*.png` (never redrawn), with
  highlight overlays only.
- A shared builder (e.g. `tools/video/`) renders TeX with the existing pipeline, synthesizes TTS per beat, builds
  the HyperFrames composition timed to the audio, renders, muxes. MP4s go to gitignored `videos/out/`.
- **Pronunciation lexicon** (`videos/lexicon.py`, shared): course term → spoken form (אס״ד, אסל״ד, ח״ה, Rank,
  $q_0$, $\varepsilon$, $a^n b^n$, `σ,x→y`, Σ*, …). Built from a listening test before the pilot.

## Visual style (builder's call within these lines)

- App look: dark theme tokens from `styles.css`, the same callout colors as lessons (🔑 rule, ⚠️ trap, example box).
- Layout: animation stage on the left (LTR math/diagrams), Hebrew text panel on the right, subtitle band at the
  bottom (2 lines max, RTL, math LTR inside). Exam question shown like the app's question card, with the id.
- Current state highlighted (fill + pulse), current letter underlined in the word, stack drawn as a vertical
  column. Large type (subtitle ≥ 44 px at 1080p).

## Quality gates per video

1. Script asserts pass (simulators) and `$…$` has no Hebrew.
2. Every exam id used exists in `questions.json`, its key matches what the video declares correct; boss ids not
   used.
3. Render check: no clipped math, subtitles inside the safe area (screenshot frames like `tools/shoot.js`).
4. Listen-through for pronunciation; terms fixed in the lexicon, not ad hoc.
5. A blind subagent review of the script against the level + questions (definitions, conventions, trap).

## Process

1. Approve this doc → implementation plan.
2. Listening test for the lexicon, then **pilot F01 end to end**. Stop for Adir's approval (style, pace, voice).
3. Then course by course, in order (no exam deadline): fa → nerode → classify (+K06a/b) → cf, each checked
   against its questions.
4. Listening (Adir's choice): every video gets an automated Hebrew speech-to-text round-trip that flags course
   terms not heard as expected; Adir listens to the first video of each course and spot-checks the rest. Fixes go
   into the shared lexicon and affected videos are re-rendered.

## Linking from the app

- Adir uploads each MP4 to **YouTube as unlisted** (needs his account; manual upload is simplest).
- Add an optional `video` argument to `level(...)` in `tools/needhelp/nh.py` (YouTube id), emitted into the level
  JS; `course-ui.js` shows a "▶ צפה בסרטון" button on the lesson screen that opens the video in a new tab (no
  embed, keeps the site static/offline-friendly). K06 shows three buttons (K06, K06a, K06b).
- Bump `?v=N` in `index.html` when shipping.

## Calls made by Claude (not yet confirmed by Adir)

- Normal videos may reuse the level's **lesson** examples, but never solve that level's own **quiz** questions
  (keeps the in-app quiz a test); worked examples beyond the lesson are new, machine-verified machines.
- If no cited question of a level has a real trap, the anchor may be any uncited bank question of the topic
  (never a boss id; the uncited pool is ~145 questions, enough for bosses and K06a/b too).
- "Extra care" videos (N01–N08, K06, K06a, K06b) may run up to ~10 min instead of being split further.

## Left to the builder

Scene timing, exact layouts, GSAP easing, which cited exam question is the anchor (must have a real trap), SVG
layout positions, intro/outro length, file names inside `videos/<course>/<ID>/`.
