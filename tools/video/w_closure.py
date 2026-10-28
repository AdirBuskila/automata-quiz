# -*- coding: utf-8 -*-
"""Widgets for the closure / CFL-pumping videos (K06, K06a, K06b, K07, K08).

Everything here is HTML with $TeX$ (rendered later by the bank pipeline). Class names are prefixed `clo-`;
the CSS travels inside the stage HTML (`STYLE`, include it once per scene that uses these widgets).

  closure_table(pfx, rows)   the closure table, ✓/✗ cells revealed one by one
  blocks(pfx, word, …)       a word drawn as coloured letter blocks, with sliding windows and pumped letters
  sigma_box(pfx, …)          Σ* split into L and its complement: union = everything, intersection = nothing
  steps(pfx, items)          a vertical chain of proof steps, revealed one by one
  qcard(Q, pfx, notes)       an exam question (id + stem + options) sized for the side panel
  KP(sub, say=None, …)       P() whose spoken form is derived from the closure vocabulary below
"""
import re
import lexicon
import stage as st
from vid import P

STYLE = """<style>
/* Chrome does not stretch the overline glyph of \\overline (a tiny accent): hide it, draw a rule over the base */
mover:has(>mo[stretchy="true"]:last-child)>mo:last-child{color:transparent}
mover:has(>mo[stretchy="true"]:last-child)>:first-child{border-top:.065em solid currentColor;padding-top:.06em}
.clo-tab{border-collapse:separate;border-spacing:0;font-size:40px;background:var(--card2);border:1px solid var(--line);
  border-radius:14px;overflow:hidden;direction:rtl}
.clo-tab th,.clo-tab td{position:relative;padding:7px 26px;text-align:center;border-bottom:1px solid var(--line)}
.clo-tab thead th{color:var(--muted);font-weight:600}
.clo-tab tbody tr:last-child>*{border-bottom:none}
.clo-tab td.op{text-align:right;min-width:330px}
.clo-tab td.mk{width:150px;font-size:36px;font-weight:700}
.clo-tab .yes{color:var(--ok)} .clo-tab .no{color:var(--bad)}
.clo-hl{position:absolute;inset:2px;border-radius:9px;background:rgba(45,212,191,.16);box-shadow:0 0 0 3px var(--brand) inset}
.clo-row td,.clo-row th{background:transparent}
.clo-w{position:relative;display:flex;gap:0;direction:ltr}
.clo-c{position:relative;width:var(--cw);height:var(--ch);display:flex;align-items:center;justify-content:center;
  font-family:"Cambria Math",serif;font-size:calc(var(--cw) * .62);border:2px solid rgba(255,255,255,.18);margin-right:-2px;color:var(--ink)}
.clo-c b{position:relative;font-weight:400}
.clo-A{background:rgba(56,189,248,.20)} .clo-B{background:rgba(251,191,36,.18)} .clo-C{background:rgba(52,211,153,.18)}
.clo-D{background:rgba(251,113,133,.18)} .clo-H{background:rgba(160,160,200,.18)}
.clo-pm{position:absolute;inset:0;background:rgba(45,212,191,.55);box-shadow:0 0 14px rgba(45,212,191,.8) inset}
.clo-win{position:absolute;top:-12px;height:calc(var(--ch) + 20px);border:5px solid var(--brand);border-radius:12px;
  box-shadow:0 0 22px rgba(45,212,191,.6);box-sizing:border-box}
.clo-win.bad{border-color:var(--bad);box-shadow:0 0 22px rgba(251,113,133,.6)}
.clo-lbls{position:relative;height:50px;direction:ltr;font-size:30px;color:var(--muted)}
.clo-lbls span{position:absolute;top:6px;transform:translateX(-50%);white-space:nowrap}
.clo-sig{position:relative;width:860px;height:300px;border:3px solid #c9cdf0;border-radius:18px;overflow:hidden;display:flex;direction:ltr}
.clo-sig>div{flex:1;display:flex;align-items:center;justify-content:center;font-size:44px}
.clo-sig .l{background:rgba(56,189,248,.18)} .clo-sig .c{background:rgba(251,191,36,.14)}
.clo-sig .wave{position:absolute;left:50%;top:0;bottom:0;border-left:4px dashed #c9cdf0}
.clo-sig .ov{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:46px;
  background:rgba(45,212,191,.30);box-shadow:0 0 0 6px var(--brand) inset}
.clo-sig .ov.i{background:transparent;box-shadow:none}
.clo-sig .ov.i span{background:rgba(5,6,14,.86);border:3px solid var(--warn);border-radius:14px;padding:8px 24px}
.clo-sig .ov.u span{background:rgba(5,6,14,.86);border:3px solid var(--brand);border-radius:14px;padding:8px 24px}
.clo-steps{display:flex;flex-direction:column;gap:14px;width:980px;direction:rtl}
.clo-st{font-size:33px;line-height:1.45;background:var(--card2);border:1px solid var(--line);border-radius:14px;padding:12px 22px}
.clo-st.bad{border-inline-start:7px solid var(--bad)} .clo-st.ok{border-inline-start:7px solid var(--ok)}
.clo-st.key{border-inline-start:7px solid var(--brand)}
.clo-q .qstem{font-size:28px;line-height:1.45}
.clo-q .opt{font-size:28px;padding:8px 18px;line-height:1.35}
.clo-q .onote{font-size:24px;white-space:nowrap}
.clo-q .ook{left:-46px;font-size:40px}
.clo-q.sm .qstem{font-size:23px;line-height:1.38}
.clo-q.sm .opt{font-size:24px;padding:6px 16px}
.clo-q.sm .opts{gap:8px}
.clo-big{font-size:44px;line-height:1.6;direction:ltr;text-align:center}
.clo-heb{font-size:34px;line-height:1.5;direction:rtl;text-align:center;color:var(--muted)}
</style>"""


# ----------------------------------------------------------------------------- closure table
def closure_table(pfx, rows, head=("פעולה", "רגולריות", "חסרות הקשר")):
    """rows: [(op_html, reg_closed, cfl_closed)]. Ids: {pfx}-m-<i>-r / {pfx}-m-<i>-c (✓/✗ marks, hidden),
    {pfx}-hl-<i> (row highlight, hidden)."""
    body = []
    for i, (op, r, c) in enumerate(rows):
        def mk(ok, col):
            return (f'<td class="mk"><span id="{pfx}-m-{i}-{col}" class="{"yes" if ok else "no"} h">'
                    f'{"✓" if ok else "✗"}</span></td>')
        body.append(f'<tr class="clo-row"><td class="op"><i id="{pfx}-hl-{i}" class="clo-hl h"></i>'
                    f'<span style="position:relative">{op}</span></td>{mk(r, "r")}{mk(c, "c")}</tr>')
    return (f'<table class="clo-tab" id="{pfx}"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head)
            + f'</tr></thead><tbody>{"".join(body)}</tbody></table>')


# ----------------------------------------------------------------------------- letter blocks + windows
BLOCK_CLASS = "ABCDH"


def blocks(pfx, word, cw=56, ch=70, windows=(), labels=(), colors=None):
    """word drawn letter by letter, each maximal run of one letter in its own colour.
    windows: [(name, start, length[, 'bad'])] -> {pfx}-w-<name> rectangles (hidden);
    every cell has {pfx}-p-<i> (pumped highlight, hidden); labels: [(html, center_index_float)] under the word."""
    colors = dict(colors or {})
    nxt = iter(BLOCK_CLASS)
    for c in word:
        if c not in colors:
            colors[c] = next(nxt)
    cells = "".join(f'<span class="clo-c clo-{colors[c]}"><i id="{pfx}-p-{i}" class="clo-pm h"></i><b>{c}</b></span>'
                    for i, c in enumerate(word))
    step = cw - 2
    wins = "".join(f'<i id="{pfx}-w-{w[0]}" class="clo-win {w[3] if len(w) > 3 else ""} h" '
                   f'style="left:{w[1] * step - 6}px;width:{w[2] * step + 14}px"></i>' for w in windows)
    lab = "".join(f'<span style="left:{(x + .5) * step}px">{h}</span>' for h, x in labels)
    width = len(word) * step + 2
    return (f'<div style="--cw:{cw}px;--ch:{ch}px;width:{width}px">'
            f'<div class="clo-w" id="{pfx}">{cells}{wins}</div>'
            + (f'<div class="clo-lbls" style="width:{width}px">{lab}</div>' if labels else "") + "</div>")


def block_labels(word, fmt):
    """labels under each maximal block: fmt(letter, length) -> html, centred on the block"""
    out, i = [], 0
    while i < len(word):
        j = i
        while j < len(word) and word[j] == word[i]:
            j += 1
        out.append((fmt(word[i], j - i), (i + j - 1) / 2))
        i = j
    return out


# ----------------------------------------------------------------------------- Σ* = L ∪ L̄
def sigma_box(pfx, left=r"$L$", right=r"$\overline{L}$",
              union=r"$L\cup\overline{L}=\Sigma^*$", inter=r"$L\cap\overline{L}=\emptyset$"):
    """ids: {pfx}-u (union overlay), {pfx}-i (intersection label)"""
    return (f'<div class="clo-sig" id="{pfx}"><div class="l">{left}</div><div class="c">{right}</div><i class="wave"></i>'
            f'<div id="{pfx}-u" class="ov u h"><span>{union}</span></div>'
            f'<div id="{pfx}-i" class="ov i h"><span>{inter}</span></div></div>')


# ----------------------------------------------------------------------------- proof steps
def steps(pfx, items, width=980):
    """items: [(html, kind)] kind in '', 'ok', 'bad', 'key'. Ids {pfx}-<i>, hidden."""
    return (f'<div class="clo-steps" style="width:{width}px">'
            + "".join(f'<div id="{pfx}-{i}" class="clo-st {k} h">{h}</div>' for i, (h, k) in enumerate(items))
            + "</div>")


# ----------------------------------------------------------------------------- exam question in the panel
def qcard(Q, pfx, notes=None, stem=None, small=False):
    """the bank question as the app shows it (id + stem + options), smaller type for long stems"""
    opts = [(o["id"], o["html"]) for o in Q["options"]]
    # lockOrder questions (an option cites siblings by letter, "א + ב") keep their letters in the app too
    letters = "אבגדהו" if Q.get("lockOrder") else "••••••"
    return (f'<div class="clo-q{" sm" if small else ""}"><div class="qstem"><span class="qid">{Q["id"]}</span>{stem or Q["questionHtml"]}</div>'
            + st.options(pfx, opts, notes=notes, letters=letters) + "</div>")


# ----------------------------------------------------------------------------- narration vocabulary
L_ = "אֵל"
TEXSAY = {
    "L": L_, "L'": L_ + " גג", "L_1": L_ + " אחת", "L_2": L_ + " שתיים", "L_3": L_ + " שלוש",
    "R": "אָר", "F": "אֶף", "X": "אִקְס", "w": "דאבל יו", "u": "יו", "n": "אֵן", "k": "קיי", r"\ell": L_,
    r"\overline{L}": "המשלים של " + L_, r"\overline{L_2}": "המשלים של " + L_ + " שתיים",
    r"\Sigma^*": "סיגמא כוכבית", r"\emptyset": "הקבוצה הריקה",
    r"\{a^nb^n\}": "אֵיי בחזקת אֵן, בִּי בחזקת אֵן", "a^nb^n": "אֵיי בחזקת אֵן, בִּי בחזקת אֵן",
    r"\{0^n1^n\}": "אפס בחזקת אֵן, אחת בחזקת אֵן", "0^n1^n": "אפס בחזקת אֵן, אחת בחזקת אֵן",
    "a^nb^nc^n": "אֵיי בִּי סִי בחזקת אֵן", r"\{a^nb^nc^n\}": "אֵיי בִּי סִי בחזקת אֵן",
    "uu": "יו יו", r"\overline{uu}": "המשלים של יו יו", r"\{uu\}": "יו יו",
    "a^*": "אֵיי כוכבית", "b^*": "בִּי כוכבית", "a^*b^*": "אֵיי כוכבית בִּי כוכבית",
    r"\cap": "חיתוך", r"\cup": "איחוד",
    "I": "אחת", "II": "שתיים", "p": "פי",
}


def tsay(tex):
    t = tex.strip()
    if t in TEXSAY:
        return TEXSAY[t]
    s = lexicon.tex_say(t)
    if s is None:
        raise ValueError(f"w_closure: no spoken form for ${t}$ -> give say=")
    return s


def KP(sub, say=None, do=(), hold=0.0):
    """P() with the spoken form derived through TEXSAY (then the shared lexicon)"""
    if say is None:
        s = re.sub(r"\$([^$]+)\$", lambda m: tsay(m.group(1)), sub.replace("**", ""))
        say = re.sub(r"<[^>]+>", "", s)
    return P(sub, say=say, do=do, hold=hold)
