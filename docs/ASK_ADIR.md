# ASK ADIR — open questions

Paths are relative to `C:\Users\Adir\Desktop\BSC\שנה ג\אוטומטים ושפות פורמליות`.
Section A items are **already in the bank** (kept, key from the official solution) — they only
need a yes/no. Section B items are **not in the bank** until you answer.

## A. In the bank — please confirm

### Course conventions (affect several answers)
1. **PDA acceptance** — the exam formula sheet says a word is accepted only if the run ends in an
   accepting state **and with an empty stack**. All PDA answers/explanations follow this (it is
   what makes the official keys right). ✅ Resolved from the formula sheet; listed for visibility.
2. **CNF and `S→ε`** — `25A-A-Q15` (solution p.10): the key ד needs the course's Chomsky normal
   form to allow `S→ε` (L(G)=(ΣΣ)* contains ε); otherwise ג would be true. Is that the course convention?

### Keys taken from the solution's text (no yellow highlight on that question)
3. `21S-A-Q9` (solution p.5) — key ג from the blue "נכון" note.
4. `21S-A-Q24` (solution p.14) — key ד from the explanation ("קיים אלגוריתם יעיל").
5. `21S-B-Q25` (solution p.15) — key ב from the blue "נכון" note.
6. `21S-A-Q7` (solution p.4) — ג highlighted yellow **and** ב marked green "נכון"; both claims are
   true, so both are accepted (`acceptedIds: [b, c]`). OK?

### Dates / labels
7. `24X-A` (short semester מועד א) — both PDF covers say **01/04/2024**; the filenames say 4.1.2024.
   The app uses 1.4.2024.
8. `25A-C` (מועד ג) — cover of file `1…` says **18/05/2025**; filenames say 24.5.2025. The app uses 24.5.2025.

### Notes found in the sources
9. `24A-A-Q9` (solution p.7) — green note: "בטופס הבחינה הושמטה אחת התשובות האפשריות של שאלה זו".
   The exam PDF shows all 4 options (same as the solution), key ב is clearly right. Kept.
10. `24X-A-Q16` and `25A-B-Q16` have no "איזו מהטענות…" line in the print — kept as printed.

### Moodle evidence
11. `מבדקים במודל/בוחן 1/100/100 (2).pdf` — is this your single 100/100 attempt (24.11.2025)? It is
    the only evidence for MQ1 questions 4 (|L1·L2|=4) and 8 (max accepting states 2^(n−1)).
12. `בוחן 3/בוחן 3/שאלה 1–4.jpeg` show "תשובה נשמרה" — were these picks unchanged at submission
    (the attempt scored 100)? They key MQ3 Q1–Q4.

## B. Not in the bank — need an answer

### Moodle — need the correct answer
- `מבדקים במודל/בוחן 1/100/100 (3).pdf` — is this a graded-100 attempt (the "101" is handwritten)?
  If yes, MQ1 variants 3b (4-state DFA, pick 1100101) and 4b (NFA, pick 010100) can be added.
- MQ1 6b "ε∈L ⟺ ε∉L̄" (`100.docx`, `100 (1).docx`, `שאלות תשפה/8.jpg`) — picks "נכון", no feedback.
- `בוחן 2/100_100/` — which set is the 100/100 attempt: `1–4.jpg` or the `_v2` files?
- `בוחן 2` ε-NFA→regex question: `4.jpg`, `שאלות תשפה/5.jpg`, `/15.jpg` pick `(11)*((10)*(00)*)*`
  but `בוחן 2/2.png` picks `(11)*(00)*(10)*` — which is right?
- `שאלות תשפה/12.jpg` vs `/14.jpg` (regex for even # of 0s) — the picks disagree.
- No key at all: בוחן 2 questions E–J, בוחן 3 loose `שאלה 1.png`–`3.png` (palindromes, Rank(L·L),
  PDA membership), `שאלות תשפה/7.jpg, 9.jpg (blurry), 11.jpg`.

### Exams
- **`19B-A-Q10`** — NOT in the bank. The exam (`2019/סמסטר ב/מועד א/…27.6.19 מבחן.pdf` p.4) asks about
  `L={u c u′ | #a(u)=#a(u′) and #b(u)=#b(u′)}`, but both solutions (v1 p.7, v2 p.6) key a different
  language `{u u′ | |u|=|u′| …}` (answer ד, not CFL). Our own derivation also gives ד for the printed
  language. Add it with key ד?
- `מבחנים ופתרונות/2023/סמסטר ב/מועד ב` — exam without solution, and open-ended anyway → skipped.
