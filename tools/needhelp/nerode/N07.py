# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *

# suffix pool: every word to length 5 plus every a^i b^j with i, j <= 14
ZS = words("ab", 5) + ["a" * i + "b" * j for i in range(15) for j in range(15)]


def sep_infinite(pred, gen, n=8):
    """first n elements of the generator separate pairwise (for the infinite family 'gen')"""
    T = [gen(k) for k in range(n)]
    return all(any(pred(x + z) != pred(y + z) for z in ZS) for i, x in enumerate(T) for y in T[i + 1:])


EQ = lambda w: w.count("a") == w.count("b")
GT = lambda w: bool(re.fullmatch(r"a*b*", w)) and w.count("a") > w.count("b")      # a^n b^m, n > m
MODL = lambda w: w.count("a") % 3 == w.count("b") % 3

# Q1  #a = #b
fam1 = {"a^k": (lambda k: "a" * k, True), "a^k b^k": (lambda k: "a" * k + "b" * k, True),
        "(ab)^k": (lambda k: "ab" * k, True)}
S1 = {n: sep_infinite(EQ, g) for n, (g, inf) in fam1.items()}
assert S1 == {"a^k": True, "a^k b^k": False, "(ab)^k": False}
FIN = is_separating_set(EQ, ["a", "aa", "aba"], "ab", 8)     # finite -> proves nothing
# Q2  #a = #b (mod 3)
RMOD = rank_stable(MODL, "ab", 7, (4, 5, 6))
S2_a = sep_infinite(MODL, lambda k: "a" * k)
S2_ab = sep_infinite(MODL, lambda k: "a" * k + "b" * k)
assert RMOD == 3 and not S2_a and not S2_ab
# Q3
ALL = lambda w: True
EVENL = lambda w: len(w) % 2 == 0
big_class = rank_stable(ALL, "ab", 6, (4, 5, 6)) == 1            # Sigma* has one (infinite) class and is regular
# for L = even length, a^i and a^i b are separated by eps whenever i is even/odd... and the language is regular:
fact3 = all(EVENL("a" * i) != EVENL("a" * i + "b") for i in range(9)) and rank_stable(EVENL, "ab", 7, (4, 5, 6)) == 2
# Q4
R_UNION1 = rank_stable(ALL, "ab", 6, (4, 5, 6))
# Q5
S5 = {"a^{2k}": sep_infinite(GT, lambda k: "a" * (2 * k)), "a^k b^k": sep_infinite(GT, lambda k: "a" * k + "b" * k),
      "b^k": sep_infinite(GT, lambda k: "b" * k), "a^k b^(k+1)": sep_infinite(GT, lambda k: "a" * k + "b" * (k + 1))}
assert S5 == {"a^{2k}": True, "a^k b^k": False, "b^k": False, "a^k b^(k+1)": False}

LEVEL = level("N07", 7, "♾️", "Rank אינסופי וקבוצה מפרידה אינסופית",
  "להוכיח אי-רגולריות בעזרת קבוצה מפרידה אינסופית, ולפסול אפשרויות שהן אינסופיות אבל לא מפרידות.",
  r'''
<p>$\mathrm{Rank}(L)=\infty$ היא פשוט דרך אחרת לכתוב &quot;$L$ <b>לא רגולרית</b>&quot; (משפט נרוד). וכדי להוכיח אותה מספיק למצוא קבוצה מפרידה <b>אינסופית</b>: אם יש אינסוף מילים שכל שתיים מהן ניתנות להפרדה, יש אינסוף מחלקות.</p>
<div class="lesson-rule">🔑 <b>שני תנאים, שניהם:</b> $T$ אינסופית <b>וגם</b> כל זוג מילים ב-$T$ ניתן להפרדה. קבוצה סופית לא מוכיחה אי-רגולריות, וקבוצה אינסופית שכל איבריה באותה מחלקה לא מוכיחה כלום.</div>
<div class="lesson-ex"><b>דוגמה (19B-A-Q12).</b> $L=\{w\mid\#_a=\#_b\}$. הקבוצה $\{a^k\}$ אינסופית ומפרידה: $b^i$ מפרידה בין $a^i$ ל-$a^j$ כש-$j\ne i$ ($a^ib^i\in L$ אבל $a^jb^i\notin L$). לעומת זאת $\{a^kb^k\}$ אינסופית אך <b>כולן ב-$L$</b> והן שקולות (הפרש $0$), ולכן היא לא מפרידה.</div>
<h3>תבנית שעובדת כמעט תמיד</h3>
<p>$T=\{a^k\}$ (או תת-קבוצה אינסופית שלה) עם הסיפא ה&quot;משלימה&quot; $b^k$. מסיח קבוע: קבוצה אינסופית שכל איבריה באותה מחלקה. ב-SAMP-19-Q21 ($\{a^nb^m\mid n>m\}$) הקבוצה $\{a^{2k}\}$ מפרידה (הסיפא $b^{2d-1}$), וה&quot;הוכחה&quot; $a^kb^k$ שגויה: $a^kb^k$ אפילו לא בשפה, והן כולן שקולות.</p>
<h3>גם הפוך: רגולרית כי Rank סופי</h3>
<p>שפות עם ספירה <b>מודולו</b> הן רגולריות: אותה מחלקה לכל המילים עם אותן שאריות. ב-SAMP-19-Q10 &quot;$\#_a$ אי-זוגי ו-$\#_b$ זוגי&quot; רגולרית, ו&quot;יש אס״ד עם $3$ מצבים&quot; שגוי: צריך $4$ (זוגיות כפול זוגיות). ב-19B-B-Q19 ($(n+m)\bmod3=k\bmod3$) הכול &quot;אינסופי&quot; באפשרויות ושום קבוצה לא מפרידה.</p>
<h3>טענות לוגיות</h3>
<table dir="ltr"><thead><tr><th>הטענה</th><th></th></tr></thead><tbody>
<tr><td>כל מחלקה סופית &rarr; $L$ לא רגולרית</td><td>נכון (אינסוף מחלקות)</td></tr>
<tr><td>קיימת מחלקה אינסופית &rarr; $L$ לא רגולרית</td><td>לא: $\Sigma^*$</td></tr>
<tr><td>$\mathrm{Rank}(L)\ge10000$ &rarr; לא רגולרית</td><td>לא: $\mathrm{Rank}$ סופי יכול להיות גדול</td></tr>
<tr><td>$\mathrm{Rank}(L_1\cup L_2)=\infty$ &rarr; אחת מהן אינסופית</td><td>נכון</td></tr>
<tr><td>$\mathrm{Rank}(L_1\cup L_2)\ge\max$</td><td>לא: $\{0^n1^n\}\cup\Sigma^*=\Sigma^*$</td></tr></tbody></table>
<div class="lesson-trap">⚠️ <b>&quot;לכל $i$ יש סיפא מפרידה בין $a^i$ ל-$a^ib$&quot;</b> אינה קבוצה מפרידה: כל זוג יכול להיות מופרד בסיפא אחרת, אבל המילים $a^i$ ו-$a^j$ בכלל לא נבדקו אחת מול השנייה (19B-B-Q11). באורך זוגי, $z=\varepsilon$ מפרידה בין $a^i$ ל-$a^ib$ לכל $i$, והשפה רגולרית.</div>
''',
  [
    Q(r"$L=\{w\in\{a,b\}^*\mid\#_a(w)=\#_b(w)\}$. איזו קבוצה היא אינסופית **ומפרידה** (ולכן מוכיחה ש-$L$ לא רגולרית)?",
      [C(r"$\{a^k\mid k\ge0\}$", S1["a^k"]), C(r"$\{a^kb^k\mid k\ge0\}$", S1["a^k b^k"]),
       C(r"$\{(ab)^k\mid k\ge0\}$", S1["(ab)^k"]), C(r"$\{a,aa,aba\}$", FIN and False)],
      why=r"ב-$\{a^k\}$ כל זוג $a^i,a^j$ ($i\ne j$) מופרד ע״י $b^i$. $\{a^kb^k\}$ ו-$\{(ab)^k\}$ אינסופיות אבל כל איבריהן ב-$L$ באותה מחלקה (הפרש $0$): לא מפרידות. $\{a,aa,aba\}$ סופית, ולכן אפילו אם היא מפרידה אינה מוכיחה אי-רגולריות. (בדקנו את ההפרדה של שמונה האיברים הראשונים בכל משפחה.)",
      recap="אינסופית וגם מפרידה, שני תנאים"),
    Q(r"$L=\{w\in\{a,b\}^*\mid\#_a(w)\equiv\#_b(w)\pmod3\}$. איזה נימוק נכון?",
      [C(r"$L$ רגולרית כי $\mathrm{Rank}(L)=3$ סופי", RMOD == 3),
       C(r"$L$ לא רגולרית כי $\{a^k\}$ אינסופית ומפרידה", S2_a),
       C(r"$L$ לא רגולרית כי $\{a^kb^k\}$ אינסופית ומפרידה", S2_ab),
       C(r"$L$ רגולרית כי יש לה אס״ד עם $2$ מצבים", RMOD == 2)],
      why=r"המצב הוא ההפרש $\#_a-\#_b$ מודולו $3$: שלוש מחלקות, ולכן $L$ רגולרית עם $\mathrm{Rank}=3$ (חישבנו). $\{a^k\}$ לא מפרידה: $a^3\equiv\varepsilon$ (אותה שארית). $\{a^kb^k\}$: כולן בשארית $0$, שקולות. אס״ד עם $2$ מצבים לא מספיק ($\mathrm{Rank}=3$).",
      recap="מודולו = זיכרון סופי = רגולרית"),
    Q(r"איזו טענה נכונה?",
      [J(r"אם כל מחלקות השקילות של $L$ סופיות אז $L$ לא רגולרית", True),
       C(r"אם קיימת מחלקת שקילות אינסופית אז $L$ לא רגולרית", not big_class),
       C(r"אם לכל $i$ יש סיפא מפרידה בין $a^i$ ל-$a^ib$ אז $L$ לא רגולרית", not fact3),
       J(r"אם $\mathrm{Rank}(L)\ge10000$ אז $L$ לא רגולרית", False)],
      why=r"$\Sigma^*$ אינסופית, ולכן אם כל מחלקה סופית יש אינסוף מחלקות, כלומר לא רגולרית. הפרכות: ב-$\Sigma^*$ המחלקה היחידה אינסופית ו-$L$ רגולרית; ב&quot;אורך זוגי&quot; הסיפא $\varepsilon$ מפרידה בין $a^i$ ל-$a^ib$ לכל $i$ והשפה רגולרית (Rank $2$); $\mathrm{Rank}$ סופי יכול להיות גדול ככל שרוצים (אורך מתחלק ב-$10000$).",
      recap="אינסוף מחלקות = לא רגולרית; מחלקה אינסופית אחת לא מוכיחה"),
    Q(r"$L_1=\{a^nb^n\mid n\ge0\}$ ($\mathrm{Rank}=\infty$) ו-$L_2=\Sigma^*$ מעל $\{a,b\}$. מהו $\mathrm{Rank}(L_1\cup L_2)$?",
      [C("$1$", R_UNION1 == 1), C(r"$\infty$", R_UNION1 is None), C("$2$", R_UNION1 == 2), C("$3$", R_UNION1 == 3)],
      why=r"$L_1\subseteq\Sigma^*$, ולכן $L_1\cup L_2=\Sigma^*$, עם $\mathrm{Rank}=1$. זה מפיל כל טענה &quot;$\mathrm{Rank}$ של האיחוד גדול או שווה לשל כל אחת&quot;. אבל אם $\mathrm{Rank}(L_1\cup L_2)=\infty$ אז לפחות אחת משתי השפות אינסופית.",
      recap="Σ* בולעת: Rank של האיחוד יכול לרדת ל-1"),
    Q(r"$L=\{a^nb^m\mid n>m\ge0\}$. איזו קבוצה אינסופית ומפרידה?",
      [C(r"$\{a^{2k}\mid k\ge0\}$", S5["a^{2k}"]), C(r"$\{a^kb^k\mid k\ge0\}$", S5["a^k b^k"]),
       C(r"$\{b^k\mid k\ge1\}$", S5["b^k"]), C(r"$\{a^kb^{k+1}\mid k\ge0\}$", S5["a^k b^(k+1)"])],
      why=r"ב-$\{a^{2k}\}$ הסיפא $b^{2d-1}$ מפרידה בין $a^{2d}$ ל-$a^{2k}$ ($k<d$): $a^{2d}b^{2d-1}\in L$ אבל $a^{2k}b^{2d-1}\notin L$. שלוש האחרות מכילות רק מילים שאין להן שום המשך בשפה, או שכולן מאותו סוג, ולכן הן שקולות (למשל $a^kb^k\notin L$ ו-$a^kb^kz\notin L$ לכל $z$).",
      recap="התבנית: a^k עם הסיפא המשלימה b^k".replace("a^k עם הסיפא המשלימה b^k", "$a^k$ עם הסיפא $b^k$")),
  ])
