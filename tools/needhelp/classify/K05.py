# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# Q1  a^n b^m c^m d^n : nested
P1 = lambda w: (lambda t: t is not None and t[0] == t[3] and t[1] == t[2])(parts(w, "abcd"))
K1 = classify(P1, "abcd", ("cfl", "S->aSd|T;T->bTc|ε"), n=7)
# Q2  a^n b^m c^n d^m : crossing
P2 = lambda w: (lambda t: t is not None and t[0] == t[2] and t[1] == t[3])(parts(w, "abcd"))
K2 = classify(P2, "abcd", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p + "d" * p), n=7)
assert (K1, K2) == ("cfl", "noncfl")

# Q3  which is not context-free
A_NB = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab"))
UUR = lambda w: len(w) % 2 == 0 and w == w[::-1]
UU = lambda w: len(w) % 2 == 0 and w[: len(w) // 2] == w[len(w) // 2:]
K3 = {"a^n b^n": classify(A_NB, "ab", ("cfl", "S->aSb|ε")),
      "uu^R": classify(UUR, "ab", ("cfl", "S->aSa|bSb|ε")),
      "uu": classify(UU, "ab", ("noncfl", lambda p: "a" * p + "b" * p + "a" * p + "b" * p), n=7),
      "a^n b^m c^m d^n": K1}
assert K3 == {"a^n b^n": "cfl", "uu^R": "cfl", "uu": "noncfl", "a^n b^m c^m d^n": "cfl"}

# Q4  intersection with a regular language to expose the crossing structure
L4 = lambda w: w.count("a") == w.count("c") and w.count("b") == w.count("d")
def inter(R):
    r = rx(R, "abcd")
    return lambda w: L4(w) and r.accepts(w)
I1 = classify(inter("a*b*c*d*"), "abcd", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p + "d" * p), n=7)
I2 = classify(inter("a*c*b*d*"), "abcd", ("cfl", "S->TU;T->aTc|ε;U->bUd|ε"), n=7)
I3 = classify(inter("(a+c)*(b+d)*"), "abcd", ("cfl", "S->TU;T->TT|aTc|cTa|ε;U->UU|bUd|dUb|ε"), n=7)
I4 = classify(inter("a*b*"), "abcd", ("finite", 0), n=7)
assert (I1, I2, I3, I4) == ("noncfl", "cfl", "cfl", "finite")

# Q5  a^n b^m c^k with k = n + m
P5 = lambda w: (lambda t: t is not None and t[2] == t[0] + t[1])(parts(w, "abc"))
K5 = classify(P5, "abc", ("cfl", "S->aSc|T;T->bTc|ε"), n=7)
assert K5 == "cfl"

LEVEL = level("K05", 5, "🪆", "חסרת הקשר מול לא חסרת הקשר: מקונן וחוצה",
  "להבחין בין השוואות מקוננות (ח״ה) להשוואות חוצות או משולשות (לא ח״ה), ולהוכיח לא ח״ה בעזרת חיתוך עם שפה רגולרית.",
  r'''
<p>מה מכונת המחסנית יכולה לבדוק? היא עובדת בשיטת <b>LIFO</b>: מה שנדחף אחרון נשלף ראשון. לכן היא יכולה להשוות ספירות שנסגרות <b>בסדר הפוך</b> לפתיחה, כמו סוגריים, ולא ספירות שנסגרות <b>באותו סדר</b> שנפתחו.</p>
<div class="lesson-rule">🔑 <b>מקונן מול חוצה (ישר מדף הנוסחאות):</b> $a^nb^mc^md^n$: המונים <b>מקוננים</b> (ה-$a$ החיצוני נסגר אחרון) &rarr; ח״ה. $a^nb^mc^nd^m$: המונים <b>חוצים</b> &rarr; לא ח״ה. כך גם $uu^R$ ח״ה ו-$uu$ לא, ו-$a^nb^nc^n$ (שלוש השוואות) לא.</div>
<table dir="ltr"><thead><tr><th>ח״ה, לא רגולרית</th><th>לא ח״ה</th></tr></thead><tbody>
<tr><td>$a^nb^n$</td><td>$a^nb^nc^n$</td></tr>
<tr><td>$a^nb^mc^md^n$</td><td>$a^nb^mc^nd^m$</td></tr>
<tr><td>$uu^R$ (מעל $\ge2$ אותיות)</td><td>$uu$ (מעל $\ge2$ אותיות)</td></tr>
<tr><td>$\overline{uu}$</td><td>$a^{n^2}$, $a^{n!}$ ומשלימותיהן</td></tr></tbody></table>
<p>את הרשימה הזאת מותר לצטט בלי הוכחה. כל השאר מפרקים אליה.</p>
<h3>איך מוכיחים לא ח״ה בלי לנפח</h3>
<p>ח״ה סגורות לחיתוך <b>עם שפה רגולרית</b>: אם $L$ ח״ה ו-$R$ רגולרית אז $L\cap R$ ח״ה. לכן אם $L\cap R$ <b>לא</b> ח״ה, גם $L$ לא ח״ה. בוחרים $R$ שמסדרת את האותיות בגושים.</p>
<div class="lesson-ex"><b>דוגמה (25A-B-Q17).</b> $L=\{w\mid\#_a=\#_c\wedge\#_b=\#_d\}$: האותיות מעורבבות וקשה לנפח. $L\cap a^*b^*c^*d^*=\{a^nb^mc^nd^m\}$ היא השפה החוצה מדף הנוסחאות. לכן $L$ לא ח״ה. אבל $L\cap a^*c^*b^*d^*=\{a^nc^nb^md^m\}$ היא שרשור של שתי ח״ה, שהיא ח״ה ולכן לא מוכיחה כלום. בחירת $R$ היא כל העניין.</div>
<div class="lesson-ex"><b>עוד שתי דוגמאות.</b> ב-25A-C-Q6, $\{a^kb^kc^id^k\}\cap a^*b^*d^*=\{a^kb^kd^k\}$, לא ח״ה. וב-21S-B-Q19 החיתוך $\{a^mb^mc^i\}\cap\{a^kb^nc^k\}=\{a^nb^nc^n\}$ מראה שח״ה אינן סגורות לחיתוך.</div>
<div class="lesson-trap">⚠️ $\{a^kb^mc^i\mid\ldots\}$ עם שני תנאים שחולקים משתנה עוזרים: $\{a^mb^mc^k\mid k\ge m\}$ ו-$\{a^nb^{2n}a^n\}$ מוכחות בלמת הניפוח (24A-B-Q17, 24A-A-Q17), ו-$\{a^nb^na^nb^n\}$ בניפוח עם $i=0$ (SAMP-19-Q12). אבל $a^ib^kc^{i+k}$ ו-$\{a^{n+2}b^{2n}\}$ ח״ה (מקוננות), כי $c^{i+k}$ נסגר על $b^k$ ואז על $a^i$.</div>
''',
  [
    Q(r"תהי $L=\{a^nb^mc^md^n\mid n,m\ge0\}$. איזו טענה נכונה?", cls_opts(K1),
      why=r"המונים מקוננים: $a^n\ldots d^n$ עוטפים את $b^m\ldots c^m$. דקדוק: $S\to aSd\mid T$, $T\to bTc\mid\varepsilon$. לכן ח״ה. לא רגולרית: $\{a^k\}$ אינסופית ומפרידה (הסיפא $d^k$). אומת הדקדוק על כל המילים עד אורך $8$.",
      recap="מקונן: ח״ה, לא רגולרית"),
    Q(r"תהי $L=\{a^nb^mc^nd^m\mid n,m\ge0\}$. איזו טענה נכונה?", cls_opts(K2),
      why=r"המונים חוצים: $a^n$ נסגר ב-$c^n$ ו-$b^m$ ב-$d^m$ באותו סדר שנפתחו, ומחסנית לא יכולה. למת הניפוח לח״ה עם $a^pb^pc^pd^p$: החלון $|vxy|\le p$ נוגע לכל היותר בשני גושים סמוכים, ולכן הניפוח אינו יכול לשנות את כל ארבעת הגושים, והוא שובר לפחות זוג אחד. בדקנו את המשחק עבור $p=2,3,4$. לכן לא ח״ה.",
      recap="חוצה: לא ח״ה"),
    Q(r"איזו מהשפות הבאות מעל $\{a,b\}$ **לא** חסרת הקשר?",
      [C(r"$\{a^nb^n\mid n\ge0\}$", K3["a^n b^n"] == "noncfl"), C(r"$\{uu^R\mid u\in\{a,b\}^*\}$", K3["uu^R"] == "noncfl"),
       C(r"$\{uu\mid u\in\{a,b\}^*\}$", K3["uu"] == "noncfl"), C(r"$\{a^nb^mc^md^n\}$", K3["a^n b^m c^m d^n"] == "noncfl")],
      why=r"$uu$ משווה את המילה לעצמה **באותו סדר**, כלומר חוצה, ולכן לא ח״ה (למת הניפוח עם $a^pb^pa^pb^p$, אומת עבור $p=2,3,4$). $uu^R$ מקונן ($S\to aSa\mid bSb\mid\varepsilon$), ו-$a^nb^n$ ו-$a^nb^mc^md^n$ גם הן ח״ה.",
      recap=r"$uu$ חוצה: לא ח״ה; $uu^R$ מקונן: ח״ה"),
    Q(r"$L$ היא שפת המילים מעל $\{a,b,c,d\}$ שבהן $\#_a=\#_c$ וגם $\#_b=\#_d$. איזו שפה רגולרית $R$ מראה ש-$L$ לא ח״ה (כי $L\cap R$ לא ח״ה)?",
      [C(r"$R=a^*b^*c^*d^*$", I1 == "noncfl"), C(r"$R=a^*c^*b^*d^*$", I2 == "noncfl"),
       C(r"$R=(a+c)^*(b+d)^*$", I3 == "noncfl"), C(r"$R=a^*b^*$", I4 == "noncfl")],
      why=r"עם $a^*b^*c^*d^*$ מתקבל $\{a^nb^mc^nd^m\}$, שפה חוצה מדף הנוסחאות: לא ח״ה. עם $a^*c^*b^*d^*$ מתקבל $\{a^nc^nb^md^m\}$ (שרשור של שתי ח״ה: ח״ה). עם $(a+c)^*(b+d)^*$ מתקבל שרשור של &quot;מספר שווה של $a$ ו-$c$&quot; ו&quot;מספר שווה של $b$ ו-$d$&quot;, גם ח״ה. עם $a^*b^*$ מתקבל $\{\varepsilon\}$. אימתנו את הדקדוקים של החיתוכים שאינם מוכיחים כלום.",
      recap="R שמסדרת את האותיות כך שההשוואות חוצות"),
    Q(r"תהי $L=\{a^nb^mc^k\mid k=n+m\}$. איזו טענה נכונה?", cls_opts(K5),
      why=r"$c^{n+m}$ נסגר קודם על $b^m$ ואז על $a^n$: מקונן. דקדוק: $S\to aSc\mid T$, $T\to bTc\mid\varepsilon$. ח״ה. לא רגולרית: $\{a^i\}$ מפרידה אינסופית עם הסיפא $c^i$. אומת הדקדוק על כל המילים עד אורך $8$.",
      recap="מונה אחד שנסגר בסדר הפוך: ח״ה"),
  ])
