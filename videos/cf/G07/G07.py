# -*- coding: utf-8 -*-
"""G07 · אוטומט מחסנית: סיווג, מודלים ותיאוריה — video script.

Source: tools/needhelp/cf/G07.py (lesson + goal). Exam anchor: 24X-A-Q18 (cited by the lesson's classification paragraph).
Not used on purpose: the quiz items of G07 — the one-state a^{2k} PDA (19B-B-Q12), the {ε}->∅ flipped NFA, the
never-pushing PDA (24X-C-Q18 shape), the DPDA statement, the "every pop must push" model (19B-A-Q3).
The flipping counterexample here is the one of the bank explanation of 24A-C-Q8 (start accepting + ε edge).
Course convention, said every time: accepted = the whole word read, an accepting state AND an empty stack.
"""
import random
from nh import PDA, NFA, nfa_from_edges, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, pda_svg, stack, run_pda_raster, pda_path, replay, edge_strip, CSS

# ---------------------------------------------------------------- model 21S-B-Q21: no pop+push in one transition
def split(M):
    """replace every p --a,x->y--> r (x and y both letters) by p --a,x->ε--> m --ε,ε->y--> r with a new state m"""
    out, k = [], 0
    for (p_, a, pop, r, push) in M.edges:
        if pop and push:
            m = f"m{k}"
            k += 1
            out += [(p_, a, pop, m, ""), (m, "", "", r, push)]
        else:
            out.append((p_, a, pop, r, push))
    return PDA(out, M.start, M.acc)


REP = PDA([("0", "a", "", "0", "x"), ("0", "b", "x", "1", "y"), ("1", "b", "y", "1", "y"), ("1", "a", "y", "2", ""),
           ("2", "a", "x", "2", "")], "0", {"2"})
assert split(REP).lang("ab", 7) == REP.lang("ab", 7) and REP.lang("ab", 7)
random.seed(11)
EDGES = [(s, a, pop, r, push) for s in "01" for a in ("", "a", "b") for pop in ("", "x") for r in "01" for push in ("", "x", "y")]
for _ in range(150):
    Mr = PDA(random.sample(EDGES, random.randint(2, 7)), "0", {s for s in "01" if random.random() < 0.5})
    assert split(Mr).lang("ab", 5) == Mr.lang("ab", 5)
# the split picture (one edge)
ONE = PDA([("0", "a", "x", "1", "y")], "0", {"1"})
TWO = split(ONE)
assert [e for e in TWO.edges] == [("0", "a", "x", "m0", ""), ("m0", "", "", "1", "y")]

# ---------------------------------------------------------------- flipping (bank explanation of 24A-C-Q8)
NA = nfa_from_edges("a", [("0", "", "1")], "0", {"0"})
NB = nfa_from_edges("a", [("0", "", "1")], "0", {"1"})
assert NA.accepts("") and NB.accepts("")              # ε accepted before AND after flipping
assert NA.lang(5) == {""} and NB.lang(5) == {""}       # so L(B) is not the complement of L(A)

# ---------------------------------------------------------------- exam 24X-A-Q18 (transcribed from the figure)
Q = BANK["24X-A-Q18"]
E = PDA([("0", "0", "", "0", ""), ("0", "1", "", "1", "Z"), ("1", "0", "", "1", ""), ("1", "1", "", "2", ""),
         ("2", "0", "", "2", ""), ("2", "1", "Z", "3", ""), ("3", "0", "", "3", ""), ("3", "1", "", "3", "")], "0", {"3"})
assert E.lang("01", 9) == {w for w in words("01", 9) if w.count("1") >= 3}      # Σ*1Σ*1Σ*1Σ*
assert Q["correctId"] == "b"
assert any(len(w) == 9 for w in E.lang("01", 9))                                  # infinite (words of every length >= 3)
assert not E.accepts("11") and E.accepts("111")
XW = "1011"
PX = pda_path(E, XW)
CX = replay(E, XW, PX)
assert CX[-1] == ("3", 4, "", XW)
RINGS = [("0", 95, 45, 32), ("1", 290, 45, 32), ("2", 487, 45, 32), ("3", 683, 45, 32)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה: שאלות התיאוריה על אוטומט מחסנית. סיווג השפה שלו, ומודלים מומצאים."),
    p("כמעט תמיד הן נפתרות בשאלה אחת: האם אפשר לחקות? או בדוגמה נגדית קטנה.", hold=0.4),
], stage=CSS + '<div class="kicker">G07 · דקדוקים ואוטומט מחסנית</div><h1>סיווג, מודלים ותיאוריה</h1>'
         '<p>להכריע שאלות מודל: מה היפוך מצבים נותן, מה מחלקת השפות של מודל מוגבל, ואיך מסווגים L(M).</p>',
   layout="title")

classify = Scene("classify", "סיווג L(M)", [
    p("נתון אוטומט מחסנית, ושואלים: השפה שלו סופית? רגולרית? חסרת הקשר?"),
    p("דבר אחד בטוח: **כל אוטומט מחסנית מקבל שפה חסרת הקשר**. לכן לא חסרת הקשר נפסלת תמיד.", do=show("k1", "lv-cfl")),
    p("נשאר להכריע: רגולרית, או לא.", do=show("lv-reg")),
    p("וזו המלכודת: יש מחסנית, אז קופצים ללא רגולרית. אבל אוטומט מחסנית יכול לקבל גם שפה רגולרית, ואפילו סופית.",
      do=show("k2")),
    p("לכן קודם **מפענחים** את $L(M)$: מה הוא קורא, מה הוא דוחף, ומתי המחסנית מתרוקנת. ורק אז מסווגים.",
      say="לכן קודם מפענחים את השפה: מה האוטומט קורא, מה הוא דוחף, ומתי המחסנית מתרוקנת. ורק אז מסווגים.",
      do=show("k3"), hold=0.4),
], stage='<div style="display:flex;flex-direction:column;gap:18px;align-items:center;font-size:40px">'
         '<div class="cf-chip ok" style="font-size:38px">סופית</div><div>⊂</div>'
         '<div id="lv-reg" class="cf-chip h" style="font-size:38px;color:var(--warn)">רגולרית?</div><div>⊂</div>'
         '<div id="lv-cfl" class="cf-chip ok h" style="font-size:38px">חסרת הקשר ✓</div></div>',
   panel=st.card("k1", "rule", "🔑 אם יש אוטומט מחסנית, אז השפה <b>חסרת הקשר</b>")
       + st.card("k2", "trap", "⚠️ יש מחסנית ≠ לא רגולרית")
       + st.card("k3", "rule", "🔑 קודם מפענחים את $L(M)$, אחר כך מסווגים"))

N2 = {"0": "q_0", "1": "q_1", "m0": "m"}
POSONE = {"0": (200, 150), "1": (760, 150)}
POSTWO = {"0": (150, 150), "m0": (480, 150), "1": (810, 150)}
models = Scene("models", "מודלים מומצאים", [
    p("סוג שני: השאלה ממציאה מודל עם מגבלה, ושואלת איזו מחלקת שפות הוא מקבל."),
    p("השיטה: האם המודל הרגיל יכול **לחקות** את החדש? והאם החדש יכול לחקות את הרגיל?", do=show("j1")),
    p("שני הכיוונים: שקול לחסרות הקשר. ואם המגבלה משתקת את המחסנית: רגולרי.", do=show("j2")),
    p("דוגמה: מודל שבו **אסור** באותו מעבר גם לשלוף וגם לדחוף.", do=show("mo-one")),
    p("החדש הוא מקרה פרטי של הרגיל, אז הרגיל מחקה אותו. ולהפך?"),
    p("מעבר כמו $a,x\\to y$ מפצלים לשניים, דרך מצב ביניים חדש:",
      say="מעבר כמו אֵיי, אִקְס, חץ, וַואי, מפצלים לשניים, דרך מצב ביניים חדש.", do=show("mo-two")),
    p("קודם $a,x\\to\\varepsilon$: קוראים ושולפים. אחר כך $\\varepsilon,\\varepsilon\\to y$: דוחפים.",
      say="קודם אֵיי, אִקְס, חץ, אפסילון: קוראים ושולפים. אחר כך אפסילון, אפסילון, חץ, וַואי: דוחפים.",
      do=show("tw-he-0-m0", "tw-hl-0")),
    p("אותה ריצה בדיוק, ולכן המודל שקול לחסרות הקשר.", do=hide("tw-he-0-m0", "tw-hl-0") + show("j3")),
    p("דוגמה נוספת מהבנק: מודל שמקבל אם יש ריצה מקבלת **וגם** ריצה לא מקבלת. מוסיפים מצב לא מקבל, ומעבר $\\varepsilon$ אליו מכל מצב מקבל.",
      say="דוגמה נוספת מהבנק: מודל שמקבל אם יש ריצה מקבלת וגם ריצה לא מקבלת. מוסיפים מצב לא מקבל, ומעבר אפסילון אליו מכל מצב מקבל.",
      do=show("j4")),
    p("כך המודל החדש מקבל כל שפה ח״ה; הכיוון השני: הדרישה הנוספת רק מצמצמת, ולפי המחוון זו בדיוק מחלקת הח״ה.",
      say="כך המודל החדש מקבל כל שפה חסרת הקשר. הכיוון השני: הדרישה הנוספת רק מצמצמת, ולפי המחוון זו בדיוק מחלקת השפות חסרות ההקשר.",
      hold=0.4),
], stage='<div id="mo-one" class="h">' + pda_svg("on", ONE, POSONE, {"0": "q_0", "1": "q_1"}, w=960, h=230) + '</div>'
         '<div id="mo-two" class="h">' + pda_svg("tw", TWO, POSTWO, N2, w=960, h=230) + '</div>',
   panel=st.card("j1", "rule", "🔑 שאלו: מי יכול <b>לחקות</b> את מי?")
       + st.card("j2", "plain", "חיקוי בשני הכיוונים: ח״ה. מחסנית משותקת: רגולרי")
       + st.card("j3", "plain", "אסור לשלוף ולדחוף יחד: מפצלים, ולכן <b>ח״ה</b> (21S-B-Q21)")
       + st.card("j4", "plain", "ריצה מקבלת וגם לא מקבלת: מצב לא מקבל חדש, ולכן <b>ח״ה</b> (19B-B-Q20)"))

NF = {"0": "q_0", "1": "q_1"}
POSN = {"0": (230, 150), "1": (690, 150)}
flip = Scene("flip", "היפוך מצבים מקבלים", [
    p("שאלה תיאורטית נפוצה: הופכים כל מצב מקבל לדוחה, וכל דוחה למקבל. האם מקבלים את המשלים?"),
    p("באס״ד שלם: כן. לכל מילה יש ריצה **אחת**, והיא נגמרת במקבל או בדוחה.", do=show("f1")),
    p("אבל באסל״ד לא. הנה אסל״ד: $q_0$ התחלתי ומקבל, ומעבר $\\varepsilon$ ל-$q_1$ הדוחה.",
      say="אבל באסלאד לא. הנה אסלאד: קיו אפס התחלתי ומקבל, ומעבר אפסילון לקיו אחת הדוחה.", do=show("fa")),
    p("$\\varepsilon$ מתקבלת: נשארים ב-$q_0$.", say="אפסילון מתקבלת: נשארים בקיו אפס.", do=show("na-hs-0")),
    p("עכשיו הופכים: $q_0$ דוחה, $q_1$ מקבל.", say="עכשיו הופכים: קיו אפס דוחה, קיו אחת מקבל.",
      do=hide("na-hs-0", "fa") + show("fb")),
    p("ו-$\\varepsilon$ **עדיין** מתקבלת: במעבר $\\varepsilon$ מגיעים ל-$q_1$, שעכשיו מקבל.",
      say="ואפסילון עדיין מתקבלת: במעבר אפסילון מגיעים לקיו אחת, שעכשיו מקבל.", do=show("nb-hs-1", "nb-he-0-1")),
    p("מילה שמתקבלת בשניהם: זה לא משלים. ובאוטומט מחסנית, שגם הוא לא דטרמיניסטי, אותו דבר.",
      do=show("f2")),
    p("ובכלל, שפות חסרות הקשר לא סגורות למשלים.", do=show("f3"), hold=0.4),
], stage='<div class="swap cf-c" style="--swap-h:300px">'
         '<div id="fa" class="h"><div class="cf-cap">לפני ההיפוך</div>' + st.dfa_svg("na", NA, POSN, NF, w=920, h=230, scale=1.0) + '</div>'
         '<div id="fb" class="h"><div class="cf-cap">אחרי ההיפוך</div>' + st.dfa_svg("nb", NB, POSN, NF, w=920, h=230, scale=1.0) + '</div></div>'
         '<div class="cf-words"><span>$\\varepsilon\\in L(A)$</span><span id="f2" class="h">$\\varepsilon\\in L(B)$: לא משלים</span></div>',
   panel=st.card("f1", "rule", "🔑 היפוך מקבלים = משלים <b>רק באס״ד שלם</b>")
       + st.card("f3", "plain", "ח״ה לא סגורות למשלים (24A-C-Q8)"))

RING = {s: s for s in "0123"}
runX, cfX, leftX = run_pda_raster("ex", E, XW, PX, "xt", "xs", "xl", RING,
                                  lead="נריץ את $1011$. מתחילים במצב השמאלי, עם מחסנית ריקה.",
                                  lead_say="נריץ את אחת אפס אחת אחת. מתחילים במצב השמאלי, עם מחסנית ריקה.")
runX[0].do += show("xt-box") + hide("xdec")
opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן: סווגו את השפה של האוטומט הזה, מעל $\\{0,1\\}$.",
      say="שאלה ממבחן: סווגו את השפה של האוטומט הזה, מעל אפס ואחת."),
    p("קודם הבטוח: יש אוטומט מחסנית, ולכן השפה חסרת הקשר. לא חסרת הקשר נפסלת.", do=show("q-x-d", "q-n-d")),
    p("עכשיו מפענחים. בכל מצב יש לולאת $0$ שלא נוגעת במחסנית: אפסים לא משנים כלום.",
      say="עכשיו מפענחים. בכל מצב יש לולאת אפס שלא נוגעת במחסנית: אפסים לא משנים כלום.", do=show("d1")),
    p("ה-$1$ הראשונה דוחפת $Z$, השנייה לא נוגעת, והשלישית שולפת את $Z$ ומגיעה למצב המקבל.",
      say="האחת הראשונה דוחפת זֶד, השנייה לא נוגעת, והשלישית שולפת את הזֶד ומגיעה למצב המקבל.",
      do=show("d2", "ex-ring-3")),
    p("ושם קוראים כל המשך, בלי לגעת במחסנית. המחסנית ריקה, והמצב מקבל.", do=show("d3")),
    p("כלומר $L(M)$ היא כל המילים עם **לפחות שלושה** $1$: $\\Sigma^*1\\Sigma^*1\\Sigma^*1\\Sigma^*$.",
      say="כלומר השפה היא כל המילים עם לפחות שלוש אחדות.", do=show("d4")),
    p("זו שפה רגולרית: ביטוי רגולרי. והיא אינסופית: אפשר להוסיף כמה אפסים שרוצים.",
      do=show("q-x-a", "q-n-a")),
    p("והמלכודת: יש מחסנית, אז חסרת הקשר ולא רגולרית. אבל המחסנית מחזיקה לכל היותר $Z$ אחד; את הספירה עושים המצבים.",
      do=show("xtrap", "q-x-c", "q-n-c")),
    *runX,
    p("קראנו הכל, מצב מקבל, מחסנית ריקה: $1011$ מתקבלת. התשובה: רגולרית ואינסופית.",
      say="קראנו הכל, מצב מקבל, מחסנית ריקה: אחת אפס אחת אחת מתקבלת. התשובה: רגולרית ואינסופית.",
      do=show("xv", "q-ok-b"), hold=0.6),
], stage=st.raster("ex", "images/exams/24X-A-Q18.png", 960, (746, 181), rings=RINGS)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:640px"><div class="swap cf-c" style="--swap-h:420px">'
           '<div id="xdec"><div id="d1" class="cf-mid h">$0$: לא נוגעת במחסנית, בכל מצב</div>'
           '<div id="d2" class="cf-mid h">$1$ ראשונה: דוחפת $Z$ · שלישית: שולפת $Z$</div>'
           '<div id="d3" class="cf-mid h">במצב המקבל: כל המשך</div>'
           '<div id="d4" class="cf-eq cf-ltr h">$L(M)=\\Sigma^*1\\Sigma^*1\\Sigma^*1\\Sigma^*$</div>'
         + st.card("xtrap", "trap", "⚠️ מחסנית ≠ לא רגולרית: המחסנית מחזיקה לכל היותר $Z$ אחד; את הספירה עושים המצבים") + '</div>'
           f'<div id="xt-box" class="h">{st.tape("xt", XW)}{edge_strip("xl", E, PX)}'
           '<div id="xv" class="verdict ok h">מצב מקבל + מחסנית ריקה ✓</div></div>'
           '</div></div>'
         + stack("xs", [c[2] for c in CX]) + '</div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>נתון האוטומט-מחסנית $M$ שמשמאל, מעל הא״ב הבינארי. איזו טענה נכונה?</div>'
       + st.options("q", opts, notes={"a": "אינסופית", "c": "רגולרית", "d": "יש אוטומט מחסנית"}))

recap = Scene("recap", "סיכום", [
    p("לסיכום: אוטומט מחסנית מקבל שפה חסרת הקשר, אבל זה לא אומר שהיא לא רגולרית. מפענחים קודם.", do=show("c1")),
    p("במודל מומצא שואלים: מי מחקה את מי? ומחסנית משותקת נותנת רגולרי.", do=show("c2")),
    p("היפוך מצבים מקבלים נותן משלים רק באס״ד שלם.", do=show("c3")),
    p("ותמיד: מתקבלת פירושו מצב מקבל וגם מחסנית ריקה. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=st.raster("rc", "images/exams/24X-A-Q18.png", 960, (746, 181)),
   panel=st.card("c1", "rule", "🔑 אוטומט מחסנית: ח״ה; פענחו לפני \"לא רגולרית\"")
       + st.card("c2", "rule", "🔑 מודל מומצא: אם יש חיקוי בשני הכיוונים, אז ח״ה")
       + st.card("c3", "rule", "🔑 היפוך מקבלים = משלים רק באס״ד שלם")
       + st.card("c4", "trap", "⚠️ מתקבלת = מצב מקבל <b>וגם</b> מחסנית ריקה"))

VIDEO = Video("G07", "cf", "אוטומט מחסנית: סיווג ומודלים",
              [title, classify, models, flip, exam, recap],
              bank={"24X-A-Q18": "b"})
