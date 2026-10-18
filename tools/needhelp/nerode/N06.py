# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def R(pred, alpha="ab", slen=7, plens=(4, 5, 6)):
    r = rank_stable(pred, alpha, slen, plens)
    return r if r is not None else rank_stable(pred, alpha, slen + 2, tuple(x + 2 for x in plens))


EVEN = lambda w: len(w) % 2 == 0
ODD = lambda w: len(w) % 2 == 1
M3 = lambda w: len(w) % 3 == 0
ALL = lambda w: True
EMPTY = lambda w: False
AA = lambda w: len(w) % 2 == 0 and set(w) <= {"a"}          # (aa)* over {a,b}
comp = lambda p: (lambda w: not p(w))
cap = lambda p, q: (lambda w: p(w) and q(w))
cup = lambda p, q: (lambda w: p(w) or q(w))

# the five facts as computed statements
LANGS = [EVEN, M3, AA, lambda w: w.endswith("a"), lambda w: "ab" in w]
f_comp = all(R(comp(p)) == R(p) for p in LANGS)
f_union_prod = all(R(cup(p, q)) == R(p) * R(q) for p in LANGS for q in LANGS)
f_cap_max = all(R(cap(p, q)) <= max(R(p), R(q)) for p in LANGS for q in LANGS)
# L1 subset of L2 implies Rank(L1) <= Rank(L2): fails for (aa)... use even lengths inside Sigma*
f_subset = all(R(p) <= R(q) for p, q in [(EVEN, ALL), (AA, EVEN), (EMPTY, ALL)])
assert f_comp and not f_union_prod and not f_cap_max and not f_subset
R_CAP = R(cap(EVEN, M3))
assert R_CAP == 6
R_UNION, R_CAPEO = R(cup(EVEN, ODD)), R(cap(EVEN, ODD))
assert (R(EVEN), R(ODD), R_UNION, R_CAPEO) == (2, 2, 1, 1)

# reversal: third letter from the end is 'a'  vs  third letter from the start is 'a'
T_END = lambda w: len(w) >= 3 and w[-3] == "a"
T_REV = lambda w: T_END(w[::-1])
R_TE, R_TR = R(T_END), R(T_REV)
assert (R_TE, R_TR) == (8, 5)

# star: palindromes* = Sigma*  (each letter is a palindrome)
def in_star(w, p):
    ok = [True] + [False] * len(w)
    for j in range(1, len(w) + 1):
        ok[j] = any(ok[i] and p(w[i:j]) for i in range(j))
    return ok[len(w)]


PAL = lambda w: w == w[::-1]
pal_star_is_all = all(in_star(w, PAL) for w in words("ab", 9))
star_greater = all(R(lambda w, p=p: in_star(w, p)) > R(p) for p in [ALL, EVEN, AA])
star_equal = all(R(lambda w, p=p: in_star(w, p)) == R(p) for p in [lambda w: w == "a", ALL])
assert pal_star_is_all and not star_greater and not star_equal

LEVEL = level("N06", 6, "🔧", "Rank של פעולות על שפות",
  "לדעת מה נכון תמיד על Rank של משלים, איחוד, חיתוך, היפוך וכוכבית, ולהפיל כל טענה אחרת בדוגמה נגדית קבועה.",
  r'''
<p>15 שאלות בבנק שואלות על $\mathrm{Rank}$ של פעולות. כמעט כולן נפתרות בלי חישוב: יש <b>כמה טענות שנכונות תמיד</b>, וכל האחרות נופלות על אחת משלוש דוגמאות נגדיות קבועות.</p>
<h3>מה נכון תמיד</h3>
<ul>
<li>$\mathrm{Rank}(\overline{L})=\mathrm{Rank}(L)$, <b>לכל $L$</b> (גם לא רגולרית): אותה סיפא מפרידה מפרידה בשתי השפות (24X-C-Q17, 26A-A-Q14).</li>
<li>$\mathrm{Rank}(L_1\cap L_2)\le\mathrm{Rank}(L_1)\cdot\mathrm{Rank}(L_2)$ וגם $\mathrm{Rank}(L_1\cup L_2)\le\mathrm{Rank}(L_1)\cdot\mathrm{Rank}(L_2)$: אוטומט מכפלה (19B-A-Q22, 23A-A-Q21).</li>
<li>חיתוך עם &quot;אורך זוגי&quot;: $\mathrm{Rank}\le2\cdot\mathrm{Rank}(L)$ (19B-B-Q21, SAMP-19-Q20).</li>
<li>$\mathrm{Rank}(L)<\infty\Rightarrow\mathrm{Rank}(L^*)<\infty$, כי רגולריות סגורה לכוכבית (24A-B-Q9).</li>
</ul>
<h3>שלוש הדוגמאות שמפילות כל טענה אחרת</h3>
<table dir="ltr"><thead><tr><th>הזוג</th><th>Ranks</th><th>$\cup$</th><th>$\cap$</th></tr></thead><tbody>
<tr><td>אי-זוגי, זוגי</td><td>$2,2$</td><td>$\Sigma^*$: $1$</td><td>$\emptyset$: $1$</td></tr>
<tr><td>אורך מתחלק ב-$3$, אורך זוגי</td><td>$3,2$</td><td>$6$</td><td>$6$</td></tr>
<tr><td>$\Sigma^*,\Sigma^*$</td><td>$1,1$</td><td>$1$</td><td>$1$</td></tr></tbody></table>
<ul>
<li>הזוג הראשון מפיל כל &quot;=&quot; למכפלה או לסכום וכל &quot;$\ge$&quot; (25A-B-Q18, 21S-B-Q8).</li>
<li>הזוג השני מפיל &quot;$\le$ מקסימום&quot; ו&quot;$\le$ סכום&quot; (19B-A-Q22).</li>
<li>$L_1\subseteq L_2$ לא גורר $\mathrm{Rank}(L_1)\le\mathrm{Rank}(L_2)$: $(\Sigma\Sigma)^*\subseteq\Sigma^*$ אבל $2>1$.</li>
</ul>
<div class="lesson-trap">⚠️ <b>היפוך:</b> ל-$L$ <b>רגולרית</b> אין כלל ש-$\mathrm{Rank}(L^R)=\mathrm{Rank}(L)$: &quot;האות השלישית מהסוף היא $1$&quot; נותנת $8$, וההיפוך (&quot;השלישית מההתחלה&quot;) נותן $5$. אבל אם $L$ לא רגולרית, שתי ה-$\mathrm{Rank}$ אינסופיים (MQ3-Q4, 23A-A-Q6).</div>
<div class="lesson-trap">⚠️ <b>כוכבית:</b> $\mathrm{Rank}(L^*)=\infty$ גורר $\mathrm{Rank}(L)=\infty$, אבל לא להפך: פלינדרומים הם לא רגולריים, ואילו אוסף הפלינדרומים בכוכבית הוא $\Sigma^*$ (כל אות היא פלינדרום), עם $\mathrm{Rank}=1$ (24A-B-Q9, 24X-A-Q10).</div>
''',
  [
    Q(r"איזו טענה נכונה **לכל** שתי שפות $L_1,L_2$ (ולכל $L$)?",
      [C(r"$\mathrm{Rank}(\overline{L})=\mathrm{Rank}(L)$", f_comp),
       C(r"$\mathrm{Rank}(L_1\cup L_2)=\mathrm{Rank}(L_1)\cdot\mathrm{Rank}(L_2)$", f_union_prod),
       C(r"$\mathrm{Rank}(L_1\cap L_2)\le\max\{\mathrm{Rank}(L_1),\mathrm{Rank}(L_2)\}$", f_cap_max),
       C(r"$L_1\subseteq L_2\Rightarrow\mathrm{Rank}(L_1)\le\mathrm{Rank}(L_2)$", f_subset)],
      why=r"סיפא מפרידה בין $x,y$ עבור $L$ אם ורק אם היא מפרידה עבור $\overline{L}$, ולכן המחלקות זהות. הפרכות: איחוד של $(aa)^*$ עם עצמה נותן $2\ne2\cdot2$; חיתוך של &quot;אורך זוגי&quot; ו&quot;אורך מתחלק ב-$3$&quot; נותן $6>\max\{2,3\}$; $(\Sigma\Sigma)^*\subseteq\Sigma^*$ אך $2>1$. (בדקנו את כל אלה על דוגמאות.)",
      recap="Rank של משלים שווה תמיד; כל השאר נופל על דוגמה"),
    Q(r"$L_1$ היא שפת המילים מעל $\{a,b\}$ באורך זוגי ($\mathrm{Rank}=2$), ו-$L_2$ היא שפת המילים שאורכן מתחלק ב-$3$ ($\mathrm{Rank}=3$). מהו $\mathrm{Rank}(L_1\cap L_2)$?",
      [C(str(k), R_CAP == k) for k in (5, 6, 2, 3)],
      why=r"החיתוך הוא המילים שאורכן מתחלק ב-$6$, ולכן צריך לזכור את האורך מודולו $6$: $6$ מחלקות. זה בדיוק חסם המכפלה $2\cdot3=6$ והוא מושג כאן. הוא מפיל &quot;$\le$ מקסימום&quot; ו&quot;$\le$ סכום&quot; ($3$ ו-$5$).",
      recap="אורך זוגי ∩ אורך מתחלק ב-3: Rank 6"),
    Q(r"$L_1$ היא שפת המילים באורך אי-זוגי ו-$L_2$ היא שפת המילים באורך זוגי (מעל $\{a,b\}$), כל אחת עם $\mathrm{Rank}=2$. מהו $\mathrm{Rank}(L_1\cup L_2)$?",
      [C(str(k), R_UNION == k) for k in (1, 2, 3, 4)],
      why=r"האיחוד הוא כל המילים, $\Sigma^*$, ו-$\mathrm{Rank}(\Sigma^*)=1$. (החיתוך הוא $\emptyset$ וגם בו $\mathrm{Rank}=1$.) לכן $\mathrm{Rank}$ של איחוד לא שווה למכפלה ($4$) ולא לסכום ($4$) ולא למקסימום ($2$).",
      recap="אי-זוגי ∪ זוגי = Σ*: Rank 1"),
    Q(r"$L$ היא שפת המילים מעל $\{a,b\}$ שהאות השלישית מהסוף בהן היא $a$ ($\mathrm{Rank}(L)=8$). מהו $\mathrm{Rank}(L^R)$, כלומר של שפת ההיפוכים?",
      [C(str(k), R_TR == k) for k in (4, 5, 6, 8)],
      why=r"$L^R$ היא שפת המילים שהאות השלישית מ**ההתחלה** בהן היא $a$. קוראים שלוש אותיות ואז מחליטים: שלושה מצבים לקריאה, ועוד &quot;כן&quot; (מקבל) ו&quot;לא&quot; (מלכודת): $5$. לכן $\mathrm{Rank}(L^R)\ne\mathrm{Rank}(L)$ גם כש-$L$ רגולרית (חישבנו: $8$ מול $5$). &quot;מההתחלה&quot; זול ו&quot;מהסוף&quot; יקר.",
      recap="היפוך משנה Rank בשפות רגולריות: 8 מול 5"),
    Q(r"איזו טענה על $\mathrm{Rank}$ והכוכבית נכונה?",
      [J(r"אם $\mathrm{Rank}(L)<\infty$ אז $\mathrm{Rank}(L^*)<\infty$", True),
       C(r"אם $\mathrm{Rank}(L)=\infty$ אז $\mathrm{Rank}(L^*)=\infty$ (למשל עבור פלינדרומים)", not pal_star_is_all),
       C(r"$\mathrm{Rank}(L^*)>\mathrm{Rank}(L)$ תמיד", star_greater),
       C(r"$\mathrm{Rank}(L^*)=\mathrm{Rank}(L)$ תמיד", star_equal)],
      why=r"אם $L$ רגולרית אז גם $L^*$ (רגולריות סגורה לכוכבית), ולכן $\mathrm{Rank}$ סופי. ההפך נופל על פלינדרומים: הם לא רגולריים ($\mathrm{Rank}=\infty$), אבל כל אות היא פלינדרום ולכן $L^*=\Sigma^*$ ו-$\mathrm{Rank}=1$ (בדקנו שכל מילה עד אורך $9$ פירוק לפלינדרומים). $\mathrm{Rank}(L^*)>\mathrm{Rank}(L)$ נופל על $\Sigma^*$; השוויון נופל על $L=\{a\}$ ($3$ מול $1$).",
      recap="Rank(L) סופי גורר Rank(L*) סופי, לא להפך"),
  ])
