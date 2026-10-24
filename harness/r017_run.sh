#!/usr/bin/env bash
# R-017 runner: LongCat, standard arm, with a quota watcher. Stops the run on sustained 429s
# (> 20 in the last 15 min of calls logs; logs are written at session end, so the lag is one session).
#   bash harness/r017_run.sh OUT TASKS CONDS REPS CONCURRENCY
set -u
OUT=$1 TASKS=$2 CONDS=$3 REPS=$4 CONC=$5
node harness/sweep.mjs
R013_MODEL=longcat-2.5-preview-free node harness/run.mjs --out "$OUT" --tasks "$TASKS" --conds "$CONDS" \
  --reps "$REPS" --max-steps 20 --concurrency "$CONC" > "$OUT.log" 2>&1 &
RUNNER=$!
while kill -0 $RUNNER 2>/dev/null; do
  sleep 120
  read -r n total < <(python harness/watch429.py "$OUT" 15)
  if [ "${n:-0}" -gt 20 ]; then
    echo "$(date -u +%FT%TZ) quota stop: $n of $total attempts were 429" | tee -a "$OUT.log"
    powershell -NoProfile -Command "Get-CimInstance Win32_Process | ? { \$_.CommandLine -match 'run.mjs' -and \$_.CommandLine -match '$(basename "$OUT")' } | % { Stop-Process -Id \$_.ProcessId -Force }"
    break
  fi
done
wait $RUNNER 2>/dev/null
node harness/sweep.mjs
echo "results: $(ls "$OUT"/units/*/result.json 2>/dev/null | wc -l)"
