# -*- coding: utf-8 -*-
"""F01 · הרצת אס״ד על מילה — video script (source of truth for the video; build: tools/video/vid.py F01).

Source: tools/needhelp/fa/F01.py (lesson + goal). Exam anchor: 24A-B-Q10 (cited by the lesson, not by the quiz).
Not used on purpose: the quiz machines D2–D5 of F01, and 19B-B-Q9 (its automaton is the quiz's D4).
Every machine below is checked against the simulator before anything is rendered.
"""
from nh import dfa_table, words
from vid import P, Scene, Video, show, hide, run_dfa, BANK
import lexicon
import stage as st

# ---------------------------------------------------------------- machines (verified)
# lesson example: contains 11
D1 = dfa_table("01", {"0": "0 1", "1": "0 2", "2": "2 2"}, "0", {"2"})
assert D1.lang(8) == {w for w in words("01", 8) if "11" in w}
# what each state remembers (scene "memory")
for w in words("01", 8):
    q = D1.run(w)
    assert (q == "2") == ("11" in w)
    assert (q == "1") == ("11" not in w and w.endswith("1"))
assert D1.run("0110") == "2" and D1.run("1010") == "0"      # the two runs the lesson shows

# new example: ends with ab
D6 = dfa_table("ab", {"0": "1 0", "1": "1 2", "2": "1 0"}, "0", {"2"})
assert D6.lang(8) == {w for w in words("ab", 8) if w.endswith("ab")}
EX2 = [("1", ""), ("2", "abba"), ("3", "aab"), ("4", "bbaa")]
assert [w for _, w in EX2 if D6.accepts(w)] == ["aab"]
assert D6.acc == {"2"} and D6.start not in D6.acc
assert [p for (p, a), r in D6.delta.items() if r in D6.acc] == ["1"] and D6.delta[("1", "b")] == "2"  # only b enters q2
assert D6.run("aba") == "1" and "ab" in "aba"                 # the trap: contains ab, rejected

# exam 24A-B-Q10 (states numbered from the left, as in the bank explanation)
E = dfa_table("01", {"1": "1 2", "2": "1 3", "3": "4 2", "4": "4 4"}, "1", {"1", "2"})
Q = BANK["24A-B-Q10"]
EXOPT = {o["id"]: o["value"] for o in Q["options"]}
assert [oid for oid, w in EXOPT.items() if E.accepts(w)] == [Q["correctId"]] == ["a"]
def trace(D, w):
    s = [D.start]
    for c in w:
        s.append(D.delta[(s[-1], c)])
    return s
assert trace(E, "111010") == list("1232121")                 # bank explanation: 1→2→3→2→1→2→1
assert trace(E, "111011")[-1] == "3" and trace(E, "111011")[:-1] == trace(E, "111010")[:-1]
assert all(E.delta[("4", a)] == "4" for a in "01") and "4" not in E.acc   # sink
assert trace(E, "0110") == list("11234") and trace(E, "11001") == list("123444")
assert E.delta[("3", "0")] == "4"

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS = {"0": (170, 190), "1": (450, 190), "2": (730, 190)}

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להריץ אס״ד על מילה, אות אחר אות."),
    P("נלמד לסנן אפשרויות לפני שמריצים, ולזהות מהי השפה של אס״ד קטן."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">F01 · אוטומטים סופיים וביטויים</div><h1>הרצת אס״ד על מילה</h1>'
         '<p>להריץ אס״ד על מילה אות אחר אות, לסנן אפשרויות לפי המצבים המקבלים, ולזהות מהי השפה של אס״ד קטן.</p>',
   layout="title")

terms = Scene("terms", "מושגים", [
    P("נתחיל במושגים. **א״ב** הוא קבוצה של אותיות, למשל $\\{0,1\\}$.", do=show("t-ab")),
    P("**מילה** היא רצף של אותיות מתוך הא״ב, למשל $0110$.", do=show("t-w", "tw-tape")),
    P("המילה הריקה, $\\varepsilon$, היא מילה בלי אותיות בכלל.", do=show("t-eps")),
    P("ו**שפה** היא קבוצה של מילים.", do=show("t-lang")),
    P("**אס״ד**, אוטומט סופי דטרמיניסטי, הוא מכונה קטנה שמחליטה על כל מילה: בשפה, או לא בשפה.",
      say="אסאד, אוטומט סופי דטרמיניסטי, הוא מכונה קטנה שמחליטה על כל מילה: בשפה, או לא בשפה.",
      do=show("t-dfa"), hold=0.4),
], stage='<div id="tw-tape" class="h">' + st.tape("tw", "0110") + '</div>'
         '<div class="hint">מילה באורך 4 מעל $\\{0,1\\}$</div>',
   panel=st.card("t-ab", "plain", "<b>א״ב</b>: קבוצת אותיות, למשל $\\{0,1\\}$")
       + st.card("t-w", "plain", "<b>מילה</b>: רצף אותיות מהא״ב, למשל $0110$")
       + st.card("t-eps", "plain", "<b>$\\varepsilon$</b>: המילה הריקה, בלי אותיות")
       + st.card("t-lang", "plain", "<b>שפה</b>: קבוצה של מילים")
       + st.card("t-dfa", "rule", "<b>אס״ד</b> מחליט על כל מילה: בשפה או לא"))

anatomy = Scene("anatomy", "מה יש באס״ד", [
    P("הנה אס״ד מעל $\\{0,1\\}$. יש בו שלושה **מצבים**: $q_0$, $q_1$ ו-$q_2$.", do=show("a-states")),
    P("$q_0$ הוא המצב ההתחלתי: החץ שנכנס מבחוץ מצביע עליו.", do=show("a-start", "an-hs-0")),
    P("$q_2$ הוא מצב **מקבל**, וזה מסומן בעיגול כפול.", do=hide("an-hs-0") + show("an-hs-2", "a-acc")),
    P("ומכל מצב יוצא **בדיוק חץ אחד לכל אות**: מ-$q_0$ יוצא חץ אחד ב-$0$, וחץ אחד ב-$1$.",
      do=hide("an-hs-2") + show("a-one", "an-hs-0", "an-he-0-0", "an-he-0-1")),
    P("את אותו מידע כותבים גם בטבלת המעברים $\\delta$.", do=hide("an-hs-0", "an-he-0-0", "an-he-0-1") + show("an-tabw")),
    P("השורה היא המצב הנוכחי, והעמודה היא האות שקראנו.", do=show("ant-row-0")),
    P("למשל, מ-$q_0$ עם האות $1$ עוברים ל-$q_1$.", do=show("ant-c-0-1", "an-he-0-1"), hold=0.5),
], stage=st.dfa_svg("an", D1, POS, N3, w=900, h=300)
         + '<div id="an-tabw" class="h">' + st.dfa_table("ant", D1, N3) + "</div>",
   panel=st.card("a-states", "plain", "<b>מצבים</b>: העיגולים")
       + st.card("a-start", "plain", "<b>מצב התחלתי אחד</b>: החץ שנכנס מבחוץ")
       + st.card("a-acc", "plain", "<b>מצבים מקבלים</b>: עיגול כפול")
       + st.card("a-one", "rule", "מכל מצב: <b>בדיוק חץ אחד לכל אות</b>"))

run1, s1, left1 = run_dfa("r1", D1, "0110", N3, tp="w1", tab="r1t",
                          lead="מתחילים, כמו תמיד, במצב ההתחלתי $q_0$.")
run2, s2, _ = run_dfa("r1", D1, "1010", N3, tp="w2", tab="r1t", fast=True, clear=left1 + ["w1-box"],
                      lead="עכשיו המילה $1010$. שוב מתחילים ב-$q_0$.")
run2[0].do += show("w2-box")
running = Scene("run", "דוגמה 1: הרצה", [
    P("נריץ את האס״ד על המילה $0110$, אות אחר אות.", do=show("w1-box")),
    *run1, *run2,
    P("זה **כלל ההרצה**: מילה מתקבלת אם **הריצה היחידה שלה** נגמרת במצב מקבל.", do=show("r-rule")),
    P('באס״ד יש ריצה אחת בלבד: אין "אולי", ואין "נתקע".', say="באסאד יש ריצה אחת בלבד: אין אולי, ואף פעם לא נתקעים.",
      hold=0.5),
], stage=st.dfa_svg("r1", D1, POS, N3, w=900, h=300)
         + '<div class="swap" style="--swap-h:260px">'
         + f'<div id="w1-box" class="h">{st.tape("w1", "0110")}{st.trace("w1", s1, N3)}{st.verdict("w1", s1[-1] in D1.acc)}</div>'
         + f'<div id="w2-box" class="h">{st.tape("w2", "1010")}{st.trace("w2", s2, N3)}{st.verdict("w2", s2[-1] in D1.acc)}</div>'
         + "</div>",
   panel=st.dfa_table("r1t", D1, N3)
       + st.card("r-rule", "rule", "🔑 <b>כלל ההרצה:</b> מילה מתקבלת אם <b>הריצה היחידה שלה</b> נגמרת במצב מקבל."))

memory = Scene("memory", "מהי השפה?", [
    P("כדי לזהות את השפה של אס״ד קטן, שואלים: מה כל מצב **זוכר** על מה שקראנו עד עכשיו?"),
    P("ב-$q_0$ עוד לא ראינו $11$, והאות האחרונה שקראנו אינה $1$.", do=show("m-0", "me-hs-0")),
    P("ב-$q_1$ עוד לא ראינו $11$, אבל האות האחרונה היא $1$.", do=hide("me-hs-0") + show("m-1", "me-hs-1")),
    P("אם עכשיו מגיע עוד $1$, עוברים ל-$q_2$: ראינו שני $1$ צמודים.",
      say="אם עכשיו מגיע עוד אחת, עוברים לקיו שתיים: ראינו שתי אחדות צמודות.",
      do=show("me-he-1-2")),
    P("ומ-$q_2$ כל אות משאירה אותנו ב-$q_2$.", do=hide("me-hs-1", "me-he-1-2") + show("m-2", "me-hs-2", "me-he-2-2")),
    P("$q_2$ הוא המקבל היחיד, ולכן השפה היא כל המילים **שמכילות** $11$.", do=show("m-lang"), hold=0.6),
], stage=st.dfa_svg("me", D1, POS, N3, w=900, h=300),
   panel=st.card("m-0", "plain", "$q_0$: עוד לא ראינו $11$, והאות האחרונה אינה $1$")
       + st.card("m-1", "plain", "$q_1$: עוד לא ראינו $11$, והאות האחרונה $1$")
       + st.card("m-2", "plain", "$q_2$: כבר ראינו $11$, ונשארים בו לתמיד")
       + st.card("m-lang", "rule", "🔑 $L$ = כל המילים <b>שמכילות</b> $11$"))

N6 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS6 = {"0": (170, 200), "1": (450, 200), "2": (730, 200)}
run3, s3, left3 = run_dfa("e2", D6, "aab", N6, tp="x1", fast=True, lead="מריצים את $aab$: מתחילים ב-$q_0$.")
run3[0].do += show("x1-box")
run3[-1].do += show("o2-ok-3")
filtering = Scene("filter", "דוגמה 2: סינון", [
    P("עכשיו אס״ד חדש, מעל $\\{a,b\\}$. השאלה: איזו מילה מתקבלת?"),
    P("לפני שמריצים משהו, מסננים. בדיקה ראשונה: האם $\\varepsilon$ באפשרויות?", do=show("o2-o-1")),
    P("$\\varepsilon$ מתקבלת **אם ורק אם המצב ההתחלתי מקבל**. כאן $q_0$ לא מקבל, אז היא נפסלת.",
      do=show("e2-hs-0", "o2-x-1", "o2-n-1")),
    P("בדיקה שנייה: לאילו מצבים מקבלים נכנסים חצים, ובאיזו אות?", do=hide("e2-hs-0")),
    P("למצב המקבל $q_2$ נכנס רק חץ אחד, באות $b$.", do=show("e2-hs-2", "e2-he-1-2")),
    P("לכן מילה מתקבלת חייבת להסתיים ב-$b$. $abba$ ו-$bbaa$ נגמרות ב-$a$: נפסלות.",
      do=show("o2-x-2", "o2-n-2", "o2-x-4", "o2-n-4")),
    P("נשארה אפשרות אחת, ורק אותה מריצים.", do=hide("e2-hs-2", "e2-he-1-2"), hold=0.3),
    *run3,
    P("שימו לב: האס״ד הזה מקבל מילים **שמסתיימות** ב-$ab$, לא מילים **שמכילות** $ab$.",
      do=hide("x1-box", *left3) + show("trap2")),
    P("למשל $aba$ מכילה $ab$, אבל ה-$a$ האחרונה מעבירה ל-$q_1$, שאינו מקבל.",
      say="למשל אֵיי בִּי אֵיי מכילה אֵיי בִּי, אבל האֵיי האחרונה מעבירה לקיו אחת, שאינו מקבל.",
      do=show("e2-hs-1"), hold=0.6),
], stage=st.dfa_svg("e2", D6, POS6, N6, w=900, h=350, bend={("2", "0"): 0.33})
         + '<div class="swap" style="--swap-h:240px">'
         + f'<div id="x1-box" class="h">{st.tape("x1", "aab")}{st.trace("x1", s3, N6)}{st.verdict("x1", True)}</div>'
         + '<div id="trap2" class="h">' + st.card("trap2c", "trap", "⚠️ <b>מסתיימת ב-</b> אינה <b>מכילה</b>: "
                                                  "$aba$ מכילה $ab$ ובכל זאת נדחית.").replace(' h"', '"') + "</div>"
         + "</div>",
   panel='<div class="qstem">איזו מילה מתקבלת?</div>'
       + st.options("o2", [(k, f"${w}$" if w else "$\\varepsilon$") for k, w in EX2],
                    notes={"1": "$q_0$ לא מקבל", "2": "נגמרת ב-$a$", "4": "נגמרת ב-$a$"}))

# exam: run on the original figure
NUM = {"1": "אחד", "2": "שתיים", "3": "שלוש", "4": "ארבע"}
RINGS = [("1", 148, 197, 56), ("2", 328, 197, 56), ("3", 512, 197, 56), ("4", 700, 197, 56)]
TAGS = [("1", 148, 250), ("2", 328, 250), ("3", 512, 250), ("4", 700, 250)]


def raster_run(word, lead, say=None, clear=()):
    s = trace(E, word)
    ph = [P(lead, say=say, do=hide(*clear) + show("xw-box", "ex-ring-1"))]
    for i, c in enumerate(word):
        do = hide(f"ex-ring-{s[i]}") + (hide(f"xw-k-{i - 1}") + show(f"xw-d-{i - 1}") if i else [])
        do += show(f"xw-k-{i}", f"ex-ring-{s[i + 1]}")
        ph.append(P(f"${c}$: מצב {s[i + 1]}", say=f"{lexicon.word_say(c)}: למצב {NUM[s[i + 1]]}.", do=do))
    return ph


opts_html = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה אמיתית ממבחן: איזו מילה מתקבלת על ידי האס״ד הזה?"),
    P("קודם מסמנים מי ההתחלתי ומי המקבלים. ההתחלתי הוא השמאלי, ויש בו עיגול כפול.", do=show("ex-ring-1")),
    P("כלומר, **המצב ההתחלתי עצמו מקבל**. גם המצב השני מקבל. השלישי והרביעי לא.", do=show("ex-ring-2")),
    P("זו המלכודת: מילה שנגמרת במצב ההתחלתי **מתקבלת**, גם אם היא חזרה אליו. מקבל לא חייב להיות בסוף האוטומט.",
      do=hide("ex-ring-2") + show("trap3")),
    P("המצב הרביעי הוא **מצב בור**: כל החצים ממנו חוזרים אליו, והוא לא מקבל.",
      do=hide("ex-ring-1", "trap3") + show("ex-ring-4")),
    P("נכנסים אליו רק מהמצב השלישי, באות $0$. מילה שנופלת לבור נדחית.",
      do=show("ex-ring-3")),
    P("$0110$: אחרי $011$ אנחנו במצב השלישי, ואז $0$ מפיל לבור.", do=show("q-x-c", "q-n-c")),
    P("$11001$: אחרי $11$ במצב השלישי, ואז $0$. גם היא בבור.", do=show("q-x-d", "q-n-d")),
    P("נשארו שתיים, ורק אותן מריצים.", do=hide("ex-ring-3", "ex-ring-4"), hold=0.3),
    *raster_run("111010", "$111010$: מתחילים במצב 1.", say="אחת אחת אחת אפס אחת אפס: מתחילים במצב אחד."),
    P("נגמרנו במצב ההתחלתי, שהוא מקבל: $111010$ מתקבלת.", do=show("q-ok-a"), hold=0.4),
    P("ו-$111011$? אותה ריצה עד האות האחרונה. אבל ה-$1$ האחרון מעביר למצב 3, שאינו מקבל.",
      say="ואחת אחת אחת אפס אחת אחת? אותה ריצה עד האות האחרונה. אבל האחת האחרונה מעבירה למצב שלוש, שאינו מקבל.",
      do=hide("ex-ring-1", "xw-box") + show("ex-ring-3", "q-x-b", "q-n-b")),
    P("התשובה: $111010$. והמלכודת השנייה: $111011$ שונה ממנה רק באות האחרונה, אז מריצים עד הסוף.",
      hold=0.6),
], stage=st.raster("ex", "images/exams/24A-B-Q10.png", 860, (763, 295), rings=RINGS, tags=TAGS)
         + '<div class="swap" style="--swap-h:230px">'
         + f'<div id="xw-box" class="h">{st.tape("xw", "111010")}</div>'
         + '<div id="trap3" class="h">' + st.card("trap3c", "trap", "⚠️ <b>מצב התחלתי מקבל:</b> מילה שחוזרת אליו מתקבלת.").replace(' h"', '"') + "</div>"
         + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>{Q["questionHtml"]}</div>'
       + st.options("q", opts_html, notes={"b": "נגמרת במצב 3", "c": "בור", "d": "בור"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מריצים אות אחר אות, ומילה מתקבלת אם הריצה נגמרת במצב מקבל.", do=show("c1")),
    P("$\\varepsilon$ מתקבלת אם ורק אם המצב ההתחלתי מקבל.", do=show("c2")),
    P("האות האחרונה היא אות של חץ שנכנס למצב מקבל, ומילה שנכנסת לבור נדחית.", do=show("c3")),
    P("ו**מסתיימת ב-** אינה **מכילה**. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=st.dfa_svg("rc", D1, POS, N3, w=900, h=300),
   panel=st.card("c1", "rule", "🔑 אות אחר אות; מתקבלת = נגמרת במצב מקבל")
       + st.card("c2", "rule", "🔑 $\\varepsilon$ מתקבלת ⇔ ההתחלתי מקבל")
       + st.card("c3", "rule", "🔑 האות האחרונה = אות של חץ שנכנס למקבל; בור = נדחית")
       + st.card("c4", "trap", "⚠️ <b>מסתיימת ב-</b> ≠ <b>מכילה</b>"))

VIDEO = Video("F01", "fa", "הרצת אס״ד על מילה",
              [title, terms, anatomy, running, memory, filtering, exam, recap],
              bank={"24A-B-Q10": "a"})
