def fine(due, returned):
    return min(max(0, (returned - due).days) * 50, 1000)
