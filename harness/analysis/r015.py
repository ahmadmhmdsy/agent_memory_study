"""R-015 pre-registered analysis: success, priced cost per success, speed, the screen drop rule.

Paired bootstrap over projects (each resample draws projects with replacement and keeps all
their repeats, so paths stay paired by project x repeat): 10,000 resamples, seed 15, 95%
percentile CIs. Success is the unit's success flag; cost is priced per session from its usage
block at the paid sibling's list price (input $0.30, output $1.20, cached $0.06 per 1M).

    python r015.py RUN_DIR [RUN_DIR ...] [--screen] [--tasks L05,L06f]

--screen applies the stage-1 drop rule and survivor cap. Units with a harness error or > 5%
failed provider attempts are listed as reruns and left out of the scores.
"""
import argparse
import collections
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

# dated list prices per token: MiniMax M3 (R-015, 2026-10-20) and LongCat-2.0 (R-013); --price picks one
PRICES = {"minimax": {"in": 0.30e-6, "out": 1.20e-6, "cached": 0.06e-6},
          "longcat": {"in": 0.30e-6, "out": 1.20e-6, "cached": 0.006e-6}}
PRICE = dict(PRICES["minimax"])
REFS = ["C0", "C2", "C3"]
DELTA = 5.0
CAP = 8
B, SEED = 10_000, 15
# session ends that are limits (scored as the task's result), not harness errors: step cap, and
# cancellation by the token budget or the session timeout
LIMITS = {"AgentMaxStepsError", "AgentCancelledError"}


def session_cost(run, unit, s):
    """(measured, no-cache, prefix-bound) dollars for one session."""
    u = s.get("usage") or {}
    p = u.get("prompt", (s.get("tokenUsage") or {}).get("inputTokens", 0))
    c = u.get("completion", (s.get("tokenUsage") or {}).get("outputTokens", 0))
    k = min(u.get("cached", 0), p)
    measured = (p - k) * PRICE["in"] + k * PRICE["cached"] + c * PRICE["out"]
    nocache = p * PRICE["in"] + c * PRICE["out"]
    # prefix bound: each call could at best reuse the previous call's whole prompt from cache
    f = pathlib.Path(run) / "units" / unit / f"s{s['session']}.calls.json"
    log = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    per = [x["prompt"] for x in log if x.get("ok") and x.get("prompt")]
    kb = sum(min(a, b) for a, b in zip(per, per[1:]))
    kb = min(kb, p)
    bound = (p - kb) * PRICE["in"] + kb * PRICE["cached"] + c * PRICE["out"]
    return measured, nocache, bound


def load(runs, tasks):
    rows, reruns = [], []
    for run in runs:
        for f in sorted(pathlib.Path(run).glob("units/*/result.json")):
            r = json.loads(f.read_text(encoding="utf-8"))
            if tasks and r["task"] not in tasks:
                continue
            ss = r["sessions"]
            att = sum((s.get("usage") or {}).get("calls", 0) for s in ss)
            fail = sum((s.get("usage") or {}).get("failedAttempts", 0) for s in ss)
            harness = [s["session"] for s in ss if s.get("state") == "error" and (s.get("failure") or {}).get("name")
                       not in LIMITS]
            if harness or (att and fail / (att + fail) > 0.05):
                reruns.append((r["unit"], f"harness error in s{harness}" if harness else f"{fail}/{att + fail} failed attempts"))
                continue
            cost = np.sum([session_cost(run, r["unit"], s) for s in ss], axis=0)
            rows.append(dict(task=r["task"], cond=r["cond"], rep=r["rep"], success=float(r["success"]),
                             fact=r.get("factScore") or 0.0, stale=r.get("staleErrors") or 0,
                             cost=cost[0], nocache=cost[1], bound=cost[2],
                             ms=sum(s.get("modelMs") or 0 for s in ss),
                             capped=sum((s.get("failure") or {}).get("name") == "AgentMaxStepsError" for s in ss),
                             budget=sum(bool(s.get("budgetHit")) for s in ss), n=len(ss)))
    return rows, reruns


def table(rows):
    """{cond: {task: arrays of per-unit success, cost, ms}} for bootstrap."""
    t = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for r in rows:
        for k in ("success", "cost", "ms"):
            t[r["cond"]][r["task"]][k].append(r[k])
    return t


def boot(t, conds, projects):
    """Per resample and path: success rate (pts), total cost, successes, model ms."""
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(projects), (B, len(projects)))
    out = {}
    for c in conds:
        # per project sums: successes, units, cost, ms
        m = np.array([[sum(t[c][p]["success"]), len(t[c][p]["success"]), sum(t[c][p]["cost"]), sum(t[c][p]["ms"])]
                      for p in projects])
        s = m[idx].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            out[c] = dict(succ=100 * s[:, 0] / s[:, 1], cps=np.where(s[:, 0] > 0, s[:, 2] / s[:, 0], np.inf),
                          mps=np.where(s[:, 0] > 0, s[:, 3] / s[:, 0], np.inf))
    return out


def ci(x):
    """95% percentile CI. A resample with no successes has infinite cost per success; it is kept
    (nearest-rank, so inf never interpolates) and only undefined ratios (inf / inf) are left out."""
    return np.nanpercentile(x, [2.5, 97.5], method="nearest")


def main():
    global SEED
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--screen", action="store_true")
    ap.add_argument("--tasks", default="")
    ap.add_argument("--price", choices=sorted(PRICES), default="minimax")
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()
    PRICE.update(PRICES[a.price]); SEED = a.seed
    sys.stdout.reconfigure(encoding="utf-8")
    rows, reruns = load(a.runs, set(filter(None, a.tasks.split(","))))
    t = table(rows)
    conds = sorted(t, key=lambda c: (c not in REFS, c))
    projects = sorted({r["task"] for r in rows})
    # pair only on projects every path has
    projects = [p for p in projects if all(p in t[c] for c in conds)]
    print(f"{len(rows)} units, {len(conds)} paths, {len(projects)} paired projects: {', '.join(projects)}")
    if reruns:
        print("reruns (left out):", "; ".join(f"{u} ({w})" for u, w in reruns))

    agg = {}
    for c in conds:
        rs = [r for r in rows if r["cond"] == c and r["task"] in projects]
        ns = sum(r["success"] for r in rs)
        g = lambda k: sum(r[k] for r in rs)
        agg[c] = dict(units=len(rs), succ=100 * ns / len(rs), ns=ns, fact=100 * np.mean([r["fact"] for r in rs]),
                      stale=g("stale"), capped=g("capped"), budget=g("budget"), sessions=g("n"),
                      cost=g("cost"), cps=g("cost") / ns if ns else np.inf, nc=g("nocache") / ns if ns else np.inf,
                      pb=g("bound") / ns if ns else np.inf, mps=g("ms") / ns / 1e3 if ns else np.inf,
                      fail_cost=sum(r["cost"] for r in rs if not r["success"]))
    bs = boot(t, conds, projects)
    best = max(conds, key=lambda c: agg[c]["succ"])

    print(f"\n{'path':6} {'units':>5} {'success':>8} {'CI95':>15} {'fact':>5} {'stale':>5} {'cap':>4} {'bud':>4}"
          f" {'$/succ':>8} {'CI95':>17} {'nocache':>8} {'prefix':>8} {'s/succ':>7} {'$fail':>7}")
    for c in sorted(conds, key=lambda c: agg[c]["cps"]):
        g = agg[c]; s, k = ci(bs[c]["succ"]), ci(bs[c]["cps"])
        print(f"{c:6} {g['units']:5} {g['succ']:7.1f}% [{s[0]:5.1f},{s[1]:5.1f}] {g['fact']:5.1f} {g['stale']:5}"
              f" {g['capped']:4} {g['budget']:4} {g['cps']:8.4f} [{k[0]:.4f},{k[1]:.4f}] {g['nc']:8.4f}"
              f" {g['pb']:8.4f} {g['mps']:7.1f} {g['fail_cost']:7.3f}")

    # ranking: acceptable = within delta of best success; cheapest wins; within 10% tied, speed breaks
    acc = [c for c in conds if agg[c]["succ"] >= agg[best]["succ"] - DELTA]
    rank = sorted(acc, key=lambda c: agg[c]["cps"])
    if rank:
        lo = agg[rank[0]]["cps"]
        tied = [c for c in rank if agg[c]["cps"] <= 1.10 * lo]
        win = min(tied, key=lambda c: agg[c]["mps"])
        print(f"\nbest success: {best} {agg[best]['succ']:.1f}%; acceptable (within {DELTA:g} pts): {', '.join(rank)}")
        print(f"cheapest-acceptable tie set (within 10%): {', '.join(tied)} -> winner by speed: {win}")
    front = [c for c in conds if not any(agg[q]["succ"] >= agg[c]["succ"] and agg[q]["cps"] <= agg[c]["cps"]
                                         and (agg[q]["succ"] > agg[c]["succ"] or agg[q]["cps"] < agg[c]["cps"]) for q in conds)]
    print("Pareto frontier (success vs $/success):", ", ".join(sorted(front, key=lambda c: agg[c]["cps"])))

    if not a.screen:
        return
    print("\nscreen drop rule (non-reference paths):")
    dropped = {}
    for p in conds:
        if p in REFS:
            continue
        d = ci(bs[p]["succ"] - bs[best]["succ"]) if p != best else None
        if d is not None and d[1] < -DELTA:
            dropped[p] = f"(a) success - {best} CI [{d[0]:+.1f},{d[1]:+.1f}] below -{DELTA:g}"
            continue
        for q in conds:
            if q == p or agg[q]["succ"] < agg[p]["succ"]:
                continue
            with np.errstate(divide="ignore", invalid="ignore"):
                r = ci(bs[p]["cps"] / bs[q]["cps"])
            if r[0] > 1:
                dropped[p] = f"(b) $/succ ratio vs {q} CI [{r[0]:.2f},{r[1]:.2f}] above 1"
                break
    for p, why in dropped.items():
        print(f"  drop {p}: {why}")
    surv = [c for c in conds if c not in dropped]
    print(f"  survivors ({len(surv)}): {', '.join(surv)}")
    if len(surv) > CAP:
        rest = sorted((c for c in surv if c not in REFS), key=lambda c: agg[c]["cps"])
        keep = REFS + rest[:CAP - len(REFS)]
        print(f"  survivor cap {CAP}: confirm {', '.join(keep)}; not dropped, not confirmed: {', '.join(rest[CAP - len(REFS):])}")


if __name__ == "__main__":
    main()
