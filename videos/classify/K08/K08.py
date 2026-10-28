# -*- coding: utf-8 -*-
"""K08 · מבחן גמר: סיווג שפות — boss walkthrough video (build: tools/video/vid.py K08).

Source: tools/needhelp/classify/K08.py (the checklist of the boss lesson). No new concept: how to attack a
classification question, then four bank questions that NO level cites and that are not in the K08 boss quiz
(24A-B-Q8 26A-A-Q17 21S-A-Q3 25A-B-Q12 26A-A-Q12) nor used by K06a / K06b:
  23A-B-Q19 (a grammar that only looks like palindromes), 21S-A-Q19 (an absorbing union; right answer, wrong reason),
  21S-A-Q13 (regular ∩ {#a=#b}: "possibly regular"), 23A-A-Q22 ((0^k 1^k)^k: not CFL).
Every language claim is checked with the simulators.
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
# 23A-B-Q19
Q1 = BANK["23A-B-Q19"]
assert Q1["correctId"] == "b"
G1 = CFG("S -> 0S0 | 0S1 | 1S0 | 1S1 | ε")
assert G1.lang(10) == {w for w in words("01", 10) if len(w) % 2 == 0}
assert classify_cert(lambda w: len(w) % 2 == 0, "01", ("reg", "((0+1)(0+1))*"), n=10) == "reg"
assert G1.derives("01") and "01" != "10"                                  # 01 is generated and is no palindrome

# 21S-A-Q19
Q2 = BANK["21S-A-Q19"]
assert Q2["correctId"] == "b"
R1 = rx("1*(11)*0*1*", "01")
L2 = lambda w: (lambda m: bool(m) and len(m.group(1)) % 2 == 0 and len(m.group(2)) == len(m.group(3)))(
    re.fullmatch("(1*)(0*)(1*)", w))
assert all(R1.accepts(w) for w in words("01", 11) if L2(w))                 # L2 ⊆ L1
LU = lambda w: R1.accepts(w) or L2(w)
assert same_pred(LU, R1.accepts, "01", 10) and R1.equiv(rx("1*0*1*", "01"))  # L = L1 = 1*0*1*
assert rank_growing(L2, "01")                                               # L2 is not regular
T = ["1" * (2 * d + 1) + "0" * d for d in range(1, 4)]
assert separable(LU, T[0], T[1], "01") is None                              # T is not a separating set for L
assert all(L2("0" * d + "1" * d) and R1.accepts("0" * d + "1" * d) for d in range(6))   # {0^d1^d} ⊆ both

# 21S-A-Q13
Q3 = BANK["21S-A-Q13"]
assert Q3["correctId"] == "c"
EQ = lambda w: w.count("a") == w.count("b")
A_ = rx("a*", "ab")
assert {w for w in words("ab", 9) if A_.accepts(w) and EQ(w)} == {""}        # L = a*  ->  {ε}: regular, finite
AB = rx("a*b*", "ab")
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab"))
assert same_pred(lambda w: AB.accepts(w) and EQ(w), ANBN, "ab", 9)           # L = a*b*  ->  a^n b^n
assert classify_cert(ANBN, "ab", ("cfl", "S -> aSb | ε")) == "cfl"
assert classify_cert(EQ, "ab", ("cfl", "S -> aSbS | bSaS | ε")) == "cfl"    # {#a = #b} is CFL

# 23A-A-Q22
Q4 = BANK["23A-A-Q22"]
assert Q4["correctId"] == "d"
def KK(w):
    m = re.fullmatch("((0+)(1+))+", w)
    if not m:
        return False
    runs = re.findall("0+|1+", w)
    k = len(runs[0])
    return all(len(r) == k for r in runs) and len(runs) == 2 * k
assert [w for w in words("01", 8) if KK(w)] == ["01", "00110011"]
assert all(pump_breaks_cf(KK, ("0" * p + "1" * p) * p, p) for p in (2, 3))
# the case split narrated: y or u mixes 0 and 1 -> n=2 breaks; otherwise n=0 breaks
for p in (2, 3):
    w = ("0" * p + "1" * p) * p
    for a in range(len(w) + 1):
        for b in range(a, min(len(w), a + p) + 1):
            for c in range(b, min(len(w), a + p) + 1):
                for d in range(c, min(len(w), a + p) + 1):
                    x_, y_, z_, u_, v_ = w[:a], w[a:b], w[b:c], w[c:d], w[d:]
                    if not (y_ + u_):
                        continue
                    n = 2 if (len(set(y_)) > 1 or len(set(u_)) > 1) else 0
                    assert not KK(x_ + y_ * n + z_ + u_ * n + v_)
assert rank_growing(KK, "01")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    KP("מבחן הגמר של סיווג שפות. אין כאן חומר חדש."),
    KP("נעבור על רשימת הבדיקה, ואז נפתור ארבע שאלות אמיתיות שלא ראיתם באף רמה, כמו במבחן.", hold=0.4),
], stage='<div class="kicker">K08 · סיווג שפות</div><h1>מבחן גמר: סיווג שפות</h1>'
         '<p>לסווג שפות אמיתיות מהמבחנים: רגולרית, חסרת הקשר או לא, בלי עזרה.</p>',
   layout="title")

attack = Scene("attack", "איך תוקפים שאלה", [
    KP("רשימת הבדיקה, לפי הסדר. אחת: לפשט. אי-שוויונות שמתכנסים לשוויון, כוכבית שבולעת, איחוד שבו חלק מוכל בחלק אחר.",
       do=show("at-0")),
    KP("שתיים: סופית? רגולרית? מודולו, ספירה עד קבוע ותבנית קבועה הם זיכרון סופי.", do=show("at-1")),
    KP("שלוש: לא רגולרית? קבוצה מפרידה אינסופית, או חיתוך עם רגולרית. השוואה בין מונים: חשד ללא רגולרית, ומוכיחים בקבוצה מפרידה.",
       do=show("at-2")),
    KP("ארבע: חסרת הקשר? מקונן, כן. חוצה, או שלוש השוואות, לא, ומוכיחים בלמת הניפוח או בחיתוך עם רגולרית.", do=show("at-3")),
    KP("וחמש: נתון דקדוק? הוא חסר הקשר, אבל **פענחו** אותו לפני שבוחרים \"לא רגולרית\".",
       say="וחמש: נתון דקדוק? הוא חסר הקשר, אבל פענחו אותו לפני שבוחרים: לא רגולרית.", do=show("at-4")),
    KP("ועוד שני דברים. ארבע האפשרויות מוציאות זו את זו: מצאתם רגולרית אינסופית? שתי האחרות נופלות אוטומטית.",
       do=show("at-r")),
    KP("והכלה לא אומרת כלום על מחלקה. $a^*$ מוכלת בשפה לא רגולרית, ו-$\\{\\varepsilon\\}$ מוכלת ב-$\\{a^nb^n\\}$.",
       say="והכלה לא אומרת כלום על מחלקה. אֵיי כוכבית מוכלת בשפה לא רגולרית, והקבוצה של אפסילון מוכלת באֵיי בחזקת אֵן, בִּי בחזקת אֵן.",
       do=show("at-t"), hold=0.5),
], stage=W.STYLE + W.steps("at", [
    ("<b>1. לפשט</b>: אי-שוויונות, כוכבית שבולעת, איחוד מוכל", "key"),
    ("<b>2. סופית? רגולרית?</b> מודולו, עד קבוע, תבנית קבועה", ""),
    ("<b>3. לא רגולרית?</b> קבוצה מפרידה אינסופית, חיתוך עם רגולרית", ""),
    ("<b>4. ח״ה?</b> מקונן כן; חוצה / שלוש השוואות לא", ""),
    ("<b>5. דקדוק נתון?</b> פענחו לפני \"לא רגולרית\"", "key")]),
   panel=st.card("at-r", "rule", "🔑 ארבע האפשרויות <b>מוציאות זו את זו</b>")
       + st.card("at-t", "trap", "⚠️ <b>הכלה</b> לא אומרת כלום על מחלקה: $\\{\\varepsilon\\}\\subseteq\\{a^nb^n\\}$"))

q1 = Scene("q1", "שאלה 1: דקדוק", [
    KP("שאלה ראשונה: דקדוק. הכללים $0S0$ ו-$1S1$ מזכירים מיד פלינדרומים, ושם המלכודת.",
       say="שאלה ראשונה: דקדוק. הכללים אפס אס אפס, ואחת אס אחת, מזכירים מיד פלינדרומים, ושם המלכודת.",
       do=show("q1-trap")),
    KP("פלינדרומים זו שפה חסרת הקשר ולא רגולרית, ולכן הרבה בוחרים בתשובה הזו. אבל צעד חמש: לפענח קודם."),
    KP("יש כאן גם $0S1$ ו-$1S0$. כלומר בכל צעד מוסיפים אות **כלשהי** משמאל, ואות **כלשהי** מימין.",
       say="יש כאן גם אפס אס אחת, ואחת אס אפס. כלומר בכל צעד מוסיפים אות כלשהי משמאל, ואות כלשהי מימין.",
       do=show("q1-a")),
    KP("אין שום קשר בין שתי האותיות. למשל $01$ נגזרת, והיא לא פלינדרום.",
       say="אין שום קשר בין שתי האותיות. למשל אפס אחת נגזרת, והיא לא פלינדרום.", do=show("q1-b")),
    KP("אז הדקדוק יוצר בדיוק את כל המילים באורך זוגי: $((0+1)(0+1))^*$. רגולרית ואינסופית.",
       say="אז הדקדוק יוצר בדיוק את כל המילים באורך זוגי. ביטוי רגולרי: אפס או אחת, פעמיים, בכוכבית. רגולרית ואינסופית.",
       do=show("q1-c", "qa-ok-b", "qa-x-a", "qa-n-a")),
    KP("וכיוון שהאפשרויות מוציאות זו את זו, \"חסרת הקשר ולא רגולרית\" ו\"לא חסרת הקשר\" נופלות.",
       say="וכיוון שהאפשרויות מוציאות זו את זו, חסרת הקשר ולא רגולרית, ולא חסרת הקשר, נופלות.",
       do=show("qa-x-c", "qa-n-c", "qa-x-d"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q1-a" class="h">$S\\to\\sigma_1S\\sigma_2\\mid\\varepsilon$ &nbsp; <span class="clo-heb">כל זוג אותיות</span></div>'
         '<div id="q1-b" class="h">$S\\Rightarrow0S1\\Rightarrow01$</div>'
         '<div id="q1-c" class="h">$L(G)=((0+1)(0+1))^*$ ✓</div></div>'
         + '<div id="q1-trap" class="h">' + st.card("q1-trapc", "trap", "⚠️ <b>נראה כמו פלינדרומים</b>: פענחו לפני שבוחרים").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q1, "qa", notes={"a": "אינסופית", "c": "$01\\in L(G)$"}))

q2 = Scene("q2", "שאלה 2: איחוד שבולע", [
    KP("שאלה שנייה: איחוד. $L_1$ רגולרית, ו-$L_2$, עם $0^k1^k$ בפנים, לא רגולרית.",
       say="שאלה שנייה: איחוד. אֵל אחת רגולרית, ואֵל שתיים, עם אפס בחזקת קיי, אחת בחזקת קיי בפנים, לא רגולרית."),
    KP("צעד אחת: לפשט. כל מילה של $L_2$ היא מספר זוגי של $1$, אחר כך אפסים, אחר כך אחדות.",
       say="צעד אחת: לפשט. כל מילה של אֵל שתיים היא מספר זוגי של אחדות, אחר כך אפסים, אחר כך אחדות.",
       do=show("q2-a")),
    KP("ו-$L_1$ מכילה כל מילה מהצורה הזו. כלומר $L_2$ מוכלת ב-$L_1$, והאיחוד הוא פשוט $L_1$: רגולרית.",
       say="ואֵל אחת מכילה כל מילה מהצורה הזו. כלומר אֵל שתיים מוכלת באֵל אחת, והאיחוד הוא פשוט אֵל אחת: רגולרית.",
       do=show("q2-b", "qb-ok-b")),
    KP("שתי התשובות של \"לא רגולרית\" נופלות. קבוצה מפרידה **אינסופית** לא קיימת לשפה רגולרית.",
       say="שתי התשובות של לא רגולרית נופלות. קבוצה מפרידה אינסופית לא קיימת לשפה רגולרית.",
       do=show("qb-x-c", "qb-n-c")),
    KP("וההכלה של $0^d1^d$ בשתי השפות לא אומרת כלום על מחלקה. זו המלכודת מרשימת הבדיקה.",
       say="וההכלה של אפס בחזקת דִי, אחת בחזקת דִי, בשתי השפות לא אומרת כלום על מחלקה. זו המלכודת מרשימת הבדיקה.",
       do=show("qb-x-a", "qb-n-a")),
    KP("והמלכודת הגדולה: \"רגולרית, כי איחוד של שתי רגולריות\". המסקנה נכונה, **הנימוק** לא. $L_2$ לא רגולרית.",
       say="והמלכודת הגדולה: רגולרית, כי איחוד של שתי רגולריות. המסקנה נכונה, הנימוק לא. אֵל שתיים לא רגולרית.",
       do=show("q2-trap", "qb-x-d", "qb-n-d")),
    KP("כשהתשובות כוללות נימוק, בודקים גם את הנימוק.", hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q2-a" class="h">$1^{2n}0^k1^k\\ \\in\\ 1^*(11)^*0^*1^*$</div>'
         '<div id="q2-b" class="h" style="direction:rtl">$L_2\\subseteq L_1$, ולכן $L=L_1$ &nbsp; ✓</div></div>'
         + '<div id="q2-trap" class="h">' + st.card("q2-trapc", "trap", "⚠️ <b>מסקנה נכונה, נימוק שגוי</b>: "
                                                    "$L_2$ לא רגולרית, והאיחוד רגולרי כי $L_2\\subseteq L_1$").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q2, "qb", notes={"a": "הכלה", "c": "$L$ רגולרית", "d": "נימוק שגוי"}, small=True))

q3 = Scene("q3", "שאלה 3: חיתוך עם שוויון", [
    KP("שאלה שלישית. $L$ רגולרית, ו-$L'$ הן המילים שלה עם אותו מספר $a$ ו-$b$.",
       say="שאלה שלישית. אֵל רגולרית, ואֵל גג הן המילים שלה עם אותו מספר אֵיי ובִּי."),
    KP("$L'$ היא $L$ חיתוך שפת השוויון. שפת השוויון חסרת הקשר, ו-$L$ רגולרית, אז $L'$ חסרת הקשר.",
       say="אֵל גג היא אֵל חיתוך שפת השוויון. שפת השוויון חסרת הקשר, ואֵל רגולרית, אז אֵל גג חסרת הקשר.",
       do=show("q3-a")),
    KP("המלכודת: \"יש השוואת מונים, אז לא רגולרית\". אבל השאלה היא על **כל** $L$ רגולרית.",
       say="המלכודת: יש השוואת מונים, אז לא רגולרית. אבל השאלה היא על כל אֵל רגולרית.", do=show("q3-trap")),
    KP("אם $L=a^*$, אין בה אף $b$, ולכן נשארת רק המילה הריקה: $L'$ רגולרית. \"לא רגולרית\" נופלת.",
       say="אם אֵל שווה אֵיי כוכבית, אין בה אף בִּי, ולכן נשארת רק המילה הריקה: אֵל גג רגולרית. לא רגולרית נופלת.",
       do=show("q3-b", "qc-x-d", "qc-n-d")),
    KP("ואם $L=a^*b^*$, נשארת $\\{a^nb^n\\}$: לא סופית ולא רגולרית. אז \"סופית\" ו\"רגולרית ואינסופית\" נופלות.",
       say="ואם אֵל שווה אֵיי כוכבית בִּי כוכבית, נשארת אֵיי בחזקת אֵן, בִּי בחזקת אֵן: לא סופית ולא רגולרית. אז סופית, ורגולרית ואינסופית, נופלות.",
       do=show("q3-c", "qc-x-a", "qc-n-a", "qc-x-b", "qc-n-b")),
    KP("נשארה התשובה: חסרת הקשר, ו**ייתכן** שרגולרית. התשובה תלויה ב-$L$, והמילה \"ייתכן\" היא המפתח.",
       say="נשארה התשובה: חסרת הקשר, וייתכן שרגולרית. התשובה תלויה באֵל, והמילה ייתכן היא המפתח.",
       do=show("qc-ok-c"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px">'
         '<div id="q3-a" class="h">$L\'=L\\cap\\{w\\mid\\#_a(w)=\\#_b(w)\\}$ ✓</div>'
         '<div id="q3-b" class="h" style="direction:rtl">אם $L=a^*$, אז $L\'=\\{\\varepsilon\\}$</div>'
         '<div id="q3-c" class="h" style="direction:rtl">אם $L=a^*b^*$, אז $L\'=\\{a^nb^n\\}$</div></div>'
         + '<div id="q3-trap" class="h">' + st.card("q3-trapc", "trap", "⚠️ \"יש השוואת מונים, אז לא רגולרית\": "
                                                    "לא כש-$L$ חונקת את השוויון").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q3, "qc", notes={"a": "$a^*b^*$", "b": "$a^*b^*$", "d": "$a^*$"}, small=True))

K = 3
WK = ("0" * K + "1" * K) * K
q4 = Scene("q4", "שאלה 4: גושים בחזקה", [
    KP("שאלה אחרונה: $(0^k1^k)^k$. למשל $01$, ו-$00110011$.",
       say="שאלה אחרונה: אפס בחזקת קיי, אחת בחזקת קיי, והכול בחזקת קיי. למשל אפס אחת, ואפס אפס אחת אחת אפס אפס אחת אחת.",
       do=show("q4-w")),
    KP("המלכודת: זה נראה כמו $0^k1^k$ שחוזר על עצמו, ולכן \"חסרת הקשר ולא רגולרית\". אבל כמה פעמים חוזרים? $k$.",
       say="המלכודת: זה נראה כמו אפס בחזקת קיי, אחת בחזקת קיי, שחוזר על עצמו, ולכן חסרת הקשר ולא רגולרית. אבל כמה פעמים חוזרים? קיי.",
       do=show("q4-trap")),
    KP("כלומר אורך הגוש קשור גם למספר הגושים: השוואות שחוצות זו את זו. זו האינטואיציה. ההוכחה: למת הניפוח לחסרות הקשר.",
       do=show("q4-a")),
    KP("נוכיח בלמת הניפוח לחסרות הקשר, עם $(0^\\ell1^\\ell)^\\ell$. החלון נוגע לכל היותר בשני גושים סמוכים.",
       say="נוכיח בלמת הניפוח לחסרות הקשר, עם אפס בחזקת אֵל, אחת בחזקת אֵל, והכול בחזקת אֵל. החלון נוגע לכל היותר בשני גושים סמוכים.",
       do=show("q4-b")),
    KP("אם $y$ או $u$ מכילים גם אפס וגם אחת, ניפוח בשתיים יוצר גושים חדשים וקצרים: לא בשפה.",
       say="אם וואי או יו מכילים גם אפס וגם אחת, ניפוח בשתיים יוצר גושים חדשים וקצרים: לא בשפה.",
       do=show("q4-c")),
    KP("אחרת, ניפוח באפס מקצר או מוחק גוש. הגושים שלא נגעו בהם נשארים $\\ell$, אבל האורך הכולל השתנה: לא בשפה.",
       say="אחרת, ניפוח באפס מקצר או מוחק גוש. הגושים שלא נגעו בהם נשארים באורך קבוע הניפוח, אבל האורך הכולל השתנה: לא בשפה.",
       do=show("q4-d", "qd-ok-d")),
    KP("לא חסרת הקשר. ובפרט אינסופית ולא רגולרית, אז שלוש האחרות נופלות.",
       do=show("qd-x-a", "qd-x-b", "qd-x-c", "qd-n-c"), hold=0.6),
], stage=W.STYLE + '<div class="clo-big" style="font-size:40px"><div id="q4-w" class="h">$(0^k1^k)^k$</div></div>'
         + '<div id="q4-b" class="h">' + W.blocks("kb", WK, cw=46, ch=58,
                                                  labels=W.block_labels(WK, lambda c, k: f"${c}^\\ell$")) + "</div>"
         + W.steps("q4s", [("אורך גוש = מספר הזוגות: השוואות <b>חוצות</b>", "key"),
                           ("$y$ או $u$ מערבבים $0$ ו-$1$: עם $n=2$ נוצרים גושים חדשים", "ok"),
                           ("אחרת, עם $n=0$: גוש מתקצר או נמחק, האורך הכולל משתנה", "ok")], width=900)
           .replace('id="q4s-0"', 'id="q4-a"').replace('id="q4s-1"', 'id="q4-c"').replace('id="q4s-2"', 'id="q4-d"')
         + '<div id="q4-trap" class="h">' + st.card("q4-trapc", "trap", "⚠️ \"$0^k1^k$ שחוזר\" נשמע ח״ה; "
                                                    "אבל מספר החזרות הוא $k$").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q4, "qd", notes={"c": "השוואות חוצות"}))

recap = Scene("recap", "סיכום הקורס", [
    KP("לסיכום הקורס כולו. קודם מפשטים, ורק אז מסווגים.", do=show("c1")),
    KP("לא רגולרית: קבוצה מפרידה אינסופית, או סגירות עם רגולרית. לא חסרת הקשר: חוצה, ולמת הניפוח עם החלון.",
       do=show("c2")),
    KP("סגירות: הטבלה, והדוגמאות הנגדיות הקבועות. הכלה לא אומרת כלום על מחלקה.", do=show("c3")),
    KP("דקדוק נתון? פענחו לפני שבוחרים. ונימוק בתשובה? בדקו גם אותו. בהצלחה במבחן!", do=show("c4"), hold=0.8),
], stage=W.STYLE + W.steps("rq", [
    ('<span class="qid" style="display:inline-block">23A-B-Q19</span> נראה כמו פלינדרומים: כל המילים הזוגיות', "bad"),
    ('<span class="qid" style="display:inline-block">21S-A-Q19</span> $L_2\\subseteq L_1$: מסקנה נכונה, נימוק שגוי', "bad"),
    ('<span class="qid" style="display:inline-block">21S-A-Q13</span> $L=a^*$ או $a^*b^*$: \"ייתכן\"', "bad"),
    ('<span class="qid" style="display:inline-block">23A-A-Q22</span> $(0^k1^k)^k$: חוצה, לא ח״ה', "bad")]),
   panel=st.card("c1", "rule", "🔑 קודם <b>לפשט</b>, אחר כך לסווג")
       + st.card("c2", "rule", "🔑 לא רגולרית: קבוצה מפרידה / סגירות. לא ח״ה: חוצה / חלון")
       + st.card("c3", "rule", "🔑 טבלת הסגירויות + דוגמאות נגדיות; <b>הכלה</b> לא קובעת מחלקה")
       + st.card("c4", "trap", "⚠️ דקדוק: פענחו. נימוק בתשובה: בדקו אותו"))
recap.phrases[0].do += show(*[f"rq-{i}" for i in range(4)])

VIDEO = Video("K08", "classify", "מבחן גמר: סיווג שפות",
              [title, attack, q1, q2, q3, q4, recap],
              bank={"23A-B-Q19": "b", "21S-A-Q19": "b", "21S-A-Q13": "c", "23A-A-Q22": "d"})
