# Per-call token usage from the step logs, the only complete source for R-013 and R-014.
# A session that ends in error (step cap, timeout) has tokenUsage null in sessions.jsonl and
# result.json, so totals from those files leave its calls out. The step log keeps every call.
# C3 logs start with the earlier sessions' steps, so a session's own calls are its last n actions.
# Usage: python harness/analysis/usage.py runs/r014_scored   (prints the check per condition)
import json
import pathlib
import sys


def calls(run_dir, unit, session, n):
    """[(input, output)] for one session's own model calls, oldest first."""
    f = pathlib.Path(run_dir) / "units" / unit / f"s{session}.steps.json"
    acts = [s["tokenUsage"] for s in json.loads(f.read_text(encoding="utf-8"))
            if s.get("kind") == "action" and s.get("tokenUsage")]
    return [(u["inputTokens"], u["outputTokens"]) for u in acts[-n:]] if n else []


def unit_tokens(run_dir, result):
    """(input, output) for a whole unit, every session counted, from a result.json dict."""
    i = o = 0
    for s in result["sessions"]:
        for a, b in calls(run_dir, result["unit"], s["session"], s["actionSteps"]):
            i, o = i + a, o + b
    return i, o


if __name__ == "__main__":
    run = pathlib.Path(sys.argv[1])
    agg = {}
    for p in sorted(run.glob("units/*/result.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        a = agg.setdefault(r["cond"], [0, 0, 0, 0])
        for s in r["sessions"]:
            c = calls(run, r["unit"], s["session"], s["actionSteps"])
            if s.get("tokenUsage"):
                a[0] += sum(x for x, _ in c)
                a[1] += s["tokenUsage"]["inputTokens"]
            else:
                a[2] += 1
                a[3] += sum(x + y for x, y in c)
    for c, (log, rec, nerr, errtok) in sorted(agg.items()):
        print(f"{c:4} sessions with a total: log/recorded input {100 * log / rec:.2f}%;"
              f" {nerr} sessions without a total carry {errtok / 1e6:.2f}M tokens")
