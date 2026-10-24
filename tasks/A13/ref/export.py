"""Receipts and CSV export."""
import csv

from fees import subtotal, total


def receipt(orders, oid):
    rest, _, km, _ = orders.get(oid)
    return [f"restaurant: {rest}", f"km: {km}", f"subtotal: {subtotal(orders, oid)}",
            f"total: {total(orders, oid)}"]


def export_orders(orders, path):
    ids = sorted(orders.ids(), key=lambda k: (orders.get(k)[0], k))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "restaurant", "total"])
        for k in ids:
            w.writerow([k, orders.get(k)[0], total(orders, k)])
