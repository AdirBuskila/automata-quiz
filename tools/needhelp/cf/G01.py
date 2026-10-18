# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def parts(w, letters):
    m = re.fullmatch("".join(f"({c}*)" for c in letters), w)
    return None if not m else tuple(len(g) for g in m.groups())


def lang_is(g, alpha, pred, n=8):
    return g.lang(n) == {w for w in words(alpha, n) if pred(w)}


# lesson facts
assert lang_is(CFG("S->aSb|ε"), "ab", lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] == parts(w, "ab")[1])
assert CFG("S->S101").lang(8) == set()
assert sorted(CFG("S->SaS|b").lang(7), key=lambda w: (len(w), w)) == ["b", "bab", "babab", "bababab"]

# Q1
G1 = CFG("S->aSb|bSa|ε")
W1 = ["aabb", "abba", "aaab", "abb"]
# Q2
G2 = CFG("T->aTb|ε", start="T")
A_NB = lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] == parts(w, "ab")[1]
# Q3
G3 = CFG("S->SaS|b")
third = sorted(G3.lang(8), key=lambda w: (len(w), w))[2]
# Q4
G4 = CFG("S->AB;A->aAb|ε;B->bB|b")
LESS = lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] < parts(w, "ab")[1]
LEQ = lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] <= parts(w, "ab")[1]
GT = lambda w: parts(w, "ab") is not None and parts(w, "ab")[0] > parts(w, "ab")[1]
# Q5
G5 = CFG("S->S101")

LEVEL = level("G01", 1, "📖", "לקרוא דקדוק: גזירה, משתנים והמילים הקצרות",
  "לפענח דקדוק חסר הקשר בשיטה של משתנה אחר משתנה ולפסול אפשרויות במילה קצרה.",
  r'''
<p>דקדוק חסר הקשר (ח״ה) הוא ארבעייה $G=\langle\Sigma,V,S,R\rangle$: $\Sigma$ אותיות (<b>טרמינלים</b>), $V$ <b>משתנים</b>, $S\in V$ משתנה התחלתי, ו-$R$ כללי גזירה $A\to\alpha$. גזירה מחליפה משתנה בצד ימין של כלל שלו, ו-$L(G)=\{w\in\Sigma^*\mid S\overset{*}{\Rightarrow}w\}$.</p>
<div class="lesson-rule">🔑 <b>רק מילים טרמינליות נכנסות לשפה.</b> גזירה שאי אפשר לסיים (אין כלל שמחסל את המשתנה) לא תורמת כלום. בדקדוק $S\to S101$ אין שום דרך להיפטר מ-$S$, ולכן הוא יוצר את <b>השפה הריקה</b>, וזה חוקי לגמרי (24A-B-Q11).</div>
<h3>שיטת הפענוח</h3>
<ol>
<li><b>פענחו כל משתנה לבד</b>, מלמטה למעלה: מה כל משתנה גוזר?</li>
<li>זהו תבניות מוכרות (הטבלה).</li>
<li>הרכיבו: $S\to AB$ הוא <b>שרשור</b>, $S\to A\mid B$ הוא <b>איחוד</b>.</li>
<li>בדקו את $\varepsilon$ ואת המילים הקצרות ביותר. רוב המסיחים נופלים עליהן.</li>
</ol>
<table dir="ltr"><thead><tr><th>הכללים</th><th>המשתנה גוזר</th></tr></thead><tbody>
<tr><td>$T\to aTb\mid\varepsilon$</td><td>$\{a^nb^n\mid n\ge0\}$</td></tr>
<tr><td>$A\to aA\mid a$</td><td>$a^+$</td></tr>
<tr><td>$B\to aB\mid bB\mid\varepsilon$</td><td>$\Sigma^*$</td></tr>
<tr><td>$S\to aSa\mid bSb\mid a\mid b\mid\varepsilon$</td><td>כל הפלינדרומים</td></tr>
<tr><td>$S\to aSc\mid B$, $B\to bBc\mid\varepsilon$</td><td>$a^nb^mc^{n+m}$</td></tr></tbody></table>
<div class="lesson-ex"><b>דוגמה (23A-A-Q12): $S\to SaS\mid b$.</b> המילים הקצרות: $b$, אחר כך $bab$, אחר כך $babab$. כלומר $b(ab)^k$. ולכן $(a+b)^*$ נופל ($bb$ לא נגזרת), ו-$\#_b=\#_a$ נופל על $babab$ (שלושה $b$ ושני $a$). כשכל האפשרויות נראות סבירות, כתבו את שלוש המילים הקצרות ביותר.</div>
<div class="lesson-trap">⚠️ <b>הצבה מבטלת משתני עזר:</b> $S\to aMb\mid\varepsilon$ עם $M\to aSb$ שקול ל-$S\to aaSbb\mid\varepsilon$, כלומר $\{a^{2n}b^{2n}\}$ (25A-A-Q9, 25A-C-Q8). $\{a^nb^n\}$ נופל על $ab$. ובשאלה 23A-A-Q7 המילה הריקה לא בשפה, כי אין כלל $S\to\varepsilon$ וחייבים לעבור דרך $aTb$ או $bTa$: המילים באורך זוגי שאינן פלינדרומים.</div>
<p>ועוד שני סימני זיהוי: ב-SAMP-19-Q22, $A$ גוזר $a^{k+1}b^k$ ו-$B$ גוזר $b^{m+1}a^m$ (שניהם באורך אי-זוגי), ו-$S\to AB$ נותן את כל המילים באורך זוגי. ב-21S-A-Q18 הדקדוק יוצר פלינדרומים בלי $aa$.</p>
''',
  [
    Q("נתון הדקדוק:\n" + gram("S->aSb|bSa|ε") + "\nאיזו מילה נגזרת מ-$S$?",
      [C(f"${w}$", G1.derives(w)) for w in W1],
      why=r"כל צעד עוטף את מה שנגזר עד כה בזוג אותיות שונות: $a\ldots b$ או $b\ldots a$, וכלל $\varepsilon$ מסיים. לכן $ab$ ו-$aabb=a(ab)b$ נגזרות, ו-$aabb$ היא התשובה. $abba$ מתחילה ונגמרת באותה אות, וכל מילה לא ריקה שנגזרת מתחילה ונגמרת באותיות שונות. $aaab$ נופלת כי הפנים $aa$ לא נגזר (מילה נגזרת תמיד מאוזנת בין $a$ ל-$b$), ו-$abb$ כי הפנים $b$ באורך אי-זוגי. בדקנו את כל המילים עד אורך $8$.",
      recap="גוזרים מבפנים החוצה, ובודקים מילים קצרות"),
    Q("נתון הדקדוק $T\\to aTb\\mid\\varepsilon$. מהי $L$ שהוא יוצר מ-$T$?",
      [C(r"$\{a^nb^n\mid n\ge0\}$", lang_is(G2, "ab", A_NB)), C(r"$\{(ab)^n\mid n\ge0\}$", lang_is(G2, "ab", lambda w: re.fullmatch("(ab)*", w) is not None)),
       C(r"$\{a^nb^{2n}\mid n\ge0\}$", lang_is(G2, "ab", lambda w: parts(w, "ab") is not None and 2 * parts(w, "ab")[0] == parts(w, "ab")[1])),
       C(r"$\{a^nb^m\mid n,m\ge0\}$", lang_is(G2, "ab", lambda w: parts(w, "ab") is not None))],
      why=r"כל שימוש בכלל הראשון מוסיף $a$ משמאל ו-$b$ מימין, וכלל $\varepsilon$ מסיים. לכן אחרי $n$ צעדים מתקבל $a^nb^n$. $(ab)^n$ נופלת על $abab$, שאינה נגזרת. בדקנו את הדקדוק על כל המילים עד אורך $8$.",
      recap="T → aTb | ε יוצר a^n b^n".replace("T → aTb | ε", "$T\\to aTb\\mid\\varepsilon$").replace("a^n b^n", "$a^nb^n$")),
    Q("נתון הדקדוק:\n" + gram("S->SaS|b") + "\nמהי המילה **השלישית** הקצרה ביותר שהוא יוצר?",
      [C(f"${w}$", third == w) for w in ("babab", "bbb", "baab", "bab")],
      why=r"המילים: $b$ (מיד), $bab$ ($S\to SaS\to bab$), $babab$ (שלוש $b$ עם שני $a$ ביניהם, באורך $5$). לכן המילה השלישית היא $babab$. $bbb$ ו-$baab$ אינן נגזרות בכלל: אין כלל שמדביק שני $b$.",
      recap="בודקים את שלוש המילים הקצרות: b, bab, babab"),
    Q("נתון הדקדוק:\n" + gram("S->AB;A->aAb|ε;B->bB|b") + "\nמהי השפה $L(G)$?",
      [C(r"$\{a^nb^m\mid m>n\}$", lang_is(G4, "ab", LESS)), C(r"$\{a^nb^m\mid m\ge n\}$", lang_is(G4, "ab", LEQ)),
       C(r"$\{a^nb^n\mid n\ge0\}$", lang_is(G4, "ab", A_NB)), C(r"$\{a^nb^m\mid n>m\}$", lang_is(G4, "ab", GT))],
      why=r"$A$ גוזר $a^nb^n$, ו-$B$ גוזר $b^+$ (לפחות $b$ אחד). השרשור נותן $a^nb^{n+k}$ עם $k\ge1$, כלומר $m>n$. המילה הריקה לא בשפה, כי $B$ תמיד מוסיף אות, ולכן $m\ge n$ שגויה. בדקנו על כל המילים עד אורך $8$.",
      recap="שרשור: A גוזר a^n b^n, B גוזר b+".replace("A גוזר a^n b^n, B גוזר b+", "$A$ גוזר $a^nb^n$ ו-$B$ גוזר $b^+$")),
    Q("נתון הדקדוק $S\\to S101$ (כלל יחיד). איזו טענה נכונה?",
      [C(r"קיים דקדוק ח״ה עם $L(G)=\emptyset$, למשל הדקדוק הזה", G5.lang(8) == set()), C(r"$L(G)=\{\varepsilon\}$", G5.lang(8) == {""}),
       C(r"$L(G)=\{101\}^*$", G5.lang(8) == {w for w in words("01", 8) if re.fullmatch("(101)*", w)}), C(r"$L(G)$ אינסופית", len(G5.lang(8)) > 8)],
      why=r"כל גזירה מתחילה ב-$S\Rightarrow S101\Rightarrow S101101\ldots$ ואין כלל שמחסל את $S$, ולכן אף גזירה לא נגמרת במילה טרמינלית: $L(G)=\emptyset$ (חישבנו: אין אף מילה). השפה הריקה היא ח״ה, וכל דקדוק כזה חוקי.",
      recap="גזירה בלי סיום אינה תורמת: השפה ריקה"),
  ])
