from parse import parse_lines
from stats import top_paths


def write_report(lines, path):
    recs = parse_lines(lines)
    with open(path, "w", encoding="utf8") as f:
        if recs:
            f.write(f"Log report {recs[0]['date']}\n")
        for p, c in top_paths(recs, len(recs)):
            f.write(f"{p}: {c} requests\n")
