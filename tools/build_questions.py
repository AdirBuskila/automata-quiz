# -*- coding: utf-8 -*-
"""tools/raw/*.json  ->  questions.json + questions.js + tools/build_report.md

The raw per-exam files are the source of truth (see docs/build_plan.md). This build:
  * namespaces ids (<CODE>-Q<num>) and context ids (<CODE>-<localId>),
  * derives topicLabel / examLabel / year / dedupKey / lockOrder / per-option `last`,
  * renders every stem, option, explanation and context to HTML, with all TeX turned
    into MathML by tools/render_math.js (KaTeX, build-time only — the site ships no math JS).

Run:  PYTHONUTF8=1 python tools/build_questions.py
"""
import json, re, sys, hashlib, subprocess, pathlib, html
from collections import Counter, defaultdict

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
RAW = TOOLS / "raw"

# Closed topic set — keep in sync with validate.py, app.js TOPICS, and the learn MANIFEST.
TOPIC_LABEL = {
    "basics": "מחרוזות, שפות ופעולות",
    "dfa": "אס״ד",
    "nfa": "אסל״ד ומסעי ε",
    "regex": "ביטויים רגולריים",
    "reg_closure": "תכונות סגירות (רגולריות)",
    "pumping_reg": "למת הניפוח (רגולריות)",
    "nerode": "נרוד · Rank · מינימיזציה",
    "cfg": "דקדוקים חסרי הקשר",
    "pda": "אוטומט מחסנית",
    "cfl_props": "תכונות שפות ח״ה",
    "classify": "סיווג שפות",
}

# An option that talks about "the other claims" must stay last, wherever the rest land.
LAST_RE = re.compile(r"כל הטענות|כל המחרוזות|כל התשובות|אף אחת מה")
# An option that cites a sibling by its printed letter pins the whole question's order.
LOCK_RE = re.compile(r"(תשובות|טענות|סעיפים)\s+[אבגד]['׳]?\s*(,|\+|ו-?|וגם)\s*[אבגד]|סעיף\s+[אבגד]['׳]?(?=[\s.,)])")

HEB = re.compile(r"[֐-׿]")


def esc(s):
    return html.escape(str(s), quote=False)


class MathBatch:
    """Collects TeX snippets, renders them all in one node call, then fills placeholders."""
    def __init__(self):
        self.items = []

    def add(self, tex, display):
        if HEB.search(tex):
            raise ValueError(f"Hebrew inside math is not allowed: {tex!r}")
        self.items.append({"tex": tex, "display": display})
        return f"\u0000M{len(self.items) - 1}\u0000"

    def render(self):
        if not self.items:
            return []
        p = subprocess.run(["node", str(TOOLS / "render_math.js")], input=json.dumps({"items": self.items}),
                           capture_output=True, text=True, encoding="utf-8")
        if p.returncode != 0:
            sys.exit("render_math.js failed:\n" + p.stderr)
        out = json.loads(p.stdout)
        if out["errors"]:
            for e in out["errors"]:
                print(f"  MATH ERROR [{e['tex']}]: {e['err']}")
            sys.exit("math errors — fix the TeX in tools/raw/*.json")
        return out["html"]


ARRAY_L = re.compile(r"^\\begin\{array\}\{l\}(.*)\\end\{array\}$", re.S)
PUNCT_AFTER = re.compile(r"^[.,:;?!)\]]+")


def display_math(tex, mb):
    # Chrome's MathML ignores mtable column alignment, so a left-aligned multi-line block
    # (grammar productions, one per row) is emitted as one display formula per row inside
    # a shrink-wrapped, centred, left-aligned box.
    m = ARRAY_L.match(tex)
    if m:
        rows = [r.strip() for r in re.split(r"\\\\", m.group(1)) if r.strip()]
        return '<div class="math-lines">' + "".join(f"<div>{mb.add(r, False)}</div>" for r in rows) + "</div>"
    # a long one-line display formula would be clipped at phone width: render it as
    # wrapping inline pieces in a centred block instead (no fractions/sums in this course)
    if len(tex) > 44 and len(split_inline(tex)) > 1 and not re.search(r"\\(frac|sum|prod|begin)", tex):
        return f'<div class="math-block math-wrapd">{inline_math(tex, mb)}</div>'
    return f'<div class="math-block">{mb.add(tex, True)}</div>'


# Top-level relation symbols where a long inline formula may wrap onto the next line.
REL_RE = re.compile(r"(?=(?:\\le(?![a-z])|\\ge(?![a-z])|\\ne(?![a-z])|\\neq|\\leq|\\geq|\\subseteq|\\subsetneq|"
                    r"\\supseteq|\\subset(?![a-z])|\\in(?![a-z])|\\notin|\\iff|\\Rightarrow|\\Leftrightarrow|"
                    r"\\mid|\\wedge|\\land|\\lor|\\vee|\\text\{|\\mathrm\{(?:and|or)\}|=|<|>))")
LONG_INLINE = 26   # TeX chars; shorter formulas always stay in one piece


def split_inline(tex):
    """A MathML <math> element never line-breaks, so a long inline formula overflows a
    phone-width option. Split it before relations / `\\mid` / logic connectives / `\\text`
    into pieces rendered separately (the reader sees one formula). Cuts only happen outside
    TeX grouping braces `{…}` and outside `\\left…\\right`, so every piece is valid TeX;
    escaped `\\{ \\}` and parentheses are plain symbols and may be split across pieces."""
    if len(tex) <= LONG_INLINE:
        return [tex]
    cuts, depth, pdepth, i = [], 0, 0, 0
    while i < len(tex):
        c = tex[i]
        if tex.startswith("\\left", i) or tex.startswith("\\right", i):
            is_left = tex.startswith("\\left", i)
            if is_left and depth == 0 and pdepth == 0 and i > 0 and tex[i - 1] in ")*}":
                cuts.append(i)                                # break between concatenated groups
            depth += 1 if is_left else -1
            i += 5 if is_left else 6
            i += 2 if i < len(tex) and tex[i] == "\\" else 1   # \left\{  /  \left(
            continue
        if c == "\\" and i + 1 < len(tex) and tex[i + 1] in "{}":
            i += 2                                            # escaped brace: a symbol
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "(":
            # regex concatenation of groups: allow a break before a group that follows ")" or "*"
            if depth == 0 and pdepth == 0 and i > 0 and tex[i - 1] in ")*": cuts.append(i)
            pdepth += 1
        elif c == ")":
            pdepth -= 1
        elif depth == 0 and i > 0 and (REL_RE.match(tex, i) or (c == "+" and pdepth == 0)):
            cuts.append(i)
        i += 1
    pieces, last = [], 0
    for c in cuts:
        if tex[last:c].strip():
            pieces.append(tex[last:c]); last = c
    pieces.append(tex[last:])
    # a piece that is only an operator (e.g. "=" before a group) would render oddly alone;
    # never split when any piece is empty after stripping
    return pieces if all(p.strip() for p in pieces) and len(pieces) > 1 else [tex]


def inline_math(tex, mb):
    parts = split_inline(tex)
    if len(parts) == 1:
        return mb.add(tex, False)
    return '<span class="mwrap">' + "<wbr>".join(mb.add(p, False) for p in parts) + "</span>"


def rich(s, mb):
    """richText markup -> HTML: $$display$$, $inline$, `code`, **bold**; newlines -> <br>.
    Punctuation right after an inline formula is glued to it (no orphan '.' on its own line)."""
    parts = re.split(r"(\$\$.+?\$\$|\$[^$]+\$|`[^`]+`|\*\*[^*]+\*\*)", str(s), flags=re.S)
    out = []
    i = 0
    while i < len(parts):
        p = parts[i]
        if p.startswith("$$") and p.endswith("$$") and len(p) > 4:
            out.append(display_math(p[2:-2].strip(), mb))
        elif p.startswith("$") and p.endswith("$") and len(p) > 2:
            m = inline_math(p[1:-1].strip(), mb)
            nxt = parts[i + 1] if i + 1 < len(parts) else ""
            g = PUNCT_AFTER.match(nxt)
            if g:
                out.append(f'<span class="nobr">{m}{esc(g.group(0))}</span>')
                parts[i + 1] = nxt[g.end():]
            else:
                out.append(m)
        elif p.startswith("`") and p.endswith("`") and len(p) > 2:
            out.append(f'<code class="tok" dir="ltr">{esc(p[1:-1])}</code>')
        elif p.startswith("**") and p.endswith("**") and len(p) > 4:
            out.append(f"<strong>{esc(p[2:-2])}</strong>")
        else:
            out.append(esc(p).replace("\n", "<br>"))
        i += 1
    return "".join(out)


def option_html(o, mb):
    t = o.get("type", "text")
    v = o["value"]
    if t == "image":
        return f'<img class="opt-img q-img" src="{esc(v)}" alt="" loading="lazy">'
    if t == "code":
        return f'<pre class="opt-code" dir="ltr"><code>{esc(v)}</code></pre>'
    if t == "math":
        return f'<span class="opt-math" dir="ltr">{inline_math(v, mb)}</span>'
    body = rich(v, mb)
    # Hebrew-free option text renders LTR, or the RTL page reorders it.
    return body if HEB.search(re.sub(r"\$[^$]*\$", "", v)) else f'<span class="opt-ltr" dir="ltr">{body}</span>'


def table_html(t, mb):
    h = '<div class="tbl-wrap"><table class="ctx-table" dir="ltr">'
    if t.get("head"):
        h += "<thead><tr>" + "".join(f"<th>{rich(c, mb)}</th>" for c in t["head"]) + "</tr></thead>"
    h += "<tbody>" + "".join("<tr>" + "".join(f"<td>{rich(c, mb)}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</tbody>"
    return h + "</table></div>"


def context_html(c, mb):
    h = ""
    if c.get("title"):
        h += f'<div class="ctx-title">{esc(c["title"])}</div>'
    if c.get("text"):
        h += f'<div class="ctx-text">{rich(c["text"], mb)}</div>'
    if c.get("tex"):
        h += f'<div class="ctx-math math-block">{mb.add(c["tex"], True)}</div>'
    if c.get("table"):
        h += table_html(c["table"], mb)
    if c.get("image"):
        cap = f'<figcaption>{esc(c["caption"])}</figcaption>' if c.get("caption") else ""
        h += f'<figure class="ctx-fig"><img class="q-img ctx-img" src="{esc(c["image"])}" alt="" loading="lazy">{cap}</figure>'
    return h


def norm(s):
    return re.sub(r"[\s.,:;?!()\[\]{}'\"״׳\-–]+", "", str(s)).lower()


def image_hash(rel):
    """Coarse perceptual hash (12x12 average hash) so two questions with the same text but
    different diagrams (e.g. Moodle variants) are not treated as duplicates, while the same
    diagram re-cropped from another exam PDF usually still matches."""
    from PIL import Image
    im = Image.open(ROOT / rel).convert("L").resize((12, 12), Image.LANCZOS)
    px = list(im.getdata()); avg = sum(px) / len(px)
    return "".join("1" if p > avg else "0" for p in px)


def dedup_key(q, ctx_images=()):
    opts = sorted(norm(o["value"]) for o in q["options"])
    imgs = [q["image"]] if q.get("image") else []
    imgs += [o["value"] for o in q["options"] if o.get("type") == "image"] + list(ctx_images)
    figs = "|".join(image_hash(p) for p in imgs)
    return hashlib.sha1((norm(q["question"]) + "|" + "|".join(opts) + "#" + figs).encode("utf-8")).hexdigest()[:12]


def main():
    # `--check CODE [CODE…]`: render only those exams' math and report errors, write nothing.
    # Extraction agents use this so parallel work never races on questions.js.
    check = "--check" in sys.argv
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    files = sorted(p for p in RAW.glob("*.json") if not only or p.stem in only)
    if not files:
        sys.exit("no tools/raw/*.json")
    mb = MathBatch()
    contexts, questions, exams = {}, [], []
    for f in files:
        ex = json.loads(f.read_text(encoding="utf-8"))
        code = ex["examCode"]
        exams.append(ex)
        for lid, c in (ex.get("contexts") or {}).items():
            cid = f"{code}-{lid}"
            contexts[cid] = {"kind": c.get("kind", "text"), "html": context_html(c, mb)}
        for q in ex["questions"]:
            out = {
                "id": f"{code}-Q{q['num']}",
                "examCode": code,
                "examLabel": ex["examLabel"],
                "year": ex["year"],
                "source": ex.get("source", "exam"),
                "num": q["num"],
                "topic": q["topic"],
                "topicLabel": TOPIC_LABEL[q["topic"]],
                "question": q["question"],
                "questionHtml": rich(q["question"], mb),
                "options": [],
                "correctId": q["correctId"],
                "official": bool(q.get("official", False)),
                "answerSource": q["answerSource"],
                "confidence": q.get("confidence", "high"),
                "explanation": q.get("explanation", ""),
                "explanationHtml": rich(q.get("explanation", ""), mb),
                "dedupKey": dedup_key(q, [c["image"] for c in [(ex.get("contexts") or {}).get(q.get("contextId"), {})] if c.get("image")]),
            }
            if q.get("acceptedIds"):
                out["acceptedIds"] = q["acceptedIds"]
            if q.get("contextId"):
                out["contextId"] = f"{code}-{q['contextId']}"
            if q.get("image"):
                out["image"] = q["image"]
            lock = bool(q.get("lockOrder"))
            for o in q["options"]:
                oo = {"id": o["id"], "type": o.get("type", "text"), "value": o["value"], "html": option_html(o, mb)}
                if o.get("type", "text") == "text" and LAST_RE.search(o["value"]):
                    oo["last"] = True
                if o.get("type", "text") == "text" and LOCK_RE.search(o["value"]):
                    lock = True
                out["options"].append(oo)
            if lock:
                out["lockOrder"] = True
            questions.append(out)

    rendered = mb.render()
    if check or only:
        print(f"check OK: {len(questions)} questions, {len(mb.items)} math snippets rendered, nothing written")
        return
    fill = lambda s: re.sub("\u0000M(\\d+)\u0000", lambda m: rendered[int(m.group(1))], s)
    for q in questions:
        q["questionHtml"] = fill(q["questionHtml"])
        q["explanationHtml"] = fill(q["explanationHtml"])
        for o in q["options"]:
            o["html"] = fill(o["html"])
    for c in contexts.values():
        c["html"] = fill(c["html"])

    ids = Counter(q["id"] for q in questions)
    dup = [i for i, n in ids.items() if n > 1]
    if dup:
        sys.exit(f"duplicate ids: {dup}")

    meta = {"course": "אוטומטים ושפות פורמליות (62208)", "count": len(questions),
            "topics": TOPIC_LABEL, "exams": [{"code": e["examCode"], "label": e["examLabel"], "year": e["year"],
                                              "source": e.get("source", "exam")} for e in exams]}
    data = {"meta": meta, "contexts": contexts, "questions": questions}
    payload = json.dumps(data, ensure_ascii=False, indent=1)
    (ROOT / "questions.json").write_text(payload, encoding="utf-8")
    (ROOT / "questions.js").write_text("window.AUTOMATA_QUIZ = " + payload + ";\n", encoding="utf-8")

    # ---- report ----
    by_topic = Counter(q["topic"] for q in questions)
    by_exam = Counter(q["examCode"] for q in questions)
    by_src = Counter(q["source"] for q in questions)
    groups = defaultdict(list)
    for q in questions:
        groups[q["dedupKey"]].append(q["id"])
    dups = {k: v for k, v in groups.items() if len(v) > 1}
    lines = ["# Build report", "", f"**{len(questions)} questions**, {len(contexts)} contexts, "
             f"{len(mb.items)} math snippets, {len(dups)} duplicate groups "
             f"({len(groups)} unique questions).", "", "## By topic", "", "| topic | label | n |", "|---|---|---|"]
    lines += [f"| {k} | {TOPIC_LABEL[k]} | {by_topic.get(k, 0)} |" for k in TOPIC_LABEL]
    lines += ["", "## By exam", "", "| exam | label | n |", "|---|---|---|"]
    lines += [f"| {e['examCode']} | {e['examLabel']} | {by_exam[e['examCode']]} |" for e in exams]
    lines += ["", "## By source", ""] + [f"- {k}: {v}" for k, v in by_src.items()]
    lines += ["", f"## lockOrder: {sum(1 for q in questions if q.get('lockOrder'))} · "
              f"pinned-last options: {sum(1 for q in questions for o in q['options'] if o.get('last'))}"]
    if dups:
        lines += ["", "## Duplicate groups (kept; deduped at runtime in practice pools)", ""]
        lines += [f"- {', '.join(v)}" for v in dups.values()]
    (TOOLS / "build_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"built {len(questions)} questions, {len(contexts)} contexts, {len(mb.items)} math snippets")


if __name__ == "__main__":
    main()
