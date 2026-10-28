# -*- coding: utf-8 -*-
"""N06 · Rank של פעולות על שפות — video script (build: tools/video/vid.py N06).

Source: tools/needhelp/nerode/N06.py (lesson + goal). The lesson's fixed counterexamples (odd/even, length divisible by
3 / even, Σ*/Σ*) are recomputed here. Exam anchors (all cited by the lesson, none in the quiz): 21S-B-Q8, 19B-A-Q22,
23A-A-Q6. Not used on purpose: the quiz's own questions (the general "which is always true", Rank(even∩mod3) asked as
a number, Rank(odd∪even) asked as a number, third-letter-from-the-end over {a,b}, the star question).
"""
from nh import words, rank_stable, rank_growing, separable, dfa_table
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, table, wd


def R(pred, alpha="ab", slen=7, plens=(4, 5, 6)):
    r = rank_stable(pred, alpha, slen, plens)
    return r if r is not None else rank_stable(pred, alpha, slen + 2, tuple(x + 2 for x in plens))


EVEN = lambda w: len(w) % 2 == 0
ODD = lambda w: len(w) % 2 == 1
M3 = lambda w: len(w) % 3 == 0
ALL = lambda w: True
comp = lambda p: (lambda w: not p(w))
cap = lambda p, q: (lambda w: p(w) and q(w))
cup = lambda p, q: (lambda w: p(w) or q(w))

# complement: same classes (the same suffix separates), for several languages incl. a non-regular one (growing)
AA = lambda w: "aa" in w
for p in (AA, EVEN, M3, lambda w: w.endswith("ab")):
    assert R(comp(p)) == R(p)
    assert all((separable(p, x, y, "ab", 6) is None) == (separable(comp(p), x, y, "ab", 6) is None)
               for x in words("ab", 3) for y in words("ab", 3))
EQ = lambda w: w.count("a") == w.count("b")
assert rank_growing(EQ, "ab") and rank_growing(comp(EQ), "ab")
DA = dfa_table("ab", {"0": "1 0", "1": "2 0", "2": "2 2"}, "0", {"2"})
DAc = DA.complement()
assert DA.n_min() == DAc.n_min() == 3 and all(DAc.accepts(w) != AA(w) for w in words("ab", 7))

# the lesson's three counterexample IDEAS, with different numbers than the quiz's answers (quiz: odd∪even=1,
# even∩mod3=6, (ΣΣ)*⊆Σ*): a language with its complement, two coprime length counters, Σ* with itself.
N3_ = lambda w: len(w) % 3 != 0
M4 = lambda w: len(w) % 4 == 0
RU = lambda p: rank_stable(p, "a", 16, (14, 15, 16))      # length-only languages: the same classes over {a}
assert R(M3) == RU(M3) == 3 and R(N3_) == RU(N3_) == 3 and RU(M4) == 4 and R(M4, "ab", 7, (5, 6, 7)) == 4
P1 = (RU(M3), RU(N3_), RU(cup(M3, N3_)), RU(cap(M3, N3_)))
P2 = (RU(M3), RU(M4), RU(cup(M3, M4)), RU(cap(M3, M4)))
P3 = (R(ALL), R(ALL), R(ALL), R(ALL))
assert P1 == (3, 3, 1, 1) and P2 == (3, 4, 12, 12) and P3 == (1, 1, 1, 1)
assert R(cup(M3, N3_)) == 1 and not any(M3(w) and N3_(w) for w in words("ab", 7))       # disjoint, union Σ*
assert P2[3] > max(3, 4) and P2[3] > 3 + 4 and P2[3] <= 3 * 4
# subset is not monotone: (ΣΣΣ)* ⊆ Σ*, 3 > 1
assert R(M3) == 3 > R(ALL) == 1
P1q = (R(ODD), R(EVEN), R(cup(ODD, EVEN)), R(cap(ODD, EVEN)))                     # the lesson's own pair (not shown)
assert P1q == (2, 2, 1, 1)
# product bound holds on all pairs of a small family; max and sum bounds fail on pair 2
FAM = [EVEN, ODD, M3, AA, ALL, lambda w: w.endswith("a")]
assert all(R(op(p, q)) <= R(p) * R(q) for p in FAM for q in FAM for op in (cap, cup))
assert R(cap(M3, EVEN)) > max(3, 2) and R(cap(M3, EVEN)) > 3 + 2
# intersection with even length: <= 2 Rank(L)
assert all(R(cap(p, EVEN)) <= 2 * R(p) for p in FAM)
# subset is not monotone: (ΣΣ)* ⊆ Σ*, 2 > 1
assert all(ALL(w) for w in words("ab", 6) if EVEN(w)) and R(EVEN) == 2 > R(ALL) == 1

# reversal (bank's counterexample for 23A-A-Q6): starts with 1 (3) vs ends with 1 (2)
S1 = lambda w: w.startswith("1")
E1 = lambda w: w.endswith("1")
assert all(S1(w) == E1(w[::-1]) for w in words("01", 7))
assert R(S1, "01") == 3 and R(E1, "01") == 2
ANBN = lambda w: w == "a" * (len(w) // 2) + "b" * (len(w) // 2)
ANBN_R = lambda w: ANBN(w[::-1])
assert rank_growing(ANBN, "ab") and rank_growing(ANBN_R, "ab")       # non-regular stays non-regular: ∞ = ∞

# exam questions
QA, QB, QC = BANK["21S-B-Q8"], BANK["19B-A-Q22"], BANK["23A-A-Q6"]
assert (QA["correctId"], QB["correctId"], QC["correctId"]) == ("d", "c", "c")
VA = {o["id"]: o["value"] for o in QA["options"]}
assert "\\times\\mathrm{Rank}(L_2)" in VA["a"] and "+\\mathrm{Rank}(L_2)" in VA["b"] and "subseteq" in VA["c"]
VB = {o["id"]: o["value"] for o in QB["options"]}
assert "max" in VB["a"] and "+" in VB["b"] and "cdot" in VB["c"] and "infty" in VB["d"]
VC = {o["id"]: o["value"] for o in QC["options"]}
assert "רגולרית אז" in VC["a"] and "אינסופית" in VC["b"] and "לא-רגולרית" in VC["c"] and "כל" in VC["d"]

title = Scene("title", "", [
    N("חמש עשרה שאלות בבנק שואלות על Rank של פעולות: משלים, איחוד, חיתוך, היפוך וכוכבית.",
      say="חמש עשרה שאלות בבנק שואלות על ראנק של פעולות: משלים, איחוד, חיתוך, היפוך וכוכבית."),
    N("כמעט כולן נפתרות בלי חישוב: כמה טענות שנכונות תמיד, ושלוש דוגמאות נגדיות קבועות שמפילות את כל השאר.", hold=0.4),
], stage=CSS + '<div class="kicker">N06 · נרוד, Rank וקבוצות מפרידות</div><h1>Rank של פעולות על שפות</h1>'
         '<p>לדעת מה נכון תמיד על Rank של משלים, איחוד, חיתוך, היפוך וכוכבית, ולהפיל כל טענה אחרת בדוגמה נגדית קבועה.</p>',
   layout="title")

POS = {"0": (170, 160), "1": (450, 160), "2": (730, 160)}
NM = {"0": "q_0", "1": "q_1", "2": "q_2"}
compl = Scene("compl", "משלים: תמיד שווה", [
    N("נתחיל בטענה שנכונה **תמיד**: ל-$L$ ולמשלים שלה יש אותו Rank. לכל שפה, גם לא רגולרית.",
      say="נתחיל בטענה שנכונה תמיד: לאל ולמשלים שלה יש אותו ראנק. לכל שפה, גם לא רגולרית.", do=show("c-rule")),
    N("למה? נניח ש-$z$ מפרידה בין $x$ ל-$y$ עבור $L$: $xz\\in L$ ו-$yz\\notin L$.",
      say="למה? נניח שזד מפרידה בין אקס לוואי עבור אל: אקס זד בשפה, ווואי זד לא.", do=show("c-1")),
    N("אז במשלים הכול מתהפך: $xz$ לא במשלים, ו-$yz$ כן. אותה $z$ מפרידה גם שם.",
      say="אז במשלים הכול מתהפך: אקס זד לא במשלים, ווואי זד כן. אותה זד מפרידה גם שם.", do=show("c-2")),
    N("אותן הפרדות, אותן מחלקות, אותו Rank.", say="אותן הפרדות, אותן מחלקות, אותו ראנק."),
    N("ובאוטומט רואים את זה: הופכים מקבלים ללא מקבלים. אותו מספר מצבים.",
      do=hide("c-1", "c-2") + show("c-dfa1")),
    N("למשל ״מכילה $aa$״: שלושה מצבים. והמשלים, ״לא מכילה $aa$״: אותם שלושה מצבים, עם מקבלים הפוכים.",
      say="למשל מכילה אֵיי אֵיי: שלושה מצבים. והמשלים, לא מכילה אֵיי אֵיי: אותם שלושה מצבים, עם מקבלים הפוכים.",
      do=show("c-dfa2"), hold=0.5),
], stage='<div id="c-1" class="h nr-big">$xz\\in L$, &nbsp; $yz\\notin L$</div>'
         '<div id="c-2" class="h nr-big">$xz\\notin\\overline{L}$, &nbsp; $yz\\in\\overline{L}$</div>'
         f'<div id="c-dfa1" class="h">{st.dfa_svg("ca", DA, POS, NM, w=900, h=270, scale=0.8)}</div>'
         f'<div id="c-dfa2" class="h">{st.dfa_svg("cb", DAc, POS, NM, w=900, h=270, scale=0.8)}</div>',
   panel=st.card("c-rule", "rule", "🔑 $\\mathrm{Rank}(\\overline{L})=\\mathrm{Rank}(L)$, <b>לכל</b> $L$"))

always = Scene("always", "מה עוד נכון תמיד", [
    N("שתי טענות נוספות שנכונות תמיד. אחת: Rank של חיתוך, וגם של איחוד, קטן או שווה **למכפלה** של ה-Ranks.",
      say="שתי טענות נוספות שנכונות תמיד. אחת: ראנק של חיתוך, וגם של איחוד, קטן או שווה למכפלה של הראנקים.", do=show("a1")),
    N("הסיבה: אוטומט המכפלה. מצב שלו הוא זוג, מצב מכל אוטומט, ויש בדיוק מכפלה של זוגות כאלה.",
      do=show("a-pr")),
    N("ומקרה פרטי שחוזר: חיתוך עם ״אורך זוגי״ קטן או שווה לפעמיים ה-Rank. ל״אורך זוגי״ יש שתי מחלקות.",
      say="ומקרה פרטי שחוזר: חיתוך עם אורך זוגי קטן או שווה לפעמיים הראנק. לאורך זוגי יש שתי מחלקות.", do=show("a2")),
    N("ושתיים: אם ה-Rank של $L$ סופי, גם של $L^*$ סופי. שפה רגולרית בכוכבית נשארת רגולרית.",
      say="ושתיים: אם הראנק של אל סופי, גם של אל כוכבית סופי. שפה רגולרית בכוכבית נשארת רגולרית.", do=show("a3")),
    N("שימו לב לכיוון: ההפך לא נכון. פלינדרומים לא רגולריים, אבל בכוכבית הם כל המילים, כי כל אות היא פלינדרום.",
      do=show("a4")),
    N("וזהו. **כמעט כל טענה אחרת** במבחן, ובמיוחד כל ״שווה״, נופלת על דוגמה נגדית.", do=show("a5")),
    N("חוץ מהיפוך של שפה לא רגולרית, שנראה בהמשך.", hold=0.5),
], stage='<div id="a-pr" class="h nr-big">$(p,q)$: &nbsp; מצב של $L_1$ × מצב של $L_2$</div>',
   panel=st.card("a1", "rule", "🔑 $\\mathrm{Rank}(L_1\\cap L_2),\\ \\mathrm{Rank}(L_1\\cup L_2)\\le\\mathrm{Rank}(L_1)\\cdot\\mathrm{Rank}(L_2)$")
       + st.card("a2", "rule", "🔑 חיתוך עם אורך זוגי: $\\le2\\cdot\\mathrm{Rank}(L)$")
       + st.card("a3", "rule", "🔑 אם $\\mathrm{Rank}(L)<\\infty$, אז $\\mathrm{Rank}(L^*)<\\infty$")
       + st.card("a4", "trap", "⚠️ לא להפך: פלינדרומים בכוכבית $=\\Sigma^*$")
       + st.card("a5", "trap", "⚠️ כמעט כל ״שווה״ נופל על דוגמה נגדית"))

TRIO = table("t", ["הזוג", "Ranks", "$\\cup$", "$\\cap$"],
             [["שפה ומשלימתה", "$3,3$", "$\\Sigma^*$: $1$", "$\\emptyset$: $1$"],
              ["$3\\mid|w|$, &nbsp;$4\\mid|w|$", "$3,4$", "$12$", "$12$"],
              ["$\\Sigma^*,\\Sigma^*$", "$1,1$", "$1$", "$1$"]])
trio = Scene("trio", "שלוש הדוגמאות הנגדיות", [
    N("שלושה רעיונות לדוגמאות נגדיות, כולן מעל $\\{a,b\\}$. כדאי לזכור אותם בעל פה.",
      say="שלושה רעיונות לדוגמאות נגדיות, כולן מעל אֵיי ובִּי. כדאי לזכור אותם בעל פה.", do=show("t")),
    N("ראשון: שפה **והמשלימה שלה**. למשל אורך שמתחלק בשלוש, ואורך שלא מתחלק בשלוש. לכל אחת Rank שלוש.",
      say="ראשון: שפה והמשלימה שלה. למשל אורך שמתחלק בשלוש, ואורך שלא מתחלק בשלוש. לכל אחת ראנק שלוש.", do=show("t-r-0")),
    N("הן זרות, האיחוד שלהן הוא כל המילים, והחיתוך ריק. Rank אחת בשניהם!", say="הן זרות, האיחוד שלהן הוא כל המילים, והחיתוך ריק. ראנק אחת בשניהם!",
      do=show("t-s-0")),
    N("זה מפיל כל ״שווה למכפלה״, כל ״שווה לסכום״ וכל ״גדול או שווה״.", do=show("t-k1")),
    N("שני: שני מוני אורך זרים. אורך שמתחלק בשלוש, ואורך שמתחלק בארבע. Ranks שלוש וארבע.",
      say="שני: שני מוני אורך זרים. אורך שמתחלק בשלוש, ואורך שמתחלק בארבע. ראנקים שלוש וארבע.",
      do=hide("t-s-0") + show("t-r-1")),
    N("החיתוך הוא אורך שמתחלק בשתים עשרה: שתים עשרה מחלקות. יותר מהמקסימום, ויותר מהסכום, שבע.",
      do=show("t-s-1", "t-k2")),
    N("ושלישי: כל המילים עם עצמה. הכול אחת. זה מפיל כל ״גדול ממש״.",
      do=hide("t-s-1") + show("t-r-2", "t-k3")),
    N("ובונוס: אורך שמתחלק בשלוש מוכל בכל המילים, אבל ה-Rank שלו שלוש, ושל כל המילים אחת. הכלה לא שומרת על סדר.",
      say="ובונוס: אורך שמתחלק בשלוש מוכל בכל המילים, אבל הראנק שלו שלוש, ושל כל המילים אחת. הכלה לא שומרת על סדר.",
      do=show("t-k4"), hold=0.5),
], stage=TRIO.replace('class="nr-st"', 'class="nr-st h"', 1),
   panel=st.card("t-k1", "plain", "זוג 1 מפיל: $=$ מכפלה, $=$ סכום, $\\ge$")
       + st.card("t-k2", "plain", "זוג 2 מפיל: $\\le\\max$, $\\le$ סכום")
       + st.card("t-k3", "plain", "זוג 3 מפיל: $>$ ממש")
       + st.card("t-k4", "trap", "⚠️ $(\\Sigma\\Sigma\\Sigma)^*\\subseteq\\Sigma^*$ אבל $3>1$"))

OA = [("a", "אם $L_1\\cap L_2=\\emptyset$, אז $\\mathrm{Rank}(L_1\\cup L_2)=\\mathrm{Rank}(L_1)\\times\\mathrm{Rank}(L_2)$"),
      ("b", "אם $L_1\\cap L_2=\\emptyset$, אז $\\mathrm{Rank}(L_1\\cup L_2)=\\mathrm{Rank}(L_1)+\\mathrm{Rank}(L_2)$"),
      ("c", "אם $L_1\\subseteq L_2$, אז $\\mathrm{Rank}(L_1)\\le\\mathrm{Rank}(L_2)$"),
      ("d", "כל הטענות האחרות לא נכונות")]
examA = Scene("examA", "שאלה ממבחן", [
    N("שאלה ממבחן: $L_1,L_2$ רגולריות. איזו טענה נכונה?", say="שאלה ממבחן: אל אחת ואל שתיים רגולריות. איזו טענה נכונה?"),
    N("שתי הראשונות: ״אם השפות זרות, ה-Rank של האיחוד שווה למכפלה״, או ״לסכום״. ״שווה״? מחפשים דוגמה.",
      say="שתי הראשונות: אם השפות זרות, הראנק של האיחוד שווה למכפלה, או לסכום. שווה? מחפשים דוגמה."),
    N("רעיון מספר אחת: שפה ומשלימתה. אורך שמתחלק בשלוש, ואורך שלא. הן זרות! והאיחוד הוא כל המילים, Rank אחת.",
      say="רעיון מספר אחת: שפה ומשלימתה. אורך שמתחלק בשלוש, ואורך שלא. הן זרות! והאיחוד הוא כל המילים, ראנק אחת.",
      do=show("x-1")),
    N("לא המכפלה, תשע, ולא הסכום, שש. שתיהן נופלות.", do=show("q-x-a", "q-x-b")),
    N("השלישית, הכלה: אורך שמתחלק בשלוש מוכל בכל המילים, אבל שלוש גדול מאחת. נופלת.",
      do=show("x-2", "q-x-c")),
    N("התשובה: ״כל הטענות האחרות לא נכונות״. והמלכודת: לחשוב ש״זרות״ הופכת את האיחוד לפשוט לחישוב.",
      say="התשובה: כל הטענות האחרות לא נכונות. והמלכודת: לחשוב שזרות הופכת את האיחוד לפשוט לחישוב.",
      do=show("q-ok-d"), hold=0.6),
], stage='<div id="x-1" class="h nr-big">$|w|\\bmod3=0$ $\\cup$ $|w|\\bmod3\\ne0$ $=\\Sigma^*$: &nbsp; $1\\ne9$, $1\\ne6$</div>'
         '<div id="x-2" class="h nr-big">$(\\Sigma\\Sigma\\Sigma)^*\\subseteq\\Sigma^*$: &nbsp; $3>1$</div>',
   panel=f'<div class="qstem"><span class="qid">{QA["id"]}</span>$L_1,L_2$ רגולריות. איזו טענה נכונה?</div>'
       + st.options("q", OA))

examB = Scene("examB", "עוד שאלה: חיתוך", [
    N("עוד שאלה: $L$ היא החיתוך של שתי שפות רגולריות. מה נכון?", say="עוד שאלה: אל היא החיתוך של שתי שפות רגולריות. מה נכון?"),
    N("״Rank אינסופי״? לא: חיתוך של רגולריות הוא רגולרי.", say="ראנק אינסופי? לא: חיתוך של רגולריות הוא רגולרי.",
      do=show("p-x-d")),
    N("״קטן או שווה למקסימום״, או ״לסכום״? רעיון מספר שתיים: Ranks שלוש וארבע, והחיתוך שתים עשרה.",
      say="קטן או שווה למקסימום, או לסכום? רעיון מספר שתיים: ראנקים שלוש וארבע, והחיתוך שתים עשרה.", do=show("y-1")),
    N("שתים עשרה גדול מארבע ומשבע. שתיהן נופלות.", do=show("p-x-a", "p-x-b")),
    N("נשאר חסם המכפלה: שתים עשרה קטן או שווה לשתים עשרה. וזה נכון תמיד, בגלל אוטומט המכפלה.",
      do=show("p-ok-c"), hold=0.6),
], stage='<div id="y-1" class="h nr-big">$|w|\\bmod3=0$ $\\cap$ $|w|\\bmod4=0$ $=$ $|w|\\bmod12=0$: &nbsp; $\\mathrm{Rank}=12$</div>'
         '<div class="nr-big">$12>\\max\\{3,4\\}$ &nbsp; $12>3+4$ &nbsp; $12\\le3\\cdot4$</div>',
   panel=f'<div class="qstem"><span class="qid">{QB["id"]}</span>{QB["questionHtml"]}</div>'
       + st.options("p", [(o["id"], o["html"]) for o in QB["options"]]))

OC = [("a", "אם $L$ רגולרית, אז $\\mathrm{Rank}(L)=\\mathrm{Rank}(L^R)$"),
      ("b", "אם $\\mathrm{Rank}(L)\\ne\\mathrm{Rank}(L^R)$, אז יש ל-$L^R$ קבוצה מפרידה אינסופית"),
      ("c", "אם $L$ לא רגולרית, אז $\\mathrm{Rank}(L)=\\mathrm{Rank}(L^R)$"),
      ("d", "כל הטענות האחרות לא נכונות")]
examC = Scene("examC", "שאלה שלישית: היפוך", [
    N("ושאלה על היפוך: $L^R$ היא השפה של המילים ההפוכות. מה נכון?", say="ושאלה על היפוך: אל ההפוכה היא השפה של המילים ההפוכות. מה נכון?"),
    N("ניקח $L$ = מתחילה ב-$1$. ההיפוך שלה: נגמרת ב-$1$.", say="ניקח אל שווה מתחילה באחת. ההיפוך שלה: נגמרת באחת.", do=show("z-1")),
    N("מתחילה ב-$1$: התחלה, כן, ובור. שלושה. נגמרת ב-$1$: רק שניים. שתיהן רגולריות, וה-Rank שונה!",
      say="מתחילה באחת: התחלה, כן, ובור. שלושה. נגמרת באחת: רק שניים. שתיהן רגולריות, והראנק שונה!",
      do=show("z-2", "r-x-a")),
    N("וזה מפיל גם את הטענה על קבוצה מפרידה אינסופית: ה-Ranks שונים, אבל שניהם סופיים.",
      say="וזה מפיל גם את הטענה על קבוצה מפרידה אינסופית: הראנקים שונים, אבל שניהם סופיים.", do=show("r-x-b")),
    N("ואם $L$ **לא** רגולרית? אז גם $L^R$ לא רגולרית, אחרת היינו הופכים בחזרה ומקבלים ש-$L$ רגולרית.",
      say="ואם אל לא רגולרית? אז גם אל ההפוכה לא רגולרית, אחרת היינו הופכים בחזרה ומקבלים שאל רגולרית.", do=show("z-3")),
    N("שני ה-Ranks אינסופיים, ולכן שווים. התשובה: הטענה על שפה לא רגולרית.",
      say="שני הראנקים אינסופיים, ולכן שווים. התשובה: הטענה על שפה לא רגולרית.", do=show("r-ok-c", "r-x-d")),
    N("המלכודת: לחשוב שהיפוך תמיד שומר על Rank. ברגולריות לא בהכרח. ״מההתחלה״ ו״מהסוף״ שונים.",
      say="המלכודת: לחשוב שהיפוך תמיד שומר על ראנק. ברגולריות לא בהכרח. מההתחלה ומהסוף שונים.", hold=0.6),
], stage='<div id="z-1" class="h nr-big">$L=1\\Sigma^*$, &nbsp; $L^R=\\Sigma^*1$</div>'
         '<div id="z-2" class="h nr-big">$\\mathrm{Rank}=3$ &nbsp; מול &nbsp; $\\mathrm{Rank}=2$</div>'
         '<div id="z-3" class="h nr-big">לא רגולרית: $\\infty=\\infty$</div>',
   panel=f'<div class="qstem"><span class="qid">{QC["id"]}</span>$L^R$ = ההיפוך של $L$. איזו טענה נכונה?</div>'
       + st.options("r", OC))

recap = Scene("recap", "סיכום", [
    N("לסיכום: משלים שומר על Rank, תמיד.", say="לסיכום: משלים שומר על ראנק, תמיד.", do=show("r1")),
    N("איחוד וחיתוך: קטן או שווה למכפלה. אף פעם לא ״שווה״ באופן כללי.", do=show("r2")),
    N("כוכבית: אם ה-Rank של $L$ סופי, אז גם של $L^*$, לא להפך. והיפוך: שוויון **מובטח** רק כשהשפה לא רגולרית.",
      say="כוכבית: אם הראנק של אל סופי, אז גם של אל כוכבית, לא להפך. והיפוך: שוויון מובטח רק כשהשפה לא רגולרית.", do=show("r3")),
    N("ולכל טענת ״תמיד״, שלפו דוגמה נגדית: שפה ומשלימתה, שני מוני אורך, וכל המילים. נתראה ברמה הבאה.",
      do=show("r4"), hold=0.8),
], stage=TRIO.replace('id="t"', 'id="rt"').replace('id="t-', 'id="rt-').replace(' class="h"', ""),
   panel=st.card("r1", "rule", "🔑 $\\mathrm{Rank}(\\overline{L})=\\mathrm{Rank}(L)$ תמיד")
       + st.card("r2", "rule", "🔑 $\\cup,\\cap\\le$ מכפלה; לא $=$, לא $\\le\\max$")
       + st.card("r3", "trap", "⚠️ $L^*$: אם $\\mathrm{Rank}(L)$ סופי אז גם של $L^*$, לא להפך. $L^R$: שוויון מובטח רק ב-$\\infty$")
       + st.card("r4", "rule", "🔑 דוגמאות נגדיות: שפה ומשלימתה, $\\bmod3$ מול $\\bmod4$, $\\Sigma^*$"))

VIDEO = Video("N06", "nerode", "Rank של פעולות על שפות",
              [title, compl, always, trio, examA, examB, examC, recap],
              bank={"21S-B-Q8": "d", "19B-A-Q22": "c", "23A-A-Q6": "c"})
