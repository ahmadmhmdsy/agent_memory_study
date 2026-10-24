def parse_bool(s):
    return s.strip().lower() in ("yes", "true", "1", "on")


def load(text):
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def get(cfg, key, default=None):
    for k, v in cfg.items():
        if k.lower() == key.lower():
            return v
    return default
