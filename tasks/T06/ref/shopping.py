"""Shopping lists."""


def shopping_list(recipes):
    out = {}
    for r in recipes:
        for k in r.ingredients():
            out[k] = out.get(k, 0) + r.grams(k)
    return out
