# -*- coding: utf-8 -*-
"""Independent answer-key check: read the yellow highlights out of a solution PDF and
compare them with tools/raw/<CODE>.json.

    python tools/detect_keys.py <CODE> "<solution.pdf>" [--renumber "1:3,2:8,..."]

Yellow = a filled drawing with (r,g > .85, b < .45) or a Highlight annotation. Each
highlight is attributed to the last "שאלה N" heading above it (reading order), and its
letter is taken from the highlighted line. A '?' means the highlight had no letter
(e.g. only a math span was highlighted) — resolve it visually. Exit 1 on any disagreement.
"""
import sys, re, json, argparse, pathlib
import fitz

LET = {"א": "a", "ב": "b", "ג": "c", "ד": "d"}

def yellow(f): return bool(f) and f[0] > .85 and f[1] > .85 and f[2] < .45

def headings(page):
    out = []
    for m in page.search_for("שאלה"):
        line = page.get_textbox(fitz.Rect(m.x0 - 80, m.y0 - 2, m.x1 + 80, m.y1 + 2)).replace("\n", " ")
        # the number glued to the word (either side — some PDFs store visual order), with
        # digits split by stray spaces rejoined ("1 1" -> 11); fall back to any number
        g = re.search(r"שאלה\s*(\d(?:\s?\d)?)(?!\d)", line) or re.search(r"(?<!\d)(\d(?:\s?\d)?)\s*שאלה", line)
        n = [g.group(1).replace(" ", "")] if g else re.findall(r"(?<!\d)(\d{1,2})(?!\d)", line)
        if n and 1 <= int(n[0]) <= 30: out.append((m.y0, int(n[0])))
    return out

def detect(pdf):
    d = fitz.open(pdf); ev = []
    for pno, pg in enumerate(d):
        rects = [dr["rect"] for dr in pg.get_drawings() if yellow(dr.get("fill")) and dr["rect"].width > 6]
        rects += [a.rect for a in (pg.annots() or []) if a.type[1] == "Highlight"]
        rects.sort(key=lambda r: -r.width); seen = set()
        for r in rects:
            band = round((r.y0 + r.y1) / 16)
            if band in seen: continue
            seen.add(band)
            t = pg.get_textbox(fitz.Rect(r.x0 - 4, r.y0, r.x1 + 30, r.y1)).replace("\n", " ")
            m = re.search(r"([אבגד])\s*[.)]|[.)]\s*([אבגד])(?:\s|$)", t)
            ev.append((pno, r.y0, "Y", (m.group(1) or m.group(2)) if m else "?"))
        ev += [(pno, y, "H", n) for y, n in headings(pg)]
    ev.sort(key=lambda e: (e[0], e[1], e[2] == "Y"))
    keys, cur = {}, None
    for _, _, k, v in ev:
        if k == "H": cur = v
        elif cur is not None and v != "?": keys.setdefault(cur, [])
        if k == "Y" and cur is not None and v != "?": keys[cur].append(LET[v])
    return {n: sorted(set(v)) for n, v in keys.items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("code"); ap.add_argument("pdf"); ap.add_argument("--renumber", default="")
    a = ap.parse_args()
    ren = dict(tuple(map(int, p.split(":"))) for p in a.renumber.split(",") if p)
    found = detect(a.pdf)
    raw = json.loads((pathlib.Path(__file__).parent / "raw" / f"{a.code}.json").read_text(encoding="utf-8"))
    agree = disagree = unknown = 0
    for q in raw["questions"]:
        n = ren.get(q["num"], q["num"]); got = found.get(n, [])
        if not got: unknown += 1; print(f"  Q{q['num']:>2}: raw={q['correctId']} detector=?  (verify visually)")
        elif got == [q["correctId"]]: agree += 1
        else: disagree += 1; print(f"  Q{q['num']:>2}: raw={q['correctId']} detector={got}  <-- DISAGREE")
    print(f"{a.code}: agree {agree}, disagree {disagree}, undetected {unknown}")
    sys.exit(1 if disagree else 0)

if __name__ == "__main__":
    main()
