# -*- coding: utf-8 -*-
"""G03 · איזה דקדוק יוצר את L, והכלה בין שפות — video script.

Source: tools/needhelp/cf/G03.py (lesson + goal). Exam anchor: 23A-B-Q20 (cited by the lesson's intro, not a quiz item; 23A-A-Q20 is avoided: its
reasoning repeats quiz Q5's distractor).
Not used on purpose: the quiz languages/grammars of G03 (#a=#b, a^k b^2k, AB with c/d against a^n b^n c^n d^n,
the SSS grammar of 26A-A-Q2, a^k b^k with k>=1). Example 2 is the lesson's own containment example.
Every grammar below is checked with lib.CFG before anything is rendered.
"""
import re
from nh import CFG, words, dfa_table
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, grammar, leftmost, deriv_inline, CSS


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def tex(rules):
    return "$" + rules.replace("->", r"\to ").replace("|", r"\mid ").replace("ε", r"\varepsilon ").replace(";", r";\ ") + "$"


# ---------------------------------------------------------------- example 1: odd palindromes (new)
ODDPAL = lambda w: len(w) % 2 == 1 and w == w[::-1]
R1 = [("1", "S->aSa|bSb|a|b", None), ("2", "S->aSa|bSb|ε", ""), ("3", "S->aSb|bSa|a|b", "aab"), ("4", "S->aS|bS|a|b", "ab")]
for k, r, killer in R1:
    G = CFG(r)
    good = G.lang(9) == {w for w in words("ab", 9) if ODDPAL(w)}
    assert good == (killer is None), r
    if killer is not None:
        assert G.derives(killer) and not ODDPAL(killer)        # each killer is derived but not in L
        assert all(len(w) >= len(killer) for w in words("ab", 9) if (w in G.lang(9)) != ODDPAL(w))   # and it is a shortest one
D3 = leftmost(CFG("S->aSb|bSa|a|b"), "aab")[0]
D4 = leftmost(CFG("S->aS|bS|a|b"), "ab")[0]

# ---------------------------------------------------------------- example 2: strict containment (the lesson's example)
GC = CFG("S->AB;A->0A1|ε;B->1B0|ε")
LG = lambda w: (lambda t: t is not None and t[1] == t[0] + t[2])(parts(w, "010"))
L1 = lambda w: (lambda t: t is not None and t[1] == 2 * t[0] and t[2] == t[0])(parts(w, "010"))
assert GC.lang(9) == {w for w in words("01", 9) if LG(w)}
assert all(GC.derives(w) for w in words("01", 9) if L1(w))           # L1 ⊆ L(G)
assert GC.derives("01") and not L1("01")                              # strict: 01 (m=1, k=0)
assert GC.derives("10") and not L1("10")

# ---------------------------------------------------------------- exam 23A-B-Q20 (the DFA transcribed from the figure)
Q = BANK["23A-B-Q20"]
DE = dfa_table("ab", {"0": "0 1", "1": "0 1"}, "0", {"1"})       # left state: a-loop, b->right; right: b-loop, a->left
LE = DE.lang(7)
assert LE == {w for w in words("ab", 7) if w.endswith("b")}       # bank: the words that end with b
GRAMS = {"a": CFG("S->aS|bT|b;T->aS|bT|a|b"), "b": CFG("S->aS|bT|b;T->aS|bT"), "c": CFG("S->Sa|Tb|b;T->Sa|Tb|a")}
OK = {k: G.lang(7) == LE for k, G in GRAMS.items()}
assert not any(OK.values()) and Q["correctId"] == "d"              # none of the three: "all other claims are false"
assert GRAMS["a"].derives("ba") and "ba" not in LE                 # a: derives ba, which does not end with b
assert "bb" in LE and not GRAMS["b"].derives("bb") and not GRAMS["c"].derives("bb")
assert "b" not in GRAMS["c"].lang(7, "T")                          # c: bb needs S->Tb with T=>b
assert "b" not in GRAMS["b"].lang(7, "T")                          # b: T has only aS and bT, never "b" alone
GOOD = CFG("S->aS|bT|b;T->aS|bT|b")                               # the state-by-state translation
assert GOOD.lang(7) == LE
DA = leftmost(GRAMS["a"], "ba")[0]
RINGS = [("0", 175, 213, 70), ("1", 568, 213, 70)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("עד עכשיו קיבלנו דקדוק ושאלנו מהי השפה שלו. עכשיו הכיוון ההפוך."),
    p("נתונה שפה וכמה דקדוקים: איזה מהם יוצר אותה בדיוק? ובסוף, הכלה ממש בין שפה לדקדוק.", hold=0.4),
], stage=CSS + '<div class="kicker">G03 · דקדוקים ואוטומט מחסנית</div><h1>איזה דקדוק יוצר את L?</h1>'
         '<p>לבחור את הדקדוק הנכון לשפה נתונה בעזרת מילה קצרה שנופלת, ולהכריע הכלה ממש בעזרת שני פרמטרים בלתי תלויים.</p>',
   layout="title")

method = Scene("method", "השיטה", [
    p("השאלה נראית ככה: נתונה שפה $L$, וארבעה דקדוקים. איזה מהם יוצר **בדיוק** את $L$?"),
    p("בדיוק פירושו שתי דרישות: כל מילה של $L$ נגזרת, ושום מילה מחוץ ל-$L$ לא נגזרת.", do=show("m0")),
    p("ולכן כדי לפסול דקדוק מספיקה **מילה אחת**:", do=show("m1")),
    p("מילה קצרה ב-$L$ שהדקדוק **לא** גוזר,", do=show("m2")),
    p("או מילה שהדקדוק גוזר, ו**אינה** ב-$L$.", do=show("m3")),
    p("ואיפה מחפשים? במילים הקצרות ביותר, ובראשן $\\varepsilon$: **כלל הבסיס קובע אם $\\varepsilon$ בשפה**.",
      do=show("m4"), hold=0.4),
], stage='<div class="cf-two"><div><div class="cf-cap">$L$</div><div class="cf-eq" style="font-size:44px">מילים של $L$</div></div>'
         '<div><div class="cf-cap">$L(G)$</div><div class="cf-eq" style="font-size:44px">מילים שהדקדוק גוזר</div></div></div>'
         '<div id="m0" class="cf-eq h" style="font-size:46px">$L(G)=L$ &nbsp;אם ורק אם&nbsp; $L\\subseteq L(G)$ וגם $L(G)\\subseteq L$</div>',
   panel=st.card("m1", "rule", "🔑 <b>מילה אחת מספיקה כדי לפסול דקדוק:</b>")
       + st.card("m2", "plain", "• מילה ב-$L$ שהדקדוק <b>לא</b> גוזר")
       + st.card("m3", "plain", "• מילה שהדקדוק גוזר ו<b>אינה</b> ב-$L$")
       + st.card("m4", "trap", "⚠️ <b>כלל הבסיס קובע אם $\\varepsilon$ בשפה</b>: התחילו מ-$\\varepsilon$ ומהמילים הקצרות"))

O1 = [(k, tex(r)) for k, r, _ in R1]
pal = Scene("pal", "דוגמה 1: פלינדרומים באורך אי-זוגי", [
    p("$L$ היא הפלינדרומים באורך **אי-זוגי** מעל $\\{a,b\\}$: $a$, $b$, $aba$, $bab$, $aaa$ וכן הלאה.",
      say="אֶל היא הפלינדרומים באורך אי-זוגי מעל אֵיי ובִּי: אֵיי, בִּי, אֵיי בִּי אֵיי, בִּי אֵיי בִּי, אֵיי אֵיי אֵיי, וכן הלאה."),
    p("ארבעה מועמדים. נתחיל מ-$\\varepsilon$: היא לא ב-$L$, כי האורך שלה אפס, זוגי.", do=show("pw-0")),
    p("הדקדוק עם $S\\to\\varepsilon$ גוזר אותה. נפסל.",
      say="הדקדוק שבו אֶס גוזר אפסילון גוזר אותה. נפסל.", do=show("p-x-2", "p-n-2")),
    p("מילים באורך שתיים: אף אחת מהן לא ב-$L$. הדקדוק עם $S\\to aS\\mid bS$ גוזר את $ab$.",
      say="מילים באורך שתיים: אף אחת מהן לא בשפה. הדקדוק עם אֶס גוזר אֵיי אֶס, או בִּי אֶס, גוזר את אֵיי בִּי.",
      do=show("pw-2", "pd4")),
    p("$ab$ אינה פלינדרום: נפסל.", say="אֵיי בִּי אינה פלינדרום: נפסל.", do=show("p-x-4", "p-n-4")),
    p("ומה עם $S\\to aSb\\mid bSa$? הוא עוטף באותיות **שונות**: $aab$ נגזרת, ואינה פלינדרום.",
      say="ומה עם הדקדוק שעוטף באֵיי ובִּי? הוא עוטף באותיות שונות: אֵיי אֵיי בִּי נגזרת, ואינה פלינדרום.",
      do=hide("pd4") + show("pw-3", "pd3")),
    p("נפסל.", do=show("p-x-3", "p-n-3")),
    p("נשאר הדקדוק שעוטף באותה אות משני הצדדים, ומסיים באות אחת: $S\\to aSa\\mid bSb\\mid a\\mid b$.",
      say="נשאר הדקדוק שעוטף באותה אות משני הצדדים, ומסיים באות אחת.", do=hide("pd3") + show("p-ok-1")),
    p("שלוש מילים קצרות, ושלושה דקדוקים נפלו. בלי להוכיח כלום על הדקדוק הנכון.", hold=0.5),
], stage='<div class="cf-eq" style="font-size:42px">$L$ = פלינדרומים באורך אי-זוגי: &nbsp;<span class="cf-ltr" style="display:inline-block">$a,\\ b,\\ aba,\\ bab,\\ aaa,\\ldots$</span></div>'
         '<div class="cf-words" style="font-size:44px">'
         '<span id="pw-0" class="h">$\\varepsilon\\notin L$</span><span id="pw-2" class="h">$ab\\notin L$</span>'
         '<span id="pw-3" class="h">$aab\\notin L$</span></div>'
         '<div class="swap cf-c" style="--swap-h:120px">'
         f'<div id="pd4" class="h"><div class="cf-eq cf-ltr">${deriv_inline(CFG("S->aS|bS|a|b"), D4)}$</div></div>'
         f'<div id="pd3" class="h"><div class="cf-eq cf-ltr">${deriv_inline(CFG("S->aSb|bSa|a|b"), D3)}$</div></div></div>',
   panel='<div class="qstem">איזה דקדוק יוצר את הפלינדרומים באורך אי-זוגי?</div>'
       + st.options("p", O1, notes={"2": "גוזר $\\varepsilon$", "3": "גוזר $aab$", "4": "גוזר $ab$"}))

cont = Scene("cont", "דוגמה 2: הכלה ממש", [
    p("סוג שני של שאלה: נתונה שפה $L_1$ ודקדוק $G$. האם $L_1$ שווה ל-$L(G)$, מוכלת בה ממש, או להפך?",
      say="סוג שני של שאלה: נתונה שפה אֶל אחת ודקדוק גֵ'י. האם אֶל אחת שווה לשפת הדקדוק, מוכלת בה ממש, או להפך?"),
    p("שלושה צעדים. אחת: כותבים את $L(G)$ עם **פרמטר נפרד לכל משתנה**.",
      say="שלושה צעדים. אחת: כותבים את שפת הדקדוק עם פרמטר נפרד לכל משתנה.", do=show("s1")),
    p("$A$ גוזר $0^m1^m$, ו-$B$ גוזר $1^k0^k$. לכן $L(G)=\\{0^m1^{m+k}0^k\\}$.",
      say="אֵיי גדולה גוזר אפס בחזקת אֶם, אחת בחזקת אֶם. בִּי גדולה גוזר אחת בחזקת קֵיי, אפס בחזקת קֵיי. לכן בשפת הדקדוק יש אפס בחזקת אֶם, אחת בחזקת אֶם ועוד קֵיי, אפס בחזקת קֵיי.",
      do=show("gc-rh-A", "gc-rh-B", "c1")),
    p("שתיים: השפה הנתונה היא כמעט תמיד המקרה שבו הפרמטרים **שווים**. כאן $m=k=n$.",
      say="שתיים: השפה הנתונה היא כמעט תמיד המקרה שבו הפרמטרים שווים. כאן אֶם שווה קֵיי שווה אֵן.",
      do=hide("gc-rh-A", "gc-rh-B") + show("s2", "c2")),
    p("לכן $L_1\\subseteq L(G)$.", say="לכן אֶל אחת מוכלת בשפת הדקדוק.", do=show("c3")),
    p("שלוש: מילת עדות להכלה ממש. פרמטר אחד $1$ והשני $0$: $m=1$, $k=0$ נותן $01$.",
      say="שלוש: מילת עדות להכלה ממש. פרמטר אחד שווה אחת, והשני אפס. אֶם שווה אחת וקֵיי שווה אפס נותן אפס אחת.",
      do=show("s3", "c4")),
    p("$01$ נגזרת, אבל היא לא ב-$L_1$. ולכן $L_1\\subsetneq L(G)$: מוכלת **ממש**.",
      say="אפס אחת נגזרת, אבל היא לא באֶל אחת. ולכן אֶל אחת מוכלת ממש בשפת הדקדוק.", do=show("c5")),
    p("ועוד הערה: $\\Sigma^*$ לא יכולה להיות מוכלת ממש באף שפה מעל $\\Sigma$. אין לאן לגדול.",
      say="ועוד הערה: סיגמא כוכבית לא יכולה להיות מוכלת ממש באף שפה מעל סיגמא. אין לאן לגדול.",
      do=show("s4"), hold=0.5),
], stage=grammar("gc", GC, big=True)
         + '<div style="display:flex;flex-direction:column;gap:12px;align-items:center">'
           '<div id="c1" class="cf-eq h">$L(G)=\\{0^m1^{m+k}0^k\\mid m,k\\ge0\\}$</div>'
           '<div id="c2" class="cf-eq h">$L_1=\\{0^n1^{2n}0^n\\mid n\\ge0\\}$ &nbsp;=&nbsp; המקרה $m=k$</div>'
           '<div id="c3" class="cf-mid h">$L_1\\subseteq L(G)$</div>'
           '<div id="c4" class="cf-mid h">$m=1,\\ k=0$: &nbsp; $01\\in L(G)$, &nbsp; $01\\notin L_1$</div>'
           '<div id="c5" class="verdict ok h">$L_1\\subsetneq L(G)$</div></div>',
   panel=st.card("s1", "plain", "<b>1.</b> $L(G)$ עם פרמטר בלתי תלוי לכל משתנה")
       + st.card("s2", "plain", "<b>2.</b> השפה הנתונה = המקרה שבו הפרמטרים <b>שווים</b>")
       + st.card("s3", "rule", "🔑 <b>3.</b> מילת עדות: פרמטר אחד $1$, השני $0$")
       + st.card("s4", "trap", "⚠️ $\\Sigma^*$ לא מוכלת ממש באף שפה מעל $\\Sigma$"))

opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן: איזה דקדוק יוצר את השפה של האס״ד הזה? שלושה דקדוקים, ועוד האפשרות שכל הטענות האחרות לא נכונות."),
    p("קודם השפה. המצב המקבל הוא הימני, ונכנסים אליו רק באות $b$. ומכל מצב, $b$ מובילה אליו.",
      say="קודם השפה. המצב המקבל הוא הימני, ונכנסים אליו רק באות בִּי. ומכל מצב, בִּי מובילה אליו.",
      do=show("ex-ring-1")),
    p("כלומר $L$ היא כל המילים שמסתיימות ב-$b$.", say="כלומר השפה היא כל המילים שמסתיימות בבִּי.",
      do=hide("ex-ring-1") + show("xl")),
    p("המילים הקצרות: $b$, ואז $ab$ ו-$bb$. ו-$\\varepsilon$, $a$, $ba$ **לא** בשפה.",
      say="המילים הקצרות: בִּי, ואז אֵיי בִּי ובִּי בִּי. ואפסילון, אֵיי ובִּי אֵיי לא בשפה.", do=show("xw")),
    p("איך נראה הדקדוק הנכון? מתרגמים מצב למשתנה: $S$ למצב השמאלי, $T$ לימני.",
      say="איך נראה הדקדוק הנכון? מתרגמים מצב למשתנה: אֶס למצב השמאלי, טִי לימני.", do=show("ex-ring-0", "ex-ring-1")),
    p("כל חץ הוא כלל, ומעבר לתוך המצב המקבל מוסיף גם כלל שמסיים: $b$ לבד.",
      say="כל חץ הוא כלל, ומעבר לתוך המצב המקבל מוסיף גם כלל שמסיים: בִּי לבד.",
      do=hide("ex-ring-0", "ex-ring-1") + show("xg")),
    p("עכשיו משווים. הדקדוק עם $T\\to a$: אפשר לסיים אחרי $a$.",
      say="עכשיו משווים. הדקדוק שבו טִי גוזר אֵיי: אפשר לסיים אחרי אֵיי.", do=show("xa")),
    p("הוא גוזר את $ba$, שלא מסתיימת ב-$b$. נפסל.", say="הוא גוזר את בִּי אֵיי, שלא מסתיימת בבִּי. נפסל.",
      do=show("q-x-a", "q-n-a")),
    p("הדקדוק בלי $T\\to b$: בלעדיו ל-$T$ יש רק $aS$ ו-$bT$, ולכן $T$ לא גוזר את $b$ לבד.",
      say="הדקדוק שאין בו את הכלל טִי גוזר בִּי: בלעדיו לטִי יש רק אֵיי אֶס ובִּי טִי, ולכן טִי לא גוזר את בִּי לבד.", do=hide("xa")),
    p("לכן $bb$, שמסתיימת ב-$b$, לא נגזרת: היא צריכה $S\\to bT$ ו-$T$ שגוזר $b$. נפסל.",
      say="לכן בִּי בִּי, שמסתיימת בבִּי, לא נגזרת: היא צריכה שאֶס יגזור בִּי טִי, וטִי שגוזר בִּי. נפסל.",
      do=show("q-x-b", "q-n-b")),
    p("הדקדוק השמאלי, עם המשתנה משמאל. גם בו $bb$ לא נגזרת: צריך $S\\to Tb$ עם $T$ שגוזר $b$, ו-$T$ לא גוזר $b$. נפסל.",
      say="הדקדוק השמאלי, עם המשתנה משמאל. גם בו בִּי בִּי לא נגזרת: צריך שאֶס יגזור טִי בִּי, עם טִי שגוזר בִּי, וטִי לא גוזר בִּי. נפסל.",
      do=show("q-x-c", "q-n-c")),
    p("שלושתם נפלו, ולכן התשובה: כל הטענות האחרות לא נכונות.", do=show("q-ok-d")),
    p("המלכודת: שניים הם התרגום עם כלל מיותר או חסר, והשלישי כתוב בכיוון ההפוך. מילה קצרה מכריעה.",
      say="המלכודת: שניים הם התרגום עם כלל מיותר או חסר, והשלישי כתוב בכיוון ההפוך. מילה קצרה מכריעה.",
      do=show("xtrap"), hold=0.6),
], stage=st.raster("ex", "images/exams/23A-B-Q20.png", 520, (702, 295), rings=RINGS)
         + '<div id="xl" class="cf-eq h">$L$ = כל המילים שמסתיימות ב-$b$</div>'
         + '<div id="xw" class="cf-words h"><span>$b$</span><span>$ab$</span><span>$bb$</span>'
           '<span>$\\varepsilon,\\ a,\\ ba\\notin L$</span></div>'
         + '<div class="swap cf-c" style="--swap-h:150px">'
         + '<div id="xg" class="h">' + grammar("xgg", GOOD) + '</div></div>'
         # the derivation is hidden before the trap card appears: they share one slot (the card ran into the subtitles)
         + '<div class="swap" style="--swap-h:130px">'
         + f'<div><div id="xa" class="cf-eq cf-ltr h">${deriv_inline(GRAMS["a"], DA)}$</div></div>'
         + '<div>' + st.card("xtrap", "trap", "⚠️ <b>כמעט התרגום</b>: כלל אחד מיותר ($T\\to a$) או חסר ($T\\to b$), או כתוב בכיוון ההפוך, מספיק כדי לפסול.")
         + '</div></div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>איזה מהדקדוקים הבאים יוצר את השפה של האס״ד שמשמאל?</div>'
       + '<div class="cf-sm">' + st.options("q", opts, notes={"a": "גוזר $ba$", "b": "לא גוזר $bb$", "c": "לא גוזר $bb$"}) + '</div>')

recap = Scene("recap", "סיכום", [
    p("לסיכום: כדי לפסול דקדוק מספיקה מילה קצרה אחת, בכיוון אחד או בשני.", do=show("c1")),
    p("כלל הבסיס קובע אם $\\varepsilon$ בשפה: תמיד מתחילים ממנה.", do=show("c2")),
    p("ובהכלה: פרמטר נפרד לכל משתנה, השפה הנתונה היא המקרה שבו הם שווים, ומילת העדות היא פרמטר אחד $1$ והשני $0$.",
      say="ובהכלה: פרמטר נפרד לכל משתנה, השפה הנתונה היא המקרה שבו הם שווים, ומילת העדות היא פרמטר אחד אחת והשני אפס.",
      do=show("c3")),
    p("נתראה ברמה הבאה.", hold=0.8),
], stage=grammar("rc", GC, big=True),
   panel=st.card("c1", "rule", "🔑 מילה קצרה אחת פוסלת דקדוק")
       + st.card("c2", "trap", "⚠️ כלל הבסיס קובע אם $\\varepsilon$ בשפה")
       + st.card("c3", "rule", "🔑 הכלה ממש: פרמטרים בלתי תלויים; עדות = פרמטר אחד $1$, השני $0$"))

VIDEO = Video("G03", "cf", "איזה דקדוק יוצר את L",
              [title, method, pal, cont, exam, recap],
              bank={"23A-B-Q20": "d"})
