# Authoring a level video — rules (approved pilot: videos/fa/F01/F01.py)

Read first: `CLAUDE.md`, `docs/superpowers/specs/2026-10-28-video-course-design.md`, `videos/README.md`,
`tools/video/vid.py`, `tools/video/stage.py`, `videos/lexicon.py`, and the pilot `videos/fa/F01/F01.py` end to end.
F01 is the approved reference for pace, tone, structure and code style: copy its shape.

## What a video is

- One file `videos/<course>/<ID>/<ID>.py` defining `VIDEO = Video(id, course, title, scenes, bank={id: correct})`.
- 5–8 min (Nerode N01–N08 and closure K06/K06a/K06b may run to ~10). Scenes, in order:
  1. title (layout "title": kicker `<ID> · <course name>`, the level title, the level goal);
  2. concept — the level's `lesson` (tools/needhelp/<course>/<ID>.py) in its own words, terms and notation, expanded;
  3. 1–2 worked examples animated step by step (run, construction, derivation, stack, separating set, split…);
  4. one real exam question (bank id on screen via `<span class="qid">`), solved by elimination, **the trap named**;
  5. recap ~20 s: the level's 🔑 rules as cards.
- Boss levels (F08, N08, K08, G08): no new concept; a short "how to attack an exam question" opener, then 3–4 bank
  questions of the course's topics that NO level cites and that are NOT in that boss quiz (`vid.py` refuses boss ids),
  each solved with its trap, then a recap of the course's top rules.
- K06a (closure of regular languages) and K06b (closure of CFLs) are bonus videos: build them from the uncited
  closure questions listed in the design doc (reg_closure for K06a, cfl_props for K06b), 3–5 questions each, plus the
  closure table / fixed counterexamples of the K06 lesson. Files `videos/classify/K06a/K06a.py`, id `"K06a"`.

## Correctness (non-negotiable)

- Sources of truth in order: the level's lesson/goal (`tools/needhelp/<course>/<ID>.py`), `questions.json`, the course
  conventions in `CLAUDE.md`. Never invent a definition. PDA acceptance = accepting state AND empty stack.
  Automaton→regex = "רישא וסיבובים" (never Arden). Pumping constant written `n` as in exams. Classification follows the
  formula-sheet table (CLAUDE.md).
- Every machine/grammar/regex/PDA/language claim in a video is asserted at import with the simulators
  (`from nh import *` gives `tools/verify/needhelp/lib.py`: DFA/NFA/Rx/CFG/PDA, `classes`, `rank_est`, `separable`,
  `is_separating_set`, `pump_breaks`, …). Every run shown is computed, not typed (see `run_dfa` and F01's `raster_run`).
- Exam questions: transcribe the figure's machine from `images/exams/<id>.png` (look at it), assert it reproduces the
  bank key (`BANK[id]["correctId"]`) and what the bank explanation says, and pass `bank={id: key}` to `Video`.
  If the bank's explanation is sloppy, the video explains correctly; the key is never questioned.
- Do NOT solve the level's own quiz questions (the `Q(...)` items in its .py) or reuse their machines; reusing the
  lesson's own examples is fine. Prefer an exam anchor the lesson cites; if none has a real trap, any bank question of
  the topic that is not a boss-quiz id.
- Never name an option by letter or position (options are shuffled in the app): say the option's content.
  `stage.options` draws bullets, not letters.

## Lessons from the first review (K01–K05)

- Write implications in words ("אם …, אז …"), never as ← / → / ⇒ arrows in Hebrew text: read in the other
  direction they state the converse (e.g. the pumping lemma). Never mix arrow directions in one view.
- An intuition ("the stack is already used up", "it has to remember n") is not a proof. Say it's the intuition and
  name the actual proof tool the course uses (pumping lemma, intersection with a regular language, separating set,
  the formula-sheet table).
- Check every "why" sentence against the definition of the language, not just the conclusion (a correct verdict
  with a wrong reason was found).
- Not even an option, word or example from the level's quiz may appear in a worked example.
- Hebrew agreement: letters are feminine (אות): "שתי $b$", "ארבע $a$"; keep subtitle and `say` in the same gender.

## Narration and subtitles

- `P(sub, say=None, do=..., hold=...)`: `sub` = subtitle in course spelling, `$TeX$` for all math, **no Hebrew inside
  TeX**, ≤ 120 visible chars. Natural Israeli-student Hebrew, short sentences, female narrator (the presenter is Shosh; the TTS voice is he-IL-HilaNeural) — but address
  the viewer in plural (שימו לב, נריץ).
- `say` is derived through `videos/lexicon.py`; any TeX the lexicon can't speak needs an explicit `say=`. Spell words
  over the alphabet with `lexicon.word_say` (it gives the STT-checked forms אֵיי / בִּי), states with
  `lexicon.state_say`. Plain digits outside TeX are read as numbers — write them in words in `say`.
  Step-by-step lists read best as "אחת: לקיו אחת." (colon, then period per step). Hebrew letters as words:
  "אָלֶף", "בֵּית". Read regex `+` as "או", `*` as "כוכבית"; `\to` in grammars as "עובר ל" / "גוזר".
- Do NOT edit the shared files (`tools/video/vid.py`, `stage.py`, `shosh.py`, `video.css`, `videos/lexicon.py`):
  four authors work in parallel. Put new widgets in `tools/video/w_<course>.py` (fa / nerode / classify / cf) and
  extra CSS in a `<style>` block inside your stage HTML, class names prefixed by the course (`.cf-…`).
  If a term needs a lexicon entry, use `say=` now and list the request in your report.

## Layout

- 1920×1080. Stage (left) 60..1120 × 118..838, panel (right) 1180..1860 × 118..838, subtitles bottom-center
  (≤1360 px wide), **Shosh** (the presenter) in the bottom-right corner (x ≥ 1700, y ≥ 838): keep everything else out of her box.
- Ids must be unique across the whole video (prefix per scene). Elements with class `h` start hidden; `show/hide`.
- Diagrams: `stage.dfa_svg` (DFA, NFA with sets/ε, or `edges=[(p, label, r)]` for PDA), `dfa_table`, `tape`,
  `trace`, `verdict`, `card` (rule/trap/ex/plain), `options(…, notes=)`, `raster` (original exam figure + rings/tags;
  never redraw an exam figure). Two things in one spot: `<div class="swap" style="--swap-h:…">` (see F01).

## Check every video before reporting it done

```bash
PY=/c/Users/Adir/AppData/Local/Programs/Python/Python313/python
PYTHONUTF8=1 $PY tools/video/vid.py <ID> --no-render          # asserts + gates + TTS + composition + lint
tools/node_modules/.bin/hyperframes snapshot videos/out/<ID>/proj --at <t1,t2,…> --no-end -o videos/out/<ID>/snap
```
Take times from `videos/out/<ID>/timeline.json`: the end of every scene plus the middle of every animation. Look at
the contact sheet / frames: no overflow, nothing clipped, nothing under Shosh or the subtitles, rings on the right
states, the highlighted thing is the thing being said. Fix and re-check. Do NOT run a full render (no `--no-render`
omitted) and do NOT commit: the lead renders and commits. Git-Bash heredocs and `sed` mangle backslashes and Hebrew:
edit files with the file tools only.
