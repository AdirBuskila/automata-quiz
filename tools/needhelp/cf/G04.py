# -*- coding: utf-8 -*-
import sys, pathlib, re
from itertools import product
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def rules_of(text):
    out = []
    for part in text.split(";"):
        lhs, rhs = part.split("->")
        for alt in rhs.split("|"):
            out.append((lhs.strip(), "" if alt.strip() in ("ε", "") else alt.strip()))
    return out


def cnf_ok(text, start="S"):
    for a, r in rules_of(text):
        if r == "":
            if a != start:
                return False
        elif len(r) == 1:
            if not r.islower() and not r.isdigit():
                return False
        elif len(r) == 2:
            if not (r[0].isupper() and r[1].isupper()):
                return False
        else:
            return False
    return True


def rl_rule_ok(lhs, rhs, start="S"):
    if rhs == "":
        return lhs == start
    return (len(rhs) == 1 and rhs.islower()) or (len(rhs) == 2 and rhs[0].islower() and rhs[1].isupper())


def tex(rules):
    return "$" + rules.replace("->", r"\to ").replace("|", r"\mid ").replace("ε", r"\varepsilon ").replace(";", r",\ ") + "$"


# Q1  Chomsky normal form
R1 = ["S->AB|a;A->a;B->SA", "S->aSb|ε", "S->AB|ε;A->aA|a;B->b", "S->ABC;A->a;B->b;C->c"]
T1 = [cnf_ok(r) for r in R1]
assert T1 == [True, False, False, False]
assert CFG("S->AB|a;A->a;B->SA").lang(7) == {w for w in words("a", 7) if len(w) % 2 == 1}
# Q2  which rule cannot appear in a right-linear grammar
Q2 = [("A", "aB"), ("A", "b"), ("S", ""), ("S", "Ab")]
T2 = [not rl_rule_ok(a, r) for a, r in Q2]
assert T2 == [False, False, False, True]
# Q3  ambiguity
G3 = CFG("S->a|aS|aA;A->a")
amb_aa = G3.count_trees("aa") >= 2
amb_a = G3.count_trees("a") >= 2
G3u = CFG("S->aS|a")
unamb_exists = all(G3u.count_trees(w) <= 1 for w in words("a", 6) if w) and G3u.lang(6) == G3.lang(6)
assert amb_aa and not amb_a and unamb_exists
# Q4  grammar of order n: every right-hand side has exactly n symbols, no epsilon
ORD1 = [CFG("S->A|a;A->S|b"), CFG("S->a|b"), CFG("S->A;A->B|c;B->a")]
fin1 = all(max((len(w) for w in g.lang(8)), default=0) <= 1 for g in ORD1)
ORD2 = CFG("S->AS|aa;A->aa")
inf2 = any(len(w) >= 8 for w in ORD2.lang(8))
assert fin1 and inf2
# Q5  right-linear with N variables, a word of length >= N+1 forces an infinite language
ok5 = True
options_S = ["a", "aS", "aA"]
options_A = ["a", "aS", "aA"]
for sm in product([0, 1], repeat=3):
    for am in product([0, 1], repeat=3):
        rs = [("S", r) for r, f in zip(options_S, sm) if f]
        ra = [("A", r) for r, f in zip(options_A, am) if f]
        if not rs or not ra:
            continue
        txt = ";".join(f"{v}->" + "|".join(r for vv, r in rs + ra if vv == v) for v in "SA")
        g = CFG(txt)
        L = g.lang(10)
        if any(len(w) >= 3 for w in L) and not any(len(w) >= 8 for w in L):
            ok5 = False
assert ok5

LEVEL = level("G04", 4, "🏗️", "צורת חומסקי, ליניארי ימני ורב-משמעיות",
  "לזהות דקדוק בצורת חומסקי ודקדוק ליניארי ימני, להכריע רב-משמעיות, ולהסיק על אינסופיות משובך יונים.",
  r'''
<p>ארבעה סוגי שאלות מבנה על דקדוקים: צורה נורמלית של חומסקי (CNF), דקדוק ליניארי ימני, רב-משמעיות, והגדרות חדשות בתוך השאלה.</p>
<h3>צורת חומסקי (CNF)</h3>
<p>כל כלל הוא $A\to BC$ (<b>שני משתנים</b>) או $A\to a$ (<b>טרמינל יחיד</b>). לפי חומרי הקורס מותר גם $S\to\varepsilon$ (רק למשתנה ההתחלתי). <b>לכל דקדוק ח״ה יש דקדוק שקול ב-CNF</b> (המבחנים מניחים ש-$S\to\varepsilon$ מותר: 25A-A-Q15, 26A-A-Q15). ב-21S-B-Q5, $S\to AN\mid a$, $N\to SA$, $A\to a$ הוא ב-CNF ויוצר את השפה הרגולרית $(aa)^*a$. ב-23A-A-Q18, $S\to00S0\mid1$ לא ב-CNF (צד ימין באורך $4$).</p>
<div class="lesson-trap">⚠️ ההגדרה אינה בדף הנוסחאות, ובמחוונים של 21S-B-Q5 ו-23A-B-Q18 דקדוק עם $S$ בצד ימין <b>כן</b> נחשב CNF. אל תפסלו אפשרות רק בגלל זה.</div>
<h3>דקדוק ליניארי ימני</h3>
<p>כל כלל הוא $A\to a$ או $A\to aB$ (<b>טרמינל, ואחריו לכל היותר משתנה אחד, מימין</b>), ובנוסף מותר $S\to\varepsilon$. לכן $S\to Ab$ <b>אסור</b> (21S-B-Q12). הדקדוקים האלה שקולים בדיוק לשפות רגולריות.</p>
<ul>
<li>דקדוק ליניארי ימני עם $N$ משתנים נותן אסל״ד עם $N+1$ מצבים. ב-25A-B-Q2: $3$ משתנים, ולכן $4$ מצבים, אס״ד לכל היותר $2^4=16$ מצבים, ומילה באורך $18$ מבטיחה מעגל: השפה <b>אינסופית</b> (שובך יונים).</li>
<li>בלי כללי $\varepsilon$ כל צעד גזירה מוסיף טרמינל אחד, ולכן גובה העץ הוא $|w|$ (25A-B-Q16). זה נכון <b>רק</b> לליניארי ימני בלי $\varepsilon$; בדקדוק כללי אין חסם (SAMP-19-Q11: $S\to\varepsilon\mid S$).</li>
<li>$S\to aBa$, $B\to BB\mid b\mid\varepsilon$ יוצר את $ab^*a$, רגולרית, ולכן יש לה דקדוק ליניארי ימני (24A-B-Q7).</li>
</ul>
<h3>רב-משמעיות</h3>
<div class="lesson-rule">🔑 דקדוק הוא <b>רב-משמעי</b> אם יש מילה עם <b>שני עצי גזירה</b> שונים. זו תכונה של <b>הדקדוק</b> ולא של השפה: ב-21S-A-Q2 המילה $ba$ נגזרת בשתי דרכים, ובכל זאת קיים דקדוק חד-משמעי שקול.</div>
<p>ליניארי ימני <b>לא</b> תמיד חד-משמעי: $S\to a\mid aS\mid aA$, $A\to a$ גוזר את $aa$ בשתי דרכים (21S-A-Q7). ב-23A-A-Q18 ($S\to00S0\mid1$) יש משתנה אחד וכלל רקורסיבי אחד, ולכן אין בחירה: חד-משמעי.</p>
<h3>הגדרה חדשה בשאלה</h3>
<p>נסו את הדקדוק הכי פשוט שעומד בהגדרה. 23A-B-Q2: דקדוק מסדר $n$ (כל צד ימין באורך $n$ בדיוק, בלי $\varepsilon$). מסדר $1$ השפה סופית (אותיות בודדות). מסדר $2$ היא יכולה להיות אינסופית: $S\to AS\mid aa$. ב-21S-B-Q24 &quot;דקדוק אלמנטרי&quot; (לכל היותר משתנה אחד בצד ימין): קיימת שפה ח״ה בלי כזה (שרשור שני פלינדרומים).</p>
''',
  [
    Q("איזה דקדוק הוא בצורת חומסקי (כל כלל $A\\to BC$ או $A\\to a$, ו-$S\\to\\varepsilon$ מותר)?",
      [C(tex(r), t) for r, t in zip(R1, T1)],
      why=r"הדקדוק הראשון: $S\to AB$ (שני משתנים), $S\to a$ (טרמינל), $A\to a$, $B\to SA$: כולם בצורה. השני: $aSb$ באורך $3$. השלישי: $A\to aA$ (טרמינל ומשתנה) אינו מותר. הרביעי: $S\to ABC$ באורך $3$.",
      recap="CNF: שני משתנים או טרמינל יחיד"),
    Q("איזה כלל **לא** יכול להופיע בדקדוק ליניארי ימני?",
      [C(f"${a}\\to {r if r else chr(92) + 'varepsilon'}$", t) for (a, r), t in zip(Q2, T2)],
      why=r"בדקדוק ליניארי ימני כל כלל הוא $A\to a$ או $A\to aB$ (המשתנה מימין לטרמינל), ו-$S\to\varepsilon$ מותר למשתנה ההתחלתי. $S\to Ab$ מציב משתנה משמאל לטרמינל, ולכן אסור. $A\to aB$ ו-$A\to b$ וגם $S\to\varepsilon$ חוקיים.",
      recap="ליניארי ימני: A → a או A → aB".replace("A → a או A → aB", "$A\\to a$ או $A\\to aB$")),
    Q("נתון הדקדוק:\n" + gram("S->a|aS|aA;A->a") + "\nאיזו טענה נכונה?",
      [C(r"הדקדוק רב-משמעי: למילה $aa$ שני עצי גזירה", amb_aa), C(r"הדקדוק חד-משמעי כי הוא ליניארי ימני", not amb_aa),
       C(r"לשפה $L(G)$ אין שום דקדוק חד-משמעי", not unamb_exists), C(r"למילה $a$ שני עצי גזירה", amb_a)],
      why=r"$aa$ נגזרת ב-$S\Rightarrow aS\Rightarrow aa$ (עם $S\to a$) וגם ב-$S\Rightarrow aA\Rightarrow aa$: שני עצים, ולכן הדקדוק רב-משמעי. ליניארי ימני לא מבטיח חד-משמעיות. השפה $a^+$ כן יוצרת דקדוק חד-משמעי: $S\to aS\mid a$ (בדקנו שאין מילה עם שני עצים). ול-$a$ עץ יחיד.",
      recap="רב-משמעות היא תכונה של הדקדוק, לא של השפה"),
    Q("דקדוק מסדר $n$ הוא דקדוק שבו כל צד ימין באורך $n$ בדיוק (ללא $\\varepsilon$). I: אם $G$ מסדר $1$ אז $L(G)$ סופית. II: אם $G$ מסדר $2$ אז $L(G)$ סופית. איזו נכונה?",
      [C(r"רק I נכונה", fin1 and inf2), C(r"רק II נכונה", (not fin1) and (not inf2)), C(r"שתיהן נכונות", fin1 and not inf2), C(r"אף אחת לא נכונה", (not fin1) and inf2)],
      why=r"בדקדוק מסדר $1$ כל כלל הוא $A\to a$ או $A\to B$, ולכן המילים היחידות הן אותיות בודדות: השפה סופית (I נכונה). מסדר $2$ יש $S\to AS\mid aa$ עם $A\to aa$ שיוצר $(aa)^+$, אינסופית (II שגויה). בדקנו על כמה דקדוקים מסדר $1$ ועל הדוגמה.",
      recap="מסדר 1 סופית; מסדר 2 יכולה להיות אינסופית"),
    Q(r"$G$ הוא דקדוק ליניארי ימני עם $2$ משתנים ובלי כללי $\varepsilon$, ו-$L(G)$ מכילה מילה באורך $3$ לפחות. מה נכון?",
      [C(r"$L(G)$ אינסופית", ok5), J(r"$L(G)$ סופית", False), J(r"$L(G)$ ריקה", False), J(r"אי אפשר לדעת", False)],
      why=r"דקדוק ליניארי ימני עם $2$ משתנים נותן אסל״ד עם $2+1=3$ מצבים. מסלול מקבל על מילה באורך $3$ עובר ב-$4$ מצבים, ולכן מצב חוזר: מעגל, וניתן לסובב אותו כמה שרוצים. $L(G)$ אינסופית. (בדקנו את הטענה על כל הדקדוקים האפשריים בשני משתנים מעל $\{a\}$.)",
      recap="N משתנים: N+1 מצבים; מילה ארוכה גוררת מעגל"),
  ])
