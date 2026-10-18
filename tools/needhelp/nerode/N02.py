# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def fin_rank(S, alpha="01"):
    S = set(S)
    return rank_stable(lambda w: w in S, alpha, 9, (6, 7, 8))


R_EMPTY, R_EPS, R_ZERO = fin_rank([]), fin_rank([""]), fin_rank(["0"])
R_00, R_1_01, R_01_10 = fin_rank(["00"]), fin_rank(["1", "01"]), fin_rank(["01", "10"])
R_SIGMA = rank_stable(lambda w: True, "01", 9, (6, 7, 8))
assert (R_EMPTY, R_SIGMA, R_EPS, R_ZERO, R_00, R_1_01, R_01_10) == (1, 1, 2, 3, 4, 4, 5)
R_UN = rank_stable(lambda w: w in {"aa", "aaaaaa"}, "a", 12, (9, 10, 11))
assert R_UN == 8
R_LE3 = rank_stable(lambda w: len(w) <= 3, "01", 9, (6, 7, 8))
assert R_LE3 == 5 and fin_rank(["a" * k for k in range(5)], "a") == 6

LEVEL = level("N02", 2, "🧩", "Rank של שפות קטנות ומצב הבור",
  "לחשב Rank של שפה סופית, ולא לשכוח את מצב הבור.",
  r'''
<p>כדי לחשב $\mathrm{Rank}(L)$ שפה אחר שפה, כל מה שצריך הוא לשאול: <b>כמה מצבים שונים צריך אוטומט</b> שמזהה אותה, והאם כולם באמת ניתנים להפרדה. נתחיל בשפות הקטנות ביותר, כי הן מופיעות בבחינות שוב ושוב.</p>
<h3>הטבלה שכדאי לזכור (מעל $\{0,1\}$)</h3>
<table dir="ltr"><thead><tr><th>השפה</th><th>$\mathrm{Rank}$</th><th>שאלה</th></tr></thead><tbody>
<tr><td>$\emptyset$, $\Sigma^*$</td><td>$1$</td><td>25A-A-Q18</td></tr>
<tr><td>$\{\varepsilon\}$</td><td>$2$</td><td>25A-C-Q14</td></tr>
<tr><td>$\{0\}$</td><td>$3$</td><td>25A-C-Q14</td></tr>
<tr><td>$\{00\}$</td><td>$4$</td><td>24A-C-Q5</td></tr>
<tr><td>$\{1,01\}$</td><td>$4$</td><td>25A-A-Q8</td></tr>
<tr><td>$\{01,10\}$</td><td>$5$</td><td>25A-C-Q1</td></tr>
<tr><td>$\{w\mid|w|\le4\}$</td><td>$6$</td><td>21S-A-Q14</td></tr></tbody></table>
<h3>למה דווקא כך</h3>
<p>לכל שפה יש לפחות מחלקה אחת, ולכן $\mathrm{Rank}=0$ לא קיים. ל-$\emptyset$ ול-$\Sigma^*$ מחלקה אחת: כל המילים נתנות אותה תשובה לכל סיפא. ל-$\{\varepsilon\}$ שתי מחלקות: $\varepsilon$ עצמה ו&quot;כל השאר&quot; (הסיפא $\varepsilon$ מפרידה בין $\varepsilon$ לכל מילה אחרת).</p>
<div class="lesson-ex"><b>$\{0\}$:</b> שלוש מחלקות: $\varepsilon$ (&quot;עוד לא התחלתי, צריך $0$&quot;), $0$ (&quot;סיימתי&quot;), ו-&quot;מלכודת&quot; (כל מילה אחרת, למשל $1$ או $00$). $T=\{\varepsilon,0,1\}$ מפרידה: $z=0$ מפרידה בין $\varepsilon$ ל-$0$ ו-$1$, $z=\varepsilon$ בין $0$ ל-$1$.</div>
<div class="lesson-rule">🔑 <strong>בשפה סופית יש תמיד מלכודת:</strong> מילה ש&quot;אין לה שום המשך בשפה&quot;. לכן כמעט כל מסיח &quot;קטן באחד&quot; הוא האוטומט <b>בלי</b> מצב המלכודת (25A-C-Q1: האס״ד של $\{01,10\}$ הוא התחלה, אחרי $0$, אחרי $1$, מקבל, ומלכודת: $5$).</div>
<h3>שפה סופית מעל אות אחת</h3>
<p>אם $L\subseteq\{a\}^*$ סופית ו-$a^d$ היא המילה הארוכה ביותר שלה, אז $\mathrm{Rank}(L)=d+2$: שרשרת $a^0,a^1,\dots,a^d$ ($d+1$ מצבים) ועוד מלכודת (26A-A-Q18, וגם 19B-A-Q9 עבור $\{a,aa,aaa\}$ מעל $\{a,b\}$: $T=\{\varepsilon,a,aa,aaa,aaab\}$).</p>
<div class="lesson-trap">⚠️ בדיקת שפיות: $L=\{\varepsilon\}$ נותן $d=0$ ו-$\mathrm{Rank}=2$ (נכון); $L=\{a\}$ נותן $d=1$ ו-$\mathrm{Rank}=3$ (נכון). המסיחים $d$ ו-$d+1$ שוכחים את $\varepsilon$ או את המלכודת. ב-26A-A-Q1 נאמר $\mathrm{Rank}(L)=10$: אז <b>קיימת</b> קבוצה מפרידה בגודל $10$, ו<b>אין</b> בגודל $11$.</div>
''',
  [
    Q(r"מהו $\mathrm{Rank}(\{0\})$ מעל הא״ב $\{0,1\}$?",
      [C(str(k), R_ZERO == k) for k in (2, 3, 4, 1)],
      why=r"שלוש מחלקות: $\varepsilon$, $0$ (המילה בשפה) ומלכודת (למשל $1$, $00$). הקבוצה $\{\varepsilon,0,1\}$ מפרידה בגודל $3$. חישבנו את מספר המחלקות בפועל: $3$. $2$ שוכח את המלכודת.",
      recap="שפה סופית: לא לשכוח מלכודת"),
    Q(r"מהו $\mathrm{Rank}(\{01,10\})$ מעל $\{0,1\}$?",
      [C(str(k), R_01_10 == k) for k in (4, 5, 6, 3)],
      why=r"המחלקות: $\varepsilon$, אחרי $0$ (מחכה ל-$1$), אחרי $1$ (מחכה ל-$0$), מילה מלאה ($01$ או $10$, מחכה ל-$\varepsilon$), ומלכודת. $\varepsilon$ ו-$0$ נבדלות ב-$z=1$; $0$ ו-$1$ ב-$z=1$; המילה המלאה נבדלת מכולן ב-$z=\varepsilon$. סה״כ $5$.",
      recap="מה חסר להשלמה? כל תשובה שונה היא מצב"),
    Q(r"$L=\{aa,aaaaaa\}\subseteq\{a\}^*$. מהו $\mathrm{Rank}(L)$?",
      [C(str(k), R_UN == k) for k in (6, 7, 8, 9)],
      why=r"המילה הארוכה ביותר היא $a^6$, ולכן $d=6$ ו-$\mathrm{Rank}=d+2=8$: שרשרת $a^0,\dots,a^6$ (שבעה מצבים) ועוד מלכודת. כל $a^0,\dots,a^6$ שונות זו מזו: הסיפא $a^{6-i}$ מפרידה בין $a^i$ לכל $a^k$ עם $k>i$ (כי $a^6\in L$ ו-$a^{6-i+k}$ ארוכה מדי). חישבנו בפועל: $8$.",
      recap=r"שפה אונרית סופית: $d+2$ כש-$a^d$ הארוכה"),
    Q(r"איזה סדר נכון בין $\mathrm{Rank}(\emptyset)$, $\mathrm{Rank}(\{\varepsilon\})$ ו-$\mathrm{Rank}(\{0\})$ (מעל $\{0,1\}$)?",
      [C(r"$\mathrm{Rank}(\emptyset)<\mathrm{Rank}(\{\varepsilon\})<\mathrm{Rank}(\{0\})$", R_EMPTY < R_EPS < R_ZERO),
       C(r"$\mathrm{Rank}(\{\varepsilon\})<\mathrm{Rank}(\emptyset)$", R_EPS < R_EMPTY),
       C(r"$\mathrm{Rank}(\{0\})=\mathrm{Rank}(\{\varepsilon\})$", R_ZERO == R_EPS),
       C(r"$\mathrm{Rank}(\emptyset)=0$", R_EMPTY == 0)],
      why=r"$\mathrm{Rank}(\emptyset)=1$, $\mathrm{Rank}(\{\varepsilon\})=2$, $\mathrm{Rank}(\{0\})=3$. אין $\mathrm{Rank}=0$, כי לפחות המחלקה של $\varepsilon$ קיימת.",
      recap="1, 2, 3: ריקה, {ε}, {0}"),
    Q(r"$L=\{w\in\{0,1\}^*\mid|w|\le3\}$. מהו $\mathrm{Rank}(L)$?",
      [C(str(k), R_LE3 == k) for k in (4, 5, 6, 8)],
      why=r"האורך הוא מה שחשוב: אחרי $0,1,2,3$ אותיות המילה עדיין בשפה, ואחרי $4$ ומעלה היא במלכודת. מחלקות: אורך $0$, $1$, $2$, $3$ ומלכודת: $5$. (עבור $|w|\le4$ זה $6$, כמו בטבלה.)",
      recap="|w| ≤ d: d+2 מחלקות"),
  ])
