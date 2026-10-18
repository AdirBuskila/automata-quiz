# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def R(pred, alpha):
    return rank_stable(pred, alpha, 9, (5, 6, 7))


def proof(pred, alpha, claim, T):
    """a valid 'Rank = claim because T separates' argument: T separating, |T| = claim = the true Rank"""
    return R(pred, alpha) == claim and len(T) == claim and is_separating_set(pred, T, alpha, 8)


AOB = lambda w: w.startswith("a") or w.endswith("b")
MOD3 = lambda w: w.count("1") % 3 == 0
EVEN2 = lambda w: w.count("0") % 2 == 0 and w.count("1") % 2 == 0
FIN3 = lambda w: w in {"a", "aa", "aaa"}
assert R(AOB, "ab") == 4 and R(MOD3, "01") == 3 and R(EVEN2, "01") == 4 and R(FIN3, "ab") == 5


LEVEL = level("N04", 4, "🧷", "להוכיח Rank = k: אס״ד וגם קבוצה מפרידה",
  "לבדוק אם נימוק של Rank = k שלם: צריך חסם עליון (אס״ד) וחסם תחתון (קבוצה מפרידה בגודל k).",
  r'''
<p>שאלה טיפוסית (23A-B-Q11, 19B-A-Q9, 26A-A-Q1): &quot;איזה נימוק נכון להוכחה ש-$\mathrm{Rank}(L)=k$?&quot; לכל אפשרות יש מספר ו-$T$, ורק אחת שלמה.</p>
<h3>המתכון</h3>
<ul>
<li><b>חסם עליון ($\mathrm{Rank}\le k$):</b> אס״ד <b>מלא</b> (כולל מצב מלכודת) עם $k$ מצבים.</li>
<li><b>חסם תחתון ($\mathrm{Rank}\ge k$):</b> קבוצה מפרידה $T$ עם $|T|=k$, ולכל זוג ב-$T$ סיפא מפרידה.</li>
</ul>
<div class="lesson-trap">⚠️ <b>צריך את שניהם.</b> אס״ד בגודל $k$ בלבד לא מוכיח כלום (אולי הוא לא מינימלי). קבוצה מפרידה בגודל $k-1$ מוכיחה רק $\mathrm{Rank}\ge k-1$, גם אם המספר $k$ נכון.</div>
<h3>בדיקה של אפשרות במבחן, בשלוש שאלות</h3>
<ol>
<li>האם המספר נכון?</li>
<li>האם $|T|$ <b>שווה</b> אליו?</li>
<li>האם <b>כל זוג</b> ב-$T$ ניתן להפרדה? מספיק זוג שקול אחד כדי לפסול.</li>
</ol>
<div class="lesson-ex"><b>דוגמה (23A-B-Q11).</b> $L$ = מתחילה ב-$a$ <b>או</b> נגמרת ב-$b$. נכון: $\mathrm{Rank}=4$ ו-$T=\{\varepsilon,a,b,ba\}$ (ארבעת הנציגים: &quot;עוד כלום&quot;, &quot;התחיל ב-$a$&quot;, &quot;התחיל ב-$b$ ונגמר ב-$b$&quot;, &quot;התחיל ב-$b$ ונגמר ב-$a$&quot;). אבל $T=\{\varepsilon,a,b,ab\}$ נופלת: $a\equiv ab$, כי שתיהן מתחילות ב-$a$ וכל המשך נשאר בשפה.</div>
<h3>קבוצות מפרידות לפי &quot;מה נשאר לזכור&quot;</h3>
<ul>
<li>שאריות: מילים עם שאריות שונות. ב-21S-A-Q9 (סכום ספרות מודולו $3$) $\{00,11,22\}$ מפרידה (שאריות $0,2,1$), אבל $\{\varepsilon,11,111\}$ לא ($\varepsilon\equiv111$, שתיהן שארית $0$).</li>
<li>שפה סופית: מוסיפים נציג של המלכודת. ב-19B-A-Q9 הנציג הוא $aaab$, ולכן $T=\{\varepsilon,a,aa,aaa,aaab\}$.</li>
<li>אם יש אפשרות עם קבוצה <b>אינסופית</b> לשפה שבנית לה אס״ד, פסלו אותה מיד.</li>
</ul>
''',
  [
    Q(r"$L$ היא שפת המילים מעל $\{a,b\}$ שמתחילות ב-$a$ **או** נגמרות ב-$b$. איזה נימוק מוכיח נכון ש-$\mathrm{Rank}(L)$ הוא מה שנאמר?",
      [C(r"$\mathrm{Rank}(L)=4$ וקבוצה מפרידה $T=\{\varepsilon,a,b,ba\}$", proof(AOB, "ab", 4, ["", "a", "b", "ba"])),
       C(r"$\mathrm{Rank}(L)=4$ וקבוצה מפרידה $T=\{\varepsilon,a,b,ab\}$", proof(AOB, "ab", 4, ["", "a", "b", "ab"])),
       C(r"$\mathrm{Rank}(L)=4$ וקבוצה מפרידה $T=\{\varepsilon,a,b\}$", proof(AOB, "ab", 4, ["", "a", "b"])),
       C(r"$\mathrm{Rank}(L)=3$ וקבוצה מפרידה $T=\{\varepsilon,a,b\}$", proof(AOB, "ab", 3, ["", "a", "b"]))],
      why=r"$\mathrm{Rank}=4$ (חישבנו). ב-$\{\varepsilon,a,b,ba\}$ כל ארבע המילים נבדלות. ב-$\{\varepsilon,a,b,ab\}$ יש $a\equiv ab$, ולכן היא לא מפרידה. $T$ בגודל $3$ מוכיחה רק $\mathrm{Rank}\ge3$, ו-&quot;$\mathrm{Rank}=3$&quot; פשוט לא נכון (קיימת $T$ בגודל $4$).",
      recap="מספר נכון, |T| שווה לו, וכל זוג ב-T מופרד"),
    Q(r"$L$ היא שפת המילים מעל $\{0,1\}$ שמספר ה-$1$ בהן מתחלק ב-$3$. איזו קבוצה מפרידה ובגודל $3$?",
      [C(r"$\{\varepsilon,1,11\}$", is_separating_set(MOD3, ["", "1", "11"], "01")),
       C(r"$\{\varepsilon,1,111\}$", is_separating_set(MOD3, ["", "1", "111"], "01")),
       C(r"$\{0,00,000\}$", is_separating_set(MOD3, ["0", "00", "000"], "01")),
       C(r"$\{1,01,101\}$", is_separating_set(MOD3, ["1", "01", "101"], "01"))],
      why=r"המצב הוא השארית של מספר ה-$1$ מודולו $3$. $\{\varepsilon,1,11\}$ נותנת שאריות $0,1,2$ שונות. ב-$\{\varepsilon,1,111\}$ יש $\varepsilon\equiv111$ (שתיהן שארית $0$). ב-$\{0,00,000\}$ כולן שארית $0$. ב-$\{1,01,101\}$: $1\equiv01$ (שארית $1$).",
      recap="שאריות שונות = מילים שונות ב-T"),
    Q(r"מה צריך כדי להוכיח ש-$\mathrm{Rank}(L)=k$?",
      [J(r"אס״ד מלא עם $k$ מצבים **וגם** קבוצה מפרידה בגודל $k$", True),
       J(r"מספיק אס״ד מלא עם $k$ מצבים", False),
       J(r"מספיקה קבוצה מפרידה בגודל $k$", False),
       J(r"מספיקה קבוצה מפרידה אינסופית", False)],
      why=r"האס״ד נותן $\mathrm{Rank}\le k$ והקבוצה המפרידה נותנת $\mathrm{Rank}\ge k$, ורק יחד הם נותנים שוויון. אס״ד בגודל $k$ יכול להיות לא מינימלי. קבוצה מפרידה בגודל $k$ בלבד מוכיחה רק $\ge k$. קבוצה מפרידה אינסופית מוכיחה ש-$L$ **לא** רגולרית, כלומר ש-$\mathrm{Rank}$ אינסופי.",
      recap="חסם עליון ותחתון, שניהם"),
    Q(r"$L=\{a,aa,aaa\}$ מעל $\{a,b\}$. איזו קבוצה היא **מפרידה** ובגודל $5$?",
      [C(r"$\{\varepsilon,a,aa,aaa,aaab\}$", is_separating_set(FIN3, ["", "a", "aa", "aaa", "aaab"], "ab")),
       C(r"$\{\varepsilon,a,aaaa,aaab,b\}$", is_separating_set(FIN3, ["", "a", "aaaa", "aaab", "b"], "ab")),
       C(r"$\{\varepsilon,a,aa,b,bb\}$", is_separating_set(FIN3, ["", "a", "aa", "b", "bb"], "ab")),
       C(r"$\{aa,aaa,aaaa,b,ba\}$", is_separating_set(FIN3, ["aa", "aaa", "aaaa", "b", "ba"], "ab"))],
      why=r"ארבע מחלקות רגילות ($\varepsilon,a,aa,aaa$ שונות) ועוד המלכודת, שהנציג שלה הוא $aaab$ (אין לה המשך בשפה). באפשרויות האחרות יש מילים שנופלות לאותה מלכודת ($aaaa\equiv aaab\equiv b$, $b\equiv bb$, $aaaa\equiv b$), ולכן הקבוצה לא מפרידה.",
      recap="שפה סופית: מוסיפים נציג של המלכודת"),
    Q(r"$L$ היא שפת המילים מעל $\{0,1\}$ שמספר ה-$0$ **וגם** מספר ה-$1$ בהן זוגיים. איזו קבוצה מוכיחה $\mathrm{Rank}(L)\ge4$?",
      [C(r"$\{\varepsilon,0,1,01\}$", len(["", "0", "1", "01"]) == 4 and is_separating_set(EVEN2, ["", "0", "1", "01"], "01")),
       C(r"$\{\varepsilon,00,11,0011\}$", is_separating_set(EVEN2, ["", "00", "11", "0011"], "01")),
       C(r"$\{0,1,01,10\}$", is_separating_set(EVEN2, ["0", "1", "01", "10"], "01")),
       C(r"$\{\varepsilon,0,1\}$", len(["", "0", "1"]) >= 4 and is_separating_set(EVEN2, ["", "0", "1"], "01"))],
      why=r"נציגי ארבע הזוגיויות (זוגי/זוגי, אי-זוגי/זוגי, זוגי/אי-זוגי, אי-זוגי/אי-זוגי) הם $\varepsilon,0,1,01$, והם מופרדים. $\{\varepsilon,00,11,0011\}$: כולן זוגי/זוגי. ב-$\{0,1,01,10\}$: $01\equiv10$. $\{\varepsilon,0,1\}$ מפרידה אבל בגודל $3$ ולכן מוכיחה רק $\ge3$.",
      recap="Rank ≥ k דורש T מפרידה בגודל k"),
  ])
