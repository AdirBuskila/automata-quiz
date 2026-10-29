# -*- coding: utf-8 -*-
"""Prepare the YouTube upload folder (manual upload in YouTube Studio; the API locks new projects' uploads to private).

Writes <dest>/ with one MP4 per video named "NN · <ID> · <title>.mp4" (Studio uses the file name as the title; NN keeps
course order), titles_and_descriptions.txt (title + description per video, ready to paste) and README.txt (Hebrew
instructions). Refuses a video whose MP4 is missing or older than its script (not re-rendered after a change).

Run:  PYTHONUTF8=1 python tools/video/prepare_upload.py ["C:/Users/Adir/Desktop/YouTube upload"] [--only F01,N03,…]
--only limits the folder to videos that passed QA (the mtime check cannot see a lexicon change).
"""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://adirbuskila.github.io/automata-quiz/"
BAD = re.compile(r'[<>:"/\\|?*]')
BONUS_GOAL = {
    "K06a": "סגירות של שפות רגולריות: לפתור שאלות מבחן על איחוד, חיתוך, משלים, שרשור וכוכבית, עם המלכודת של כל אחת.",
    "K06b": "סגירות של שפות חסרות הקשר: מה נשמר, מה נשבר, ואיך מוכיחים בדוגמה נגדית — על שאלות מבחן אמיתיות.",
}


def manifest():
    s = (ROOT / "videos.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def goal(course, vid, level):
    if vid in BONUS_GOAL:                 # bonus videos share their level's goal; they get their own
        return BONUS_GOAL[vid]
    m = re.search(r'"goal":\s*"([^"]*)"', (ROOT / "courses" / course / f"{level}.js").read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def main():
    args = sys.argv[1:]
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = set(args[i + 1].split(","))
        del args[i:i + 2]
    dest = pathlib.Path(args[0] if args else pathlib.Path.home() / "Desktop" / "YouTube upload")
    dest.mkdir(parents=True, exist_ok=True)
    blocks, problems, n = [], [], 0
    for c in manifest()["courses"]:
        for v in c["videos"]:
            n += 1
            vid = v["id"]
            if only is not None and vid not in only:
                continue
            mp4 = ROOT / "videos" / "out" / vid / f"{vid}.mp4"
            script = ROOT / "videos" / c["id"] / vid / f"{vid}.py"
            if not mp4.exists():
                problems.append(f"{vid}: not rendered")
                continue
            newest = max(script.stat().st_mtime, (ROOT / "tools" / "video" / "shosh.py").stat().st_mtime)
            if mp4.stat().st_mtime < newest:
                problems.append(f"{vid}: MP4 is older than its script or the presenter (re-render)")
                continue
            title = f"{vid} · {v['title']} | אוטומטים ושפות פורמליות"
            if len(title) > 100:
                title = f"{vid} · {v['title']}"[:100]
            name = BAD.sub("-", f"{n:02d} · {vid} · {v['title']}".replace(": ", " · ").replace("?", "")) + ".mp4"
            shutil.copy2(mp4, dest / name)
            desc = (f"{c['title']} · {vid}{' (סרטון בונוס)' if v.get('bonus') else ''}\n\n"
                    f"{goal(c['id'], vid, v['level'])}\n\n"
                    "הסבר, דוגמאות שרצות צעד אחר צעד, ושאלה אמיתית ממבחן עם המלכודת שלה — "
                    "במושגים ובסימונים של הקורס אוטומטים ושפות פורמליות (62208).\n\n"
                    f"לתרגול השלב הזה ולכל שאר הסרטונים: {SITE}?video={vid}\n"
                    "מגישה: שוש 😊")
            blocks.append(f"===== {name}\nכותרת:\n{title}\n\nתיאור:\n{desc}\n")
    (dest / "titles_and_descriptions.txt").write_text("\n".join(blocks), encoding="utf-8")
    (dest / "README.txt").write_text(
        "העלאה ל-YouTube (בערך 20–30 דקות)\n"
        "==================================\n"
        f"1. YouTube Studio ← יצירה ← העלאת סרטונים. גוררים עד 15 קבצים בכל פעם ({-(-len(blocks) // 15)} סבבים).\n"
        "   שם הקובץ הופך לכותרת. אפשר להשאיר אותו, או להעתיק כותרת ותיאור מ-titles_and_descriptions.txt.\n"
        "2. בכל סרטון: \"לא, הסרטון לא מיועד לילדים\". אפשר לדלג על שאר השלבים.\n"
        "3. אחרי שכולם עלו: בתוכן, מסמנים את כולם ← עריכה ← חשיפה ← \"לא רשום\" (Unlisted) ← עדכון.\n"
        "4. (רשות) פלייליסט \"אוטומטים ושפות פורמליות · קורס וידאו\" לפי סדר המספרים.\n"
        "5. מעתיקים את הקישורים של כל הסרטונים (בכל סדר) ושולחים לClaude, והוא יחבר אותם לאתר.\n",
        encoding="utf-8")
    print(f"{len(blocks)} videos -> {dest}")
    if problems:
        print("NOT copied:\n  " + "\n  ".join(problems))


if __name__ == "__main__":
    main()
