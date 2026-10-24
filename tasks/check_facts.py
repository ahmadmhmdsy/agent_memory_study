"""Fact-coverage check: is each hidden fact test's fact stated in some session prompt?

check_long.py only checks that the reference passes and the start repo fails, so it missed
L06 (a decision no prompt states) and L10 (a slug step no prompt fully states). This check is a
screen, not a proof: for every test_fact_<name>, it takes the expected strings the test compares
against (not its input data) and looks for each in the project's prompts (exact first, then ignoring case and runs of
whitespace). A literal found in no prompt is flagged; a flagged test must be read by hand, since
a test may compute an expected value the prompt states in other words.

    python check_facts.py            # every project that has facts
    python check_facts.py L10f A01   # only these
"""
import ast
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def literals(fn):
    """Expected strings: constants compared directly in the test (a == "x", "x" in out), minus
    ones the test also passes in as input (test data echoed back), regexes and short labels."""
    inputs = {a.value for n in ast.walk(fn) if isinstance(n, ast.Call)
              for a in [*n.args, *(k.value for k in n.keywords)]
              if isinstance(a, ast.Constant) and isinstance(a.value, str)}
    out = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Compare):
            continue
        for side in [node.left, *node.comparators]:
            parts = side.elts if isinstance(side, (ast.List, ast.Tuple, ast.Set)) else [side]
            for c in parts:
                if not (isinstance(c, ast.Constant) and isinstance(c.value, str)):
                    continue
                v = c.value
                if v in inputs or len(v.strip()) < 3 or not re.search(r"[A-Za-z]", v):
                    continue
                out.append(v)
    return list(dict.fromkeys(out))


def check(task_dir):
    spec = json.loads((task_dir / "sessions.json").read_text(encoding="utf8"))
    facts = spec.get("facts") or {}
    prompts = "\n".join(s["prompt"] for s in spec["sessions"])
    tree = ast.parse((task_dir / "hidden" / "test_hidden.py").read_text(encoding="utf8"))
    tests = {n.name[len("test_fact_"):]: n for n in tree.body
             if isinstance(n, ast.FunctionDef) and n.name.startswith("test_fact_")}
    issues = []
    for name in facts:
        if name not in tests:
            issues.append(f"{name}: no test_fact_{name}")
    for name, fn in tests.items():
        if name not in facts:
            issues.append(f"{name}: test has no entry in facts")
        missing = [v for v in literals(fn) if v not in prompts and norm(v) not in norm(prompts)]
        if missing:
            issues.append(f"{name} ({facts.get(name, '?')}): not in any prompt: " + ", ".join(map(repr, missing)))
    return len(tests), issues


def main(ids):
    sys.stdout.reconfigure(encoding="utf-8")
    dirs = [HERE / i for i in ids] if ids else sorted(
        d for d in HERE.iterdir() if (d / "sessions.json").exists()
        and "facts" in json.loads((d / "sessions.json").read_text(encoding="utf8")))
    flagged = 0
    for d in dirs:
        n, issues = check(d)
        flagged += bool(issues)
        print(f"{d.name}: {n} fact tests, " + ("ok" if not issues else f"{len(issues)} flagged"))
        for i in issues:
            print("   ", i)
    print(f"{len(dirs)} projects, {flagged} with flags")


if __name__ == "__main__":
    main(sys.argv[1:])
