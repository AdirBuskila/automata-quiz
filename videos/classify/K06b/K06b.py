# -*- coding: utf-8 -*-
"""K06b · (בונוס) סגירות של שפות חסרות הקשר — video script (build: tools/video/vid.py K06b).

Bonus video of level K06 (tools/needhelp/classify/K06.py: closure table + fixed counterexamples + proof method).
Exam questions: five cfl_props questions that no level cites (design doc list):
  24X-C-Q10 (L ∩ a*b*), 21S-A-Q15 (L1 \\ L2: which is NOT true), 23A-A-Q15 (zero(w), both directions),
  24A-B-Q6 (w#w: copying is not a closure operation), 23A-A-Q19 (intersection of two non-CFLs).
Closure theorems are stated as the K06 lesson (and the bank explanations) state them; every concrete language
claim is checked below. Classifications follow the formula-sheet table of known languages (CLAUDE.md).
"""
import re
from nh import *
from vid import Scene, Video, show, hide, BANK
import stage as st
import w_closure as W
from w_closure import KP


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# ---------------------------------------------------------------- verified facts
# 24X-C-Q10: A(L) = L ∩ a*b*
Q1 = BANK["24X-C-Q10"]
assert Q1["correctId"] == "a" and Q1.get("lockOrder")
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab"))
AB = rx("a*b*", "ab")
assert all((ANBN(w) and AB.accepts(w)) == ANBN(w) for w in words("ab", 9))      # A({a^n b^n}) = {a^n b^n}
assert classify_cert(ANBN, "ab", ("cfl", "S -> aSb | ε")) == "cfl"               # CFL, not regular

# 21S-A-Q15: Σ* \ complement(uu) = uu
Q2 = BANK["21S-A-Q15"]
assert Q2["correctId"] == "a"
UU = lambda w: len(w) % 2 == 0 and w[: len(w) // 2] == w[len(w) // 2:]
NUU_G = "S -> O | AB | BA ; O -> X | XXO ; A -> a | XAX ; B -> b | XBX ; X -> a | b"
NUU = lambda w: not UU(w)
assert classify_cert(NUU, "ab", ("cfl", NUU_G), n=8) == "cfl"
assert all((True and not NUU(w)) == UU(w) for w in words("ab", 9))              # Σ* \ L2 = uu
assert classify_cert(UU, "ab", ("noncfl", lambda p: "a" * p + "b" * p + "a" * p + "b" * p), n=8) == "noncfl"

# 23A-A-Q15: zero(w) keeps only the 0s
Q3 = BANK["23A-A-Q15"]
assert Q3["correctId"] == "c"
zero = lambda w: "0" * w.count("0")
assert zero("0010") == "000" and zero("1111") == ""
G = CFG("S -> 0S0 | 1")                               # an example CFL: 0^n 1 0^n
G0 = CFG("S -> 0S0 | ε")                              # the same grammar with every 1 replaced by ε
assert {zero(w) for w in G.lang(11)} == G0.lang(10)
L010 = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2] >= 1)(parts(w, "010"))
assert classify_cert(L010, "01", ("noncfl", lambda p: "0" * p + "1" * p + "0" * p), n=9) == "noncfl"
assert {zero(w) for w in words("01", 12) if L010(w)} == {"0" * (2 * n) for n in range(1, 5)}     # Z(L) = (00)^+
assert rx("00(00)*", "01").dfa().is_infinite()

# 24A-B-Q6: Z(L) = { w#w | w in L }
Q4 = BANK["24A-B-Q6"]
assert Q4["correctId"] == "b"
def copy_of(member):
    def pred(s):
        if s.count("#") != 1:
            return False
        a, b = s.split("#")
        return a == b and member(a)
    return pred
ONES = copy_of(lambda w: set(w) <= {"1"})                 # L = 1^* (regular)
assert rank_growing(ONES, "1#")                            # {1^n # 1^n}: not regular
PAL = copy_of(lambda w: w == w[::-1])                       # L = palindromes (CFL)
for p in (2, 3):
    u = "0" * p + "1" * p + "0" * p
    assert pump_breaks_cf(PAL, u + "#" + u, p, ipow=range(0, 3))

# 23A-A-Q19: two non-CFLs
Q5 = BANK["23A-A-Q19"]
assert Q5["correctId"] == "d"
SQ = lambda w: set(w) <= {"a"} and int(len(w) ** .5) ** 2 == len(w)
assert all(pump_breaks_cf(SQ, "a" * (p * p), p) for p in (2, 3, 4))          # a^{n^2}: not CFL
assert rank_growing(lambda w: not SQ(w), "a")                                   # its complement: not regular
assert not any(SQ(w) and not SQ(w) for w in words("a", 30))                     # the intersection is ∅

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    KP("סרטון בונוס לרמת הסגירויות: הפעם שפות חסרות הקשר."),
    KP("כאן יש בטבלה שני חורים, ושם נמצאות כמעט כל המלכודות. נפתור חמש שאלות אמיתיות ממבחנים.", hold=0.4),
], stage='<div class="kicker">K06b · סיווג שפות · בונוס</div><h1>סגירות של שפות חסרות הקשר</h1>'
         '<p>חמש שאלות מבחן על סגירות של שפות חסרות הקשר, עם המלכודת של כל אחת.</p>',
   layout="title")

CFL_ROWS = [("איחוד, שרשור, כוכבית, היפוך", True, True), ("חיתוך <b>עם רגולרית</b>", True, True),
            ("חיתוך של שתי ח״ה", True, False), ("משלים", True, False)]
tools = Scene("tools", "ארגז הכלים", [
    KP("נזכיר את עמודת חסרות ההקשר בטבלה. איחוד, שרשור, כוכבית והיפוך: סגורות.", do=show("tb-m-0-r", "tb-m-0-c")),
    KP("חיתוך עם רגולרית: סגורות. זה הכלי הכי חשוב בסרטון הזה.", do=show("tb-m-1-r", "tb-m-1-c", "tb-hl-1")),
    KP("חיתוך של שתי חסרות הקשר, ומשלים: **לא** סגורות.", do=hide("tb-hl-1") + show("tb-m-2-r", "tb-m-2-c", "tb-m-3-r", "tb-m-3-c")),
    KP("מזה יוצא כלל להפרש: $L\\setminus R$ הוא $L$ חיתוך המשלים של $R$. אם $R$ רגולרית, גם המשלים שלה רגולרי, אז זה סגור.",
       say="מזה יוצא כלל להפרש: אֵל פחות אָר הוא אֵל חיתוך המשלים של אָר. אם אָר רגולרית, גם המשלים שלה רגולרי, אז זה סגור.",
       do=show("tk-1")),
    KP("אבל הפרש של **שתי** חסרות הקשר, כבר לא בטוח.", do=show("tk-2")),
    KP("וכדי להוכיח ששפה $X$ **לא** חסרת הקשר: אילו הייתה, גם $X$ חיתוך רגולרית הייתה. מספיק למצוא חיתוך כזה שאינו חסר הקשר.",
       say="וכדי להוכיח ששפה אִקְס לא חסרת הקשר: אילו הייתה, גם אִקְס חיתוך רגולרית הייתה. מספיק למצוא חיתוך כזה שאינו חסר הקשר.",
       do=show("tk-3"), hold=0.5),
], stage=W.STYLE + W.closure_table("tb", CFL_ROWS),
   panel=st.card("tk-1", "rule", "🔑 $L\\setminus R=L\\cap\\overline{R}$: ח״ה פחות <b>רגולרית</b> = ח״ה")
       + st.card("tk-2", "trap", "⚠️ ח״ה פחות <b>ח״ה</b>: לא סגור")
       + st.card("tk-3", "rule", "🔑 <b>לא ח״ה?</b> אם $X\\cap R$ לא ח״ה, אז $X$ לא ח״ה"))

q1 = Scene("q1", "שאלה 1: חיתוך עם a*b*", [
    KP("שאלה ראשונה. $A(L)$ היא המילים של $L$ שהן מהצורה $a^*b^*$.",
       say="שאלה ראשונה. אֵיי של אֵל היא המילים של אֵל שהן מהצורה אֵיי כוכבית בִּי כוכבית.", do=show("q1-def")),
    KP("כלומר $A(L)$ היא $L$ חיתוך $a^*b^*$, ו-$a^*b^*$ רגולרית.",
       say="כלומר אֵיי של אֵל היא אֵל חיתוך אֵיי כוכבית בִּי כוכבית, ואֵיי כוכבית בִּי כוכבית רגולרית.", do=show("q1-f")),
    KP("חסרת הקשר חיתוך רגולרית היא חסרת הקשר, ולא בהכרח רגולרית. אז הטענה הראשונה נכונה.", do=show("qa-ok-a")),
    KP("והמלכודת: \"חתכנו עם רגולרית, אז יצא רגולרי\". זה לא מה שהטבלה אומרת: התוצאה **חסרת הקשר**, לא יותר.",
       say="והמלכודת: חתכנו עם רגולרית, אז יצא רגולרי. זה לא מה שהטבלה אומרת: התוצאה חסרת הקשר, לא יותר.",
       do=show("q1-trap")),
    KP("דוגמה נגדית: $L=\\{a^nb^n\\}$. כל המילים שלה כבר מהצורה $a^*b^*$, ולכן $A(L)=L$, שאינה רגולרית.",
       say="דוגמה נגדית: אֵל שווה אֵיי בחזקת אֵן, בִּי בחזקת אֵן. כל המילים שלה כבר מהצורה אֵיי כוכבית בִּי כוכבית, ולכן אֵיי של אֵל שווה אֵל, שאינה רגולרית.",
       do=show("q1-ce", "qa-x-b", "qa-n-b")),
    KP("אז רק הראשונה נכונה, והתשובות \"שתיהן\" ו\"אף אחת\" נופלות.",
       say="אז רק הראשונה נכונה, והתשובות שתיהן ואף אחת נופלות.",
       do=show("qa-x-c", "qa-x-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big">'
         '<div id="q1-def" class="h">$A(L)=\\{w\\mid w\\in L\\ \\wedge\\ w\\in a^*b^*\\}$</div>'
         '<div id="q1-f" class="h">$A(L)=L\\cap a^*b^*$ &nbsp; ✓</div>'
         '<div id="q1-ce" class="h">$A(\\{a^nb^n\\})=\\{a^nb^n\\}$ &nbsp; ✗</div></div>'
         + '<div id="q1-trap" class="h">' + st.card("q1-trapc", "trap", "⚠️ ח״ה ∩ רגולרית = <b>ח״ה</b>, לא בהכרח רגולרית").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q1, "qa", notes={"b": "$\\{a^nb^n\\}$"}))

q2 = Scene("q2", "שאלה 2: הפרש", [
    KP("שאלה שנייה, ושימו לב: מחפשים את הטענה **שלא** נכונה."),
    KP("ח״ה פחות רגולרית: זה חיתוך עם המשלים של הרגולרית. סגור, אז הטענה נכונה, ולא אותה מחפשים.",
       say="חסרת הקשר פחות רגולרית: זה חיתוך עם המשלים של הרגולרית. סגור, אז הטענה נכונה, ולא אותה מחפשים.",
       do=show("q2-0", "qb-x-b", "qb-n-b")),
    KP("שתי רגולריות: $L_1$ משורשרת עם המשלים של $L_2$. משלים ושרשור סגורים לרגולריות. נכונה.",
       say="שתי רגולריות: אֵל אחת משורשרת עם המשלים של אֵל שתיים. משלים ושרשור סגורים לרגולריות. נכונה.",
       do=show("q2-1", "qb-x-c", "qb-n-c")),
    KP("$L_2$ סופית: המשלים שלה רגולרי, ובפרט חסר הקשר. ושרשור של חסרות הקשר סגור. נכונה.",
       say="אֵל שתיים סופית: המשלים שלה רגולרי, ובפרט חסר הקשר. ושרשור של חסרות הקשר סגור. נכונה.",
       do=show("q2-2", "qb-x-d", "qb-n-d")),
    KP("נשארה הטענה על **שתי** חסרות הקשר. נמצא דוגמה נגדית מהדוגמאות הקבועות.", do=show("q2-trap")),
    KP("$L_1=\\Sigma^*$, ו-$L_2=\\overline{uu}$. שתיהן חסרות הקשר.",
       say="אֵל אחת שווה סיגמא כוכבית, ואֵל שתיים שווה המשלים של יו יו. שתיהן חסרות הקשר.", do=show("q2-ce")),
    KP("ההפרש: כל המילים, פחות אלה שאינן $uu$. נשארות בדיוק מילים מהצורה $uu$, וזו לא חסרת הקשר.",
       say="ההפרש: כל המילים, פחות אלה שאינן יו יו. נשארות בדיוק מילים מהצורה יו יו, וזו לא חסרת הקשר.",
       do=show("q2-ce2", "qb-ok-a")),
    KP("זו הטענה הלא נכונה. המשלים הוא מקרה פרטי של הפרש: $\\Sigma^*\\setminus L$. אילו הפרש היה סגור, גם משלים היה סגור.",
       say="זו הטענה הלא נכונה. המשלים הוא מקרה פרטי של הפרש: סיגמא כוכבית פחות אֵל. אילו הפרש היה סגור, גם משלים היה סגור.",
       do=show("q2-rule"), hold=0.6),
], stage=W.STYLE + W.steps("q2", [
    ("ח״ה $\\setminus$ רגולרית $=$ ח״ה $\\cap$ רגולרית ✓", "ok"),
    ("$L_1\\cdot\\overline{L_2}$, שתיהן רגולריות: רגולרית ✓", "ok"),
    ("ח״ה $\\cdot\\,\\overline{F}$, $F$ סופית: ח״ה ✓", "ok")])
         + '<div class="clo-big" style="font-size:40px"><div id="q2-ce" class="h">$\\Sigma^*\\setminus\\overline{uu}$</div>'
           '<div id="q2-ce2" class="h">$=\\{uu\\mid u\\in\\{a,b\\}^*\\}$ &nbsp; ✗ לא ח״ה</div></div>'
         + '<div id="q2-trap" class="h">' + st.card("q2-trapc", "trap", "⚠️ <b>שתי</b> ח״ה: $L_1\\setminus L_2$ לא בהכרח ח״ה").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q2, "qb", notes={"b": "∩ רגולרית", "c": "סגורות", "d": "סגורות"}, small=True)
       + st.card("q2-rule", "rule", "🔑 $\\overline{L}=\\Sigma^*\\setminus L$: משלים הוא מקרה פרטי של הפרש. אילו הפרש היה סגור, גם משלים היה סגור"))

q3 = Scene("q3", "שאלה 3: לשמור רק אפסים", [
    KP("שאלה שלישית. $zero(w)$ משאירה רק את האפסים. למשל, מ-$0010$ נשאר $000$.",
       say="שאלה שלישית. זירו של דאבל יו משאירה רק את האפסים. למשל, מאפס אפס אחת אפס נשאר אפס אפס אפס.",
       do=show("q3-def")),
    KP("טענה ראשונה: אם $L$ חסרת הקשר, גם $Z(L)$ חסרת הקשר.",
       say="טענה ראשונה: אם אֵל חסרת הקשר, גם זֵד של אֵל חסרת הקשר."),
    KP("לוקחים דקדוק של $L$, ומחליפים בו כל $1$ ב-$\\varepsilon$. למשל, $0S0\\mid1$ הופך ל-$0S0\\mid\\varepsilon$.",
       say="לוקחים דקדוק של אֵל, ומחליפים בו כל אחת באפסילון. למשל, אס גוזר אפס אס אפס או אחת, הופך לאפס אס אפס או אפסילון.",
       do=show("q3-g")),
    KP("זה עדיין דקדוק חסר הקשר, והוא יוצר בדיוק את $Z(L)$. אז הטענה הראשונה נכונה.",
       say="זה עדיין דקדוק חסר הקשר, והוא יוצר בדיוק את זֵד של אֵל. אז הטענה הראשונה נכונה."),
    KP("טענה שנייה, הכיוון ההפוך: אם $Z(L)$ חסרת הקשר, אז $L$ חסרת הקשר. וזו המלכודת.",
       say="טענה שנייה, הכיוון ההפוך: אם זֵד של אֵל חסרת הקשר, אז אֵל חסרת הקשר. וזו המלכודת.", do=show("q3-trap")),
    KP("ניקח $L=\\{0^n1^n0^n\\}$, שלושה מונים שווים: לא חסרת הקשר.",
       say="ניקח אֵל שווה אפס בחזקת אֵן, אחת בחזקת אֵן, אפס בחזקת אֵן. שלושה מונים שווים: לא חסרת הקשר.",
       do=show("q3-ce")),
    KP("מוחקים את האחדות, ונשארים $2n$ אפסים: שפת המילים עם מספר זוגי וחיובי של אפסים. היא אפילו רגולרית.",
       say="מוחקים את האחדות, ונשארים שתיים אֵן אפסים: שפת המילים עם מספר זוגי וחיובי של אפסים. היא אפילו רגולרית.",
       do=show("q3-ce2", "qc-ok-c", "qc-x-a", "qc-x-b", "qc-x-d")),
    KP("המחיקה לקחה איתה את האחדות, ואיתן את ההשוואה השלישית. בדיוק כמו $D_a$ בסרטון K06.",
       say="המחיקה לקחה איתה את האחדות, ואיתן את ההשוואה השלישית. בדיוק כמו דֵי אֵיי בסרטון קיי אפס שש.", hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q3-def" class="h">$zero(0010)=000$</div>'
         '<div id="q3-g" class="h">$S\\to0S0\\mid1\\quad\\Longrightarrow\\quad S\\to0S0\\mid\\varepsilon$</div>'
         '<div id="q3-ce" class="h">$L=\\{0^n1^n0^n\\mid n\\ge1\\}$ &nbsp; ✗ לא ח״ה</div>'
         '<div id="q3-ce2" class="h">$Z(L)=\\{0^{2n}\\mid n\\ge1\\}$ &nbsp; ✓ ח״ה</div></div>'
         + '<div id="q3-trap" class="h">' + st.card("q3-trapc", "trap", "⚠️ <b>הכיוון ההפוך</b>: $Z(L)$ ח״ה לא אומר כלום על $L$").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q3, "qc", small=True))

q4 = Scene("q4", "שאלה 4: להעתיק מילה", [
    KP("שאלה רביעית. $Z(L)$ מכילה את $w\\#w$: מילה מ-$L$, סולמית, ואותה מילה שוב.",
       say="שאלה רביעית. זֵד של אֵל מכילה את דאבל יו סולמית דאבל יו: מילה מאֵל, סולמית, ואותה מילה שוב.", do=show("q4-def")),
    KP("המלכודת כאן הפוכה: הפעולה נראית תמימה, אז מצפים שהיא תשמור על המחלקה. אבל **העתקה** היא לא פעולה מהטבלה.",
       do=show("q4-trap")),
    KP("טענה ראשונה, רגולריות. ניקח $L=1^*$, רגולרית. אז $Z(L)$ היא $1^n\\#1^n$.",
       say="טענה ראשונה, רגולריות. ניקח אֵל שווה אחת כוכבית, רגולרית. אז זֵד של אֵל היא אחת בחזקת אֵן, סולמית, אחת בחזקת אֵן.",
       do=show("q4-1")),
    KP("ההוכחה: הרישות $1$, $11$, $111$… הן קבוצה מפרידה אינסופית. הסיפא $\\#1^i$ מקבלת רק אחרי $1^i$. לא רגולרית: הטענה הראשונה נופלת.",
       say="ההוכחה: הרישות אחת, אחת אחת, אחת אחת אחת, וכן הלאה, הן קבוצה מפרידה אינסופית. הסיפא סולמית ואחריה אחת בחזקת אַי, מתקבלת רק אחרי אחת בחזקת אַי. לא רגולרית: הטענה הראשונה נופלת.",
       do=show("q4-1b")),
    KP("טענה שנייה, חסרות הקשר. ניקח $L$ = הפלינדרומים, חסרת הקשר.",
       say="טענה שנייה, חסרות הקשר. ניקח אֵל שווה הפלינדרומים, חסרת הקשר.", do=show("q4-2")),
    KP("ניקח את $0^\\ell1^\\ell0^\\ell\\#0^\\ell1^\\ell0^\\ell$ בלמת הניפוח לחסרות הקשר, שנלמד ברמה הבאה. החלון קצר: לכל היותר $\\ell$ אותיות.",
       say="ניקח את המילה: אפס, אחת ואפס, כל אחד בחזקת קבוע הניפוח, סולמית, ושוב אותו דבר. בלמת הניפוח לחסרות הקשר, שנלמד ברמה הבאה. החלון קצר: לכל היותר קבוע הניפוח אותיות.",
       do=show("q4-2b")),
    KP("אז ניפוח באפס פעמים לא יכול לתקן את שני העותקים באותה צורה: או שאין סולמית, או שהעותקים שונים, או שהם כבר לא פלינדרום.",
       say="אז ניפוח באפס פעמים לא יכול לתקן את שני העותקים באותה צורה: או שאין סולמית, או שהעותקים שונים, או שהם כבר לא פלינדרום."),
    KP("בכל מקרה המילה יוצאת מהשפה: $Z(L)$ לא חסרת הקשר. הטענה השנייה נופלת.",
       say="בכל מקרה המילה יוצאת מהשפה: זֵד של אֵל לא חסרת הקשר. הטענה השנייה נופלת."),
    KP("שתי הטענות לא נכונות. האינטואיציה: העתקה יוצרת השוואה **חוצה**, כמו $uu$. ההוכחה היא מה שראינו: קבוצה מפרידה, ולמת הניפוח.",
       say="שתי הטענות לא נכונות. האינטואיציה: העתקה יוצרת השוואה חוצה, כמו יו יו. ההוכחה היא מה שראינו: קבוצה מפרידה, ולמת הניפוח.",
       do=show("qd-ok-b", "qd-x-a", "qd-x-c", "qd-x-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q4-def" class="h">$Z(L)=\\{w\\#w\\mid w\\in L\\}$</div>'
         '<div id="q4-1" class="h">$Z(1^*)=\\{1^n\\#1^n\\}$</div>'
         '<div id="q4-1b" class="clo-heb h">לא רגולרית: טענה I נופלת</div>'
         '<div id="q4-2" class="h">$L=\\{w\\mid w=w^R\\}$</div>'
         '<div id="q4-2b" class="h">$0^\\ell1^\\ell0^\\ell\\#0^\\ell1^\\ell0^\\ell$ &nbsp; ✗ לא ח״ה</div></div>'
         + '<div id="q4-trap" class="h">' + st.card("q4-trapc", "trap", "⚠️ <b>העתקה</b> אינה פעולה מהטבלה: היא יוצרת השוואה חוצה").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q4, "qd", small=True))

q5 = Scene("q5", "שאלה 5: שתי לא ח״ה", [
    KP("שאלה אחרונה. $L_1$ ו-$L_2$ שתיהן **לא** חסרות הקשר. מה אפשר לומר בהכרח על החיתוך שלהן?",
       say="שאלה אחרונה. אֵל אחת ואֵל שתיים שתיהן לא חסרות הקשר. מה אפשר לומר בהכרח על החיתוך שלהן?"),
    KP("\"בהכרח רגולרית\", או \"בהכרח חסרת הקשר\": ניקח את אותה שפה פעמיים. החיתוך הוא השפה עצמה, לא חסרת הקשר.",
       say="בהכרח רגולרית, או בהכרח חסרת הקשר: ניקח את אותה שפה פעמיים. החיתוך הוא השפה עצמה, לא חסרת הקשר.",
       do=show("q5-1", "qe-x-a", "qe-x-b")),
    KP("והמלכודת: \"בהכרח לא חסרת הקשר\". נשמע כמו כלל, אבל זה הזוג הקסום שוב.",
       say="והמלכודת: בהכרח לא חסרת הקשר. נשמע כמו כלל, אבל זה הזוג הקסום שוב.", do=show("q5-trap")),
    KP("ניקח $\\{a^{n^2}\\}$ ואת המשלים שלה. לפי טבלת השפות הידועות, שתיהן לא חסרות הקשר.",
       say="ניקח אֵיי בחזקת אֵן בריבוע, ואת המשלים שלה. לפי טבלת השפות הידועות, שתיהן לא חסרות הקשר.",
       do=show("q5-2")),
    KP("החיתוך שלהן ריק, וריקה היא רגולרית. אז שלוש הטענות נופלות, והתשובה: אף אחת מהן.",
       do=show("q5-3", "qe-x-c", "qe-ok-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q5-1" class="h">$L_1=L_2$: &nbsp; $L_1\\cap L_2=L_1$</div>'
         '<div id="q5-2" class="h">$L_1=\\{a^{n^2}\\},\\ L_2=\\overline{L_1}$</div>'
         '<div id="q5-3" class="h">$L_1\\cap L_2=\\emptyset$ &nbsp; ✓ רגולרית</div></div>'
         + '<div id="q5-trap" class="h">' + st.card("q5-trapc", "trap", "⚠️ \"אם שתיהן לא ח״ה, אז החיתוך לא ח״ה\": "
                                                    "נופל עם $L$ ו-$\\overline{L}$").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q5, "qe"))

recap = Scene("recap", "סיכום", [
    KP("לסיכום: חסרת הקשר חיתוך רגולרית היא חסרת הקשר, ולא בהכרח רגולרית.", do=show("c1")),
    KP("ח״ה פחות רגולרית סגור. ח״ה פחות ח״ה לא, כי זה משלים בתחפושת.",
       say="חסרת הקשר פחות רגולרית סגור. חסרת הקשר פחות חסרת הקשר לא, כי זה משלים בתחפושת.", do=show("c2")),
    KP("החלפה או מחיקה של אות בדקדוק שומרת על חסרות הקשר. אבל הכיוון ההפוך נופל, כי המחיקה מוחקת גם השוואה.",
       do=show("c3")),
    KP("העתקה, $w\\#w$, אינה פעולה מהטבלה. והזוג הקסום מפיל כל \"בהכרח\" על לא חסרות הקשר. בהצלחה!",
       say="העתקה, דאבל יו סולמית דאבל יו, אינה פעולה מהטבלה. והזוג הקסום מפיל כל בהכרח על לא חסרות הקשר. בהצלחה!",
       do=show("c4"), hold=0.8),
], stage=W.STYLE + W.steps("rq", [
    ('<span class="qid" style="display:inline-block">24X-C-Q10</span> ח״ה ∩ $a^*b^*$: ח״ה, לא בהכרח רגולרית', "bad"),
    ('<span class="qid" style="display:inline-block">21S-A-Q15</span> $\\Sigma^*\\setminus\\overline{uu}=uu$', "bad"),
    ('<span class="qid" style="display:inline-block">23A-A-Q15</span> $\\{0^n1^n0^n\\}\\to\\{0^{2n}\\}$', "bad"),
    ('<span class="qid" style="display:inline-block">24A-B-Q6</span> $w\\#w$: אף מחלקה לא נשמרת', "bad"),
    ('<span class="qid" style="display:inline-block">23A-A-Q19</span> $\\{a^{n^2}\\}\\cap\\overline{\\{a^{n^2}\\}}=\\emptyset$', "bad")]),
   panel=st.card("c1", "rule", "🔑 ח״ה ∩ רגולרית = <b>ח״ה</b>, לא בהכרח רגולרית")
       + st.card("c2", "rule", "🔑 ח״ה $\\setminus$ רגולרית ✓ · ח״ה $\\setminus$ ח״ה ✗")
       + st.card("c3", "trap", "⚠️ מחיקה/החלפה שומרת על ח״ה; הכיוון ההפוך נופל")
       + st.card("c4", "trap", "⚠️ העתקה $w\\#w$ שוברת הכול; $L,\\overline{L}$ מפילים כל \"בהכרח\""))
recap.phrases[0].do += show(*[f"rq-{i}" for i in range(5)])

VIDEO = Video("K06b", "classify", "סגירות של שפות חסרות הקשר",
              [title, tools, q1, q2, q3, q4, q5, recap],
              bank={"24X-C-Q10": "a", "21S-A-Q15": "a", "23A-A-Q15": "c", "24A-B-Q6": "b", "23A-A-Q19": "d"})
