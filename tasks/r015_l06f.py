"""R-015 copy of L06 with its missing decision stated: L06f.

R-014's L06 hides test_fact_report_count (the summary's last line is "sensors: N"), but none of
its 8 prompts states that decision, so L06 cannot succeed (0/15 in R-014, 0/12 in the R-015
pilot). L06 stays frozen as R-014 ran it; L06f is L06 with the decision added to session 2,
next to the other summary-format decision. Everything else is copied unchanged.
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC, DST = HERE / "L06", HERE / "L06f"
DEC = "Design decision for this project: "

if DST.exists():
    shutil.move(str(DST), str(HERE / "_aside" / f"L06f_{DST.stat().st_mtime_ns}"))
shutil.copytree(SRC, DST)

p = DST / "sessions.json"
spec = json.loads(p.read_text(encoding="utf8"))
spec["id"] = "L06f"
s2 = spec["sessions"][1]
s2["prompt"] += (f"\n\n{DEC}the last line of the summary report is \"sensors: N\", where N is the "
                 "number of sensors that have readings, for example sensors: 2.")
s2["given"]["decisions"].append('The summary report ends with the line "sensors: N", N = number of sensors with readings.')
p.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf8")
print("L06f written")
