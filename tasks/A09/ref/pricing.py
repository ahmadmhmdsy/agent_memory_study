"""Stay prices."""

DOG = 3200
CAT = 2400
LARGE_KG = 20
LARGE_PCT = 50
MEDS = 400


def nightly(pets, name):
    if pets.species(name) == "cat":
        return CAT
    if pets.kg(name) > LARGE_KG:
        return round(DOG * (100 + LARGE_PCT) / 100)
    return DOG


def price(stays, sid):
    pet, _, nights, meds = stays.get(sid)
    return nights * (nightly(stays.pets, pet) + (MEDS if meds else 0))


def revenue(stays):
    return sum(price(stays, k) for k in stays.ids())
