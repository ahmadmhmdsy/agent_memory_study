"""Counts provider HTTP 429 attempts in a run's calls logs over the last N minutes. steps.json never
records them (failed attempts are retried inside one step), so the calls logs are the only source.

    python watch429.py RUN_DIR [MINUTES]    prints "<count> <total attempts in window>"
"""
import glob
import json
import os
import sys
import time
from datetime import datetime

run, minutes = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 5
since = time.time() - minutes * 60
n429 = total = 0
for f in glob.glob(os.path.join(run, "units", "*", "s*.calls.json")):
    if os.path.getmtime(f) < since:
        continue
    try:
        log = json.load(open(f, encoding="utf8"))
    except (OSError, ValueError):
        continue  # being written
    for c in log:
        t = c.get("t")
        if not t or datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp() < since:
            continue
        total += 1
        n429 += c.get("status") == 429
print(n429, total)
