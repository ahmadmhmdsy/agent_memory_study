"""Boarding passes and CSV export."""
import csv


def boarding_pass(bookings, bid):
    _, name, _, seat = bookings.get(bid)
    return [name.upper(), f"seat: {seat}"]


def manifest(bookings, code):
    return sorted(bookings.get(b)[1] for b in bookings.of_flight(code))


def export_flight(bookings, code, path):
    ids = sorted(bookings.of_flight(code), key=lambda b: bookings.get(b)[1])
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seat", "name", "bags"])
        for b in ids:
            _, name, _, seat = bookings.get(b)
            w.writerow([seat, name, len(bookings.bags(b))])
