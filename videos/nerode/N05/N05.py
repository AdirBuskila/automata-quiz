# -*- coding: utf-8 -*-
"""N05 · משפחת x ו-y — video script (build: tools/video/vid.py N05).

Source: tools/needhelp/nerode/N05.py (lesson + goal). Exam anchors: 26A-A-Q13 (1Σ*+Σ*0+ε) and 24A-C-Q10
((ΣΣΣ)*+(ΣΣΣΣ)*), both cited by the lesson, neither in the quiz; plus 24X-A-Q14 (01*, uncited). Not used on purpose: the quiz's languages (Σ*111,
#0≠#1, palindromes, #0≤#1, 1Σ*1). New worked examples: 0Σ*, |w| mod 3 ∈ {0,1}, |w| mod 4 ∈ {0,1}.
The buckets on screen are lib.classes() of all words up to length 4 (suffixes up to length 8).
"""
from nh import words, classes, rank_stable, separable  # noqa
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, buckets, wd


def sides(pred, plen=4):
    """(classes inside L, classes outside L), each class shortest-first"""
    cl = [sorted(c, key=lambda w: (len(w), w)) for c in classes(pred, "01", plen, 8)]
    cl.sort(key=lambda c: (len(c[0]), c[0]))
    return [c for c in cl if pred(c[0])], [c for c in cl if not pred(c[0])]


def answer(pred):
    ins, outs = sides(pred)
    t = {"in": len(ins) == 1, "out": len(outs) == 1}
    return "in" if t["in"] and not t["out"] else "out" if t["out"] and not t["in"] else "none" if not any(t.values()) else "both"


def groups(pred, k=4):
    ins, outs = sides(pred)
    return ([("בשפה", c[:k], True) for c in ins] + [("מחוץ לשפה", c[:k], False) for c in outs])


# worked examples
S0 = lambda w: w.startswith("0")
M3 = lambda w: len(w) % 3 in (0, 1)
M4 = lambda w: len(w) % 4 in (0, 1)
assert answer(S0) == "in" and answer(M3) == "out" and answer(M4) == "none"
assert separable(S0, "", "1", "01") == "0"
assert separable(M3, "0", "000", "01") == "00" or separable(M3, "0", "000", "01") is not None
assert separable(M4, "", "0", "01") == "0" and separable(M4, "00", "000", "01") == "0"
# the always-false option: ε separates in from out, for every language here
for p in (S0, M3, M4):
    assert all(separable(p, x, y, "01") == "" for x in words("01", 3) for y in words("01", 3) if p(x) and not p(y))

# exam 26A-A-Q13: 1Σ* + Σ*0 + ε  -> the outside is 0Σ*1, one class
QA = BANK["26A-A-Q13"]
LA = lambda w: w == "" or w.startswith("1") or w.endswith("0")
assert answer(LA) == "out" and QA["correctId"] == "c"
assert all((not LA(w)) == (len(w) >= 2 and w[0] == "0" and w[-1] == "1") for w in words("01", 8))
assert separable(LA, "1", "0", "01") == "1" and not LA("01") and LA("11")
assert len(sides(LA)[0]) == 3

# exam 24A-C-Q10: lengths divisible by 3 or by 4 -> neither side is one class
QB = BANK["24A-C-Q10"]
LB = lambda w: len(w) % 3 == 0 or len(w) % 4 == 0
assert QB["correctId"] == "d"
assert rank_stable(LB, "01", 13, (12, 13, 14)) == 12
assert separable(LB, "000", "0000", "01") is not None and not LB("0" * 7) and LB("0" * 6)
assert separable(LB, "0", "00", "01") == "0" and LB("000") and not LB("00")
INB = [r for r in range(12) if r % 3 == 0 or r % 4 == 0]
assert INB == [0, 3, 4, 6, 8, 9]


def xy_opts(order):
    txt = {"in-out": "אם $y\\in L$ ו-$x\\notin L$, אז לא ניתנות להפרדה",
           "in": "אם $x,y\\in L$, אז לא ניתנות להפרדה",
           "out": "אם $x,y\\notin L$, אז לא ניתנות להפרדה",
           "none": "כל הטענות האחרות לא נכונות"}
    return [(oid, txt[k]) for oid, k in order]


# option ids per exam (matched by content from questions.json)
def kinds(Q):
    out = []
    for o in Q["options"]:
        v = o["value"]
        k = ("none" if "כל" in v else "in-out" if "\\notin" in v and "\\in L" in v.replace("\\notin", "")
             else "out" if "\\notin" in v else "in")
        out.append((o["id"], k))
    return out


KA, KB = kinds(QA), kinds(QB)
assert dict(KA)[QA["correctId"]] == "out" and dict(KB)[QB["correctId"]] == "none"
assert sorted(k for _, k in KA) == sorted(k for _, k in KB) == ["in", "in-out", "none", "out"]
IDA = {k: i for i, k in KA}
IDB = {k: i for i, k in KB}

title = Scene("title", "", [
    N("תשע שאלות בבנק פותחות באותו נוסח: ״יהיו $x$ ו-$y$ שתי מילים שונות. איזו טענה נכונה?״",
      say="תשע שאלות בבנק פותחות באותו נוסח: יהיו אקס ווואי שתי מילים שונות. איזו טענה נכונה?"),
    N("בסרטון הזה נלמד לפתור אותן בשתי שורות, בעזרת **מחלקות השקילות**.", hold=0.4),
], stage=CSS + '<div class="kicker">N05 · נרוד, Rank וקבוצות מפרידות</div><h1>משפחת x ו-y: מתי שתי מילים לא ניתנות להפרדה</h1>'
         '<p>לפתור בשתי שורות את שאלות ״יהיו x ו-y״: לזהות אם כל מילות השפה (או כל המילים מחוץ לה) באותה מחלקה.</p>',
   layout="title")

family = Scene("family", "ארבע האפשרויות", [
    N("ארבע האפשרויות תמיד אותן אפשרויות. שלוש מהן אומרות ״$x,y$ לא ניתנות להפרדה״, בתנאים שונים.",
      say="ארבע האפשרויות תמיד אותן אפשרויות. שלוש מהן אומרות: אקס ווואי לא ניתנות להפרדה, בתנאים שונים.", do=show("f-opts")),
    N("הראשונה: מילה בשפה ומילה מחוץ לה. היא **תמיד שגויה**: הסיפא $\\varepsilon$ מפרידה ביניהן.",
      say="הראשונה: מילה בשפה ומילה מחוץ לה. היא תמיד שגויה: הסיפא אפסילון מפרידה ביניהן.", do=show("f-x-a", "f-n-a", "f-r1")),
    N("השנייה, ״$x,y\\in L$״: נכונה אם ורק אם **כל המילים של $L$ במחלקה אחת**. באס״ד המינימלי: מצב מקבל יחיד.",
      say="השנייה, אקס ווואי בשפה: נכונה אם ורק אם כל המילים של אל במחלקה אחת. באסאד המינימלי: מצב מקבל יחיד.", do=show("f-r2")),
    N("השלישית, ״$x,y\\notin L$״: נכונה אם ורק אם **כל המילים מחוץ ל-$L$ במחלקה אחת**: מצב דוחה יחיד.",
      say="השלישית, אקס ווואי מחוץ לשפה: נכונה אם ורק אם כל המילים מחוץ לאל במחלקה אחת: מצב דוחה יחיד.", do=show("f-r3")),
    N("ואם אף צד הוא לא מחלקה אחת, התשובה היא ״כל הטענות האחרות לא נכונות״.", do=show("f-r4")),
    N("אז כל מה שצריך: **לספור מחלקות בכל צד**. בואו נראה שלוש שפות, אחת לכל תשובה.", hold=0.5),
], stage=st.options("f", xy_opts([("a", "in-out"), ("b", "in"), ("c", "out"), ("d", "none")]),
                    notes={"a": "$z=\\varepsilon$"}).replace('class="opts"', 'class="opts h"').replace('id="f-opts"', 'id="f-opts" style="width:900px"'),
   panel=st.card("f-r1", "rule", "🔑 בשפה מול מחוץ: <b>תמיד</b> ניתנות להפרדה, עם $z=\\varepsilon$")
       + st.card("f-r2", "rule", "🔑 ״$x,y\\in L$״ נכונה אם ורק אם כל $L$ במחלקה <b>אחת</b>")
       + st.card("f-r3", "rule", "🔑 ״$x,y\\notin L$״ נכונה אם ורק אם כל המשלים במחלקה <b>אחת</b>")
       + st.card("f-r4", "rule", "🔑 אם אף צד אינו מחלקה אחת, אז ״כל הטענות האחרות״"))


def bucket_scene(key, label, pred, lang_html, lines, verdict_html, pfx):
    G = groups(pred)
    ids = [f"{pfx}-b-{k}" for k in range(len(G))] + [f"{pfx}-w-{k}-{n}" for k, (_, ws_, _) in enumerate(G) for n in range(len(ws_))]
    ph = []
    for i, (sub, say, extra) in enumerate(lines):
        ph.append(N(sub, say=say, do=(show(pfx, *ids) if i == 1 else []) + extra, hold=0.5 if i == len(lines) - 1 else 0))
    return Scene(key, label, ph,
                 stage=f'<div class="nr-big">{lang_html}</div>' + buckets(pfx, G).replace('class="nr-bk"', 'class="nr-bk h"', 1),
                 panel=verdict_html)


ex1 = bucket_scene("ex1", "דוגמה 1: מצב מקבל יחיד", S0, "$L=0\\Sigma^*$: מתחילה ב-$0$", [
    ("ראשונה: $L$ = המילים שמתחילות ב-$0$.", "ראשונה: אל שווה המילים שמתחילות באפס.", []),
    ("נמיין מילים קצרות למחלקות. ירוק: בשפה. אפור: מחוץ לשפה.", None, []),
    ("בשפה יש מחלקה **אחת**: אחרי $0$ בהתחלה, כל המשך נשאר בשפה. לכן ״$x,y\\in L$״ נכונה.",
     "בשפה יש מחלקה אחת: אחרי אפס בהתחלה, כל המשך נשאר בשפה. לכן הטענה על אקס ווואי בשפה נכונה.", show("v1-in")),
    ("ובחוץ שתי מחלקות: $\\varepsilon$ ו-$1$. הסיפא $0$ מפרידה ביניהן: $0\\in L$, $10\\notin L$.",
     "ובחוץ שתי מחלקות: אפסילון ואחת. הסיפא אפס מפרידה ביניהן: אפס בשפה, ואחת אפס לא.", show("v1-out")),
], st.card("v1-in", "rule", "בשפה: מחלקה <b>אחת</b>, לכן ״$x,y\\in L$״ ✓")
   + st.card("v1-out", "plain", "מחוץ: $\\varepsilon$ ו-$1$ נבדלות בסיפא $z=0$, לכן ״$x,y\\notin L$״ ✗"), "c1")

ex2 = bucket_scene("ex2", "דוגמה 2: מצב דוחה יחיד", M3, "$L$: $|w|\\bmod3\\in\\{0,1\\}$", [
    ("שנייה: המילים שהאורך שלהן מודולו שלוש הוא אפס או אחת.", None, []),
    ("כאן המחלקות הן השאריות: אפס, אחת ושתיים.", None, []),
    ("בשפה שתי מחלקות, שארית אפס ושארית אחת. הסיפא $00$ מפרידה ביניהן.",
     "בשפה שתי מחלקות, שארית אפס ושארית אחת. הסיפא אפס אפס מפרידה ביניהן.", show("v2-in")),
    ("ובחוץ רק שארית שתיים: מחלקה **אחת**. לכן ״$x,y\\notin L$״ נכונה.",
     "ובחוץ רק שארית שתיים: מחלקה אחת. לכן הטענה על אקס ווואי מחוץ לשפה נכונה.", show("v2-out")),
], st.card("v2-in", "plain", "בשפה: שתי מחלקות, לכן ״$x,y\\in L$״ ✗")
   + st.card("v2-out", "rule", "מחוץ: מחלקה <b>אחת</b>, לכן ״$x,y\\notin L$״ ✓"), "c2")

ex3 = bucket_scene("ex3", "דוגמה 3: אף צד", M4, "$L$: $|w|\\bmod4\\in\\{0,1\\}$", [
    ("ושלישית: אורך מודולו ארבע הוא אפס או אחת.", None, []),
    ("ארבע שאריות, ארבע מחלקות: שתיים בפנים, שתיים בחוץ.", None, []),
    ("בפנים: $\\varepsilon$ ו-$0$ נבדלות בסיפא $0$. בחוץ: $00$ ו-$000$ נבדלות גם הן בסיפא $0$.",
     "בפנים: אפסילון ואפס נבדלות בסיפא אפס. בחוץ: אפס אפס ושלושה אפסים נבדלות גם הן בסיפא אפס.", show("v3-a")),
    ("אף צד הוא לא מחלקה אחת. התשובה: ״כל הטענות האחרות לא נכונות״.", None, show("v3-b")),
], st.card("v3-a", "plain", "בשפה: $2$ מחלקות. מחוץ: $2$ מחלקות.")
   + st.card("v3-b", "rule", "אף צד אינו מחלקה אחת, לכן ״כל הטענות האחרות״ ✓"), "c3")

GA = groups(LA)
examA = Scene("examA", "שאלה ממבחן", [
    N("שאלה ממבחן: $L=1\\Sigma^*+\\Sigma^*0+\\varepsilon$. יהיו $x\\ne y$. איזו טענה נכונה?",
      say="שאלה ממבחן: אל שווה אחת סיגמא כוכבית, או סיגמא כוכבית אפס, או אפסילון. יהיו אקס שונה מוואי. איזו טענה נכונה?"),
    N("הטענה על מילה בשפה ומילה מחוצה לה: שגויה תמיד. $\\varepsilon$ מפרידה.", say="הטענה על מילה בשפה ומילה מחוצה לה: שגויה תמיד. אפסילון מפרידה.",
      do=show(f"q-x-{IDA['in-out']}")),
    N("מה **מחוץ** לשפה? מילה שלא מתחילה ב-$1$, לא נגמרת ב-$0$, ולא ריקה. כלומר מתחילה ב-$0$ ונגמרת ב-$1$.",
      say="מה מחוץ לשפה? מילה שלא מתחילה באחת, לא נגמרת באפס, ולא ריקה. כלומר מתחילה באפס ונגמרת באחת.",
      do=show("a-bk", *[f"a-b-{k}" for k in range(len(GA))], *[f"a-w-{k}-{n}" for k, (_, w_, _) in enumerate(GA) for n in range(len(w_))])),
    N("ולכולן אותו גורל: $xz\\in L$ בדיוק כשהסיפא נגמרת ב-$0$. מחלקה **אחת**.",
      say="ולכולן אותו גורל: אקס זד בשפה בדיוק כשהסיפא נגמרת באפס. מחלקה אחת.", do=show("a-out")),
    N("ובשפה עצמה שלוש מחלקות. למשל $1$ ו-$0$: הסיפא $1$ מפרידה, כי $11\\in L$ ו-$01\\notin L$.",
      say="ובשפה עצמה שלוש מחלקות. למשל אחת ואפס: הסיפא אחת מפרידה, כי אחת אחת בשפה, ואפס אחת לא.",
      do=show(f"q-x-{IDA['in']}", "a-in")),
    N("המלכודת: ״$x,y\\in L$״, כי השפה נראית ״פשוטה״. אבל היא איחוד של שלושה דברים שונים.",
      say="המלכודת: הטענה על אקס ווואי בשפה, כי השפה נראית פשוטה. אבל היא איחוד של שלושה דברים שונים."),
    N("התשובה: ״אם $x,y\\notin L$, אז לא ניתנות להפרדה״. והתשובה ״כל האחרות״ נופלת, כי יש טענה נכונה.",
      say="התשובה: אקס ווואי מחוץ לשפה, לא ניתנות להפרדה. והתשובה כל האחרות נופלת, כי יש טענה נכונה.",
      do=show(f"q-ok-{IDA['out']}", f"q-x-{IDA['none']}"), hold=0.6),
], stage=buckets("a", GA).replace('class="nr-bk"', 'class="nr-bk h"', 1).replace('id="a"', 'id="a-bk"', 1)
         + st.card("a-out", "rule", "מחוץ ל-$L$ = $0\\Sigma^*1$: מחלקה <b>אחת</b>")
         + st.card("a-in", "plain", "בשפה: $3$ מחלקות. למשל $1$ מול $0$, עם $z=1$"),
   panel=f'<div class="qstem"><span class="qid">{QA["id"]}</span>$L=1\\Sigma^*+\\Sigma^*0+\\varepsilon$, $x\\ne y$. איזו טענה נכונה?</div>'
       + st.options("q", xy_opts(KA)))

RES = ('<div class="nr-chips" style="flex-wrap:wrap;max-width:980px;justify-content:center">'
       + "".join(f'<span class="nr-chip" style="font-size:46px;min-width:64px;text-align:center;border-width:3px;border-color:{"var(--ok)" if r in INB else "var(--line)"};background:{"rgba(52,211,153,.18)" if r in INB else "var(--card)"}">{r}</span>' for r in range(12))
       + "</div>")
examB = Scene("examB", "עוד שאלה ממבחן", [
    N("ועוד אחת: $L=(\\Sigma\\Sigma\\Sigma)^*+(\\Sigma\\Sigma\\Sigma\\Sigma)^*$. אורך שמתחלק בשלוש **או** בארבע.",
      say="ועוד אחת: מילים שהאורך שלהן מתחלק בשלוש או בארבע."),
    N("כאן זוכרים את האורך מודולו שתים עשרה: שתים עשרה מחלקות. בירוק, השאריות שבשפה.", do=show("b-res")),
    N("בשפה: $000$ ו-$0000$. הסיפא $000$ נותנת אורך שש, בשפה, ואורך שבע, לא בשפה.",
      say="בשפה: שלושה אפסים וארבעה אפסים. הסיפא של שלושה אפסים נותנת אורך שש, בשפה, ואורך שבע, לא בשפה.",
      do=show(f"r-x-{IDB['in']}")),
    N("מחוץ לשפה: $0$ ו-$00$. הסיפא $0$ נותנת אורך שתיים, לא בשפה, ואורך שלוש, בשפה.",
      say="מחוץ לשפה: אפס ואפס אפס. הסיפא אפס נותנת אורך שתיים, לא בשפה, ואורך שלוש, בשפה.", do=show(f"r-x-{IDB['out']}")),
    N("ומילה בשפה מול מילה בחוץ: תמיד $\\varepsilon$. נשארה ״כל הטענות האחרות לא נכונות״.",
      say="ומילה בשפה מול מילה בחוץ: תמיד אפסילון. נשארה: כל הטענות האחרות לא נכונות.",
      do=show(f"r-x-{IDB['in-out']}", f"r-ok-{IDB['none']}"), hold=0.6),
], stage=f'<div id="b-res" class="h">{RES}<div class="nr-sm" style="margin-top:14px">$|w|\\bmod12$; ירוק = בשפה</div></div>',
   panel=f'<div class="qstem"><span class="qid">{QB["id"]}</span>$L=(\\Sigma\\Sigma\\Sigma)^*+(\\Sigma\\Sigma\\Sigma\\Sigma)^*$, $x\\ne y$.</div>'
       + st.options("r", xy_opts(KB)))

QC = BANK["24X-A-Q14"]
L01 = lambda w: len(w) >= 1 and w[0] == "0" and set(w[1:]) <= {"1"}           # 01*
assert QC["correctId"] == "b" and {o["id"]: o["value"] for o in QC["options"]}["b"] == "3"
assert rank_stable(L01, "01") == 3 and answer(L01) == "in"
INS, OUTS = sides(L01)
assert len(INS) == 1 and len(OUTS) == 2 and [c[0] for c in OUTS] == ["", "1"]
assert separable(L01, "", "1", "01") == "0"
GC = groups(L01)
examC = Scene("examC", "עוד שאלה: לספור צדדים", [
    N("ועוד שאלה, הפעם ״כמה מצבים״: $L=01^*$. אפס, ואחריו כמה אחדות שרוצים. נשתמש באותו מיון לצדדים.",
      say="ועוד שאלה, הפעם כמה מצבים: אל שווה אפס, אחת כוכבית. אפס, ואחריו כמה אחדות שרוצים. נשתמש באותו מיון לצדדים.",
      do=show("c3", *[f"c3-b-{k}" for k in range(len(GC))], *[f"c3-w-{k}-{n}" for k, (_, w_, _) in enumerate(GC) for n in range(len(w_))])),
    N("בשפה: $0$, $01$, $011$… לכולן חסר אותו דבר, עוד אחדות או כלום. מחלקה **אחת**.",
      say="בשפה: אפס, אפס אחת, אפס אחת אחת, וכן הלאה. לכולן חסר אותו דבר, עוד אחדות או כלום. מחלקה אחת.", do=show("c-in")),
    N("ומחוץ לשפה שתי מחלקות: $\\varepsilon$, שעוד יכולה להיכנס עם $0$, וכל מה שכבר נפל לבור, כמו $1$ ו-$00$.",
      say="ומחוץ לשפה שתי מחלקות: אפסילון, שעוד יכולה להיכנס עם אפס, וכל מה שכבר נפל לבור, כמו אחת ואפס אפס.", do=show("c-out")),
    N("סך הכול שלוש מחלקות. והקבוצה $\\{\\varepsilon,0,1\\}$ מפרידה. התשובה: שלושה מצבים.",
      say="סך הכול שלוש מחלקות. והקבוצה אפסילון, אפס, אחת מפרידה. התשובה: שלושה מצבים.", do=show("t-ok-b")),
    N("המלכודת: שתיים, ״בפנים ובחוץ״. אבל הצד שבחוץ אינו מחלקה אחת: $\\varepsilon$ עוד לא הפסידה, ו-$1$ כבר כן.",
      say="המלכודת: שתיים, בפנים ובחוץ. אבל הצד שבחוץ אינו מחלקה אחת: אפסילון עוד לא הפסידה, ואחת כבר כן.",
      do=show("t-x-a", "t-n-a", "t-x-c", "t-x-d"), hold=0.6),
], stage=buckets("c3", GC).replace('class="nr-bk"', 'class="nr-bk h"', 1)
         + st.card("c-in", "rule", "בשפה: מחלקה <b>אחת</b>")
         + st.card("c-out", "plain", "מחוץ: $\\varepsilon$ ובור, שתי מחלקות. $z=0$ מפרידה ביניהן"),
   panel=f'<div class="qstem"><span class="qid">{QC["id"]}</span>$L=01^*$. כמה מצבים באס״ד המינימלי?</div>'
       + st.options("t", [(o["id"], o["html"]) for o in QC["options"]], notes={"a": "בפנים/בחוץ בלבד"}))

recap = Scene("recap", "סיכום", [
    N("לסיכום: מילה בשפה ומילה בחוץ תמיד ניתנות להפרדה, עם $\\varepsilon$.", say="לסיכום: מילה בשפה ומילה בחוץ תמיד ניתנות להפרדה, עם אפסילון.",
      do=show("r1")),
    N("״$x,y\\in L$״ נכונה כשכל השפה מחלקה אחת. ״$x,y\\notin L$״ כשכל המשלים מחלקה אחת.",
      say="הטענה על אקס ווואי בשפה נכונה כשכל השפה מחלקה אחת. הטענה על אקס ווואי בחוץ, כשכל המשלים מחלקה אחת.", do=show("r2")),
    N("ואם אף צד לא, התשובה ״כל הטענות האחרות״. סופרים מחלקות בכל צד, ומסיימים. נתראה ברמה הבאה.",
      do=show("r3"), hold=0.8),
], stage=buckets("rk", groups(S0), hidden=False),
   panel=st.card("r1", "rule", "🔑 בשפה מול בחוץ: <b>תמיד</b> ניתנות להפרדה, עם $z=\\varepsilon$")
       + st.card("r2", "rule", "🔑 אם צד הוא מחלקה <b>אחת</b>, אז הטענה על הצד הזה נכונה")
       + st.card("r3", "trap", "⚠️ אם אף צד אינו מחלקה אחת, אז ״כל הטענות האחרות לא נכונות״"))

VIDEO = Video("N05", "nerode", "משפחת x ו-y: מתי שתי מילים לא ניתנות להפרדה",
              [title, family, ex1, ex2, ex3, examA, examB, examC, recap],
              bank={"26A-A-Q13": "c", "24A-C-Q10": "d", "24X-A-Q14": "b"})
