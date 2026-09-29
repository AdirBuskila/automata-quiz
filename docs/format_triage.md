# Format triage — Automata & Formal Languages (62208)

Phase-1 deliverable. Every exam/quiz file → code, format, question style, counts, answer source,
figures, extraction confidence. Method: PyMuPDF text layer + page renders viewed by eye +
an automatic yellow-highlight key detector + stem-matching across versions. Nothing extracted yet.

## Outcome (M2, 2026-09-30)
All 16 MCQ sittings extracted: **336 exam questions** (only `19B-A-Q10` excluded — see ASK_ADIR),
plus **13 keyed Moodle questions** (MQ1 ×9, MQ3 ×4). Findings made during extraction:
- `24X-A` is really 1.4.2024 (cover) and its solution is גרסה 0 vs exam גרסה 1 (solution order used).
- `25A-C` cover says 18.5.2025; `24A-C`, `25A-C` solutions carry highlights only (explanations derived).
- `21S-A-Q9/Q24`, `21S-B-Q25` have no highlight — key from the solution's written text.
- PDA acceptance = accepting state **and empty stack** (formula sheet) — several keys depend on it.
- `24A-C` and `24X-C` share 9 questions; `25A-A`/`25A-C` share 2.

## Headline (Phase-1 triage)
- **MCQ papers (in scope): 16 sittings, ≈337 questions** (7 × 25 + 9 × 18). All have a text
  layer (no scans), clean embedded raster diagrams, and a solution PDF that is a **full copy of
  the exam with the correct claim highlighted yellow + a worked explanation**.
- **Open-ended papers (out of scope): 12 files / 11 sittings** — all of 2016–2018 and **every
  Semester-B paper 2023–2026** (7 proof questions, "נמקו/בנו/הוכיחו"). Not MCQ; converting would
  mean inventing options.
- **Moodle: ≈33 distinct questions**, of which ~13 have a trustworthy key; the rest go to ASK_ADIR.

## A. MCQ sittings — IN SCOPE
Format for all: text PDF, 4 claims (א–ד) one correct, figures = embedded PNG state diagrams.

| Code | Sitting | Date | Q | Exam file | Key (primary) | Cross-checks | Figures | Confidence |
|---|---|---|---|---|---|---|---|---|
| **26A-A** | 2026 סמ א מועד א | 1.2.2026 | 18 | `2026/סמסטר א מועד א.pdf` | `…מועד א - פתרון.pdf` (yellow) | detector | ~9 | high — **flagship** |
| 25A-A | 2025 סמ א מועד א | 9.2.2025 | 18 | ✓ | פתרון (yellow) | detector | ~9 | high |
| 25A-B | 2025 סמ א מועד ב | 6.3.2025 | 18 | ✓ | פתרון (yellow) | detector | ~8 | high |
| 25A-C | 2025 סמ א מועד ג | 24.5.2025 | 18 | — (solution only) | `1אוטומטים…פתרון.pdf` | `2אוטומטים…` = **same exam, questions+options permuted** (18↔18 bijection) → content-matched 2nd key | ~5 | high |
| 24A-A | 2024 סמ א מועד א | 20.3.2024 | 18 | ✓ | פתרון | detector | ~9 | high |
| 24A-B | 2024 סמ א מועד ב | 11.4.2024 | 18 | ✓ | פתרון | detector | ~9 | high |
| 24A-C | 2024 סמ א מועד ג | 17.5.2024 | 18 | — (solution only) | פתרון | detector | ~7 | high |
| 24X-A | 2024 סמ א **קצר** מועד א | 4.1.2024 | 18 | ✓ | פתרון | detector | ~9 | high |
| 24X-C | 2024 סמ א **קצר** מועד ג | 14.4.2024 | 18 | — (solution only) | פתרון | detector | ~5 | high |
| 23A-A | 2023 סמ א מועד א | 31.1.2023 | 25 | ✓ (text layer in reversed visual order — read from image) | פתרון | detector | ~8 | high |
| 23A-B | 2023 סמ א מועד ב | 23.2.2023 | 25 | the "מבחן" file **is a copy of the solution** (identical text) | פתרון | detector | ~13 | high |
| 21S-A | 2021 קיץ מועד א | 30.9.2021 | 25 | ✓ | פתרון | detector | ~9 | high |
| 21S-B | 2021 קיץ מועד ב | 2.11.2021 | 25 | ✓ | פתרון | detector | ~14 | high |
| 19B-A | 2019 סמ ב מועד א | 27.6.2019 | 25 | ✓ (v1) | **`2019/סמסטר א/…27.6.19 פתרון.pdf` — mis-filed, it is the v1 solution of this exam** | `גרסה 2 פתרון` (permuted + some options reworded) · איגוד pp.18–37 | many (≈50 incl. formula images) | high; option text from exam file (solution has inline counterexamples) |
| 19B-B | 2019 סמ ב מועד ב | 28.7.2019 | 25 | ✓ | `…28.7.19 פתרון.pdf` (v1, matches exam 25/25) | `גרסה 2 פתרון` (permuted) · איגוד pp.38–54 | many | high |
| SAMP-19 | 2019 מבחן לדוגמה | 27.6.2019 | 25 | ✓ | פתרון | איגוד pp.1–17 | many | high; ~5 questions shared with 19B-A → `dedupKey` |

Detector run (all 16 keys found; `?` only where the highlight covers pure math with no letter —
resolved visually during extraction). Question numbering/lockOrder: "כל הטענות האחרות לא נכונות"
and "טענה I / II" formats are common → `lockOrder`.

## B. Open-ended — OUT OF SCOPE (recommend skip)
| Sitting | Files | Style |
|---|---|---|
| 2016 סמ ב מועד א (23.6.16), 2016 קיץ מועד א (28.9.16) | exam + scanned handwritten solution | 7 open questions, all compulsory |
| 2017 קיץ מועד א (19.10.17) | exam + scanned solution | open |
| 2018 קיץ מועד א/ב (16.10.18, 18.11.18) | exam + solution | "הוכיחו/הפריכו" + constructions |
| 2023 סמ ב מועד א (26.6.23) | exam + solution | 7 open |
| 2023 סמ ב מועד ב (17.7.23) | exam only, **no solution** | 7 open |
| 2024 סמ ב מועד א/ב/ג (18.7, 8.8, 12.9.24) | exam + solution | 7 open |
| 2025 סמ ב מועד א | exam + solution | 7 open |
| **2026 סמ ב מועד א (18.6.26)** | exam + solution | 7 open, choose 5 |
| איגוד pp.55–68 | homework solutions 1–3 (2019) | open |
| `תרגולים תשפו/*` | tutorial sheets + solutions | open (only תרגול 0 has a few prerequisite MCQs) → learn mode |

## C. Moodle quizzes (images / docx / pdf) — `source:"moodle"`
All single-answer MCQ or true/false, typeset and legible (WhatsApp photos readable despite moiré;
TASHPA 9 blurry). Most shots are **mid-attempt** ("תשובה נשמרה") → they show the student's pick,
not the key. `שאלות תשפה/` is **not a separate quiz**: 2025 copies of MQ1 (1,2,3,4,6,8) and MQ2
(5,7,9–15) plus 4 unmatched items.

| Quiz | Distinct Q | Key by explicit feedback | Key = pick in a proven 100 attempt | No reliable key |
|---|---|---|---|---|
| MQ1 (בוחן 1) | 12 (6 slots × 2 variants) | 7 (1a,1b,2a,3a,4a,5a,6a) | 2 (2b, 5b — in `100 (2).pdf`, grade 100/100 screen) | 3 (3b, 4b: only in `100 (3).pdf` whose "101" is handwritten; 6b: docx picks only) |
| MQ2 (בוחן 2) + TASHPA extras | 14 | 0 | 0 proven (100/100 screen exists but two attempt sets `1–4.jpg` vs `_v2`) | 14 — incl. **conflict** on Q-D (ε-NFA→regex) and "even # of 0s" |
| MQ3 (בוחן 3) | 7 | 0 | 4 (`בוחן 3/בוחן 3/שאלה 1–4` next to `ציון 100` = 4×25) | 3 (loose `שאלה 1–3.png` attempt, no score) |
| **Total** | **33** | **7** | **6** | **20 → ASK_ADIR** |

83-attempt check: agrees with the key on 5/6 (differs on 5a: picked 2n, key 2^n) — consistent
with a score of 83; used only where it agrees.

## Recommended scope ("cutoff")
The dividing line is **format, not year**: include **all 16 MCQ sittings 2019–2026** (≈337 Q,
≈300 after dedup) + the ~13 keyed Moodle questions; skip every open-ended paper (2016–2018 and all
Semester-B 2023–2026, including 2026 Sem B). Flagship = **26A-A**.
