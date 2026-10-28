# -*- coding: utf-8 -*-
"""K01 · ההיררכיה ואלגוריתם הסיווג — video script (build: tools/video/vid.py K01).

Source: tools/needhelp/classify/K01.py (lesson + goal). Exam anchor: 23A-A-Q8 (cited by the lesson; trap: three
compared lengths look like a^n b^n c^n, but the split is ours to choose, so L = Σ*). Worked "simplify first" examples:
23A-B-Q8 and 21S-A-Q8 (both cited by the lesson, not by the quiz).
Not used on purpose: the quiz languages of K01 (n+m≤4, i≤j≤i, a^nb^n as a question, a^nb^nc^n as a question, i≤2 or j≤2).
Every classification below is certified with lib.classify_cert before anything is rendered.
"""
import re

from nh import classify_cert, words, same_pred
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_classify import CSS, Pk, ladder, arcs, pump, opts_panel

# ---------------------------------------------------------------- languages (verified)
def blocks(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


FIN = lambda w: w in {"a", "aa", "aaa"}
AST = lambda w: set(w) <= {"a"}
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(blocks(w, "ab"))
ANBNCN = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(blocks(w, "abc"))
assert classify_cert(FIN, "ab", ("finite", 3)) == "finite"
assert classify_cert(AST, "ab", ("reg", "a*")) == "reg"
assert classify_cert(ANBN, "ab", ("cfl", "S->aSb|ε")) == "cfl"
assert classify_cert(ANBNCN, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7) == "noncfl"

CLS = {"finite": "a", "reg": "b", "cfl": "c", "noncfl": "d"}      # option ids of the standard four-way question

# 23A-B-Q8: i<=k and k<=m and m<=i  ==  i=k=m
Q8B = lambda w: (lambda t: t is not None and t[0] <= t[1] and t[1] <= t[2] and t[2] <= t[0])(blocks(w, "abc"))
assert same_pred(Q8B, ANBNCN, "abc", 7)
assert CLS[classify_cert(Q8B, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7)] \
    == BANK["23A-B-Q8"]["correctId"] == "d"

# 21S-A-Q8: a b^n b^n a, n>=1  ==  abb(bb)*a
Q8S = lambda w: any(w == "a" + "b" * (2 * n) + "a" for n in range(1, 8))
assert CLS[classify_cert(Q8S, "ab", ("reg", "abb(bb)*a"))] == BANK["21S-A-Q8"]["correctId"] == "b"

# exam 23A-A-Q8: { xyz : |x| <= |y| <= |z| }  ==  Σ*   (x = y = ε always works)
def xyz(w):
    return any(a <= b - a <= len(w) - b for a in range(len(w) + 1) for b in range(a, len(w) + 1))
assert all(xyz(w) for w in words("ab", 9))
assert all(0 <= 0 <= len(w) for w in words("ab", 9))                     # the split x = y = ε, z = w
Q = BANK["23A-A-Q8"]
assert CLS[classify_cert(xyz, "ab", ("reg", "(a+b)*"))] == Q["correctId"] == "b"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    Pk("בסרטון הזה נלמד לסווג שפה לפי הסולם: סופית, רגולרית, חסרת הקשר, או לא."),
    Pk("נלמד לפשט את ההגדרה לפני שמחליטים, ולשאול כמה זיכרון השפה צריכה."),
    Pk("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K01 · סיווג שפות</div><h1>ההיררכיה ואלגוריתם הסיווג</h1>'
         '<p>לסווג שפה לפי הסולם: סופית, רגולרית, חסרת הקשר, או לא, ולפשט את הגדרתה לפני שמחליטים.</p>',
   layout="title")

LAD = ladder("ld", [("fin", "fin", "$\\{a,aa,aaa\\}$"), ("reg", "reg", "$a^*$"),
                    ("cfl", "cfl", "$\\{a^nb^n\\}$"), ("all", "all", "$\\{a^nb^nc^n\\}$")])
ladder_sc = Scene("ladder", "הסולם", [
    Pk("שאלת הסיווג היא המשפחה הגדולה בבנק: שבעים שאלות. וכמעט תמיד יש בה אותן ארבע תשובות.",
       do=show("l-o1", "l-o2", "l-o3", "l-o4")),
    Pk("הנה הסולם. בפנים, השפות הסופיות, למשל $\\{a,aa,aaa\\}$.", do=show("ld-hl-fin", "ld-c-fin")),
    Pk("סביבן, השפות הרגולריות. $a^*$ רגולרית, אבל היא לא סופית.",
       do=hide("ld-hl-fin") + show("ld-hl-reg", "ld-c-reg")),
    Pk("סביבן, השפות חסרות ההקשר. $a^nb^n$ היא ח״ה, אבל לא רגולרית.",
       do=hide("ld-hl-reg") + show("ld-hl-cfl", "ld-c-cfl")),
    Pk("ובחוץ, כל השאר. $a^nb^nc^n$ אפילו לא ח״ה.", do=hide("ld-hl-cfl") + show("ld-hl-all", "ld-c-all")),
    Pk("כל שפה סופית היא רגולרית. וכל שפה רגולרית היא ח״ה: אס״ד הוא אוטומט מחסנית שלא נוגע במחסנית.",
       do=hide("ld-hl-all")),
    Pk("לכן ארבע התשובות **מוציאות זו את זו**: כל שפה נמצאת בדיוק בטבעת אחת.", do=show("l-rule")),
    Pk("ולכן שואלים תמיד מלמטה למעלה: קודם סופית? אחר כך רגולרית? ואחר כך ח״ה?", hold=0.5),
], stage=CSS + LAD,
   panel=st.card("l-o1", "plain", "• סופית") + st.card("l-o2", "plain", "• רגולרית ואינסופית")
       + st.card("l-o3", "plain", "• ח״ה ולא רגולרית") + st.card("l-o4", "plain", "• לא ח״ה")
       + st.card("l-rule", "rule", "🔑 סופיות $\\subsetneq$ רגולריות $\\subsetneq$ ח״ה $\\subsetneq$ כל השפות"))

memory = Scene("memory", "כמה זיכרון?", [
    Pk("איך מנחשים באיזו טבעת השפה נמצאת? שואלים: **כמה זיכרון** צריך כדי לבדוק מילה?"),
    Pk("כמות חסומה: ספירה עד קבוע, ספירה מודולו, או תבנית קבועה. זה זיכרון סופי, ולכן רגולרית.",
       do=show("m-1")),
    Pk("מונה אחד שעולה ואז יורד: ב-$a^nb^n$ סופרים את ה-$a$, ומורידים אחד עם כל $b$.",
       do=show("mw1", "ma1-a-0")),
    Pk("זו השוואה אחת, ומחסנית יודעת לעשות אותה: ח״ה.", do=show("m-2")),
    Pk("ב-$a^nb^nc^n$ צריך להשוות שלוש כמויות בבת אחת: $a$ מול $b$, וגם $b$ מול $c$.",
       do=show("mw2", "ma2-a-0", "ma2-a-1")),
    Pk("האינטואיציה: אחרי שהמחסנית השוותה את ה-$a$ ל-$b$, היא ריקה, ואין לה במה להשוות את ה-$c$."),
    Pk("זו האינטואיציה; ההוכחה: למת הניפוח לח״ה, או טבלת השפות בדף הנוסחאות. לא ח״ה.",
       do=show("m-3"), hold=0.5),
], stage=CSS + '<div id="mw1" class="h">' + arcs("ma1", ["$a^n$", "$b^n$"], [(0, 1)], hmax=90) + '</div>'
         + '<div id="mw2" class="h">' + arcs("ma2", ["$a^n$", "$b^n$", "$c^n$"], [(0, 1), (1, 2)], hmax=90) + '</div>',
   panel=st.card("m-1", "rule", "🔑 זיכרון חסום (עד קבוע, מודולו, תבנית): <b>רגולרית</b>")
       + st.card("m-2", "rule", "🔑 מונה אחד שעולה ויורד: <b>ח״ה</b>")
       + st.card("m-3", "rule", "🔑 שלוש כמויות בבת אחת: <b>לא ח״ה</b>"))

EX1 = ('<div id="e1" class="h"><span class="qid">23A-B-Q8</span>'
       '<div id="e1-1" class="kl-line kl-big h">$i\\le k,\\ k\\le m,\\ m\\le i$</div>'
       '<div id="e1-2" class="kl-line kl-big h">$i\\le k\\le m\\le i\\ \\Rightarrow\\ i=k=m$</div>'
       '<div id="e1-3" class="kl-line kl-big h">$L=\\{a^nb^nc^n\\}$</div>'
       + st.verdict("e1", False, no="לא ח״ה") + '</div>')
EX2 = ('<div id="e2" class="h"><span class="qid">21S-A-Q8</span>'
       '<div id="e2-1" class="kl-line kl-big h">$ab^nb^na,\\ n\\ge1$</div>'
       '<div id="e2-2" class="kl-line kl-big h">$b^nb^n=b^{2n}$</div>'
       '<div id="e2-3" class="kl-line kl-big h">$L=abb(bb)^*a$</div>'
       + st.verdict("e2", True, yes="רגולרית ואינסופית") + '</div>')
algo = Scene("algo", "האלגוריתם", [
    Pk("האלגוריתם בארבעה צעדים. הצעד הראשון הוא החשוב ביותר: **פשטו את ההגדרה לפני הכול**.", do=show("s1")),
    Pk("דוגמה ממבחן: המילים $a^ib^kc^m$, שבהן $i\\le k$, $k\\le m$, וגם $m\\le i$.",
       say="דוגמה ממבחן: המילים אֵיי אַיי, בִּי קֵיי, סִי אֶם, שבהן אַיי קטן או שווה לקֵיי, קֵיי קטן או שווה לאֶם, וגם אֶם קטן או שווה לאַיי.",
       do=show("e1", "e1-1")),
    Pk("נשרשר את התנאים: $i\\le k\\le m\\le i$. השרשרת חוזרת ל-$i$, ולכן כולם שווים.",
       say="נשרשר את התנאים: אַיי, קֵיי, אֶם, ושוב אַיי. השרשרת חוזרת לאַיי, ולכן כולם שווים.", do=show("e1-2")),
    Pk("כלומר $L=\\{a^nb^nc^n\\}$, ומדף הנוסחאות: היא לא ח״ה. שלושה אי-שוויונים הם בעצם שוויון.",
       say="כלומר, אֶל היא אֵיי אֶן בִּי אֶן סִי אֶן, ומדף הנוסחאות: היא לא חסרת הקשר. שלושה אי שוויונים הם בעצם שוויון.",
       do=show("e1-3", "e1-v"), hold=0.4),
    Pk("עוד דוגמה ממבחן: $ab^nb^na$, עם $n\\ge1$.", say="עוד דוגמה ממבחן: אֵיי, בִּי אֶן, בִּי אֶן, אֵיי, עם אֶן גדול או שווה לאחת.",
       do=hide("e1") + show("e2", "e2-1")),
    Pk("$b^nb^n$ הוא פשוט $b^{2n}$: מספר זוגי של $b$, לפחות שניים. אין כאן שום השוואה.",
       say="בִּי אֶן בִּי אֶן הוא פשוט בִּי בחזקת שתיים אֶן: מספר זוגי של בִּי, לפחות שניים. אין כאן שום השוואה.",
       do=show("e2-2")),
    Pk("הביטוי $abb(bb)^*a$ מתאר אותה. היא רגולרית ואינסופית.",
       say="הביטוי אֵיי בִּי בִּי, סוגריים בִּי בִּי כוכבית, אֵיי, מתאר אותה. היא רגולרית ואינסופית.",
       do=show("e2-3", "e2-v"), hold=0.4),
    Pk("אחרי הפישוט עולים בסולם. האם היא סופית? אורכים חסומים פירושם סופית, ולכן גם רגולרית.",
       do=hide("e2") + show("s2")),
    Pk("האם היא רגולרית? מחפשים ביטוי או אס״ד. אם אין, מוכיחים שהיא לא רגולרית.", do=show("s3")),
    Pk("האם היא ח״ה? מחפשים דקדוק או אוטומט מחסנית. ואם אין, מוכיחים שהיא לא ח״ה.", do=show("s4")),
    Pk("ועוד דבר: התשובה **סופית** לא הייתה נכונה אף פעם בבנק. אבל היא שלב ביניים מצוין: סופית, ולכן רגולרית.",
       do=show("a-trap"), hold=0.5),
], stage=CSS + '<div class="swap" style="--swap-h:470px">' + EX1 + EX2
         + '<div id="a-trap" class="h">' + st.card("a-trapc", "trap", "⚠️ <b>סופית</b> לא הייתה אף פעם התשובה בבנק, "
                                                    "אבל &quot;סופית, ולכן רגולרית&quot; הוא צעד ביניים.").replace(' h"', '"')
         + '</div></div>',
   panel=st.card("s1", "rule", "1. <b>פשטו את ההגדרה</b> לפני הכול")
       + st.card("s2", "plain", "2. סופית? אם האורכים חסומים, אז סופית, ולכן רגולרית")
       + st.card("s3", "plain", "3. רגולרית? ביטוי או אס״ד. אם לא: הוכחת אי-רגולריות")
       + st.card("s4", "plain", "4. ח״ה? דקדוק או אוטומט מחסנית. אם לא: הוכחה שאינה ח״ה"))

exam = Scene("exam", "שאלה ממבחן", [
    Pk("ועכשיו שאלה אמיתית ממבחן: $L$ היא כל המילים $xyz$ שבהן $|x|\\le|y|\\le|z|$.",
       say="ועכשיו שאלה אמיתית ממבחן: אֶל היא כל המילים אקס וואי זד, שבהן האורך של אקס קטן או שווה לאורך של וואי, שקטן או שווה לאורך של זד."),
    Pk("זו המלכודת: שלושה אורכים שמושווים זה לזה נראים בדיוק כמו $a^nb^nc^n$. הרבה בוחרים לא ח״ה.",
       do=show("x-trap")),
    Pk("אבל רגע. מתי מילה $w$ בשפה? כש**קיים** פירוק אחד שלה שמקיים את התנאי.", do=hide("x-trap")),
    Pk("ואת הפירוק בוחרים אנחנו. ניקח את $x$ ואת $y$ ריקות, ואת $z$ כל המילה.",
       do=show("xt", "xt-s-e")),
    Pk("אז $|x|=|y|=0$, וזה תמיד קטן או שווה ל-$|z|$. התנאי מתקיים לכל מילה.",
       say="אז האורך של אקס והאורך של וואי שווים לאפס, וזה תמיד קטן או שווה לאורך של זד. התנאי מתקיים לכל מילה.",
       do=show("x-eq")),
    Pk("לכן כל מילה בשפה: $L=\\Sigma^*$.", say="לכן כל מילה בשפה: אֶל שווה לסיגמא כוכבית.", do=show("x-sig")),
    Pk("סופית? לא, יש בה את כל המילים.", do=show("q-x-a", "q-n-a")),
    Pk("ח״ה ולא רגולרית, או לא ח״ה? גם לא, כי $\\Sigma^*$ רגולרית.",
       say="חסרת הקשר ולא רגולרית, או לא חסרת הקשר? גם לא, כי סיגמא כוכבית רגולרית.",
       do=show("q-x-c", "q-n-c", "q-x-d", "q-n-d")),
    Pk("התשובה: רגולרית ואינסופית. ההגדרה המסובכת הסתירה שפה פשוטה מאוד.", do=show("q-ok-b"), hold=0.6),
], stage=CSS + '<div id="xt" class="h">' + pump("xt", "abba", splits={"e": (0, 0)}) + '</div>'
         + '<div id="x-eq" class="kl-line kl-big h">$x=y=\\varepsilon,\\ z=w$</div>'
         + '<div id="x-sig" class="kl-line kl-big h">$L=\\Sigma^*$</div>'
         + st.card("x-trap", "trap", "⚠️ שלושה אורכים מושווים &ne; $a^nb^nc^n$: <b>הפירוק נבחר על ידינו</b>"),
   panel=opts_panel("q", Q, notes={"a": "מכילה הכול", "c": "רגולרית", "d": "רגולרית"}))

recap = Scene("recap", "סיכום", [
    Pk("לסיכום: סופיות בתוך רגולריות, בתוך ח״ה, בתוך כל השפות. ארבע התשובות מוציאות זו את זו.", do=show("c1")),
    Pk("לפני הכול מפשטים: שרשרת שנסגרת היא שוויון, וחלקים בפירוק יכולים להיות ריקים.", do=show("c2")),
    Pk("כמה זיכרון? חסום: רגולרית. מונה אחד שעולה ויורד: ח״ה. שלוש כמויות בבת אחת: לא ח״ה.", do=show("c3")),
    Pk("ו**סופית** היא שלב ביניים, לא תשובה. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=CSS + LAD.replace('id="ld', 'id="rl').replace('kl-chip h"', 'kl-chip"'),
   panel=st.card("c1", "rule", "🔑 סופיות $\\subsetneq$ רגולריות $\\subsetneq$ ח״ה $\\subsetneq$ הכול")
       + st.card("c2", "rule", "🔑 מפשטים לפני שמסווגים")
       + st.card("c3", "rule", "🔑 חסום: רגולרית. מונה אחד: ח״ה. שלוש כמויות בבת אחת: לא ח״ה")
       + st.card("c4", "trap", "⚠️ <b>סופית</b>: צעד ביניים, לא תשובה"))

VIDEO = Video("K01", "classify", "ההיררכיה ואלגוריתם הסיווג",
              [title, ladder_sc, memory, algo, exam, recap],
              bank={"23A-A-Q8": "b", "23A-B-Q8": "d", "21S-A-Q8": "b"})
