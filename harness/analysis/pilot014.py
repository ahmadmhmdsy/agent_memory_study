"""R-014 pilot summary: fact score, stale errors, success and tokens per condition; per-fact
pass table; step cap and code-step share for the pilot rules. Usage: python pilot014.py RUN_DIR"""
import collections
import glob
import json
import os
import sys

RUN = sys.argv[1]
CONDS = ["C0", "C1", "C2", "C2g", "C3"]
units = [json.load(open(f, encoding="utf8")) for f in sorted(glob.glob(os.path.join(RUN, "units", "*", "result.json")))]
by = collections.defaultdict(list)
for u in units:
    by[u["cond"]].append(u)


def tok(u, k):
    return sum((s.get("tokenUsage") or {}).get(k, 0) for s in u["sessions"])


print(f"{len(units)} units")
print("cond  n  factScore  stale  success  in_k/unit  out_k/unit")
for c in CONDS:
    us = by[c]
    if not us:
        continue
    n = len(us)
    print(f"{c:4} {n:2}  {100 * sum(u['factScore'] for u in us) / n:8.1f}  {sum(u['staleErrors'] for u in us):5}"
          f"  {sum(u['success'] for u in us):3}/{n}  {sum(tok(u, 'inputTokens') for u in us) / n / 1e3:9.1f}"
          f"  {sum(tok(u, 'outputTokens') for u in us) / n / 1e3:9.1f}")

print("\nper fact test (task: cond results, P = pass)")
for task in sorted({u["task"] for u in units}):
    names = sorted(n for n in next(u for u in units if u["task"] == task)["hidden"]["results"]
                   if n.startswith(("test_fact", "test_stale")))
    for n in names:
        row = " ".join(f"{c}:{'P' if u['hidden']['results'].get(n) == 'PASSED' else '-'}"
                       for c in CONDS for u in by[c] if u["task"] == task)
        print(f"  {task} {n:28} {row}")

steps = sorted(s["actionSteps"] for u in units for s in u["sessions"] if s["state"] == "success")
allsteps = [s for u in units for s in u["sessions"]]
code = sum(s["stepsWithCode"] for s in allsteps) / max(1, sum(s["actionSteps"] for s in allsteps))
p90 = steps[int(0.9 * (len(steps) - 1))] if steps else None
print(f"\nsessions {len(allsteps)}, finished {len(steps)}, p90 steps {p90}, max {steps[-1] if steps else None}")
print(f"steps with code {100 * code:.1f}%; provider errors {sum(len(s['providerErrors']) for s in allsteps)}")
print(f"states {collections.Counter(s['state'] for s in allsteps)}")
tin = sum(tok(u, "inputTokens") for u in units)
tout = sum(tok(u, "outputTokens") for u in units)
print(f"total tokens: in {tin / 1e6:.2f}M, out {tout / 1e6:.3f}M; x12 for 240 units: in {12 * tin / 1e6:.1f}M, out {12 * tout / 1e6:.2f}M")
