"""R-015 copy of L10 with its slug finishing step stated in full: L10f.

R-014's L10 hides test_fact_slug_clean, which also needs slug("  Jazz   Night ") == "jazz-night",
but session 5's deferred step only asks to remove punctuation and collapse hyphens; no prompt
says that leading and trailing spaces are dropped (1/12 passes in the R-015 pilot). L10 stays
frozen as R-014 ran it; L10f is L10 with the trimming added to that deferred step. Everything
else is copied unchanged.
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC, DST = HERE / "L10", HERE / "L10f"
OLD = 'runs of hyphens become one ("Rock & Roll!" becomes "rock-roll").'
NEW = ('runs of hyphens become one ("Rock & Roll!" becomes "rock-roll"), and leading and trailing '
       'spaces and hyphens are dropped ("  Jazz   Night " becomes "jazz-night").')

if DST.exists():
    shutil.move(str(DST), str(HERE / "_aside" / f"L10f_{DST.stat().st_mtime_ns}"))
shutil.copytree(SRC, DST)

p = DST / "sessions.json"
spec = json.loads(p.read_text(encoding="utf8"))
spec["id"] = "L10f"
s5 = spec["sessions"][4]
assert s5["prompt"].count(OLD) == 1
s5["prompt"] = s5["prompt"].replace(OLD, NEW)
g = s5["given"]
g["tasks"][1]["task"] = "slug: remove punctuation, collapse hyphens, trim ends"
g["handoff"] = g["handoff"].replace("collapse hyphens.", "collapse hyphens, drop leading and trailing spaces and hyphens.")
p.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf8")
print("L10f written")
