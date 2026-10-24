"""R-013 pre-registered test: H1-H5 on task success (per-task mean over repeats, paired by task),
one-sided Wilcoxon for H1-H3/H5, two-sided for H4, Holm over H1-H5, paired bootstrap 95% CIs.
Also reported: cost per success, how often C1/C2/C2g sessions 1-2 skip writing memory.

    python prereg.py RUN_DIR
"""
import collections, glob, json, os, re, sys
import numpy as np
from scipy.stats import wilcoxon

RUN = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(RUN, "rescored.jsonl"), encoding="utf8")]
C = ["C0", "C1", "C2", "C2g", "C3"]
rng = np.random.default_rng(0)

def per_task(cond, metric, keep=lambda r: True):
    d = collections.defaultdict(list)
    for r in rows:
        if r["cond"] == cond and keep(r): d[r["task"]].append(float(r[metric]))
    return {t: np.mean(v) for t, v in d.items()}

def diff(a, b, metric="success", keep=lambda r: True):
    A, B = per_task(a, metric, keep), per_task(b, metric, keep)
    ts = sorted(A); return np.array([A[t] - B[t] for t in ts])

def ci(d):
    bs = rng.choice(d, (10000, len(d))).mean(1); return np.percentile(bs, [2.5, 97.5])

H = [("H1", "C2", "C0", 15, "greater", "success"), ("H2", "C2", "C1", 10, "greater", "success"),
     ("H3", "C1", "C2", 0, "greater", "violation"), ("H4", "C2", "C3", None, "two-sided", "success"),
     ("H5", "C2g", "C2", 0, "greater", "success")]
for r in rows: r["violation"] = float(r["kind"] == "constraint" and not r["factPassed"])
out = []
for name, a, b, thr, alt, metric in H:
    keep = (lambda r: r["kind"] == "constraint") if metric == "violation" else (lambda r: True)
    d = diff(a, b, metric, keep); nz = d[d != 0]
    p = wilcoxon(nz, alternative=alt).pvalue if len(nz) else 1.0
    out.append([name, a, b, thr, alt, metric, 100 * d.mean(), 100 * ci(d), p, len(d), int((d > 0).sum()), int((d < 0).sum())])
order = sorted(range(len(out)), key=lambda i: out[i][8]); m = len(out); run_max = 0
for rank, i in enumerate(order):
    run_max = max(run_max, min(1.0, out[i][8] * (m - rank))); out[i].append(run_max)
for name, a, b, thr, alt, metric, dm, c, p, n, pos, neg, ph in out:
    lab = f"{a}-{b}" if metric == "success" else f"violations {a}-{b}"
    verdict = "reported" if thr is None else ("PASS" if ph < 0.05 and dm >= thr and dm > 0 else "fail")
    print(f"{name} {lab}: {dm:+.1f} pts CI95 [{c[0]:+.1f},{c[1]:+.1f}] n={n} +{pos}/-{neg} p={p:.2g} p_holm={ph:.2g} -> {verdict}")

# cost per success: total model tokens / successes, by condition. Tokens come from the step logs
# (2026-10-20 correction): sessions that end in error have no recorded total.
sys.path.insert(0, os.path.dirname(__file__))
from usage import unit_tokens
tok = collections.defaultdict(lambda: [0, 0])
for f in glob.glob(os.path.join(RUN, "units", "*", "result.json")):
    u = json.load(open(f, encoding="utf8")); i, o = unit_tokens(RUN, u)
    tok[u["cond"]][0] += i; tok[u["cond"]][1] += o
succ = collections.Counter(r["cond"] for r in rows if r["success"])
print("tokens per success (k in / k out):", {c: f"{tok[c][0]/succ[c]/1e3:.0f}/{tok[c][1]/succ[c]/1e3:.1f}" for c in C})

# memory skipped: session 1 or 2 whose code never writes the memory file(s)
MEM = {"C1": r"NOTES\.md", "C2": r"(AGENTS\.md|docs/)", "C2g": r"(AGENTS\.md|docs/)"}
skip = collections.Counter(); tot = collections.Counter()
for f in glob.glob(os.path.join(RUN, "units", "*", "s[12].steps.json")):
    unit = os.path.basename(os.path.dirname(f)); cond = unit.split("_")[1]
    if cond not in MEM: continue
    wrote = any(re.search(MEM[cond], x.get("codeAction") or "") and re.search(r"open\([^)]*['\"][wa]|write_text|\.write\(", x.get("codeAction") or "")
                for x in json.load(open(f, encoding="utf8")) if x.get("kind") == "action")
    tot[cond] += 1; skip[cond] += not wrote
print("sessions 1-2 that never write memory:", {c: f"{skip[c]}/{tot[c]}" for c in MEM})
