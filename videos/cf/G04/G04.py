# -*- coding: utf-8 -*-
"""G04 · צורת חומסקי, ליניארי ימני ורב-משמעיות — video script.

Source: tools/needhelp/cf/G04.py (lesson + goal). Exam anchor: 21S-A-Q2 (cited by the lesson's ambiguity rule box).
Not used on purpose: the quiz items of G04 (its CNF grammars, the rule set aB / b / ε / Ab of 21S-B-Q12, the grammar
S->a|aS|aA of 21S-A-Q7, order-n grammars, the 2-variable pigeonhole question).
CNF with S->ε: CLAUDE.md lists it as open; the video says exactly what the lesson says ("לפי חומרי הקורס מותר גם S→ε")
and nothing more.
"""
from nh import CFG, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, grammar, leftmost, deriv_lines, tree_svg, CSS


def cnf_rule(lhs, rhs, start="S"):
    """the lesson's definition: A->BC (two variables) or A->a (one terminal); S->ε allowed for the start variable.
    A variable S on the right is NOT disqualified (the lesson's trap: keys of 21S-B-Q5 / 23A-B-Q18 count it as CNF)."""
    if rhs == "":
        return lhs == start
    if len(rhs) == 1:
        return rhs.islower()
    return len(rhs) == 2 and rhs.isupper()


def rl_rule(lhs, rhs, start="S"):
    """the lesson's definition: A->a or A->aB, plus S->ε"""
    if rhs == "":
        return lhs == start
    return (len(rhs) == 1 and rhs.islower()) or (len(rhs) == 2 and rhs[0].islower() and rhs[1].isupper())


def rtex(lhs, rhs):
    return f"${lhs}\\to {rhs if rhs else chr(92) + 'varepsilon'}$"


# ---------------------------------------------------------------- CNF / right-linear rule sorting (new rule sets)
CNF = [("1", "A", "b"), ("2", "S", "BA"), ("3", "A", "bB"), ("4", "S", "BAB"), ("5", "B", ""), ("6", "S", "")]
CNF_OK = {k: cnf_rule(l, r) for k, l, r in CNF}
assert CNF_OK == {"1": True, "2": True, "3": False, "4": False, "5": False, "6": True}
assert cnf_rule("B", "SA")                        # S on the right side: still CNF by the course keys
RL = [("1", "B", "bA"), ("2", "A", "a"), ("3", "C", "cA"), ("4", "A", "Ba"), ("5", "S", "AB")]
RL_OK = {k: rl_rule(l, r) for k, l, r in RL}
assert RL_OK == {"1": True, "2": True, "3": True, "4": False, "5": False}

# pigeonhole (lesson, 25A-B-Q2): N variables -> NFA with N+1 states -> DFA with at most 2^(N+1) states
N = 3
assert N + 1 == 4 and 2 ** (N + 1) == 16 and 18 > 16

# ---------------------------------------------------------------- ambiguity example (new): S -> SS | ab on ababab
GA = CFG("S->SS|ab")
DA = leftmost(GA, "ababab", limit=5)
assert len(DA) == 2 and GA.count_trees("ababab", limit=5) == 2
DA1, DA2 = sorted(DA, key=lambda d: [s[3] for s in d])     # first: S=>SS=>SSS..., second: S=>SS=>abS...
assert [s[3] for s in DA1][:2] == [0, 0] and [s[3] for s in DA2][:2] == [0, 1]
GU = CFG("S->abS|ab")
assert GU.lang(8) == GA.lang(8) == {"ab" * k for k in range(1, 5)}
assert all(GU.count_trees(w) <= 1 for w in GU.lang(8))      # same language, unambiguous grammar

# ---------------------------------------------------------------- exam 21S-A-Q2
Q = BANK["21S-A-Q2"]
GE = CFG("S->bA|bB;A->aA|bA|a|c;B->bB|aB|a|b")
DE = leftmost(GE, "ba", limit=5)
assert len(DE) == 2 and GE.count_trees("ba") >= 2
DE1, DE2 = sorted(DE, key=lambda d: d[0][3])                 # via A, via B
GE_U = CFG("S->bB;B->aB|bB|a|b|c")                           # the bank's unambiguous equivalent
assert GE_U.lang(7) == GE.lang(7)
assert all(GE_U.count_trees(w) <= 1 for w in GE_U.lang(7))
assert Q["correctId"] == "a"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה: שאלות מבנה על דקדוקים. צורת חומסקי, דקדוק ליניארי ימני, ורב-משמעיות."),
    p("נלמד לזהות כל אחד מהם, ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage=CSS + '<div class="kicker">G04 · דקדוקים ואוטומט מחסנית</div><h1>חומסקי, ליניארי ימני, רב-משמעיות</h1>'
         '<p>לזהות דקדוק בצורת חומסקי ודקדוק ליניארי ימני, להכריע רב-משמעיות, ולהסיק על אינסופיות משובך יונים.</p>',
   layout="title")

cnf = Scene("cnf", "צורת חומסקי", [
    p("צורה נורמלית של חומסקי. כל כלל הוא אחת משתי צורות:", say="צורה נורמלית של חומסקי. כל כלל הוא אחת משתי צורות."),
    p("$A\\to BC$: **בדיוק שני משתנים**. או $A\\to a$: **טרמינל יחיד**.",
      say="אֵיי גדולה גוזר בִּי גדולה סִי גדולה: בדיוק שני משתנים. או אֵיי גדולה גוזר אֵיי: טרמינל יחיד.", do=show("n1")),
    p("ולפי חומרי הקורס מותר גם $S\\to\\varepsilon$, רק למשתנה ההתחלתי.",
      say="ולפי חומרי הקורס מותר גם אֶס גוזר אפסילון, רק למשתנה ההתחלתי.", do=show("n2")),
    p("נמיין כללים. $A\\to b$: טרמינל יחיד. בסדר.", say="נמיין כללים. אֵיי גדולה גוזר בִּי: טרמינל יחיד. בסדר.", do=show("cn-ok-1")),
    p("$S\\to BA$: שני משתנים. בסדר.", say="אֶס גוזר בִּי גדולה אֵיי גדולה: שני משתנים. בסדר.", do=show("cn-ok-2")),
    p("$A\\to bB$: טרמינל **ו**משתנה. זו לא אף אחת מהצורות.",
      say="אֵיי גדולה גוזר בִּי בִּי גדולה: טרמינל ומשתנה. זו לא אף אחת מהצורות.", do=show("cn-x-3", "cn-n-3")),
    p("$S\\to BAB$: שלושה משתנים, ארוך מדי.", say="אֶס גוזר שלושה משתנים: ארוך מדי.", do=show("cn-x-4", "cn-n-4")),
    p("$B\\to\\varepsilon$: מחיקה מותרת רק ל-$S$.", say="בִּי גדולה גוזר אפסילון: מחיקה מותרת רק לאֶס.",
      do=show("cn-x-5", "cn-n-5")),
    p("ו-$S\\to\\varepsilon$ מותר.", say="ואֶס גוזר אפסילון מותר.", do=show("cn-ok-6")),
    p("שימו לב: ההגדרה לא בדף הנוסחאות, ובמחוונים דקדוק עם $S$ בצד ימין **כן** נחשב חומסקי. אל תפסלו בגלל זה.",
      say="שימו לב: ההגדרה לא בדף הנוסחאות, ובמחוונים דקדוק עם אֶס בצד ימין כן נחשב חומסקי. אל תפסלו בגלל זה.",
      do=show("n3")),
    p("ועוד עובדה: **לכל דקדוק חסר הקשר יש דקדוק שקול בצורת חומסקי**.", do=show("n4"), hold=0.4),
], stage='<div style="width:640px">' + st.options("cn", [(k, rtex(l, r)) for k, l, r in CNF],
         notes={"3": "טרמינל + משתנה", "4": "שלושה משתנים", "5": "רק $S$ נמחק"}) + '</div>',
   panel=st.card("n1", "rule", "🔑 <b>חומסקי:</b> $A\\to BC$ או $A\\to a$")
       + st.card("n2", "plain", "לפי חומרי הקורס מותר גם $S\\to\\varepsilon$ (רק למשתנה ההתחלתי)")
       + st.card("n3", "trap", "⚠️ $S$ בצד ימין: במחוונים זה <b>כן</b> חומסקי (21S-B-Q5, 23A-B-Q18)")
       + st.card("n4", "rule", "🔑 לכל דקדוק ח״ה יש דקדוק שקול בצורת חומסקי"))

rl = Scene("rl", "ליניארי ימני", [
    p("דקדוק **ליניארי ימני**: כל כלל הוא $A\\to a$, או $A\\to aB$.",
      say="דקדוק ליניארי ימני: כל כלל הוא אֵיי גדולה גוזר אֵיי, או אֵיי גדולה גוזר אֵיי בִּי גדולה.", do=show("l1")),
    p("כלומר טרמינל, ואחריו **לכל היותר משתנה אחד, מימין**. ובנוסף מותר $S\\to\\varepsilon$.",
      say="כלומר טרמינל, ואחריו לכל היותר משתנה אחד, מימין. ובנוסף מותר אֶס גוזר אפסילון."),
    p("$B\\to bA$, $A\\to a$ ו-$C\\to cA$: כולם חוקיים.",
      say="בִּי גדולה גוזר בִּי אֵיי גדולה, אֵיי גדולה גוזר אֵיי, וסִי גדולה גוזר סִי אֵיי גדולה: כולם חוקיים.",
      do=show("rl-ok-1", "rl-ok-2", "rl-ok-3")),
    p("$A\\to Ba$: המשתנה **משמאל** לטרמינל. אסור.", say="אֵיי גדולה גוזר בִּי גדולה אֵיי: המשתנה משמאל לטרמינל. אסור.",
      do=show("rl-x-4", "rl-n-4")),
    p("$S\\to AB$: שני משתנים בלי טרמינל. אסור.", say="אֶס גוזר אֵיי גדולה בִּי גדולה: שני משתנים בלי טרמינל. אסור.",
      do=show("rl-x-5", "rl-n-5")),
    p("הדקדוקים האלה שקולים **בדיוק לשפות הרגולריות**: כל משתנה הוא מצב.", do=show("l2")),
    p("עם $N$ משתנים בונים אסל״ד עם $N+1$ מצבים: מצב לכל משתנה, ועוד מצב מקבל.",
      say="עם אֵן משתנים בונים אסל״ד עם אֵן ועוד אחד מצבים: מצב לכל משתנה, ועוד מצב מקבל.", do=show("ph1")),
    p("למשל שלושה משתנים: ארבעה מצבים, ואס״ד עם לכל היותר $2^4=16$ מצבים.",
      say="למשל שלושה משתנים: ארבעה מצבים, ואס״ד עם לכל היותר שתיים בחזקת ארבע, שש עשרה מצבים.", do=show("ph2")),
    p("מילה באורך $18$ עוברת יותר מ-$16$ מצבים, אז מצב חוזר: יש מעגל, והשפה **אינסופית**. שובך יונים.",
      say="מילה באורך שמונה עשרה עוברת יותר משש עשרה מצבים, אז מצב חוזר: יש מעגל, והשפה אינסופית. שובך יונים.",
      do=show("ph3"), hold=0.4),
], stage='<div style="width:600px">' + st.options("rl", [(k, rtex(l, r)) for k, l, r in RL],
         notes={"4": "משתנה משמאל", "5": "שני משתנים"}) + '</div>'
         '<div style="display:flex;flex-direction:column;gap:10px;align-items:center">'
         '<div id="ph1" class="cf-mid h">$N$ משתנים: אסל״ד עם $N+1$ מצבים</div>'
         '<div id="ph2" class="cf-mid h">$N=3$: אס״ד עם $\\le 2^4=16$ מצבים</div>'
         '<div id="ph3" class="cf-mid h">אם $|w|=18>16$, אז יש מעגל, ולכן אינסופית</div></div>',
   panel=st.card("l1", "rule", "🔑 <b>ליניארי ימני:</b> $A\\to a$ או $A\\to aB$ (ועוד $S\\to\\varepsilon$)")
       + st.card("l2", "rule", "🔑 שקול בדיוק לשפות <b>רגולריות</b>"))

T1 = tree_svg("ta", GA, DA1, w=380, dy=72, scale=1.25)
T2 = tree_svg("tb", GA, DA2, w=380, dy=72, scale=1.25)
amb = Scene("amb", "רב-משמעיות", [
    p("דקדוק הוא **רב-משמעי** אם יש מילה עם **שני עצי גזירה שונים**.", do=show("a1")),
    p("הדקדוק $S\\to SS\\mid ab$, והמילה $ababab$. עץ ראשון: מפצלים את ה-$S$ השמאלי.",
      say="הדקדוק: אֶס גוזר אֶס אֶס, או אֵיי בִּי. והמילה אֵיי בִּי שלוש פעמים. עץ ראשון: מפצלים את האֶס השמאלי.",
      do=show("ta-t-1", "ta-t-2")),
    p("ומסיימים: $ababab$.", say="ומסיימים: אֵיי בִּי, אֵיי בִּי, אֵיי בִּי.", do=show("ta-t-3", "ta-t-4", "ta-t-5")),
    p("עץ שני: מפצלים דווקא את ה-$S$ הימני.", say="עץ שני: מפצלים דווקא את האֶס הימני.",
      do=show("tb-t-1", "tb-t-2", "tb-t-3")),
    p("ומסיימים. אותה מילה, שני עצים שונים: הדקדוק רב-משמעי.", do=show("tb-t-4", "tb-t-5", "av")),
    p("אבל הדקדוק $S\\to abS\\mid ab$ יוצר **אותה שפה**, $(ab)^+$, ולכל מילה בו יש עץ אחד בלבד.",
      say="אבל הדקדוק שבו אֶס גוזר אֵיי בִּי אֶס, או אֵיי בִּי, יוצר אותה שפה, אֵיי בִּי פלוס, ולכל מילה בו יש עץ אחד בלבד.",
      do=show("a2")),
    p("כלומר רב-משמעיות היא **תכונה של הדקדוק, ולא של השפה**.", do=show("a3"), hold=0.5),
], stage='<div class="cf-two">'
         f'<div><div class="cf-cap">עץ 1</div>{T1}</div><div><div class="cf-cap">עץ 2</div>{T2}</div></div>'
         '<div id="av" class="verdict bad h">$ababab$: שני עצי גזירה</div>',
   panel=grammar("ga", GA)
       + st.card("a1", "rule", "🔑 <b>רב-משמעי</b>: מילה עם <b>שני עצי גזירה</b> שונים")
       + st.card("a2", "plain", "$S\\to abS\\mid ab$: אותה שפה, עץ יחיד לכל מילה")
       + st.card("a3", "trap", "⚠️ תכונה של <b>הדקדוק</b>, לא של השפה"))

E1 = tree_svg("e1", GE, DE1, w=200, dy=80, scale=1.0)
E2 = tree_svg("e2", GE, DE2, w=200, dy=80, scale=1.0)
opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן. הדקדוק: $S$ גוזר $bA$ או $bB$, ושני המשתנים גוזרים זנבות של אותיות.",
      say="שאלה ממבחן. בדקדוק, אֶס גוזר בִּי אֵיי גדולה, או בִּי בִּי גדולה, ושני המשתנים גוזרים זנבות של אותיות."),
    p("$A$ וגם $B$ יכולים לגזור את האות $a$. אז נחפש מילה שנגזרת דרך שניהם: $ba$.",
      say="אֵיי גדולה וגם בִּי גדולה יכולים לגזור את האות אֵיי. אז נחפש מילה שנגזרת דרך שניהם: בִּי אֵיי.",
      do=show("ex-a-A-2", "ex-a-B-2")),
    p("עץ ראשון: $S\\Rightarrow bA\\Rightarrow ba$.", say="עץ ראשון: אֶס, בִּי אֵיי גדולה, בִּי אֵיי.",
      do=show("e1-t-1", "e1-t-2", "ex-a-S-0")),
    p("עץ שני: $S\\Rightarrow bB\\Rightarrow ba$. שני עצים: הדקדוק **רב-משמעי**.",
      say="עץ שני: אֶס, בִּי בִּי גדולה, בִּי אֵיי. שני עצים: הדקדוק רב-משמעי.",
      do=hide("ex-a-S-0") + show("e2-t-1", "e2-t-2", "ex-a-S-1")),
    p("שתי האפשרויות שאומרות חד-משמעי נפסלות.", do=hide("ex-a-S-1", "ex-a-A-2", "ex-a-B-2") + show("q-x-c", "q-x-d")),
    p("ועכשיו המלכודת: רב-משמעי, **ולא קיים** דקדוק חד-משמעי שקול?", do=show("xtrap")),
    p("השפה: $b$ ואחריה מילה לא ריקה מעל $a$ ו-$b$, או מילה מעל $a$ ו-$b$ ואחריה $c$. ויש לה דקדוק בלי הכפילות:",
      say="השפה: בִּי, ואחריה מילה לא ריקה מעל אֵיי ובִּי, או מילה מעל אֵיי ובִּי ואחריה סִי. ויש לה דקדוק בלי הכפילות.",
      do=show("xu")),
    p("$S\\to bB$, ו-$B$ גוזר $aB$, $bB$, $a$, $b$ או $c$. לכל מילה עץ אחד.",
      say="אֶס גוזר בִּי בִּי גדולה, ובִּי גדולה גוזר אֵיי בִּי גדולה, בִּי בִּי גדולה, אֵיי, בִּי או סִי. לכל מילה עץ אחד.",
      do=show("q-x-b")),
    p("התשובה: רב-משמעי, וגם קיים דקדוק חד-משמעי שקול. רב-משמעיות היא תכונה של הדקדוק.",
      do=show("q-ok-a"), hold=0.6),
], stage=grammar("ex", GE)
         + '<div class="cf-two">'
           f'<div><div class="cf-cap">דרך $A$</div>{E1}</div><div><div class="cf-cap">דרך $B$</div>{E2}</div></div>'
         + '<div class="swap cf-c" style="--swap-h:130px">'
         + '<div id="xu" class="h">' + grammar("gu", GE_U) + '</div></div>'
         + st.card("xtrap", "trap", "⚠️ רב-משמעי ≠ אין דקדוק חד-משמעי: <b>תכונה של הדקדוק</b>"),
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>נתון הדקדוק שמשמאל, המשתנה ההתחלתי הוא $S$. איזו טענה נכונה?</div>'
       + '<div class="cf-sm">' + st.options("q", opts) + '</div>')

recap = Scene("recap", "סיכום", [
    p("לסיכום: חומסקי הוא שני משתנים או טרמינל יחיד, ולפי חומרי הקורס גם $S\\to\\varepsilon$.",
      say="לסיכום: חומסקי הוא שני משתנים, או טרמינל יחיד, ולפי חומרי הקורס גם אֶס גוזר אפסילון.", do=show("c1")),
    p("ליניארי ימני הוא טרמינל ואחריו לכל היותר משתנה, והוא שקול לשפות הרגולריות.", do=show("c2")),
    p("$N$ משתנים נותנים $N+1$ מצבים, ומילה ארוכה מספיק מבטיחה מעגל.",
      say="אֵן משתנים נותנים אֵן ועוד אחד מצבים, ומילה ארוכה מספיק מבטיחה מעגל.", do=show("c3")),
    p("ורב-משמעי הוא שני עצי גזירה, תכונה של הדקדוק. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=grammar("rc", GA, big=True),
   panel=st.card("c1", "rule", "🔑 חומסקי: $A\\to BC$ או $A\\to a$ (ו-$S\\to\\varepsilon$)")
       + st.card("c2", "rule", "🔑 ליניארי ימני: $A\\to a$ או $A\\to aB$; שקול לרגולריות")
       + st.card("c3", "rule", "🔑 $N$ משתנים: $N+1$ מצבים; אם יש מילה ארוכה, אז יש מעגל")
       + st.card("c4", "trap", "⚠️ רב-משמעי = שני עצים; תכונה של הדקדוק, לא של השפה"))

VIDEO = Video("G04", "cf", "חומסקי, ליניארי ימני ורב-משמעיות",
              [title, cnf, rl, amb, exam, recap],
              bank={"21S-A-Q2": "a"})
