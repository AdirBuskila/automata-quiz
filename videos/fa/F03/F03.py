# -*- coding: utf-8 -*-
"""F03 · אסל״ד, מסעי ε והשוואת שפות — video script (build: tools/video/vid.py F03).

Source: tools/needhelp/fa/F03.py (lesson + goal). Exam anchor: 21S-A-Q20 (cited by the lesson, not by the quiz).
Not used on purpose: the quiz machines N1 (third letter from the end = MQ1-Q6), N2, UA/UB (= 24A-C-Q3), N3, M1/M2.
New machines: NE (ends with ab) for the run sets, NX (a*b* with one ε move) for the ε-closure.
"""
from nh import nfa_from_edges, dfa_table, rx, words
from vid import P, Scene, Video, show, hide, BANK
import lexicon
import stage as st
import w_fa as fa

# ---------------------------------------------------------------- machines (verified)
NE = nfa_from_edges("ab", [("0", "a", "0"), ("0", "b", "0"), ("0", "a", "1"), ("1", "b", "2")], "0", {"2"})
assert NE.lang(8) == {w for w in words("ab", 8) if w.endswith("ab")}
SE1 = fa.nfa_sets(NE, "bbab")
assert SE1 == [{"0"}, {"0"}, {"0"}, {"0", "1"}, {"0", "2"}] and NE.accepts("bbab")
SE2 = fa.nfa_sets(NE, "aba")
assert SE2[-1] == {"0", "1"} and not NE.accepts("aba")
# one accepting path for bbab: q0 -b-> q0 -b-> q0 -a-> q1 -b-> q2
PATH = ["0", "0", "0", "1", "2"]
assert all(PATH[i + 1] in NE.delta[(PATH[i], c)] for i, c in enumerate("bbab")) and PATH[-1] in NE.acc
# words of this level's quiz are not used in the worked examples
QUIZ_WORDS = {"010110", "100010", "010001", "1010", "11", "01", "000", "100", "ba", "abba", "aab", "abab", "1", "0"}
# flipping F does not complement an NFA: ab is accepted by both
NEF = nfa_from_edges("ab", [("0", "a", "0"), ("0", "b", "0"), ("0", "a", "1"), ("1", "b", "2")], "0", {"0", "1"})
assert NE.accepts("ab") and NEF.accepts("ab")

NX = nfa_from_edges("ab", [("0", "a", "0"), ("0", "", "1"), ("1", "b", "1")], "0", {"1"})
assert NX.lang(8) == rx("a*b*", "ab").lang(8)
assert NX.eclose({"0"}) == {"0", "1"} and NX.accepts("")
SX1 = fa.nfa_sets(NX, "aabb")
assert SX1 == [{"0", "1"}, {"0", "1"}, {"0", "1"}, {"1"}, {"1"}] and NX.accepts("aabb")
SX2 = fa.nfa_sets(NX, "bab")
assert SX2 == [{"0", "1"}, {"1"}, set(), set()] and not NX.accepts("bab")
NXA = nfa_from_edges("ab", [("0", "a", "0"), ("0", "", "1"), ("1", "b", "1")], "0", {"0", "1"})   # F = Q
assert NXA.states == NXA.acc and not NXA.accepts("bab") and NXA.lang(8) == NX.lang(8)
assert not {"bbab", "aba", "aabb", "bab", "ab", "010", "00"} & QUIZ_WORDS

# exam 21S-A-Q20 (states of B numbered 1..4 from the left)
Q = BANK["21S-A-Q20"]
EA = dfa_table("01", {"1": "2 2", "2": "1 1"}, "1", {"2"})
EB = nfa_from_edges("01", [("1", "0", "2"), ("1", "1", "2"), ("2", "0", "1"), ("2", "1", "1"), ("2", "", "3"),
                           ("3", "0", "4"), ("3", "1", "4"), ("4", "0", "3"), ("4", "1", "3")], "1", {"2", "3"})
ODD = {w for w in words("01", 9) if len(w) % 2 == 1}
assert EA.lang(9) == ODD and EB.lang(9) == ODD and Q["correctId"] == "a"
assert not EA.accepts("") and not EB.accepts("") and EA.accepts("0") and EB.accepts("0")
assert not EA.accepts("00") and not EB.accepts("00") and EA.accepts("010") and EB.accepts("010")
SB = fa.nfa_sets(EB, "010")
assert SB == [{"1"}, {"2", "3"}, {"1", "4"}, {"2", "3"}]

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
NB = {"1": "q_1", "2": "q_2", "3": "q_3", "4": "q_4"}
POSE = {"0": (200, 230), "1": (480, 230), "2": (760, 230)}
POSX = {"0": (280, 200), "1": (640, 200)}

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את האסל״ד: אוטומט שיכול להיות בכמה מצבים בבת אחת.",
      say="בסרטון הזה נכיר את האסלאד: אוטומט שיכול להיות בכמה מצבים בבת אחת."),
    P("נריץ אותו על מילה, נבין את מסעי $\\varepsilon$, ונשווה שפות של שני אוטומטים."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">F03 · אוטומטים סופיים וביטויים</div><h1>אסל״ד, מסעי ε והשוואת שפות</h1>'
         '<p>להכריע אם מילה מתקבלת באסל״ד (מספיק מסלול אחד), לדעת מה לא עובר מאס״ד, ולהשוות שפות של אוטומטים עם מסעי ε.</p>',
   layout="title")

concept = Scene("concept", "מהו אסל״ד", [
    P("**אסל״ד** הוא אוטומט סופי **לא דטרמיניסטי**. הוא דומה לאס״ד, עם שני הבדלים.",
      say="אסלאד הוא אוטומט סופי לא דטרמיניסטי. הוא דומה לאסאד, עם שני הבדלים."),
    P("הבדל ראשון: ממצב ואות הולכים ל**קבוצה** של מצבים. אחד, כמה, או אף אחד.", do=show("k-1")),
    P("כאן מ-$q_0$ עם $a$ יש שתי אפשרויות: להישאר ב-$q_0$, או לעבור ל-$q_1$.",
      do=show("ce-hs-0", "ce-he-0-0", "ce-he-0-1")),
    P("ומ-$q_1$ עם $a$ אין אף חץ. ריצה שמגיעה לשם פשוט **נתקעת**.",
      do=hide("ce-hs-0", "ce-he-0-0", "ce-he-0-1") + show("ce-hs-1")),
    P("הבדל שני: **מסע $\\varepsilon$**, מעבר בלי לקרוא אות. נראה אותו עוד מעט.", do=hide("ce-hs-1") + show("k-2")),
    P("ומתי מילה מתקבלת? אם **קיימת** ריצה אחת שקוראת את כל המילה ונגמרת במצב מקבל.", do=show("k-rule")),
    P("ומילה נדחית רק אם **כל** הריצות נתקעות או נגמרות במצב לא מקבל.", do=show("k-rej"), hold=0.5),
], stage=st.dfa_svg("ce", NE, POSE, N3, w=960, h=330) + '<div class="hint">אסל״ד מעל $\\{a,b\\}$</div>',
   panel=st.card("k-1", "plain", "ממצב ואות: <b>קבוצה</b> של מצבים, גם ריקה")
       + st.card("k-2", "plain", "<b>מסע $\\varepsilon$</b>: מעבר בלי לקרוא אות")
       + st.card("k-rule", "rule", "🔑 מילה מתקבלת אם ורק אם <b>קיימת</b> ריצה שקוראת הכול ונגמרת במקבל")
       + st.card("k-rej", "plain", "נדחית אם ורק אם <b>כל</b> ריצה נתקעת או נגמרת בלא מקבל"))

r1, s1, left1 = fa.run_nfa("rs", NE, "bbab", N3, "w1", lead="נריץ את $bbab$. במקום ריצה אחת, נעקוב אחרי **קבוצת** כל המצבים האפשריים. מתחילים ב-$\\{q_0\\}$.",
                           lead_say="נריץ את בִּי בִּי אֵיי בִּי. במקום ריצה אחת, נעקוב אחרי קבוצת כל המצבים האפשריים. מתחילים בקיו אפס.")
r1[0].do += show("w1-box")
r2, s2, left2 = fa.run_nfa("rs", NE, "aba", N3, "w2", lead="ועכשיו $aba$, שוב מ-$\\{q_0\\}$.",
                           lead_say="ועכשיו אֵיי בִּי אֵיי, שוב מקיו אפס.", clear=left1 + ["w1-box", "w1-path"])
r2[0].do += show("w2-box")
runs = Scene("runs", "דוגמה 1: כל הריצות", [
    *r1,
    P("ריצה מקבלת אחת מספיקה: $q_0\\to q_0\\to q_0\\to q_1\\to q_2$. נשארים ב-$q_0$, ובאות הלפני אחרונה קופצים.",
      do=show("w1-path")),
    *r2,
    P("$q_1$ מחכה ל-$b$ שלא הגיע. אין ריצה מקבלת, אז $aba$ נדחית. האוטומט מקבל מילים ש**מסתיימות** ב-$ab$.",
      say="קיו אחת מחכה לבִּי שלא הגיע. אין ריצה מקבלת, אז אֵיי בִּי אֵיי נדחית. האוטומט מקבל מילים שמסתיימות באֵיי בִּי.",
      do=show("rs-sum")),
    P("שימו לב לטריק: כדי להוכיח שמילה **מתקבלת** מספיק מסלול אחד. כדי להוכיח שהיא **נדחית** צריך לשלול את כולם.",
      do=show("rs-tip")),
    P("לכן בשאלת \"איזו מילה נדחית\" עדיף לפסול בתנאי כללי, כמו האות האחרונה, ולא להריץ כל ריצה.",
      say="לכן בשאלה איזו מילה נדחית, עדיף לפסול בתנאי כללי, כמו האות האחרונה, ולא להריץ כל ריצה.", hold=0.5),
], stage=fa.FA_CSS + st.dfa_svg("rs", NE, POSE, N3, w=960, h=330)
    + '<div class="swap" style="--swap-h:280px">'
    + fa.run_box("w1", "bbab", s1, N3, True)
    + fa.run_box("w2", "aba", s2, N3, False)
    + "</div>",
   panel=st.card("w1-path", "ex", "ריצה מקבלת אחת:<br>$q_0\\xrightarrow{b}q_0\\xrightarrow{b}q_0\\xrightarrow{a}q_1\\xrightarrow{b}q_2$")
       + st.card("rs-sum", "plain", "$L$ = המילים ש<b>מסתיימות</b> ב-$ab$")
       + st.card("rs-tip", "rule", "🔑 מתקבלת: מסלול אחד מספיק. נדחית: לשלול את <b>כל</b> המסלולים"))

x1, sx1, xl1 = fa.run_nfa("ex", NX, "aabb", N3, "x1", lead="נריץ את $aabb$. כבר בהתחלה הקבוצה היא $\\{q_0,q_1\\}$.",
                          lead_say="נריץ את אֵיי אֵיי בִּי בִּי. כבר בהתחלה הקבוצה היא קיו אפס וקיו אחת.")
x1[0].do += show("x1-box")
x2, sx2, xl2 = fa.run_nfa("ex", NX, "bab", N3, "x2", lead="ועכשיו $bab$.", lead_say="ועכשיו בִּי אֵיי בִּי.", clear=xl1 + ["x1-box"])
x2[0].do += show("x2-box")
eps = Scene("eps", "דוגמה 2: מסעי ε", [
    P("עכשיו אסל״ד עם **מסע $\\varepsilon$** מ-$q_0$ ל-$q_1$. אפשר לעבור בו בלי לקרוא אות.",
      say="עכשיו אסלאד עם מסע אפסילון מקיו אפס לקיו אחת. אפשר לעבור בו בלי לקרוא אות.", do=show("ex-he-0-1")),
    P("לכן כל פעם שאנחנו ב-$q_0$, אנחנו **גם** ב-$q_1$. זו **סגירת $\\varepsilon$**: מוסיפים כל מצב שמגיעים אליו במסעי $\\varepsilon$.",
      say="לכן כל פעם שאנחנו בקיו אפס, אנחנו גם בקיו אחת. זו סגירת אפסילון: מוסיפים כל מצב שמגיעים אליו במסעי אפסילון.",
      do=show("e-1")),
    P("ובהתחלה, $q_1$ מקבל. כלומר $\\varepsilon$ בשפה. את זה בודקים **ראשון**: האם מההתחלתי יש שרשרת $\\varepsilon$ למקבל?",
      say="ובהתחלה, קיו אחת מקבל. כלומר אפסילון בשפה. את זה בודקים ראשון: האם מההתחלתי יש שרשרת אפסילון למקבל?",
      do=hide("ex-he-0-1") + show("ex-hs-0", "ex-hs-1", "e-2")),
    *x1, *x2,
    P("השפה היא $a^*b^*$: קודם $a$-ים, אחר כך $b$-ים, ואחרי $b$ אין חזרה ל-$a$.",
      say="השפה היא אֵיי כוכבית בִּי כוכבית: קודם אֵיי-ים, אחר כך בִּי-ים, ואחרי בִּי אין חזרה לאֵיי.", hold=0.4),
    P("ועכשיו ניסוי: נהפוך **גם את $q_0$** למקבל. עכשיו $F=Q$, כל המצבים מקבלים.",
      say="ועכשיו ניסוי: נהפוך גם את קיו אפס למקבל. עכשיו כל המצבים מקבלים.",
      do=hide(*xl2, "x2-box", "ex-box") + show("exa-box")),
    P("ובכל זאת $bab$ נדחית: הריצה נתקעת, ומצב מקבל לא עוזר לריצה שלא קיימת.",
      say="ובכל זאת בִּי אֵיי בִּי נדחית: הריצה נתקעת, ומצב מקבל לא עוזר לריצה שלא קיימת.", do=show("e-3")),
    P("זו עובדה של אס״ד שלא עוברת: באסל״ד $F=Q$ **לא** אומר $\\Sigma^*$. וגם היפוך $F$ לא נותן משלים.",
      say="זו עובדה של אסאד שלא עוברת: באסלאד, כל המצבים מקבלים לא אומר סיגמא כוכבית. וגם היפוך המקבלים לא נותן משלים.",
      do=show("e-4")),
    P("למשל באסל״ד של \"מסתיימת ב-$ab$\" עם $F$ הפוכה, $ab$ עדיין מתקבלת, דרך $q_0$. מה שכן עובד: $F=\\emptyset$ נותן שפה ריקה.",
      say="למשל באסלאד של מסתיימת באֵיי בִּי עם מקבלים הפוכים, אֵיי בִּי עדיין מתקבלת, דרך קיו אפס. מה שכן עובד: בלי מצבים מקבלים, השפה ריקה.",
      hold=0.5),
], stage=fa.FA_CSS
    + '<div class="swap" style="--swap-h:330px">'
    + f'<div id="ex-box">{st.dfa_svg("ex", NX, POSX, N3, w=920, h=320, loops={"0": "up", "1": "up"})}</div>'
    + f'<div id="exa-box" class="h">{st.dfa_svg("exa", NXA, POSX, N3, w=920, h=320)}</div>'
    + '</div><div class="swap" style="--swap-h:280px">'
    + fa.run_box("x1", "aabb", sx1, N3, True) + fa.run_box("x2", "bab", sx2, N3, False)
    + '<div id="e-3" class="h">' + fa.shown(st.card("e-3c", "trap", "⚠️ $F=Q$ ובכל זאת $bab\\notin L$: הריצה <b>נתקעת</b>")) + "</div>"
    + "</div>",
   panel=st.card("e-1", "rule", "🔑 <b>סגירת $\\varepsilon$</b>: מוסיפים כל מצב שמגיעים אליו במסעי $\\varepsilon$")
       + st.card("e-2", "plain", "שרשרת $\\varepsilon$ מההתחלתי למקבל: $\\varepsilon\\in L$")
       + st.card("e-4", "trap", "⚠️ לא עובר לאסל״ד: $F=Q$ לא גורר $\\Sigma^*$, והיפוך $F$ לא נותן משלים. כן עובר: אם $F=\\emptyset$, אז $L=\\emptyset$"))

# exam on the original figure: rings on B's four states (and A's two)
RINGS = [("a1", 145, 107, 46), ("a2", 425, 107, 46), ("1", 132, 335, 46), ("2", 425, 335, 46), ("3", 628, 335, 46), ("4", 818, 335, 46)]
TAGS = [("1", 132, 385), ("2", 425, 385), ("3", 628, 385), ("4", 818, 385)]


def ring_run(word, sets, lead, lead_say):
    ph = [P(lead, say=lead_say, do=show(*[f"xr-ring-{q}" for q in sets[0]]))]
    for i, c in enumerate(word):
        do = hide(*[f"xr-ring-{q}" for q in sets[i]]) + show(*[f"xr-ring-{q}" for q in sets[i + 1]])
        names = " ו".join("מצב " + {"1": "אחד", "2": "שתיים", "3": "שלוש", "4": "ארבע"}[q] for q in sorted(sets[i + 1]))
        ph.append(P(f"${c}$: ${fa.set_tex(sets[i + 1], NB)}$", say=f"{lexicon.word_say(c)}: {names}.", do=do))
    return ph


opts_html = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אס״ד $A$, ואסל״ד $B$ עם מסע $\\varepsilon$. מה היחס בין השפות?",
      say="שאלה ממבחן: אסאד אֵיי, ואסלאד בִּי עם מסע אפסילון. מה היחס בין השפות?"),
    P("$A$ קל: הוא מקפץ בין שני מצבים, והמקבל הוא הימני. הוא מקבל בדיוק מילים באורך **אי-זוגי**.",
      say="אֵיי קל: הוא מקפץ בין שני מצבים, והמקבל הוא הימני. הוא מקבל בדיוק מילים באורך אי זוגי.",
      do=show("xr-ring-a2")),
    P("השיטה להשוואה: בודקים $\\varepsilon$, אחר כך מילים באורך אחת, אחר כך שתיים.", do=hide("xr-ring-a2")),
    P("$\\varepsilon$: ההתחלתי של $B$ לא מקבל, ואין ממנו מסע $\\varepsilon$. היא לא באף אחת מהשפות.",
      say="אפסילון: ההתחלתי של בִּי לא מקבל, ואין ממנו מסע אפסילון. היא לא באף אחת מהשפות.",
      do=show("xr-ring-1", "xg-w-0", "xg-c-0-0", "xg-c-0-1")),
    *ring_run("010", SB, "עכשיו נריץ את $B$ על $010$ עם קבוצות: מתחילים ב-$\\{q_1\\}$.",
              "עכשיו נריץ את בִּי על אפס אחת אפס עם קבוצות: מתחילים במצב אחד."),
    P("אחרי אות אחת: מצבים שתיים ושלוש, שניהם מקבלים. אחרי שתיים: אחד וארבע, אין מקבל. ואחרי שלוש שוב יש מקבל.",
      do=show("xg-w-1", "xg-c-1-0", "xg-c-1-1", "xg-w-2", "xg-c-2-0", "xg-c-2-1")),
    P("בדיוק כמו ב-$A$: $00$ באף אחת, ו-$010$ בשתיהן.",
      say="בדיוק כמו באֵיי: אפס אפס באף אחת, ואפס אחת אפס בשתיהן."),
    P("אין מילה קצרה שמפרידה. אז נבין את $B$ במבנה: עד מסע ה-$\\varepsilon$ הוא בדיוק $A$, אורך אי-זוגי.",
      say="אין מילה קצרה שמפרידה. אז נבין את בִּי במבנה: עד מסע האפסילון הוא בדיוק אֵיי, אורך אי זוגי.",
      do=hide("xr-ring-3")),
    P("אחרי ה-$\\varepsilon$, בחלק הימני כל סיבוב חזרה ל-$q_3$ מוסיף **שתי** אותיות: אורך זוגי.",
      say="אחרי האפסילון, בחלק הימני כל סיבוב חזרה למצב שלוש מוסיף שתי אותיות: אורך זוגי.",
      do=hide("xr-ring-2") + show("xr-ring-3", "xr-ring-4")),
    P("אי-זוגי ועוד זוגי זה שוב אי-זוגי. לכן $L(A)=L(B)$.",
      say="אי זוגי ועוד זוגי זה שוב אי זוגי. לכן השפות שוות.", do=show("q-ok-a", "xa-3")),
    P("המלכודת: לחשוב שהחלק הימני \"מוסיף\" מילים, ולבחור ש-$L(A)$ מוכלת ממש ב-$L(B)$. הוא לא מוסיף אף אורך חדש.",
      say="המלכודת: לחשוב שהחלק הימני מוסיף מילים, ולבחור שהשפה של אֵיי מוכלת ממש בשפה של בִּי. הוא לא מוסיף אף אורך חדש.",
      do=show("q-x-b", "q-n-b", "xa-trap")),
    P("וגם הכלה בכיוון השני נופלת: כל מילה של $A$ מתקבלת ב-$B$ דרך החלק השמאלי. אז גם \"אף אחת\" לא נכונה.",
      say="וגם הכלה בכיוון השני נופלת: כל מילה של אֵיי מתקבלת בבִּי דרך החלק השמאלי. אז גם אף אחת לא נכונה.",
      do=show("q-x-c", "q-n-c", "q-x-d", "q-n-d"), hold=0.6),
], stage=fa.FA_CSS
    + st.raster("xr", "images/exams/21S-A-Q20.png", 900, (917, 425), rings=RINGS, tags=TAGS)
    + '<div class="fa-row">'
    + fa.member_grid("xg", [r"\varepsilon", "00", "010"], ["A", "B"],
                     [[EA.accepts(w), EB.accepts(w)] for w in ["", "00", "010"]])
    + '<div style="width:460px;display:flex;flex-direction:column;gap:14px">' + st.card("xa-3", "rule", "🔑 אי-זוגי ואחריו זוגי = אי-זוגי") + st.card("xa-trap", "trap", "⚠️ מסע $\\varepsilon$ לחלק זוגי <b>לא מוסיף</b> אורכים") + "</div></div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>{Q["questionHtml"]}</div>'
       + st.options("q", opts_html, notes={"b": "לא מוסיף מילים", "c": "$A$ בתוך $B$", "d": "הן שוות"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: באסל״ד מילה מתקבלת אם **קיימת** ריצה מקבלת אחת. ומריצים עם **קבוצת** מצבים.",
      say="לסיכום: באסלאד מילה מתקבלת אם קיימת ריצה מקבלת אחת. ומריצים עם קבוצת מצבים.", do=show("c1")),
    P("מסעי $\\varepsilon$: סוגרים, ובודקים ראשון אם יש שרשרת $\\varepsilon$ מההתחלתי למקבל.",
      say="מסעי אפסילון: סוגרים, ובודקים ראשון אם יש שרשרת אפסילון מההתחלתי למקבל.", do=show("c2")),
    P("$F=Q$ לא נותן $\\Sigma^*$, והיפוך מקבלים לא נותן משלים.",
      say="כל המצבים מקבלים לא נותן סיגמא כוכבית, והיפוך מקבלים לא נותן משלים.", do=show("c3")),
    P("ובהשוואת שפות: $\\varepsilon$, אורך אחת, אורך שתיים. נתראה ברמה הבאה.",
      say="ובהשוואת שפות: אפסילון, אורך אחת, אורך שתיים. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=st.dfa_svg("rc", NE, POSE, N3, w=960, h=330),
   panel=st.card("c1", "rule", "🔑 מתקבלת אם ורק אם <b>קיימת</b> ריצה מקבלת; מריצים עם קבוצות")
       + st.card("c2", "rule", "🔑 סגירת $\\varepsilon$; שרשרת $\\varepsilon$ מההתחלתי למקבל: $\\varepsilon\\in L$")
       + st.card("c3", "trap", "⚠️ באסל״ד: $F=Q$ לא גורר $\\Sigma^*$, והיפוך $F$ לא נותן משלים")
       + st.card("c4", "rule", "🔑 השוואה: $\\varepsilon$, אורך $1$, אורך $2$"))

VIDEO = Video("F03", "fa", "אסל״ד, מסעי ε והשוואת שפות",
              [title, concept, runs, eps, exam, recap],
              bank={"21S-A-Q20": "a"})
