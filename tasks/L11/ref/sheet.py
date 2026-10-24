DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Timesheet:
    def __init__(self):
        self.shifts = {}

    def log(self, worker, day, start, end):
        if end <= start:
            raise ValueError("shift must end after it starts")
        if end - start > 720:
            raise ValueError("shift longer than 12 hours")
        for d, a, b in self.shifts.get(worker, []):
            if d == day and start < b and a < end:
                raise ValueError("overlapping shift")
        self.shifts.setdefault(worker, []).append((day, start, end))

    def workers(self):
        return sorted(self.shifts)

    def minutes(self, worker):
        t = 0
        for _, a, b in self.shifts.get(worker, []):
            m = b - a
            t += m - 30 if m > 360 else m
        return t

    def shift_count(self, worker):
        return len(self.shifts.get(worker, []))


def worker_days(sheet, worker):
    ds = {d for d, _, _ in sheet.shifts.get(worker, [])}
    return [d for d in DAYS if d in ds]
