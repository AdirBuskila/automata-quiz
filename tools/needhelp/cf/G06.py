# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def P(letters, cond):
    return lambda w: (lambda t: t is not None and cond(*t))(parts(w, letters))


def lang_is(pda, alpha, pred, n):
    return pda.lang(alpha, n) == {w for w in words(alpha, n) if pred(w)}


# Q1  a pushes, b pops, c ignores the stack
M1 = PDA([("0", "a", "", "0", "X"), ("0", "", "", "1", ""), ("1", "b", "X", "1", ""), ("1", "", "", "2", ""), ("2", "c", "", "2", "")],
         "0", {"2"})
O1 = {"a^n b^n c^k": P("abc", lambda a, b, c: a == b), "a^n b^k c^n": P("abc", lambda a, b, c: a == c),
      "a^n b^n c^n": P("abc", lambda a, b, c: a == b == c), "a^n b^k c^k": P("abc", lambda a, b, c: b == c)}
T1 = {k: lang_is(M1, "abc", p, 8) for k, p in O1.items()}
assert T1 == {"a^n b^n c^k": True, "a^n b^k c^n": False, "a^n b^n c^n": False, "a^n b^k c^k": False}, T1
# Q2  nested: a pushes 1, b pushes 2, c pops 2, d pops 1
M2 = PDA([("0", "a", "", "0", "1"), ("0", "", "", "1", ""), ("1", "b", "", "1", "2"), ("1", "", "", "2", ""), ("2", "c", "2", "2", ""),
          ("2", "", "", "3", ""), ("3", "d", "1", "3", "")], "0", {"3"})
O2 = {"nested": P("abcd", lambda a, b, c, d: a == d and b == c), "crossing": P("abcd", lambda a, b, c, d: a == c and b == d),
      "a=b,c=d": P("abcd", lambda a, b, c, d: a == b and c == d), "all equal": P("abcd", lambda a, b, c, d: a == b == c == d)}
T2 = {k: lang_is(M2, "abcd", p, 7) for k, p in O2.items()}
assert T2 == {"nested": True, "crossing": False, "a=b,c=d": False, "all equal": False}, T2
# Q3  a may or may not push, b pops
M3 = PDA([("0", "a", "", "0", "A"), ("0", "a", "", "0", ""), ("0", "", "", "1", ""), ("1", "b", "A", "1", "")], "0", {"1"})
O3 = {"n<=i": P("ab", lambda i, n: n <= i), "n>=i": P("ab", lambda i, n: n >= i), "n=i": P("ab", lambda i, n: n == i),
      "n<i": P("ab", lambda i, n: n < i)}
T3 = {k: lang_is(M3, "ab", p, 8) for k, p in O3.items()}
assert T3 == {"n<=i": True, "n>=i": False, "n=i": False, "n<i": False}, T3
# Q4  b may skip the pop
M4 = PDA([("0", "a", "", "0", "A"), ("0", "", "", "1", ""), ("1", "b", "A", "1", ""), ("1", "b", "", "1", "")], "0", {"1"})
O4 = {"n>=i": P("ab", lambda i, n: n >= i), "n<=i": P("ab", lambda i, n: n <= i), "n=i": P("ab", lambda i, n: n == i),
      "n>i": P("ab", lambda i, n: n > i)}
T4 = {k: lang_is(M4, "ab", p, 8) for k, p in O4.items()}
assert T4 == {"n>=i": True, "n<=i": False, "n=i": False, "n>i": False}, T4
# Q5  a marker Z at the bottom
M5 = PDA([("0", "", "", "1", "Z"), ("1", "a", "", "1", "A"), ("1", "", "", "3", ""), ("3", "b", "A", "3", ""), ("3", "b", "Z", "2", "")],
         "0", {"2"})
O5 = {"k,k+1": P("ab", lambda a, b: b == a + 1), "k,k": P("ab", lambda a, b: a == b), "k+1,k": P("ab", lambda a, b: a == b + 1),
      "k,k+2": P("ab", lambda a, b: b == a + 2)}
T5 = {k: lang_is(M5, "ab", p, 8) for k, p in O5.items()}
assert T5 == {"k,k+1": True, "k,k": False, "k+1,k": False, "k,k+2": False}, T5

LEVEL = level("G06", 6, "🔍", "מהי L(M)? משוואת איזון",
  "למצוא את השפה של אוטומט מחסנית לפי סדר המצבים ומשוואת האיזון של דחיפות ושליפות.",
  r'''
<p>שמונה שאלות בבנק שואלות &quot;מהי $L(M)$?&quot; (19B-A-Q25, 19B-B-Q25, 21S-A-Q25, 21S-B-Q23, 23A-A-Q25, 23A-B-Q25, 25A-B-Q9, SAMP-19-Q25).</p>
<h3>שיטה</h3>
<ol>
<li><b>סדר המצבים הוא סדר האותיות.</b> שרשרת $q_0\to q_1\to q_2$ עם לולאות $a$, $b$, $c$ נותנת מילים מהצורה $a^*b^*c^*$.</li>
<li><b>כתבו משוואת איזון:</b> לכל אות, כמה היא דוחפת ($+$) וכמה שולפת ($-$). המחסנית ריקה בסוף אם ורק אם הסכום $0$.</li>
<li>אות שלא נוגעת במחסנית: המספר שלה <b>חופשי</b>.</li>
<li>פסלו מסיחים במילים קטנות מהשפה שלכם שאינן בהם, ולהפך.</li>
</ol>
<table dir="ltr"><thead><tr><th>דחיפה / שליפה</th><th>$L(M)$</th><th>שאלה</th></tr></thead><tbody>
<tr><td>$a$: $+1$ · $b$: $-1$ · $c$: $-1$</td><td>$a^ib^nc^k$, $i=n+k$</td><td>23A-B-Q25, 21S-B-Q23</td></tr>
<tr><td>$a$: $+1$ <b>או</b> $0$ · $b$: $-1$ · $c$: $0$</td><td>$a^ib^nc^k$, $i\ge n$ ($k$ חופשי)</td><td>19B-A-Q25</td></tr>
<tr><td>$a$ דוחף $1$ · $b$ דוחף $2$ · $c$ שולף $2$ · $d$ שולף $1$</td><td>$a^ib^jc^jd^i$ (מקונן)</td><td>SAMP-19-Q25</td></tr>
<tr><td>$\varepsilon$ דוחף $Z$ · $a$: $+1$ · $b$: $-1$ · $b$ אחרון שולף $Z$</td><td>$a^kb^{k+1}$</td><td>25A-B-Q9</td></tr>
<tr><td>אין דחיפה של $b$</td><td>$a^*$</td><td>23A-A-Q25</td></tr></tbody></table>
<div class="lesson-trap">⚠️ <b>שתי קשתות על אותה אות</b> (אחת דוחפת ואחת לא) פירושן אי-שוויון: &quot;לא חייבים לדחוף על כל $a$&quot; נותן $i\ge n$ ולא $i=n$ (19B-A-Q25). תחשבו &quot;לפחות&quot; או &quot;לכל היותר&quot;.</div>
<div class="lesson-ex"><b>בדיקה עם מילה קטנה (21S-B-Q23).</b> התשובה $a^nb^kc^{n-k}$ והמסיח $a^nb^{n+k}c^k$ נראים דומים. עם $bc$: לפי המסיח היא בשפה ($n=0,k=1$), אבל באוטומט אין $a$ לשלוף, ולכן לא.</div>
''',
  [
    Q("באוטומט מחסנית: " + pda_info(M1) + " (האות $a$ דוחפת $X$, האות $b$ שולפת $X$, והאות $c$ לא נוגעת במחסנית). מהי $L(M)$?",
      [C(f"${k.replace(' ', '')}$".replace("^n", "^{n}"), T1[k]) for k in O1],
      why=r"קודם קוראים $a$-ים ודוחפים, אחר כך $b$-ים ושולפים, ולבסוף $c$-ים בלי להשפיע על המחסנית. המחסנית ריקה אם ורק אם מספר ה-$b$ שווה למספר ה-$a$, ולכן $a^nb^nc^k$ ($k$ חופשי). בדקנו על כל המילים עד אורך $8$.",
      recap="אות שלא נוגעת במחסנית: מספרה חופשי", table=pda_tab(M1)),
    Q("באוטומט מחסנית: " + pda_info(M2) + " מהי $L(M)$?",
      [C(r"$\{a^ib^jc^jd^i\}$ (מקונן)", T2["nested"]), C(r"$\{a^ib^jc^id^j\}$ (חוצה)", T2["crossing"]),
       C(r"$\{a^ib^ic^jd^j\}$", T2["a=b,c=d"]), C(r"$\{a^ib^ic^id^i\}$", T2["all equal"])],
      why=r"$a$ דוחף $1$, $b$ דוחף $2$, $c$ שולף $2$, $d$ שולף $1$. $c$ חייב לשלוף את מה שנדחף אחרון, כלומר $2$ ($j$ פעמים), ואחריו $d$ שולף $1$ ($i$ פעמים). המחסנית ריקה כש-$c$ כמספר ה-$b$ ו-$d$ כמספר ה-$a$: מקונן. בדקנו עד אורך $7$.",
      recap="LIFO: מה שנדחף אחרון נשלף ראשון", table=pda_tab(M2)),
    Q("באוטומט מחסנית: " + pda_info(M3) + " על האות $a$ יש <b>שתי</b> קשתות (אחת דוחפת $A$ ואחת לא). מהי $L(M)$ (מילים $a^ib^n$)?".replace("<b>", "**").replace("</b>", "**"),
      [C(r"$\{a^ib^n\mid n\le i\}$", T3["n<=i"]), C(r"$\{a^ib^n\mid n\ge i\}$", T3["n>=i"]),
       C(r"$\{a^ib^n\mid n=i\}$", T3["n=i"]), C(r"$\{a^ib^n\mid n<i\}$", T3["n<i"])],
      why=r"לא חייבים לדחוף על כל $a$: אפשר לדחוף רק על חלק מהן. כל $b$ שולף אחד, והמחסנית ריקה כשמספר הדחיפות שווה ל-$n$. מספר הדחיפות יכול להיות כל מספר בין $0$ ל-$i$, ולכן $n\le i$ ($n=i$ כולל). בדקנו עד אורך $8$.",
      recap="שתי קשתות על אות: אי-שוויון (לפחות / לכל היותר)", table=pda_tab(M3)),
    Q("באוטומט מחסנית: " + pda_info(M4) + " על האות $b$ יש שתי קשתות (אחת שולפת $A$ ואחת לא). מהי $L(M)$ (מילים $a^ib^n$)?",
      [C(r"$\{a^ib^n\mid n\ge i\}$", T4["n>=i"]), C(r"$\{a^ib^n\mid n\le i\}$", T4["n<=i"]),
       C(r"$\{a^ib^n\mid n=i\}$", T4["n=i"]), C(r"$\{a^ib^n\mid n>i\}$", T4["n>i"])],
      why=r"כל $a$ דוחף $A$ ($i$ דחיפות). ה-$b$ יכולים לשלוף אותו או לא, ולכן צריך לפחות $i$ שליפות כדי לרוקן, ובנוסף $b$-ים עודפים: $n\ge i$ (כולל שוויון). בדקנו עד אורך $8$.",
      recap="b עם אפשרות לא לשלוף: n ≥ i", table=pda_tab(M4)),
    Q("באוטומט מחסנית: " + pda_info(M5) + " מהי $L(M)$?",
      [C(r"$\{a^kb^{k+1}\mid k\ge0\}$", T5["k,k+1"]), C(r"$\{a^kb^k\mid k\ge0\}$", T5["k,k"]),
       C(r"$\{a^{k+1}b^k\mid k\ge0\}$", T5["k+1,k"]), C(r"$\{a^kb^{k+2}\mid k\ge0\}$", T5["k,k+2"])],
      why=r"קודם דוחפים סימן תחתית $Z$ (במסע $\varepsilon$), אחר כך $a$ דוחף $A$ ו-$b$ שולף $A$. ה-$b$ האחרון שולף את $Z$ ומגיע ל-$q_2$. בדיוק $k$ שליפות של $A$ ועוד אחת של $Z$: $b^{k+1}$, והמחסנית ריקה. בדקנו עד אורך $8$.",
      recap="סימן תחתית Z: שליפה אחת נוספת", table=pda_tab(M5)),
  ])
