import json, collections, numpy as np
from scipy.stats import binomtest, wilcoxon
rows = json.load(open("leak_rows.json"))
C = ["C0", "C1", "C2", "C2g", "C3"]
rng = np.random.default_rng(0)
def rate(rs): return 100 * sum(x["fact"] for x in rs) / len(rs) if rs else float("nan")
print("fact % (rescored):", {c: round(rate([x for x in rows if x["cond"] == c]), 1) for c in C})
print("by kind:", {k: {c: round(rate([x for x in rows if x["cond"] == c and x["kind"] == k]), 1) for c in C} for k in ["constraint", "decision", "unfinished"]})
def per_task(cond, keep=lambda x: True, metric="fact"):
    d = collections.defaultdict(list)
    for x in rows:
        if x["cond"] == cond and keep(x): d[x["task"]].append(x[metric])
    return {t: np.mean(v) for t, v in d.items()}
def compare(a, b, keep_a=lambda x: True, label="", metric="fact"):
    A, B = per_task(a, metric=metric), per_task(b, keep_a, metric)
    ts = sorted(set(A) & set(B)); d = np.array([A[t] - B[t] for t in ts])
    pos, neg = int((d > 0).sum()), int((d < 0).sum())
    ps = binomtest(pos, pos + neg).pvalue if pos + neg else 1.0
    pw = wilcoxon(d[d != 0]).pvalue if (d != 0).sum() else 1.0
    bs = [rng.choice(d, len(d)).mean() for _ in range(10000)]
    print(f"{label}{a} vs {b} [{metric}] n={len(ts)} diff={d.mean():+.3f} CI95=[{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}] +{pos}/-{neg} sign p={ps:.2g} wilcoxon p={pw:.2g}")
    return pw
print("\n-- vs C0, all tasks")
for c in C[1:]: compare(c, "C0")
for c in C[1:]: compare(c, "C0", metric="success")
print("\n-- vs C0 with self-written carriers counted as fails (C0 note/code units -> fact False)")
orig = {id(x): x["fact"] for x in rows}
for x in rows:
    if x["cond"] == "C0" and x["carrier"] != "-": x["fact"] = False
for c in C[1:]: compare(c, "C0")
for x in rows: x["fact"] = orig[id(x)]
print("\n-- among memory conditions (Holm over 6)")
ps = []
for a, b in [("C2g","C1"),("C2g","C2"),("C2g","C3"),("C2","C1"),("C3","C1"),("C2","C3")]:
    ps.append(((a,b), compare(a, b)))
ps.sort(key=lambda p: p[1]); m = len(ps)
print("Holm:", [(f"{a}-{b}", round(min(1, p * (m - i)), 3)) for i, ((a, b), p) in enumerate(ps)])
