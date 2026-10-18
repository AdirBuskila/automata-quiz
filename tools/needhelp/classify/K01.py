# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def ab_form(w, s):
    m = re.fullmatch(s, w)
    return m


def counts(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w)
    return None if not m else tuple(len(g) for g in m.groups())


# Q1: a^n b^m with n+m <= 4  (finite)
P1 = lambda w: bool(re.fullmatch(r"a*b*", w)) and len(w) <= 4
K1 = classify(P1, "ab", ("finite", 4))
# Q2: a^i b^j c^k with i <= j <= i   ==  i = j
P2 = lambda w: counts(w) is not None and counts(w)[0] <= counts(w)[1] <= counts(w)[0]
K2 = classify(P2, "abc", ("cfl", "S->TC;T->aTb|ε;C->cC|ε"), n=8)
# Q3: a^n b^n
P3 = lambda w: bool(re.fullmatch(r"a*b*", w)) and w.count("a") == w.count("b")
K3 = classify(P3, "ab", ("cfl", "S->aSb|ε"))
# Q4: a^n b^n c^n
P4 = lambda w: counts(w) is not None and counts(w)[0] == counts(w)[1] == counts(w)[2]
K4 = classify(P4, "abc", ("noncfl", lambda p: "a" * p + "b" * p + "c" * p), n=7)
# Q5: a^i b^j with i <= 2 or j <= 2
P5 = lambda w: bool(re.fullmatch(r"a*b*", w)) and (w.count("a") <= 2 or w.count("b") <= 2)
K5 = classify(P5, "ab", ("reg", "(ε+a+aa)b*+a*(ε+b+bb)"))
assert (K1, K2, K3, K4, K5) == ("finite", "cfl", "cfl", "noncfl", "reg")

LEVEL = level("K01", 1, "🗺️", "ההיררכיה ואלגוריתם הסיווג",
  "לסווג שפה לפי הסולם: סופית, רגולרית, חסרת הקשר, או לא, ולפשט את הגדרתה לפני שמחליטים.",
  r'''
<p>שאלת הסיווג היא המשפחה הגדולה בבנק: 70 שאלות. כמעט תמיד ארבע האפשרויות הן אותן ארבע: <b>(א) סופית</b>, <b>(ב) רגולרית ואינסופית</b>, <b>(ג) חסרת הקשר (ח״ה) ולא רגולרית</b>, <b>(ד) לא ח״ה</b>.</p>
<div class="lesson-rule">🔑 <b>ההיררכיה:</b> סופיות $\subsetneq$ רגולריות $\subsetneq$ ח״ה $\subsetneq$ כל השפות. כל שפה סופית רגולרית, וכל שפה רגולרית היא ח״ה (אס״ד הוא אוטומט מחסנית שלא נוגע במחסנית). לכן ארבע האפשרויות <b>מוציאות זו את זו</b>, ושואלים תמיד מלמטה למעלה.</div>
<table dir="ltr"><thead><tr><th>המחלקה</th><th>דוגמה שמוכיחה שהיא ממש גדולה יותר</th></tr></thead><tbody>
<tr><td>רגולרית, לא סופית</td><td>$a^*$</td></tr>
<tr><td>ח״ה, לא רגולרית</td><td>$\{a^nb^n\}$</td></tr>
<tr><td>לא ח״ה</td><td>$\{a^nb^nc^n\}$</td></tr></tbody></table>
<h3>האלגוריתם</h3>
<ol>
<li><b>פשטו את ההגדרה לפני הכול.</b> מחצית מהמלכודות נפתרות כאן: $i\le k\le m\le i$ פירושו $i=k=m$ (23A-B-Q8); $ab^nb^na$ הוא $a(bb)^+a$ (21S-A-Q8); $\{xyz\mid|x|\le|y|\le|z|\}$ הוא $\Sigma^*$ כי אפשר לבחור $x=y=\varepsilon$ (23A-A-Q8); $\{uv\mid|u|=|v|\}$ הוא $(\Sigma\Sigma)^*$ (21S-B-Q20).</li>
<li><b>האם היא סופית?</b> אורכים חסומים &rarr; סופית &rarr; רגולרית.</li>
<li><b>האם היא רגולרית?</b> חפשו ביטוי או אס״ד. סימנים: תבנית קבועה, ספירה <b>מודולו</b>, ספירה <b>עד קבוע</b>, או &quot;או $i>50$&quot; שבולע את הכול.</li>
<li>אם לא, הוכיחו לא רגולרית (שלב הבא בקורס).</li>
<li><b>האם היא ח״ה?</b> דקדוק או אוטומט מחסנית. אם לא, הוכיחו לא ח״ה.</li>
</ol>
<div class="lesson-trap">⚠️ <b>&quot;סופית&quot; לא הייתה אף פעם התשובה</b> בבנק (בין 56 שאלות בנוסח ארבע האפשרויות: ח״ה לא רגולרית 25, רגולרית אינסופית 16, לא ח״ה 15). אבל היא שלב ביניים נהדר: &quot;סופית &rarr; רגולרית&quot; (24A-A-Q2). ובשפה אחת עם &quot;או&quot; (19B-B-Q18) החלק הקשה ($i=j=k$) נבלע בחלק רגולרי רחב, ולכן השפה כולה רגולרית אף שהיא נראית כמו $a^nb^nc^n$.</div>
<div class="lesson-rule">🔑 <b>כמה זיכרון צריך?</b> כמות חסומה (עד קבוע, מודולו, תבנית) &rarr; רגולרית. מונה אחד שעולה ואז יורד, בסדר מקונן &rarr; ח״ה. שתי השוואות בבת אחת, או חוצות &rarr; לא ח״ה. ב-25A-C-Q2 נראה שהשפה &quot;ריבועים&quot;, אבל הכוכבית מכילה גם את $a$, ולכן היא $a^*$.</div>
''',
  [
    Q(r"תהי $L=\{a^nb^m\mid n+m\le4\}$ מעל $\{a,b\}$. איזו טענה נכונה?", cls_opts(K1),
      why=r"הסכום $n+m$ חסום ב-$4$, ולכן אורך כל מילה לכל היותר $4$ ויש מספר סופי של מילים: $L$ סופית. (וכל שפה סופית היא גם רגולרית, אבל &quot;רגולרית ואינסופית&quot; שגויה כי השפה סופית.)",
      recap="סכום חסום של מונים: שפה סופית"),
    Q(r"תהי $L=\{a^ib^jc^k\mid i\le j\le i\}$ מעל $\{a,b,c\}$. איזו טענה נכונה?", cls_opts(K2),
      why=r"קודם מפשטים: $i\le j\le i$ אומר $i=j$, ו-$k$ חופשי. לכן $L=\{a^ib^ic^k\}$, שנוצרת ע״י $S\to TC$, $T\to aTb\mid\varepsilon$, $C\to cC\mid\varepsilon$. היא ח״ה. היא לא רגולרית: $\{a^i\}$ קבוצה מפרידה אינסופית (הסיפא $b^i$). (בדקנו שהדקדוק מתאים לשפה על כל המילים עד אורך $8$.)",
      recap="מפשטים תחילה: i ≤ j ≤ i פירושו i = j"),
    Q(r"תהי $L=\{a^nb^n\mid n\ge0\}$. איזו טענה נכונה?", cls_opts(K3),
      why=r"$S\to aSb\mid\varepsilon$ יוצר אותה, ולכן היא ח״ה. היא לא רגולרית: $\{a^k\}$ אינסופית ומפרידה (הסיפא $b^k$). זו הדוגמה הקלאסית לח״ה שאינה רגולרית: מונה אחד שעולה ויורד.",
      recap="מונה אחד: ח״ה לא רגולרית"),
    Q(r"תהי $L=\{a^nb^nc^n\mid n\ge0\}$. איזו טענה נכונה?", cls_opts(K4),
      why=r"צריך להשוות שלוש כמויות בבת אחת, ולמחסנית יש רק מונה אחד. למת הניפוח לח״ה עם $w=a^pb^pc^p$: החלון $|vxy|\le p$ נוגע לכל היותר בשני גושים, ולכן ניפוח משנה רק אותם ושובר את השוויון. (בדקנו את המשחק בפועל עבור $p=2,3,4$.)",
      recap="שלוש השוואות בבת אחת: לא ח״ה"),
    Q(r"תהי $L$ שפת המילים $a^ib^j$ שבהן $i\le2$ או $j\le2$. איזו טענה נכונה?", cls_opts(K5),
      why=r"&quot;או&quot; בולע: אם $i\le2$ מותר כל $j$, ואם $j\le2$ מותר כל $i$. לכן $L=(\varepsilon+a+aa)b^*+a^*(\varepsilon+b+bb)$, שהוא רגולרי ואינסופי. שום השוואה בין $i$ ל-$j$ לא נשארה. (בדקנו את הביטוי על כל המילים עד אורך $9$.)",
      recap="או עם תנאי רחב בולע את החלק הקשה"),
  ])
