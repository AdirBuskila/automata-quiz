# -*- coding: utf-8 -*-
"""K03 · להוכיח שפה לא רגולרית — video script (build: tools/video/vid.py K03).

Source: tools/needhelp/classify/K03.py (lesson + goal). Exam anchor: 24A-B-Q13 (cited by the lesson; trap: the listed
pieces a^{2k}, b^{2k} look regular, but the mixed part a^{2k}b^{2k} is exposed by intersecting with aa*bb*).
Worked examples are new languages: {a^n b^{2n}} (infinite separating set, plus a non-separating infinite set) and
{#a = #b + #c} over {a,b,c} (intersection with a*b*, plus the useless R = (ab)*).
Not used on purpose: the quiz languages of K03 (0^i1^j with i≠j, #a=#b with four R's, n−m≤2 …, unary, mod/eq).
"""
import re

from nh import (classify_cert, words, rank_growing, sep_infinite, separable, same_pred, rx, CFG)
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_classify import CSS, Pk, grid, opts_panel

CLS = {"finite": "a", "reg": "b", "cfl": "c", "noncfl": "d"}


def blocks(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# ---------------------------------------------------------------- example 1: separating set for {a^n b^{2n}}
L1 = lambda w: (lambda t: t is not None and t[1] == 2 * t[0])(blocks(w, "ab"))
assert classify_cert(L1, "ab", ("cfl", "S->aSbb|ε")) == "cfl"
ZS = ["b" * (2 * j) for j in range(12)]
assert sep_infinite(L1, lambda k: "a" * k, ZS, n=10)                 # {a^k}: every pair separated by some b^{2j}
for i in range(10):
    for j in range(10):
        if i != j:                                                    # the suffix b^{2i} separates a^i from a^j
            assert L1("a" * i + "b" * (2 * i)) and not L1("a" * j + "b" * (2 * i))
ROWS = [(str(i), f"$a^{i}$") for i in range(4)]
COLS = [(str(j), f"$b^{{{2 * j}}}$" if j else "$\\varepsilon$") for j in range(4)]
OK1 = {(str(i), str(j)): L1("a" * i + "b" * (2 * j)) for i in range(4) for j in range(4)}
assert [k for k, v in OK1.items() if v] == [(str(i), str(i)) for i in range(4)]          # exactly the diagonal
# trap: {a^k b^{2k}} is infinite but NOT separating: all in L, every non-empty suffix throws all out
T2 = ["a" * k + "b" * (2 * k) for k in range(1, 6)]
assert all(separable(L1, x, y, "ab", 7) is None for i, x in enumerate(T2) for y in T2[i + 1:])

# ---------------------------------------------------------------- example 2: intersection with a regular language
L2 = lambda w: w.count("a") == w.count("b") + w.count("c")
assert rank_growing(L2, "abc")
ANBN = lambda w: (lambda t: t is not None and t[0] == t[1])(blocks(w, "ab"))
R1, R2 = rx("a*b*", "abc"), rx("(ab)*", "abc")
assert same_pred(lambda w: L2(w) and R1.accepts(w), ANBN, "abc", 7)              # L ∩ a*b* = {a^n b^n}
assert rank_growing(ANBN, "ab")
assert same_pred(lambda w: L2(w) and R2.accepts(w), R2.accepts, "abc", 7)        # L ∩ (ab)* = (ab)*: regular

# ---------------------------------------------------------------- exam 24A-B-Q13
def ex(w):
    return any(w in ("a" * (2 * k), "b" * (2 * k), "a" * (2 * k) + "b" * (2 * k)) for k in range(len(w) // 2 + 1))
LIST = ["", "aa", "bb", "aabb", "aaaa", "bbbb", "aaaabbbb", "aaaaaa", "bbbbbb", "aaaaaabbbbbb"]
FULL = {c * (2 * k) for c in "ab" for k in range(7)} | {"a" * (2 * k) + "b" * (2 * k) for k in range(4)}
assert {w for w in words("ab", 12) if ex(w)} == FULL and set(LIST) <= FULL      # the question's list, to length 12
Q = BANK["24A-B-Q13"]
assert CLS[classify_cert(ex, "ab", ("cfl", "S->A|M|B;A->aaA|ε;B->bbB|ε;M->aaMbb|ε"))] == Q["correctId"] == "c"
RX = rx("aa*bb*", "ab")
MID = lambda w: (lambda t: t is not None and t[0] == t[1] and t[0] >= 2 and t[0] % 2 == 0)(blocks(w, "ab"))
assert same_pred(lambda w: ex(w) and RX.accepts(w), MID, "ab", 12)                 # L ∩ aa*bb* = {a^{2k}b^{2k}, k≥1}
assert rank_growing(lambda w: ex(w) and RX.accepts(w), "ab")
assert sep_infinite(MID, lambda k: "a" * (2 * k + 2), ["b" * (2 * j) for j in range(14)], n=6)
assert all(rx(r, "ab").dfa().is_infinite() for r in ("(aa)*", "(bb)*"))           # the tempting regular pieces

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    Pk("בסרטון הזה נלמד להוכיח ששפה **לא** רגולרית."),
    Pk("נראה שתי דרכים: קבוצה מפרידה אינסופית, וחיתוך עם שפה רגולרית."),
    Pk("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K03 · סיווג שפות</div><h1>להוכיח שפה לא רגולרית</h1>'
         '<p>להוכיח אי-רגולריות בעזרת קבוצה מפרידה אינסופית או חיתוך עם שפה רגולרית, ולהבדיל בין ספירה מודולו לספירה אמיתית.</p>',
   layout="title")

ideas = Scene("ideas", "שתי דרכים", [
    Pk("לא מצאתם ביטוי ולא אס״ד? כנראה השפה לא רגולרית. עכשיו צריך להוכיח את זה."),
    Pk("נזכיר: סיפא $z$ **מפרידה** בין $x$ ל-$y$ אם בדיוק אחת מ-$xz$ ו-$yz$ בשפה.",
       say="נזכיר: סיפא זד מפרידה בין אקס לוואי, אם בדיוק אחת מהמילים אקס זד, וואי זד, בשפה.",
       do=show("i-sep")),
    Pk("דרך א׳: קבוצה **אינסופית** שכל שתי מילים בה ניתנות להפרדה.", say="דרך אָלֶף: קבוצה אינסופית, שכל שתי מילים בה ניתנות להפרדה.",
       do=show("i-a")),
    Pk("אז יש ל-$L$ אינסוף מחלקות שקילות, ואס״ד עם מספר סופי של מצבים לא יכול לזהות אותה.", do=show("i-a2")),
    Pk("דרך ב׳: רגולריות סגורות לחיתוך. אם $L$ רגולרית, גם $L\\cap R$ רגולרית לכל $R$ רגולרית.",
       say="דרך בֵּית: רגולריות סגורות לחיתוך. אם אֶל רגולרית, גם אֶל חיתוך אַר רגולרית, לכל אַר רגולרית.",
       do=show("i-b")),
    Pk("לכן אם מצאנו $R$ רגולרית שהחיתוך איתה **לא** רגולרי, אז $L$ לא רגולרית.", do=show("i-b2"), hold=0.5),
], stage=CSS + '<div id="i-sep" class="kl-line kl-big h">$xz\\in L,\\ yz\\notin L$</div>'
         + '<div id="i-a2" class="kl-line h">אם $|T|=\\infty$, אז $\\mathrm{Rank}(L)=\\infty$</div>'
         + '<div id="i-b2" class="kl-line kl-big h">אם $L\\cap R$ לא רגולרית, אז $L$ לא רגולרית</div>',
   panel=st.card("i-a", "rule", "🔑 <b>דרך א׳</b>: אם יש קבוצה מפרידה <b>אינסופית</b>, אז יש אינסוף מחלקות, ולכן לא רגולרית")
       + st.card("i-b", "rule", "🔑 <b>דרך ב׳</b>: אם $R$ רגולרית ו-$L\\cap R$ לא רגולרית, אז $L$ לא רגולרית"))

sep = Scene("sep", "דוגמה 1: קבוצה מפרידה", [
    Pk("נוכיח ש-$\\{a^nb^{2n}\\}$ לא רגולרית: על כל $a$ באות בדיוק שתי $b$.",
       say="נוכיח שהשפה אֵיי אֶן, בִּי בחזקת שתיים אֶן, לא רגולרית: על כל אֵיי באות בדיוק שתי בִּי."),
    Pk("ניקח את הקבוצה $T=\\{a^k\\}$: $\\varepsilon$, $a$, $aa$, $aaa$, וכן הלאה. היא אינסופית.",
       say="ניקח את הקבוצה טִי, של כל המילים אֵיי קֵיי: אפסילון, אֵיי, אֵיי אֵיי, וכן הלאה. היא אינסופית.",
       do=show("sg", "sg-r-0", "sg-r-1", "sg-r-2", "sg-r-3")),
    Pk("הסיפא **המשלימה** של $a^i$ היא $b^{2i}$: היא משלימה אותה בדיוק למילה בשפה.",
       say="הסיפא המשלימה של אֵיי אַיי, היא בִּי בחזקת שתיים אַיי: היא משלימה אותה בדיוק למילה בשפה.",
       do=hide("sg-r-1", "sg-r-2", "sg-r-3") + show(*[f"sg-c-{i}-{i}" for i in range(4)])),
    Pk("אבל אותה סיפא אחרי $a^j$ אחרת נותנת מספר לא נכון של $b$: מחוץ לשפה.",
       say="אבל אותה סיפא, אחרי אֵיי גֵ'יי אחרת, נותנת מספר לא נכון של בִּי: מחוץ לשפה.",
       do=hide("sg-r-0") + show(*[f"sg-c-{i}-{j}" for i in range(4) for j in range(4) if i != j])),
    Pk("כלומר כל שתי שורות נבדלות בעמודה כלשהי: כל זוג מופרד. הקבוצה אינסופית ומפרידה.", do=show("sp-ok")),
    Pk("לכן ל-$L$ אינסוף מחלקות, והיא לא רגולרית.", hold=0.4),
    Pk("ועכשיו המלכודת: הקבוצה $\\{a^kb^{2k}\\mid k\\ge1\\}$ גם אינסופית, וכל המילים בה בשפה.",
       say="ועכשיו המלכודת: הקבוצה של כל המילים אֵיי קֵיי בִּי בחזקת שתיים קֵיי, עם קֵיי לפחות אחת, גם היא אינסופית, וכל המילים בה בשפה.",
       do=show("sp-trap")),
    Pk("אבל היא לא מפרידה: הסיפא הריקה משאירה את כולן בשפה, וכל סיפא אחרת מוציאה את כולן.",
       do=show("sp-trap2")),
    Pk("מילה בקבוצה מפרידה צריכה **לזכור משהו שונה**, לא סתם להיות ארוכה או מסובכת.", hold=0.5),
], stage=CSS + '<div id="sg" class="h">' + grid("sg", ROWS, COLS, OK1, corner="$x\\ \\backslash\\ z$") + '</div>',
   panel=st.card("sp-ok", "rule", "🔑 $T=\\{a^k\\}$ עם הסיפא $b^{2i}$: אינסופית ומפרידה")
       + st.card("sp-trap", "trap", "⚠️ $\\{a^kb^{2k}\\mid k\\ge1\\}$: אינסופית, <b>לא</b> מפרידה")
       + st.card("sp-trap2", "plain", "$z=\\varepsilon$: כולן בשפה. $z\\ne\\varepsilon$: כולן בחוץ."))

inter = Scene("inter", "דוגמה 2: חיתוך", [
    Pk("שפה חדשה מעל $\\{a,b,c\\}$: המילים שבהן $\\#_a=\\#_b+\\#_c$. אפשר גם בקבוצה מפרידה, אבל החיתוך מראה את זה מיד.",
       say="שפה חדשה מעל אֵיי, בִּי וסִי: המילים שבהן מספר האֵיי שווה למספר הבִּי ועוד מספר הסִי. אפשר גם בקבוצה מפרידה, אבל החיתוך מראה את זה מיד.",
       do=show("n-1")),
    Pk("אז נחתוך אותה עם $R=a^*b^*$: ה-$c$ נעלמות, והאותיות מסתדרות בגושים.",
       say="אז נחתוך אותה עם אַר שווה אֵיי כוכבית בִּי כוכבית: הסִי נעלמות, והאותיות מסתדרות בגושים.",
       do=show("n-2")),
    Pk("נשארות המילים $a^nb^m$ עם $n=m$, כלומר בדיוק $\\{a^nb^n\\}$. והיא לא רגולרית.",
       say="נשארות המילים אֵיי אֶן בִּי אֶם, עם אֶן שווה לאֶם. כלומר בדיוק אֵיי אֶן בִּי אֶן. והיא לא רגולרית.",
       do=show("n-3")),
    Pk("אילו $L$ הייתה רגולרית, גם החיתוך היה רגולרי. סתירה, ולכן $L$ לא רגולרית.",
       do=show("n-ok")),
    Pk("המלכודת: לא כל $R$ עוזרת. עם $R=(ab)^*$ החיתוך הוא $(ab)^*$ עצמה, שהיא רגולרית.",
       say="המלכודת: לא כל אַר עוזרת. עם אַר שווה אֵיי בִּי כוכבית, החיתוך הוא אֵיי בִּי כוכבית עצמה, שהיא רגולרית.",
       do=show("n-4", "n-trap")),
    Pk("וחיתוך רגולרי לא מוכיח כלום. בוחרים $R$ שהחיתוך איתה הוא שפה לא רגולרית **ידועה**.",
       hold=0.5),
], stage=CSS + '<div id="n-1" class="kl-line kl-big h">$L:\\ \\#_a=\\#_b+\\#_c$</div>'
         + '<div id="n-2" class="kl-line kl-big h">$L\\cap a^*b^*$</div>'
         + '<div id="n-3" class="kl-line kl-big h">$=\\{a^nb^n\\}$</div>'
         + '<div id="n-4" class="kl-line h">$L\\cap(ab)^*=(ab)^*$</div>',
   panel=st.card("n-ok", "rule", "🔑 בוחרים $R$ שמסדרת את האותיות בגושים, כך שהחיתוך הוא שפה לא רגולרית ידועה")
       + st.card("n-trap", "trap", "⚠️ חיתוך שיוצא רגולרי <b>לא מוכיח כלום</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    Pk("ועכשיו שאלה אמיתית ממבחן. השפה נתונה כרשימה: $\\varepsilon$, $aa$, $bb$, $aabb$, $a^4$, $b^4$, $a^4b^4$, וכן הלאה.",
       say="ועכשיו שאלה אמיתית ממבחן. השפה נתונה כרשימה: אפסילון, אֵיי אֵיי, בִּי בִּי, אֵיי אֵיי בִּי בִּי, ארבע אֵיי, ארבע בִּי, ארבע אֵיי וארבע בִּי, וכן הלאה."),
    Pk("נפרק אותה לשלושה חלקים: $a^{2k}$, $b^{2k}$, ו-$a^{2k}b^{2k}$.",
       say="נפרק אותה לשלושה חלקים: אֵיי בחזקת שתיים קֵיי, בִּי בחזקת שתיים קֵיי, ואֵיי בחזקת שתיים קֵיי, בִּי בחזקת שתיים קֵיי.",
       do=show("e-1")),
    Pk("המלכודת: שני החלקים הראשונים רגולריים, $(aa)^*$ ו-$(bb)^*$, אז בוחרים רגולרית. אבל החלק השלישי משווה.",
       say="המלכודת: שני החלקים הראשונים רגולריים, אֵיי אֵיי כוכבית, ובִּי בִּי כוכבית, אז בוחרים רגולרית. אבל החלק השלישי משווה.",
       do=show("e-trap")),
    Pk("נחתוך עם $R=aa^*bb^*$: לפחות $a$ אחד ולפחות $b$ אחד. החלקים הטהורים נעלמים.",
       say="נחתוך עם אַר שווה אֵיי, אֵיי כוכבית, בִּי, בִּי כוכבית: לפחות אֵיי אחת ולפחות בִּי אחת. החלקים הטהורים נעלמים.",
       do=hide("e-trap") + show("e-2")),
    Pk("נשאר $\\{a^{2k}b^{2k}\\mid k\\ge1\\}$, שאינה רגולרית: $\\{a^{2k}\\}$ מפרידה עם הסיפא $b^{2k}$.",
       say="נשאר אֵיי בחזקת שתיים קֵיי, בִּי בחזקת שתיים קֵיי, כאשר קֵיי לפחות אחת. היא אינה רגולרית: הקבוצה אֵיי בחזקת שתיים קֵיי מפרידה, עם הסיפא בִּי בחזקת שתיים קֵיי.",
       do=show("e-3")),
    Pk("אז $L$ לא רגולרית. סופית או רגולרית: נפסלות.", do=show("q-x-a", "q-n-a", "q-x-b", "q-n-b")),
    Pk("והאם היא ח״ה? כן: שלושה חלקים, וכל אחד מהם ח״ה. בדקדוק, $S$ גוזר משתנה אחד לכל חלק.",
       say="והאם היא חסרת הקשר? כן: שלושה חלקים, וכל אחד מהם חסר הקשר. בדקדוק, אֶס גוזר משתנה אחד לכל חלק.",
       do=show("e-4")),
    Pk("$M$ מוסיף $aa$ משמאל ו-$bb$ מימין בכל צעד: מונה אחד, מקונן. לכן לא ח״ה נפסלת.",
       say="המשתנה של החלק השלישי מוסיף אֵיי אֵיי משמאל, ובִּי בִּי מימין, בכל צעד: מונה אחד, מקונן. לכן לא חסרת הקשר נפסלת.",
       do=show("e-5", "q-x-d", "q-n-d")),
    Pk("התשובה: ח״ה ולא רגולרית. כשחלק קטן קשה, החיתוך שולף אותו החוצה.", do=show("q-ok-c"), hold=0.6),
], stage=CSS + '<div id="e-1" class="kl-line h">$L=\\{a^{2k}\\}\\cup\\{b^{2k}\\}\\cup\\{a^{2k}b^{2k}\\}$</div>'
         + '<div id="e-2" class="kl-line kl-big h">$L\\cap aa^*bb^*$</div>'
         + '<div id="e-3" class="kl-line kl-big h">$=\\{a^{2k}b^{2k}\\mid k\\ge1\\}$</div>'
         + '<div id="e-4" class="kl-line h">$S\\to A\\mid M\\mid B,\\quad A\\to aaA\\mid\\varepsilon,\\quad B\\to bbB\\mid\\varepsilon$</div>'
         + '<div id="e-5" class="kl-line h">$M\\to aaMbb\\mid\\varepsilon$</div>'
         + st.card("e-trap", "trap", "⚠️ חלקים רגולריים לא הופכים את <b>האיחוד</b> לרגולרי, אם חלק אחר משווה"),
   panel=opts_panel("q", Q, notes={"a": "אינסופית", "b": "החיתוך לא רגולרי", "d": "יש דקדוק"}))

recap = Scene("recap", "סיכום", [
    Pk("לסיכום, דרך א׳: קבוצה אינסופית ומפרידה, בדרך כלל $\\{a^i\\}$ עם הסיפא המשלימה.",
       say="לסיכום, דרך אָלֶף: קבוצה אינסופית ומפרידה, בדרך כלל אֵיי אַיי, עם הסיפא המשלימה.", do=show("c1")),
    Pk("דרך ב׳: חיתוך עם $R$ רגולרית שמסדרת את האותיות בגושים, ונותן שפה לא רגולרית ידועה.",
       say="דרך בֵּית: חיתוך עם אַר רגולרית, שמסדרת את האותיות בגושים, ונותן שפה לא רגולרית ידועה.", do=show("c2")),
    Pk("קבוצה אינסופית שכולה שקולה לא מוכיחה כלום, וגם חיתוך שיוצא רגולרי לא.", do=show("c3")),
    Pk("ומודולו או ״לפחות $k$״ עדיין רגולריות. נתראה ברמה הבאה.", say="ומודולו, או לפחות קֵיי, עדיין רגולריות. נתראה ברמה הבאה.",
       do=show("c4"), hold=0.8),
], stage=CSS + grid("rg", ROWS, COLS, OK1, corner="$x\\ \\backslash\\ z$").replace('class="h kl-', 'class="kl-'),
   panel=st.card("c1", "rule", "🔑 קבוצה מפרידה אינסופית, למשל $\\{a^i\\}$ + סיפא משלימה")
       + st.card("c2", "rule", "🔑 אם $L\\cap R$ לא רגולרית, אז $L$ לא רגולרית")
       + st.card("c3", "trap", "⚠️ קבוצה של מילים שקולות, או חיתוך רגולרי: לא מוכיחים כלום")
       + st.card("c4", "plain", "מודולו / &quot;לפחות $k$&quot;: עדיין רגולרית"))

VIDEO = Video("K03", "classify", "להוכיח שפה לא רגולרית",
              [title, ideas, sep, inter, exam, recap],
              bank={"24A-B-Q13": "c"})
