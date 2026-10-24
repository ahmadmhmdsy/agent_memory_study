"""Carrier per unit from session 1-2 code: 'note' = marker in a comment, docstring or prose text written
to the workspace; 'code' = marker only in executable code; '-' = none. final_answer/print/grep lines skipped."""
import collections, glob, json, os, re, sys
sys.argv = ["x", sys.argv[1]]
exec(open("leak.py", encoding="utf8").read().split("rows = []")[0])
SKIP = re.compile(r"final_answer\(|print\(|subprocess|grep|os\.walk|startswith\(")

def carrier(unit):
    kind = "-"
    for s in (1, 2):
        p = os.path.join(RUN, "units", unit, f"s{s}.steps.json")
        steps = json.load(open(p, encoding="utf8"))
        last = max((i for i, x in enumerate(steps) if x.get("kind") == "task"), default=-1)
        for x in steps[last + 1:]:
            c = x.get("codeAction") or ""
            if x.get("kind") != "action" or not c: continue
            if not re.search(r"open\(|write_text|\.write\(", c): continue  # must write a file
            inq = False
            for l in c.splitlines():
                q = l.count('"""') + l.count("'''")
                note = inq or q > 0 or l.lstrip().startswith(("#", "-", "*")) or "#" in l
                if q % 2: inq = not inq
                if SKIP.search(l) or not re.search(M[unit[:3]], l): continue
                if note: return "note"
                kind = "code"
    return kind

RS = {json.loads(l)["unit"]: json.loads(l)["factPassed"] for l in open(os.path.join(RUN, "rescored.jsonl"), encoding="utf8")}
rows = []
for f in sorted(glob.glob(os.path.join(RUN, "units", "*", "result.json"))):
    r = json.load(open(f, encoding="utf8"))
    rows.append(dict(task=r["task"], kind=r["kind"], cond=r["cond"], rep=r["rep"], carrier=carrier(r["unit"]), fact=RS[r["unit"]], success=r["success"]))
json.dump(rows, open("leak_rows.json", "w"))
for c in ["C0", "C1", "C2", "C2g", "C3"]:
    t = collections.Counter((x["carrier"], x["fact"]) for x in rows if x["cond"] == c)
    print(c, "  ".join(f"{k}: {t[(k,True)]}/{t[(k,True)]+t[(k,False)]}" for k in ["note", "code", "-"]))
print("C0:")
for task in sorted(M):
    print(task, " ".join(f"r{x['rep']}:{x['carrier'][0]}{'P' if x['fact'] else 'f'}" for x in rows if x["task"] == task and x["cond"] == "C0"))
