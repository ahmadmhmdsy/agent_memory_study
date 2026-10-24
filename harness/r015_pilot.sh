#!/usr/bin/env bash
# R-015 pilot: the standard arm (step cap 20, no token budget), then the limited arm
# (step cap 8, per-session token budget = half the standard arm's p90 session tokens).
set -u
cd "$(dirname "$0")/.."
export R013_MODEL=minimax-m3.1-flash-free
TASKS=T01,T02,L05,L06,A01,A02
CONDS=C0,C1,C1t,C2,C2-t,C2-h,C2-d,C2a,C2x,C3,C3c,C4
node harness/run.mjs --out runs/r015_pilot_std --tasks $TASKS --conds $CONDS --reps 1 --max-steps 20 --concurrency 72
BUDGET=$(python - <<'EOF'
import glob, json
v = sorted(s["usage"]["prompt"] + s["usage"]["completion"]
           for f in glob.glob("runs/r015_pilot_std/units/*/result.json")
           for s in json.load(open(f, encoding="utf8"))["sessions"] if s.get("usage"))
print(round(v[int(.9 * len(v))] / 2 / 1000) * 1000)
EOF
)
echo "limited-arm token budget: $BUDGET" | tee runs/r015_pilot_budget.txt
node harness/run.mjs --out runs/r015_pilot_lim --tasks $TASKS --conds $CONDS --reps 1 --max-steps 8 --token-budget "$BUDGET" --concurrency 72
echo pilot-done
