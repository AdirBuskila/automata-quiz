# -*- coding: utf-8 -*-
"""Pronunciation lexicon for the narration (he-IL-HilaNeural via edge-tts).

Subtitles keep the course spelling; the TTS gets the spoken form. Every entry was checked by synthesizing it and
transcribing it back with ivrit-ai/whisper-large-v3-turbo (2026-10-28):
  אס״ד raw -> heard "אסט" (wrong)        -> "אסאד" heard "אסד"
  אסל״ד raw -> heard "אסלת"              -> "אסלאד" (same; final ד/ת is the recognizer's ambiguity)
  ח״ה raw -> heard "היכה" (wrong)        -> said in full, "חסרת הקשר"
  Rank -> heard "רנק" (fine)              -> "ראנק"
  a -> "איי" heard "I"/"E" (wrong)         -> "אֵיי" heard "A";  b -> "בִּי" heard "B"
  run steps "אחת, קיו אחת אפס, …" ran together (heard "Q 1 0") -> "אחת: לקיו אחת." per step
Add a term here (never ad hoc in a script) and re-run the build: every video picks it up.
"""
import re

# Hebrew text replacements, applied to the spoken text (longest first). Both gershayim forms are covered.
WORDS = {
    "אס״ד": "אסאד",
    "אסל״ד": "אסלאד",
    "ח״ה": "חסרת הקשר",
    "שפות ח״ה": "שפות חסרות הקשר",    # plural / adjectival uses (longest match wins)
    "ח״ה סגורות": "חסרות הקשר סגורות",
    "שפות ה-ח״ה": "השפות חסרות ההקשר",
    "הח״ה": "חסרות ההקשר",            # "מחלקת הח״ה" was read "מחלקת החסרת הקשר"
    # STT 2026-10-28: "למת הניפוח" (with or without niqqud) is heard "למטה ניפוח"; "הלמה של הניפוח" is heard exactly
    "בלמת הניפוח": "בלמה של הניפוח",
    "ללמת הניפוח": "ללמה של הניפוח",
    "שלמת הניפוח": "שהלמה של הניפוח",
    "ולמת הניפוח": "והלמה של הניפוח",
    "מלמת הניפוח": "מהלמה של הניפוח",
    "למת הניפוח": "הלמה של הניפוח",
    # STT 2026-10-29: plain "הכלה" (inclusion) is heard "הקלה"; vocalized it is heard right
    "הכלה": "הֲכָלָה",
    "הכלות": "הֲכָלוֹת",
    "אין אף חץ": "אין שום חץ",          # "אין אף חץ" ran together into nonsense
    "א״ב": "אָלֶף בֵּית",          # Adir: plain "אלף" was read "elef"
    "Rank": "ראנק",
    "ע״י": "על ידי",
}

DIGIT = {"0": "אפס", "1": "אחת", "2": "שתיים", "3": "שלוש", "4": "ארבע", "5": "חמש", "6": "שש", "7": "שבע",
         "8": "שמונה", "9": "תשע"}
LETTER = {"a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִּי", "x": "אקס", "y": "וואי", "z": "זד"}
SYMBOL = {r"\varepsilon": "אפסילון", r"\epsilon": "אפסילון", r"\delta": "דלתא", r"\Sigma": "סיגמא",
          r"\emptyset": "הקבוצה הריקה",
          r"\ell": "קבוע הניפוח"}    # spoken "אֵל" it collides with the language L


def state_say(name):
    """q_0 / q_{12} / q0 -> 'קיו אפס'"""
    m = re.fullmatch(r"q_?\{?(\d+)\}?", name)
    if not m:
        raise ValueError(f"not a state name: {name!r}")
    return "קיו " + " ".join(DIGIT[d] for d in m.group(1))


def word_say(w):
    """a word over the alphabet, letter by letter: 0110 -> 'אפס אחת אחת אפס'; '' -> 'אפסילון'"""
    if w == "":
        return "אפסילון"
    return " ".join(DIGIT.get(c) or LETTER[c] for c in w)


def tex_say(tex):
    """speak a TeX span when it is one of the simple shapes; None = the script must give an explicit `say`"""
    t = tex.strip().replace(r"\,", "").replace(" ", "")
    if t in SYMBOL:
        return SYMBOL[t]
    if re.fullmatch(r"[01ab]+", t):
        return word_say(t)
    if re.fullmatch(r"q_?\{?\d+\}?", t):
        return state_say(t)
    parts = re.split(r"\\to|\\rightarrow", t)
    if len(parts) > 1 and all(re.fullmatch(r"q_?\{?\d+\}?", p) for p in parts):
        return ", ".join(state_say(p) for p in parts)
    if t in (r"\{0,1\}", r"\{a,b\}"):
        return "הקבוצה " + " ו".join(word_say(c) for c in t[2:-2].split(","))
    return None


def say_hebrew(s):
    for k in sorted(WORDS, key=len, reverse=True):
        for v in (k, k.replace("״", '"')):
            s = s.replace(v, WORDS[k])
    # a prefix (ו, ב, ומ, …) glued with a hyphen ("ו-$q_2$", "ב-$0$") is read as one word, not "vav, hyphen"
    s = re.sub(r"(^|[\s(])([ובכלמהש]{1,3})-", r"\1\2", s)
    return s
