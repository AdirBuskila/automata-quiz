# -*- coding: utf-8 -*-
"""F02 · מבנה של אס״ד: מצב בור, משלים ומכפלה — video script (build: tools/video/vid.py F02).

Source: tools/needhelp/fa/F02.py (lesson + goal). Exam anchor: 19B-A-Q4 (cited by the lesson, not by the quiz).
Not used on purpose: the quiz numbers (6/3 x 4/2 intersection, 5/2 x 4/3 union), 19B-A-Q6 / SAMP-19-Q4 /
23A-A-Q2 (their content is quiz Q3-Q5). The product example below is a new pair of 2-state DFAs.
"""
from nh import dfa_table, all_dfas, words, DFA
from vid import P, Scene, Video, show, hide, BANK
import lexicon
import stage as st
import w_fa as fa

# ---------------------------------------------------------------- machines (verified)
D1 = dfa_table("01", {"0": "0 1", "1": "0 2", "2": "2 2"}, "0", {"2"})          # contains 11 (F01)
assert D1.lang(8) == {w for w in words("01", 8) if "11" in w}
DC = D1.complement()
assert DC.lang(8) == {w for w in words("01", 8) if "11" not in w} and DC.acc == {"0", "1"}
assert D1.run("0110") == "2" and not DC.accepts("0110")

# Σ* with an unreachable non-accepting state
U = dfa_table("01", {"0": "0 0", "1": "1 1"}, "0", {"0"})
assert U.lang(8) == set(words("01", 8)) and U.states != U.acc and U.reachable() == {"0"}

# product: A1 = even number of a, A2 = last letter is b
A1 = dfa_table("ab", {"0": "1 0", "1": "0 1"}, "0", {"0"})
A2 = dfa_table("ab", {"0": "0 1", "1": "0 1"}, "0", {"1"})
assert A1.lang(8) == {w for w in words("ab", 8) if w.count("a") % 2 == 0}
assert A2.lang(8) == {w for w in words("ab", 8) if w.endswith("b")}


def relabel(D):
    """product states (p, q) -> 'pq' so the ids stay plain"""
    f = lambda s: s[0] + s[1]
    return DFA(D.alpha, {(f(p), a): f(r) for (p, a), r in D.delta.items()}, f(D.start), {f(s) for s in D.acc})


PI, PU = relabel(A1.product(A2, "and")), relabel(A1.product(A2, "or"))
assert len(PI.states) == 4 and PI.acc == {"01"} and PU.acc == {"00", "01", "11"}
assert len(PI.acc) == 1 * 1 and len(PU.acc) == 4 - (2 - 1) * (2 - 1)
assert PI.lang(8) == A1.lang(8) & A2.lang(8) and PU.lang(8) == A1.lang(8) | A2.lang(8)
TR = fa.dfa_trace(PI, "abb")
assert TR == ["00", "10", "11", "11"] and not PI.accepts("abb") and PU.accepts("abb")

# pigeonhole: the run of 0110 repeats q0; pumping that cycle keeps the word accepted
T0 = fa.dfa_trace(D1, "0110")
assert T0 == ["0", "0", "1", "2", "2"] and T0[0] == T0[1]
assert all(D1.accepts("0" * k + "110") for k in range(8))

# exam 19B-A-Q4
Q = BANK["19B-A-Q4"]
assert Q["correctId"] == "b"
SIG = dfa_table("01", {"0": "0 0"}, "0", {"0"})
EMP = dfa_table("01", {"0": "0 0"}, "0", set())
assert SIG.product(D1, "or").lang(8) != D1.lang(8) and SIG.product(D1, "or").accepts("0") and not D1.accepts("0")  # a false
for B2 in all_dfas(2, "01"):                                                   # b true (every 2-state A2)
    assert EMP.product(B2, "or").lang(6) == B2.lang(6)
assert D1.product(D1, "or").states != D1.product(D1, "or").acc                 # c false: L1=L2, a non-accepting state
assert not EMP.product(EMP, "or").acc                                          # d false: L1∩L2=∅, no accepting state

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS = {"0": (170, 190), "1": (450, 190), "2": (730, 190)}
PT = {"00": r"\langle 0,0\rangle", "01": r"\langle 0,1\rangle", "10": r"\langle 1,0\rangle", "11": r"\langle 1,1\rangle"}
PS = {"00": "הזוג אפס אפס", "01": "הזוג אפס אחת", "10": "הזוג אחת אפס", "11": "הזוג אחת אחת"}
PN = {"00": "0,0", "01": "0,1", "10": "1,0", "11": "1,1"}
PPOS = {"00": (230, 130), "01": (690, 130), "10": (230, 400), "11": (690, 400)}
PBEND = {("01", "10"): 0.12, ("11", "00"): 0.12}
PLOOP = {"01": "up", "11": "down", "00": "up", "10": "down"}

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נסתכל על **המבנה** של אס״ד, בלי להריץ מילים."),
    P("נלמד ארבע עובדות שפותרות חצי מהטענות, נבנה אוטומט מכפלה ונספור בו מצבים מקבלים."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">F02 · אוטומטים סופיים וביטויים</div><h1>מבנה של אס״ד: מצב בור, משלים ומכפלה</h1>'
         '<p>לספור מצבים מקבלים באוטומט מכפלה, לדעת מה נכון תמיד על אס״ד ומה נפל על מצב שאינו ישיג, ולהשתמש בשובך היונים.</p>',
   layout="title")

facts = Scene("facts", "עובדות של מבנה", [
    P("בשלב הקודם הרצנו אס״ד. רוב הטענות במבחן נפתרות בשתי שורות מהמבנה שלו."),
    P("עובדה ראשונה: $\\varepsilon$ בשפה אם ורק אם המצב ההתחלתי מקבל.", do=show("f-1")),
    P("שנייה: אם אין אף מצב מקבל, $F=\\emptyset$, השפה ריקה.",
      say="שנייה: אם אין אף מצב מקבל, כלומר קבוצת המקבלים ריקה, השפה ריקה.", do=show("f-2")),
    P("ואם כל המצבים מקבלים, $F=Q$, השפה היא $\\Sigma^*$, כל המילים. וזה **רק באס״ד**.",
      say="ואם כל המצבים מקבלים, השפה היא סיגמא כוכבית, כל המילים. וזה רק באסאד.", do=show("f-3")),
    P("אבל הכיוון ההפוך לא נכון. הנה אס״ד שמקבל את $\\Sigma^*$, ובכל זאת יש בו מצב לא מקבל.",
      say="אבל הכיוון ההפוך לא נכון. הנה אסאד שמקבל את סיגמא כוכבית, ובכל זאת יש בו מצב לא מקבל.",
      do=show("fu-box")),
    P("$q_1$ לא מקבל, אבל מ-$q_0$ אין אליו אף חץ: הוא **לא ישיג** מההתחלה, ואף ריצה לא מגיעה אליו.",
      do=show("fu-hs-1")),
    P("לכן כשטענה מדברת על **כל המצבים**, חפשו מצב לא ישיג: הוא משנה את המצבים, ולא משנה את השפה.",
      do=show("f-trap"), hold=0.5),
], stage=f'<div id="fu-box" class="h">{st.dfa_svg("fu", U, {"0": (260, 180), "1": (640, 180)}, N3, w=900, h=300)}'
         '<div class="hint">$L=\\Sigma^*$, ובכל זאת $F\\neq Q$</div></div>',
   panel=st.card("f-1", "rule", "🔑 $\\varepsilon\\in L$ אם ורק אם המצב ההתחלתי מקבל")
       + st.card("f-2", "plain", "אם $F=\\emptyset$, אז $L=\\emptyset$")
       + st.card("f-3", "plain", "אם $F=Q$, אז $L=\\Sigma^*$ (<b>רק באס״ד</b>)")
       + st.card("f-trap", "trap", "⚠️ מצב לא ישיג משנה את המצבים, לא את השפה"))

comp = Scene("complement", "משלים", [
    P("עובדה רביעית: **משלים**. ניקח את האס״ד מהשלב הקודם, שמקבל מילים שמכילות $11$."),
    P("הופכים: כל מצב מקבל נהיה לא מקבל, וכל לא מקבל נהיה מקבל.", do=hide("cm-a") + show("cm-b")),
    P("עכשיו $q_0$ ו-$q_1$ מקבלים, ו-$q_2$ לא. השפה החדשה: כל המילים ש**לא** מכילות $11$.",
      do=show("cmb-hs-0", "cmb-hs-1", "cm-r1")),
    P("למשל $0110$: הריצה היחידה שלה נגמרת ב-$q_2$. קודם היא התקבלה, ועכשיו היא נדחית.",
      do=hide("cmb-hs-0", "cmb-hs-1") + show("cmb-hs-2", "cm-tr")),
    P("למה זה עובד? כי באס״ד לכל מילה יש **ריצה אחת ומלאה**. אנחנו רק הופכים את התשובה בסוף שלה.",
      say="למה זה עובד? כי באסאד לכל מילה יש ריצה אחת ומלאה. אנחנו רק הופכים את התשובה בסוף שלה.", do=show("cm-r2")),
    P("באסל״ד זה לא עובד, כי שם יש הרבה ריצות. נראה את זה ברמה הבאה.",
      say="באסלאד זה לא עובד, כי שם יש הרבה ריצות. נראה את זה ברמה הבאה.", hold=0.5),
], stage='<div class="swap" style="--swap-h:360px">'
         f'<div id="cm-a">{st.dfa_svg("cma", D1, POS, N3, w=900, h=300)}<div class="hint">$L$: מכילות $11$</div></div>'
         f'<div id="cm-b" class="h">{st.dfa_svg("cmb", DC, POS, N3, w=900, h=300)}<div class="hint">$\\overline{{L}}$: לא מכילות $11$</div></div>'
         '</div>'
         f'<div id="cm-tr" class="h">{st.tape("cmt", "0110")}'
         + st.trace("cmt", T0, N3).replace(' class="h"', "") + st.verdict("cmt", False).replace(" h\"", "\"") + "</div>",
   panel=st.card("cm-r1", "rule", "🔑 <b>משלים</b>: הופכים מקבלים ללא מקבלים, ולהפך")
       + st.card("cm-r2", "plain", "עובד <b>רק באס״ד</b>: ריצה אחת ומלאה לכל מילה"))

# product run
prun, ps, pleft = fa.run_named("pi", PI, "abb", PT, PS, "pt", lead="נריץ את $abb$. מתחילים בזוג $\\langle 0,0\\rangle$: שני הרכיבים בהתחלה.",
                               lead_say="נריץ את אֵיי בִּי בִּי. מתחילים בזוג אפס אפס: שני הרכיבים בהתחלה.")
prun[0].do += hide("pa-box") + show("pp-box")
product = Scene("product", "אוטומט מכפלה", [
    P("עכשיו **אוטומט מכפלה**: מריצים שני אס״דים במקביל, על אותה מילה.",
      say="עכשיו אוטומט מכפלה: מריצים שני אסאדים במקביל, על אותה מילה."),
    P("$A_1$ זוכר אם מספר ה-$a$ זוגי: מצב $0$ זוגי, ומצב $1$ אי-זוגי.",
      say="אֵיי אחת זוכר אם מספר האֵיי זוגי: מצב אפס זוגי, ומצב אחת אי זוגי.", do=show("pa-box", "pr-1")),
    P("$A_2$ זוכר אם האות האחרונה היא $b$: מצב $1$ אומר כן.",
      say="אֵיי שתיים זוכר אם האות האחרונה היא בִּי: מצב אחת אומר כן.", do=show("pa-2", "pr-2")),
    P("מצב של המכפלה הוא **זוג**: איפה $A_1$, ואיפה $A_2$. יש $2\\cdot2=4$ זוגות.",
      say="מצב של המכפלה הוא זוג: איפה אֵיי אחת, ואיפה אֵיי שתיים. יש שתיים כפול שתיים, ארבעה זוגות.",
      do=show("pr-3")),
    *prun,
    P("נגמרנו ב-$\\langle 1,1\\rangle$: $A_1$ לא מקבל, כי ראינו $a$ אחת, אבל $A_2$ מקבל, כי האחרונה $b$.",
      say="נגמרנו בזוג אחת אחת: אֵיי אחת לא מקבל, כי ראינו אֵיי אחת, אבל אֵיי שתיים מקבל, כי האחרונה בִּי."),
    P("בחיתוך, זוג מקבל רק אם **שניהם** מקבלים. רק $\\langle 0,1\\rangle$, עיגול כפול אחד: $1\\cdot1$.",
      say="בחיתוך, זוג מקבל רק אם שניהם מקבלים. רק הזוג אפס אחת, עיגול כפול אחד: אחת כפול אחת.",
      do=hide(*pleft) + show("pi-hs-01", "pr-and")),
    P("לכן $abb$ **לא** בחיתוך.", do=hide("pi-hs-01") + show("pi-hs-11")),
    P("באיחוד, זוג מקבל אם **לפחות אחד** מקבל. עכשיו יש שלושה עיגולים כפולים.",
      do=hide("pi-hs-11", "pp-i") + show("pp-u", "pr-or")),
    P("ו-$abb$ כן באיחוד: $\\langle 1,1\\rangle$ מקבל.", say="ואֵיי בִּי בִּי כן באיחוד: הזוג אחת אחת מקבל.",
      do=show("pu-hs-11"), hold=0.5),
], stage=fa.FA_CSS
    + '<div class="swap" style="--swap-h:600px">'
      '<div id="pa-box" class="h fa-small"><div class="fa-row">'
      f'<div><div class="fa-lab">$A_1$: זוגיות של $a$</div>{st.dfa_svg("pa1", A1, {"0": (110, 150), "1": (330, 150)}, {"0": "0", "1": "1"}, w=440, h=260, scale=1.0)}</div>'
      f'<div id="pa-2" class="h"><div class="fa-lab">$A_2$: האחרונה $b$</div>{st.dfa_svg("pa2", A2, {"0": (110, 150), "1": (330, 150)}, {"0": "0", "1": "1"}, w=440, h=260, scale=1.0)}</div>'
      '</div></div>'
      '<div id="pp-box" class="h fa-pair"><div class="swap" style="--swap-h:520px">'
      f'<div id="pp-i">{st.dfa_svg("pi", PI, PPOS, PN, w=920, h=530, scale=0.98, bend=PBEND, loops=PLOOP)}</div>'
      f'<div id="pp-u" class="h">{st.dfa_svg("pu", PU, PPOS, PN, w=920, h=530, scale=0.98, bend=PBEND, loops=PLOOP)}</div>'
      f'</div>{fa.named_trace("pt", ps, PT)}</div>'
      '</div>',
   panel=st.card("pr-1", "plain", "$A_1$: מצב $0$ = מספר זוגי של $a$ (מקבל)")
       + st.card("pr-2", "plain", "$A_2$: מצב $1$ = האות האחרונה $b$ (מקבל)")
       + st.card("pr-3", "rule", "🔑 מצב מכפלה = <b>זוג</b> $\\langle p,q\\rangle$; כל אות מזיזה את שניהם")
       + st.card("pr-and", "plain", "<b>חיתוך</b>: מקבל אם <b>שניהם</b> מקבלים")
       + st.card("pr-or", "plain", "<b>איחוד</b>: מקבל אם <b>לפחות אחד</b> מקבל"))
# the tape is not drawn in this scene: drop the tape ids run_named touches
for p in prun:
    p.do = [(k, e) for k, e in p.do if not e.startswith("pt-k-") and not e.startswith("pt-d-")]

count = Scene("count", "ספירה", [
    P("עכשיו בכלל. ל-$A_1$ יש $n_1$ מצבים, מתוכם $f_1$ מקבלים, ול-$A_2$ יש $n_2$ ו-$f_2$.",
      say="עכשיו בכלל. לאוטומט הראשון יש אן אחת מצבים, ומספר המקבלים שלו הוא אֶף אחת. לשני יש אן שתיים מצבים, ומספר המקבלים שלו הוא אֶף שתיים."),
    P("מספר הזוגות הוא $n_1n_2$, גם בחיתוך וגם באיחוד.", say="מספר הזוגות הוא אן אחת כפול אן שתיים, גם בחיתוך וגם באיחוד.",
      do=show("ct-r1")),
    P("בחיתוך בוחרים מקבל מכל צד: $f_1f_2$.", say="בחיתוך בוחרים מקבל מכל צד: מספר המקבלים של הראשון, כפול מספר המקבלים של השני.", do=show("ct-r2")),
    P("באיחוד קל יותר לספור את הלא מקבלים: זוגות ששני הרכיבים בהם לא מקבלים.", do=show("ct-r3")),
    P("יש $(n_1-f_1)(n_2-f_2)$ כאלה, ומחסירים אותם מכל הזוגות.",
      say="מספר הלא מקבלים בראשון, כפול מספר הלא מקבלים בשני. ומחסירים אותם מכל הזוגות.", do=show("ct-r4")),
    P("בדוגמה שלנו: חיתוך $1\\cdot1=1$, ואיחוד $4-1\\cdot1=3$. בדיוק מה שראינו בשרטוט.",
      say="בדוגמה שלנו: חיתוך, אחת כפול אחת, אחת. ואיחוד, ארבע פחות אחת, שלוש. בדיוק מה שראינו בשרטוט.", do=show("ct-ex")),
    P("במבחן, המסיחים הם מספרים **אמיתיים** מאותה בנייה: המקבלים באיחוד, הסכום, או כל הזוגות.",
      do=show("ct-trap")),
    P("אז קוראים פעמיים את המילה המודגשת: **חיתוך** או **איחוד**. ואוטומט המכפלה גם לא בהכרח מינימלי.", hold=0.5),
], stage=fa.FA_CSS
    + '<table class="fa-mini" dir="ltr"><thead><tr><th></th><th>מצבים</th><th>מקבלים</th></tr></thead><tbody>'
      '<tr id="ct-r1" class="h"><th>כל הזוגות</th><td>$n_1n_2$</td><td></td></tr>'
      '<tr id="ct-r2" class="h"><th>חיתוך</th><td>$n_1n_2$</td><td>$f_1f_2$</td></tr>'
      '<tr id="ct-r3" class="h"><th>איחוד</th><td>$n_1n_2$</td><td>הכול פחות הזוגות הלא מקבלים</td></tr>'
      '<tr id="ct-r4" class="h"><th></th><td></td><td>$n_1n_2-(n_1-f_1)(n_2-f_2)$</td></tr>'
      '</tbody></table>',
   panel=st.card("ct-ex", "ex", "בדוגמה: $n_1=n_2=2$, $f_1=f_2=1$.<br>חיתוך $1$, איחוד $4-1=3$")
       + st.card("ct-trap", "trap", "⚠️ המסיחים: המקבלים בפעולה השנייה, $f_1+f_2$, או $n_1n_2$. קראו פעמיים: <b>חיתוך</b> או <b>איחוד</b>?"))

pigeon = Scene("pigeon", "שובך היונים", [
    P("ועובדה אחרונה: **שובך היונים**."),
    P("ריצה על מילה באורך $m$ עוברת ב-$m+1$ מצבים, כי מתחילים במצב לפני שקוראים משהו.",
      say="ריצה על מילה באורך אֶם עוברת באֶם ועוד אחד מצבים, כי מתחילים במצב לפני שקוראים משהו."),
    P("באס״ד הזה שלושה מצבים, והוא מקבל את $0110$, באורך ארבע. הריצה עוברת בחמישה מצבים.",
      say="באסאד הזה שלושה מצבים, והוא מקבל את אפס אחת אחת אפס, באורך ארבע. הריצה עוברת בחמישה מצבים.",
      do=show("pg-tr")),
    P("חמישה מצבים, ורק שלושה שונים: מצב חייב לחזור. כאן $q_0$ חוזר מיד, אחרי ה-$0$ הראשון.",
      say="חמישה מצבים, ורק שלושה שונים: מצב חייב לחזור. כאן קיו אפס חוזר מיד, אחרי האפס הראשון.",
      do=show("pg-hs-0", "pg-mark")),
    P("החזרה היא **מעגל** בריצה, ואפשר לסובב אותו כמה פעמים שרוצים: $110$, $00110$, $000110$. כולן מתקבלות.",
      say="החזרה היא מעגל בריצה, ואפשר לסובב אותו כמה פעמים שרוצים: אחת אחת אפס, אפס אפס אחת אחת אפס, "
          "אפס אפס אפס אחת אחת אפס. כולן מתקבלות.", do=show("pg-pump")),
    P("הכלל: אס״ד עם $n$ מצבים שמקבל מילה באורך $n$ **לפחות**, מקבל שפה **אינסופית**.",
      say="הכלל: אסאד עם אן מצבים שמקבל מילה באורך אן לפחות, מקבל שפה אינסופית.", do=show("pg-rule"), hold=0.5),
], stage=st.dfa_svg("pg", D1, POS, N3, w=900, h=300)
         + f'<div id="pg-tr" class="h">{st.trace("pgt", T0, N3).replace(" class=\"h\"", "")}</div>'
         + '<div id="pg-mark" class="h hint">$q_0\\xrightarrow{0}q_0$: מעגל</div>',
   panel=st.card("pg-pump", "ex", "$0^k110$ מתקבלת לכל $k$")
       + st.card("pg-rule", "rule", "🔑 $n$ מצבים ומילה מתקבלת באורך $n$ לפחות: יש מעגל, ולכן $L$ <b>אינסופית</b>"))

opts_html = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $A$ הוא אוטומט המכפלה ל**איחוד** של שתי השפות. איזו טענה נכונה?",
      say="שאלה ממבחן: אֵיי הוא אוטומט המכפלה לאיחוד של שתי השפות. איזו טענה נכונה?"),
    P("הכלי: איך הקבוצה הריקה ו-$\\Sigma^*$ מתנהגות באיחוד ובחיתוך.",
      say="הכלי: איך הקבוצה הריקה וסיגמא כוכבית מתנהגות באיחוד ובחיתוך.", do=show("xt-1")),
    P("$\\emptyset$ **ניטרלית** באיחוד: לא מוסיפה כלום. ובחיתוך היא **בולעת**: התוצאה ריקה.",
      say="הקבוצה הריקה ניטרלית באיחוד: לא מוסיפה כלום. ובחיתוך היא בולעת: התוצאה ריקה.", do=show("xt-2")),
    P("$\\Sigma^*$ הפוך: באיחוד היא בולעת, ובחיתוך היא ניטרלית.",
      say="סיגמא כוכבית הפוך: באיחוד היא בולעת, ובחיתוך היא ניטרלית.", do=show("xt-3")),
    P("לכן אם $L(A_1)$ ריקה, האיחוד הוא בדיוק $L(A_2)$. זו התשובה.",
      say="לכן אם השפה של אֵיי אחת ריקה, האיחוד הוא בדיוק השפה של אֵיי שתיים. זו התשובה.", do=show("q-ok-b")),
    P("המלכודת: אותה טענה עם $\\Sigma^*$. אבל באיחוד $\\Sigma^*$ בולעת, והאיחוד יוצא $\\Sigma^*$.",
      say="המלכודת: אותה טענה עם סיגמא כוכבית. אבל באיחוד סיגמא כוכבית בולעת, והאיחוד יוצא סיגמא כוכבית.",
      do=show("q-x-a", "q-n-a", "xs-a")),
    P("למשל $A_1$ מקבל הכול, ו-$A_2$ רק מילים עם $11$. המילה $0$ באיחוד, ולא ב-$L(A_2)$.",
      say="למשל אֵיי אחת מקבל הכול, ואֵיי שתיים רק מילים עם אחת אחת. המילה אפס באיחוד, ולא בשפה של אֵיי שתיים."),
    P("שתי הטענות על **כל מצב** מקבל: אם כל מצב באיחוד מקבל, אז האיחוד הוא $\\Sigma^*$.",
      say="שתי הטענות על כל מצב מקבל: אם כל מצב באיחוד מקבל, אז האיחוד הוא סיגמא כוכבית.", do=hide("xs-a")),
    P("אבל אם שתי השפות הן המילים עם $11$, האיחוד הוא אותה שפה, ויש בו מצב לא מקבל.",
      say="אבל אם שתי השפות הן המילים עם אחת אחת, האיחוד הוא אותה שפה, ויש בו מצב לא מקבל.",
      do=show("q-x-c", "q-n-c")),
    P("ולמשל שני אוטומטים בני מצב אחד שאינו מקבל: החיתוך ריק, ובאיחוד שלהם אין אף מצב מקבל.",
      do=show("q-x-d", "q-n-d"), hold=0.6),
], stage=fa.FA_CSS
    + '<table class="fa-mini"><thead><tr><th></th><th>איחוד</th><th>חיתוך</th></tr></thead><tbody>'
      '<tr id="xt-1" class="h"><th></th><td>$L\\cup X$</td><td>$L\\cap X$</td></tr>'
      '<tr id="xt-2" class="h"><th>$X=\\emptyset$</th><td>ניטרלי: $L$</td><td>בולע: $\\emptyset$</td></tr>'
      '<tr id="xt-3" class="h"><th>$X=\\Sigma^*$</th><td>בולע: $\\Sigma^*$</td><td>ניטרלי: $L$</td></tr>'
      '</tbody></table>'
      + '<div id="xs-a" class="h">' + fa.shown(st.card("xs-ac", "trap", "⚠️ $\\Sigma^*$ <b>בולעת</b> באיחוד: "
                                                        "$\\Sigma^*\\cup L(A_2)=\\Sigma^*$, לא $L(A_2)$")) + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>{Q["questionHtml"]}</div>'
       + st.options("q", opts_html, notes={"a": "$\\Sigma^*$ בולעת", "c": "שתיהן: מכילות $11$", "d": "שתיהן ריקות"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: $\\varepsilon$ בשפה אם ורק אם ההתחלתי מקבל. ו-$F=Q$ נותן $\\Sigma^*$ רק באס״ד.",
      say="לסיכום: אפסילון בשפה אם ורק אם ההתחלתי מקבל. וכשכל המצבים מקבלים, השפה היא סיגמא כוכבית, רק באסאד.",
      do=show("c1")),
    P("מצב לא ישיג מפיל כל טענה על כל המצבים.", do=show("c2")),
    P("משלים: הופכים מקבלים. במכפלה: חיתוך $f_1f_2$, ואיחוד הכול פחות הזוגות הלא מקבלים.",
      say="משלים: הופכים מקבלים. במכפלה: חיתוך, מכפלת מספרי המקבלים, ואיחוד, הכול פחות הזוגות הלא מקבלים.",
      do=show("c3")),
    P("ומילה מתקבלת באורך $n$ לפחות נותנת שפה אינסופית. נתראה ברמה הבאה.",
      say="ומילה מתקבלת באורך אן לפחות נותנת שפה אינסופית. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=st.dfa_svg("rc", U, {"0": (260, 180), "1": (640, 180)}, N3, w=900, h=300),
   panel=st.card("c1", "rule", "🔑 $\\varepsilon\\in L$ אם ורק אם ההתחלתי מקבל; אם $F=Q$, אז $L=\\Sigma^*$ (רק באס״ד)")
       + st.card("c2", "trap", "⚠️ מצב לא ישיג מפיל טענות על <b>כל</b> המצבים")
       + st.card("c3", "rule", "🔑 חיתוך: $f_1f_2$ מקבלים. איחוד: $n_1n_2-(n_1-f_1)(n_2-f_2)$")
       + st.card("c4", "rule", "🔑 מילה מתקבלת באורך $n$ לפחות: מעגל, ושפה אינסופית"))

VIDEO = Video("F02", "fa", "מבנה של אס״ד: מצב בור, משלים ומכפלה",
              [title, facts, comp, product, count, pigeon, exam, recap],
              bank={"19B-A-Q4": "b"})
