def parse_reading(s):
    s = s.strip()
    if s[-1] in "Ff":
        return (float(s[:-1]) - 32) * 5 / 9
    return float(s.rstrip("Cc"))


def fmt_temp(x):
    r = round(x, 1)
    if r == 0:
        r = 0.0
    return f"{r:.1f}°C"
