"""Settling up."""


def summary(trip):
    return [f"{p}: {trip.balance(p)}" for p in trip.people() if trip.balance(p) != 0]
