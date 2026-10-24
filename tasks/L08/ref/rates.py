def fee(minutes):
    if minutes <= 30:
        return 0
    return min(-(-minutes // 60) * 250, 2000)
