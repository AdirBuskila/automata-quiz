# -*- coding: utf-8 -*-
"""Emit tools/raw/MQ3.json — Moodle quiz 3 (בוחן 3, 20.1.2026), 4 questions.

Transcribed by eye from "מבדקים במודל/בוחן 3/בוחן 3/שאלה 1–4.jpeg" (in-attempt captures, "תשובה נשמרה",
"ניקוד השאלה: 25" each). They sit next to "ציון 100.jpeg": the summary of the ONLY attempt
(attempt 1, finished 20 Jan 2026 6:44 PM, 100/100). 4 × 25 = 100, so every saved pick is correct
(answerSource "moodle-100"). Option order as printed in those captures. Every key was re-derived.
The loose "בוחן 3/שאלה N.png" / "(2)" captures are NOT used as keys.
After running this, tools/raw/MQ3.json is the source of truth.
"""
import json, pathlib

M100 = "moodle-100"
OTHERS = "כל הטענות האחרות לא נכונות."


def T(v): return {"type": "text", "value": v}
def M(v): return {"type": "math", "value": v}


def opts(*vals):
    return [dict(v, id=k) for k, v in zip("abcd", vals)]


Q = []
def q(num, topic, question, options, correct, explanation, **kw):
    Q.append(dict(num=num, topic=topic, question=question, options=options, correctId=correct,
                  answerSource=M100, official=False, confidence="high", explanation=explanation, **kw))


q(1, "nerode",
  r"תהי $L$ השפה הנוצרת על ידי הביטוי הרגולרי $\Sigma^*(01+10)\Sigma^*$, מעל הא״ב הבינארי." "\n"
  r"כמה מצבים יש באס״ד $A$ עם מספר מצבים מינימלי כך שמתקיים $L(A)=L$?",
  opts(M("4"), T("לפחות 5"), M("3"), M("2")),
  "a",
  r"מילה מכילה $01$ או $10$ אם״ם מופיעות בה שתי האותיות, ולכן $L$ היא שפת המילים שמכילות גם $0$ וגם $1$. "
  r"יש אס״ד עם 4 מצבים: מצב התחלתי, ״ראינו רק $0$-ים״, ״ראינו רק $1$-ים״ ומצב מקבל בולע. "
  r"$T=\{\varepsilon,0,1,01\}$ היא קבוצה מפרידה (למשל הסיפא $1$ מפרידה בין $\varepsilon$ ל-$0$, ו-$\varepsilon$ מפרידה בין $01$ לכל האחרות) — לכן אי אפשר פחות מ-4.")

q(2, "classify",
  r"נתון האוטומט-מחסנית $M$ הבא, מעל הא״ב $\Sigma=\{a,b\}$." "\n" r"איזו מהטענות הבאות נכונה?",
  [dict(T(r"השפה $L(M)$ היא חסרת הקשר אבל לא-רגולרית."), id="a"),
   dict(T(r"השפה $L(M)$ היא סופית."), id="b"),
   dict(T(r"השפה $L(M)$ היא רגולרית ואינסופית."), id="c")],
  "a",
  r"ב-$q_1$ נדחף $a$ לכל $a$ שנקרא, המעבר ל-$q_2$ קורא $a$ אחד נוסף או אף אות, וב-$q_2$ כל $b$ מוציא $a$ מהמחסנית. "
  r"לכן $L(M)\subseteq a^*b^*$, לכל $n$ מתקיים $a^nb^n\in L(M)$, ומילה $a^ib^j$ עם $j>i$ לא מתקבלת. "
  r"השפה ח״ה (יש לה אוטומט מחסנית) ואינסופית, ולא-רגולרית: $\{a^i\mid i\ge0\}$ היא קבוצה מפרידה אינסופית — עבור $i<j$ הסיפא $b^j$ מפרידה בין $a^i$ ל-$a^j$.",
  image="images/exams/MQ3-Q2.png")

q(3, "nerode",
  r"תהי $L$ שפת המילים מהצורה $(\Sigma\Sigma\Sigma)^*+(\Sigma\Sigma\Sigma\Sigma)^*$ מעל הא״ב הבינארי." "\n"
  r"יהיו $x,y$ מילים כלשהן שונות זו מזו, מעל הא״ב הבינארי." "\n"
  r"איזו מהטענות הבאות היא טענה נכונה?",
  opts(T(r"אם $y\in L$ וגם $x\in L$ אז $x,y$ **לא**-ניתנות להפרדה ביחס לשפה $L$."),
       T(OTHERS),
       T(r"אם $y\in L$ וגם $x\notin L$ אז $x,y$ **לא**-ניתנות להפרדה ביחס לשפה $L$."),
       T(r"אם $y\notin L$ וגם $x\notin L$ אז $x,y$ **לא**-ניתנות להפרדה ביחס לשפה $L$.")),
  "b",
  r"$L$ היא שפת המילים שאורכן מתחלק ב-3 או ב-4. "
  r"א׳: $x=\varepsilon,\ y=000\in L$, והסיפא $z=0$ מפרידה ($0\notin L$ אבל $0000\in L$). "
  r"ג׳: הסיפא $z=\varepsilon$ מפרידה תמיד בין מילה בשפה למילה שלא בשפה. "
  r"ד׳: $x=0,\ y=00\notin L$, והסיפא $z=0$ מפרידה ($00\notin L$ אבל $000\in L$).")

q(4, "nerode",
  r"תהי $L$ שפה מעל הא״ב הבינארי. ותהי $L^R$ השפה ההפכית לה." "\n"
  r"כלומר, $w=\sigma_1\sigma_2\dots\sigma_n\in L$ אם ורק אם $w^R=\sigma_n\sigma_{n-1}\dots\sigma_1\in L^R$." "\n"
  r"איזו מהטענות הבאות נכונה?",
  opts(T(r"אם $L$ שפה לא-רגולרית אז מתקיים $\mathrm{Rank}(L)=\mathrm{Rank}(L^R)$."),
       T(r"אם $L$ שפה רגולרית אז מתקיים $\mathrm{Rank}(L)=\mathrm{Rank}(L^R)$."),
       T(OTHERS),
       T(r"אם $\mathrm{Rank}(L)\ne\mathrm{Rank}(L^R)$ אז קיימת קבוצה מפרידה אינסופית עבור $L^R$.")),
  "a",
  r"השפות הרגולריות סגורות להיפוך, ולכן אם $L$ לא-רגולרית גם $L^R$ לא-רגולרית (אחרת $L=(L^R)^R$ רגולרית), "
  r"ולפי משפט נרוד $\mathrm{Rank}(L)=\infty=\mathrm{Rank}(L^R)$ — א׳ נכונה. "
  r"ב׳ לא נכונה: ל-$L=\Sigma^*1\Sigma\Sigma$ מתקיים $\mathrm{Rank}(L)=8$, ואילו ל-$L^R=\Sigma\Sigma1\Sigma^*$ יש אס״ד מינימלי עם 5 מצבים. "
  r"ד׳ לא נכונה: אם הדרגות שונות, לפי א׳ שתי השפות רגולריות, ולכן ל-$L^R$ אין קבוצה מפרידה אינסופית.")

MB = "מבדקים במודל/בוחן 3/בוחן 3/"
exam = {
    "examCode": "MQ3",
    "examLabel": "בוחן מודל 3",
    "year": 2026,
    "examDate": "20.1.2026",
    "course": "62208",
    "source": "moodle",
    "files": {
        "exam": [MB + "שאלה 1.jpeg", MB + "שאלה 2.jpeg", MB + "שאלה 3.jpeg", MB + "שאלה 4.jpeg"],
        "solution": [MB + "ציון 100.jpeg"],
        "crossChecks": [],
    },
    "contexts": {},
    "questions": Q,
}
out = pathlib.Path(__file__).resolve().parent.parent / "raw" / "MQ3.json"
out.write_text(json.dumps(exam, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {out} ({len(Q)} questions)")
