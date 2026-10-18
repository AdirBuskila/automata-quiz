# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def abc(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w)
    return None if not m else tuple(len(g) for g in m.groups())


def ab(w):
    m = re.fullmatch(r"(a*)(b*)", w)
    return None if not m else tuple(len(g) for g in m.groups())


P1 = lambda w: abc(w) is not None and (abc(w)[0] == abc(w)[1] == abc(w)[2] or abc(w)[0] > 3)
K1 = classify(P1, "abc", ("reg", "ε+abc+aabbcc+aaabbbccc+aaaaa*b*c*"), n=7)
P2 = lambda w: w.count("0") % 3 == 1
K2 = classify(P2, "01", ("reg", "1*01*(01*01*01*)*"))
P3 = lambda w: ab(w) is not None and ab(w)[0] + 2 * ab(w)[1] <= 6
K3 = classify(P3, "ab", ("finite", 6))
P4 = lambda w: ab(w) is not None and ab(w)[0] - ab(w)[1] <= 2
K4 = classify(P4, "ab", ("cfl", "S->PT|TQ;P->ε|a|aa;T->aTb|ε;Q->bQ|ε"))
P5 = lambda w: "".join(sorted(w)) == w
K5 = classify(P5, "abc", ("reg", "a*b*c*"), n=7)
assert (K1, K2, K3, K4, K5) == ("reg", "reg", "finite", "cfl", "reg")

LEVEL = level("K02", 2, "🎭", "שפות שנראות קשות ובעצם רגולריות",
  "לזהות מתי ספירה היא בעצם זיכרון סופי: מודולו, עד קבוע, סכום חסום, תבנית קבועה, או &quot;או&quot; שבולע.".replace("&quot;", "״"),
  r'''
<p>חצי מהשאלות &quot;רגולרית ואינסופית&quot; נראות כמו שפות שצריכות לספור. המטרה בשלב הזה היא לזהות מתי הספירה <b>לא</b> דורשת זיכרון בלתי חסום.</p>
<h3>הסימנים שבהם השפה רגולרית</h3>
<table dir="ltr"><thead><tr><th>סימן</th><th>למה רגולרית</th><th>מהבחינות</th></tr></thead><tbody>
<tr><td>ספירה <b>מודולו</b></td><td>זוכרים רק שארית</td><td>25A-C-Q13, 24A-B-Q2</td></tr>
<tr><td>&quot;לפחות $k$&quot; / &quot;עד $k$&quot;</td><td>סופרים עד קבוע ועוצרים</td><td>25A-A-Q4, 24X-A-Q2</td></tr>
<tr><td>תבנית קבועה (גושים בסדר)</td><td>ביטוי רגולרי</td><td>24A-C-Q9, 24A-B-Q4</td></tr>
<tr><td>שרשור של רגולריות</td><td>סגירות</td><td>24A-B-Q12</td></tr>
<tr><td>&quot;או&quot; עם תנאי רחב</td><td>בולע את החלק הקשה</td><td>19B-B-Q18</td></tr></tbody></table>
<div class="lesson-ex"><b>דוגמה: המילים $a^ib^jc^k$ עם $i=j=k$ או $i>3$ (בנוסח של 19B-B-Q18).</b> החלק $i=j=k$ עם $i\le3$ הוא <b>סופי</b>: $\varepsilon,abc,aabbcc,aaabbbccc$. כל השאר הוא $aaaa\,a^*b^*c^*$, תבנית קבועה. סופי איחוד רגולרי הוא רגולרי, ולכן השפה רגולרית ואינסופית. הטרמינולוגיה $a^nb^nc^n$ בהגדרה היא רק הסחה.</div>
<h3>סכום חסום מול הפרש חסום</h3>
<div class="lesson-rule">🔑 <b>סכום חסום של מונים לא שליליים &rarr; סופית.</b> <b>הפרש חסום &rarr; בדרך כלל לא רגולרית</b> (24A-A-Q2). ב-$\{a^nb^m\mid n+3m\le2024\}$ גם $n$ וגם $m$ חסומים, ולכן השפה סופית ורגולרית. ב-$\{a^nb^m\mid n-3m\le2024\}$ ה-$n$ יכול לגדול כל עוד $m$ גדל איתו, וצריך לזכור את $n$: לא רגולרית.</div>
<div class="lesson-trap">⚠️ <b>שוויון או אי-שוויון בין שני מונים &rarr; לא רגולרית; מודולו &rarr; רגולרית.</b> $\#_0=5\cdot\#_1$ לא רגולרית (25A-C-Q13), אבל $\#_0\bmod5=3$ כן. ובמעל אות אחת: לא כל שפה היא רגולרית (ראשוניים, 21S-A-Q10).</div>
<p>ושני כללי פישוט: כוכבית של שפה שמכילה אות בודדת $a$ (מעל $\{a\}$) היא תמיד $a^*$ (25A-C-Q2), ושפה שהיא $\Sigma^*$ בתחפושת (24A-C-Q9: מילים עם ספרות ממוינות הן $0^*1^*\cdots9^*$) היא רגולרית.</p>
''',
  [
    Q(r"תהי $L$ שפת המילים $a^ib^jc^k$ שבהן $i=j=k$ או $i>3$. איזו טענה נכונה?", cls_opts(K1),
      why=r"החלק $i=j=k$ עם $i\le3$ סופי (ארבע מילים). כל מילה עם $i>3$ מתאימה לתבנית $aaaa\,a^*b^*c^*$. לכן $L=\varepsilon+abc+aabbcc+aaabbbccc+aaaaa^*b^*c^*$: רגולרית ואינסופית. אומתה על כל המילים עד אורך $7$.",
      recap="או שבולע: חלק סופי וחלק רגולרי רחב"),
    Q(r"תהי $L$ שפת המילים מעל $\{0,1\}$ שמספר ה-$0$ בהן שווה ל-$1$ מודולו $3$. איזו טענה נכונה?", cls_opts(K2),
      why=r"האוטומט זוכר רק את שארית מספר ה-$0$ מודולו $3$, שלוש אפשרויות. הביטוי: $1^*01^*(01^*01^*01^*)^*$ (אפס אחד, ואז קבוצות של שלושה). לכן $L$ רגולרית ואינסופית.",
      recap="מודולו: זיכרון סופי"),
    Q(r"תהי $L=\{a^nb^m\mid n+2m\le6\}$. איזו טענה נכונה?", cls_opts(K3),
      why=r"הסכום $n+2m$ חסום ב-$6$ וגם $n,m\ge0$, ולכן $n\le6$ ו-$m\le3$: מספר סופי של מילים. השפה סופית.",
      recap="סכום חסום: סופית"),
    Q(r"תהי $L=\{a^nb^m\mid n-m\le2\}$. איזו טענה נכונה?", cls_opts(K4),
      why=r"ההפרש חסום אבל $n$ יכול לגדול יחד עם $m$, ולכן צריך לזכור את $n$: לא רגולרית ($\{a^k\}$ מפרידה אינסופית עם הסיפא $b^{k-2}$ ומעלה). היא ח״ה: $S\to PT\mid TQ$, $P\to\varepsilon\mid a\mid aa$, $T\to aTb\mid\varepsilon$, $Q\to bQ\mid\varepsilon$. אומתה על כל המילים עד אורך $9$.",
      recap="הפרש חסום: מונה אחד, ח״ה לא רגולרית"),
    Q(r"תהי $L$ שפת המילים מעל $\{a,b,c\}$ שבהן האותיות מופיעות ממוינות (כל ה-$a$ לפני ה-$b$, וכל ה-$b$ לפני ה-$c$). איזו טענה נכונה?", cls_opts(K5),
      why=r"המילים הן בדיוק $a^*b^*c^*$, תבנית קבועה של שלושה גושים. אין שום השוואה בין הכמויות. רגולרית ואינסופית.",
      recap="תבנית קבועה של גושים: רגולרית"),
  ])
