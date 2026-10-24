def parse_hm(s):
    s = s.strip().lower()
    suf = None
    if s[-2:] in ("am", "pm"):
        suf = s[-2:]
        s = s[:-2].strip()
    h, m = (int(x) for x in s.split(":"))
    if suf:
        h = h % 12 + (12 if suf == "pm" else 0)
    return h * 60 + m
