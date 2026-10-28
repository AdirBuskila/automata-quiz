# -*- coding: utf-8 -*-
"""G01 · לקרוא דקדוק: גזירה, משתנים והמילים הקצרות — video script.

Source: tools/needhelp/cf/G01.py (lesson + goal). Exam anchor: 25A-A-Q9 (cited by the lesson's trap box, not by the quiz).
Not used on purpose: the quiz grammars of G01 (S->aSb|bSa|ε, S->SaS|b — so 23A-A-Q12 is not solved here —,
S->AB with B->bB|b, S->S101 as a quiz question). S->S101 appears only as the lesson's own rule (24A-B-Q11).
Every grammar below is checked with lib.CFG before anything is rendered.
"""
import re
from nh import CFG, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, grammar, leftmost, deriv_lines, tree_svg, grow, grow_end, gram_tex, CSS


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def same(G, alpha, pred, n=8):
    return G.lang(n) == {w for w in words(alpha, n) if pred(w)}


# ---------------------------------------------------------------- grammars (verified)
G1 = CFG("S->aSb|c")                                   # new (the quiz uses T->aTb|ε, so it is not shown)
assert same(G1, "abc", lambda w: (lambda t: t is not None and t[0] == t[2] and t[1] == 1)(parts(w, "acb")))
D1 = leftmost(G1, "aacbb")
assert len(D1) == 1 and len(D1[0]) == 3                 # S => aSb => aaSbb => aacbb, the only derivation
STEPS1 = D1[0]

G0 = CFG("S->aSb")                                     # the lesson's rule (no rule finishes S), new grammar
assert G0.lang(9) == set()

# new example: decode variable by variable
G2 = CFG("S->AB;A->aAbb|ε;B->cB|ε")
L2 = lambda w: (lambda t: t is not None and t[1] == 2 * t[0])(parts(w, "abc"))
assert same(G2, "abc", L2)
assert G2.lang(8, "A") == {"a" * n + "b" * (2 * n) for n in range(3)}
assert G2.lang(8, "B") == {"c" * n for n in range(9)}
SHORT2 = sorted(G2.lang(4), key=lambda w: (len(w), w))[:4]
assert SHORT2 == ["", "c", "cc", "abb"]
OPT2 = [("1", r"$\{a^nb^{2n}c^k\mid n,k\ge0\}$", L2),
        ("2", r"$\{a^nb^{2n}c^n\mid n\ge0\}$", lambda w: (lambda t: t is not None and t[1] == 2 * t[0] and t[2] == t[0])(parts(w, "abc"))),
        ("3", r"$\{a^nb^nc^k\mid n,k\ge0\}$", lambda w: (lambda t: t is not None and t[1] == t[0])(parts(w, "abc")))]
assert [k for k, _, f in OPT2 if same(G2, "abc", f)] == ["1"]
assert G2.derives("c") and not OPT2[1][2]("c")          # c kills a^n b^2n c^n
assert G2.derives("abb") and not OPT2[2][2]("abb")      # abb kills a^n b^n c^k

# exam 25A-A-Q9
Q = BANK["25A-A-Q9"]
GE = CFG("S->aMb|ε;M->aSb")
GS = CFG("S->aaSbb|ε")                                 # after substituting M
assert GE.lang(12) == GS.lang(12)
EXP = {"a": lambda w: (lambda t: t is not None and t[0] == t[1] and t[0] % 2 == 0)(parts(w, "ab")),
       "b": lambda w: re.fullmatch("(abab)*", w) is not None,
       "c": lambda w: (lambda t: t is not None and t[0] == t[1])(parts(w, "ab")),
       "d": lambda w: re.fullmatch("(ab)*", w) is not None}
assert [k for k, f in EXP.items() if same(GE, "ab", f, 12)] == [Q["correctId"]] == ["a"]
SHORTE = sorted(GE.lang(8), key=lambda w: (len(w), w))
assert SHORTE == ["", "aabb", "aaaabbbb"]
assert EXP["c"]("ab") and not GE.derives("ab") and EXP["d"]("ab")
assert EXP["b"]("abab") and not GE.derives("abab")
assert all("aSb" not in alt for alt in GE.rules["S"])  # S alone never wraps a single a...b

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה נלמד לקרוא דקדוק חסר הקשר: מה גוזרים, ואיך מגיעים למילה."),
    p("נפענח דקדוק משתנה אחר משתנה, ונפסול אפשרויות בעזרת המילים הקצרות."),
    p("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage=CSS + '<div class="kicker">G01 · דקדוקים ואוטומט מחסנית</div><h1>לקרוא דקדוק</h1>'
         '<p>לפענח דקדוק חסר הקשר בשיטה של משתנה אחר משתנה, ולפסול אפשרויות במילה קצרה.</p>',
   layout="title")

terms = Scene("terms", "מה זה דקדוק", [
    p("דקדוק חסר הקשר, ח״ה, הוא רביעייה: $G=\\langle\\Sigma,V,S,R\\rangle$.",
      say="דקדוק חסר הקשר הוא רביעייה: גֵ'י שווה סיגמא, וִי, אֶס, אָר.", do=show("t-g")),
    p("$\\Sigma$ הן האותיות, ה**טרמינלים**. כאן $a$, $b$ ו-$c$.", say="סיגמא הן האותיות, הטרמינלים. כאן אֵיי, בִּי וסִי.",
      do=show("t-sig")),
    p("$V$ הם ה**משתנים**, באותיות גדולות. כאן יש משתנה אחד: $S$, והוא גם המשתנה ההתחלתי.",
      do=show("t-v", "g1-rh-S")),
    p("$R$ הם **כללי הגזירה**. הכלל $S\\to aSb$ אומר: מותר להחליף את $S$ ב-$aSb$.",
      do=hide("g1-rh-S") + show("t-r", "g1-a-S-0")),
    p("והכלל $S\\to c$ אומר: מותר להחליף את $S$ באות $c$, וכך לסיים.", do=hide("g1-a-S-0") + show("g1-a-S-1")),
    p("השפה $L(G)$ היא כל המילים שאפשר לגזור מ-$S$, ושיש בהן **רק טרמינלים**.",
      say="השפה אֶל של גֵ'י היא כל המילים שאפשר לגזור מאֶס, ושיש בהן רק טרמינלים.",
      do=hide("g1-a-S-1") + show("t-l"), hold=0.4),
], stage=grammar("g1", G1, big=True)
         + '<div class="hint">$\\to$ פירושו: מותר להחליף את המשתנה שמשמאל במה שמימין</div>',
   panel=st.card("t-g", "plain", "<b>דקדוק ח״ה</b>: $G=\\langle\\Sigma,V,S,R\\rangle$")
       + st.card("t-sig", "plain", "$\\Sigma$: <b>טרמינלים</b>, האותיות של המילה")
       + st.card("t-v", "plain", "$V$: <b>משתנים</b>; $S\\in V$ המשתנה ההתחלתי")
       + st.card("t-r", "plain", "$R$: <b>כללי גזירה</b> $A\\to\\alpha$")
       + st.card("t-l", "rule", "$L(G)$ = כל המילים <b>הטרמינליות</b> שנגזרות מ-$S$"))

ph_d = [p("נגזור את המילה $aacbb$. מתחילים תמיד במשתנה ההתחלתי, $S$.", do=show("t1-x-1")),
        p("צעד ראשון: מחליפים את $S$ ב-$aSb$.", do=grow("t1", "d1", STEPS1, 1, gram="g2")),
        p("עכשיו יש לנו $aSb$. ה-$S$ באמצע הוא עדיין משתנה, אז ממשיכים.", say="עכשיו יש לנו אֵיי אֶס בִּי. האֶס באמצע הוא עדיין משתנה, אז ממשיכים."),
        p("שוב $S\\to aSb$: מקבלים $aaSbb$.", do=grow("t1", "d1", STEPS1, 2, gram="g2")),
        p("ועכשיו מסיימים עם הכלל $S\\to c$.", do=grow("t1", "d1", STEPS1, 3, gram="g2")),
        p("נשארו רק טרמינלים: $aacbb$. סיימנו, והמילה בשפה.", do=grow_end("t1", STEPS1, gram="g2") + show("d-ok")),
        p("כל הפעלה של $S\\to aSb$ מוסיפה $a$ משמאל ו-$b$ מימין, ולכן השפה היא $\\{a^ncb^n\\mid n\\ge0\\}$.",
          do=show("d-lang"), hold=0.4),
        p("ועכשיו דקדוק אחר: $S\\to aSb$, בלי שום כלל נוסף.", do=hide("d1-box", "d-lang", "d-ok") + show("d0-box")),
        p("$S$ הופך ל-$aSb$, ואז ל-$aaSbb$, וה-$S$ תמיד נשאר.",
          say="אֶס הופך לאֵיי אֶס בִּי, ואז לאֵיי אֵיי אֶס בִּי בִּי, והאֶס תמיד נשאר.", do=show("d0-l")),
        p("אין שום כלל שמחסל את $S$, ולכן אף גזירה לא נגמרת במילה טרמינלית.", do=show("d0-x")),
        p("השפה של הדקדוק הזה היא **השפה הריקה**, וזה דקדוק חוקי לגמרי.", do=show("d-rule"), hold=0.5)]
derive = Scene("derive", "דוגמה 1: גזירה ועץ", ph_d,
    stage='<div class="swap cf-c" style="--swap-h:680px">'
          '<div id="d1-box">' + '<div class="cf-row" style="align-items:flex-start;gap:70px">'
          + deriv_lines("d1", G1, STEPS1) + tree_svg("t1", G1, STEPS1, w=420, scale=1.25) + '</div>'
          + '<div id="d-ok" class="verdict ok h">$aacbb\\in L(G)$ ✓</div>'
          + '<div id="d-lang" class="cf-eq h">$L(G)=\\{a^ncb^n\\mid n\\ge0\\}$</div></div>'
          '<div id="d0-box" class="h">' + grammar("g0", G0, big=True)
          + '<div id="d0-l" class="cf-deriv h" style="margin-top:30px">$S\\Rightarrow aSb\\Rightarrow aaSbb\\Rightarrow aaaSbbb\\Rightarrow\\ldots$</div>'
          + '<div id="d0-x" class="verdict bad h">אין כלל שמחסל את $S$: $L(G)=\\emptyset$</div></div>'
          '</div>',
    panel=grammar("g2", G1)
        + '<div class="hint">גזירה שמאלית: בכל צעד מחליפים את המשתנה השמאלי ביותר (בצבע)</div>'
        + st.card("d-rule", "rule", "🔑 <b>רק מילים טרמינליות נכנסות לשפה.</b> גזירה שאי אפשר לסיים לא תורמת כלום."))

method = Scene("method", "שיטת הפענוח", [
    p("איך מפענחים דקדוק גדול? ארבעה צעדים."),
    p("אחת: **מפענחים כל משתנה לבד**, מלמטה למעלה. מה כל משתנה גוזר?", do=show("m1")),
    p("שתיים: מזהים תבניות מוכרות. הנה כמה מהן.", do=show("m2", "mt")),
    p("$A\\to aA\\mid a$ גוזר $a^+$, כלומר לפחות $a$ אחת.",
      say="אֵיי גדולה, שגוזר אֵיי אֵיי גדולה או אֵיי, גוזר אֵיי פלוס, כלומר לפחות אֵיי אחת.", do=show("mt-2")),
    p("$S\\to aSa\\mid bSb\\mid a\\mid b\\mid\\varepsilon$ גוזר את כל הפלינדרומים: עוטפים באותה אות משני הצדדים.",
      say="אֶס, שעוטף באֵיי משני הצדדים או בבִּי משני הצדדים, ומסיים באות אחת או באפסילון, גוזר את כל הפלינדרומים.",
      do=show("mt-1")),
    p("ו-$B\\to aB\\mid bB\\mid\\varepsilon$ גוזר את כל המילים, $\\Sigma^*$.",
      say="ובִּי גדולה, שגוזר אֵיי בִּי גדולה, או בִּי בִּי גדולה, או אפסילון, גוזר את כל המילים, סיגמא כוכבית.",
      do=show("mt-3")),
    p("שלוש: מרכיבים. $S\\to AB$ הוא **שרשור**, ו-$S\\to A\\mid B$ הוא **איחוד**.", do=show("m3")),
    p("וארבע: בודקים את $\\varepsilon$ ואת המילים הקצרות ביותר. רוב המסיחים נופלים עליהן.", do=show("m4"), hold=0.4),
], stage='<div id="mt" class="h" style="display:flex;flex-direction:column;gap:22px;align-items:center">'
         '<div id="mt-2" class="cf-eq h">$A\\to aA\\mid a$ &nbsp;גוזר&nbsp; $a^+$</div>'
         '<div id="mt-1" class="cf-eq h">$S\\to aSa\\mid bSb\\mid a\\mid b\\mid\\varepsilon$ &nbsp;גוזר&nbsp; פלינדרומים</div>'
         '<div id="mt-3" class="cf-eq h">$B\\to aB\\mid bB\\mid\\varepsilon$ &nbsp;גוזר&nbsp; $\\Sigma^*$</div></div>',
   panel=st.card("m1", "plain", "<b>1.</b> פענחו כל משתנה לבד, מלמטה למעלה")
       + st.card("m2", "plain", "<b>2.</b> זהו תבניות מוכרות")
       + st.card("m3", "plain", "<b>3.</b> הרכיבו: $AB$ שרשור, $A\\mid B$ איחוד")
       + st.card("m4", "rule", "🔑 <b>4.</b> בדקו את $\\varepsilon$ ואת המילים הקצרות ביותר"))

W2 = "".join(f'<span id="w2-{i}" class="h">${w if w else chr(92) + "varepsilon"}$</span>' for i, w in enumerate(SHORT2))
decode = Scene("decode", "דוגמה 2: משתנה אחר משתנה", [
    p("דקדוק חדש, מעל $\\{a,b,c\\}$. מהי השפה שלו?", say="דקדוק חדש, מעל אֵיי, בִּי וסִי. מהי השפה שלו?"),
    p("מתחילים מלמטה. $A\\to aAbb\\mid\\varepsilon$: כל צעד מוסיף $a$ אחת משמאל ו**שתי** $b$ מימין. $A$ גוזר $a^nb^{2n}$.",
      say="מתחילים מלמטה. אֵיי גדולה גוזר אֵיי, אֵיי גדולה, בִּי בִּי, או אפסילון: כל צעד מוסיף אֵיי אחת משמאל ושתי בִּי מימין. אֵיי גדולה גוזר אֵיי בחזקת אֵן, בִּי בחזקת שתיים אֵן.",
      do=show("g3-rh-A", "dc-a")),
    p("$B\\to cB\\mid\\varepsilon$: כל צעד מוסיף $c$, ולכן $B$ גוזר $c^*$, מספר כלשהו של $c$.",
      do=hide("g3-rh-A") + show("g3-rh-B", "dc-b")),
    p("ו-$S\\to AB$ הוא שרשור: קודם מה ש-$A$ גוזר, ואחריו מה ש-$B$ גוזר.",
      say="ואֶס שגוזר אֵיי גדולה בִּי גדולה הוא שרשור: קודם מה שאֵיי גדולה גוזר, ואחריו מה שבִּי גדולה גוזר.",
      do=hide("g3-rh-B") + show("g3-rh-S", "dc-s")),
    p("ה-$n$ של $A$ וה-$k$ של $B$ לא קשורים זה לזה. לכן $L=\\{a^nb^{2n}c^k\\mid n,k\\ge0\\}$.",
      say="האֵן של אֵיי גדולה והקֵיי של בִּי גדולה לא קשורים זה לזה. לכן השפה היא אֵיי בחזקת אֵן, בִּי בחזקת שתיים אֵן, סִי בחזקת קֵיי.",
      do=hide("g3-rh-S") + show("dc-l")),
    p("עכשיו בודקים במילים קצרות. הראשונה: $\\varepsilon$, כש-$A$ ו-$B$ שניהם נמחקים.",
      do=show("dc-w", "w2-0")),
    p("אחריה $c$, ואז $cc$ ו-$abb$.", say="אחריה סִי, ואז סִי סִי, ואֵיי בִּי בִּי.",
      do=show("w2-1", "w2-2", "w2-3")),
    p("נניח שהאפשרויות הן אלה. $c$ בשפה שלנו: אין $a$, אבל יש $c$ אחת. ב-$a^nb^{2n}c^n$ היא לא: נפסלת.",
      say="נניח שהאפשרויות הן אלה. סִי בשפה שלנו: אין אֵיי, אבל יש סִי אחת. בשפה שבה מספר הסִי שווה למספר האֵיי היא לא: נפסלת.",
      do=show("o2-x-2", "o2-n-2")),
    p("$abb$ בשפה שלנו: $a$ אחת ושתי $b$. ב-$a^nb^nc^k$ מספר ה-$b$ שווה למספר ה-$a$: נפסלת.",
      say="אֵיי בִּי בִּי בשפה שלנו: אֵיי אחת ושתי בִּי. בשפה שבה מספר הבִּי שווה למספר האֵיי היא לא: נפסלת.",
      do=show("o2-x-3", "o2-n-3")),
    p("נשארה $a^nb^{2n}c^k$. שתי מילים קצרות הספיקו.",
      say="נשארה אֵיי בחזקת אֵן, בִּי בחזקת שתיים אֵן, סִי בחזקת קֵיי. שתי מילים קצרות הספיקו.", do=show("o2-ok-1"), hold=0.5),
], stage=grammar("g3", G2, big=True)
         + '<div style="display:flex;flex-direction:column;gap:10px;align-items:center">'
           '<div id="dc-a" class="cf-mid h">$A$ גוזר $a^nb^{2n}$</div>'
           '<div id="dc-b" class="cf-mid h">$B$ גוזר $c^*$</div>'
           '<div id="dc-s" class="cf-mid h">$S\\to AB$: שרשור</div>'
           '<div id="dc-l" class="cf-eq h">$L(G)=\\{a^nb^{2n}c^k\\mid n,k\\ge0\\}$</div></div>'
         + f'<div id="dc-w" class="cf-words h">{W2}</div>',
   panel='<div class="qstem">מהי $L(G)$?</div>'
       + st.options("o2", [(k, t) for k, t, _ in OPT2], notes={"2": "$c$ נופלת", "3": "$abb$ נופלת"}))

opts = [(o["id"], o["html"]) for o in Q["options"]]
WE = "".join(f'<span id="we-{i}" class="h">${w if w else chr(92) + "varepsilon"}$</span>' for i, w in enumerate(SHORTE))
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן: מהי השפה של הדקדוק הזה? יש בו שני משתנים, $S$ ו-$M$."),
    p("$M$ מופיע רק בתוך $S$, אז נציב אותו: נכתוב את $aSb$ במקום $M$.", do=show("ex-rh-M")),
    p("$S\\to a(aSb)b$, כלומר $S\\to aaSbb\\mid\\varepsilon$.",
      say="אֶס גוזר אֵיי, אֵיי אֶס בִּי, בִּי. כלומר אֶס גוזר אֵיי אֵיי אֶס בִּי בִּי, או אפסילון.",
      do=hide("ex-rh-M") + show("ex-sub")),
    p("**הצבה מבטלת משתני עזר**: עכשיו רואים שכל סיבוב מוסיף **שתי** $a$ ו**שתי** $b$.", do=show("ex-rule")),
    p("המילים הקצרות: $\\varepsilon$, אחר כך $aabb$, אחר כך $aaaabbbb$.",
      say="המילים הקצרות: אפסילון, אחר כך אֵיי אֵיי בִּי בִּי, ואחר כך ארבע אֵיי וארבע בִּי.",
      do=show("ex-w", "we-0", "we-1", "we-2")),
    p("והמלכודת: $a^nb^n$ נראית נכונה, כי הדקדוק עוטף $a$ משמאל ו-$b$ מימין.",
      do=show("ex-trap")),
    p("אבל $ab$ לא נגזרת: אין דרך לסיים אחרי סיבוב אחד, כי $M$ חייב להחזיר $S$ עם עוד $a$ ועוד $b$.",
      say="אבל אֵיי בִּי לא נגזרת: אין דרך לסיים אחרי סיבוב אחד, כי אֶם חייב להחזיר אֶס עם עוד אֵיי ועוד בִּי.",
      do=show("q-x-c", "q-n-c")),
    p("גם $(ab)^n$ נופלת על $ab$, ו-$(ab)^{2n}$ נופלת על $abab$, שגם היא לא נגזרת.",
      say="גם אֵיי בִּי בחזקת אֵן נופלת על אֵיי בִּי, ואֵיי בִּי בחזקת שתיים אֵן נופלת על אֵיי בִּי אֵיי בִּי, שגם היא לא נגזרת.",
      do=show("q-x-d", "q-n-d", "q-x-b", "q-n-b")),
    p("התשובה: $\\{a^{2n}b^{2n}\\mid n\\ge0\\}$. והמלכודת: לבחור $a^nb^n$ בלי לבדוק את $ab$.",
      do=show("q-ok-a"), hold=0.6),
], stage=grammar("ex", GE, big=True)
         + '<div id="ex-sub" class="cf-eq h">$S\\to aaSbb\\mid\\varepsilon$</div>'
         + f'<div id="ex-w" class="cf-words h">{WE}</div>'
         + st.card("ex-rule", "rule", "🔑 <b>הצבה מבטלת משתני עזר</b> ומראה מה השפה.")
         + st.card("ex-trap", "trap", "⚠️ $a^nb^n$ נראית נכונה, אבל $ab\\notin L(G)$."),
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>{Q["questionHtml"]}</div>'
       + st.options("q", opts, notes={"b": "$abab$ לא נגזרת", "c": "$ab$ לא נגזרת", "d": "$ab$ לא נגזרת"}))

recap = Scene("recap", "סיכום", [
    p("לסיכום: רק מילים טרמינליות נכנסות לשפה, וגזירה בלי סוף לא תורמת כלום.", do=show("c1")),
    p("מפענחים משתנה אחר משתנה: $AB$ הוא שרשור, $A\\mid B$ הוא איחוד.",
      say="מפענחים משתנה אחר משתנה: אֵיי גדולה בִּי גדולה הוא שרשור, אֵיי גדולה או בִּי גדולה הוא איחוד.", do=show("c2")),
    p("הצבה מבטלת משתני עזר.", do=show("c3")),
    p("ותמיד בודקים את $\\varepsilon$ ואת שלוש המילים הקצרות. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=grammar("rc", G2, big=True),
   panel=st.card("c1", "rule", "🔑 רק מילים <b>טרמינליות</b>; גזירה בלי סוף: $\\emptyset$")
       + st.card("c2", "rule", "🔑 משתנה אחר משתנה: $AB$ שרשור, $A\\mid B$ איחוד")
       + st.card("c3", "rule", "🔑 הצבה מבטלת משתני עזר")
       + st.card("c4", "trap", "⚠️ בדקו $\\varepsilon$ ושלוש מילים קצרות לפני שבוחרים"))

VIDEO = Video("G01", "cf", "לקרוא דקדוק",
              [title, terms, derive, method, decode, exam, recap],
              bank={"25A-A-Q9": "a"})
