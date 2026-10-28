# -*- coding: utf-8 -*-
"""G08 · מבחן גמר: דקדוקים ואוטומט מחסנית — boss walkthrough video.

No new concept. Four bank questions of the cf course that NO level cites and that are NOT in the G08 boss quiz
(19B-B-Q8 25A-C-Q18 19B-B-Q23 25A-C-Q3 24A-B-Q18 are excluded; vid.py refuses them):
  19B-A-Q21 (cfg)  ·  24X-A-Q17 (pda run)  ·  26A-A-Q7 (pda run)  ·  24A-C-Q16 (classify L(M)).
Every grammar / machine is transcribed from the bank text / figure and checked with lib.CFG / lib.PDA against the key.
Course convention, said every time: accepted = the whole word read, an accepting state AND an empty stack.
"""
from nh import CFG, PDA, words
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_cf import p, grammar, stack, stack_do, run_pda_raster, pda_path, replay, edge_strip, CSS

# ---------------------------------------------------------------- Q1 19B-A-Q21
Q1 = BANK["19B-A-Q21"]
G1 = CFG("S->aSb|aaA|bB;A->a|aA|ε;B->b|bB")
L1 = G1.lang(9)
assert "" not in L1                                          # ε not in L
assert "aa" in L1 and "aaa" in L1                            # both parities occur
G1n = CFG("S->aSb|aaA|aa|bB;A->a|aA;B->b|bB")               # equivalent grammar without an ε rule (bank explanation)
assert G1n.lang(9) == L1 and all("" not in alts for alts in G1n.rules.values())
assert Q1["correctId"] == "d"
SH1 = sorted(L1, key=lambda w: (len(w), w))[:4]
assert SH1 == ["aa", "bb", "aaa", "bbb"] and "b" not in L1

# ---------------------------------------------------------------- Q2 24X-A-Q17 (figure)
Q2 = BANK["24X-A-Q17"]
M2 = PDA([("0", "a", "", "0", "Z"), ("0", "b", "", "0", "Z"), ("0", "b", "", "1", ""),
          ("1", "a", "Z", "1", ""), ("1", "b", "Z", "1", "")], "0", {"1"})
assert M2.lang("ab", 9) == {w for w in words("ab", 9) if len(w) % 2 == 1 and w[len(w) // 2] == "b"}
assert not M2.accepts("abba") and M2.accepts("aabba") and Q2["correctId"] == "b"
assert M2.accepts("abba", require_empty=False)               # the trap: "accepting state only" would accept abba
W2 = "aabba"
P2 = pda_path(M2, W2)
C2 = replay(M2, W2, P2)
assert C2[-1] == ("1", 5, "", W2)
R2 = [("0", 190, 283, 74), ("1", 603, 283, 74)]

# ---------------------------------------------------------------- Q3 26A-A-Q7 (figure)
Q3 = BANK["26A-A-Q7"]
M3 = PDA([("0", "0", "", "0", "A"), ("0", "1", "", "0", "A"), ("0", "", "A", "1", ""), ("1", "", "", "0", ""),
          ("1", "0", "A", "1", ""), ("1", "1", "A", "1", "")], "0", {"0"})
assert M3.lang("01", 8) == set(words("01", 8))              # Σ*
assert M3.accepts("00111") and M3.accepts("1101") and Q3["correctId"] == "a"
CYC = [0, 2, 3]                                              # read a letter + push A, ε pop A to q1, ε back to q0
C3 = replay(M3, "0", CYC)
assert C3[-1] == ("0", 1, "", "0")
assert M3.accepts("")                                        # q0 accepting, stack empty
R3 = [("0", 160, 208, 62), ("1", 545, 208, 56)]

# ---------------------------------------------------------------- Q4 24A-C-Q16 (figure)
Q4 = BANK["24A-C-Q16"]
M4 = PDA([("0", "a", "", "0", "A"), ("0", "", "", "1", ""), ("1", "b", "A", "1", ""), ("1", "", "", "2", ""),
          ("2", "c", "A", "2", "")], "0", {"0", "1", "2"})
import re
def _abc(w):
    m = re.fullmatch("(a*)(b*)(c*)", w)
    return m is not None and len(m.group(1)) == len(m.group(2)) + len(m.group(3))
assert M4.lang("abc", 8) == {w for w in words("abc", 8) if _abc(w)}
assert Q4["correctId"] == "c"
for i in range(5):                                           # {a^i} is an infinite separating set: b^j separates
    for j in range(i + 1, 6):
        assert M4.accepts("a" * j + "b" * j) and not M4.accepts("a" * i + "b" * j)
assert not M4.accepts("a")                                   # all states accepting, still not every word
R4 = [("0", 180, 165, 52), ("1", 470, 165, 52), ("2", 760, 165, 52)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    p("מבחן הגמר של דקדוקים ואוטומט מחסנית. בלי חומר חדש: ארבע שאלות אמיתיות, כמו במבחן."),
    p("לכל שאלה: איך תוקפים אותה, ואיפה המלכודת.", hold=0.4),
], stage=CSS + '<div class="kicker">G08 · דקדוקים ואוטומט מחסנית</div><h1>מבחן גמר: איך פותרים</h1>'
         '<p>ארבע שאלות אמיתיות מהמבחנים על דקדוקים ואוטומט מחסנית, כל אחת עם המלכודת שלה.</p>',
   layout="title")

attack = Scene("attack", "איך תוקפים שאלה", [
    p("לפני הכל, קוראים מה בדיוק שואלים: שייכת, מוכלת ממש, קיים, כל הטענות האחרות.", do=show("a1")),
    p("בדקדוק: מפענחים כל משתנה לבד, ובודקים את $\\varepsilon$ ואת שלוש המילים הקצרות.", do=show("a2")),
    p("באוטומט מחסנית: מסמנים מה כל מצב עושה, מריצים עם מחסנית, ומתקבלת פירושו מצב מקבל **וגם** מחסנית ריקה.",
      do=show("a3")),
    p("ובסיווג: יש דקדוק או אוטומט מחסנית, אז חסרת הקשר. אבל רגולרית או לא, מכריעים רק אחרי שמפענחים.",
      do=show("a4"), hold=0.4),
], stage='<div class="cf-eq" style="font-size:44px">קוראים · מפענחים · מילים קצרות · פוסלים</div>',
   panel=st.card("a1", "plain", "<b>1.</b> מה בדיוק שואלים?")
       + st.card("a2", "rule", "🔑 דקדוק: משתנה אחר משתנה; $\\varepsilon$ ושלוש מילים קצרות")
       + st.card("a3", "rule", "🔑 אוטומט מחסנית: מצב מקבל <b>וגם</b> מחסנית ריקה")
       + st.card("a4", "trap", "⚠️ ח״ה בוודאות; רגולרית רק אחרי פענוח"))

o1 = [(o["id"], o["html"]) for o in Q1["options"]]
q1 = Scene("q1", "שאלה 1: דקדוק", [
    p("שאלה ראשונה. דקדוק עם שלושה משתנים, ושלוש טענות. וגם האפשרות שכל הטענות האחרות לא נכונות."),
    p("מפענחים. $B\\to b\\mid bB$ גוזר $b^+$: לפחות $b$ אחת. $A$ גוזר $a^*$, כולל המילה הריקה.",
      say="מפענחים. בִּי גדולה גוזר בִּי פלוס: לפחות בִּי אחת. אֵיי גדולה גוזר אֵיי כוכבית, כולל המילה הריקה.",
      do=show("g1-rh-B", "g1-rh-A")),
    p("ו-$S$ עוטף $a\\ldots b$, ומסיים ב-$aaA$ או ב-$bB$.",
      say="ואֶס עוטף אֵיי משמאל ובִּי מימין, ומסיים באֵיי אֵיי אֵיי גדולה, או בבִּי בִּי גדולה.",
      do=hide("g1-rh-B", "g1-rh-A") + show("g1-rh-S")),
    p("המילים הקצרות: $aa$, $bb$, $aaa$, $bbb$.", say="המילים הקצרות: אֵיי אֵיי, בִּי בִּי, אֵיי אֵיי אֵיי, בִּי בִּי בִּי.",
      do=hide("g1-rh-S") + show("w1")),
    p("$aa$ באורך זוגי, אז לא כל המילים באורך אי-זוגי. $aaa$ באורך אי-זוגי, אז לא כל המילים באורך זוגי.",
      say="אֵיי אֵיי באורך זוגי, אז לא כל המילים באורך אי-זוגי. אֵיי אֵיי אֵיי באורך אי-זוגי, אז לא כל המילים באורך זוגי.",
      do=show("q1-x-b", "q1-n-b", "q1-x-c", "q1-n-c")),
    p("ועכשיו המלכודת: יש כלל $A\\to\\varepsilon$, אז כל דקדוק שקול חייב כלל אפסילון?",
      say="ועכשיו המלכודת: יש כלל שבו אֵיי גדולה גוזר אפסילון. אז כל דקדוק שקול חייב כלל אפסילון?", do=show("t1")),
    p("לא. $\\varepsilon$ בכלל לא בשפה. מחליפים את $aaA$ ב-$aaA\\mid aa$ ומוחקים את כלל האפסילון. אותה שפה.",
      say="לא. אפסילון בכלל לא בשפה. מוסיפים לאֶס את הכלל אֵיי אֵיי, ומוחקים את כלל האפסילון. אותה שפה.",
      do=show("g1n", "q1-x-a", "q1-n-a")),
    p("שלוש הטענות נפלו, אז התשובה: כל הטענות האחרות לא נכונות.", do=show("q1-ok-d"), hold=0.6),
], stage=grammar("g1", G1, big=True)
         + '<div id="w1" class="cf-words h">' + "".join(f"<span>${w}$</span>" for w in SH1) + '<span>$\\varepsilon\\notin L$</span></div>'
         + '<div id="g1n" class="h">' + grammar("g1b", G1n) + '</div>'
         + st.card("t1", "trap", "⚠️ כלל $\\varepsilon$ בדקדוק ≠ $\\varepsilon$ בשפה: אפשר להיפטר ממנו"),
   panel=f'<div class="qstem"><span class="qid">{Q1["id"]}</span>נתון הדקדוק שמשמאל. איזו טענה נכונה?</div>'
       + st.options("q1", o1, notes={"a": "$\\varepsilon\\notin L$", "b": "$aaa\\in L$", "c": "$aa\\in L$"}))

run2, cf2, left2 = run_pda_raster("x2", M2, W2, P2, "t2", "s2", "l2", {"0": "0", "1": "1"},
                                  lead="נריץ את $aabba$. מתחילים במצב השמאלי, מחסנית ריקה.")
run2[0].do += show("t2-box") + hide("d2")
o2 = [(o["id"], o["html"]) for o in Q2["options"]]
q2 = Scene("q2", "שאלה 2: ריצה", [
    p("שאלה שנייה: אוטומט מחסנית, ושתי מילים: $abba$ ו-$aabba$.",
      say="שאלה שנייה: אוטומט מחסנית, ושתי מילים: אֵיי בִּי בִּי אֵיי, ואֵיי אֵיי בִּי בִּי אֵיי.", do=show("x2-ring-0")),
    p("משמאל: כל אות דוחפת $Z$. המעבר ימינה קורא $b$ ולא נוגע במחסנית. מימין: כל אות שולפת $Z$.",
      say="משמאל: כל אות דוחפת זֶד. המעבר ימינה קורא בִּי ולא נוגע במחסנית. מימין: כל אות שולפת זֶד.",
      do=show("x2-ring-1", "d2a")),
    p("כלומר: אותו מספר אותיות לפני ה-$b$ האמצעית ואחריה. מילים באורך אי-זוגי שהאות האמצעית בהן $b$.",
      say="כלומר: אותו מספר אותיות לפני הבִּי האמצעית ואחריה. מילים באורך אי-זוגי שהאות האמצעית בהן בִּי.",
      do=hide("x2-ring-1") + show("d2b")),
    p("$abba$ באורך זוגי: לא שייכת.", say="אֵיי בִּי בִּי אֵיי באורך זוגי: לא שייכת.", do=show("q2-x-a", "q2-x-c")),
    p("המלכודת: $abba$ **כן** מגיעה למצב המקבל, עם $Z$ אחד במחסנית. מצב מקבל לבד לא מספיק.",
      say="המלכודת: אֵיי בִּי בִּי אֵיי כן מגיעה למצב המקבל, עם זֶד אחת במחסנית. מצב מקבל לבד לא מספיק.",
      do=show("tr2")),
    *run2,
    p("קראנו הכל, מצב מקבל, ומחסנית ריקה: $aabba$ שייכת.", say="קראנו הכל, מצב מקבל, ומחסנית ריקה: אֵיי אֵיי בִּי בִּי אֵיי שייכת.",
      do=show("v2", "q2-x-d")),
    p("התשובה: $abba$ לא שייכת, ו-$aabba$ שייכת.", say="התשובה: אֵיי בִּי בִּי אֵיי לא שייכת, ואֵיי אֵיי בִּי בִּי אֵיי שייכת.",
      do=show("q2-ok-b"), hold=0.6),
], stage=st.raster("x2", "images/exams/24X-A-Q17.png", 520, (782, 516), rings=R2)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:620px"><div class="swap cf-c" style="--swap-h:240px">'
           '<div id="d2"><div id="d2a" class="cf-mid h">משמאל $+1$ · אמצע $b$ · מימין $-1$</div>'
           '<div id="d2b" class="cf-mid h">אורך אי-זוגי, באמצע $b$</div>'
         + st.card("tr2", "trap", "⚠️ $abba$ מגיעה למצב המקבל עם $Z$ במחסנית: <b>לא שייכת</b>") + '</div>'
           f'<div id="t2-box" class="h">{st.tape("t2", W2)}{edge_strip("l2", M2, P2)}'
           '<div id="v2" class="verdict ok h">מצב מקבל + מחסנית ריקה ✓</div></div>'
           '</div></div>' + stack("s2", [c[2] for c in C2]) + '</div>',
   panel=f'<div class="qstem"><span class="qid">{Q2["id"]}</span>נתון האוטומט-מחסנית $M$ שמשמאל. איזו טענה נכונה?</div>'
       + '<div class="cf-sm">' + st.options("q2", o2) + '</div>')

run3, cf3, left3 = run_pda_raster("x3", M3, "0", CYC, "t3", "s3", "l3", {"0": "0", "1": "1"},
                                  lead="נראה את המחזור על אות אחת, $0$.", lead_say="נראה את המחזור על אות אחת, אפס.")
run3[0].do += show("t3-box") + hide("d3")
o3 = [(o["id"], o["html"]) for o in Q3["options"]]
q3 = Scene("q3", "שאלה 3: מחזור קצר", [
    p("שאלה שלישית: $00111$ ו-$1101$.", say="שאלה שלישית: אפס אפס אחת אחת אחת, ואחת אחת אפס אחת.", do=show("x3-ring-0")),
    p("המלכודת כאן: ב-$q_0$ דוחפים, ב-$q_1$ שולפים. נראה כמו חצי ראשון וחצי שני, ואז $00111$ באורך אי-זוגי נדחית.",
      say="המלכודת כאן: בקיו אפס דוחפים, בקיו אחת שולפים. נראה כמו חצי ראשון וחצי שני, ואז אפס אפס אחת אחת אחת, באורך אי-זוגי, נדחית.",
      do=show("tr3")),
    p("אבל יש מסלול קצר יותר. שימו לב לשני מעברי ה-$\\varepsilon$ בין המצבים.",
      say="אבל יש מסלול קצר יותר. שימו לב לשני מעברי האפסילון בין המצבים.", do=show("x3-ring-1")),
    *run3,
    p("חזרנו ל-$q_0$ המקבל, עם מחסנית ריקה, אחרי אות אחת. את המחזור הזה עושים לכל אות.",
      say="חזרנו לקיו אפס המקבל, עם מחסנית ריקה, אחרי אות אחת. את המחזור הזה עושים לכל אות.", do=show("v3")),
    p("ו-$\\varepsilon$ מתקבלת מיד: $q_0$ מקבל והמחסנית ריקה. לכן $L(M)=\\Sigma^*$.",
      say="ואפסילון מתקבלת מיד: קיו אפס מקבל והמחסנית ריקה. לכן השפה היא סיגמא כוכבית, כל המילים.", do=show("d3l")),
    p("שתי המילים שייכות. התשובה: שתיהן בשפה.", do=show("q3-x-b", "q3-x-c", "q3-x-d", "q3-ok-a"), hold=0.6),
], stage=st.raster("x3", "images/exams/26A-A-Q7.png", 640, (640, 288), rings=R3)
         + '<div class="cf-row" style="align-items:center;gap:40px">'
           '<div class="cf-col" style="width:620px"><div class="swap cf-c" style="--swap-h:280px">'
           '<div id="d3">' + st.card("tr3", "trap", "⚠️ דוחפים בחצי הראשון ושולפים בשני? <b>לא בהכרח</b>: חפשו מסלול אחר") + '</div>'
           f'<div id="t3-box" class="h">{st.tape("t3", "0")}{edge_strip("l3", M3, CYC)}'
           '<div id="v3" class="verdict ok h">$q_0$ מקבל + מחסנית ריקה ✓</div>'
           '<div id="d3l" class="cf-eq h">$L(M)=\\Sigma^*$</div></div>'
           '</div></div>' + stack("s3", [c[2] for c in C3]) + '</div>',
   panel=f'<div class="qstem"><span class="qid">{Q3["id"]}</span>נתון האוטומט-מחסנית $M$ שמשמאל, מעל $\\{{0,1\\}}$. איזו טענה נכונה?</div>'
       + '<div class="cf-sm">' + st.options("q3", o3) + '</div>')

o4 = [(o["id"], o["html"]) for o in Q4["options"]]
q4 = Scene("q4", "שאלה 4: סיווג", [
    p("שאלה רביעית: סווגו את $L(M)$. כל שלושת המצבים מקבלים.",
      say="שאלה רביעית: סווגו את השפה של האוטומט. כל שלושת המצבים מקבלים.", do=show("x4-ring-0", "x4-ring-1", "x4-ring-2")),
    p("יש אוטומט מחסנית, אז השפה חסרת הקשר: לא חסרת הקשר נפסלת.", do=show("q4-x-d", "q4-n-d")),
    p("מפענחים: $a$ דוחפת, $b$ ו-$c$ שולפות, והסדר הוא $a$, אחר כך $b$, אחר כך $c$.",
      say="מפענחים: אֵיי דוחפת, בִּי וסִי שולפות, והסדר הוא אֵיי, אחר כך בִּי, אחר כך סִי.",
      do=hide("x4-ring-1", "x4-ring-2") + show("e4a")),
    p("ומתקבלת פירושו מצב מקבל **וגם** מחסנית ריקה. כל המצבים מקבלים, אבל המחסנית חייבת להתרוקן: $a$ לבד לא מתקבלת.",
      say="ומתקבלת פירושו מצב מקבל וגם מחסנית ריקה. כל המצבים מקבלים, אבל המחסנית חייבת להתרוקן: אֵיי לבד לא מתקבלת.",
      do=show("e4b")),
    p("לכן $L(M)=\\{a^nb^mc^k\\mid m+k=n\\}$. אינסופית: סופית נפסלת.",
      say="לכן השפה היא אֵיי בחזקת אֵן, בִּי בחזקת אֶם, סִי בחזקת קֵיי, כך שאֶם ועוד קֵיי שווה אֵן. אינסופית: סופית נפסלת.",
      do=show("e4c", "q4-x-a", "q4-n-a")),
    p("רגולרית? הקבוצה $\\{a^i\\}$ מפרידה: הסיפא $b^j$ מקבלת את $a^j$ ודוחה את $a^i$ לכל $i<j$. קבוצה מפרידה אינסופית: לא רגולרית.",
      say="רגולרית? הקבוצה של כל החזקות של אֵיי מפרידה: הסיפא בִּי בחזקת ג'יי מקבלת את אֵיי בחזקת ג'יי, ודוחה כל חזקה קטנה יותר. קבוצה מפרידה אינסופית: לא רגולרית.",
      do=show("e4d", "q4-x-b", "q4-n-b")),
    p("התשובה: חסרת הקשר וגם לא רגולרית. המלכודת: כל המצבים מקבלים לא אומר שהשפה היא $\\Sigma^*$.",
      do=show("q4-ok-c", "tr4"), hold=0.6),
], stage=st.raster("x4", "images/exams/24A-C-Q16.png", 900, (925, 246), rings=R4)
         + '<div style="display:flex;flex-direction:column;gap:10px;align-items:center">'
           '<div id="e4a" class="cf-mid h">$a:+1$ · $b:-1$ · $c:-1$</div>'
           '<div id="e4b" class="cf-mid h">כל המצבים מקבלים, אבל: $a\\notin L$</div>'
           '<div id="e4c" class="cf-eq h">$L(M)=\\{a^nb^mc^k\\mid m+k=n\\}$</div>'
           '<div id="e4d" class="cf-mid h">$\\{a^i\\}$ קבוצה מפרידה אינסופית, ולכן לא רגולרית</div></div>'
         + st.card("tr4", "trap", "⚠️ כל המצבים מקבלים ≠ $\\Sigma^*$: המחסנית עדיין צריכה להתרוקן"),
   panel=f'<div class="qstem"><span class="qid">{Q4["id"]}</span>נתון האוטומט-מחסנית $M$ שמשמאל, מעל $\\{{a,b,c\\}}$. איזו טענה נכונה?</div>'
       + st.options("q4", o4, notes={"a": "אינסופית", "b": "$\\{a^i\\}$ מפרידה", "d": "יש אוטומט מחסנית"}))

recap = Scene("recap", "סיכום הקורס", [
    p("לסיכום הקורס כולו. דקדוק: משתנה אחר משתנה, שרשור ואיחוד, והצבה.", do=show("c1")),
    p("תמיד בודקים $\\varepsilon$ ושלוש מילים קצרות, ומילה קצרה אחת פוסלת.", do=show("c2")),
    p("אוטומט מחסנית: קרא, שלוף, דחוף. ומתקבלת פירושו מצב מקבל **וגם** מחסנית ריקה.", do=show("c3")),
    p("ודקדוק או אוטומט מחסנית אומרים חסרת הקשר, אבל לא אומרים לא רגולרית. בהצלחה במבחן!", do=show("c4"), hold=0.8),
], stage='<div class="cf-eq" style="font-size:44px">דקדוק ח״ה ואוטומט מחסנית: שקולים</div>',
   panel=st.card("c1", "rule", "🔑 דקדוק: משתנה אחר משתנה; $AB$ שרשור, $A\\mid B$ איחוד; הצבה")
       + st.card("c2", "rule", "🔑 $\\varepsilon$ ושלוש מילים קצרות; מילה אחת פוסלת")
       + st.card("c3", "rule", "🔑 מתקבלת = מצב מקבל <b>וגם</b> מחסנית ריקה")
       + st.card("c4", "trap", "⚠️ ח״ה בוודאות; \"לא רגולרית\" רק אחרי פענוח"))

VIDEO = Video("G08", "cf", "מבחן גמר: דקדוקים ואוטומט מחסנית",
              [title, attack, q1, q2, q3, q4, recap],
              bank={"19B-A-Q21": "d", "24X-A-Q17": "b", "26A-A-Q7": "a", "24A-C-Q16": "c"})
