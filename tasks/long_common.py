"""Shared helpers for the R-014 scored long projects (L05-L20). The same helpers as in
make_long_tasks.py, which stays frozen with the pilot projects L01-L04."""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

RULE = "Project rule (it applies to all later work too): "
DEC = "Design decision for this project: "
CHG = "Change to an earlier decision (it replaces the old one): "
FINISH = "Then finish any work that earlier sessions left for later."


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(textwrap.dedent(text).lstrip("\n"))


def g(handoff, tasks, decisions=None):
    out = {"tasks": [{"task": t, "status": s} for t, s in tasks], "handoff": handoff}
    if decisions:
        out["decisions"] = decisions
    return out


def later(fn, step):
    return f"The plan for {fn} has one more step: {step} Do not do that step now; leave it for a later session."


def mk(tid, kinds, readme, modules, prompts, given, hidden, ref):
    """modules: {file: start text}; prompts: 8 session prompts; given: C2g facts for sessions 1-7;
    ref: {file: reference text}."""
    assert len(prompts) == 8 and len(given) == 7 and len(kinds) == 12
    assert sum(k == "superseded" for k in kinds.values()) == 3
    assert sum(k == "unfinished" for k in kinds.values()) == 3
    base = os.path.join(ROOT, tid)
    _w(os.path.join(base, "repo", "README.md"), f"# {tid.lower()}\n\n{readme}\n")
    for name, text in modules.items():
        _w(os.path.join(base, "repo", name), text)
    names = ", ".join(m[:-3] for m in modules)
    _w(os.path.join(base, "repo", "tests", "test_smoke.py"), f"def test_import():\n    import {names}\n")
    _w(os.path.join(base, "repo", "conftest.py"), "")
    _w(os.path.join(base, "repo", "pytest.ini"), "[pytest]\ntestpaths = tests\n")
    sessions = [{"prompt": textwrap.dedent(p).strip()} for p in prompts]
    for s, gv in zip(sessions, given):
        s["given"] = gv
    with open(os.path.join(base, "sessions.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump({"id": tid, "kind": "long", "facts": kinds, "sessions": sessions}, f, indent=1)
        f.write("\n")
    _w(os.path.join(base, "hidden", "test_hidden.py"), hidden)
    for name, text in ref.items():
        _w(os.path.join(base, "ref", name), text)
