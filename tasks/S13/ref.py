from datetime import timezone


class Logger:
    def __init__(self):
        self.entries = []

    def count(self):
        return len(self.entries)

    def lines(self):
        return list(self.entries)

    def log(self, msg, now):
        ts = now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.entries.append(f"{ts} {msg}")
