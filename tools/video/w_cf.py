# -*- coding: utf-8 -*-
"""Widgets and helpers for the `cf` videos (G01–G08: grammars and pushdown automata).

Everything drawn here comes from a verified object (lib.CFG / lib.PDA): derivations are searched, trees are built from
the derivation, PDA runs are replayed edge by edge and every configuration is checked.

Widgets (ids, all prefixed by the caller's pfx):
  grammar(pfx, text)            grammar panel, one row per variable; {pfx}-a-<V>-<k> highlights alternative k of V
  deriv_lines(pfx, steps)       leftmost derivation, one line per step: {pfx}-l-<i> (line 0 = the start variable)
  tree_svg(pfx, steps)          derivation tree growing: {pfx}-t-<i> = what step i adds; {pfx}-x-<i> rings the node
                                expanded at step i
  pda_svg(pfx, M, pos, names)   PDA diagram, edge labels "σ,x→y" stacked: {pfx}-hs-<q>, {pfx}-he-<p>-<r>,
                                {pfx}-hl-<edge index> (the one label being used)
  stack(pfx, snaps)             live stack column: {pfx}-c-<depth>-<sym> cells, {pfx}-e "ריקה"
  run_pda(...)                  phrases replaying a PDA run (state, edge, tape cursor, stack)
Speech: tsay(tex) speaks the TeX subset used in these videos; p(sub, ...) = P with say derived through tsay.
"""
import re
import math
import html as _html

import stage as st
from vid import P, show, hide
import lexicon

# ----------------------------------------------------------------------------- speech
TERM = {"a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִי"}
PARAM = {"n": "אֵן", "m": "אֶם", "k": "קֵיי", "i": "אַיי", "j": "גֵ'יי", "x": "אִקְס", "y": "וַואי", "w": "דַאבְּלְיוּ",
         "u": "יוּ", "l": "אֶל", "p": "פִּי", "r": "אָר", "z": "זֶד", "e": "אִי", "h": "הֵייץ'", "s": "אֶס"}
VARS = {"S": "אֶס", "A": "אֵיי גדולה", "B": "בִּי גדולה", "C": "סִי גדולה", "T": "טִי", "M": "אֶם", "N": "אֶן",
        "X": "אִקְס גדולה", "Y": "וַואי גדולה", "Z": "זֶד", "H": "הֵייץ'", "G": "גֵ'י", "L": "אֶל", "V": "וִי",
        "R": "אָר", "D": "דִי גדולה", "P": "פִּי גדולה", "Q": "קיוּ", "K": "קֵיי גדולה"}
NUM = {"0": "אפס", "1": "אחת", "2": "שתיים", "3": "שלוש", "4": "ארבע", "5": "חמש", "6": "שש", "7": "שבע",
       "8": "שמונה", "9": "תשע", "10": "עשר", "12": "שתים עשרה", "16": "שש עשרה", "18": "שמונה עשרה"}
CMD = {r"\to": " גוזר ", r"\rightarrow": " גוזר ", r"\Rightarrow": " גוזר ", r"\varepsilon": " אפסילון ",
       r"\epsilon": " אפסילון ", r"\ge": " גדול או שווה ל", r"\geq": " גדול או שווה ל", r"\le": " קטן או שווה ל",
       r"\leq": " קטן או שווה ל", r"\ne": " שונה מ", r"\neq": " שונה מ", r"\cup": " איחוד ", r"\cap": " חיתוך ",
       r"\subsetneq": " מוכלת ממש ב", r"\subseteq": " מוכלת ב", r"\in": " שייכת ל", r"\notin": " לא שייכת ל",
       r"\Sigma": " סיגמא ", r"\sigma": " סיגמא ", r"\emptyset": " הקבוצה הריקה ", r"\ldots": " וכן הלאה ",
       r"\dots": " וכן הלאה ", r"\cdot": " ", r"\delta": " דלתא ", r"\wedge": " וגם ", r"\land": " וגם ",
       r"\Leftrightarrow": " אם ורק אם ", r"\iff": " אם ורק אם ", r"\times": " כפול ", r"\pm": " פלוס מינוס ",
       r"\lvert": "", r"\rvert": ""}
SYM = {"<": " קטן מ", ">": " גדול מ", "=": " שווה ", "+": " ועוד ", "-": " פחות ", ",": ", ", "(": " ", ")": " ",
       "|": " ", ";": ", "}


def _num(s):
    if s in NUM:
        return NUM[s]
    return " ".join(NUM[c] for c in s)


def _atom(t):
    """one letter / digit run -> spoken"""
    if t.isdigit():
        return _num(t)
    if t in VARS:
        return VARS[t]
    if t in TERM:
        return TERM[t]
    if t in PARAM:
        return PARAM[t]
    raise ValueError(f"tsay: unknown symbol {t!r}")


def _exp(e):
    """exponent text (no braces) -> spoken"""
    if e == "*":
        return " כוכבית"
    if e == "+":
        return " פלוס"
    if e == "R":
        return " הפוך"
    return " בחזקת " + _plain(e)


def _plain(t):
    """a flat run like 2n, n+m, k+1, 2i (inside an exponent or a condition)"""
    out = []
    for tok in re.findall(r"\d+|[A-Za-z]|[+\-*<>=]", t):
        if tok.isdigit():
            out.append(_num(tok))
        elif tok in SYM:
            out.append(SYM[tok].strip())
        else:
            out.append(_atom(tok))
    return " ".join(out)


def tsay(tex, set_mid="כך ש", mid="או"):
    """speak a TeX span of the subset used in the cf videos; raises on anything unknown"""
    t = tex.strip()
    t = t.replace(r"\,", " ").replace(r"\ ", " ").replace(r"\quad", " ").replace(r"\left", "").replace(r"\right", "")
    t = re.sub(r"\\mathrm\{([^}]*)\}|\\text\{([^}]*)\}|\\mathbf\{([^}]*)\}", lambda m: " " + (m.group(1) or m.group(2) or m.group(3)) + " ", t)
    t = re.sub(r"\\textcolor\{[^}]*\}\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\underline\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\overline\{([^}]*)\}", r" המשלים של \1 ", t)
    t = re.sub(r"\\#_\{?([a-z0-9])\}?", lambda m: f" מספר ה{_atom(m.group(1))} ", t)
    t = re.sub(r"L\(([GM])\)", lambda m: " אֶל של " + VARS[m.group(1)] + " ", t)
    t = re.sub(r"q_\{?(\d+)\}?", lambda m: " " + lexicon.state_say("q_" + m.group(1)) + " ", t)
    out, depth = [], 0
    i = 0
    while i < len(t):
        c = t[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|[{}#|])", t[i:])
            name = "\\" + m.group(1)
            i += len(m.group(0))
            if name == r"\{":
                out.append(" הקבוצה ")
                depth += 1
            elif name == r"\}":
                depth -= 1
                out.append(" ")
            elif name == r"\mid":
                out.append(f" {set_mid} " if depth > 0 else f" {mid} ")
            elif name in CMD:
                out.append(CMD[name])
            else:
                raise ValueError(f"tsay: unknown command {name} in {tex!r}")
            continue
        if c == "^":
            m = re.match(r"\^(\{([^{}]*)\}|.)", t[i:])
            e = m.group(2) if m.group(2) is not None else m.group(1)
            out.append(_exp(e.replace("\\ast", "*")))
            i += len(m.group(0))
            continue
        if c == "_":
            m = re.match(r"_(\{([^{}]*)\}|.)", t[i:])
            e = m.group(2) if m.group(2) is not None else m.group(1)
            out.append(" " + _plain(e))
            i += len(m.group(0))
            continue
        if c in "{}":
            i += 1
            continue
        if c.isdigit():
            m = re.match(r"\d+", t[i:])
            run = m.group(0)
            # binary words (0110) are read digit by digit, small numbers as numbers
            out.append(" " + (lexicon.word_say(run) if (len(run) > 1 and set(run) <= {"0", "1"}) else _num(run)) + " ")
            i += len(run)
            continue
        if "֐" <= c <= "׿":          # already-spoken Hebrew (inserted by the substitutions above)
            m = re.match(r"[֐-׿' ]+", t[i:])
            out.append(m.group(0))
            i += len(m.group(0))
            continue
        if c.isalpha():
            out.append(" " + _atom(c) + " ")
            i += 1
            continue
        if c in SYM:
            out.append(SYM[c])
            i += 1
            continue
        if c.isspace():
            i += 1
            continue
        if c in "'":
            i += 1
            continue
        raise ValueError(f"tsay: unknown char {c!r} in {tex!r}")
    s = re.sub(r"\s+", " ", "".join(out)).strip()
    s = re.sub(r"(שווה ל|שונה מ|קטן מ|גדול מ|מוכלת ממש ב|מוכלת ב|שייכת ל) ", r"\1", s)
    return re.sub(r"\s+,", ",", s)


MATH = re.compile(r"\$([^$]+)\$")


def say_of(sub, **kw):
    s = MATH.sub(lambda m: tsay(m.group(1), **kw), sub.replace("**", ""))
    return re.sub(r"<[^>]+>", "", s)


def p(sub, say=None, do=(), hold=0.0, **kw):
    """P whose spoken form is derived from the subtitle with tsay (unless say= is given)"""
    return P(sub, say=say if say is not None else say_of(sub, **kw), do=do, hold=hold)


# ----------------------------------------------------------------------------- TeX of grammars
def alt_tex(alt):
    return r"\varepsilon" if alt == "" else alt


def rule_tex(G, v):
    return f"{v}\\to " + r"\mid ".join(alt_tex(a) for a in G.rules[v])


def gram_tex(G, order=None):
    """multi-line grammar as \\begin{array}{l} rows (CLAUDE.md: mobile/width rule)"""
    order = order or _order(G)
    rows = r"\\ ".join(rule_tex(G, v) for v in order)
    return r"\begin{array}{l}" + rows + r"\end{array}"


def _order(G):
    vs = list(G.rules)
    return [G.start] + [v for v in vs if v != G.start]


def grammar(pfx, G, order=None, big=False):
    """grammar card: one row per variable, each alternative a separate highlightable span"""
    rows = []
    for v in order or _order(G):
        alts = []
        for k, a in enumerate(G.rules[v]):
            sep = "<span class=\"cf-bar\">$\\mid$</span>" if k else ""
            alts.append(f'{sep}<span class="cf-alt"><i id="{pfx}-a-{v}-{k}" class="cf-ahi h"></i>${alt_tex(a)}$</span>')
        rows.append(f'<div class="cf-grow" id="{pfx}-r-{v}"><i id="{pfx}-rh-{v}" class="cf-rhi h"></i>'
                    f'<span class="cf-lhs">${v}\\to$</span>{"".join(alts)}</div>')
    return f'<div class="cf-gram{" big" if big else ""}" id="{pfx}" dir="ltr">{"".join(rows)}</div>'


# ----------------------------------------------------------------------------- derivations
def leftmost(G, w, limit=4, depth=24):
    """all leftmost derivations of w (up to `limit`), each a list of steps (form, pos, var, alt_index)"""
    found = []

    def go(form, steps):
        if len(found) >= limit or len(steps) > depth:
            return
        i = 0
        while i < len(form) and form[i] not in G.vars:
            i += 1
        if not w.startswith(form[:i]):
            return
        if i == len(form):
            if form == w:
                found.append(list(steps))
            return
        if sum(1 for c in form if c not in G.vars) > len(w):
            return
        if sum(1 for c in form if c in G.vars) > len(w) + 2:
            return
        A = form[i]
        for k, alt in enumerate(G.rules[A]):
            steps.append((form, i, A, k))
            go(form[:i] + alt + form[i + 1:], steps)
            steps.pop()
    go(G.start, [])
    return found


def apply_steps(G, steps):
    """replay steps and return the list of sentential forms (first = start variable), asserting leftmost-ness"""
    forms = [G.start]
    for form, i, A, k in steps:
        assert forms[-1] == form and form[i] == A
        assert all(c not in G.vars for c in form[:i])
        forms.append(form[:i] + G.rules[A][k] + form[i + 1:])
    return forms


def form_tex(G, form, hi=True):
    """a sentential form; the leftmost variable (the next to expand) in the brand colour"""
    if form == "":
        return r"\varepsilon"
    out, done = [], False
    for c in form:
        if c in G.vars and not done and hi:
            out.append(r"\textcolor{#2dd4bf}{" + c + "}")
            done = True
        else:
            out.append(c)
    return "".join(out)


def deriv_lines(pfx, G, steps, first_shown=True):
    forms = apply_steps(G, steps)
    lines = []
    for i, f in enumerate(forms):
        arrow = r"\Rightarrow " if i else ""
        cls = "cf-dl" + ("" if (i == 0 and first_shown) else " h")
        lines.append(f'<div id="{pfx}-l-{i}" class="{cls}">${arrow}{form_tex(G, f)}$</div>')
    return f'<div class="cf-deriv" dir="ltr">{"".join(lines)}</div>'


def deriv_inline(G, steps):
    """S ⇒ aSb ⇒ … as one TeX string (no colours)"""
    forms = apply_steps(G, steps)
    return r"\Rightarrow ".join(f if f else r"\varepsilon" for f in forms)


def tree_svg(pfx, G, steps, w=520, h=None, dy=78, scale=1.0, hide_root=False):
    """derivation tree that grows step by step. Node = a symbol occurrence. Step i adds the children of the node it
    expands: group {pfx}-t-<i> (1-based, step 1 = first rule applied); {pfx}-x-<i> rings that node."""
    nodes = [{"sym": G.start, "kids": [], "depth": 0}]
    frontier = [0]                      # node ids of the current sentential form, left to right
    for si, (form, i, A, k) in enumerate(steps):
        nid = frontier[i]
        assert nodes[nid]["sym"] == A
        alt = G.rules[A][k]
        kids = []
        for c in (alt if alt else "ε"):
            nodes.append({"sym": c, "kids": [], "depth": nodes[nid]["depth"] + 1, "step": si + 1})
            kids.append(len(nodes) - 1)
        nodes[nid]["kids"] = kids
        nodes[nid]["exp"] = si + 1
        frontier = frontier[:i] + (kids if alt else []) + frontier[i + 1:]   # one node per symbol of the form
    # leaf order
    leaves = []

    def dfs(n):
        if not nodes[n]["kids"]:
            leaves.append(n)
        for c in nodes[n]["kids"]:
            dfs(c)
    dfs(0)
    maxd = max(n["depth"] for n in nodes)
    h = h or (maxd * dy + 90)
    gap = (w - 60) / max(1, len(leaves) - 1) if len(leaves) > 1 else 0
    pos = {}
    for j, n in enumerate(leaves):
        pos[n] = (30 + j * gap if len(leaves) > 1 else w / 2, 40 + nodes[n]["depth"] * dy)

    def place(n):
        if n in pos:
            return pos[n]
        xs = [place(c)[0] for c in nodes[n]["kids"]]
        pos[n] = ((min(xs) + max(xs)) / 2, 40 + nodes[n]["depth"] * dy)
        return pos[n]
    place(0)
    groups = {}
    rings = []
    for n, node in enumerate(nodes):
        x, y = pos[n]
        sym = node["sym"]
        cls = "cf-tv" if sym in G.vars else ("cf-te" if sym == "ε" else "cf-tt")
        label = f'<text x="{x:.1f}" y="{y + 12:.1f}" class="{cls}">{_html.escape(sym)}</text>'
        if n == 0:
            groups.setdefault(0, []).append(label)
        else:
            par = next(m for m, nn in enumerate(nodes) if n in nn["kids"])
            px, py = pos[par]
            line = f'<line x1="{px:.1f}" y1="{py + 20:.1f}" x2="{x:.1f}" y2="{y - 24:.1f}" class="cf-tedge"/>'
            groups.setdefault(node["step"], []).append(line + label)
        if "exp" in node:
            rings.append(f'<circle id="{pfx}-x-{node["exp"]}" cx="{x:.1f}" cy="{y:.1f}" r="27" class="cf-tring h"/>')
    out = [f'<svg class="cf-tree" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" direction="ltr">']
    out += rings
    for gi in sorted(groups):
        body = "".join(groups[gi])
        if gi == 0:
            out.append(f'<g id="{pfx}-t-0"{" class=\"h\"" if hide_root else ""}>{body}</g>')
        else:
            out.append(f'<g id="{pfx}-t-{gi}" class="h">{body}</g>')
    out.append("</svg>")
    return "".join(out)


def grow(pfx_tree, pfx_lines, steps, i, gram=None, G=None):
    """actions for derivation step i (1-based): show the tree group + the line, ring the expanded node,
    highlight the rule alternative in the grammar card"""
    do = show(f"{pfx_tree}-t-{i}") if pfx_tree else []
    if pfx_lines:
        do += show(f"{pfx_lines}-l-{i}")
    if pfx_tree:
        do += show(f"{pfx_tree}-x-{i}") + (hide(f"{pfx_tree}-x-{i - 1}") if i > 1 else [])
    if gram:
        _, _, A, k = steps[i - 1]
        do += show(f"{gram}-a-{A}-{k}")
        if i > 1:
            _, _, A0, k0 = steps[i - 2]
            if (A0, k0) != (A, k):
                do += hide(f"{gram}-a-{A0}-{k0}")
    return do


def grow_end(pfx_tree, steps, gram=None):
    do = hide(f"{pfx_tree}-x-{len(steps)}") if pfx_tree else []
    if gram:
        _, _, A, k = steps[-1]
        do += hide(f"{gram}-a-{A}-{k}")
    return do


# ----------------------------------------------------------------------------- PDA
class _D:
    """the little interface stage.dfa_svg expects (unused here, kept for start/acc)"""
    def __init__(self, M):
        self.start, self.acc, self.alpha = M.start, M.acc, ()


def sym_txt(x):
    return "ε" if x == "" else x


def label_txt(e):
    _, a, pop, _, push = e
    return f"{sym_txt(a)},{sym_txt(pop)}→{sym_txt(push)}"


def label_tex(e):
    _, a, pop, _, push = e
    t = lambda x: r"\varepsilon" if x == "" else x
    return f"{t(a)},{t(pop)}\\to {t(push)}"


def label_say(e):
    """spoken edge: 'קוראים אֵיי, שולפים כלום, דוחפים אֵיי גדולה' in short form"""
    _, a, pop, _, push = e
    rd = f"קוראים {TERM.get(a) or _atom(a)}" if a else "בלי לקרוא"
    if pop and push:
        st_ = f"מחליפים {stack_say(pop)} ב{stack_say(push)}"
    elif pop:
        st_ = f"שולפים {stack_say(pop)}"
    elif push:
        st_ = f"דוחפים {stack_say(push)}"
    else:
        st_ = "בלי לגעת במחסנית"
    return f"{rd}, {st_}"


def stack_say(s):
    return " ".join(VARS.get(c) or TERM.get(c) or _atom(c) for c in s)


def pda_svg(pfx, M, pos, names, w=900, h=360, bend=None, loops=None, scale=1.0, start_side="left", lab_dx=None):
    """PDA diagram from the verified lib.PDA: labels of parallel edges are stacked lines, one per edge.
    {pfx}-hl-<k> = edge k's label in the highlight colour."""
    R = st.R
    bend = dict(bend or {})
    loops = dict(loops or {})
    lab_dx = dict(lab_dx or {})
    pairs = {}
    for k, e in enumerate(M.edges):
        pairs.setdefault((e[0], e[3]), []).append(k)
    out = [f'<svg class="dfa cf-pda" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" direction="ltr">',
           '<defs>',
           f'<marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c9cdf0"/></marker>',
           f'<marker id="{pfx}-ahh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker>',
           '</defs>']
    base, hi, labs = [], [], []
    LH = 34
    for (pp, r), ks in pairs.items():
        x1, y1 = pos[pp]
        if pp == r:
            up = loops.get(pp, "up") == "up"
            sgn = -1 if up else 1
            a1, a2 = (-120, -60) if up else (120, 60)
            sx, sy = x1 + R * math.cos(math.radians(a1)), y1 + R * math.sin(math.radians(a1))
            ex, ey = x1 + R * math.cos(math.radians(a2)), y1 + R * math.sin(math.radians(a2))
            cy = y1 + sgn * (R + 78)
            d = f"M{sx:.1f},{sy:.1f} C{x1 - 46:.1f},{cy:.1f} {x1 + 46:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
            lx = x1
            ys = [y1 + sgn * (R + 74) + (0 if up else 28) + sgn * LH * j for j in range(len(ks))]
        else:
            x2, y2 = pos[r]
            kb = bend.get((pp, r), 0.22 if (r, pp) in pairs else 0.0)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ux, uy = st._unit(x2 - x1, y2 - y1)
            nx, ny = uy, -ux
            dist = math.hypot(x2 - x1, y2 - y1)
            cx, cy = mx + nx * kb * dist, my + ny * kb * dist
            s1 = st._unit(cx - x1, cy - y1)
            s2 = st._unit(cx - x2, cy - y2)
            sx, sy = x1 + R * s1[0], y1 + R * s1[1]
            ex, ey = x2 + (R + 3) * s2[0], y2 + (R + 3) * s2[1]
            d = f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
            qx, qy = 0.25 * sx + 0.5 * cx + 0.25 * ex, 0.25 * sy + 0.5 * cy + 0.25 * ey
            side = 1 if kb >= 0 else -1
            lx = qx + nx * 22 * side
            above = (ny * side) < 0 or abs(ny) < 1e-9
            if above:      # stack upwards from the line
                y0 = qy + ny * 22 * side - 6
                ys = [y0 - LH * (len(ks) - 1 - j) for j in range(len(ks))]
            else:
                y0 = qy + ny * 22 * side + 26
                ys = [y0 + LH * j for j in range(len(ks))]
        lx += lab_dx.get((pp, r), 0)
        base.append(f'<path d="{d}" class="edge" marker-end="url(#{pfx}-ah)"/>')
        hi.append(f'<path id="{pfx}-he-{pp}-{r}" d="{d}" class="edge-hi h" marker-end="url(#{pfx}-ahh)"/>')
        for k, y in zip(ks, ys):
            t = _html.escape(label_txt(M.edges[k]))
            labs.append(f'<text x="{lx:.1f}" y="{y:.1f}" class="elabel cf-el">{t}</text>'
                        f'<text id="{pfx}-hl-{k}" x="{lx:.1f}" y="{y:.1f}" class="elabel cf-elh h">{t}</text>')
    sx0, sy0 = pos[M.start]
    if start_side == "left":
        base.append(f'<path d="M{sx0 - R - 70},{sy0} L{sx0 - R - 4},{sy0}" class="edge" marker-end="url(#{pfx}-ah)"/>')
    else:
        base.append(f'<path d="M{sx0},{sy0 - R - 70} L{sx0},{sy0 - R - 4}" class="edge" marker-end="url(#{pfx}-ah)"/>')
    nodes = []
    for q in sorted(pos, key=str):
        x, y = pos[q]
        ring = f'<circle cx="{x}" cy="{y}" r="{R - 7}" class="node-in"/>' if q in M.acc else ""
        nodes.append(f'<g id="{pfx}-s-{q}"><circle cx="{x}" cy="{y}" r="{R}" class="node"/>{ring}'
                     f'<text x="{x}" y="{y + 9}" class="nlabel">{st._sub_name(names[q])}</text></g>'
                     f'<circle id="{pfx}-hs-{q}" cx="{x}" cy="{y}" r="{R + 7}" class="node-hi h"/>')
    out += base + hi + nodes + labs + ["</svg>"]
    return "".join(out)


def pda_step(M, cfg, e):
    """apply edge e to configuration (q, i, stack, w); None if not applicable"""
    q, i, s, w = cfg
    p_, a, pop, r, push = e
    if p_ != q:
        return None
    if a:
        if i >= len(w) or w[i] != a:
            return None
        i += 1
    if pop:
        if not s or s[-1] != pop:
            return None
        s = s[:-1]
    return (r, i, s + push, w)


def pda_path(M, w, require_empty=True, max_stack=None):
    """shortest accepting run (list of edge indices) under the course convention, or None (BFS)"""
    from collections import deque
    max_stack = max_stack if max_stack is not None else 2 * len(w) + 6
    start = (M.start, 0, "", w)
    par = {start: None}
    dq = deque([start])
    while dq:
        c = dq.popleft()
        q, i, s, _ = c
        if i == len(w) and q in M.acc and (s == "" or not require_empty):
            path = []
            while par[c] is not None:
                c, k = par[c]
                path.append(k)
            return path[::-1]
        for k, e in enumerate(M.edges):
            n = pda_step(M, c, e)
            if n is not None and len(n[2]) <= max_stack and n not in par:
                par[n] = (c, k)
                dq.append(n)
    return None


def replay(M, w, path):
    """configurations along a given path; asserts every edge applies"""
    cfgs = [(M.start, 0, "", w)]
    for k in path:
        n = pda_step(M, cfgs[-1], M.edges[k])
        assert n is not None, (w, path, k, cfgs[-1])
        cfgs.append(n)
    return cfgs


def stack(pfx, snaps, cap="מחסנית", slot=58):
    """stack column for the given snapshots (strings, bottom first). Cells (depth, symbol) that ever occur."""
    cells = sorted({(d, c) for s in snaps for d, c in enumerate(s)})
    depth = max([len(s) for s in snaps] + [3])
    hh = depth * slot + 14
    o = [f'<div class="cf-stack" id="{pfx}"><div class="cf-stcap">{cap}</div>'
         f'<div class="cf-stcol" style="height:{hh}px" dir="ltr">']
    for d, c in cells:
        o.append(f'<div id="{pfx}-c-{d}-{c}" class="cf-cell h" style="bottom:{6 + d * slot}px;height:{slot - 8}px">{_html.escape(c)}</div>')
    o.append(f'<div id="{pfx}-e" class="cf-stempty">ריקה</div></div></div>')
    return "".join(o)


def stack_do(pfx, before, after):
    b = {(d, c) for d, c in enumerate(before)}
    a = {(d, c) for d, c in enumerate(after)}
    do = hide(*[f"{pfx}-c-{d}-{c}" for d, c in sorted(b - a)]) + show(*[f"{pfx}-c-{d}-{c}" for d, c in sorted(a - b)])
    if before == "" and after != "":
        do += hide(f"{pfx}-e")
    if after == "" and before != "":
        do += show(f"{pfx}-e")
    return do


def run_pda(pfx, M, w, path, names, tp, stk, lead=None, fast=False, clear=(), end=True, verdict_id=None):
    """phrases that replay `path` on the diagram {pfx}, the tape {tp} and the stack column {stk}.
    Returns (phrases, cfgs, left_on_ids)."""
    cfgs = replay(M, w, path)
    st0 = names[M.start]
    ph = [p(lead or f"מתחילים ב-${st0}$, והמחסנית ריקה.",
            do=hide(*clear) + show(f"{pfx}-hs-{M.start}"))]
    prev_e, prev_k = None, None
    for j, k in enumerate(path):
        e = M.edges[k]
        c0, c1 = cfgs[j], cfgs[j + 1]
        do = []
        if prev_e is not None:
            do += hide(f"{pfx}-he-{prev_e[0]}-{prev_e[3]}", f"{pfx}-hl-{prev_k}")
        do += hide(f"{pfx}-hs-{c0[0]}") + show(f"{pfx}-he-{e[0]}-{e[3]}", f"{pfx}-hl-{k}", f"{pfx}-hs-{c1[0]}")
        if e[1]:
            i = c0[1]
            if i:
                do += hide(f"{tp}-k-{i - 1}") + show(f"{tp}-d-{i - 1}")
            do += show(f"{tp}-k-{i}")
        do += stack_do(stk, c0[2], c1[2])
        lt = label_tex(e)
        if fast:
            sub = f"${lt}$"
            say = label_say(e) + "."
        else:
            to = names[e[3]]
            move = "" if e[0] == e[3] else f", ועוברים ל-${to}$"
            sub = f"${lt}$: " + _verb_sub(e) + move + "."
            say = label_say(e) + (f", ועוברים ל{lexicon.state_say(to)}" if e[0] != e[3] else "") + "."
        ph.append(P(sub, say=say, do=do))
        prev_e, prev_k = e, k
    left = [f"{pfx}-hs-{cfgs[-1][0]}"]
    if path:
        left += [f"{pfx}-he-{prev_e[0]}-{prev_e[3]}", f"{pfx}-hl-{prev_k}"]
    last = max((j for j, k in enumerate(path) if M.edges[k][1]), default=None)
    if last is not None:
        left += [f"{tp}-k-{cfgs[last][1]}"]
    return ph, cfgs, left


def edge_strip(labp, M, path):
    """one div per step showing the edge used (for runs on an exam raster, where the figure is never redrawn)"""
    divs = "".join(f'<div id="{labp}-{j}" class="h"><div class="cf-eq cf-ltr">${label_tex(M.edges[k])}$</div></div>'
                   for j, k in enumerate(path))
    return f'<div class="swap cf-c" style="--swap-h:90px">{divs}</div>'


def run_pda_raster(rid, M, w, path, tp, stk, labp, ring, lead, lead_say=None, clear=()):
    """phrases that replay `path` on an exam raster: ring = {state: ring name} ({rid}-ring-<name>), the edge used in
    the strip {labp}-<j>, the tape {tp}, the stack {stk}. Returns (phrases, cfgs, left_on_ids)."""
    cfgs = replay(M, w, path)
    ph = [P(lead, say=lead_say if lead_say is not None else say_of(lead),
            do=hide(*clear) + show(f"{rid}-ring-{ring[M.start]}"))]
    for j, k in enumerate(path):
        e = M.edges[k]
        c0, c1 = cfgs[j], cfgs[j + 1]
        do = hide(f"{labp}-{j - 1}") if j else []
        if c0[0] != c1[0]:
            do += hide(f"{rid}-ring-{ring[c0[0]]}") + show(f"{rid}-ring-{ring[c1[0]]}")
        do += show(f"{labp}-{j}")
        if e[1]:
            i = c0[1]
            if i:
                do += hide(f"{tp}-k-{i - 1}") + show(f"{tp}-d-{i - 1}")
            do += show(f"{tp}-k-{i}")
        do += stack_do(stk, c0[2], c1[2])
        say = label_say(e) + "."
        if e[0] != e[3]:
            say = label_say(e) + ", ועוברים למצב המקבל." if e[3] in M.acc else label_say(e) + ", ועוברים מצב."
        ph.append(P(f"${label_tex(e)}$: " + _verb_sub(e) + ".", say=say, do=do))
    left = [f"{rid}-ring-{ring[cfgs[-1][0]]}", f"{labp}-{len(path) - 1}"] if path else []
    last = max((j for j, k in enumerate(path) if M.edges[k][1]), default=None)
    if last is not None:
        left += [f"{tp}-k-{cfgs[last][1]}"]
    return ph, cfgs, left


def _verb_sub(e):
    _, a, pop, _, push = e
    rd = f"קוראים ${a}$" if a else "בלי לקרוא"
    if pop and push:
        return f"{rd}, מחליפים ${pop}$ ב-${push}$"
    if pop:
        return f"{rd}, שולפים ${pop}$"
    if push:
        return f"{rd}, דוחפים ${push}$"
    return f"{rd}, המחסנית לא משתנה"


def checks(pfx, acc_ok, empty_ok):
    """the two acceptance checks of the course convention, as chips: {pfx}-c1, {pfx}-c2, verdict {pfx}-v"""
    c1 = ("✓" if acc_ok else "✗")
    c2 = ("✓" if empty_ok else "✗")
    ok = acc_ok and empty_ok
    return (f'<div class="cf-checks" dir="rtl">'
            f'<span id="{pfx}-c1" class="cf-chip {"ok" if acc_ok else "bad"} h">מצב מקבל {c1}</span>'
            f'<span id="{pfx}-c2" class="cf-chip {"ok" if empty_ok else "bad"} h">מחסנית ריקה {c2}</span>'
            f'<span id="{pfx}-v" class="verdict {"ok" if ok else "bad"} h">{"מתקבלת ✓" if ok else "לא מתקבלת ✗"}</span></div>')


# ----------------------------------------------------------------------------- CSS (goes into the title scene's stage)
CSS = """<style>
.cf-gram{display:flex;flex-direction:column;gap:6px;font-size:40px;background:var(--card2);border:1px solid var(--line);
  border-radius:16px;padding:14px 28px;direction:ltr;width:fit-content}
.cf-gram.big{font-size:46px}
.cf-grow{position:relative;display:flex;align-items:center;gap:4px;white-space:nowrap}
.cf-lhs{margin-right:8px}
.cf-bar{color:var(--muted);margin:0 6px}
.cf-alt{position:relative;padding:0 6px}
.cf-ahi{position:absolute;inset:-4px -2px;border-radius:10px;background:rgba(45,212,191,.25);box-shadow:0 0 0 3px var(--brand) inset}
.cf-rhi{position:absolute;inset:-4px -14px;border-radius:12px;background:rgba(56,189,248,.14);box-shadow:0 0 0 3px var(--brand2) inset}
.cf-deriv{display:flex;flex-direction:column;gap:4px;font-size:46px;align-items:flex-start;direction:ltr}
.cf-dl{white-space:nowrap}
svg.cf-tree{overflow:visible}
svg.cf-tree text{font-family:"Cambria Math",serif;font-size:36px;text-anchor:middle}
svg.cf-tree .cf-tv{fill:var(--brand);font-style:italic}
svg.cf-tree .cf-tt{fill:var(--ink);font-style:italic}
svg.cf-tree .cf-te{fill:var(--muted)}
svg.cf-tree .cf-tedge{stroke:#c9cdf0;stroke-width:2.4}
svg.cf-tree .cf-tring{fill:rgba(45,212,191,.18);stroke:var(--brand);stroke-width:4}
svg.cf-pda .cf-el{font-size:31px}
svg.cf-pda .cf-elh{font-size:31px;fill:var(--brand);font-weight:700;paint-order:stroke;stroke:#0a0c18;stroke-width:6px}
.cf-stack{display:flex;flex-direction:column;align-items:center;gap:8px}
.cf-stcap{font-size:26px;color:var(--muted);direction:rtl}
.cf-stcol{position:relative;width:118px;border:4px solid #c9cdf0;border-top:none;border-radius:0 0 14px 14px}
.cf-cell{position:absolute;left:8px;right:8px;border-radius:9px;background:rgba(45,212,191,.22);border:2px solid var(--brand);
  display:flex;align-items:center;justify-content:center;font-family:"Cambria Math",serif;font-style:italic;font-size:36px;color:#fff}
.cf-stempty{position:absolute;left:0;right:0;bottom:10px;text-align:center;font-size:26px;color:var(--muted);direction:rtl}
.cf-row{display:flex;align-items:flex-end;justify-content:center;gap:60px;width:100%}
.cf-col{display:flex;flex-direction:column;align-items:center;gap:16px}
.cf-checks{display:flex;gap:16px;align-items:center;flex-wrap:wrap;justify-content:center}
.cf-chip{font-size:30px;padding:6px 18px;border-radius:999px;border:2px solid var(--line)}
.cf-chip.ok{color:var(--ok);border-color:rgba(52,211,153,.5)}
.cf-chip.bad{color:var(--bad);border-color:rgba(251,113,133,.5)}
.cf-big{font-size:44px;direction:ltr}
.cf-mid{font-size:38px;direction:rtl}
.cf-words{display:flex;gap:18px;flex-wrap:wrap;justify-content:center;font-size:40px;direction:ltr;max-width:1000px}
.cf-words>span{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:4px 18px}
.cf-two{display:flex;gap:40px;justify-content:center;align-items:flex-start;width:100%}
.cf-two>div{display:flex;flex-direction:column;align-items:center;gap:8px}
.cf-cap{font-size:28px;color:var(--muted);direction:rtl}
.cf-eq{font-size:40px;direction:rtl;background:var(--card2);border:1px solid var(--line);border-radius:14px;padding:10px 26px}
.panel .cf-gram{font-size:36px}
.swap.cf-c>div{justify-content:center}
.cf-ltr{direction:ltr!important}
.stage>*{flex-shrink:0}
.cf-sm .opt{font-size:28px;padding:8px 18px}
.cf-sm .onote{font-size:24px}
.cf-sm{display:flex;flex-direction:column;gap:12px;width:100%}
</style>"""
