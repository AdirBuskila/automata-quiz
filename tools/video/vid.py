# -*- coding: utf-8 -*-
"""Video builder for the guided levels:  videos/<course>/<ID>/<ID>.py  ->  videos/out/<ID>/<ID>.mp4

A video script defines VIDEO = Video(...): scenes, each with stage HTML (stage.py widgets), a side panel, and a list
of phrases P(sub, say=None, do=[...]). `sub` is the subtitle in course spelling ($TeX$ allowed); `say` is what the
TTS reads (derived from `sub` through videos/lexicon.py when omitted; a TeX span the lexicon can't speak is an
error, so nothing is read wrongly by accident). `do` = show()/hide() actions fired when the phrase starts.

Pipeline: import the script (its simulator asserts run here) -> gates (bank ids/keys, boss ids, no Hebrew in TeX,
subtitle length) -> edge-tts per chunk (cached) with word-boundary alignment -> HyperFrames composition (MathML
from the bank's KaTeX pipeline) -> lint -> render -> loudness normalization -> review frames -> optional Hebrew
speech-to-text round trip (--stt).

Run:  PYTHONUTF8=1 python tools/video/vid.py F01 [--no-render] [--draft] [--stt] [--workers N]
"""
import asyncio, difflib, hashlib, importlib.util, json, pathlib, re, shutil, subprocess, sys, wave

TOOLS = pathlib.Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
VIDEOS = ROOT / "videos"
OUT = VIDEOS / "out"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TOOLS / "needhelp"))
sys.path.insert(0, str(VIDEOS))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lexicon  # noqa: E402

VOICE = "he-IL-HilaNeural"
RATE = "-6%"
SR = 24000
HEB = re.compile(r"[֐-׿]")
MATH = re.compile(r"\$([^$]+)\$")
BANK = {q["id"]: q for q in json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["questions"]}


# ----------------------------------------------------------------------------- script DSL
class P:
    """one subtitle line = one narration phrase. hold: silence after it (s); a hold ends the TTS chunk."""
    def __init__(self, sub, say=None, do=(), hold=0.0):
        self.sub, self.say_override, self.do, self.hold = sub, say, list(do), hold

    @property
    def say(self):
        if self.say_override is not None:
            return lexicon.say_hebrew(self.say_override)
        def tex(m):
            s = lexicon.tex_say(m.group(1))
            if s is None:
                raise ValueError(f"no spoken form for ${m.group(1)}$ in: {self.sub}\n  -> give P(..., say=...)")
            return s
        s = MATH.sub(tex, self.sub.replace("**", ""))
        return lexicon.say_hebrew(re.sub(r"<[^>]+>", "", s))


def show(*ids):
    return [("show", i) for i in ids]


def hide(*ids):
    return [("hide", i) for i in ids]


class Scene:
    """layout: 'split' (stage left, panel right), 'full' (stage only), 'title'"""
    def __init__(self, key, label, phrases, stage="", panel="", layout="split"):
        self.key, self.label, self.phrases, self.stage, self.panel, self.layout = key, label, phrases, stage, panel, layout


class Video:
    def __init__(self, id, course, title, scenes, bank=None):
        """bank: {bank_id: option id the video presents as correct} — checked against questions.json"""
        self.id, self.course, self.title, self.scenes, self.bank = id, course, title, scenes, dict(bank or {})


def run_dfa(pfx, D, word, names, tp=None, tab=None, lead=None, clear=(), fast=False):
    """phrases that run D on `word` letter by letter, every step computed by the simulator.
    pfx: diagram ids (stage.dfa_svg); tp: tape/trace/verdict ids (stage.tape/trace/verdict, default pfx);
    tab: table ids (stage.dfa_table) to highlight δ cells; clear: ids to hide first (a previous run's marks).
    Returns (phrases, states, end_ids) — end_ids are the marks left on, to pass as `clear` to the next run."""
    tp = tp or pfx
    states = [D.start]
    for c in word:
        states.append(D.delta[(states[-1], c)])
    ph = [P(lead or f"מתחילים במצב ההתחלתי ${names[D.start]}$.",
            do=hide(*clear) + show(f"{pfx}-hs-{D.start}", f"{tp}-r-0"))]
    for i, c in enumerate(word):
        p, r = states[i], states[i + 1]
        do = hide(f"{pfx}-hs-{p}")
        if i:
            pp = states[i - 1]
            do += hide(f"{tp}-k-{i - 1}", f"{pfx}-he-{pp}-{p}") + (hide(f"{tab}-c-{pp}-{word[i - 1]}") if tab else [])
            do += show(f"{tp}-d-{i - 1}")
        do += show(f"{tp}-k-{i}", f"{pfx}-he-{p}-{r}", f"{pfx}-hs-{r}", f"{tp}-r-{i + 1}")
        if tab:
            do += show(f"{tab}-c-{p}-{c}")
        verb = "נשארים ב" if p == r else "עוברים ל"
        if fast:
            sub = f"${c}$: ${names[r]}$"
            say = f"{lexicon.word_say(c)}: ל{lexicon.state_say(names[r])}."   # STT-checked pacing
        else:
            sub = f"קוראים ${c}$: {verb}-${names[r]}$."
            say = f"קוראים {lexicon.word_say(c)}, {verb}{lexicon.state_say(names[r])}."
        ph.append(P(sub, say=say, do=do))
    end = states[-1]
    ok = end in D.acc
    tail = (hide(f"{tp}-k-{len(word) - 1}") + show(f"{tp}-d-{len(word) - 1}") if word else []) + show(f"{tp}-v")
    ph.append(P(f"המילה נגמרה ב-${names[end]}$, " + ("שהוא מצב מקבל: המילה מתקבלת." if ok else "שאינו מקבל: המילה לא מתקבלת."),
                do=tail, hold=0.5))
    left = [f"{pfx}-hs-{end}"]
    if word:
        left += [f"{pfx}-he-{states[-2]}-{end}"] + ([f"{tab}-c-{states[-2]}-{word[-1]}"] if tab else [])
    return ph, states, left


# ----------------------------------------------------------------------------- loading + gates
def load(vid_id):
    hits = list(VIDEOS.glob(f"*/{vid_id}/{vid_id}.py"))
    if len(hits) != 1:
        sys.exit(f"{vid_id}: expected one videos/<course>/{vid_id}/{vid_id}.py, found {hits}")
    spec = importlib.util.spec_from_file_location(f"video_{vid_id}", hits[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)      # simulator asserts run here
    return m.VIDEO, hits[0].parent


def boss_ids():
    """bank ids used by the boss levels' quizzes: a video must never solve them"""
    import nh
    out = set()
    for f in (TOOLS / "needhelp").glob("*/*08.py"):
        spec = importlib.util.spec_from_file_location(f"boss_{f.stem}", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        if m.LEVEL.boss:
            out |= {q.bid for q in m.LEVEL.questions if isinstance(q, nh.Bank)}
    return out


def visible_len(sub):
    return len(MATH.sub(lambda m: "x" * max(1, len(m.group(1)) // 2), sub.replace("**", "")))


def gates(V):
    errs = []
    bosses = boss_ids()
    for bid, oid in V.bank.items():
        if bid not in BANK:
            errs.append(f"unknown bank id {bid}")
        elif BANK[bid]["correctId"] != oid and oid not in BANK[bid].get("acceptedIds", []):
            errs.append(f"{bid}: video says {oid}, bank key is {BANK[bid]['correctId']}")
        if bid in bosses and not V.id.endswith("08"):
            errs.append(f"{bid} is a boss-quiz question")
        if V.id.endswith("08") and bid in bosses:
            errs.append(f"{bid} is this course's boss question (spoiler)")
    texts = []
    for S in V.scenes:
        texts += [S.stage, S.panel] + [p.sub for p in S.phrases]
        for p in S.phrases:
            if visible_len(p.sub) > 120:
                errs.append(f"[{S.key}] subtitle too long ({visible_len(p.sub)}): {p.sub}")
            try:
                p.say
            except ValueError as e:
                errs.append(f"[{S.key}] {e}")
    for t in texts:
        for m in MATH.finditer(t):
            if HEB.search(m.group(1)):
                errs.append(f"Hebrew inside TeX: ${m.group(1)}$")
    if errs:
        sys.exit("gates failed:\n  " + "\n  ".join(errs))


# ----------------------------------------------------------------------------- TTS + timing
CACHE = OUT / "_tts"


async def _tts(text, mp3):
    import edge_tts
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    bounds, audio = [], bytearray()
    async for ch in c.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            bounds.append((ch["offset"] / 1e7, ch["text"]))
    mp3.write_bytes(bytes(audio))
    return bounds


def tts(text):
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:16]
    mp3, js = CACHE / f"{h}.mp3", CACHE / f"{h}.json"
    if not js.exists():
        js.write_text(json.dumps(asyncio.run(_tts(text, mp3)), ensure_ascii=False), encoding="utf-8")
    pcm = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return pcm, json.loads(js.read_text(encoding="utf-8"))


TOK = re.compile(r"[\w֐-׿]+")


def phrase_starts(says, bounds, dur):
    """start time of each phrase inside one TTS chunk, by aligning phrase tokens with the word-boundary events"""
    toks, owner = [], []
    for i, s in enumerate(says):
        for t in TOK.findall(s):
            toks.append(t)
            owner.append(i)
    ev = [(t, TOK.findall(w)) for t, w in bounds]
    ev_toks, ev_time = [], []
    for t, ws in ev:
        for w in ws:
            ev_toks.append(w)
            ev_time.append(t)
    tok_time = [None] * len(toks)
    for a, b, n in difflib.SequenceMatcher(None, toks, ev_toks, autojunk=False).get_matching_blocks():
        for k in range(n):
            tok_time[a + k] = ev_time[b + k]
    starts = []
    for i in range(len(says)):
        idx = [k for k, o in enumerate(owner) if o == i]
        t = next((tok_time[k] for k in idx if tok_time[k] is not None), None)
        if t is None:   # no matched token: interpolate by token position
            t = dur * (idx[0] / max(1, len(toks))) if idx else (starts[-1] if starts else 0.0)
        starts.append(max(0.0, t - 0.08))
    starts[0] = 0.0
    for i in range(1, len(starts)):
        starts[i] = max(starts[i], starts[i - 1] + 0.3)
    return starts


def build_timeline(V):
    """synthesize every chunk; return (pcm bytes, timeline) with absolute times per phrase and scene"""
    pcm = bytearray()
    t = 0.0
    sil = lambda s: b"\x00\x00" * int(SR * s)
    scenes, phrases = [], []
    LEAD, SCENE_GAP, CHUNK_GAP = 0.5, 0.7, 0.28
    for S in V.scenes:
        pcm += sil(LEAD)
        t += LEAD
        s_start = t - LEAD
        chunk = []
        groups = []
        for p in S.phrases:
            chunk.append(p)
            if p.hold > 0:
                groups.append(chunk)
                chunk = []
        if chunk:
            groups.append(chunk)
        for g in groups:
            text = " ".join(p.say for p in g)
            audio, bounds = tts(text)
            dur = len(audio) / 2 / SR
            starts = phrase_starts([p.say for p in g], bounds, dur)
            for k, p in enumerate(g):
                end = t + (starts[k + 1] if k + 1 < len(g) else dur + 0.15)
                phrases.append({"scene": S.key, "p": p, "start": t + starts[k], "end": end, "text": text})
            pcm += audio
            t += dur
            gap = max(CHUNK_GAP, g[-1].hold)
            pcm += sil(gap)
            t += gap
        pcm += sil(SCENE_GAP)
        t += SCENE_GAP
        scenes.append({"scene": S, "start": s_start, "end": t})
    return bytes(pcm), scenes, phrases, t


# ----------------------------------------------------------------------------- composition
def render_math(chunks):
    """$TeX$ in a list of HTML strings -> MathML (bank pipeline), same order"""
    import build_questions as bq
    from build_courses import html_math
    mb = bq.MathBatch()
    tmp = [html_math(c, mb) for c in chunks]
    rendered = mb.render()
    return [re.sub("\x00M(\\d+)\x00", lambda m: rendered[int(m.group(1))], c) for c in tmp]


def compose(V, scenes, phrases, total):
    css = (pathlib.Path(__file__).parent / "video.css").read_text(encoding="utf-8")
    blocks = []
    for sc in scenes:
        S = sc["scene"]
        blocks += [S.stage, S.panel]
    subs = [re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ph["p"].sub) for ph in phrases]
    rendered = render_math(blocks + subs)
    rb, rs = rendered[:len(blocks)], rendered[len(blocks):]
    body = []
    for i, sc in enumerate(scenes):
        S = sc["scene"]
        stage, panel = rb[2 * i], rb[2 * i + 1]
        top = (f'<header class="top"><span class="vid">{V.id}</span><span class="ttl">{V.title}</span>'
               f'<span class="lbl">{S.label}</span></header>') if S.layout != "title" else ""
        inner = {"split": f'<div class="stage">{stage}</div><aside class="panel">{panel}</aside>',
                 "full": f'<div class="stage full">{stage}</div>',
                 "title": f'<div class="titlecard">{stage}</div>'}[S.layout]
        body.append(f'<section class="scene clip {S.layout}" id="sc-{S.key}" data-start="{sc["start"]:.3f}" '
                    f'data-duration="{sc["end"] - sc["start"]:.3f}">{top}{inner}</section>')
    for i, ph in enumerate(phrases):
        body.append(f'<div class="sub clip" id="sub-{i}" data-start="{ph["start"]:.3f}" '
                    f'data-duration="{ph["end"] - ph["start"]:.3f}"><span>{rs[i]}</span></div>')
    js = []
    for ph in phrases:
        last = {}                       # hide+show of one element in one phrase (a self-loop step): the last wins
        for kind, el in ph["p"].do:
            last.pop(el, None)
            last[el] = kind
        for el, kind in last.items():
            op = 1 if kind == "show" else 0
            js.append(f'tl.to("#{el}",{{opacity:{op},duration:.25}},{ph["start"]:.3f});')
    ids = set(re.findall(r'id="([^"]+)"', "".join(body)))
    missing = sorted({el for ph in phrases for _, el in ph["p"].do} - ids)
    if missing:
        sys.exit(f"actions refer to missing ids: {missing}")
    return f"""<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{V.id}</title><style>{css}</style></head><body>
<div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-start="0" data-duration="{total:.3f}">
{"".join(body)}
<audio id="narr" src="narration.wav" data-start="0" data-duration="{total:.3f}"></audio>
</div>
<script src="gsap.min.js"></script>
<script>const tl=gsap.timeline({{paused:true}});
{"".join(js)}
window.__timelines={{root:tl}};</script>
</body></html>"""


# ----------------------------------------------------------------------------- render + checks
def hf(*args, cwd):
    exe = TOOLS / "node_modules" / ".bin" / ("hyperframes.cmd" if sys.platform == "win32" else "hyperframes")
    return subprocess.run([str(exe), *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def stt_check(phrases, outdir):
    """Hebrew speech-to-text round trip per chunk: flags chunks whose transcript drifts from the spoken text"""
    import numpy as np
    from faster_whisper import WhisperModel
    m = WhisperModel("ivrit-ai/whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8")
    sym = {**lexicon.DIGIT, "q": "קיו", "a": "איי", "b": "בי", "e": "איי", "i": "איי"}

    def norm(s):
        """letters only; the recognizer writes digits/Latin letters (0110, Q0, AB) where we spelled them out"""
        s = re.sub(r"[0-9a-z]", lambda m: sym.get(m.group(0), m.group(0)), s.lower())
        return re.sub(r"[^א-ת]", "", s)
    seen, rows = set(), []
    for ph in phrases:
        if ph["text"] in seen:
            continue
        seen.add(ph["text"])
        pcm, _ = tts(ph["text"])
        a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
        a = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
        segs, _ = m.transcribe(a, language="he")
        heard = " ".join(s.text.strip() for s in segs)
        r = difflib.SequenceMatcher(None, norm(ph["text"]), norm(heard)).ratio()
        rows.append((r, ph["scene"], ph["text"], heard))
    rows.sort(key=lambda x: x[0])
    lines = ["# STT round trip (lowest similarity first)", "",
             "Similarity of the normalized letters of the spoken text vs the ivrit-ai Whisper transcript.",
             "Digits/letters in the transcript (0110, Q0) vs spelled-out text lower the score; read the flagged rows.", ""]
    for r, sc, said, heard in rows:
        flag = "⚠️ " if r < 0.8 else ""
        lines += [f"- {flag}**{r:.2f}** [{sc}]", f"  - said:  {said}", f"  - heard: {heard}"]
    (outdir / "stt_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    bad = sum(1 for r in rows if r[0] < 0.8)
    print(f"stt: {len(rows)} chunks, {bad} below 0.8 -> {outdir / 'stt_report.md'}")


def main():
    args = sys.argv[1:]
    vid_id = next(a for a in args if not a.startswith("--"))
    workers = args[args.index("--workers") + 1] if "--workers" in args else "4"
    V, src = load(vid_id)
    gates(V)
    out = OUT / V.id
    proj = out / "proj"
    if proj.exists():
        shutil.rmtree(proj)
    proj.mkdir(parents=True)
    pcm, scenes, phrases, total = build_timeline(V)
    with wave.open(str(proj / "narration.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm)
    shutil.copy(TOOLS / "node_modules" / "gsap" / "dist" / "gsap.min.js", proj)
    html = compose(V, scenes, phrases, total)
    for src_img in set(re.findall(r'src="(images/[^"]+)"', html)):
        dst = proj / src_img
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src_img, dst)
    (proj / "index.html").write_text(html, encoding="utf-8")
    (out / "timeline.json").write_text(json.dumps(
        {"total": total, "scenes": [{"key": s["scene"].key, "start": s["start"], "end": s["end"]} for s in scenes],
         "phrases": [{"scene": p["scene"], "start": p["start"], "end": p["end"], "sub": p["p"].sub, "say": p["p"].say}
                     for p in phrases]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{V.id}: {len(scenes)} scenes, {len(phrases)} phrases, {total / 60:.1f} min")
    lint = hf("lint", cwd=proj)
    if not re.search(r"\b0 error", lint.stdout):    # warnings are Studio-only (nested <math> in timed divs)
        sys.exit("hyperframes lint failed:\n" + lint.stdout[-3000:])
    if "--no-render" not in args:
        raw = out / f"{V.id}_raw.mp4"
        r = hf("render", "-o", str(raw), "-q", "draft" if "--draft" in args else "looks", "-w", workers, cwd=proj)
        if r.returncode != 0 or not raw.exists():
            sys.exit("render failed:\n" + (r.stdout + r.stderr)[-3000:])
        final = out / f"{V.id}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-c:v", "copy", "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", str(final)],
                       check=True)
        frames = out / "frames"
        if frames.exists():
            shutil.rmtree(frames)
        frames.mkdir()
        shots = []
        for s in scenes:
            ps = [p for p in phrases if p["scene"] == s["scene"].key]
            for p in ps[:: max(1, len(ps) // 3)]:
                shots.append((s["scene"].key, p["end"] - 0.05))
            shots.append((s["scene"].key, s["end"] - 0.3))
        for i, (k, t) in enumerate(shots):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1",
                            "-vf", "scale=1280:-1", str(frames / f"{i:03d}_{k}_{t:06.1f}.png")], check=True)
        print(f"-> {final}  ({len(shots)} review frames in {frames})")
    if "--stt" in args:
        stt_check(phrases, out)


if __name__ == "__main__":
    main()
