def tracking_code(n):
    d = f"{n:06d}"
    return f"TR{d}{sum(int(c) for c in d) % 10}"


def write_label(n, country, grams, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(tracking_code(n) + "\n")
        f.write(f"To: {country.upper()}\n")
        f.write(f"Weight: {grams / 1000:g} kg\n")
