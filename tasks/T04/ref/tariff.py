"""Parking prices."""

FREE = 15


def fee(minutes):
    if minutes <= FREE:
        return 0
    return min(1500, -(-minutes // 60) * 200)
