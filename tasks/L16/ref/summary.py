def write_summary(log, path):
    with open(path, "w", encoding="utf8") as f:
        for d in reversed(log.days()):
            for k, m, km in log.entries(d):
                f.write(f"{d.isoformat()} {k.title()}: {m} min\n")
        f.write(f"Total: {log.total()} min\n")
