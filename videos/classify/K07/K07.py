# -*- coding: utf-8 -*-
"""K07 · משחק למת הניפוח לשפות חסרות הקשר — video script (build: tools/video/vid.py K07).

Source: tools/needhelp/classify/K07.py (lesson + goal). Notation follows the lesson / formula sheet: constant ℓ,
split w = xyzuv, |yzu| <= ℓ, exponent n (the solutions' uvwxy / |vwx| <= ℓ / i is shown once as a mapping).
Worked example: the crossing language a^n b^m c^n d^m (formula-sheet table: not CFL), window animated on
a^ℓ b^ℓ c^ℓ d^ℓ (a^ℓ b^ℓ c^ℓ itself appears in the quiz, so it is not used). Exam anchor: 23A-A-Q5 (cited by the lesson; the "word from the easy part" trap).
Not used on purpose: the quiz's languages a^k b^{2k} a^k, a^{k^2}, uu, a^i b^j c^k (i<j<k).
Every window, split and pump below is computed and checked with the simulators.
"""
import re
from nh import *
from vid import Scene, Video, show, hide, BANK
import stage as st
import w_closure as W
from w_closure import KP


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# ---------------------------------------------------------------- verified facts
CROSS = lambda w: (lambda t: t is not None and t[0] == t[2] and t[1] == t[3])(parts(w, "abcd"))
assert all(pump_breaks_cf(CROSS, "a" * p + "b" * p + "c" * p + "d" * p, p) for p in (2, 3))
assert rank_growing(CROSS, "abcd", plens=(2, 3, 4), slen=6)
P_ = 3
W1 = "a" * P_ + "b" * P_ + "c" * P_ + "d" * P_
assert all(not ("a" in W1[i:i + P_] and "c" in W1[i:i + P_]) and not ("b" in W1[i:i + P_] and "d" in W1[i:i + P_])
           for i in range(len(W1) - P_ + 1))                                    # never a with c, never b with d
WIN_STARTS = [0, 2, 4, 6, 8]
WIN_SETS = {s_: "".join(sorted(set(W1[s_:s_ + P_]))) for s_ in WIN_STARTS}
assert WIN_SETS == {0: "a", 2: "ab", 4: "bc", 6: "c", 8: "cd"}
# one concrete split: y = the last a, z = '', u = the first b
x, y, z, u, v = W1[:2], W1[2], "", W1[3], W1[4:]
assert x + y + z + u + v == W1 and len(y + z + u) <= P_ and (y + u)
PUMP2 = x + y * 2 + z + u * 2 + v
assert parts(PUMP2, "abcd") == (4, 4, 3, 3) and not CROSS(PUMP2)
# the narrated case split: n = 2 breaks EVERY split (mixed pieces scramble the order, else a pair is unbalanced)
assert all(pump_breaks_cf(CROSS, "a" * p + "b" * p + "c" * p + "d" * p, p, ipow=(2,)) for p in (2, 3, 4))

# exam 23A-A-Q5
Q = BANK["23A-A-Q5"]
assert Q["correctId"] == "c"
def LQ(w):
    m = re.fullmatch("(0*)(1*)", w)
    if m and len(m.group(1)) == 2 * len(m.group(2)):
        return True
    m = re.fullmatch("(0*)(1*)(0*)", w)
    if m and len(m.group(1)) == len(m.group(2)) == len(m.group(3)):
        return True
    m = re.fullmatch("(1*)(0*)", w)
    return bool(m and len(m.group(2)) == 2 * len(m.group(1)))


T1 = lambda w: (lambda t: t is not None and t[0] == 2 * t[1])(parts(w, "01"))       # 0^{2n} 1^n
assert classify_cert(T1, "01", ("cfl", "S -> 00S1 | ε"), n=9) == "cfl"
assert all(pump_breaks_cf(LQ, "0" * p + "1" * p + "0" * p, p) for p in (2, 3, 4))   # the right word
assert all(pump_breaks_cf(LQ, "0" * p + "1" * p + "0" * p, p, ipow=(2,)) for p in (2, 3, 4, 5))   # n = 2 always works
assert not any(pump_breaks_cf(LQ, "0" * (2 * p) + "1" * p, p) for p in (3, 4))        # the trap word survives
WT = "0" * 8 + "1" * 4                                                                # ℓ = 4: the adversary's split
sx, sy, sz, su, sv = WT[:6], WT[6:8], "", WT[8], WT[9:]
assert sx + sy + sz + su + sv == WT and len(sy + sz + su) <= 4
assert all(LQ(sx + sy * n + sz + su * n + sv) for n in range(6))
assert LQ("0" * 10 + "1" * 5)
assert not pump_breaks_cf(LQ, "0" * 4 + "1" * 2, 9) and len("000011") < 9               # a fixed word is too short

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    KP("בסרטון הזה נלמד את למת הניפוח לשפות חסרות הקשר, כמשחק נגד יריב."),
    KP("נראה למה חלון של $\\ell$ אותיות נוגע בשני גושים לכל היותר, ונפתור שאלה ממבחן עם המלכודת שלה.",
       say="נראה למה חלון של אֵל אותיות נוגע בשני גושים לכל היותר, ונפתור שאלה ממבחן עם המלכודת שלה.", hold=0.4),
], stage='<div class="kicker">K07 · סיווג שפות</div><h1>משחק למת הניפוח לשפות חסרות הקשר</h1>'
         '<p>לבחור מילה שמפריכה חסרות הקשר בלמת הניפוח לח״ה, ולהסביר למה חלון של $\\ell$ אותיות נוגע בשני גושים לכל היותר.</p>',
   layout="title")

lemma = Scene("lemma", "הלמה", [
    KP("מתי צריך את הלמה? כשרוצים להראות ששפה **לא** חסרת הקשר, והחיתוך עם שפה רגולרית לא עוזר."),
    KP("הנוסח מדף הנוסחאות: לכל שפה חסרת הקשר יש קבוע $\\ell$.",
       say="הנוסח מדף הנוסחאות: לכל שפה חסרת הקשר יש קבוע, אֵל.", do=show("lm-0")),
    KP("כל מילה בשפה שאורכה לפחות $\\ell$ מתפרקת לחמישה חלקים: $xyzuv$.",
       say="כל מילה בשפה שאורכה לפחות אֵל מתפרקת לחמישה חלקים: אִקְס, וואי, זד, יו, וִי.", do=show("lm-1")),
    KP("החלקים $y$ ו-$u$ הם **המנופחים**. לפחות אחד מהם לא ריק.",
       say="החלקים וואי ויו הם המנופחים. לפחות אחד מהם לא ריק.", do=show("lm-2")),
    KP("שלושת החלקים האמצעיים יחד, $yzu$, הם **החלון**, ואורכו לכל היותר $\\ell$.",
       say="שלושת החלקים האמצעיים יחד, וואי זד יו, הם החלון, ואורכו לכל היותר אֵל.", do=show("lm-3")),
    KP("ולכל $n$, גם אפס, אם מכפילים את $y$ ואת $u$ פי $n$, המילה נשארת בשפה.",
       say="ולכל אֵן, גם אפס, אם מכפילים את וואי ואת יו פי אֵן, המילה נשארת בשפה.", do=show("lm-4")),
    KP("בפתרונות כותבים לפעמים $uvwxy$. זו אותה למה: המנופחים הם החלק השני והרביעי, והחלון הוא שלושת האמצעיים.",
       say="בפתרונות כותבים לפעמים יו, וִי, דאבל יו, אקס, וואי. זו אותה למה: המנופחים הם החלק השני והרביעי, והחלון הוא שלושת האמצעיים.",
       do=show("lm-map")),
    KP("עכשיו המשחק: את הקבוע ואת הפירוק בוחר **היריב**. את המילה ואת $n$ בוחרים **אתם**.",
       say="עכשיו המשחק: את הקבוע ואת הפירוק בוחר היריב. את המילה ואת אֵן בוחרים אתם.", do=show("lm-game"), hold=0.5),
], stage=W.STYLE + W.steps("lm", [
    ("קיים קבוע $\\ell$", ""),
    ("אם $w\\in L$ ו-$|w|\\ge\\ell$, אז $w=xyzuv$", ""),
    ("$yu\\ne\\varepsilon$ &nbsp;(<b>המנופחים</b>)", ""),
    ("$|yzu|\\le\\ell$ &nbsp;(<b>החלון</b>)", ""),
    ("$\\forall n\\ge0:\\ xy^nzu^nv\\in L$", "key")], width=900),
   panel=st.card("lm-map", "plain", "בפתרונות: $w=uvwxy$, $|vwx|\\le\\ell$, $uv^iwx^iy\\in L$")
       + st.card("lm-game", "rule", "🔑 <b>היריב</b> בוחר את $\\ell$ ואת הפירוק.<br><b>אתם</b> בוחרים את המילה ואת $n$."))

game = Scene("game", "תבנית ההוכחה", [
    KP("תבנית ההוכחה, חמישה צעדים. אחת: נניח בשלילה שהשפה חסרת הקשר, ויהי $\\ell$ קבוע הניפוח.",
       say="תבנית ההוכחה, חמישה צעדים. אחת: נניח בשלילה שהשפה חסרת הקשר, ויהי אֵל קבוע הניפוח.", do=show("gm-0")),
    KP("שתיים: בוחרים מילה **שתלויה ב-$\\ell$**, למשל $a^\\ell b^\\ell c^\\ell d^\\ell$. לא דוגמה מספרית.",
       say="שתיים: בוחרים מילה שתלויה באֵל, למשל אֵל אותיות מכל אחת מאֵיי, בִּי, סִי ודִּי. לא דוגמה מספרית.",
       do=show("gm-1")),
    KP("שלוש: יהי פירוק **כלשהו**. לא אנחנו בוחרים אותו, אז צריך לטפל בכל פירוק אפשרי.", do=show("gm-2")),
    KP("ארבע, הטיעון המרכזי: החלון נוגע לכל היותר בשני גושים סמוכים. לכן הניפוח משאיר גוש אחד בלי שינוי.",
       do=show("gm-3")),
    KP("וחמש: מחלקים למקרים, ובוחרים $n$, בדרך כלל אפס או שתיים, כך שהמילה יוצאת מהשפה. סתירה.",
       say="וחמש: מחלקים למקרים, ובוחרים אֵן, בדרך כלל אפס או שתיים, כך שהמילה יוצאת מהשפה. סתירה.",
       do=show("gm-4"), hold=0.5),
], stage=W.STYLE + W.steps("gm", [
    ("<b>1.</b> נניח בשלילה ש-$L$ ח״ה, ויהי $\\ell$ קבוע הניפוח", ""),
    ("<b>2.</b> בוחרים מילה <b>שתלויה ב-$\\ell$</b>: $a^\\ell b^\\ell c^\\ell d^\\ell$", "key"),
    ("<b>3.</b> פירוק <b>כלשהו</b> עם $yu\\ne\\varepsilon$, $|yzu|\\le\\ell$", ""),
    ("<b>4.</b> החלון נוגע ב<b>שני גושים סמוכים</b> לכל היותר", "key"),
    ("<b>5.</b> בוחרים $n$ (בדרך כלל $0$ או $2$): $xy^nzu^nv\\notin L$. סתירה", "ok")]))

lbl1 = W.block_labels(W1, lambda c, k: f"${c}^\\ell$")
blk1 = W.blocks("wb", W1, cw=70, ch=84, windows=[(str(s_), s_, P_) for s_ in WIN_STARTS] + [("yu", 2, 2)], labels=lbl1)
pumped = W.blocks("wp", PUMP2, cw=62, ch=74, labels=W.block_labels(PUMP2, lambda c, k: f"${c}^{{{k}}}$"))
SAYSET = {"a": "רק אֵיי", "ab": "אֵיי ובִּי", "bc": "בִּי וסִי", "c": "רק סִי", "cd": "סִי ודִּי"}
slide = [
    KP("דוגמה: $\\{a^nb^mc^nd^m\\}$. מספר ה-$a$ שווה למספר ה-$c$, ומספר ה-$b$ שווה למספר ה-$d$.",
       say="דוגמה: אֵיי בחזקת אֵן, בִּי בחזקת אֵם, סִי בחזקת אֵן, דִּי בחזקת אֵם. מספר האֵיי שווה למספר הסִי, ומספר הבִּי שווה למספר הדִּי.",
       do=show("cr-l")),
    KP("אלה השוואות **חוצות**. לפי טבלת השפות הידועות היא לא חסרת הקשר. עכשיו נראה את ההוכחה בלמה.",
       do=show("cr-t")),
    KP("המילה: $a^\\ell b^\\ell c^\\ell d^\\ell$. כדי לראות, נבחר $\\ell=3$: שלוש $a$, שלוש $b$, שלוש $c$, שלוש $d$.",
       say="המילה: אֵל אותיות מכל אחת. כדי לראות, נבחר אֵל שווה שלוש: שלוש אֵיי, שלוש בִּי, שלוש סִי, שלוש דִּי."),
    KP("החלון הוא שלוש אותיות רצופות. נזיז אותו.", say="החלון הוא שלוש אותיות רצופות. נזיז אותו."),
]
prev = None
for s_ in WIN_STARTS:
    letters = WIN_SETS[s_]
    slide.append(KP("חלון כאן: " + ("רק " if len(letters) == 1 else "") + " ו-".join(f"${c}$" for c in letters) + ".",
                    say=f"חלון כאן: {SAYSET[letters]}.", do=(hide(f"wb-w-{prev}") if prev is not None else []) + show(f"wb-w-{s_}")))
    prev = s_
window = Scene("window", "החלון", slide + [
    KP("בשום מקום החלון לא נוגע גם ב-$a$ וגם ב-$c$: ביניהם יש $\\ell$ אותיות $b$, והחלון קצר מדי כדי לעבור אותן.",
       say="בשום מקום החלון לא נוגע גם באֵיי וגם בסִי: ביניהן יש אֵל אותיות בִּי, והחלון קצר מדי כדי לעבור אותן.",
       do=hide(f"wb-w-{prev}") + show("wn-r1")),
    KP("ומאותה סיבה הוא לא נוגע גם ב-$b$ וגם ב-$d$.", say="ומאותה סיבה הוא לא נוגע גם בבִּי וגם בדִּי."),
    KP("עכשיו היריב בוחר פירוק. נגיד: $y$ היא ה-$a$ האחרונה, ו-$u$ היא ה-$b$ הראשונה.",
       say="עכשיו היריב בוחר פירוק. נגיד: וואי היא האֵיי האחרונה, ויו היא הבִּי הראשונה.",
       do=show("wb-w-yu", "wb-p-2", "wb-p-3")),
    KP("ננפח עם $n=2$: נוספו $a$ אחת ו-$b$ אחת. יוצא ארבע, ארבע, שלוש, שלוש.",
       say="ננפח עם אֵן שווה שתיים: נוספו אֵיי אחת ובִּי אחת. יוצא ארבע, ארבע, שלוש, שלוש.",
       do=show("wp-box", "wp-p-2", "wp-p-3", "wp-p-4", "wp-p-5")),
    KP("גוש ה-$c$ נשאר שלוש, וגוש ה-$a$ כבר ארבע: המילה לא בשפה.",
       say="גוש הסִי נשאר שלוש, וגוש האֵיי כבר ארבע: המילה לא בשפה.", do=show("wp-v")),
    KP("וזה עובד לכל פירוק. אם $y$ או $u$ מכילים שתי אותיות שונות, ניפוח בשתיים מערבב את הסדר.",
       say="וזה עובד לכל פירוק. אם וואי או יו מכילים שתי אותיות שונות, ניפוח בשתיים מערבב את הסדר.",
       do=show("wn-r2")),
    KP("אחרת, הניפוח משנה לפחות גוש אחד בלי בן הזוג שלו: $a$ עם $c$, $b$ עם $d$. בכל מקרה סתירה: השפה לא חסרת הקשר.",
       say="אחרת, הניפוח משנה לפחות גוש אחד בלי בן הזוג שלו: אֵיי עם סִי, בִּי עם דִּי. בכל מקרה סתירה: השפה לא חסרת הקשר.",
       hold=0.5),
], stage=W.STYLE + '<div id="cr-l" class="clo-big h">$L=\\{a^nb^mc^nd^m\\}$</div>' + blk1
         + '<div id="wp-box" class="h" style="display:flex;flex-direction:column;align-items:center;gap:10px">'
         + '<div class="hint">אחרי ניפוח עם $n=2$:</div>' + pumped
         + '<div id="wp-v" class="verdict bad h">$4\\ne3$: לא בשפה ✗</div></div>',
   panel=st.card("cr-t", "plain", "השוואות <b>חוצות</b>: $a$ עם $c$, ו-$b$ עם $d$")
       + st.card("wn-r1", "rule", "🔑 חלון של $\\ell$ אותיות לא נוגע גם ב-$a$ וגם ב-$c$, ולא גם ב-$b$ וגם ב-$d$")
       + st.card("wn-r2", "rule", "🔑 $y$ או $u$ מעורבבים: הסדר נשבר. אחרת: זוג אחד יוצא לא מאוזן"))

opts_notes = {"a": "השפה לא ח״ה", "b": "חלק ח״ה", "d": "חלק ח״ה"}
blk3 = W.blocks("tb", WT, cw=58, ch=70, windows=[("yu", 6, 3)],
                labels=W.block_labels(WT, lambda c, k: f"${c}^{{{k}}}$"))
exam = Scene("exam", "שאלה ממבחן", [
    KP("שאלה ממבחן. השפה היא איחוד של שלוש צורות: $0^{2n}1^n$, $0^n1^n0^n$, ו-$1^n0^{2n}$.",
       say="שאלה ממבחן. השפה היא איחוד של שלוש צורות: אפס בחזקת שתיים אֵן, אחת בחזקת אֵן. אפס, אחת, אפס, כל אחד בחזקת אֵן. ואחת בחזקת אֵן, אפס בחזקת שתיים אֵן."),
    KP("שלוש מהתשובות אומרות \"לא חסרת הקשר\", וכל אחת מציעה מילה אחרת לנפח. איזו מילה עובדת?",
       say="שלוש מהתשובות אומרות: לא חסרת הקשר, וכל אחת מציעה מילה אחרת לנפח. איזו מילה עובדת?"),
    KP("המלכודת: לבחור מילה מהחלק **הקל** של השפה. החלק $0^{2n}1^n$ לבדו הוא שפה חסרת הקשר.",
       say="המלכודת: לבחור מילה מהחלק הקל של השפה. החלק אפס בחזקת שתיים אֵן, אחת בחזקת אֵן, לבדו הוא שפה חסרת הקשר.",
       do=show("ex-trap")),
    KP("ולכן היריב תמיד ינצח עליה. נראה עם $\\ell=4$: המילה $0^81^4$.",
       say="ולכן היריב תמיד ינצח עליה. נראה עם אֵל שווה ארבע: שמונה אפסים וארבע אחדות.", do=show("tb-box")),
    KP("היריב בוחר: $y$ הם שני האפסים האחרונים, ו-$u$ היא האחת הראשונה.",
       say="היריב בוחר: וואי הם שני האפסים האחרונים, ויו היא האחת הראשונה.",
       do=show("tb-w-yu", "tb-p-6", "tb-p-7", "tb-p-8")),
    KP("כל ניפוח מוסיף או מוריד שני אפסים ואחת אחת יחד. היחס שתיים לאחד נשמר, והמילה נשארת בשפה.",
       say="כל ניפוח מוסיף או מוריד יחד שני אפסים וספרת אחת אחת. היחס שתיים לאחד נשמר, והמילה נשארת בשפה.",
       do=show("tb-v", "q-x-b", "q-n-b", "q-x-d", "q-n-d")),
    KP("אותו דבר במראה, $1^k0^{2k}$. שתי המילים האלה לא מביאות לסתירה.",
       say="אותו דבר במראה, אחת בחזקת קיי, אפס בחזקת שתיים קיי. שתי המילים האלה לא מביאות לסתירה."),
    KP("המילה הנכונה מגיעה מהחלק **הקשה**: $0^k1^k0^k$, שלושה גושים שווים.",
       say="המילה הנכונה מגיעה מהחלק הקשה: אפס בחזקת קיי, אחת בחזקת קיי, אפס בחזקת קיי. שלושה גושים שווים.",
       do=hide("tb-box") + show("ex-good")),
    KP("החלון לא נוגע באחד משני גושי האפסים, אז הגוש הזה נשאר $\\ell$. ננפח בשתיים: משהו אחר גדל, או שהסדר מתערבב.",
       say="החלון לא נוגע באחד משני גושי האפסים, אז הגוש הזה נשאר אֵל. ננפח בשתיים: משהו אחר גדל, או שהסדר מתערבב.",
       do=show("ex-1")),
    KP("המילה עדיין מתחילה ונגמרת באפס, אז רק הצורה האמצעית אפשרית. אבל הגושים כבר לא שווים, או שיש יותר משלושה גושים: לא בשפה.",
       do=show("ex-2", "q-ok-c")),
    KP("ולכן גם \"קיים דקדוק\" נופל: השפה לא חסרת הקשר. התשובה: $0^k1^k0^k$.",
       say="ולכן גם קיים דקדוק נופל: השפה לא חסרת הקשר. התשובה: אפס בחזקת קיי, אחת בחזקת קיי, אפס בחזקת קיי.",
       do=show("q-x-a", "q-n-a"), hold=0.6),
], stage=W.STYLE + '<div class="swap" style="--swap-h:330px">'
         + '<div id="tb-box" class="h">' + blk3 + '<div id="tb-v" class="verdict ok h">$0^{2m}1^m$: נשארת בשפה לכל $n$</div></div>'
         + '<div id="ex-good" class="h">' + W.steps("ex", [
             ("$0^\\ell1^\\ell0^\\ell$: החלון לא נוגע בשני גושי ה-$0$", "key"),
             ("עם $n=2$: גוש אחד נשאר $\\ell$, משהו אחר גדל או מתערבב", "ok"),
             ("מתחילה ונגמרת ב-$0$: רק $0^n1^n0^n$ אפשרית, והיא נשברת", "ok")], width=900).replace('id="ex-0" class="clo-st key h"', 'id="ex-0" class="clo-st key"')
         + "</div></div>"
         + '<div id="ex-trap" class="h">' + st.card("ex-trapc", "trap", "⚠️ <b>מילה מהחלק הקל</b> ($0^{2k}1^k$, $1^k0^{2k}$): "
                                                    "חלק ח״ה, תמיד אפשר לנפח").replace(' h"', '"') + "</div>",
   panel=W.qcard(Q, "q", notes=opts_notes, small=True))

recap = Scene("recap", "סיכום", [
    KP("לסיכום: היריב בוחר את $\\ell$ ואת הפירוק. אתם בוחרים מילה שתלויה ב-$\\ell$, ואת $n$.",
       say="לסיכום: היריב בוחר את אֵל ואת הפירוק. אתם בוחרים מילה שתלויה באֵל, ואת אֵן.", do=show("c1")),
    KP("החלון $yzu$ באורך לכל היותר $\\ell$, ולכן נוגע בשני גושים סמוכים לכל היותר. גוש אחד נשאר במקום.",
       say="החלון, וואי זד יו, באורך לכל היותר קבוע הניפוח, ולכן נוגע בשני גושים סמוכים לכל היותר. גוש אחד נשאר במקום.",
       do=show("c2")),
    KP("בוחרים את המילה מהחלק הקשה של השפה. מילה באורך קבוע, כמו $a^{100}$, נכשלת כש-$\\ell$ גדול ממנה.",
       say="בוחרים את המילה מהחלק הקשה של השפה. מילה באורך קבוע, כמו אֵיי בחזקת מאה, נכשלת כשאֵל גדול ממנה.",
       do=show("c3")),
    KP("ובשפה עם אות אחת אין גושים: שם הטיעון הוא על האורך. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=W.STYLE + W.blocks("rc", W1, cw=70, ch=84, windows=[("w", 2, P_)], labels=lbl1),
   panel=st.card("c1", "rule", "🔑 היריב: $\\ell$ ופירוק. אתם: מילה שתלויה ב-$\\ell$, ו-$n$")
       + st.card("c2", "rule", "🔑 $|yzu|\\le\\ell$, ולכן לכל היותר <b>שני גושים סמוכים</b>")
       + st.card("c3", "trap", "⚠️ מילה מהחלק <b>הקשה</b>; לא מילה באורך קבוע")
       + st.card("c4", "plain", "אות אחת: הטיעון הוא על <b>האורך</b>"))
recap.phrases[0].do += show("rc-w-w")

VIDEO = Video("K07", "classify", "משחק למת הניפוח לשפות חסרות הקשר",
              [title, lemma, game, window, exam, recap],
              bank={"23A-A-Q5": "c"})
