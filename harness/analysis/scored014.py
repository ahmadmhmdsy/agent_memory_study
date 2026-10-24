"""R-014 scored analysis (amended plan, 2026-10-20). Usage: python scored014.py RUN_DIR
Primary: P1a-d (C1/C2/C2g/C3 - C0 fact score >= 20 points), P2 (C2 stale < C1), P3 (C2 tokens < C1);
one-sided Wilcoxon signed-rank on per-project means over repeats (n = 16), Holm over all six.
Reported, not gated: H1, H3, H4, stale vs C0, by fact kind, tokens/steps, C0 self-note rate."""
import collections
import glob
import json
import os
import re
import sys

import numpy as np
from scipy.stats import wilcoxon

sys.path.insert(0, os.path.dirname(__file__))
from usage import unit_tokens  # noqa: E402

RUN = sys.argv[1]
TASKS = os.path.join(os.path.dirname(__file__), "..", "..", "tasks")
CONDS = ["C0", "C1", "C2", "C2g", "C3"]
rng = np.random.default_rng(0)
units = [json.load(open(f, encoding="utf8")) for f in sorted(glob.glob(os.path.join(RUN, "units", "*", "result.json")))]
KINDS = {t: json.load(open(os.path.join(TASKS, t, "sessions.json"), encoding="utf8"))["facts"]
         for t in sorted({u["task"] for u in units})}


def tok(u):
    # From the step logs (2026-10-20 correction): sessions that end in error have no recorded total.
    return sum(unit_tokens(RUN, u))


def metric(u, m):
    return {"fact": 100 * u["factScore"], "stale": u["staleErrors"], "tokens": tok(u),
            "steps": sum(s["actionSteps"] for s in u["sessions"]), "success": 100 * u["success"]}[m]


def per_task(cond, m):
    d = collections.defaultdict(list)
    for u in units:
        if u["cond"] == cond:
            d[u["task"]].append(metric(u, m))
    return {t: float(np.mean(v)) for t, v in d.items()}


def paired(a, b, m):
    A, B = per_task(a, m), per_task(b, m)
    ts = sorted(set(A) & set(B))
    return np.array([A[t] - B[t] for t in ts])


def boot(d):
    bs = [rng.choice(d, len(d)).mean() for _ in range(10000)]
    return np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def one_sided(d, alt, shift=0.0):
    x = d - shift
    if not (x != 0).any():
        return 1.0
    return float(wilcoxon(x[x != 0], alternative=alt).pvalue)


print(f"{len(units)} units; per condition: {dict(collections.Counter(u['cond'] for u in units))}")
print("\ncond  fact%  stale/unit  success%  tokens_k/unit  steps/unit")
for c in CONDS:
    us = [u for u in units if u["cond"] == c]
    if us:
        print(f"{c:4} {np.mean([metric(u, 'fact') for u in us]):6.1f}  {np.mean([u['staleErrors'] for u in us]):9.2f}"
              f"  {np.mean([metric(u, 'success') for u in us]):7.1f}  {np.mean([tok(u) for u in us]) / 1e3:12.0f}"
              f"  {np.mean([metric(u, 'steps') for u in us]):9.1f}")

# primary tests: (name, a, b, metric, alternative, threshold check on observed mean diff a-b)
tests = [(f"P1{x} {c}-C0 fact >= 20", c, "C0", "fact", "greater", lambda m: m >= 20)
         for x, c in zip("abcd", ["C1", "C2", "C2g", "C3"])]
tests += [("P2 C2 stale < C1", "C2", "C1", "stale", "less", lambda m: m < 0),
          ("P3 C2 tokens < C1", "C2", "C1", "tokens", "less", lambda m: m < 0)]
rows = []
for name, a, b, m, alt, ok in tests:
    d = paired(a, b, m)
    rows.append([name, d, one_sided(d, alt), ok(d.mean())])
order = np.argsort([r[2] for r in rows])
k, run_max = len(rows), 0.0
for i, j in enumerate(order):
    run_max = max(run_max, min(1.0, (k - i) * rows[j][2]))
    rows[j].append(run_max)
print("\nprimary (one-sided Wilcoxon, Holm over 6; pass = p_holm < 0.05 and threshold met)")
for name, d, p, ok, ph in rows:
    lo, hi = boot(d)
    print(f"  {name:24} n={len(d)} diff={d.mean():+10.2f} CI95=[{lo:+.2f},{hi:+.2f}] p={p:.3g} p_holm={ph:.3g}"
          f" threshold={'met' if ok else 'not met'} -> {'PASS' if ph < 0.05 and ok else 'fail'}")

print("\nreported, not gated")
d = paired("C2", "C1", "fact")
print(f"  H1 C2-C1 fact >= 10: diff={d.mean():+.2f} CI95=[{boot(d)[0]:+.2f},{boot(d)[1]:+.2f}] p={one_sided(d, 'greater'):.3g}")
d = paired("C2", "C3", "fact")
tr = np.mean([tok(u) for u in units if u["cond"] == "C2"]) / max(1, np.mean([tok(u) for u in units if u["cond"] == "C3"]))
print(f"  H3 C2-C3 fact > -5: diff={d.mean():+.2f} CI95=[{boot(d)[0]:+.2f},{boot(d)[1]:+.2f}]"
      f" p={one_sided(d, 'greater', -5):.3g}; C2/C3 tokens={tr:.2f} (need < 0.6)")
d = paired("C2g", "C2", "fact")
print(f"  H4 C2g-C2 fact > 0: diff={d.mean():+.2f} CI95=[{boot(d)[0]:+.2f},{boot(d)[1]:+.2f}] p={one_sided(d, 'greater'):.3g}")
for c in CONDS[1:]:
    d = paired(c, "C0", "stale")
    print(f"  stale {c}-C0: diff={d.mean():+.2f} CI95=[{boot(d)[0]:+.2f},{boot(d)[1]:+.2f}] p(less)={one_sided(d, 'less'):.3g}")
for c in CONDS[1:]:
    d = paired(c, "C0", "tokens") / 1e3
    print(f"  tokens_k {c}-C0: diff={d.mean():+.0f} CI95=[{boot(d)[0]:+.0f},{boot(d)[1]:+.0f}]")

print("\nfact pass % by kind (stale = % of stale tests that pass, lower is better)")
kinds = ["superseded", "unfinished", "constraint", "decision"]
print("cond  " + "  ".join(f"{k[:10]:>10}" for k in kinds) + "       stale")
for c in CONDS:
    tally = collections.defaultdict(list)
    for u in units:
        if u["cond"] != c:
            continue
        for n, r in u["hidden"]["results"].items():
            if n.startswith("test_fact_"):
                tally[KINDS[u["task"]].get(n[len("test_fact_"):], "?")].append(r == "PASSED")
            elif n.startswith("test_stale"):
                tally["stale"].append(r == "PASSED")
    print(f"{c:4}  " + "  ".join(f"{100 * np.mean(tally[k]) if tally[k] else float('nan'):10.1f}" for k in kinds + ["stale"]))
unk = {n for u in units for n in u["hidden"]["results"] if n.startswith("test_fact_")
       and n[len("test_fact_"):] not in KINDS[u["task"]]}
if unk:
    print(f"  fact tests without a kind: {sorted(unk)}")

# C0 self-note heuristic: an action writes a non-.py file (notes, md, txt, json) into the workspace
NOTE = re.compile(r"""(open\(\s*['"][^'"]+\.(md|txt|json|ya?ml|ini|cfg)['"]\s*,\s*['"][wa])|"""
                  r"""(Path\(\s*['"][^'"]+\.(md|txt|json|ya?ml)['"]\s*\)\.write_text)""")
c0 = [u for u in units if u["cond"] == "C0"]
noted = 0
for u in c0:
    hit = False
    for s in range(1, 8):
        p = os.path.join(RUN, "units", u["unit"], f"s{s}.steps.json")
        if os.path.exists(p) and any(x.get("kind") == "action" and NOTE.search(x.get("codeAction") or "")
                                     for x in json.load(open(p, encoding="utf8"))):
            hit = True
            break
    noted += hit
print(f"\nC0 self-note rate (heuristic, sessions 1-7 write a non-.py file): {noted}/{len(c0)}")

allsess = [s for u in units for s in u["sessions"]]
fin = sorted(s["actionSteps"] for s in allsess if s["state"] == "success")
print(f"\nsessions {len(allsess)}; states {dict(collections.Counter(s['state'] for s in allsess))}")
print(f"steps p90 {fin[int(0.9 * (len(fin) - 1))] if fin else None}, max {fin[-1] if fin else None}; "
      f"code steps {100 * sum(s['stepsWithCode'] for s in allsess) / max(1, sum(s['actionSteps'] for s in allsess)):.1f}%; "
      f"provider errors {sum(len(s['providerErrors']) for s in allsess)}")
print(f"total tokens {sum(tok(u) for u in units) / 1e6:.1f}M")
