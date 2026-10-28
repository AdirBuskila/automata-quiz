# -*- coding: utf-8 -*-
"""K05 · חסרת הקשר מול לא חסרת הקשר: מקונן וחוצה — video script (build: tools/video/vid.py K05).

Source: tools/needhelp/classify/K05.py (lesson + goal). Exam anchor: 25A-C-Q6 (cited by the lesson; trap: a^k…d^k
wrapping the middle looks nested like a^n b^m c^m d^n, but k is compared three times; ∩ a*b*d* gives a^k b^k d^k).
Worked examples are new languages: {a^i b^j c^j a^i} (nested) vs {a^i b^j a^i b^j} (crossing), and
{#a = #b = #c} ∩ a*b*c* (plus the useless R = (abc)*).
Not used on purpose: the quiz languages of K05 (a^nb^mc^md^n and a^nb^mc^nd^m as questions, uu/uu^R as a question,
#a=#c ∧ #b=#d with four R's (= 25A-B-Q17), a^nb^mc^{n+m}); the formula-sheet table is only quoted, as in the lesson.
"""
import re

from nh import classify_cert, same_pred, rx, pump_breaks_cf
from vid import Scene, Video, show, hide, BANK
import stage as st
from w_classify import CSS, Pk, arcs, stack, opts_panel

CLS = {"finite": "a", "reg": "b", "cfl": "c", "noncfl": "d"}


def blocks(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


# ---------------------------------------------------------------- nested vs crossing
def NEST(w):     # a^i b^j c^j a^i (enumerated: the two a-blocks make a greedy block split ambiguous)
    return any(w == "a" * i + "b" * j + "c" * j + "a" * i for i in range(len(w) // 2 + 1) for j in range(len(w) // 2 + 1))
def CROSS(w):
    return any(w == "a" * i + "b" * j + "a" * i + "b" * j for i in range(len(w) // 2 + 1) for j in range(len(w) // 2 + 1))
assert classify_cert(NEST, "abc", ("cfl", "S->aSa|T;T->bTc|ε"), n=8) == "cfl"
assert classify_cert(CROSS, "ab", ("noncfl", lambda p: "a" * p + "b" * p + "a" * p + "b" * p)) == "noncfl"
# the stack story for the nested word (top first): push a^i, push b^j, pop b^j with c^j, pop a^i with a^i -> empty
FR = [("$a^i$", ["$a^i$"]), ("$b^j$", ["$b^j$", "$a^i$"]), ("$c^j$", ["$a^i$"]), ("$a^i$", [])]
FRX = [("$a^i$", ["$a^i$"]), ("$b^j$", ["$b^j$", "$a^i$"]), ("$a^i$ ?", ["$b^j$", "$a^i$"])]

# ---------------------------------------------------------------- intersection: #a = #b = #c
L3 = lambda w: w.count("a") == w.count("b") == w.count("c")
ANBNCN = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(blocks(w, "abc"))
R1, R2 = rx("a*b*c*", "abc"), rx("(abc)*", "abc")
I1 = lambda w: L3(w) and R1.accepts(w)
assert same_pred(I1, ANBNCN, "abc", 7)
assert classify_cert(I1, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7) == "noncfl"
assert same_pred(lambda w: L3(w) and R2.accepts(w), R2.accepts, "abc", 7)          # ∩ (abc)* = (abc)*: regular

# ---------------------------------------------------------------- exam 25A-C-Q6: a^k b^k c^i d^k
EXL = lambda w: (lambda t: t is not None and t[0] == t[1] == t[3])(blocks(w, "abcd"))
Q = BANK["25A-C-Q6"]
assert CLS[classify_cert(EXL, "abcd", ("noncfl", lambda p: "a" * p + "b" * p + "d" * p), n=6)] == Q["correctId"] == "d"
RX = rx("a*b*d*", "abcd")
ABD = lambda w: (lambda t: t is not None and t[0] == t[1] == t[2])(blocks(w, "abd"))
assert same_pred(lambda w: EXL(w) and RX.accepts(w), ABD, "abcd", 7)              # L ∩ a*b*d* = {a^k b^k d^k}
assert all(pump_breaks_cf(ABD, "a" * p + "b" * p + "d" * p, p) for p in (2, 3, 4))
# the look-alike on the formula sheet: a^n b^m c^m d^n is nested (only the shape is quoted, not solved)
assert classify_cert(lambda w: (lambda t: t is not None and t[0] == t[3] and t[1] == t[2])(blocks(w, "abcd")),
                     "abcd", ("cfl", "S->aSd|T;T->bTc|ε"), n=6) == "cfl"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    Pk("בסרטון הזה נלמד להבדיל בין השוואות **מקוננות**, שמחסנית יודעת לבדוק, להשוואות **חוצות**, שהיא לא יודעת."),
    Pk("ונלמד להוכיח ששפה לא ח״ה, בעזרת חיתוך עם שפה רגולרית."),
    Pk("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">K05 · סיווג שפות</div><h1>חסרת הקשר מול לא חסרת הקשר: מקונן וחוצה</h1>'
         '<p>להבחין בין השוואות מקוננות (ח״ה) להשוואות חוצות או משולשות (לא ח״ה), ולהוכיח לא ח״ה בעזרת חיתוך עם שפה רגולרית.</p>',
   layout="title")

nested = Scene("nested", "מקונן", [
    Pk("מה אוטומט מחסנית יודע לבדוק? המחסנית עובדת ב-LIFO: מה שנדחף אחרון, נשלף ראשון.",
       say="מה אוטומט מחסנית יודע לבדוק? המחסנית עובדת בשיטת לִיפוֹ: מה שנדחף אחרון, נשלף ראשון.",
       do=show("n-lifo")),
    Pk("ניקח את $\\{a^ib^jc^ja^i\\}$. ה-$a$ בהתחלה מושוות ל-$a$ בסוף, וה-$b$ ל-$c$ באמצע.",
       say="ניקח את השפה אֵיי אַיי, בִּי גֵ'יי, סִי גֵ'יי, אֵיי אַיי. האֵיי בהתחלה מושוות לאֵיי בסוף, והבִּי לסִי באמצע.",
       do=show("na", "na-a-0", "na-a-1")),
    Pk("הקשתות לא חוצות זו את זו: אחת בתוך השנייה, כמו סוגריים. זה **מקונן**.", do=show("n-rule")),
    Pk("נריץ מחסנית: קוראים $a^i$ ודוחפים.", say="נריץ מחסנית: קוראים אֵיי אַיי, ודוחפים.", do=show("ns-f-0")),
    Pk("קוראים $b^j$, ודוחפים מעליהן.", say="קוראים בִּי גֵ'יי, ודוחפים מעליהן.", do=show("ns-f-1")),
    Pk("קוראים $c^j$: ה-$b$ בראש המחסנית, ושולפים אחת לכל $c$.",
       say="קוראים סִי גֵ'יי: הבִּי בראש המחסנית, ושולפים אחת לכל סִי.", do=show("ns-f-2")),
    Pk("ועכשיו ה-$a$ שוב בראש, וה-$a$ האחרונות שולפות אותן. המחסנית ריקה, ומגיעים למצב מקבל.",
       say="ועכשיו האֵיי שוב בראש, והאֵיי האחרונות שולפות אותן. המחסנית ריקה, ומגיעים למצב מקבל.",
       do=show("ns-f-3")),
    Pk("זכרו: בקורס מילה מתקבלת רק במצב מקבל **וגם** מחסנית ריקה. השפה ח״ה.",
       do=show("n-acc"), hold=0.5),
], stage=CSS + '<div id="na" class="h">' + arcs("na", ["$a^i$", "$b^j$", "$c^j$", "$a^i$"], [(0, 3), (1, 2)]) + '</div>'
         + stack("ns", FR),
   panel=st.card("n-lifo", "plain", "<b>LIFO</b>: נדחף אחרון, נשלף ראשון")
       + st.card("n-rule", "rule", "🔑 <b>מקונן</b>, נסגר בסדר הפוך לפתיחה: ח״ה")
       + st.card("n-acc", "plain", "מתקבלת = מצב מקבל <b>וגם</b> מחסנית ריקה"))

crossing = Scene("crossing", "חוצה", [
    Pk("עכשיו נחליף את הסדר: $\\{a^ib^ja^ib^j\\}$. ה-$a$ מושוות ל-$a$, וה-$b$ ל-$b$.",
       say="עכשיו נחליף את הסדר: אֵיי אַיי, בִּי גֵ'יי, אֵיי אַיי, בִּי גֵ'יי. האֵיי מושוות לאֵיי, והבִּי לבִּי.",
       do=show("ca", "ca-a-0", "ca-a-1")),
    Pk("הקשתות **חוצות**: הזוג השני נפתח לפני שהראשון נסגר, ונסגר אחריו.", do=show("c-rule")),
    Pk("במחסנית: דחפנו $a^i$ ואז $b^j$. עכשיו צריך להשוות את ה-$a$, אבל הן קבורות מתחת ל-$b$.",
       say="במחסנית: דחפנו אֵיי אַיי ואז בִּי גֵ'יי. עכשיו צריך להשוות את האֵיי, אבל הן קבורות מתחת לבִּי.",
       do=show("cs-f-0", "cs-f-1", "cs-f-2")),
    Pk("אם נשלוף את ה-$b$ כדי להגיע אליהן, נשכח כמה $b$ היו. זו האינטואיציה לכך שהשפה לא ח״ה.",
       say="אם נשלוף את הבִּי כדי להגיע אליהן, נשכח כמה בִּי היו. זו האינטואיציה לכך שהשפה לא חסרת הקשר.", do=show("c-no")),
    Pk("ההוכחה: למת הניפוח לח״ה, או טבלת השפות בדף הנוסחאות.", do=hide("ca", "cs-f-0", "cs-f-1", "cs-f-2") + show("tab")),
    Pk("$a^nb^mc^md^n$ מקונן: ח״ה. $a^nb^mc^nd^m$ חוצה: לא ח״ה.",
       say="אֵיי אֶן בִּי אֶם סִי אֶם דִּי אֶן, מקונן: חסרת הקשר. אֵיי אֶן בִּי אֶם סִי אֶן דִּי אֶם, חוצה: לא חסרת הקשר.",
       do=show("tab-1")),
    Pk("$uu^R$ מקונן: ח״ה. $uu$ חוצה: לא ח״ה. ו-$a^nb^nc^n$, שלוש כמויות בבת אחת: לא ח״ה.",
       say="יוּ יוּ הפוך, מקונן: חסרת הקשר. יוּ יוּ, חוצה: לא חסרת הקשר. ואֵיי אֶן בִּי אֶן סִי אֶן, שלוש כמויות בבת אחת: לא חסרת הקשר.",
       do=show("tab-2", "tab-3")),
    Pk("את הרשימה הזאת מותר לצטט בלי הוכחה. כל שפה אחרת מנסים לפרק אליה.", do=show("c-cite"), hold=0.5),
], stage=CSS + '<div class="swap" style="--swap-h:640px">'
         + '<div id="ca" class="h">' + arcs("ca", ["$a^i$", "$b^j$", "$a^i$", "$b^j$"], [(0, 2), (1, 3)])
         + stack("cs", FRX) + '</div>'
         + '<div id="tab" class="h"><table class="kl-grid" dir="ltr"><thead><tr><th>ח״ה, לא רגולרית</th><th>לא ח״ה</th></tr></thead><tbody>'
         + '<tr id="tab-1" class="h"><td>$a^nb^mc^md^n$</td><td>$a^nb^mc^nd^m$</td></tr>'
         + '<tr id="tab-2" class="h"><td>$uu^R$</td><td>$uu$</td></tr>'
         + '<tr id="tab-3" class="h"><td>$a^nb^n$</td><td>$a^nb^nc^n$</td></tr></tbody></table></div>'
         + '</div>',
   panel=st.card("c-rule", "rule", "🔑 <b>חוצה</b>, נסגר באותו סדר שנפתח: לא ח״ה")
       + st.card("c-no", "plain", "ה-$a$ קבורות מתחת ל-$b$")
       + st.card("c-cite", "rule", "🔑 שפות דף הנוסחאות: מצטטים בלי הוכחה"))

inter = Scene("inter", "חיתוך עם רגולרית", [
    Pk("איך מוכיחים לא ח״ה בלי לנפח? ח״ה סגורות לחיתוך **עם שפה רגולרית**.", do=show("i-rule")),
    Pk("אם $L$ ח״ה ו-$R$ רגולרית, אז $L\\cap R$ ח״ה. לכן אם החיתוך לא ח״ה, גם $L$ לא ח״ה.",
       say="אם אֶל חסרת הקשר, ואַר רגולרית, אז אֶל חיתוך אַר חסרת הקשר. לכן אם החיתוך לא חסר הקשר, גם אֶל לא חסרת הקשר."),
    Pk("דוגמה: המילים מעל $a$, $b$, $c$ שבהן $\\#_a=\\#_b=\\#_c$. האותיות מעורבבות, וקשה לנפח.",
       say="דוגמה: המילים מעל אֵיי, בִּי וסִי, שבהן מספר האֵיי, מספר הבִּי ומספר הסִי שווים. האותיות מעורבבות, וקשה לנפח.",
       do=show("i-1")),
    Pk("נחתוך עם $a^*b^*c^*$, שמסדרת את האותיות בגושים. נשאר בדיוק $\\{a^nb^nc^n\\}$.",
       say="נחתוך עם אֵיי כוכבית, בִּי כוכבית, סִי כוכבית, שמסדרת את האותיות בגושים. נשאר בדיוק אֵיי אֶן בִּי אֶן סִי אֶן.",
       do=show("i-2")),
    Pk("והיא מדף הנוסחאות: לא ח״ה. לכן גם השפה המקורית לא ח״ה.", do=show("i-ok")),
    Pk("המלכודת: עם $(abc)^*$ החיתוך הוא $(abc)^*$ עצמה, רגולרית. זה לא מוכיח כלום.",
       say="המלכודת: עם אֵיי בִּי סִי, כוכבית, החיתוך הוא אֵיי בִּי סִי כוכבית עצמה, רגולרית. זה לא מוכיח כלום.",
       do=show("i-3", "i-trap")),
    Pk("בחירת $R$ היא כל העניין: היא צריכה להשאיר שפה לא ח״ה **ידועה**.",
       say="בחירת אַר היא כל העניין: היא צריכה להשאיר שפה לא חסרת הקשר ידועה.", hold=0.5),
], stage=CSS + '<div id="i-1" class="kl-line kl-big h">$L:\\ \\#_a=\\#_b=\\#_c$</div>'
         + '<div id="i-2" class="kl-line kl-big h">$L\\cap a^*b^*c^*=\\{a^nb^nc^n\\}$</div>'
         + '<div id="i-3" class="kl-line h">$L\\cap(abc)^*=(abc)^*$</div>',
   panel=st.card("i-rule", "rule", "🔑 אם $L$ ח״ה ו-$R$ רגולרית, אז $L\\cap R$ ח״ה")
       + st.card("i-ok", "rule", "🔑 אם $L\\cap R$ לא ח״ה, אז $L$ לא ח״ה")
       + st.card("i-trap", "trap", "⚠️ חיתוך שיוצא ח״ה או רגולרי לא מוכיח כלום"))

exam = Scene("exam", "שאלה ממבחן", [
    Pk("ועכשיו שאלה אמיתית ממבחן: $L=\\{a^kb^kc^id^k\\}$.",
       say="ועכשיו שאלה אמיתית ממבחן: אֶל היא אֵיי קֵיי, בִּי קֵיי, סִי אַיי, דִּי קֵיי.",
       do=show("ea", "ea-a-0", "ea-a-1")),
    Pk("המלכודת: היא נראית כמו $a^nb^mc^md^n$ מדף הנוסחאות, ה-$a$ עוטפים וה-$d$ סוגרים. אז בוחרים ח״ה.",
       say="המלכודת: היא נראית כמו אֵיי אֶן בִּי אֶם סִי אֶם דִּי אֶן מדף הנוסחאות: האֵיי עוטפות והדִּי סוגרות. אז בוחרים חסרת הקשר.",
       do=show("x-trap")),
    Pk("אבל תסתכלו על הקשתות: אותו $k$ מופיע **שלוש** פעמים. $a$ מול $b$, וגם $a$ מול $d$. וה-$c$ חופשיים.",
       say="אבל תסתכלו על הקשתות: אותו קֵיי מופיע שלוש פעמים. אֵיי מול בִּי, וגם אֵיי מול דִּי. והסִי חופשיות.",
       do=hide("x-trap")),
    Pk("נחתוך עם $a^*b^*d^*$: זה פשוט מוחק את ה-$c$. נשאר $\\{a^kb^kd^k\\}$.",
       say="נחתוך עם אֵיי כוכבית, בִּי כוכבית, דִּי כוכבית: זה פשוט מוחק את הסִי. נשאר אֵיי קֵיי, בִּי קֵיי, דִּי קֵיי.",
       do=show("e-1")),
    Pk("זה בדיוק $a^nb^nc^n$ עם שם אחר לאות השלישית: לא ח״ה. ולכן $L$ לא ח״ה.",
       say="זה בדיוק אֵיי אֶן בִּי אֶן סִי אֶן, עם שם אחר לאות השלישית: לא חסרת הקשר. ולכן אֶל לא חסרת הקשר.",
       do=show("e-2")),
    Pk("סופית ורגולרית נפסלות מיד: אם $L$ הייתה רגולרית, היא הייתה גם ח״ה.",
       say="סופית ורגולרית נפסלות מיד: אם אֶל הייתה רגולרית, היא הייתה גם חסרת הקשר.",
       do=show("q-x-a", "q-n-a", "q-x-b", "q-n-b")),
    Pk("וח״ה ולא רגולרית נפסלת בגלל החיתוך.", do=show("q-x-c", "q-n-c")),
    Pk("התשובה: לא ח״ה. לפני שמחליטים ״מקונן״, סופרים כמה פעמים כל מונה מופיע.",
       say="התשובה: לא חסרת הקשר. לפני שמחליטים מקונן, סופרים כמה פעמים כל מונה מופיע.",
       do=show("q-ok-d"), hold=0.6),
], stage=CSS + '<div id="ea" class="h">' + arcs("ea", ["$a^k$", "$b^k$", "$c^i$", "$d^k$"], [(0, 1), (0, 3)]) + '</div>'
         + '<div id="e-1" class="kl-line kl-big h">$L\\cap a^*b^*d^*=\\{a^kb^kd^k\\}$</div>'
         + st.verdict("e-2", False, no="לא ח״ה").replace('id="e-2-v"', 'id="e-2"')
         + st.card("x-trap", "trap", "⚠️ נראה כמו $a^nb^mc^md^n$, אבל $k$ מושווה <b>שלוש</b> פעמים"),
   panel=opts_panel("q", Q, notes={"a": "אינסופית", "b": "לא ח״ה", "c": "החיתוך לא ח״ה"}))

recap = Scene("recap", "סיכום", [
    Pk("לסיכום: מחסנית בודקת השוואות **מקוננות**, שנסגרות בסדר הפוך לפתיחה.", do=show("c1")),
    Pk("השוואות **חוצות**, או שלוש כמויות בבת אחת: לא ח״ה.", do=show("c2")),
    Pk("כדי להוכיח לא ח״ה: חותכים עם שפה רגולרית שמסדרת גושים, ומגיעים לשפה מדף הנוסחאות.", do=show("c3")),
    Pk("ולפני ״מקונן״, סופרים כמה פעמים כל מונה מופיע. נתראה ברמה הבאה.",
       say="ולפני שאומרים מקונן, סופרים כמה פעמים כל מונה מופיע. נתראה ברמה הבאה.", do=show("c4"), hold=0.8),
], stage=CSS + arcs("ra", ["$a^i$", "$b^j$", "$c^j$", "$a^i$"], [(0, 3), (1, 2)]).replace('kl-arc h"', 'kl-arc"')
         + arcs("rb", ["$a^i$", "$b^j$", "$a^i$", "$b^j$"], [(0, 2), (1, 3)]).replace('kl-arc h"', 'kl-arc"'),
   panel=st.card("c1", "rule", "🔑 מקונן: ח״ה")
       + st.card("c2", "rule", "🔑 חוצה, או שלוש כמויות בבת אחת: לא ח״ה")
       + st.card("c3", "rule", "🔑 אם $L\\cap R$ לא ח״ה, אז $L$ לא ח״ה")
       + st.card("c4", "trap", "⚠️ סופרים כמה פעמים כל מונה מופיע"))

VIDEO = Video("K05", "classify", "חסרת הקשר מול לא חסרת הקשר: מקונן וחוצה",
              [title, nested, crossing, inter, exam, recap],
              bank={"25A-C-Q6": "d"})
