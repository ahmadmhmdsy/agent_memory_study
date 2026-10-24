from zones import zone

BASE = {1: 500, 2: 900, 3: 1500}


def vol_weight(l, w, h):
    return -(-(l * w * h) // 4)


def cost(country, grams, dims=None):
    if not 0 < grams <= 30000:
        raise ValueError("bad weight")
    z = zone(country)
    charged = max(grams, vol_weight(*dims)) if dims else grams
    per = 150 * (2 if z == 3 else 1)
    return BASE[z] + per * -(-charged // 1000)
