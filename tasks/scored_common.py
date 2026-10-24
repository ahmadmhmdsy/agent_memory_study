"""Shared writer for the 24 scored tasks. Each task gets repo/, sessions.json, hidden/ and,
outside repo/, ref.py (a full reference module used only to check the hidden tests)."""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(textwrap.dedent(text).lstrip("\n"))


def mk(tid, kind, module, readme, start, visible, prompts, given, hidden, ref):
    """prompts: 3 session prompts; given: C2g facts for sessions 1 and 2."""
    base = os.path.join(ROOT, tid)
    _w(os.path.join(base, "repo", "README.md"), f"# {module[:-3]}\n\n{readme}\n")
    _w(os.path.join(base, "repo", module), start)
    _w(os.path.join(base, "repo", "tests", f"test_{module}"), visible)
    _w(os.path.join(base, "repo", "conftest.py"), "")
    _w(os.path.join(base, "repo", "pytest.ini"), "[pytest]\ntestpaths = tests\n")
    sessions = [{"prompt": textwrap.dedent(p).strip()} for p in prompts]
    for s, g in zip(sessions, given):
        s["given"] = g
    with open(os.path.join(base, "sessions.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump({"id": tid, "kind": kind, "module": module, "sessions": sessions}, f, indent=1)
        f.write("\n")
    _w(os.path.join(base, "hidden", "test_hidden.py"), hidden)
    _w(os.path.join(base, "ref.py"), ref)


def g(handoff, tasks, decisions=None):
    out = {"tasks": [{"task": t, "status": s} for t, s in tasks], "handoff": handoff}
    if decisions:
        out["decisions"] = decisions
    return out
