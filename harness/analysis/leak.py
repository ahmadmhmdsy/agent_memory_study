"""Per unit: did session 1-2 code write a fact-specific marker into the workspace (any file)?
Fact rate by condition, split by carrier yes/no."""
import collections, glob, json, os, re, sys

RUN = sys.argv[1]
# Fact-specific markers (spec details, not just names).
M = {
    "S01": r"DD/MM/YYYY|%d/%m/%Y", "S02": r"(?i)descending|reverse=True", "S03": r"(?i)never raise|must not raise|not raise|return None",
    "S04": r"(?i)built-?in|not a subclass|InventoryError\(Exception\)", "S05": r"(?i)fraction|0-1|0\.\.1|4 (decimal|places)|four", "S06": r"(?i)Y/N|'Y'|\"Y\"",
    "S07": r"(?i)lowercase|lower-case|'\.'|\"\.\"", "S08": r"(?i)kelvin|273\.15", "S09": r"(?i)\bLFU\b|least.frequently",
    "S10": r"(?i)0-based|zero-based|start at 0|start from 0|page 0", "S11": r"(?i)underscore", "S12": r"(?i)semicolon|delimiter=';'|delimiter=\";\"|\";\"\.join|';'\.join",
    "S13": r"(?i)\bUTC\b|%SZ", "S14": r"T0001|T%04d|:04d", "S15": r"(?i)case.insensitive|ignor\w* case", "S16": r"(?i)truncat",
    "S17": r"(?i)peek", "S18": r"(?i)truncate|…|\\u2026", "S19": r"(?i)\bletter\b", "S20": r"(?i)low_stock",
    "S21": r"(?i)to_seconds", "S22": r"(?i)query_params", "S23": r"(?i)statement", "S24": r"(?i)rare_words",
}


def code(unit, s):
    p = os.path.join(RUN, "units", unit, f"s{s}.steps.json")
    steps = json.load(open(p, encoding="utf8"))
    last = max((i for i, x in enumerate(steps) if x.get("kind") == "task"), default=-1)
    return "\n".join(x.get("codeAction") or "" for x in steps[last + 1:] if x.get("kind") == "action")


rows = []
for f in sorted(glob.glob(os.path.join(RUN, "units", "*", "result.json"))):
    r = json.load(open(f, encoding="utf8"))
    u = r["unit"]
    text = code(u, 1) + "\n" + code(u, 2)
    rows.append((r["task"], r["kind"], r["cond"], r["rep"], bool(re.search(M[r["task"]], text)), r["factPassed"], r["success"]))
json.dump(rows, open(os.path.join(os.path.dirname(__file__), "leak_rows.json"), "w"))

t = collections.Counter((c, k, fp) for _, _, c, _, k, fp, _ in rows)
for c in ["C0", "C1", "C2", "C2g", "C3"]:
    cy, py = t[(c, True, True)] + t[(c, True, False)], t[(c, True, True)]
    cn, pn = t[(c, False, True)] + t[(c, False, False)], t[(c, False, True)]
    print(f"{c}: marker {cy} units, fact {py}/{cy}; no marker {cn} units, fact {pn}/{cn}")
print("C0 per task (rep: marker/fact):")
for task in sorted(M):
    print(task, " ".join(f"r{rep}:{'M' if k else '-'}{'P' if fp else 'f'}" for tk, _, c, rep, k, fp, _ in rows if tk == task and c == "C0"))
