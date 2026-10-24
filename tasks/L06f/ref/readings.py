class Log:
    def __init__(self):
        self.data = {}

    def add(self, sensor, value):
        value = float(value)
        if value < -40:
            raise ValueError("impossible reading")
        if value > 50:
            return
        vals = self.data.setdefault(sensor.upper(), [])
        if vals and vals[-1] == value:
            return
        vals.append(value)

    def values(self, sensor):
        return list(self.data.get(sensor.upper(), []))

    def sensors(self):
        return sorted(s for s, v in self.data.items() if v)

    def count(self, sensor):
        return len(self.values(sensor))
