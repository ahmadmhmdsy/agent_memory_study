from text import clean_title
from timeutil import parse_ts


class Calendar:
    def __init__(self):
        self.items = []

    def add(self, title, start, end):
        title = clean_title(title)
        if not title:
            raise ValueError("empty title")
        eid = f"EVT-{len(self.items) + 1:05d}"
        self.items.append({"id": eid, "title": title, "start": start, "end": end})
        return eid

    def events(self):
        return sorted(self.items, key=lambda e: (parse_ts(e["start"]), e["title"]))

    def duration(self, event_id):
        e = next(e for e in self.items if e["id"] == event_id)
        return int((parse_ts(e["end"]) - parse_ts(e["start"])).total_seconds() // 60)
