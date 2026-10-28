# -*- coding: utf-8 -*-
"""K06a · (בונוס) סגירות של שפות רגולריות — video script (build: tools/video/vid.py K06a).

Bonus video of level K06 (tools/needhelp/classify/K06.py: closure table + fixed counterexamples + proof method).
Exam questions: five reg_closure questions that no level cites (design doc list):
  24X-A-Q3 (closure of the class "infinite regular"), 25A-B-Q6 (a^{n^2} cut at 2025),
  25A-A-Q6 (primes ∪ {a,aa}, and its star), 25A-C-Q16 (Z(L1,L2) = "both or neither"),
  19B-A-Q5 (what proves non-regularity).
Closure theorems are stated as the K06 lesson states them; every concrete language claim is checked below.
"""
import re
from nh import *
from vid import Scene, Video, show, hide, BANK
import stage as st
import w_closure as W
from w_closure import KP

# ---------------------------------------------------------------- verified facts
SIG = rx("(a+b)*", "ab")
EVEN = rx("((a+b)(a+b))*", "ab")
ODD = rx("(a+b)((a+b)(a+b))*", "ab")
assert EVEN.dfa().is_infinite() and ODD.dfa().is_infinite() and SIG.dfa().is_infinite()
assert not (EVEN.lang(8) & ODD.lang(8))                         # even ∩ odd = ∅
assert SIG.dfa().complement().is_empty()                         # complement of Σ* = ∅
assert (EVEN.lang(8) | ODD.lang(8)) == SIG.lang(8)

# 24X-A-Q3
Q1 = BANK["24X-A-Q3"]
assert Q1["correctId"] == "c"

# 25A-B-Q6: L = {a^{n^2} | n >= 1}
Q2 = BANK["25A-B-Q6"]
assert Q2["correctId"] == "c"
SQ = lambda w: set(w) <= {"a"} and len(w) >= 1 and int(len(w) ** .5) ** 2 == len(w)
assert rank_growing(SQ, "a", plens=(3, 6, 9), slen=14)           # a^{n^2} is not regular
assert sep_infinite(SQ, lambda k: "a" * (k * k), ["a" * j for j in range(40)], n=6)
SQUARES = [n * n for n in range(1, 60)]
LOW = [k for k in SQUARES if k < 2025]
assert len(LOW) == 44 and LOW[-1] == 1936 and 45 * 45 == 2025     # the finite part: a^1 … a^1936, 44 words

# 25A-A-Q6: L = {a^p | p prime}
Q3 = BANK["25A-A-Q6"]
assert Q3["correctId"] == "d"
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
PR = lambda w: set(w) <= {"a"} and isprime(len(w))
assert rank_growing(PR, "a")
assert isprime(2) and not isprime(1)                              # aa is already in L, a is the new word
M = {1, 2} | {p for p in range(60) if isprime(p)}                # lengths in L ∪ {a, aa}
STAR = {0}
for _ in range(60):
    STAR |= {s + m for s in STAR for m in M if s + m <= 60}
assert STAR == set(range(61))                                    # (L ∪ {a,aa})^* = a^*
UNION = lambda w: PR(w) or w in ("a", "aa")
assert rank_growing(UNION, "a")                                  # L ∪ {a,aa} is still not regular

# 25A-C-Q16: Z(L1,L2) = both or neither
Q4 = BANK["25A-C-Q16"]
assert Q4["correctId"] == "a"
def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())
ZOZ = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "01"))
Z = lambda A, B: (lambda w: (A(w) and B(w)) or (not A(w) and not B(w)))
assert rank_growing(ZOZ, "01")
assert all(Z(ZOZ, ZOZ)(w) for w in words("01", 9)) and rank_stable(Z(ZOZ, ZOZ), "01") == 1   # Σ*
R1, R2 = rx("0*1*", "01"), rx("(0+1)*1", "01")                   # sample regular pair: Z regular
assert rank_stable(Z(R1.accepts, R2.accepts), "01") is not None

# 19B-A-Q5: how to show non-regularity
Q5 = BANK["19B-A-Q5"]
assert Q5["correctId"] == "d"
assert CFG("S -> aS | bS | ε").lang(7) == set(words("ab", 7))             # Σ* has a grammar (and a PDA)
assert classify_cert(lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(parts(w, "abc")), "abc",
                     ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7) == "noncfl"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    KP("סרטון בונוס לרמת הסגירויות: הפעם רק שפות רגולריות."),
    KP("נבנה ארגז כלים קטן, ואז נפתור חמש שאלות אמיתיות ממבחנים. בכל אחת נמצא את המלכודת.", hold=0.4),
], stage='<div class="kicker">K06a · סיווג שפות · בונוס</div><h1>סגירות של שפות רגולריות</h1>'
         '<p>חמש שאלות מבחן על סגירות של רגולריות, עם המלכודת של כל אחת.</p>',
   layout="title")

tools = Scene("tools", "ארגז הכלים", [
    KP("השפות הרגולריות סגורות לכל הפעולות בטבלה: איחוד, שרשור, כוכבית, היפוך, חיתוך ומשלים.", do=show("tl-0")),
    KP("ומזה מקבלים עוד פעולות בחינם. הפרש: $L_1\\setminus L_2$ הוא $L_1$ חיתוך המשלים של $L_2$.",
       say="ומזה מקבלים עוד פעולות בחינם. הפרש: אֵל אחת פחות אֵל שתיים, הוא אֵל אחת חיתוך המשלים של אֵל שתיים.",
       do=show("tl-1")),
    KP("וכל צירוף של פעולות כאלה, כמה שתרצו, נשאר רגולרי.", do=show("tl-2")),
    KP("כלי ראשון, כדי להוכיח **רגולרית**: לכתוב את השפה כצירוף כזה.", do=show("tk-1")),
    KP("כלי שני, כדי להוכיח **לא רגולרית**: בשלילה. אילו הייתה רגולרית, היינו מקבלים ממנה בפעולות סגורות שפה שידוע שאינה רגולרית.",
       do=show("tk-2")),
    KP("כלי שלישי, נגד טענה כללית מדי: דוגמה נגדית. הזוג הקסום, $\\Sigma^*$, $\\emptyset$, וקבוצה סופית.",
       do=show("tk-3")),
    KP("ומלכודת אחת שחוזרת בכל השאלות: הטבלה מדברת על **רגולרית בפעולה עם רגולרית**. היא לא אומרת כלום על שפה לא רגולרית.",
       do=show("tk-4"), hold=0.5),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="tl-0" class="clo-heb h" style="color:var(--ink)">איחוד · שרשור · כוכבית · היפוך · חיתוך · משלים &nbsp;✓</div>'
         '<div id="tl-1" class="h">$L_1\\setminus L_2=L_1\\cap\\overline{L_2}$</div>'
         '<div id="tl-2" class="h">$(L_1\\cap L_2)\\cup(\\overline{L_1}\\cap\\overline{L_2})$ &nbsp;✓</div></div>',
   panel=st.card("tk-1", "rule", "🔑 <b>רגולרית?</b> צירוף של פעולות סגורות")
       + st.card("tk-2", "rule", "🔑 <b>לא רגולרית?</b> בשלילה: ממנה מקבלים שפה לא רגולרית ידועה")
       + st.card("tk-3", "rule", "🔑 <b>טענה כללית?</b> הזוג הקסום · $\\Sigma^*$ · $\\emptyset$ · קבוצה סופית")
       + st.card("tk-4", "trap", "⚠️ הטבלה: <b>רגולרית</b> op <b>רגולרית</b>. על לא רגולרית היא שותקת"))

q1 = Scene("q1", "שאלה 1: מחלקה חדשה", [
    KP("שאלה ראשונה. המחלקה כאן היא לא כל הרגולריות, אלא רק **הרגולריות האינסופיות**."),
    KP("זו המלכודת: מחלקה אחרת, ולכן גם טבלה אחרת. צריך לבדוק שהתוצאה גם רגולרית **וגם** אינסופית.",
       do=show("q1-trap")),
    KP("משלים: ניקח $\\Sigma^*$, רגולרית ואינסופית. המשלים שלה הוא $\\emptyset$, ריקה, כלומר סופית. נפסל.",
       do=show("q1-c", "qa-x-a", "qa-n-a")),
    KP("חיתוך: המילים באורך זוגי, והמילים באורך אי זוגי. שתיהן רגולריות ואינסופיות, והחיתוך שלהן ריק. נפסל.",
       do=show("q1-i", "qa-x-b", "qa-n-b")),
    KP("איחוד: האיחוד רגולרי, כי הרגולריות סגורות לאיחוד. והוא מכיל את $L_1$ האינסופית, ולכן גם הוא אינסופי.",
       do=show("q1-u", "qa-ok-c")),
    KP("אז האיחוד סגור, והתשובה שאף טענה לא נכונה נופלת.", do=show("qa-x-d", "qa-n-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big">'
         '<div id="q1-c" class="h">$\\overline{\\Sigma^*}=\\emptyset$ &nbsp; סופית ✗</div>'
         '<div id="q1-i" class="h">$(\\Sigma\\Sigma)^*\\cap\\Sigma(\\Sigma\\Sigma)^*=\\emptyset$ &nbsp; ✗</div>'
         '<div id="q1-u" class="h">$L_1\\subseteq L_1\\cup L_2$ &nbsp; אינסופית ✓</div></div>'
         + '<div id="q1-trap" class="h">' + st.card("q1-trapc", "trap", "⚠️ מחלקה חדשה = בודקים את <b>שני</b> התנאים: "
                                                    "רגולרית <b>וגם</b> אינסופית").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q1, "qa", notes={"a": "$\\overline{\\Sigma^*}=\\emptyset$", "b": "זוגי ∩ אי-זוגי", "d": "איחוד סגור"}))

q2 = Scene("q2", "שאלה 2: לחתוך ב-2025", [
    KP("שאלה שנייה. $L$ היא שפת המילים שאורכן ריבוע: $a$, $a^4$, $a^9$, וכן הלאה. היא לא רגולרית.",
       say="שאלה שנייה. אֵל היא שפת המילים שאורכן ריבוע: אֵיי, אֵיי בחזקת ארבע, אֵיי בחזקת תשע, וכן הלאה. היא לא רגולרית.",
       do=show("q2-l")),
    KP("טענה ראשונה: החלק של $L$ עם אורך קטן מ-2025.", say="טענה ראשונה: החלק של אֵל עם אורך קטן מאלפיים עשרים וחמש.",
       do=show("q2-lo")),
    KP("זה ארבעים וארבעה ריבועים, מאחת ועד אלף תשע מאות שלושים ושש. שפה **סופית**, ולכן רגולרית. הטענה הראשונה נכונה.",
       do=show("q2-lo2")),
    KP("טענה שנייה: החלק עם אורך לפחות 2025. כאן המלכודת.", say="טענה שנייה: החלק עם אורך לפחות אלפיים עשרים וחמש. כאן המלכודת.",
       do=show("q2-hi")),
    KP("קל לחשוב: חתכנו עם שפה רגולרית, אז יצא רגולרי. אבל הטבלה אומרת רגולרית חיתוך רגולרית. $L$ לא רגולרית.",
       say="קל לחשוב: חתכנו עם שפה רגולרית, אז יצא רגולרי. אבל הטבלה אומרת רגולרית חיתוך רגולרית. ואֵל לא רגולרית.",
       do=show("q2-trap")),
    KP("נוכיח בשלילה. אילו החלק העליון היה רגולרי, אז $L$ היא איחוד שלו עם החלק התחתון, הסופי.",
       say="נוכיח בשלילה. אילו החלק העליון היה רגולרי, אז אֵל היא איחוד שלו עם החלק התחתון, הסופי.",
       do=show("q2-pf")),
    KP("איחוד של שתי רגולריות הוא רגולרי, ולכן $L$ הייתה רגולרית. סתירה.",
       say="איחוד של שתי רגולריות הוא רגולרי, ולכן אֵל הייתה רגולרית. סתירה."),
    KP("זה בדיוק הכלל של קבוצה סופית: הסרנו מ-$L$ מספר סופי של מילים, וזה לא שינה כלום.",
       say="זה בדיוק הכלל של קבוצה סופית: הסרנו מאֵל מספר סופי של מילים, וזה לא שינה כלום.",
       do=show("q2-rule")),
    KP("אז הראשונה נכונה והשנייה לא.", do=show("qb-ok-c", "qb-x-a", "qb-x-b", "qb-x-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q2-l" class="h">$L=\\{a^{n^2}\\mid n\\ge1\\}$</div>'
         '<div id="q2-lo" class="h">$L\\cap\\{a^k\\mid k<2025\\}=\\{a^1,a^4,\\dots,a^{1936}\\}$</div>'
         '<div id="q2-lo2" class="clo-heb h">44 מילים: סופית, ולכן רגולרית ✓</div>'
         '<div id="q2-hi" class="h">$L\\cap\\{a^k\\mid k\\ge2025\\}$ &nbsp; ?</div>'
         '<div id="q2-pf" class="h">$L=(L\\cap\\{a^k\\mid k\\ge2025\\})\\cup(L\\cap\\{a^k\\mid k<2025\\})$'
         '<div class="clo-heb">? &nbsp; איחוד &nbsp; סופית</div></div></div>'
         + '<div id="q2-trap" class="h">' + st.card("q2-trapc", "trap", "⚠️ \"חתכנו עם רגולרית, אז רגולרי\": רק אם גם $L$ רגולרית").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q2, "qb") + st.card("q2-rule", "rule", "🔑 הסרה של מספר סופי של מילים לא משנה רגולריות"))

q3 = Scene("q3", "שאלה 3: ראשוניים וכוכבית", [
    KP("שאלה שלישית. $L$: מילים מעל $a$ שאורכן ראשוני: $aa$, $aaa$, $a^5$, וכן הלאה. גם היא לא רגולרית: מוכיחים בלמת הניפוח.",
       say="שאלה שלישית. אֵל: מילים מעל אֵיי שאורכן ראשוני: אֵיי אֵיי, אֵיי אֵיי אֵיי, אֵיי בחזקת חמש, וכן הלאה. גם היא לא רגולרית: מוכיחים בלמת הניפוח.",
       do=show("q3-l")),
    KP("טענה ראשונה: מוסיפים ל-$L$ את $a$ ואת $aa$. האם יצא רגולרי?",
       say="טענה ראשונה: מוסיפים לאֵל את אֵיי ואת אֵיי אֵיי. האם יצא רגולרי?", do=show("q3-u")),
    KP("$aa$ כבר בפנים, כי 2 ראשוני. ו-$a$ היא מילה אחת חדשה. הוספנו מספר סופי של מילים, אז לא רגולרי.",
       say="אֵיי אֵיי כבר בפנים, כי שתיים ראשוני. ואֵיי היא מילה אחת חדשה. הוספנו מספר סופי של מילים, אז לא רגולרי.",
       do=show("q3-u2")),
    KP("פורמלית: אילו $L\\cup\\{a,aa\\}$ הייתה רגולרית, אז החיתוך שלה עם המשלים של $\\{a\\}$, שהוא $L$, היה רגולרי. סתירה.",
       say="פורמלית: אילו אֵל איחוד אֵיי ואֵיי אֵיי הייתה רגולרית, אז החיתוך שלה עם המשלים של הקבוצה אֵיי, שהוא אֵל, היה רגולרי. סתירה.",
       do=show("q3-pf")),
    KP("טענה שנייה: הכוכבית של אותה שפה. והמלכודת: \"כוכבית של לא רגולרית נשארת לא רגולרית\".",
       say="טענה שנייה: הכוכבית של אותה שפה. והמלכודת: כוכבית של לא רגולרית נשארת לא רגולרית.",
       do=show("q3-trap")),
    KP("אבל עכשיו $a$ בפנים. ובכוכבית מותר לשרשר את $a$ כמה פעמים שרוצים: מקבלים **כל** $a^k$.",
       say="אבל עכשיו אֵיי בפנים. ובכוכבית מותר לשרשר את אֵיי כמה פעמים שרוצים: מקבלים כל אֵיי בחזקת קיי.",
       do=show("q3-s")),
    KP("כלומר הכוכבית היא $a^*$, רגולרית. הראשונה לא נכונה, והשנייה נכונה.",
       say="כלומר הכוכבית היא אֵיי כוכבית, רגולרית. הראשונה לא נכונה, והשנייה נכונה.",
       do=show("qc-ok-d", "qc-x-a", "qc-x-b", "qc-x-c")),
    KP("הכלל: פעולה על שפה לא רגולרית יכולה לבלוע את כל המבנה. ככה בדיוק מתנהגת כוכבית עם $a$ בפנים.",
       say="הכלל: פעולה על שפה לא רגולרית יכולה לבלוע את כל המבנה. ככה בדיוק מתנהגת כוכבית עם אֵיי בפנים.",
       do=show("q3-rule"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q3-l" class="h">$L=\\{a^p\\}$ <span class="clo-heb">, $p$ ראשוני</span></div>'
         '<div id="q3-u" class="h">$L\\cup\\{a,aa\\}=L\\cup\\{a\\}$</div>'
         '<div id="q3-u2" class="clo-heb h">נוספה מילה אחת: עדיין לא רגולרית ✗</div>'
         '<div id="q3-pf" class="h">$(L\\cup\\{a,aa\\})\\cap\\overline{\\{a\\}}=L$</div>'
         '<div id="q3-s" class="h">$(L\\cup\\{a,aa\\})^*=a^*$ &nbsp; ✓</div></div>'
         + '<div id="q3-trap" class="h">' + st.card("q3-trapc", "trap", "⚠️ \"כוכבית של לא רגולרית היא לא רגולרית\": לא נכון. "
                                                    "$a$ בפנים, ולכן הכוכבית היא $a^*$").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q3, "qc") + st.card("q3-rule", "rule", "🔑 אם $a\\in L$ (מעל $\\{a\\}$), אז $L^*=a^*$"))

q4 = Scene("q4", "שאלה 4: שתיהן או אף אחת", [
    KP("שאלה רביעית. $\\mathbf{Z}$ מכילה מילה אם היא בשתי השפות, או באף אחת מהן.",
       say="שאלה רביעית. זֵד מכילה מילה אם היא בשתי השפות, או באף אחת מהן.", do=show("q4-def")),
    KP("טענה ראשונה: אם שתיהן רגולריות, $\\mathbf{Z}$ רגולרית. נכתוב אותה בפעולות:",
       say="טענה ראשונה: אם שתיהן רגולריות, זֵד רגולרית. נכתוב אותה בפעולות:"),
    KP("חיתוך של שתיהן, איחוד חיתוך של המשלימים. רק חיתוך, איחוד ומשלים, כולם סגורים. אז נכונה.",
       do=show("q4-f")),
    KP("טענה שנייה: אם שתיהן **לא** רגולריות, $\\mathbf{Z}$ לא רגולרית. זו המלכודת: נשמע הגיוני, וזה לא.",
       say="טענה שנייה: אם שתיהן לא רגולריות, זֵד לא רגולרית. זו המלכודת: נשמע הגיוני, וזה לא.",
       do=show("q4-trap")),
    KP("ניקח את אותה שפה פעמיים: $L_1=L_2=\\{0^n1^n\\}$.",
       say="ניקח את אותה שפה פעמיים: אֵל אחת שווה אֵל שתיים שווה אפס בחזקת אֵן, אחת בחזקת אֵן.", do=show("q4-ce")),
    KP("כל מילה נמצאת בשתיהן או באף אחת, כי הן אותה שפה. אז $\\mathbf{Z}=\\Sigma^*$, רגולרית.",
       say="כל מילה נמצאת בשתיהן או באף אחת, כי הן אותה שפה. אז זֵד שווה סיגמא כוכבית, רגולרית.",
       do=show("q4-ce2")),
    KP("הראשונה נכונה, השנייה לא.", do=show("qd-ok-a", "qd-x-b", "qd-x-c", "qd-x-d")),
    KP("וזה אותו רעיון כמו הזוג הקסום: שתי לא רגולריות, ותוצאה שבולעת הכול.", do=show("q4-rule"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:38px">'
         '<div id="q4-def" class="h">$w\\in\\mathbf{Z}\\iff$ <span class="clo-heb">בשתיהן, או באף אחת</span></div>'
         '<div id="q4-f" class="h">$\\mathbf{Z}=(L_1\\cap L_2)\\cup(\\overline{L_1}\\cap\\overline{L_2})$ ✓</div>'
         '<div id="q4-ce" class="h">$L_1=L_2=\\{0^n1^n\\}$</div>'
         '<div id="q4-ce2" class="h">$\\mathbf{Z}(L_1,L_1)=\\Sigma^*$ &nbsp; ✓</div></div>'
         + '<div id="q4-trap" class="h">' + st.card("q4-trapc", "trap", "⚠️ \"לא רגולרית op לא רגולרית = לא רגולרית\": "
                                                    "נופל עם <b>אותה שפה פעמיים</b>").replace(' h"', '"') + "</div>"
         + st.card("q4-rule", "rule", "🔑 $L_1=L_2$ או $L_2=\\overline{L_1}$: הדוגמה הנגדית הראשונה לנסות"),
   panel=W.qcard(Q4, "qd", small=True))

q5 = Scene("q5", "שאלה 5: איך מוכיחים", [
    KP("ושאלה חמישית, קצרה: מה מספיק כדי להראות ששפה $L$ **לא** רגולרית?"),
    KP("חיתוך עם רגולרית: אם $L$ חיתוך רגולרית יוצאת לא רגולרית, אז $L$ לא רגולרית.",
       say="חיתוך עם רגולרית: אם אֵל חיתוך רגולרית יוצאת לא רגולרית, אז אֵל לא רגולרית.", do=show("q5-0")),
    KP("כי אילו $L$ הייתה רגולרית, גם החיתוך היה רגולרי. זה הכלי השני שלנו, בדיוק.",
       say="כי אילו אֵל הייתה רגולרית, גם החיתוך היה רגולרי. זה הכלי השני שלנו, בדיוק.",
       do=show("q5-1", "qe-ok-d")),
    KP("אוטומט מחסנית ל-$L$ מראה רק ש-$L$ חסרת הקשר. גם ל-$\\Sigma^*$ יש אוטומט מחסנית, והיא רגולרית.",
       say="אוטומט מחסנית לאֵל מראה רק שאֵל חסרת הקשר. גם לסיגמא כוכבית יש אוטומט מחסנית, והיא רגולרית.",
       do=show("q5-2", "qe-x-b", "qe-n-b")),
    KP("דקדוק למשלים: אותו דבר. למשלים של $\\Sigma^*$, הקבוצה הריקה, יש דקדוק.",
       say="דקדוק למשלים: אותו דבר. למשלים של סיגמא כוכבית, הקבוצה הריקה, יש דקדוק.",
       do=show("qe-x-c", "qe-n-c")),
    KP("והמלכודת: \"אי אפשר להשתמש בלמת הניפוח לחסרות הקשר\". נשמע נכון, כי זו למה של מחלקה אחרת.",
       say="והמלכודת: אי אפשר להשתמש בלמת הניפוח לחסרות הקשר. נשמע נכון, כי זו למה של מחלקה אחרת.",
       do=show("q5-trap")),
    KP("אבל אם הלמה מראה ש-$L$ לא חסרת הקשר, אז היא בפרט לא רגולרית. כל רגולרית היא חסרת הקשר.",
       say="אבל אם הלמה מראה שאֵל לא חסרת הקשר, אז היא בפרט לא רגולרית. כל רגולרית היא חסרת הקשר.",
       do=show("q5-3", "qe-x-a", "qe-n-a"), hold=0.6),
], stage=W.STYLE + W.steps("q5", [
    ("אם $R$ רגולרית ו-$L\\cap R$ לא רגולרית, אז $L$ לא רגולרית", "ok"),
    ("כי אילו $L$ רגולרית, גם $L\\cap R$ הייתה רגולרית: <b>סתירה</b>", "ok"),
    ("אוטומט מחסנית / דקדוק מוכיחים רק ח״ה. גם ל-$\\Sigma^*$ יש", "bad"),
    ("אם $L$ לא ח״ה, אז בפרט היא לא רגולרית: כל רגולרית היא ח״ה", "key")])
         + '<div id="q5-trap" class="h">' + st.card("q5-trapc", "trap", "⚠️ למת הניפוח לח״ה <b>כן</b> מוכיחה אי-רגולריות: "
                                                    "אם לא ח״ה, אז לא רגולרית").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q5, "qe", notes={"a": "לא ח״ה: גם לא רגולרית", "b": "גם $\\Sigma^*$", "c": "גם $\\Sigma^*$"}))

recap = Scene("recap", "סיכום", [
    KP("לסיכום: כדי להוכיח שרגולרית, כותבים אותה כצירוף של פעולות סגורות.", do=show("c1")),
    KP("כדי להוכיח שלא רגולרית, בשלילה: ממנה מקבלים בפעולות סגורות שפה לא רגולרית ידועה.", do=show("c2")),
    KP("הוספה או הסרה של מספר סופי של מילים לא משנה כלום.", do=show("c3")),
    KP("ולא רגולרית בפעולה עם עוד שפה יכולה לצאת רגולרית: אותה שפה פעמיים, המשלים, או כוכבית שבולעת הכול.",
       do=show("c4")),
    KP("ובמחלקה חדשה, כמו רגולריות אינסופיות, בודקים את שני התנאים. בהצלחה!", do=show("c5"), hold=0.8),
], stage=W.STYLE + W.steps("rq", [
    ('<span class="qid" style="display:inline-block">24X-A-Q3</span> מחלקה חדשה: רגולרית <b>וגם</b> אינסופית', "bad"),
    ('<span class="qid" style="display:inline-block">25A-B-Q6</span> חיתוך עם רגולרית לא מציל לא רגולרית', "bad"),
    ('<span class="qid" style="display:inline-block">25A-A-Q6</span> כוכבית עם $a$ בפנים: $a^*$', "bad"),
    ('<span class="qid" style="display:inline-block">25A-C-Q16</span> אותה שפה פעמיים: $\\Sigma^*$', "bad"),
    ('<span class="qid" style="display:inline-block">19B-A-Q5</span> אם לא ח״ה, אז בפרט לא רגולרית', "bad")]),
   panel=st.card("c1", "rule", "🔑 רגולרית: צירוף של פעולות סגורות")
       + st.card("c2", "rule", "🔑 לא רגולרית: בשלילה, דרך פעולה סגורה")
       + st.card("c3", "rule", "🔑 מספר סופי של מילים לא משנה רגולריות")
       + st.card("c4", "trap", "⚠️ לא רגולרית op משהו יכולה לצאת רגולרית: $L_1=L_2$, $\\overline{L}$, כוכבית")
       + st.card("c5", "trap", "⚠️ מחלקה חדשה: בודקים <b>כל</b> תנאי"))
recap.phrases[0].do += show(*[f"rq-{i}" for i in range(5)])

VIDEO = Video("K06a", "classify", "סגירות של שפות רגולריות",
              [title, tools, q1, q2, q3, q4, q5, recap],
              bank={"24X-A-Q3": "c", "25A-B-Q6": "c", "25A-A-Q6": "d", "25A-C-Q16": "a", "19B-A-Q5": "d"})
