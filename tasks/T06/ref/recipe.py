"""Recipes."""


class Recipe:
    def __init__(self, servings=2):
        self.servings = servings
        self._g = {}

    def add(self, ingredient, grams):
        if grams <= 0:
            raise ValueError("grams must be positive")
        k = ingredient.lower()
        self._g[k] = self._g.get(k, 0) + grams

    def grams(self, ingredient):
        return self._g.get(ingredient.lower(), 0)

    def ingredients(self):
        return sorted(self._g)

    def remove(self, ingredient):
        self._g.pop(ingredient.lower(), None)


def scale(recipe, servings):
    if servings <= 0:
        raise ValueError("servings must be positive")
    r = Recipe(servings)
    for k, g in recipe._g.items():
        r._g[k] = max(1, round(g * servings / recipe.servings))
    return r
