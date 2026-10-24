def write_report(s, path):
    codes = sorted(s.links, key=lambda c: (-s.stats(c), c))
    with open(path, "w", encoding="utf8") as f:
        f.write(f"Links: {len(codes)}\n")
        for c in codes:
            f.write(f"{c} | {s.stats(c)} clicks | {s.links[c][0]}\n")
