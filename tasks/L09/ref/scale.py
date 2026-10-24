from recipe import Recipe


def scale(recipe, servings):
    if servings < 1 or servings > 10 * recipe.servings:
        raise ValueError("bad servings")
    out = Recipe(recipe.name, servings)
    f = servings / recipe.servings
    for n, q, u in recipe.items():
        out.add(n, round(q * f * 4) / 4, u)
    return out
