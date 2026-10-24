"""Rescores fact passes from each result.json's hidden results: a fact pass needs at least one test_fact
that ran and every one PASSED. (Before the run.mjs fix, a hidden-test collection error counted as a fact
pass.) Writes RUN_DIR/rescored.jsonl and leaves result.json as recorded.

    python rescore.py RUN_DIR
"""
import glob
import json
import os
import sys

run = sys.argv[1]
changed = 0
with open(os.path.join(run, "rescored.jsonl"), "w", encoding="utf8") as out:
    for f in sorted(glob.glob(os.path.join(run, "units", "*", "result.json"))):
        r = json.load(open(f, encoding="utf8"))
        facts = [v for k, v in r["hidden"]["results"].items() if k.startswith("test_fact")]
        fact = bool(facts) and all(v == "PASSED" for v in facts)
        changed += fact != r["factPassed"]
        out.write(json.dumps({k: r[k] for k in ("unit", "task", "kind", "cond", "rep", "success")} | {"factPassed": fact, "factPassedRecorded": r["factPassed"]}) + "\n")
print("fact passes changed:", changed)
