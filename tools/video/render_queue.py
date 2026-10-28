# -*- coding: utf-8 -*-
"""Sequential render queue: renders the ids listed in videos/out/_queue.txt one at a time (full render + STT),
appending results to videos/out/_queue.log. Ids can be appended while it runs; a line "END" stops it once the
queue is empty. Usage:  PYTHONUTF8=1 python tools/video/render_queue.py [queue-name]
"""
import pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "videos" / "out"
NAME = sys.argv[1] if len(sys.argv) > 1 else "_queue"      # a second runner: render_queue.py _queue2
Q, LOG = OUT / f"{NAME}.txt", OUT / f"{NAME}.log"


def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    Q.touch()
    log("queue started")
    while True:
        lines = [l.strip() for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
        if not lines:
            time.sleep(30)
            continue
        vid = lines[0]
        if vid == "END":
            Q.write_text("\n".join(lines[1:]) + "\n", encoding="utf-8")
            log("queue ended")
            return
        log(f"start {vid}")
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "video" / "vid.py"), vid, "--stt", "--workers", "3"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip() and "Warning" not in l][-4:]
        log(f"{'done' if r.returncode == 0 else 'FAILED'} {vid}: " + " | ".join(tail))
        cur = [l.strip() for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
        if cur and cur[0] == vid:
            cur = cur[1:]
        Q.write_text("\n".join(cur) + ("\n" if cur else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
