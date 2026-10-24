"""Invoices and CSV export."""
import csv

from pricing import price


def invoice(stays, sid):
    pet, _, nights, _ = stays.get(sid)
    return [f"pet: {pet}", f"nights: {nights}", f"total: {price(stays, sid)}"]


def export_stays(stays, path):
    ids = sorted(stays.ids(), key=lambda k: (stays.get(k)[1], stays.get(k)[0]))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pet", "checkin", "nights"])
        for k in ids:
            pet, c, n, _ = stays.get(k)
            w.writerow([pet, c.isoformat(), n])
