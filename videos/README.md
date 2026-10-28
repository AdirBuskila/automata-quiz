# Video course (one video per guided level)

Design: `docs/superpowers/specs/2026-10-28-video-course-design.md`.

```
videos/<course>/<ID>/<ID>.py   the video script (committed): verified machines + scenes + narration
videos/lexicon.py              pronunciation lexicon (course spelling -> spoken form), shared by all videos
tools/video/vid.py             builder: gates -> edge-tts -> HyperFrames composition -> MP4 (+ STT check)
tools/video/stage.py           stage widgets (DFA diagram, δ table, tape, trace, options, exam raster)
tools/video/video.css          the look (app dark tokens)
videos/out/                    gitignored: <ID>/<ID>.mp4, proj/ (composition), frames/, timeline.json, stt_report.md
```

## Build

```bash
PY=/c/Users/Adir/AppData/Local/Programs/Python/Python313/python
PYTHONUTF8=1 $PY tools/video/vid.py F01 --no-render     # gates + TTS + composition only (fast)
tools/node_modules/.bin/hyperframes snapshot videos/out/F01/proj --at 12.5,40 --no-end -o videos/out/F01/snap
PYTHONUTF8=1 $PY tools/video/vid.py F01 --stt           # full render + Hebrew speech-to-text round trip
```

Deps (free, local): `pip install edge-tts faster-whisper`; `cd tools && npm install hyperframes gsap`.
The STT model (`ivrit-ai/whisper-large-v3-turbo-ct2`, ~1.6 GB) downloads on first `--stt`.

## Writing a script

- `P(sub, say=None, do=[...], hold=0)`: `sub` is the subtitle in course spelling with `$TeX$`; the spoken form is
  derived through the lexicon, and a TeX span it can't speak is a build error (give `say=`). Subtitles ≤ 120 chars.
- `do=show(ids…) + hide(ids…)` fires when the phrase starts. Widget ids are documented in `stage.py`.
- `run_dfa(...)` generates a letter-by-letter run from the simulator (narration, highlights, trace, verdict).
- Every machine is asserted with `tools/verify/needhelp/lib.py`; `Video(bank={id: option})` is checked against
  the bank key. Boss-quiz ids are refused. Never solve the level's own quiz questions.
- New pronunciation fix -> `videos/lexicon.py` (with the STT evidence in its docstring), never ad hoc.
