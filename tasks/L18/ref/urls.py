def normalize(url):
    u = url.strip()
    if "://" not in u:
        u = "https://" + u
    scheme, rest = u.split("://", 1)
    scheme = scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError("only http and https")
    host, _, path = rest.partition("/")
    out = f"{scheme}://{host.lower()}"
    if path:
        out += "/" + path
    return out.rstrip("/")


def domain_of(url):
    host = normalize(url).split("://", 1)[1].split("/")[0]
    return host[4:] if host.startswith("www.") else host
