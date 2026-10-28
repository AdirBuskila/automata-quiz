# -*- coding: utf-8 -*-
"""N01 · סיפא מפרידה ומחלקות שקילות — video script (build: tools/video/vid.py N01).

Source: tools/needhelp/nerode/N01.py (lesson + goal). Exam anchor: 21S-B-Q9 (cited by the lesson, not by the quiz).
Not used on purpose: the quiz's languages as worked examples (ends-with-00 with x=0,y=1; even number of 1s; ends with 1).
The worked example is new: L = words over {a,b} that contain aa. Every claim is checked with the simulators below.
"""
from nh import dfa_table, words, classes, rank_stable, separable, is_separating_set
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, sufftest, pairs, pair_cells, cell_html, buckets, chips, wd, ws

# ---------------------------------------------------------------- the worked language: contains aa
AA = lambda w: "aa" in w
D = dfa_table("ab", {"0": "1 0", "1": "2 0", "2": "2 2"}, "0", {"2"})
assert D.lang(8) == {w for w in words("ab", 8) if AA(w)}
assert D.n_min() == 3 and rank_stable(AA, "ab") == 3

# tester 1: x=b, y=a — suffixes tried in order, only the third separates
Z1 = ["", "b", "a"]
st1, sep1 = sufftest("t1", AA, "b", "a", Z1)
assert sep1 == [False, False, True]
assert not AA("b") and not AA("a") and not AA("bb") and not AA("ab") and not AA("ba") and AA("aa")
# tester 2: x=ε, y=b — equivalent: nothing separates (searched up to length 8), and they reach the same state
Z2 = ["", "a", "b", "aa", "ba"]
st2, sep2 = sufftest("t2", AA, "", "b", Z2)
assert not any(sep2) and separable(AA, "", "b", "ab") is None and D.run("") == D.run("b") == "0"

# ε separates every word in L from every word outside L (any language): checked on several languages
for pred in (AA, lambda w: w.endswith("b"), lambda w: len(w) % 3 == 0, lambda w: w.count("a") == w.count("b")):
    assert all(pred(x) != pred(y) for x in words("ab", 4) for y in words("ab", 4) if pred(x) and not pred(y))

# the classes of "contains aa" (prefixes up to length 4, suffixes up to length 6)
CL = classes(AA, "ab", 4, 6)
assert len(CL) == 3
GROUPS = {"0": [w for w in words("ab", 4) if D.run(w) == "0"], "1": [w for w in words("ab", 4) if D.run(w) == "1"],
          "2": [w for w in words("ab", 4) if D.run(w) == "2"]}
assert sorted(map(sorted, CL)) == sorted(map(sorted, GROUPS.values()))   # classes = states of the minimal DFA
SHOW = {"0": ["", "b", "ab", "bb", "bab"], "1": ["a", "ba", "aba", "bba"], "2": ["aa", "aab", "baa", "aaa"]}
assert all(w in GROUPS[k] for k, v in SHOW.items() for w in v)
assert all((D.run(w) == "0") == (not AA(w) and not w.endswith("a")) and (D.run(w) == "1") == (not AA(w) and w.endswith("a"))
           for w in words("ab", 8))

# separating set: one representative per class
T = ["", "a", "aa"]
assert is_separating_set(AA, T, "ab")
PC = pair_cells(AA, T, "ab")
assert PC == {(1, 0): "a", (2, 0): "", (2, 1): ""}
TB = ["", "a", "aa", "b"]
PCB = pair_cells(AA, TB, "ab")
assert PCB[(3, 0)] is None and not is_separating_set(AA, TB, "ab")
assert all(PCB[k] is not None for k in PCB if k != (3, 0))

# ---------------------------------------------------------------- exam 21S-B-Q9: Σ*(00+11)Σ*
EXL = lambda w: "00" in w or "11" in w
Q = BANK["21S-B-Q9"]
R4 = rank_stable(EXL, "01")
assert R4 == 4
E = dfa_table("01", {"s": "z o", "z": "f o", "o": "z f", "f": "f f"}, "s", {"f"})
assert E.lang(8) == {w for w in words("01", 8) if EXL(w)} and E.n_min() == 4
OPTS = {"a": ["", "1", "11"], "b": ["", "0", "1", "111"], "c": ["0", "1", "01", "10"], "d": ["", "1", "11", "111", "1111"]}
SEP = {k: is_separating_set(EXL, v, "01") for k, v in OPTS.items()}
assert SEP == {"a": True, "b": True, "c": False, "d": False}
right = [k for k, v in OPTS.items() if SEP[k] and len(v) == R4]
assert right == [Q["correctId"]] == ["b"]
assert separable(EXL, "1", "01", "01") is None and separable(EXL, "0", "10", "01") is None      # option c
assert separable(EXL, "11", "111", "01") is None                                               # option d
EXT = OPTS["b"]
PCE = pair_cells(EXL, EXT, "01")
assert PCE == {(1, 0): "0", (2, 0): "1", (2, 1): "0", (3, 0): "", (3, 1): "", (3, 2): ""}

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS = {"0": (170, 190), "1": (450, 190), "2": (730, 190)}
NE = {"s": "q_0", "z": "q_1", "o": "q_2", "f": "q_3"}
POSE = {"s": (120, 200), "z": (400, 90), "o": (400, 330), "f": (700, 200)}

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    N("נרוד הוא הנושא הכבד ביותר בקורס: שישים ושתיים שאלות בבנק. אבל הכול נשען על רעיון אחד פשוט."),
    N("בסרטון הזה נלמד מתי שתי מילים ״זהות״ עבור שפה, ואיך מוצאים סיפא שמפרידה ביניהן."),
    N("נבנה מחלקות שקילות, נכיר את ה-Rank ואת הקבוצה המפרידה, ונפתור שאלה ממבחן.", hold=0.4),
], stage=CSS + '<div class="kicker">N01 · נרוד, Rank וקבוצות מפרידות</div><h1>סיפא מפרידה ומחלקות שקילות</h1>'
         '<p>להבין מתי שתי מילים ״זהות״ עבור שפה, ולמצוא סיפא שמפרידה ביניהן.</p>', layout="title")

idea = Scene("idea", "מה האוטומט זוכר?", [
    N("נתחיל מהשאלה החשובה: **מה האוטומט חייב לזכור** על מה שקרא עד עכשיו?"),
    N("ניקח את $L$: כל המילים מעל $\\{a,b\\}$ **שמכילות** $aa$.", say="ניקח את אל: כל המילים מעל הקבוצה אֵיי ובִּי שמכילות אֵיי אֵיי.",
      do=show("i-lang")),
    N("נניח שהאוטומט כבר קרא מילה $x$, ומחכה להמשך. את ההמשך נקרא $z$, הסיפא.", do=show("i-xz")),
    N("השאלה היא אם $xz\\in L$. ואם שתי מילים שונות, $x$ ו-$y$, נותנות תשובות שונות לאותה סיפא,",
      do=show("i-q")),
    N("אז האוטומט **חייב** לזכור במה הן שונות. הן לא יכולות להגיע לאותו מצב.", do=show("i-must")),
    N("וזו בדיוק ההגדרה של **סיפא מפרידה**.", do=show("i-def")),
    N("$z$ מפרידה בין $x$ ל-$y$ אם בדיוק אחת משתי המילים $xz$ ו-$yz$ שייכת ל-$L$.",
      say="זד מפרידה בין אקס לוואי אם בדיוק אחת משתי המילים, אקס זד ווואי זד, שייכת לשפה."),
    N("ואם **אין** אף סיפא כזאת, המילים **שקולות**, וכותבים $x\\equiv_L y$.", say="ואם אין אף סיפא כזאת, המילים שקולות, וכותבים אקס שקולה לוואי.",
      do=show("i-eq"), hold=0.5),
], stage='<div id="i-lang" class="h nr-big">$L$ = המילים מעל $\\{a,b\\}$ שמכילות $aa$</div>'
         '<div id="i-xz" class="h nr-big" style="font-size:54px"><span class="nr-w"><span class="x">x</span></span>'
         '<span class="nr-sm"> &nbsp;(כבר נקרא)&nbsp; </span><span class="nr-w">z</span><span class="nr-sm"> &nbsp;(ההמשך)</span></div>'
         '<div id="i-q" class="h nr-big">$xz\\in L$ ? &nbsp; $yz\\in L$ ?</div>'
         '<div id="i-must" class="h nr-sm" style="font-size:32px">אם התשובות שונות, אז המצבים באוטומט שונים</div>',
   panel=st.card("i-def", "rule", "🔑 $z$ <b>מפרידה</b> בין $x$ ל-$y$ אם $xz\\in L$ ו-$yz\\notin L$, או להפך.")
       + st.card("i-eq", "rule", "🔑 $x\\equiv_L y$ (<b>שקולות</b>) אם ורק אם אין אף סיפא מפרידה: לכל $z$, $xz\\in L$ אם ורק אם $yz\\in L$."))

try1 = Scene("try1", "דוגמה 1: מחפשים סיפא", [
    N("נבדוק את $x=b$ ואת $y=a$. ננסה סיפות אחת אחרי השנייה, מהקצרה.", say="נבדוק את אקס שווה בִּי ואת וואי שווה אֵיי. ננסה סיפות אחת אחרי השנייה, מהקצרה.",
      do=show("t1-box")),
    N("קודם $z=\\varepsilon$: $b$ ו-$a$, ואף אחת לא מכילה $aa$. אותה תשובה, לא מפרידה.",
      say="קודם זד שווה אפסילון: בִּי ואֵיי, ואף אחת לא מכילה אֵיי אֵיי. אותה תשובה, לא מפרידה.", do=show("t1-r-0")),
    N("$z=b$: $bb$ ו-$ab$. שוב שתיהן בחוץ. לא מפרידה.", say="זד שווה בִּי: בִּי בִּי ואֵיי בִּי. שוב שתיהן בחוץ. לא מפרידה.",
      do=show("t1-r-1")),
    N("$z=a$: $ba$ בחוץ, אבל $aa$ בפנים! מצאנו סיפא מפרידה.", say="זד שווה אֵיי: בִּי אֵיי בחוץ, אבל אֵיי אֵיי בפנים! מצאנו סיפא מפרידה.",
      do=show("t1-r-2", "t1-s-2", "t1-t-2")),
    N("ולמה זה הגיוני? אחרי $a$ האוטומט כבר ״באמצע״ $aa$, ואחרי $b$ הוא מתחיל מאפס.",
      say="ולמה זה הגיוני? אחרי אֵיי האוטומט כבר באמצע אֵיי אֵיי, ואחרי בִּי הוא מתחיל מאפס.",
      do=show("p1-hs-1", "p1-hs-0")),
    N("מספיקה סיפא **אחת** כדי לקבוע שהמילים נבדלות. לא צריך לבדוק את כל השאר.", do=show("t1-c1")),
    N("עכשיו $x=\\varepsilon$ ו-$y=b$. ננסה כמה סיפות.", say="עכשיו אקס שווה אפסילון ווואי שווה בִּי. ננסה כמה סיפות.",
      do=hide("t1-box", "p1-hs-1", "p1-hs-0") + show("t2-box", "t2-r-0", "t2-r-1")),
    N("$aa$ ו-$baa$, שתיהן בפנים. $ba$ ו-$bba$, שתיהן בחוץ. תמיד אותה תשובה.",
      say="אֵיי אֵיי ובִּי אֵיי אֵיי, שתיהן בפנים. בִּי אֵיי ובִּי בִּי אֵיי, שתיהן בחוץ. תמיד אותה תשובה.",
      do=show("t2-r-2", "t2-r-3", "t2-r-4")),
    N("וזה לא מקרה: $b$ לא מתחילה שום $aa$, אז אחרי $\\varepsilon$ ואחרי $b$ האוטומט באותו מצב.",
      say="וזה לא מקרה: בִּי לא מתחילה שום אֵיי אֵיי, אז אחרי אפסילון ואחרי בִּי האוטומט באותו מצב.", do=show("p1-hs-0")),
    N("לכן $\\varepsilon\\equiv_L b$: אין אף סיפא מפרידה. בדקנו את כל הסיפות עד אורך שמונה.",
      say="לכן אפסילון שקולה לבִּי: אין אף סיפא מפרידה. בדקנו את כל הסיפות עד אורך שמונה.", do=show("t2-c2"), hold=0.5),
], stage=st.dfa_svg("p1", D, POS, N3, w=900, h=300, scale=0.85)
         + '<div class="swap" style="--swap-h:330px">'
         + f'<div id="t1-box" class="h">{st1}</div>'
         + f'<div id="t2-box" class="h">{st2}</div></div>',
   panel='<div class="nr-sm" style="text-align:right">$L$: מכילה $aa$</div>'
       + st.card("t1-c1", "ex", "$z=a$ מפרידה בין $b$ ל-$a$: $ba\\notin L$, $aa\\in L$.")
       + st.card("t2-c2", "ex", "$\\varepsilon\\equiv_L b$: כל סיפא נותנת לשתיהן אותה תשובה."))

eps = Scene("eps", "הסיפא הריקה", [
    N("עכשיו כלל קצר שחוסך הרבה עבודה במבחן."),
    N("נניח ש-$x\\in L$ ו-$y\\notin L$. נבחר את הסיפא הריקה, $z=\\varepsilon$.", do=show("e-1")),
    N("אז $xz$ היא פשוט $x$, שבשפה, ו-$yz$ היא $y$, שלא בשפה. כלומר, היא מפרידה.",
      say="אז אקס זד היא פשוט אקס, שבשפה, ווואי זד היא וואי, שלא בשפה. כלומר, היא מפרידה.", do=show("e-2")),
    N("למשל $aa$ ו-$a$: $aa\\in L$ ו-$a\\notin L$, ו-$\\varepsilon$ מפרידה ביניהן.",
      say="למשל אֵיי אֵיי ואֵיי: אֵיי אֵיי בשפה ואֵיי לא בשפה, ואפסילון מפרידה ביניהן.", do=show("e-3")),
    N("**$z=\\varepsilon$ מפרידה כל מילה ב-$L$ מכל מילה מחוץ ל-$L$**, לכל שפה, גם לא רגולרית.",
      say="זד שווה אפסילון מפרידה כל מילה בשפה מכל מילה מחוץ לשפה, לכל שפה, גם לא רגולרית.", do=show("e-rule")),
    N("לכן הטענה ״מילה בשפה ומילה מחוץ לה לא ניתנות להפרדה״ היא **תמיד שגויה**.", do=show("e-trap"), hold=0.5),
], stage='<div id="e-1" class="h nr-big">$x\\in L$, &nbsp; $y\\notin L$, &nbsp; $z=\\varepsilon$</div>'
         '<div id="e-2" class="h nr-big">$x\\varepsilon=x\\in L$ &nbsp; אבל &nbsp; $y\\varepsilon=y\\notin L$</div>'
         '<div id="e-3" class="h nr-big">$aa\\in L$, $a\\notin L$: לכן $z=\\varepsilon$ מפרידה</div>',
   panel=st.card("e-rule", "rule", "🔑 <b>$z=\\varepsilon$ מפרידה כל מילה ב-$L$ מכל מילה מחוץ ל-$L$.</b>")
       + st.card("e-trap", "trap", "⚠️ ״אם $x\\in L$ ו-$y\\notin L$, אז הן לא ניתנות להפרדה״ היא <b>תמיד</b> טענה שגויה."))

cls = Scene("classes", "מחלקות שקילות ו-Rank", [
    N("שקילות מחלקת את כל המילים לקבוצות: **מחלקות שקילות**. בכל מחלקה, כל שתי מילים שקולות.",
      do=show("c")),
    N("נמיין מילים של השפה שלנו. מחלקה ראשונה: אין $aa$, והאות האחרונה אינה $a$.",
      say="נמיין מילים של השפה שלנו. מחלקה ראשונה: אין אֵיי אֵיי, והאות האחרונה אינה אֵיי.",
      do=show("c-b-0", *[f"c-w-0-{n}" for n in range(len(SHOW['0']))], "q1-hs-0")),
    N("שנייה: אין $aa$, אבל נגמרת ב-$a$. כאן חסרה רק עוד $a$ אחת.",
      say="שנייה: אין אֵיי אֵיי, אבל נגמרת באֵיי. כאן חסרה רק עוד אֵיי אחת.",
      do=hide("q1-hs-0") + show("c-b-1", *[f"c-w-1-{n}" for n in range(len(SHOW['1']))], "q1-hs-1")),
    N("ושלישית: כבר יש $aa$. מכאן כל המשך נשאר בשפה.", say="ושלישית: כבר יש אֵיי אֵיי. מכאן כל המשך נשאר בשפה.",
      do=hide("q1-hs-1") + show("c-b-2", *[f"c-w-2-{n}" for n in range(len(SHOW['2']))], "q1-hs-2")),
    N("מילים מאותה מחלקה מגיעות לאותו מצב באוטומט **המינימלי**. שלוש מחלקות, שלושה מצבים.", do=hide("q1-hs-2")),
    N("מספר המחלקות נקרא $\\mathrm{Rank}(L)$. כאן $\\mathrm{Rank}(L)=3$.", say="מספר המחלקות נקרא ראנק של אל. כאן ראנק של אל שווה שלוש.",
      do=show("c-rank")),
    N("ו**משפט נרוד** אומר: $L$ רגולרית אם ורק אם $\\mathrm{Rank}(L)$ סופי.",
      say="ומשפט נרוד אומר: אל רגולרית אם ורק אם הראנק של אל סופי.", do=show("c-thm")),
    N("ואז באס״ד **המינימלי** של $L$ יש בדיוק $\\mathrm{Rank}(L)$ מצבים. כל מחלקה היא מצב שהאוטומט חייב להבחין בו.",
      say="ואז באסאד המינימלי של אל יש בדיוק ראנק של אל מצבים. כל מחלקה היא מצב שהאוטומט חייב להבחין בו.",
      do=show("c-min"), hold=0.5),
], stage=st.dfa_svg("q1", D, POS, N3, w=900, h=300)
         + buckets("c", [("$q_0$: אין $aa$, לא נגמרת ב-$a$", SHOW["0"], False),
                         ("$q_1$: אין $aa$, נגמרת ב-$a$", SHOW["1"], False),
                         ("$q_2$: יש $aa$", SHOW["2"], True)]).replace('class="nr-bk"', 'class="nr-bk h"', 1),
   panel=st.card("c-rank", "rule", "🔑 $\\mathrm{Rank}(L)$ = מספר מחלקות השקילות")
       + st.card("c-thm", "rule", "🔑 <b>נרוד:</b> $L$ רגולרית אם ורק אם $\\mathrm{Rank}(L)$ סופי")
       + st.card("c-min", "rule", "🔑 באס״ד המינימלי יש בדיוק $\\mathrm{Rank}(L)$ מצבים"))

PG = pairs("g1", T, {k: cell_html(v) for k, v in PC.items()})
PGB = pairs("g2", TB, {k: cell_html(v) for k, v in PCB.items()})
sepset = Scene("sepset", "קבוצה מפרידה", [
    N("קבוצה $T$ היא **מפרידה** אם **כל שתי מילים שונות** בה ניתנות להפרדה.", do=show("s-def")),
    N("איך בונים אחת? לוקחים נציג אחד מכל מחלקה, למשל את המילה הקצרה ביותר בכל מחלקה.",
      do=show("g1-box")),
    N("$T=\\{\\varepsilon,a,aa\\}$. נמלא טבלת זוגות: לכל זוג, הסיפא שמפרידה אותו.",
      say="טי שווה הקבוצה אפסילון, אֵיי, אֵיי אֵיי. נמלא טבלת זוגות: לכל זוג, הסיפא שמפרידה אותו."),
    N("$a$ מול $\\varepsilon$: הסיפא $a$. כי $aa\\in L$, אבל $a\\notin L$.",
      say="אֵיי מול אפסילון: הסיפא אֵיי. כי אֵיי אֵיי בשפה, אבל אֵיי לא בשפה.", do=show("g1-c-1-0", "g1-h-1-0")),
    N("$aa$ מול $\\varepsilon$: הסיפא הריקה. $aa$ בשפה, $\\varepsilon$ לא.",
      say="אֵיי אֵיי מול אפסילון: הסיפא הריקה. אֵיי אֵיי בשפה, אפסילון לא.", do=hide("g1-h-1-0") + show("g1-c-2-0", "g1-h-2-0")),
    N("$aa$ מול $a$: שוב הסיפא הריקה. כל הזוגות מופרדים, אז $T$ מפרידה.",
      say="אֵיי אֵיי מול אֵיי: שוב הסיפא הריקה. כל הזוגות מופרדים, אז טי מפרידה.",
      do=hide("g1-h-2-0") + show("g1-c-2-1", "g1-h-2-1", "s-ok")),
    N("ועכשיו נוסיף ל-$T$ את $b$. נקבל ארבע מילים, ונבדוק שוב.", say="ועכשיו נוסיף לטי את בִּי. נקבל ארבע מילים, ונבדוק שוב.",
      do=hide("g1-box", "g1-h-2-1") + show("g2-box", *[f"g2-c-{i}-{j}" for (i, j) in PCB if (i, j) != (3, 0)])),
    N("אבל $b$ מול $\\varepsilon$: ראינו שהן שקולות. אין סיפא מפרידה.",
      say="אבל בִּי מול אפסילון: ראינו שהן שקולות. אין סיפא מפרידה.", do=show("g2-c-3-0", "g2-h-3-0")),
    N("זוג שקול אחד מספיק: $\\{\\varepsilon,a,aa,b\\}$ **אינה** מפרידה. שתי מילים מאותה מחלקה פוסלות את הקבוצה.",
      say="זוג שקול אחד מספיק: הקבוצה הזו אינה מפרידה. שתי מילים מאותה מחלקה פוסלות את הקבוצה.", do=show("s-trap")),
    N("ולכן אם $T$ מפרידה, $|T|\\le\\mathrm{Rank}(L)$. וה-Rank הוא בדיוק גודל הקבוצה המפרידה **הגדולה ביותר**.",
      say="ולכן אם טי מפרידה, הגודל של טי קטן או שווה לראנק. והראנק הוא בדיוק גודל הקבוצה המפרידה הגדולה ביותר.",
      do=show("s-max"), hold=0.5),
], stage=f'<div class="swap" style="--swap-h:420px"><div id="g1-box" class="h">{PG}'
         f'<div id="s-ok" class="h verdict ok">$T$ מפרידה ✓</div></div>'
         f'<div id="g2-box" class="h">{PGB}<div class="nr-sm">≡ = אין סיפא מפרידה</div></div></div>',
   panel=st.card("s-def", "rule", "🔑 $T$ <b>מפרידה</b>: כל שתי מילים שונות ב-$T$ ניתנות להפרדה.")
       + st.card("s-trap", "trap", "⚠️ אם יש ב-$T$ שתי מילים מאותה מחלקה, אז $T$ <b>לא</b> מפרידה.")
       + st.card("s-max", "rule", "🔑 אם $T$ מפרידה, אז $|T|\\le\\mathrm{Rank}(L)$. ה-Rank = גודל המפרידה הגדולה ביותר."))

# exam
OPT_HTML = [(k, "$T=\\{" + ",".join(w or "\\varepsilon" for w in v) + "\\}$") for k, v in OPTS.items()]
PGE = pairs("g3", EXT, {k: cell_html(v) for k, v in PCE.items()})
exam = Scene("exam", "שאלה ממבחן", [
    N("ועכשיו שאלה ממבחן. $L$ היא המילים הבינאריות שמכילות $00$ או $11$.",
      say="ועכשיו שאלה ממבחן. אל היא המילים הבינאריות שמכילות אפס אפס או אחת אחת."),
    N("איזו קבוצה היא מפרידה, **ואין** קבוצה מפרידה גדולה ממנה? כלומר, הגודל שלה הוא בדיוק ה-Rank.",
      say="איזו קבוצה היא מפרידה, ואין קבוצה מפרידה גדולה ממנה? כלומר, הגודל שלה הוא בדיוק הראנק."),
    N("קודם ה-Rank. מה צריך לזכור? התחלה, האות האחרונה $0$, האות האחרונה $1$, או ״כבר מצאנו״.",
      say="קודם הראנק. מה צריך לזכור? התחלה, האות האחרונה אפס, האות האחרונה אחת, או שכבר מצאנו.", do=show("x-dfa")),
    N("זה אס״ד עם ארבעה מצבים, ולכן כל קבוצה מפרידה מכילה לכל היותר ארבע מילים.", do=show("x-r4")),
    N("הקבוצה עם חמש מילים נפסלת מיד: יש בה יותר מילים מה-Rank. ובאמת, $11$ ו-$111$ שתיהן ״כבר מצאנו״.",
      say="הקבוצה עם חמש מילים נפסלת מיד: יש בה יותר מילים מהראנק. ובאמת, אחת אחת ואחת אחת אחת שתיהן כבר מצאנו.",
      do=show("q-x-d", "q-n-d")),
    N("ב-$\\{0,1,01,10\\}$: $1$ ו-$01$ שתיהן נגמרות ב-$1$, ועוד אין בהן $00$ או $11$. הן שקולות, אז היא לא מפרידה.",
      say="בקבוצה אפס, אחת, אפס אחת, אחת אפס: אחת ואפס אחת שתיהן נגמרות באחת, ועוד אין בהן אפס אפס או אחת אחת. הן שקולות, אז היא לא מפרידה.",
      do=show("q-x-c", "q-n-c")),
    N("ועכשיו המלכודת: $\\{\\varepsilon,1,11\\}$ **כן** מפרידה. אבל יש בה רק שלוש מילים.",
      say="ועכשיו המלכודת: הקבוצה אפסילון, אחת, אחת אחת, כן מפרידה. אבל יש בה רק שלוש מילים.",
      do=show("x-trap")),
    N("ובעוד רגע נראה קבוצה מפרידה בגודל ארבע, אז $\\{\\varepsilon,1,11\\}$ אינה הגדולה ביותר. ״מפרידה״ לבד לא מספיק.",
      say="ובעוד רגע נראה קבוצה מפרידה בגודל ארבע, אז אפסילון, אחת, אחת אחת, אינה הגדולה ביותר. מפרידה לבד לא מספיק.", do=show("q-x-a", "q-n-a")),
    N("נשארה $\\{\\varepsilon,0,1,111\\}$. נוודא בטבלת זוגות.", say="נשארה הקבוצה אפסילון, אפס, אחת, אחת אחת אחת. נוודא בטבלת זוגות.",
      do=hide("x-dfa", "x-r4", "x-trap") + show("x-pg")),
    N("$0$ מול $\\varepsilon$: הסיפא $0$. $00$ בשפה, $0$ לא.", say="אפס מול אפסילון: הסיפא אפס. אפס אפס בשפה, אפס לא.",
      do=show("g3-c-1-0", "g3-h-1-0")),
    N("$1$ מול $\\varepsilon$: הסיפא $1$. ו-$1$ מול $0$: הסיפא $0$, כי $00$ בשפה ו-$10$ לא.",
      say="אחת מול אפסילון: הסיפא אחת. ואחת מול אפס: הסיפא אפס, כי אפס אפס בשפה ואחת אפס לא.",
      do=hide("g3-h-1-0") + show("g3-c-2-0", "g3-c-2-1", "g3-h-2-1")),
    N("ו-$111$ בשפה, ושלוש האחרות לא: הסיפא הריקה מפרידה אותה מכולן.",
      say="ואחת אחת אחת בשפה, ושלוש האחרות לא: הסיפא הריקה מפרידה אותה מכולן.",
      do=hide("g3-h-2-1") + show("g3-c-3-0", "g3-c-3-1", "g3-c-3-2")),
    N("ארבע מילים, כולן מופרדות, וה-Rank ארבע. זו התשובה.", say="ארבע מילים, כולן מופרדות, והראנק ארבע. זו התשובה.",
      do=show("q-ok-b"), hold=0.6),
], stage='<div class="swap" style="--swap-h:600px">'
         '<div id="x-dfa" class="h">' + st.dfa_svg("xe", E, POSE, NE, w=820, h=420, scale=1.0)
         + '<div id="x-r4" class="h nr-big">יש אס״ד עם $4$ מצבים, לכן $|T|\\le4$</div>'
         + st.card("x-trap", "trap", "⚠️ <b>מפרידה</b> אינה <b>הכי גדולה</b>: $\\{\\varepsilon,1,11\\}$ מפרידה, אבל $3<4$.") + '</div>'
         + f'<div id="x-pg" class="h">{PGE}</div></div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>$L=\\Sigma^*(00+11)\\Sigma^*$. איזו $T$ מפרידה '
         f'<b>ואין</b> מפרידה גדולה יותר?</div>'
       + st.options("q", OPT_HTML, notes={"a": "רק $3$", "c": "$1\\equiv01$", "d": "$5>4$"}))

recap = Scene("recap", "סיכום", [
    N("לסיכום: $z$ מפרידה בין $x$ ל-$y$ אם בדיוק אחת מ-$xz$ ו-$yz$ בשפה. אין כזאת? הן שקולות.",
      say="לסיכום: זד מפרידה בין אקס לוואי אם בדיוק אחת מאקס זד ווואי זד בשפה. אין כזאת? הן שקולות.", do=show("r1")),
    N("הסיפא הריקה מפרידה כל מילה בשפה מכל מילה מחוצה לה.", do=show("r2")),
    N("ה-Rank הוא מספר המחלקות, והוא גודל האס״ד המינימלי.", say="הראנק הוא מספר המחלקות, והוא גודל האסאד המינימלי.", do=show("r3")),
    N("וקבוצה מפרידה לוקחת נציג אחד מכל מחלקה. שתי מילים מאותה מחלקה פוסלות אותה. נתראה ברמה הבאה.",
      do=show("r4"), hold=0.8),
], stage=st.dfa_svg("rc", D, POS, N3, w=900, h=300),
   panel=st.card("r1", "rule", "🔑 $z$ מפרידה: בדיוק אחת מ-$xz,yz$ ב-$L$; אין כזאת: $x\\equiv_L y$")
       + st.card("r2", "rule", "🔑 $z=\\varepsilon$ מפרידה כל מילה ב-$L$ מכל מילה מחוץ ל-$L$")
       + st.card("r3", "rule", "🔑 $\\mathrm{Rank}(L)$ = מספר המחלקות = גודל האס״ד המינימלי")
       + st.card("r4", "trap", "⚠️ קבוצה מפרידה: נציג אחד מכל מחלקה; שתיים מאותה מחלקה פוסלות"))

VIDEO = Video("N01", "nerode", "סיפא מפרידה ומחלקות שקילות",
              [title, idea, try1, eps, cls, sepset, exam, recap], bank={"21S-B-Q9": "b"})
