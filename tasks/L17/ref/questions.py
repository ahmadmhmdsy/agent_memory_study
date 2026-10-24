def parse_answer(s):
    s = s.strip().strip("()").upper()
    if s in ("1", "2", "3", "4"):
        s = "ABCD"[int(s) - 1]
    if s not in ("A", "B", "C", "D"):
        raise ValueError("answer must be A-D")
    return s
