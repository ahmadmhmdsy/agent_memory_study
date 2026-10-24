def read_lines(path):
    with open(path) as f:
        return [l.rstrip("\r\n") for l in f if l.strip()]
