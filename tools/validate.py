# -*- coding: utf-8 -*-
"""Lint tools/raw/*.json before building.   PYTHONUTF8=1 python tools/validate.py [CODE ...]"""
import json, re, sys, pathlib

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
# keep in sync with build_questions.py TOPIC_LABEL / app.js TOPICS
TOPICS = {"basics", "dfa", "nfa", "regex", "reg_closure", "pumping_reg", "nerode", "cfg", "pda", "cfl_props", "classify"}
SOURCES = {"solution-pdf": True, "solution-pdf-v2": True, "merged-pdf": True,          # value = may be official
           "moodle-feedback": False, "moodle-100": False}
OPT_TYPES = {"text", "math", "code", "image"}
HEB = re.compile(r"[֐-׿]")
CODE_RE = re.compile(r"^(\d{2}[ABSX]-[ABC]|SAMP-\d{2}|MQ\d|MQ-T)$")


def math_spans(s):
    return re.findall(r"\$\$(.+?)\$\$|\$([^$]+)\$", str(s), flags=re.S)


def check_text(where, s, probs):
    s = str(s)
    if s.count("$") % 2:
        probs.append(f"{where}: unbalanced $")
    for a, b in math_spans(s):
        if HEB.search(a or b):
            probs.append(f"{where}: Hebrew inside math: {(a or b)[:40]!r}")
        # a wide one-line display gets clipped at 390px — put each definition on its own
        # row with \begin{array}{l} … \\ … \end{array} (rendered as left-aligned lines)
        if a and re.search(r"\\q?quad", a):
            probs.append(f"{where}: \\quad in display math — split into array{{l}} rows")


def main():
    only = set(sys.argv[1:])
    probs = []
    files = sorted(p for p in (TOOLS / "raw").glob("*.json") if not only or p.stem in only)
    for f in files:
        try:
            ex = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            probs.append(f"{f.name}: bad JSON: {e}"); continue
        code = ex.get("examCode")
        if code != f.stem: probs.append(f"{f.name}: examCode {code!r} != filename")
        if not CODE_RE.match(str(code)): probs.append(f"{f.name}: bad exam code {code!r}")
        for k in ("examLabel", "year", "questions"):
            if k not in ex: probs.append(f"{f.name}: missing {k}")
        ctx = ex.get("contexts") or {}
        for lid, c in ctx.items():
            if c.get("image") and not (ROOT / c["image"]).exists():
                probs.append(f"{code} ctx {lid}: image missing {c['image']}")
            for k in ("text", "caption"):
                if c.get(k): check_text(f"{code} ctx {lid}.{k}", c[k], probs)
            if c.get("tex") and HEB.search(c["tex"]): probs.append(f"{code} ctx {lid}: Hebrew in tex")
        nums = [q.get("num") for q in ex.get("questions", [])]
        if len(nums) != len(set(nums)): probs.append(f"{code}: duplicate question nums")
        for q in ex.get("questions", []):
            w = f"{code}-Q{q.get('num')}"
            if q.get("topic") not in TOPICS: probs.append(f"{w}: bad topic {q.get('topic')!r}")
            if not str(q.get("question", "")).strip(): probs.append(f"{w}: empty question")
            check_text(f"{w} question", q.get("question", ""), probs)
            check_text(f"{w} explanation", q.get("explanation", ""), probs)
            if q.get("contextId") and q["contextId"] not in ctx: probs.append(f"{w}: unknown contextId {q['contextId']}")
            if q.get("image") and not (ROOT / q["image"]).exists(): probs.append(f"{w}: image missing {q['image']}")
            opts = q.get("options") or []
            ids = [o.get("id") for o in opts]
            if len(opts) < 2: probs.append(f"{w}: <2 options")
            if len(ids) != len(set(ids)): probs.append(f"{w}: duplicate option ids")
            for o in opts:
                if o.get("type", "text") not in OPT_TYPES: probs.append(f"{w} opt {o.get('id')}: bad type")
                if not str(o.get("value", "")).strip(): probs.append(f"{w} opt {o.get('id')}: blank")
                if o.get("type") == "math" and HEB.search(o["value"]): probs.append(f"{w} opt {o['id']}: Hebrew in math option")
                if o.get("type") == "image" and not (ROOT / o["value"]).exists(): probs.append(f"{w} opt {o['id']}: image missing")
                if o.get("type", "text") == "text": check_text(f"{w} opt {o.get('id')}", o["value"], probs)
            if q.get("correctId") not in ids: probs.append(f"{w}: correctId {q.get('correctId')!r} not an option id")
            for a in q.get("acceptedIds") or []:
                if a not in ids: probs.append(f"{w}: acceptedId {a!r} not an option id")
            src = q.get("answerSource")
            if src not in SOURCES: probs.append(f"{w}: bad answerSource {src!r}")
            elif q.get("official") and not SOURCES[src]: probs.append(f"{w}: official=true needs a solution file")
            if q.get("confidence") not in ("high", "med", "low"): probs.append(f"{w}: bad confidence")
            if not str(q.get("explanation", "")).strip(): probs.append(f"{w}: no explanation")
    for p in probs: print(p)
    print(f"validate: {len(files)} files, {len(probs)} problems")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
