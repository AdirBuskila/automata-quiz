# -*- coding: utf-8 -*-
"""Dump the question bank grouped by topic, for writing learn briefs.

    PYTHONUTF8=1 python tools/dump_topics.py            -> tools/raw/_digest/<topic>.md
Each entry: id, stem, options (✅ on the key), explanation. Reads tools/raw/*.json directly
(skips any file that doesn't parse, e.g. one being written right now).
"""
import json, pathlib, collections

TOOLS = pathlib.Path(__file__).resolve().parent
OUT = TOOLS / "raw" / "_digest"
OUT.mkdir(parents=True, exist_ok=True)
by = collections.defaultdict(list)
for f in sorted((TOOLS / "raw").glob("*.json")):
    try:
        ex = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"skip {f.name}: {e}"); continue
    for q in ex["questions"]:
        by[q["topic"]].append((ex, q))
for topic, items in sorted(by.items()):
    lines = [f"# {topic} — {len(items)} questions", ""]
    for ex, q in items:
        acc = set(q.get("acceptedIds") or [q["correctId"]])
        lines.append(f"## `{ex['examCode']}-Q{q['num']}` ({ex['examLabel']})" + (" [image]" if q.get("image") or q.get("contextId") else ""))
        lines.append(q["question"])
        for o in q["options"]:
            lines.append(f"- {'✅' if o['id'] in acc else '  '} {o['id']}) {o['value']}")
        lines.append(f"> {q.get('explanation','')}")
        lines.append("")
    (OUT / f"{topic}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{topic:12s} {len(items):3d}")
