# -*- coding: utf-8 -*-
"""K06 · סגירויות: מה נשמר ומה נשבר — video script (build: tools/video/vid.py K06).

Source: tools/needhelp/classify/K06.py (lesson + goal): the closure table, the five fixed counterexamples, the proof
method and the flipping trap. Exam anchor: 24A-A-Q15 (cited by the lesson, not by the quiz; the reverse-direction trap).
Not used on purpose: the quiz's own questions (A(L) statements, "which operation is not closed", "at least two of
three", L∪F with a finite F as a multiple choice, the L/L̄ statements). The bonus videos K06a / K06b solve the
uncited closure questions.
Closure theorems are stated as the lesson states them; every language claim below is checked with the simulators.
"""
import re
from nh import *
from vid import Scene, Video, show, hide, BANK
import stage as st
import w_closure as W
from w_closure import KP

# ---------------------------------------------------------------- verified facts
def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# (1) CFL ∩ CFL: {a^n b^n c^k} ∩ {a^k b^n c^n} = {a^n b^n c^n}
A1 = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "abc"))      # a^n b^n c^k
A2 = lambda w: (lambda t: t is not None and t[1] == t[2])(parts(w, "abc"))      # a^k b^n c^n
ABC = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(parts(w, "abc"))
assert classify_cert(A1, "abc", ("cfl", "S->TC;T->aTb|ε;C->cC|ε"), n=7) == "cfl"
assert classify_cert(A2, "abc", ("cfl", "S->AT;A->aA|ε;T->bTc|ε"), n=7) == "cfl"
assert same_pred(lambda w: A1(w) and A2(w), ABC, "abc", 8)
assert classify_cert(ABC, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7) == "noncfl"
TRY = ["aabbc", "abbcc", "aabbcc"]
MEMB = {w: (A1(w), A2(w)) for w in TRY}
assert MEMB == {"aabbc": (True, False), "abbcc": (False, True), "aabbcc": (True, True)}

# (2) CFL complement: uu is not CFL, its complement is
UU = lambda w: len(w) % 2 == 0 and w[: len(w) // 2] == w[len(w) // 2:]
assert classify_cert(UU, "ab", ("noncfl", lambda p: "a" * p + "b" * p + "a" * p + "b" * p), n=8) == "noncfl"
NUU_G = "S -> O | AB | BA ; O -> X | XXO ; A -> a | XAX ; B -> b | XBX ; X -> a | b"
assert classify_cert(lambda w: not UU(w), "ab", ("cfl", NUU_G), n=8) == "cfl"

# (3) the magic pair: L = {a^n b^n} and its complement
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab"))
assert rank_growing(ANBN, "ab") and rank_growing(lambda w: not ANBN(w), "ab")
assert rank_stable(lambda w: ANBN(w) or not ANBN(w), "ab") == 1          # Σ*
assert rank_stable(lambda w: ANBN(w) and not ANBN(w), "ab") == 1         # ∅
assert not any(ANBN(w) and not ANBN(w) for w in words("ab", 8))

PALS = lambda w: w == w[::-1]                                              # the pair shown: palindromes
assert rank_growing(PALS, "ab") and rank_growing(lambda w: not PALS(w), "ab")
SIGS = rx("(a+b)*", "ab")
assert {x + y for x in SIGS.lang(4) for y in SIGS.lang(4) if len(x + y) <= 4} == SIGS.lang(4)   # Σ*·Σ* = Σ*

# (4) a finite set does not change regularity: L ∪ F and L \ F stay non-regular (L = a^n b^n)
FIN = {"b", "ba", "aab"}
assert rank_growing(lambda w: ANBN(w) or w in FIN, "ab") and rank_growing(lambda w: ANBN(w) and w not in FIN, "ab")
assert same_pred(ANBN, lambda w: (ANBN(w) or w in FIN) and w not in (FIN - {w for w in FIN if ANBN(w)}), "ab")

# (5) exam 24A-A-Q15: D_a deletes every a
Q = BANK["24A-A-Q15"]
assert Q["correctId"] == "a"
dela = lambda z: z.replace("a", "")
ANBN3 = lambda w: (lambda t: t is not None and t[0] == t[1] and t[2] == 0)(parts(w, "abc"))    # {a^n b^n} over {a,b,c}
IMG = {dela(z) for z in words("abc", 10) if ANBN3(z)}
assert IMG == {"b" * k for k in range(6)}                                    # D_a({a^n b^n}) = b^*
assert rank_growing(ANBN3, "abc") and rx("b*", "abc").dfa().is_infinite()
R1 = rx("(a+b)*c", "abc")                                                   # a regular L: D_a gives b^*c
assert {dela(z) for z in R1.lang(8)} & set(words("abc", 6)) == rx("b*c", "abc").lang(6)
assert dela("bacab") == "bcb"

# (6) the flipping trap: an NFA for "ends with b"
N = nfa_from_edges("ab", [("0", "a", "0"), ("0", "b", "0"), ("0", "b", "1")], "0", {"1"})
assert N.lang(7) == {w for w in words("ab", 7) if w.endswith("b")}
NF = nfa_from_edges("ab", [("0", "a", "0"), ("0", "b", "0"), ("0", "b", "1")], "0", {"0"})
assert NF.lang(7) == set(words("ab", 7))                                   # flipped: accepts everything
assert N.accepts("ab") and NF.accepts("ab")                                # ab is in L and also "in the complement"
NN = {"0": "q_0", "1": "q_1"}
NPOS = {"0": (260, 170), "1": (640, 170)}
D = N.to_dfa()
assert D.complement().lang(7) == {w for w in words("ab", 7) if not w.endswith("b")}   # a DFA flips correctly

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    KP("בסרטון הזה נלמד את טבלת הסגירויות של שפות רגולריות ושל שפות חסרות הקשר."),
    KP("נלמד חמש דוגמאות נגדיות קבועות, שמפילות כמעט כל טענה שגויה."),
    KP("ובסוף נפתור שאלה אמיתית ממבחן, עם המלכודת שלה.", hold=0.4),
], stage='<div class="kicker">K06 · סיווג שפות</div><h1>סגירויות: מה נשמר ומה נשבר</h1>'
         '<p>להשתמש בטבלת הסגירויות של רגולריות וח״ה, ובדוגמאות הנגדיות הקבועות, כדי להכריע טענות על שפות שנבנות משפות אחרות.</p>',
   layout="title")

moves = Scene("moves", "שני מהלכים", [
    KP("מה זה **סגירות**? מחלקה של שפות סגורה לפעולה, אם הפעולה על שפות מהמחלקה תמיד נותנת שפה מהמחלקה.",
       do=show("mv-def")),
    KP("למשל: איחוד של שתי שפות רגולריות הוא תמיד שפה רגולרית.", do=show("mv-ex")),
    KP("כמעט כל שאלת סגירות נפתרת באחד משני מהלכים.", do=show("mv-0")),
    KP("מהלך ראשון: לכתוב את השפה החדשה כצירוף של פעולות **שכבר סגורות**. אז היא במחלקה.", do=show("mv-1")),
    KP("מהלך שני: להביא **דוגמה נגדית** קטנה. ולא ממציאים אותה מחדש: יש חמש קבועות.", do=show("mv-2")),
    KP("נתחיל בטבלה, ואחר כך נעבור על הדוגמאות הנגדיות אחת אחת.", hold=0.4),
], stage=W.STYLE + W.steps("mv", [
    ("שאלת סגירות? שני מהלכים:", "key"),
    ("<b>(1)</b> אם השפה היא צירוף של פעולות סגורות, אז היא במחלקה", "ok"),
    ("<b>(2)</b> דוגמה נגדית קטנה, מתוך <b>חמש קבועות</b>: הטענה נופלת", "bad")]),
   panel=st.card("mv-def", "rule", "<b>סגורה לפעולה</b>: הפעולה על שפות מהמחלקה נותנת <b>תמיד</b> שפה מהמחלקה")
       + st.card("mv-ex", "ex", "אם $L_1,L_2$ רגולריות, אז $L_1\\cup L_2$ רגולרית"))

ROWS = [("איחוד $L_1\\cup L_2$", True, True), ("שרשור $L_1L_2$", True, True), ("כוכבית $L^*$", True, True),
        ("היפוך $L^R$", True, True), ("חיתוך <b>עם רגולרית</b>", True, True),
        ("חיתוך של שתיים $L_1\\cap L_2$", True, False), ("משלים $\\overline{L}$", True, False)]


def row(i, *cols):
    return show(*[f"tb-m-{i}-{c}" for c in cols])


table = Scene("table", "טבלת הסגירויות", [
    KP("הנה הטבלה. בכל שורה פעולה, ובעמודות: האם הרגולריות סגורות לה, והאם חסרות ההקשר סגורות לה."),
    KP("איחוד: שתי המחלקות סגורות.", do=show("tb-hl-0") + row(0, "r", "c")),
    KP("שרשור: שתיהן סגורות.", do=hide("tb-hl-0") + show("tb-hl-1") + row(1, "r", "c")),
    KP("כוכבית: שתיהן סגורות.", do=hide("tb-hl-1") + show("tb-hl-2") + row(2, "r", "c")),
    KP("היפוך, כלומר לקרוא כל מילה מהסוף להתחלה: שתיהן סגורות.", do=hide("tb-hl-2") + show("tb-hl-3") + row(3, "r", "c")),
    KP("חיתוך **עם שפה רגולרית**: גם כאן שתיהן סגורות. שפה חסרת הקשר, חיתוך רגולרית, נשארת חסרת הקשר.",
       do=hide("tb-hl-3") + show("tb-hl-4") + row(4, "r", "c")),
    KP("ועכשיו שתי השורות שבהן הכול קורה.", do=hide("tb-hl-4")),
    KP("חיתוך של **שתי** שפות: הרגולריות סגורות. חסרות ההקשר **לא סגורות**.",
       do=show("tb-hl-5") + row(5, "r", "c")),
    KP("משלים: הרגולריות סגורות. חסרות ההקשר **לא סגורות**.", do=hide("tb-hl-5") + show("tb-hl-6") + row(6, "r", "c")),
    KP("כלומר, הרגולריות סגורות לכל הפעולות בטבלה. אצל חסרות ההקשר יש בדיוק שני חורים.",
       do=hide("tb-hl-6") + show("tb-r1")),
    KP("שימו לב להבדל בין שתי שורות החיתוך: עם **רגולרית** זה בטוח. עם **חסרת הקשר** אחרת, לא.",
       do=show("tb-r2", "tb-hl-4", "tb-hl-5"), hold=0.5),
    KP("ומה פירוש \"לא סגורות\"? לא שהתוצאה תמיד מחוץ למחלקה. רק שיש **לפחות דוגמה אחת** שבה היא יוצאת ממנה.",
       say="ומה פירוש לא סגורות? לא שהתוצאה תמיד מחוץ למחלקה. רק שיש לפחות דוגמה אחת שבה היא יוצאת ממנה.",
       do=hide("tb-hl-4", "tb-hl-5") + show("tb-r3"), hold=0.5),
], stage=W.STYLE + W.closure_table("tb", ROWS),
   panel=st.card("tb-r1", "rule", "🔑 רגולריות: סגורות <b>לכל</b> הפעולות בטבלה")
       + st.card("tb-r2", "trap", "⚠️ ח״ה: חיתוך <b>עם רגולרית</b> כן, חיתוך של <b>שתי ח״ה</b> לא")
       + st.card("tb-r3", "plain", "<b>לא סגורות</b> = קיימת <b>דוגמה אחת</b> שיוצאת מהמחלקה, לא \"תמיד יוצאת\""))

CAP_ROWS = "".join(
    f'<tr><td class="op" style="direction:ltr;text-align:center">${w}$</td>'
    + "".join(f'<td class="mk"><span id="ci-m-{w}-{k}" class="{"yes" if ok else "no"} h">{"✓" if ok else "✗"}</span></td>'
              for k, ok in (("1", MEMB[w][0]), ("2", MEMB[w][1]), ("3", all(MEMB[w]))))
    + "</tr>" for w in TRY)
CAP_TAB = ('<table class="clo-tab" id="ci-tab"><thead><tr><th>מילה</th><th>$L_1$</th><th>$L_2$</th>'
           '<th>$L_1\\cap L_2$</th></tr></thead><tbody>' + CAP_ROWS + "</tbody></table>")

cfl_cap = Scene("cap", "דוגמה נגדית 1: חיתוך", [
    KP("דוגמה נגדית ראשונה: חיתוך של שתי שפות חסרות הקשר."),
    KP("$L_1$: מספר ה-$a$ שווה למספר ה-$b$, ומספר ה-$c$ חופשי. יש לה דקדוק, ולכן היא חסרת הקשר.",
       say="אֵל אחת: מספר האֵיי שווה למספר הבִּי, ומספר הסִי חופשי. יש לה דקדוק, ולכן היא חסרת הקשר.",
       do=show("ci-l1")),
    KP("$L_2$: מספר ה-$b$ שווה למספר ה-$c$, ומספר ה-$a$ חופשי. גם לה יש דקדוק.",
       say="אֵל שתיים: מספר הבִּי שווה למספר הסִי, ומספר האֵיי חופשי. גם לה יש דקדוק.",
       do=show("ci-l2")),
    KP("נבדוק כמה מילים. $aabbc$ ב-$L_1$, אבל לא ב-$L_2$: שתי $b$ ו-$c$ אחת.",
       say="נבדוק כמה מילים. אֵיי אֵיי בִּי בִּי סִי באֵל אחת, אבל לא באֵל שתיים: שתי בִּי וסִי אחת.",
       do=show("ci-m-aabbc-1", "ci-m-aabbc-2", "ci-m-aabbc-3")),
    KP("$abbcc$ ב-$L_2$, אבל לא ב-$L_1$.", say="אֵיי בִּי בִּי סִי סִי באֵל שתיים, אבל לא באֵל אחת.",
       do=show("ci-m-abbcc-1", "ci-m-abbcc-2", "ci-m-abbcc-3")),
    KP("ו-$aabbcc$ בשתיהן. כדי להיות בחיתוך, מילה צריכה לקיים את **שני** השוויונות.",
       say="ואֵיי אֵיי בִּי בִּי סִי סִי בשתיהן. כדי להיות בחיתוך, מילה צריכה לקיים את שני השוויונות.",
       do=show("ci-m-aabbcc-1", "ci-m-aabbcc-2", "ci-m-aabbcc-3")),
    KP("לכן החיתוך הוא $\\{a^nb^nc^n\\}$: שלושה מונים שווים. לפי טבלת השפות הידועות, היא לא חסרת הקשר.",
       say="לכן החיתוך הוא אֵיי בחזקת אֵן, בִּי בחזקת אֵן, סִי בחזקת אֵן: שלושה מונים שווים. לפי טבלת השפות הידועות, היא לא חסרת הקשר.",
       do=show("ci-res")),
    KP("שתי שפות חסרות הקשר, והחיתוך שלהן לא. זו הדוגמה שמראה שחיתוך לא סגור.", do=show("ci-rule"), hold=0.5),
], stage=W.STYLE + '<div class="clo-big">'
         '<div id="ci-l1" class="h">$L_1=\\{a^nb^nc^k\\}$</div><div id="ci-l2" class="h">$L_2=\\{a^kb^nc^n\\}$</div></div>'
         + CAP_TAB
         + '<div id="ci-res" class="clo-big h">$L_1\\cap L_2=\\{a^nb^nc^n\\}$</div>',
   panel=st.card("ci-rule", "rule", "🔑 $\\{a^nb^nc^k\\}\\cap\\{a^kb^nc^n\\}=\\{a^nb^nc^n\\}$<br>"
                 "שתיהן ח״ה, החיתוך לא. לכן ח״ה <b>לא סגורות לחיתוך</b>"))

comp = Scene("comp", "דוגמה נגדית 2: משלים", [
    KP("דוגמה נגדית שנייה: משלים של שפה חסרת הקשר."),
    KP("$uu$ היא שפת המילים שבנויות משני עותקים זהים של אותה מילה. לפי טבלת השפות הידועות, היא לא חסרת הקשר.",
       say="יו יו היא שפת המילים שבנויות משני עותקים זהים של אותה מילה. לפי טבלת השפות הידועות, היא לא חסרת הקשר.",
       do=show("cp-uu")),
    KP("אבל המשלים שלה, $\\overline{uu}$, כן חסרת הקשר. אותה טבלה.",
       say="אבל המשלים שלה, המשלים של יו יו, כן חסרת הקשר. אותה טבלה.",
       do=show("cp-nuu")),
    KP("אז הנה שפה חסרת הקשר, $\\overline{uu}$, שהמשלים שלה, $uu$, אינו חסר הקשר.",
       do=show("cp-arrow")),
    KP("ולכן חסרות ההקשר לא סגורות למשלים.", do=show("cp-rule")),
    KP("ויש גם קשר בין שני החורים: איחוד הוא סגור. אילו גם משלים היה סגור, אז החיתוך, שהוא משלים של איחוד משלימים, היה סגור.",
       do=show("cp-dm")),
    KP("החיתוך לא סגור, אז גם המשלים לא יכול להיות סגור.", hold=0.5),
], stage=W.STYLE + '<div class="clo-big">'
         '<div id="cp-nuu" class="h">$\\overline{uu}$ &nbsp; ✓ ח״ה</div>'
         '<div id="cp-arrow" class="clo-heb h">והמשלים שלה:</div>'
         '<div id="cp-uu" class="h">$uu=\\{uu\\mid u\\in\\{a,b\\}^*\\}$ &nbsp; ✗ לא ח״ה</div></div>'
         + '<div id="cp-dm" class="clo-big h">$L_1\\cap L_2=\\overline{\\overline{L_1}\\cup\\overline{L_2}}$</div>',
   panel=st.card("cp-rule", "rule", "🔑 $\\overline{uu}$ ח״ה, ו-$uu$ לא. לכן ח״ה <b>לא סגורות למשלים</b>"))

magic = Scene("magic", "דוגמה נגדית 3–5", [
    KP("דוגמה נגדית שלישית: **הזוג הקסום**. ניקח שפה לא רגולרית, למשל הפלינדרומים, ואת המשלים שלה.",
       do=show("mg-pair")),
    KP("גם המשלים לא רגולרי: אילו היה רגולרי, גם המשלים שלו, כלומר $L$ עצמה, הייתה רגולרית.",
       say="גם המשלים לא רגולרי: אילו היה רגולרי, גם המשלים שלו, כלומר אֵל עצמה, הייתה רגולרית."),
    KP("כל מילה נמצאת בדיוק באחת משתיהן. לכן האיחוד שלהן הוא $\\Sigma^*$, כל המילים.", do=show("mg-u")),
    KP("והחיתוך שלהן ריק: $\\emptyset$.", do=hide("mg-u") + show("mg-i")),
    KP("$\\Sigma^*$ ו-$\\emptyset$ שתיהן רגולריות. כלומר: צירוף של שתי לא רגולריות **יכול** לצאת רגולרי.",
       do=hide("mg-i") + show("mg-rule")),
    KP("דוגמה נגדית רביעית: $\\Sigma^*$ לבדה, שפת כל המילים. היא מפילה טענות חזקות מדי על \"כל מילה\" או \"תמיד משתנה\".",
       say="דוגמה נגדית רביעית: סיגמא כוכבית לבדה, שפת כל המילים. היא מפילה טענות חזקות מדי על כל מילה, או על תמיד משתנה.",
       do=show("mg-sig")),
    KP("למשל הטענה \"שרשור של שפה עם עצמה תמיד נותן שפה אחרת\": $\\Sigma^*\\cdot\\Sigma^*=\\Sigma^*$.",
       say="למשל הטענה: שרשור של שפה עם עצמה תמיד נותן שפה אחרת. אבל סיגמא כוכבית כפול סיגמא כוכבית שווה סיגמא כוכבית."),
    KP("דוגמה חמישית: **מספר סופי של מילים**. קבוצה סופית היא רגולרית, ולכן הוספה או הסרה שלה לא משנה רגולריות.",
       do=show("mg-fin")),
    KP("למה? אילו $L\\cup F$ הייתה רגולרית, אז $L$ שווה ל-$L\\cup F$ פחות $F$, והייתה רגולרית.",
       say="למה? אילו אֵל איחוד אֶף הייתה רגולרית, אז אֵל שווה לאֵל איחוד אֶף פחות אֶף, והייתה רגולרית.",
       do=show("mg-fin2")),
    KP("כאן ההנחה היא ש-$F$ זרה ל-$L$. ובמקרה הכללי מחזירים את המילים של $F$ ששייכות ל-$L$: גם הן קבוצה סופית.",
       say="כאן ההנחה היא שאֶף זרה לאֵל. ובמקרה הכללי מחזירים את המילים של אֶף ששייכות לאֵל: גם הן קבוצה סופית.",
       hold=0.5),
], stage=W.STYLE + '<div id="mg-pair" class="clo-big h">$L=\\{w\\mid w=w^R\\}$ &nbsp; , &nbsp; $\\overline{L}$</div>'
         + W.sigma_box("mg") + '<div id="mg-fin2" class="clo-big h">$L=(L\\cup F)\\setminus F$</div>',
   panel=st.card("mg-rule", "rule", "🔑 <b>הזוג הקסום</b>: $L$ לא רגולרית ו-$\\overline{L}$. איחוד $\\Sigma^*$, חיתוך $\\emptyset$")
       + st.card("mg-sig", "ex", "$\\Sigma^*$ מפילה טענות חזקות מדי: $\\Sigma^*\\cdot\\Sigma^*=\\Sigma^*$")
       + st.card("mg-fin", "rule", "🔑 הוספה או הסרה של <b>מספר סופי</b> של מילים לא משנה רגולריות"))

QOPTS = {o["id"]: o for o in Q["options"]}
method = Scene("method", "שיטת ההוכחה", [
    KP("איך מוכיחים ששפה $X$ **לא** רגולרית בעזרת סגירות? בשלילה.", do=show("me-0")),
    KP("נניח ש-$X$ רגולרית. אז $L$ שווה ל-$X$ בפעולה סגורה עם שפה רגולרית $R$, ולכן גם $L$ רגולרית.",
       do=show("me-1")),
    KP("אבל אנחנו יודעים ש-$L$ לא רגולרית. סתירה, ולכן $X$ לא רגולרית.", do=show("me-2")),
    KP("זה בדיוק מה שעשינו עכשיו עם $L\\cup F$.",
       say="זה בדיוק מה שעשינו עכשיו עם אֵל איחוד אֶף."),
    KP("ומה עם הכיוון ההפוך: \"אם $f(L)$ רגולרית, אז $L$ רגולרית\"? כמעט תמיד מפריכים אותו.",
       say="ומה עם הכיוון ההפוך: אם אֶף של אֵל רגולרית, אז אֵל רגולרית? כמעט תמיד מפריכים אותו.",
       do=show("me-3")),
    KP("הכלי: $\\{a^nb^n\\}$, ופעולה $f$ שמוחקת לה את המבנה. זה בדיוק מה שנראה עכשיו בשאלה ממבחן.",
       say="הכלי: אֵיי בחזקת אֵן, בִּי בחזקת אֵן, ופעולה אֶף שמוחקת לה את המבנה. זה בדיוק מה שנראה עכשיו בשאלה ממבחן.",
       do=show("me-4"), hold=0.5),
], stage=W.STYLE + W.steps("me", [
    ("נניח בשלילה ש-$X$ רגולרית", ""),
    ("אז $L=X\\ \\mathrm{op}\\ R$ עם $R$ רגולרית, ולכן $L$ רגולרית", ""),
    ("אבל $L$ לא רגולרית: <b>סתירה</b>. לכן $X$ לא רגולרית", "ok"),
    ("הכיוון ההפוך: \"אם $f(L)$ רגולרית, אז $L$ רגולרית\"", "bad"),
    ("מפריכים עם $L=\\{a^nb^n\\}$, ש-$f$ מוחקת לה את המבנה", "key")]))

exam = Scene("exam", "שאלה ממבחן", [
    KP("השאלה: $D_a$ מוחקת מכל מילה את כל ה-$a$. למשל, מ-$bacab$ נשאר $bcb$.",
       say="השאלה: דֵי אֵיי מוחקת מכל מילה את כל האֵיי. למשל, מבִּי אֵיי סִי אֵיי בִּי נשאר בִּי סִי בִּי.",
       do=show("ex-del")),
    KP("כיוון ראשון: אם $L$ רגולרית, האם $D_a(L)$ רגולרית?",
       say="כיוון ראשון: אם אֵל רגולרית, האם דֵי אֵיי של אֵל רגולרית?", do=show("q-o-a")),
    KP("כן. לוקחים ביטוי רגולרי של $L$, ומחליפים בו כל $a$ ב-$\\varepsilon$. מקבלים ביטוי רגולרי של $D_a(L)$.",
       say="כן. לוקחים ביטוי רגולרי של אֵל, ומחליפים בו כל אֵיי באפסילון. מקבלים ביטוי רגולרי של דֵי אֵיי של אֵל.",
       do=show("ex-rx")),
    KP("למשל, $(a+b)^*c$ הופך ל-$b^*c$.", say="למשל, אֵיי או בִּי, בכוכבית, סִי, הופך לבִּי כוכבית סִי.",
       do=show("q-ok-a")),
    KP("כיוון שני: אם $D_a(L)$ רגולרית, האם $L$ רגולרית? זו המלכודת. זה נשמע סימטרי, וזה לא.",
       say="כיוון שני: אם דֵי אֵיי של אֵל רגולרית, האם אֵל רגולרית? זו המלכודת. זה נשמע סימטרי, וזה לא.",
       do=show("ex-trap")),
    KP("ניקח $L=\\{a^nb^n\\}$, שאינה רגולרית. מוחקים את כל ה-$a$ ונשארים רק $b$-ים, בכל מספר.",
       say="ניקח אֵל שווה אֵיי בחזקת אֵן, בִּי בחזקת אֵן, שאינה רגולרית. מוחקים את כל האֵיי ונשארים רק בִּי, בכל מספר.",
       do=hide("ex-rx") + show("ex-ce")),
    KP("כלומר $D_a(L)=b^*$, שפה רגולרית. ה-$a$ שנמחקו לקחו איתם את הספירה.",
       say="כלומר דֵי אֵיי של אֵל שווה בִּי כוכבית, שפה רגולרית. האֵיי שנמחקו לקחו איתם את הספירה.",
       do=show("q-x-b", "q-n-b")),
    KP("לכן הכיוון השני לא נכון, וגם התשובה ששתיהן נכונות נופלת.", do=show("q-x-c", "q-n-c")),
    KP("והתשובה \"אף אחת\" נופלת, כי הכיוון הראשון נכון. התשובה: אם $L$ רגולרית, $D_a(L)$ רגולרית.",
       say="והתשובה אף אחת נופלת, כי הכיוון הראשון נכון. התשובה: אם אֵל רגולרית, דֵי אֵיי של אֵל רגולרית.",
       do=show("q-x-d", "q-n-d"), hold=0.6),
], stage=W.STYLE + '<div id="ex-del" class="clo-big h">$del_a(bacab)=bcb$</div>'
         + '<div class="swap" style="--swap-h:150px">'
         + '<div id="ex-rx" class="h"><div class="clo-big">$(a+b)^*c\\ \\longrightarrow\\ (\\varepsilon+b)^*c=b^*c$</div></div>'
         + '<div id="ex-ce" class="h"><div class="clo-big">$D_a(\\{a^nb^n\\})=\\{b^n\\}=b^*$</div></div></div>'
         + '<div id="ex-trap" class="h">' + st.card("ex-trapc", "trap", "⚠️ <b>הכיוון ההפוך</b>: $D_a(L)$ רגולרית לא אומר כלום על $L$. "
                                                  "המחיקה מוחקת גם את הספירה.").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q, "q", notes={"b": "$\\{a^nb^n\\}\\to b^*$", "c": "הכיוון ההפוך נופל", "d": "הכיוון הראשון נכון"}))

flip = Scene("flip", "מלכודת: הפיכת מצבים", [
    KP("מלכודת אחרונה. ברגולריות, משלים בונים בהפיכת המצבים המקבלים. אבל זה עובד **רק באס״ד**, שהוא שלם."),
    KP("הנה אסל״ד לשפת המילים שמסתיימות ב-$b$.", say="הנה אסלאד לשפת המילים שמסתיימות בבִּי.", do=show("fl-hs-1")),
    KP("נהפוך את המצבים: $q_0$ יהיה מקבל, ו-$q_1$ לא.", do=hide("fl-hs-1") + show("fl2-box", "fl-arrow")),
    KP("עכשיו $q_0$ מקבל, ותמיד יש ריצה שנשארת בו. אז האוטומט החדש מקבל **כל** מילה.",
       do=show("fl2-hs-0")),
    KP("למשל $ab$: היא מסתיימת ב-$b$, כלומר ב-$L$, ובכל זאת האוטומט ההפוך מקבל אותה. זה לא המשלים.",
       say="למשל אֵיי בִּי: היא מסתיימת בבִּי, כלומר באֵל, ובכל זאת האוטומט ההפוך מקבל אותה. זה לא המשלים.",
       do=show("fl-trap")),
    KP("באסל״ד מספיקה ריצה מקבלת אחת. לכן הפיכה שם לא נותנת משלים. וכך גם באוטומט מחסנית.",
       do=show("fl-rule")),
    KP("ועוד דבר: שפה שמקיימת את למת הניפוח היא לא בהכרח רגולרית. הלמה מפריכה, היא לא מוכיחה סגירות.",
       do=show("fl-lem"), hold=0.5),
], stage=st.dfa_svg("fl", N, NPOS, NN, w=900, h=260, scale=1.0)
         + '<div id="fl-arrow" class="hint h">אחרי הפיכה:</div>'
         + '<div id="fl2-box" class="h">' + st.dfa_svg("fl2", NF, NPOS, NN, w=900, h=260, scale=1.0) + "</div>",
   panel=st.card("fl-trap", "trap", "⚠️ $ab\\in L$, והאוטומט ההפוך מקבל אותה: <b>זה לא המשלים</b>")
       + st.card("fl-rule", "rule", "🔑 הפיכת מצבים מקבלים = משלים <b>רק באס״ד</b> שלם. לא באסל״ד, לא באוטומט מחסנית")
       + st.card("fl-lem", "plain", "שפה שמקיימת את הלמה <b>לא בהכרח</b> רגולרית"))

recap = Scene("recap", "סיכום", [
    KP("לסיכום: שאלת סגירות פותרים בצירוף של פעולות סגורות, או בדוגמה נגדית קבועה.", do=show("c1")),
    KP("הרגולריות סגורות לכל הפעולות. חסרות ההקשר: לא לחיתוך של שתיים, ולא למשלים. עם רגולרית, כן.", do=show("c2")),
    KP("הדוגמאות: $\\{a^nb^nc^n\\}$ כחיתוך, $uu$ ומשלימה, הזוג הקסום, $\\Sigma^*$, וקבוצה סופית.",
       say="הדוגמאות: אֵיי בִּי סִי בחזקת אֵן כחיתוך, יו יו ומשלימה, הזוג הקסום, סיגמא כוכבית, וקבוצה סופית.",
       do=show("c3")),
    KP("והכיוון ההפוך, \"אם $f(L)$ רגולרית אז $L$\", נופל עם $\\{a^nb^n\\}$. בסרטוני הבונוס נפתור עוד הרבה שאלות כאלה.",
       say="והכיוון ההפוך, אם אֶף של אֵל רגולרית אז אֵל, נופל עם אֵיי בחזקת אֵן, בִּי בחזקת אֵן. בסרטוני הבונוס נפתור עוד הרבה שאלות כאלה.",
       do=show("c4"), hold=0.8),
], stage=W.STYLE + W.closure_table("rt", ROWS),
   panel=st.card("c1", "rule", "🔑 צירוף של פעולות סגורות, או דוגמה נגדית קבועה")
       + st.card("c2", "rule", "🔑 ח״ה: <b>לא</b> חיתוך של שתיים, <b>לא</b> משלים; חיתוך עם רגולרית כן")
       + st.card("c3", "rule", "🔑 $\\{a^nb^nc^n\\}$ · $uu$ / $\\overline{uu}$ · $L,\\overline{L}$ · $\\Sigma^*$ · קבוצה סופית")
       + st.card("c4", "trap", "⚠️ \"אם $f(L)$ רגולרית, אז $L$ רגולרית\" נופל עם $\\{a^nb^n\\}$"))
recap.phrases[0].do += show(*[f"rt-m-{i}-{c}" for i in range(len(ROWS)) for c in "rc"])

VIDEO = Video("K06", "classify", "סגירויות: מה נשמר ומה נשבר",
              [title, moves, table, cfl_cap, comp, magic, method, exam, flip, recap],
              bank={"24A-A-Q15": "a"})
