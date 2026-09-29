# -*- coding: utf-8 -*-
"""Emit tools/raw/25A-C.json — 2025 סמסטר א מועד ג (24.5.2025), 18 MCQ.

There is no exam PDF. Transcribed by eye from solution file 1 (tools/raw/25A-C-SOL/page-02..08.png,
"גרסא מס' 1") — the PRIMARY source for numbering, option order and key (yellow highlight).
Solution file 2 (tools/raw/25A-C-SOL2) is the same exam with questions and options permuted;
every question was content-matched to its twin there and the highlighted option CONTENT agrees
for all 18 (file1->file2: 1->2, 2->8, 3->1, 4->16, 5->18, 6->3, 7->6, 8->15, 9->14, 10->5,
11->11, 12->13, 13->10, 14->12, 15->7, 16->4, 17->17, 18->9).
Neither file has blue explanation text, so explanations are our own derivations; every key was
re-derived and agrees with the highlight. Figures are lossless xrefs from file 1 (clean rasters).
Course PDA convention: accept in a final state with an empty stack. Raw strings keep TeX exact.
"""
import json, pathlib

SOL = "solution-pdf"
OTHERS = "כל הטענות האחרות לא נכונות."


def T(v): return {"type": "text", "value": v}
def M(v): return {"type": "math", "value": v}


def opts(*vals):
    return [dict(v, id=k) for k, v in zip("abcd", vals)]


Q = []
def q(num, topic, question, options, correct, explanation, **kw):
    Q.append(dict(num=num, topic=topic, question=question, options=options, correctId=correct,
                  answerSource=SOL, official=True, confidence="high", explanation=explanation, **kw))


BOTH_T = T(r"שתי הטענות $I,\,II$ הן נכונות.")
BOTH_F = T(r"שתי הטענות $I,\,II$ הן לא נכונות.")
ONLY_I = T(r"טענה $I$ נכונה וגם טענה $II$ לא נכונה.")
ONLY_II = T(r"טענה $II$ נכונה וגם טענה $I$ לא נכונה.")


def CLS(x="L", comma=True):
    sep = ", וגם לא-רגולרית." if comma else " אבל לא-רגולרית."
    dash = "לא-חסרת הקשר." if comma else "לא-חסרת-הקשר."
    return opts(T(rf"השפה ${x}$ היא סופית."), T(rf"השפה ${x}$ היא רגולרית ואינסופית."),
                T(rf"השפה ${x}$ היא חסרת הקשר{sep}"), T(rf"השפה ${x}$ היא {dash}"))


def SEP(a, b, c):
    return opts(*(T(rf"אם {s} אז $x,y$ **לא**-ניתנות להפרדה ביחס לשפה $L$.") for s in (a, b, c)), T(OTHERS))


q(1, "nerode",
  r"תהי $L=\{01,\ 10\}$, שפה מעל הא״ב הבינארי." "\n"
  r"כמה מצבים יש באס״ד $A$ עם מספר המצבים המינימלי כך שמתקיים $L(A)=L$?",
  opts(M(r"3"), M(r"2"), M(r"4"), T(r"לפחות 5")),
  "d",
  r"$T=\{\varepsilon,0,1,01,00\}$ היא קבוצה מפרידה בגודל 5: הסיפא $1$ מפרידה בין $\varepsilon$ ל-$0$ ובין $0$ ל-$1$, הסיפא $0$ מפרידה בין $\varepsilon$ ל-$1$, "
  r"הסיפא $\varepsilon$ מפרידה את $01$ מכל השאר, ו-$00$ (שאין לה המשך לשפה) מופרדת מ-$\varepsilon,0,1$ ע״י $01$, $1$, $0$ בהתאמה. "
  r"ואכן יש אס״ד עם 5 מצבים: התחלתי, אחרי $0$, אחרי $1$, מקבל, ומלכודת.")

q(2, "classify",
  r"תהי $L=\left(\{a^{n^2}\mid n\ge1\}\cup\{aa\}\right)^*$, שפה מעל הא״ב $\Sigma=\{a\}$." "\n"
  r"לדוגמא, $a^9\cdot a^{16}\cdot a^2\in L$." "\n" r"איזו מהטענות הבאות נכונה?",
  CLS("L", comma=False),
  "b",
  r"עבור $n=1$ מתקיים $a^{1^2}=a$, ולכן $a$ שייכת לשפה שבתוך הכוכב. לכן $L=a^*$ — שפה רגולרית ואינסופית.")

q(3, "pda",
  r"נתון האוטומט-מחסנית $M$ הבא, מעל הא״ב $\Sigma=\{a,b\}$." "\n" r"איזו מהטענות הבאות נכונה?",
  opts(T(r"המילה $aabbb$ **לא שייכת** לשפה של $M$ והמילה $aaabb$ **לא שייכת** לשפה של $M$."),
       T(r"המילה $aabbb$ **שייכת** לשפה של $M$ והמילה $aaabb$ **לא שייכת** לשפה של $M$."),
       T(r"המילה $aabbb$ **לא שייכת** לשפה של $M$ והמילה $aaabb$ **שייכת** לשפה של $M$."),
       T(r"המילה $aabbb$ **שייכת** לשפה של $M$ והמילה $aaabb$ **שייכת** לשפה של $M$.")),
  "c",
  r"$aaabb$ מתקבלת: דוחפים $A$ פעמיים ב-$q_1$, עוברים ל-$q_2$ עם ה-$a$ השלישית, ושתי ה-$b$ שולפות את שני ה-$A$ — מסיימים ב-$q_2$ עם מחסנית ריקה. "
  r"$aabbb$ לא מתקבלת: במחסנית יש לכל היותר $A$ אחד כשמגיעים ל-$q_2$ (ה-$a$ השנייה עוברת ל-$q_2$ בלי לדחוף), ולכן אי אפשר לשלוף שלוש פעמים.",
  image="images/exams/25A-C-Q3.png")

q(4, "nerode",
  r"תהי $L=\{w\mid \#_0(w)\ne\#_1(w)\}$, שפה מעל הא״ב $\Sigma=\{0,1\}$." "\n"
  r"לדוגמא: $011,\ 100,\ 1\in L$. אבל, $\varepsilon,\ 01\notin L$." "\n"
  r"יהיו $x,y\in\Sigma^*$ מילים כלשהן שונות זו מזו." "\n" r"איזו מהטענות הבאות היא טענה נכונה?",
  SEP(r"$y\in L$ וגם $x\notin L$", r"$y\notin L$ וגם $x\notin L$", r"$y\in L$ וגם $x\in L$"),
  "b",
  r"ב׳: אם $x,y\notin L$ אז בשתיהן $\#_0=\#_1$, ולכן לכל סיפא $z$: $xz\in L\iff \#_0(z)\ne\#_1(z)\iff yz\in L$. "
  r"א׳ מופרכת ע״י הסיפא $\varepsilon$. ג׳ מופרכת ע״י $y=1$, $x=0$ והסיפא $0$: $10\notin L$ אבל $00\in L$.")

q(5, "regex",
  r"איזה ביטוי רגולרי מתאר את השפה של האסל״ד $A$ הבא, מעל הא״ב $\Sigma=\{0,1\}$?",
  opts(M(r"101\left(1+1(0+1)\right)^*"), M(r"10\left(1+(0+1)\right)^*"),
       M(r"1^*0\left(1+(1(0+1)^*)\right)^*"), M(r"1^*01\left((0+1)1\right)^*")),
  "d",
  r"מ-$q_1$ קוראים $1^*0$ ומגיעים ל-$q_2$, אחר כך $1$ למצב המקבל $q_3$, וכל חזרה ל-$q_3$ היא $(0+1)1$ — כלומר $1^*01\left((0+1)1\right)^*$. "
  r"א׳: $01\in L(A)$ אבל לא מתחילה ב-$1$. ב׳: $10$ מתוארת אבל $10\notin L(A)$. ג׳: $0$ מתוארת אבל $0\notin L(A)$.",
  image="images/exams/25A-C-Q5.png")

q(6, "classify",
  r"תהי $L=\{a^kb^kc^id^k\mid i,k\ge0\}$, שפה מעל הא״ב $\Sigma=\{a,b,c,d\}$." "\n" r"איזו מהטענות הבאות נכונה?",
  CLS(),
  "d",
  r"אילו $L$ הייתה ח״ה, גם $L\cap a^*b^*d^*=\{a^kb^kd^k\mid k\ge0\}$ הייתה ח״ה (חיתוך ח״ה עם רגולרית), "
  r"אבל שפה זו לא-ח״ה (למת הניפוח לשפות ח״ה) — סתירה.")

q(7, "nerode",
  r"תהיינה $L_1,L_2$ שפות כלשהן, מעל הא״ב $\Sigma=\{0,1\}$." "\n" r"איזו מהטענות הבאות היא טענה נכונה?",
  opts(T(r"אם $\mathrm{Rank}(L_1\setminus L_2)=\infty$ וגם $L_2$ היא רגולרית אז מתקיים $\mathrm{Rank}(L_1\cup L_2)=\infty$"),
       T(r"אם $\mathrm{Rank}(L_2\setminus L_1)=\mathrm{Rank}(L_1)=\infty$ אז מתקיים $\mathrm{Rank}(L_1\cup L_2)=\infty$"),
       T(r"מתקיים $\mathrm{Rank}(L_1\cup L_2)\ge\min\{\mathrm{Rank}(L_1),\mathrm{Rank}(L_2)\}$"),
       T(OTHERS)),
  "a",
  r"א׳: $L_1\setminus L_2=(L_1\cup L_2)\cap\overline{L_2}$. אילו $L_1\cup L_2$ הייתה רגולרית, גם $L_1\setminus L_2$ הייתה רגולרית (סגירות לחיתוך ולהשלמה) — בסתירה ל-$\mathrm{Rank}(L_1\setminus L_2)=\infty$. "
  r"ב׳ ו-ג׳ מופרכות ע״י $L_1=\{0^n1^n\mid n\ge0\}$ ו-$L_2=\overline{L_1}$: שתיהן לא-רגולריות, אבל $L_1\cup L_2=\Sigma^*$ ודרגתה 1.")

q(8, "cfg",
  r"נתון הדקדוק $G$ הבא, מעל הא״ב $\Sigma=\{a,b\}$. המשתנה ההתחלתי בדקדוק זה הוא $S$:" "\n"
  r"$$\begin{array}{l}S\to aM\mid\varepsilon\\ M\to aSbb\end{array}$$" "\n"
  r"איזו מהטענות הבאות נכונה?",
  opts(M(r"L(G)=\{a^nb^n\mid n\ge0\}"), M(r"L(G)=\{(ab)^{2n}\mid n\ge0\}"),
       M(r"L(G)=\{(ab)^n\mid n\ge0\}"), M(r"L(G)=\{a^{2n}b^{2n}\mid n\ge0\}")),
  "d",
  r"הדקדוק שקול לדקדוק $S\to aaSbb\mid\varepsilon$, ולכן $L(G)=\{a^{2n}b^{2n}\mid n\ge0\}$. "
  r"א׳, ג׳ מופרכים כי $ab\notin L(G)$, ו-ב׳ מופרך כי $abab\notin L(G)$.")

q(9, "regex",
  r"איזה מהביטויים הרגולרים הבאים שקול לביטוי הרגולרי $a^*b(a+b)^*b$, מעל הא״ב $\Sigma=\{a,b\}$?",
  opts(M(r"(a^*ba^*b)^*"), M(r"a^*ba^*b^*(a+b)^*"), M(r"(a+b)^*b(a+b)^*bb^*"), T(OTHERS)),
  "c",
  r"שני הביטויים מתארים את שפת המילים שמכילות לפחות שני תווי $b$ ומסתיימות ב-$b$. "
  r"א׳ מופרך: $\varepsilon$ מתוארת ע״י א׳ אבל לא ע״י הביטוי הנתון. ב׳ מופרך: $b$ מתוארת ע״י ב׳ אבל לא ע״י הביטוי הנתון.")

q(10, "cfg",
  r"תהי $L_1=\{0^{2n}1^{2n}0^n\mid n\ge0\}$, שפה מעל הא״ב $\Sigma=\{0,1\}$. "
  r"בנוסף, נתון הדקדוק $G$ הבא, מעל אותו הא״ב. המשתנה ההתחלתי בדקדוק זה הוא $S$:" "\n"
  r"$$\begin{array}{l}S\to AB\\ A\to 00A1\mid\varepsilon\\ B\to 1B0\mid\varepsilon\end{array}$$" "\n"
  r"איזו מהטענות הבאות נכונה?",
  opts(T(r"השפה $L_1$ שווה לשפה $L(G)$."),
       T(r"השפה $L(G)$ מוכלת ממש בשפה $L_1$."),
       T(r"השפה $L_1$ מוכלת ממש בשפה $L(G)$."),
       T(OTHERS)),
  "c",
  r"מתקיים $L(G)=\{0^{2m}1^{m+k}0^k\mid m,k\ge0\}$, ו-$L_1$ היא המקרה $m=k$ — לכן $L_1\subseteq L(G)$. "
  r"ההכלה ממש, כי $001\in L(G)$ אבל $001\notin L_1$.")

q(11, "classify",
  r"תהי $L=\{a^\ell b^mc^r\mid \ell\ne r\ \mathbf{or}\ m=r\}$, שפה מעל הא״ב $\Sigma=\{a,b,c\}$." "\n" r"איזו מהטענות הבאות נכונה?",
  CLS(),
  "c",
  r"$L$ היא איחוד של $\{a^\ell b^mc^r\mid \ell\ne r\}$ ו-$\{a^\ell b^mc^r\mid m=r\}$, ששתיהן ח״ה — ולכן $L$ ח״ה. "
  r"היא לא-רגולרית: $T=\{a,a^2,a^3,\dots\}$ היא קבוצה מפרידה אינסופית — לכל $i\ne k$ הסיפא $c^k$ נותנת $a^ic^k\in L$ ($\ell\ne r$) אבל $a^kc^k\notin L$ ($\ell=r$ ו-$m=0\ne r$).")

q(12, "reg_closure",
  r"תהי $L=\{a^{n^2}\mid n\ge1\}$, שפה מעל הא״ב $\Sigma=\{a\}$." "\n"
  r"נתבונן בשתי הטענות הבאות:" "\n"
  r"$I$. השפה $L\setminus\{a^k\mid k<2025\}$ היא לא-רגולרית." "\n"
  r"$II$. השפה $L\setminus\{a^k\mid k\ge2025\}$ היא לא-רגולרית." "\n"
  r"איזה מהסעיפים הבאים נכון?",
  opts(BOTH_F, ONLY_I, ONLY_II, BOTH_T),
  "b",
  r"$I$ נכונה: אילו $L\setminus\{a^k\mid k<2025\}$ הייתה רגולרית, אז $L$ — האיחוד שלה עם השפה הסופית $L\cap\{a^k\mid k<2025\}$ — הייתה רגולרית, סתירה. "
  r"$II$ לא נכונה: $L\setminus\{a^k\mid k\ge2025\}$ היא שפה סופית ולכן רגולרית.")

q(13, "classify",
  r"איזו מהשפות הבאות היא שפה **לא**-רגולרית, מעל הא״ב $\Sigma=\{0,1\}$?",
  opts(M(r"\{w\in\Sigma^*\mid \#_0(w)\ge5\}"),
       M(r"\{w\in\Sigma^*\mid \#_0(w)\bmod 5=3\ \mathbf{and}\ \#_1(w)\bmod 5=1\}"),
       M(r"\{w\in\Sigma^*\mid \#_0(w)=5\cdot\#_1(w)\}"),
       T(r"כל השפות הנ״ל הן שפות רגולריות")),
  "c",
  r"א׳ ו-ב׳ רגולריות (אס״ד סופר עד 5, או מכפלה של שני מונים מודולו 5). "
  r"ג׳ לא-רגולרית: $T=\{0^5,0^{10},0^{15},\dots\}$ היא קבוצה מפרידה אינסופית — הסיפא $1^j$ מפרידה בין $0^{5j}$ לבין $0^{5i}$ לכל $i\ne j$.")

q(14, "nerode",
  r"תהי $L_1=\{0\}$ ותהי $L_2=\{\varepsilon\}$, מעל הא״ב $\Sigma=\{0,1\}$." "\n" r"איזו מהטענות הבאות נכונה?",
  opts(T(r"מתקיים $\mathrm{Rank}(L_2)=\mathrm{Rank}(L_1)$"),
       T(r"מתקיים $\mathrm{Rank}(L_1)=1$ וגם $\mathrm{Rank}(L_1)>\mathrm{Rank}(L_2)$"),
       T(r"מתקיים $\mathrm{Rank}(L_2)=2$ וגם $\mathrm{Rank}(L_2)<\mathrm{Rank}(L_1)$"),
       T(OTHERS)),
  "c",
  r"האס״ד המינימלי ל-$\{\varepsilon\}$ הוא מצב התחלתי מקבל ומצב מלכודת — $\mathrm{Rank}(L_2)=2$. "
  r"ל-$\{0\}$ צריך 3 מצבים: $T=\{\varepsilon,0,1\}$ מפרידה (הסיפא $0$ מפרידה בין $\varepsilon$ ל-$1$, והסיפא $\varepsilon$ מפרידה את $0$) — $\mathrm{Rank}(L_1)=3$.")

q(15, "classify",
  r"נתון האוטומט-מחסנית $M$ הבא, מעל הא״ב $\Sigma=\{a,b\}$:" "\n" r"איזו מהטענות הבאות נכונה?",
  CLS("L(M)", comma=False),
  "c",
  r"$L(M)=\{a^nb^n\mid n\ge0\}\cup\{a^{n+1}b^n\mid n\ge0\}$: כל $a$ ב-$q_1$ נדחפת, מעבר ל-$q_2$ ב-$a$ או ב-$\varepsilon$ בלי לדחוף, וכל $b$ שולפת $a$. "
  r"השפה ח״ה (יש לה אוטומט מחסנית) ולא-רגולרית: $T=\{a,a^2,a^3,\dots\}$ קבוצה מפרידה אינסופית (הסיפא $b^k$ מקבלת את $a^k$ ודוחה את $a^i$ לכל $i<k$).",
  image="images/exams/25A-C-Q15.png")

q(16, "reg_closure",
  r"בהינתן שתי שפות $L_1,L_2$ כלשהן, מעל הא״ב $\Sigma=\{0,1\}$, נגדיר את השפה:" "\n"
  r"$$\mathbf{Z}(L_1,L_2)=\{w\in\Sigma^*\mid (w\in L_1\ \mathbf{and}\ w\in L_2)\ \mathbf{or}\ (w\notin L_1\ \mathbf{and}\ w\notin L_2)\}$$" "\n"
  r"נתבונן בשתי הטענות הבאות:" "\n"
  r"$I$. אם השפות $L_1,L_2$ הן רגולריות אזי השפה $\mathbf{Z}(L_1,L_2)$ רגולרית." "\n"
  r"$II$. אם השפות $L_1,L_2$ הן לא-רגולריות אזי השפה $\mathbf{Z}(L_1,L_2)$ לא-רגולרית." "\n"
  r"איזה מהסעיפים הבאים נכון?",
  opts(ONLY_I, ONLY_II, BOTH_T, BOTH_F),
  "a",
  r"$I$ נובעת מסגירות השפות הרגולריות לחיתוך, איחוד והשלמה: $\mathbf{Z}(L_1,L_2)=(L_1\cap L_2)\cup(\overline{L_1}\cap\overline{L_2})$. "
  r"$II$ מופרכת ע״י $L_1=L_2=\{0^n1^n\mid n\ge0\}$: אז $\mathbf{Z}(L_1,L_2)=\Sigma^*$, שהיא רגולרית.")

q(17, "pumping_reg",
  r"תהי $L=\{a\}\cdot\{w\in\Sigma^*\mid \#_a(w)=\#_b(w)\}\cdot\{b\}$, שפה מעל הא״ב $\Sigma=\{a,b\}$." "\n"
  r"לדוגמא, $ab,\ aabb,\ ababab\in L$ אבל $\varepsilon,\ abb,\ bba\notin L$." "\n"
  r"רוצים להוכיח שהשפה $L$ היא לא-רגולרית, תוך שימוש בלמת הניפוח לשפות רגולריות. נגדיר את $n$ להיות הקבוע המובטח מהלמה." "\n"
  r"איזו מילה תביא **בהכרח** לסתירה לתנאי למת הניפוח?",
  opts(M(r"a(ab)^nb"), M(r"ab^na^nb"), M(r"a(ba)^nb"), M(r"aba^nb^n")),
  "b",
  r"ב-$ab^na^nb$ כל פירוק עם $|xy|\le n$ נותן $y$ בתוך $ab^{n-1}$. עבור $i=0$: אם $y$ מכיל את ה-$a$ הראשונה המילה כבר לא מתחילה ב-$a$, "
  r"ואחרת $y=b^k$ ומתקבלת $ab^{n-k}a^nb$ שבה החלק האמצעי לא מאוזן — סתירה. "
  r"בא׳ ($y=ab$), בג׳ ($y=ba$ אחרי ה-$a$ הראשונה) ובד׳ ($y=ab$ בתחילת המילה) יש פירוק שמקיים את הלמה.")

q(18, "cfg",
  r"נתון הדקדוק $G$ הבא, מעל הא״ב $\Sigma=\{0,1\}$. המשתנה ההתחלתי בדקדוק זה הוא $S$:" "\n"
  r"$$\begin{array}{l}S\to AB\mid CD\\ A\to 1A1\mid\varepsilon\\ B\to 0B00\mid\varepsilon\\ C\to 01C\mid\varepsilon\\ D\to D10\mid\varepsilon\end{array}$$" "\n"
  r"נתבונן בשתי הטענות הבאות:" "\n"
  r"$I$. קיים דקדוק ליניארי ימני $G_R$ כך שמתקיים $L(G)=L(G_R)$" "\n"
  r"$II$. קיים אוטומט מחסנית $M$ כך שמתקיים $L(G)=L(M)$" "\n"
  r"איזה מהסעיפים הבאים נכון?",
  opts(BOTH_F, ONLY_II, ONLY_I, BOTH_T),
  "d",
  r"הדקדוק יוצר את השפה הרגולרית $(11)^*(000)^*+(01)^*(10)^*$, ולכן יש לה דקדוק ליניארי ימני ($I$ נכונה). "
  r"לכל שפה שנוצרת ע״י דקדוק ח״ה יש אוטומט מחסנית שמזהה אותה ($II$ נכונה).")

exam = {
    "examCode": "25A-C",
    "examLabel": "2025 סמסטר א׳ מועד ג׳",
    "year": 2025,
    "examDate": "24.5.2025",
    "course": "62208",
    "source": "exam",
    "files": {"exam": None,
              "solution": "מבחנים ופתרונות/2025/סמסטר א/מועד ג/1אוטומטים- סמס_ א_ מועד ג_ 24.5.2025 פתרון.pdf",
              "crossChecks": ["מבחנים ופתרונות/2025/סמסטר א/מועד ג/2אוטומטים- סמס_ א_ מועד ג_ 24.5.2025 פתרון.pdf",
                              "tools/detect_keys.py"]},
    "contexts": {},
    "questions": Q,
}
out = pathlib.Path(__file__).resolve().parent.parent / "raw" / "25A-C.json"
out.write_text(json.dumps(exam, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {out} ({len(Q)} questions)")
