# -*- coding: utf-8 -*-
"""K02 · שפות שנראות קשות ובעצם רגולריות — video script (build: tools/video/vid.py K02).

Source: tools/needhelp/classify/K02.py (lesson + goal). Exam anchor: 24A-B-Q2 (cited by the lesson; trap: the number
of b's "depends on k", which looks like a^n b^n, but k mod 3 ≤ 2 is a bounded count). Second worked example: 24A-A-Q2
(cited by the lesson: bounded sum vs bounded difference).
Not used on purpose: the quiz languages of K02 (i=j=k or i>3, #0 mod 3 = 1, n+2m≤6, n−m≤2, sorted abc) and 19B-B-Q18
(the quiz's first question is its scaled copy).
"""
import re

from nh import classify_cert, dfa_table, words, rank_growing
from vid import Scene, Video, show, hide, run_dfa, BANK
import stage as st
from w_classify import CSS, Pk, opts_panel

CLS = {"finite": "a", "reg": "b", "cfl": "c", "noncfl": "d"}


def ab(w):
    m = re.fullmatch(r"(a*)(b*)", w)
    return None if not m else (len(m.group(1)), len(m.group(2)))


# ---------------------------------------------------------------- example 1: difference counted modulo 3
MOD = lambda w: (w.count("a") - w.count("b")) % 3 == 0
D = dfa_table("ab", {"0": "1 2", "1": "2 0", "2": "0 1"}, "0", {"0"})
assert D.lang(8) == {w for w in words("ab", 8) if MOD(w)}
for w in words("ab", 7):                                   # what each state remembers
    assert int(D.run(w)) == (w.count("a") - w.count("b")) % 3
assert classify_cert(MOD, "ab", ("reg", "(a(ab)*(b+aa)+b(ba)*(a+bb))*")) == "reg"
RUNW = "abaaa"
assert D.accepts(RUNW) and RUNW.count("a") == 4 and RUNW.count("b") == 1      # accepted, counts unequal
EQ = lambda w: w.count("a") == w.count("b")
assert rank_growing(EQ, "ab")                              # the look-alike #a = #b is not regular

# ---------------------------------------------------------------- "or": swallowing vs not swallowing
OR1 = lambda w: ab(w) is not None and (ab(w)[0] == ab(w)[1] or ab(w)[1] > 2)
OR2 = lambda w: ab(w) is not None and (ab(w)[0] == ab(w)[1] or ab(w)[1] < 2)
assert classify_cert(OR1, "ab", ("reg", "ε+ab+aabb+a*bbbb*")) == "reg"
assert classify_cert(OR2, "ab", ("cfl", "S->T|A|Ab;T->aTb|ε;A->aA|ε")) == "cfl"

# ---------------------------------------------------------------- 24A-A-Q2: bounded sum vs bounded difference
C = 2024
assert max(m for m in range(C + 1) if 3 * m <= C) == 674             # n <= 2024 and m <= 674: finitely many words
S4 = lambda w: ab(w) is not None and ab(w)[0] + 3 * ab(w)[1] <= 4    # the same shapes with a small constant
D4 = lambda w: ab(w) is not None and ab(w)[0] - 3 * ab(w)[1] <= 4
assert classify_cert(S4, "ab", ("finite", 4)) == "finite"
assert rank_growing(D4, "ab")
assert all((3 * m + C) - 3 * m <= C for m in range(50))              # a^{3m+2024} b^m in L2: n grows with m
assert BANK["24A-A-Q2"]["correctId"] == "b"                          # L1 regular (finite), L2 not regular

# ---------------------------------------------------------------- exam 24A-B-Q2: a^k b^(k mod 3)
EXL = lambda w: ab(w) is not None and ab(w)[1] == ab(w)[0] % 3
Q = BANK["24A-B-Q2"]
assert CLS[classify_cert(EXL, "ab", ("reg", "(aaa)*(ε+ab+aabb)"))] == Q["correctId"] == "b"
ROWS = [(k, "a" * k + "b" * (k % 3)) for k in range(6)]
assert all(EXL(w) for _, w in ROWS) and [w for _, w in ROWS][:3] == ["", "ab", "aabb"]
assert all(EXL("a" * (3 * n)) for n in range(10))                   # infinite: a^{3n}


def wtex(w):
    """aaaab -> a^4b, '' -> ε (display only)"""
    if not w:
        return "\\varepsilon"
    return "".join(c + (f"^{{{len(g)}}}" if len(g) > 1 else "") for c, g in
                   ((m.group(0)[0], m.group(0)) for m in re.finditer(r"a+|b+", w)))


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    Pk("בסרטון הזה נלמד לזהות שפות שנראות כאילו הן צריכות לספור, אבל בעצם הן רגולריות."),
    Pk("נראה ספירה מודולו, ספירה עד קבוע, תבנית קבועה, ו״או״ שבולע את החלק הקשה.",
       say="נראה ספירה מודולו, ספירה עד קבוע, תבנית קבועה, ואו שבולע את החלק הקשה."),
    Pk("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K02 · סיווג שפות</div><h1>שפות שנראות קשות ובעצם רגולריות</h1>'
         '<p>לזהות מתי ספירה היא בעצם זיכרון סופי: מודולו, עד קבוע, סכום חסום, תבנית קבועה, או ״או״ שבולע.</p>',
   layout="title")

signs = Scene("signs", "הסימנים", [
    Pk("חצי מהשאלות שהתשובה בהן רגולרית ואינסופית נראות כמו שפות שצריכות לספור."),
    Pk("השאלה היא תמיד אחת: האם הספירה דורשת זיכרון **בלתי חסום**? אם לא, השפה רגולרית."),
    Pk("סימן ראשון: ספירה **מודולו**. זוכרים רק שארית, ויש מספר סופי של שאריות.", do=show("g1", "gl1")),
    Pk("סימן שני: ״לפחות ארבע״ או ״עד ארבע״. סופרים עד הקבוע, ועוצרים.",
       say="סימן שני: לפחות ארבע, או עד ארבע. סופרים עד הקבוע, ועוצרים.", do=show("g2", "gl2")),
    Pk("סימן שלישי: תבנית קבועה, כמו גושים בסדר קבוע. יש לה ביטוי רגולרי.", do=show("g3", "gl3")),
    Pk("סימן רביעי: שרשור של שפות רגולריות. רגולריות סגורות לשרשור.", do=show("g4", "gl4")),
    Pk("וסימן חמישי: ״או״ עם תנאי רחב, שבולע את החלק הקשה. נראה אותו עוד מעט.",
       say="וסימן חמישי: או, עם תנאי רחב, שבולע את החלק הקשה. נראה אותו עוד מעט.", do=show("g5", "gl5")),
    Pk("ושימו לב: **שוויון** בין שני מונים, כמו $\\#_a=\\#_b$, הוא לא רגולרי. מודולו כן.",
       do=show("g-trap"), hold=0.5),
], stage=CSS + '<div id="gl1" class="kl-line kl-big h">$\\#_a\\bmod3=0$</div>'
         + '<div id="gl2" class="kl-line kl-big h">$\\#_a\\ge4$</div>'
         + '<div id="gl3" class="kl-line kl-big h">$a^*b^*c^*$</div>'
         + '<div id="gl4" class="kl-line kl-big h">$(aaaa)^*(bbbb)^*$</div>'
         + '<div id="gl5" class="kl-line kl-big h">$i=j\\ \\mathrm{or}\\ j>2$</div>',
   panel=st.card("g1", "plain", "• <b>מודולו</b>: זוכרים רק שארית")
       + st.card("g2", "plain", "• <b>עד קבוע</b>: סופרים עד $k$ ועוצרים")
       + st.card("g3", "plain", "• <b>תבנית קבועה</b>: ביטוי רגולרי")
       + st.card("g4", "plain", "• <b>שרשור</b> של רגולריות: סגירות")
       + st.card("g5", "plain", "• <b>״או״ רחב</b> בולע את החלק הקשה")
       + st.card("g-trap", "trap", "⚠️ שוויון בין מונים ($\\#_a=\\#_b$): <b>לא</b> רגולרית. מודולו: <b>כן</b>."))

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS = {"0": (170, 300), "1": (450, 90), "2": (730, 300)}
run1, s1, left1 = run_dfa("md", D, RUNW, N3, tp="mw", fast=True, lead="נריץ את $abaaa$. מתחילים ב-$q_0$.")
run1[0].do += show("mw-box")
modulo = Scene("modulo", "דוגמה 1: מודולו", [
    Pk("הנה שפה שנראית מסוכנת: המילים שבהן $\\#_a-\\#_b$ מתחלק בשלוש.",
       say="הנה שפה שנראית מסוכנת: המילים שבהן מספר האֵיי פחות מספר הבִּי, מתחלק בשלוש."),
    Pk("נראה שצריך לזכור את שני המונים. אבל צריך לזכור רק את ההפרש **מודולו שלוש**: שלוש אפשרויות.",
       do=show("mo1")),
    Pk("$q_0$, $q_1$, $q_2$ הם השאריות. כל $a$ מוסיף אחת, וכל $b$ מוריד אחת, מודולו שלוש.",
       say="קיו אפס, קיו אחת וקיו שתיים הם השאריות. כל אֵיי מוסיף אחת, וכל בִּי מוריד אחת, מודולו שלוש.",
       do=show("mo2")),
    *run1,
    Pk("ב-$abaaa$ יש ארבע $a$ ו-$b$ אחת: לא שווים, ובכל זאת ההפרש מתחלק בשלוש.",
       say="באֵיי בִּי אֵיי אֵיי אֵיי יש ארבע אֵיי ובִּי אחת: לא שווים, ובכל זאת ההפרש מתחלק בשלוש.",
       do=show("mo3")),
    Pk("שלושה מצבים, וזה הכול: רגולרית ואינסופית. בלי המודולו, $\\#_a=\\#_b$ כבר לא רגולרית.",
       do=hide("mw-box", *left1) + show("mo-trap"), hold=0.5),
], stage=st.dfa_svg("md", D, POS, N3, w=900, h=400)
         + '<div class="swap" style="--swap-h:220px">'
         + f'<div id="mw-box" class="h">{st.tape("mw", RUNW)}{st.trace("mw", s1, N3)}{st.verdict("mw", True)}</div>'
         + '<div id="mo-trap" class="h">' + st.card("mo-trapc", "trap", "⚠️ $\\#_a=\\#_b$: לא רגולרית. "
                                                    "$(\\#_a-\\#_b)\\bmod3=0$: רגולרית.").replace(' h"', '"')
         + '</div></div>',
   panel=st.card("mo1", "rule", "🔑 זוכרים רק את <b>השארית</b>: שלוש אפשרויות")
       + st.card("mo2", "plain", "$q_r$: ההפרש עד עכשיו, מודולו $3$, הוא $r$")
       + st.card("mo3", "ex", "$abaaa$: $\\#_a=4$, $\\#_b=1$, וההפרש $3$"))

orsc = Scene("or", "דוגמה 2: ״או״ שבולע", [
    Pk("עכשיו ״או״. השפה הראשונה: המילים $a^ib^j$ שבהן $i=j$, או $j>2$.",
       say="עכשיו או. השפה הראשונה: המילים אֵיי אַיי בִּי גֵ'יי, שבהן אַיי שווה לגֵ'יי, או גֵ'יי גדול משתיים.",
       do=show("o1", "o1-1")),
    Pk("כל מילה עם יותר משתי $b$ נכנסת, בלי קשר למספר ה-$a$. זה $a^*bbbb^*$.",
       say="כל מילה עם יותר משתי בִּי נכנסת, בלי קשר למספר האֵיי. זה אֵיי כוכבית, שלוש בִּי, ובִּי כוכבית.",
       do=show("o1-2")),
    Pk("מה נשאר מהחלק $i=j$? רק $j\\le2$: המילים $\\varepsilon$, $ab$ ו-$aabb$. חלק סופי.",
       say="מה נשאר מהחלק אַיי שווה לגֵ'יי? רק גֵ'יי קטן או שווה לשתיים: המילים אפסילון, אֵיי בִּי, ואֵיי אֵיי בִּי בִּי. חלק סופי.",
       do=show("o1-3")),
    Pk("סופי איחוד רגולרי הוא רגולרי. השוויון הקשה **נבלע** בתנאי הרחב.", do=show("o1-v", "or-r")),
    Pk("ועכשיו הופכים את התנאי: $i=j$, או $j<2$.",
       say="ועכשיו הופכים את התנאי: אַיי שווה לגֵ'יי, או גֵ'יי קטן משתיים.", do=show("o2", "o2-1")),
    Pk("התנאי $j<2$ צר: הוא לא מכסה את $a^nb^n$ עם $n\\ge2$. החלק הקשה נשאר אינסופי.",
       say="התנאי גֵ'יי קטן משתיים צר: הוא לא מכסה את אֵיי אֶן בִּי אֶן עם אֶן גדול או שווה לשתיים. החלק הקשה נשאר אינסופי.",
       do=show("o2-2")),
    Pk("והשפה הזאת ח״ה ולא רגולרית. אז בודקים: **מי בולע את מי**?",
       do=show("o2-v", "or-t"), hold=0.5),
], stage=CSS + '<div id="o1" class="h"><div id="o1-1" class="kl-line kl-big h">$i=j\\ \\mathrm{or}\\ j>2$</div>'
         + '<div id="o1-2" class="kl-line h">$j>2:\\ a^*bbbb^*$</div>'
         + '<div id="o1-3" class="kl-line h">$i=j\\le2:\\ \\varepsilon,\\ ab,\\ aabb$</div>'
         + st.verdict("o1", True, yes="רגולרית ואינסופית") + '</div>'
         + '<div id="o2" class="h" style="margin-top:30px"><div id="o2-1" class="kl-line kl-big h">$i=j\\ \\mathrm{or}\\ j<2$</div>'
         + '<div id="o2-2" class="kl-line h">$a^nb^n,\\ n\\ge2$</div>'
         + st.verdict("o2", False, no="ח״ה ולא רגולרית") + '</div>',
   panel=st.card("or-r", "rule", "🔑 ״או״ עם תנאי <b>רחב</b>: החלק הקשה נשאר סופי, ולכן רגולרית")
       + st.card("or-t", "trap", "⚠️ ״או״ עם תנאי <b>צר</b> לא בולע: החלק הקשה נשאר אינסופי"))

sumdiff = Scene("sumdiff", "סכום מול הפרש", [
    Pk("ועוד זוג ממבחן. $L_1$: המילים $a^nb^m$ שבהן $n+3m\\le2024$.",
       say="ועוד זוג ממבחן. אֶל אחת: המילים אֵיי אֶן בִּי אֶם, שבהן אֶן ועוד שלוש אֶם קטן או שווה לאלפיים עשרים וארבע.",
       do=show("sd-1")),
    Pk("שני המונים לא שליליים, ולכן $n\\le2024$ וגם $m\\le674$. מספר סופי של מילים: סופית, ולכן רגולרית.",
       say="שני המונים לא שליליים, ולכן אֶן לכל היותר אלפיים עשרים וארבע, ואֶם לכל היותר שש מאות שבעים וארבע. מספר סופי של מילים: סופית, ולכן רגולרית.",
       do=show("sd-1b", "sd-r1")),
    Pk("$L_2$: אותו דבר, אבל עם מינוס: $n-3m\\le2024$.",
       say="אֶל שתיים: אותו דבר, אבל עם מינוס: אֶן פחות שלוש אֶם, קטן או שווה לאלפיים עשרים וארבע.",
       do=show("sd-2")),
    Pk("עכשיו $n$ יכול לגדול בלי גבול, כל עוד $m$ גדל איתו. למשל $a^{3m+2024}b^m$.",
       say="עכשיו אֶן יכול לגדול בלי גבול, כל עוד אֶם גדל איתו. למשל אֵיי בחזקת שלוש אֶם ועוד אלפיים עשרים וארבע, בִּי אֶם.",
       do=show("sd-2b")),
    Pk("כדי לבדוק אם הגיעו מספיק $b$, צריך לזכור את $n$ במדויק: לא רגולרית. את ההוכחה נראה ברמה הבאה.",
       say="כדי לבדוק אם הגיעו מספיק בִּי, צריך לזכור את אֶן במדויק: לא רגולרית. את ההוכחה נראה ברמה הבאה.",
       do=show("sd-r2")),
    Pk("זו המלכודת: שתי שפות כמעט זהות, והסימן אחד משנה הכול. סכום חסום: סופית. הפרש חסום: לא רגולרית.",
       do=show("sd-t"), hold=0.5),
], stage=CSS + '<span class="qid">24A-A-Q2</span>'
         + '<div id="sd-1" class="kl-line kl-big h">$L_1:\\ n+3m\\le2024$</div>'
         + '<div id="sd-1b" class="kl-line h">$n\\le2024,\\ m\\le674$</div>'
         + '<div id="sd-2" class="kl-line kl-big h">$L_2:\\ n-3m\\le2024$</div>'
         + '<div id="sd-2b" class="kl-line h">$a^{3m+2024}b^m\\in L_2$</div>',
   panel=st.card("sd-r1", "rule", "🔑 אם <b>הסכום חסום</b>, אז השפה סופית, ולכן רגולרית")
       + st.card("sd-r2", "rule", "🔑 <b>הפרש חסום</b>: צריך לזכור את $n$, ולכן לא רגולרית")
       + st.card("sd-t", "trap", "⚠️ פלוס או מינוס: סימן אחד משנה את התשובה"))

TAB = ('<table class="kl-grid" id="xt" dir="ltr"><thead><tr><th>$k$</th>'
       + "".join(f"<th>${k}$</th>" for k, _ in ROWS) + '</tr></thead><tbody><tr><th>$w$</th>'
       + "".join(f'<td><span id="xt-{k}" class="h">${wtex(w)}$</span></td>' for k, w in ROWS) + '</tr></tbody></table>')
exam = Scene("exam", "שאלה ממבחן", [
    Pk("ועכשיו שאלה אמיתית ממבחן: $L=\\{a^kb^{k\\bmod3}\\}$.",
       say="ועכשיו שאלה אמיתית ממבחן: אֶל היא אֵיי קֵיי, בִּי בחזקת קֵיי מודולו שלוש."),
    Pk("המלכודת: מספר ה-$b$ **תלוי** במספר ה-$a$. זה נראה כמו $a^nb^n$, ואז בוחרים ח״ה ולא רגולרית.",
       do=show("x-trap")),
    Pk("אבל בואו נכתוב כמה מילים. $k=0$: המילה הריקה. $k=1$: $ab$. $k=2$: $aabb$.",
       say="אבל בואו נכתוב כמה מילים. קֵיי שווה אפס: המילה הריקה. קֵיי שווה אחת: אֵיי בִּי. קֵיי שווה שתיים: אֵיי אֵיי בִּי בִּי.",
       do=hide("x-trap") + show("xt", "xt-0", "xt-1", "xt-2")),
    Pk("$k=3$: שלוש $a$ ואף $b$. ואז זה חוזר על עצמו: $a^4b$, $a^5b^2$.",
       say="קֵיי שווה שלוש: שלוש אֵיי, ואף בִּי. ואז זה חוזר על עצמו: ארבע אֵיי ובִּי אחת, חמש אֵיי ושתי בִּי.",
       do=show("xt-3", "xt-4", "xt-5")),
    Pk("השארית של $k$ היא $0$, $1$ או $2$. לכן יש **לכל היותר שתי** $b$: ספירה עד קבוע.",
       say="השארית של קֵיי היא אפס, אחת או שתיים. לכן יש לכל היותר שתי בִּי: ספירה עד קבוע.",
       do=show("x-r")),
    Pk("והביטוי: $(aaa)^*(\\varepsilon+ab+aabb)$. קבוצות של שלוש $a$, ואז אחת משלוש סיומות.",
       say="והביטוי: אֵיי אֵיי אֵיי כוכבית, ואחריו אפסילון, או אֵיי בִּי, או אֵיי אֵיי בִּי בִּי. קבוצות של שלוש אֵיי, ואז אחת משלוש סיומות.",
       do=show("x-rx")),
    Pk("סופית? לא: כל $a^{3n}$ בשפה.", say="סופית? לא: כל אֵיי בחזקת שלוש אֶן בשפה.", do=show("q-x-a", "q-n-a")),
    Pk("ח״ה ולא רגולרית, או לא ח״ה? לא, כי מצאנו ביטוי רגולרי.",
       do=show("q-x-c", "q-n-c", "q-x-d", "q-n-d")),
    Pk("התשובה: רגולרית ואינסופית. ״תלוי ב-$k$״ לא אומר ״צריך לזכור את $k$״: מספיקה השארית.",
       say="התשובה: רגולרית ואינסופית. תלוי בקֵיי, לא אומר שצריך לזכור את קֵיי: מספיקה השארית.",
       do=show("q-ok-b"), hold=0.6),
], stage=CSS + TAB + '<div id="x-r" class="kl-line h">$k\\bmod3\\in\\{0,1,2\\}$</div>'
         + '<div id="x-rx" class="kl-line kl-big h">$L=(aaa)^*(\\varepsilon+ab+aabb)$</div>'
         + st.card("x-trap", "trap", "⚠️ מספר ה-$b$ <b>תלוי</b> ב-$k$, אבל הוא <b>חסום</b>"),
   panel=opts_panel("q", Q, notes={"a": "$a^{3n}\\in L$", "c": "יש ביטוי", "d": "יש ביטוי"}))

recap = Scene("recap", "סיכום", [
    Pk("לסיכום: מודולו, עד קבוע, תבנית קבועה ושרשור של רגולריות: זיכרון סופי, רגולרית.", do=show("c1")),
    Pk("״או״ עם תנאי רחב בולע את החלק הקשה. תנאי צר לא בולע.", say="או, עם תנאי רחב, בולע את החלק הקשה. תנאי צר לא בולע.",
       do=show("c2")),
    Pk("סכום חסום: סופית. הפרש חסום: לא רגולרית.", do=show("c3")),
    Pk("ושוויון בין שני מונים לא רגולרי, אבל מודולו כן. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=st.dfa_svg("rc", D, POS, N3, w=900, h=400),
   panel=st.card("c1", "rule", "🔑 מודולו / עד קבוע / תבנית / שרשור: רגולרית")
       + st.card("c2", "rule", "🔑 ״או״ רחב בולע; ״או״ צר לא")
       + st.card("c3", "rule", "🔑 סכום חסום: סופית. הפרש חסום: לא רגולרית")
       + st.card("c4", "trap", "⚠️ $\\#_a=\\#_b$ לא רגולרית; $\\#_a\\bmod3=0$ כן"))

VIDEO = Video("K02", "classify", "שפות שנראות קשות ובעצם רגולריות",
              [title, signs, modulo, orsc, sumdiff, exam, recap],
              bank={"24A-B-Q2": "b", "24A-A-Q2": "b"})
