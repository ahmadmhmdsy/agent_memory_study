# Dollar cost and wall time per unit for R-013 and R-014, at the list prices of the paid sibling models.
# The runs used free models and the library drops cached_tokens, so caching is modelled from the
# per-call input counts in the step logs: "none" pays every input token at the input price; "prefix"
# assumes each call reuses the previous call's whole prompt in the same session (the agent's memory
# only appends), which is the best a prefix cache can do. The first call of a session pays in full.
# Usage: python harness/analysis/cost.py
import json
import pathlib
import statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[2] / "runs"
# $ per 1M tokens (input, output, cached read), OpenCode Go table, 2026-10-20.
PRICES = {"R-013 (LongCat-2.0 prices)": (0.30, 1.20, 0.006), "R-014 (MiniMax M3 prices)": (0.30, 1.20, 0.06)}
RUNS = {"R-013 (LongCat-2.0 prices)": ("scored", "rescored.jsonl"), "R-014 (MiniMax M3 prices)": ("r014_scored", None)}
CONDS = ["C0", "C1", "C2", "C2g", "C3"]


def session_calls(steps_file, n):
    """Per-call (input, output) for the session's own calls; C3 logs carry earlier sessions first."""
    acts = [s["tokenUsage"] for s in json.loads(steps_file.read_text(encoding="utf-8")) if s.get("kind") == "action" and s.get("tokenUsage")]
    return [(u["inputTokens"], u["outputTokens"]) for u in acts[-n:]] if n else []


def cost(calls, p_in, p_out, p_cache):
    none = sum(i * p_in + o * p_out for i, o in calls) / 1e6
    pref, prev = 0.0, 0
    for i, o in calls:
        c = min(prev, i)
        pref += ((i - c) * p_in + c * p_cache + o * p_out) / 1e6
        prev = i
    return none, pref


for run, (folder, scorefile) in RUNS.items():
    p_in, p_out, p_cache = PRICES[run]
    d = ROOT / folder
    sessions = {}
    for line in (d / "sessions.jsonl").read_text(encoding="utf-8").splitlines():
        s = json.loads(line)
        sessions.setdefault(s["unit"], {})[s["session"]] = s  # last record per session wins
    if scorefile:
        success = {r["unit"]: r["success"] for r in map(json.loads, (d / scorefile).read_text(encoding="utf-8").splitlines())}
    else:
        success = {p.parent.name: json.loads(p.read_text(encoding="utf-8"))["success"] for p in d.glob("units/*/result.json")}
    rows, check = {c: [] for c in CONDS}, [0, 0]
    for unit, ok in success.items():
        cond = unit.split("_")[1]
        none = pref = wall = model = tin = logtok = errs = 0.0
        for k, s in sorted(sessions.get(unit, {}).items()):
            calls = session_calls(d / "units" / unit / f"s{k}.steps.json", s["actionSteps"])
            a, b = cost(calls, p_in, p_out, p_cache)
            none, pref = none + a, pref + b
            wall += s["wallMs"] / 1000
            model += s["modelMs"] / 1000
            tin += (s["tokenUsage"] or {}).get("inputTokens", 0)
            logtok += sum(i + o for i, o in calls)
            errs += s["state"] != "success"
            check[0] += sum(i for i, _ in calls)
            check[1] += (s["tokenUsage"] or {}).get("inputTokens", 0)
        rows[cond].append((ok, none, pref, wall, model, tin, logtok, errs))
    print(f"\n{run}: {sum(len(v) for v in rows.values())} units; step-log input covers "
          f"{100 * check[0] / max(check[1], 1):.1f}% of session input")
    print("cond  succ%  $/unit none  $/unit prefix  cache%  $/success none  $/success prefix  "
          "wall s/unit  model s/unit  wall s/success  tok k/unit (logs)  error sessions/unit")
    for c in CONDS:
        r = rows[c]
        if not r:
            continue
        n_ok = sum(x[0] for x in r)
        tot = [sum(x[i] for x in r) for i in range(1, 8)]
        saved = 1 - tot[1] / tot[0]
        per = lambda v: f"{v / n_ok:.4f}" if n_ok else "   -  "
        print(f"{c:4}  {100 * n_ok / len(r):5.1f}  {tot[0] / len(r):11.4f}  {tot[1] / len(r):13.4f}  "
              f"{100 * saved:5.1f}  {per(tot[0]):>15}  {per(tot[1]):>16}  {tot[2] / len(r):11.0f}  "
              f"{tot[3] / len(r):12.0f}  {(f'{tot[2] / n_ok:.0f}' if n_ok else '-'):>14}  {tot[5] / len(r) / 1e3:17.0f}  {tot[6] / len(r):19.2f}")
    print("median wall s/unit:", {c: round(st.median(x[3] for x in rows[c])) for c in CONDS if rows[c]})
