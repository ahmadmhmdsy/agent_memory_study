import re

PAT = re.compile(r"(\d{4}-\d\d-\d\d) (\d\d):(\d\d):(\d\d) (\w+) (\w+) (\S+) (\d{3}) (\d+(?:\.\d+)?)(ms|s)")


def parse_line(line):
    m = PAT.fullmatch(line.strip())
    if not m:
        raise ValueError("malformed line")
    d, h, mi, s, level, method, path, status, num, unit = m.groups()
    return {"date": d, "time": f"{h}:{mi}:{s}", "hour": int(h), "level": level,
            "method": method.upper(), "path": path, "status": int(status),
            "ms": int(round(float(num) * (1000 if unit == "s" else 1)))}


def parse_lines(lines):
    out = []
    for l in lines:
        try:
            out.append(parse_line(l))
        except ValueError:
            pass
    return out
