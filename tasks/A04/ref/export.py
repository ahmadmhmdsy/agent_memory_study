"""Agenda and CSV export."""
import csv


def hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def agenda(schedule, day):
    out = []
    for a in schedule.day(day):
        pid, _, start, kind = schedule.get(a)
        out.append(f"{hhmm(start)} {schedule.patients.name(pid)} ({kind})")
    return out


def export_day(schedule, day, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start", "patient", "kind"])
        for a in schedule.day(day):
            pid, _, start, kind = schedule.get(a)
            w.writerow([hhmm(start), schedule.patients.name(pid), kind])
