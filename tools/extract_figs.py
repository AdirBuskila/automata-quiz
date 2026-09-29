# -*- coding: utf-8 -*-
"""List / extract embedded raster figures from an exam PDF (lossless, no re-render).

Usage:
    python tools/extract_figs.py "<pdf>"                      # list figures: page, xref, bbox, nearest "שאלה N"
    python tools/extract_figs.py "<pdf>" --xref 12 --out images/exams/26A-A-Q7.png

Header logos (small images at the top of each page) are skipped in the listing.
"""
import sys, argparse, pathlib, re
import fitz

def nearest_question(page, y):
    best = None
    for r in page.search_for("שאלה"):
        if r.y0 <= y + 5:
            line = page.get_textbox(fitz.Rect(r.x0 - 60, r.y0, r.x1 + 60, r.y1)).replace("\n", " ")
            n = re.findall(r"\d{1,2}", line)
            if n and (best is None or r.y0 > best[0]): best = (r.y0, int(n[0]))
    return best[1] if best else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--xref", type=int); ap.add_argument("--out")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    if a.xref:
        pix = fitz.Pixmap(doc, a.xref)
        if pix.alpha or pix.n > 3: pix = fitz.Pixmap(fitz.csRGB, pix)
        out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
        pix.save(out); print(f"xref {a.xref} -> {out} ({pix.width}x{pix.height})"); return
    for pno, page in enumerate(doc):
        for info in page.get_image_info(xrefs=True):
            b = fitz.Rect(info["bbox"])
            if b.y0 < 90 and b.height < 80: continue
            if b.width < 40 or b.height < 30: continue
            print(f"p{pno+1:02d} xref={info['xref']:4d} bbox={[round(x) for x in b]} "
                  f"{info['width']}x{info['height']} ~Q{nearest_question(page, b.y0)}")

if __name__ == "__main__":
    main()
