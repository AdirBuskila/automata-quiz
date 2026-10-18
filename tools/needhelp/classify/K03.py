# -*- coding: utf-8 -*-
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nh import *


def zeros_ones(w):
    m = re.fullmatch(r"(0*)(1*)", w)
    return None if not m else (len(m.group(1)), len(m.group(2)))


# Q1  L = 0^i 1^j with i != j : which infinite family separates?
P1 = lambda w: zeros_ones(w) is not None and zeros_ones(w)[0] != zeros_ones(w)[1]
ZS = words("01", 5) + ["0" * i + "1" * j for i in range(15) for j in range(15)]
F = {"0^k": lambda k: "0" * k, "0^k1^k": lambda k: "0" * k + "1" * k, "1^k": lambda k: "1" * (k + 1), "(01)^k": lambda k: "01" * (k + 1)}
S1 = {n: sep_infinite(P1, g, ZS, 8) for n, g in F.items()}
assert S1 == {"0^k": True, "0^k1^k": False, "1^k": False, "(01)^k": False}

# Q2  L = #a = #b : which regular R shows (L ∩ R) is not regular
EQ = lambda w: w.count("a") == w.count("b")
def inter(R):
    r = rx(R, "ab")
    return lambda w: EQ(w) and r.accepts(w)
NR = {R: rank_growing(inter(R), "ab") for R in ("a*b*", "(ab)*", "a*+b*", "ab*")}
assert NR == {"a*b*": True, "(ab)*": False, "a*+b*": False, "ab*": False}

# Q3  which language is not regular
ab = lambda w: (lambda m: None if not m else (len(m.group(1)), len(m.group(2))))(re.fullmatch(r"(a*)(b*)", w))
LA = lambda w: ab(w) is not None and ab(w)[0] - ab(w)[1] <= 2
LB = lambda w: ab(w) is not None and ab(w)[0] + ab(w)[1] <= 5
LC = lambda w: ab(w) is not None and ab(w)[0] >= 2 and ab(w)[1] >= 1
LD = lambda w: ab(w) is not None and ab(w)[0] % 3 == ab(w)[1] % 3
def regular(pred, alpha="ab"):
    return rank_stable(pred, alpha, 9, (5, 6, 7)) is not None and not rank_growing(pred, alpha)
NRG = {n: rank_growing(p, "ab") for n, p in dict(A=LA, B=LB, C=LC, D=LD).items()}
assert NRG == {"A": True, "B": False, "C": False, "D": False}, NRG

# Q4  unary languages: which is regular
U_MOD = lambda w: len(w) % 4 == 1
U_SQ = lambda w: int(len(w) ** 0.5) ** 2 == len(w)
U_POW = lambda w: len(w) > 0 and (len(w) & (len(w) - 1)) == 0
U_PRIME = lambda w: len(w) > 1 and all(len(w) % d for d in range(2, len(w)))
UREG = {n: rank_stable(p, "a", 14, (8, 9, 10)) is not None for n, p in dict(mod=U_MOD, sq=U_SQ, pw=U_POW, pr=U_PRIME).items()}
UNONREG = {n: rank_growing(p, "a", (3, 5, 7, 9), 16) for n, p in dict(mod=U_MOD, sq=U_SQ, pw=U_POW, pr=U_PRIME).items()}
assert UREG == dict(mod=True, sq=False, pw=False, pr=False) and UNONREG == dict(mod=False, sq=True, pw=True, pr=True), (UREG, UNONREG)

# Q5  which is regular
M1 = lambda w: w.count("0") % 3 == 1 and w.count("1") % 2 == 0
M2 = lambda w: w.count("0") == w.count("1")
M3 = lambda w: w.count("0") == 5 * w.count("1")
M4 = lambda w: w.count("0") >= w.count("1")
REG5 = {n: rank_stable(p, "01", 9, (5, 6, 7)) is not None for n, p in dict(a=M1, b=M2, c=M3, d=M4).items()}
NR5 = {n: rank_growing(p, "01") for n, p in dict(a=M1, b=M2, c=M3, d=M4).items()}
assert REG5 == dict(a=True, b=False, c=False, d=False) and NR5 == dict(a=False, b=True, c=True, d=True), (REG5, NR5)

LEVEL = level("K03", 3, "🚧", "להוכיח שפה לא רגולרית",
  "להוכיח אי-רגולריות בעזרת קבוצה מפרידה אינסופית או חיתוך עם שפה רגולרית, ולהבדיל בין ספירה מודולו לספירה אמיתית.",
  r'''
<p>אם לא מצאתם ביטוי או אס״ד לשפה, כנראה היא לא רגולרית, ועכשיו צריך להוכיח זאת. יש שתי דרכים מלאות, ושתיהן נשענות על חומר שכבר למדתם.</p>
<h3>דרך א׳: קבוצה מפרידה אינסופית</h3>
<div class="lesson-rule">🔑 אם קיימת קבוצה <b>אינסופית</b> של מילים שכל שתיים מהן ניתנות להפרדה, אז ל-$L$ אינסוף מחלקות שקילות, כלומר היא <b>לא רגולרית</b>. בדרך כלל $T=\{a^i\}$ (או $\{0^i\}$) והסיפא היא &quot;המשלימה&quot; $b^i$.</div>
<div class="lesson-ex"><b>דוגמה.</b> $L=\{0^i1^j\mid i\ne j\}$. הקבוצה $\{0^k\}$ מפרידה: $0^i$ ו-$0^j$ עם $i\ne j$ מופרדות בסיפא $1^i$ ($0^i1^i\notin L$ אבל $0^j1^i\in L$). לעומת זאת $\{0^k1^k\}$ אינה מפרידה: כולן מחוץ ל-$L$ ושקולות. מילה בתוך קבוצה צריכה לזכור משהו שונה, לא סתם להיות מסובכת.</div>
<h3>דרך ב׳: חיתוך עם שפה רגולרית</h3>
<p>רגולריות סגורות לחיתוך. לכן אם $L$ הייתה רגולרית, גם $L\cap R$ הייתה רגולרית לכל $R$ רגולרית. אם $L\cap R$ <b>לא</b> רגולרית, נובע ש-$L$ לא רגולרית. בוחרים $R$ שמסדרת את האותיות בגושים: $\{w\mid\#_a=\#_b\}\cap a^*b^*=\{a^nb^n\}$ (24A-B-Q13, 24X-C-Q11).</p>
<div class="lesson-trap">⚠️ $R$ חייבת להיות כזאת שהחיתוך נותן שפה <b>לא רגולרית ידועה</b>. עם $(ab)^*$ החיתוך הוא $(ab)^*$ ורגולרי (לא מוכיח כלום), ועם $a^*+b^*$ הוא $\{\varepsilon\}$.</div>
<h3>מה לא רגולרי ומה כן</h3>
<ul>
<li><b>ספירה מודולו או &quot;לפחות $k$&quot;: רגולרית.</b> $\#_0\bmod5=3$ רגולרית; $\#_0=5\cdot\#_1$ ו-$\#_0\ge\#_1$ לא (25A-C-Q13, 25A-A-Q4).</li>
<li><b>הפרש חסום:</b> $\{a^nb^m\mid n-m\le3\}$ לא רגולרית. <b>סכום חסום:</b> סופית (24A-A-Q2).</li>
<li><b>אות אחת:</b> ריבועים $a^{n^2}$, $a^{n!}$, חזקות של $2$ ראשוניים הם לא רגולריים, אבל $\{a^n\mid n\bmod4=1\}$ רגולרית. לא כל שפה אונרית רגולרית (21S-A-Q10).</li>
</ul>
<p>ב-21S-A-Q17 ו-24A-C-Q4 הקבוצות המפרידות הן $\{a^i\}$ (או $\{b^i\}$), והסיפות &quot;משלימות&quot; את המונה. ב-19B-B-Q13 אותו רעיון עם $\{b^i\}$.</p>
''',
  [
    Q(r"תהי $L=\{0^i1^j\mid i\ne j\}$. איזו קבוצה אינסופית **ומפרידה** (ולכן מוכיחה ש-$L$ לא רגולרית)?",
      [C(r"$\{0^k\mid k\ge0\}$", S1["0^k"]), C(r"$\{0^k1^k\mid k\ge0\}$", S1["0^k1^k"]),
       C(r"$\{1^k\mid k\ge1\}$", S1["1^k"]), C(r"$\{(01)^k\mid k\ge1\}$", S1["(01)^k"])],
      why=r"ב-$\{0^k\}$ הסיפא $1^i$ מפרידה בין $0^i$ ל-$0^j$ ($j\ne i$). בשלוש האחרות כל איברי הקבוצה שקולים: $0^k1^k\notin L$ ולכל סיפא $z$ התשובה לכולן זהה; $1^k$ (עם $k\ge1$) כולן ב-$L$ וכל המשך אפשרי בלבד ב-$1$; $(01)^k$ ל-$k\ge2$ בכלל לא בצורה $0^i1^j$ (מלכודת). (בדקנו את ההפרדה של שמונה האיברים הראשונים.)",
      recap=r"קבוצה מפרידה: $0^k$ עם הסיפא המשלימה"),
    Q(r"$L=\{w\in\{a,b\}^*\mid\#_a=\#_b\}$. איזו שפה רגולרית $R$ מראה ש-$L$ לא רגולרית (כי $L\cap R$ לא רגולרית)?",
      [C(r"$R=a^*b^*$", NR["a*b*"]), C(r"$R=(ab)^*$", NR["(ab)*"]), C(r"$R=a^*+b^*$", NR["a*+b*"]), C(r"$R=ab^*$", NR["ab*"])],
      why=r"$L\cap a^*b^*=\{a^nb^n\}$, שאינה רגולרית. עם $(ab)^*$ החיתוך הוא $(ab)^*$ (רגולרית). עם $a^*+b^*$ החיתוך הוא $\{\varepsilon\}$. עם $ab^*$ החיתוך הוא $\{ab\}$ (סופית). בדקנו שרק בחיתוך הראשון מספר מחלקות השקילות ממשיך לגדול.",
      recap="חיתוך עם a*b* מסדר את האותיות בגושים"),
    Q(r"איזו מהשפות הבאות **לא** רגולרית?",
      [C(r"$\{a^nb^m\mid n-m\le2\}$", NRG["A"]), C(r"$\{a^nb^m\mid n+m\le5\}$", NRG["B"]),
       C(r"$\{a^nb^m\mid n\ge2,\ m\ge1\}$", NRG["C"]), C(r"$\{a^nb^m\mid n\equiv m\pmod3\}$", NRG["D"])],
      why=r"הפרש חסום מכריח לזכור את $n$ (כל עוד $m$ גדל איתו): לא רגולרית. סכום חסום ($n+m\le5$): סופית. $n\ge2,m\ge1$: $aaa^*bb^*$. $n\equiv m\pmod3$: אוטומט סופי זוכר את $n\bmod3$ ואחר כך מסיים לספור $m$ מודולו $3$. בדקנו את מספר המחלקות של כל אחת.",
      recap="הפרש חסום: לא רגולרית; סכום חסום ומודולו: כן"),
    Q(r"איזו מהשפות הבאות מעל $\{a\}$ היא **רגולרית**?",
      [C(r"$\{a^n\mid n\bmod4=1\}$", UREG["mod"]), C(r"$\{a^{n^2}\mid n\ge0\}$", UREG["sq"]),
       C(r"$\{a^{2^n}\mid n\ge0\}$", UREG["pw"]), C(r"$a^p$ עבור $p$ ראשוני", UREG["pr"])],
      why=r"$\{a^n\mid n\bmod4=1\}$ מתארת ביטוי $a(aaaa)^*$ ויש לה $\mathrm{Rank}=5$. הריבועים, חזקות הדו והראשוניים הם סדרות עם פערים שגדלים בלי גבול: ל-$a^i$ ו-$a^j$ שונות תמיד יש סיפא מפרידה, ולכן מספר המחלקות אינסופי. (בדקנו: מספר המחלקות קבוע בשפה הראשונה וממשיך לגדול בשלוש האחרות.)",
      recap="לא כל שפה אונרית רגולרית; פערים שגדלים: לא"),
    Q(r"איזו מהשפות הבאות מעל $\{0,1\}$ היא **רגולרית**?",
      [C(r"מספר ה-$0$ שווה ל-$1$ מודולו $3$ **וגם** מספר ה-$1$ זוגי", REG5["a"]), C(r"$\#_0=\#_1$", REG5["b"]),
       C(r"$\#_0=5\cdot\#_1$", REG5["c"]), C(r"$\#_0\ge\#_1$", REG5["d"])],
      why=r"הראשונה סופרת מודולו, ולכן זיכרון סופי ($3\cdot2=6$ מצבים). שלוש האחרות משוות מונים שגדלים בלי גבול ולכן צריכות זיכרון בלתי חסום (בדקנו שמספר המחלקות שלהן ממשיך לגדול).",
      recap="מודולו: רגולרית; שוויון או אי-שוויון בין מונים: לא"),
  ])
