from rates import fee


class Garage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cars = {}

    def enter(self, plate, t):
        if plate in self.cars:
            raise ValueError("already inside")
        if len(self.cars) >= self.capacity:
            raise ValueError("garage full")
        self.cars[plate] = t

    def inside(self):
        return sorted(self.cars)

    def free(self):
        return self.capacity - len(self.cars)

    def entry_time(self, plate):
        return self.cars[plate]

    def exit(self, plate, t):
        if plate not in self.cars:
            return None
        if t < self.cars[plate]:
            raise ValueError("exit before entry")
        return fee(t - self.cars.pop(plate))


def parked_before(garage, t):
    return sorted((p for p, e in garage.cars.items() if e < t), key=lambda p: (garage.cars[p], p))
