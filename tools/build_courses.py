# -*- coding: utf-8 -*-
"""tools/needhelp/<course>/<ID>.py  ->  courses/<course>/<ID>.js   (the guided "צריך עזרה?" courses)

The Python level modules are the source of truth: every option's truth value is computed by a simulator from
tools/verify/needhelp/lib.py at import time (nh.Q refuses to build unless exactly one option is true).
This script renders their text (TeX -> MathML via render_math.js / KaTeX, same pipeline as the bank) and writes
one `AF_LEVEL("<course>", {...})` script per level. Then run `node tools/course_check.js --sync`.

Run:  PYTHONUTF8=1 python tools/build_courses.py [course ...]
"""
import importlib.util, json, pathlib, re, sys
from collections import Counter

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TOOLS / "needhelp"))
import build_questions as bq   # noqa: E402
import nh                     # noqa: E402

COURSES = ["fa", "nerode", "classify", "cf"]
PREFIX = {"fa": "F", "nerode": "N", "classify": "K", "cf": "G"}
BANK = {q["id"]: q for q in json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["questions"]}


def load_levels(course):
    out = []
    d = TOOLS / "needhelp" / course
    for f in sorted(d.glob(PREFIX[course] + "[0-9][0-9].py")):
        spec = importlib.util.spec_from_file_location(f"nh_{course}_{f.stem}", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out.append(m.LEVEL)
    return out


MATH_RE = re.compile(r"(\$\$.+?\$\$|\$[^$]+\$)", re.S)
PUNCT_AFTER = re.compile(r"^[.,:;?!)\]]+")


def html_math(s, mb):
    """raw HTML with $…$ / $$…$$ -> MathML placeholders (the HTML around it is left alone)"""
    parts = MATH_RE.split(s)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 0:
            out.append(p)
        elif p.startswith("$$"):
            out.append(bq.display_math(p[2:-2].strip(), mb))
        else:
            m = bq.inline_math(p[1:-1].strip(), mb)
            nxt = parts[i + 1] if i + 1 < len(parts) else ""
            g = PUNCT_AFTER.match(nxt)
            if g:
                out.append(f'<span class="nobr">{m}{g.group(0)}</span>')
                parts[i + 1] = nxt[g.end():]
            else:
                out.append(m)
    return "".join(out)


def option_obj(text, oid, mb):
    m = re.fullmatch(r"\$([^$]+)\$", text.strip())
    o = {"id": oid, "type": "math", "value": m.group(1)} if m else {"id": oid, "type": "text", "value": text}
    o["html"] = bq.option_html(o, mb)
    return o


def build_level(course, L, mb):
    d = {"id": L.id, "order": L.order, "icon": L.icon, "title": L.title, "goal": L.goal}
    if "$" in L.title:
        d["titleHtml"] = bq.rich(L.title, mb)
    if "$" in L.goal:
        d["goalHtml"] = bq.rich(L.goal, mb)
    if L.boss:
        d["boss"] = True
    d["lessonHtml"] = html_math(L.lesson.strip(), mb)
    qs = []
    for q in L.questions:
        if isinstance(q, nh.Bank):
            if q.bid not in BANK:
                sys.exit(f"{L.id}: unknown bank question {q.bid}")
            e = {"bankId": q.bid, "recapHtml": bq.rich(q.recap, mb)}
            if q.why:
                e["explanationHtml"] = bq.rich(q.why, mb)
            qs.append(e)
            continue
        ids = "abcde"
        opts = [option_obj(o.text, ids[i], mb) for i, o in enumerate(q.opts)]
        right = [ids[i] for i, o in enumerate(q.opts) if o.ok][0]
        qh = bq.rich(q.stem, mb)
        if q.table:
            qh += bq.table_html(q.table, mb)
        qs.append({"id": q.id, "questionHtml": qh, "options": opts, "correctId": right,
                   "explanationHtml": bq.rich(q.why, mb), "recapHtml": bq.rich(q.recap, mb)})
    d["questions"] = qs
    return d


def main():
    which = [a for a in sys.argv[1:] if not a.startswith("--")] or COURSES
    mb = bq.MathBatch()
    built = []   # (course, level dict)
    stats = Counter()
    for c in which:
        levels = load_levels(c)
        if not levels:
            print(f"{c}: no levels yet")
            continue
        seen = set()
        for L in levels:
            if L.id in seen:
                sys.exit(f"duplicate level id {L.id}")
            seen.add(L.id)
            built.append((c, build_level(c, L, mb)))
            for q in L.questions:
                if isinstance(q, nh.Question):
                    for o in q.opts:
                        stats[o.kind] += 1
                    stats["own"] += 1
                else:
                    stats["bank"] += 1
    rendered = mb.render()
    for c, d in built:
        # json.dumps writes the NUL placeholders as \u0000M<i>\u0000; swap in the rendered MathML (JSON-escaped)
        out = json.dumps(d, ensure_ascii=False, indent=1)
        out = re.sub(r"\\u0000M(\d+)\\u0000", lambda m: json.dumps(rendered[int(m.group(1))], ensure_ascii=False)[1:-1], out)
        folder = ROOT / "courses" / c
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{d['id']}.js").write_text(
            f"/* {c} course · level {d['order']} · {d['title']} — GENERATED by tools/build_courses.py from "
            f"tools/needhelp/{c}/{d['id']}.py; edit the .py, not this file */\nAF_LEVEL({json.dumps(c)}, {out});\n",
            encoding="utf-8")
    print(f"built {len(built)} levels, {stats['own']} own questions, {stats['bank']} bank questions, "
          f"{len(mb.items)} math snippets; options: {stats['sim']} simulator-computed, {stats['judged']} judged")


if __name__ == "__main__":
    main()
