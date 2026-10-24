def hottest(log, n):
    sensors = log.sensors()
    if n > len(sensors):
        raise ValueError("n is larger than the number of sensors")
    return sorted(sensors, key=lambda s: -log.values(s)[-1])[:n]


def average(log, sensor):
    vals = log.values(sensor)[-5:]
    if not vals:
        return None
    return round(sum(vals) / len(vals), 2)


def spread(log, sensor):
    vals = log.values(sensor)
    return max(vals) - min(vals)
