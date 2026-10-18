# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def finite_rank(pred, alpha="ab"):
    return rank_stable(pred, alpha, 8, (4, 5, 6)) is not None


# Q1  A(L) = {w : w in L and w^R in L}
SAMPLES = [rx(r, "ab") for r in ("a*b", "(ab)*", "(a+b)*a", "a(a+b)*b", "b*a*")]
A_of = lambda L: (lambda w: L.accepts(w) and L.accepts(w[::-1]))
I_ok = all(finite_rank(A_of(L)) for L in SAMPLES)
SIGMA = rx("(a+b)*", "ab")
II_ok = all(w == w[::-1] for w in words("ab", 6) if A_of(SIGMA)(w))      # every word of A(L) is a palindrome?  (L = Sigma*: no)
assert I_ok and not II_ok

# Q2  intersection of two CFLs
L1 = lambda w: (lambda t: t is not None and t[1] == t[2])(parts(w, "abc"))      # a^i b^k c^k
L2 = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "abc"))      # a^k b^k c^i
cfl1 = classify(L1, "abc", ("cfl", "S->AT;A->aA|ε;T->bTc|ε"), n=7)
cfl2 = classify(L2, "abc", ("cfl", "S->TC;T->aTb|ε;C->cC|ε"), n=7)
INT = lambda w: L1(w) and L2(w)
int_label = classify(INT, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7)
assert (cfl1, cfl2, int_label) == ("cfl", "cfl", "noncfl")

# Q3  at least two of three:  a^i b^k c^k , a^k b^i c^k , a^k b^k c^i
L3 = lambda w: (lambda t: t is not None and t[0] == t[2])(parts(w, "abc"))
M = lambda w: (L1(w) + L2(w) + L3(w)) >= 2
ANBNCN = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(parts(w, "abc"))
assert all(M(w) == ANBNCN(w) for w in words("abc", 8))
m_label = classify(M, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7)

# Q4  adding / removing a finite set of words
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab"))
FIN = {"c" if False else "aab", "b", "abab", "", "bbb"}
union_nonreg = rank_growing(lambda w: ANBN(w) or w in FIN, "ab")
diff_nonreg = rank_growing(lambda w: ANBN(w) and w not in FIN, "ab")
assert union_nonreg and diff_nonreg
union_reg = False
# Q5  non-regular L and its complement
comp = lambda w: not ANBN(w)
rank_union = rank_stable(lambda w: ANBN(w) or comp(w), "ab", 6, (3, 4, 5))
rank_inter = rank_stable(lambda w: ANBN(w) and comp(w), "ab", 6, (3, 4, 5))
comp_nonreg = rank_growing(comp, "ab")
assert (rank_union, rank_inter, comp_nonreg) == (1, 1, True)

LEVEL = level("K06", 6, "🔗", "סגירויות: מה נשמר ומה נשבר",
  "להשתמש בטבלת הסגירויות של רגולריות וח״ה, ובדוגמאות הנגדיות הקבועות, כדי להכריע טענות על שפות שנבנות משפות אחרות.",
  r'''
<p>כמעט כל שאלת סגירות נפתרת בשני מהלכים: <b>(1)</b> לכתוב את השפה החדשה כצירוף של פעולות שכבר סגורות, או <b>(2)</b> להביא דוגמה נגדית קטנה מתוך חמש קבועות.</p>
<table dir="ltr"><thead><tr><th>פעולה</th><th>רגולריות</th><th>ח״ה</th></tr></thead><tbody>
<tr><td>איחוד</td><td>סגורות</td><td>סגורות</td></tr>
<tr><td>שרשור</td><td>סגורות</td><td>סגורות</td></tr>
<tr><td>כוכבית</td><td>סגורות</td><td>סגורות</td></tr>
<tr><td>היפוך</td><td>סגורות</td><td>סגורות</td></tr>
<tr><td>חיתוך <b>עם רגולרית</b></td><td>סגורות</td><td>סגורות</td></tr>
<tr><td>חיתוך (של שתיים)</td><td>סגורות</td><td><b>לא סגורות</b></td></tr>
<tr><td>משלים</td><td>סגורות</td><td><b>לא סגורות</b></td></tr></tbody></table>
<h3>הדוגמאות הנגדיות הקבועות</h3>
<ul>
<li><b>חיתוך ח״ה:</b> $\{a^nb^nc^k\}\cap\{a^kb^nc^n\}=\{a^nb^nc^n\}$. שתיהן ח״ה, החיתוך לא (21S-B-Q19, 24A-A-Q6).</li>
<li><b>משלים ח״ה:</b> $\overline{uu}$ ח״ה, ו-$uu$ לא (21S-B-Q10, 19B-B-Q15).</li>
<li><b>הזוג הקסום:</b> $L$ לא רגולרית ו-$\overline{L}$. האיחוד שלהן הוא $\Sigma^*$ והחיתוך $\emptyset$, שתיהן רגולריות. לכן אין &quot;צירוף של לא רגולריות הוא לא רגולרי&quot; (25A-A-Q2, 25A-A-Q14, 23A-A-Q10).</li>
<li>$L=\Sigma^*$ מפיל כל טענה שאומרת ש-$A(L)$ מורכבת רק מפלינדרומים: $A(L)=\{w\mid w\in L,w^R\in L\}=L\cap L^R$ היא רגולרית, אבל $01\in A(\Sigma^*)$ אינה פלינדרום (23A-B-Q9).</li>
<li><b>מספר סופי של מילים:</b> הוספה או הסרה של קבוצה סופית (שהיא רגולרית) לא משנה רגולריות (25A-C-Q12): אילו $L\cup F$ הייתה רגולרית, גם $L=(L\cup F)\setminus F$.</li>
</ul>
<div class="lesson-rule">🔑 <b>שיטת ההוכחה:</b> אילו $X$ הייתה רגולרית &rarr; אז $L=X\ \mathrm{op}\ R$ עם $R$ רגולרית הייתה רגולרית &rarr; סתירה. ואת הכיוון ההפוך (&quot;אם $f(L)$ רגולרית אז $L$ רגולרית&quot;) כמעט תמיד מפריכים עם $L=\{a^nb^n\}$ ש-$f$ מוחקת לה את המבנה: אם $D_a$ מוחקת כל $a$, אז $D_a(\{a^nb^n\})=b^*$ (24A-A-Q15).</div>
<div class="lesson-trap">⚠️ <b>הפיכת מצבים מקבלים</b> נותנת משלים <b>רק באס״ד</b> (שלם). באסל״ד ובאוטומט מחסנית היא לא (24X-C-Q12, 24A-C-Q8). ושפה שמקיימת את הלמה היא לא בהכרח רגולרית, ולכן הלמה לא מוכיחה סגירות.</div>
''',
  [
    Q(r"$L$ רגולרית, ו-$A(L)=\{w\mid w\in L\ \text{וגם}\ w^R\in L\}$. נתונות שתי טענות. I: אם $L$ רגולרית אז $A(L)$ רגולרית. II: כל מילה ב-$A(L)$ היא פלינדרום. איזו נכונה?".replace(r"\ \text{וגם}\ ", r"\ \wedge\ "),
      [C(r"רק I נכונה", I_ok and not II_ok), C(r"רק II נכונה", II_ok and not I_ok), C(r"שתיהן נכונות", I_ok and II_ok), C(r"אף אחת לא נכונה", not I_ok and not II_ok)],
      why=r"$A(L)=L\cap L^R$, וחיתוך והיפוך סגורים לרגולריות, ולכן I נכונה (בדקנו על כמה שפות שהשפה $A(L)$ אכן בעלת Rank סופי). II שגויה: עבור $L=\Sigma^*$ מתקבל $A(L)=\Sigma^*$ וכולל את $ab$ שאינה פלינדרום. $w\in L$ וגם $w^R\in L$ לא אומר $w=w^R$.",
      recap="Σ* היא הדוגמה הנגדית האוניברסלית לטענה חזקה מדי"),
    Q(r"איזו פעולה **לא** סגורה למחלקת השפות חסרות ההקשר?",
      [C(r"חיתוך של שתי שפות ח״ה", int_label == "noncfl" and cfl1 == "cfl" and cfl2 == "cfl"), J(r"איחוד של שתי שפות ח״ה", False),
       J(r"שרשור של שתי שפות ח״ה", False), J(r"חיתוך של שפה ח״ה עם שפה רגולרית", False)],
      why=r"$\{a^ib^kc^k\}$ ו-$\{a^kb^kc^i\}$ שתיהן ח״ה (אימתנו דקדוקים), והחיתוך שלהן הוא $\{a^nb^nc^n\}$, שאינה ח״ה (בדקנו את משחק הניפוח עבור $p=2,3,4$). איחוד, שרשור וחיתוך עם שפה רגולרית סגורים (דף הנוסחאות).",
      recap="חיתוך של שתי ח״ה לא סגור; עם רגולרית כן"),
    Q(r"$L_1=\{a^ib^kc^k\}$, $L_2=\{a^kb^ic^k\}$, $L_3=\{a^kb^kc^i\}$ ו-$M$ היא קבוצת המילים ששייכות **לפחות** לשתיים משלוש השפות. מהי $M$?",
      cls_opts(m_label),
      why=r"מילה ששייכת לשתיים מהשלוש חייבת לקיים שני שוויונות בין שלושת המונים, ולכן $i=k$ לכל המונים: $M=\{a^kb^kc^k\}$ (בדקנו שוויון על כל המילים עד אורך $8$). זו לא ח״ה. לכן הסגירות לחיתוך ולאיחוד של ח״ה לא נשמרת (24A-A-Q6), בעוד שברגולריות כן.",
      recap="לפחות שתיים משלוש: a^k b^k c^k".replace("a^k b^k c^k", "$a^kb^kc^k$")),
    Q(r"$L=\{a^nb^n\}$ ו-$F$ שפה **סופית** של מילים. איזו טענה נכונה?",
      [C(r"$L\cup F$ אף פעם לא רגולרית", union_nonreg), C(r"$L\cup F$ תמיד רגולרית", not union_nonreg),
       C(r"$L\setminus F$ תמיד רגולרית", not diff_nonreg), J(r"אי אפשר לדעת בלי לדעת מה $F$", False)],
      why=r"אילו $L\cup F$ הייתה רגולרית, אז $L=(L\cup F)\setminus F$ הייתה רגולרית (הפרש עם סופית, והיא רגולרית), בסתירה לכך ש-$L$ לא רגולרית. אותו טיעון עבור $L\setminus F$ (נוסיף $F\cap L$ חזרה). בדקנו על דוגמה ש-$\mathrm{Rank}$ ממשיך לגדול בשתי השפות.",
      recap="הוספה או הסרה של מספר סופי של מילים לא משנה רגולריות"),
    Q(r"$L$ לא רגולרית. איזו טענה נכונה?",
      [C(r"$L\cup\overline{L}$ רגולרית, ולכן איחוד (וגם חיתוך) של שפות לא רגולריות יכול להיות רגולרי", rank_union == 1 and rank_inter == 1),
       C(r"איחוד של שתי שפות לא רגולריות אף פעם לא רגולרי", not (rank_union == 1)),
       C(r"המשלים של שפה לא רגולרית הוא תמיד רגולרי", not comp_nonreg), C(r"חיתוך של שתי שפות לא רגולריות אף פעם לא רגולרי", not (rank_inter == 1))],
      why=r"עבור $L=\{a^nb^n\}$ האיחוד $L\cup\overline{L}=\Sigma^*$ והחיתוך $L\cap\overline{L}=\emptyset$ רגולריים (שניהם $\mathrm{Rank}=1$), אף ששתי השפות לא רגולריות. המשלים של לא רגולרית הוא לא רגולרי (אחרת $L$ הייתה רגולרית, כי רגולריות סגורות למשלים).",
      recap="L והמשלים שלה: איחוד Σ*, חיתוך ∅"),
  ])
