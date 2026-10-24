"""Settings loader: `key = value` lines, `#` comments, blank lines ignored."""


def load(text):
    cfg = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        cfg[key.strip()] = value.strip()
    return cfg
