# -*- coding: utf-8 -*-
"""N07 · Rank אינסופי וקבוצה מפרידה אינסופית — video script (build: tools/video/vid.py N07).

Source: tools/needhelp/nerode/N07.py (lesson + goal). Exam anchors: 24A-A-Q13 (CFL with finite Rank; uncited),
19B-B-Q19 (a^n b^m c^k mod 3, regular; cited) and 23A-B-Q6 (symmetric difference; uncited). Not used on purpose:
19B-A-Q12 (its options are the quiz's first question), SAMP-19-Q21 and 19B-B-Q11 (quiz).
New worked example: L = {a^n b^n}. Every separation shown is computed.
"""
import re
from nh import words, rank_stable, rank_growing, separable, is_separating_set, sep_infinite, CFG, PDA, dfa_table
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, pairs, sufftest, wd

# ---------------------------------------------------------------- worked example: a^n b^n
ANBN = lambda w: w == "a" * (len(w) // 2) + "b" * (len(w) // 2)
assert rank_growing(ANBN, "ab")
K = 4
TK = ["a" * k for k in range(K)]
for i in range(K):
    for j in range(i + 1, 8):
        assert ANBN("a" * i + "b" * i) and not ANBN("a" * j + "b" * i)      # b^i separates a^i from a^j
assert sep_infinite(ANBN, lambda k: "a" * k, ["b" * i for i in range(12)], n=10)
CELLS = {(j, i): (f"$b^{i}$" if i > 1 else "$b$") if i else "$\\varepsilon$" for j in range(1, K) for i in range(j)}
LAB = ["$\\varepsilon$", "$a$"] + [f"$a^{k}$" for k in range(2, K)]
ST, SEPS = sufftest("t1", ANBN, "aa", "aaa", ["b", "bb", "bbb"])
assert SEPS == [False, True, True]
# trap: {a^k b^k} is infinite but not separating (ab ≡ aabb ≡ ...; only ε stands apart)
TT = ["", "ab", "aabb", "aaabbb"]
assert separable(ANBN, "ab", "aabb", "ab") is None and separable(ANBN, "aabb", "aaabbb", "ab") is None
assert separable(ANBN, "", "ab", "ab") == "" or separable(ANBN, "", "ab", "ab") is not None
assert not is_separating_set(ANBN, TT, "ab")
CT = {(1, 0): "$ab$", (2, 0): "$ab$", (3, 0): "$ab$", (2, 1): "≡", (3, 1): "≡", (3, 2): "≡"}
for (i, j), v in CT.items():
    z = separable(ANBN, TT[i], TT[j], "ab")
    assert (v == "≡") == (z is None)
    if v != "≡":
        assert ANBN(TT[j] + "ab") != ANBN(TT[i] + "ab")
LABT = ["$\\varepsilon$", "$ab$", "$a^2b^2$", "$a^3b^3$"]
# trap: "for every i some suffix separates a^i from a^i b" holds for a regular language (even length)
ENDB = lambda w: w.endswith("b")
assert all(separable(ENDB, "a" * i, "a" * i + "b", "ab") == "" for i in range(8)) and rank_stable(ENDB, "ab") == 2

# ---------------------------------------------------------------- exam 19B-B-Q19: a^n b^m c^k, (n+m) mod 3 = k mod 3
QB = BANK["19B-B-Q19"]
PB = lambda w: bool(re.fullmatch("a*b*c*", w)) and (w.count("a") + w.count("b")) % 3 == w.count("c") % 3
assert QB["correctId"] == "a"
assert rank_stable(PB, "abc", 6, (4, 5, 6)) == 10
assert separable(PB, "b", "aaabbbb", "abc", 6) is None                          # option c: d=0 and d=3 equivalent
assert separable(PB, "abbccc", "aabbbbcccccc", "abc", 6) is None                # option d: d=1 and d=2 equivalent

title = Scene("title", "", [
    N("עד עכשיו ספרנו מחלקות. אבל מה קורה כשאי אפשר לגמור לספור?"),
    N("בסרטון הזה נלמד שמספר מחלקות אינסופי פירושו שפה **לא רגולרית**, ואיך מוכיחים את זה נכון.",
      hold=0.4),
], stage=CSS + '<div class="kicker">N07 · נרוד, Rank וקבוצות מפרידות</div><h1>Rank אינסופי וקבוצה מפרידה אינסופית</h1>'
         '<p>להוכיח אי-רגולריות בעזרת קבוצה מפרידה אינסופית, ולפסול אפשרויות שהן אינסופיות אבל לא מפרידות.</p>',
   layout="title")

idea = Scene("idea", "Rank אינסופי", [
    N("משפט נרוד: $L$ רגולרית אם ורק אם ה-Rank שלה סופי. אז ״Rank אינסוף״ זו פשוט דרך אחרת לכתוב ״לא רגולרית״.",
      say="משפט נרוד: אל רגולרית אם ורק אם הראנק שלה סופי. אז ראנק אינסוף זו פשוט דרך אחרת לכתוב לא רגולרית.", do=show("i-1")),
    N("וכדי להוכיח את זה, מספיק למצוא קבוצה מפרידה **אינסופית**. אינסוף מילים, כל שתיים במחלקה אחרת.",
      do=show("i-2")),
    N("**שני תנאים, שניהם**: $T$ אינסופית, **וגם** כל זוג ב-$T$ ניתן להפרדה.",
      say="שני תנאים, שניהם: טי אינסופית, וגם כל זוג בטי ניתן להפרדה.", do=show("i-rule")),
    N("קבוצה סופית לא מוכיחה כלום על אי-רגולריות. וקבוצה אינסופית שכל המילים בה באותה מחלקה, גם היא לא.",
      do=show("i-trap"), hold=0.5),
], stage='<div id="i-1" class="h nr-big" style="font-size:46px">$\\mathrm{Rank}(L)=\\infty$ אם ורק אם $L$ לא רגולרית</div>'
         '<div id="i-2" class="h nr-big">אם $T$ מפרידה ואינסופית, אז $\\mathrm{Rank}(L)=\\infty$</div>',
   panel=st.card("i-rule", "rule", "🔑 $T$ <b>אינסופית וגם</b> כל זוג ב-$T$ ניתן להפרדה")
       + st.card("i-trap", "trap", "⚠️ סופית: לא מוכיחה כלום. אינסופית עם זוג שקול: לא מפרידה."))

PG = pairs("g1", TK, CELLS, labels=LAB)
build = Scene("build", "דוגמה: aⁿbⁿ", [
    N("ניקח את $L=\\{a^nb^n\\mid n\\ge0\\}$: כמה $a$, ואחריהן אותו מספר של $b$.",
      say="ניקח את אל: אֵיי בחזקת אן, בִּי בחזקת אן. כמה אֵיי, ואחריהן אותו מספר של בִּי."),
    N("האינטואיציה: האוטומט צריך לזכור **כמה $a$ קרא**, כדי לבדוק אחר כך אותו מספר של $b$. אבל זו לא הוכחה.",
      say="האינטואיציה: האוטומט צריך לזכור כמה אֵיי קרא, כדי לבדוק אחר כך אותו מספר של בִּי. אבל זו לא הוכחה."),
    N("ההוכחה בקורס היא קבוצה מפרידה אינסופית. בואו נבנה אותה."),
    N("נבדוק את $aa$ מול $aaa$. ננסה סיפות: $b$, $bb$, $bbb$.", say="נבדוק את אֵיי אֵיי מול שלוש אֵיי. ננסה סיפות: בִּי, בִּי בִּי, שלוש בִּי.",
      do=show("t1-box", "t1-r-0")),
    N("$b$: שתיהן בחוץ. $bb$: $aabb$ בשפה, ו-$aaabb$ לא. מצאנו!",
      say="בִּי: שתיהן בחוץ. בִּי בִּי: אֵיי אֵיי בִּי בִּי בשפה, ושלוש אֵיי ושתי בִּי לא. מצאנו!",
      do=show("t1-r-1", "t1-s-1", "t1-t-1")),
    N("וזה הכלל: הסיפא ״המשלימה״ $b^i$ מפרידה בין $a^i$ לכל $a^j$ אחרת.",
      say="וזה הכלל: הסיפא המשלימה, בִּי בחזקת איי, מפרידה בין אֵיי בחזקת איי לכל אֵיי בחזקת ג'יי אחרת.", do=show("b-rule")),
    N("נמלא טבלת זוגות ל-$T=\\{a^k\\mid k\\ge0\\}$. כל תא: הסיפא $b$ בחזקת האינדקס הקטן.",
      say="נמלא טבלת זוגות לטי שווה הקבוצה אֵיי בחזקת קיי. כל תא: הסיפא בִּי בחזקת האינדקס הקטן.",
      do=hide("t1-box") + show("g1-box", "g1-c-1-0", "g1-c-2-0", "g1-c-3-0")),
    N("עמודה של $\\varepsilon$: הסיפא הריקה, כי $\\varepsilon\\in L$ ו-$a^j\\notin L$. ואחר כך $b$, ואחר כך $bb$.",
      say="עמודה של אפסילון: הסיפא הריקה, כי אפסילון בשפה ואֵיי בחזקת ג'יי לא. ואחר כך בִּי, ואחר כך בִּי בִּי.",
      do=show("g1-c-2-1", "g1-c-3-1", "g1-c-3-2", "g1-h-3-2")),
    N("והטבלה ממשיכה לנצח: כל שורה חדשה מתמלאת באותו כלל. $T$ אינסופית ומפרידה, ולכן $L$ לא רגולרית.",
      say="והטבלה ממשיכה לנצח: כל שורה חדשה מתמלאת באותו כלל. טי אינסופית ומפרידה, ולכן אל לא רגולרית.",
      do=hide("g1-h-3-2") + show("g1-more", "b-ok"), hold=0.5),
], stage='<div class="swap" style="--swap-h:600px">'
         f'<div id="t1-box" class="h">{ST}</div>'
         f'<div id="g1-box" class="h">{PG}<div id="g1-more" class="h nr-sm">⋮ &nbsp; $a^j$ מול $a^i$ ($i<j$): $z=b^i$</div>'
         '<div id="b-ok" class="h verdict ok">$\\mathrm{Rank}(L)=\\infty$</div></div></div>',
   panel='<div class="nr-big">$L=\\{a^nb^n\\mid n\\ge0\\}$</div>'
       + st.card("b-rule", "rule", "🔑 $T=\\{a^k\\}$ עם הסיפא המשלימה $b^i$: $a^ib^i\\in L$, $a^jb^i\\notin L$"))

PGT = pairs("g2", TT, CT, labels=LABT)
traps = Scene("traps", "אינסופית אבל לא מפרידה", [
    N("ועכשיו המסיח הקבוע: $\\{a^kb^k\\mid k\\ge0\\}$. היא אינסופית. אבל האם היא מפרידה?",
      say="ועכשיו המסיח הקבוע: הקבוצה אֵיי בחזקת קיי, בִּי בחזקת קיי. היא אינסופית. אבל האם היא מפרידה?", do=show("g2-box")),
    N("$ab$ מול $a^2b^2$: שתיהן בשפה, ולשתיהן כל המשך לא ריק מוציא מהשפה. אין סיפא מפרידה: שקולות.",
      say="אֵיי בִּי מול אֵיי בריבוע בִּי בריבוע: שתיהן בשפה, ולשתיהן כל המשך לא ריק מוציא מהשפה. אין סיפא מפרידה: שקולות.",
      do=show("g2-c-2-1", "g2-h-2-1")),
    N("וכך כל הזוגות שבלי $\\varepsilon$. מספיק זוג שקול אחד, והיא לא מפרידה. היא לא מוכיחה כלום.",
      say="וכך כל הזוגות שבלי אפסילון. מספיק זוג שקול אחד, והיא לא מפרידה. היא לא מוכיחה כלום.",
      do=hide("g2-h-2-1") + show("g2-c-3-1", "g2-c-3-2", "g2-c-1-0", "g2-c-2-0", "g2-c-3-0", "tr-1")),
    N("מלכודת שנייה: להראות הפרדה רק בתוך זוגות שבחרנו מראש, ולא בין **כל** שתי מילים בקבוצה.",
      do=show("tr-2")),
    N("זו לא קבוצה מפרידה. בקבוצה מפרידה בודקים כל זוג, וכל מילה מול כל מילה אחרת בה.", hold=0.5),
], stage=f'<div id="g2-box" class="h">{PGT}<div class="nr-sm">≡ = אין סיפא מפרידה</div></div>',
   panel=st.card("tr-1", "trap", "⚠️ $\\{a^kb^k\\}$: אינסופית, אבל $ab\\equiv a^2b^2$, לכן לא מפרידה")
       + st.card("tr-2", "trap", "⚠️ הפרדה רק בזוגות שנבחרו מראש אינה קבוצה מפרידה: בודקים <b>כל</b> זוג."))

QA = BANK["24A-A-Q13"]
assert QA["correctId"] == "a"
VA = {o["id"]: o["value"] for o in QA["options"]}
assert "חסרת הקשר" in VA["a"] and "שלושה מצבים מקבלים" in VA["b"] and "אוטומט-מחסנית" in VA["c"] and "כל התשובות" in VA["d"]
ASTAR = lambda w: set(w) <= {"a"}
GA = CFG("S -> aS | ε")
assert GA.lang(8) == {w for w in words("ab", 8) if ASTAR(w)} and rank_stable(ASTAR, "ab") == 2     # a CFL with Rank 2
LE2 = lambda w: len(w) <= 2
DM = dfa_table("01", {"0": "1 1", "1": "2 2", "2": "3 3", "3": "3 3"}, "0", {"0", "1", "2"}).minimize()
assert DM.lang(8) == {w for w in words("01", 8) if LE2(w)} and len(DM.states) == 4 and len(DM.acc) == 3
PEPS = PDA([], "s", {"s"})
assert PEPS.lang("ab") == {""}                                            # a PDA whose language is finite
OA = [("a", "קיימת $L$ חסרת הקשר עם $\\mathrm{Rank}(L)$ סופי"),
      ("b", "באס״ד מינימלי לא ייתכנו שלושה מצבים מקבלים"),
      ("c", "אם $L=L(M)$ לאוטומט מחסנית $M$, אז $L$ בהכרח אינסופית"),
      ("d", "כל התשובות האחרות לא נכונות")]
examA = Scene("examA", "שאלה ממבחן", [
    N("שאלה ממבחן: איזו טענה נכונה? שלוש טענות על Rank, על אס״ד מינימלי ועל אוטומט מחסנית.",
      say="שאלה ממבחן: איזו טענה נכונה? שלוש טענות על ראנק, על אסאד מינימלי ועל אוטומט מחסנית."),
    N("״קיימת שפה חסרת הקשר עם Rank סופי״. המלכודת: לחשוב ש״חסרת הקשר״ פירושו ״לא רגולרית״, כלומר Rank אינסוף.",
      say="קיימת שפה חסרת הקשר עם ראנק סופי. המלכודת: לחשוב שחסרת הקשר פירושו לא רגולרית, כלומר ראנק אינסוף.",
      do=show("ea-trap")),
    N("אבל כל שפה רגולרית היא גם חסרת הקשר. למשל $a^*$: יש לה דקדוק, ו-Rank שתיים. הטענה נכונה.",
      say="אבל כל שפה רגולרית היא גם חסרת הקשר. למשל אֵיי כוכבית: יש לה דקדוק, וראנק שתיים. הטענה נכונה.",
      do=show("ea-1", "q-ok-a")),
    N("״אין שלושה מצבים מקבלים באס״ד מינימלי״? המילים באורך שתיים לכל היותר: אורך אפס, אחת ושתיים, כולם מקבלים ושונים.",
      say="אין שלושה מצבים מקבלים באסאד מינימלי? המילים באורך שתיים לכל היותר: אורך אפס, אחת ושתיים, כולם מקבלים ושונים.",
      do=show("ea-2", "q-x-b")),
    N("ואוטומט מחסנית לא חייב לקבל שפה אינסופית: מצב אחד מקבל, בלי מעברים, מקבל רק את $\\varepsilon$.",
      say="ואוטומט מחסנית לא חייב לקבל שפה אינסופית: מצב אחד מקבל, בלי מעברים, מקבל רק את אפסילון.",
      do=show("ea-3", "q-x-c", "q-x-d"), hold=0.6),
], stage='<div id="ea-1" class="h nr-big">$a^*$: חסרת הקשר וגם רגולרית, $\\mathrm{Rank}=2$</div>'
         '<div id="ea-2" class="h nr-big">$|w|\\le2$: שלושה מצבים מקבלים ועוד בור</div>'
         '<div id="ea-3" class="h nr-big">$L(M)=\\{\\varepsilon\\}$: סופית</div>'
         + st.card("ea-trap", "trap", "⚠️ חסרת הקשר <b>אינה</b> ״לא רגולרית״: כל שפה רגולרית היא גם חסרת הקשר."),
   panel=f'<div class="qstem"><span class="qid">{QA["id"]}</span>איזו מהטענות הבאות נכונה?</div>'
       + st.options("q", OA))

QC = BANK["23A-B-Q6"]
assert QC["correctId"] == "d"
VC = {o["id"]: o["value"] for o in QC["options"]}
assert "=1" in VC["a"] and "=0" in VC["b"] and "infty" in VC["c"] and "emptyset" in VC["d"]
SD = lambda p, q: (lambda w: p(w) != q(w))
ALLW = lambda w: True
NONE = lambda w: False
assert rank_stable(SD(ALLW, NONE), "ab") == 1                              # L1 = Σ*, L2 = ∅: L = Σ*, Rank 1, L1 ≠ L2
assert rank_stable(SD(ASTAR, ASTAR), "ab") == 1 and not any(SD(ASTAR, ASTAR)(w) for w in words("ab", 6))
assert all(any(SD(p, q)(w) for w in words("ab", 6)) for p, q in [(ASTAR, ALLW), (ALLW, NONE), (ASTAR, NONE)])
OC = [("a", "$\\mathrm{Rank}(L)=1$ אם ורק אם $L_1=L_2$"), ("b", "$\\mathrm{Rank}(L)=0$ אם ורק אם $L_1=L_2$"),
      ("c", "$\\mathrm{Rank}(L)=\\infty$ אם ורק אם $L\\ne\\emptyset$"), ("d", "$L=\\emptyset$ אם ורק אם $L_1=L_2$")]
examC = Scene("examC", "שאלה שלישית: הפרש סימטרי", [
    N("ושאלה אחרונה: $L_1,L_2$ רגולריות, ו-$L$ היא ההפרש הסימטרי שלהן: המילים שנמצאות בדיוק באחת מהן.",
      say="ושאלה אחרונה: אל אחת ואל שתיים רגולריות, ואל היא ההפרש הסימטרי שלהן: המילים שנמצאות בדיוק באחת מהן."),
    N("״Rank אינסוף אם ורק אם $L$ לא ריקה״? $L$ בנויה מרגולריות בעזרת הפרש ואיחוד, אז היא רגולרית. ה-Rank שלה סופי תמיד.",
      say="ראנק אינסוף אם ורק אם אל לא ריקה? אל בנויה מרגולריות בעזרת הפרש ואיחוד, אז היא רגולרית. הראנק שלה סופי תמיד.",
      do=show("s-x-c")),
    N("״Rank אפס״? אין דבר כזה: לכל שפה יש לפחות מחלקה אחת.", say="ראנק אפס? אין דבר כזה: לכל שפה יש לפחות מחלקה אחת.",
      do=show("s-x-b")),
    N("והמלכודת: ״Rank אחת אם ורק אם השפות שוות״. כיוון אחד נכון: שפות שוות נותנות $L$ ריקה, Rank אחת.",
      say="והמלכודת: ראנק אחת אם ורק אם השפות שוות. כיוון אחד נכון: שפות שוות נותנות אל ריקה, ראנק אחת.", do=show("ec-1")),
    N("אבל הכיוון השני נופל: $L_1=\\Sigma^*$ ו-$L_2=\\emptyset$ שונות, ו-$L=\\Sigma^*$, גם היא עם Rank אחת.",
      say="אבל הכיוון השני נופל: אל אחת שווה כל המילים, ואל שתיים ריקה. הן שונות, ואל שווה כל המילים, גם היא עם ראנק אחת.",
      do=show("ec-2", "s-x-a", "ec-trap")),
    N("נשארה: $L$ ריקה אם ורק אם $L_1=L_2$. נכון בשני הכיוונים: מילה שנמצאת רק באחת היא בדיוק מילה שמבדילה ביניהן.",
      say="נשארה: אל ריקה אם ורק אם אל אחת שווה לאל שתיים. נכון בשני הכיוונים: מילה שנמצאת רק באחת היא בדיוק מילה שמבדילה ביניהן.",
      do=show("s-ok-d"), hold=0.6),
], stage='<div id="ec-1" class="h nr-big">$L_1=L_2$: &nbsp; $L=\\emptyset$, &nbsp; $\\mathrm{Rank}=1$</div>'
         '<div id="ec-2" class="h nr-big">$L_1=\\Sigma^*$, $L_2=\\emptyset$: &nbsp; $L=\\Sigma^*$, &nbsp; $\\mathrm{Rank}=1$</div>'
         + st.card("ec-trap", "trap", "⚠️ ״אם ורק אם״: בודקים <b>שני</b> כיוונים. $\\mathrm{Rank}=1$ גם ל-$\\emptyset$ וגם ל-$\\Sigma^*$."),
   panel=f'<div class="qstem"><span class="qid">{QC["id"]}</span>$L=(L_1\\setminus L_2)\\cup(L_2\\setminus L_1)$, $L_1,L_2$ רגולריות</div>'
       + st.options("s", OC))

OB = [("a", "רגולרית: יש לה ביטוי רגולרי"), ("b", "לא רגולרית: $T=\\{a,aa,aaa\\}$ מפרידה"),
      ("c", "לא רגולרית: $T=\\{a^db^{d+1}\\mid d\\ge0\\}$ מפרידה"), ("d", "לא רגולרית: $T=\\{a^db^{2d}c^{3d}\\mid d\\ge0\\}$ מפרידה")]
VB = {o["id"]: o["value"] for o in QB["options"]}
assert "ביטוי רגולרי" in VB["a"] and "aaa" in VB["b"] and "d+1" in VB["c"] and "3d" in VB["d"]
examB = Scene("examB", "עוד שאלה: מודולו", [
    N("ועוד שאלה: $a^nb^mc^k$, כאשר $n+m$ ו-$k$ שווים מודולו שלוש.",
      say="ועוד שאלה: אֵיי בחזקת אן, בִּי בחזקת אֶם, סי בחזקת קיי, כאשר אן ועוד אֶם, וקיי, שווים מודולו שלוש."),
    N("נראה מסובך, אבל מה צריך לזכור? באיזה שלב אנחנו, $a$, $b$ או $c$, ושארית מודולו שלוש. זיכרון **סופי**.",
      say="נראה מסובך, אבל מה צריך לזכור? באיזה שלב אנחנו, אֵיי, בִּי או סי, ושארית מודולו שלוש. זיכרון סופי.", do=show("eb-1")),
    N("שלושה שלבים כפול שלוש שאריות, ועוד בור: עשר מחלקות. חישבנו. השפה רגולרית.",
      do=show("eb-2", "r-ok-a")),
    N("אז כל אפשרות ״לא רגולרית״ נופלת. $\\{a,aa,aaa\\}$ סופית.", say="אז כל אפשרות לא רגולרית נופלת. אֵיי, אֵיי אֵיי, שלוש אֵיי: סופית.",
      do=show("r-x-b", "r-n-b")),
    N("ושתי הקבוצות האינסופיות חוזרות על שאריות. למשל $b$ ו-$a^3b^4$ שקולות. אינסופיות, אבל לא מפרידות.",
      say="ושתי הקבוצות האינסופיות חוזרות על שאריות. למשל בִּי, ואֵיי בשלישית בִּי ברביעית, שקולות. אינסופיות, אבל לא מפרידות.",
      do=show("r-x-c", "r-n-c", "r-x-d", "r-n-d")),
    N("זה הלקח ההפוך: ספירה **מודולו** היא זיכרון סופי. היא לא הופכת שפה ללא רגולרית.", do=show("eb-trap"), hold=0.6),
], stage='<div id="eb-1" class="h nr-big">זוכרים שלב: $a$, $b$ או $c$.<br>ועוד שארית מודולו $3$.</div>'
         '<div id="eb-2" class="h nr-big">$3\\cdot3+1=10$ מחלקות: רגולרית</div>'
         + st.card("eb-trap", "trap", "⚠️ ספירה <b>מודולו</b> = זיכרון סופי = רגולרית."),
   panel=f'<div class="qstem"><span class="qid">{QB["id"]}</span>$\\{{a^nb^mc^k\\mid(n+m)\\bmod3=k\\bmod3\\}}$</div>'
       + st.options("r", OB, notes={"b": "סופית", "c": "$b\\equiv a^3b^4$", "d": "חוזרות"}))

recap = Scene("recap", "סיכום", [
    N("לסיכום: Rank אינסוף פירושו לא רגולרית. מוכיחים בקבוצה מפרידה אינסופית.",
      say="לסיכום: ראנק אינסוף פירושו לא רגולרית. מוכיחים בקבוצה מפרידה אינסופית.", do=show("r1")),
    N("התבנית שעובדת כמעט תמיד: $a^k$, עם הסיפא המשלימה $b^k$.", say="התבנית שעובדת כמעט תמיד: אֵיי בחזקת קיי, עם הסיפא המשלימה בִּי בחזקת קיי.",
      do=show("r2")),
    N("קבוצה אינסופית שכל איבריה שקולים, כמו $a^kb^k$, לא מוכיחה כלום. וקבוצה סופית גם לא.",
      say="קבוצה אינסופית שכל איבריה שקולים, כמו אֵיי בחזקת קיי בִּי בחזקת קיי, לא מוכיחה כלום. וקבוצה סופית גם לא.", do=show("r3")),
    N("וספירה מודולו היא רגולרית. נתראה במבחן הגמר.", do=show("r4"), hold=0.8),
], stage=pairs("rg", TK, CELLS, labels=LAB).replace('class="nr-c h"', 'class="nr-c"'),
   panel=st.card("r1", "rule", "🔑 $\\mathrm{Rank}=\\infty$ אם ורק אם לא רגולרית; מוכיחים ב-$T$ אינסופית <b>ומפרידה</b>")
       + st.card("r2", "rule", "🔑 $T=\\{a^k\\}$ (או תת-קבוצה אינסופית) עם הסיפא $b^k$")
       + st.card("r3", "trap", "⚠️ אינסופית עם איברים שקולים ($a^kb^k$), או סופית: לא מוכיחה")
       + st.card("r4", "trap", "⚠️ ספירה מודולו = רגולרית"))

VIDEO = Video("N07", "nerode", "Rank אינסופי וקבוצה מפרידה אינסופית",
              [title, idea, build, traps, examA, examB, examC, recap],
              bank={"24A-A-Q13": "a", "19B-B-Q19": "a", "23A-B-Q6": "d"})
