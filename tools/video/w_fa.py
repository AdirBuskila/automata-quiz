# -*- coding: utf-8 -*-
"""Stage widgets + phrase helpers for the `fa` course videos (F02-F08). Shared widgets live in stage.py.

Everything that shows a run, a subset or a membership verdict is computed here from the simulators
(tools/verify/needhelp/lib.py), never typed. CSS for these widgets is FA_CSS: put it inside the stage HTML of a
scene that uses them (class names are prefixed `fa-`).
"""
import lexicon
import stage as st
from vid import P, show, hide

FA_CSS = """<style>
.fa-strace{font-size:36px;min-height:56px;direction:ltr;display:flex;flex-wrap:wrap;gap:8px 12px;justify-content:center;max-width:1040px}
.fa-sub{font-size:31px}
.fa-sub th,.fa-sub td{padding:7px 22px}
.fa-sub .fa-acc{color:var(--brand);font-size:26px;margin-inline-end:4px}
.fa-grid{border-collapse:separate;border-spacing:0;font-size:32px;background:var(--card2);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.fa-grid th,.fa-grid td{position:relative;padding:6px 26px;text-align:center;border-bottom:1px solid var(--line)}
.fa-grid thead th{color:var(--muted);font-weight:600}
.fa-grid tbody tr:last-child>*{border-bottom:none}
.fa-yes{color:var(--ok);font-weight:700}
.fa-no{color:var(--bad);font-weight:700}
.fa-rx{display:flex;align-items:flex-end;justify-content:center;gap:2px;font-size:58px;direction:ltr;padding:10px 0 46px}
.fa-rxp{position:relative;padding:4px 6px}
.fa-rxhi{position:absolute;inset:-4px -2px;border-radius:12px;background:rgba(45,212,191,.20);box-shadow:0 0 0 4px var(--brand) inset}
.fa-rxhi.alt{background:rgba(251,191,36,.16);box-shadow:0 0 0 4px var(--warn) inset}
.fa-cap{position:absolute;left:50%;top:100%;transform:translate(-50%,6px);white-space:nowrap;font-size:26px;color:var(--brand);direction:rtl}
.fa-pair svg.dfa .nlabel{font-size:25px;font-style:normal}
.fa-small svg.dfa .nlabel{font-size:30px}
.fa-row{display:flex;gap:40px;align-items:center;justify-content:center}
.fa-lab{font-size:30px;color:var(--muted);direction:rtl}
.fa-big{font-size:44px;direction:ltr}
.fa-mini{border-collapse:separate;border-spacing:0;font-size:32px;background:var(--card2);border:1px solid var(--line);border-radius:14px;overflow:hidden;direction:rtl}
.fa-mini th,.fa-mini td{position:relative;padding:8px 26px;text-align:center;border-bottom:1px solid var(--line)}
.fa-mini thead th{color:var(--muted)}
.fa-mini tbody tr:last-child>*{border-bottom:none}
</style>"""


# ----------------------------------------------------------------------------- sets of states
def _key(q):
    return (len(str(q)), str(q))


def set_tex(S, names):
    if not S:
        return r"\emptyset"
    return r"\{" + ",".join(names[q] for q in sorted(S, key=_key)) + r"\}"


def set_say(S, names):
    if not S:
        return "הקבוצה הריקה"
    parts = [lexicon.state_say(names[q]) for q in sorted(S, key=_key)]
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " ו" + parts[-1]


def nfa_sets(N, word):
    """the set of states the NFA can be in before/after every letter (ε-closures included)"""
    S = [frozenset(N.eclose({N.start}))]
    for c in word:
        S.append(frozenset(N.step(S[-1], c)))
    return S


def set_trace(pfx, sets, word, names):
    """{q0} -a-> {q0,q1} ... revealed step by step: {pfx}-r-<i>"""
    parts = [f'<span id="{pfx}-r-0" class="h">${set_tex(sets[0], names)}$</span>']
    for i, c in enumerate(word):
        parts.append(f'<span id="{pfx}-r-{i + 1}" class="h">$\\xrightarrow{{{c}}}{set_tex(sets[i + 1], names)}$</span>')
    return f'<div class="fa-strace">{"".join(parts)}</div>'


def run_nfa(pfx, N, word, names, tp, lead, lead_say=None, clear=()):
    """phrases running NFA N on `word` with the whole set of current states lit on diagram `pfx`
    (stage.dfa_svg) and the tape/set-trace/verdict ids `tp` (stage.tape + set_trace + stage.verdict).
    Returns (phrases, sets, end_ids)."""
    S = nfa_sets(N, word)
    hs = lambda X: [f"{pfx}-hs-{q}" for q in X]
    ph = [P(lead, say=lead_say, do=hide(*clear) + show(*hs(S[0]), f"{tp}-r-0"))]
    for i, c in enumerate(word):
        do = hide(*hs(S[i]))
        if i:
            do += hide(f"{tp}-k-{i - 1}") + show(f"{tp}-d-{i - 1}")
        do += show(f"{tp}-k-{i}", *hs(S[i + 1]), f"{tp}-r-{i + 1}")
        if S[i + 1]:
            sub = f"קוראים ${c}$: ${set_tex(S[i + 1], names)}$."
            say = f"קוראים {lexicon.word_say(c)}: {set_say(S[i + 1], names)}."
        else:
            sub = f"קוראים ${c}$: אין לאן ללכת. הקבוצה ריקה, כל הריצות נתקעו."
            say = f"קוראים {lexicon.word_say(c)}: אין לאן ללכת. הקבוצה ריקה, כל הריצות נתקעו."
        ph.append(P(sub, say=say, do=do))
    end = S[-1]
    hit = sorted(end & N.acc, key=_key)
    tail = (hide(f"{tp}-k-{len(word) - 1}") + show(f"{tp}-d-{len(word) - 1}") if word else []) + show(f"{tp}-v")
    if hit:
        sub = f"בקבוצה האחרונה יש מצב מקבל, ${names[hit[0]]}$: יש ריצה מקבלת, והמילה מתקבלת."
    elif end:
        sub = "בקבוצה האחרונה אין אף מצב מקבל: כל הריצות נכשלו, והמילה נדחית."
    else:
        sub = "הקבוצה ריקה: אין אף ריצה שקוראת את כל המילה, והמילה נדחית."
    ph.append(P(sub, do=tail, hold=0.5))
    return ph, S, hs(end)


def run_box(tp, word, sets, names, ok, hidden=True):
    """tape + set trace + verdict, in one box with id {tp}-box"""
    return (f'<div id="{tp}-box"{" class=\"h\"" if hidden else ""}>{st.tape(tp, word)}'
            f'{set_trace(tp, sets, word, names)}{st.verdict(tp, ok)}</div>')


# ----------------------------------------------------------------------------- DFA run with any state names
def dfa_trace(D, word):
    s = [D.start]
    for c in word:
        s.append(D.delta[(s[-1], c)])
    return s


def run_named(pfx, D, word, tex, say, tp, lead, lead_say=None, clear=()):
    """like vid.run_dfa (fast form) for states whose names are not q_i: tex/say map state -> TeX / spoken form"""
    s = dfa_trace(D, word)
    ph = [P(lead, say=lead_say, do=hide(*clear) + show(f"{pfx}-hs-{D.start}", f"{tp}-r-0"))]
    for i, c in enumerate(word):
        p, r = s[i], s[i + 1]
        do = hide(f"{pfx}-hs-{p}")
        if i:
            do += hide(f"{tp}-k-{i - 1}", f"{pfx}-he-{s[i - 1]}-{p}") + show(f"{tp}-d-{i - 1}")
        do += show(f"{tp}-k-{i}", f"{pfx}-he-{p}-{r}", f"{pfx}-hs-{r}", f"{tp}-r-{i + 1}")
        ph.append(P(f"${c}$: ${tex[r]}$", say=f"{lexicon.word_say(c)}: ל{say[r]}.", do=do))
    left = [f"{pfx}-hs-{s[-1]}"] + ([f"{pfx}-he-{s[-2]}-{s[-1]}"] if word else [])
    return ph, s, left


def named_trace(pfx, states, tex):
    parts = []
    for i, q in enumerate(states):
        arrow = "$\\to$ " if i else ""
        parts.append(f'<span id="{pfx}-r-{i}" class="h">{arrow}${tex[q]}$</span>')
    return f'<div class="trace" dir="ltr">{" ".join(parts)}</div>'


# ----------------------------------------------------------------------------- subset construction table
def subset_table(pfx, rows, alpha, head=r"\delta_D"):
    """rows: [(key, S_tex, {letter: T_tex}, accepting, start)] in build order. Ids: {pfx}-r-<k> the row (starts
    hidden), {pfx}-c-<k>-<a> a target cell's content (hidden), {pfx}-hc-<k>-<a> cell highlight,
    {pfx}-row-<k> row-header highlight, {pfx}-acc-<k> the accepting star (hidden)."""
    th = "".join(f"<th>${a}$</th>" for a in alpha)
    out = []
    for k, S, moves, acc, start in rows:
        cells = "".join(f'<td><i id="{pfx}-hc-{k}-{a}" class="cell-hi h"></i>'
                        f'<span id="{pfx}-c-{k}-{a}" class="h">${moves[a]}$</span></td>' for a in alpha)
        star = f'<span id="{pfx}-acc-{k}" class="fa-acc h">*</span>' if acc else ""
        mark = '<span class="mark">→</span>' if start else ""
        out.append(f'<tr id="{pfx}-r-{k}" class="h"><th><i id="{pfx}-row-{k}" class="cell-hi h"></i>{mark}{star}'
                   f'${S}$</th>{cells}</tr>')
    return (f'<table class="delta fa-sub" id="{pfx}-tab" dir="ltr"><thead><tr><th>${head}$</th>{th}</tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table>')


# ----------------------------------------------------------------------------- membership grid (word x regex)
def member_grid(pfx, words_tex, cols_tex, truth, head="מילה"):
    """rows = words, cols = expressions/languages. truth[i][j] -> ✓/✗ (computed by the caller).
    Ids: {pfx}-w-<i> row (hidden), {pfx}-c-<i>-<j> verdict (hidden), {pfx}-hl-<i> row highlight."""
    th = "".join(f"<th>${c}$</th>" for c in cols_tex)
    out = []
    for i, w in enumerate(words_tex):
        cells = "".join(
            f'<td><span id="{pfx}-c-{i}-{j}" class="h {"fa-yes" if truth[i][j] else "fa-no"}">'
            f'{"✓" if truth[i][j] else "✗"}</span></td>' for j in range(len(cols_tex)))
        out.append(f'<tr id="{pfx}-w-{i}" class="h"><th><i id="{pfx}-hl-{i}" class="cell-hi h"></i>${w}$</th>{cells}</tr>')
    return (f'<table class="fa-grid" id="{pfx}-grid" dir="ltr"><thead><tr><th>{head}</th>{th}</tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table>')


# ----------------------------------------------------------------------------- a regex with highlightable parts
def rx_parts(pfx, parts, size=None):
    """parts: [(key or None, tex, caption or None)]. Ids: {pfx}-hp-<key> highlight, {pfx}-ha-<key> warn highlight,
    {pfx}-cap-<key> caption under the part (all hidden)."""
    out = []
    for key, tex, cap in parts:
        if key is None:
            out.append(f'<span class="fa-rxp">${tex}$</span>')
            continue
        c = f'<span id="{pfx}-cap-{key}" class="fa-cap h">{cap}</span>' if cap else ""
        out.append(f'<span class="fa-rxp"><i id="{pfx}-hp-{key}" class="fa-rxhi h"></i>'
                   f'<i id="{pfx}-ha-{key}" class="fa-rxhi alt h"></i>${tex}${c}</span>')
    style = f' style="font-size:{size}px"' if size else ""
    return f'<div class="fa-rx" id="{pfx}"{style}>{"".join(out)}</div>'


def shown(card_html):
    """a stage.card that starts visible (inside a swap slot that is itself hidden)"""
    return card_html.replace(' h"', '"', 1)
