# -*- coding: utf-8 -*-
"""K04 · משחק למת הניפוח לשפות רגולריות — video script (build: tools/video/vid.py K04).

Source: tools/needhelp/classify/K04.py (lesson + goal). Exam anchor: 26A-A-Q5 (cited by the lesson; traps: a free
letter at the start (c^n a^n b^n), a balanced unit (abc^{2n}), a safety margin (a^{2n} b^n c^{2n})).
Worked examples: the game on {a^k b^k} with w = a^n b^n (drawn with n = 4), and the traps "fixed length" (a^{50}b^{50})
and "balanced unit" ((ab)^n) on {#a = #b}.
Not used on purpose: the quiz languages of K04 (a^k b^m c^k, a^n b^m with n>m, ww^R, a^{k^2}) and the exam questions
on those languages (24A-C-Q6, 24X-C-Q4, 24X-A-Q4, 24A-B-Q5).
Every claim about a word is checked with lib.pump_breaks / pump_adversary_split for n = 2..7 before rendering.
"""
import re

from nh import pump_breaks, pump_word_works, pump_adversary_split
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_classify import CSS, Pk, pump, opts_panel, wtex

NS = range(2, 8)
IP = range(0, 7)


def splits(w, n):
    return [(w[:a], w[a:b], w[b:]) for a in range(n + 1) for b in range(a + 1, min(n, len(w)) + 1)]


# ---------------------------------------------------------------- example 1: {a^k b^k}, w = a^n b^n
ANBN = lambda w: (lambda m: m is not None and len(m.group(1)) == len(m.group(2)))(re.fullmatch(r"(a*)(b*)", w))
for n in NS:
    w = "a" * n + "b" * n
    assert ANBN(w) and len(w) >= n
    for x, y, z in splits(w, n):
        assert set(y) == {"a"} and not ANBN(x + z)               # y is inside the a's; i = 0 always breaks
assert pump_word_works(ANBN, lambda n: "a" * n + "b" * n, NS, IP)
N = 4
W1 = "a" * N + "b" * N
SPL1 = {"1": (1, 3), "2": (0, 4)}
OUT1 = {k: W1[:a] + W1[b:] for k, (a, b) in SPL1.items()}         # x z  (i = 0)
assert OUT1 == {"1": "aabbbb", "2": "bbbb"} and not any(ANBN(v) for v in OUT1.values())

# ---------------------------------------------------------------- example 2: traps on {#a = #b}
EQ = lambda w: w.count("a") == w.count("b")
W50 = "a" * 50 + "b" * 50
assert pump_breaks(EQ, W50, 50, IP)                                # fine while n <= 50 ...
assert not pump_breaks(EQ, W50, 120, IP) and len(W50) < 120        # ... but useless when the adversary picks n = 120
for n in NS:                                                       # (ab)^n: the adversary takes y = ab
    w = "ab" * n
    assert EQ(w) and not pump_breaks(EQ, w, n, IP)
    assert all(EQ("ab" * i + w[2:]) for i in IP)
assert pump_word_works(EQ, lambda n: "a" * n + "b" * n, NS, IP)
WAB = "ab" * N

# ---------------------------------------------------------------- exam 26A-A-Q5: #a >= #b over {a,b,c}
GE = lambda w: w.count("a") >= w.count("b")
Q = BANK["26A-A-Q5"]
WORD = {"a": lambda n: "a" * (2 * n) + "b" * n + "c" * (2 * n), "b": lambda n: "ab" + "c" * (2 * n),
        "c": lambda n: "c" * n + "a" * n + "b" * n, "d": lambda n: "a" * n + "c" * n + "b" * n}
assert {o["id"]: o["value"] for o in Q["options"]} == {"a": "a^{2n}b^nc^{2n}", "b": "abc^{2n}",
                                                      "c": "c^na^nb^n", "d": "a^nc^nb^n"}
WIN = {k: pump_word_works(GE, f, NS, IP) for k, f in WORD.items()}
assert [k for k, v in WIN.items() if v] == [Q["correctId"]] == ["d"]
for n in NS:
    assert all(GE(WORD[k](n)) for k in WORD)                       # every option is in L: no "not in L" shortcut
    assert all(GE("ab" * i + "c" * (2 * n)) for i in IP)           # abc^{2n}: y = ab survives
    assert all(GE("c" * i + "c" * (n - 1) + "a" * n + "b" * n) for i in IP)          # c^n a^n b^n: y = c survives
    w = WORD["a"](n)
    assert all(GE(w[:0] + "a" * i + w[1:]) for i in IP)            # a^{2n} b^n c^{2n}: y = a survives (margin n)
    for x, y, z in splits(WORD["d"](n), n):
        assert set(y) == {"a"} and not GE(x + z)                   # a^n c^n b^n: y = a^j, i = 0 breaks
WX = WORD["c"](N)
WD = WORD["d"](N)
assert WD[:1] + WD[3:] == "aa" + "c" * N + "b" * N and not GE(WD[:1] + WD[3:])                                       # the drawn split x=a, y=aa: x z = a^2 c^4 b^4

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    Pk("בסרטון הזה נשחק את המשחק של למת הניפוח לשפות רגולריות."),
    Pk("נלמד לבחור מילה שמביאה **בהכרח** לסתירה, ולזהות את שלוש המלכודות: אות חופשית, יחידה מאוזנת, ואורך קבוע."),
    Pk("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K04 · סיווג שפות</div><h1>משחק למת הניפוח לשפות רגולריות</h1>'
         '<p>לבחור את המילה שמביאה בהכרח לסתירה בלמת הניפוח, ולפסול מילים שנופלות על אות חופשית, יחידה מאוזנת או אורך קבוע.</p>',
   layout="title")

game = Scene("game", "הלמה כמשחק", [
    Pk("הלמה אומרת: אם $L$ רגולרית, יש קבוע $n$, כך שכל מילה ב-$L$ באורך לפחות $n$ אפשר לנפח.",
       say="הלמה אומרת: אם אֶל רגולרית, יש קבוע אֶן, כך שכל מילה באֶל, באורך לפחות אֶן, אפשר לנפח.",
       do=show("gm-lem")),
    Pk("כלומר לפרק אותה ל-$xyz$, עם $|xy|\\le n$ ו-$y\\ne\\varepsilon$, כך ש-$xy^iz\\in L$ לכל $i\\ge0$.",
       say="כלומר לפרק אותה לאקס וואי זד, כשהאורך של אקס וואי קטן או שווה לאֶן, ווואי לא ריקה, כך שאקס, וואי בחזקת אַיי, זד, בשפה, לכל אַיי."),
    Pk("ועכשיו בתור משחק. צעד ראשון: **היריב** בוחר את $n$. אנחנו לא יודעים כמה הוא.",
       say="ועכשיו בתור משחק. צעד ראשון: היריב בוחר את אֶן. אנחנו לא יודעים כמה הוא.", do=show("gm-1")),
    Pk("צעד שני: **אנחנו** בוחרים מילה $w$ בשפה, באורך לפחות $n$.",
       say="צעד שני: אנחנו בוחרים מילה דאבל יו בשפה, באורך לפחות אֶן.", do=show("gm-2")),
    Pk("צעד שלישי: **היריב** מפרק אותה, כרצונו, לפי הכללים.", do=show("gm-3")),
    Pk("צעד רביעי: **אנחנו** בוחרים $i$. אם המילה המנופחת יצאה מהשפה, ניצחנו.",
       say="צעד רביעי: אנחנו בוחרים אַיי. אם המילה המנופחת יצאה מהשפה, ניצחנו.", do=show("gm-4")),
    Pk("והעיקר: צריך לנצח **כל** פירוק חוקי. מילה שיש לה אפילו פירוק אחד בטוח לא שווה כלום.",
       do=show("gm-key"), hold=0.5),
], stage=CSS + st.card("gm-lem", "rule", "<b>הלמה:</b> אם $L$ רגולרית, אז קיים $n$, כך שלכל $w\\in L$ עם $|w|\\ge n$ "
                                        "יש פירוק $w=xyz$ עם $|xy|\\le n$, $y\\ne\\varepsilon$, ו-$xy^iz\\in L$ לכל $i\\ge0$."),
   panel=st.card("gm-1", "plain", "1. <b>היריב</b> בוחר את $n$")
       + st.card("gm-2", "plain", "2. <b>אנחנו</b> בוחרים $w\\in L$, $|w|\\ge n$")
       + st.card("gm-3", "plain", "3. <b>היריב</b> בוחר פירוק $xyz$")
       + st.card("gm-4", "plain", "4. <b>אנחנו</b> בוחרים $i$, ו-$xy^iz\\notin L$")
       + st.card("gm-key", "rule", "🔑 מנצחים רק אם <b>כל</b> פירוק חוקי נשבר"))

ex1 = Scene("ex1", "דוגמה 1: המשחק", [
    Pk("נשחק על $\\{a^kb^k\\}$. נבחר $w=a^nb^n$. נצייר אותה עם $n=4$, אבל ההוכחה לכל $n$.",
       say="נשחק על השפה אֵיי קֵיי בִּי קֵיי. נבחר דאבל יו שווה אֵיי אֶן בִּי אֶן. נצייר אותה עם אֶן שווה ארבע, אבל ההוכחה לכל אֶן.",
       do=show("t1")),
    Pk("היא בשפה, ואורכה $2n$, לפחות $n$. עכשיו תור היריב.",
       say="היא בשפה, ואורכה שתיים אֶן, לפחות אֶן. עכשיו תור היריב."),
    Pk("הכלל $|xy|\\le n$ אומר: $x$ ו-$y$ נמצאות בתוך $n$ האותיות **הראשונות**.",
       say="הכלל, האורך של אקס וואי קטן או שווה לאֶן, אומר: אקס ווואי נמצאות בתוך אֶן האותיות הראשונות.",
       do=show("t1-n")),
    Pk("ושם יש רק $a$. אז לא משנה איך היריב מפרק, $y$ היא כמה $a$.",
       say="ושם יש רק אֵיי. אז לא משנה איך היריב מפרק, וואי היא כמה אֵיי."),
    Pk("למשל $x=a$ ו-$y=aa$. אנחנו בוחרים $i=0$, כלומר מוחקים את $y$: נשאר $a^2b^4$.",
       say="למשל אקס שווה אֵיי, ווואי שווה אֵיי אֵיי. אנחנו בוחרים אַיי שווה אפס, כלומר מוחקים את וואי: נשאר אֵיי בריבוע, בִּי בחזקת ארבע.",
       do=show("t1-s-1", "o1-1")),
    Pk("פחות $a$ מ-$b$: מחוץ לשפה.", say="פחות אֵיי מבִּי: מחוץ לשפה."),
    Pk("פירוק אחר: $y=aaaa$. שוב $i=0$, ונשאר $b^4$. גם היא בחוץ.",
       say="פירוק אחר: וואי היא כל ארבע האֵיי. שוב אַיי שווה אפס, ונשאר בִּי בחזקת ארבע. גם היא בחוץ.",
       do=hide("t1-s-1") + show("t1-s-2", "o1-2")),
    Pk("ובאופן כללי: $y=a^j$ עם $j\\ge1$, ו-$i=0$ נותן $a^{n-j}b^n$, שאינה בשפה. ניצחנו כל פירוק.",
       say="ובאופן כללי: וואי שווה אֵיי גֵ'יי, עם גֵ'יי לפחות אחת, ואַיי שווה אפס נותן אֵיי בחזקת אֶן פחות גֵ'יי, בִּי אֶן, שאינה בשפה. ניצחנו כל פירוק.",
       do=hide("t1-s-2") + show("o1-g"), hold=0.5),
], stage=CSS + '<div id="t1" class="h">' + pump("t1", W1, n=N, splits=SPL1) + '</div>'
         + f'<div id="o1-1" class="kl-line h">$i=0:\\ {wtex(OUT1["1"])}\\notin L$</div>'
         + f'<div id="o1-2" class="kl-line h">$i=0:\\ {wtex(OUT1["2"])}\\notin L$</div>',
   panel=st.card("o1-g", "rule", "🔑 $|xy|\\le n$, ולכן $y=a^j$. עם $i=0$: $a^{n-j}b^n\\notin L$"))

ex2 = Scene("ex2", "דוגמה 2: מלכודות", [
    Pk("עכשיו השפה $\\#_a=\\#_b$, ושתי מילים שנראות טובות, אבל נופלות.",
       say="עכשיו השפה שבה מספר האֵיי שווה למספר הבִּי, ושתי מילים שנראות טובות, אבל נופלות."),
    Pk("מלכודת ראשונה: **אורך קבוע**. $a^{50}b^{50}$ בשפה, ונראה שהיא עובדת.",
       say="מלכודת ראשונה: אורך קבוע. אֵיי בחזקת חמישים, בִּי בחזקת חמישים, בשפה, ונראה שהיא עובדת.",
       do=show("f-1")),
    Pk("אבל את $n$ בוחר היריב. אם הוא בוחר $n=120$, המילה קצרה מ-$n$, ואסור בכלל להשתמש בה.",
       say="אבל את אֶן בוחר היריב. אם הוא בוחר אֶן שווה מאה עשרים, המילה קצרה מאֶן, ואסור בכלל להשתמש בה.",
       do=show("f-2", "tr-1")),
    Pk("לכן המילה חייבת להיות תלויה ב-$n$.", say="לכן המילה חייבת להיות תלויה באֶן."),
    Pk("מלכודת שנייה: **יחידה מאוזנת**. $(ab)^n$ בשפה, ואורכה לפחות $n$.",
       say="מלכודת שנייה: יחידה מאוזנת. אֵיי בִּי, בחזקת אֶן, בשפה, ואורכה לפחות אֶן.",
       do=hide("f-1", "f-2") + show("t2")),
    Pk("אבל היריב בוחר $y=ab$. כל ניפוח מוסיף או מוריד אותו מספר של $a$ ושל $b$, והאיזון נשמר.",
       say="אבל היריב בוחר וואי שווה אֵיי בִּי. כל ניפוח מוסיף או מוריד אותו מספר של אֵיי ושל בִּי, והאיזון נשמר.",
       do=show("t2-s-1", "tr-2")),
    Pk("פירוק אחד בטוח ליריב, והמילה פסולה. ולעומתן $a^nb^n$ כן עובדת, בדיוק כמו בדוגמה הקודמת.",
       say="פירוק אחד בטוח ליריב, והמילה פסולה. ולעומתן, אֵיי אֶן בִּי אֶן כן עובדת, בדיוק כמו בדוגמה הקודמת.",
       do=show("tr-ok"), hold=0.5),
], stage=CSS + '<div class="swap" style="--swap-h:330px">'
         + '<div id="f-1" class="h"><div class="kl-line kl-big">$w=a^{50}b^{50},\\ |w|=100$</div>'
         + '<div id="f-2" class="kl-line kl-big h">$n=120>|w|$</div></div>'
         + '<div id="t2" class="h">' + pump("t2", WAB, n=N, splits={"1": (0, 2)})
         + '<div class="kl-line">$x\\,(ab)^i\\,z:\\ \\#_a=\\#_b$</div></div>'
         + '</div>',
   panel=st.card("tr-1", "trap", "⚠️ <b>אורך קבוע</b>: היריב בוחר $n$ גדול מהמילה")
       + st.card("tr-2", "trap", "⚠️ <b>יחידה מאוזנת</b>: $y=ab$ שומר על השפה")
       + st.card("tr-ok", "rule", "🔑 $a^nb^n$: בתוך $n$ הראשונות יש רק $a$"))

exam = Scene("exam", "שאלה ממבחן", [
    Pk("ועכשיו שאלה אמיתית ממבחן: $L$ היא המילים מעל $a$, $b$, $c$ שבהן $\\#_a\\ge\\#_b$.",
       say="ועכשיו שאלה אמיתית ממבחן: אֶל היא המילים מעל אֵיי, בִּי וסִי, שבהן מספר האֵיי גדול או שווה למספר הבִּי."),
    Pk("איזו מילה מביאה בהכרח לסתירה? כל ארבע המילים בשפה, אז בודקים את פירוקי היריב."),
    Pk("$abc^{2n}$: היריב בוחר $y=ab$, יחידה מאוזנת. כל ניפוח שומר על $\\#_a=\\#_b$. נפסלת.",
       say="אֵיי בִּי, סִי בחזקת שתיים אֶן: היריב בוחר וואי שווה אֵיי בִּי, יחידה מאוזנת. כל ניפוח שומר על השוויון. נפסלת.",
       do=show("q-x-b", "q-n-b")),
    Pk("$c^na^nb^n$: $n$ האותיות הראשונות הן כולן $c$. היריב בוחר $y=c$.",
       say="סִי אֶן אֵיי אֶן בִּי אֶן: אֶן האותיות הראשונות הן כולן סִי. היריב בוחר וואי שווה סִי.",
       do=show("t3", "t3-n", "t3-s-1")),
    Pk("זו המלכודת המרכזית: $c$ היא **אות חופשית**, שהשפה לא סופרת. ניפוח שלה לא משנה כלום. נפסלת.",
       say="זו המלכודת המרכזית: סִי היא אות חופשית, שהשפה לא סופרת. ניפוח שלה לא משנה כלום. נפסלת.",
       do=show("q-x-c", "q-n-c", "xt-free")),
    Pk("$a^{2n}b^nc^{2n}$: כאן $y$ היא כמה $a$. אבל יש **רווח ביטחון**: $n$ אותיות $a$ מיותרות.",
       say="אֵיי בחזקת שתיים אֶן, בִּי אֶן, סִי בחזקת שתיים אֶן: כאן וואי היא כמה אֵיי. אבל יש רווח ביטחון: יש אֵיי מיותרות, בכמות אֶן.",
       do=hide("t3") + show("xt-mg")),
    Pk("היריב בוחר $y=a$. גם בלי ה-$a$ הזאת נשארות לפחות $n$ אותיות $a$. נפסלת.",
       say="היריב בוחר וואי שווה אֵיי. גם בלי האֵיי הזאת נשארות לפחות אֶן אותיות אֵיי. נפסלת.",
       do=show("q-x-a", "q-n-a")),
    Pk("$a^nc^nb^n$: $n$ הראשונות כולן $a$, אז $y=a^j$. עם $i=0$ יש פחות מ-$n$ אותיות $a$, ועדיין $n$ אותיות $b$.",
       say="אֵיי אֶן סִי אֶן בִּי אֶן: אֶן הראשונות כולן אֵיי, אז וואי שווה אֵיי גֵ'יי. עם אַיי שווה אפס יש פחות מאֶן אותיות אֵיי, ועדיין אֶן אותיות בִּי.",
       do=hide("xt-mg") + show("t4", "t4-n", "t4-s-1")),
    Pk("זו סתירה לכל פירוק. התשובה: $a^nc^nb^n$. המילה **צמודה**: אין ליריב שום מרווח.",
       say="זו סתירה לכל פירוק. התשובה: אֵיי אֶן סִי אֶן בִּי אֶן. המילה צמודה: אין ליריב שום מרווח.",
       do=show("q-ok-d"), hold=0.6),
], stage=CSS + '<div class="swap" style="--swap-h:420px">'
         + '<div id="t3" class="h">' + pump("t3", WX, n=N, splits={"1": (0, 1)}, cw=58)
         + st.card("xt-free", "trap", "⚠️ <b>אות חופשית</b>: $y=c$, והספירה לא משתנה") + '</div>'
         + '<div id="xt-mg" class="h"><div class="kl-line kl-big">$a^{2n-1}b^nc^{2n}\\in L$</div>'
         + st.card("xt-mgc", "trap", "⚠️ <b>רווח ביטחון</b>: מחיקת $a$ אחד לא מוציאה מהשפה").replace(' h"', '"') + '</div>'
         + '<div id="t4" class="h">' + pump("t4", WD, n=N, splits={"1": (1, 3)}, cw=58)
         + f'<div class="kl-line">$i=0:\\ {wtex(WD[:1] + WD[3:])}\\notin L$</div></div>'
         + '</div>',
   panel=opts_panel("q", Q, notes={"a": "$y=a$", "b": "$y=ab$", "c": "$y=c$"},
                    stem=r"תהי $L=\{w\in\{a,b,c\}^*\mid\#_a(w)\ge\#_b(w)\}$. יהי $n$ הקבוע מהלמה. איזו מילה תביא <b>בהכרח</b> לסתירה לתנאי למת הניפוח?"))

recap = Scene("recap", "סיכום", [
    Pk("לסיכום: היריב בוחר את $n$ ואת הפירוק. אנחנו בוחרים את המילה ואת $i$, וצריך לנצח **כל** פירוק.",
       say="לסיכום: היריב בוחר את אֶן ואת הפירוק. אנחנו בוחרים את המילה ואת אַיי, וצריך לנצח כל פירוק.",
       do=show("c1")),
    Pk("בודקים כל מילה: האם היא בשפה? האם אורכה תלוי ב-$n$? מה יש ב-$n$ האותיות הראשונות?",
       say="בודקים כל מילה: האם היא בשפה? האם אורכה תלוי באֶן? מה יש באֶן האותיות הראשונות?", do=show("c2")),
    Pk("פוסלים אות חופשית, יחידה מאוזנת, אורך קבוע, ומילה עם רווח ביטחון.", do=show("c3")),
    Pk("והמילה הנכונה היא **צמודה**: אין ליריב שום מרווח. נתראה ברמה הבאה.",
       do=show("c4"), hold=0.8),
], stage=CSS + pump("rc", W1, n=N, splits={"1": (1, 3)}).replace('kl-ruler h"', 'kl-ruler"').replace('id="rc-s-1" class="h"', 'id="rc-s-1"'),
   panel=st.card("c1", "rule", "🔑 היריב: $n$ ופירוק. אנחנו: $w$ ו-$i$")
       + st.card("c2", "rule", "🔑 בשפה? תלויה ב-$n$? מה יש ב-$n$ הראשונות?")
       + st.card("c3", "trap", "⚠️ אות חופשית, יחידה מאוזנת, אורך קבוע, רווח ביטחון")
       + st.card("c4", "plain", "המילה הנכונה <b>צמודה</b>: אין ליריב מרווח"))

VIDEO = Video("K04", "classify", "משחק למת הניפוח לשפות רגולריות",
              [title, game, ex1, ex2, exam, recap],
              bank={"26A-A-Q5": "d"})
