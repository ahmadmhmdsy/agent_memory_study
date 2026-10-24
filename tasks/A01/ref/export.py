"""CSV exports."""
import csv

from stock import needs_reorder


def _write(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def export_stock(stock, path):
    _write(path, ["sku", "count"], [(k, stock.count(k)) for k in stock.skus()])


def export_orders(orders, path):
    rows = []
    for oid in orders.ids():
        sku, qty, day = orders.get(oid)
        rows.append((oid, sku, qty, day.strftime("%Y%m%d")))
    _write(path, ["id", "sku", "qty", "day"], rows)


def export_reorder(stock, path):
    _write(path, ["sku", "count"], [(k, stock.count(k)) for k in needs_reorder(stock)])
