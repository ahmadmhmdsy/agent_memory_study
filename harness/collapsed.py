"""Finds units with a collapsed session: the provider fault where replies are cut to a few tokens
before the code fence on most steps. A session is collapsed when at least half of its action steps
are cut replies (no code, <= 30 output tokens). A unit is collapsed when any session is.

    python collapsed.py RUN_DIR             list collapsed units
    python collapsed.py RUN_DIR --move DIR  move their units/, ws/ and sessions.jsonl lines into RUN_DIR/DIR
"""
import glob
import json
import os
import shutil
import sys

CUT_TOKENS = 30
COLLAPSE_SHARE = 0.5


def session_actions(steps):
    # C3 carries earlier sessions' steps; keep only this session's (after its last task step).
    last_task = max((i for i, s in enumerate(steps) if s.get("kind") == "task"), default=-1)
    return [s for s in steps[last_task + 1:] if s.get("kind") == "action"]


def is_cut(step):
    code = step.get("codeAction")
    return (not code or not code.strip()) and (step.get("tokenUsage") or {}).get("outputTokens", 10**9) <= CUT_TOKENS


def collapsed_units(run):
    found = {}
    for f in sorted(glob.glob(os.path.join(run, "units", "*", "s*.steps.json"))):
        unit = os.path.basename(os.path.dirname(f))
        if not os.path.exists(os.path.join(run, "units", unit, "result.json")):
            continue
        acts = session_actions(json.load(open(f, encoding="utf8")))
        cut = sum(map(is_cut, acts))
        if acts and cut / len(acts) >= COLLAPSE_SHARE:
            found.setdefault(unit, []).append(f"{os.path.basename(f).split('.')[0]} {cut}/{len(acts)}")
    return found


def move(run, units, dest):
    dest = os.path.join(run, dest)
    os.makedirs(os.path.join(dest, "units"), exist_ok=True)
    os.makedirs(os.path.join(dest, "ws"), exist_ok=True)
    for u in units:
        for sub in ("units", "ws"):
            src = os.path.join(run, sub, u)
            if os.path.exists(src):
                shutil.move(src, os.path.join(dest, sub, u))
    keep, aside = [], []
    path = os.path.join(run, "sessions.jsonl")
    for line in open(path, encoding="utf8"):
        (aside if json.loads(line)["unit"] in units else keep).append(line)
    with open(os.path.join(dest, "sessions.jsonl"), "a", encoding="utf8") as f:
        f.writelines(aside)
    with open(path, "w", encoding="utf8") as f:
        f.writelines(keep)


if __name__ == "__main__":
    run = sys.argv[1]
    found = collapsed_units(run)
    for u, sessions in found.items():
        print(u, *sessions)
    print("collapsed units:", len(found))
    if "--move" in sys.argv and found:
        move(run, set(found), sys.argv[sys.argv.index("--move") + 1])
        print("moved to", sys.argv[sys.argv.index("--move") + 1])
