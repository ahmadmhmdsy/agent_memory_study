"""Watering schedule."""


def next_day(garden, plant):
    return garden.last(plant) + garden.every[plant]


def due(garden, day):
    rows = [(day - next_day(garden, p), p) for p in garden.plants() if next_day(garden, p) <= day]
    return [p for _, p in sorted(rows, key=lambda r: (-r[0], r[1]))]
