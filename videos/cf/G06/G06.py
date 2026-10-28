# -*- coding: utf-8 -*-
"""G06 · מהי L(M)? משוואת איזון — video script.

Source: tools/needhelp/cf/G06.py (lesson + goal). Exam anchor: 19B-B-Q25 (cited by the lesson's list of L(M) questions).
Not used on purpose: the quiz machines of G06 (a+/b-/c free, the nested 1/2 machine, a may-push, b may-pop, the Z bottom
marker). The worked example is a new chain machine (a +1, b -1, c free, d -1).
Course convention, said every time: accepted = the whole word read, an accepting state AND an empty stack.
Every machine, language and run below is checked with lib.PDA.
"""
import re
from nh import PDA, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, pda_svg, stack, run_pda, run_pda_raster, pda_path, replay, checks, edge_strip, CSS


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def P_(letters, cond):
    return lambda w: (lambda t: t is not None and cond(*t))(parts(w, letters))


# ---------------------------------------------------------------- worked example (new): chain a(+1) b(-1) c(0) d(-1)
M = PDA([("0", "a", "", "0", "A"), ("0", "", "", "1", ""), ("1", "b", "A", "1", ""), ("1", "", "", "2", ""),
         ("2", "c", "", "2", ""), ("2", "", "", "3", ""), ("3", "d", "A", "3", "")], "0", {"3"})
LM = P_("abcd", lambda i, n, k, m: i == n + m)
assert M.lang("abcd", 7) == {w for w in words("abcd", 7) if LM(w)}
# distractors killed by small words
assert M.accepts("ad") and not P_("abcd", lambda i, n, k, m: i == n and k == m)("ad")      # "i=n, k=m" falls on ad
assert M.accepts("c") and not P_("abcd", lambda i, n, k, m: i == n + m + k)("c")            # "c pops too" falls on c
assert not M.accepts("ba")                                                                   # order of states = order of letters
W = "aabcd"
PW = pda_path(M, W)
CW = replay(M, W, PW)
assert CW[-1] == ("3", 5, "", W)
N4 = {s: f"q_{s}" for s in "0123"}
POS4 = {"0": (110, 220), "1": (370, 220), "2": (630, 220), "3": (890, 220)}

# ---------------------------------------------------------------- exam 19B-B-Q25 (transcribed from the figure)
Q = BANK["19B-B-Q25"]
E = PDA([("0", "a", "", "1", "a"), ("1", "", "", "0", "a"), ("0", "", "", "2", "a"),
         ("2", "b", "a", "2", ""), ("2", "b", "", "2", "")], "0", {"2"})
EXP = {"a": P_("ab", lambda i, n: 2 * i < n), "b": P_("ab", lambda i, n: i < 2 * n),
       "c": P_("ab", lambda i, n: 2 * i > n), "d": P_("ab", lambda i, n: i > 2 * n)}
LE = E.lang("ab", 9)
assert [k for k, f in EXP.items() if LE == {w for w in words("ab", 9) if f(w)}] == [Q["correctId"]] == ["a"]
assert E.accepts("b") and not EXP["c"]("b") and not EXP["d"]("b")        # b kills 2i>n and i>2n
assert not E.accepts("ab") and EXP["b"]("ab")                             # ab kills i<2n
assert not E.accepts("abb") and E.accepts("abbb")                          # 2i+1 pops needed: equality would be n=2i+1
# without the extra push on the edge to q2 the language would be 2i <= n: the trap of forgetting it
E0 = PDA([("0", "a", "", "1", "a"), ("1", "", "", "0", "a"), ("0", "", "", "2", ""),
          ("2", "b", "a", "2", ""), ("2", "b", "", "2", "")], "0", {"2"})
assert E0.accepts("abb") and not E.accepts("abb")
XW = "abbb"
PX = pda_path(E, XW)
CX = replay(E, XW, PX)
assert [c[2] for c in CX][-1] == "" and CX[-1][0] == "2"
RINGS = [("0", 160, 168, 56), ("1", 482, 76, 56), ("2", 478, 364, 56)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה נמצא את השפה של אוטומט מחסנית, בלי להריץ אינסוף מילים."),
    p("שני כלים: סדר המצבים, ומשוואת איזון של דחיפות ושליפות.", hold=0.4),
], stage=CSS + '<div class="kicker">G06 · דקדוקים ואוטומט מחסנית</div><h1>מהי L(M)? משוואת איזון</h1>'
         '<p>למצוא את השפה של אוטומט מחסנית לפי סדר המצבים ומשוואת האיזון של דחיפות ושליפות.</p>',
   layout="title")

method = Scene("method", "השיטה", [
    p("שמונה שאלות בבנק שואלות: מהי $L(M)$? השיטה היא ארבעה צעדים.",
      say="שמונה שאלות בבנק שואלות: מהי השפה של האוטומט? השיטה היא ארבעה צעדים."),
    p("אחת: **סדר המצבים הוא סדר האותיות**. שרשרת מצבים עם לולאות $a$, $b$, $c$ נותנת מילים מהצורה $a^*b^*c^*$.",
      say="אחת: סדר המצבים הוא סדר האותיות. שרשרת מצבים עם לולאות אֵיי, בִּי, סִי, נותנת אֵיי כוכבית, בִּי כוכבית, סִי כוכבית.",
      do=show("m1")),
    p("שתיים: **משוואת איזון**. לכל אות כותבים כמה היא דוחפת, פלוס, וכמה היא שולפת, מינוס.", do=show("m2")),
    p("המחסנית ריקה בסוף אם ורק אם הסכום הוא אפס. וזה התנאי, כי מתקבלת פירושו מצב מקבל **וגם** מחסנית ריקה.",
      do=show("m2b")),
    p("שלוש: אות שלא נוגעת במחסנית, המספר שלה **חופשי**.", do=show("m3")),
    p("וארבע: בודקים את התשובה במילים קטנות, ופוסלים מסיחים.", do=show("m4"), hold=0.4),
], stage='<div class="cf-eq" style="font-size:46px">$q_0\\to q_1\\to q_2$ &nbsp;נותן&nbsp; $a^*b^*c^*$</div>'
         '<div id="m2b" class="cf-eq h" style="font-size:44px">סכום הדחיפות והשליפות $0$ אם ורק אם המחסנית ריקה</div>',
   panel=st.card("m1", "plain", "<b>1.</b> סדר המצבים = סדר האותיות")
       + st.card("m2", "rule", "🔑 <b>2.</b> משוואת איזון: דחיפה פלוס, שליפה מינוס, סכום אפס")
       + st.card("m3", "plain", "<b>3.</b> אות שלא נוגעת במחסנית: מספר חופשי")
       + st.card("m4", "plain", "<b>4.</b> פסילת מסיחים במילים קטנות"))

runW, cfW, leftW = run_pda("mx", M, W, PW, N4, tp="tw", stk="sw", fast=True,
                           lead="נוודא על $aabcd$. מתחילים ב-$q_0$, מחסנית ריקה.")
runW[0].do += show("tw-box")
example = Scene("example", "דוגמה: שרשרת וסכום", [
    p("אוטומט עם ארבעה מצבים בשרשרת, ומעברי $\\varepsilon$ ביניהם. לכן המילים הן $a^ib^nc^kd^m$.",
      say="אוטומט עם ארבעה מצבים בשרשרת, ומעברי אפסילון ביניהם. לכן המילים הן אֵיי, אחריהן בִּי, אחריהן סִי, ואחריהן דִי."),
    p("עכשיו האיזון. $a$ דוחפת: פלוס אחת.", say="עכשיו האיזון. אֵיי דוחפת: פלוס אחת.", do=show("bl-a", "mx-hs-0")),
    p("$b$ שולפת: מינוס אחת.", say="בִּי שולפת: מינוס אחת.", do=hide("mx-hs-0") + show("bl-b", "mx-hs-1")),
    p("$c$ לא נוגעת במחסנית: אפס. המספר שלה חופשי.", say="סִי לא נוגעת במחסנית: אפס. המספר שלה חופשי.",
      do=hide("mx-hs-1") + show("bl-c", "mx-hs-2")),
    p("ו-$d$ שולפת: מינוס אחת.", say="ודִי שולפת: מינוס אחת.", do=hide("mx-hs-2") + show("bl-d", "mx-hs-3")),
    p("המשוואה: $i-n-m=0$, כלומר $i=n+m$. ו-$k$ חופשי.",
      say="המשוואה: אַיי פחות אֵן פחות אֶם שווה אפס. כלומר אַיי שווה אֵן ועוד אֶם. וקֵיי חופשי.",
      do=hide("mx-hs-3") + show("bl-eq")),
    p("$L(M)=\\{a^ib^nc^kd^m\\mid i=n+m\\}$.",
      say="השפה היא אֵיי בחזקת אַיי, בִּי בחזקת אֵן, סִי בחזקת קֵיי, דִי בחזקת אֶם, כך שאַיי שווה אֵן ועוד אֶם.",
      do=show("bl-l")),
    *runW,
    p("קראנו הכל, $q_3$ מקבל, והמחסנית ריקה: מתקבלת. בדיוק כמו שהמשוואה אמרה.",
      do=show("vw-c1", "vw-c2", "vw-v")),
    p("ומילים קטנות פוסלות מסיחים: $ad$ בשפה, ולכן לא $i=n$. $c$ בשפה, ולכן $c$ לא שולפת.",
      say="ומילים קטנות פוסלות מסיחים: אֵיי דִי בשפה, ולכן לא אַיי שווה אֵן. סִי בשפה, ולכן סִי לא שולפת.",
      do=show("small"), hold=0.5),
], stage=pda_svg("mx", M, POS4, N4, w=1000, h=290, scale=1.15)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:640px"><div class="swap cf-c" style="--swap-h:250px">'
           '<div id="bal"><div class="cf-words" style="font-size:38px">'
           '<span id="bl-a" class="h">$a:+1$</span><span id="bl-b" class="h">$b:-1$</span>'
           '<span id="bl-c" class="h">$c:0$</span><span id="bl-d" class="h">$d:-1$</span></div>'
           '<div id="bl-eq" class="cf-eq cf-ltr h">$i-n-m=0$, &nbsp; $i=n+m$</div>'
           '<div id="bl-l" class="cf-eq h">$L(M)=\\{a^ib^nc^kd^m\\mid i=n+m\\}$</div></div>'
           f'<div id="tw-box" class="h">{st.tape("tw", W)}{checks("vw", True, True)}'
           '<div id="small" class="cf-words h" style="font-size:34px"><span>$ad\\in L$: לא $i=n$</span><span>$c\\in L$: $c$ לא שולפת</span></div></div>'
           '</div></div>'
         + stack("sw", [c[2] for c in CW]) + '</div>',
   panel='')
runW[0].do += hide("bal")
example.layout = "full"

RING = {"0": "0", "1": "1", "2": "2"}
runX, cfX, leftX = run_pda_raster("ex", E, XW, PX, "xt", "xs", "xl", RING,
                                  lead="נוודא על $abbb$: $i=1$, $n=3$, ו-$2<3$.",
                                  lead_say="נוודא על אֵיי בִּי בִּי בִּי: אַיי שווה אחת, אֵן שווה שלוש, ושתיים קטן משלוש.")
runX[0].do += show("xt-box") + hide("xbal")
opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן. סדר המצבים: $a$-ים בלולאה בין $q_0$ ל-$q_1$, ואז מעבר ל-$q_2$, ושם $b$-ים. כלומר $a^ib^n$.",
      say="שאלה ממבחן. סדר המצבים: אֵיי בלולאה בין קיו אפס לקיו אחת, ואז מעבר לקיו שתיים, ושם בִּי. כלומר אֵיי בחזקת אַיי, בִּי בחזקת אֵן.",
      do=show("ex-ring-0", "ex-ring-1")),
    p("כל $a$ דוחפת $a$ אחת בדרך ל-$q_1$, ועוד אחת בחזרה. כלומר פלוס שתיים.",
      say="כל אֵיי דוחפת אֵיי אחת בדרך לקיו אחת, ועוד אחת בחזרה. כלומר פלוס שתיים.", do=show("xb1")),
    p("ושימו לב: גם המעבר ל-$q_2$ דוחף $a$. עוד פלוס אחת, פעם אחת.",
      say="ושימו לב: גם המעבר לקיו שתיים דוחף אֵיי. עוד פלוס אחת, פעם אחת.",
      do=hide("ex-ring-1") + show("ex-ring-2", "xb2")),
    p("ב-$q_2$ יש **שתי** קשתות על $b$: אחת שולפת, ואחת לא נוגעת. כל $b$ היא מינוס אחת, **או** אפס.",
      say="בקיו שתיים יש שתי קשתות על בִּי: אחת שולפת, ואחת לא נוגעת. כל בִּי היא מינוס אחת, או אפס.", do=show("xb3")),
    p("שתי קשתות על אותה אות פירושן **אי-שוויון**: צריך $2i+1$ שליפות, ויש לכל היותר $n$.",
      say="שתי קשתות על אותה אות פירושן אי-שוויון: צריך שתיים אַיי ועוד אחת שליפות, ויש לכל היותר אֵן.",
      do=show("xb4")),
    p("לכן $2i+1\\le n$, כלומר $2i<n$.", say="לכן שתיים אַיי ועוד אחת קטן או שווה לאֵן, כלומר שתיים אַיי קטן מאֵן.",
      do=show("xb5")),
    p("מי ששוכח את הדחיפה במעבר ל-$q_2$ מקבל $2i\\le n$, ומי שמתעלם מהקשת השנייה כותב שוויון. שתיהן מלכודות.",
      say="מי ששוכח את הדחיפה במעבר לקיו שתיים מקבל שתיים אַיי קטן או שווה לאֵן, ומי שמתעלם מהקשת השנייה כותב שוויון. שתיהן מלכודות.",
      do=show("xtrap")),
    p("עכשיו מילים קטנות. $b$ בשפה: אפס $a$, ובִּי אחת שולפת את ה-$a$ של המעבר. זה פוסל את $2i>n$ ואת $i>2n$.",
      say="עכשיו מילים קטנות. בִּי בשפה: אין אֵיי, ובִּי אחת שולפת את האֵיי של המעבר. זה פוסל את שתי האפשרויות שבהן הצד של אַיי גדול.",
      do=show("q-x-c", "q-n-c", "q-x-d", "q-n-d")),
    p("$ab$ לא בשפה: שלוש דחיפות, ושליפה אחת לכל היותר. היא פוסלת את $i<2n$.",
      say="אֵיי בִּי לא בשפה: שלוש דחיפות, ושליפה אחת לכל היותר. היא פוסלת את אַיי קטן משתיים אֵן.",
      do=show("q-x-b", "q-n-b")),
    *runX,
    p("קראנו הכל, $q_2$ מקבל, והמחסנית ריקה: $abbb$ מתקבלת. התשובה: $2i<n$.",
      say="קראנו הכל, קיו שתיים מקבל, והמחסנית ריקה: אֵיי בִּי בִּי בִּי מתקבלת. התשובה: שתיים אַיי קטן מאֵן.",
      do=show("xv", "q-ok-a"), hold=0.6),
], stage=st.raster("ex", "images/exams/19B-B-Q25.png", 400, (634, 442), rings=RINGS)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:620px"><div class="swap cf-c" style="--swap-h:400px">'
           '<div id="xbal"><div class="cf-words" style="font-size:34px">'
           '<span id="xb1" class="h">$a:+2$</span><span id="xb2" class="h">מעבר ל-$q_2$: $+1$</span>'
           '<span id="xb3" class="h">$b:-1$ או $0$</span></div>'
           '<div id="xb4" class="cf-eq h">$2i+1$ שליפות, לכל היותר $n$</div>'
           '<div id="xb5" class="cf-eq cf-ltr h">$2i+1\\le n$, &nbsp; $2i<n$</div>'
         + st.card("xtrap", "trap", "⚠️ שתי קשתות על $b$: <b>אי-שוויון</b>; ואל תשכחו את הדחיפה במעבר") + '</div>'
           f'<div id="xt-box" class="h">{st.tape("xt", XW)}{edge_strip("xl", E, PX)}'
           '<div id="xv" class="verdict ok h">מצב מקבל + מחסנית ריקה ✓</div></div>'
           '</div></div>'
         + stack("xs", [c[2] for c in CX]) + '</div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>נתון האוטומט-מחסנית שמשמאל. מהי $L(A)$?</div>'
       + '<div class="cf-sm">' + st.options("q", opts, notes={"b": "$ab\\notin L$", "c": "$b\\in L$", "d": "$b\\in L$"}) + '</div>')

recap = Scene("recap", "סיכום", [
    p("לסיכום: סדר המצבים הוא סדר האותיות.", do=show("c1")),
    p("משוואת איזון: דחיפה פלוס, שליפה מינוס, והסכום אפס, כי מתקבלת פירושו מצב מקבל וגם מחסנית ריקה.", do=show("c2")),
    p("אות שלא נוגעת במחסנית: מספר חופשי.", do=show("c3")),
    p("ושתי קשתות על אותה אות: אי-שוויון, לא שוויון. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=pda_svg("rc", M, POS4, N4, w=1000, h=290),
   panel=st.card("c1", "rule", "🔑 סדר המצבים = סדר האותיות")
       + st.card("c2", "rule", "🔑 איזון: דחיפה פלוס, שליפה מינוס; סכום אפס אם ורק אם מחסנית ריקה")
       + st.card("c3", "rule", "🔑 אות שלא נוגעת במחסנית: חופשית")
       + st.card("c4", "trap", "⚠️ אם יש שתי קשתות על אותה אות, אז אי-שוויון"))

VIDEO = Video("G06", "cf", "מהי L(M)? משוואת איזון",
              [title, method, example, exam, recap],
              bank={"19B-B-Q25": "a"})
