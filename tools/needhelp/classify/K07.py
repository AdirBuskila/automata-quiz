# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def wins(pred, f, ps=(2, 3, 4)):
    """the word family f(p) forces a contradiction in the CFL pumping game for every constant p in ps"""
    return all(pump_breaks_cf(pred, f(p), p) for p in ps)


# Q1  a^k b^{2k} a^k
def L1(w):
    m = re.fullmatch("(a*)(b*)(a*)", w)
    if not m:
        return False
    x, y, z = (len(g) for g in m.groups())
    return x == z and y == 2 * x


Q1 = {"a^n b^{2n} a^n": wins(L1, lambda p: "a" * p + "b" * (2 * p) + "a" * p),
      "a^2 b^4 a^2": wins(L1, lambda p: "aa" + "bbbb" + "aa", (2, 3, 4, 9)),
      "b^{2n}": wins(L1, lambda p: "b" * (2 * p)),
      "a^n b^{2n}": wins(L1, lambda p: "a" * p + "b" * (2 * p))}
assert Q1 == {"a^n b^{2n} a^n": True, "a^2 b^4 a^2": False, "b^{2n}": False, "a^n b^{2n}": False}, Q1
# Q2  squares
SQ = lambda w: int(len(w) ** 0.5) ** 2 == len(w)
Q2 = {"a^{n^2}": wins(SQ, lambda p: "a" * p * p), "a^100": wins(SQ, lambda p: "a" * 100, (2, 3, 4, 101)),
      "a^{n^2+1}": wins(SQ, lambda p: "a" * (p * p + 1)), "a^{2n}": wins(SQ, lambda p: "a" * (2 * p))}
assert Q2 == {"a^{n^2}": True, "a^100": False, "a^{n^2+1}": False, "a^{2n}": False}, Q2
# Q3  uu
UU = lambda w: len(w) % 2 == 0 and w[: len(w) // 2] == w[len(w) // 2:]
Q3 = {"a^n b^n a^n b^n": wins(UU, lambda p: "a" * p + "b" * p + "a" * p + "b" * p), "a^{2n}": wins(UU, lambda p: "a" * (2 * p)),
      "(ab)^{2n}": wins(UU, lambda p: "ab" * (2 * p)), "a^n b^n": wins(UU, lambda p: "a" * p + "b" * p)}
assert Q3 == {"a^n b^n a^n b^n": True, "a^{2n}": False, "(ab)^{2n}": False, "a^n b^n": False}, Q3
# Q4  a^i b^j c^k with i < j < k
def L4(w):
    t = parts(w, "abc")
    return t is not None and t[0] < t[1] < t[2]


Q4 = {"a^n b^{n+1} c^{n+2}": wins(L4, lambda p: "a" * p + "b" * (p + 1) + "c" * (p + 2)),
      "a b^2 c^3": wins(L4, lambda p: "a" + "bb" + "ccc", (2, 3, 4, 9)),
      "a^n b^n c^n": wins(L4, lambda p: "a" * p + "b" * p + "c" * p, (2,)),
      "a^n b^{n+1} c^{n+1}": wins(L4, lambda p: "a" * p + "b" * (p + 1) + "c" * (p + 1), (2,))}
assert Q4 == {"a^n b^{n+1} c^{n+2}": True, "a b^2 c^3": False, "a^n b^n c^n": False, "a^n b^{n+1} c^{n+1}": False}, Q4


# Q5  the window |vxy| <= p of a^p b^p c^p touches at most two different letters
def touches_le2(p):
    w = "a" * p + "b" * p + "c" * p
    return all(len(set(w[i:i + p])) <= 2 for i in range(len(w) - p + 1))


T2 = all(touches_le2(p) for p in range(2, 9))
assert T2

LEVEL = level("K07", 7, "🎯", "משחק למת הניפוח לשפות חסרות הקשר",
  "לבחור מילה שמפריכה חסרות הקשר בלמת הניפוח לח״ה, ולהסביר למה חלון של p אותיות נוגע בשני גושים לכל היותר.",
  r'''
<p>כשהחיתוך עם שפה רגולרית לא עוזר, מפריכים ח״ה בלמת הניפוח לח״ה. הנוסח בדף הנוסחאות:</p>
<div class="lesson-rule">🔑 לכל שפה ח״ה $L$ קיים קבוע $\ell$ כך שלכל $w\in L$ באורך לפחות $\ell$ יש פירוק $w=xyzuv$ עם: $yu\ne\varepsilon$, $|yzu|\le\ell$, ולכל $n\ge0$: $xy^nzu^nv\in L$. (בפתרונות כותבים גם $uvwxy$ עם $|vwx|\le\ell$. אותה למה: החלקים <b>המנופחים</b> הם השני והרביעי, והחלק <b>החסום</b> הוא שלושת האמצעיים.)</div>
<h3>תבנית ההוכחה</h3>
<ol>
<li>נניח בשלילה ש-$L$ ח״ה, ויהי $\ell$ קבוע הניפוח.</li>
<li><b>בחרו מילה שתלויה ב-$\ell$</b>, למשל $a^\ell b^\ell c^\ell$ (לא דוגמה מספרית!).</li>
<li>יהי פירוק <b>כלשהו</b> עם $yu\ne\varepsilon$ ו-$|yzu|\le\ell$.</li>
<li><b>הטיעון המרכזי:</b> החלון $yzu$ באורך $\le\ell$ נוגע <b>לכל היותר בשני גושים סמוכים</b>, ולכן הניפוח משנה רק אותם ומשאיר גוש אחד קבוע.</li>
<li>מחלקים למקרים ובוחרים $n$ (בדרך כלל $0$ או $2$) כך ש-$xy^nzu^nv\notin L$. סתירה.</li>
</ol>
<div class="lesson-ex"><b>דוגמה (24A-A-Q17): $\{a^nb^{2n}a^n\}$.</b> $w=a^\ell b^{2\ell}a^\ell$. החלון מוכל ב-$a^\ell b^{2\ell}$ או ב-$b^{2\ell}a^\ell$, ולכן הוא לא נוגע באחד מגושי ה-$a$. אחרי ניפוח עם $n=2$ הגוש שלא נגעו בו נשאר $\ell$ והאחרים גדלים: היחס $1:2:1$ נשבר.</div>
<div class="lesson-ex"><b>אות אחת (25A-A-Q17): $\{a^{k^2}\}$.</b> אין גושים, ולכן הטיעון הוא על <b>האורך</b>: עם $n=2$ האורך הוא $\ell^2+d$ כש-$1\le d\le\ell$, ו-$\ell^2<\ell^2+d\le\ell^2+\ell<(\ell+1)^2$: בין שני ריבועים עוקבים.</div>
<div class="lesson-trap">⚠️ <b>בחרו את המילה מהחלק ה&quot;קשה&quot; של השפה.</b> ב-23A-A-Q5 המסיחים $0^{2k}1^k$ ו-$1^k0^{2k}$ הם מילים משפות ח״ה, ולכן תמיד ניתנות לניפוח. המילה הנכונה היא $0^k1^k0^k$. מילה באורך קבוע ($a^{100}$) נכשלת כש-$\ell$ גדול ממנה.</div>
<p>עוד כללים: כל תת-שפה <b>אינסופית</b> של $a^nb^nc^n$ גם לא ח״ה (19B-A-Q16); $\{a^nb^na^nb^n\}$ נוכיח עם $n=0$ (SAMP-19-Q12); $\{ab^nab^nab^n\}$ (21S-B-Q18) ו-$\{a^mb^mc^k\mid k\ge m\}$ (24A-B-Q17) בניפוח.</p>
''',
  [
    Q(r"$L=\{a^kb^{2k}a^k\mid k\ge0\}$ ו-$\ell$ הוא קבוע הניפוח לח״ה. איזו מילה מביאה בהכרח לסתירה?",
      [C(r"$a^\ell b^{2\ell}a^\ell$", Q1["a^n b^{2n} a^n"]), C(r"$aabbbbaa$", Q1["a^2 b^4 a^2"]),
       C(r"$b^{2\ell}$", Q1["b^{2n}"]), C(r"$a^\ell b^{2\ell}$", Q1["a^n b^{2n}"])],
      why=r"ב-$a^\ell b^{2\ell}a^\ell$ החלון נוגע לכל היותר בשני גושים, ולכן הניפוח שובר את היחס $1:2:1$. $aabbbbaa$ באורך קבוע, וכש-$\ell\ge9$ היא קצרה מדי. $b^{2\ell}$ ו-$a^\ell b^{2\ell}$ אינן ב-$L$ בכלל. בדקנו את המשחק במלואו עבור $\ell=2,3,4$.",
      recap="מילה שתלויה ב-ℓ, בשפה, עם חלון שלא נוגע בכל הגושים".replace("ℓ", "$\\ell$")),
    Q(r"$L=\{a^{k^2}\mid k\ge0\}$ ו-$\ell$ הוא קבוע הניפוח לח״ה. איזו מילה מביאה בהכרח לסתירה?",
      [C(r"$a^{\ell^2}$", Q2["a^{n^2}"]), C(r"$a^{100}$", Q2["a^100"]), C(r"$a^{\ell^2+1}$", Q2["a^{n^2+1}"]), C(r"$a^{2\ell}$", Q2["a^{2n}"])],
      why=r"עם $a^{\ell^2}$ והניפוח $n=2$ האורך הוא $\ell^2+d$ עם $1\le d\le\ell$, ממש בין $\ell^2$ ל-$(\ell+1)^2$: לא ריבוע. $a^{100}$ באורך קבוע ואינה מועילה כש-$\ell>100$. $a^{\ell^2+1}$ ו-$a^{2\ell}$ אינן ב-$L$ (פרט לערכים מקריים). בדקנו עבור $\ell=2,3,4$ וגם $\ell=101$.",
      recap="אונרי: האורך חייב להיות ריבוע, והניפוח נופל בין שני ריבועים"),
    Q(r"$L=\{uu\mid u\in\{a,b\}^*\}$ ו-$\ell$ הוא קבוע הניפוח לח״ה. איזו מילה מביאה בהכרח לסתירה?",
      [C(r"$a^\ell b^\ell a^\ell b^\ell$", Q3["a^n b^n a^n b^n"]), C(r"$a^{2\ell}$", Q3["a^{2n}"]),
       C(r"$(ab)^{2\ell}$", Q3["(ab)^{2n}"]), C(r"$a^\ell b^\ell$", Q3["a^n b^n"])],
      why=r"ב-$a^\ell b^\ell a^\ell b^\ell$ החלון נוגע בשני גושים סמוכים לכל היותר, ולכן הניפוח משבש את ההתאמה בין שתי החצאים. ב-$a^{2\ell}$ אפשר לנפח $v=a,y=a$ ולהישאר בצורה $uu$. ב-$(ab)^{2\ell}$ אפשר לנפח $v=ab,y=ab$. $a^\ell b^\ell$ בכלל לא ב-$L$. בדקנו עבור $\ell=2,3,4$.",
      recap="uu: מילה שבה ארבעה גושים שונים".replace("uu", "$uu$")),
    Q(r"$L=\{a^ib^jc^k\mid i<j<k\}$ ו-$\ell$ הוא קבוע הניפוח לח״ה. איזו מילה מביאה בהכרח לסתירה?",
      [C(r"$a^\ell b^{\ell+1}c^{\ell+2}$", Q4["a^n b^{n+1} c^{n+2}"]), C(r"$abbccc$", Q4["a b^2 c^3"]),
       C(r"$a^\ell b^\ell c^\ell$", Q4["a^n b^n c^n"]), C(r"$a^\ell b^{\ell+1}c^{\ell+1}$", Q4["a^n b^{n+1} c^{n+1}"])],
      why=r"במילה $a^\ell b^{\ell+1}c^{\ell+2}$ ההפרשים הם בדיוק $1$ (צמודה), והחלון נוגע בשני גושים לכל היותר. ניפוח מעלה או מוריד אחד מהם ושובר את $i<j<k$ (לכל פירוק יש $n$ שמפיל). $abbccc$ באורך קבוע. שתי האחרות אינן ב-$L$ ($i<j<k$ נכשל). בדקנו עבור $\ell=2,3,4$.",
      recap="אי-שוויונות: מילה צמודה, והחלון נוגע בשני גושים"),
    Q(r"במילה $a^\ell b^\ell c^\ell$ ובלמת הניפוח לח״ה, איזו טענה נכונה?",
      [C(r"כל חלון באורך $\le\ell$ נוגע לכל היותר בשתי אותיות שונות, ולכן הניפוח משאיר גוש אחד קבוע", T2),
       J(r"הלמה מוכיחה שהשפה ח״ה כשאין פירוק שנשבר", False),
       J(r"שפה שמקיימת את הלמה היא בהכרח ח״ה", False), J(r"אפשר לבחור את הפירוק כרצוננו", False)],
      why=r"בחלון רצוף של $\ell$ אותיות מתוך $a^\ell b^\ell c^\ell$ (בדקנו ל-$\ell=2..8$) יש לכל היותר שני סוגי אותיות, כי כל גוש באורך $\ell$ בדיוק. לכן הניפוח לא משנה גוש אחד, ושובר את השוויון. הלמה היא תנאי הכרחי בלבד (היא רק מפריכה), והפירוק נבחר על ידי היריב.",
      recap="חלון של ℓ אותיות נוגע בשני גושים לכל היותר".replace("ℓ", "$\\ell$")),
  ])
