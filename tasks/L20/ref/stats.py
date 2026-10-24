def _path(r):
    return r["path"].split("?")[0]


def _live(records):
    return [r for r in records if _path(r) != "/health"]


def count_levels(records):
    out = {}
    for r in _live(records):
        out[r["level"]] = out.get(r["level"], 0) + 1
    return out


def error_rate(records):
    r = _live(records)
    if not r:
        return 0.0
    return round(sum(x["status"] >= 400 for x in r) * 100 / len(r), 1)


def top_paths(records, n):
    c = {}
    for r in _live(records):
        c[_path(r)] = c.get(_path(r), 0) + 1
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def by_hour(records):
    hours = [r["hour"] for r in _live(records)]
    if not hours:
        return {}
    return {h: hours.count(h) for h in range(min(hours), max(hours) + 1)}


def slow_requests(records):
    return [r for r in _live(records) if r["ms"] > 300]


def summary(records):
    r = _live(records)
    return {"requests": len(r), "errors": sum(x["status"] >= 400 for x in r),
            "slow": len(slow_requests(records))}
