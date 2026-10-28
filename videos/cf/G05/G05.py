# -*- coding: utf-8 -*-
"""G05 · אוטומט מחסנית: ריצה, וההגדרה של ״מתקבלת״ — video script.

Source: tools/needhelp/cf/G05.py (lesson + goal). Exam anchor: 23A-B-Q23 (cited by the lesson's parity filter).
Not used on purpose: the quiz machines of G05 (a^n b^n with an ε edge, the 24X-C-Q13 machine — so the lesson's example
is described but not run —, the Z push/pop ε machine, the one-state a,ε→A machine, the replace-edge machine).
Course convention, said every time: accepted = the whole word read, an accepting state AND an empty stack.
Every machine and run below is checked with lib.PDA (runs are replayed edge by edge).
"""
from nh import PDA, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import (p, pda_svg, stack, stack_do, run_pda, run_pda_raster, pda_path, replay, checks, edge_strip,
                  CSS)

# ---------------------------------------------------------------- worked example (new): a^n c a^n
M1 = PDA([("0", "a", "", "0", "A"), ("0", "c", "", "1", ""), ("1", "a", "A", "1", "")], "0", {"1"})
assert M1.lang("ac", 8) == {"a" * n + "c" + "a" * n for n in range(4)}
W1, W2 = "aacaa", "aaca"
P1 = pda_path(M1, W1)
assert P1 is not None and [M1.edges[k][1] for k in P1] == list(W1)
assert not M1.accepts(W2) and M1.accepts(W2, require_empty=False)       # accepting state, stack not empty
P2 = [0, 0, 1, 2]                                                        # the only run that reads all of aaca
C2 = replay(M1, W2, P2)
assert C2[-1] == ("1", 4, "A", W2) and "1" in M1.acc
assert not M1.accepts("ab")                                              # b is read on no edge
N1 = {"0": "q_0", "1": "q_1"}
POS1 = {"0": (230, 230), "1": (670, 230)}
C1 = replay(M1, W1, P1)
assert C1[-1][0] in M1.acc and C1[-1][2] == "" and C1[-1][1] == len(W1)

# ---------------------------------------------------------------- exam 23A-B-Q23 (transcribed from the figure)
Q = BANK["23A-B-Q23"]
E = PDA([("0", "a", "b", "0", ""), ("0", "a", "", "0", "a"), ("0", "b", "a", "0", ""), ("0", "b", "", "0", "b"),
         ("0", "", "", "1", "")], "0", {"1"})
assert E.lang("ab", 8) == {w for w in words("ab", 8) if w.count("a") == w.count("b")}   # bank: #a = #b
XA, XB = "aabbba", "ababb"
assert E.accepts(XA) and not E.accepts(XB)
assert Q["correctId"] == "c"                                             # first belongs, second does not
assert E.accepts(XB, require_empty=False)                                # the trap: "accepting state only" would accept it
# parity: every loop reads one letter and changes the height by exactly 1
assert all((e[1] != "") and ((e[2] != "") != (e[4] != "")) for e in E.edges if e[0] == e[3])
PE = pda_path(E, XA)
CE = replay(E, XA, PE)
assert CE[-1] == ("1", 6, "", XA)
RINGS = [("0", 160, 232, 62), ("1", 490, 232, 62)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה נכיר את האוטומט מחסנית: איך קוראים קשת, ואיך מריצים אותו על מילה."),
    p("ונלמד את הכלל הכי חשוב בפרק: מתי מילה מתקבלת.", hold=0.4),
], stage=CSS + '<div class="kicker">G05 · דקדוקים ואוטומט מחסנית</div><h1>אוטומט מחסנית: ריצה ו״מתקבלת״</h1>'
         '<p>לקרוא קשת $\\sigma,x\\to y$, להריץ אוטומט מחסנית על מילה, ולזכור שמתקבלת = מצב מקבל וגם מחסנית ריקה.</p>',
   layout="title")

TAB = ('<table class="delta" dir="rtl" style="font-size:38px"><thead><tr><th>על הקשת</th><th>משמעות</th></tr></thead><tbody>'
       '<tr id="tb-1" class="h"><td dir="ltr">$a,\\varepsilon\\to A$</td><td>קרא $a$, <b>דחוף</b> $A$</td></tr>'
       '<tr id="tb-2" class="h"><td dir="ltr">$b,A\\to\\varepsilon$</td><td>קרא $b$, <b>שלוף</b> $A$ (רק אם $A$ בראש)</td></tr>'
       '<tr id="tb-3" class="h"><td dir="ltr">$a,x\\to y$</td><td>קרא $a$, <b>החלף</b> $x$ ב-$y$</td></tr>'
       '<tr id="tb-4" class="h"><td dir="ltr">$\\varepsilon,\\varepsilon\\to\\varepsilon$</td><td>מעבר חינם בין מצבים</td></tr>'
       '<tr id="tb-5" class="h"><td dir="ltr">$a,\\varepsilon\\to\\varepsilon$</td><td>קרא $a$ בלי לגעת במחסנית</td></tr>'
       '</tbody></table>')
concept = Scene("concept", "מה זה אוטומט מחסנית", [
    p("אוטומט מחסנית הוא אסל״ד, עם תוספת אחת: **מחסנית**.", do=show("k1")),
    p("מחסנית היא זיכרון שדוחפים אליו ושולפים ממנו **רק מהראש**: מה שנכנס אחרון יוצא ראשון.", do=show("k2")),
    p("היא מתחילה **ריקה**, והגודל שלה לא חסום.", do=show("k3")),
    p("על כל קשת כתוב $\\sigma,x\\to y$: קרא $\\sigma$ מהקלט, שלוף $x$ מראש המחסנית, ודחוף $y$.",
      say="על כל קשת כתוב סיגמא, אִקְס, חץ, וַואי: קרא סיגמא מהקלט, שלוף אִקְס מראש המחסנית, ודחוף וַואי.",
      do=show("k4")),
    p("$a,\\varepsilon\\to A$: קרא $a$, ודחוף $A$.", say="אֵיי, אפסילון, חץ, אֵיי גדולה: קרא אֵיי, ודחוף אֵיי גדולה.",
      do=show("tb-1")),
    p("$b,A\\to\\varepsilon$: קרא $b$ ושלוף $A$. אפשר רק אם $A$ באמת בראש המחסנית.",
      say="בִּי, אֵיי גדולה, חץ, אפסילון: קרא בִּי ושלוף אֵיי גדולה. אפשר רק אם אֵיי גדולה באמת בראש המחסנית.",
      do=show("tb-2")),
    p("$a,x\\to y$ מחליף את $x$ ב-$y$: הגובה **לא משתנה**.",
      say="אֵיי, אִקְס, חץ, וַואי, מחליף את אִקְס בוַואי: הגובה לא משתנה.", do=show("tb-3")),
    p("$\\varepsilon,\\varepsilon\\to\\varepsilon$ הוא מעבר חינם, ו-$a,\\varepsilon\\to\\varepsilon$ קורא בלי לגעת במחסנית.",
      say="אפסילון, אפסילון, חץ, אפסילון, הוא מעבר חינם. ואֵיי, אפסילון, חץ, אפסילון, קורא בלי לגעת במחסנית.",
      do=show("tb-4", "tb-5"), hold=0.4),
], stage=TAB,
   panel=st.card("k1", "plain", "<b>אוטומט מחסנית</b> = אסל״ד + <b>מחסנית</b>")
       + st.card("k2", "plain", "דוחפים ושולפים <b>רק מהראש</b>")
       + st.card("k3", "plain", "מתחילה <b>ריקה</b>, גודל לא חסום")
       + st.card("k4", "rule", "🔑 $\\sigma,x\\to y$: קרא $\\sigma$, שלוף $x$, דחוף $y$"))

rule = Scene("rule", "מתי מילה מתקבלת", [
    p("ועכשיו הכלל הכי חשוב בפרק, מוסכמת הקורס.", do=show("r0")),
    p("מילה מתקבלת אם יש ריצה שקוראת את **כל המילה**,", do=show("r1")),
    p("נגמרת **במצב מקבל**,", do=show("r2")),
    p("**וגם** עם **מחסנית ריקה**.", do=show("r3")),
    p("חסר אחד מהשלושה: המילה לא מתקבלת. גם אם כל המצבים באוטומט מקבלים.", do=show("r4")),
    p("והאוטומט לא דטרמיניסטי: מספיקה **ריצה אחת** מקבלת.", do=show("r5"), hold=0.4),
], stage='<div id="r0" class="h" style="display:flex;flex-direction:column;gap:20px;align-items:center">'
         '<div id="r1" class="cf-chip ok h" style="font-size:40px">קראנו את כל המילה</div>'
         '<div id="r2" class="cf-chip ok h" style="font-size:40px">+ מצב מקבל</div>'
         '<div id="r3" class="cf-chip ok h" style="font-size:40px">+ מחסנית ריקה</div>'
         '<div id="r4" class="verdict ok h" style="font-size:44px">= מתקבלת</div></div>',
   panel=st.card("r5", "rule", "🔑 <b>מוסכמת הקורס:</b> מתקבלת = קוראת את כל המילה, נגמרת <b>במצב מקבל</b> "
                 "<b>וגם</b> עם <b>מחסנית ריקה</b>. מספיקה ריצה אחת כזאת."))

ALL1 = [c[2] for c in replay(M1, W1, P1)] + [c[2] for c in C2]
run1, cf1, left1 = run_pda("m1", M1, W1, P1, N1, tp="t1", stk="s1", fast=False,
                           lead="נריץ על $aacaa$. מתחילים ב-$q_0$, והמחסנית ריקה.")
run1[0].do += show("t1-box")
run2, cf2, left2 = run_pda("m1", M1, W2, P2, N1, tp="t2", stk="s1", fast=True,
                           lead="עכשיו $aaca$. שוב מ-$q_0$, עם מחסנית ריקה.",
                           clear=left1 + ["t1-box", "v1-c1", "v1-c2", "v1-v"])
run2[0].do += show("t2-box") + stack_do("s1", cf1[-1][2], "")
example = Scene("example", "דוגמה: ריצה עם מחסנית", [
    p("אוטומט חדש. ב-$q_0$ כל $a$ דוחפת $A$. האות $c$ מעבירה ל-$q_1$, ושם כל $a$ שולפת $A$.",
      say="אוטומט חדש. בקיו אפס כל אֵיי דוחפת אֵיי גדולה. האות סִי מעבירה לקיו אחת, ושם כל אֵיי שולפת אֵיי גדולה."),
    *run1,
    p("קראנו הכל. אנחנו ב-$q_1$, שהוא מקבל,", do=show("v1-c1")),
    p("והמחסנית ריקה. שני התנאים מתקיימים: $aacaa$ מתקבלת.", say="והמחסנית ריקה. שני התנאים מתקיימים: אֵיי אֵיי סִי אֵיי אֵיי מתקבלת.",
      do=show("v1-c2", "v1-v"), hold=0.4),
    *run2,
    p("קראנו הכל, ואנחנו ב-$q_1$ המקבל.", do=show("v2-c1")),
    p("אבל נשארה $A$ במחסנית. המחסנית לא ריקה, ולכן $aaca$ **לא מתקבלת**.",
      say="אבל נשארה אֵיי גדולה במחסנית. המחסנית לא ריקה, ולכן אֵיי אֵיי סִי אֵיי לא מתקבלת.",
      do=show("v2-c2", "v2-v")),
    p("זה בדיוק המקום שבו טועים: מצב מקבל לבד **לא מספיק**. השפה כאן היא $a^nca^n$.",
      say="זה בדיוק המקום שבו טועים: מצב מקבל לבד לא מספיק. השפה כאן היא אֵיי בחזקת אֵן, סִי, אֵיי בחזקת אֵן.",
      do=show("ex-trap"), hold=0.5),
], stage=pda_svg("m1", M1, POS1, N1, w=900, h=300, scale=1.15)
         + '<div class="cf-row" style="align-items:center;gap:50px">'
           '<div class="cf-col"><div class="swap cf-c" style="--swap-h:200px;width:520px">'
           f'<div id="t1-box" class="h">{st.tape("t1", W1)}{checks("v1", True, True)}</div>'
           f'<div id="t2-box" class="h">{st.tape("t2", W2)}{checks("v2", True, False)}</div></div></div>'
         + stack("s1", ALL1) + '</div>',
   panel=st.card("ex-r", "rule", "🔑 מתקבלת = כל המילה + מצב מקבל + <b>מחסנית ריקה</b>").replace(' h"', '"')
       + st.card("ex-trap", "trap", "⚠️ מצב מקבל עם מחסנית לא ריקה: <b>לא מתקבלת</b>"))

method = Scene("method", "בדיקות מהירות", [
    p("לפני שמריצים, שלוש בדיקות מהירות שפוסלות מילים.", do=show("f0")),
    p("אחת: **אות שלא נקראת באף קשת**. באוטומט שראינו אין קשת שקוראת $b$, ולכן כל מילה עם $b$ נדחית.",
      say="אחת: אות שלא נקראת באף קשת. באוטומט שראינו אין קשת שקוראת בִּי, ולכן כל מילה עם בִּי נדחית.", do=show("f1")),
    p("שתיים: **זוגיות**. אם כל מעבר קורא אות אחת ומשנה את הגובה בדיוק באחד, מילה באורך אי-זוגי לא תרוקן את המחסנית.",
      do=show("f2")),
    p("שלוש: **קשת מתה**. קשת ששולפת סימן שאף פעם לא נדחף, אי אפשר לעבור בה.", do=show("f3")),
    p("ואם הבדיקות לא הכריעו, עוקבים אחרי המחסנית צעד אחר צעד, ובסוף בודקים: מצב מקבל **וגם** מחסנית ריקה.",
      do=show("f4"), hold=0.4),
], stage=pda_svg("mm", M1, POS1, N1, w=900, h=300, scale=1.15),
   panel=st.card("f0", "plain", "<b>שיטה: האם $w\\in L(M)$?</b>")
       + st.card("f1", "plain", "<b>1.</b> אם אות לא נקראת באף קשת, אז מילה איתה נדחית")
       + st.card("f2", "plain", "<b>2.</b> זוגיות: אם כל מעבר קורא אות אחת ומשנה גובה ב-$1$, אז אורך אי-זוגי נדחה")
       + st.card("f3", "plain", "<b>3.</b> קשת מתה: שולפת סימן שלא נדחף")
       + st.card("f4", "rule", "🔑 <b>4.</b> מעקב, ובסוף: מצב מקבל <b>וגם</b> מחסנית ריקה"))

RING = {"0": "0", "1": "1"}
runE, cfE, leftE = run_pda_raster("ex", E, XA, PE, "xt", "xs", "xl", RING,
                                  lead="נריץ את $aabbba$. מתחילים במצב השמאלי, עם מחסנית ריקה.")
runE[0].do += show("xt-box")
opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן. מצב אחד עם ארבע לולאות, ומעבר $\\varepsilon$ למצב המקבל, בלי לגעת במחסנית.",
      say="שאלה ממבחן. מצב אחד עם ארבע לולאות, ומעבר אפסילון למצב המקבל, בלי לגעת במחסנית.",
      do=show("ex-ring-0")),
    p("על $a$: שולפים $b$ אם היא בראש, או דוחפים $a$. ועל $b$ להפך: שולפים $a$, או דוחפים $b$.",
      say="על אֵיי: שולפים בִּי אם היא בראש, או דוחפים אֵיי. ועל בִּי להפך: שולפים אֵיי, או דוחפים בִּי."),
    p("קודם בדיקת זוגיות: כל לולאה קוראת אות אחת ומשנה את הגובה בדיוק באחד.", do=show("par")),
    p("$ababb$ באורך חמש. אחרי מספר אי-זוגי של צעדים הגובה אי-זוגי, ולא יכול להיות אפס.",
      say="אֵיי בִּי אֵיי בִּי בִּי באורך חמש. אחרי מספר אי-זוגי של צעדים הגובה אי-זוגי, ולא יכול להיות אפס."),
    p("לכן $ababb$ לא מתקבלת: שתי האפשרויות שאומרות שהיא שייכת נפסלות.",
      say="לכן אֵיי בִּי אֵיי בִּי בִּי לא מתקבלת: שתי האפשרויות שאומרות שהיא שייכת נפסלות.",
      do=show("q-x-a", "q-x-b")),
    p("וזו המלכודת: $ababb$ **כן** מגיעה למצב המקבל, אבל עם $b$ במחסנית.",
      say="וזו המלכודת: אֵיי בִּי אֵיי בִּי בִּי כן מגיעה למצב המקבל, אבל עם בִּי במחסנית.", do=show("xtrap")),
    p("מי ששוכח את המחסנית הריקה, בוחר שהיא שייכת. בקורס: מצב מקבל **וגם** מחסנית ריקה.", hold=0.3),
    *runE,
    p("קראנו הכל, אנחנו במצב המקבל, והמחסנית ריקה: $aabbba$ מתקבלת.",
      say="קראנו הכל, אנחנו במצב המקבל, והמחסנית ריקה: אֵיי אֵיי בִּי בִּי בִּי אֵיי מתקבלת.",
      do=show("xv", "q-x-d")),
    p("התשובה: $aabbba$ שייכת, ו-$ababb$ לא שייכת.",
      say="התשובה: אֵיי אֵיי בִּי בִּי בִּי אֵיי שייכת, ואֵיי בִּי אֵיי בִּי בִּי לא שייכת.", do=show("q-ok-c"), hold=0.6),
], stage=st.raster("ex", "images/exams/23A-B-Q23.png", 500, (563, 461), rings=RINGS)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:600px"><div class="swap cf-c" style="--swap-h:230px">'
           '<div id="par" class="h">' + st.card("parc", "plain", "כל לולאה: אות אחת, וגובה משתנה ב-$1$. לכן אם האורך אי-זוגי, אז המחסנית לא מתרוקנת").replace(' h"', '"')
         + st.card("xtrap", "trap", "⚠️ $ababb$ מגיעה למצב המקבל, אבל עם $b$ במחסנית: <b>לא מתקבלת</b>") + '</div>'
           f'<div id="xt-box" class="h">{st.tape("xt", XA)}{edge_strip("xl", E, PE)}'
           '<div id="xv" class="verdict ok h">מצב מקבל + מחסנית ריקה: מתקבלת ✓</div></div></div></div>'
         + stack("xs", [c[2] for c in CE]) + '</div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>נתון האוטומט-מחסנית $M$ שמשמאל. איזו טענה נכונה?</div>'
       + '<div class="cf-sm">' + st.options("q", opts) + '</div>')
# the run hides the parity/trap box
runE[0].do += hide("par")

recap = Scene("recap", "סיכום", [
    p("לסיכום: $\\sigma,x\\to y$ פירושו קרא, שלוף, דחוף.", say="לסיכום: סיגמא, אִקְס, חץ, וַואי, פירושו קרא, שלוף, דחוף.",
      do=show("c1")),
    p("מילה מתקבלת אם הריצה קוראת הכל, נגמרת במצב מקבל, **וגם** המחסנית ריקה.", do=show("c2")),
    p("לפני שמריצים: אות שלא נקראת, זוגיות, וקשת מתה.", do=show("c3")),
    p("ומצב מקבל עם מחסנית לא ריקה: נדחית. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=pda_svg("rc", M1, POS1, N1, w=900, h=300, scale=1.15),
   panel=st.card("c1", "rule", "🔑 $\\sigma,x\\to y$: קרא, שלוף, דחוף")
       + st.card("c2", "rule", "🔑 מתקבלת = כל המילה + מצב מקבל + <b>מחסנית ריקה</b>")
       + st.card("c3", "rule", "🔑 בדיקות: אות שלא נקראת, זוגיות, קשת מתה")
       + st.card("c4", "trap", "⚠️ מצב מקבל עם מחסנית לא ריקה: נדחית"))

VIDEO = Video("G05", "cf", "אוטומט מחסנית: ריצה ו״מתקבלת״",
              [title, concept, rule, example, method, exam, recap],
              bank={"23A-B-Q23": "c"})
