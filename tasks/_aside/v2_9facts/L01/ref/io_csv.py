import csv


def export_stock(store, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["sku", "qty"])
        for s in store.skus():
            w.writerow([s, store.qty(s)])
        w.writerow(["total", sum(store.qty(s) for s in store.skus())])
