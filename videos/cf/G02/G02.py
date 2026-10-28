# -*- coding: utf-8 -*-
"""G02 · פענוח דקדוקים: קינון, שרשור, איחוד והצבה — video script.

Source: tools/needhelp/cf/G02.py (lesson + goal). Exam anchor: 24A-C-Q17 (the lesson's i≠k example, not a quiz item).
Not used on purpose: the quiz grammars of G02 (S->aSd|B, S->0M1|ε, S->AB with aAb/bBa, S->A|B with aAb|ab, S->aTa|bTb),
so the lesson's own d^{n+m} and 0^{2n}1^{3n} examples (= quiz Q1, Q2) are replaced by new grammars of the same shape.
Every grammar below is checked with lib.CFG before anything is rendered.
"""
import re
from nh import CFG, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, grammar, leftmost, deriv_lines, tree_svg, grow, grow_end, CSS


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def same(G, alpha, pred, n=9):
    return G.lang(n) == {w for w in words(alpha, n) if pred(w)}


def P_(letters, cond):
    return lambda w: (lambda t: t is not None and cond(*t))(parts(w, letters))


# ---------------------------------------------------------------- grammars (verified)
# nesting: B wraps b..c, S wraps a..cc around it
GN = CFG("S->aScc|B;B->bBc|ε")
assert same(GN, "abc", P_("abc", lambda a, b, c: c == 2 * a + b))
assert GN.lang(9, "B") == {"b" * m + "c" * m for m in range(5)}
DN = leftmost(GN, "abccc")
assert len(DN) == 1 and len(DN[0]) == 4
STEPSN = DN[0]
assert not same(GN, "abc", P_("abc", lambda a, b, c: c == a + b))        # the "one c per letter" guess is wrong
assert GN.derives("abccc") and not P_("abc", lambda a, b, c: c == a + b)("abccc")

# concatenation: two independent parameters
GC = CFG("S->AB;A->aA|ε;B->bBc|ε")
assert same(GC, "abc", P_("abc", lambda a, b, c: b == c))
assert GC.derives("a") and GC.derives("bc") and GC.derives("aabc")
assert not P_("abc", lambda a, b, c: a == b == c)("aabc")

# substitution: M only appears inside S
GS = CFG("S->aM|b;M->Sa")
GS2 = CFG("S->aSa|b")
assert GS.lang(11) == GS2.lang(11) == {"a" * n + "b" + "a" * n for n in range(6)}
SHORTS = sorted(GS.lang(5), key=lambda w: (len(w), w))
assert SHORTS == ["b", "aba", "aabaa"]

# exam 24A-C-Q17
Q = BANK["24A-C-Q17"]
GE = CFG("S->A|B;A->aA|aT;B->Bb|Tb;T->aTb|ε")
assert GE.lang(9, "T") == {"a" * n + "b" * n for n in range(5)}
AB = lambda w: parts(w, "ab")
EXP = {"a": P_("ab", lambda i, k: i != k), "b": P_("ab", lambda i, k: i == k),
       "c": P_("ab", lambda i, k: i > k), "d": P_("ab", lambda i, k: k > i)}
assert [k for k, f in EXP.items() if same(GE, "ab", f)] == [Q["correctId"]] == ["a"]
assert same(CFG("A->aA|aT;T->aTb|ε", start="A"), "ab", P_("ab", lambda i, k: i > k))
assert same(CFG("B->Bb|Tb;T->aTb|ε", start="B"), "ab", P_("ab", lambda i, k: k > i))
assert "" not in GE.lang(9) and EXP["b"]("") and not GE.derives("ab")
assert GE.derives("b") and not EXP["c"]("b")
assert GE.derives("a") and not EXP["d"]("a")
DE = leftmost(GE, "aab")
assert len(DE) == 1
STEPSE = DE[0]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("בסרטון הזה נלמד לפענח דקדוק ולכתוב את השפה שלו בנוסח של קבוצה."),
    p("ארבעה כלים: קינון, שרשור, איחוד והצבה, ובדיקה במילים קצרות."),
    p("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage=CSS + '<div class="kicker">G02 · דקדוקים ואוטומט מחסנית</div><h1>פענוח דקדוקים</h1>'
         '<p>לכתוב את השפה של דקדוק בנוסח קבוצה, כולל שני פרמטרים בלתי תלויים, ולבדוק בעזרת מילים קצרות.</p>',
   layout="title")

tools = Scene("tools", "ארבעה כלים", [
    p("רוב שאלות הדקדוק במבחן הן: פענחו את הדקדוק. כלומר, כתבו את השפה שלו בנוסח של קבוצה."),
    p("כלי ראשון, **קינון**: כלל כמו $S\\to aSc$ עוטף את מה שבפנים, $a$ משמאל ו-$c$ מימין.",
      say="כלי ראשון, קינון: כלל כמו אֶס גוזר אֵיי אֶס סִי עוטף את מה שבפנים, אֵיי משמאל וסִי מימין.", do=show("k1")),
    p("**המונה החיצוני עוטף את הפנימי**: מספר ה-$c$ מימין סופר את שניהם.", do=show("k1b")),
    p("כלי שני, **שרשור**: $S\\to AB$. קודם מה ש-$A$ גוזר, ואחריו מה ש-$B$ גוזר.",
      say="כלי שני, שרשור: אֶס גוזר אֵיי גדולה בִּי גדולה. קודם מה שאֵיי גדולה גוזר, ואחריו מה שבִּי גדולה גוזר.",
      do=show("k2")),
    p("והפרמטרים של $A$ ושל $B$ **בלתי תלויים**: כל אחד סופר לבד.", do=show("k2b")),
    p("כלי שלישי, **איחוד**: $S\\to A\\mid B$. או מה ש-$A$ גוזר, או מה ש-$B$ גוזר.",
      say="כלי שלישי, איחוד: אֶס גוזר אֵיי גדולה או בִּי גדולה. או מה שאֵיי גדולה גוזר, או מה שבִּי גדולה גוזר.",
      do=show("k3")),
    p("וכלי רביעי, **הצבה**: משתנה עזר שמופיע רק במקום אחד, מציבים אותו ומקבלים כלל פשוט.", do=show("k4"), hold=0.4),
], stage='<div class="cf-eq">$S\\to aSc$ &nbsp;עוטף:&nbsp; $a\\,(\\ldots)\\,c$</div>'
         '<div class="cf-eq">$S\\to AB$ &nbsp;שרשור:&nbsp; $(A)(B)$</div>'
         '<div class="cf-eq">$S\\to A\\mid B$ &nbsp;איחוד:&nbsp; $(A)\\cup(B)$</div>',
   panel=st.card("k1", "plain", "<b>קינון</b>: $S\\to aSc$ עוטף את מה שבפנים")
       + st.card("k1b", "rule", "🔑 המונה החיצוני עוטף את הפנימי")
       + st.card("k2", "plain", "<b>שרשור</b>: $S\\to AB$")
       + st.card("k2b", "rule", "🔑 בשרשור הפרמטרים <b>בלתי תלויים</b>")
       + st.card("k3", "plain", "<b>איחוד</b>: $S\\to A\\mid B$")
       + st.card("k4", "plain", "<b>הצבה</b>: מבטלת משתני עזר"))

nest = Scene("nest", "דוגמה 1: קינון", [
    p("דוגמה לקינון. $B\\to bBc\\mid\\varepsilon$ עוטף $b$ משמאל ו-$c$ מימין: $B$ גוזר $b^mc^m$.",
      do=show("gn-rh-B", "nb")),
    p("ו-$S\\to aScc\\mid B$ עוטף את כל זה ב-$a$ משמאל ו**שתי** $c$ מימין.",
      say="ואֶס, שגוזר אֵיי אֶס סִי סִי או בִּי גדולה, עוטף את כל זה באֵיי משמאל ובשתי סִי מימין.",
      do=hide("gn-rh-B") + show("gn-rh-S", "ns")),
    p("נראה את זה על המילה $abccc$. מתחילים ב-$S$.", do=hide("gn-rh-S") + show("tn-x-1", "nbox")),
    p("$S\\to aScc$: $a$ אחת משמאל ושתי $c$ מימין.",
      say="אֶס גוזר אֵיי אֶס סִי סִי: אֵיי אחת משמאל ושתי סִי מימין.", do=grow("tn", "dn", STEPSN, 1, gram="gn")),
    p("עכשיו $S\\to B$: יורדים לשכבה הפנימית.", say="עכשיו אֶס גוזר בִּי גדולה: יורדים לשכבה הפנימית.",
      do=grow("tn", "dn", STEPSN, 2, gram="gn")),
    p("$B\\to bBc$: $b$ משמאל ו-$c$ מימין.", say="בִּי גדולה גוזר בִּי, בִּי גדולה, סִי: בִּי משמאל וסִי מימין.",
      do=grow("tn", "dn", STEPSN, 3, gram="gn")),
    p("ו-$B\\to\\varepsilon$ מסיים. קיבלנו $abccc$: שלוש $c$, שתיים בשביל ה-$a$ ואחת בשביל ה-$b$.",
      say="ובִּי גדולה גוזר אפסילון מסיים. קיבלנו אֵיי בִּי סִי סִי סִי: שלוש סִי, שתיים בשביל האֵיי ואחת בשביל הבִּי.",
      do=grow("tn", "dn", STEPSN, 4, gram="gn")),
    p("ולכן $L=\\{a^nb^mc^{2n+m}\\mid n,m\\ge0\\}$. המונה החיצוני עוטף את הפנימי.",
      say="ולכן השפה היא אֵיי בחזקת אֵן, בִּי בחזקת אֶם, סִי בחזקת שתיים אֵן ועוד אֶם.",
      do=grow_end("tn", STEPSN, gram="gn") + show("nl")),
    p("שימו לב: מי שכותב $c^{n+m}$ שוכח שכל $a$ מקבלת **שתי** $c$. המילה $abccc$ מפילה אותו.",
      say="שימו לב: מי שכותב סִי בחזקת אֵן ועוד אֶם שוכח שכל אֵיי מקבלת שתי סִי. המילה אֵיי בִּי סִי סִי סִי מפילה אותו.",
      do=show("ntrap"), hold=0.5),
], stage='<div class="cf-row" style="gap:40px">'
         '<div class="cf-col"><div id="nb" class="cf-mid h">$B$ גוזר $b^mc^m$</div>'
         '<div id="ns" class="cf-mid h">$S$ עוטף: $a^n(\\ldots)c^{2n}$</div></div></div>'
         '<div id="nbox" class="cf-row h" style="align-items:flex-start;gap:60px">'
         + deriv_lines("dn", GN, STEPSN) + tree_svg("tn", GN, STEPSN, w=440, dy=70, scale=1.15) + '</div>'
         '<div id="nl" class="cf-eq h">$L(G)=\\{a^nb^mc^{2n+m}\\mid n,m\\ge0\\}$</div>',
   panel=grammar("gn", GN)
       + st.card("ntrap", "trap", "⚠️ כל $a$ עוטפת <b>שתי</b> $c$: לא $c^{n+m}$ אלא $c^{2n+m}$."))

concat = Scene("concat", "דוגמה 2: שרשור והצבה", [
    p("דוגמה לשרשור: $S\\to AB$, עם $A\\to aA\\mid\\varepsilon$ ו-$B\\to bBc\\mid\\varepsilon$.",
      say="דוגמה לשרשור: אֶס גוזר אֵיי גדולה בִּי גדולה. אֵיי גדולה גוזר כמה אֵיי שרוצים, ובִּי גדולה עוטף בִּי וסִי."),
    p("$A$ גוזר $a^k$, כל מספר של $a$. ו-$B$ גוזר $b^mc^m$.", do=show("gc-rh-A", "gc-rh-B", "cc1")),
    p("השרשור: $a^kb^mc^m$, וה-$k$ וה-$m$ **בלתי תלויים**.",
      say="השרשור: אֵיי בחזקת קֵיי, בִּי בחזקת אֶם, סִי בחזקת אֶם. והקֵיי והאֶם בלתי תלויים.",
      do=hide("gc-rh-A", "gc-rh-B") + show("cc2")),
    p("לכן $a$ לבד בשפה, וגם $aabc$. מי שכותב $a^nb^nc^n$ קושר פרמטרים שהדקדוק לא קושר.",
      say="לכן אֵיי לבד בשפה, וגם אֵיי אֵיי בִּי סִי. מי שכותב אֵיי בחזקת אֵן, בִּי בחזקת אֵן, סִי בחזקת אֵן, קושר פרמטרים שהדקדוק לא קושר.",
      do=show("cc3")),
    p("ועכשיו הצבה. $S\\to aM\\mid b$ ו-$M\\to Sa$.", say="ועכשיו הצבה. אֶס גוזר אֵיי אֶם, או בִּי. ואֶם גוזר אֶס אֵיי.",
      do=hide("cbox1") + show("cbox2")),
    p("$M$ מופיע רק בתוך $S$, אז מציבים: $S\\to aSa\\mid b$.",
      say="אֶם מופיע רק בתוך אֶס, אז מציבים: אֶס גוזר אֵיי אֶס אֵיי, או בִּי.", do=show("gs-rh-M", "cs1")),
    p("עכשיו רואים: אותו מספר $a$ משני צדי ה-$b$. המילים הקצרות: $b$, $aba$, $aabaa$.",
      say="עכשיו רואים: אותו מספר אֵיי משני צדי הבִּי. המילים הקצרות: בִּי, אֵיי בִּי אֵיי, ואֵיי אֵיי בִּי אֵיי אֵיי.",
      do=hide("gs-rh-M") + show("cs2")),
    p("כלומר $L=\\{a^nba^n\\mid n\\ge0\\}$.", say="כלומר השפה היא אֵיי בחזקת אֵן, בִּי, אֵיי בחזקת אֵן.",
      do=show("cs3"), hold=0.5),
], stage='<div class="swap cf-c" style="--swap-h:640px">'
         '<div id="cbox1">' + grammar("gc", GC, big=True)
         + '<div id="cc1" class="cf-mid h">$A$ גוזר $a^k$, &nbsp; $B$ גוזר $b^mc^m$</div>'
         + '<div id="cc2" class="cf-eq h">$L(G)=\\{a^kb^mc^m\\mid k,m\\ge0\\}$</div>'
         + '<div id="cc3" class="cf-words h"><span>$a$ ✓</span><span>$aabc$ ✓</span></div></div>'
         '<div id="cbox2" class="h">' + grammar("gs", GS, big=True)
         + '<div id="cs1" class="cf-eq h">$S\\to aSa\\mid b$</div>'
         + '<div id="cs2" class="cf-words h">' + "".join(f"<span>${w}$</span>" for w in SHORTS) + '</div>'
         + '<div id="cs3" class="cf-eq h">$L(G)=\\{a^nba^n\\mid n\\ge0\\}$</div></div>'
         '</div>',
   panel=st.card("cr1", "rule", "🔑 שרשור $S\\to AB$: פרמטר נפרד לכל משתנה").replace(' h"', '"')
       + st.card("cr2", "rule", "🔑 הצבה: משתנה עזר שמופיע במקום אחד מציבים, ורואים את השפה").replace(' h"', '"'))

opts = [(o["id"], o["html"]) for o in Q["options"]]
exam = Scene("exam", "שאלה ממבחן", [
    p("שאלה ממבחן. ארבעה משתנים. מפענחים מלמטה למעלה, משתנה אחר משתנה."),
    p("$T\\to aTb\\mid\\varepsilon$: זה $a^nb^n$, כולל המילה הריקה.", do=show("ex-rh-T", "e1")),
    p("$A\\to aA\\mid aT$: מוסיף לפחות $a$ אחת משמאל, ואז $T$. כלומר $a^ib^k$ עם $i>k$.",
      say="אֵיי גדולה גוזר אֵיי אֵיי גדולה, או אֵיי טִי: מוסיף לפחות אֵיי אחת משמאל, ואז טִי. כלומר יותר אֵיי מבִּי.",
      do=hide("ex-rh-T") + show("ex-rh-A", "e2")),
    p("$B\\to Bb\\mid Tb$: מוסיף לפחות $b$ אחת מימין. כלומר $k>i$.",
      say="בִּי גדולה גוזר בִּי גדולה בִּי, או טִי בִּי: מוסיף לפחות בִּי אחת מימין. כלומר יותר בִּי מאֵיי.",
      do=hide("ex-rh-A") + show("ex-rh-B", "e3")),
    p("ו-$S\\to A\\mid B$ הוא איחוד: יותר $a$, **או** יותר $b$. ביחד: $i\\ne k$.",
      say="ואֶס, שגוזר אֵיי גדולה או בִּי גדולה, הוא איחוד: יותר אֵיי, או יותר בִּי. ביחד: אַיי שונה מקֵיי.",
      do=hide("ex-rh-B") + show("ex-rh-S", "e4")),
    p("למשל $aab$: $S\\Rightarrow A\\Rightarrow aT\\Rightarrow aaTb\\Rightarrow aab$.",
      say="למשל אֵיי אֵיי בִּי: אֶס, אֵיי גדולה, אֵיי טִי, אֵיי אֵיי טִי בִּי, אֵיי אֵיי בִּי.", do=hide("ex-rh-S", "e-dec") + show("e-tr")),
    p("עכשיו המלכודת: $i>k$ ו-$k>i$ הן כל אחת **חצי** מהשפה.", do=show("ex-trap")),
    p("$b$ נגזרת דרך $B$, ולכן $i>k$ נופלת. ו-$a$ נגזרת דרך $A$, ולכן $k>i$ נופלת.",
      say="בִּי נגזרת דרך בִּי גדולה, ולכן יותר אֵיי נופלת. ואֵיי נגזרת דרך אֵיי גדולה, ולכן יותר בִּי נופלת.",
      do=show("q-x-c", "q-n-c", "q-x-d", "q-n-d")),
    p("ו-$i=k$? $T$ לבד היה גוזר אותה, אבל $S$ חייב לעבור דרך $A$ או $B$, שתמיד מוסיפים אות. $\\varepsilon$ לא בשפה.",
      say="ואַיי שווה קֵיי? טִי לבד היה גוזר אותה, אבל אֶס חייב לעבור דרך אֵיי גדולה או בִּי גדולה, שתמיד מוסיפים אות. אפסילון לא בשפה.",
      do=show("q-x-b", "q-n-b")),
    p("התשובה: $i\\ne k$. **תמיד בדקו את $\\varepsilon$** ואת המילים באורך אחת.",
      say="התשובה: אַיי שונה מקֵיי. תמיד בדקו את אפסילון ואת המילים באורך אחת.", do=show("q-ok-a"), hold=0.6),
], stage=grammar("ex", GE, big=True)
         + '<div class="swap cf-c" style="--swap-h:330px">'
           '<div id="e-dec"><div id="e1" class="cf-mid h">$T$ גוזר $a^nb^n$</div>'
           '<div id="e2" class="cf-mid h">$A$ גוזר $a^ib^k$, $i>k$</div>'
           '<div id="e3" class="cf-mid h">$B$ גוזר $a^ib^k$, $k>i$</div>'
           '<div id="e4" class="cf-eq h">$L(G)=\\{a^ib^k\\mid i\\ne k\\}$</div></div>'
           '<div id="e-tr" class="h"><div id="e5" class="cf-mid cf-ltr">$S\\Rightarrow A\\Rightarrow aT\\Rightarrow aaTb\\Rightarrow aab$</div>'
         + st.card("ex-trap", "trap", "⚠️ $i>k$ ו-$k>i$ הן <b>חצי</b> מהשפה; $i=k$ נופלת על $\\varepsilon$.") + '</div></div>',
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>נתון הדקדוק שמשמאל, מעל $\\{{a,b\\}}$. תהי $L$ השפה שהוא יוצר. איזו טענה נכונה?</div>'
       + '<div class="cf-sm">' + st.options("q", opts, notes={"b": "$\\varepsilon\\notin L$", "c": "$b\\in L$", "d": "$a\\in L$"}) + '</div>')

recap = Scene("recap", "סיכום", [
    p("לסיכום: בקינון, המונה החיצוני עוטף את הפנימי.", do=show("c1")),
    p("בשרשור $AB$ יש פרמטר נפרד לכל משתנה, ובאיחוד $A\\mid B$ לוקחים את שניהם.",
      say="בשרשור יש פרמטר נפרד לכל משתנה, ובאיחוד לוקחים את שניהם.", do=show("c2")),
    p("הצבה מבטלת משתני עזר.", do=show("c3")),
    p("ותמיד בודקים את $\\varepsilon$ ומילים באורך אחת עד שלוש. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=grammar("rc", GE, big=True),
   panel=st.card("c1", "rule", "🔑 קינון: המונה החיצוני עוטף את הפנימי")
       + st.card("c2", "rule", "🔑 $AB$: פרמטרים בלתי תלויים; $A\\mid B$: איחוד")
       + st.card("c3", "rule", "🔑 הצבה מבטלת משתני עזר")
       + st.card("c4", "trap", "⚠️ בדקו $\\varepsilon$ ומילים באורך $1$ עד $3$"))

VIDEO = Video("G02", "cf", "פענוח דקדוקים",
              [title, tools, nest, concat, exam, recap],
              bank={"24A-C-Q17": "a"})
