# -*- coding: utf-8 -*-
"""Authoring helpers for the guided courses ("צריך עזרה?").

A level is a Python module tools/needhelp/<course>/<ID>.py that builds `LEVEL = level(...)`.

    from nh import *
    LEVEL = level("F01", 1, "▶️", "הרצת אס״ד", "goal sentence",
        lesson=r'''<p>…$\\delta(q,a)$…</p>''',
        questions=[
          Q(r"stem with $tex$",
            [C(r"$11$", accepts(d, "11")), J("conceptual statement", False), ...],   # exactly ONE option is true
            why=r"explanation: why the right one is right AND why the tempting wrong ones are wrong",
            recap="one line shown in the summary when this was answered wrong"),
        ])

* `C(text, cond)`  an option whose truth is COMPUTED by a simulator (cond is a bool from tools/verify/needhelp/lib.py)
* `J(text, truth)` an option whose truth is a judged, conceptual statement (kept to a minimum, listed in the report)
* `Q(...)` refuses to build unless exactly one option is true (so "only one defensible option" is enforced at import).
* `B("24X-A-Q9", recap)` a real bank question (boss levels), pulled by id.

Text takes `$tex$` / `$$tex$$` (rendered to MathML at build time), `**bold**`, `` `code` ``, "\\n".
Lesson html is raw HTML plus `$tex$`; boxes: <div class="lesson-rule">🔑 …</div>, lesson-trap (⚠️), lesson-ex (worked example).
"""
import sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "verify" / "needhelp"))
from lib import *  # noqa: F401,F403  (simulators)


class Opt:
    def __init__(self, text, ok, kind):
        self.text, self.ok, self.kind = text, bool(ok), kind


def C(text, cond):
    return Opt(text, cond, "sim")


def J(text, truth):
    return Opt(text, truth, "judged")


class Question:
    def __init__(self, stem, opts, why, recap, table=None):
        n = sum(o.ok for o in opts)
        if n != 1:
            raise AssertionError(f"{n} true options (want exactly 1) in: {stem[:90]!r}\n  " +
                                 "\n  ".join(f"[{'T' if o.ok else 'F'}] {o.text}" for o in opts))
        if not 3 <= len(opts) <= 5:
            raise AssertionError(f"{len(opts)} options in: {stem[:60]!r}")
        if len({o.text for o in opts}) != len(opts):
            raise AssertionError(f"duplicate option text in: {stem[:60]!r}")
        fix = lambda t: t.replace("&quot;", '"')
        for o in opts:
            o.text = fix(o.text)
        self.stem, self.opts, self.why, self.recap, self.table = fix(stem), opts, fix(why), fix(recap), table
        self.id = None


def Q(stem, opts, why, recap, table=None):
    return Question(stem, opts, why, recap, table)


class Bank:
    def __init__(self, bid, recap, why=None):
        self.bid, self.recap, self.why = bid, recap, why


def B(bid, recap, why=None):
    return Bank(bid, recap, why)


class Level:
    def __init__(self, id, order, icon, title, goal, lesson, questions, boss=False):
        self.id, self.order, self.icon, self.title, self.goal = id, order, icon, title, goal
        self.lesson, self.questions, self.boss = lesson, questions, boss
        n = len(questions)
        if not 4 <= n <= 6:
            raise AssertionError(f"{id}: {n} questions (want 4-6)")
        if boss and not all(isinstance(q, Bank) for q in questions):
            raise AssertionError(f"{id}: a boss level is made of bank questions only")
        if not boss and any(isinstance(q, Bank) for q in questions):
            raise AssertionError(f"{id}: only the boss level pulls bank questions")
        for i, q in enumerate(questions, 1):
            if isinstance(q, Question):
                q.id = f"{id}-Q{i}"


def level(id, order, icon, title, goal, lesson, questions, boss=False):
    return Level(id, order, icon, title, goal, lesson, questions, boss)


# ----------------------------------------------------------------------------- table / description helpers
def ql(s):
    """TeX for a state name: '0' -> q_0, '12' -> q_{12}"""
    s = str(s)
    return f"q_{s}" if len(s) == 1 else "q_{" + s + "}"


def dfa_tab(d, order=None, caption=None):
    """transition table of a DFA whose states are strings, as a Q(table=...) value"""
    order = order or sorted(d.states, key=lambda x: str(x))
    t = {"head": [r"$\delta$"] + [f"${a}$" for a in d.alpha],
         "rows": [[f"${ql(q)}$"] + [f"${ql(d.delta[(q, a)])}$" for a in d.alpha] for q in order]}
    if caption:
        t["caption"] = caption
    return t


def dfa_info(d):
    acc = ", ".join(f"${ql(q)}$" for q in sorted(d.acc, key=str)) or "אין"
    return f"מצב התחלתי ${ql(d.start)}$, מצבים מקבלים: {acc}."


def nfa_tab(n, order=None):
    """transition table of an NFA (a column per letter, plus epsilon if used)"""
    order = order or sorted(n.states, key=str)
    cols = list(n.alpha) + ([""] if any(k[1] == "" for k in n.delta) else [])

    def cell(q, a):
        t = sorted(n.delta.get((q, a), ()), key=str)
        return r"$\emptyset$" if not t else r"$\{" + ",".join(ql(x) for x in t) + r"\}$"
    return {"head": [r"$\delta$"] + [(r"$\varepsilon$" if a == "" else f"${a}$") for a in cols],
            "rows": [[f"${ql(q)}$"] + [cell(q, a) for a in cols] for q in order]}


def nfa_info(n):
    acc = ", ".join(f"${ql(q)}$" for q in sorted(n.acc, key=str)) or "אין"
    return f"מצב התחלתי ${ql(n.start)}$, מצבים מקבלים: {acc}."


def quote_words(ws):
    return ", ".join(f"${w if w else chr(92) + 'varepsilon'}$" for w in ws)


def cls_opts(label):
    """the four standard options of a classification question; `label` is what classify_cert verified"""
    return [C(text, label == k) for k, text in CLASS_LABELS]


def classify(pred, alpha, cert, n=9):
    return classify_cert(pred, alpha, cert, n)


def pda_tab(p):
    """edge table of a PDA: from, read, pop, push, to (an empty symbol is shown as epsilon)"""
    def s(x):
        return r"$\varepsilon$" if x == "" else f"${x}$"
    rows = [[f"${ql(a)}$", s(b), s(c), s(e), f"${ql(d)}$"] for (a, b, c, d, e) in p.edges]
    return {"head": ["מ-", "קורא", "שולף", "דוחף", "אל"], "rows": rows}


def pda_info(p):
    acc = ", ".join(f"${ql(q)}$" for q in sorted(p.acc, key=str)) or "אין"
    return f"מצב התחלתי ${ql(p.start)}$, מצבים מקבלים: {acc}. המחסנית מתחילה ריקה."


def gram(rules):
    """a grammar written in TeX lines, one per variable, for a question stem"""
    return "\n".join("$" + r.replace("->", r"\to ").replace("|", r"\mid ").replace("ε", r"\varepsilon ") + "$" for r in rules.split(";"))
