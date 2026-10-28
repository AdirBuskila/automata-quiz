# -*- coding: utf-8 -*-
"""N08 · מבחן גמר: נרוד, Rank ומינימיזציה — boss walkthrough (build: tools/video/vid.py N08).

Source: tools/needhelp/nerode/N08.py (checklist). No new concept. Four nerode bank questions that NO level cites and that
are not in N08's boss quiz (21S-A-Q6 23A-A-Q11 23A-A-Q14 21S-A-Q21 25A-C-Q7): 25A-B-Q8, 24A-B-Q16 (NFA figure),
SAMP-19-Q17, 21S-A-Q11. Each is checked with the simulators below; the figure of 24A-B-Q16 is the original raster.
"""
from nh import dfa_table, nfa_from_edges, words, rank_stable, is_separating_set, separable
from vid import show, hide, Scene, Video, BANK
import stage as st
from w_nerode import N, CSS, pairs, pair_cells, cell_html, wd

# ---------------------------------------------------------------- Q1 25A-B-Q8: does not end with bb
Q1 = BANK["25A-B-Q8"]
NBB = lambda w: not w.endswith("bb")
BB = lambda w: w.endswith("bb")
assert rank_stable(NBB, "ab") == rank_stable(BB, "ab") == 3 and Q1["correctId"] == "b"
assert {o["id"]: o["value"] for o in Q1["options"]}["b"] == "3"
D1 = dfa_table("ab", {"0": "0 1", "1": "0 2", "2": "0 2"}, "0", {"0", "1"})
assert D1.lang(8) == {w for w in words("ab", 8) if NBB(w)} and D1.n_min() == 3
assert is_separating_set(NBB, ["", "b", "bb"], "ab")
assert rank_stable(lambda w: len(w) >= 2 and w[-2] == "b", "ab") == 4            # the trap 4: "second from the end"

# ---------------------------------------------------------------- Q2 24A-B-Q16: the NFA of the figure
Q2 = BANK["24A-B-Q16"]
A = nfa_from_edges("01", [("p", "1", "m"), ("m", "0", "r"), ("m", "1", "r"), ("r", "1", "m")], "p", {"p", "r"})
LA = lambda w: len(w) % 2 == 0 and all(w[i] == "1" for i in range(0, len(w), 2))  # (1(0+1))*
assert A.lang(8) == {w for w in words("01", 8) if LA(w)}
SUB = A.to_dfa()
assert len(SUB.states) == 4 and SUB.n_min() == 3 == rank_stable(LA, "01") and Q2["correctId"] == "a"
assert is_separating_set(LA, ["", "0", "1"], "01")
assert separable(LA, "", "10", "01") is None                                      # start ≡ "after a pair"

# ---------------------------------------------------------------- Q3 SAMP-19-Q17: {ab, ba}
Q3 = BANK["SAMP-19-Q17"]
L3 = lambda w: w in {"ab", "ba"}
assert all(L3(w) == (w.count("a") == w.count("b") and len(w) == 2) for w in words("ab", 7))
R3 = rank_stable(L3, "ab", 9, (6, 7, 8))
assert R3 == 5 and Q3["correctId"] == "d"
OPT3 = {"a": ["a", "b"], "b": ["a", "b", ""], "c": ["a", "b", "", "ab"]}
assert all(is_separating_set(L3, v, "ab") and len(v) < R3 for v in OPT3.values())
T5 = ["", "a", "b", "ab", "abb"]
assert is_separating_set(L3, T5, "ab")
PC3 = pair_cells(L3, T5, "ab")
assert all(v is not None for v in PC3.values())

# ---------------------------------------------------------------- Q4 21S-A-Q11: what survives a change of L or T
Q4 = BANK["21S-A-Q11"]
AA = lambda w: "aa" in w
T = ["", "a", "aa"]
assert is_separating_set(AA, T, "ab") and is_separating_set(lambda w: not AA(w), T, "ab")
assert not is_separating_set(lambda w: True, T, "ab")          # L ⊆ L' = Σ*
assert not is_separating_set(lambda w: False, T, "ab")         # L'' = ∅ ⊆ L
assert not is_separating_set(AA, T + ["b"], "ab")              # T ⊆ T' = T ∪ {b}, b ≡ ε
assert Q4["correctId"] == "a"
V4 = {o["id"]: o["value"] for o in Q4["options"]}
assert "המשלימה" in V4["a"] and "L\\subseteq L'" in V4["b"] and "L''\\subseteq L" in V4["c"] and "T\\subseteq T'" in V4["d"]

title = Scene("title", "", [
    N("מבחן הגמר של נרוד. אין כאן חומר חדש: ארבע שאלות אמיתיות, שלא ראינו באף רמה.",
      say="מבחן הגמר של נרוד. אין כאן חומר חדש: ארבע שאלות אמיתיות, שלא ראינו באף רמה."),
    N("לכל שאלה: נזהה את הסוג, נפעיל את הכלל, ונמצא את המלכודת.", hold=0.4),
], stage=CSS + '<div class="kicker">N08 · נרוד, Rank וקבוצות מפרידות</div><h1>מבחן גמר: נרוד, Rank ומינימיזציה</h1>'
         '<p>לפתור שאלות אמיתיות מהמבחנים על Rank, קבוצות מפרידות ופעולות, בלי עזרה.</p>', layout="title")

attack = Scene("attack", "איך תוקפים שאלה", [
    N("איך תוקפים שאלת נרוד? קודם מזהים את הסוג. ״כמה מצבים?״: שואלים מה לזכור, וסופרים, כולל בור.",
      say="איך תוקפים שאלת נרוד? קודם מזהים את הסוג. כמה מצבים? שואלים מה לזכור, וסופרים, כולל בור.", do=show("k1")),
    N("״קבוצה מפרידה ואין גדולה יותר״: הגודל חייב להיות בדיוק ה-Rank, וכל זוג מופרד.",
      say="קבוצה מפרידה ואין גדולה יותר: הגודל חייב להיות בדיוק הראנק, וכל זוג מופרד.", do=show("k2")),
    N("״תמיד נכון״ על פעולות: מחפשים דוגמה נגדית מהשלישייה. ומשלים שומר על ה-Rank ועל כל הפרדה.", do=show("k3")),
    N("ו״לא רגולרית כי…״: קבוצה אינסופית **ומפרידה**. נתחיל.", say="ולא רגולרית כי: קבוצה אינסופית ומפרידה. נתחיל.",
      do=show("k4"), hold=0.5),
], stage='<div class="nr-big" style="font-size:46px">1. סוג &nbsp; 2. כלל &nbsp; 3. מלכודת</div>',
   panel=st.card("k1", "plain", "<b>כמה מצבים?</b> מה לזכור, לספור, לא לשכוח בור")
       + st.card("k2", "plain", "<b>מפרידה ואין גדולה?</b> $|T|=\\mathrm{Rank}$ וכל זוג מופרד")
       + st.card("k3", "plain", "<b>תמיד נכון?</b> השלישייה; $\\mathrm{Rank}(\\overline{L})=\\mathrm{Rank}(L)$")
       + st.card("k4", "plain", "<b>לא רגולרית?</b> $T$ אינסופית <b>ומפרידה</b>"))

N3 = {"0": "q_0", "1": "q_1", "2": "q_2"}
POS3 = {"0": (170, 190), "1": (450, 190), "2": (730, 190)}
q1 = Scene("q1", "שאלה 1", [
    N("שאלה ראשונה: $L$ = המילים מעל $\\{a,b\\}$ ש**לא** מסתיימות ב-$bb$. כמה מצבים באס״ד המינימלי?",
      say="שאלה ראשונה: אל שווה המילים מעל אֵיי ובִּי שלא מסתיימות בבִּי בִּי. כמה מצבים באסאד המינימלי?"),
    N("המשלים שלה הוא ״מסתיימת ב-$bb$״. ולמשלים יש אותו Rank. אז נחשב את הקלה מביניהן.",
      say="המשלים שלה הוא מסתיימת בבִּי בִּי. ולמשלים יש אותו ראנק. אז נחשב את הקלה מביניהן.", do=show("a-1")),
    N("מסתיימת בשתי אותיות קבועות: שתיים ועוד אחת, שלושה מצבים. בלי $b$ בסוף, $b$ אחת, ו-$bb$.",
      say="מסתיימת בשתי אותיות קבועות: שתיים ועוד אחת, שלושה מצבים. בלי בִּי בסוף, בִּי אחת, ובִּי בִּי.", do=show("a-dfa")),
    N("ושלוש מילים מופרדות: $\\{\\varepsilon,b,bb\\}$. התשובה: שלושה.", say="ושלוש מילים מופרדות: אפסילון, בִּי, בִּי בִּי. התשובה: שלושה.",
      do=show("q-ok-b")),
    N("המלכודת: ארבע, ״לזכור את שתי האותיות האחרונות״. זה הכלל של ״האות השנייה מהסוף״, לא של ״מסתיימת ב-״.",
      do=show("q-x-c", "q-n-c")),
    N("ושתיים שוכח את ה-$b$ הבודדת, שממנה חסרה רק עוד $b$ אחת כדי לצאת מהשפה.",
      say="ושתיים שוכח את הבִּי הבודדת, שממנה חסרה רק עוד בִּי אחת כדי לצאת מהשפה.", do=show("q-x-a", "q-n-a", "q-x-d"), hold=0.6),
], stage='<div id="a-1" class="h nr-big">$\\mathrm{Rank}(L)=\\mathrm{Rank}(\\overline{L})$, &nbsp; $\\overline{L}=\\Sigma^*bb$</div>'
         f'<div id="a-dfa" class="h">{st.dfa_svg("a", D1, POS3, N3, w=900, h=330, scale=0.95, bend={("2", "0"): 0.33})}</div>',
   panel=f'<div class="qstem"><span class="qid">{Q1["id"]}</span>$L$ = המילים מעל $\\{{a,b\\}}$ שלא מסתיימות ב-$bb$. '
         'כמה מצבים באס״ד המינימלי?</div>'
       + st.options("q", [(o["id"], o["html"]) for o in Q1["options"]], notes={"c": "האות השנייה מהסוף", "a": "בלי $b$ בודדת"}))

RINGS = [("p", 152, 70, 42), ("m", 356, 70, 42), ("r", 557, 70, 42)]
q2 = Scene("q2", "שאלה 2", [
    N("שאלה שנייה: נתון אסל״ד, ושואלים על ה-Rank של השפה שלו.", say="שאלה שנייה: נתון אסלאד, ושואלים על הראנק של השפה שלו."),
    N("מה השפה? מההתחלה, שהוא מקבל, קוראים $1$, ואז $0$ או $1$, ומגיעים שוב למקבל. ומשם $1$ מחזיר לאמצע.",
      say="מה השפה? מההתחלה, שהוא מקבל, קוראים אחת, ואז אפס או אחת, ומגיעים שוב למקבל. ומשם אחת מחזירה לאמצע.",
      do=show("f-ring-p", "f-ring-r")),
    N("כלומר זוגות של אותיות, שכל אחד מהם מתחיל ב-$1$: $(1(0+1))^*$.", say="כלומר זוגות של אותיות, שכל אחד מהם מתחיל באחת.",
      do=show("b-1")),
    N("מה לזכור? ״בגבול בין זוגות״, ״באמצע זוג״, או ״נפלנו״: בור. שלוש מחלקות.", do=hide("f-ring-p", "f-ring-r") + show("f-ring-m", "b-2")),
    N("ו-$\\{\\varepsilon,0,1\\}$ מפרידה: $\\varepsilon$ בשפה, $0$ בבור, ו-$1$ באמצע. התשובה: Rank שלוש.",
      say="והקבוצה אפסילון, אפס, אחת מפרידה: אפסילון בשפה, אפס בבור, ואחת באמצע. התשובה: ראנק שלוש.", do=show("p-ok-a")),
    N("המלכודת: לבנות אוטומט חזקה, לקבל ארבעה מצבים עם הבור, ולענות ״גדול משלוש״.",
      do=hide("f-ring-m") + show("b-3", "p-x-b")),
    N("אבל המצב ההתחלתי ו״אחרי זוג״ שקולים: שניהם מקבלים, ושניהם צריכים $1$ ואז אות. אוטומט החזקה לא בהכרח מינימלי, וכאן הוא לא.",
      say="אבל המצב ההתחלתי ואחרי זוג שקולים: שניהם מקבלים, ושניהם צריכים אחת ואז אות. אוטומט החזקה לא בהכרח מינימלי, וכאן הוא לא.",
      do=show("f-ring-p", "f-ring-r", "p-x-c", "p-x-d"), hold=0.6),
], stage=st.raster("f", "images/exams/24A-B-Q16.png", 900, (600, 150), rings=RINGS)
         + '<div id="b-1" class="h nr-big">$L=(1(0+1))^*$</div>'
         '<div id="b-2" class="h nr-big">גבול זוג (מקבל) · באמצע זוג · בור</div>'
         '<div id="b-3" class="h nr-sm" style="font-size:32px">אוטומט החזקה: $4$ מצבים. אחרי מינימיזציה: $3$</div>',
   panel=f'<div class="qstem"><span class="qid">{Q2["id"]}</span>{Q2["questionHtml"]}</div>'
       + st.options("p", [(o["id"], o["html"]) for o in Q2["options"]]))

PG3 = pairs("g3", T5, {k: cell_html(v) for k, v in PC3.items()})
O3 = [("a", "$\\{a,b\\}$ מפרידה, ואין מפרידה גדולה יותר"), ("b", "$\\{a,b,\\varepsilon\\}$ מפרידה, ואין מפרידה גדולה יותר"),
      ("c", "$\\{a,b,\\varepsilon,ab\\}$ מפרידה, ואין מפרידה גדולה יותר"), ("d", "שלוש הטענות האחרות לא נכונות")]
q3 = Scene("q3", "שאלה 3", [
    N("שאלה שלישית: $L$ = מילים באורך שתיים, עם אותו מספר של $a$ ושל $b$. כלומר $L=\\{ab,ba\\}$.",
      say="שאלה שלישית: אל שווה מילים באורך שתיים, עם אותו מספר של אֵיי ושל בִּי. כלומר אל שווה הקבוצה אֵיי בִּי, בִּי אֵיי."),
    N("שלוש אפשרויות אומרות ״מפרידה, **ואין** גדולה יותר״. אז קודם ה-Rank.", say="שלוש אפשרויות אומרות מפרידה, ואין גדולה יותר. אז קודם הראנק."),
    N("שפה סופית: התחלה, אחרי $a$, אחרי $b$, ״מילה מלאה״, ובור. חמש מחלקות.",
      say="שפה סופית: התחלה, אחרי אֵיי, אחרי בִּי, מילה מלאה, ובור. חמש מחלקות.", do=show("c-1")),
    N("ובאמת: $\\{\\varepsilon,a,b,ab,abb\\}$ מפרידה. כל תא בטבלה מתמלא בסיפא.",
      say="ובאמת: אפסילון, אֵיי, בִּי, אֵיי בִּי, ואֵיי בִּי בִּי, מפרידה. כל תא בטבלה מתמלא בסיפא.",
      do=show("c-pg", *[f"g3-c-{i}-{j}" for (i, j) in PC3])),
    N("עכשיו, שלוש הקבוצות באפשרויות **מפרידות**. זו המלכודת! אבל יש בהן שתיים, שלוש וארבע מילים.",
      say="עכשיו, שלוש הקבוצות באפשרויות מפרידות. זו המלכודת! אבל יש בהן שתיים, שלוש וארבע מילים."),
    N("וכולן פחות מחמש, אז בכולן ״אין גדולה יותר״ שקרי. אפילו הגדולה מביניהן שכחה את הבור.",
      do=show("r-x-a", "r-x-b", "r-x-c", "r-n-c")),
    N("התשובה: שלוש הטענות האחרות לא נכונות.", do=show("r-ok-d"), hold=0.6),
], stage='<div id="c-1" class="h nr-big">$\\varepsilon$ · $a$ · $b$ · מלאה · בור: $\\mathrm{Rank}=5$</div>'
         f'<div id="c-pg" class="h">{PG3}</div>',
   panel=f'<div class="qstem"><span class="qid">{Q3["id"]}</span>$L=\\{{w\\mid\\#_a(w)=\\#_b(w),\\ |w|=2\\}}$</div>'
       + st.options("r", O3, notes={"c": "$4<5$"}))

O4 = [("a", "$T$ מפרידה גם ביחס ל<b>משלימה</b> של $L$"), ("b", "אם $L\\subseteq L'$, אז $T$ מפרידה ביחס ל-$L'$"),
      ("c", "אם $L''\\subseteq L$, אז $T$ מפרידה ביחס ל-$L''$"), ("d", "לכל $T\\subseteq T'$: $T'$ מפרידה ביחס ל-$L$")]
q4 = Scene("q4", "שאלה 4", [
    N("שאלה רביעית: $T$ קבוצה מפרידה עבור $L$. מה נשאר נכון?", say="שאלה רביעית: טי קבוצה מפרידה עבור אל. מה נשאר נכון?"),
    N("נבדוק עם דוגמה שאנחנו מכירים: $L$ = מכילה $aa$, ו-$T=\\{\\varepsilon,a,aa\\}$.",
      say="נבדוק עם דוגמה שאנחנו מכירים: אל שווה מכילה אֵיי אֵיי, וטי שווה אפסילון, אֵיי, אֵיי אֵיי.", do=show("d-1")),
    N("שפה גדולה יותר? קחו את כל המילים. שם יש מחלקה אחת, ושום דבר לא מופרד.", do=show("s-x-b", "s-n-b")),
    N("שפה קטנה יותר? הקבוצה הריקה. אותה בעיה.", do=show("s-x-c", "s-n-c")),
    N("קבוצה גדולה יותר? נוסיף את $b$. אבל $b$ שקולה ל-$\\varepsilon$, אז היא כבר לא מפרידה.",
      say="קבוצה גדולה יותר? נוסיף את בִּי. אבל בִּי שקולה לאפסילון, אז היא כבר לא מפרידה.", do=show("s-x-d", "s-n-d")),
    N("והמשלימה: אותה סיפא מפרידה את אותו זוג גם שם, רק הפוך. לכן $T$ מפרידה גם ביחס למשלימה.",
      say="והמשלימה: אותה סיפא מפרידה את אותו זוג גם שם, רק הפוך. לכן טי מפרידה גם ביחס למשלימה.", do=show("s-ok-a")),
    N("המלכודת: לחשוב ש״הכלה״ שומרת על הפרדה. היא לא. רק המשלים שומר.", hold=0.6),
], stage='<div id="d-1" class="h nr-big">$L$ = מכילה $aa$, &nbsp; $T=\\{\\varepsilon,a,aa\\}$</div>',
   panel=f'<div class="qstem"><span class="qid">{Q4["id"]}</span>$T$ מפרידה ביחס ל-$L$. איזו טענה נכונה?</div>'
       + st.options("s", O4, notes={"b": "$L'=\\Sigma^*$", "c": "$L''=\\emptyset$", "d": "$T\\cup\\{b\\}$"}))

recap = Scene("recap", "סיכום הקורס", [
    N("סיכום של כל נרוד. $x$ ו-$y$ שקולות אם אין סיפא שמפרידה ביניהן. ה-Rank הוא מספר המחלקות, וגודל האס״ד המינימלי.",
      say="סיכום של כל נרוד. אקס ווואי שקולות אם אין סיפא שמפרידה ביניהן. הראנק הוא מספר המחלקות, וגודל האסאד המינימלי.",
      do=show("r1")),
    N("Rank שווה $k$: אס״ד מלא עם $k$ מצבים, וגם קבוצה מפרידה בגודל $k$. ובשפה סופית, תמיד בור.",
      say="ראנק שווה קיי: אסאד מלא עם קיי מצבים, וגם קבוצה מפרידה בגודל קיי. ובשפה סופית, תמיד בור.", do=show("r2")),
    N("מסתיימת ב-$k$: $k+1$. האות ה-$k$ מהסוף: $2^k$. משלים שומר Rank, ואיחוד וחיתוך חסומים במכפלה.",
      say="מסתיימת בקיי: קיי ועוד אחת. האות הקיי מהסוף: שתיים בחזקת קיי. משלים שומר ראנק, ואיחוד וחיתוך חסומים במכפלה.",
      do=show("r3")),
    N("ו-Rank אינסוף פירושו לא רגולרית, עם קבוצה מפרידה אינסופית. בהצלחה במבחן!",
      say="וראנק אינסוף פירושו לא רגולרית, עם קבוצה מפרידה אינסופית. בהצלחה במבחן!", do=show("r4"), hold=0.8),
], stage='<div class="nr-big" style="font-size:44px">מה האוטומט חייב לזכור?</div>',
   panel=st.card("r1", "rule", "🔑 $x\\equiv_L y$ אם ורק אם אין סיפא מפרידה; $\\mathrm{Rank}$ = מחלקות = אס״ד מינימלי")
       + st.card("r2", "rule", "🔑 $\\mathrm{Rank}=k$: אס״ד מלא + $T$ מפרידה בגודל $k$; בשפה סופית יש בור")
       + st.card("r3", "rule", "🔑 $k+1$ / $2^k$; $\\overline{L}$ שומר; $\\cup,\\cap\\le$ מכפלה")
       + st.card("r4", "rule", "🔑 $\\mathrm{Rank}=\\infty$ אם ורק אם לא רגולרית; מוכיחים ב-$T$ אינסופית <b>ומפרידה</b>"))

VIDEO = Video("N08", "nerode", "מבחן גמר: נרוד, Rank ומינימיזציה", [title, attack, q1, q2, q3, q4, recap],
              bank={"25A-B-Q8": "b", "24A-B-Q16": "a", "SAMP-19-Q17": "d", "21S-A-Q11": "a"})
