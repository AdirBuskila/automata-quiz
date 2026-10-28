# -*- coding: utf-8 -*-
"""N02 · Rank של שפות קטנות ומצב הבור — video script (build: tools/video/vid.py N02).

Source: tools/needhelp/nerode/N02.py (lesson + goal). Exam anchors: 25A-A-Q8 ({1,01}) and 26A-A-Q18 (unary d+2), both
cited by the lesson, neither in the quiz. Not used on purpose: the quiz's languages {0}, {01,10}, {aa,aaaaaa}, |w|<=3
and the ordering question. New worked examples: {a, ab} over {a,b} and {ε, a, aaa} over {a}.
Method shown: two prefixes are equivalent iff they have the same set of completions {z : xz ∈ L} (exact for a finite
language, checked here against lib.classes / separable).
"""
from nh import dfa_table, words, classes, rank_stable, separable, is_separating_set
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, pairs, pair_cells, cell_html, table, completions, setw, wd, buckets

fin = lambda S: (lambda w: w in S)
FR = lambda S, alpha="01": rank_stable(fin(set(S)), alpha, 9, (6, 7, 8))

# the base table (lesson)
assert rank_stable(lambda w: False, "01", 9, (6, 7, 8)) == 1 and rank_stable(lambda w: True, "01", 9, (6, 7, 8)) == 1
assert FR([""]) == 2 and separable(fin({""}), "", "0", "01") == ""

# worked example 1: L = {a, ab} over {a,b}
L1 = fin({"a", "ab"})
assert FR(["a", "ab"], "ab") == 4
CX = ["", "a", "ab", "b", "aa", "abb"]
COMP = {x: completions(L1, x, "ab") for x in CX}
assert COMP == {"": ["a", "ab"], "a": ["", "b"], "ab": [""], "b": [], "aa": [], "abb": []}
# same completions <=> equivalent (checked with the suffix search)
for x in CX:
    for y in CX:
        assert (COMP[x] == COMP[y]) == (separable(L1, x, y, "ab") is None)
D1 = dfa_table("ab", {"0": "1 3", "1": "3 2", "2": "3 3", "3": "3 3"}, "0", {"1", "2"})
assert D1.lang(8) == {"a", "ab"} and D1.n_min() == 4
T1 = ["", "a", "ab", "b"]
PC1 = pair_cells(L1, T1, "ab")
assert is_separating_set(L1, T1, "ab") and PC1 == {(1, 0): "", (2, 0): "", (2, 1): "b", (3, 0): "a", (3, 1): "", (3, 2): ""}

# worked example 2: unary {ε, a, aaa}: chain a^0..a^3 + sink = d + 2 = 5
L2 = fin({"", "a", "aaa"})
assert FR(["", "a", "aaa"], "a") == 5
U = ["", "a", "aa", "aaa", "aaaa"]
CU = {x: completions(L2, x, "a") for x in U}
assert CU == {"": ["", "a", "aaa"], "a": ["", "aa"], "aa": ["a"], "aaa": [""], "aaaa": []}
assert is_separating_set(L2, U, "a")
assert all(completions(L2, "a" * k, "a") == [] for k in range(4, 9))     # everything longer: the sink

# exam 25A-A-Q8: {1, 01}
QA = BANK["25A-A-Q8"]
L3 = fin({"1", "01"})
assert FR(["1", "01"]) == 4
OA = {o["id"]: o["value"] for o in QA["options"]}
assert OA[QA["correctId"]] == "4" and QA["correctId"] == "c"
C3 = {x: completions(L3, x, "01") for x in ["", "0", "1", "01", "00", "11"]}
assert C3 == {"": ["1", "01"], "0": ["1"], "1": [""], "01": [""], "00": [], "11": []}
assert separable(L3, "1", "01", "01") is None
D3 = dfa_table("01", {"s": "z f", "z": "t f", "f": "t t", "t": "t t"}, "s", {"f"})
assert D3.lang(8) == {"1", "01"} and D3.n_min() == 4

# exam 26A-A-Q18: Rank = d + 2 for a finite non-empty unary language with longest word a^d
QB = BANK["26A-A-Q18"]
assert QB["correctId"] == "c"
import itertools
for d in range(0, 6):
    for extra in itertools.product([0, 1], repeat=d):
        S = {"a" * i for i in range(d) if extra[i]} | {"a" * d}
        assert FR(S, "a") == d + 2

NAME1 = {"0": "q_0", "1": "q_1", "2": "q_2", "3": "q_3"}
POS1 = {"0": (130, 150), "1": (420, 150), "2": (710, 150), "3": (420, 380)}
NAME3 = {"s": "q_0", "z": "q_1", "f": "q_2", "t": "q_3"}
POS3 = {"s": (110, 110), "z": (400, 110), "f": (690, 110), "t": (400, 320)}

title = Scene("title", "", [
    N("בסרטון הזה נחשב Rank של שפות קטנות, שפה אחר שפה.", say="בסרטון הזה נחשב ראנק של שפות קטנות, שפה אחר שפה."),
    N("נלמד שיטה אחת פשוטה: לשאול **מה חסר להשלמה**. ונלמד לא לשכוח את **מצב הבור**.", hold=0.4),
], stage=CSS + '<div class="kicker">N02 · נרוד, Rank וקבוצות מפרידות</div><h1>Rank של שפות קטנות ומצב הבור</h1>'
         '<p>לחשב Rank של שפה סופית, ולא לשכוח את מצב הבור.</p>', layout="title")

base = Scene("base", "השפות הקטנות ביותר", [
    N("לכל שפה יש לפחות מחלקה אחת, כי המילה $\\varepsilon$ נמצאת באיזושהי מחלקה. לכן $\\mathrm{Rank}=0$ לא קיים.",
      say="לכל שפה יש לפחות מחלקה אחת, כי המילה אפסילון נמצאת באיזושהי מחלקה. לכן ראנק אפס לא קיים.", do=show("b-0")),
    N("בשפה הריקה, ובשפת כל המילים, כל מילה נותנת אותה תשובה לכל סיפא. מחלקה אחת: Rank אחת.",
      say="בשפה הריקה, ובשפת כל המילים, כל מילה נותנת אותה תשובה לכל סיפא. מחלקה אחת: ראנק אחת.", do=show("b-r-0")),
    N("ב-$\\{\\varepsilon\\}$ יש שתי מחלקות: $\\varepsilon$ עצמה, ו״כל השאר״.",
      say="בשפה שמכילה רק את אפסילון יש שתי מחלקות: אפסילון עצמה, וכל השאר.", do=show("b-r-1")),
    N("הסיפא הריקה מפרידה בין $\\varepsilon$, שבשפה, לכל מילה אחרת, שלא בשפה.",
      say="הסיפא הריקה מפרידה בין אפסילון, שבשפה, לכל מילה אחרת, שלא בשפה."),
    N("ו״כל השאר״ הוא כבר **מצב הבור**, או בשם השני שלו בשיעור: **מלכודת**. מילה שאין לה שום המשך בשפה.",
      do=show("b-sink"), hold=0.5),
], stage=table("b", ["השפה", "$\\mathrm{Rank}$", "המחלקות"],
               [["$\\emptyset$, $\\Sigma^*$", "$1$", "כל המילים במחלקה אחת"],
                ["$\\{\\varepsilon\\}$", "$2$", "$\\varepsilon$ / כל השאר"]]).replace('class="nr-st"', 'class="nr-st" dir="rtl"', 0),
   panel=st.card("b-0", "rule", "🔑 תמיד $\\mathrm{Rank}\\ge1$: אין $\\mathrm{Rank}=0$.")
       + st.card("b-sink", "rule", "🔑 <b>מצב הבור</b> (מלכודת): מילה שאין לה שום המשך בשפה."))

TC = table("m", ["$x$", "מה חסר להשלמה: $\\{z\\mid xz\\in L\\}$"], [[wd(x), setw(COMP[x])] for x in CX])
missing = Scene("missing", "דוגמה 1: מה חסר להשלמה?", [
    N("ניקח שפה חדשה: $L=\\{a,ab\\}$ מעל $\\{a,b\\}$.", say="ניקח שפה חדשה: אל שווה הקבוצה אֵיי, אֵיי בִּי. מעל אֵיי ובִּי."),
    N("השיטה: לכל מילה $x$ שואלים, **מה חסר להשלמה?** כלומר, אילו סיפות $z$ מכניסות את $xz$ לשפה.",
      say="השיטה: לכל מילה אקס שואלים, מה חסר להשלמה? כלומר, אילו סיפות זד מכניסות את אקס זד לשפה.", do=show("m-box")),
    N("ל-$\\varepsilon$ חסר $a$ או $ab$.", say="לאפסילון חסר אֵיי, או אֵיי בִּי.", do=show("m-r-0")),
    N("ל-$a$ חסר כלום, כי היא כבר בשפה. או $b$, כדי לקבל $ab$.", say="לאֵיי חסר כלום, כי היא כבר בשפה. או בִּי, כדי לקבל אֵיי בִּי.",
      do=show("m-r-1")),
    N("ל-$ab$ חסר רק כלום. היא בשפה, וכל המשך מוציא אותה.", say="לאֵיי בִּי חסר רק כלום. היא בשפה, וכל המשך מוציא אותה.",
      do=show("m-r-2")),
    N("ול-$b$, $aa$ ו-$abb$? שום דבר לא עוזר. הקבוצה ריקה.", say="ולבִּי, לאֵיי אֵיי, ולאֵיי בִּי בִּי? שום דבר לא עוזר. הקבוצה ריקה.",
      do=show("m-r-3", "m-r-4", "m-r-5")),
    N("והכלל: **שתי מילים שקולות אם ורק אם חסר להן אותו דבר.** כל תשובה שונה היא מחלקה.",
      do=show("m-rule")),
    N("יש כאן ארבע תשובות שונות, ולכן ארבע מחלקות: $\\mathrm{Rank}(L)=4$.", say="יש כאן ארבע תשובות שונות, ולכן ארבע מחלקות: ראנק של אל שווה ארבע.",
      do=show("m-s-0", "m-s-1", "m-s-2", "m-s-3"), hold=0.5),
], stage=f'<div id="m-box" class="h">{TC}</div>',
   panel='<div class="nr-big">$L=\\{a,ab\\}$</div>'
       + st.card("m-rule", "rule", "🔑 $x\\equiv_L y$ אם ורק אם <b>חסר להן אותו דבר</b>. כל תשובה שונה = מחלקה."))

PG1 = pairs("g1", T1, {k: cell_html(v) for k, v in PC1.items()})
sink = Scene("sink", "מצב הבור", [
    N("הנה האס״ד המינימלי של $\\{a,ab\\}$: ארבעה מצבים.", say="הנה האסאד המינימלי של הקבוצה אֵיי, אֵיי בִּי: ארבעה מצבים.", do=show("k-dfa")),
    N("$q_3$ הוא **מצב הבור**: נכנסים אליו, ולא יוצאים. כל מילה שנופלת אליו נדחית.", do=show("k-hs-3")),
    N("ושימו לב: **בשפה סופית יש תמיד בור.** תמיד יש מילה ארוכה מדי, שאין לה שום המשך בשפה.",
      do=show("k-rule")),
    N("וזו המלכודת של המבחן: מי שסופר רק את המצבים ״המעניינים״, שוכח את הבור ועונה אחד פחות.",
      do=show("k-trap")),
    N("כדי להוכיח שאי אפשר פחות מארבעה, ניקח נציג מכל מחלקה: $\\varepsilon$, $a$, $ab$, ו-$b$ בשביל הבור.",
      say="כדי להוכיח שאי אפשר פחות מארבעה, ניקח נציג מכל מחלקה: אפסילון, אֵיי, אֵיי בִּי, ובִּי בשביל הבור.",
      do=hide("k-hs-3", "k-dfa") + show("g1-box")),
    N("$a$ ו-$ab$ בשפה, והשאר לא. לכן הסיפא הריקה מפרידה כל זוג של ״בפנים״ מול ״בחוץ״.",
      say="אֵיי ואֵיי בִּי בשפה, והשאר לא. לכן הסיפא הריקה מפרידה כל זוג של בפנים מול בחוץ.",
      do=show("g1-c-1-0", "g1-c-2-0", "g1-c-3-1", "g1-c-3-2")),
    N("$ab$ מול $a$: הסיפא $b$. ו-$b$ מול $\\varepsilon$: הסיפא $a$.", say="אֵיי בִּי מול אֵיי: הסיפא בִּי. ובִּי מול אפסילון: הסיפא אֵיי.",
      do=show("g1-c-2-1", "g1-h-2-1", "g1-c-3-0", "g1-h-3-0")),
    N("כל הזוגות מופרדים: קבוצה מפרידה בגודל ארבע. והבור הוא חלק ממנה.", do=hide("g1-h-2-1", "g1-h-3-0"), hold=0.5),
], stage=f'<div id="k-dfa" class="h">{st.dfa_svg("k", D1, POS1, NAME1, w=860, h=470, scale=0.95, loops={"3": "down"})}</div>'
         f'<div id="g1-box" class="h">{PG1}</div>',
   panel=st.card("k-rule", "rule", "🔑 <b>בשפה סופית יש תמיד בור</b>: מילה שאין לה שום המשך בשפה.")
       + st.card("k-trap", "trap", "⚠️ מסיח ״קטן באחד״ = האוטומט <b>בלי</b> הבור."))

TU = table("u", ["$x$", "מה חסר"], [[wd(x) if x != "aaaa" else '<span class="nr-w">aaaa, aaaaa, …</span>', setw(CU[x])] for x in U])
unary = Scene("unary", "דוגמה 2: אות אחת", [
    N("עכשיו שפה מעל אות אחת: $L=\\{\\varepsilon,a,aaa\\}$.", say="עכשיו שפה מעל אות אחת: אל שווה הקבוצה אפסילון, אֵיי, אֵיי אֵיי אֵיי.",
      do=show("u-box")),
    N("נשאל שוב מה חסר. ל-$\\varepsilon$: כלום, $a$, או $aaa$.", say="נשאל שוב מה חסר. לאפסילון: כלום, אֵיי, או אֵיי אֵיי אֵיי.",
      do=show("u-r-0")),
    N("ל-$a$: כלום, או $aa$. ל-$aa$: רק $a$. ל-$aaa$: רק כלום.", say="לאֵיי: כלום, או אֵיי אֵיי. לאֵיי אֵיי: רק אֵיי. לאֵיי אֵיי אֵיי: רק כלום.",
      do=show("u-r-1", "u-r-2", "u-r-3")),
    N("ומ-$aaaa$ והלאה: שום דבר. זה הבור.", say="ומארבע אֵיי והלאה: שום דבר. זה הבור.", do=show("u-r-4")),
    N("חמש תשובות שונות: $\\mathrm{Rank}=5$. השרשרת $a^0$ עד $a^3$, ועוד בור.",
      say="חמש תשובות שונות: ראנק חמש. השרשרת מאֵיי בחזקת אפס עד אֵיי בחזקת שלוש, ועוד בור.", do=show("u-sum")),
    N("ובאופן כללי: אם $a^d$ היא המילה הארוכה ביותר, אז $\\mathrm{Rank}=d+2$.",
      say="ובאופן כללי: אם אֵיי בחזקת די היא המילה הארוכה ביותר, אז הראנק הוא די ועוד שתיים.", do=show("u-rule")),
    N("$d+1$ מצבים לשרשרת, מ-$a^0$ עד $a^d$, ועוד אחד לבור. כאן $d=3$, ויצא חמש.",
      say="די ועוד אחת מצבים לשרשרת, מאֵיי בחזקת אפס עד אֵיי בחזקת די, ועוד אחד לבור. כאן די שווה שלוש, ויצא חמש.", hold=0.5),
], stage=f'<div id="u-box" class="h">{TU}</div>'
         '<div id="u-sum" class="h nr-chips">'
         + "".join(f'<span class="nr-chip">$a^{k}$</span>' for k in range(4))
         + '<span class="nr-chip" style="border-color:var(--bad)">בור</span></div>',
   panel='<div class="nr-big">$L=\\{\\varepsilon,a,aaa\\}\\subseteq\\{a\\}^*$</div>'
       + st.card("u-rule", "rule", "🔑 אם $L\\subseteq\\{a\\}^*$ סופית ו-$a^d$ הארוכה, אז $\\mathrm{Rank}(L)=d+2$"))

TE = table("ec", ["$x$", "מה חסר"], [[wd(x), setw(C3[x])] for x in ["", "0", "1", "01", "00"]])
exam1 = Scene("exam1", "שאלה ממבחן", [
    N("שאלה ממבחן: כמה מצבים באס״ד המינימלי של $L=\\{1,01\\}$?", say="שאלה ממבחן: כמה מצבים באסאד המינימלי של הקבוצה אחת, אפס אחת?"),
    N("נשאל מה חסר. ל-$\\varepsilon$: $1$ או $01$. ל-$0$: רק $1$.", say="נשאל מה חסר. לאפסילון: אחת או אפס אחת. לאפס: רק אחת.",
      do=show("ec-r-0", "ec-r-1")),
    N("ועכשיו הנקודה החשובה: ל-$1$ ול-$01$ חסר **אותו דבר**: רק כלום.", say="ועכשיו הנקודה החשובה: לאחת ולאפס אחת חסר אותו דבר: רק כלום.",
      do=show("ec-r-2", "ec-r-3", "ec-s-2", "ec-s-3")),
    N("שתי מילים שונות בשפה, אבל הן שקולות. הן מגיעות לאותו מצב מקבל.", do=show("ex-hs-f")),
    N("ול-$00$ לא חסר כלום שיעזור. זה הבור.", say="ולאפס אפס לא חסר כלום שיעזור. זה הבור.", do=show("ec-r-4", "ex-hs-t")),
    N("סה״כ ארבע מחלקות: התחלה, אחרי $0$, ״בשפה״, ובור. התשובה: ארבעה מצבים.",
      say="סך הכול ארבע מחלקות: התחלה, אחרי אפס, בשפה, ובור. התשובה: ארבעה מצבים.", do=show("q-ok-c")),
    N("מלכודת ראשונה: שלוש. זה האוטומט בלי הבור.", do=show("q-x-b", "q-n-b")),
    N("מלכודת שנייה: ״לפחות חמש״, למי שנותן מצב נפרד לכל מילה בשפה. אבל $1$ ו-$01$ שקולות.",
      say="מלכודת שנייה: לפחות חמש, למי שנותן מצב נפרד לכל מילה בשפה. אבל אחת ואפס אחת שקולות.",
      do=show("q-x-d", "q-n-d", "q-x-a"), hold=0.6),
], stage=f'{TE}' + st.dfa_svg("ex", D3, POS3, NAME3, w=820, h=440, scale=0.6, loops={"t": "down"}),
   panel=f'<div class="qstem"><span class="qid">{QA["id"]}</span>{QA["questionHtml"]}</div>'
       + st.options("q", [(o["id"], o["html"]) for o in QA["options"]], notes={"b": "בלי בור", "d": "$1\\equiv01$"}))

INST = [(["", ], 0), (["aa"], 2), (["", "a", "aaa"], 3), (["aaaa"], 4)]
assert all(FR(S, "a") == d + 2 for S, d in INST)
UT = table("ut", ["$L$", "$d$", "$\\mathrm{Rank}$"],
           [["$\\{" + ",".join(w or "\\varepsilon" for w in S) + "\\}$", f"${d}$", f"${d + 2}$"] for S, d in INST], hidden=False)
exam2 = Scene("exam2", "עוד שאלה: אות אחת", [
    N("ועוד שאלה: $L\\subseteq\\{a\\}^*$ סופית ולא ריקה, ו-$a^d$ היא המילה הארוכה ביותר שלה. מהו ה-Rank?",
      say="ועוד שאלה: אל היא שפה סופית ולא ריקה מעל האות אֵיי, ואֵיי בחזקת די היא המילה הארוכה ביותר. מהו הראנק?"),
    N("זה בדיוק הכלל שראינו: שרשרת של $d+1$ מצבים, ועוד בור. $d+2$.",
      say="זה בדיוק הכלל שראינו: שרשרת של די ועוד אחת מצבים, ועוד בור. די ועוד שתיים.", do=show("p-ok-c")),
    N("ובדיקת שפיות עם $L=\\{\\varepsilon\\}$: כאן $d=0$, ו-$d+2=2$. וזה נכון, כמו שראינו בהתחלה.",
      say="ובדיקת שפיות עם השפה שמכילה רק את אפסילון: כאן די שווה אפס, ודי ועוד שתיים זה שתיים. וזה נכון, כמו שראינו בהתחלה.",
      do=show("p-chk")),
    N("$d$ שוכח גם את $\\varepsilon$ וגם את הבור. ו-$d+1$ שוכח אחד מהם.", say="די שוכח גם את אפסילון וגם את הבור. ודי ועוד אחת שוכח אחד מהם.",
      do=show("p-x-a", "p-n-a", "p-x-b", "p-n-b")),
    N("ולא משנה אילו מילים קצרות יש בשפה. בדקנו את כל השפות עד $d=5$: תמיד $d+2$.",
      say="ולא משנה אילו מילים קצרות יש בשפה. בדקנו את כל השפות עד די שווה חמש: תמיד די ועוד שתיים.",
      do=show("p-x-d"), hold=0.6),
], stage=UT + st.card("p-chk", "ex", "$L=\\{\\varepsilon\\}$: $d=0$, $\\mathrm{Rank}=2$ ✓"),
   panel=f'<div class="qstem"><span class="qid">{QB["id"]}</span>{QB["questionHtml"]}</div>'
       + st.options("p", [(o["id"], o["html"]) for o in QB["options"]], notes={"a": "בלי $\\varepsilon$ ובור", "b": "בלי בור"}))

recap = Scene("recap", "סיכום", [
    N("לסיכום: כל שפה מתחילה ב-Rank אחת לפחות. השפה הריקה וכל המילים: אחת. $\\{\\varepsilon\\}$: שתיים.",
      say="לסיכום: לכל שפה יש ראנק אחת לפחות. השפה הריקה וכל המילים: אחת. השפה של אפסילון בלבד: שתיים.", do=show("r1")),
    N("כדי לספור מחלקות שואלים מה חסר להשלמה. אותה תשובה, אותה מחלקה.", do=show("r2")),
    N("בשפה סופית תמיד יש בור, וכמעט כל מסיח ״קטן באחד״ שוכח אותו.", do=show("r3")),
    N("ומעל אות אחת: $d+2$. נתראה ברמה הבאה.", say="ומעל אות אחת: די ועוד שתיים. נתראה ברמה הבאה.", do=show("r4"), hold=0.8),
], stage=st.dfa_svg("rc", D1, POS1, NAME1, w=860, h=470, scale=0.95, loops={"3": "down"}),
   panel=st.card("r1", "rule", "🔑 $\\emptyset,\\Sigma^*$: $1$ &nbsp; $\\{\\varepsilon\\}$: $2$ &nbsp; אין $\\mathrm{Rank}=0$")
       + st.card("r2", "rule", "🔑 אותו ״מה חסר להשלמה״ = אותה מחלקה")
       + st.card("r3", "trap", "⚠️ בשפה סופית יש תמיד <b>בור</b>; ״קטן באחד״ שוכח אותו")
       + st.card("r4", "rule", "🔑 $L\\subseteq\\{a\\}^*$ סופית, $a^d$ הארוכה: $\\mathrm{Rank}=d+2$"))

VIDEO = Video("N02", "nerode", "Rank של שפות קטנות ומצב הבור",
              [title, base, missing, sink, unary, exam1, exam2, recap], bank={"25A-A-Q8": "c", "26A-A-Q18": "c"})
