def zone(country):
    c = country.strip().upper()
    if len(c) != 2 or not c.isalpha():
        raise ValueError("bad country code")
    if c in ("KP", "IR"):
        raise ValueError("blocked country")
    if c == "NL":
        return 1
    return 2 if c in ("BE", "DE", "FR", "LU") else 3


def zone_name(country):
    return {1: "home", 2: "eu", 3: "world"}[zone(country)]
