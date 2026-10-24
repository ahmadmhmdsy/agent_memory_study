def price(adult_cents, adults, children):
    child = adult_cents * 40 // 100
    return adults * adult_cents + children * child + 50 * (adults + children)
