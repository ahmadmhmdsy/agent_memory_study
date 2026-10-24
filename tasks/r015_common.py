"""Shared helpers for the R-015 projects: simple T01-T02 (4 sessions, about 5 facts) and
advanced A01-A02 (20+ sessions, facts superseded 2-3 times). Same style as long_common.py,
without its 8-session / 12-fact asserts and without C2g facts (C2g is dropped in R-015)."""
import json
import os
import textwrap

from long_common import CHG, DEC, FINISH, RULE, _w, later  # noqa: F401  (re-exported)

ROOT = os.path.dirname(os.path.abspath(__file__))


def mk(tid, kinds, readme, modules, prompts, hidden, ref, tier):
    """kinds: {fact: superseded|unfinished|constraint|decision}; prompts: one per session, the last
    one says FINISH; hidden: tests (test_fact_<fact> for every fact, test_stale_* for old values)."""
    assert FINISH in prompts[-1]
    for f in kinds:
        assert f"def test_fact_{f}(" in hidden, f"{tid}: no test for {f}"
    base = os.path.join(ROOT, tid)
    _w(os.path.join(base, "repo", "README.md"), f"# {tid.lower()}\n\n{readme}\n")
    for name, text in modules.items():
        _w(os.path.join(base, "repo", name), text)
    names = ", ".join(m[:-3] for m in modules)
    _w(os.path.join(base, "repo", "tests", "test_smoke.py"), f"def test_import():\n    import {names}\n")
    _w(os.path.join(base, "repo", "conftest.py"), "")
    _w(os.path.join(base, "repo", "pytest.ini"), "[pytest]\ntestpaths = tests\n")
    sessions = [{"prompt": textwrap.dedent(p).strip()} for p in prompts]
    with open(os.path.join(base, "sessions.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump({"id": tid, "kind": "long", "tier": tier, "facts": kinds, "sessions": sessions}, f, indent=1)
        f.write("\n")
    _w(os.path.join(base, "hidden", "test_hidden.py"), hidden)
    for name, text in ref.items():
        _w(os.path.join(base, "ref", name), text)
