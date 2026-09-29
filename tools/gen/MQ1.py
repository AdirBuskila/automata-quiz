# -*- coding: utf-8 -*-
"""Emit tools/raw/MQ1.json — Moodle quiz 1 (בוחן 1, Nov 2025), only questions with a trustworthy key.

Transcribed by eye from the Moodle screenshots under "מבדקים במודל/" (course dir). The quiz has
6 slots with 2 variants each; Moodle shuffles option order per attempt, so each question keeps the
order printed in the capture it was transcribed from (noted per question below).

Keys:
  moodle-feedback — the review page shows "התשובה הנכונה: …" (1a, 1b, 2a, 3a, 4a, 5a, 6a).
  moodle-100      — "100 (2).pdf": in-attempt captures + summary page of the ONLY attempt
                    (24 Nov 2025, 101/101 points, grade 100/100) → every pick there is correct
                    (2b, 5b). 2b's options are cut off in that PDF, so its option order comes from
                    the "100.docx" capture (same four values; pick 4 there too).
Not included (no proven key, on the ask list): 3b, 4b, 6b. Every key was also re-derived.
After running this, tools/raw/MQ1.json is the source of truth.
"""
import json, pathlib

FB = "moodle-feedback"
M100 = "moodle-100"
OTHERS = "כל הטענות האחרות לא נכונות"


def T(v): return {"type": "text", "value": v}
def M(v): return {"type": "math", "value": v}


def opts(*vals):
    return [dict(v, id=k) for k, v in zip("abcd", vals)]


Q = []
def q(num, topic, question, options, correct, src, explanation, **kw):
    Q.append(dict(num=num, topic=topic, question=question, options=options, correctId=correct,
                  answerSource=src, official=False, confidence="high", explanation=explanation, **kw))


NFA_STEM = (r"נתבונן באסל״ד $A$ ובאסל״ד $B$, המכילים מעברי $\varepsilon$, מעל הא״ב $\{a\}$:" "\n"
            r"איזו מהטענות הבאות נכונה?")
EQ = T(r"השפה $L(A)$ שווה לשפה $L(B)$")
A_IN_B = T(r"השפה $L(A)$ מוכלת ממש בשפה $L(B)$")
B_IN_A = T(r"השפה $L(B)$ מוכלת ממש בשפה $L(A)$")

# slot 1, variant a — "בוחן 1/100/שאלה 4.png" (feedback: L(A) מוכלת ממש ב-L(B))
q(1, "nfa", NFA_STEM,
  opts(EQ, B_IN_A, T(OTHERS), A_IN_B),
  "d", FB,
  r"ב-$A$ המצב ההתחלתי מקבל, ואחרי מעבר ה-$\varepsilon$ מגיעים למצב המקבל הימני רק אחרי מספר אי-זוגי של $a$-ים (בין שני המצבים הימניים קוראים $a$ בכל כיוון): "
  r"$L(A)=\{\varepsilon\}\cup\{a^{2k+1}\mid k\ge0\}$. "
  r"ב-$B$, אחרי ה-$a$ הראשון מעבר ה-$\varepsilon$ מביא למצב המקבל, ומשם כל $a$ נוסף חוזר אליו: $L(B)=a^*$. "
  r"לכן $L(A)\subseteq L(B)$, ו-$aa\in L(B)\setminus L(A)$ — ההכלה ממש.",
  image="images/exams/MQ1-Q1.png")

# slot 1, variant b — "שאלות תשפה (חלק עם תשובות נכונות)/1.jpg" (feedback); diagram from "100.docx"
q(2, "nfa", NFA_STEM,
  opts(EQ, A_IN_B, T(OTHERS), B_IN_A),
  "b", FB,
  r"ב-$A$ המצב ההתחלתי מקבל, ומגיעים למצב המקבל הימני רק אחרי $aa$; מעבר ה-$\varepsilon$ חזרה מאפשר לקרוא משם עוד $a$-ים. "
  r"לכן $L(A)=\{\varepsilon\}\cup\{a^k\mid k\ge2\}$, ואילו $L(B)=a^*$. "
  r"מתקיים $L(A)\subseteq L(B)$, ו-$a\in L(B)\setminus L(A)$ — ההכלה ממש.",
  image="images/exams/MQ1-Q2.png")

L1L2_Q = r"כמה מילים יש בשפה $L_1\cdot L_2$?"

# slot 2, variant a — "בוחן 1/100/שאלה 2.jpg" (feedback: 5)
q(3, "basics",
  r"תהי $L_1=\{a,ab\}$ ותהי $L_2=\{\varepsilon,b,bbb\}$ שפות מעל הא״ב $\{a,b\}$." "\n" + L1L2_Q,
  opts(M("4"), T("לפחות 6"), M("3"), M("5")),
  "d", FB,
  r"$L_1\cdot L_2=\{a,\ ab,\ abbb\}\cup\{ab,\ abb,\ abbbb\}$. המילה $ab$ מתקבלת פעמיים ($a\cdot b$ וגם $ab\cdot\varepsilon$), "
  r"ולכן יש בדיוק 5 מילים שונות: $a,ab,abb,abbb,abbbb$.")

# slot 2, variant b — options as printed in "בוחן 1/100/100.docx"; key from "100 (2).pdf" (100/100)
q(4, "basics",
  r"תהי $L_1=\{a,ab,abb\}$ ותהי $L_2=\{\varepsilon,b\}$ שפות מעל הא״ב $\{a,b\}$." "\n" + L1L2_Q,
  opts(T("לפחות 6"), M("5"), M("3"), M("4")),
  "d", M100,
  r"$L_1\cdot L_2=\{a,ab\}\cup\{ab,abb\}\cup\{abb,abbb\}=\{a,ab,abb,abbb\}$. "
  r"המילים $ab$ ו-$abb$ מתקבלות פעמיים, ולכן יש 4 מילים שונות בלבד.")

# slot 3, variant a — "בוחן 1/100/שאלה 3.jpg" (feedback: 010110); diagram from "100 (1).docx" (larger copy)
q(5, "dfa",
  r"איזו מילה מתקבלת על ידי האס״ד הבא, מעל הא״ב הבינארי?",
  opts(M("100010"), M("010001"), M(r"\varepsilon"), M("010110")),
  "d", FB,
  r"האס״ד מגיע למצב המקבל (עם לולאת $0,1$) בדיוק כשקוראים שני $1$ רצופים, כלומר $L=\{0,1\}^*11\{0,1\}^*$. "
  r"רק $010110$ מכילה $11$; ב-$100010$ וב-$010001$ אין $11$, ו-$\varepsilon$ נדחית כי המצב ההתחלתי אינו מקבל.",
  image="images/exams/MQ1-Q5.png")

# slot 4, variant a — "בוחן 1/100/שאלה 6.png" (feedback: 010110); diagram from "100.docx" (larger copy)
q(6, "nfa",
  r"איזו מילה מתקבלת על ידי האסל״ד הבא, מעל הא״ב הבינארי?",
  opts(M("1010"), M("010001"), M("100010"), M("010110")),
  "d", FB,
  r"האסל״ד נשאר ב-$q_1$ ו״מנחש״ את ה-$1$ שאחריו נותרו בדיוק עוד שתי אותיות, ולכן הוא מקבל בדיוק את המילים שהאות השלישית מהסוף שלהן היא $1$: "
  r"$L=\{0,1\}^*1\{0,1\}^2$. ב-$010110$ שלוש האותיות האחרונות הן $110$ — מתקבלת; "
  r"ב-$1010$, $010001$ ו-$100010$ האות השלישית מהסוף היא $0$.",
  image="images/exams/MQ1-Q6.png")

PS = (r"יהי $B$ אוטומט החזקה השקול לאסל״ד $A$, כך שמתקיים $L(A)=L(B)$." "\n"
      r"נניח כי השתמשנו באלגוריתם הסטנדרטי שנלמד בהרצאה כדי לבנות את $B$." "\n")

# slot 5, variant a — "בוחן 1/100/שאלה 1.jpg" (feedback: 2^n)
q(7, "nfa",
  r"יהי $A$ אסל״ד ללא מעברי $\varepsilon$ המכיל $n$ מצבים." "\n" + PS +
  r"כמה מצבים יש לכל היותר באוטומט החזקה $B$?",
  opts(M(r"(2n)!"), M(r"2^n"), M(r"2n"), M(r"n^2")),
  "b", FB,
  r"בבניית החזקה כל מצב של $B$ הוא תת-קבוצה של קבוצת המצבים של $A$. "
  r"לקבוצה בגודל $n$ יש $2^n$ תתי-קבוצות, ולכן ל-$B$ יש לכל היותר $2^n$ מצבים.")

# slot 5, variant b — "בוחן 1/100/100 (2).pdf" p.5 (pick c, attempt graded 100/100);
# "100 (1).docx" (different option order) also says "תשובה נכונה : d" = 2^{n-1} there
q(8, "nfa",
  r"יהי $A$ אסל״ד ללא מעברי $\varepsilon$ המכיל $n$ מצבים, מתוכם מצב אחד בלבד הוא מצב מקבל." "\n" + PS +
  r"כמה מצבים מקבלים יש לכל היותר באוטומט החזקה $B$?",
  opts(M(r"2^n"), M(r"(n-1)!"), M(r"2^{n-1}"), M(r"n^2")),
  "c", M100,
  r"מצב של $B$ (תת-קבוצה של מצבי $A$) הוא מקבל אם״ם הוא מכיל את המצב המקבל היחיד של $A$. "
  r"תת-קבוצה כזו נקבעת ע״י בחירה חופשית של אילו מ-$n-1$ המצבים האחרים נכללים בה, ולכן יש לכל היותר $2^{n-1}$ מצבים מקבלים.")

# slot 6, variant a — "בוחן 1/100/שאלה 5.png" (feedback: "לא נכון")
q(9, "basics",
  r"קיימת שפה מעל הא״ב הבינארי, שגם היא וגם משלימתה מכילות את המילה הריקה.",
  [dict(T("נכון"), id="a"), dict(T("לא נכון"), id="b")],
  "b", FB,
  r"$L\cap\overline{L}=\emptyset$: כל מילה, ובפרט $\varepsilon$, שייכת לשפה $L$ או למשלימה $\overline{L}$ — אבל לא לשתיהן. "
  r"לכן אין שפה שגם היא וגם משלימתה מכילות את המילה הריקה.")

MB = "מבדקים במודל/"
exam = {
    "examCode": "MQ1",
    "examLabel": "בוחן מודל 1",
    "year": 2025,
    "course": "62208",
    "source": "moodle",
    "files": {
        "exam": [MB + "בוחן 1/100/שאלה 1.jpg", MB + "בוחן 1/100/שאלה 2.jpg", MB + "בוחן 1/100/שאלה 3.jpg",
                 MB + "בוחן 1/100/שאלה 4.png", MB + "בוחן 1/100/שאלה 5.png", MB + "בוחן 1/100/שאלה 6.png",
                 MB + "שאלות תשפה (חלק עם תשובות נכונות)/1.jpg",
                 MB + "בוחן 1/100/100.docx", MB + "בוחן 1/100/100 (1).docx"],
        "solution": [MB + "בוחן 1/100/100 (2).pdf"],
        "crossChecks": [MB + "בוחן 1/100/100 (3).pdf"],
    },
    "contexts": {},
    "questions": Q,
}
out = pathlib.Path(__file__).resolve().parent.parent / "raw" / "MQ1.json"
out.write_text(json.dumps(exam, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {out} ({len(Q)} questions)")
