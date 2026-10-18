# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def lang_is(g, alpha, pred, n=9):
    return g.lang(n) == {w for w in words(alpha, n) if pred(w)}


def P(letters, cond):
    return lambda w: (lambda t: t is not None and cond(*t))(parts(w, letters))


# Q1  S -> aSd | B ; B -> bBd | eps
G1 = CFG("S->aSd|B;B->bBd|ε")
O1 = {"d=a+b": P("abd", lambda a, b, d: d == a + b), "d=a": P("abd", lambda a, b, d: d == a),
      "d=b": P("abd", lambda a, b, d: d == b), "d=|a-b|": P("abd", lambda a, b, d: d == abs(a - b))}
T1 = {k: lang_is(G1, "abd", p) for k, p in O1.items()}
assert T1 == {"d=a+b": True, "d=a": False, "d=b": False, "d=|a-b|": False}
# Q2  substitution  S -> 0M1 | eps ; M -> 0S11
G2 = CFG("S->0M1|ε;M->0S11")
O2 = {"2n,3n": P("01", lambda a, b: b * 2 == a * 3 or (a * 3 == b * 2)), "n,n": P("01", lambda a, b: a == b),
      "2n,2n": P("01", lambda a, b: a == b and a % 2 == 0), "n,3n": P("01", lambda a, b: b == 3 * a)}
O2["2n,3n"] = P("01", lambda a, b: a % 2 == 0 and b == 3 * a // 2)
T2 = {k: lang_is(G2, "01", p) for k, p in O2.items()}
assert T2 == {"2n,3n": True, "n,n": False, "2n,2n": False, "n,3n": False}, T2
# Q3  concatenation
G3 = CFG("S->AB;A->aAb|ε;B->bBa|ε")
O3 = {"n,n+m,m": P("aba", lambda x, y, z: y == x + z), "n,n,n": P("aba", lambda x, y, z: x == y == z),
      "any": P("aba", lambda x, y, z: True), "n,2n,n": P("aba", lambda x, y, z: y == 2 * x and z == x)}
T3 = {k: lang_is(G3, "ab", p) for k, p in O3.items()}
assert T3 == {"n,n+m,m": True, "n,n,n": False, "any": False, "n,2n,n": False}, T3
# Q4  union
G4 = CFG("S->A|B;A->aAb|ab;B->bBa|ba")
AB = lambda w: re.fullmatch("(a+)(b+)", w) is not None and w.count("a") == w.count("b")
BA = lambda w: re.fullmatch("(b+)(a+)", w) is not None and w.count("a") == w.count("b")
O4 = {"union": lambda w: AB(w) or BA(w), "with eps": lambda w: AB(w) or BA(w) or w == "",
      "eq": lambda w: w.count("a") == w.count("b"), "only ab": lambda w: AB(w)}
T4 = {k: lang_is(G4, "ab", p) for k, p in O4.items()}
assert T4 == {"union": True, "with eps": False, "eq": False, "only ab": False}, T4
# Q5
G5 = CFG("S->aTa|bTb;T->aT|bT|ε")
O5 = {"same": lambda w: len(w) >= 2 and w[0] == w[-1], "pal": lambda w: w == w[::-1],
      "diff": lambda w: len(w) >= 2 and w[0] != w[-1], "even": lambda w: len(w) % 2 == 0}
T5 = {k: lang_is(G5, "ab", p) for k, p in O5.items()}
assert T5 == {"same": True, "pal": False, "diff": False, "even": False}, T5

LEVEL = level("G02", 2, "🧩", "פענוח דקדוקים: קינון, שרשור, איחוד והצבה",
  "לכתוב את השפה של דקדוק בנוסח קבוצה, כולל שני פרמטרים בלתי תלויים, ולבדוק בעזרת מילים קצרות.",
  r'''
<p>25 מתוך 39 שאלות הדקדוק בבנק הן &quot;פענח את הדקדוק&quot;. המיומנות: לקרוא דקדוק ולכתוב את השפה שלו בנוסח קבוצה תוך חצי דקה.</p>
<h3>כלי הקינון והשרשור</h3>
<ul>
<li><b>קינון:</b> הכלל $S\to aSd\mid B$ עוטף את מה ש-$B$ גוזר ב-$a\ldots d$. אם $B\to bBd\mid\varepsilon$, אז לכל $b$ יש $d$ ממול, ולכל $a$ יש $d$ ממול: סה״כ $d^{n+m}$. המונה החיצוני עוטף את הפנימי.</li>
<li><b>שרשור:</b> $S\to AB$: מה ש-$A$ גוזר ואחריו מה ש-$B$ גוזר, והפרמטרים של $A$ ו-$B$ <b>בלתי תלויים</b>. לכן $A\to aAb\mid\varepsilon$ ו-$B\to bBa\mid\varepsilon$ נותנים $a^nb^nb^ma^m=a^nb^{n+m}a^m$.</li>
<li><b>איחוד:</b> $S\to A\mid B$: או מה ש-$A$ גוזר או מה ש-$B$ גוזר.</li>
</ul>
<div class="lesson-ex"><b>הצבה.</b> $S\to0M1\mid\varepsilon$ ו-$M\to0S11$: מציבים את $M$ ומקבלים $S\to00S111\mid\varepsilon$, כלומר $\{0^{2n}1^{3n}\}$. אותו עקרון כמו ב-25A-A-Q9 ו-25A-C-Q8: ההצבה מבטלת משתני עזר ומראה מה השפה.</div>
<div class="lesson-ex"><b>$a^ib^k$ עם $i\ne k$ (23A-B-Q7, 24A-C-Q17, 24X-C-Q8).</b> $T\to aTb\mid\varepsilon$ גוזר $a^nb^n$. $A\to aA\mid aT$ מוסיף לפחות $a$ אחד משמאל ($i>k$), $B\to Bb\mid Tb$ מוסיף לפחות $b$ אחד מימין ($k>i$). האיחוד הוא $i\ne k$. המסיחים $i>k$ ו-$k>i$ הם חצי מהשפה. המילה הריקה לא בשפה, כי $A$ ו-$B$ תמיד מוסיפים אות.</div>
<div class="lesson-trap">⚠️ <b>תמיד בדקו את $\varepsilon$.</b> רוב המסיחים נופלים עליה או על מילה באורך $1$ עד $3$. ב-19B-A-Q11 הכללים $S\to aa\mid bb$ מיותרים (פלינדרומים), וב-23A-A-Q7 כל המילים באורך זוגי אינן פלינדרומים, אבל &quot;כל המחרוזות באורך זוגי&quot; נופלת על $\varepsilon$.</div>
<p>תבניות נוספות מהבחינות: 24A-A-Q7 ($a^nb^mc^k$ עם $k=m+n$), 24X-A-Q8 ($a^nb^ka^kb^n$), 24A-C-Q12 ו-24X-C-Q2 (לפחות שלושה $1$), 21S-B-Q2 ($0^n1^na^kb^k$).</p>
''',
  [
    Q("נתון הדקדוק:\n" + gram("S->aSd|B;B->bBd|ε") + "\nמהי $L(G)$?",
      [C(r"$\{a^nb^md^{n+m}\mid n,m\ge0\}$", T1["d=a+b"]), C(r"$\{a^nb^md^n\mid n,m\ge0\}$", T1["d=a"]),
       C(r"$\{a^nb^md^m\mid n,m\ge0\}$", T1["d=b"]), C(r"$\{a^nb^md^{|n-m|}\mid n,m\ge0\}$", T1["d=|a-b|"])],
      why=r"$B$ גוזר $b^md^m$. $S$ עוטף אותו ב-$a^n\ldots d^n$, ולכן $a^nb^md^md^n=a^nb^md^{n+m}$. בדקנו את הדקדוק על כל המילים עד אורך $9$. $a^nb^md^n$ ו-$a^nb^md^m$ הן חצי מהמידע: $d$ סוגר גם את $a$ וגם את $b$.",
      recap="המונה החיצוני עוטף את הפנימי: d^(n+m)".replace("d^(n+m)", "$d^{n+m}$")),
    Q("נתון הדקדוק:\n" + gram("S->0M1|ε;M->0S11") + "\nמהי $L(G)$?",
      [C(r"$\{0^{2n}1^{3n}\mid n\ge0\}$", T2["2n,3n"]), C(r"$\{0^n1^n\mid n\ge0\}$", T2["n,n"]),
       C(r"$\{0^{2n}1^{2n}\mid n\ge0\}$", T2["2n,2n"]), C(r"$\{0^n1^{3n}\mid n\ge0\}$", T2["n,3n"])],
      why=r"מציבים: $S\to0(0S11)1=00S111$, ולכן כל סיבוב מוסיף שני $0$ ושלושה $1$, ואחרי כל גזירה של $\varepsilon$ מתקבל $0^{2n}1^{3n}$. המילה הריקה בשפה ($n=0$). בדקנו עד אורך $9$.",
      recap="הצבה: S → 00S111 | ε".replace("S → 00S111 | ε", "$S\\to00S111\\mid\\varepsilon$")),
    Q("נתון הדקדוק:\n" + gram("S->AB;A->aAb|ε;B->bBa|ε") + "\nמהי $L(G)$?",
      [C(r"$\{a^nb^{n+m}a^m\mid n,m\ge0\}$", T3["n,n+m,m"]), C(r"$\{a^nb^na^n\mid n\ge0\}$", T3["n,n,n"]),
       C(r"$\{a^nb^ma^k\mid n,m,k\ge0\}$", T3["any"]), C(r"$\{a^nb^{2n}a^n\mid n\ge0\}$", T3["n,2n,n"])],
      why=r"$A$ גוזר $a^nb^n$ ו-$B$ גוזר $b^ma^m$, <b>בלי קשר</b> בין $n$ ל-$m$. השרשור הוא $a^nb^{n+m}a^m$. $\{a^nb^na^n\}$ היא המקרה $m=n$ בלבד (הכלה ממש). בדקנו עד אורך $9$.".replace("<b>", "**").replace("</b>", "**"),
      recap="שרשור: שני פרמטרים בלתי תלויים"),
    Q("נתון הדקדוק:\n" + gram("S->A|B;A->aAb|ab;B->bBa|ba") + "\nמהי $L(G)$?",
      [C(r"$\{a^nb^n\mid n\ge1\}\cup\{b^na^n\mid n\ge1\}$", T4["union"]), C(r"$\{a^nb^n\mid n\ge0\}\cup\{b^na^n\mid n\ge0\}$", T4["with eps"]),
       C(r"$\{w\mid\#_a=\#_b\}$", T4["eq"]), C(r"$\{a^nb^n\mid n\ge1\}$", T4["only ab"])],
      why=r"$A$ גוזר $a^nb^n$ עם $n\ge1$ (כלל הבסיס הוא $ab$ ולא $\varepsilon$), ו-$B$ גוזר $b^na^n$ עם $n\ge1$. האיחוד לא כולל את $\varepsilon$. לא כל המילים עם $\#_a=\#_b$ (למשל $abab$ אינה נגזרת). בדקנו עד אורך $9$.",
      recap="איחוד, ובדיקת ε: כלל הבסיס ab ולא ε"),
    Q("נתון הדקדוק:\n" + gram("S->aTa|bTb;T->aT|bT|ε") + "\nמהי $L(G)$?",
      [C("מילים באורך לפחות $2$ שמתחילות ונגמרות באותה אות", T5["same"]), C("כל הפלינדרומים", T5["pal"]),
       C("מילים באורך לפחות $2$ שהאות הראשונה שונה מהאחרונה", T5["diff"]), C("כל המילים באורך זוגי", T5["even"])],
      why=r"$T$ גוזר $\Sigma^*$. $S$ עוטף אותו באות זהה משני הצדדים: $a\ldots a$ או $b\ldots b$. לכן המילים מתחילות ונגמרות באותה אות ואורכן לפחות $2$. &quot;פלינדרומים&quot; שגויה: $abaa\in L$ אך אינה פלינדרום. &quot;אורך זוגי&quot; שגויה: $aba\in L$ באורך $3$. &quot;אות ראשונה שונה מהאחרונה&quot; שגויה: $ab\notin L$. בדקנו עד אורך $9$.",
      recap="T גוזר Σ*: S רק עוטף באות זהה"),
  ])
