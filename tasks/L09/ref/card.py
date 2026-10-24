SMALL = {"and", "of", "with"}


def title(name):
    words = name.split()
    return " ".join(w.lower() if i and w.lower() in SMALL else w.capitalize() for i, w in enumerate(words))


def _num(q):
    return str(int(q)) if float(q).is_integer() else str(q)


def write_card(recipe, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(f"{title(recipe.name)} (serves {recipe.servings})\n")
        for n, q, u in recipe.items():
            f.write(f"{n}: {_num(q)} {u}\n")
