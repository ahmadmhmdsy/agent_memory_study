def low_stock(store, threshold):
    return sorted((s for s in store.skus() if store.qty(s) < threshold), key=lambda s: (store.qty(s), s))
