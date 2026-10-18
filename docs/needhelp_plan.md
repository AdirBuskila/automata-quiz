# "צריך עזרה?" — plan for the four guided courses

Spec: `course-factory/docs/superpowers/specs/2026-10-17-course-factory-design.md` §3.4. Shell ported from
`machine-learning-quiz` (course-ui.js, courses.js, course_check.js, course_flow.js and the render fix a7b795e),
adapted to this app's engine (option objects with ids, MathML built at build time, `bidi.js` isolates).

## Which four areas (from the bank, 349 questions)

| bank topic | questions | note |
|---|---|---|
| classify | 70 | biggest family; pumping lemma (9 more in `pumping_reg`), closure (20 + 23) feed it |
| nerode | 62 | the brief calls it "the heaviest topic in the course" |
| regex | 44 | + nfa 23 + dfa 12 = 79 questions on finite automata and expressions |
| cfg | 39 | + pda 36 = 75 questions |
| nfa / cfl_props / reg_closure / dfa / basics / pumping_reg | 23 / 23 / 20 / 12 / 11 / 9 | folded into the four courses |

The suggested candidates (automata and regex, pumping lemma, CFG and PDA) were confirmed, with one change: **Nerode /
Rank / minimization is its own course** (62 questions, 15 on "how many states", 15 on Rank of operations), and the
**pumping lemma lives inside the classification course**, next to the closure properties and the CFL/non-CFL
tools it is always used with.

| course id | title | bank topics | levels (last = 🏆 boss) |
|---|---|---|---|
| `fa` 🔀 | אוטומטים סופיים וביטויים רגולריים | dfa, nfa, regex | F01–F08 |
| `nerode` 📏 | נרוד, Rank ומינימיזציה | nerode | N01–N08 |
| `classify` 🗂️ | סיווג שפות ולמת הניפוח | classify, pumping_reg, reg_closure, cfl_props | K01–K08 |
| `cf` 🥞 | דקדוקים ואוטומט מחסנית | cfg, pda | G01–G08 |

Each course: 7 teaching levels of 5 original questions (lesson first, teach before you ask) and a boss of 5 real bank
questions pulled by id (never cited in a lesson, so the peek cannot show their answer).

## Level ladders

- **fa**: run a DFA · DFA structure, product, pigeonhole · NFA and epsilon moves · subset construction and sizes ·
  reading/writing regexes · comparing regexes · automaton to regex · boss.
- **nerode**: separating suffix and classes · Rank of small languages and the trap state · Rank of pattern languages ·
  proving Rank = k (DFA and separating set) · the x,y family · Rank of operations · infinite Rank · boss.
- **classify**: hierarchy and the classification algorithm · regular languages in disguise · proving non-regularity ·
  pumping game (regular) · nested vs crossing, intersection with a regular language · closure properties ·
  pumping game (CFL) · boss.
- **cf**: reading a grammar · decoding (nesting, concatenation, union, substitution) · which grammar generates L,
  strict containment · CNF, right-linear, ambiguity · PDA runs (accept = accepting state AND empty stack) · L(M) by the
  balance equation · PDA theory, invented models, classification of L(M) · boss.

## How the answers are checked

Courses are written in Python (`tools/needhelp/<course>/<ID>.py`). An option is built with `C(text, cond)` where `cond`
is computed by a simulator in `tools/verify/needhelp/lib.py` (DFA/NFA runs, subset construction, minimization, product,
regex parser, CFG string-fixpoint and derivation counting, PDA runner with the course's acceptance convention, Nerode
class estimation, separating-set test, pumping-lemma game solvers for the regular and CFL lemmas, classification
certificates). `nh.Q` refuses to build unless **exactly one** option is true. `J(text, truth)` marks the few conceptual
statements that no simulator can decide (listed in the build line). Everything is brute force over all words up to
length 8 (or exact, e.g. DFA equivalence by product emptiness). `python tools/verify/needhelp/<id>/check.py` re-imports
the course and cross-validates the simulators themselves against independent implementations (`re`, derivation search,
a second PDA runner).

Pipeline: `python tools/build_courses.py` (TeX to MathML through `render_math.js`, writes `courses/<id>/<ID>.js`) then
`node tools/course_check.js --sync`, `node tools/course_flow.js all light mobile`.
