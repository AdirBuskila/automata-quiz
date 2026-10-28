# -*- coding: utf-8 -*-
"""Widgets and narration helpers for the nerode videos (N01–N08).

Widgets (HTML with stable ids, class `h` = starts hidden; CSS is in `CSS`, put it once in a stage of the video):
  sufftest(pfx, pred, x, y, zs)   a suffix tester: rows z | xz | yz with ✓/✗; ids {pfx}-r-<k> row, {pfx}-s-<k> "מפרידה"
  pairs(pfx, T, cells)            a triangular pairs grid; ids {pfx}-c-<i>-<j> the cell text, {pfx}-h-<i>-<j> highlight
  buckets(pfx, groups)            class buckets; ids {pfx}-b-<k> box, {pfx}-w-<k>-<n> word chip
  chips(pfx, words)               a row of word chips; ids {pfx}-w-<n>, {pfx}-x-<n> (crossed out)
Narration: N(sub, say=None, do=(), hold=0) is vid.P whose spoken form comes from `tex_say` when the shared lexicon
cannot speak a TeX span (x, y, z, L, Rank(L), sets, a^k, ∈ L …). Anything tex_say does not know raises: give say=.
"""
import re

import lexicon
from vid import P, MATH

# ----------------------------------------------------------------------------- spoken TeX (nerode notation)
VAR = {"x": "אקס", "y": "וואי", "z": "זד", "w": "דאבליו", "k": "קיי", "i": "איי", "j": "ג'יי", "n": "אן", "m": "אֶם",
       "d": "די", "u": "יו", "c": "סי", "a": "אֵיי", "b": "בִּי", "p": "פי", "q": "קיו"}
UPPER = {"L": "אל", "T": "טי", "A": "אֵיי", "M": "אם"}
NUM = {"2": "שתיים", "3": "שלוש", "4": "ארבע", "5": "חמש", "6": "שש", "7": "שבע", "8": "שמונה", "9": "תשע",
       "10": "עשר", "11": "אחת עשרה", "12": "שתים עשרה", "16": "שש עשרה"}
OPS = [
    (r"\iff", " אם ורק אם "), (r"\Rightarrow", " גורר "), (r"\Leftrightarrow", " אם ורק אם "),
    (r"\notin", " לא שייכת ל- "), (r"\in", " שייכת ל- "), (r"\equiv", " שקולה ל- "),
    (r"\ne", " שונה מ- "), (r"\neq", " שונה מ- "), (r"\le", " קטן או שווה ל- "), (r"\leq", " קטן או שווה ל- "),
    (r"\ge", " גדול או שווה ל- "), (r"\geq", " גדול או שווה ל- "), (r"\cdot", " כפול "), (r"\times", " כפול "),
    (r"\cup", " איחוד "), (r"\cap", " חיתוך "), (r"\setminus", " פחות "), (r"\subseteq", " מוכלת ב- "),
    (r"\infty", " אינסוף "), (r"\varepsilon", " אפסילון "), (r"\emptyset", " הקבוצה הריקה "), (r"\Sigma", " סיגמא "),
    (r"\mid", " כאשר "), (r"\dots", " וכן הלאה "), (r"\ldots", " וכן הלאה "), (r"\to", " עובר ל- "),
    (r"\max", " מקסימום "), (r"\min", " מינימום "), (r"\bmod", " מודולו "), (r"\pmod", " מודולו "),
]


def _exp(e):
    """exponent text -> spoken"""
    e = e.strip("{}")
    if e == "*":
        return " כוכבית"
    if e == "R":
        return " ההפוכה"
    m = re.fullmatch(r"(\d*)([a-z])(?:\^2)?(?:([+-])(\d))?", e.replace("{", "").replace("}", ""))
    if m:
        k, v, s, c = m.groups()
        out = (NUM.get(k, lexicon.DIGIT.get(k, k)) + " " if k else "") + VAR[v]
        if "^2" in e:
            out += " בריבוע"
        if s:
            out += (" ועוד " if s == "+" else " פחות ") + lexicon.DIGIT[c]
        return " בחזקת " + out
    if re.fullmatch(r"\d+", e):
        return " בחזקת " + NUM.get(e, lexicon.DIGIT.get(e, e))
    raise ValueError(e)


def tex_say(t):
    """speak a nerode TeX span; ValueError if something is left that we do not know"""
    s0 = lexicon.tex_say(t)
    if s0 is not None:
        return s0
    s = t.replace(r"\,", " ").replace(r"\ ", " ").replace(r"\!", "")
    s = re.sub(r"\\mathrm\{Rank\}\(([^()]*)\)", lambda m: " ראנק של " + m.group(1) + " ", s)
    s = s.replace(r"\mathrm{Rank}", " ראנק ")
    s = re.sub(r"\\overline\{([^{}]*)\}", lambda m: " המשלים של " + m.group(1) + " ", s)
    s = re.sub(r"\\#_(\w)(\(w\))?", lambda m: " מספר ה-" + VAR.get(m.group(1), lexicon.DIGIT.get(m.group(1), "")) + " ", s)
    s = re.sub(r"\\in L(?![_\w])", " בשפה ", s)
    s = re.sub(r"\\notin L(?![_\w])", " לא בשפה ", s)
    s = re.sub(r"\\equiv_L", r"\\equiv", s)
    s = re.sub(r"\(([^()]*)\)\^(\{[^{}]*\}|\S)", lambda m: " " + m.group(1) + " בסוגריים" + _exp(m.group(2)) + " ", s)
    s = re.sub(r"([A-Za-z]|\\Sigma)\^(\{(?:[^{}]|\{[^{}]*\})*\}|\S)", lambda m: " " + m.group(1) + _exp(m.group(2)) + " ", s)
    s = re.sub(r"(\d)\^(\{[^{}]*\}|\S)", lambda m: " " + lexicon.DIGIT[m.group(1)] + _exp(m.group(2)) + " ", s)
    s = re.sub(r"\|(\w)\|", lambda m: " הגודל של " + m.group(1) + " ", s)
    s = re.sub(r"([A-Za-z])_(\{?\w+\}?)", lambda m: m.group(1) + " " + m.group(2).strip("{}") + " ", s)
    s = s.replace(r"\{", " הקבוצה ").replace(r"\}", " ").replace("|", " ")
    for k, v in sorted(OPS, key=lambda kv: -len(kv[0])):
        s = re.sub(re.escape(k) + r"(?![A-Za-z])", v, s)
    s = s.replace("=", " שווה ").replace("<", " קטן מ- ").replace(">", " גדול מ- ").replace("+", " ועוד ")
    s = s.replace("{", " ").replace("}", " ").replace("(", " ").replace(")", " ")

    def num(m):
        g = m.group(0)
        if re.fullmatch(r"[01]+", g):
            return " " + " ".join(lexicon.DIGIT[c] for c in g) + " "
        if g in NUM:
            return " " + NUM[g] + " "
        raise ValueError(g)
    s = re.sub(r"\d+", num, s)
    s = re.sub(r"[a-z]", lambda m: " " + VAR[m.group(0)] + " ", s)
    s = re.sub(r"[A-Z]", lambda m: " " + UPPER[m.group(0)] + " ", s)
    if "\\" in s or re.search(r"[^\s֐-׿',\-]", s):
        raise ValueError(f"cannot speak ${t}$ -> {s!r}")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r"-\s+", "-", s)
    return s


def say_of(sub):
    def rep(m):
        return tex_say(m.group(1))
    s = MATH.sub(rep, sub.replace("**", ""))
    return re.sub(r"<[^>]+>", "", s)


def N(sub, say=None, do=(), hold=0.0):
    if say is None:
        try:
            say = say_of(sub)
        except (ValueError, KeyError) as e:
            raise ValueError(f"no spoken form: {e}\n  in: {sub}\n  -> give say=") from None
    return P(sub, say=say, do=do, hold=hold)


def ws(w):
    """a word spoken letter by letter (ε for the empty word)"""
    return lexicon.word_say(w)


# ----------------------------------------------------------------------------- widgets
CSS = """<style>
.nr-w{font-family:"Cambria Math",serif;font-style:italic;direction:ltr;unicode-bidi:isolate;white-space:nowrap}
.nr-w .x{color:#5eead4;font-style:italic}
table.nr-st{border-collapse:separate;border-spacing:0;font-size:40px;background:var(--card2);border:1px solid var(--line);
  border-radius:14px;overflow:hidden;direction:ltr}
table.nr-st th,table.nr-st td{position:relative;padding:7px 26px;text-align:center;border-bottom:1px solid var(--line)}
table.nr-st thead th{color:var(--muted);font-weight:600;font-size:30px}
table.nr-st tbody tr:last-child>*{border-bottom:none}
.nr-in{color:var(--ok);font-weight:700;margin-left:10px}.nr-out{color:var(--bad);font-weight:700;margin-left:10px}
.nr-sep{position:absolute;inset:2px;border-radius:9px;background:rgba(45,212,191,.16);box-shadow:0 0 0 3px var(--brand) inset}
.nr-tag{position:absolute;right:-150px;top:50%;transform:translateY(-50%);font-size:26px;font-weight:700;color:var(--brand);
  direction:rtl;white-space:nowrap}
table.nr-pg{border-collapse:separate;border-spacing:8px;direction:ltr;font-size:46px}
table.nr-pg th{color:var(--brand2);font-weight:600;padding:2px 14px;font-size:44px}
table.nr-pg td{position:relative;min-width:150px;height:84px;text-align:center;border-radius:10px;background:var(--card2);
  border:1px solid var(--line)}
table.nr-pg td.nr-off{background:none;border:none}
table.nr-pg td .nr-c{position:relative;font-family:"Cambria Math",serif;font-style:italic}
table.nr-pg td .nr-eq{color:var(--bad);font-style:normal;font-weight:700}
.nr-hl{position:absolute;inset:-2px;border-radius:10px;box-shadow:0 0 0 4px var(--brand) inset;background:rgba(45,212,191,.14)}
.nr-hlb{position:absolute;inset:-2px;border-radius:10px;box-shadow:0 0 0 4px var(--bad) inset;background:rgba(251,113,133,.14)}
.nr-bk{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;direction:rtl;max-width:1040px}
.nr-b{position:relative;min-width:200px;border-radius:16px;border:3px solid #c9cdf0;background:var(--card2);padding:10px 16px 12px;
  display:flex;flex-direction:column;align-items:center;gap:8px}
.nr-b.acc{border-color:var(--ok);box-shadow:0 0 0 3px rgba(52,211,153,.25)}
.nr-b .nr-bl{font-size:30px;color:var(--muted);direction:rtl;text-align:center}
.nr-b .nr-ws{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;direction:ltr;max-width:420px}
.nr-chip{position:relative;font-family:"Cambria Math",serif;font-style:italic;font-size:38px;background:var(--card);
  border:1px solid var(--line);border-radius:10px;padding:2px 12px;direction:ltr}
.nr-chips{display:flex;gap:14px;direction:ltr;align-items:center;font-size:34px}
.nr-xo{position:absolute;inset:0;border-radius:10px;background:linear-gradient(transparent calc(50% - 2px),var(--bad) calc(50% - 2px),
  var(--bad) calc(50% + 2px),transparent calc(50% + 2px));background-color:rgba(251,113,133,.15)}
.nr-big{font-size:40px;direction:rtl;text-align:center}
.nr-sm{font-size:28px;color:var(--muted);direction:rtl;text-align:center}
.nr-bounds{display:flex;gap:26px;justify-content:center;direction:rtl}
.nr-bound{font-size:32px;border-radius:14px;padding:10px 22px;border:2px solid var(--line);background:var(--card2);direction:rtl}
.nr-bound.up{border-color:var(--brand2)}.nr-bound.lo{border-color:var(--brand)}
</style>"""


def wd(w, xlen=0):
    """a word as HTML (ε for the empty word); the first xlen letters are tinted (the x/y part of xz)"""
    if w == "":
        return '<span class="nr-w">ε</span>'
    if xlen:
        return f'<span class="nr-w"><span class="x">{w[:xlen] or ""}</span>{w[xlen:]}</span>'
    return f'<span class="nr-w">{w}</span>'


def mark(ok):
    return '<span class="nr-in">✓</span>' if ok else '<span class="nr-out">✗</span>'


def sufftest(pfx, pred, x, y, zs, xname="x", yname="y"):
    """suffix tester table; every ✓/✗ is computed with pred. Returns (html, [separating?])"""
    rows, seps = [], []
    for k, z in enumerate(zs):
        a, b = pred(x + z), pred(y + z)
        seps.append(a != b)
        tag = f'<i id="{pfx}-s-{k}" class="nr-sep h"></i>' if a != b else ""
        tagt = f'<span id="{pfx}-t-{k}" class="nr-tag h">מפרידה ✂</span>' if a != b else ""
        rows.append(f'<tr id="{pfx}-r-{k}" class="h"><td>{tag}{wd(z)}</td><td>{wd(x + z, len(x))} {mark(a)}</td>'
                    f'<td>{wd(y + z, len(y))} {mark(b)}{tagt}</td></tr>')
    head = (f'<thead><tr><th>$z$</th><th>${xname}z$ &nbsp;({wd(x)})</th><th>${yname}z$ &nbsp;({wd(y)})</th></tr></thead>')
    return f'<table class="nr-st" id="{pfx}">{head}<tbody>{"".join(rows)}</tbody></table>', seps


def pairs(pfx, T, cells, labels=None):
    """triangular grid over the words T. cells: {(i, j): text-html} for i > j (row word i, column word j)."""
    labels = labels or [wd(w) for w in T]
    head = "<tr><th></th>" + "".join(f"<th>{labels[j]}</th>" for j in range(len(T) - 1)) + "</tr>"
    body = []
    for i in range(1, len(T)):
        tds = []
        for j in range(len(T) - 1):
            if j < i:
                tds.append(f'<td><i id="{pfx}-h-{i}-{j}" class="nr-hl h"></i>'
                           f'<span id="{pfx}-c-{i}-{j}" class="nr-c h">{cells.get((i, j), "")}</span></td>')
            else:
                tds.append('<td class="nr-off"></td>')
        body.append(f"<tr><th>{labels[i]}</th>{''.join(tds)}</tr>")
    return f'<table class="nr-pg" id="{pfx}">{head}{"".join(body)}</table>'


def pair_cells(pred, T, alpha, slen=8):
    """for every pair i > j of T: the shortest separating suffix (lib.separable), or None if equivalent"""
    from lib import separable
    return {(i, j): separable(pred, T[i], T[j], alpha, slen) for i in range(1, len(T)) for j in range(i)}


def cell_html(z):
    return '<span class="nr-eq">≡</span>' if z is None else wd(z)


def buckets(pfx, groups, hidden=True):
    """groups: [(label_html, [words], accepting)] -> boxes; chips hidden when hidden=True"""
    out = []
    for k, (lab, ws_, acc) in enumerate(groups):
        chips_ = "".join(f'<span id="{pfx}-w-{k}-{n}" class="nr-chip{" h" if hidden else ""}">{wd(w) if isinstance(w, str) else w[0]}</span>'
                         for n, w in enumerate(ws_))
        out.append(f'<div id="{pfx}-b-{k}" class="nr-b{" acc" if acc else ""}{" h" if hidden else ""}">'
                   f'<div class="nr-bl">{lab}</div><div class="nr-ws">{chips_}</div></div>')
    return f'<div class="nr-bk" id="{pfx}">{"".join(out)}</div>'


def chips(pfx, items, lead=""):
    """a row of chips (words or html); ids {pfx}-w-<n>, {pfx}-x-<n> crossed out"""
    cs = "".join(f'<span id="{pfx}-w-{n}" class="nr-chip"><i id="{pfx}-x-{n}" class="nr-xo h"></i>'
                 f'{wd(w) if isinstance(w, str) else w[0]}</span>' for n, w in enumerate(items))
    return f'<div class="nr-chips" id="{pfx}">{lead}{cs}</div>'


def table(pfx, head, rows, hidden=True):
    """a plain LTR table (nr-st look). head: [html]; rows: [[html]] -> row ids {pfx}-r-<k>, cell highlight {pfx}-s-<k>"""
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = []
    for k, r in enumerate(rows):
        tds = "".join((f'<td><i id="{pfx}-s-{k}" class="nr-sep h"></i>{c}</td>' if n == 0 else f"<td>{c}</td>")
                      for n, c in enumerate(r))
        trs.append(f'<tr id="{pfx}-r-{k}"{" class=\"h\"" if hidden else ""}>{tds}</tr>')
    return f'<table class="nr-st" id="{pfx}"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def completions(pred, x, alpha, n=6):
    """{z : xz in L} for z up to length n (finite languages: the exact 'what is still missing')"""
    from lib import words
    return [z for z in words(alpha, n) if pred(x + z)]


def setw(zs):
    """a set of words as HTML: {ε, b} / ∅"""
    if not zs:
        return '<span class="nr-w">∅</span>'
    return '<span class="nr-w">{' + ", ".join(z or "ε" for z in zs) + "}</span>"


def opts_of(Q):
    return [(o["id"], o["html"]) for o in Q["options"]]
