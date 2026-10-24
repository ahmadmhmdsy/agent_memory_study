from stats import average


def summary(log, path):
    with open(path, "w", encoding="utf8") as f:
        for s in log.sensors():
            f.write(f"{s}: {average(log, s)}\n")
        f.write(f"sensors: {len(log.sensors())}\n")
