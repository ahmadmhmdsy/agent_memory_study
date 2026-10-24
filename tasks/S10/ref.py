def clamp(n, lo, hi):
    return max(lo, min(hi, n))


def count_pages(n_items, size):
    return -(-n_items // size)


def page(items, number, size):
    return list(items[number * size:(number + 1) * size])
