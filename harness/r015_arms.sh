#!/usr/bin/env bash
# R-015 stage 3: limited then near-unlimited arm on the finalists, MiniMax, with the r017_run.sh quota watcher.
#   bash harness/r015_arms.sh CONDS CONCURRENCY
set -u
CONDS=$1 CONC=$2
T=$(echo T{01..16}|tr ' ' ,); L=$(echo L05 L06f L07 L08 L09 L10f L{11..20}|tr ' ' ,); A=$(echo A{01..16}|tr ' ' ,)
run_arm() {  # OUT then extra run.mjs args
  local OUT=$1; shift
  node harness/sweep.mjs
  R013_MODEL=minimax-m3.1-flash-free node harness/run.mjs --out "$OUT" --tasks "$T,$L,$A" --conds "$CONDS" \
    --reps 3 --concurrency "$CONC" "$@" >> "$OUT.log" 2>&1 &
  local RUNNER=$!
  while kill -0 $RUNNER 2>/dev/null; do
    sleep 120
    read -r n total < <(python harness/watch429.py "$OUT" 15)
    if [ "${n:-0}" -gt 20 ]; then
      echo "$(date -u +%FT%TZ) quota stop: $n of $total attempts were 429" | tee -a "$OUT.log"
      powershell -NoProfile -Command "Get-CimInstance Win32_Process | ? { \$_.CommandLine -match 'run.mjs' -and \$_.CommandLine -match '$(basename "$OUT")' } | % { Stop-Process -Id \$_.ProcessId -Force }"
      wait $RUNNER 2>/dev/null; node harness/sweep.mjs; return 1
    fi
  done
  wait $RUNNER 2>/dev/null
  node harness/sweep.mjs
  echo "$OUT results: $(ls "$OUT"/units/*/result.json 2>/dev/null | wc -l)"
}
run_arm runs/r015_lim --max-steps 8 --token-budget 78000 || exit 1
run_arm runs/r015_unlim --max-steps 60 --session-minutes 135 || exit 1
