# -*- coding: utf-8 -*-
"""Stage widgets + narration helpers for the `classify` videos (K01–K05 author).

Widgets (HTML fragments; ids follow stage.py conventions, `h` = starts hidden):
  ladder(p, chips)        nested boxes finite ⊂ regular ⊂ CFL ⊂ all; {p}-hl-<k> box highlight, {p}-c-<cid> chip
  pump(p, word, n, splits) pumping tape: cells, an `n` ruler over the first n cells ({p}-n), and per split s a group
                          {p}-s-<s> with x|y|z brackets + the y cells lit
  arcs(p, blocks, pairs)  letter blocks with comparison arcs above them: {p}-b-<i> block, {p}-a-<k> arc
  stack(p, frames)        stack columns, one per moment: {p}-f-<k>
  grid(p, rows, cols, ok) prefix × suffix membership table: {p}-c-<r>-<c> mark, {p}-r-<r> row highlight
Narration: tsay(tex) speaks the TeX shapes these videos use (None when it can't); Pk(sub, ...) = vid.P with `say`
derived through tsay (a TeX span it can't speak is an error: give say=).
Extra CSS lives in CSS (prefix kl-); put it in every stage that uses a widget.
"""
import re

import lexicon
from vid import P

CSS = """<style>
.kl-ladder{position:relative;width:1000px;direction:rtl}
.kl-box{position:relative;border:3px solid rgba(201,205,240,.55);border-radius:22px;padding:10px 20px 18px;background:rgba(255,255,255,.035)}
.kl-box .kl-box{margin-top:8px}
.kl-head{display:flex;align-items:center;gap:18px;min-height:76px}
.kl-name{font-size:37px;font-weight:700;white-space:nowrap}
.kl-chips{display:flex;gap:14px;flex-wrap:wrap;margin-inline-start:auto;direction:ltr}
.kl-chip{font-size:36px;background:var(--card);border:2px solid var(--line);border-radius:999px;padding:2px 18px}
.kl-chip.on{border-color:var(--warn);box-shadow:0 0 16px rgba(251,191,36,.5)}
.kl-hl{position:absolute;inset:-6px;border-radius:26px;border:6px solid var(--brand);box-shadow:0 0 26px rgba(45,212,191,.55);pointer-events:none}
.kl-fin{border-color:#38bdf8}.kl-reg{border-color:#2dd4bf}.kl-cfl{border-color:#a78bfa}.kl-all{border-color:#fb7185}
.kl-pump{position:relative;direction:ltr}
.kl-cells{display:flex;position:relative}
.kl-cell{position:relative;height:78px;border:2px solid var(--line);border-radius:12px;display:flex;align-items:center;
  justify-content:center;font-family:"Cambria Math",serif;font-size:42px;background:var(--card);box-sizing:border-box}
.kl-cell b{position:relative;font-weight:400}
.kl-ylit{position:absolute;inset:0;border-radius:10px;background:rgba(251,191,36,.30);box-shadow:0 0 0 3px var(--warn) inset}
.kl-ruler{position:absolute;top:-58px;height:40px;border:3px solid var(--brand);border-bottom:none;border-radius:10px 10px 0 0;
  box-sizing:border-box;text-align:center;font-size:28px;color:var(--brand)}
.kl-ruler span{position:relative;top:-36px;background:var(--bg);padding:0 10px}
.kl-br{position:absolute;top:92px;height:26px;border:3px solid #c9cdf0;border-top:none;border-radius:0 0 10px 10px;box-sizing:border-box}
.kl-br.y{border-color:var(--warn)}
.kl-br span{position:absolute;top:26px;left:0;right:0;text-align:center;font-size:30px}
.kl-br.y span{color:var(--warn)}
.kl-arcs{position:relative;direction:ltr}
.kl-blocks{display:flex;position:relative}
.kl-blk{height:96px;border:2px solid var(--line);border-radius:14px;display:flex;align-items:center;justify-content:center;
  font-size:48px;background:var(--card);box-sizing:border-box}
.kl-arcs svg{position:absolute;left:0;overflow:visible}
.kl-arc{fill:none;stroke-width:6;stroke-linecap:round}
.kl-stacks{display:flex;gap:34px;align-items:flex-end;direction:ltr}
.kl-stk{display:flex;flex-direction:column;align-items:center;gap:10px}
.kl-col{width:170px;min-height:150px;justify-content:flex-end;border:3px solid #c9cdf0;border-top:none;border-radius:0 0 14px 14px;padding:8px;
  display:flex;flex-direction:column;gap:6px;box-sizing:border-box}
.kl-it{font-size:40px;text-align:center;background:rgba(167,139,250,.18);border:2px solid #a78bfa;border-radius:10px;padding:2px 0}
.kl-cap{font-size:34px;color:var(--muted)}
table.kl-grid{border-collapse:separate;border-spacing:0;font-size:40px;background:var(--card2);border:1px solid var(--line);border-radius:14px}
table.kl-grid th,table.kl-grid td{position:relative;padding:8px 26px;text-align:center;border-bottom:1px solid var(--line)}
table.kl-grid thead th{color:var(--muted);font-weight:600}
table.kl-grid tbody tr:last-child>*{border-bottom:none}
.kl-ok{color:var(--ok);font-weight:700}.kl-no{color:var(--bad);font-weight:700}
.kl-row{position:absolute;inset:2px;border-radius:9px;background:rgba(45,212,191,.16);box-shadow:0 0 0 3px var(--brand) inset}
.kl-line{font-size:40px;direction:rtl}
.kl-big{font-size:54px}
</style>"""

# ----------------------------------------------------------------------------- ladder
RUNGS = [("all", "כל השפות"), ("cfl", "חסרות הקשר"), ("reg", "רגולריות"), ("fin", "סופיות")]


def ladder(p, chips=(), names=None):
    """chips: [(rung, cid, html)] placed in the rung's header (hidden until shown)"""
    names = dict(RUNGS, **(names or {}))
    by = {}
    for r, cid, h in chips:
        by.setdefault(r, []).append(f'<span id="{p}-c-{cid}" class="kl-chip h">{h}</span>')
    inner = ""
    for r, _ in reversed(RUNGS):
        inner = (f'<div class="kl-box kl-{r}" id="{p}-b-{r}"><i id="{p}-hl-{r}" class="kl-hl h"></i>'
                 f'<div class="kl-head"><span class="kl-name">{names[r]}</span>'
                 f'<span class="kl-chips">{"".join(by.get(r, []))}</span></div>{inner}</div>')
    return f'<div class="kl-ladder" id="{p}">{inner}</div>'


# ----------------------------------------------------------------------------- pumping tape
def pump(p, word, n=None, splits=None, cw=66, gap=8):
    """splits: {key: (a, b)} meaning x = word[:a], y = word[a:b], z = word[b:]"""
    step = cw + gap
    W = len(word) * step - gap
    cells = "".join(f'<span class="kl-cell" style="width:{cw}px;margin-right:{gap if i < len(word) - 1 else 0}px">'
                    f'<b>{c}</b></span>' for i, c in enumerate(word))
    o = [f'<div class="kl-pump" id="{p}" style="width:{W}px;height:160px;margin-top:60px">'
         f'<div class="kl-cells">{cells}</div>']
    if n is not None:
        o.append(f'<div id="{p}-n" class="kl-ruler h" style="left:0;width:{n * step - gap}px"><span>$n={n}$</span></div>')
    for key, (a, b) in (splits or {}).items():
        g = [f'<div id="{p}-s-{key}" class="h" style="position:absolute;inset:0">']
        for i in range(a, b):
            g.append(f'<i class="kl-ylit" style="left:{i * step}px;width:{cw}px;top:0;height:78px;position:absolute"></i>')
        for lab, s, e, cls in (("x", 0, a, ""), ("y", a, b, " y"), ("z", b, len(word), "")):
            if e > s:
                g.append(f'<div class="kl-br{cls}" style="left:{s * step + 3}px;width:{(e - s) * step - gap - 6}px">'
                         f'<span>${lab}$</span></div>')
        g.append("</div>")
        o.append("".join(g))
    o.append("</div>")
    return "".join(o)


# ----------------------------------------------------------------------------- comparison arcs
ARC_COL = ["#2dd4bf", "#fbbf24", "#38bdf8", "#fb7185"]


def arcs(p, blocks, pairs, bw=180, gap=26, hmax=140):
    """blocks: [html]; pairs: [(i, j)] block indices compared (arc k gets id {p}-a-<k>)"""
    step = bw + gap
    W = len(blocks) * step - gap
    bl = "".join(f'<div id="{p}-b-{i}" class="kl-blk" style="width:{bw}px;margin-right:{gap if i < len(blocks) - 1 else 0}px">'
                 f'{h}</div>' for i, h in enumerate(blocks))
    paths = []
    for k, (i, j) in enumerate(pairs):
        x1, x2 = i * step + bw / 2, j * step + bw / 2
        h = hmax * (0.45 + 0.55 * (j - i) / max(1, len(blocks) - 1))
        base = hmax + 8
        paths.append(f'<path id="{p}-a-{k}" class="kl-arc h" stroke="{ARC_COL[k % 4]}" '
                     f'd="M{x1:.0f},{base} C{x1:.0f},{base - h * 1.3:.0f} {x2:.0f},{base - h * 1.3:.0f} {x2:.0f},{base}"/>')
    return (f'<div class="kl-arcs" id="{p}" style="width:{W}px;padding-top:{hmax + 10}px">'
            f'<svg width="{W}" height="{hmax + 10}" style="top:0">{"".join(paths)}</svg>'
            f'<div class="kl-blocks">{bl}</div></div>')


# ----------------------------------------------------------------------------- stack columns
def stack(p, frames):
    """frames: [(caption_html, [item_html top → bottom])]"""
    cols = []
    for k, (cap, items) in enumerate(frames):
        its = "".join(f'<div class="kl-it">{it}</div>' for it in items)
        cols.append(f'<div id="{p}-f-{k}" class="kl-stk h"><div class="kl-col">{its}</div><div class="kl-cap">{cap}</div></div>')
    return f'<div class="kl-stacks" id="{p}">{"".join(cols)}</div>'


# ----------------------------------------------------------------------------- membership grid
def grid(p, rows, cols, ok, corner=""):
    """rows/cols: [(id, html)]; ok: {(rid, cid): bool}; marks start hidden"""
    head = "".join(f"<th>{h}</th>" for _, h in cols)
    body = []
    for rid, rh in rows:
        tds = "".join(f'<td><span id="{p}-c-{rid}-{cid}" class="h {"kl-ok" if ok[(rid, cid)] else "kl-no"}">'
                      f'{"$\\in L$" if ok[(rid, cid)] else "$\\notin L$"}</span></td>' for cid, _ in cols)
        body.append(f'<tr><th><i id="{p}-r-{rid}" class="kl-row h"></i>{rh}</th>{tds}</tr>')
    return (f'<table class="kl-grid" id="{p}" dir="ltr"><thead><tr><th>{corner}</th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


def opts_panel(pfx, Q, notes=None, stem=None):
    """an exam question as the app shows it: id chip, stem, options (bank html, never lettered).
    stem: a shortened stem ($TeX$ allowed) when the bank's full text does not fit the panel"""
    import stage as st
    return (f'<div class="qstem"><span class="qid">{Q["id"]}</span>{stem or Q["questionHtml"]}</div>'
            + st.options(pfx, [(o["id"], o["html"]) for o in Q["options"]], notes=notes))


def wtex(w):
    """a concrete word in run-length TeX: aaaab -> a^{4}b, '' -> \\varepsilon"""
    if not w:
        return "\\varepsilon"
    return "".join(g[0] + (f"^{{{len(g)}}}" if len(g) > 1 else "") for g in (m.group(0) for m in re.finditer(r"(.)\1*", w)))


# ----------------------------------------------------------------------------- speaking TeX
VAR = {"n": "אֶן", "m": "אֶם", "k": "קֵיי", "i": "אַיי", "j": "גֵ'יי", "p": "פִּי", "x": "אקס", "y": "וואי", "z": "זד",
       "u": "יוּ", "v": "וִי", "w": "דאבל יו", "L": "אֶל", "R": "אַר", "T": "טִי", "S": "אֶס", "N": "אֶן"}
LET = {"a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִּי", "0": "אפס", "1": "אחת"}
REL = {r"\le": "קטן או שווה ל§", r"\leq": "קטן או שווה ל§", r"\ge": "גדול או שווה ל§", r"\geq": "גדול או שווה ל§",
       "<": "קטן מ§", ">": "גדול מ§", "=": "שווה ל§", r"\ne": "שונה מ§", r"\neq": "שונה מ§", r"\in": "שייכת ל§",
       r"\notin": "לא שייכת ל§", r"\cap": "חיתוך", r"\cup": "איחוד", r"\subsetneq": "מוכלת ממש ב§",
       r"\subseteq": "מוכלת ב§", r"\mid": "כאשר", ",": ",", r"\cdot": "כפול", r"\wedge": "וגם", r"\vee": "או",
       r"\bmod": "מודולו", r"\ldots": "וכן הלאה", r"\dots": "וכן הלאה", r"\cdots": "וכן הלאה", "-": "מינוס",
       r"\varepsilon": "אפסילון", r"\Sigma": "סיגמא", r"\emptyset": "הקבוצה הריקה", r"\infty": "אינסוף",
       r"\Rightarrow": "ולכן", r"\to": "עובר ל§", r"\times": "כפול", r"\checkmark": "", "!": "עצרת"}
SKIP = {r"\{", r"\}", r"\,", r"\ ", r"\;", r"\quad", r"\!", r"\left", r"\right", "~"}
TOKRE = re.compile(r"\\[a-zA-Z]+|\\.|\d+|.")


class _Fail(Exception):
    pass


def _toks(t):
    return [x for x in TOKRE.findall(t) if not x.isspace()]


def _group(ts, i):
    """the argument at ts[i]: a {...} group or one token -> (tokens, next index)"""
    if ts[i] == "{":
        d, j = 0, i
        while True:
            d += {"{": 1, "}": -1}.get(ts[j], 0)
            if d == 0:
                return ts[i + 1:j], j + 1
            j += 1
    return [ts[i]], i + 1


def _num(s):
    return lexicon.DIGIT[s] if len(s) == 1 else s


def _speak(ts, exp=False):
    out, i = [], 0
    while i < len(ts):
        t = ts[i]
        if t in SKIP:
            i += 1
            continue
        if t == r"\mathrm" or t == r"\text":
            g, i = _group(ts, i + 1)
            w = "".join(g)
            out.append({"Rank": "ראנק", "and": "וגם", "or": "או"}.get(w) or _fail(w))
            continue
        if t == r"\pmod":
            g, i = _group(ts, i + 1)
            out.append("מודולו " + _speak(g, True))
            continue
        if t == r"\overline":
            g, i = _group(ts, i + 1)
            out.append("המשלימה של " + _speak(g))
            continue
        if t == r"\#":
            if i + 1 < len(ts) and ts[i + 1] == "_":
                g, i = _group(ts, i + 2)
                out.append("מספר ה§ " + _speak(g))
                continue
            _fail(t)
        if t == "|":
            j = ts.index("|", i + 1)
            out.append("האורך של " + _speak(ts[i + 1:j]))
            i = j + 1
            base = None
        elif t == "(":
            d, j = 0, i
            while True:
                d += {"(": 1, ")": -1}.get(ts[j], 0)
                if d == 0:
                    break
                j += 1
            inner = _speak(ts[i + 1:j])
            i = j + 1
            if i < len(ts) and ts[i] == "^":
                out.append(inner + ",")
                base = "grp"
            else:
                out.append(inner)
                continue
        elif t == "+":
            out.append("פלוס" if exp else "או")
            i += 1
            continue
        elif t in REL:
            out.append(REL[t])
            i += 1
            continue
        elif t.isdigit():
            out.append(_num(t))
            i += 1
            base = t
        elif t in LET and not exp:
            out.append(LET[t])
            i += 1
            base = t
        elif t in VAR:
            out.append(VAR[t])
            i += 1
            base = t
        elif t in LET:
            out.append(LET[t])
            i += 1
            base = t
        else:
            _fail(t)
        # postfix ^ and _
        while i < len(ts) and ts[i] in "^_":
            op = ts[i]
            g, i = _group(ts, i + 1)
            if op == "_":
                out.append(_speak(g, True))
            elif g == ["*"]:
                out.append("כוכבית")
            elif g == ["R"]:
                out.append("הפוך")
            elif g == ["+"]:
                out.append("פלוס")
            elif g == ["2"]:
                out.append("בריבוע")
            elif len(g) == 1 and g[0] in VAR and base in LET:
                out.append(VAR[g[0]])
            else:
                out.append("בחזקת " + _speak(g, True) + ("," if len(g) > 1 and i < len(ts) else ""))
    return re.sub(r",\s*,", ",", " ".join(o for o in out if o)).replace(" ,", ",")


def _fail(t):
    raise _Fail(t)


def tsay(tex):
    s = lexicon.tex_say(tex)
    if s is not None:
        return s
    try:
        s = re.sub(r"§\s*", "", _speak(_toks(tex)))
        return re.sub(r"(^|\s)([למב])ה(אורך|קבוצה|משלימה)", r"\1\2\3", s)
    except (_Fail, ValueError, IndexError):
        return None


MATH = re.compile(r"\$([^$]+)\$")


def auto_say(sub):
    def f(m):
        s = tsay(m.group(1))
        if s is None:
            raise ValueError(f"tsay can't speak ${m.group(1)}$ in: {sub}")
        return s
    s = MATH.sub(f, sub.replace("**", ""))
    return re.sub(r"<[^>]+>", "", s)


def Pk(sub, say=None, do=(), hold=0.0):
    return P(sub, say=say if say is not None else auto_say(sub), do=do, hold=hold)
