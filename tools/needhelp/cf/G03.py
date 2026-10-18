# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def gen(rules, alpha, pred, n=9):
    return CFG(rules).lang(n) == {w for w in words(alpha, n) if pred(w)}


def tex(rules):
    return "$" + rules.replace("->", r"\to ").replace("|", r"\mid ").replace("ε", r"\varepsilon ") + "$"


# Q1  #a = #b
EQ = lambda w: w.count("a") == w.count("b")
R1 = ["S->SS|aSb|bSa|ε", "S->aSb|bSa|ε", "S->aSbS|ε", "S->SS|aSa|bSb|ε"]
T1 = [gen(r, "ab", EQ) for r in R1]
assert T1 == [True, False, False, False]
# Q2  a^k b^2k
P2 = lambda w: parts(w, "ab") is not None and 2 * parts(w, "ab")[0] == parts(w, "ab")[1]
R2 = ["S->aSbb|ε", "S->aSb|bb", "S->aSb|b", "S->aaSb|ε"]
T2 = [gen(r, "ab", P2) for r in R2]
assert T2 == [True, False, False, False]
# Q3  strict containment
G3 = CFG("S->AB;A->aAb|ε;B->cBd|ε")
alpha3 = "abcd"
L3 = lambda w: (lambda t: t is not None and t[0] == t[1] and t[2] == t[3])(parts(w, "abcd"))
L1_ = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2] == t[3])(parts(w, "abcd"))
LG = G3.lang(8)
W3 = [w for w in words(alpha3, 8)]
sub = all(L1_(w) <= (w in LG) for w in W3) and all((w in LG) == L3(w) for w in W3)
strict = sub and any((w in LG) and not L1_(w) for w in W3)
eq3 = all((w in LG) == L1_(w) for w in W3)
rev = all((w in LG) <= L1_(w) for w in W3) and any(L1_(w) and w not in LG for w in W3)
assert strict and not eq3 and not rev
# Q4  S -> SSS does not break the language
G4 = CFG("S->ε|SSS|10S|01S|11S|00S")
G4b = CFG("S->ε|10S|01S|11S|00S")
EVEN = lambda w: len(w) % 2 == 0
t_even = G4.lang(8) == {w for w in words("01", 8) if EVEN(w)} and G4b.lang(8) == G4.lang(8)
t_all = G4.lang(8) == set(words("01", 8))
t_break = G4.lang(8) != G4b.lang(8)
t_eq = G4.lang(8) == {w for w in words("01", 8) if w.count("0") == w.count("1")}
assert t_even and not t_all and not t_break and not t_eq
# Q5  a^k b^k, k >= 1
P5 = lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] == parts(w, "ab")[1] and w != ""
R5 = ["S->aSb|ab", "S->aSb|ε", "S->aSb|b", "S->SS|ab"]
T5 = [gen(r, "ab", P5) for r in R5]
assert T5 == [True, False, False, False]

LEVEL = level("G03", 3, "🛠️", "איזה דקדוק יוצר את L, והכלה בין שפות",
  "לבחור את הדקדוק הנכון לשפה נתונה בעזרת מילה קצרה שנופלת, ולהכריע הכלה ממש בעזרת שני פרמטרים בלתי תלויים.",
  r'''
<p>עכשיו הכיוון ההפוך: נתונה שפה $L$ וארבעה דקדוקים, ואיזה מהם יוצר בדיוק את $L$? (26A-A-Q2, 21S-A-Q12, 23A-A-Q20, 23A-B-Q20.)</p>
<div class="lesson-rule">🔑 <b>השיטה:</b> לכל דקדוק מועמד חפשו מילה קצרה ב-$L$ שהוא <b>לא</b> גוזר, או מילה שהוא גוזר ו<b>אינה</b> ב-$L$. מספיק אחת כדי לפסול.</div>
<div class="lesson-ex"><b>דוגמה (26A-A-Q2): $L=(\Sigma\Sigma)^*$.</b> $S\to\varepsilon\mid S10\mid S01$ לא גוזר $11$. $S\to\varepsilon\mid1S0S\mid0S1S$ לא גוזר $11$ (תמיד מספר שווה של $0$ ו-$1$). רק $S\to\varepsilon\mid SSS\mid10S\mid01S\mid11S\mid00S$ נכון. ו-$S\to SSS$ לא &quot;מקלקל&quot;: הוא משרשר מילים שכבר בשפה, ובלעדיו הדקדוק כבר יוצר את $L$.</div>
<div class="lesson-trap">⚠️ <b>כלל הבסיס קובע אם $\varepsilon$ בשפה.</b> $S\to aSb\mid ab$ יוצר $a^nb^n$ עם $n\ge1$; $S\to aSb\mid\varepsilon$ כולל את $\varepsilon$. ב-23A-A-Q20 השפה $a^kb^{k+1}$ נוצרת ע״י $S\to b\mid aSb$, והמסיח $S\to b\mid aSbb$ נופל על $abbb$.</div>
<h3>הכלה ממש בין שפה לדקדוק (25A-A-Q10, 25A-B-Q10, 25A-C-Q10, 26A-A-Q10)</h3>
<ol>
<li>כתבו את $L(G)$ עם <b>פרמטרים בלתי תלויים</b>, אחד לכל משתנה.</li>
<li>השפה הנתונה היא כמעט תמיד המקרה שבו הפרמטרים <b>שווים</b>.</li>
<li>לכן $L_1\subsetneq L(G)$, ומילת העדות מתקבלת מפרמטר אחד $0$ ופרמטר אחר $1$.</li>
</ol>
<div class="lesson-ex"><b>דוגמה.</b> $S\to AB$, $A\to0A1\mid\varepsilon$, $B\to1B0\mid\varepsilon$ נותן $\{0^m1^{m+k}0^k\}$. השפה $\{0^n1^{2n}0^n\}$ היא המקרה $m=k$, והמילה $01$ ($m=1,k=0$) מוכיחה שההכלה ממש. אבל $\Sigma^*$ לא יכולה להיות מוכלת ממש באף שפה מעל $\Sigma$ (26A-A-Q10).</div>
''',
  [
    Q("איזה דקדוק (עם משתנה התחלתי $S$) יוצר את $L=\\{w\\in\\{a,b\\}^*\\mid\\#_a=\\#_b\\}$?",
      [C(tex(r), t) for r, t in zip(R1, T1)],
      why=r"$S\to SS\mid aSb\mid bSa\mid\varepsilon$ יוצר בדיוק את המילים המאוזנות: עוטפים ב-$a\ldots b$ או ב-$b\ldots a$, ומשרשרים. הדקדוקים האחרים נופלים על מילה קצרה: $S\to aSb\mid bSa\mid\varepsilon$ לא גוזר $abba\in L$; $S\to aSbS\mid\varepsilon$ לא גוזר $ba\in L$; $S\to SS\mid aSa\mid bSb\mid\varepsilon$ גוזר $aa\notin L$. בדקנו כל מילה עד אורך $9$.",
      recap="לכל מועמד: מילה קצרה שנופלת"),
    Q("איזה דקדוק יוצר את $L=\\{a^kb^{2k}\\mid k\\ge0\\}$?",
      [C(tex(r), t) for r, t in zip(R2, T2)],
      why=r"כל $a$ צריך שני $b$: $S\to aSbb\mid\varepsilon$. $S\to aSb\mid bb$ נותן $a^kb^{k+2}$; $S\to aSb\mid b$ נותן $a^kb^{k+1}$; $S\to aaSb\mid\varepsilon$ נותן $a^{2k}b^k$ (הפוך). בדקנו כל מילה עד אורך $9$.",
      recap="כל אות a דורשת שני b: aSbb"),
    Q("נתון הדקדוק:\n" + gram("S->AB;A->aAb|ε;B->cBd|ε") + "\nיהי $L_1=\\{a^nb^nc^nd^n\\mid n\\ge0\\}$. איזו טענה נכונה?",
      [C(r"$L_1\subsetneq L(G)$", strict), C(r"$L(G)\subsetneq L_1$", rev), C(r"$L_1=L(G)$", eq3), J("אף אחת מהטענות", False)],
      why=r"$A$ גוזר $a^nb^n$ ו-$B$ גוזר $c^md^m$ בפרמטרים בלתי תלויים: $L(G)=\{a^nb^nc^md^m\}$. $L_1$ היא המקרה $m=n$. לכן $L_1\subseteq L(G)$, וההכלה ממש כי $ab\in L(G)$ ($n=1,m=0$) אבל $ab\notin L_1$. בדקנו על כל המילים עד אורך $8$.",
      recap="פרמטרים בלתי תלויים; L1 הוא המקרה m = n"),
    Q("נתון הדקדוק:\n" + gram("S->ε|SSS|10S|01S|11S|00S") + "\nאיזו טענה נכונה?",
      [C(r"$L(G)=(\Sigma\Sigma)^*$, והכלל $S\to SSS$ מיותר אך לא מקלקל", t_even), C(r"$L(G)=\Sigma^*$", t_all),
       C(r"הכלל $S\to SSS$ מוסיף מילים שלא היו נגזרות בלעדיו", t_break), C(r"$L(G)=\{w\mid\#_0=\#_1\}$", t_eq)],
      why=r"כל כלל מלבד $SSS$ מוסיף שתי אותיות, ו-$SSS$ משרשר מילים באורך זוגי, ולכן $L(G)=(\Sigma\Sigma)^*$: כל המילים באורך זוגי (בדקנו עד אורך $8$, וגם שבלי $SSS$ מתקבלת אותה שפה). $0$ לא נגזרת ולכן לא $\Sigma^*$, ו-$11$ נגזרת ולכן לא $\#_0=\#_1$.",
      recap="S → SSS לא מקלקל: מאחד מילים שכבר בשפה".replace("S → SSS", "$S\\to SSS$")),
    Q("איזה דקדוק יוצר את $L=\\{a^kb^k\\mid k\\ge1\\}$?",
      [C(tex(r), t) for r, t in zip(R5, T5)],
      why=r"$S\to aSb\mid ab$ מתחיל ב-$ab$ ולכן אין $\varepsilon$. $S\to aSb\mid\varepsilon$ גוזר $\varepsilon\notin L$. $S\to aSb\mid b$ גוזר $b$. $S\to SS\mid ab$ גוזר $abab\notin L$. בדקנו עד אורך $9$.",
      recap="כלל הבסיס קובע אם ε בשפה"),
  ])
